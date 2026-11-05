/** Stripe subscription primitives. NOT deployed or connected to the public site.
 * Only test keys are accepted. Do not use a success redirect as proof of payment.
 */
import { createHmac, timingSafeEqual } from 'node:crypto';

const API = 'https://api.stripe.com/v1';
const PRICE_RE = /^price_[A-Za-z0-9]+$/;
const EVENT_TYPES = new Set([
  'checkout.session.completed', 'invoice.paid', 'invoice.payment_failed',
  'customer.subscription.updated', 'customer.subscription.deleted',
]);

export function configuration(env = process.env) {
  if (env.STRIPE_BILLING_ENABLED !== 'true') throw new Error('billing-disabled');
  if (!/^sk_test_[A-Za-z0-9]+$/.test(env.STRIPE_SECRET_KEY || '')) throw new Error('test-key-required');
  const prices = { pro: env.STRIPE_PRICE_PRO, premium: env.STRIPE_PRICE_PREMIUM };
  if (!Object.values(prices).every(p => PRICE_RE.test(p || '')) || prices.pro === prices.premium) {
    throw new Error('invalid-test-price-ids');
  }
  return { secret: env.STRIPE_SECRET_KEY, prices };
}

export async function createTestCheckout({ plan, partnerId, requestId, successUrl, cancelUrl }, env = process.env, fetchImpl = fetch) {
  const { secret, prices } = configuration(env);
  if (!Object.hasOwn(prices, plan)) throw new Error('unknown-plan');
  // Only an approved partner ID from a private onboarding process may be used.
  if (!/^[a-z0-9](?:[a-z0-9-]{0,30}[a-z0-9])?$/.test(partnerId || '')) throw new Error('invalid-partner');
  const approved = (env.STRIPE_APPROVED_PARTNERS || '').split(',').map(s => s.trim());
  if (!approved.includes(partnerId)) throw new Error('partner-not-approved');
  // The authenticated backend must persist this ID and reuse it on retries.
  if (!/^[A-Za-z0-9_-]{16,80}$/.test(requestId || '')) throw new Error('invalid-request-id');
  for (const url of [successUrl, cancelUrl]) {
    const parsed = new URL(url);
    if (parsed.protocol !== 'https:' || parsed.origin !== 'https://vuelosclaim.eu' || parsed.username || parsed.password) {
      throw new Error('invalid-return-url');
    }
  }
  const body = new URLSearchParams({
    mode: 'subscription', 'line_items[0][price]': prices[plan], 'line_items[0][quantity]': '1',
    success_url: successUrl, cancel_url: cancelUrl,
    client_reference_id: partnerId,
    'metadata[partner_id]': partnerId, 'metadata[plan]': plan,
    'subscription_data[metadata][partner_id]': partnerId,
  });
  const response = await fetchImpl(`${API}/checkout/sessions`, {
    method: 'POST', headers: {
      Authorization: `Bearer ${secret}`, 'Content-Type': 'application/x-www-form-urlencoded',
      'Idempotency-Key': `pilot-${partnerId}-${plan}-${requestId}`,
    }, body: body.toString(),
  });
  const data = await response.json();
  if (!response.ok || data.mode !== 'subscription' || !/^https:\/\/checkout\.stripe\.com\//.test(data.url || '')) {
    throw new Error('stripe-checkout-failed');
  }
  return { id: data.id, url: data.url }; // Never return the Stripe secret.
}

/** Verify Stripe's signature against the *raw* request body; reject replayed timestamps. */
export function verifyWebhook(rawBody, header, secret, nowSeconds = Math.floor(Date.now() / 1000)) {
  if (!Buffer.isBuffer(rawBody) || rawBody.length > 1024 * 1024 || !/^whsec_[^\s]+$/.test(secret || '')) {
    throw new Error('invalid-webhook-input');
  }
  const parts = (header || '').split(',').map(s => s.trim());
  const timestamp = parts.find(s => s.startsWith('t='))?.slice(2);
  const signatures = parts.filter(s => s.startsWith('v1=')).map(s => s.slice(3));
  if (!/^\d{10}$/.test(timestamp || '') || Math.abs(nowSeconds - Number(timestamp)) > 300) {
    throw new Error('webhook-timestamp-invalid');
  }
  const expected = createHmac('sha256', secret).update(`${timestamp}.`).update(rawBody).digest();
  const match = signatures.some(sig => {
    if (!/^[a-f0-9]{64}$/i.test(sig)) return false;
    return timingSafeEqual(expected, Buffer.from(sig, 'hex'));
  });
  if (!match) throw new Error('webhook-signature-invalid');
  let event;
  try { event = JSON.parse(rawBody.toString('utf8')); }
  catch { throw new Error('invalid-event'); }
  if (!event || typeof event !== 'object' || typeof event.id !== 'string' || !/^evt_[A-Za-z0-9]+$/.test(event.id)) throw new Error('invalid-event');
  // These are notifications to reconcile against Stripe and a durable database,
  // NOT authorizations to activate a license from the browser or this module.
  return { eventId: event.id, type: EVENT_TYPES.has(event.type) ? event.type : 'ignored',
    objectId: typeof event.data?.object?.id === 'string' ? event.data.object.id : null };
}
