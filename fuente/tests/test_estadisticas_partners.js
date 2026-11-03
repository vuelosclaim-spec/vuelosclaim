// Estadísticas por agencia (VuelosClaim Partners) en un navegador real, con el widget incrustado en otra web.
// Comprueba el embudo widget_view → widget_start → widget_result → affiliate_click con partner_id,
// que no se envía nada sin consentimiento, que no se envían respuestas del formulario y que no hay doble conteo.
// Uso: python3 -m http.server 8765 -d docs &  y luego  node fuente/tests/test_estadisticas_partners.js [http://127.0.0.1:8765]
"use strict";
let chromium;
try { ({ chromium } = require("playwright")); } catch (e) { console.log("Playwright no está instalado: prueba de estadísticas de socios omitida."); process.exit(0); }
const http = require("http");

const BASE = process.argv[2] || "http://127.0.0.1:8765";
let HOST = "";
let fail = 0, ok = 0;
const check = (name, cond, extra) => { if (cond) ok++; else { fail++; console.log(`FALLO  ${name} ${extra || ""}`); } };
const FUNNEL = ["widget_view", "widget_start", "widget_result", "affiliate_click"];
const ALLOWED = new Set(["site_language", "source_page", "partner_id", "affiliate_id", "placement", "wizard_step"]);

async function open(browser, path) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  page.errors = [];
  page.on("pageerror", (e) => page.errors.push(e.message));
  ctx.on("page", (p) => { if (p !== page) p.close().catch(() => {}); }); // pestañas abiertas por el enlace de reclamación
  await ctx.route("**/*", (r) => {
    const u = r.request().url();
    if (!u.startsWith(BASE) && !u.startsWith(HOST)) return r.abort(); // Analytics y terceros bloqueados: se mira dataLayer
    return r.continue();
  });
  await page.goto(HOST + "?src=" + encodeURIComponent(BASE + path));
  const f = await (await page.waitForSelector("#vc")).contentFrame();
  await f.waitForSelector("#calc");
  return { ctx, page, f };
}
// Eventos enviados a gtag dentro del iframe: [nombre, parámetros]
const events = (f) => f.evaluate(() => (window.dataLayer || []).filter((a) => a[0] === "event").map((a) => [a[1], Object.assign({}, a[2])]));
const count = (ev, name) => ev.filter((e) => e[0] === name).length;

async function flow(f) {
  await f.click("label:has(input[name=what][value=delay])");
  await f.waitForFunction(() => document.querySelector("#calc").dataset.at === "2");
  for (let k = 0; k < 6 && (await f.getAttribute("#calc", "data-at")) !== "5"; k++) await f.click(".wiz-next");
  await f.waitForTimeout(1400); // calculator_completed espera a que el visitante deje de cambiar respuestas
}
async function clickClaim(f) {
  const a = await f.$('[data-cta] a[rel~="sponsored"]');
  if (!a) return false;
  await a.click();
  await f.waitForTimeout(200);
  return true;
}

async function main(browser) {
  // 1. Consentimiento rechazado: no sale ningún evento
  {
    const { ctx, f } = await open(browser, "/widget/p/demo/");
    await f.$eval("#ckn", (b) => b.click()); // el aviso está fijo abajo del iframe (más alto que la ventana)
    await flow(f);
    await clickClaim(f);
    const ev = await events(f);
    check("rechazo: ningún evento", ev.length === 0, JSON.stringify(ev));
    await ctx.close();
  }
  // 2. Sin responder al aviso: tampoco
  {
    const { ctx, f } = await open(browser, "/widget/p/demo/");
    await flow(f);
    check("sin respuesta al aviso: ningún evento", (await events(f)).length === 0);
    await ctx.close();
  }
  // 3. Consentimiento aceptado al entrar: embudo completo, una vez cada paso, con partner_id y sin respuestas
  {
    const { ctx, page, f } = await open(browser, "/widget/p/demo/");
    await f.$eval("#cky", (b) => b.click());
    let ev = await events(f);
    check("aceptado: widget_view al aceptar", count(ev, "widget_view") === 1, JSON.stringify(ev.map((e) => e[0])));
    await flow(f);
    // Volver a editar y regresar al resultado no debe contar dos veces
    await f.click(".wiz-back");
    await f.click(".wiz-next");
    check("aceptado: vuelve al resultado", (await f.getAttribute("#calc", "data-at")) === "5");
    check("aceptado: hay botón de reclamación", await clickClaim(f));
    ev = await events(f);
    for (const n of FUNNEL) check(`aceptado: ${n} exactamente una vez`, count(ev, n) === 1, `${n}=${count(ev, n)}`);
    const order = FUNNEL.map((n) => ev.findIndex((e) => e[0] === n));
    check("aceptado: orden del embudo", order.every((v, i) => i === 0 || v > order[i - 1]), JSON.stringify(order));
    check("aceptado: todos los eventos llevan partner_id=demo", ev.every((e) => e[1].partner_id === "demo"));
    const extra = ev.flatMap((e) => Object.keys(e[1]).filter((k) => !ALLOWED.has(k)).map((k) => e[0] + "." + k));
    check("aceptado: sin parámetros con respuestas del formulario", extra.length === 0, extra.join(","));
    const leaked = ev.filter((e) => /MAD|BER|delay|gt4|posible|400|250/.test(JSON.stringify(e[1])));
    check("aceptado: sin ruta, incidencia ni importe en los valores", leaked.length === 0, JSON.stringify(leaked));
    const click = ev.find((e) => e[0] === "affiliate_click");
    check("aceptado: clic con afiliado y ubicación", click && click[1].affiliate_id && click[1].placement === "calculator", JSON.stringify(click));
    check("aceptado: sin errores de JavaScript", page.errors.length === 0, page.errors.join(" | "));
    await ctx.close();
  }
  // 4. Acepta después de empezar: la vista se cuenta una vez y antes del inicio
  {
    const { ctx, f } = await open(browser, "/widget/p/demo/");
    await f.click("label:has(input[name=what][value=cancel])");
    check("tarde: nada antes de aceptar", (await events(f)).length === 0);
    await f.$eval("#cky", (b) => b.click());
    await f.click(".wiz-back"); // vuelve a la primera pregunta y cambia la respuesta
    await f.click("label:has(input[name=what][value=delay])");
    const ev = await events(f);
    check("tarde: widget_view una vez", count(ev, "widget_view") === 1, JSON.stringify(ev.map((e) => e[0])));
    check("tarde: widget_start una vez", count(ev, "widget_start") === 1, JSON.stringify(ev.map((e) => e[0])));
    check("tarde: la vista va antes del inicio", ev.findIndex((e) => e[0] === "widget_view") < ev.findIndex((e) => e[0] === "widget_start"));
    check("tarde: calculator_started (respuesta cambiada) con partner_id y sin incident_type", ev.some((e) => e[0] === "calculator_started" && e[1].partner_id === "demo" && !("incident_type" in e[1])));
    // 5. Consentimiento recordado: al recargar se cuenta la vista sin pulsar nada
    await f.goto(BASE + "/widget/p/demo/");
    await f.waitForSelector("#calc");
    const ev2 = await events(f);
    check("recordado: widget_view al cargar", count(ev2, "widget_view") === 1, JSON.stringify(ev2.map((e) => e[0])));
    await ctx.close();
  }
  // 6. Widget estándar y web principal: sin partner_id ni eventos de socio (la medición existente no cambia)
  for (const path of ["/widget/", "/"]) {
    const { ctx, f } = await open(browser, path);
    await f.$eval("#cky", (b) => b.click());
    await f.click("label:has(input[name=what][value=cancel])");
    await f.waitForTimeout(100);
    const ev = await events(f);
    check(`${path}: sin eventos de socio`, count(ev, "widget_view") + count(ev, "widget_start") + count(ev, "widget_result") === 0 && ev.every((e) => !("partner_id" in e[1])), JSON.stringify(ev));
    const st = ev.find((e) => e[0] === "calculator_started");
    check(`${path}: calculator_started conserva incident_type`, st && st[1].incident_type === "cancel", JSON.stringify(st));
    await ctx.close();
  }
}

(async () => {
  const srv = http.createServer((q, res) => {
    const src = new URL(q.url, "http://x").searchParams.get("src") || "";
    res.writeHead(200, { "content-type": "text/html; charset=utf-8" });
    res.end(`<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Agencia</title></head><body>
<h1>Web de la agencia</h1><iframe id="vc" src="${src.replace(/"/g, "")}" title="Calculadora" style="width:100%;max-width:560px;height:960px;border:0"></iframe></body></html>`);
  });
  await new Promise((r) => srv.listen(0, "127.0.0.1", r));
  HOST = `http://127.0.0.1:${srv.address().port}/`;
  const browser = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
  try { await main(browser); } finally { await browser.close(); srv.close(); }
  console.log(`Estadísticas de socios: ${ok} comprobaciones correctas, ${fail} fallos`);
  process.exit(fail ? 1 : 0);
})();
