// Prueba de la calculadora en un navegador real (móvil táctil y escritorio), con red simulada.
// Uso: python3 -m http.server 8765 -d docs &  y luego  node fuente/tests/test_navegador.js [http://127.0.0.1:8765]
// Necesita Playwright (no es una dependencia del proyecto): si no está instalado, la prueba se salta sin fallar.
// Opcional: CHROMIUM=/ruta/a/chromium para usar un navegador ya instalado.
"use strict";
let chromium;
try { ({ chromium } = require("playwright")); } catch (e) { console.log("Playwright no está instalado: prueba de navegador omitida."); process.exit(0); }

const BASE = process.argv[2] || "http://127.0.0.1:8765";
const DATA = "/data/airports.min.json";
let fail = 0, ok = 0;
const check = (name, cond, extra) => { if (cond) ok++; else { fail++; console.log(`FALLO  ${name} ${extra || ""}`); } };

async function newPage(browser, device, opts = {}) {
  const ctx = await browser.newContext(device === "movil"
    ? { viewport: { width: 375, height: 760 }, hasTouch: true, isMobile: true, deviceScaleFactor: 2, acceptDownloads: true }
    : { viewport: { width: 1280, height: 900 }, acceptDownloads: true });
  if (opts.clipboard) await ctx.grantPermissions(["clipboard-read", "clipboard-write"], { origin: BASE });
  const page = await ctx.newPage();
  page.errors = [];
  page.requests = [];
  page.on("pageerror", (e) => page.errors.push(e.message));
  page.on("request", (r) => page.requests.push(r.url() + " " + (r.postData() || "")));
  // Solo se sirve el sitio local; la red de terceros (Analytics, anuncios) se bloquea
  await page.route("**/*", async (r) => {
    const u = r.request().url();
    if (!u.startsWith(BASE)) return r.abort();
    if (u.includes(DATA) && opts.data) return opts.data(r);
    return r.continue();
  });
  await page.goto(BASE + (opts.path || "/"));
  await page.evaluate(() => { const c = document.getElementById("ck"); if (c) c.remove(); });
  return page;
}
const state = (p) => p.getAttribute("#result", "data-state");
const tapOrClick = (p, device, sel) => (device === "movil" ? p.tap(sel) : p.click(sel));
const choose = (p, name, value) => p.click(`label:has(input[name=${name}][value=${value}])`);

async function pickAirport(p, device, id, text, code) {
  await p.click("#" + id);
  await p.fill("#" + id, "");
  await p.type("#" + id, text, { delay: 20 });
  await p.waitForSelector(`#${id}-list li[role=option]`);
  const items = await p.$$eval(`#${id}-list li[role=option] .opt-code`, (els) => els.map((e) => e.textContent));
  const i = items.indexOf(code);
  if (i < 0) return false;
  await tapOrClick(p, device, `#${id}-opt-${i}`);
  return (await p.getAttribute("#" + id, "data-code")) === code;
}

(async () => {
  const browser = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
  for (const device of ["movil", "escritorio"]) {
    const T = (n) => `[${device}] ${n}`;

    // 1. Carga normal, búsqueda por ciudad y elección con toque o clic
    let p = await newPage(browser, device);
    await p.waitForFunction(() => !/Cargando|Loading/.test(document.querySelector(".empty-msg").textContent) && document.querySelector("#result").dataset.state !== "error");
    check(T("la lista carga: sin el mensaje de error visible"), !(await p.isVisible(".error-msg")));
    check(T("el ejemplo precargado se calcula"), ["posible", "no", "insuficiente", "empty"].includes(await state(p)), await state(p));
    check(T("elegir Madrid tocando la sugerencia"), await pickAirport(p, device, "from", "madrid", "MAD"));
    check(T("distingue aeropuertos de Londres y elige Gatwick"), await pickAirport(p, device, "to", "londres", "LGW"));
    check(T("resultado calculado"), (await state(p)) === "posible", await state(p));
    check(T("distancia mostrada"), /\d km/.test(await p.textContent("[data-km]")));

    // 2. Teclado: flechas + Enter, y Tab con texto exacto
    await p.fill("#to", ""); await p.type("#to", "londres", { delay: 10 });
    await p.waitForSelector("#to-list li[role=option]");
    const second = await p.textContent("#to-opt-1 .opt-code");
    await p.keyboard.press("ArrowDown"); await p.keyboard.press("ArrowDown");
    check(T("aria-activedescendant sigue a las flechas"), (await p.getAttribute("#to", "aria-activedescendant")) === "to-opt-1");
    await p.keyboard.press("Enter");
    check(T("Enter elige la opción marcada"), (await p.getAttribute("#to", "data-code")) === second, second);
    await p.fill("#to", ""); await p.type("#to", "BCN", { delay: 10 }); await p.keyboard.press("Tab");
    await p.waitForFunction(() => document.querySelector("#to").dataset.code === "BCN");
    check(T("salir del campo con un código exacto lo elige"), (await p.inputValue("#to")).includes("BCN"));
    await p.keyboard.press("Escape");

    // 3. Mensajes comprensibles
    await p.fill("#to", ""); await p.type("#to", "zzqxw", { delay: 10 });
    check(T("sin coincidencias se explica"), /No encontramos|can't find/.test(await p.textContent("#to-list")));
    check(T("texto sin elegir pide elegir de la lista"), /Elige el aeropuerto|Choose the airport/.test(await p.textContent(".empty-msg")));
    await pickAirport(p, device, "to", "MAD", "MAD");
    check(T("mismo origen y destino se explica"), /mismo aeropuerto|same airport/.test(await p.textContent(".empty-msg")));
    await pickAirport(p, device, "to", "BCN", "BCN");

    // 4. Carta: sin IBAN, solo para "posible", refleja el resultado, copiar y descargar
    check(T("no existe el campo IBAN"), (await p.$("#l-iban")) === null);
    await p.selectOption("#cause", "weather");
    check(T("sin botón de carta cuando no parece corresponder"), !(await p.isVisible("#letter-open")));
    await p.selectOption("#cause", "tech");
    check(T("botón de carta visible si es posible"), await p.isVisible("#letter-open"));
    await tapOrClick(p, device, "#letter-open");
    await p.fill("#l-name", "Zz Prueba Privada");
    await p.fill("#l-booking", "QQ9ZZ9");
    const txt = await p.inputValue("#letter-text");
    check(T("carta con nombre y motivo técnico, sin datos bancarios"), txt.includes("Zz Prueba Privada") && txt.includes("C-549/07") && !/IBAN/i.test(txt));
    const [dl] = await Promise.all([p.waitForEvent("download"), tapOrClick(p, device, "#letter-dl")]);
    check(T("descarga .txt"), /\.txt$/.test(dl.suggestedFilename()));
    await tapOrClick(p, device, "#letter-copy");
    check(T("copiar muestra confirmación"), (await p.textContent("#letter-msg")).length > 5);
    await choose(p, "what", "cancel");
    check(T("al cambiar a un caso sin datos se oculta la carta"), !(await p.isVisible("#letter")) && (await p.inputValue("#letter-text")) === "");
    check(T("los datos de la carta no salen del navegador"), !page_leak(p.requests, ["Zz Prueba Privada", "Zz+Prueba", "QQ9ZZ9"]));
    check(T("sin desbordamiento horizontal"), (await p.evaluate(() => document.documentElement.scrollWidth)) <= (device === "movil" ? 375 : 1280));
    check(T("sin errores de JavaScript"), p.errors.length === 0, p.errors.join(" | "));
    await p.context().close();

    // 5. Red lenta: escribir antes de que llegue la lista
    p = await newPage(browser, device, { data: async (r) => { await new Promise((ok2) => setTimeout(ok2, 2500)); r.continue(); } });
    await p.click("#from"); await p.type("#from", "valencia", { delay: 10 });
    check(T("aviso de carga mientras llega la lista"), /Cargando|Loading/.test(await p.textContent("#from-list")));
    await p.waitForSelector("#from-list li[role=option]", { timeout: 10000 });
    check(T("sugerencias en cuanto llega la lista"), (await p.textContent("#from-opt-0 .opt-code")) === "VLC");
    await p.context().close();

    // 6. Fallo del servidor dos veces: error visible con reintento, y el reintento funciona
    let fails = 0, broken = true;
    p = await newPage(browser, device, { data: (r) => (broken ? (fails++, r.fulfill({ status: 500, body: "error" })) : r.continue()) });
    await p.waitForFunction(() => document.querySelector("#result").dataset.state === "error", null, { timeout: 10000 });
    check(T("tras un fallo reintenta una vez sola"), fails === 2, String(fails));
    check(T("mensaje de error y botón visibles"), (await p.isVisible(".error-msg")) && (await p.isVisible("#ac-retry")));
    await p.click("#from"); await p.type("#from", "mad", { delay: 10 });
    check(T("el desplegable explica el fallo"), /No se ha podido|could not load/.test(await p.textContent("#from-list")));
    broken = false;
    await tapOrClick(p, device, "#ac-retry");
    await p.waitForFunction(() => document.querySelector("#result").dataset.state !== "error");
    check(T("reintentar carga la lista"), await pickAirport(p, device, "from", "mad", "MAD"));
    await p.context().close();

    // 7. Respuesta con formato incorrecto (por ejemplo, una página HTML de error con estado 200)
    p = await newPage(browser, device, { data: (r) => r.fulfill({ status: 200, contentType: "text/html", body: "<html>404</html>" }) });
    await p.waitForFunction(() => document.querySelector("#result").dataset.state === "error", null, { timeout: 10000 });
    check(T("HTML en lugar de JSON se trata como error"), true);
    await p.context().close();

    // 8. Página de aerolínea con ruta precargada
    p = await newPage(browser, device, { path: device === "movil" ? "/compensacion-retraso-iberia/" : "/en/" });
    await p.waitForFunction(() => document.querySelector("#result").dataset.state !== "empty" || !document.querySelector("#from").dataset.code, null, { timeout: 10000 });
    const pre = await p.getAttribute("#from", "data-code");
    if (pre) check(T("ruta precargada calculada"), ["posible", "no", "insuficiente"].includes(await state(p)) && (await p.inputValue("#from")).includes(pre));
    await p.context().close();
  }
  await browser.close();
  console.log(`\nNavegador: ${ok} comprobaciones correctas, ${fail} fallos`);
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });

function page_leak(reqs, needles) { return reqs.some((r) => needles.some((n) => r.includes(n) || decodeURIComponent(r).includes(n))); }
