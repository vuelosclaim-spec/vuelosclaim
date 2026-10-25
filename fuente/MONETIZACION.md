# Monetización: instrumentación y experimentos controlados

Actualizado: 25-10-2026. Este documento es un plan de optimización **sin cambios en los importes ni en los derechos del pasajero**.

## Embudo principal y fuente de verdad

1. `page_view`: visitas que aceptan analítica.
2. `calculator_started`: comienzan a introducir datos.
3. `calculator_completed`: obtienen una evaluación.
4. `compensation_possible`: el resultado indica posible compensación.
5. `affiliate_click`: pulsan un enlace patrocinado a un proveedor.

El evento `affiliate_click` se registra solo tras consentimiento de analítica. No se debe tratar como venta ni como reclamación. Los **ingresos y conversiones atribuidas** deben obtenerse del panel de Travelpayouts/AirHelp, descontando anulaciones si aplica.

**KPIs:**

- Inicio / páginas vistas = `calculator_started / page_view`.
- Finalización / inicio = `calculator_completed / calculator_started`.
- Clic patrocinado / resultado positivo = `affiliate_click / compensation_possible`. Analizar por sesión/usuario, no por número bruto de eventos, para evitar distorsión por varios clics.
- Tasa de conversión atribuida e ingreso neto por clic: solo si Travelpayouts proporciona clics, ventas y comisiones fiables.
- Experiencia: Core Web Vitals móvil, rebote, opción de reclamación gratuita utilizada y reclamaciones/quejas por expectativas engañosas.

No guardar en GA4 nombres, reservas, números de vuelo ni el contenido de cartas. No introducir scripts adicionales antes de consentir.

## Experimentos propuestos (uno cada vez)

1. **Claridad de la propuesta:** comparar una CTA genérica contra «Que AirHelp gestione la reclamación» con comisión de afiliación y opción gratuita visibles. Evitar «Cobra garantizado», «Gratis» aplicado al servicio o importes no confirmados.
2. **Contexto del clic:** ubicar la explicación de costes y del servicio junto al enlace, sin eliminar el acceso directo al formulario oficial de la aerolínea.
3. **Momento de presentación:** mostrar la opción de servicio solo si existe posible derecho, incluido el caso pendiente de acreditar circunstancias extraordinarias; no incentivar clics desde resultados «no corresponde».
4. **Página comparativa:** comprobar si el cálculo de cuánto retiene cada empresa ayuda a convertir, manteniendo fuentes y fechas verificadas.

Definir previamente métrica principal (`affiliate_click` / sesiones con posible derecho), métricas de seguridad y duración. No declarar vencedor con muestras pequeñas ni modificar precios, obligaciones o probabilidades de éxito para generar más clics.

## Reglas de transparencia

- «Reclamar por tu cuenta» y «Usar un intermediario» son alternativas diferentes. La primera no cobra comisión del intermediario.
- Mostrar que VuelosClaim cobra comisión si se usa el enlace de AirHelp y que AirHelp puede descontar honorarios de la compensación.
- Marcar enlaces de afiliación con `rel="sponsored nofollow noopener"` cuando abran nueva pestaña.
- No redirigir automáticamente ni interponer enlaces de afiliación entre la persona y la carta gratuita.
- Verificar tarifas, recargos judiciales y canales oficiales antes de publicar comparativas actualizadas.
- No enviar a Analytics información personal procedente de la calculadora/carta.

## Comprobación operativa mensual

Revisar el panel Travelpayouts frente al embudo de GA4, las URLs de destino, los términos comerciales oficiales y los informes de rendimiento de Search Console. Documentar fecha, métricas y cambios realizados. Las discrepancias GA4 ↔ Travelpayouts pueden deberse al consentimiento, al bloqueo de rastreo o a ventanas de atribución distintas.
