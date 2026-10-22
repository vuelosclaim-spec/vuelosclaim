# SEO de VuelosClaim — auditoría y estrategia (22-10-2026)

Todo lo que aparece aquí se ha medido sobre el sitio generado (`docs/`, 177 páginas) o se ha comprobado en fuentes oficiales.
No hay volúmenes de búsqueda ni dificultades: no disponemos de una herramienta que los acredite. Para priorizar con datos reales, usar el informe de Rendimiento de Google Search Console.

## 1. Auditoría técnica

| Punto | Estado antes | Cambio | Comprobación |
| --- | --- | --- | --- |
| Títulos y descripciones | 11 títulos > 60 caracteres, 7 descripciones < 70 (páginas legales) y 5 > 160 | Títulos acortados en guías y aerolíneas con nombre largo; descripciones propias en páginas legales | `test_sitio.py`: 0 avisos |
| H1–H3 | Un H1 por página, sin saltos de nivel | Sin cambios necesarios | `test_sitio.py` + script de auditoría |
| Canonical y hreflang | Correctos y recíprocos ES/EN, con x-default | Sin cambios | `test_sitio.py` |
| robots.txt y sitemap | Correctos, pero `lastmod` fijado a mano | `lastmod` = fecha del último cambio real de título, descripción o contenido principal (hash) | Dos compilaciones seguidas dan el mismo sitemap; prueba de fecha válida |
| Enlaces internos | 14 páginas de aeropuertos británicos con un solo enlace entrante | Enlazadas desde todas las páginas en inglés de aerolíneas y aeropuertos | Ninguna página indexable con menos de 2 enlaces entrantes |
| Indexabilidad | Todas indexables salvo `/widget/` (noindex a propósito) | Sin cambios | `test_sitio.py` |
| Datos estructurados | `WebSite` duplicado en las portadas; FAQ visibles | Un solo `WebSite`; prueba de que las preguntas FAQ se ven en la página | `test_sitio.py` (con prueba negativa) |
| Contenido parecido | Aerolíneas ES: 62 % de texto propio compartido (n-gramas de 5 palabras, sin listas de enlaces); aeropuertos ES: 49 % | Se quita el bloque genérico repetido y se añade una ficha con datos de cada aerolínea | Aerolíneas: 56 %; aeropuertos: 37 % |
| Móvil y Core Web Vitals | Medido en laboratorio (CPU ×4, red 1,6 Mbps, sin scripts de terceros): LCP 0,7–1,1 s, CLS ≤ 0,03, sin desbordamiento | Enlaces del pie con área táctil de 24 px; tabla de normas legible en móvil | `test_navegador.js` y medición con Playwright |

Los datos de campo de Core Web Vitals (usuarios reales) solo están en Search Console o en PageSpeed Insights; los scripts de AdSense, Analytics y Travelpayouts no se incluyeron en la medición de laboratorio.

`FAQPage`: Google solo muestra resultados enriquecidos de FAQ para webs gubernamentales y de salud. El marcado se mantiene porque describe contenido visible y no penaliza.

## 2. Contenido jurídico corregido

| Afirmación | Problema | Corrección y fuente |
| --- | --- | --- |
| «400 € hasta 3.500 km y 600 € a partir de ahí» | Omitía que los vuelos dentro de la UE de más de 3.500 km pagan 400 € | Art. 7.1.b Reglamento 261/2004 |
| «llegaba como mucho 4 h / 2 h después» | El reglamento dice «menos de» | Art. 5.1.c.ii y iii |
| «La compensación por overbooking es automática» | Exagerado: hay motivos razonables que eximen | Art. 2.j y 4.3; TJUE C-22/11 |
| «documentación, seguridad, comportamiento» | No es la lista del reglamento | Salud, seguridad o documentación inadecuada (art. 2.j) |
| Escalas: «distancia total» | Es la distancia ortodrómica origen–destino final | TJUE C-559/16 |
| «300 € con 3–4 h» sin matiz | Solo fuera de la UE | Art. 7.2.c |
| «Si el tiempo era el problema, no salió nadie» | Afirmación no demostrable | Se presenta como indicio que el pasajero puede alegar |
| «La aerolínea suele pagar en unas semanas» (comparativa) | Tiempo de resolución sin fuente | Eliminado |
| Ryanair «resuelve en unos 10 días»; Wizz Air «30 días y descuenta 50 €» | Plazos y cargos sin fuente verificable | Eliminados |
| Ryanair y Wizz Air (inglés): «escala tras 8 semanas a AESA» | AESA: un mes | Un mes para AESA; 8 semanas para ADR/CAA en Reino Unido |
| Aerolíneas no europeas (español): «aeropuerto europeo» | Ambiguo tras el Brexit | UE, EEE o Suiza; añadido UK261 para aerolíneas británicas |

Plazos publicados, todos con fuente: España, 5 años para reclamar a la aerolínea y un año desde esa reclamación para acudir a AESA, cuya resolución es vinculante para la aerolínea (AESA). Inglaterra y Gales, 6 años (Dawson contra Thomson, 2014). Resto de países, ley nacional (TJUE C-139/11).

## 3. Contenido nuevo por página

- **Aerolíneas (88 páginas):** ficha propia con:
  - canal oficial de reclamación;
  - tabla de qué norma se aplica según la dirección del vuelo, calculada con los datos de la aerolínea (comunitaria, británica, mixta o de fuera);
  - dónde acudir si no paga;
  - documentos;
  - plazos con fuente;
  - 3 preguntas frecuentes con respuestas según esos datos.
- **Aeropuertos españoles (54 páginas):** cómo y dónde reclamar un vuelo de ese aeropuerto (AESA, UK261), con plazos y artículos del reglamento.
- **Huelgas:** cada huelga lleva fecha de fin y se oculta sola cuando pasa (H13).

No se han creado páginas nuevas ni cambiado URL: no hace falta ninguna redirección 301.

## 4. Estrategia de palabras clave por intención (sin volúmenes)

| Intención | Ejemplos de búsqueda | Página que debe posicionar | Por qué es oportunidad |
| --- | --- | --- | --- |
| Calcular / reclamar ya | reclamar vuelo retrasado, compensación retraso vuelo, calculadora indemnización vuelo | `/` y `/en/` | Máxima intención; la calculadora responde mejor que un artículo |
| Aerolínea + problema | reclamar a Vueling retraso, Ryanair compensación cancelación, Jet2 delay compensation | Páginas de aerolínea | Intención alta y página específica con canal oficial y normas aplicables |
| Situación concreta | vuelo cancelado qué hacer, overbooking indemnización, circunstancias extraordinarias vuelo | Guías | Informacional con salida natural a la calculadora |
| Actualidad | huelga controladores noviembre, huelga vuelos España | `/huelgas-vuelos-espana/` | Picos de demanda; requiere actualizar la tabla en cuanto hay convocatorias |
| Comparativa | AirHelp comisión, Reclamador o AirHelp | Comparativa | Intención comercial ligada a la afiliación; datos con fuente |
| Reino Unido → España | flight delay compensation Spain, Manchester to Spain delay compensation | Páginas de aeropuertos británicos | Mercado británico con UK261 y EU261 a la vez |
| Aeropuerto | retraso vuelo aeropuerto Valencia | Páginas de aeropuerto | Intención menor; útiles como apoyo y para enlazado interno |

Cómo priorizar con datos: en Search Console, filtrar consultas con impresiones y posición entre 5 y 20, y mejorar primero esas páginas. Revisar cada mes «Rastreada: actualmente sin indexar» y «Duplicada, Google ha elegido otra canónica» en las páginas de aerolíneas.

## 5. Riesgos y vigilancia

- Las páginas de aerolíneas siguen compartiendo bastante texto, porque las normas son las mismas. Si Search Console marca páginas como duplicadas o no indexadas, añadir datos propios verificados (requisitos de cada formulario, idiomas, canales) antes que más texto genérico.
- 174 páginas cambian de `lastmod` a la vez (cambio real de contenido); es normal que Google las rastree de nuevo en los próximos días.
- Títulos cambiados en 7 páginas: puede haber fluctuaciones de posición temporales.
- Los organismos ADR británicos de cada aerolínea salen de `data/airlines.json`; conviene revisarlos en la lista de la CAA cada pocos meses.
- Los datos de campo de Core Web Vitals pueden empeorar por los scripts de terceros (anuncios); vigilar en Search Console cuando AdSense empiece a servir anuncios.
