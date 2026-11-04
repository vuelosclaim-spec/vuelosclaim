import test from 'node:test';
import assert from 'node:assert/strict';
import { createHmac } from 'node:crypto';
import { configuration, createTestCheckout, verifyWebhook } from './stripe.mjs';

const env = { STRIPE_BILLING_ENABLED: 'true', STRIPE_SECRET_KEY: 'sk_test_mockonly',
  STRIPE_PRICE_PRO: 'price_ProTest', STRIPE_PRICE_PREMIUM: 'price_PremiumTest',
  STRIPE_APPROVED_PARTNERS: 'agency-one' };
test('disabled by default and live keys forbidden', () => {
  assert.throws(() => configuration({}), /billing-disabled/);
  assert.throws(() => configuration({ ...env, STRIPE_SECRET_KEY: 'sk_live_secret' }), /test-key-required/);
});
test('checkout cannot be created for unapproved agencies or unsafe URLs', async () => {
  const args = { plan: 'pro', partnerId: 'unknown', successUrl: 'https://vuelosclaim.eu/partners/', cancelUrl: 'https://vuelosclaim.eu/partners/' };
  await assert.rejects(createTestCheckout(args, env), /partner-not-approved/);
  await assert.rejects(createTestCheckout({ ...args, partnerId: 'agency-one', successUrl: 'https://evil.test/' }, env), /invalid-return-url/);
});
test('test checkout sends server-side price and fixed subscription mode', async () => {
  let called = false;
  const args = { plan: 'pro', partnerId: 'agency-one', successUrl: 'https://vuelosclaim.eu/partners/', cancelUrl: 'https://vuelosclaim.eu/partners/' };
  const result = await createTestCheckout(args, env, async (url, options) => {
    called = true;
    assert.equal(url, 'https://api.stripe.com/v1/checkout/sessions');
    assert.equal(new URLSearchParams(options.body).get('mode'), 'subscription');
    assert.equal(new URLSearchParams(options.body).get('line_items[0][price]'), 'price_ProTest');
    return { ok: true, json: async () => ({ id: 'cs_test_mock', mode: 'subscription', url: 'https://checkout.stripe.com/c/mock' }) };
  });
  assert.ok(called);
  assert.equal(result.id, 'cs_test_mock');
});
test('webhook rejects tampering and old timestamps', () => {
  const raw = Buffer.from(JSON.stringify({ id: 'evt_123', type: 'invoice.paid', data: { object: { id: 'in_123' } } }));
  const ts = 1790000000;
  const sig = createHmac('sha256', 'whsec_mock').update(`${ts}.`).update(raw).digest('hex');
  assert.equal(verifyWebhook(raw, `t=${ts},v1=${sig}`, 'whsec_mock', ts).type, 'invoice.paid');
  assert.throws(() => verifyWebhook(raw, `t=${ts},v1=${sig}`, 'whsec_mock', ts + 301), /timestamp/);
  assert.throws(() => verifyWebhook(Buffer.from('{}'), `t=${ts},v1=${sig}`, 'whsec_mock', ts), /signature/);
});
