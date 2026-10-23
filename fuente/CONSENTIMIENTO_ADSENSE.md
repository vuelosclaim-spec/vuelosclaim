# Consentimiento publicitario y AdSense — revisión del 22-10-2026

Comprobado en `main` (388fee6) y en vuelosclaim.eu desde un navegador en España.

## Estado real

| Punto | Resultado |
| --- | --- |
| Carga de AdSense | `adsbygoogle.js` se carga en la cabecera de todas las páginas al abrirlas, sin esperar a ningún aviso. No hay bloques de anuncio en el código: es AdSense automático. Antes de este cambio también se cargaba en el widget (insertado en webs ajenas) y en la página 404 |
| CMP | La de Google (Privacidad y mensajes, «Funding Choices»): `cmpId` 300, certificada por Google, API TCF v2.3, política TCF v5. La carga el propio `adsbygoogle.js` |
| EEE / España | `gdprApplies: true` desde España. **No se muestra ningún mensaje de consentimiento** (`displayStatus: hidden`), no hay cadena TC y el estado es «desconocido» (`ConsentStatus 0`, `AllowAds 0`). No hay ningún mensaje de normativas europeas publicado o activo para el sitio. El sitio sigue «Preparando» en AdSense |
| Peticiones de anuncios | Desde España no se pidió ningún anuncio (`doubleclick.net/pagead/ads`). Desde EE. UU. sí (`gdpr=0`) |
| Cookies antes de decidir | En España, solo `FCCDCF`, la cookie propia de la CMP que guarda el estado del consentimiento |
| Aceptar / rechazar / modificar | Publicidad: hoy no es posible porque no hay mensaje. Analítica: sí, con nuestro aviso y el enlace del pie |
| Analytics frente a publicidad | Están separados. Nuestro aviso solo controla Analytics y Travelpayouts (`analytics_storage`). `ad_storage`, `ad_user_data` y `ad_personalization` se quedan siempre denegados en `gtag` y nuestro código nunca los activa |
| Política de privacidad | Decía «personalizados o no según lo que elijas en el aviso de consentimiento», cuando no había aviso publicitario. Faltaban la base jurídica, los destinatarios, las transferencias, la conservación y los derechos |

Requisitos de Google: para anuncios personalizados en el EEE y el Reino Unido (desde el 16-01-2024) y en Suiza (desde el 31-07-2024) hace falta una CMP certificada e integrada con TCF. Sin ella, solo anuncios no personalizados o limitados. Es obligatorio un enlace para revocar el consentimiento.

## Cambios en el código

- AdSense deja de cargarse en el widget (`/widget/`, insertado en webs de terceros) y en la página 404 (sin contenido).
- Enlace «Privacidad de los anuncios» / «Ad privacy settings» en el pie, distinto de «Cookies de analítica». Si la CMP de Google está cargada, abre su mensaje de revocación (`googlefc.callbackQueue.push(googlefc.showRevocationMessage)`); si no, lleva a la sección de publicidad de la política.
- Política de privacidad, en español y en inglés:
  - secciones separadas para analítica y afiliación y para publicidad;
  - la CMP de Google con TCF, y anuncios no personalizados o limitados sin consentimiento;
  - base jurídica (art. 22.2 LSSI y 6.1.a RGPD), destinatarios y transferencias (Google Ireland, Marco de Privacidad UE-EE. UU.);
  - conservación de Analytics (2 meses de eventos y 14 de usuario, comprobado en la propiedad) y derechos con la AEPD.
- No se activa nada publicitario: ni anuncios personalizados ni ninguna señal `ad_*`.
- Pruebas: `test_sitio.py` comprueba que el widget y la 404 no cargan AdSense y que toda página con AdSense tiene el enlace de consentimiento publicitario.

## Pasos manuales en AdSense (cuenta vuelosclaim@gmail.com)

1. **Privacidad y mensajes** → tarjeta **Normativas europeas** → **Crear** (o **Gestionar** → **Crear mensaje**).
2. **Sitios:** marcar `vuelosclaim.eu` → Confirmar.
3. **Idiomas:** predeterminado Español (es); adicionales Inglés (en) e Inglés (en-GB). Revisar el texto en cada idioma.
4. **Opciones del usuario:** activar **«No consentir»** en todos los países, para que rechazar sea igual de fácil que aceptar. Dejar desactivado el icono de cerrar.
5. **«Optimizar mi mensaje de consentimiento»:** desactivar, para que el aviso no cambie sin revisarlo.
6. **Nombre del mensaje:** «VuelosClaim UE».
7. **URL de la política de privacidad:** `https://vuelosclaim.eu/privacidad/`.
8. **Publicar.**
9. **Comprobar:** en una ventana de incógnito desde España, abrir vuelosclaim.eu. Debe aparecer el aviso de Google con «Consentir», «No consentir» y «Gestionar opciones». Después, el enlace «Privacidad de los anuncios» del pie debe volver a abrirlo.

Si algún día se quieren **solo anuncios no personalizados** para todo el mundo, hay un ajuste de anuncios personalizados en la cuenta de AdSense. No hace falta tocarlo: con la CMP, los anuncios personalizados solo se muestran a quien los acepta.

## Pendiente y riesgos

- Mientras no se publique el mensaje de Google, el EEE no tiene forma de dar o negar el consentimiento publicitario y Google no servirá anuncios personalizados allí.
- Con el mensaje de Google publicado, los visitantes nuevos verán dos avisos: el de Google (publicidad) y el nuestro (analítica). Se podría unificar usando el modo de consentimiento del mensaje de Google también para Analytics, pero implica rehacer nuestro aviso y probarlo de nuevo.
- `adsbygoogle.js` se carga antes de la decisión porque es el que trae la CMP. Desde España solo se ha visto la cookie de estado de la CMP.
