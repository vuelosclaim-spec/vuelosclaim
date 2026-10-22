// Pruebas del motor de reglas de la calculadora (src/app.js), sin dependencias: `node fuente/tests/test_reglas.js`.
// Carga app.js en un entorno mínimo (sin DOM: init() no hace nada) y llama a window.CTT_compute.
// Fuentes de las reglas: Reglamento (CE) 261/2004 (arts. 2, 3, 4, 5, 7), FAQ de la Comisión Europea,
// AESA (cancelaciones y plazos), CAA (tabla de aplicación de UK261 y cancelaciones) y la jurisprudencia citada en cada caso.
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.join(__dirname, "..");
const airports = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "airports.min.json"), "utf8"));
const airlines = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "airlines.json"), "utf8"));
const byCode = Object.fromEntries(airports.map((a) => [a[0], a]));

function load(lang) {
  const window = { CTT: { lang, airlines: airlines.map((a) => ({ slug: a.slug, eu: a.eu, uk: a.uk })) } };
  const document = { readyState: "complete", getElementById: () => null, addEventListener() {} };
  const ctx = vm.createContext({ window, document, location: { search: "" }, URLSearchParams, URL, fetch: () => Promise.reject(new Error("sin red")), console });
  vm.runInContext(fs.readFileSync(path.join(ROOT, "src", "app.js"), "utf8"), ctx);
  return window;
}
const W = { es: load("es"), en: load("en") };
const al = (x) => (typeof x === "string" ? airlines.find((a) => a.slug === x) : x) || { eu: "unknown" };

// Cada caso: [descripción, entrada, veredicto, importe, moneda (opcional), comprobación extra (opcional)]
// Entrada: r=ruta "MAD-BCN", a=aerolínea; el resto se pasa tal cual a compute().
const D = { what: "delay", delay: "gt4", cause: "unknown" };
const C = (x) => Object.assign({ what: "cancel", cause: "unknown" }, x);
const B = (x) => Object.assign({ what: "denied", denied: "invol", checkin: "yes", dreason: "overbooking" }, x);
const has = (key) => (r, t) => r.lines.concat(r.notes).includes(typeof t[key] === "function" ? t[key]("") : t[key]);
const hasC = (key) => (r, t) => r.lines.includes(t.c[key]);

const CASES = [
  // ---- Cobertura territorial (art. 3; tabla de la CAA para UK261) ----
  ["Sale de la UE, aerolínea europea", { r: "MAD-BCN", a: "vueling", ...D }, "posible", 250, "EUR", has("regEU")],
  ["Sale de la UE con aerolínea no europea: cubierto", { r: "MAD-JFK", a: "emirates", ...D }, "posible", 600, "EUR"],
  ["Llega a la UE desde fuera con aerolínea europea", { r: "JFK-MAD", a: "iberia", ...D }, "posible", 600, "EUR", has("reg3EU")],
  ["Llega a la UE desde fuera con aerolínea no europea: no cubierto", { r: "JFK-MAD", a: "emirates", ...D }, "no", 0, null, has("notIn")],
  ["Llega a la UE con aerolínea desconocida: faltan datos", { r: "DXB-MAD", a: { eu: "unknown" }, ...D }, "insuficiente", 600, "EUR", (r, t) => r.missing.includes(t.mCarrier)],
  ["Llega a la UE con aerolínea mixta (easyJet): UE con aviso", { r: "RAK-MAD", a: "easyjet", ...D }, "posible", 250, "EUR", has("mixed")],
  ["Llega a la UE desde fuera con aerolínea británica: UK261", { r: "JFK-MAD", a: { eu: "no", uk: true }, ...D }, "posible", 520, "GBP", has("reg3EUuk")],
  ["Ni sale ni llega a Europa, aunque la aerolínea sea europea", { r: "JFK-BOS", a: "iberia", ...D }, "no", 0, null, has("not3")],
  ["Sale del Reino Unido: UK261 en libras", { r: "MAN-ALC", a: "jet2", ...D }, "posible", 350, "GBP", has("regUK")],
  ["Sale de España con aerolínea británica: EU261 y aviso de UK261", { r: "ALC-MAN", a: "jet2", ...D }, "posible", 400, "EUR", has("alsoUK")],
  ["Sale del Reino Unido a la UE con aerolínea europea: aviso doble régimen", { r: "LGW-MAD", a: "iberia", ...D }, "posible", 220, "GBP", has("alsoEU")],
  ["Sale del Reino Unido con aerolínea no europea: UK261", { r: "LHR-DXB", a: "emirates", ...D }, "posible", 520, "GBP"],
  ["Llega al Reino Unido desde fuera con aerolínea británica", { r: "JFK-LHR", a: "virgin-atlantic", ...D }, "posible", 520, "GBP", has("regUKin")],
  ["Llega al Reino Unido desde fuera con aerolínea europea", { r: "JFK-LHR", a: "iberia", ...D }, "posible", 520, "GBP"],
  ["Llega al Reino Unido desde fuera con aerolínea no europea", { r: "DXB-LHR", a: "emirates", ...D }, "no", 0],
  ["Llega al Reino Unido con aerolínea desconocida", { r: "JFK-LHR", a: { eu: "unknown" }, ...D }, "insuficiente", 520, "GBP"],
  ["Suiza cuenta como UE", { r: "ZRH-MAD", a: "swiss", ...D }, "posible", 250, "EUR"],
  ["Islandia (EEE) cuenta como UE", { r: "KEF-MAD", a: { eu: "no" }, ...D }, "posible", 400, "EUR"],
  ["Salida de Guernsey: régimen propio, faltan datos", { r: "GCI-LGW", a: { eu: "no", uk: true }, ...D }, "insuficiente", 220, "GBP", has("special")],
  ["Salida del Reino Unido a Guernsey: UK261", { r: "LGW-GCI", a: { eu: "no", uk: true }, ...D }, "posible", 220, "GBP"],
  ["Salida de Gibraltar: faltan datos", { r: "GIB-LHR", a: "british-airways", ...D }, "insuficiente", 400, "EUR"],
  ["Salida de España a Gibraltar: EU261", { r: "MAD-GIB", a: "iberia", ...D }, "posible", 250, "EUR"],
  ["Salida de Svalbard: faltan datos", { r: "LYR-OSL", a: { eu: "yes" }, ...D }, "insuficiente", 400, "EUR"],
  ["Salida del norte de Chipre: faltan datos", { r: "ECN-IST", a: { eu: "no" }, ...D }, "insuficiente", 250, "EUR"],
  ["Región ultraperiférica: París–Reunión es intra-UE", { r: "CDG-RUN", a: "air-france", ...D }, "posible", 400, "EUR"],

  // ---- Distancia: límites exactos (art. 7.1) ----
  ["1.500 km exactos: 250 €", { r: "MAD-JFK", a: "iberia", distKm: 1500, ...D }, "posible", 250, "EUR"],
  ["1.501 km: 400 €", { r: "MAD-JFK", a: "iberia", distKm: 1501, ...D }, "posible", 400, "EUR"],
  ["3.500 km exactos: 400 €", { r: "MAD-JFK", a: "iberia", distKm: 3500, ...D }, "posible", 400, "EUR"],
  ["3.501 km fuera de la UE: 600 €", { r: "MAD-JFK", a: "iberia", distKm: 3501, ...D }, "posible", 600, "EUR"],
  ["3.501 km dentro de la UE: 400 €", { r: "MAD-BCN", a: "iberia", distKm: 3501, ...D }, "posible", 400, "EUR"],
  ["Intra-UE real de más de 3.500 km (LPA–HEL): 400 €", { r: "LPA-HEL", a: "finnair", ...D }, "posible", 400, "EUR"],
  ["UK261 1.500 km: 220 £", { r: "LHR-JFK", a: "jet2", distKm: 1500, ...D }, "posible", 220, "GBP"],
  ["UK261 1.501 km: 350 £", { r: "LHR-JFK", a: "jet2", distKm: 1501, ...D }, "posible", 350, "GBP"],
  ["UK261 3.501 km: 520 £", { r: "LHR-JFK", a: "jet2", distKm: 3501, ...D }, "posible", 520, "GBP"],

  // ---- Retrasos: límites exactos (Sturgeon C-402/07; art. 7.2.c) ----
  ["179 min: sin compensación", { r: "MAD-JFK", a: "iberia", ...D, delayMin: 179 }, "no", 0, null, has("lt3")],
  ["180 min (3 h exactas) corto radio: 250 €", { r: "MAD-BCN", a: "iberia", ...D, delayMin: 180 }, "posible", 250, "EUR"],
  ["180 min largo radio: mitad, 300 €", { r: "MAD-JFK", a: "iberia", ...D, delayMin: 180 }, "posible", 300, "EUR"],
  ["240 min (4 h exactas) largo radio: mitad, 300 €", { r: "MAD-JFK", a: "iberia", ...D, delayMin: 240 }, "posible", 300, "EUR"],
  ["241 min largo radio: 600 €", { r: "MAD-JFK", a: "iberia", ...D, delayMin: 241 }, "posible", 600, "EUR"],
  ["Intra-UE >3.500 km con 3-4 h: sin reducción, 400 €", { r: "LPA-HEL", a: "finnair", ...D, delayMin: 200 }, "posible", 400, "EUR"],
  ["UK261 largo radio 3-4 h: 260 £", { r: "LHR-JFK", a: "virgin-atlantic", ...D, delay: "3to4" }, "posible", 260, "GBP"],
  ["Retraso: opción 'menos de 3 h'", { r: "MAD-BCN", a: "vueling", ...D, delay: "lt3" }, "no", 0],
  ["Retraso desconocido: faltan datos", { r: "MAD-BCN", a: "vueling", ...D, delay: "unknown" }, "insuficiente", 250, "EUR", (r, t) => r.missing.includes(t.mDelay)],

  // ---- Cancelaciones: aviso (art. 5.1.c) ----
  ["Aviso de 14 días exactos: sin compensación", C({ r: "MAD-BCN", a: "vueling", noticeDays: 14 }), "no", 0, null, has("gt14")],
  ["Aviso de 13 días sin datos del alternativo: faltan datos", C({ r: "MAD-BCN", a: "vueling", noticeDays: 13 }), "insuficiente", 250, "EUR", has("n7to14")],
  ["Aviso de 7 días: tramo de 7 a 13", C({ r: "MAD-BCN", a: "vueling", noticeDays: 7, reroute: "no" }), "posible", 250, "EUR", has("n7to14")],
  ["Aviso de 6 días: tramo de menos de 7", C({ r: "MAD-BCN", a: "vueling", noticeDays: 6, reroute: "no" }), "posible", 250, "EUR", has("nlt7")],
  ["Aviso desconocido: faltan datos", C({ r: "MAD-BCN", a: "vueling", notice: "unknown" }), "insuficiente", 250, "EUR", (r, t) => r.missing.includes(t.mNotice)],
  ["Menos de 7 días sin alternativo: compensación", C({ r: "MAD-BCN", a: "vueling", notice: "lt7", reroute: "no" }), "posible", 250, "EUR", has("rerouteNo")],
  ["Menos de 7 días sin saber si hubo alternativo: no se concede", C({ r: "MAD-BCN", a: "vueling", notice: "lt7", reroute: "unknown" }), "insuficiente", 250, "EUR"],
  ["Menos de 7 días, opción por defecto: no se concede", C({ r: "MAD-BCN", a: "vueling", notice: "lt7" }), "insuficiente", 250, "EUR"],

  // ---- Cancelaciones: márgenes del vuelo alternativo, en minutos ----
  ["<7 d: sale 60 min antes y llega 119 min tarde: exenta", C({ r: "MAD-BCN", a: "vueling", notice: "lt7", reroute: "yes", rerouteDepEarlyMin: 60, rerouteArrLateMin: 119 }), "no", 0, null, has("exempt")],
  ["<7 d: sale 61 min antes: no exenta (y art. 7.2: mitad)", C({ r: "MAD-BCN", a: "vueling", notice: "lt7", reroute: "yes", rerouteDepEarlyMin: 61, rerouteArrLateMin: 0 }), "posible", 125, "EUR", has("notExempt")],
  ["<7 d: llega 120 min tarde: no exenta, mitad (≤2 h)", C({ r: "MAD-BCN", a: "vueling", notice: "lt7", reroute: "yes", rerouteDepEarlyMin: 0, rerouteArrLateMin: 120 }), "posible", 125, "EUR"],
  ["<7 d: llega 121 min tarde: compensación completa", C({ r: "MAD-BCN", a: "vueling", notice: "lt7", reroute: "yes", rerouteDepEarlyMin: 0, rerouteArrLateMin: 121 }), "posible", 250, "EUR"],
  ["7-13 d: sale 120 min antes y llega 239 min tarde: exenta", C({ r: "MAD-BCN", a: "vueling", notice: "7to14", reroute: "yes", rerouteDepEarlyMin: 120, rerouteArrLateMin: 239 }), "no", 0],
  ["7-13 d: sale 121 min antes: no exenta", C({ r: "MAD-BCN", a: "vueling", notice: "7to14", reroute: "yes", rerouteDepEarlyMin: 121, rerouteArrLateMin: 0 }), "posible", 125, "EUR"],
  ["7-13 d: llega 240 min tarde: no exenta, completa en corto radio", C({ r: "MAD-BCN", a: "vueling", notice: "7to14", reroute: "yes", rerouteDepEarlyMin: 120, rerouteArrLateMin: 240 }), "posible", 250, "EUR"],
  ["7-13 d largo radio: llega 240 min tarde: mitad (≤4 h)", C({ r: "MAD-JFK", a: "iberia", notice: "7to14", reroute: "yes", rerouteDepEarlyMin: 0, rerouteArrLateMin: 240 }), "posible", 300, "EUR"],
  ["7-13 d largo radio: llega 241 min tarde: 600 €", C({ r: "MAD-JFK", a: "iberia", notice: "7to14", reroute: "yes", rerouteDepEarlyMin: 0, rerouteArrLateMin: 241 }), "posible", 600, "EUR"],
  ["<7 d tramo 2: llega 180 min tarde: mitad (≤3 h)", C({ r: "MAD-BCN", a: "vueling", distKm: 2000, notice: "lt7", reroute: "yes", rerouteDepEarlyMin: 0, rerouteArrLateMin: 180 }), "posible", 200, "EUR"],
  ["<7 d tramo 2: llega 181 min tarde: 400 €", C({ r: "MAD-BCN", a: "vueling", distKm: 2000, notice: "lt7", reroute: "yes", rerouteDepEarlyMin: 0, rerouteArrLateMin: 181 }), "posible", 400, "EUR"],

  // ---- Cancelaciones: opciones del formulario ----
  ["<7 d, alternativo ≤1 h antes y <2 h tarde: exenta", C({ r: "MAD-BCN", a: "vueling", notice: "lt7", reroute: "yes", rdep: "le1", rarr: "lt2" }), "no", 0],
  ["<7 d, alternativo 1-2 h antes: no exenta", C({ r: "MAD-BCN", a: "vueling", notice: "lt7", reroute: "yes", rdep: "1to2", rarr: "lt2" }), "posible", 125, "EUR"],
  ["<7 d, llega 2-4 h tarde: no exenta, completa", C({ r: "MAD-BCN", a: "vueling", notice: "lt7", reroute: "yes", rdep: "le1", rarr: "2to4" }), "posible", 250, "EUR"],
  ["7-13 d, 1-2 h antes y 2-4 h tarde: exenta", C({ r: "MAD-BCN", a: "vueling", notice: "7to14", reroute: "yes", rdep: "1to2", rarr: "2to4" }), "no", 0],
  ["7-13 d, llega 4 h o más tarde: no exenta", C({ r: "MAD-BCN", a: "vueling", notice: "7to14", reroute: "yes", rdep: "le1", rarr: "ge4" }), "posible", 250, "EUR"],
  ["7-13 d, más de 2 h antes: no exenta aunque falte la llegada", C({ r: "MAD-BCN", a: "vueling", notice: "7to14", reroute: "yes", rdep: "gt2", rarr: "unknown" }), "posible", 250, "EUR"],
  ["<7 d, salida del alternativo desconocida: faltan datos", C({ r: "MAD-BCN", a: "vueling", notice: "lt7", reroute: "yes", rdep: "unknown", rarr: "lt2" }), "insuficiente", 125, "EUR", (r, t) => r.missing.includes(t.mRerouteTimes)],
  ["Tramo 2 con llegada 2-4 h: completa y aviso de posible reducción", C({ r: "MAD-BCN", a: "vueling", distKm: 2000, notice: "lt7", reroute: "yes", rdep: "le1", rarr: "2to4" }), "posible", 400, "EUR", (r, t) => r.notes.includes(t.reduceMaybe("200 €"))],
  ["Rechazó el alternativo: aviso de reembolso", C({ r: "MAD-BCN", a: "vueling", notice: "lt7", reroute: "yes", rdep: "gt2", rarr: "ge4", accepted: "no" }), "posible", 250, "EUR", has("rejected")],
  ["Cancelación por meteorología: no parece", C({ r: "MAD-BCN", a: "vueling", notice: "lt7", reroute: "no", cause: "weather" }), "no", 0, null, (r) => r.potential === 250],
  ["Cancelación por restricción ATC: faltan datos", C({ r: "MAD-BCN", a: "vueling", notice: "lt7", reroute: "no", cause: "atc" }), "insuficiente", 250, "EUR"],

  // ---- Denegación de embarque (arts. 2.j, 3.2, 4) ----
  ["Overbooking involuntario: compensación", B({ r: "MAD-BCN", a: "vueling" }), "posible", 250, "EUR", has("overbook")],
  ["Overbooking: las circunstancias extraordinarias no eximen (C-22/11)", B({ r: "MAD-BCN", a: "vueling", cause: "weather" }), "posible", 250, "EUR", has("deniedNoExtra")],
  ["Cesión voluntaria: sin compensación fija", B({ r: "MAD-BCN", a: "vueling", denied: "vol" }), "no", 0, null, has("vol")],
  ["No sabe si fue voluntario: faltan datos", B({ r: "MAD-BCN", a: "vueling", denied: "unknown" }), "insuficiente", 250, "EUR"],
  ["No se presentó a tiempo: sin compensación", B({ r: "MAD-BCN", a: "vueling", checkin: "no" }), "no", 0, null, has("checkinNo")],
  ["No sabe si llegó a tiempo: faltan datos", B({ r: "MAD-BCN", a: "vueling", checkin: "unknown" }), "insuficiente", 250, "EUR"],
  ["Motivos razonables (salud, seguridad, documentos): sin compensación", B({ r: "MAD-BCN", a: "vueling", dreason: "reasonable" }), "no", 0, null, has("reasonable")],
  ["Motivo no explicado: posible (C-321/11)", B({ r: "MAD-BCN", a: "vueling", dreason: "unknown" }), "posible", 250, "EUR", has("reasonUnknown")],
  ["Opciones por defecto del formulario: faltan datos", { r: "MAD-BCN", a: "vueling", what: "denied", denied: "unknown", checkin: "unknown", dreason: "unknown" }, "insuficiente", 250, "EUR"],

  // ---- Circunstancias extraordinarias (art. 5.3 y jurisprudencia) ----
  ["Sin motivo: posible", { r: "MAD-BCN", a: "vueling", ...D }, "posible", 250, "EUR", hasC("unknown")],
  ["Avería técnica ordinaria: posible (C-549/07)", { r: "MAD-BCN", a: "vueling", ...D, cause: "tech" }, "posible", 250, "EUR", hasC("tech")],
  ["Tripulación: posible (C-156/22)", { r: "MAD-BCN", a: "vueling", ...D, cause: "crew" }, "posible", 250, "EUR", hasC("crew")],
  ["Huelga del personal propio: posible (C-28/20)", { r: "MAD-BCN", a: "vueling", ...D, cause: "strike_own" }, "posible", 250, "EUR", has("strikeOwnNote")],
  ["Huelga ajena: no parece", { r: "MAD-BCN", a: "vueling", ...D, cause: "strike_ext" }, "no", 0, null, (r) => r.potential === 250],
  ["Meteorología: no parece, con importe si no lo prueba", { r: "MAD-BCN", a: "vueling", ...D, cause: "weather" }, "no", 0, null, (r, t) => r.notes.includes(t.extraNote("250 €"))],
  ["Seguridad: no parece", { r: "MAD-BCN", a: "vueling", ...D, cause: "security" }, "no", 0],
  ["Ave u objeto en pista: no parece (C-315/15)", { r: "MAD-BCN", a: "vueling", ...D, cause: "bird" }, "no", 0],
  ["Restricción ATC: faltan datos (C-108/26)", { r: "MAD-BCN", a: "vueling", ...D, cause: "atc" }, "insuficiente", 250, "EUR", (r, t) => r.missing.includes(t.mAtc)],
  ["Retraso del vuelo anterior: faltan datos (C-74/19, T-656/24)", { r: "MAD-BCN", a: "vueling", ...D, cause: "knock" }, "insuficiente", 250, "EUR", (r, t) => r.missing.includes(t.mKnock)],
  ["Valor antiguo 'strike' = huelga propia", { r: "MAD-BCN", a: "vueling", ...D, cause: "strike" }, "posible", 250, "EUR"],
  ["Valor antiguo 'extra' = circunstancia extraordinaria", { r: "MAD-BCN", a: "vueling", ...D, cause: "extra" }, "no", 0],
  ["Menos de 3 h con huelga propia: sigue sin compensación", { r: "MAD-BCN", a: "vueling", ...D, delay: "lt3", cause: "strike_own" }, "no", 0],
];

let fail = 0, ok = 0;
function check(name, got, exp) { if (got) ok++; else { fail++; console.log(`FALLO  ${name}  ${exp}`); } }

for (const [name, inp, verdict, amount, cur, extra] of CASES) {
  const [d, a] = inp.r.split("-");
  const o = Object.assign({}, inp, { dep: byCode[d], arr: byCode[a], airline: al(inp.a) });
  if (!o.dep || !o.arr) { fail++; console.log(`FALLO  ${name}: aeropuerto desconocido ${inp.r}`); continue; }
  const r = W.es.CTT_compute(o);
  const en = W.en.CTT_compute(o);
  const good = r.verdict === verdict && r.amount === amount && (!cur || r.cur === cur);
  check(name, good, `(esperado ${verdict} ${amount} ${cur || ""}, obtenido ${r.verdict} ${r.amount} ${r.cur})`);
  if (extra) check(name + " [explicación]", extra(r, W.es.CTT_strings.es), "(falta el texto esperado)");
  // Paridad ES/EN: mismo resultado y el mismo número de explicaciones
  check(name + " [ES/EN]", en.verdict === r.verdict && en.amount === r.amount && en.lines.length === r.lines.length &&
    en.notes.length === r.notes.length && en.missing.length === r.missing.length, "(la versión inglesa da otro resultado)");
  // Coherencia: "insuficiente" siempre dice qué falta; "posible" nunca tiene datos pendientes; todo resultado se explica
  check(name + " [coherencia]", (r.verdict !== "insuficiente" || r.missing.length > 0) && (r.verdict !== "posible" || (r.missing.length === 0 && r.amount > 0)) &&
    (r.verdict !== "no" || r.amount === 0) && r.lines.length > 0 && !/undefined|NaN/.test(JSON.stringify(r) + JSON.stringify(en)), "(resultado incoherente)");
}

// Todas las claves de texto existen en los dos idiomas
const S = W.es.CTT_strings;
function keys(x, p) { return Object.keys(x).flatMap((k) => (x[k] && typeof x[k] === "object" && !Array.isArray(x[k]) ? keys(x[k], p + k + ".") : [p + k])); }
const kes = keys(S.es, ""), ken = keys(S.en, "");
check("Textos ES y EN con las mismas claves", kes.length === ken.length && kes.every((k) => ken.includes(k)), `(solo ES: ${kes.filter((k) => !ken.includes(k))}; solo EN: ${ken.filter((k) => !kes.includes(k))})`);

// Cartas: organismo correcto según el régimen y el país, y hechos de la cancelación
function letterFor(lang, route, inp) {
  const [d, a] = route.split("-");
  const o = Object.assign({ dep: byCode[d], arr: byCode[a], airline: al(inp.a) }, inp);
  const r = W[lang].CTT_compute(o);
  const dd = { n: 1, name: "N", flight: "F", booking: "B", date: "01/01/2026", iban: "", route: route, today: "01/01/2026" };
  return W[lang].CTT_letters[lang]({ r, o, dep: o.dep, arr: o.arr, airline: "X" }, dd);
}
check("Carta ES desde España cita AESA", letterFor("es", "MAD-BCN", { a: "vueling", ...D }).includes("AESA"), "");
check("Carta ES desde Francia no cita AESA", !letterFor("es", "CDG-MAD", { a: "air-france", ...D }).includes("AESA"), "");
check("Carta ES desde Reino Unido cita la CAA", letterFor("es", "MAN-ALC", { a: "jet2", ...D }).includes("CAA"), "");
check("Carta EN desde Reino Unido cita UK261 y la CAA", /UK261[\s\S]*CAA/.test(letterFor("en", "MAN-ALC", { a: "jet2", ...D })), "");
check("Carta de cancelación sin alternativo lo dice", letterFor("es", "MAD-BCN", C({ a: "vueling", notice: "lt7", reroute: "no" })).includes("No se me ofreció"), "");
check("Carta de cancelación con alternativo fuera de márgenes lo describe", letterFor("en", "MAD-BCN", C({ a: "vueling", notice: "lt7", reroute: "yes", rdep: "gt2", rarr: "ge4" })).includes("outside the limits"), "");

// ---- Base de aeropuertos: formato, coordenadas y distancias ----
check("Aeropuertos: más de 3.000 y sin códigos repetidos", airports.length > 3000 && new Set(airports.map((a) => a[0])).size === airports.length, "");
check("Aeropuertos: formato [IATA, nombre, ciudad, país, lat, lon, UE]", airports.every((a) => a.length === 7 && /^[A-Z0-9]{3}$/.test(a[0]) && a[1] && /^[A-Z]{2}$/.test(a[3]) &&
  a[4] >= -90 && a[4] <= 90 && a[5] >= -180 && a[5] <= 180 && (a[6] === 0 || a[6] === 1)), "");
// Distancias ortodrómicas de referencia (±1 %): calculadas con las coordenadas oficiales de los aeropuertos
for (const [r, ref] of [["MAD-BCN", 483], ["MAD-JFK", 5767], ["LHR-JFK", 5555], ["SYD-LAX", 12051]]) {
  const [d, a] = r.split("-");
  const km = W.es.CTT_compute({ dep: byCode[d], arr: byCode[a], airline: { eu: "yes" }, what: "delay", delay: "gt4" }).dist;
  check(`Distancia ${r} ≈ ${ref} km (obtenido ${km})`, Math.abs(km - ref) / ref < 0.01, "");
}
// Ciudades con varios aeropuertos: deben estar en la base y tener coordenadas distintas
for (const set of [["LHR", "LGW", "STN", "LTN", "LCY"], ["CDG", "ORY"], ["JFK", "EWR", "LGA"], ["TFN", "TFS"], ["FCO", "CIA"]]) {
  check(`Aeropuertos distintos: ${set}`, set.every((c) => byCode[c]) && new Set(set.map((c) => byCode[c][4] + "," + byCode[c][5])).size === set.length, "");
}

// ---- Autocompletado: códigos IATA, ciudades, nombres, alias, acentos ----
const findES = (q) => W.es.CTT_search(q, airports).map((a) => a[0]);
const findEN = (q) => W.en.CTT_search(q, airports).map((a) => a[0]);
const SEARCH = [
  ["Código en mayúsculas", findES("MAD")[0] === "MAD"],
  ["Código en minúsculas", findES("bcn")[0] === "BCN"],
  ["Código exacto aunque haya muchas coincidencias parciales (san)", findES("san")[0] === "SAN"],
  ["Ciudad", findES("madrid")[0] === "MAD"],
  ["Ciudad sin acento (malaga)", findES("malaga")[0] === "AGP"],
  ["Ciudad con acento (Málaga)", findES("Málaga")[0] === "AGP"],
  ["Nombre del aeropuerto (barajas)", findES("barajas").includes("MAD")],
  ["Nombre del aeropuerto (gatwick)", findES("gatwick")[0] === "LGW"],
  ["Nombre del aeropuerto (heathrow)", findES("heathrow")[0] === "LHR"],
  ["Alias en español (Londres) devuelve los 5 aeropuertos", ["LHR", "LGW", "STN", "LTN", "LCY"].every((c) => findES("londres").includes(c))],
  ["Alias en español (Nueva York)", findES("nueva york").slice(0, 3).includes("JFK")],
  ["En inglés (London)", ["LHR", "LGW", "STN"].every((c) => findEN("london").includes(c))],
  ["Ciudad con dos aeropuertos (Tenerife)", ["TFN", "TFS"].every((c) => findES("tenerife").includes(c))],
  ["Varias palabras (londres gatwick)", findES("londres gatwick")[0] === "LGW"],
  ["Texto tal como queda al elegir (Madrid (MAD))", findES("Madrid (MAD)")[0] === "MAD"],
  ["Espacios sobrantes", findES("  bcn ")[0] === "BCN"],
  ["Sin coincidencias", findES("zzqxw").length === 0],
  ["Como mucho 8 sugerencias", findES("a").length <= 8],
];
for (const [n, ok2] of SEARCH) check("Búsqueda: " + n, ok2, "");

// ---- Cartas: sin datos bancarios, sin afirmar un derecho seguro, reflejan el resultado ----
const LTR = [
  ["es", "MAD-BCN", { a: "vueling", ...D, cause: "tech" }],
  ["en", "MAN-ALC", { a: "jet2", ...D }],
  ["es", "MAD-JFK", { a: "iberia", ...D, delay: "3to4" }],
  ["es", "MAD-BCN", C({ a: "vueling", notice: "lt7", reroute: "yes", rdep: "1to2", rarr: "lt2", accepted: "yes" })],
  ["en", "MAD-BCN", B({ a: "vueling", dreason: "unknown" })],
];
for (const [lang, route, inp] of LTR) {
  const t = letterFor(lang, route, inp);
  const tag = `Carta ${lang} ${route} ${inp.what}`;
  check(tag + ": sin IBAN ni cuenta bancaria", !/IBAN|cuenta [A-Z0-9]|account [A-Z0-9]|\[iban/i.test(t), "");
  check(tag + ": pide cómo se abonará", lang === "es" ? t.includes("cómo y cuándo abonarán") : t.includes("how and when you will pay"), "");
  check(tag + ": se presenta como reclamación, no como derecho reconocido", lang === "es" ? t.includes("Considero que") && !/Te corresponden|me corresponden sin/.test(t) : t.includes("I consider that"), "");
  check(tag + ": pide acreditar una circunstancia extraordinaria", lang === "es" ? t.includes("documentación que lo acredite") : t.includes("supporting evidence"), "");
  check(tag + ": sin textos vacíos", !/undefined|NaN|null/.test(t), "");
}
const l1 = letterFor("es", "MAD-BCN", { a: "vueling", ...D, cause: "tech" });
check("Carta refleja el motivo técnico", l1.includes("C-549/07") && l1.includes("250 €"), "");
const l2 = letterFor("es", "MAD-JFK", { a: "iberia", ...D, delay: "3to4" });
check("Carta de largo radio 3-4 h pide 300 € y explica la reducción", l2.includes("300 €") && l2.includes("artículo 7.2"), "");
const l3 = letterFor("es", "MAD-BCN", C({ a: "vueling", notice: "lt7", reroute: "yes", rdep: "1to2", rarr: "lt2", accepted: "yes" }));
check("Carta de cancelación con alternativo describe horarios, aceptación y reducción", l3.includes("entre 1 y 2 horas antes") && l3.includes("Lo acepté") && l3.includes("125 €"), "");
const l4 = letterFor("en", "MAD-BCN", B({ a: "vueling", dreason: "unknown" }));
check("Carta de denegación sin motivo lo dice", l4.includes("not given any reason"), "");
const appSrc = fs.readFileSync(path.join(ROOT, "src", "app.js"), "utf8");
check("app.js no usa almacenamiento ni envía los datos de la carta", !/localStorage|sessionStorage|indexedDB|sendBeacon|XMLHttpRequest/.test(appSrc) && (appSrc.match(/fetch\(/g) || []).length === 1, "");

console.log(`\nMotor de reglas: ${CASES.length} casos, ${ok} comprobaciones correctas, ${fail} fallos`);
process.exit(fail ? 1 : 0);
