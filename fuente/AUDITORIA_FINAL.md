# Auditoría final — 22-10-2026

**Versión anterior:** `5bb93cb` (21-10-2026). **Versión revisada:** `main` tras los PR #2, #3 y #4, más las correcciones de este PR.

Los PR #2, #3 y #4 ya están publicados con autorización expresa. Este PR solo contiene las correcciones encontradas en la auditoría y no se fusionará sin autorización.

## 1. Cambios implementados

| Bloque | Qué cambió |
| --- | --- |
| Calculadora (PR #2) | Tres resultados: posible, no parece, información insuficiente. Cancelaciones con aviso y vuelo alternativo (art. 5); límites exactos de 3 y 4 h; denegación voluntaria o involuntaria; cobertura UE/EEE/Suiza/Reino Unido; causas diferenciadas según la jurisprudencia |
| Formularios y cartas (PR #3) | Carga de aeropuertos con reintento y mensajes de error; autocompletado sin pérdidas de resultados; cartas sin IBAN, redactadas como reclamación y fieles al resultado |
| SEO (PR #4) | Ficha por aerolínea con canal oficial, norma aplicable, plazos y fuentes; sección «dónde reclamar» en aeropuertos; correcciones jurídicas; `lastmod` real; enlaces internos; datos estructurados |
| Medición (PR #4) | Analytics y Travelpayouts solo tras aceptar las cookies; 9 eventos del embudo sin datos personales; botón de afiliado que dice quién es el proveedor, su comisión y que no garantiza el resultado |
| Esta auditoría | Corrección de parámetros reservados de GA4, botones del banner con la misma prominencia, archivo sobrante y verificador independiente en la integración continua |

## 2. Problemas corregidos en esta auditoría

1. **Parámetros reservados de GA4.** Los eventos enviaban `language` y `page_path`. En la petición real a Google se vio que sobrescribían el idioma del navegador (`ul`) y la ruta de la página (`dp`). Ahora son `site_language` y `source_page`.
2. **Banner de cookies.** «Rechazar» tenía menos prominencia que «Aceptar». Ahora los dos tienen el mismo estilo.
3. **`fuente/src_static/ads.txt` sobrante.** Ya existía `ads.txt` generado por `build.py` antes del 22-10; lo añadí por error y no se usaba. Eliminado.
4. **Prueba independiente.** Se añade `tests/test_oraculo.js` a la integración continua: compara el motor con un oráculo escrito aparte en ~19.000 casos.

## 3. Pruebas superadas

| Prueba | Resultado |
| --- | --- |
| `test_reglas.js` | 95 casos, 391 comprobaciones: límites de 179/180/240/241 min, 1.500/1.501/3.500/3.501 km, 6/7/13/14 días, márgenes del vuelo alternativo, ES/EN, cartas, búsqueda de aeropuertos |
| `test_oraculo.js` (nuevo) | ~19.000 casos aleatorios de retraso y cancelación con límites exactos: 0 discrepancias |
| `test_sitio.py` | 177 páginas: 0 enlaces internos rotos; canonical, hreflang, sitemap, títulos, descripciones, datos estructurados, FAQ visibles, `lastmod`, huelgas con fecha de fin, canal oficial en cada aerolínea, sin IBAN |
| `test_navegador.js` | 79 comprobaciones en móvil táctil y escritorio: autocompletado (toque, teclado, red lenta, error 500, HTML en vez de JSON), carta (copiar, descargar, sin datos bancarios), sin desbordamiento, consentimiento y eventos |
| Producción, navegador real | Antes de aceptar: 0 peticiones a Analytics y 0 a Travelpayouts. Tras aceptar, solo los eventos previstos y ningún dato de la carta (nombre o reserva de prueba no aparecen en ninguna petición) |
| Afiliación | 161 enlaces, todos `https://airhelp.tpx.gr/Ow8vczQM` con `rel="sponsored nofollow noopener"`; la redirección llega a AirHelp con los parámetros de Travelpayouts |
| Diseño | Capturas a 375 px y 1.280 px de portada, aerolínea, guía, inglés y huelgas: sin desbordamiento ni errores de JavaScript |
| Secretos | Sin tokens, contraseñas ni claves en los archivos ni en el historial de Git |
| Integración continua de GitHub | Validación en verde en todos los PR |

## 4. Pruebas que no se han podido ejecutar

- **26 enlaces externos** (formularios de aerolíneas como Iberia, Vueling, Ryanair o British Airways) responden 403 o no responden desde el servidor de pruebas, probablemente por protección anti-robots. No se ha podido confirmar si funcionan; conviene abrirlos a mano. OurAirports devuelve error 500 en su propio servidor.
- **Móviles físicos** (Safari en iPhone, Chrome en Android) y lectores de pantalla: solo se ha usado Chromium emulando móvil.
- **Core Web Vitals de usuarios reales:** solo hay medidas de laboratorio sin scripts de terceros (LCP 0,7–1,1 s, CLS ≤ 0,03).
- **Informes de GA4:** se ha comprobado que las peticiones salen bien, no que aparezcan en la interfaz de Analytics; las dimensiones personalizadas aún no están creadas.
- **Consentimiento de AdSense en la UE:** las pruebas salen desde una IP de EE. UU. (`gdpr=0`), así que no se ha visto el mensaje de consentimiento de Google tal y como lo vería un usuario europeo.
- **Atribución de Travelpayouts:** no se puede comprobar de principio a fin sin una reclamación real.
- **Revisión jurídica por un abogado:** las reglas se han contrastado con AESA, la CAA, la FAQ de la Comisión y sentencias del TJUE, pero no las ha revisado un profesional.

## 5. Riesgos pendientes

- Cuestiones jurídicas abiertas: Jersey, Guernsey, Man, Gibraltar, Svalbard y el norte de Chipre; restricciones ATC según C-108/26; huelgas de subcontratas; aerolíneas mixtas; vuelos Reino Unido–UE con doble régimen; retraso de 3 h exactas en el tramo de 1.500–3.500 km; escalas y billetes no públicos.
- AdSense carga antes de cualquier consentimiento hasta que se active el mensaje de consentimiento de Google en AdSense, cuando se apruebe la cuenta.
- Analytics solo mide a quien acepta: las cifras son una muestra.
- Las páginas de aerolíneas siguen pareciéndose entre sí (56 % de texto propio compartido).
- El calendario de huelgas y los organismos ADR de las aerolíneas necesitan revisión manual periódica.
- Tu NIF y tu nombre aparecen en el aviso legal: lo exige la LSSI para un titular persona física, pero son públicos.
- Fuera del repositorio: el token de Netlify usado en semanas anteriores sigue activo en tu cuenta. Conviene revocarlo, porque ya no se usa.

## 6. Diferencias respecto a la versión anterior (`5bb93cb`)

- **Mismas 176 URL.** Ninguna página añadida ni eliminada, sin redirecciones.
- **Código fuente:**
  - `build.py`: plantillas, textos, consentimiento, sitemap y fichas.
  - `src/app.js`: motor, formulario, autocompletado, cartas y eventos.
  - `src/style.css`: estilos.
  - `guides.py`, `compare.py`, `uk_deep.py`, `uk_airports.py`, `strikes.py`: textos jurídicos y huelgas.
  - `data/airlines.json`: dos notas sin fuente eliminadas.
- **Pruebas:** `test_reglas.js` ampliada; `test_sitio.py` con más comprobaciones; `test_navegador.js` y `test_oraculo.js` nuevas.
- **Documentación:** `CAMBIOS.md`, `SEO.md`, `MEDICION.md`, este informe y el `README.md` de la raíz.
- **Raíz del repositorio:** eliminadas las 195 copias antiguas (PR #2). La web se publica solo desde `docs/`.
- **Sin cambios:** enlace de afiliado, ID de Analytics `G-6JRCZVTNDG`, cuenta de AdSense, identificador de Travelpayouts, dominio y `CNAME`.
- **Dependencias y costes:** ninguna dependencia nueva en la web ni en la integración continua (solo Python y Node estándar). Playwright se usa en local y es opcional. Ningún coste recurrente nuevo: GitHub Pages es gratuito y el dominio sigue en DonDominio como antes.

## 7. Pasos para el despliegue

1. Revisar este PR y, si estás de acuerdo, autorizar la fusión.
2. Al fusionar, GitHub Pages publica `docs/` en 1–2 minutos. Comprobar portada, una página de aerolínea y el banner de cookies.
3. Avisar a buscadores (IndexNow) y revisar Search Console en los días siguientes.
4. En Google Analytics: crear las dimensiones personalizadas, marcar `affiliate_click` como evento clave y crear el embudo (pasos en `MEDICION.md`).
5. Cuando AdSense apruebe la cuenta: activar el mensaje de consentimiento de Google para la UE y el Reino Unido.
6. Abrir a mano los enlaces oficiales de aerolíneas que no se pudieron comprobar y corregir los que hayan cambiado en `data/airlines.json`.
