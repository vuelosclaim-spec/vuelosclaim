"""Strike calendar page (ES + EN): upcoming air-travel strikes affecting Spain/UK/Europe + what you're owed.
Linkable, newsjackable asset. Update STRIKES and UPDATED when news changes.
"""
import json
from html import escape as e

UPDATED = {"es": "19 de octubre de 2026", "en": "19 October 2026", "iso": "2026-10-19"}
SRC_MIN = "https://www.transportes.gob.es/aviacion-civil/informacion-util-al-pasajero/huelga-servicios-minimos"
SRC_EU = "https://myflyright.com/blog/europe-flight-strikes-october-and-november-2026/"
SRC_GEN = "https://pixidia.com/es/huelga-general-espana-11-noviembre-2026"

# date_sort, ES when, EN when, ES what, EN what, where, kind(airline|atc|airport|general), status ES, status EN, source
STRIKES = [
    ("2026-10-01", "Hasta el 30 nov", "Until 30 Nov", "Control aéreo de torre (SAERCO), huelga indefinida", "Control tower staff (SAERCO), open-ended strike",
     "Jerez, A Coruña, Sevilla, Vigo, Fuerteventura, Lanzarote, La Palma, El Hierro, Madrid-Cuatro Vientos", "atc", "Con servicios mínimos", "Minimum services set", SRC_MIN),
    ("2026-10-01", "Hasta el 30 nov", "Until 30 Nov", "Handling de Groundforce en El Prat (CGT), indefinida", "Groundforce ground handling at El Prat (CGT), open-ended",
     "Barcelona-El Prat", "airport", "Con servicios mínimos", "Minimum services set", SRC_MIN),
    ("2026-10-01", "Hasta el 30 nov (lun, jue, vie, sáb, dom)", "Until 30 Nov (Mon, Thu, Fri, Sat, Sun)", "Sistema de equipajes de Barajas (Outsmart), paros de 05:00–07:00 y 13:00–15:00",
     "Barajas baggage system (Outsmart), stoppages 05:00–07:00 and 13:00–15:00", "Madrid-Barajas", "airport", "Con servicios mínimos", "Minimum services set", SRC_MIN),
    ("2026-10-23", "23 oct – 2 nov", "23 Oct – 2 Nov", "Acciones de protesta del personal del aeropuerto", "Proposed industrial action at the airport",
     "Leeds Bradford (Reino Unido)", "airport", "Propuesta, sin confirmar", "Proposed, not confirmed", SRC_EU),
    ("2026-11-06", "6 nov, 13:00–17:00", "6 Nov, 13:00–17:00", "Control aéreo de Italia (ENAV)", "Italian air traffic control (ENAV)",
     "Toda Italia", "atc", "Convocada", "Scheduled", SRC_EU),
    ("2026-11-11", "11 nov, 24 h", "11 Nov, 24 h", "Huelga general en España (CCOO y UGT)", "General strike in Spain (CCOO and UGT unions)",
     "Toda España: posible impacto en tierra y en el transporte al aeropuerto", "general", "Convocada; impacto en vuelos sin confirmar", "Called; impact on flights not yet confirmed", SRC_GEN),
    ("2026-11-21", "21 nov, 13:00–17:00", "21 Nov, 13:00–17:00", "Control aéreo de Italia (ENAV)", "Italian air traffic control (ENAV)",
     "Toda Italia", "atc", "Convocada", "Scheduled", SRC_EU),
    ("2026-11-22", "22 nov, 24 h", "22 Nov, 24 h", "Control aéreo (ENAV) en Malpensa y seguridad en Venecia", "ATC (ENAV) at Malpensa and security staff at Venice",
     "Milán-Malpensa, Venecia", "atc", "Convocada", "Scheduled", SRC_EU),
]

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


def _rows(l):
    out = []
    for s in sorted(STRIKES, key=lambda x: x[0]):
        _, wes, wen, des, den, where, kind, ses, sen, src = s
        when, what, st = (wes, des, ses) if l == "es" else (wen, den, sen)
        out.append(f"<tr><td>{e(when)}</td><td>{e(what)}<br><small>{e(where)}</small></td><td>{KIND[l][kind]}</td><td>{COMP[l][kind]}</td>"
                   f"<td>{e(st)} · <a href=\"{src}\" rel=\"noopener\">{'fuente' if l == 'es' else 'source'}</a></td></tr>")
    return "".join(out)


def build(ctx):
    paths = {"es": "/huelgas-vuelos-espana/", "en": "/en/flight-strikes-spain-europe/"}
    for l in ("es", "en"):
        other = "en" if l == "es" else "es"
        if l == "es":
            title = "Huelgas de vuelos en España 2026: calendario y qué te deben"
            desc = "Calendario actualizado de huelgas que afectan a vuelos en España y Europa (oct–nov 2026) y cuándo te toca compensación de 250–600 €."
            h1 = "Huelgas que afectan a vuelos en España: calendario y tus derechos"
            lead = (f"Actualizado el {UPDATED['es']}. Estas son las huelgas convocadas que pueden afectar a vuelos con salida o llegada en España y a los destinos europeos más habituales. "
                    "Si te cancelan el vuelo con menos de 14 días de aviso, lo que decide si cobras 250–600 € es <strong>quién hace la huelga</strong>.")
            th = "<th>Cuándo</th><th>Qué y dónde</th><th>Tipo</th><th>¿Compensación?</th><th>Estado</th>"
            rules = f"""<h2>¿Me pagan si cancelan mi vuelo por huelga?</h2>
<ul><li><strong>Huelga de la plantilla de la propia aerolínea</strong> (pilotos, tripulantes): normalmente <strong>sí</strong>. El Tribunal de Justicia de la UE dice que no es una circunstancia extraordinaria (asunto C-28/20).</li>
<li><strong>Huelga de control aéreo</strong>: normalmente <strong>no</strong>, porque la aerolínea no la controla.</li>
<li><strong>Huelga de aeropuerto, handling o huelga general</strong>: <strong>depende</strong> de si la aerolínea podía haber evitado la cancelación. Pídele la causa por escrito.</li>
<li><strong>Siempre</strong>, sea cual sea la huelga: reembolso completo en 7 días o vuelo alternativo, y comida, bebida y hotel mientras esperas.</li>
<li><strong>Si te avisan con 14 días o más</strong>, no hay compensación fija por la cancelación. Por ejemplo, para la huelga general del 11 de noviembre, una cancelación avisada antes del 28 de octubre no daría compensación.</li></ul>"""
            checker = """<h2>¿Me toca algo? Compruébalo</h2>
<form id="sk-form" class="sk"><label>Fecha del vuelo <input type="date" id="sk-flight" required></label>
<label>Fecha en que te avisaron de la cancelación <input type="date" id="sk-notice" required></label>
<label>¿Quién hacía huelga? <select id="sk-kind"><option value="airline">La plantilla de la aerolínea</option><option value="atc">Control aéreo</option><option value="airport">Aeropuerto o handling</option><option value="general">Huelga general</option></select></label>
<button class="btn btn-sign" type="submit">Comprobar</button></form><p id="sk-out" class="lead" aria-live="polite"></p>
<p>¿Retraso en vez de cancelación? <a href="/">Calcula el importe exacto de tu ruta aquí</a>.</p>"""
            src = f"<p><small>Fuentes: <a href=\"{SRC_MIN}\">Ministerio de Transportes, servicios mínimos</a> · <a href=\"{SRC_EU}\">calendario europeo de huelgas</a> · <a href=\"{SRC_GEN}\">huelga general del 11 de noviembre</a>. Las convocatorias pueden cambiar o desconvocarse; revisa con tu aerolínea.</small></p>"
            faq = [("¿Me devuelven el dinero si cancelan mi vuelo por huelga?", "Sí. Sea cual sea la huelga, puedes elegir el reembolso completo del billete en 7 días o un vuelo alternativo, y la aerolínea debe darte comida y hotel si tienes que esperar."),
                   ("¿Me pagan compensación si la huelga es de controladores?", "Normalmente no: las huelgas de control aéreo se consideran circunstancias extraordinarias. Sí tienes derecho al reembolso o a un vuelo alternativo y a asistencia."),
                   ("¿Y si la huelga es de los pilotos o tripulantes de la aerolínea?", "Entonces normalmente sí: el Tribunal de Justicia de la UE considera que la huelga de la propia plantilla no es extraordinaria, así que te tocan 250, 400 o 600 € si te avisan con menos de 14 días.")]
        else:
            title = "Flight strikes Spain & Europe 2026: dates and your rights"
            desc = "Up-to-date calendar of strikes affecting flights in Spain and Europe (Oct–Nov 2026) and when you're owed €250–€600 compensation."
            h1 = "Strikes affecting flights to and from Spain: calendar and your rights"
            lead = (f"Updated {UPDATED['en']}. These are the strikes called that may affect flights to and from Spain and the most common European connections. "
                    "If your flight is cancelled with less than 14 days' notice, what decides whether you get €250–€600 is <strong>who is on strike</strong>.")
            th = "<th>When</th><th>What and where</th><th>Type</th><th>Compensation?</th><th>Status</th>"
            rules = f"""<h2>Will I be compensated if my flight is cancelled by a strike?</h2>
<ul><li><strong>The airline's own staff on strike</strong> (pilots, cabin crew): usually <strong>yes</strong>. The EU Court of Justice ruled this is not an extraordinary circumstance (case C-28/20).</li>
<li><strong>Air traffic control strike</strong>: usually <strong>no</strong>, because the airline can't control it.</li>
<li><strong>Airport, ground handling or general strike</strong>: <strong>it depends</strong> on whether the airline could have avoided the cancellation. Ask it for the cause in writing.</li>
<li><strong>Always</strong>, whatever the strike: a full refund within 7 days or a new flight, plus meals, drinks and a hotel while you wait.</li>
<li><strong>Told 14 days or more in advance</strong>: no fixed compensation for the cancellation. For the 11 November general strike, a cancellation notified before 28 October would not carry compensation.</li></ul>"""
            checker = """<h2>Am I owed anything? Check it</h2>
<form id="sk-form" class="sk"><label>Flight date <input type="date" id="sk-flight" required></label>
<label>Date you were told about the cancellation <input type="date" id="sk-notice" required></label>
<label>Who was on strike? <select id="sk-kind"><option value="airline">The airline's own staff</option><option value="atc">Air traffic control</option><option value="airport">Airport or ground handling</option><option value="general">General strike</option></select></label>
<button class="btn btn-sign" type="submit">Check</button></form><p id="sk-out" class="lead" aria-live="polite"></p>
<p>Delayed rather than cancelled? <a href="/en/">Work out the exact amount for your route here</a>.</p>"""
            src = f"<p><small>Sources: <a href=\"{SRC_MIN}\">Spanish Ministry of Transport, minimum services</a> · <a href=\"{SRC_EU}\">European strike calendar</a> · <a href=\"{SRC_GEN}\">11 November general strike</a>. Strikes can change or be called off; check with your airline.</small></p>"
            faq = [("Do I get a refund if my flight is cancelled by a strike?", "Yes. Whatever the strike, you can choose a full refund within 7 days or a new flight, and the airline must provide meals and a hotel if you have to wait."),
                   ("Do I get compensation for an air traffic control strike?", "Usually not: ATC strikes count as extraordinary circumstances. You are still owed a refund or rerouting and care while you wait."),
                   ("What if the airline's pilots or cabin crew are on strike?", "Then usually yes: the EU Court of Justice treats an airline's own staff strike as not extraordinary, so you're owed €250, €400 or €600 if told less than 14 days before.")]
        faq_html = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faq)
        faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
        body = f"""<div class="wrap prose"><h1>{h1}</h1><p class="lead">{lead}</p>
<div class="board"><table><thead><tr>{th}</tr></thead><tbody>{_rows(l)}</tbody></table></div>
{checker}
{rules}
<h2>{'Preguntas frecuentes' if l == 'es' else 'Common questions'}</h2>{faq_html}
{src}</div>
<style>.sk{{display:grid;gap:12px;max-width:520px;margin:12px 0}}.sk label{{display:grid;gap:4px;font-weight:600}}.sk input,.sk select{{font:inherit;padding:10px;border:1px solid var(--line);border-radius:8px;background:transparent;color:inherit}}</style>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
<script>{CHECKER_JS}</script>"""
        ctx["emit"](l, paths[l], ctx["page"](l, title, desc, paths[l], body, paths, paths[other]))
    return list(paths.values())
