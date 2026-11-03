# VuelosClaim Partners — lanzamiento y coordinación

Estado: piloto; aún no hay suscripciones ni marca blanca. Coordinación con Claude Code: https://github.com/vuelosclaim-spec/vuelosclaim/issues/34

## Precios propuestos (IVA no incluido)
- Gratis: 0 €, widget estándar ya existente y atribuible.
- Pro: 9,90 €/mes, propuesta futura de logo/colores e integración asistida.
- Premium: 19,90 €/mes, propuesta futura de estadísticas agregadas y soporte.

## Trabajo pendiente propuesto para Claude Code
1. Revisar la PR de landing enlazada desde el issue #34. No sobrescribir cambios de ChatGPT.
2. Widget real personalizable, con identificador de cliente validado, valores de marca seguros y aviso visible de atribución y afiliación; no aceptar HTML/CSS arbitrarios.
3. Estadísticas agregadas con consentimiento y segregación por cliente; no exponer identificadores privados ni respuestas personales.
4. Prueba de integración en navegador móvil, teclado y consentimiento en terceros sitios.
5. Cobros recurrentes, facturación y gestión de cancelaciones solamente cuando el propietario conecte la pasarela y valide condiciones comerciales.

## Captación comercial
Identificar 15 agencias de viajes pequeñas y 15 blogs públicos con nombre, URL, necesidad real y canal autorizado. No inventar datos ni recopilar contactos privados. Validar tres pilotos y si alguien acepta contratar antes de desarrollar un panel complejo.
En España, un correo público no autoriza por sí mismo el envío de publicidad electrónica: respetar LSSI-CE/RGPD. No enviar mensajes masivos sin consentimiento o base jurídica adecuada. Medir enlaces públicos con UTM sin incluir datos personales.

## Mensaje orientativo personalizado (sin enviar automáticamente)
Asunto: Calculadora gratuita de derechos de pasajeros para [web]

Hola, he visto vuestra sección de [sección real]. Tenemos una calculadora gratuita que puede ayudar a los visitantes a orientarse sobre posibles compensaciones por retrasos, cancelaciones y overbooking.
Se puede insertar en vuestra web sin coste, con mención a VuelosClaim. Si os interesa la demostración, puedo facilitar el código. Estamos estudiando una versión futura con vuestra marca, todavía sin suscripción activa.

Un saludo, equipo VuelosClaim
## Widget con marca (hito 1, Claude Code)
- Alta de un socio: añadir una entrada en `fuente/partners_registry.py`, con id, nombre en texto plano, color `#rrggbb` e idioma `es` o `en`. El logo es opcional y va en `fuente/partners_logos/`, en PNG, SVG o WebP de hasta 100 KB, revisado antes de subirlo. Después se ejecuta `python3 fuente/build.py`.
- Resultado: `https://vuelosclaim.eu/widget/p/<id>/`, una página `noindex` que queda fuera del sitemap. Código para el socio: el mismo iframe del widget gratuito, cambiando `/widget/` por `/widget/p/<id>/`.
- La marca solo sale del registro. La web anfitriona no puede cambiarla con parámetros, HTML ni CSS. La atribución a VuelosClaim y el aviso de afiliación son siempre visibles.
- El color se ajusta solo para mantener un contraste AA (4,5:1) en modo claro y oscuro.
- `?aff=` funciona igual que en el widget gratuito. Motor, consentimiento y GA4 sin cambios.
- Pendiente para el siguiente hito: estadísticas por socio con consentimiento. `window.CTT.partner` ya lleva el id para usarlo sin datos personales.
- Pruebas: `fuente/tests/test_partners_widget.py` (registro, contraste y páginas) y `fuente/tests/test_widget_partners.js` (Playwright, con el widget incrustado en una web de otro origen, en escritorio y móvil).
