# Páginas de aerolíneas: calidad y texto compartido (23-10-2026)

Rama `seo-aerolineas-2026`, creada desde `main` (5979874).

## Diagnóstico

Las 44 páginas de aerolínea (88 con las inglesas) compartían la mayor parte del texto. Las partes propias de cada página eran:

- el ámbito de la norma según el país de la aerolínea;
- la tabla de rutas;
- el enlace al canal oficial;
- el organismo de resolución de conflictos británico.

El apartado «Cómo reclamar a X» era el mismo párrafo genérico en todas.

**Cómo se mide el texto compartido:** porcentaje de los grupos de 5 palabras de cada página que aparecen en al menos la mitad de las páginas de aerolínea del mismo idioma. Se excluyen la cabecera, el pie, la calculadora, los scripts y las listas de enlaces internos. El script está en el registro de la tarea; mide distinto que la auditoría de SEO.md, así que las cifras no son comparables con aquella.

| | Antes (ES / EN) | Después (ES / EN) |
| --- | --- | --- |
| Media de las 44 páginas | 72,9 % / 66,1 % | 68,5 % / 62,5 % |
| Las 12 aerolíneas con ficha comprobada | — | 54,1 % / 47,0 % |
| Las 32 restantes | — | 73,9 % / 68,4 % |

## Qué se ha hecho

- **Nuevo archivo `data/airline_claims.json`.** Contiene, para cada aerolínea:
  - canal y formularios oficiales;
  - qué datos pide;
  - requisitos particulares;
  - qué pasa después de enviar la reclamación;
  - avisos y fuentes, con la fecha de comprobación.

  Solo incluye lo que publica la aerolínea en su web. Los plazos de respuesta aparecen únicamente cuando la propia aerolínea los publica, y siempre atribuidos («Iberia publica que su objetivo es…»). No hay estadísticas ni opiniones.
- **Nueva sección «Cómo reclamar a X, paso a paso».** Sustituye al párrafo genérico en las 12 aerolíneas con ficha: Iberia, Iberia Express, Vueling, Air Europa, Volotea, Binter, World2fly, easyJet, Jet2, TUI, Air France y British Airways. Las demás conservan el texto anterior.
- **Avisos con fuente** cuando lo que dice la aerolínea choca con la jurisprudencia. easyJet y Jet2 presentan las restricciones del control aéreo como causa que les exime de pagar; para vuelos con el reglamento europeo, el TJUE (C-108/26) exige que la aerolínea demuestre que la causa de fondo era extraordinaria.
- **Enlaces corregidos:**
  - Iberia Express: llevaba a la portada; ahora lleva a «Atención al cliente», con el formulario y la dirección postal. Se descartó «Solicitudes online», que es para bonos.
  - Volotea: llevaba a la portada del centro de ayuda; ahora lleva a la categoría «Claims».
- **Preguntas frecuentes:** la respuesta a «¿Dónde reclamo a X?» nombra el canal concreto en las aerolíneas con ficha.

## Datos comprobados por aerolínea (resumen)

- **Iberia:**
  - Formularios por retraso y por cancelación, y página de consulta del estado.
  - Pide el código de reserva y el número de billete, y envía un número de expediente por correo.
  - Se puede reclamar en nombre de otro con autorización.
  - Atiende en 9 idiomas.
  - Objetivo publicado: responder en 7 días laborables, o hasta 21 en casos complejos.
- **Vueling:** se reclama con un asistente de chat. Pide el código de reserva y el correo de compra, o el código, el aeropuerto de origen y la fecha.
- **Air Europa:**
  - El formulario pide el motivo, los apellidos y el localizador o el billete.
  - Vuelos UX-2000 a UX-3999: código compartido; hay que reclamar a la aerolínea que los operó.
  - Con billetes independientes no asume la pérdida del otro vuelo.
- **Volotea:**
  - Tres formularios, solo en inglés.
  - Recomienda esperar 7 días tras el vuelo.
  - Cada pasajero reclama por separado.
  - Objetivo publicado: 6 semanas.
  - Si no se está de acuerdo, remite al organismo de resolución alternativa de conflictos.
- **easyJet:**
  - Formulario en español.
  - Quien reclama tiene que ser un pasajero de la reserva, con el mismo nombre.
  - Pide la cuenta bancaria en la que cobrar.
- **Iberia Express:** formulario o correo postal a Calle Alcañiz 23, 1.ª planta, 28042 Madrid.
- **Jet2:**
  - Cuenta el retraso a la llegada.
  - Para pasajeros fuera del grupo familiar exige permiso firmado.
  - Por correo: EU261 Team, PO Box 284, Leeds LS11 1GE.
  - Objetivo publicado: contactar en 28 días.
  - Para escalar: CAA PACT, o AESA en vuelos que salen de España.
- **TUI:**
  - Solo vuelos TOM, BY u OR.
  - Envía un acuse automático y no da más avisos hasta la respuesta final.
  - Dice que responde en un plazo de 56 días.
- **Binter:** web oficial bintercanarias.com, con formulario de consultas o reclamaciones.
- **World2fly:** ahora W2Fly (w2fly.es). Apartado «Reclamaciones sobre servicios»; sus condiciones de transporte remiten a AESA o a la ANAC.
- **Air France:** formulario de reembolso, vale o compensación. Se añade que el vale solo vale si lo aceptas por escrito (art. 7.3).
- **British Airways:** chat solo en inglés; si reservaste con una agencia, las consultas se le hacen a ella.

## Sin comprobar

- **Ryanair:** `eu261expenseclaim.ryanair.com` no cargó en el navegador (navegación denegada o fallida). Sin ficha.
- **Las otras 31 aerolíneas:** el navegador de comprobación se desconectó antes de revisarlas. Siguen con el texto anterior. Es el siguiente lote, empezando por las que tienen más búsquedas en Search Console.

## SEO técnico

- No cambia ninguna URL ni ningún título: se compararon los 176 `<title>` con `main` y coinciden.
- Canonical, hreflang recíproco, sitemap (sin páginas fuera ni páginas inexistentes), JSON-LD y H1: `test_sitio.py` pasa sin errores.
- Datos estructurados: las páginas de aerolínea siguen con `BreadcrumbList`. No se añade `FAQPage`, porque Google ya no muestra ese resultado enriquecido para estos sitios.
- Cambian los 170 HTML porque cada página incluye la configuración de las aerolíneas para la calculadora, pero el contenido visible solo cambia en las 24 páginas con ficha.

## Pruebas nuevas (`test_sitio.py`)

- Ningún enlace oficial de reclamación puede ser una portada. Excepción: un subdominio dedicado a reclamaciones, como el de Ryanair. La prueba negativa con la antigua URL de Binter da error, como se esperaba.
- Cada ficha debe tener fecha, fuentes y URLs https, el mismo número de pasos en español e inglés, y aparecer completa en las dos páginas.
- Un plazo de respuesta solo se admite si se atribuye a la aerolínea.
