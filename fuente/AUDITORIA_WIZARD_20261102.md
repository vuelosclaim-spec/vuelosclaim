# Revisión del asistente y localización — 2 noviembre 2026

## Cambios preparados

- Volver desde el resultado al cuarto paso para modificar la aerolínea, billete o causa, conservando los datos.
- En pasos 3 y 4, impedir avanzar si hay un grupo de opciones visible sin selección. La respuesta explícita «no lo sé» sigue siendo válida.
- Aviso jurídico breve y visible en ES, EN, IT y DE, incluso con el razonamiento detallado plegado.
- Nuevo evento de GA4 `wizard_step_viewed` con parámetro de lista cerrada `wizard_step` (1–5). No se envían respuestas, rutas, nombres ni números de reserva. Solo se emite cuando el visitante consiente la analítica.

## Límites importantes

**No considerar `wizard_step_viewed` una medición exhaustiva de abandonos.** Permite ver el embudo agregado entre pasos, condicionado al consentimiento. Los eventos no garantizan entrega en cierres bruscos, bloqueadores o navegación inmediata. Configurar `wizard_step` como dimensión personalizada de ámbito evento en GA4 cuando esté desplegado y comparar volúmenes por pasos y sesiones.

**No actualizar automáticamente la fecha de revisión jurídica** de 7 de octubre: subirla sin revisar realmente todas las normas y el contenido de IT/DE sería engañoso. Las páginas legales de italiano y alemán todavía enlazan la versión inglesa. Hace falta una revisión local de ENAC, entidades ADR alemanas, condiciones nacionales y textos legales antes de llamar completas a esas versiones.

**No fusionar la PR #30** mientras la fuente oficial no confirme el estado de la huelga de easyJet Italia del 6 de noviembre. La discrepancia entre fuentes debe resolverse fuera de un cambio de interfaz.

## Integración pendiente obligatoria

El generador `fuente/build.py` incluye `src/app.js` **dentro de los HTML** al generar `docs/`. Por ello, una PR que actualice `src/app.js` sin regenerar `docs/` dejaría la web pública con el código antiguo. Regenerar `python3 fuente/build.py` sobre el `main` más reciente, incluir los HTML cambiados y superar todas las pruebas antes de fusionar.

Pruebas requeridas: `test_reglas.js`, `test_oraculo.js`, `test_idiomas.py` (si existe), `test_sitio.py`, `test_mantenimiento.py`, `test_monetizacion.py`, y navegador/Playwright con avance, retroceso, campos sin respuesta, teclado, modo móvil y consentimiento.
