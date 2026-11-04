# VuelosClaim Partners — lanzamiento y coordinación

Estado: piloto; hay widget con marca y eventos agregados con consentimiento, pero no panel privado, alta autoservicio ni suscripciones activas. Coordinación con Claude Code: https://github.com/vuelosclaim-spec/vuelosclaim/issues/34

## Precios propuestos (IVA no incluido)
- Gratis: 0 €, widget estándar ya existente y atribuible.
- Pro: 9,90 €/mes, precio objetivo futuro; el widget con logo/colores y la integración asistida ya se pueden probar.
- Premium: 19,90 €/mes, precio objetivo futuro; se pueden preparar informes agregados de GA4, pero aún no existe panel privado ni soporte prioritario contratado.

## Pendientes reales antes de aceptar suscripciones
1. Configurar la dimensión de evento `partner_id` en GA4 y comprobar datos consentidos de un piloto de prueba.
2. Probar una alta completa mediante `alta_socio.py`, PR, CI, publicación y código iframe entregado al socio.
3. Aprobar condiciones comerciales, prestación de soporte, cancelación, facturación e impuestos; elegir pasarela y configurar cobros cuando el propietario lo decida.
4. Revisar con el socio la responsabilidad por avisos legales, afiliación y consentimiento de su propia web.
5. No prometer un panel privado ni habilitar cobros hasta que existan y se hayan probado.

## Procedimiento para un piloto (sin cobro)
1. Recibir solicitud voluntaria del interesado en `vuelosclaim@gmail.com` con URL de su web y objetivo de integración.
2. Confirmar por escrito que es una prueba sin cuota, sin garantía de indemnizaciones ni de resultados de afiliación, y que la atribución a VuelosClaim queda visible.
3. Solicitar nombre comercial, color principal `#rrggbb`, idioma ES/EN y, opcionalmente, logo PNG/WebP de hasta 100 KB. No solicitar datos de pasajeros.
4. Ejecutar `python3 fuente/alta_socio.py --nombre "Agencia Piloto" --color "#1f4e8c" --idioma es --logo ruta.png --compilar` (omitir `--logo` si no hay), abrir PR, revisar los cambios y esperar CI verde antes de fusionar.
5. Verificar la página `/widget/p/<id>/` publicada, su comportamiento incrustado en móvil, consentimiento y aviso de afiliación. Enviar únicamente entonces el iframe al interesado.
6. Registrar fecha de alta, web, modalidad de prueba, incidencia técnica y próxima revisión en un registro interno privado; no subir correos ni datos personales a GitHub.
7. Tras dos semanas, preguntar si la herramienta le aporta valor y qué funciones justificarían 9,90 o 19,90 €/mes. No inferir ventas de los clics de afiliación.

## Captación comercial
Identificar 15 agencias de viajes pequeñas y 15 blogs públicos con nombre, URL, necesidad real y canal autorizado. No inventar datos ni recopilar contactos privados. Validar tres pilotos y si alguien acepta contratar antes de desarrollar un panel complejo.
En España, un correo público no autoriza por sí mismo el envío de publicidad electrónica: respetar LSSI-CE/RGPD. No enviar mensajes masivos sin consentimiento o base jurídica adecuada. Medir enlaces públicos con UTM sin incluir datos personales.

## Mensaje orientativo personalizado (sin enviar automáticamente)
Asunto: Calculadora gratuita de derechos de pasajeros para [web]

Hola, he visto vuestra sección de [sección real]. Tenemos una calculadora gratuita que puede ayudar a los visitantes a orientarse sobre posibles compensaciones por retrasos, cancelaciones y overbooking.
Se puede insertar en vuestra web sin coste, con mención a VuelosClaim. Si os interesa la demostración, puedo facilitar el código. Estamos estudiando una versión futura con vuestra marca, todavía sin suscripción activa.

Un saludo, equipo VuelosClaim
## Widget con marca (hito 1, Claude Code)
- Alta de un socio con un solo comando, sin editar archivos a mano:
  `python3 fuente/alta_socio.py --nombre "Viajes Sol" --color "#c0392b" [--acento "#f1c232"] [--idioma es|en] [--logo ruta.png] [--compilar]`
  - El id se crea a partir del nombre (o se elige con `--id`).
  - Logo: solo PNG o WebP de hasta 100 KB, con comprobación del formato real al darlo de alta y otra vez al compilar. No se admite SVG porque puede llevar contenido activo; si la agencia solo tiene SVG, se convierte antes a PNG. Se guarda como `fuente/partners_logos/<id>.<ext>`.
  - La entrada se valida con las mismas reglas del registro y se guarda en `fuente/partners.json`. Si falla la validación o el guardado, se retira el logo recién copiado y no se cambia nada. Nunca se sobrescribe un archivo existente.
  - El comando imprime el código de inserción para la agencia.
  - Otras opciones: `--listar` muestra las agencias y `--baja <id>` da de baja una (se puede recuperar desde git).
  - Después: abrir una PR con CI en verde antes de publicar.
- Resultado: `https://vuelosclaim.eu/widget/p/<id>/`, una página `noindex` que queda fuera del sitemap. Código para el socio: el mismo iframe del widget gratuito, cambiando `/widget/` por `/widget/p/<id>/`.
- La marca solo sale del registro. La web anfitriona no puede cambiarla con parámetros, HTML ni CSS. La atribución a VuelosClaim y el aviso de afiliación son siempre visibles.
- El color se ajusta solo para mantener un contraste AA (4,5:1) en modo claro y oscuro.
- `?aff=` funciona igual que en el widget gratuito. Motor, consentimiento y GA4 sin cambios.
- Pendiente para el siguiente hito: estadísticas por socio con consentimiento. `window.CTT.partner` ya lleva el id para usarlo sin datos personales.
- Pruebas: `fuente/tests/test_partners_widget.py` (registro, contraste y páginas) y `fuente/tests/test_widget_partners.js` (Playwright, con el widget incrustado en una web de otro origen, en escritorio y móvil).
