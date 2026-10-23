# Enlaces oficiales de reclamación: verificación del 23-10-2026

Comprobados abriendo cada página en un navegador real. Además de que la página cargue, se ha comprobado que trate de reclamaciones o derechos del pasajero y no sea la portada de la aerolínea.

Desde el servidor de trabajo (`curl`), las tres webs fallan por las restricciones de red de ese entorno, no por las webs. Por eso no se usó como comprobación.

## Aerolíneas revisadas

| Aerolínea | Antes | Ahora | Resultado |
| --- | --- | --- | --- |
| Air France (ES) | `wwws.airfrance.es/en/information/legal/remboursement` (en inglés) | `wwws.airfrance.es/information/legal/remboursement` | Versión en español de la misma página, «Reembolso, vale y compensación». Lleva a «Presentar una solicitud» (`/contact/topic/refund-compensation`) y a «Derechos de los pasajeros» (Reglamento 261/2004) |
| Air France (EN) | `wwws.airfrance.es/en/information/legal/remboursement` | Sin cambios | Carga «Refunds, vouchers, and compensation», con el mismo contenido |
| Binter (ES) | `www.binter.com/es` (portada) | `www.bintercanarias.com/es/informacion/derechos-del-pasajero` | **Enlace roto corregido.** `binter.com` no cargó en el navegador (dos intentos, 50 s cada uno). La web oficial es `bintercanarias.com`, y esta página explica el Reglamento 261/2004. El formulario de reclamaciones (`/es/formulario-contacto`) se indica en la nota |
| Binter (EN) | `www.binter.com/es` | `www.bintercanarias.com/en/information/passengers-rights` | Versión inglesa de la misma página, sacada de sus etiquetas `hreflang` |
| World2fly | `www.world2fly.com/` (portada) | `www.w2fly.es/es-es/contacto/centro-de-atencion` | **Enlace roto corregido.** `world2fly.com` no carga (el navegador rechaza la navegación y `curl` da un error TLS). La web actual es `w2fly.es`: sus condiciones de transporte identifican a World2Fly S.L.U. (CIF B16668451, Palma). El centro de atención tiene el apartado «Reclamaciones sobre servicios» con formulario. No hemos encontrado versión en inglés |

## Enlaces actualizados recientemente (commit 64a315f)

| Aerolínea | Enlace | Resultado |
| --- | --- | --- |
| Vueling (ES y EN) | `help.vueling.com/hc/es/articles/24476547783569-Retraso-en-mi-vuelo` y `/hc/en-gb/...-Delay-in-my-flight` | Correctos: «Retraso en mi vuelo» y «Delay in my flight», dentro de «Incidencias en tu vuelo» |
| TUI | `tui.co.uk/.../how-do-i-claim-my-flight-delay-compensation` | Correcto: «How do I claim my flight delay compensation?» |
| Pegasus | `flypgs.com/en/useful-info/other-info/passenger-rights` | Correcto: «Passenger Rights», basado en el Reglamento 261/2004 |
| Turkish Airlines | `turkishairlines.com/en-int/legal-notice/passenger-rights/` | Correcto: la página carga con el título «Passenger Rights \| Legal Notice». El texto lo tapa el aviso de cookies, así que solo se comprobó el título |

## Pendiente, fuera de esta tarea

- **Iberia Express** sigue enlazando a su portada (`iberiaexpress.com/`). No se ha cambiado porque no se ha verificado una página concreta de reclamaciones. Candidata: «Solicitudes Online», en `/informacion-general/informacion-pasajero/antes-de-volar/solicitudes-online`.
- `eu261expenseclaim.ryanair.com` es un subdominio dedicado a reclamaciones, no una portada.
