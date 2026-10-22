"""Evergreen guides (ES + EN): cancelled flight, denied boarding/overbooking, extraordinary circumstances.
Facts: Regulation (EC) 261/2004 arts 4, 5, 7, 8, 9, 10 and CJEU case law cited inline.
"""
import json
from html import escape as e

G = [
    {
        "paths": {"es": "/vuelo-cancelado-que-hacer/", "en": "/en/flight-cancelled-what-to-do/"},
        "es": {
            "title": "Vuelo cancelado: qué hacer, reembolso y compensación de 250 a 600 €",
            "desc": "Te han cancelado el vuelo: tus 3 derechos (reembolso o vuelo alternativo, asistencia y compensación de 250–600 €), la regla de los 14 días y cómo reclamar gratis.",
            "h1": "Vuelo cancelado: qué hacer y cuánto te deben",
            "lead": "Si te cancelan un vuelo que sale de la UE, o que llega a la UE con una aerolínea europea, el reglamento 261/2004 te da tres derechos a la vez. No tienes que elegir entre ellos.",
            "body": """<h2>1. Elige: reembolso o vuelo alternativo</h2>
<p>La aerolínea tiene que ofrecerte, a tu elección, el <strong>reembolso completo del billete en 7 días</strong> o un <strong>transporte alternativo</strong> lo antes posible (o en la fecha que prefieras). Si te han dado un vale o te han recolocado en un vuelo que no te sirve, puedes exigir el dinero.</p>
<h2>2. Asistencia mientras esperas</h2>
<p>Si esperas al vuelo alternativo: comida y bebida, dos llamadas o correos y, si hay que pasar la noche, <strong>hotel y traslado</strong>. Si no te lo dan, paga algo razonable, guarda los tickets y reclámalos después.</p>
<h2>3. Compensación de 250, 400 o 600 €</h2>
<p>Además del reembolso o el vuelo alternativo, te corresponde una cantidad fija por persona según la distancia: <strong>250 €</strong> hasta 1.500 km, <strong>400 €</strong> hasta 3.500 km y <strong>600 €</strong> a partir de ahí. Salvo que se dé alguno de estos casos:</p>
<ul><li>Te avisaron con <strong>14 días o más</strong> de antelación.</li>
<li>Te avisaron con 7 a 13 días y el vuelo alternativo salía como mucho 2 h antes y llegaba como mucho 4 h después del original.</li>
<li>Te avisaron con menos de 7 días y el alternativo salía como mucho 1 h antes y llegaba como mucho 2 h después.</li>
<li>La causa fue una <a href="/circunstancias-extraordinarias-vuelo/">circunstancia extraordinaria</a> (meteorología que impide volar, huelga de controladores…).</li></ul>
<p>Si el vuelo alternativo te deja en destino con poco retraso (2, 3 o 4 h según la distancia), la aerolínea puede rebajar la compensación a la mitad.</p>
<h2>Cómo reclamar paso a paso</h2>
<ol><li>Haz captura del aviso de cancelación y pide el motivo por escrito.</li>
<li><a href="/">Calcula cuánto te corresponde</a> con la distancia real de tu ruta.</li>
<li>Reclama en el formulario de compensación de la aerolínea (no el de reembolso: son distintos).</li>
<li>Si no contesta en un mes o lo rechaza, reclama gratis en <a href="https://www.seguridadaerea.gob.es/index.php/es/ambitos/derechos-de-los-pasajeros/inicia-tu-reclamacion-con-aesa" rel="noopener">AESA</a>.</li>
<li>Último paso: juicio verbal, sin abogado si la cantidad no pasa de 2.000 €. En España tienes 5 años para reclamar.</li></ol>
<p>Si hay huelgas a la vista, mira el <a href="/huelgas-vuelos-espana/">calendario de huelgas</a>: quién hace huelga decide si cobras.</p>""",
            "faq": [
                ("¿Me pueden dar un vale en vez de devolverme el dinero?", "Solo si tú lo aceptas por escrito. Por defecto tienes derecho al reembolso en dinero en 7 días."),
                ("¿Si acepto el reembolso pierdo la compensación?", "No. El reembolso y la compensación son derechos distintos y puedes reclamar los dos."),
                ("¿Cuánto me corresponde si me cancelan el vuelo el mismo día?", "Entre 250 y 600 € por persona según la distancia, salvo que la causa sea una circunstancia extraordinaria. Además del reembolso o vuelo alternativo."),
            ],
        },
        "en": {
            "title": "Flight cancelled? What to do, refunds and £220–£520 compensation",
            "desc": "Your flight was cancelled: your three rights (refund or new flight, food and hotel, £220–£520 / €250–€600 compensation), the 14-day rule and how to claim for free.",
            "h1": "Flight cancelled: what to do and what you're owed",
            "lead": "If a flight from the UK or EU is cancelled, or one into the UK/EU on a UK or EU airline, UK261 and EU261 give you three rights at the same time. You don't have to choose between them.",
            "body": """<h2>1. Choose: refund or new flight</h2>
<p>The airline must offer you, your choice, a <strong>full refund within 7 days</strong> or <strong>rerouting</strong> at the earliest opportunity (or on a later date that suits you). If you were given a voucher or rebooked onto a flight that doesn't work for you, you can insist on the money.</p>
<h2>2. Care while you wait</h2>
<p>While you wait for the new flight: meals and drinks, a way to communicate and, if you need to stay overnight, <strong>a hotel and transfers</strong>. If the airline doesn't arrange it, pay for something reasonable, keep the receipts and claim them back.</p>
<h2>3. Fixed compensation</h2>
<p>On top of the refund or rerouting, you're owed a fixed amount per passenger depending on distance: <strong>£220 / €250</strong> up to 1,500 km, <strong>£350 / €400</strong> up to 3,500 km, <strong>£520 / €600</strong> beyond. Unless:</p>
<ul><li>You were told <strong>14 days or more</strong> before departure.</li>
<li>You were told 7–13 days before and the new flight left no more than 2 hours earlier and arrived no more than 4 hours later.</li>
<li>You were told under 7 days before and the new flight left no more than 1 hour earlier and arrived no more than 2 hours later.</li>
<li>The cause was an <a href="/en/extraordinary-circumstances-flight-delay/">extraordinary circumstance</a> (weather that makes flying unsafe, an air traffic control strike…).</li></ul>
<p>If the new flight gets you there only slightly late (2, 3 or 4 hours depending on distance), the airline can halve the compensation.</p>
<h2>How to claim</h2>
<ol><li>Screenshot the cancellation notice and ask for the reason in writing.</li>
<li><a href="/en/">Work out what you're owed</a> using your route's real distance.</li>
<li>Claim on the airline's compensation form (not the refund form: they're different).</li>
<li>A refusal, or no answer within 8 weeks (UK flights) or one month (flights from Spain): escalate for free to the airline's ADR scheme or the <a href="https://www.caa.co.uk/passengers-and-public/resolving-travel-problems/" rel="noopener">CAA</a> for flights from the UK, or AESA for flights from Spain.</li>
<li>Last resort: small claims court, no lawyer needed. You have 6 years in England and Wales (5 in Scotland).</li></ol>
<p>Strikes coming up? Check the <a href="/en/flight-strikes-spain-europe/">strike calendar</a>: who is striking decides whether you get paid.</p>""",
            "faq": [
                ("Can the airline give me a voucher instead of a refund?", "Only if you agree to it. By default you're entitled to your money back within 7 days."),
                ("If I take the refund, do I lose the compensation?", "No. The refund and the compensation are separate rights and you can claim both."),
                ("How much do I get if my flight is cancelled on the day?", "£220–£520 or €250–€600 per passenger depending on distance, unless the cause was extraordinary. That's on top of the refund or new flight."),
            ],
        },
    },
    {
        "paths": {"es": "/overbooking-compensacion/", "en": "/en/denied-boarding-overbooking-compensation/"},
        "es": {
            "title": "Overbooking: compensación de 250 a 600 € si no te dejan embarcar",
            "desc": "Si no te dejan embarcar por overbooking te deben 250, 400 o 600 € en el acto, más reembolso o vuelo alternativo. Qué hacer en el mostrador y si te conviene ser voluntario.",
            "h1": "Overbooking: qué te deben si no te dejan embarcar",
            "lead": "Si la aerolínea vende más plazas de las que tiene y te quedas en tierra contra tu voluntad, la compensación es automática: no hay excusas de circunstancias extraordinarias que valgan.",
            "body": """<h2>Lo que te corresponde</h2>
<ul><li><strong>Compensación inmediata</strong>: 250 € hasta 1.500 km, 400 € hasta 3.500 km, 600 € a partir de ahí, por persona.</li>
<li><strong>Reembolso o vuelo alternativo</strong>, a tu elección.</li>
<li><strong>Asistencia</strong>: comida, bebida y hotel si tienes que esperar al día siguiente.</li></ul>
<p>El reglamento dice que la compensación se paga "inmediatamente". Pídela en el mostrador y, si no te la dan, reclámala después con la tarjeta de embarque y una nota por escrito de la denegación.</p>
<h2>Requisitos</h2>
<ul><li>Tener reserva confirmada.</li>
<li>Presentarte a facturación a la hora indicada o, si no la había, 45 minutos antes de la salida.</li>
<li>Que no te nieguen el embarque por motivos justificados (documentación, seguridad, comportamiento).</li></ul>
<h2>¿Ser voluntario o no?</h2>
<p>Antes de denegar el embarque, la aerolínea tiene que pedir voluntarios. Si te ofreces, cobras lo que negocies (dinero, vale, puntos) más reembolso o vuelo alternativo, <strong>pero no la compensación fija</strong>. Solo merece la pena si lo que te ofrecen supera lo que te tocaría si te dejaran en tierra, y mejor en dinero que en vale.</p>
<h2>Si te bajan de clase</h2>
<p>Si te sientan en una clase inferior a la que pagaste, te deben devolver el 30, 50 o 75% del precio de ese trayecto según la distancia.</p>
<p><a href="/">Calcula cuánto te corresponde por tu ruta</a> o compara <a href="/comparativa-empresas-reclamacion-vuelos/">reclamar tú o con una empresa</a>.</p>""",
            "faq": [
                ("¿Me pueden negar la compensación por overbooking alegando causas extraordinarias?", "No. La denegación de embarque por overbooking es responsabilidad de la aerolínea y la compensación es automática."),
                ("¿Qué pasa si acepto ser voluntario?", "Recibes lo que acuerdes con la aerolínea más reembolso o vuelo alternativo, pero renuncias a la compensación fija de 250–600 €."),
                ("¿Cuánto tiempo tengo para reclamar el overbooking?", "En España, 5 años. Pero cuanto antes reclames, mejor."),
            ],
        },
        "en": {
            "title": "Denied boarding & overbooking compensation: £220–£520 on the spot",
            "desc": "Bumped off an overbooked flight? You're owed £220–£520 / €250–€600 straight away, plus a refund or new flight. What to do at the gate and whether to volunteer.",
            "h1": "Overbooked flight: what you're owed if you're denied boarding",
            "lead": "If the airline sold more seats than it has and you're left behind against your will, compensation is automatic: extraordinary circumstances don't apply.",
            "body": """<h2>What you're owed</h2>
<ul><li><strong>Compensation on the spot</strong>: £220 / €250 up to 1,500 km, £350 / €400 up to 3,500 km, £520 / €600 beyond, per passenger.</li>
<li><strong>A refund or a new flight</strong>, your choice.</li>
<li><strong>Care</strong>: food, drinks and a hotel if you have to wait until the next day.</li></ul>
<p>The rules say compensation must be paid "immediately". Ask for it at the desk and, if they won't, claim afterwards with your boarding pass and written confirmation that you were denied boarding.</p>
<h2>Conditions</h2>
<ul><li>A confirmed booking.</li>
<li>Checking in on time, or at least 45 minutes before departure if no time was given.</li>
<li>Not being refused for valid reasons (documents, safety, behaviour).</li></ul>
<h2>Should you volunteer?</h2>
<p>Before bumping anyone, the airline must ask for volunteers. If you volunteer you get whatever you agree (cash, vouchers, points) plus a refund or new flight, <strong>but not the fixed compensation</strong>. Only worth it if the offer beats what you'd get if bumped, and cash is better than a voucher.</p>
<h2>Downgraded?</h2>
<p>If you're seated in a lower class than you paid for, you're owed 30%, 50% or 75% of that flight's price back depending on distance.</p>
<p><a href="/en/">Work out what you're owed for your route</a> or compare <a href="/en/flight-compensation-companies-compared/">claiming yourself vs a claims company</a>.</p>""",
            "faq": [
                ("Can the airline refuse overbooking compensation citing extraordinary circumstances?", "No. Denied boarding due to overbooking is the airline's responsibility and compensation is automatic."),
                ("What happens if I volunteer?", "You get what you agree with the airline plus a refund or new flight, but you give up the fixed £220–£520 / €250–€600."),
                ("How long do I have to claim?", "Up to 6 years in England and Wales (5 in Scotland) and 5 years in Spain, but the sooner the better."),
            ],
        },
    },
    {
        "paths": {"es": "/circunstancias-extraordinarias-vuelo/", "en": "/en/extraordinary-circumstances-flight-delay/"},
        "es": {
            "title": "Circunstancias extraordinarias: cuándo la aerolínea no tiene que pagar",
            "desc": "Avería, huelga, tiempo, pájaros, tripulación enferma: qué cuenta como circunstancia extraordinaria según el Tribunal de Justicia de la UE y qué no, con las sentencias.",
            "h1": "Circunstancias extraordinarias: qué vale y qué no como excusa",
            "lead": "Es la excusa que más usan las aerolíneas para no pagar. Pero el Tribunal de Justicia de la UE la ha acotado mucho: tiene que ser algo ajeno a su actividad normal y que no pudiera evitar tomando todas las medidas razonables.",
            "body": """<h2>No son extraordinarias (te tienen que pagar)</h2>
<ul><li><strong>Averías técnicas</strong> detectadas en el mantenimiento o en la revisión antes de volar (sentencia C-549/07, Wallentin-Hermann).</li>
<li><strong>Huelga del propio personal</strong> de la aerolínea, pilotos o tripulantes (C-28/20, Airhelp contra SAS).</li>
<li><strong>Falta de tripulación o enfermedad repentina</strong> de un tripulante (C-156/22 a C-158/22, TAP).</li>
<li>Problemas de organización, retrasos en cadena por mala planificación o falta de aviones.</li></ul>
<h2>Sí suelen serlo (no hay compensación)</h2>
<ul><li>Meteorología que impide volar con seguridad.</li>
<li>Huelga de controladores aéreos. Las restricciones del control aéreo, solo si la aerolínea identifica su causa de fondo y demuestra que era extraordinaria (TJUE, C-108/26, 2026).</li>
<li>Choque con un pájaro (C-315/15, Pešková).</li>
<li>Un defecto de fabricación oculto que el fabricante o las autoridades revelan (C-257/14, van der Lans).</li>
<li>Un pasajero conflictivo que obliga a desviar el avión, o cierre del aeropuerto.</li></ul>
<h2>Ojo con los retrasos "en cadena"</h2>
<p>Si tu avión venía tarde de un vuelo anterior, la aerolínea solo puede usar esa causa si de verdad fue extraordinaria y si está directamente relacionada con tu retraso (C-74/19). Si te dicen "efecto dominó", pide el motivo concreto por escrito.</p>
<h2>Aunque sea extraordinaria, sigues teniendo derechos</h2>
<p>Reembolso o vuelo alternativo, comida, bebida y hotel mientras esperas. Lo único que se pierde es la compensación fija.</p>
<h2>Qué hacer si te lo alegan</h2>
<ol><li>Pide la causa exacta por escrito.</li>
<li>Comprueba si otros vuelos salieron a la misma hora del mismo aeropuerto: si el tiempo era el problema, no salió nadie.</li>
<li>Si no te convence, reclama igualmente: la aerolínea tiene que demostrarlo, no tú. <a href="/">Calcula cuánto te corresponde</a>.</li></ol>""",
            "faq": [
                ("¿Una avería técnica es circunstancia extraordinaria?", "Normalmente no. El Tribunal de Justicia de la UE dice que las averías forman parte de la actividad normal de la aerolínea, salvo defectos de fabricación ocultos revelados por el fabricante."),
                ("¿La huelga de pilotos o tripulantes es circunstancia extraordinaria?", "No, si es personal de la propia aerolínea (sentencia C-28/20). Sí lo suele ser la huelga de controladores aéreos."),
                ("¿Quién tiene que demostrar la circunstancia extraordinaria?", "La aerolínea. Tiene que probar la causa y que tomó todas las medidas razonables para evitar el retraso o la cancelación."),
            ],
        },
        "en": {
            "title": "Extraordinary circumstances: when airlines don't have to pay",
            "desc": "Technical fault, strike, weather, bird strike, sick crew: what counts as an extraordinary circumstance under EU261/UK261 according to the courts, and what doesn't.",
            "h1": "Extraordinary circumstances: which airline excuses hold up",
            "lead": "It's the excuse airlines use most to avoid paying. But the EU Court of Justice has narrowed it a lot: it has to be outside the airline's normal activity and something it couldn't avoid even with all reasonable measures. UK courts follow the same case law.",
            "body": """<h2>Not extraordinary (they have to pay)</h2>
<ul><li><strong>Technical faults</strong> found during maintenance or pre-flight checks (case C-549/07, Wallentin-Hermann; followed in the UK in Jet2 v Huzar).</li>
<li><strong>The airline's own staff on strike</strong>, pilots or cabin crew (C-28/20, Airhelp v SAS).</li>
<li><strong>Crew shortages or a crew member falling ill</strong> suddenly (C-156/22 to C-158/22, TAP).</li>
<li>Poor planning, knock-on delays from the airline's own scheduling, or a lack of aircraft.</li></ul>
<h2>Usually extraordinary (no compensation)</h2>
<ul><li>Weather that makes flying unsafe.</li>
<li>Air traffic control strikes. ATC restrictions or system failures (like a NATS outage) only when the airline identifies the underlying cause and proves it was extraordinary (CJEU, C-108/26, 2026).</li>
<li>A bird strike (C-315/15, Pešková).</li>
<li>A hidden manufacturing defect revealed by the manufacturer or authorities (C-257/14, van der Lans).</li>
<li>A disruptive passenger forcing a diversion, or the airport closing.</li></ul>
<h2>Watch out for "knock-on" delays</h2>
<p>If your plane was late from an earlier flight, the airline can only rely on that if the earlier problem really was extraordinary and directly caused your delay (C-74/19). If they say "knock-on effect", ask for the exact reason in writing.</p>
<h2>Even if it is extraordinary, you keep your other rights</h2>
<p>A refund or new flight, plus food, drinks and a hotel while you wait. Only the fixed compensation is lost.</p>
<h2>What to do if the airline uses it</h2>
<ol><li>Ask for the exact cause in writing.</li>
<li>Check whether other flights left the same airport at the same time: if the weather was the problem, nobody left.</li>
<li>If you're not convinced, claim anyway: the airline has to prove it, not you. <a href="/en/">Work out what you're owed</a>.</li></ol>""",
            "faq": [
                ("Is a technical fault an extraordinary circumstance?", "Usually not. Courts treat technical problems as part of an airline's normal operations, except hidden manufacturing defects revealed by the manufacturer."),
                ("Is a pilot or cabin crew strike extraordinary?", "Not if it's the airline's own staff (case C-28/20). Air traffic control strikes usually are."),
                ("Who has to prove the extraordinary circumstance?", "The airline. It has to prove the cause and that it took all reasonable measures to avoid the delay or cancellation."),
            ],
        },
    },
]


def build(ctx):
    urls = []
    for g in G:
        P = g["paths"]
        for l, other in (("es", "en"), ("en", "es")):
            t = g[l]
            faq_html = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in t["faq"])
            ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]}
            home = "/" if l == "es" else "/en/"
            cta = "Calcular mi compensación" if l == "es" else "Work out my compensation"
            body = f"""<div class="wrap prose"><h1>{t['h1']}</h1><p class="lead">{t['lead']}</p>
<p><a class="btn btn-sign" href="{home}">{cta}</a></p>
{t['body']}
<h2>{'Preguntas frecuentes' if l == 'es' else 'Common questions'}</h2>{faq_html}</div>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>"""
            ctx["emit"](l, P[l], ctx["page"](l, t["title"], t["desc"], P[l], body, P, P[other]))
            urls.append(P[l])
    return urls
