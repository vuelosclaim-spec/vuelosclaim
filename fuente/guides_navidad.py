"""Guías de temporada (nov. 2026): reforma europea 2027, medidas del equipaje de mano y vuelos adelantados/cambio de horario.
Solo datos comprobados: Reglamento (UE) 2026/2202 (fechas según el seguimiento legislativo del Parlamento Europeo),
medidas de equipaje leídas el 16-11-2026 en la web oficial de cada aerolínea y la sentencia del TJUE de 21-12-2021.
"""

EP_TRAIN = "https://www.europarl.europa.eu/legislative-train/spotlight-JD22/file-common-rules-on-compensation-to-passengers"
EP_TEXT = {"es": "https://data.europarl.europa.eu/distribution/doc/TA-10-2026-0238_es.pdf",
           "en": "https://data.europarl.europa.eu/distribution/doc/TA-10-2026-0238_en.pdf"}
R261 = {"es": "https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32004R0261",
        "en": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32004R0261"}
DOT_REFUND = "https://www.transportation.gov/briefing-room/what-airline-passengers-need-know-about-dots-automatic-refund-rule"
CURIA_2021 = "https://curia.europa.eu/juris/liste.jsf?num=C-146/20"

# Equipaje de mano, comprobado el 16-11-2026 en la web oficial de cada aerolínea.
# (nombre, gratis bajo el asiento (cm), maleta de cabina (cm, kg), cuándo incluye la maleta ES, EN, fuente)
BAGS = [
    ("Ryanair", (40, 30, 20), (55, 40, 20), 10, "Con «Prioridad y 2 piezas de equipaje de cabina» (de pago)", "With 'Priority & 2 cabin bags' (paid)",
     "https://help.ryanair.com/hc/es-es/articles/12888036565521"),
    ("Vueling", (40, 30, 20), (55, 40, 20), 10, "Tarifas Fly (eligiéndola), Fly Pro y Fly Grande, o pagándola", "Fly (if selected), Fly Pro and Fly Grande fares, or paid",
     "https://www.vueling.com/es/prepara-tu-viaje/equipaje/equipaje-de-cabina"),
    ("Iberia", (40, 30, 15), (56, 40, 25), 10, "Incluida en todas las tarifas", "Included in all fares",
     "https://www.iberia.com/es/luggage/hand-luggage/"),
    ("Air Europa", (40, 30, 15), (55, 35, 25), 10, "Incluida (turista)", "Included (economy)",
     "https://www.aireuropa.com/es/es/aea/informacion-para-volar/equipaje/equipaje-de-mano.html"),
    ("easyJet", (45, 36, 20), (56, 45, 25), 15, "De pago, o con easyJet Plus / Inclusive Plus", "Paid, or with easyJet Plus / Inclusive Plus",
     "https://www.easyjet.com/es/ayuda/equipaje/equipaje-de-mano"),
    ("Volotea", (40, 30, 20), (55, 40, 25), 10, "Con embarque prioritario o Megavolotea", "With priority boarding or Megavolotea",
     "https://www.volotea.com/es/equipaje/"),
]

def _dims(t):
    return " × ".join(str(v) for v in t) + " cm"

def bag_table(l):
    es = l == "es"
    head = ("<tr><th>Aerolínea</th><th>Gratis bajo el asiento</th><th>Maleta de cabina</th><th>¿Cuándo va incluida la maleta?</th></tr>" if es else
            "<tr><th>Airline</th><th>Free under-seat bag</th><th>Cabin bag</th><th>When is the cabin bag included?</th></tr>")
    rows = "".join(f'<tr><td><a href="{src}" rel="nofollow noopener" target="_blank">{n}</a></td><td>{_dims(f)}</td><td>{_dims(c)}, {kg} kg</td><td>{inc_es if es else inc_en}</td></tr>'
                   for n, f, c, kg, inc_es, inc_en, src in BAGS)
    return f'<div class="tbl"><table class="bg-t">{head}{rows}</table></div>'

def bag_checker(l):
    import json
    es = l == "es"
    data = json.dumps([[n, list(f), list(c)] for n, f, c, *_ in BAGS])
    lab = ("Alto (cm)", "Ancho (cm)", "Fondo (cm)", "Comprobar", "Introduce las tres medidas de tu maleta o mochila, incluidas asas y ruedas.") if es else \
          ("Height (cm)", "Width (cm)", "Depth (cm)", "Check", "Enter all three measurements of your bag, including handles and wheels.")
    js = ("(function(){var B=%s,L=%s,f=document.getElementById('bg-form');if(!f)return;f.addEventListener('submit',function(e){e.preventDefault();"
          "var v=['bg-a','bg-b','bg-c'].map(function(i){return parseFloat(document.getElementById(i).value.replace(',','.'))});var o=document.getElementById('bg-out');"
          "if(v.some(function(x){return !(x>0)})){o.textContent=L?'Introduce las tres medidas.':'Enter all three measurements.';return;}"
          "v.sort(function(a,b){return b-a});function fits(d){d=d.slice().sort(function(a,b){return b-a});return v[0]<=d[0]&&v[1]<=d[1]&&v[2]<=d[2]}"
          "var free=[],cab=[],no=[];B.forEach(function(r){if(fits(r[1]))free.push(r[0]);else if(fits(r[2]))cab.push(r[0]);else no.push(r[0])});"
          "var h='';if(free.length)h+='<p><strong>'+(L?'Gratis bajo el asiento en: ':'Free under the seat with: ')+free.join(', ')+'</strong></p>';"
          "if(cab.length)h+='<p>'+(L?'Solo como maleta de cabina (compartimento superior) en: ':'Only as a cabin bag (overhead locker) with: ')+cab.join(', ')+'</p>';"
          "if(no.length)h+='<p>'+(L?'No cabe en cabina en: ':'Too big for the cabin with: ')+no.join(', ')+'</p>';"
          "o.innerHTML=h+'<p class=\"lead\">'+(L?'Orientativo: comprueba siempre tu tarifa y el peso.':'Indicative only: always check your fare and the weight limit.')+'</p>'})})();") % (data, "true" if es else "false")
    st = ("<style>#bg-form .bg-g{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}#bg-form label{display:grid;gap:6px;font-weight:600;font-size:.9rem}"
          "#bg-form input{font:inherit;padding:12px;border:1px solid var(--line-strong,#bbb);border-radius:10px;width:100%;box-sizing:border-box}"
          "#bg-out p{margin:.4rem 0}.bg-t{width:100%;border-collapse:collapse;font-size:.95rem}.bg-t th,.bg-t td{border-bottom:1px solid var(--line,#ddd);padding:10px 8px;text-align:left;vertical-align:top}"
          ".tbl{overflow-x:auto}</style>")
    return (f'{st}<form id="bg-form" class="calc" style="margin:1rem 0"><p style="margin:0">{lab[4]}</p><div class="bg-g">'
            f'<label>{lab[0]}<input id="bg-a" inputmode="decimal" required></label>'
            f'<label>{lab[1]}<input id="bg-b" inputmode="decimal" required></label>'
            f'<label>{lab[2]}<input id="bg-c" inputmode="decimal" required></label></div>'
            f'<button type="submit" class="btn btn-sign">{lab[3]}</button></form><div id="bg-out" aria-live="polite"></div><script>{js}</script>')

TSTYLE = "<style>.bg-t{width:100%;border-collapse:collapse;font-size:.95rem}.bg-t th,.bg-t td{border-bottom:1px solid var(--line,#ddd);padding:10px 8px;text-align:left;vertical-align:top}.tbl{overflow-x:auto}</style>"

NAVIDAD2 = [
 {"paths": {"es": "/nuevas-normas-vuelos-2027/", "en": "/en/new-eu-air-passenger-rules-2027/"},
  "es": {
   "title": "Nuevas normas de vuelos 2027: qué cambia y qué sigue igual",
   "desc": "La UE reforma los derechos del pasajero aéreo (Reglamento 2026/2202), que se aplica desde el 23 de octubre de 2027. Qué cambia, qué no y qué vale hoy.",
   "h1": "Nuevas normas de vuelos en la UE: qué cambia en 2027 y qué vale estas Navidades",
   "lead": "La reforma de los derechos de los pasajeros aéreos ya es ley: es el Reglamento (UE) 2026/2202, publicado en el Diario Oficial de la UE el 2 de octubre de 2026. Pero no se aplica hasta el 23 de octubre de 2027. Hasta entonces, incluidas estas Navidades, sigue valiendo el Reglamento 261/2004 de siempre.",
   "body": f"""<h2>Las fechas clave</h2>
<ul><li><strong>7 de julio de 2026:</strong> el Parlamento Europeo aprueba el texto (<a href="{EP_TEXT['es']}" rel="noopener">resolución P10_TA(2026)0238</a>).</li>
<li><strong>2 de octubre de 2026:</strong> se publica en el Diario Oficial de la UE como Reglamento (UE) 2026/2202.</li>
<li><strong>23 de octubre de 2027:</strong> empieza a aplicarse (<a href="{EP_TRAIN}" rel="noopener">seguimiento legislativo del Parlamento Europeo</a>).</li></ul>
<h2>Qué sigue igual</h2>
<ul><li><strong>Compensación desde 3 horas de retraso:</strong> se mantiene el umbral de 3 horas. Los gobiernos habían propuesto subirlo a 4 o 6 horas y no salió adelante.</li>
<li><strong>Importes:</strong> 250 € hasta 1.500 km, 400 € entre 1.500 y 3.500 km y 600 € a partir de 3.500 km. En los vuelos más largos, la aerolínea puede pagar la mitad si llegas con menos de 4 horas de retraso, como ahora.</li>
<li><strong>Cancelaciones con menos de 14 días de aviso y overbooking:</strong> los mismos importes.</li>
<li><strong>Circunstancias extraordinarias:</strong> si la causa no depende de la aerolínea (mal tiempo, control aéreo…), no hay compensación, pero sí asistencia, y la aerolínea tiene que demostrarlo.</li></ul>
<h2>Qué cambia desde el 23 de octubre de 2027</h2>
<ul><li><strong>Objeto personal gratis:</strong> un bolso o mochila de hasta 40 × 30 × 15 cm bajo el asiento, en todas las aerolíneas.</li>
<li><strong>Maleta de cabina:</strong> no pasa a ser gratis. Las aerolíneas pueden seguir vendiendo tarifas sin ella, pero el precio debe mostrar claramente lo que cuesta.</li>
<li><strong>Vuelta garantizada:</strong> la aerolínea ya no podrá anularte la vuelta por no haber cogido la ida.</li>
<li><strong>Bonos:</strong> solo si tú los aceptas; si no los usas, te tienen que devolver el dinero.</li>
<li><strong>Más derechos al recolocarte:</strong> reglas más estrictas para llevarte a destino tras una cancelación o una conexión perdida, y más información durante las esperas en pista.</li></ul>
<p>Hay detalles que conviene leer en el texto definitivo antes de dar nada por hecho, como los nuevos plazos para presentar la reclamación. Iremos actualizando esta página.</p>
<h2>Y estas Navidades, ¿qué vale?</h2>
<p>La norma actual, el <a href="{R261['es']}" rel="noopener">Reglamento (CE) 261/2004</a>: si tu vuelo llega 3 horas o más tarde o te lo cancelan con menos de 14 días de aviso, pueden corresponderte 250, 400 o 600 € por pasajero, además del reembolso o un vuelo alternativo y comida y hotel mientras esperas. <a href="/">Calcula gratis cuánto te corresponde</a> o mira las <a href="/huelgas-vuelos-navidad/">huelgas de Navidad</a> y las <a href="/medidas-equipaje-de-mano/">medidas del equipaje de mano de cada aerolínea</a>.</p>""",
   "faq": [
    ("¿Las nuevas normas de vuelos ya están en vigor?", "Ya son ley (Reglamento (UE) 2026/2202, publicado el 2 de octubre de 2026), pero se aplican desde el 23 de octubre de 2027. Hasta entonces rige el Reglamento 261/2004."),
    ("¿La maleta de cabina será gratis desde 2027?", "No. Lo que será gratis en todas las aerolíneas es un objeto personal de hasta 40 × 30 × 15 cm bajo el asiento. La maleta de cabina se podrá seguir cobrando, aunque el precio tendrá que mostrarse con claridad."),
    ("¿Bajan las compensaciones por retraso?", "No. Se mantienen 250, 400 y 600 € según la distancia, a partir de 3 horas de retraso en la llegada."),
   ],
  },
  "en": {
   "title": "New EU air passenger rules 2027: what changes and what doesn't",
   "desc": "The EU has reformed air passenger rights (Regulation 2026/2202), applying from 23 October 2027. What changes, what stays the same and what applies now.",
   "h1": "New EU flight rules: what changes in 2027 and what applies this Christmas",
   "lead": "The reform of EU air passenger rights is now law: Regulation (EU) 2026/2202, published in the EU Official Journal on 2 October 2026. But it only applies from 23 October 2027. Until then, including this Christmas, Regulation 261/2004 still applies.",
   "body": f"""<h2>Key dates</h2>
<ul><li><strong>7 July 2026:</strong> the European Parliament approves the text (<a href="{EP_TEXT['en']}" rel="noopener">resolution P10_TA(2026)0238</a>).</li>
<li><strong>2 October 2026:</strong> published in the EU Official Journal as Regulation (EU) 2026/2202.</li>
<li><strong>23 October 2027:</strong> it starts to apply (<a href="{EP_TRAIN}" rel="noopener">European Parliament legislative train</a>).</li></ul>
<h2>What stays the same</h2>
<ul><li><strong>Compensation from a 3-hour delay:</strong> the 3-hour threshold is kept. Member states had proposed 4 or 6 hours; that was dropped.</li>
<li><strong>Amounts:</strong> €250 up to 1,500 km, €400 for 1,500–3,500 km and €600 above 3,500 km. On the longest flights the airline may pay half if you arrive less than 4 hours late, as now.</li>
<li><strong>Cancellations with under 14 days' notice and denied boarding:</strong> the same amounts.</li>
<li><strong>Extraordinary circumstances:</strong> if the cause is outside the airline's control (bad weather, air traffic control…) there's no compensation, but care still applies, and the airline has to prove it.</li></ul>
<h2>What changes from 23 October 2027</h2>
<ul><li><strong>Free personal item:</strong> a bag or backpack up to 40 × 30 × 15 cm under the seat, on every airline.</li>
<li><strong>Cabin bag:</strong> it does not become free. Airlines can still sell fares without one, but prices must show clearly what it costs.</li>
<li><strong>Return flight protected:</strong> airlines can no longer cancel your return because you missed the outbound.</li>
<li><strong>Vouchers:</strong> only if you accept them; if you don't use them, you get your money back.</li>
<li><strong>Stronger rerouting rights:</strong> stricter rules for getting you to your destination after a cancellation or missed connection, and more information during tarmac delays.</li></ul>
<p>Some details, such as new deadlines for filing a claim, are best read in the final text before relying on them. We'll keep this page updated.</p>
<h2>And this Christmas?</h2>
<p>The current rules apply: <a href="{R261['en']}" rel="noopener">Regulation (EC) 261/2004</a>. If your flight arrives 3+ hours late or is cancelled with less than 14 days' notice, you may be owed €250, €400 or €600 per passenger, plus a refund or new flight and meals and a hotel while you wait. <a href="/en/">Check for free what you're owed</a>, or see the <a href="/en/christmas-flight-strikes/">Christmas strikes</a> and <a href="/en/cabin-bag-size-by-airline/">cabin bag sizes by airline</a>.</p>""",
   "faq": [
    ("Are the new EU flight rules already in force?", "They are law (Regulation (EU) 2026/2202, published on 2 October 2026) but apply from 23 October 2027. Until then, Regulation 261/2004 applies."),
    ("Will cabin bags be free from 2027?", "No. What becomes free on every airline is a personal item up to 40 × 30 × 15 cm under the seat. Airlines can still charge for a cabin bag, but must show the price clearly."),
    ("Is delay compensation being cut?", "No. It stays at €250, €400 and €600 depending on distance, from a 3-hour arrival delay."),
   ],
  },
 },
 {"paths": {"es": "/medidas-equipaje-de-mano/", "en": "/en/cabin-bag-size-by-airline/"},
  "es": {
   "title": "Medidas del equipaje de mano por aerolínea (noviembre 2026)",
   "desc": "Medidas del bolso gratis y de la maleta de cabina en Ryanair, Vueling, Iberia, Air Europa, easyJet y Volotea, comprobadas en su web, y comprobador gratis.",
   "h1": "Medidas del equipaje de mano por aerolínea: ¿cabe tu maleta?",
   "lead": "Antes de volar en Navidad, comprueba qué puedes llevar gratis en cabina. Hemos revisado una por una las medidas en la web oficial de cada aerolínea el 16 de noviembre de 2026. Las medidas incluyen asas y ruedas.",
   "body": f"""<h2>Comprueba si cabe tu maleta</h2>
{bag_checker('es')}
<h2>Tabla de medidas por aerolínea</h2>
{bag_table('es')}
<p>El enlace de cada aerolínea lleva a su página oficial de equipaje. Las condiciones pueden cambiar: revisa siempre tu reserva antes de volar.</p>
<h2>Lo que conviene saber</h2>
<ul><li><strong>El bolso bajo el asiento es gratis en todas</strong>, pero sus medidas no son iguales: easyJet admite 45 × 36 × 20 cm; Iberia y Air Europa, 40 × 30 × 15 cm.</li>
<li><strong>Iberia y Air Europa incluyen la maleta de cabina de 10 kg</strong> en su tarifa turista. En Ryanair, Vueling (tarifa básica), easyJet y Volotea normalmente se paga aparte.</li>
<li><strong>Pagar en la puerta sale caro:</strong> por ejemplo, Volotea indica 65 € por pieza y trayecto si llevas la maleta a cabina sin haberla contratado.</li>
<li><strong>Con el avión lleno</strong>, la aerolínea puede mandar tu maleta a la bodega sin coste.</li></ul>
<h2>¿Cambiará en 2027?</h2>
<p>Sí, en parte. Con la reforma europea, desde el 23 de octubre de 2027 todas las aerolíneas tendrán que dejar llevar gratis un objeto personal de hasta 40 × 30 × 15 cm, pero la maleta de cabina se podrá seguir cobrando. Lo explicamos en <a href="/nuevas-normas-vuelos-2027/">nuevas normas de vuelos 2027</a>.</p>
<h2>Si tu maleta se pierde o llega tarde</h2>
<p>Tienes 7 días para reclamar los daños de una maleta facturada y 21 días si llega con retraso. Lo explicamos en <a href="/equipaje-perdido-retrasado/">equipaje perdido o retrasado</a>.</p>""",
   "faq": [
    ("¿Cuánto mide la maleta gratis de Ryanair?", "40 × 30 × 20 cm y debe caber bajo el asiento delantero. La maleta de cabina de 10 kg (55 × 40 × 20 cm) va con la opción de prioridad, que es de pago."),
    ("¿Qué aerolíneas incluyen la maleta de cabina de 10 kg?", "Entre las que hemos revisado, Iberia la incluye en todas sus tarifas y Air Europa en clase turista. En Ryanair, Vueling (tarifa básica), easyJet y Volotea normalmente se paga aparte."),
    ("¿Las medidas incluyen las ruedas y las asas?", "Sí. Todas las aerolíneas de la tabla miden la pieza completa, con asas, ruedas y bolsillos."),
   ],
  },
  "en": {
   "title": "Cabin bag size by airline (November 2026)",
   "desc": "Free under-seat bag and cabin bag sizes for Ryanair, Vueling, Iberia, Air Europa, easyJet and Volotea, checked on their websites, plus a free size checker.",
   "h1": "Cabin bag size by airline: will your bag fit?",
   "lead": "Before you fly this Christmas, check what you can take on board for free. We checked each airline's official website on 16 November 2026. Sizes include handles and wheels.",
   "body": f"""<h2>Check whether your bag fits</h2>
{bag_checker('en')}
<h2>Sizes by airline</h2>
{bag_table('en')}
<p>Each airline name links to its official baggage page. Rules can change: always check your booking before you fly.</p>
<h2>Worth knowing</h2>
<ul><li><strong>The under-seat bag is free on all of them</strong>, but sizes differ: easyJet allows 45 × 36 × 20 cm; Iberia and Air Europa 40 × 30 × 15 cm.</li>
<li><strong>Iberia and Air Europa include a 10 kg cabin bag</strong> in economy. On Ryanair, Vueling (basic fare), easyJet and Volotea it is usually paid separately.</li>
<li><strong>Paying at the gate is expensive:</strong> for example, Volotea charges €65 per bag per flight if you bring an unbooked cabin bag.</li>
<li><strong>On full flights</strong>, the airline may put your cabin bag in the hold free of charge.</li></ul>
<h2>Will it change in 2027?</h2>
<p>Partly. Under the EU reform, from 23 October 2027 every airline must let you bring a free personal item up to 40 × 30 × 15 cm, but cabin bags can still be charged. See <a href="/en/new-eu-air-passenger-rules-2027/">new EU air passenger rules 2027</a>.</p>
<h2>If your bag is lost or delayed</h2>
<p>You have 7 days to claim for a damaged checked bag and 21 days if it arrives late. See <a href="/en/lost-delayed-baggage-compensation/">lost or delayed baggage</a>.</p>""",
   "faq": [
    ("What size is Ryanair's free bag?", "40 × 30 × 20 cm, and it must fit under the seat in front. The 10 kg cabin bag (55 × 40 × 20 cm) comes with the paid Priority option."),
    ("Which airlines include a 10 kg cabin bag?", "Of those we checked, Iberia includes it on all fares and Air Europa in economy. On Ryanair, Vueling (basic fare), easyJet and Volotea it is usually paid separately."),
    ("Do the sizes include wheels and handles?", "Yes. All airlines in the table measure the whole bag, including handles, wheels and pockets."),
   ],
  },
 },
 {"paths": {"es": "/vuelo-adelantado-cambio-horario/", "en": "/en/flight-rescheduled-brought-forward-compensation/"},
  "es": {
   "title": "Me han adelantado el vuelo: ¿tengo derecho a compensación?",
   "desc": "Si la aerolínea adelanta tu vuelo más de una hora, la justicia europea lo trata como una cancelación: cuándo te corresponden 250–600 € y qué puedes pedir.",
   "h1": "Vuelo adelantado o cambio de horario: qué te corresponde",
   "lead": "En invierno las aerolíneas cambian muchos horarios. Si te adelantan el vuelo más de una hora, el Tribunal de Justicia de la UE considera que es una cancelación (sentencia de 21 de diciembre de 2021). Y una cancelación con poco aviso puede dar derecho a 250–600 € por pasajero.",
   "body": f"""<h2>La regla: adelanto de más de una hora = cancelación</h2>
<p>El <a href="{CURIA_2021}" rel="noopener">Tribunal de Justicia de la UE</a> (asuntos acumulados C-146/20, C-188/20, C-196/20 y C-270/20, y asuntos C-263/20 y C-395/20, de 21 de diciembre de 2021) decidió que un vuelo adelantado más de una hora se considera cancelado. A partir de ahí se aplican las reglas de las cancelaciones del <a href="{R261['es']}" rel="noopener">Reglamento 261/2004</a>.</p>
<h2>¿Me pagan? Depende de cuándo te avisaron</h2>
{TSTYLE}<div class="tbl"><table class="bg-t"><tr><th>Te avisaron…</th><th>¿Compensación?</th></tr>
<tr><td>14 días o más antes del vuelo</td><td>No</td></tr>
<tr><td>Entre 7 y 13 días antes</td><td>Sí, salvo que el vuelo nuevo salga como mucho 2 h antes y llegue menos de 4 h después del original</td></tr>
<tr><td>Menos de 7 días antes</td><td>Sí, salvo que el vuelo nuevo salga como mucho 1 h antes y llegue menos de 2 h después del original</td></tr></table></div>
<p>Fuente: art. 5.1.c del Reglamento 261/2004. Los importes son los de siempre: 250 €, 400 € o 600 € según la distancia.</p>
<h2>Ejemplo</h2>
<p>Caso hipotético: tienes un Madrid–Tenerife (unos 1.750 km) a las 18:00 y, 5 días antes, la aerolínea lo adelanta a las 16:00. Es un adelanto de 2 horas con menos de 7 días de aviso, así que se trata como una cancelación: pueden corresponderte 400 € por pasajero.</p>
<h2>Siempre puedes elegir</h2>
<ul><li><strong>Reembolso del billete</strong> en 7 días si el nuevo horario no te sirve (art. 8).</li>
<li><strong>Otro vuelo</strong> lo antes posible o en la fecha que te venga bien.</li>
<li>Guarda el correo o el aviso del cambio, con su fecha: es la prueba de cuándo te avisaron.</li></ul>
<h2>¿Y si me lo retrasan?</h2>
<p>Si el cambio es a una hora más tarde, lo que cuenta es a qué hora llegas comparado con el horario de tu billete. Si es un cambio importante y no te sirve, puedes pedir el reembolso. <a href="/">Introduce los datos de tu vuelo</a> y te decimos si te corresponde algo, o lee <a href="/vuelo-cancelado-que-hacer/">qué hacer si te cancelan el vuelo</a>.</p>""",
   "faq": [
    ("¿Me compensan si adelantan mi vuelo?", "Si lo adelantan más de una hora, el TJUE lo trata como una cancelación. Si te avisaron con menos de 14 días y el nuevo horario no cumple los márgenes del art. 5.1.c, pueden corresponderte 250–600 € por pasajero."),
    ("¿Puedo pedir el reembolso si cambian el horario?", "Si el cambio equivale a una cancelación, sí: puedes elegir el reembolso del billete en 7 días o un vuelo alternativo."),
    ("¿Qué pruebas necesito?", "El correo o el SMS de la aerolínea con el cambio y su fecha, y la confirmación de tu reserva original con el horario inicial."),
   ],
  },
  "en": {
   "title": "Flight brought forward? When you're owed compensation",
   "desc": "If your airline brings your flight forward by more than an hour, EU case law treats it as a cancellation: when you're owed €250–600 and what you can ask for.",
   "h1": "Flight brought forward or rescheduled: what you're owed",
   "lead": "Airlines change a lot of schedules in winter. If your flight is brought forward by more than an hour, the EU Court of Justice treats it as a cancellation (ruling of 21 December 2021). And a short-notice cancellation can mean €250–600 per passenger.",
   "body": f"""<h2>The rule: more than one hour earlier = cancellation</h2>
<p>The <a href="{CURIA_2021}" rel="noopener">EU Court of Justice</a> (joined cases C-146/20, C-188/20, C-196/20 and C-270/20, and cases C-263/20 and C-395/20, 21 December 2021) ruled that a flight brought forward by more than one hour counts as cancelled. The cancellation rules of <a href="{R261['en']}" rel="noopener">Regulation 261/2004</a> then apply.</p>
<h2>Will I be paid? It depends on when you were told</h2>
{TSTYLE}<div class="tbl"><table class="bg-t"><tr><th>You were told…</th><th>Compensation?</th></tr>
<tr><td>14 days or more before the flight</td><td>No</td></tr>
<tr><td>7 to 13 days before</td><td>Yes, unless the new flight leaves no more than 2 h earlier and arrives less than 4 h later than the original</td></tr>
<tr><td>Less than 7 days before</td><td>Yes, unless the new flight leaves no more than 1 h earlier and arrives less than 2 h later than the original</td></tr></table></div>
<p>Source: Article 5(1)(c) of Regulation 261/2004. The usual amounts apply: €250, €400 or €600 depending on distance.</p>
<h2>Example</h2>
<p>Hypothetical case: you're booked Madrid–Tenerife (about 1,750 km) at 18:00 and, 5 days before, the airline moves it to 16:00. That's 2 hours earlier with under 7 days' notice, so it's treated as a cancellation: you may be owed €400 per passenger.</p>
<h2>You can always choose</h2>
<ul><li><strong>A refund</strong> within 7 days if the new time doesn't work for you (Art. 8).</li>
<li><strong>Another flight</strong> as soon as possible or on a date that suits you.</li>
<li>Keep the email or notice of the change, with its date: it proves when you were told.</li></ul>
<h2>What if it's moved later?</h2>
<p>If the flight is moved later, what counts is your arrival time compared with your original booking. If it's a major change that doesn't work for you, you can ask for a refund. <a href="/en/">Enter your flight</a> and we'll tell you if you're owed anything, or read <a href="/en/flight-cancelled-what-to-do/">what to do if your flight is cancelled</a>.</p>""",
   "faq": [
    ("Am I compensated if my flight is brought forward?", "If it's more than an hour earlier, the CJEU treats it as a cancellation. If you were told less than 14 days before and the new times fall outside the Article 5(1)(c) margins, you may be owed €250–600 per passenger."),
    ("Can I get a refund if the schedule changes?", "If the change amounts to a cancellation, yes: you can choose a refund within 7 days or an alternative flight."),
    ("What evidence do I need?", "The airline's email or text with the change and its date, and your original booking confirmation showing the original times."),
   ],
  },
 },
 {"paths": {"es": "/vuelo-cancelado-estados-unidos/", "en": "/en/us-flight-cancelled-eu261-compensation/"},
  "es": {
   "title": "Vuelo cancelado en Estados Unidos: qué te corresponde (UE y EE. UU.)",
   "desc": "Vuelo a o desde Nueva York u otra ciudad de EE. UU. cancelado o retrasado: cuándo se aplica el reglamento europeo (hasta 600 €) y cuándo solo el reembolso.",
   "h1": "Vuelo cancelado o retrasado en Estados Unidos: qué te corresponde",
   "lead": "Las cancelaciones masivas en Estados Unidos también dejan en tierra a pasajeros que vuelan desde o hacia España. Lo que te corresponde depende de dos cosas: desde dónde sale el vuelo y qué aerolínea lo opera.",
   "body": f"""<h2>¿Se aplica el reglamento europeo a tu vuelo?</h2>
{TSTYLE}<div class="tbl"><table class="bg-t"><tr><th>Tu vuelo</th><th>¿Reglamento 261/2004?</th></tr>
<tr><td>Sale de España o de otro país de la UE hacia EE. UU. (cualquier aerolínea)</td><td>Sí</td></tr>
<tr><td>Sale de EE. UU. hacia la UE con una aerolínea europea (Iberia, Air Europa, Level, Air France, Lufthansa…)</td><td>Sí</td></tr>
<tr><td>Sale de EE. UU. hacia la UE con una aerolínea no europea (American, Delta, United…)</td><td>No: se aplican las normas de EE. UU.</td></tr>
<tr><td>Vuelo interno dentro de EE. UU.</td><td>No, aunque lo hayas comprado en España</td></tr></table></div>
<p>Fuente: art. 3.1 del <a href="{R261["es"]}" rel="noopener">Reglamento (CE) 261/2004</a>. Si el vuelo cancelado forma parte de una misma reserva con salida en la UE, cuenta el viaje entero hasta el destino final.</p>
<h2>Si se aplica el reglamento europeo</h2>
<ul><li><strong>Siempre</strong>: puedes elegir entre el reembolso del billete en 7 días o otro vuelo lo antes posible (art. 8), y la aerolínea te debe comida, bebida y hotel si tienes que esperar (art. 9).</li>
<li><strong>Compensación</strong>: en un vuelo de más de 3.500 km, como Madrid–Nueva York, pueden corresponderte <strong>600 €</strong> por pasajero si te cancelan con menos de 14 días de aviso o llegas con más de 3 horas de retraso (300 € si te recolocan y llegas con menos de 4 horas de retraso, art. 7.2).</li>
<li><strong>Excepción</strong>: si la causa es una tormenta, una nevada o un cierre ordenado por el control aéreo de EE. UU. (la FAA), normalmente es una <a href="/circunstancias-extraordinarias-vuelo/">circunstancia extraordinaria</a> y no hay compensación. El reembolso o el vuelo alternativo y la asistencia te los deben igualmente.</li></ul>
<h2>Si se aplican solo las normas de EE. UU.</h2>
<p>El Departamento de Transporte de EE. UU. obliga a las aerolíneas a <a href="{DOT_REFUND}" rel="noopener">devolver automáticamente el dinero</a> si cancelan el vuelo o lo cambian de forma importante (más de 3 horas en vuelos internos o más de 6 en internacionales) y no aceptas la alternativa que te ofrecen. La devolución es a tu forma de pago original. Lo que no existe en EE. UU. es una compensación fija como la europea: comidas u hotel dependen de la política de cada aerolínea.</p>
<h2>Ejemplo</h2>
<p>Caso hipotético: vuelas Nueva York–Madrid con Iberia y te cancelan el vuelo el mismo día por una avería del avión. Se aplica el reglamento europeo porque Iberia es una aerolínea de la UE: tienes derecho a otro vuelo o al reembolso, a hotel y comida mientras esperas, y normalmente a 600 €. Si el mismo vuelo fuese con una aerolínea estadounidense, te correspondería el reembolso, pero no los 600 €.</p>
<h2>Qué hacer</h2>
<ol><li>Guarda la tarjeta de embarque, el aviso de cancelación y los tickets de lo que pagues.</li>
<li>Pide por escrito el motivo de la cancelación.</li>
<li>Si tu vuelo entra en el reglamento europeo, <a href="/">calcula gratis cuánto te corresponde</a> y genera la carta para reclamar tú mismo.</li></ol>""",
   "faq": [
    ("¿Me compensan si me cancelan un vuelo Nueva York–Madrid?", "Si lo opera una aerolínea europea, se aplica el reglamento 261/2004 y pueden corresponderte 600 € por pasajero, salvo circunstancias extraordinarias como una tormenta o un cierre del control aéreo. Si lo opera una aerolínea de EE. UU., solo tienes derecho al reembolso según las normas de EE. UU."),
    ("¿Y si el vuelo sale de Madrid hacia Nueva York?", "Se aplica siempre el reglamento europeo, sea cual sea la aerolínea, porque el vuelo sale de la UE."),
    ("¿Un cierre de la FAA da derecho a compensación?", "Normalmente no: un cierre decidido por el control aéreo es una circunstancia extraordinaria. Pero si tu vuelo entra en el reglamento europeo, te siguen debiendo el reembolso o un vuelo alternativo y la asistencia mientras esperas."),
    ("¿Y si el retraso o la cancelación se debe a una caída informática de la aerolínea?", "Si tu vuelo entra en el reglamento europeo, un fallo de los propios sistemas informáticos de la aerolínea forma parte de su actividad normal y no suele considerarse una circunstancia extraordinaria: si llegas con 3 horas o más de retraso o te cancelan con menos de 14 días de aviso, normalmente te corresponde la compensación. Distinto es si el fallo es del control aéreo (la FAA), que normalmente sí lo es."),
   ],
  },
  "en": {
   "title": "US flight cancelled: what you're owed (EU261 and US rules)",
   "desc": "Flight to or from New York or another US city cancelled or delayed: when EU261 applies (up to €600) and when you only get a refund under US rules.",
   "h1": "Flight cancelled or delayed in the US: what you're owed",
   "lead": "Mass cancellations in the US also strand passengers flying to and from Europe. What you're owed depends on two things: where the flight departs from and which airline operates it.",
   "body": f"""<h2>Does EU261 apply to your flight?</h2>
{TSTYLE}<div class="tbl"><table class="bg-t"><tr><th>Your flight</th><th>EU Regulation 261/2004?</th></tr>
<tr><td>Departs Spain or another EU country to the US (any airline)</td><td>Yes</td></tr>
<tr><td>Departs the US to the EU on a European airline (Iberia, Air Europa, Level, Air France, Lufthansa…)</td><td>Yes</td></tr>
<tr><td>Departs the US to the EU on a non-EU airline (American, Delta, United…)</td><td>No: US rules apply</td></tr>
<tr><td>Domestic flight within the US</td><td>No, even if you booked it in Europe</td></tr></table></div>
<p>Source: Article 3(1) of <a href="{R261["en"]}" rel="noopener">Regulation (EC) 261/2004</a>. If the cancelled flight is part of a single booking departing the EU, the whole journey to the final destination counts.</p>
<h2>If EU261 applies</h2>
<ul><li><strong>Always</strong>: you can choose a refund within 7 days or another flight as soon as possible (Art. 8), and the airline owes you meals, drinks and a hotel if you have to wait (Art. 9).</li>
<li><strong>Compensation</strong>: on a flight over 3,500 km, such as Madrid–New York, you may be owed <strong>€600</strong> per passenger if it's cancelled with less than 14 days' notice or you arrive more than 3 hours late (€300 if you're rerouted and arrive less than 4 hours late, Art. 7(2)).</li>
<li><strong>Exception</strong>: storms, snow or a ground stop ordered by US air traffic control (the FAA) are normally <a href="/en/extraordinary-circumstances-flight-delay/">extraordinary circumstances</a>, so no compensation. The refund or rerouting and the care are still owed.</li></ul>
<h2>If only US rules apply</h2>
<p>The US Department of Transportation requires airlines to <a href="{DOT_REFUND}" rel="noopener">refund you automatically</a> if they cancel your flight or change it significantly (more than 3 hours on domestic flights or more than 6 on international ones) and you don't accept the alternative offered. The refund goes back to your original form of payment. What US rules don't have is fixed compensation like the EU's: meals or hotels depend on each airline's policy.</p>
<h2>Example</h2>
<p>Hypothetical case: you fly New York–Madrid with Iberia and the flight is cancelled on the day because of a technical fault. EU261 applies because Iberia is an EU airline: you're entitled to another flight or a refund, a hotel and meals while you wait, and normally €600. If the same flight were with a US airline, you'd get a refund but not the €600.</p>
<h2>What to do</h2>
<ol><li>Keep your boarding pass, the cancellation notice and receipts for anything you pay for.</li>
<li>Ask the airline in writing for the reason for the cancellation.</li>
<li>If your flight is covered by EU261, <a href="/en/">check for free what you're owed</a> and generate a letter to claim yourself.</li></ol>""",
   "faq": [
    ("Am I compensated if my New York–Madrid flight is cancelled?", "If a European airline operates it, EU261 applies and you may be owed €600 per passenger, unless there are extraordinary circumstances such as a storm or an air traffic control ground stop. If a US airline operates it, you're only entitled to a refund under US rules."),
    ("What if the flight departs Madrid for New York?", "EU261 always applies, whatever the airline, because the flight departs the EU."),
    ("Does an FAA ground stop mean compensation?", "Normally not: a stop ordered by air traffic control is an extraordinary circumstance. But if your flight is covered by EU261, you're still owed a refund or rerouting and care while you wait."),
    ("What if the delay or cancellation is caused by an airline IT outage?", "If your flight is covered by EU261, a failure of the airline's own IT systems is part of its normal operations and is rarely treated as an extraordinary circumstance: if you arrive 3 hours or more late, or the flight is cancelled with less than 14 days' notice, compensation is normally due. It's different if the failure is in air traffic control (the FAA), which normally is extraordinary."),
   ],
  },
 },
 {"paths": {"es": "/aerolinea-deja-de-volar-quiebra/", "en": "/en/airline-stops-flying-bankruptcy/"},
  "es": {
   "title": "Aerolínea que deja de volar o en quiebra: qué te corresponde",
   "desc": "Tu aerolínea cancela todos sus vuelos o entra en concurso de acreedores, como Plus Ultra: reembolso, otro vuelo, compensación y cómo reclamar paso a paso.",
   "h1": "Tu aerolínea deja de volar o entra en quiebra: qué te corresponde",
   "lead": "Cuando una aerolínea suspende sus vuelos por problemas económicos, como ha ocurrido con Plus Ultra en noviembre de 2026, miles de pasajeros se quedan con un billete que no se va a volar. Tus derechos no desaparecen: un vuelo que no se opera es una cancelación, y el Reglamento 261/2004 sigue aplicándose. Lo que cambia es lo difícil que puede ser cobrar.",
   "body": f"""<h2>Qué te corresponde</h2>
<ul><li><strong>Reembolso u otro vuelo</strong>: si tu vuelo sale de la UE, o llega a la UE con una aerolínea europea (como Plus Ultra), tienes derecho a elegir entre el reembolso del billete en 7 días o un transporte alternativo hasta tu destino lo antes posible (arts. 5 y 8 del <a href="{R261["es"]}" rel="noopener">Reglamento (CE) 261/2004</a>).</li>
<li><strong>Asistencia</strong>: si estás esperando un vuelo alternativo, la aerolínea te debe comida, bebida y, si hace falta, hotel y traslados (art. 9).</li>
<li><strong>Compensación</strong>: si te avisan con menos de 14 días de antelación, pueden corresponderte 250, 400 o 600 € por pasajero según la distancia (art. 7), salvo que la aerolínea demuestre circunstancias extraordinarias.</li></ul>
<h2>El problema: cobrar a una aerolínea en crisis</h2>
<p>Si la aerolínea no paga, tu reembolso o tu compensación pasa a ser una deuda más de la empresa. Si se declara el concurso de acreedores, se publica en el BOE: vigila ese anuncio, porque abre el plazo para comunicar tu crédito a la administración concursal. Cuanto antes reclames por escrito, mejor documentado estará.</p>
<h2>Qué hacer, paso a paso</h2>
<ol><li><strong>Guarda todo</strong>: reserva, billete, tarjeta de embarque, el aviso de cancelación y los tickets de lo que pagues (hotel, comida, otro billete).</li>
<li><strong>Reclama por escrito a la aerolínea</strong> el reembolso o el vuelo alternativo, y la compensación si te avisaron con menos de 14 días. <a href="/">Calcula gratis cuánto te corresponde</a> y genera la carta.</li>
<li><strong>Si compraste en una agencia o en un paquete</strong> (vuelo más hotel), reclama también a la agencia u organizador del viaje.</li>
<li><strong>Si pagaste con tarjeta</strong>, pregunta a tu banco si puede retroceder el cargo de un servicio que no se ha prestado.</li>
<li><strong>Si en un mes no te responden</strong> o no estás de acuerdo, puedes reclamar gratis ante la <a href="https://www.seguridadaerea.gob.es/index.php/es/ambitos/derechos-de-los-pasajeros/inicia-tu-reclamacion-con-aesa" rel="noopener">Agencia Estatal de Seguridad Aérea (AESA)</a>.</li></ol>
<h2>Ejemplo</h2>
<p>Caso hipotético: tienes un Madrid–Lima para dentro de una semana y la aerolínea anuncia que deja de volar. Tienes derecho a elegir entre el reembolso o que te lleven a Lima lo antes posible, a asistencia mientras esperas y, como te avisan con menos de 14 días y el vuelo supera los 3.500 km, a reclamar 600 € por pasajero. Si la aerolínea no te ofrece alternativa y compras otro billete por tu cuenta, guarda el justificante: normalmente puedes reclamar su coste.</p>""",
   "faq": [
    ("¿Me devuelven el dinero si mi aerolínea deja de volar?", "Tienes derecho al reembolso en 7 días o a un vuelo alternativo según el Reglamento 261/2004. Si la aerolínea no paga, reclama por escrito, pregunta a tu banco por el contracargo si pagaste con tarjeta y, si se declara el concurso de acreedores, comunica tu crédito a la administración concursal."),
    ("¿También me corresponde compensación?", "Si te avisan con menos de 14 días y no hay circunstancias extraordinarias, pueden corresponderte 250, 400 o 600 € por pasajero según la distancia. Cobrarla depende de la situación de la aerolínea."),
    ("¿Y si el billete lo compré en una agencia?", "Reclama también a la agencia. Si era un viaje combinado (vuelo más hotel, por ejemplo), el organizador del viaje responde de que se preste."),
    ("¿Qué pasa con mis vuelos de Norse Atlantic?", "Según la prensa, Norse Atlantic suspendió sus vuelos el 25 de noviembre de 2026 por falta de financiación, sin fecha de vuelta. Es una aerolínea noruega y Noruega aplica el Reglamento 261/2004 por el Acuerdo EEE: si tu vuelo sale de la UE, de Noruega o del Reino Unido (allí rige la norma británica equivalente), o llega a la UE o a Noruega con Norse, tienes derecho a elegir entre el reembolso en 7 días o un vuelo alternativo y, si te avisan con menos de 14 días, puede corresponderte compensación. Reclama por escrito y guarda todo."),
   ],
  },
  "en": {
   "title": "Airline stops flying or goes bust: what you're owed",
   "desc": "Your airline cancels all its flights or enters insolvency, like Plus Ultra: refund, rerouting, compensation and how to claim, step by step.",
   "h1": "Your airline stops flying or goes bust: what you're owed",
   "lead": "When an airline suspends its flights because of financial trouble, as Plus Ultra did in November 2026, thousands of passengers are left with tickets that won't be flown. Your rights don't disappear: a flight that isn't operated is a cancellation, and Regulation 261/2004 still applies. What changes is how hard it can be to get paid.",
   "body": f"""<h2>What you're owed</h2>
<ul><li><strong>Refund or another flight</strong>: if your flight departs the EU, or arrives in the EU on a European airline (such as Plus Ultra), you can choose between a refund within 7 days or rerouting to your destination as soon as possible (Arts. 5 and 8 of <a href="{R261["en"]}" rel="noopener">Regulation (EC) 261/2004</a>).</li>
<li><strong>Care</strong>: while you wait for an alternative flight, the airline owes you meals, drinks and, if needed, a hotel and transfers (Art. 9).</li>
<li><strong>Compensation</strong>: if you're told less than 14 days in advance, you may be owed €250, €400 or €600 per passenger depending on distance (Art. 7), unless the airline proves extraordinary circumstances.</li></ul>
<h2>The problem: getting paid by an airline in crisis</h2>
<p>If the airline doesn't pay, your refund or compensation becomes one more of the company's debts. If insolvency proceedings are opened in Spain, they are published in the BOE (the Official State Gazette): watch for that notice, because it starts the deadline to submit your claim to the insolvency administrator. The sooner you claim in writing, the better documented it will be.</p>
<h2>What to do, step by step</h2>
<ol><li><strong>Keep everything</strong>: booking, ticket, boarding pass, the cancellation notice and receipts for anything you pay for (hotel, meals, a new ticket).</li>
<li><strong>Claim in writing from the airline</strong> for the refund or rerouting, and compensation if you were told less than 14 days ahead. <a href="/en/">Check for free what you're owed</a> and generate the letter.</li>
<li><strong>If you booked through an agency or as a package</strong> (flight plus hotel), claim from the agency or tour organiser too.</li>
<li><strong>If you paid by card</strong>, ask your bank whether it can reverse the charge for a service that wasn't provided.</li>
<li><strong>If there's no reply within a month</strong> or you disagree, you can complain free of charge to Spain's <a href="https://www.seguridadaerea.gob.es/index.php/es/ambitos/derechos-de-los-pasajeros/inicia-tu-reclamacion-con-aesa" rel="noopener">aviation safety agency (AESA)</a>.</li></ol>
<h2>Example</h2>
<p>Hypothetical case: you're booked Madrid–Lima next week and the airline announces it is stopping flights. You can choose a refund or to be taken to Lima as soon as possible, you're owed care while you wait and, because you were told less than 14 days ahead and the flight is over 3,500 km, you can claim €600 per passenger. If the airline offers no alternative and you buy another ticket yourself, keep the receipt: you can normally claim its cost.</p>""",
   "faq": [
    ("Will I get my money back if my airline stops flying?", "You're entitled to a refund within 7 days or an alternative flight under Regulation 261/2004. If the airline doesn't pay, claim in writing, ask your bank about a chargeback if you paid by card and, if insolvency proceedings are opened, submit your claim to the insolvency administrator."),
    ("Am I also owed compensation?", "If you're told less than 14 days ahead and there are no extraordinary circumstances, you may be owed €250, €400 or €600 per passenger depending on distance. Getting paid depends on the airline's situation."),
    ("What if I booked through an agency?", "Claim from the agency too. If it was a package (flight plus hotel, for example), the tour organiser is responsible for the trip being provided."),
    ("What about my Norse Atlantic flights?", "According to press reports, Norse Atlantic suspended its flights on 25 November 2026 for lack of funding, with no restart date. It is a Norwegian airline, and Norway applies Regulation 261/2004 under the EEA Agreement: if your flight departs the EU, Norway or the UK (where the equivalent UK rules apply), or arrives in the EU or Norway on Norse, you can choose between a refund within 7 days or an alternative flight and, if you were told less than 14 days ahead, you may be owed compensation. Claim in writing and keep everything."),
   ],
  },
 },
]
