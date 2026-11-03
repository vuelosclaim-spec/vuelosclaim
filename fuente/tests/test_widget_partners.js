// Widget con marca de socio (VuelosClaim Partners) incrustado en una web de terceros, en un navegador real.
// Uso: python3 -m http.server 8765 -d docs &  y luego  node fuente/tests/test_widget_partners.js [http://127.0.0.1:8765]
// Necesita Playwright: si no está instalado, la prueba se salta sin fallar (igual que test_navegador.js).
"use strict";
let chromium;
try { ({ chromium } = require("playwright")); } catch (e) { console.log("Playwright no está instalado: prueba del widget de socios omitida."); process.exit(0); }

const BASE = process.argv[2] || "http://127.0.0.1:8765";
const http = require("http");
let HOST = ""; // web de la agencia simulada: servidor propio en otro puerto, es decir, otro origen distinto de VuelosClaim
let fail = 0, ok = 0;
const check = (name, cond, extra) => { if (cond) ok++; else { fail++; console.log(`FALLO  ${name} ${extra || ""}`); } };

// Intento de cambiar la marca desde la web anfitriona: debe ignorarse
const EVIL = "?color=%23ff0000&name=%3Cimg%20src%3Dx%20onerror%3Dalert(1)%3E&logo=https%3A%2F%2Fevil.test%2Fx.png&css=body%7Bdisplay%3Anone%7D";

async function run(browser, device) {
  const ctx = await browser.newContext(device === "movil"
    ? { viewport: { width: 375, height: 760 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2 }
    : { viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const errors = [], requests = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("request", (r) => requests.push(r.url()));
  page.on("dialog", (d) => { errors.push("dialog: " + d.message()); d.dismiss(); });
  // Solo se sirven el sitio local y la web anfitriona; la red de terceros (Analytics, fuentes) se bloquea
  await page.route("**/*", async (r) => {
    const u = r.request().url();
    if (!u.startsWith(BASE) && !u.startsWith(HOST)) return r.abort();
    return r.continue();
  });
  await page.goto(HOST);
  const frameEl = await page.waitForSelector("#vc");
  const f = await frameEl.contentFrame();
  await f.waitForSelector("#calc");
  const tag = `[${device}]`;

  // Marca del registro, no de la URL
  const brand = await f.textContent(".embed-brand");
  check(`${tag} nombre del socio visible`, /Agencia de ejemplo/.test(brand), brand);
  check(`${tag} distintivo de demostración`, /Demostración/.test(brand), brand);
  check(`${tag} parámetros de la web anfitriona ignorados`, !(await f.$(".embed-brand img")) && !/onerror|img/i.test(brand) && (await f.isVisible("#calc")));
  check(`${tag} sin peticiones a dominios de la URL`, !requests.some((u) => new URL(u).hostname === "evil.test"));
  const sign = await f.evaluate(() => getComputedStyle(document.documentElement).getPropertyValue("--sign").trim());
  check(`${tag} color del socio aplicado`, sign.toLowerCase() === "#1f4e8c", sign);

  // Atribución y aviso siempre visibles
  check(`${tag} atribución a VuelosClaim`, await f.isVisible('.embed-foot a[href="https://vuelosclaim.eu/"]'));
  check(`${tag} aviso de afiliación`, /enlaces de afiliación/.test(await f.textContent(".embed-foot")));

  // Sin desbordamiento horizontal dentro del iframe
  const over = await f.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  check(`${tag} sin scroll horizontal`, over <= 1, String(over));

  // Sin consentimiento no se carga Analytics
  check(`${tag} sin Analytics antes del consentimiento`, !requests.some((u) => /google-analytics|googletagmanager/.test(u)));
  await f.evaluate(() => { const c = document.getElementById("ck"); if (c) c.remove(); });

  // La calculadora funciona: primera pregunta → paso 2 con la ruta precargada → resultado
  const opt = 'label:has(input[name=what][value=delay])';
  if (device === "movil") await f.tap(opt); else await f.click(opt);
  await f.waitForFunction(() => document.querySelector("#calc").dataset.at === "2");
  const btnBg = await f.evaluate(() => getComputedStyle(document.querySelector(".wiz-next")).backgroundColor);
  check(`${tag} botón con el color del socio`, btnBg === "rgb(31, 78, 140)", btnBg);
  for (let k = 0; k < 6 && (await f.getAttribute("#calc", "data-at")) !== "5"; k++) await f.click(".wiz-next");
  check(`${tag} llega al resultado`, (await f.getAttribute("#calc", "data-at")) === "5");
  const st = await f.getAttribute("#result", "data-state");
  check(`${tag} resultado calculado`, st && st !== "empty" && st !== "error", st);

  // Teclado: desde la web anfitriona se entra en el widget con Tab
  if (device === "escritorio") {
    await page.focus("#antes");
    let inside = false;
    for (let k = 0; k < 4 && !inside; k++) {
      await page.keyboard.press("Tab");
      inside = await f.evaluate(() => document.hasFocus() && document.activeElement && document.activeElement !== document.body);
    }
    check(`${tag} accesible con teclado`, inside);
  }
  check(`${tag} sin errores de JavaScript`, errors.length === 0, errors.join(" | "));
  await ctx.close();
}

const HOST_HTML = `<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Agencia</title></head>
<body style="margin:0;font-family:sans-serif"><h1 style="font-size:18px">Web de la agencia</h1><a id="antes" href="#">Enlace anterior</a>
<iframe id="vc" src="${BASE}/widget/p/demo/${EVIL}" title="Calculadora" style="width:100%;max-width:560px;height:960px;border:0"></iframe></body></html>`;

(async () => {
  const srv = http.createServer((q, res) => { res.writeHead(200, { "content-type": "text/html; charset=utf-8" }); res.end(HOST_HTML); });
  await new Promise((r) => srv.listen(0, "127.0.0.1", r));
  HOST = `http://127.0.0.1:${srv.address().port}/`;
  const browser = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
  try {
    for (const d of ["escritorio", "movil"]) await run(browser, d);
    // El widget sin marca sigue igual
    const ctx = await browser.newContext();
    const p = await ctx.newPage();
    await p.goto(BASE + "/widget/");
    check("widget estándar sin marca de socio", !(await p.$(".embed-brand")));
    await ctx.close();
  } finally { await browser.close(); srv.close(); }
  console.log(`Widget de socios: ${ok} comprobaciones correctas, ${fail} fallos`);
  process.exit(fail ? 1 : 0);
})();
