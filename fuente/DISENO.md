# Rediseño visual: modelo «botones apilados» (26-10-2026)

Rama `diseno-verde`, creada desde `main` (a89f037). Se aplica el prototipo 3, elegido por el propietario entre cinco propuestas basadas en las webs del sector con más tráfico.

## Qué cambia

- **Marca y colores.** El verde (#0d6b3b) es el color de las acciones. El verde muy oscuro se usa en el pie y las tablas, y el fondo es claro y verdoso. Hay versión oscura con los mismos papeles. Todo se controla con las variables de `src/style.css`.
- **Tipografía.** Noto Sans, en pesos 400, 600 y 800, sustituye a Bricolage Grotesque, Public Sans e IBM Plex Mono.
  - Se sirve desde `/fonts/`, con licencia SIL OFL (`OFL-notosans.txt`).
  - Los archivos salen de `@fontsource/noto-sans` 5.3.0.
  - Se precargan solo dos archivos: los latin 400 y 800.
- **Cabecera blanca**, con un icono de avión en verde. El enlace de idioma va en una píldora.
- **Calculadora.** Lo primero de la tarjeta es «¿Qué le pasó a tu vuelo?» / «What happened to your flight?», con tres botones grandes apilados: Retraso, Cancelación y Overbooking. Los demás grupos de opciones siguen igual, ahora en verde y con esquinas más redondeadas.
- **Importes de la portada** (250, 400 y 600 €) en tarjetas blancas.
- **Bloque nuevo en la portada ES/EN: «Por qué usar VuelosClaim» / «Why use VuelosClaim»**, con 4 tarjetas. Todas las afirmaciones son ciertas hoy:
  - gratis;
  - cada resultado cita la norma o la sentencia;
  - no pide datos personales para calcular;
  - carta gratuita o servicio de pago.

  No hay valoraciones, testimonios ni cifras de clientes.
- Las preguntas frecuentes van en tarjetas.

## Lo que no cambia

- URLs, títulos, H1, textos jurídicos, datos estructurados y el motor de cálculo.
- Enlaces de afiliación, Analytics y AdSense, consentimiento y carta.
- Las respuestas por defecto de la calculadora y el ejemplo MAD → BER.

## Psicología aplicada (con criterio ético)

- **Ley de Hick y energía de activación.** Una sola primera pregunta con tres respuestas grandes, así que empezar cuesta un toque.
- **Efecto precio cero.** «Gratis de verdad».
- **Autoridad.** Reglamento y TJUE citados.
- **Aversión al arrepentimiento.** La comisión de AirHelp se explica junto al botón, igual que antes.
- **Sin urgencia falsa ni prueba social inventada.**

## Comprobado

- Las 7 baterías de pruebas pasan (reglas, oráculo, sitio, mantenimiento, canales, monetización y navegador).
- Sin desbordamiento horizontal a 320 px.
- Capturas en escritorio, móvil y modo oscuro.
- Análisis axe con los resultados anotados en la PR.
- **No probado** en dispositivos físicos ni en Safari.
