(function () {
  "use strict";
  var cfg = window.CTT || {};
  var LANG = cfg.lang === "en" ? "en" : "es";
  var AIRLINES = cfg.airlines || [];
  var ALIAS_ES = {
    LHR: "Londres", LGW: "Londres", STN: "Londres", LTN: "Londres", LCY: "Londres", AMS: "Ámsterdam",
    BRU: "Bruselas", CRL: "Bruselas", CDG: "París", ORY: "París", BVA: "París", FCO: "Roma", CIA: "Roma",
    MXP: "Milán", BGY: "Milán", LIN: "Milán", MUC: "Múnich", BER: "Berlín", GVA: "Ginebra", ZRH: "Zúrich",
    LIS: "Lisboa", OPO: "Oporto", ATH: "Atenas", IST: "Estambul", SAW: "Estambul", JFK: "Nueva York",
    EWR: "Nueva York", CPH: "Copenhague", ARN: "Estocolmo", VIE: "Viena", WAW: "Varsovia", PRG: "Praga",
    DUB: "Dublín", EDI: "Edimburgo", MAN: "Mánchester", FRA: "Fráncfort", HAM: "Hamburgo", VCE: "Venecia",
    NAP: "Nápoles", FLR: "Florencia", RAK: "Marrakech", TFN: "Tenerife Norte", TFS: "Tenerife Sur",
    ACE: "Lanzarote", FUE: "Fuerteventura", LPA: "Gran Canaria", IBZ: "Ibiza", MAH: "Menorca",
    PMI: "Palma de Mallorca", SCQ: "Santiago de Compostela", BOG: "Bogotá", MEX: "Ciudad de México",
    EZE: "Buenos Aires", LIM: "Lima", MIA: "Miami", CUN: "Cancún", BCN: "Barcelona", MAD: "Madrid",
    VLC: "Valencia", AGP: "Málaga", ALC: "Alicante", SVQ: "Sevilla", BIO: "Bilbao", GRX: "Granada",
    XRY: "Jerez", VGO: "Vigo", OVD: "Asturias", SDR: "Santander", ZAZ: "Zaragoza", RMU: "Murcia",
    LEI: "Almería", REU: "Reus", GRO: "Girona", MLN: "Melilla", SPC: "La Palma", NCE: "Niza", MRS: "Marsella",
    LYS: "Lyon", TLS: "Toulouse", BOD: "Burdeos", NTE: "Nantes", GOT: "Gotemburgo", OSL: "Oslo",
    HEL: "Helsinki", BUD: "Budapest", OTP: "Bucarest", SOF: "Sofía", KRK: "Cracovia", DUS: "Düsseldorf",
    CGN: "Colonia", STR: "Stuttgart", BSL: "Basilea", MLA: "Malta", LCA: "Lárnaca", TLV: "Tel Aviv",
    CMN: "Casablanca", TNG: "Tánger", DXB: "Dubái", DOH: "Doha", GRU: "São Paulo", SCL: "Santiago de Chile",
    HAV: "La Habana", PUJ: "Punta Cana", SDQ: "Santo Domingo", CCS: "Caracas", UIO: "Quito", GYE: "Guayaquil"
  };
  var ALIAS_EN = {
    LHR: "London", LGW: "London", STN: "London", LTN: "London", LCY: "London", LPA: "Gran Canaria",
    TFS: "Tenerife South", TFN: "Tenerife North", PMI: "Palma de Mallorca", AGP: "Malaga", ALC: "Alicante",
    ACE: "Lanzarote", FUE: "Fuerteventura", IBZ: "Ibiza", MAH: "Menorca", SCQ: "Santiago de Compostela",
    OVD: "Asturias", SPC: "La Palma", MAD: "Madrid", BCN: "Barcelona", VLC: "Valencia", SVQ: "Seville",
    GRO: "Girona", REU: "Reus", RMU: "Murcia", LEI: "Almeria", XRY: "Jerez", GRX: "Granada",
    MAN: "Manchester", BHX: "Birmingham", BRS: "Bristol", EDI: "Edinburgh", GLA: "Glasgow", NCL: "Newcastle",
    LBA: "Leeds Bradford", EMA: "East Midlands", LPL: "Liverpool", BFS: "Belfast", DUB: "Dublin",
    JFK: "New York", EWR: "New York", BGY: "Milan", MXP: "Milan"
  };
  var T = {
    es: {
      notCovered: "El vuelo no sale de un aeropuerto europeo y no lo opera una aerolínea europea, así que el reglamento europeo no lo cubre.",
      maybeCarrier: "Como el vuelo llega a Europa desde fuera, solo está cubierto si lo operó una aerolínea europea. Lo pone en la tarjeta de embarque o en la reserva.",
      ukRegime: "El vuelo sale del Reino Unido: se aplica la norma británica (UK261), que paga en libras.",
      ukArrival: "El vuelo llega al Reino Unido con una aerolínea británica o europea: se aplica la norma británica (UK261).",
      alsoEU: "Al llegar a la UE con una aerolínea europea, también puede aplicarse el reglamento europeo (en euros). Solo se cobra una vez.",
      bands: ["hasta 1.500 km", "más de 1.500 km dentro de Europa", "entre 1.500 y 3.500 km", "más de 3.500 km"],
      dist: function (d, band, base) { return "Distancia: " + d + " km (" + band + ") → base de " + base + " por pasajero."; },
      lt3: "Con menos de 3 horas de retraso en la llegada no hay compensación económica.",
      lt3note: "Aun así, a partir de 2 horas (vuelos cortos) la aerolínea te debe comida, bebida y comunicación.",
      half: function (m) { return "En vuelos de más de 3.500 km con un retraso de entre 3 y 4 horas, la compensación se reduce a la mitad: " + m + "."; },
      full: "Llegaste con 3 horas o más de retraso: corresponde la compensación completa.",
      gt14: "Si te avisaron de la cancelación con 14 días o más de antelación, no hay compensación.",
      gt14note: "Sí tienes derecho a elegir entre el reembolso del billete o un vuelo alternativo.",
      cancel: "Cancelación avisada con menos de 14 días: corresponde compensación.",
      n7to14: "Salvo que te ofrecieran un vuelo alternativo que saliera como mucho 2 horas antes y llegara como mucho 4 horas después del original.",
      nlt7: "Salvo que te ofrecieran un vuelo alternativo que saliera como mucho 1 hora antes y llegara como mucho 2 horas después del original.",
      denied: "Te denegaron el embarque sin que cedieras tu plaza voluntariamente (por ejemplo, por overbooking): corresponde compensación.",
      extra: "La aerolínea alega una circunstancia extraordinaria (meteorología, huelga de controladores, seguridad). Si lo demuestra, no tiene que pagar.",
      extraNote: "Tiene que probarlo ella. Muchas veces alegan mal tiempo cuando la causa real fue otra: una empresa de reclamaciones lo comprueba gratis.",
      strike: "Las huelgas del personal de la propia aerolínea no la libran de pagar (Tribunal de Justicia de la UE, 2021).",
      tech: "Los problemas técnicos del avión, por regla general, no la libran de pagar.",
      yes: function (m) { return "Te corresponden " + m + " por pasajero"; },
      maybe: function (m) { return "Podrían corresponderte " + m + " por pasajero"; },
      none: "Con estos datos no te corresponde compensación",
      copied: "Carta copiada. Pégala en el formulario o el correo de la aerolínea.",
      selected: "Texto seleccionado: cópialo con Ctrl+C o mantén pulsado.",
      downloaded: "Carta descargada.", dlFail: "No se ha podido descargar. Usa el botón de copiar.",
      file: "reclamacion-vuelo.txt"
    },
    en: {
      notCovered: "The flight does not depart from a European airport and is not operated by a European airline, so EU261 does not cover it.",
      maybeCarrier: "Because the flight arrives in Europe from outside, it is only covered if a European airline operated it. Check your boarding pass or booking.",
      ukRegime: "The flight departs from the UK, so the UK rules (UK261) apply and pay in pounds.",
      ukArrival: "The flight arrives in the UK with a UK or EU airline, so the UK rules (UK261) apply.",
      alsoEU: "Arriving in the EU with an EU airline, EU261 (in euros) may also apply. You can only be paid once.",
      bands: ["up to 1,500 km", "over 1,500 km within Europe", "1,500 to 3,500 km", "over 3,500 km"],
      dist: function (d, band, base) { return "Distance: " + d + " km (" + band + ") → base of " + base + " per passenger."; },
      lt3: "With an arrival delay of less than 3 hours there is no cash compensation.",
      lt3note: "Even so, from 2 hours (short flights) the airline owes you food, drinks and a way to communicate.",
      half: function (m) { return "On flights over 3,500 km with a 3 to 4 hour delay, compensation is halved: " + m + "."; },
      full: "You arrived 3 or more hours late: full compensation applies.",
      gt14: "If you were told about the cancellation 14 or more days in advance, there is no compensation.",
      gt14note: "You can still choose between a refund or an alternative flight.",
      cancel: "Cancellation notified less than 14 days ahead: compensation applies.",
      n7to14: "Unless you were offered an alternative flight leaving no more than 2 hours earlier and arriving no more than 4 hours later than the original.",
      nlt7: "Unless you were offered an alternative flight leaving no more than 1 hour earlier and arriving no more than 2 hours later than the original.",
      denied: "You were denied boarding against your will (for example, overbooking): compensation applies.",
      extra: "The airline claims extraordinary circumstances (weather, air traffic control strike, security). If it can prove it, it does not have to pay.",
      extraNote: "The burden of proof is on the airline. Airlines often blame the weather when the real cause was different; a claims company checks this for free.",
      strike: "Strikes by the airline's own staff do not exempt it from paying (Court of Justice of the EU, 2021).",
      tech: "Technical problems with the aircraft generally do not exempt the airline from paying.",
      yes: function (m) { return "You are owed " + m + " per passenger"; },
      maybe: function (m) { return "You could be owed " + m + " per passenger"; },
      none: "Based on these details, no compensation is due",
      copied: "Letter copied. Paste it into the airline's claim form or email.",
      selected: "Text selected: copy it with Ctrl+C or a long press.",
      downloaded: "Letter downloaded.", dlFail: "Download failed. Use the copy button instead.",
      file: "flight-claim.txt"
    }
  }[LANG];
  var airports = [], byCode = {};

  function norm(s) { return (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function cityOf(a) { return (LANG === "en" ? ALIAS_EN[a[0]] : ALIAS_ES[a[0]]) || a[2] || a[1]; }
  function label(a) { return cityOf(a) + " (" + a[0] + ")"; }
  function km(a, b) {
    var R = 6371, r = Math.PI / 180;
    var dLat = (b[4] - a[4]) * r, dLon = (b[5] - a[5]) * r;
    var h = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(a[4] * r) * Math.cos(b[4] * r) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
    return Math.round(2 * R * Math.asin(Math.sqrt(h)));
  }
  function fmt(n) { return n.toLocaleString(LANG === "en" ? "en-GB" : "es-ES"); }
  function money(n, cur) {
    if (LANG === "en") return (cur === "GBP" ? "£" : "€") + fmt(n);
    return fmt(n) + (cur === "GBP" ? " £" : " €");
  }
  var UK = { GB: 1, GG: 1, JE: 1, IM: 1 };

  // ---------- Rule engine: EU261 (Reglamento CE 261/2004) and UK261 ----------
  function compute(o) {
    var r = { amount: 0, verdict: "no", lines: [], notes: [], cur: "EUR", regime: "EU" };
    var dep = o.dep, arr = o.arr;
    var dist = km(dep, arr);
    r.dist = dist;
    var al = o.airline || {};
    var carrier = al.eu || "unknown";
    var ukCarrier = !!al.uk;
    var intra = false, covered = false;

    if (UK[dep[3]]) {
      covered = true; r.regime = "UK"; r.cur = "GBP";
      r.lines.push(T.ukRegime);
      if (arr[6] === 1 && carrier === "yes") r.notes.push(T.alsoEU);
    } else if (dep[6] === 1) {
      covered = true; intra = arr[6] === 1;
    } else if (arr[6] === 1) {
      if (carrier === "yes") { covered = true; }
      else if (carrier === "mixed" || carrier === "unknown") { covered = true; r.notes.push(T.maybeCarrier); r.verdict = "maybe"; }
    } else if (UK[arr[3]] && (ukCarrier || carrier === "yes")) {
      covered = true; r.regime = "UK"; r.cur = "GBP"; r.lines.push(T.ukArrival);
    }
    if (!covered) { r.lines.push(T.notCovered); return r; }

    var tiers = r.regime === "UK" ? [220, 350, 520] : [250, 400, 600];
    var base = dist <= 1500 ? tiers[0] : (intra || dist <= 3500) ? tiers[1] : tiers[2];
    var band = dist <= 1500 ? T.bands[0] : intra ? T.bands[1] : dist <= 3500 ? T.bands[2] : T.bands[3];
    r.lines.push(T.dist(fmt(dist), band, money(base, r.cur)));
    var amount = base;

    if (o.what === "delay") {
      if (o.delay === "lt3") { r.lines.push(T.lt3); r.notes.push(T.lt3note); r.amount = 0; r.verdict = "no"; return r; }
      if (o.delay === "3to4" && base === tiers[2]) { amount = base / 2; r.lines.push(T.half(money(amount, r.cur))); }
      else r.lines.push(T.full);
    } else if (o.what === "cancel") {
      if (o.notice === "gt14") { r.lines.push(T.gt14); r.notes.push(T.gt14note); r.amount = 0; r.verdict = "no"; return r; }
      r.lines.push(T.cancel);
      r.notes.push(o.notice === "7to14" ? T.n7to14 : T.nlt7);
    } else if (o.what === "denied") {
      r.lines.push(T.denied);
    }
    if (o.cause === "extra") { r.lines.push(T.extra); r.notes.push(T.extraNote); r.amount = amount; r.verdict = "maybe"; return r; }
    if (o.cause === "strike") r.lines.push(T.strike);
    if (o.cause === "tech") r.lines.push(T.tech);
    r.amount = amount;
    if (r.verdict !== "maybe") r.verdict = "yes";
    return r;
  }
  window.CTT_compute = compute; // exposed for tests

  // ---------- Autocomplete ----------
  function search(q) {
    q = norm(q.trim());
    if (!q) return [];
    var out = [];
    for (var i = 0; i < airports.length && out.length < 60; i++) {
      var a = airports[i], code = a[0].toLowerCase();
      var es = ALIAS_ES[a[0]] || "", en = ALIAS_EN[a[0]] || "";
      var score = -1;
      if (code === q) score = 100;
      else if (norm(cityOf(a)).indexOf(q) === 0) score = 80;
      else if (norm(es).indexOf(q) === 0 || norm(en).indexOf(q) === 0 || norm(a[2]).indexOf(q) === 0) score = 70;
      else if (norm(es + " " + en + " " + a[1] + " " + a[2]).indexOf(q) >= 0) score = 50;
      var home = LANG === "en" ? (a[3] === "ES" || UK[a[3]]) : a[3] === "ES";
      if (score >= 0) out.push([score + (home ? 5 : 0) + (a[6] ? 2 : 0), a]);
    }
    out.sort(function (x, y) { return y[0] - x[0]; });
    return out.slice(0, 7).map(function (x) { return x[1]; });
  }

  function attach(input) {
    var list = document.getElementById(input.getAttribute("aria-controls"));
    var items = [], active = -1;
    function close() { list.hidden = true; input.setAttribute("aria-expanded", "false"); active = -1; }
    function pick(a) { input.value = label(a); input.dataset.code = a[0]; close(); run(); }
    function render() {
      items = search(input.value);
      list.innerHTML = "";
      items.forEach(function (a, i) {
        var li = document.createElement("li");
        li.id = input.id + "-opt-" + i;
        li.setAttribute("role", "option");
        li.innerHTML = '<span class="opt-code"></span><span class="opt-txt"><b></b><small></small></span>';
        li.querySelector(".opt-code").textContent = a[0];
        li.querySelector("b").textContent = cityOf(a);
        li.querySelector("small").textContent = a[1];
        li.addEventListener("mousedown", function (e) { e.preventDefault(); pick(a); });
        list.appendChild(li);
      });
      list.hidden = items.length === 0;
      input.setAttribute("aria-expanded", items.length ? "true" : "false");
    }
    function highlight() {
      Array.prototype.forEach.call(list.children, function (li, i) { li.classList.toggle("on", i === active); });
      if (active >= 0) input.setAttribute("aria-activedescendant", input.id + "-opt-" + active);
    }
    input.addEventListener("input", function () { input.dataset.code = ""; render(); });
    input.addEventListener("focus", function () { if (!input.dataset.code) render(); else input.select(); });
    input.addEventListener("blur", function () { setTimeout(close, 100); });
    input.addEventListener("keydown", function (e) {
      if (list.hidden) return;
      if (e.key === "ArrowDown") { active = Math.min(active + 1, items.length - 1); highlight(); e.preventDefault(); }
      else if (e.key === "ArrowUp") { active = Math.max(active - 1, 0); highlight(); e.preventDefault(); }
      else if (e.key === "Enter") { if (items[active >= 0 ? active : 0]) pick(items[active >= 0 ? active : 0]); e.preventDefault(); }
      else if (e.key === "Escape") close();
    });
  }

  // ---------- Form wiring ----------
  var form, out;
  function val(name) { var el = form.querySelector('[name="' + name + '"]:checked') || form.querySelector('[name="' + name + '"]'); return el ? el.value : ""; }
  function syncVisibility() {
    var what = val("what");
    form.querySelector("#grp-delay").hidden = what !== "delay";
    form.querySelector("#grp-notice").hidden = what !== "cancel";
  }
  function run() {
    syncVisibility();
    var dep = byCode[form.querySelector("#from").dataset.code];
    var arr = byCode[form.querySelector("#to").dataset.code];
    if (!dep || !arr || dep === arr) { out.dataset.state = "empty"; var cb = out.querySelector("[data-care]"); if (cb) cb.hidden = true; var wb = out.querySelector("[data-where]"); if (wb) wb.hidden = true; return; }
    var slug = val("airline");
    var al = AIRLINES.filter(function (x) { return x.slug === slug; })[0] || { eu: slug === "otra-ue" ? "yes" : slug === "otra-no-ue" ? "no" : "unknown" };
    var r = compute({ dep: dep, arr: arr, airline: al, what: val("what"), delay: val("delay"), notice: val("notice"), cause: val("cause") });
    out.dataset.state = r.verdict;
    out.querySelector("[data-route]").textContent = dep[0] + " → " + arr[0];
    out.querySelector("[data-km]").textContent = fmt(r.dist || 0) + " km";
    out.querySelector("[data-amount]").textContent = money(r.amount || 0, r.cur);
    out.querySelector("[data-headline]").textContent =
      r.verdict === "yes" ? T.yes(money(r.amount, r.cur))
      : r.verdict === "maybe" && r.amount ? T.maybe(money(r.amount, r.cur))
      : T.none;
    var ul = out.querySelector("[data-lines]"); ul.innerHTML = "";
    r.lines.concat(r.notes).forEach(function (t, i) { var li = document.createElement("li"); li.textContent = t; if (i >= r.lines.length) li.className = "note"; ul.appendChild(li); });
    care(r.dist || 0, val("what"));
    where(al, r, dep);
    out.querySelector("[data-cta]").hidden = !r.amount;
    var alName = (form.querySelector("#airline").selectedOptions[0] || {}).textContent || "";
    last = { r: r, dep: dep, arr: arr, what: val("what"), delay: val("delay"), notice: val("notice"),
      airline: (slug && slug.indexOf("otra") !== 0) ? alName : "" };
    letter();
  }

  // ---------- Right to care (art. 6, 8, 9 Reg. 261/2004) ----------
  function care(dist, what) {
    var box = out.querySelector("[data-care]"); if (!box) return;
    var en = LANG === "en", h = dist <= 1500 ? 2 : dist <= 3500 ? 3 : 4, items;
    if (what === "delay") {
      items = en ? [
        "Meals and drinks if your flight leaves " + h + "+ hours late (for this distance).",
        "A hotel and transfers if the new departure is the next day.",
        "Delayed 5+ hours? You can give up the trip and get a full refund (but then there's no delay compensation)."
      ] : [
        "Comida y bebida si el vuelo sale con " + h + " h o más de retraso (para esta distancia).",
        "Hotel y traslados si la salida se pasa al día siguiente.",
        "¿Más de 5 h de retraso? Puedes renunciar al viaje y pedir el reembolso completo (pero entonces no hay compensación por retraso)."
      ];
    } else {
      items = en ? [
        "Your choice of a full refund within 7 days or a new flight.",
        "Meals and drinks while you wait for the new flight.",
        "A hotel and transfers if you have to stay overnight."
      ] : [
        "A tu elección: reembolso completo en 7 días o un vuelo alternativo.",
        "Comida y bebida mientras esperas el vuelo alternativo.",
        "Hotel y traslados si tienes que pasar la noche."
      ];
    }
    var head = en ? "On top of that, while you wait you're owed:" : "Además, mientras esperas te deben:";
    var tip = en ? "Didn't get it and paid yourself? Keep the receipts: the airline must pay you back, even if the cause was extraordinary."
      : "¿No te lo dieron y lo pagaste tú? Guarda los tickets: la aerolínea tiene que devolvértelo, aunque la causa sea extraordinaria.";
    box.innerHTML = "<h3></h3><ul></ul><p class=\"tip\"></p>";
    box.querySelector("h3").textContent = head;
    items.forEach(function (t) { var li = document.createElement("li"); li.textContent = t; box.querySelector("ul").appendChild(li); });
    box.querySelector(".tip").textContent = tip;
    box.hidden = false;
  }

  // ---------- Where to claim (official airline channel + escalation) ----------
  function where(al, r, dep) {
    var box = out.querySelector("[data-where]"); if (!box) return;
    var en = LANG === "en", h = "", name = al && al.name;
    if (name && al.claim) {
      h += "<p><strong>" + (en ? "Claim from " + name + " for free: " : "Reclama gratis a " + name + ": ") + "</strong>" +
        '<a href="' + al.claim + '" rel="noopener nofollow" target="_blank">' + (en ? "official claim page" : "página oficial de reclamación") + "</a>.</p>";
      if (al.note) h += "<p>" + al.note.replace(/</g, "&lt;") + "</p>";
    }
    var esc;
    if (r.regime === "UK") {
      var adr = al && al.adr;
      esc = en ? "If they refuse or don't reply in 8 weeks: " + (adr && adr !== "CAA" ? adr + " (the airline's free dispute scheme)" : "the CAA's free complaints service (PACT)") + "."
        : "Si lo rechazan o no contestan en 8 semanas: " + (adr && adr !== "CAA" ? adr + " (mediación gratuita)" : "el servicio de reclamaciones de la CAA, gratuito") + ".";
    } else if (dep && dep[3] === "ES") {
      esc = en ? "If they refuse or don't reply in 8 weeks: AESA, Spain's aviation authority (free)." : "Si lo rechazan o no contestan en 8 semanas: AESA, gratis.";
    } else {
      esc = en ? "If they refuse or don't reply in 8 weeks: the aviation authority of the departure country (free)." : "Si lo rechazan o no contestan en 8 semanas: el organismo de aviación del país de salida, gratis.";
    }
    h += "<p class=\"tip\">" + esc + "</p>";
    box.innerHTML = "<h3>" + (en ? "Where to claim" : "Dónde reclamar") + "</h3>" + h;
    box.hidden = !r.amount;
  }

  // ---------- Claim letter (runs only in the browser) ----------
  var last = null;
  function fval(id) { var el = document.getElementById(id); return el ? el.value.trim() : ""; }
  function fdate(iso, ph) {
    if (!iso) return ph;
    var p = iso.split("-"); return p[2] + "/" + p[1] + "/" + p[0];
  }
  function letterES(L, d) {
    var facts, legal;
    if (L.what === "delay") {
      facts = "El vuelo llegó a su destino final con un retraso " + (L.delay === "3to4" ? "de entre 3 y 4 horas" : "de más de 4 horas") + ".";
      legal = "los artículos 6 y 7 del Reglamento (CE) n.º 261/2004 y la sentencia del Tribunal de Justicia de la UE de 19 de noviembre de 2009 (asuntos C-402/07 y C-432/07, Sturgeon), que reconoce el derecho a compensación a partir de 3 horas de retraso en la llegada";
    } else if (L.what === "cancel") {
      facts = "El vuelo fue cancelado y se me informó con " + (L.notice === "7to14" ? "entre 7 y 14 días" : "menos de 7 días") + " de antelación, sin ofrecerme un transporte alternativo dentro de los plazos que establece el reglamento.";
      legal = "los artículos 5 y 7 del Reglamento (CE) n.º 261/2004";
    } else {
      facts = "Se me denegó el embarque contra mi voluntad, a pesar de presentarme a tiempo con la documentación en regla.";
      legal = "los artículos 4 y 7 del Reglamento (CE) n.º 261/2004";
    }
    if (L.r.regime === "UK") legal = legal.replace("Reglamento (CE) n.º 261/2004", "Reglamento (CE) n.º 261/2004 en su versión vigente en el Reino Unido (UK261)");
    var n = d.n;
    return "Asunto: Reclamación de compensación, vuelo " + d.flight + " del " + d.date + "\n\n" +
      "A la atención de " + (L.airline || "[aerolínea]") + ", servicio de atención al cliente:\n\n" +
      "Yo, " + d.name + ", viajé " + (n > 1 ? "junto con " + (n - 1) + " pasajero" + (n > 2 ? "s" : "") + " más " : "") +
      "con la reserva " + d.booking + " en el vuelo " + d.flight + " del " + d.date + ", de " + d.route + ".\n\n" +
      facts + "\n\n" +
      "De acuerdo con " + legal + ", solicito una compensación de " + money(L.r.amount, L.r.cur) + " por pasajero" +
      (n > 1 ? " (" + money(L.r.amount * n, L.r.cur) + " en total por " + n + " pasajeros)" : "") +
      ", correspondiente a un vuelo de " + fmt(L.r.dist) + " km.\n\n" +
      (d.iban ? "Les ruego que realicen el pago en un plazo de 30 días a la cuenta " + d.iban + ", a nombre de " + d.name + "." :
        "Les ruego que me indiquen en un plazo de 30 días cómo realizarán el pago.") + "\n\n" +
      "Si no recibo una respuesta satisfactoria, presentaré la reclamación ante la autoridad nacional competente (en España, la Agencia Estatal de Seguridad Aérea, AESA) y, en su caso, ante los tribunales.\n\n" +
      "Adjunto la tarjeta de embarque y la confirmación de la reserva.\n\n" +
      "Atentamente,\n" + d.name + "\n" + d.today + "\n";
  }
  function letterEN(L, d) {
    var facts, legal;
    if (L.what === "delay") {
      facts = "The flight arrived at its final destination " + (L.delay === "3to4" ? "between 3 and 4 hours" : "more than 4 hours") + " late.";
      legal = "Articles 6 and 7 of Regulation (EC) No 261/2004 and the judgment of the Court of Justice of the EU of 19 November 2009 (Joined Cases C-402/07 and C-432/07, Sturgeon), which recognises the right to compensation for arrival delays of 3 hours or more";
    } else if (L.what === "cancel") {
      facts = "The flight was cancelled and I was informed " + (L.notice === "7to14" ? "between 7 and 14 days" : "less than 7 days") + " before departure, without being offered alternative transport within the time limits set by the regulation.";
      legal = "Articles 5 and 7 of Regulation (EC) No 261/2004";
    } else {
      facts = "I was denied boarding against my will, although I presented myself on time with valid travel documents.";
      legal = "Articles 4 and 7 of Regulation (EC) No 261/2004";
    }
    if (L.r.regime === "UK") legal = legal.replace("Regulation (EC) No 261/2004", "Regulation (EC) No 261/2004 as retained in UK law (UK261)");
    var n = d.n;
    return "Subject: Compensation claim, flight " + d.flight + " on " + d.date + "\n\n" +
      "To " + (L.airline || "[airline]") + " customer services,\n\n" +
      "I, " + d.name + ", travelled " + (n > 1 ? "with " + (n - 1) + " other passenger" + (n > 2 ? "s" : "") + " " : "") +
      "under booking " + d.booking + " on flight " + d.flight + " on " + d.date + ", from " + d.route + ".\n\n" +
      facts + "\n\n" +
      "Under " + legal + ", I request compensation of " + money(L.r.amount, L.r.cur) + " per passenger" +
      (n > 1 ? " (" + money(L.r.amount * n, L.r.cur) + " in total for " + n + " passengers)" : "") +
      ", corresponding to a flight distance of " + fmt(L.r.dist) + " km.\n\n" +
      (d.iban ? "Please make the payment within 30 days to account " + d.iban + ", in the name of " + d.name + "." :
        "Please let me know within 30 days how you will make the payment.") + "\n\n" +
      "If I do not receive a satisfactory reply, I will refer the claim to the competent national enforcement body (in Spain, AESA; in the UK, the CAA or an approved ADR scheme) and, if necessary, to the courts.\n\n" +
      "Please find attached my boarding pass and booking confirmation.\n\n" +
      "Yours faithfully,\n" + d.name + "\n" + d.today + "\n";
  }
  function letter() {
    var box = document.getElementById("letter-text");
    if (!box || !last || !last.r.amount) return;
    var L = last, en = LANG === "en";
    var today = new Date();
    var d = {
      n: Math.max(1, Math.min(9, parseInt(fval("l-pax"), 10) || 1)),
      name: fval("l-name") || (en ? "[your full name]" : "[tu nombre y apellidos]"),
      flight: fval("l-flight").toUpperCase() || (en ? "[flight number]" : "[número de vuelo]"),
      booking: fval("l-booking").toUpperCase() || (en ? "[booking reference]" : "[código de reserva]"),
      date: fdate(fval("l-date"), en ? "[flight date]" : "[fecha del vuelo]"),
      iban: fval("l-iban").replace(/\s+/g, " ").toUpperCase(),
      route: cityOf(L.dep) + " (" + L.dep[0] + ")" + (en ? " to " : " a ") + cityOf(L.arr) + " (" + L.arr[0] + ")",
      today: ("0" + today.getDate()).slice(-2) + "/" + ("0" + (today.getMonth() + 1)).slice(-2) + "/" + today.getFullYear()
    };
    box.value = en ? letterEN(L, d) : letterES(L, d);
  }
  function letterTools() {
    var panel = document.getElementById("letter");
    if (!panel) return;
    panel.addEventListener("input", letter);
    var copy = document.getElementById("letter-copy"), dl = document.getElementById("letter-dl"), msg = document.getElementById("letter-msg");
    copy.addEventListener("click", function () {
      var t = document.getElementById("letter-text");
      function sel() { t.focus(); t.select(); msg.textContent = T.selected; }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(t.value).then(function () { msg.textContent = T.copied; }, sel);
      } else sel();
    });
    dl.addEventListener("click", function () {
      try {
        var blob = new Blob([document.getElementById("letter-text").value], { type: "text/plain;charset=utf-8" });
        var a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = T.file;
        document.body.appendChild(a); a.click(); a.remove();
        msg.textContent = T.downloaded;
      } catch (e) { msg.textContent = T.dlFail; }
    });
    var open = document.getElementById("letter-open");
    open.addEventListener("click", function () {
      panel.hidden = !panel.hidden; open.setAttribute("aria-expanded", String(!panel.hidden));
      if (!panel.hidden) { letter(); document.getElementById("l-name").focus(); }
    });
  }

  function init() {
    form = document.getElementById("calc");
    out = document.getElementById("result");
    if (!form) return;
    form.addEventListener("submit", function (e) { e.preventDefault(); run(); });
    form.addEventListener("change", function (e) { if (!e.target.closest || !e.target.closest("#letter")) run(); });
    letterTools();
    // Blogs embedding the calculator may use their own affiliate link (known claims domains only)
    try {
      var aff = new URLSearchParams(location.search).get("aff");
      if (aff) {
        var u = new URL(aff), ok = /(^|\.)(airhelp\.com|airadvisor\.com|compensair\.com|flightright\.(es|com|de|co\.uk)|skyrefund\.com|reclamador\.es|tp\.media|travelpayouts\.com|postaffiliatepro\.com)$/.test(u.hostname);
        if (u.protocol === "https:" && ok) { var a = out.querySelector("[data-cta] a"); if (a) a.href = u.href; }
      }
    } catch (err) { /* invalid parameter: keep the default link */ }
    ["from", "to"].forEach(function (id) { attach(document.getElementById(id)); });
    fetch(cfg.dataUrl).then(function (r) { return r.json(); }).then(function (d) {
      airports = d; d.forEach(function (a) { byCode[a[0]] = a; });
      ["from", "to"].forEach(function (id) { var el = document.getElementById(id); var a = byCode[el.dataset.code]; if (a) el.value = label(a); });
      run();
    }).catch(function () { out.dataset.state = "error"; });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
