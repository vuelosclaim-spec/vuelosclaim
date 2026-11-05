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
  await assert.rejects(createTestCheckout({ ...args, partnerId: 'agency-one', requestId: 'request_1234567890', successUrl: 'https://evil.test/' }, env), /invalid-return-url/);
});
test('test checkout sends server-side price and fixed subscription mode', async () => {
  let called = false;
  const args = { plan: 'pro', partnerId: 'agency-one', requestId: 'request_1234567890', successUrl: 'https://vuelosclaim.eu/partners/', cancelUrl: 'https://vuelosclaim.eu/partners/' };
  const result = await createTestCheckout(args, env, async (url, options) => {
    called = true;
    assert.equal(url, 'https://api.stripe.com/v1/checkout/sessions');
    assert.equal(new URLSearchParams(options.body).get('mode'), 'subscription');
    assert.equal(options.headers['Idempotency-Key'], 'pilot-agency-one-pro-request_1234567890');
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

test('stable idempotency key is required on retries', async () => {
  const args = { plan: 'pro', partnerId: 'agency-one', requestId: 'request_1234567890',
    successUrl: 'https://vuelosclaim.eu/partners/', cancelUrl: 'https://vuelosclaim.eu/partners/' };
  await assert.rejects(createTestCheckout({ ...args, requestId: undefined }, env), /invalid-request-id/);
  const keys = [];
  const mock = async (_, options) => {
    keys.push(options.headers['Idempotency-Key']);
    return { ok: true, json: async () => ({ id: 'cs_test_mock', mode: 'subscription', url: 'https://checkout.stripe.com/c/mock' }) };
  };
  await createTestCheckout(args, env, mock);
  await createTestCheckout(args, env, mock);
  assert.equal(keys.length, 2);
  assert.equal(keys[0], keys[1]);
});

test('webhook signature alternatives, invalid JSON, unknown events', () => {
  const ts = 1790000000, secret = 'whsec_mock';
  function signed(raw) {
    return createHmac('sha256', secret).update(`${ts}.`).update(raw).digest('hex');
  }
  const raw = Buffer.from(JSON.stringify({ id: 'evt_567', type: 'unrelated.event', data: { object: { id: 'x_1' } } }));
  const good = signed(raw);
  assert.throws(() => verifyWebhook(raw, `t=${ts},v1=${good}`, 'whsec_other', ts), /signature/);
  assert.throws(() => verifyWebhook(raw, `t=${ts}`, secret, ts), /signature/);
  assert.equal(verifyWebhook(raw, `t=${ts},v1=${'0'.repeat(64)},v1=${good}`, secret, ts).type, 'ignored');
  const malformed = Buffer.from('{bad-json');
  assert.throws(() => verifyWebhook(malformed, `t=${ts},v1=${signed(malformed)}`, secret, ts), /invalid-event/);
});
