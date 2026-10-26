"""Strike calendar page (ES + EN): upcoming air-travel strikes affecting Spain/UK/Europe + what you're owed.
Linkable, newsjackable asset. Update STRIKES and UPDATED when news changes.
"""
import json
from html import escape as e

UPDATED = {"es": "25 de octubre de 2026", "en": "25 October 2026", "iso": "2026-10-25"}
SRC_MIN = "https://www.transportes.gob.es/aviacion-civil/informacion-util-al-pasajero/huelga-servicios-minimos"
# Official sources only: Spain's Transport Ministry, Italy's Transport Ministry strike calendar (Osservatorio sui conflitti
# sindacali), the union that called the strike (CCOO for 11-N, Unite for Leeds Bradford).
SRC_IT = "https://www.mit.gov.it/come-fare-per/trasporti/calendario-scioperi-trasporti"
SRC_GEN = "https://huelga.ccoo.es/"
SRC_LBA = "https://www.unitetheunion.org/news-events/news/2026/october/leeds-bradford-airport-strikes-suspended-for-talks"

# date_sort, ES when, EN when, ES what, EN what, where, kind(airline|atc|airport|general), status ES, status EN, source
STRIKES = [
    ("2026-10-01", "Hasta el 30 nov", "Until 30 Nov", "Control aéreo de torre (SAERCO), huelga indefinida", "Control tower staff (SAERCO), open-ended strike",
     "Jerez, A Coruña, Sevilla, Vigo, Fuerteventura, Lanzarote, La Palma, El Hierro, Madrid-Cuatro Vientos", "atc", "Con servicios mínimos", "Minimum services set", SRC_MIN),
    ("2026-10-01", "Hasta el 30 nov", "Until 30 Nov", "Handling de Groundforce en El Prat (CGT), indefinida", "Groundforce ground handling at El Prat (CGT), open-ended",
     "Barcelona-El Prat", "airport", "Con servicios mínimos", "Minimum services set", SRC_MIN),
    ("2026-10-01", "Hasta el 30 nov (lun, jue, vie, sáb, dom)", "Until 30 Nov (Mon, Thu, Fri, Sat, Sun)", "Sistema de equipajes de Barajas (Outsmart), paros de 05:00–07:00 y 13:00–15:00",
     "Barajas baggage system (Outsmart), stoppages 05:00–07:00 and 13:00–15:00", "Madrid-Barajas", "airport", "Con servicios mínimos", "Minimum services set", SRC_MIN),
    ("2026-10-23", "23 oct – 2 nov", "23 Oct – 2 Nov", "Personal del aeropuerto, incluidos los controladores (Unite)", "Airport staff, including air traffic controllers (Unite)",
     "Leeds Bradford (Reino Unido)", "airport", "Suspendida mientras se negocia con mediación de Acas", "Suspended while Acas-brokered talks take place", SRC_LBA),
    ("2026-11-06", "6 nov, 13:00–17:00", "6 Nov, 13:00–17:00", "Control aéreo (ENAV) en el aeropuerto de Bari", "Air traffic control (ENAV) at Bari airport",
     "Bari (Italia)", "atc", "Convocada", "Scheduled", SRC_IT),
    ("2026-11-06", "6 nov, 13:00–17:00", "6 Nov, 13:00–17:00", "Control aéreo de Italia (ENAV), huelga nacional (Filt CGIL y UGL TA)", "Italian air traffic control (ENAV), national strike (Filt CGIL and UGL TA)",
     "Toda Italia", "atc", "Sin confirmar: no figura en todos los calendarios; los mismos sindicatos tienen convocada otra el 21 nov", "Not confirmed: not in every calendar; the same unions have one called for 21 Nov", SRC_IT),
    ("2026-11-11", "11 nov, 24 h", "11 Nov, 24 h", "Huelga general en España (CCOO y UGT)", "General strike in Spain (CCOO and UGT unions)",
     "Toda España: posible impacto en tierra y en el transporte al aeropuerto", "general", "Convocada; servicios mínimos en aeropuertos aún sin publicar", "Called; airport minimum services not yet published", SRC_GEN),
    ("2026-11-20", "20 nov, toda la jornada", "20 Nov, all day", "Huelga general en Italia (CGIL)", "General strike in Italy (CGIL union)",
     "Toda Italia", "general", "Convocada; no consta en el calendario del transporte aéreo, efecto en los vuelos sin confirmar", "Called; not listed in the air transport calendar, effect on flights not confirmed", SRC_IT),
    ("2026-11-21", "21 nov, 13:00–17:00", "21 Nov, 13:00–17:00", "Control aéreo de Italia (ENAV), huelga nacional (Filt CGIL y UGL TA)", "Italian air traffic control (ENAV), national strike (Filt CGIL and UGL TA)",
     "Toda Italia", "atc", "Convocada", "Scheduled", SRC_IT),
    ("2026-11-22", "22 nov, 24 h", "22 Nov, 24 h", "Control aéreo (ENAV) en Malpensa", "Air traffic control (ENAV) at Malpensa",
     "Milán-Malpensa (Italia)", "atc", "Convocada", "Scheduled", SRC_IT),
    ("2026-11-22", "22 nov, 24 h", "22 Nov, 24 h", "Personal de seguridad del aeropuerto (Sicuritalia IVRI)", "Airport security staff (Sicuritalia IVRI)",
     "Venecia (Italia)", "airport", "Convocada", "Scheduled", SRC_IT),
]

# English for the "where" column (the table above keeps it in Spanish); every place must have a translation (test_mantenimiento.py)
WHERE_EN = {
    "Barcelona-El Prat": "Barcelona-El Prat", "Madrid-Barajas": "Madrid-Barajas",
    "Jerez, A Coruña, Sevilla, Vigo, Fuerteventura, Lanzarote, La Palma, El Hierro, Madrid-Cuatro Vientos":
        "Jerez, A Coruña, Seville, Vigo, Fuerteventura, Lanzarote, La Palma, El Hierro, Madrid-Cuatro Vientos",
    "Leeds Bradford (Reino Unido)": "Leeds Bradford (UK)", "Bari (Italia)": "Bari (Italy)", "Toda Italia": "All of Italy",
    "Milán-Malpensa (Italia)": "Milan Malpensa (Italy)", "Venecia (Italia)": "Venice (Italy)",
    "Toda España: posible impacto en tierra y en el transporte al aeropuerto": "All of Spain: possible impact on ground services and transport to the airport",
}

KIND = {
    "es": {"airline": "Plantilla de la aerolínea", "atc": "Control aéreo", "airport": "Aeropuerto / handling", "general": "Huelga general"},
    "en": {"airline": "Airline staff", "atc": "Air traffic control", "airport": "Airport / ground handling", "general": "General strike"},
}
COMP = {
    "es": {"airline": "Normalmente sí", "atc": "Normalmente no", "airport": "Depende", "general": "Depende"},
    "en": {"airline": "Usually yes", "atc": "Usually no", "airport": "It depends", "general": "It depends"},
}

CHECKER_JS = r"""
(function(){var f=document.getElementById('sk-form');if(!f)return;var L=document.documentElement.lang==='en';
f.addEventListener('submit',function(ev){ev.preventDefault();var d=new Date(document.getElementById('sk-flight').value+'T12:00:00'),n=new Date(document.getElementById('sk-notice').value+'T12:00:00'),o=document.getElementById('sk-out');
if(isNaN(d)||isNaN(n)){o.textContent=L?'Enter both dates.':'Pon las dos fechas.';return;}
var days=Math.round((d-n)/864e5),k=document.getElementById('sk-kind').value;
var msg;if(days<0){msg=L?'The notice date is after the flight: check the dates.':'La fecha del aviso es posterior al vuelo: revisa las fechas.';}
else if(days>=14){msg=L?('You were told '+days+' days before: no fixed compensation for the cancellation, but you can still choose a full refund or a new flight.'):('Te avisaron con '+days+' días: no hay compensación fija por la cancelación, pero sí puedes elegir reembolso completo o vuelo alternativo.');}
else if(k==='airline'){msg=L?('Told '+days+' days before and it was the airline\'s own staff: you are very likely owed €250–€600 per passenger, plus a refund or new flight.'):('Te avisaron con '+days+' días y la huelga era de la propia plantilla de la aerolínea: muy probablemente te tocan 250–600 € por pasajero, además de reembolso o vuelo alternativo.');}
else if(k==='atc'){msg=L?('Told '+days+' days before, but air traffic control strikes are usually extraordinary circumstances: compensation is unlikely. You are still owed a refund or new flight, plus meals and hotel while you wait.'):('Te avisaron con '+days+' días, pero las huelgas de control aéreo suelen ser circunstancia extraordinaria: es difícil cobrar compensación. Sí te deben reembolso o vuelo alternativo, y comida y hotel mientras esperas.');}
else{msg=L?('Told '+days+' days before. With airport or general strikes it depends on whether the airline could have avoided the cancellation: ask it in writing for the exact cause. Refund or new flight plus meals and hotel are owed either way.'):('Te avisaron con '+days+' días. En huelgas de aeropuerto o generales depende de si la aerolínea podía haber evitado la cancelación: pídele la causa por escrito. El reembolso o vuelo alternativo, y la comida y el hotel, te los deben igualmente.');}
o.textContent=msg;});})();
"""


MON = {m: i + 1 for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}


def end_date(s):
    """Last day of a strike, from the English date text ("Until 30 Nov", "23 Oct – 2 Nov") or the start date."""
    import re
    start, wen = s[0], s[2]
    m = re.findall(r"(\d{1,2}) ([A-Z][a-z]{2})", wen)
    if not m:
        return start
    d, mon = int(m[-1][0]), MON[m[-1][1].lower()]
    y = int(start[:4]) + (1 if mon < int(start[5:7]) else 0)
    return f"{y:04d}-{mon:02d}-{d:02d}"


# Rows whose last day has passed are hidden in the browser, so an outdated calendar never shows past strikes as upcoming.
EXPIRE_JS = ("(function(){var t=new Date(),d=t.getFullYear()+'-'+('0'+(t.getMonth()+1)).slice(-2)+'-'+('0'+t.getDate()).slice(-2),n=0;"
             "document.querySelectorAll('tr[data-end]').forEach(function(r){if(r.getAttribute('data-end')<d){r.hidden=true}else n++});"
             "var m=document.getElementById('sk-none');if(m&&!n)m.hidden=false;})();")


def _rows(l):
    out = []
    for s in sorted(STRIKES, key=lambda x: x[0]):
        _, wes, wen, des, den, where, kind, ses, sen, src = s
        when, what, st = (wes, des, ses) if l == "es" else (wen, den, sen)
        if l == "en":
            where = WHERE_EN[where]
        out.append(f"<tr data-end=\"{end_date(s)}\"><td>{e(when)}</td><td>{e(what)}<br><small>{e(where)}</small></td><td>{KIND[l][kind]}</td><td>{COMP[l][kind]}</td>"
                   f"<td>{e(st)} · <a href=\"{src}\" rel=\"noopener\">{'fuente' if l == 'es' else 'source'}</a></td></tr>")
    return "".join(out)


def build(ctx):
    paths = {"es": "/huelgas-vuelos-espana/", "en": "/en/flight-strikes-spain-europe/"}
    for l in ("es", "en"):
        other = "en" if l == "es" else "es"
        if l == "es":
            title = "Huelgas de vuelos noviembre 2026: calendario y qué te deben"
            desc = "Huelga general del 11N, control aéreo en Italia y más: calendario de huelgas de vuelos de noviembre de 2026 con fuentes oficiales y cuándo te pagan 250–600 €."
            h1 = "Huelgas que afectan a vuelos en España: calendario y tus derechos"
            lead = (f"Actualizado el {UPDATED['es']}. Estas son las huelgas convocadas que pueden afectar a vuelos con salida o llegada en España y a los destinos europeos más habituales. "
                    "Si te cancelan el vuelo con menos de 14 días de aviso, lo que decide si cobras 250–600 € es <strong>quién hace la huelga</strong>.")
            th = "<th>Cuándo</th><th>Qué y dónde</th><th>Tipo</th><th>¿Compensación?</th><th>Estado</th>"
            rules = f"""<h2>¿Me pagan si cancelan mi vuelo por huelga?</h2>
<ul><li><strong>Huelga de la plantilla de la propia aerolínea</strong> (pilotos, tripulantes): normalmente <strong>sí</strong>. El Tribunal de Justicia de la UE dice que no es una circunstancia extraordinaria (asunto C-28/20).</li>
<li><strong>Huelga de control aéreo</strong>: normalmente <strong>no</strong>, porque la aerolínea no la controla.</li>
<li><strong>Huelga de aeropuerto, handling o huelga general</strong>: <strong>depende</strong> de si la aerolínea podía haber evitado la cancelación. Pídele la causa por escrito.</li>
<li><strong>Siempre</strong>, sea cual sea la huelga: reembolso completo en 7 días o vuelo alternativo, y comida, bebida y hotel mientras esperas.</li>
<li><strong>Si te avisan con 14 días o más</strong>, no hay compensación fija por la cancelación. Por ejemplo, para la huelga general del 11 de noviembre, una cancelación avisada el 28 de octubre o antes no daría compensación.</li></ul>
<p>Guía completa: <a href="/huelga-general-11-noviembre-vuelos/">huelga general del 11 de noviembre y tu vuelo</a>.</p>"""
            checker = """<h2>¿Me toca algo? Compruébalo</h2>
<form id="sk-form" class="sk"><label>Fecha del vuelo <input type="date" id="sk-flight" required></label>
<label>Fecha en que te avisaron de la cancelación <input type="date" id="sk-notice" required></label>
<label>¿Quién hacía huelga? <select id="sk-kind"><option value="airline">La plantilla de la aerolínea</option><option value="atc">Control aéreo</option><option value="airport">Aeropuerto o handling</option><option value="general">Huelga general</option></select></label>
<button class="btn btn-sign" type="submit">Comprobar</button></form><p id="sk-out" class="lead" aria-live="polite"></p>
<p>¿Retraso en vez de cancelación? <a href="/">Calcula el importe exacto de tu ruta aquí</a>.</p>"""
            src = f"<p><small>Fuentes: <a href=\"{SRC_MIN}\">Ministerio de Transportes, servicios mínimos</a> · <a href=\"{SRC_IT}\">Ministerio de Infraestructuras y Transportes de Italia, calendario de huelgas</a> · <a href=\"{SRC_GEN}\">CCOO, huelga general del 11 de noviembre</a> · <a href=\"{SRC_LBA}\">Unite, aeropuerto de Leeds Bradford</a>. Las convocatorias pueden cambiar o desconvocarse; revisa con tu aerolínea.</small></p>"
            faq = [("¿Me devuelven el dinero si cancelan mi vuelo por huelga?", "Sí. Sea cual sea la huelga, puedes elegir el reembolso completo del billete en 7 días o un vuelo alternativo, y la aerolínea debe darte comida y hotel si tienes que esperar."),
                   ("¿Me pagan compensación si la huelga es de controladores?", "Normalmente no: las huelgas de control aéreo se consideran circunstancias extraordinarias. Sí tienes derecho al reembolso o a un vuelo alternativo y a asistencia."),
                   ("¿Y si la huelga es de los pilotos o tripulantes de la aerolínea?", "Entonces normalmente sí: el Tribunal de Justicia de la UE considera que la huelga de la propia plantilla no es extraordinaria, así que te tocan 250, 400 o 600 € si te avisan con menos de 14 días.")]
        else:
            title = "Flight strikes November 2026: Spain & Europe calendar"
            desc = "Spain's 11 Nov general strike, Italian ATC strikes and more: November 2026 flight strike calendar from official sources, and when you're owed €250–600."
            h1 = "Strikes affecting flights to and from Spain: calendar and your rights"
            lead = (f"Updated {UPDATED['en']}. These are the strikes called that may affect flights to and from Spain and the most common European connections. "
                    "If your flight is cancelled with less than 14 days' notice, what decides whether you get €250–€600 is <strong>who is on strike</strong>.")
            th = "<th>When</th><th>What and where</th><th>Type</th><th>Compensation?</th><th>Status</th>"
            rules = f"""<h2>Will I be compensated if my flight is cancelled by a strike?</h2>
<ul><li><strong>The airline's own staff on strike</strong> (pilots, cabin crew): usually <strong>yes</strong>. The EU Court of Justice ruled this is not an extraordinary circumstance (case C-28/20).</li>
<li><strong>Air traffic control strike</strong>: usually <strong>no</strong>, because the airline can't control it.</li>
<li><strong>Airport, ground handling or general strike</strong>: <strong>it depends</strong> on whether the airline could have avoided the cancellation. Ask it for the cause in writing.</li>
<li><strong>Always</strong>, whatever the strike: a full refund within 7 days or a new flight, plus meals, drinks and a hotel while you wait.</li>
<li><strong>Told 14 days or more in advance</strong>: no fixed compensation for the cancellation. For the 11 November general strike, a cancellation notified on or before 28 October would not carry compensation.</li></ul>
<p>Full guide: <a href="/en/spain-general-strike-11-november-flights/">Spain general strike on 11 November and your flight</a>.</p>"""
            checker = """<h2>Am I owed anything? Check it</h2>
<form id="sk-form" class="sk"><label>Flight date <input type="date" id="sk-flight" required></label>
<label>Date you were told about the cancellation <input type="date" id="sk-notice" required></label>
<label>Who was on strike? <select id="sk-kind"><option value="airline">The airline's own staff</option><option value="atc">Air traffic control</option><option value="airport">Airport or ground handling</option><option value="general">General strike</option></select></label>
<button class="btn btn-sign" type="submit">Check</button></form><p id="sk-out" class="lead" aria-live="polite"></p>
<p>Delayed rather than cancelled? <a href="/en/">Work out the exact amount for your route here</a>.</p>"""
            src = f"<p><small>Sources: <a href=\"{SRC_MIN}\">Spanish Ministry of Transport, minimum services</a> · <a href=\"{SRC_IT}\">Italian Ministry of Infrastructure and Transport, strike calendar</a> · <a href=\"{SRC_GEN}\">CCOO, 11 November general strike</a> · <a href=\"{SRC_LBA}\">Unite, Leeds Bradford Airport</a>. Strikes can change or be called off; check with your airline.</small></p>"
            faq = [("Do I get a refund if my flight is cancelled by a strike?", "Yes. Whatever the strike, you can choose a full refund within 7 days or a new flight, and the airline must provide meals and a hotel if you have to wait."),
                   ("Do I get compensation for an air traffic control strike?", "Usually not: ATC strikes count as extraordinary circumstances. You are still owed a refund or rerouting and care while you wait."),
                   ("What if the airline's pilots or cabin crew are on strike?", "Then usually yes: the EU Court of Justice treats an airline's own staff strike as not extraordinary, so you're owed €250, €400 or €600 if told less than 14 days before.")]
        faq_html = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faq)
        faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
        body = f"""<div class="wrap prose"><h1>{h1}</h1><p class="lead">{lead}</p>
<div class="board"><table><thead><tr>{th}</tr></thead><tbody>{_rows(l)}</tbody></table></div>
<p id="sk-none" class="lead" hidden>{'No quedan huelgas vigentes en este calendario. Consulta las fuentes de abajo por si hay convocatorias nuevas.' if l == 'es' else 'No strikes in this calendar are still ongoing. Check the sources below for new ones.'}</p>
<script>{EXPIRE_JS}</script>
{checker}
{rules}
<h2>{'Preguntas frecuentes' if l == 'es' else 'Common questions'}</h2>{faq_html}
{src}</div>
<style>.sk{{display:grid;gap:12px;max-width:520px;margin:12px 0}}.sk label{{display:grid;gap:4px;font-weight:600}}.sk input,.sk select{{font:inherit;padding:10px;border:1px solid var(--line);border-radius:8px;background:transparent;color:inherit}}</style>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
<script>{CHECKER_JS}</script>"""
        ctx["emit"](l, paths[l], ctx["page"](l, title, desc, paths[l], body, paths, paths[other]))
    return list(paths.values())
