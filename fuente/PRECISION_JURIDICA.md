# Precisión jurídica: casos especiales (23-10-2026)

Clasificación de cada caso:

- **V:** regla verificada en la norma o la jurisprudencia.
- **I:** cuestión interpretativa.
- **D:** faltan datos.

Para I y D, la calculadora responde «Información insuficiente» y explica qué falta. Nunca responde «no» en esos casos.

## Resumen

| Caso | Clase | Antes | Ahora |
| --- | --- | --- | --- |
| Jersey, Guernsey, isla de Man | V + I | Siempre «insuficiente» | Cuentan como territorio de fuera para ambas normas. Con aerolínea británica o de la UE el vuelo queda cubierto. Con aerolínea local o desconocida, «insuficiente» |
| Gibraltar | V + I | Siempre «insuficiente», en euros | Igual que las islas: Gibraltar→Reino Unido con aerolínea británica, UK261. Nota sobre el acuerdo UE–Reino Unido de 2026 |
| Svalbard | V + I | Siempre «insuficiente» | Fuera del EEE: Oslo→Svalbard cubierto por salida; Svalbard→Oslo cubierto con aerolínea del EEE. Con otra aerolínea, «insuficiente» |
| Norte de Chipre (Ercan) | V | Siempre «insuficiente» | Fuera de la UE: Ercan→Estambul no está cubierto; desde la UE a Ercan, sí |
| Reino Unido ↔ UE | V | Correcto | **Error corregido:** SWISS e Icelandair no son «aerolínea comunitaria» para UK261. Norwegian y SAS: «insuficiente» |
| Clasificación dudosa de aerolíneas | V + D | — | Campo `ukcomm` en `airlines.json` |
| Huelga de empresa subcontratada | I | Contaba como circunstancia extraordinaria («no») | Opción propia que da «insuficiente» |
| Restricción de control aéreo | V | Correcto | Sin cambios; confirmado con C-108/26 |
| Retraso de 3 horas exactas | V | Correcto en el cálculo | Etiqueta «De 3 h justas a 4 h» y nota explicativa |
| Escalas y vuelos de conexión | V + I | No se preguntaba | Nueva pregunta «¿Hiciste escala?» |
| Billetes no disponibles al público | V | No se preguntaba | Nueva pregunta «El billete»; el de empleado o gratuito da «no» |

## Detalle y fuentes

### Jersey, Guernsey e isla de Man

- **V.** Ni el Reino Unido ni la UE. El art. 3.1 de UK261 cubre los vuelos «from a country other than the United Kingdom» que llegan al Reino Unido si la aerolínea es británica (licencia de la CAA, art. 2.m) o comunitaria (licencia de un Estado miembro, art. 2.c). El art. 3.1.b del Reglamento 261/2004 cubre las llegadas a la UE con aerolínea comunitaria. Las salidas desde el Reino Unido o la UE están cubiertas siempre.
- **I.** Según el Jersey Evening Post (18-07-2025), los vuelos de salida operados por aerolíneas con base en las islas no están cubiertos ni por EU261 ni por UK261. Jersey no tiene un régimen propio de compensación. No hemos verificado la licencia de esas aerolíneas, por eso la calculadora responde «insuficiente».

### Gibraltar

- **V.** El art. 1.3 del Reglamento 261/2004 suspendía su aplicación al aeropuerto de Gibraltar.
- **V.** UK261 suprimió esa suspensión el 31-12-2020 (S.I. 2019/278, reg. 8.2). Gibraltar no es el Reino Unido, así que se aplica el art. 3.1.b. CEDR (organismo ADR británico) confirma que los vuelos de Gibraltar están cubiertos por UK261.
- **D.** El acuerdo UE–Reino Unido sobre Gibraltar se aplica desde el 15-07-2026: Schengen en el aeropuerto y un capítulo de aviación. No hemos confirmado si extiende el Reglamento 261/2004 al aeropuerto. Se avisa en el resultado y, si la ruta no quedaría cubierta, la calculadora responde «insuficiente».

### Svalbard

- **V.** El Protocolo 40 del Acuerdo EEE permite a Noruega excluir Svalbard. Es lo comúnmente aceptado, pero no hemos localizado el acto noruego que lo hace, así que la calculadora trata Svalbard como territorio de fuera del EEE.
  - Oslo→Svalbard: cubierto por salida.
  - Svalbard→Oslo con aerolínea del EEE: cubierto por el art. 3.1.b.
  - El resultado es el mismo si Svalbard estuviera dentro del EEE.
- **I.** Con una aerolínea de fuera del EEE no sabemos si la ley noruega cubre el vuelo: la calculadora responde «insuficiente».

### Norte de Chipre

- **V.** El Protocolo 10 del Acta de adhesión de 2003 suspende la aplicación del acervo de la UE en las zonas donde el Gobierno de Chipre no ejerce un control efectivo.
  - Ercan cuenta como aeropuerto de fuera de la UE.
  - Desde la UE con escala en Turquía y una sola reserva: cubierto por la salida.
  - Ercan→Turquía: no cubierto.

### Reino Unido ↔ UE y licencias

- **V:** reglas de UK261 (legislation.gov.uk).
  - Art. 3.1.a: cubre toda salida desde el Reino Unido.
  - Art. 3.1.b.i: cubre la llegada al Reino Unido con aerolínea comunitaria o británica.
  - Art. 3.1.b.ii: cubre la llegada a la UE con aerolínea británica.
- **V:** qué aerolíneas cuentan como comunitarias en UK261. Su art. 2.c define «Community carrier» como la que tiene licencia de un Estado miembro, lo que excluye a Suiza, Noruega e Islandia.
- **Error corregido:** el motor trataba a SWISS e Icelandair como comunitarias también para UK261. El error solo afectaba a vuelos de fuera que llegan al Reino Unido.
- **D:** Norwegian y SAS operan con certificados de varios países, así que la calculadora pregunta qué filial operó el vuelo.

### Huelga de una empresa subcontratada

- **V.** La huelga del propio personal no exime (TJUE C-28/20).
- **V.** La de controladores o personal del aeropuerto «puede» eximir (Directrices de la Comisión C/2024/5687, punto 5.2.3).
- **I.** Ni el TJUE ni las Directrices aclaran el caso de empresas que trabajan para la aerolínea: handling, catering, limpieza. Antes la calculadora lo incluía en «circunstancia extraordinaria» y respondía «no». Ahora responde «insuficiente».

### Restricciones del control aéreo

- **V.** TJUE, C-108/26 (reexamen, 8-10-2026), que anula en parte la sentencia del Tribunal General T-134/25:
  - Una decisión de gestión del tráfico no es por sí sola una circunstancia extraordinaria.
  - La aerolínea debe probar que la causa de fondo era extraordinaria.
  - Solo se descuenta el retraso atribuible a esa causa.
- **V.** Retraso en cadena: Tribunal General, T-656/24 (4-03-2026). La decisión propia de la aerolínea de esperar a pasajeros de otro vuelo no le permite invocar la circunstancia extraordinaria del vuelo anterior.

### Retrasos de exactamente 3 horas

- **V.** El retraso tiene que ser de «tres horas o más» (TJUE, C-402/07 Sturgeon) y se mide al abrirse las puertas en el destino final (C-452/13).
  - 180 minutos dan derecho a compensación; 179, no.
  - 240 minutos siguen en el tramo de la mitad (art. 7.2.c: «no más de cuatro horas»).
- Ya estaba bien calculado y lo comprueban `test_oraculo.js` y `test_reglas.js`.

### Escalas

- **V.** Con una sola reserva, el viaje cuenta como un todo (C-451/20). El retraso se mide en el destino final (C-11/11) y la distancia es la línea recta entre origen y destino final (C-559/16).
- **V.** Si el viaje empieza y termina fuera, una escala en la UE no lo cubre (C-451/20; Directrices, punto 2.1.4).
- **V.** Si sale de la UE, está cubierto aunque el tramo afectado lo opere una aerolínea de fuera (C-502/18; Directrices, punto 4.4.8).
- **V.** UK261, art. 3.1A: el viaje cuenta entero y como salida desde el primer tramo.
- **I.** Si el viaje llega a la UE o al Reino Unido desde fuera con aerolíneas distintas, ningún tribunal ha aclarado qué aerolínea decide la cobertura del art. 3.1.b: la calculadora responde «insuficiente».
- Con reservas separadas, cada vuelo se valora por separado: se muestra un aviso.

### Billetes no disponibles al público

- **V.** El art. 3.3 de ambas normas excluye los billetes gratuitos y las tarifas reducidas no disponibles al público (por ejemplo, los de empleado). En cambio, cubre los billetes de programas de fidelización o comerciales.
- **I (sin regla en la calculadora).** Las Directrices (punto 2.2.2) excluyen a los bebés que viajan gratis sin asiento. No hemos verificado el caso del bebé que paga una tarifa reducida, así que no se ha añadido ninguna regla.

## Pruebas

- `test_reglas.js`: 116 casos y 471 comprobaciones. Se añadieron 28 casos de esta tarea.
- `test_oraculo.js`: incluye GIB, JER, IOM, LYR y ECN y una aerolínea con licencia suiza. 19.264 casos y 0 discrepancias.
- `test_sitio.py`: 178 páginas, sin errores.
- `test_navegador.js`: 84 comprobaciones correctas.

## Fuentes

- Reglamento (CE) 261/2004, arts. 1, 2 y 3.
- UK261: [legislation.gov.uk, art. 1](https://www.legislation.gov.uk/eur/2004/261/article/1), [art. 2](https://www.legislation.gov.uk/eur/2004/261/article/2) y [art. 3](https://www.legislation.gov.uk/eur/2004/261/article/3).
- [Directrices interpretativas de la Comisión, C/2024/5687](https://eur-lex.europa.eu/eli/C/2024/5687/oj/eng).
- TJUE: [comunicado de C-108/26](https://curia.europa.eu/site/upload/docs/application/pdf/2026-10/cp260144en.pdf) y C-451/20, C-502/18, C-559/16, C-11/11, C-402/07, C-452/13, C-28/20, C-74/19.
- Tribunal General: [T-656/24](https://curia.europa.eu/site/upload/docs/application/pdf/2026-03/cp260026es.pdf) y [T-134/25](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex%3A62025TJ0134).
- [Acuerdo EEE, Protocolo 40](https://www.legislation.gov.uk/eut/eea-agreement/attachment/43/data.xht).
- [CEDR, derechos de los pasajeros tras el Brexit](https://www.cedr.com/wp-content/uploads/2022/03/Air-Passenger-Rights-following-the-UKs-withdrawal-from-the-EU.pdf).
- [Exteriores: Acuerdo sobre Gibraltar](https://www.exteriores.gob.es/en/Comunicacion/Exteriores-explica/Paginas/2026_Articulos/El-Acuerdo-con-respecto-a-Gibraltar-cuando-se-aplica-y-que-supone-para-Espana.aspx).
- [Jersey Evening Post, 18-07-2025](https://jerseyeveningpost.com/news/2025/07/18/irresponsible-to-bring-in-airline-compensation-scheme-without-analysis-says-minister/).
