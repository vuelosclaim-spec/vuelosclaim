// Pruebas del motor de reglas de la calculadora (src/app.js), sin dependencias: `node fuente/tests/test_reglas.js`.
// Carga app.js en un entorno mínimo (sin DOM: init() no hace nada) y llama a window.CTT_compute.
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.join(__dirname, "..");
const airports = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "airports.min.json"), "utf8"));
const airlines = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "airlines.json"), "utf8"));
const byCode = Object.fromEntries(airports.map((a) => [a[0], a]));

function loadEngine(lang) {
  const window = { CTT: { lang, airlines: airlines.map((a) => ({ slug: a.slug, eu: a.eu, uk: a.uk })) } };
  const document = { readyState: "complete", getElementById: () => null, addEventListener() {} };
  const ctx = vm.createContext({ window, document, location: { search: "" }, URLSearchParams, URL, fetch: () => Promise.reject(new Error("sin red")), console });
  vm.runInContext(fs.readFileSync(path.join(ROOT, "src", "app.js"), "utf8"), ctx);
  return window.CTT_compute;
}
const compute = loadEngine("es");
const al = (slug) => airlines.find((a) => a.slug === slug) || { eu: "unknown" };

// [descripción, origen, destino, aerolínea (slug u objeto), qué, retraso/aviso, motivo, veredicto, importe, moneda, pendiente]
// `pendiente` = error conocido del informe de auditoría: se informa pero no rompe la validación hasta su fase.
const CASES = [
  ["Corto radio UE, +4 h", "MAD", "BCN", "vueling", "delay", "gt4", "unknown", "yes", 250, "EUR"],
  ["Menos de 3 h: sin compensación", "MAD", "BCN", "vueling", "delay", "lt3", "unknown", "no", 0, "EUR"],
  ["Intra-UE de más de 1.500 km", "MAD", "TFS", "iberia", "delay", "gt4", "unknown", "yes", 400, "EUR"],
  ["Intra-UE de más de 3.500 km sigue en 400 €", "LPA", "HEL", "finnair", "delay", "gt4", "unknown", "yes", 400, "EUR"],
  ["Largo radio con 3-4 h: 50 %", "MAD", "JFK", "iberia", "delay", "3to4", "unknown", "yes", 300, "EUR"],
  ["Largo radio con +4 h", "MAD", "JFK", "iberia", "delay", "gt4", "unknown", "yes", 600, "EUR"],
  ["Llegada a la UE con aerolínea europea", "JFK", "MAD", "iberia", "delay", "gt4", "unknown", "yes", 600, "EUR"],
  ["Llegada a la UE con aerolínea no europea: no cubierto", "JFK", "MAD", "emirates", "delay", "gt4", "unknown", "no", 0, "EUR"],
  ["Llegada a la UE con aerolínea desconocida: quizá", "DXB", "MAD", { eu: "unknown" }, "delay", "gt4", "unknown", "maybe", 600, "EUR"],
  ["Salida del Reino Unido: UK261 en libras", "MAN", "ALC", "jet2", "delay", "gt4", "unknown", "yes", 350, "GBP"],
  ["Vuelta desde España con aerolínea británica: EU261", "ALC", "MAN", "jet2", "delay", "gt4", "unknown", "yes", 400, "EUR"],
  ["UK261 largo radio 3-4 h: 50 %", "LHR", "JFK", "virgin-atlantic", "delay", "3to4", "unknown", "yes", 260, "GBP"],
  ["Llegada al Reino Unido con aerolínea británica", "JFK", "LHR", "virgin-atlantic", "delay", "gt4", "unknown", "yes", 520, "GBP"],
  ["Llegada al Reino Unido con aerolínea no europea", "DXB", "LHR", "emirates", "delay", "gt4", "unknown", "no", 0, "EUR"],
  ["Suiza cuenta como UE", "ZRH", "MAD", "swiss", "delay", "gt4", "unknown", "yes", 250, "EUR"],
  ["Cancelación con 14 días o más: sin compensación", "MAD", "BCN", "vueling", "cancel", "gt14", "unknown", "no", 0, "EUR"],
  ["Cancelación con menos de 7 días", "MAD", "BCN", "vueling", "cancel", "lt7", "unknown", "yes", 250, "EUR"],
  ["Huelga de la propia aerolínea: paga", "MAD", "BCN", "vueling", "delay", "gt4", "strike", "yes", 250, "EUR"],
  ["Circunstancia extraordinaria en retraso: quizá", "MAD", "BCN", "vueling", "delay", "gt4", "extra", "maybe", 250, "EUR"],
  ["H6: overbooking no admite circunstancias extraordinarias", "MAD", "BCN", "vueling", "denied", null, "extra", "yes", 250, "EUR", "H6"],
  ["H8: salida de Guernsey no está cubierta por UK261", "GCI", "LGW", { eu: "no", uk: true }, "delay", "gt4", "unknown", "no", 0, "EUR", "H8"],
];

let fail = 0, pending = 0, ok = 0;
for (const [name, d, a, airline, what, x, cause, verdict, amount, cur, known] of CASES) {
  const r = compute({ dep: byCode[d], arr: byCode[a], airline: typeof airline === "string" ? al(airline) : airline,
    what, delay: what === "delay" ? x : null, notice: what === "cancel" ? x : null, cause });
  const good = r.verdict === verdict && r.amount === amount && (amount === 0 || r.cur === cur);
  const got = `${r.verdict} ${r.amount} ${r.cur}`;
  if (good) { ok++; if (known) console.log(`AVISO  ${name}: ya corregido, quitar la marca ${known}`); }
  else if (known) { pending++; console.log(`PEND.  ${name}  (esperado ${verdict} ${amount} ${cur}, obtenido ${got})`); }
  else { fail++; console.log(`FALLO  ${name}  (esperado ${verdict} ${amount} ${cur}, obtenido ${got})`); }
}
console.log(`\nMotor de reglas: ${ok} correctos, ${pending} pendientes conocidos, ${fail} fallos`);
process.exit(fail ? 1 : 0);
