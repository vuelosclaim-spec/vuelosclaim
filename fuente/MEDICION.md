# Medición con Google Analytics 4 (G-6JRCZVTNDG)

## Consentimiento

- Antes de que el visitante acepte, la página solo define los valores de consentimiento denegados. No se carga `gtag.js` ni el script de Travelpayouts, y no sale ninguna petición hacia Google Analytics ni Travelpayouts.
  - Antes de este cambio, `gtag.js` se cargaba sin consentimiento y enviaba una petición `collect` con `gcs=G100`. El script de Travelpayouts cargaba unos 15 archivos. Comprobado en producción el 22-10-2026.
- **Al aceptar:** se cargan Analytics, sin señales de Google ni personalización de anuncios, y Travelpayouts. Se envía la página vista.
- **Al rechazar,** o al retirar el consentimiento desde el enlace «Cookies» del pie: se desactiva Analytics (`ga-disable-G-6JRCZVTNDG`), se borran las cookies `_ga*` y no se envían más eventos. La elección se guarda en el navegador (`vc_consent`).
- **AdSense** no depende de este banner. Su consentimiento lo gestiona el mensaje de Google (Privacidad y mensajes de AdSense), que hay que activar cuando se apruebe la cuenta.

## Eventos

No había eventos personalizados antes de este cambio, así que no hay duplicados.

| Evento | Cuándo | Parámetros |
| --- | --- | --- |
| `calculator_started` | Primera interacción con la calculadora tras aceptar, una vez por página | `incident_type` |
| `calculator_completed` | Cada resultado distinto, cuando el visitante deja de cambiar respuestas durante 1,2 s. El ejemplo precargado no cuenta | `incident_type`, `result`, `compensation_category`, `regime` |
| `compensation_possible` | Con `calculator_completed`, si el resultado es «Posible derecho» | ídem |
| `compensation_not_eligible` | Con `calculator_completed`, si el resultado es «No parece corresponder» | ídem |
| `compensation_insufficient_data` | Con `calculator_completed`, si faltan datos | ídem |
| `affiliate_click` | Clic en cualquier enlace `rel="sponsored"` (botón de la calculadora o comparativa) | `affiliate_id` (`airhelp_tp`…), `placement` (`calculator` / `content`) y el último resultado si lo hay |
| `letter_opened` | Abrir el generador de carta | resultado |
| `letter_copied` | Copiar la carta con éxito | resultado |
| `letter_downloaded` | Descargar la carta | resultado |

Todos los eventos llevan `site_language` y `source_page`. No se usan `language` ni `page_path` porque GA4 los reserva: sobrescribirían el idioma del navegador y la ruta de la página. Los valores salen de listas cerradas:

- `incident_type`: delay / cancel / denied.
- `result`: posible / no / insuficiente.
- `compensation_category`: p. ej. `250_EUR`, `350_GBP` o `none`.
- `regime`: EU / UK / none.

El código descarta cualquier otro parámetro. Nunca se envía lo que escribe el usuario (nombre, reserva, vuelo, fecha). Lo comprueba `tests/test_navegador.js`.

## Configuración pendiente en Google Analytics (Administrar)

1. **Definiciones personalizadas → Crear dimensiones personalizadas** (ámbito de evento): `incident_type`, `result`, `compensation_category`, `regime`, `affiliate_id`, `placement`, `site_language`, `source_page`.
2. **Eventos → marcar `affiliate_click` como evento clave.** Opcional: también `letter_downloaded`.
3. **Flujos de datos → Medición mejorada:** los «Clics salientes» registran también el clic en AirHelp como evento `click`. No duplica `affiliate_click`, pero para contar conversiones usa `affiliate_click`.
4. **Flujos de datos → Medición mejorada → Interacciones con formularios:** recomendable desactivarla. Envía `form_start` con la URL de la página y el identificador del primer campo; no son datos personales, pero duplican `calculator_started`.
5. **Explorar → Exploración de embudo**, con estos pasos:
   1. `page_view`
   2. `calculator_started`
   3. `calculator_completed`
   4. `compensation_possible`
   5. `affiliate_click`

## Límites

- Solo se mide a quien acepta las cookies: las cifras de GA4 son una muestra, no el total de visitantes.
- El clic en AirHelp no equivale a una reclamación contratada: las conversiones reales están en el panel de Travelpayouts.
