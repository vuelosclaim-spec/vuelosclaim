# Cambios

## 2026-10-22 — SEO técnico y contenido verificable

Detalle, mediciones y estrategia en [SEO.md](SEO.md).

- Páginas de aerolínea: ficha propia (canal oficial, norma aplicable según la dirección del vuelo, dónde acudir, documentos, plazos con fuente y preguntas frecuentes). Se quita el bloque genérico repetido.
- Páginas de aeropuerto: sección «Dónde reclamar» con AESA, UK261, plazos y artículos.
- Correcciones jurídicas en guías, comparativa y páginas británicas (importes intra-UE, «menos de 4/2 h», overbooking, escalas, plazos de AESA). Eliminadas notas de aerolíneas y tiempos de resolución sin fuente.
- `lastmod` del sitemap según el último cambio real de cada página; huelgas que se ocultan al pasar su fecha.
- Enlaces internos a las 14 páginas de aeropuertos británicos; un solo `WebSite` en los datos estructurados; títulos y descripciones ajustados; áreas táctiles del pie.
- Pruebas: canal oficial y plazos en cada aerolínea, preguntas FAQ visibles, `lastmod` válido, huelgas con fecha de fin.

## 2026-10-22 — Formularios, aeropuertos y cartas

**Lista de aeropuertos (`src/app.js`)**
- Carga con límite de 15 s, un reintento automático, comprobación del estado HTTP y del formato (una página HTML con estado 200 se trata como error).
- Si falla: mensaje visible con botón «Reintentar»; si no hay conexión, se dice y se reintenta solo al volver la conexión.
- Mientras carga, el desplegable dice «Cargando aeropuertos…» y muestra las sugerencias en cuanto llega la lista.
- Comprobado en producción con un navegador real: `/data/airports.min.json` responde 200 (JSON, gzip) y la calculadora calcula. El texto de error que aparece en el HTML está oculto por CSS y solo se muestra si la carga falla.

**Autocompletado**
- Antes dejaba de buscar al llegar a 60 coincidencias y ordenaba después: un código exacto podía perderse (por ejemplo, «san»). Ahora puntúa todos los aeropuertos y luego ordena.
- Acepta código IATA, ciudad, nombre del aeropuerto, alias en español e inglés, varias palabras («londres gatwick») y el texto que queda al elegir («Madrid (MAD)»). Ignora mayúsculas y acentos.
- Cada sugerencia muestra código, ciudad, nombre del aeropuerto y país, para distinguir aeropuertos de una misma ciudad.
- Teclado: flecha abajo abre la lista, flechas, Enter, Tab y Escape; `aria-selected` y `aria-activedescendant`. Al salir del campo con un código exacto o una única coincidencia, se elige solo.
- Mensajes cuando no hay coincidencias, cuando se ha escrito sin elegir de la lista y cuando origen y destino son el mismo aeropuerto.

**Cartas de reclamación**
- Eliminado el campo IBAN y su uso. La carta pide a la aerolínea que indique en 30 días cómo y cuándo pagará (y recuerda que el pago es en metálico, transferencia o cheque; bonos solo con acuerdo por escrito, art. 7.3).
- Solo se ofrece con el resultado «Posible derecho a compensación»; con otro resultado se oculta y se vacía.
- Redactada como reclamación («Considero que tengo derecho…») y pide a la aerolínea que acredite una circunstancia extraordinaria si la alega.
- Refleja el resultado: motivo comunicado (avería, tripulación, huelga propia), importe reducido por el art. 7.2, horarios del vuelo alternativo y si se aceptó, y motivo de la denegación de embarque.

**Privacidad**
- Los datos de la carta solo se usan en el navegador: no se envían, no se guardan y no se usa almacenamiento local. La política de privacidad y el texto del formulario lo explican. No se piden datos bancarios.
- Una prueba comprueba que ninguna petición de red contiene los datos escritos en la carta.

**Pruebas**
- `test_reglas.js`: formato y coordenadas de la base, distancias de referencia, aeropuertos distintos en la misma ciudad, 18 casos de búsqueda y comprobaciones de las cartas.
- `test_sitio.py`: ninguna página menciona IBAN, la ruta del JSON de cada calculadora existe y hay botón de reintento.
- `test_navegador.js` (nuevo): móvil táctil y escritorio; toque, teclado, red lenta, error 500, HTML en lugar de JSON, reintento, carta, copiar, descargar, datos que no salen del navegador y sin desbordamiento.

## 2026-10-22 — Calculadora con tres resultados

Ver PR #2: resultados «posible», «no parece» e «información insuficiente»; reglas de cancelación, retraso, denegación de embarque, cobertura territorial y causas extraordinarias.
