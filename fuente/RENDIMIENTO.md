# Rendimiento y velocidad (25-10-2026)

Rama `rendimiento-2026`, creada desde `main` (cd58c1a).

## Medición inicial en producción

Lighthouse 12 en móvil (simulación de 4G lenta y CPU ×4), contra vuelosclaim.eu:

| Página | Nota | FCP | LCP | TBT | CLS |
| --- | --- | --- | --- | --- | --- |
| Portada | 87 | 2,4 s | 2,4 s | 340 ms | 0 |
| Iberia | 62 | 4,7 s | 6,5 s | 120 ms | 0 |

Lo que más pesaba:

1. **La hoja de Google Fonts bloqueaba el renderizado.** Lighthouse estimaba un ahorro de 0,7 a 2,2 s.
2. **AdSense y el mensaje de consentimiento de Google se cargaban al abrir la página:** unos 400 KB de JavaScript, entre 280 y 450 ms de hilo principal bloqueado, y competían con el contenido por la red del móvil.
3. **La lista de aeropuertos (90 KB comprimidos) se descargaba al abrir cualquier página con calculadora,** aunque el visitante no la usara.

El elemento LCP es el párrafo de entrada (`p.lede`), con la fuente Public Sans.

## Cambios

- **Fuentes propias.** Son las mismas fuentes y los mismos archivos que sirve Google Fonts (Bricolage Grotesque, IBM Plex Mono y Public Sans; subconjuntos latin y latin-ext), ahora servidas desde `/fonts/`. Ya no hay ninguna petición bloqueante a otro dominio.
  - Solo se precargan las dos que se ven arriba: Public Sans y Bricolage, latin.
  - latin-ext se descarga únicamente si la página lo necesita (`unicode-range`).
  - Licencias SIL OFL incluidas en `/fonts/`.
- **AdSense diferido.** Es el mismo script con el mismo identificador de editor. Se carga al primer gesto del visitante (tocar, desplazar o una tecla) o, como tarde, 1,5 s después de que la página termine de cargar y quede libre. El mensaje de consentimiento de Google llega con él.
- **Lista de aeropuertos bajo demanda.**
  - Los dos aeropuertos del ejemplo van incrustados en la página, así que el resultado del ejemplo sale al instante.
  - La lista completa se descarga al tocar un campo de aeropuerto, o 1,2 s después de cargar la página.
  - Se mantienen el aviso «Cargando…», el reintento y el mensaje de error.

**El diseño no cambia.** Las capturas de la página de Iberia antes y después, en móvil y escritorio, son idénticas píxel a píxel.

**Tampoco cambian:** los enlaces de afiliación, el identificador de Analytics, el consentimiento ni la calculadora.

## Resultado en laboratorio

Lighthouse móvil, mediana de 3 pasadas, sobre el sitio generado. Las dos versiones se sirvieron en local con compresión gzip, y los recursos externos (Google Fonts y AdSense) pasaron por el proxy del entorno.

| Página | Antes: nota / FCP / LCP / TBT | Después: nota / FCP / LCP / TBT |
| --- | --- | --- |
| Portada | 69 / 4,0 s / 5,3 s / 74 ms | 96 / 1,2 s / 2,0 s / 183 ms |
| Iberia | 68 / 4,1 s / 5,3 s / 84 ms | 97 / 1,2 s / 2,0 s / 180 ms |

**Cómo leer estas cifras:**

- El proxy añade latencia a Google Fonts, así que en la medición de antes la mejora parece mayor de lo que será en la web real. Hay que repetir la medición en producción tras publicar.
- El TBT sube un poco porque AdSense ahora se ejecuta 1,5 s después de cargar la página, dentro de la ventana que mide Lighthouse, en vez de al principio. Sigue por debajo de 200 ms (rango «bueno»).
- El CLS sigue en 0, pero se ha medido **sin anuncios servidos**: el sitio está «Preparando» en AdSense. Los anuncios automáticos pueden mover el contenido al insertarse.

## Riesgos y siguientes pasos

- **Aprobación de AdSense.** Para verificar el sitio están la metaetiqueta `google-adsense-account` y `ads.txt`, y Googlebot ejecuta la página, así que debería ver el script cargado. Si AdSense pidiera de nuevo «el código en el `<head>`», basta con volver a la etiqueta directa en `ADSENSE` (`fuente/build.py`).
- **Cuando AdSense sirva anuncios:**
  - vigilar CLS e INP en Search Console (Experiencia → Métricas web principales);
  - si los anuncios automáticos mueven el contenido, limitar los formatos en AdSense → Anuncios → Editar sitio, por ejemplo con exclusiones de página o menos carga de anuncios.
- **Caché.** GitHub Pages fija una caché de 10 minutos y no se puede cambiar. Las fuentes llevan un identificador en el nombre, así que una caché larga sería segura con otro alojamiento.
- **No probado en dispositivos físicos:** solo emulación de Chromium.

## Pruebas nuevas

- **`test_sitio.py`.** Da error si:
  - vuelve Google Fonts externo;
  - una página enlaza una fuente que no existe;
  - se precargan más de 2 fuentes;
  - AdSense vuelve a cargarse con una etiqueta directa;
  - una calculadora no lleva los aeropuertos del ejemplo.
- **`test_navegador.js` (bloque «rendimiento»).** Comprueba que:
  - el ejemplo se calcula antes de tener la lista;
  - la lista se pide sola una vez;
  - mientras llega se avisa;
  - las sugerencias aparecen al llegar;
  - las fuentes propias se cargan.
