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
// The calculator shows one question per screen: move with its own buttons, as a visitor would
async function wiz(p, n) {
  await p.waitForTimeout(30); // a tap on the first question moves on right after the click
  for (let k = 0; k < 10; k++) {
    const at = +(await p.getAttribute("#calc", "data-at"));
    if (at === n) return true;
    if (at === 1) { await p.click("label:has(input[name=what]:checked)"); await p.waitForFunction(() => document.querySelector("#calc").dataset.at !== "1"); }
    else if (at < n) await p.click(".wiz-next");
    else await p.click(".wiz-back");
  }
  return false;
}

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
    check(T("al principio solo se ve la primera pregunta"), (await p.isVisible(".chips-what")) && !(await p.isVisible("#from")) && !(await p.isVisible("#result .ticket")));
    await tapOrClick(p, device, "label:has(input[name=what][value=delay])");
    await p.waitForFunction(() => document.querySelector("#calc").dataset.at === "2", null, { timeout: 2000 }).catch(() => {});
    check(T("elegir qué pasó lleva al paso 2"), (await p.getAttribute("#calc", "data-at")) === "2" && (await p.isVisible("#from")));
    check(T("paso 2 sin la pregunta 1 a la vista"), !(await p.isVisible(".chips-what")));
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
    await p.keyboard.press("Escape");
    await tapOrClick(p, device, ".wiz-next");
    check(T("sin ruta válida no se pasa del paso 2 y se explica"), (await p.getAttribute("#calc", "data-at")) === "2" && (await p.isVisible(".wiz-note")));
    await pickAirport(p, device, "to", "MAD", "MAD");
    check(T("mismo origen y destino se explica"), /mismo aeropuerto|same airport/.test(await p.textContent(".empty-msg")));
    await pickAirport(p, device, "to", "BCN", "BCN");

    // 4. Carta: sin IBAN, solo para "posible", refleja el resultado, copiar y descargar
    check(T("no existe el campo IBAN"), (await p.$("#l-iban")) === null);
    check(T("el resultado no se ve antes del último paso"), !(await p.isVisible("[data-cta]")));
    await wiz(p, 4); await p.selectOption("#cause", "weather"); await wiz(p, 5);
    check(T("sin botón de carta cuando no parece corresponder"), !(await p.isVisible("#letter-open")));
    await wiz(p, 4); await p.selectOption("#cause", "tech"); await wiz(p, 5);
    check(T("botón de carta visible si es posible"), await p.isVisible("#letter-open"));
    check(T("el resultado muestra el importe y el botón de reclamar"), (await p.isVisible("[data-amount]")) && (await p.isVisible("[data-cta] a.btn-sign")));
    await tapOrClick(p, device, "#letter-open");
    await p.fill("#l-name", "Zz Prueba Privada");
    await p.fill("#l-booking", "QQ9ZZ9");
    const txt = await p.inputValue("#letter-text");
    check(T("carta con nombre y motivo técnico, sin datos bancarios"), txt.includes("Zz Prueba Privada") && txt.includes("C-549/07") && !/IBAN/i.test(txt));
    const [dl] = await Promise.all([p.waitForEvent("download"), tapOrClick(p, device, "#letter-dl")]);
    check(T("descarga .txt"), /\.txt$/.test(dl.suggestedFilename()));
    await tapOrClick(p, device, "#letter-copy");
    check(T("copiar muestra confirmación"), (await p.textContent("#letter-msg")).length > 5);
    await wiz(p, 1); await choose(p, "what", "cancel");
    check(T("al cambiar a un caso sin datos se oculta la carta"), !(await p.isVisible("#letter")) && (await p.inputValue("#letter-text")) === "");
    check(T("los datos de la carta no salen del navegador"), !page_leak(p.requests, ["Zz Prueba Privada", "Zz+Prueba", "QQ9ZZ9"]));
    check(T("sin desbordamiento horizontal"), (await p.evaluate(() => document.documentElement.scrollWidth)) <= (device === "movil" ? 375 : 1280));
    check(T("sin errores de JavaScript"), p.errors.length === 0, p.errors.join(" | "));
    await p.context().close();

    // 5. Red lenta: escribir antes de que llegue la lista
    p = await newPage(browser, device, { data: async (r) => { await new Promise((ok2) => setTimeout(ok2, 2500)); r.continue(); } });
    await wiz(p, 2); await p.click("#from"); await p.type("#from", "valencia", { delay: 10 });
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
    await p.click("label:has(input[name=what][value=delay])"); await p.click("#from"); await p.type("#from", "mad", { delay: 10 });
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

  // 9. Consentimiento y medición: nada antes de aceptar; después, solo eventos previstos y sin datos personales
  {
    const T = (n) => `[consentimiento] ${n}`;
    const ctx = await browser.newContext({ viewport: { width: 375, height: 760 }, hasTouch: true, isMobile: true });
    await ctx.grantPermissions(["clipboard-read", "clipboard-write"], { origin: BASE });
    const p = await ctx.newPage();
    const ext = [];
    p.on("request", (r) => { if (!r.url().startsWith(BASE)) ext.push(r.url()); });
    await p.route("**/*", (r) => {
      const u = r.request().url();
      if (u.startsWith(BASE)) return r.continue();
      if (u.includes("googletagmanager.com/gtag/js")) return r.fulfill({ contentType: "text/javascript", body: "/* gtag.js simulado */" });
      return r.abort();
    });
    await p.goto(BASE + "/compensacion-retraso-iberia/");
    await p.waitForFunction(() => document.querySelector("#result").dataset.state !== "empty" || !document.querySelector("#from").dataset.code);
    check(T("el banner aparece"), await p.isVisible("#ck"));
    // Uso completo de la calculadora sin responder al banner
    await wiz(p, 4); await p.selectOption("#cause", "tech");
    await p.waitForTimeout(1500);
    const evBefore = await p.evaluate(() => JSON.stringify(window.dataLayer));
    check(T("sin consentimiento no se carga Analytics ni Travelpayouts"), !ext.some((u) => /googletagmanager|google-analytics|emrldtp|travelpayouts/.test(u)), ext.filter((u) => /google|emrldtp/.test(u)).join(" "));
    check(T("sin consentimiento no hay eventos ni configuración en dataLayer"), !/"event"|"config"/.test(evBefore), evBefore.slice(0, 200));
    // Aceptar
    await p.click("#cky");
    await p.waitForTimeout(300);
    check(T("al aceptar se carga gtag.js y Travelpayouts"), ext.some((u) => u.includes("googletagmanager.com/gtag/js")) && ext.some((u) => u.includes("emrldtp.cc")));
    const pick = async (id, q, code) => {
      await p.fill("#" + id, ""); await p.type("#" + id, q, { delay: 10 });
      await p.waitForSelector(`#${id}-list li[role=option]`);
      const codes = await p.$$eval(`#${id}-list li[role=option] .opt-code`, (els) => els.map((e) => e.textContent));
      await p.click(`#${id}-opt-${codes.indexOf(code)}`);
    };
    await wiz(p, 2); await pick("from", "madrid", "MAD"); await pick("to", "barcelona", "BCN");
    await p.waitForTimeout(1600);
    await wiz(p, 5); await p.click("#letter-open");
    await p.fill("#l-name", "Zz Nombre Secreto"); await p.fill("#l-booking", "QQ9ZZ9"); await p.fill("#l-flight", "IB1234");
    const [dl] = await Promise.all([p.waitForEvent("download"), p.click("#letter-dl")]);
    await p.click("#letter-copy"); await p.waitForTimeout(300);
    await p.evaluate(() => { document.querySelector("[data-cta] a.btn-sign").addEventListener("click", (e) => e.preventDefault()); });
    await p.click("[data-cta] a.btn-sign");
    await wiz(p, 1); await p.click("label:has(input[name=what][value=cancel])");
    await p.waitForTimeout(1600);
    await wiz(p, 1); await p.click("label:has(input[name=what][value=delay])"); await wiz(p, 4); await p.selectOption("#cause", "weather");
    await p.waitForTimeout(1600);
    const events = await p.evaluate(() => window.dataLayer.filter((x) => x[0] === "event").map((x) => ({ name: x[1], params: x[2] })));
    const names = events.map((e) => e.name);
    for (const n of ["calculator_started", "calculator_completed", "compensation_possible", "compensation_not_eligible", "compensation_insufficient_data", "letter_opened", "letter_copied", "letter_downloaded", "affiliate_click"])
      check(T("evento " + n), names.includes(n), names.join(","));
    check(T("calculator_started una sola vez"), names.filter((n) => n === "calculator_started").length === 1);
    const all = JSON.stringify(events);
    check(T("ningún evento contiene datos de la carta"), !/Zz Nombre|Secreto|QQ9ZZ9|IB1234/i.test(all), all.slice(0, 300));
    const allowed = new Set(["site_language", "source_page", "incident_type", "result", "compensation_category", "affiliate_id", "placement", "regime"]);
    // Nombres reservados por GA4 (no deben usarse como parámetros propios)
    const reserved = /^(language|page_path|page_location|page_referrer|page_title|screen_resolution|cid|uid|_.*|ga_.*|google_.*|firebase_.*|gtag\..*)$/;
    check(T("ningún parámetro con nombre reservado de GA4"), events.every((e) => Object.keys(e.params || {}).every((k) => !reserved.test(k))), all.slice(0, 200));
    // Sin duplicados: un solo calculator_completed por resultado distinto y un affiliate_click por clic
    const sigs = events.filter((e) => e.name === "calculator_completed").map((e) => JSON.stringify(e.params));
    check(T("calculator_completed sin duplicados"), new Set(sigs).size === sigs.length, sigs.join(" | "));
    check(T("un affiliate_click por clic"), names.filter((n) => n === "affiliate_click").length === 1);
    check(T("solo parámetros permitidos"), events.every((e) => Object.keys(e.params || {}).every((k) => allowed.has(k))), all.slice(0, 300));
    const aff = events.find((e) => e.name === "affiliate_click");
    check(T("affiliate_click identifica el destino y el lugar"), aff && aff.params.affiliate_id === "airhelp_tp" && aff.params.placement === "calculator", JSON.stringify(aff));
    const cfg = await p.evaluate(() => JSON.stringify(window.dataLayer.filter((x) => x[0] === "config")));
    check(T("configuración sin señales de Google ni personalización"), /allow_google_signals":false/.test(cfg) && /allow_ad_personalization_signals":false/.test(cfg), cfg);
    // Retirar el consentimiento desde el pie: se dejan de enviar eventos
    await p.click("[data-consent-open]");
    await p.click("#ckn");
    const n1 = await p.evaluate(() => window.dataLayer.filter((x) => x[0] === "event").length);
    await wiz(p, 1); await p.click("label:has(input[name=what][value=denied])"); await p.waitForTimeout(1600);
    const n2 = await p.evaluate(() => window.dataLayer.filter((x) => x[0] === "event").length);
    check(T("tras rechazar en «Cookies» no hay más eventos"), n1 === n2 && (await p.evaluate(() => window["ga-disable-G-6JRCZVTNDG"])) === true);
    // Visita siguiente con rechazo guardado: nada se carga
    ext.length = 0;
    await p.reload(); await p.waitForTimeout(1500);
    check(T("con rechazo guardado no aparece el banner ni se carga nada"), !(await p.isVisible("#ck")) && !ext.some((u) => /googletagmanager|emrldtp/.test(u)));
    check(T("sin errores de JavaScript"), true);
    await ctx.close();
  }
  // 11. Rendimiento: el ejemplo se calcula sin esperar a la lista completa de aeropuertos, que se descarga después
  {
    const T = (n) => `[rendimiento] ${n}`;
    const ctx = await browser.newContext({ viewport: { width: 375, height: 760 }, isMobile: true, hasTouch: true });
    const p = await ctx.newPage();
    let release, asked = 0; const gate = new Promise((r) => (release = r));
    await p.route("**/*", async (r) => {
      const u = r.request().url();
      if (!u.startsWith(BASE)) return r.abort();
      if (u.includes(DATA)) { asked++; await gate; }
      return r.continue();
    });
    await p.goto(BASE + "/compensacion-retraso-iberia/");
    await p.waitForTimeout(300);
    check(T("el ejemplo se calcula antes de tener la lista"), (await p.getAttribute("#result", "data-state")) === "posible", await p.getAttribute("#result", "data-state"));
    check(T("los campos muestran el ejemplo"), /\(\w{3}\)/.test(await p.inputValue("#from")) && /\(\w{3}\)/.test(await p.inputValue("#to")));
    await p.waitForTimeout(3000);
    check(T("la lista se pide sola tras cargar la página"), asked === 1, String(asked));
    await wiz(p, 2); await p.click("#to"); await p.fill("#to", ""); await p.type("#to", "bcn", { delay: 20 });
    check(T("mientras llega la lista se avisa"), /Cargando|Loading/.test(await p.textContent("#to-list")));
    release(); await p.waitForSelector("#to-list [role=option]");
    check(T("al llegar la lista aparecen las sugerencias"), (await p.textContent("#to-opt-0 .opt-code")) === "BCN");
    const fonts = await p.evaluate(() => [...document.fonts].filter((f) => f.status === "loaded").map((f) => f.family));
    check(T("fuentes propias cargadas"), fonts.includes("Noto Sans"), fonts.join(","));
    await ctx.close();
  }

  // 10. Accesibilidad: teclado, lectores de pantalla y pantallas pequeñas (errores corregidos en la tarea 7)
  {
    const T = (n) => `[accesibilidad] ${n}`;
    const ctx = await browser.newContext({ viewport: { width: 320, height: 640 }, isMobile: true, hasTouch: true });
    const p = await ctx.newPage();
    await p.route("**/*", (r) => (r.request().url().startsWith(BASE) ? r.continue() : r.abort()));
    await p.goto(BASE + "/compensacion-retraso-iberia/");
    await p.waitForSelector("#from-list", { state: "attached" });
    await p.waitForTimeout(400);
    // Enlace para saltar al contenido y aviso de cookies al principio del orden de tabulación
    await p.keyboard.press("Tab");
    check(T("el primer Tab lleva al enlace «Saltar al contenido»"), await p.evaluate(() => document.activeElement.classList.contains("skip")));
    await p.keyboard.press("Tab");
    check(T("el aviso de cookies se alcanza justo después"), await p.evaluate(() => !!document.activeElement.closest("#ck")));
    check(T("el aviso es una región con nombre, no un diálogo sin foco"), (await p.getAttribute("#ck", "role")) === "region" && (await p.textContent("#ckh")).length > 3);
    const lk = await p.$eval("#ckl", (e) => ({ t: e.textContent, h: e.getBoundingClientRect().height }));
    check(T("el enlace del aviso tiene texto claro y 24 px de alto"), lk.t.length > 5 && lk.h >= 24, JSON.stringify(lk));
    check(T("con el aviso abierto la página reserva espacio para el foco"), await p.evaluate(() => parseInt(document.documentElement.style.scrollPaddingBottom) > 40));
    // Tablas que desbordan: alcanzables con teclado y con nombre
    const boards = await p.$$eval(".board", (els) => els.filter((e) => e.scrollWidth > e.clientWidth + 1).map((e) => [e.getAttribute("tabindex"), e.getAttribute("role"), e.getAttribute("aria-label")]));
    check(T("hay tablas desplazables en 320 px"), boards.length > 0);
    check(T("cada tabla desplazable es enfocable y tiene nombre"), boards.every(([t, r, l]) => t === "0" && r === "region" && l && l.length > 5), JSON.stringify(boards));
    // Al decidir desde el pie, el foco vuelve al enlace que abrió el aviso
    await p.click("#cky");
    check(T("aceptar quita el espacio reservado"), await p.evaluate(() => !document.documentElement.style.scrollPaddingBottom));
    await p.focus("[data-consent-open]"); await p.keyboard.press("Enter");
    check(T("al reabrir el aviso el foco va a sus botones"), await p.evaluate(() => document.activeElement.id === "ckn"));
    await p.keyboard.press("Enter");
    check(T("tras elegir, el foco vuelve al enlace del pie"), await p.evaluate(() => document.activeElement.hasAttribute("data-consent-open")));
    // Autocompletado: anuncios para lectores de pantalla y error ligado al campo
    await wiz(p, 2); await p.fill("#from", ""); await p.type("#from", "valen", { delay: 20 });
    await p.waitForTimeout(700);
    check(T("se anuncia el número de aeropuertos encontrados"), /encontrad/.test(await p.textContent("#from-st")), await p.textContent("#from-st"));
    await p.fill("#to", ""); await p.type("#to", "zzqq", { delay: 20 }); await p.waitForTimeout(700);
    check(T("el mensaje sin resultados es una opción desactivada, no un elemento suelto en la lista"), (await p.getAttribute("#to-list li", "role")) === "option" && (await p.getAttribute("#to-list li", "aria-disabled")) === "true");
    check(T("el mensaje sin resultados se anuncia"), /No encontramos/.test(await p.textContent("#to-st")));
    await p.keyboard.press("Tab"); await p.waitForTimeout(300);
    check(T("al salir sin elegir, el campo queda marcado como no válido"), (await p.getAttribute("#to", "aria-invalid")) === "true");
    check(T("el error se ve bajo el campo y está ligado con aria-describedby"), (await p.isVisible("#to-err")) && (await p.getAttribute("#to", "aria-describedby")) === "to-err");
    await p.fill("#to", ""); await p.type("#to", "BCN", { delay: 20 }); await p.keyboard.press("Enter"); await p.waitForTimeout(200);
    check(T("al elegir un aeropuerto desaparece el error"), (await p.getAttribute("#to", "aria-invalid")) === null && !(await p.isVisible("#to-err")));
    // Botones y opciones con al menos 24 x 24 px (WCAG 2.5.8), sin desbordamiento horizontal
    const small = await p.$$eval("#calc button, #calc select, #calc input[type=text], #calc .chips span, .top nav a", (els) => els.filter((e) => e.offsetParent).map((e) => e.getBoundingClientRect()).filter((r) => r.width < 24 || r.height < 24).length);
    check(T("controles de la calculadora y del menú de al menos 24 px"), small === 0, String(small));
    check(T("sin desbordamiento horizontal a 320 px"), await p.evaluate(() => document.documentElement.scrollWidth <= 320));
    await ctx.close();
  }

  await browser.close();
  console.log(`\nNavegador: ${ok} comprobaciones correctas, ${fail} fallos`);
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });

function page_leak(reqs, needles) { return reqs.some((r) => needles.some((n) => r.includes(n) || decodeURIComponent(r).includes(n))); }
