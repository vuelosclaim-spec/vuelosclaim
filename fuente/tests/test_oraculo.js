// Prueba diferencial: un oráculo escrito aparte aplica los arts. 3, 5 y 7 del Reglamento 261/2004 y la tabla UK261 de la CAA,
// y se compara con el motor de la calculadora en ~19.000 casos aleatorios (semilla fija) con los límites exactos.
// Uso: node fuente/tests/test_oraculo.js
const fs = require("fs"), vm = require("vm"), path = require("path");
const ROOT = path.join(__dirname, "..");
const airports = JSON.parse(fs.readFileSync(ROOT + "/data/airports.min.json", "utf8"));
const by = Object.fromEntries(airports.map((a) => [a[0], a]));
const w = { CTT: { lang: "es", airlines: [] } };
vm.runInContext(fs.readFileSync(ROOT + "/src/app.js", "utf8"), vm.createContext({ window: w, document: { readyState: "complete", getElementById: () => null, addEventListener() {} }, location: { search: "" }, URLSearchParams, URL, console }));
const compute = w.CTT_compute;
const CODES = ["MAD", "BCN", "LPA", "TFS", "PMI", "HEL", "CDG", "FRA", "ATH", "LIS", "OSL", "KEF", "ZRH", "LHR", "MAN", "EDI", "JFK", "DXB", "RAK", "IST", "BOG", "CUN", "TLV"];
let seed = 261;
const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
const R = (a) => a[Math.floor(rnd() * a.length)], ri = (lo, hi) => lo + Math.floor(rnd() * (hi - lo + 1));
const CARRIERS = [{ eu: "yes", uk: false }, { eu: "no", uk: true }, { eu: "no", uk: false }];
function hav(a, b) { const r = Math.PI / 180, dl = (b[4] - a[4]) * r, dn = (b[5] - a[5]) * r; const h = Math.sin(dl / 2) ** 2 + Math.cos(a[4] * r) * Math.cos(b[4] * r) * Math.sin(dn / 2) ** 2; return Math.round(12742 * Math.asin(Math.sqrt(h))); }
function oracle(o) {
  const isEU = (a) => a[6] === 1, isUK = (a) => a[3] === "GB";
  let reg = null;
  if (isEU(o.dep)) reg = "EU"; else if (isUK(o.dep)) reg = "UK";
  else if (isEU(o.arr)) reg = o.airline.eu === "yes" ? "EU" : o.airline.uk ? "UK" : null;
  else if (isUK(o.arr)) reg = (o.airline.eu === "yes" || o.airline.uk) ? "UK" : null;
  if (!reg) return { verdict: "no", amount: 0 };
  const d = hav(o.dep, o.arr), intra = (isEU(o.dep) && isEU(o.arr)) || (isUK(o.dep) && isUK(o.arr));
  const t = reg === "UK" ? [220, 350, 520] : [250, 400, 600];
  const tier = d <= 1500 ? 0 : (intra || d <= 3500) ? 1 : 2, base = t[tier];
  if (o.what === "delay") {
    if (o.delayMin < 180) return { verdict: "no", amount: 0 };
    return { verdict: "posible", amount: (tier === 2 && o.delayMin <= 240) ? base / 2 : base, cur: reg === "UK" ? "GBP" : "EUR" };
  }
  if (o.noticeDays >= 14) return { verdict: "no", amount: 0 };
  if (o.reroute === "no") return { verdict: "posible", amount: base, cur: reg === "UK" ? "GBP" : "EUR" };
  const [maxEarly, maxLateExcl] = o.noticeDays >= 7 ? [120, 240] : [60, 120];
  if (o.rerouteDepEarlyMin <= maxEarly && o.rerouteArrLateMin < maxLateExcl) return { verdict: "no", amount: 0 };
  const cap = [120, 180, 240][tier];
  return { verdict: "posible", amount: o.rerouteArrLateMin <= cap ? base / 2 : base, cur: reg === "UK" ? "GBP" : "EUR" };
}
let n = 0, bad = [];
for (let i = 0; i < 20000; i++) {
  const dep = by[R(CODES)], arr = by[R(CODES)]; if (dep === arr) continue;
  const o = { dep, arr, airline: R(CARRIERS), cause: "unknown" };
  if (rnd() < 0.5) { o.what = "delay"; o.delayMin = R([179, 180, 181, 239, 240, 241, ri(0, 600)]); }
  else { o.what = "cancel"; o.noticeDays = R([6, 7, 13, 14, ri(0, 30)]); o.reroute = R(["yes", "no"]);
    o.rerouteDepEarlyMin = R([0, 60, 61, 120, 121, ri(-120, 300)]); o.rerouteArrLateMin = R([0, 119, 120, 121, 180, 181, 239, 240, 241, ri(0, 600)]); }
  const a = compute(o), b = oracle(o); n++;
  if (a.verdict !== b.verdict || a.amount !== b.amount || (b.amount && a.cur !== b.cur)) bad.push({ r: o.dep[0] + "-" + o.arr[0], o: { ...o, dep: 0, arr: 0 }, motor: [a.verdict, a.amount, a.cur], oraculo: [b.verdict, b.amount, b.cur] });
}
console.log(`${n} casos aleatorios; discrepancias: ${bad.length}`);
if (bad.length) console.log(JSON.stringify(bad.slice(0, 6), null, 0));
process.exit(bad.length ? 1 : 0);
