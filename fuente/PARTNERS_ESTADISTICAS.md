# VuelosClaim Partners — estadísticas por agencia

Medición del widget con marca (`/widget/p/<id>/`) en Google Analytics 4 (propiedad ya existente). Solo se mide a quien **acepta las cookies de análisis** en el aviso del propio widget. El aviso de consentimiento no se ha modificado.

## Eventos (una vez por carga de página, salvo los clics)
| Evento | Cuándo | Para |
|---|---|---|
| `widget_view` | Al cargar el widget con consentimiento, o en la primera interacción si el visitante acepta después | Visitas a cada widget |
| `widget_start` | Primer clic, tecla o respuesta dentro de la calculadora | Usuarios que empiezan |
| `widget_result` | La primera vez que se muestra el resultado (ir y volver no cuenta dos veces) | Usuarios que terminan |
| `affiliate_click` | Cada clic en un botón de reclamación (enlace `sponsored`) | Clics en reclamar |

Los eventos que ya existían (`calculator_started`, `wizard_step_viewed`, `calculator_completed`…) también llevan `partner_id` dentro del widget de socio.

## Parámetros
- `partner_id`: id del registro (`fuente/partners_registry.py`). Se valida en el navegador con el mismo patrón que en el registro.
- `site_language` y `source_page` (`/widget/p/<id>/`, sin parámetros).
- Solo en `affiliate_click`: `affiliate_id` y `placement`. En `wizard_step_viewed`: `wizard_step`.
- **No se envía nada derivado de las respuestas:** ni tipo de incidencia, ni resultado, ni importe, ni régimen, ni ruta, ni aerolínea, ni datos de la carta. En la web principal y en `/widget/` la medición sigue exactamente igual que antes.

## Tasa de conversión por agencia (en GA4)
1. Una sola vez: en *Administrar → Definiciones personalizadas*, crear la dimensión de evento `partner_id`. Solo cuenta desde el día en que se crea.
2. En *Explorar → Exploración libre*: dimensiones `partner_id` y `Nombre del evento`; métrica `Número de eventos`; filtro: el nombre del evento empieza por `widget_` o es `affiliate_click`.
3. Fórmulas:
   - Inicio = `widget_start / widget_view`
   - Finalización = `widget_result / widget_start`
   - Clics por carga = `affiliate_click / widget_view` (puede superar el 100 % si una persona hace varios clics; **no** es una tasa de usuarios convertidos)

No existe todavía un panel privado para las agencias. Los informes se preparan desde GA4.

Para medir una tasa de cargas con al menos un clic, se necesitaría un evento adicional único por carga, sin identificadores personales. No debe presentarse el cociente actual como ventas ni reclamaciones completadas.

## Limitaciones conocidas
- Solo cuenta a los visitantes que aceptan cookies, así que las cifras son un mínimo.
- El widget va dentro de un iframe en la web de la agencia. Los navegadores que bloquean cookies de terceros (Safari y Firefox; Chrome según la configuración) pueden contar al mismo visitante como nuevo en cada visita. Por eso hay que usar **número de eventos**, no «usuarios».
- Con el bloqueo de anuncios o de Analytics activado no se registra nada.

## Pruebas
`fuente/tests/test_estadisticas_partners.js` (Playwright, con el widget incrustado en otra web) comprueba:
- que no se envía nada si el visitante rechaza o no responde;
- el embudo completo, una vez cada paso y en orden;
- que el consentimiento dado tarde y el recordado se cuentan bien;
- que no hay respuestas del formulario en los parámetros;
- que `/widget/` y la web principal no cambian.
