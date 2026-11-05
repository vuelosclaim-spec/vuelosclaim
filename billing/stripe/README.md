# Stripe para VuelosClaim Partners — preparación sin cobros

**No desplegado ni conectado a la web pública.** `STRIPE_BILLING_ENABLED` está desactivado por defecto.

La web actual es GitHub Pages: no puede recibir webhooks ni custodiar `sk_test_`/`sk_live_`. Este módulo contiene únicamente funciones de servidor y pruebas, para integrarlas posteriormente en un backend HTTPS con almacenamiento transaccional.

## Configuración futura (solo entorno de prueba)

Variables privadas del backend, **nunca en Git ni en `docs/`**:

- `STRIPE_BILLING_ENABLED=true` únicamente en el backend de pruebas.
- `STRIPE_SECRET_KEY=sk_test_...` (el módulo rechaza claves `sk_live_`).
- `STRIPE_PRICE_PRO=price_...` y `STRIPE_PRICE_PREMIUM=price_...` creados en Stripe test mode.
- `STRIPE_APPROVED_PARTNERS=...` para socios autorizados en la prueba, no entrada libre de formularios.
- `STRIPE_WEBHOOK_SECRET=whsec_...` para el listener HTTPS del backend (no implementado aún).

`node --test billing/stripe/stripe.test.mjs`

## Flujo previsto

1. El socio solicita el piloto; se valida su empresa y se crea un `partner_id` único en el registro.
2. Un backend autenticado consulta ese socio autorizado, genera y **persiste un `requestId` único de 16–80 caracteres** por intención de compra, y lo reutiliza en cualquier reintento. Crea una sesión de Stripe Checkout con `mode=subscription`, pasando ese `requestId` a `createTestCheckout`, con precio definido en el servidor. La web nunca decide el importe ni genera el identificador de idempotencia.
3. Stripe confirma por **webhook firmado**, recibido en HTTPS y comprobado con el cuerpo crudo. El ID del evento se guarda de forma única para evitar aplicar duplicados. Deben reconciliarse `customer`, `subscription`, precio, estado e invoice con Stripe antes de otorgar o retirar acceso.
4. Un almacenamiento persistente relaciona socio, suscripción, pago y estado. Nunca conceder acceso por un `success_url` ni por un evento sin reconciliar.
5. El portal de clientes para cancelaciones y métodos de pago se añadirá al backend con autenticación/autorización por socio. No hay portal todavía.

## Pasos obligatorios antes de cobrar

- Conectar Stripe empresarial, revisar identidad fiscal y condiciones legales.
- Elegir alojamiento HTTPS con base de datos, copias de seguridad y autenticación de administradores/socios.
- Implementar rutas HTTP con límites de tamaño, rate limits, sesiones y protección contra CSRF, almacenamiento de `requestId` persistente y eventos idempotentes, y proceso de conciliación.
- Probar pagos, renovaciones, fallos, cancelaciones, reintentos, reembolsos y acceso con Stripe test mode.
- Revisar los precios con/sin IVA, facturación, soporte, derecho de cancelación y textos comerciales.
- Revisar y autorizar por separado el despliegue y el paso a modo real. **No bastará con cambiar una variable: el módulo rechaza claves de producción.**

No se han creado botones ni enlaces de pago en `docs/`. El motor jurídico, el widget y la afiliación permanecen intactos.
