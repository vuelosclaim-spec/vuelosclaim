# VuelosClaim — código fuente

Este directorio genera la web estática de https://vuelosclaim.eu (español en `/`, inglés en `/en/`).
La web generada va en `../docs/`, que es la carpeta que publica GitHub Pages.

## Generar la web

```bash
python3 fuente/build.py          # genera docs/ (176 páginas)
```

No necesita dependencias: Python 3.10 o superior.

## Probar

```bash
node fuente/tests/test_reglas.js          # motor de reglas de la calculadora (Node 18+)
node fuente/tests/test_oraculo.js         # motor contra un oráculo independiente, ~19.000 casos
python3 fuente/tests/test_sitio.py docs   # enlaces, canonical, hreflang, JSON-LD, sitemap y datos
```

Prueba en navegador (opcional, necesita Playwright instalado; si no está, se omite):

```bash
python3 -m http.server 8765 -d docs &
node fuente/tests/test_navegador.js       # móvil táctil y escritorio: búsqueda, teclado, red lenta, fallos de carga, carta
```

Las mismas pruebas se ejecutan solas en cada PR (`.github/workflows/validar.yml`).
Un caso marcado como `PEND.` es un error conocido del informe de auditoría pendiente de corregir en su fase: se muestra, pero no bloquea.

## Publicar

1. Haz los cambios en una rama, no en `main`.
2. Ejecuta `python3 fuente/build.py` y sube también los cambios de `docs/`.
3. Abre un PR. La validación comprueba que `docs/` coincide con el código fuente y que pasan las pruebas.
4. Al fusionar el PR en `main`, GitHub Pages publica `docs/` en 1–2 minutos.
5. Después, avisa a buscadores: IndexNow (clave en `src_static/indexnow.key`) y Search Console.

## Qué hay en cada archivo

| Archivo | Contenido |
| --- | --- |
| `build.py` | Generador: plantillas, textos ES/EN, páginas de aerolíneas y aeropuertos, sitemap, robots, consentimiento, Analytics y AdSense |
| `src/app.js` | Calculadora en el navegador: motor de reglas (`compute`), asistencia (`care`), dónde reclamar (`where`) y cartas |
| `src/style.css` | Estilos |
| `uk_deep.py`, `uk_airports.py` | Páginas en inglés para viajeros del Reino Unido |
| `strikes.py` | Calendario de huelgas (actualizar a mano) |
| `compare.py` | Comparativa de empresas de reclamación |
| `guides.py` | Guías: vuelo cancelado, overbooking, circunstancias extraordinarias |
| `data/airlines.json` | 44 aerolíneas: país, si es europea o británica, y canal oficial de reclamación |
| `data/airports.min.json` | 3.244 aeropuertos: código, nombre, ciudad, país, coordenadas y si está en la UE/EEE/Suiza |
| `src_static/` | Logo, iconos, imagen para redes y clave de IndexNow |

`data/airports.min.json` se generó a partir de los datos abiertos de OurAirports (https://ourairports.com/data/).
El archivo original (`airports.csv`, 13 MB) no se guarda en el repositorio porque la compilación no lo usa.

Historial de cambios: [CAMBIOS.md](CAMBIOS.md). Auditoría y estrategia SEO: [SEO.md](SEO.md). Medición: [MEDICION.md](MEDICION.md).

No cambies sin revisar: el enlace de afiliado (`AFF_URL` en `build.py`), el identificador de Analytics (`G-6JRCZVTNDG`) ni el de AdSense.
