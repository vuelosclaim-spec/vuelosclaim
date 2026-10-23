# Accesibilidad y experiencia móvil (23-10-2026)

Rama `accesibilidad-2026`, creada desde `main` (5979874).

## Qué se ha probado y con qué

Se ha usado **Chromium con Playwright y emulación de móvil**: pantallas de 320×640 y 360×740 táctiles, el perfil de iPhone 13 y escritorio de 1280×800, en modo claro y oscuro. **No se ha probado en dispositivos físicos, ni en Safari/WebKit ni en Firefox.** Tampoco con lectores de pantalla reales (NVDA, JAWS, VoiceOver, TalkBack): se comprobó el árbol de accesibilidad y los atributos ARIA, no cómo los lee un lector.

- **Análisis automático con axe-core**, reglas WCAG 2.0/2.1/2.2 A y AA más buenas prácticas, en 11 páginas:
  - portada ES y EN;
  - aerolínea ES y EN;
  - aeropuerto;
  - guía;
  - huelgas;
  - comparativa;
  - privacidad;
  - 404;
  - widget.

  Cada página se analizó con el aviso de cookies abierto y después de aceptarlo.
- **Estados interactivos analizados con axe:**
  - lista de aeropuertos abierta;
  - búsqueda sin resultados;
  - error por no elegir de la lista;
  - resultados «posible», «no» e «insuficiente»;
  - carta abierta;
  - fallo de carga de la lista de aeropuertos.
- **Teclado:** 45 pulsaciones de Tab desde el inicio de la portada. En cada elemento se comprobó el indicador de foco visible y si quedaba tapado por el aviso de cookies.
- **Tamaño de los objetivos táctiles:** todo lo interactivo debe medir al menos 24×24 px (WCAG 2.5.8). Se excluyen los enlaces dentro de un texto.
- **Desbordamiento horizontal a 320 px**, que equivale a ampliar a un 400 % (WCAG 1.4.10).

## Problemas encontrados y corregidos

| Problema | Criterio | Corrección |
| --- | --- | --- |
| Tablas con desplazamiento horizontal en móvil (rutas, importes) que no se podían recorrer con teclado | 2.1.1 Teclado | Si la tabla desborda, se le añade `tabindex="0"`, `role="region"` y un nombre (el título de la sección y «tabla desplazable»). Se recalcula al cambiar el tamaño |
| Aviso de cookies al final del documento: con el teclado se llegaba a él después de toda la página | 2.4.3 Orden del foco | Ahora va al principio del documento. Como es fijo, no cambia nada visualmente |
| Elementos con foco tapados por el aviso de cookies en móvil (enlaces del final de la página) | 2.4.11 Foco no tapado (AA, 2.2) | Mientras el aviso está abierto, la página reserva su altura con `scroll-padding-bottom`, así que el elemento con foco se coloca por encima |
| Aviso con `role="dialog"` que no movía el foco | 4.1.2 | Pasa a ser `role="region"` con nombre («Aviso de cookies» / «Cookie notice»). Al abrirlo desde el pie, el foco va a «Rechazar»; al elegir, vuelve al enlace del pie |
| Enlace «+info» del aviso: texto poco claro y 17 px de alto | 2.4.4, 2.5.8 | Ahora dice «Más información» / «More info» y mide 24 px |
| Sin enlace para saltar al contenido | 2.4.1 | Se añade «Saltar al contenido» / «Skip to content», visible al recibir el foco. Apunta a `<main id="main">` en todas las páginas, incluidas la 404, las legales, la de insertar el widget y el widget |
| Mensaje del autocompletado («No encontramos…», «Cargando…») como elemento suelto dentro de un `listbox` | 4.1.2 | Ahora es una opción desactivada (`role="option"`, `aria-disabled`) |
| El lector de pantalla no anunciaba cuántos aeropuertos había ni los mensajes | 4.1.3 Mensajes de estado | Una zona `role="status"` por campo anuncia «N aeropuertos encontrados. Usa las flechas…» o el mensaje, con 450 ms de espera para no repetir |
| Si se dejaba un aeropuerto sin elegir, el error solo aparecía en el panel de resultado, lejos del campo | 3.3.1 Identificación de errores | Error visible bajo el campo, con `aria-invalid="true"` y `aria-describedby`. Desaparece al elegir un aeropuerto |
| Enlaces del menú superior de 23 px de alto | 2.5.8 | Relleno vertical de 3 px: 24 px o más |
| Widget sin `main` ni `h1` | Buenas prácticas | `<main>` y `h1` oculto visualmente |
| Botones del aviso sin `type` | Buenas prácticas | `type="button"` |

## Revisado sin problemas

- **Contraste:** sin fallos de axe en modo claro ni oscuro, tampoco en los estados de resultado ni en el error nuevo. El rojo de error es `--no`: #8a2a2a en claro y #f08a8a en oscuro.
- **Foco visible:** todos los elementos alcanzados con Tab muestran el contorno (`:focus-visible`, 3 px). Los chips de opción lo muestran en su recuadro.
- **Autocompletado con teclado:** las flechas mueven `aria-activedescendant`, Intro elige, Esc cierra (`aria-expanded="false"`) y Tab elige la opción marcada.
- **Etiquetas:** todos los campos tienen `<label for>`, los grupos de opciones `fieldset` y `legend`, y el texto de la carta tiene una etiqueta oculta.
- **Formularios en pantallas pequeñas:** sin desbordamiento horizontal a 320 px. Los campos de la carta pasan a una columna en 420 px o menos.
- **Movimiento reducido:** se respeta `prefers-reduced-motion`.

## Pruebas automáticas nuevas

- **`test_navegador.js`, bloque «accesibilidad», a 320 px.** Comprueba:
  - el enlace para saltar al contenido y el orden del aviso;
  - el nombre del aviso y el tamaño de su enlace;
  - el espacio reservado para el foco;
  - las tablas enfocables;
  - el foco al reabrir el aviso y al cerrarlo;
  - los anuncios del autocompletado;
  - la opción desactivada;
  - `aria-invalid` y `aria-describedby`;
  - los 24 px y que no haya desbordamiento.

  Son 18 comprobaciones. Ejecutadas contra `main`, fallan las que corresponden a los errores corregidos, como se esperaba.
- **`test_sitio.py`:** cada página con enlace para saltar al contenido tiene destino, y el aviso no vuelve a ser un `role="dialog"` sin gestión del foco.

## Pendiente o fuera del alcance de este entorno

- Probar con lectores de pantalla reales y en un iPhone o Android físicos.
- Probar en Safari/WebKit: el navegador del entorno es Chromium.
- El aviso de consentimiento de Google (AdSense) no se ha podido evaluar: no se muestra mientras el sitio esté «Preparando» en AdSense.
