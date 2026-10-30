// Pruebas de los idiomas añadidos (italiano y alemán) de la calculadora: `node fuente/tests/test_idiomas.js`.
// 1) Cada idioma tiene exactamente los mismos textos que el español (ni uno de más ni de menos, mismas funciones).
// 2) El motor da el mismo veredicto, importe y moneda en todos los idiomas para miles de casos aleatorios.
// 3) Las cartas en italiano y alemán se generan sin huecos ("undefined", "NaN") y citan el artículo correcto.
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.join(__dirname, "..");
const airports = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "airports.min.json"), "utf8"));
const airlines = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "airlines.json"), "utf8"));
const byCode = Object.fromEntries(airports.map((a) => [a[0], a]));
const LANGS = ["es", "en", "it", "de"];

function load(lang) {
  const window = { CTT: { lang, airlines: airlines.map((a) => ({ slug: a.slug, eu: a.eu, uk: a.uk, ukcomm: a.ukcomm === undefined ? true : a.ukcomm })) } };
  const document = { readyState: "complete", getElementById: () => null, addEventListener() {} };
  const ctx = vm.createContext({ window, document, location: { search: "" }, URLSearchParams, URL, fetch: () => Promise.reject(new Error("sin red")), console });
  vm.runInContext(fs.readFileSync(path.join(ROOT, "src", "app.js"), "utf8"), ctx);
  return window;
}
const W = Object.fromEntries(LANGS.map((l) => [l, load(l)]));
let fails = 0, checks = 0;
function ok(cond, msg) { checks++; if (!cond) { fails++; console.log("FALLO:", msg); } }

// 1) Paridad de claves con el español
function shape(o, p) {
  const out = {};
  for (const [k, v] of Object.entries(o)) {
    const key = p ? p + "." + k : k;
    if (Array.isArray(v)) out[key] = "array:" + v.length;
    else if (v && typeof v === "object") Object.assign(out, shape(v, key));
    else out[key] = typeof v;
  }
  return out;
}
const TT = W.es.CTT_strings;
ok(TT && TT.it && TT.de, "app.js debe exponer los textos (window.CTT_strings) con it y de");
if (TT) {
  const ref = shape(TT.es);
  for (const l of ["en", "it", "de"]) {
    const s = shape(TT[l]);
    for (const k of Object.keys(ref)) ok(s[k] === ref[k], `${l}: falta o cambia de tipo ${k}`);
    for (const k of Object.keys(s)) ok(k in ref, `${l}: sobra ${k}`);
    for (const [k, v] of Object.entries(TT[l])) if (typeof v === "string") ok(v.trim().length > 0, `${l}: texto vacío en ${k}`);
  }
}

// 2) Mismo resultado en todos los idiomas
const pick = (arr, i) => arr[i % arr.length];
const EU = airports.filter((a) => a[6] === 1).slice(0, 400), ALL = airports.filter((_, i) => i % 7 === 0);
const OPTS = {
  what: ["delay", "cancel", "denied"], delay: ["lt3", "3to4", "gt4", "unknown"], notice: ["gt14", "7to14", "lt7", "unknown"],
  reroute: ["yes", "no", "unknown"], rdep: ["le1", "1to2", "gt2", "unknown"], rarr: ["lt2", "2to4", "ge4", "unknown"],
  accepted: ["yes", "no", "unknown"], denied: ["invol", "vol", "unknown"], checkin: ["yes", "no", "unknown"],
  dreason: ["overbooking", "reasonable", "unknown"], via: ["direct", "same", "mixed", "separate"], fare: ["public", "staff"],
  cause: ["unknown", "tech", "crew", "strike_own", "strike_ext", "strike_sub", "atc", "weather", "security", "bird", "knock"],
};
let seed = 7;
const rnd = (n) => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed % n; };
const alist = airlines.concat([{ eu: "unknown" }, { eu: "yes" }, { eu: "no" }]);
for (let i = 0; i < 3000; i++) {
  const dep = rnd(2) ? pick(EU, rnd(EU.length)) : pick(ALL, rnd(ALL.length));
  const arr = pick(ALL, rnd(ALL.length));
  if (dep[0] === arr[0]) continue;
  const o = { dep, arr, airline: pick(alist, rnd(alist.length)) };
  for (const [k, v] of Object.entries(OPTS)) o[k] = pick(v, rnd(v.length));
  const base = W.es.CTT_compute(o);
  for (const l of ["en", "it", "de"]) {
    const r = W[l].CTT_compute(o);
    ok(r.verdict === base.verdict && r.amount === base.amount && r.cur === base.cur && r.potential === base.potential,
      `${l}: resultado distinto en ${dep[0]}-${arr[0]} ${JSON.stringify({ what: o.what, delay: o.delay, notice: o.notice, cause: o.cause })}`);
    ok(r.lines.concat(r.notes, r.missing || []).every((t) => typeof t === "string" && t && !/undefined|NaN/.test(t)), `${l}: línea vacía o con undefined`);
  }
}

// 3) Cartas en italiano y alemán
const d = { n: 2, name: "Maria Rossi", flight: "AZ123", booking: "ABC123", date: "01/11/2026", route: "Roma (FCO) a Madrid (MAD)", today: "02.11.2026" };
for (const l of ["it", "de"]) {
  const letters = W[l].CTT_letters;
  ok(letters && typeof letters[l] === "function", `${l}: falta la carta`);
  if (!letters || !letters[l]) continue;
  const cases = [
    ["delay", { what: "delay", delay: "gt4", cause: "tech" }, l === "it" ? "articoli 6 e 7" : "Artikel 6 und 7"],
    ["cancel", { what: "cancel", notice: "lt7", reroute: "yes", rdep: "gt2", rarr: "ge4", accepted: "no", cause: "crew" }, l === "it" ? "articoli 5 e 7" : "Artikel 5 und 7"],
    ["denied", { what: "denied", denied: "invol", checkin: "yes", dreason: "overbooking" }, l === "it" ? "articoli 4 e 7" : "Artikel 4 und 7"],
  ];
  for (const [name, o, art] of cases) {
    const L = { o, r: { regime: "EU", amount: 250, full: 250, cur: "EUR", dist: 1365 }, dep: byCode.FCO, arr: byCode.MAD, airline: "ITA Airways" };
    const t = letters[l](L, Object.assign({}, d));
    ok(t && !/undefined|NaN|\[object/.test(t), `${l}/${name}: carta con huecos`);
    ok(t.includes(art), `${l}/${name}: no cita ${art}`);
    ok(t.includes("Maria Rossi") && t.includes("AZ123") && t.includes("ABC123"), `${l}/${name}: faltan los datos del pasajero`);
    ok(/250\s?€/.test(t) && /500\s?€/.test(t), `${l}/${name}: importe por pasajero o total incorrecto`);
    ok(t.includes(l === "it" ? "Regolamento (CE) n. 261/2004" : "Verordnung (EG) Nr. 261/2004"), `${l}/${name}: no cita el reglamento`);
  }
}

console.log(`Idiomas: ${checks} comprobaciones, ${fails} fallos`);
process.exit(fails ? 1 : 0);
