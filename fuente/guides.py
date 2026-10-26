"""Evergreen guides (ES + EN): cancelled flight, denied boarding/overbooking, extraordinary circumstances.
Facts: Regulation (EC) 261/2004 arts 4, 5, 7, 8, 9, 10 and CJEU case law cited inline.
"""
import json
from html import escape as e

G = [
    {
        "paths": {"es": "/vuelo-cancelado-que-hacer/", "en": "/en/flight-cancelled-what-to-do/"},
        "es": {
            "title": "Vuelo cancelado: qué hacer, reembolso y compensación",
            "desc": "Te han cancelado el vuelo: reembolso o vuelo alternativo, asistencia y compensación de 250–600 €, la regla de los 14 días, plazos y cómo reclamar gratis.",
            "h1": "Vuelo cancelado: qué hacer y cuánto te deben",
            "lead": "Si te cancelan un vuelo que sale de la UE, o que llega a la UE con una aerolínea europea, el reglamento 261/2004 te da tres derechos a la vez. No tienes que elegir entre ellos.",
            "body": """<h2>1. Elige: reembolso o vuelo alternativo</h2>
<p>La aerolínea tiene que ofrecerte, a tu elección, el <strong>reembolso completo del billete en 7 días</strong> o un <strong>transporte alternativo</strong> lo antes posible (o en la fecha que prefieras). Si te han dado un vale o te han recolocado en un vuelo que no te sirve, puedes exigir el dinero.</p>
<h2>2. Asistencia mientras esperas</h2>
<p>Si esperas al vuelo alternativo: comida y bebida, dos llamadas o correos y, si hay que pasar la noche, <strong>hotel y traslado</strong>. Si no te lo dan, paga algo razonable, guarda los tickets y reclámalos después.</p>
<h2>3. Compensación de 250, 400 o 600 €</h2>
<p>Además del reembolso o el vuelo alternativo, te corresponde una cantidad fija por persona según la distancia: <strong>250 €</strong> hasta 1.500 km, <strong>400 €</strong> hasta 3.500 km (o más, si el vuelo es dentro de la UE) y <strong>600 €</strong> a partir de ahí. Salvo que se dé alguno de estos casos:</p>
<ul><li>Te avisaron con <strong>14 días o más</strong> de antelación.</li>
<li>Te avisaron con 7 a 13 días y el vuelo alternativo salía como mucho 2 h antes y llegaba menos de 4 h después del original.</li>
<li>Te avisaron con menos de 7 días y el alternativo salía como mucho 1 h antes y llegaba menos de 2 h después.</li>
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
            "title": "Flight cancelled? Refunds and £220–£520 compensation",
            "desc": "Flight cancelled? Your rights to a refund or new flight, food and hotel, £220–£520 / €250–€600 compensation, the 14-day rule and how to claim for free.",
            "h1": "Flight cancelled: what to do and what you're owed",
            "lead": "If a flight from the UK or EU is cancelled, or one into the UK/EU on a UK or EU airline, UK261 and EU261 give you three rights at the same time. You don't have to choose between them.",
            "body": """<h2>1. Choose: refund or new flight</h2>
<p>The airline must offer you, your choice, a <strong>full refund within 7 days</strong> or <strong>rerouting</strong> at the earliest opportunity (or on a later date that suits you). If you were given a voucher or rebooked onto a flight that doesn't work for you, you can insist on the money.</p>
<h2>2. Care while you wait</h2>
<p>While you wait for the new flight: meals and drinks, a way to communicate and, if you need to stay overnight, <strong>a hotel and transfers</strong>. If the airline doesn't arrange it, pay for something reasonable, keep the receipts and claim them back.</p>
<h2>3. Fixed compensation</h2>
<p>On top of the refund or rerouting, you're owed a fixed amount per passenger depending on distance: <strong>£220 / €250</strong> up to 1,500 km, <strong>£350 / €400</strong> up to 3,500 km (and any longer flight within the EU), <strong>£520 / €600</strong> beyond. Unless:</p>
<ul><li>You were told <strong>14 days or more</strong> before departure.</li>
<li>You were told 7–13 days before and the new flight left no more than 2 hours earlier and arrived less than 4 hours later.</li>
<li>You were told under 7 days before and the new flight left no more than 1 hour earlier and arrived less than 2 hours later.</li>
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
            "title": "Overbooking: compensación si no te dejan embarcar",
            "desc": "Si no te dejan embarcar por overbooking te corresponden 250, 400 o 600 €, más reembolso o vuelo alternativo. Qué hacer en el mostrador y si conviene ser voluntario.",
            "h1": "Overbooking: qué te deben si no te dejan embarcar",
            "lead": "Si la aerolínea vende más plazas de las que tiene y te quedas en tierra contra tu voluntad, te corresponde compensación y la aerolínea no puede alegar circunstancias extraordinarias (Tribunal de Justicia de la UE, asunto C-22/11).",
            "body": """<h2>Lo que te corresponde</h2>
<ul><li><strong>Compensación inmediata</strong>: 250 € hasta 1.500 km, 400 € hasta 3.500 km (o más dentro de la UE), 600 € a partir de ahí, por persona.</li>
<li><strong>Reembolso o vuelo alternativo</strong>, a tu elección.</li>
<li><strong>Asistencia</strong>: comida, bebida y hotel si tienes que esperar al día siguiente.</li></ul>
<p>El reglamento dice que la compensación se paga "inmediatamente". Pídela en el mostrador y, si no te la dan, reclámala después con la tarjeta de embarque y una nota por escrito de la denegación.</p>
<h2>Requisitos</h2>
<ul><li>Tener reserva confirmada.</li>
<li>Presentarte a facturación a la hora indicada o, si no la había, 45 minutos antes de la salida.</li>
<li>Que no te nieguen el embarque por motivos justificados (salud, seguridad o documentación de viaje inadecuada, según el art. 2.j del reglamento).</li></ul>
<h2>¿Ser voluntario o no?</h2>
<p>Antes de denegar el embarque, la aerolínea tiene que pedir voluntarios. Si te ofreces, cobras lo que negocies (dinero, vale, puntos) más reembolso o vuelo alternativo, <strong>pero no la compensación fija</strong>. Solo merece la pena si lo que te ofrecen supera lo que te tocaría si te dejaran en tierra, y mejor en dinero que en vale.</p>
<h2>Si te bajan de clase</h2>
<p>Si te sientan en una clase inferior a la que pagaste, te deben devolver el 30, 50 o 75% del precio de ese trayecto según la distancia.</p>
<p><a href="/">Calcula cuánto te corresponde por tu ruta</a> o compara <a href="/comparativa-empresas-reclamacion-vuelos/">reclamar tú o con una empresa</a>.</p>""",
            "faq": [
                ("¿Me pueden negar la compensación por overbooking alegando causas extraordinarias?", "No. El Tribunal de Justicia de la UE (asunto C-22/11) dice que la denegación de embarque no puede justificarse con circunstancias extraordinarias. Solo la eximen motivos razonables como salud, seguridad o documentación de viaje inadecuada."),
                ("¿Qué pasa si acepto ser voluntario?", "Recibes lo que acuerdes con la aerolínea más reembolso o vuelo alternativo, pero renuncias a la compensación fija de 250–600 €."),
                ("¿Cuánto tiempo tengo para reclamar el overbooking?", "En España, 5 años. Pero cuanto antes reclames, mejor."),
            ],
        },
        "en": {
            "title": "Denied boarding and overbooking compensation",
            "desc": "Bumped off an overbooked flight? You're owed £220–£520 / €250–€600 straight away, plus a refund or new flight. What to do at the gate and whether to volunteer.",
            "h1": "Overbooked flight: what you're owed if you're denied boarding",
            "lead": "If the airline sold more seats than it has and you're left behind against your will, you're owed compensation and the airline can't rely on extraordinary circumstances (CJEU, Case C-22/11).",
            "body": """<h2>What you're owed</h2>
<ul><li><strong>Compensation on the spot</strong>: £220 / €250 up to 1,500 km, £350 / €400 up to 3,500 km (or longer within the EU), £520 / €600 beyond, per passenger.</li>
<li><strong>A refund or a new flight</strong>, your choice.</li>
<li><strong>Care</strong>: food, drinks and a hotel if you have to wait until the next day.</li></ul>
<p>The rules say compensation must be paid "immediately". Ask for it at the desk and, if they won't, claim afterwards with your boarding pass and written confirmation that you were denied boarding.</p>
<h2>Conditions</h2>
<ul><li>A confirmed booking.</li>
<li>Checking in on time, or at least 45 minutes before departure if no time was given.</li>
<li>Not being refused for valid reasons (health, safety, security or inadequate travel documents, Article 2(j)).</li></ul>
<h2>Should you volunteer?</h2>
<p>Before bumping anyone, the airline must ask for volunteers. If you volunteer you get whatever you agree (cash, vouchers, points) plus a refund or new flight, <strong>but not the fixed compensation</strong>. Only worth it if the offer beats what you'd get if bumped, and cash is better than a voucher.</p>
<h2>Downgraded?</h2>
<p>If you're seated in a lower class than you paid for, you're owed 30%, 50% or 75% of that flight's price back depending on distance.</p>
<p><a href="/en/">Work out what you're owed for your route</a> or compare <a href="/en/flight-compensation-companies-compared/">claiming yourself vs a claims company</a>.</p>""",
            "faq": [
                ("Can the airline refuse overbooking compensation citing extraordinary circumstances?", "No. The Court of Justice of the EU (Case C-22/11) held that denied boarding cannot be justified by extraordinary circumstances. Only reasonable grounds such as health, safety, security or inadequate travel documents exempt the airline."),
                ("What happens if I volunteer?", "You get what you agree with the airline plus a refund or new flight, but you give up the fixed £220–£520 / €250–€600."),
                ("How long do I have to claim?", "Up to 6 years in England and Wales (5 in Scotland) and 5 years in Spain, but the sooner the better."),
            ],
        },
    },
    {
        "paths": {"es": "/circunstancias-extraordinarias-vuelo/", "en": "/en/extraordinary-circumstances-flight-delay/"},
        "es": {
            "title": "Circunstancias extraordinarias: cuándo no se paga",
            "desc": "Avería, huelga, tiempo, aves, tripulación enferma: qué cuenta como circunstancia extraordinaria según el Tribunal de Justicia de la UE, con las sentencias.",
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
<li>Comprueba si otros vuelos salieron a la misma hora del mismo aeropuerto: si salieron con normalidad, es un indicio que puedes alegar; la aerolínea tiene que probar la causa.</li>
<li>Si no te convence, reclama igualmente: la aerolínea tiene que demostrarlo, no tú. <a href="/">Calcula cuánto te corresponde</a>.</li></ol>""",
            "faq": [
                ("¿Una avería técnica es circunstancia extraordinaria?", "Normalmente no. El Tribunal de Justicia de la UE dice que las averías forman parte de la actividad normal de la aerolínea, salvo defectos de fabricación ocultos revelados por el fabricante."),
                ("¿La huelga de pilotos o tripulantes es circunstancia extraordinaria?", "No, si es personal de la propia aerolínea (sentencia C-28/20). Sí lo suele ser la huelga de controladores aéreos."),
                ("¿Quién tiene que demostrar la circunstancia extraordinaria?", "La aerolínea. Tiene que probar la causa y que tomó todas las medidas razonables para evitar el retraso o la cancelación."),
            ],
        },
        "en": {
            "title": "Extraordinary circumstances: when airlines don't pay",
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
<li>Check whether other flights left the same airport at the same time: if they left normally, that is evidence you can use; the airline has to prove its case.</li>
<li>If you're not convinced, claim anyway: the airline has to prove it, not you. <a href="/en/">Work out what you're owed</a>.</li></ol>""",
            "faq": [
                ("Is a technical fault an extraordinary circumstance?", "Usually not. Courts treat technical problems as part of an airline's normal operations, except hidden manufacturing defects revealed by the manufacturer."),
                ("Is a pilot or cabin crew strike extraordinary?", "Not if it's the airline's own staff (case C-28/20). Air traffic control strikes usually are."),
                ("Who has to prove the extraordinary circumstance?", "The airline. It has to prove the cause and that it took all reasonable measures to avoid the delay or cancellation."),
            ],
        },
    },
    {
        "paths": {"es": "/huelga-general-11-noviembre-vuelos/", "en": "/en/spain-general-strike-11-november-flights/"},
        "es": {
            "title": "Huelga general 11 de noviembre: qué pasa con tu vuelo",
            "desc": "Huelga general del 11 de noviembre de 2026 en España: si te cancelan o retrasan el vuelo, reembolso, asistencia y cuándo hay compensación de 250–600 €.",
            "h1": "Huelga general del 11 de noviembre: qué pasa con tu vuelo",
            "lead": "CCOO y UGT han convocado una huelga general de 24 horas en toda España el miércoles 11 de noviembre de 2026. Si vuelas ese día, esto es lo que te corresponde si tu vuelo se cancela o se retrasa.",
            "body": """<h2>Lo que se sabe (actualizado el 26 de octubre)</h2>
<ul><li><strong>Fecha:</strong> miércoles 11 de noviembre de 2026, 24 horas, en toda España.</li>
<li><strong>Convocan:</strong> CCOO y UGT, con el apoyo de otros sindicatos.</li>
<li><strong>Servicios mínimos en aeropuertos:</strong> aún sin publicar. Los fija el Ministerio de Transportes, normalmente pocos días antes. Como referencia, en la huelga general de 2012 se garantizó el 10 % de los vuelos peninsulares, el 50 % de los enlaces con Baleares y Canarias, el 20 % de los vuelos a la UE y el 40 % del resto de internacionales. Los de 2026 pueden ser distintos.</li></ul>
<p>Sigue el <a href="/huelgas-vuelos-espana/">calendario de huelgas</a>: lo actualizamos con fuentes oficiales.</p>
<h2>Si te cancelan el vuelo: siempre tienes estos derechos</h2>
<ul><li><strong>Reembolso en 7 días o vuelo alternativo</strong>, a tu elección (art. 8 del Reglamento 261/2004).</li>
<li><strong>Asistencia mientras esperas:</strong> comida, bebida y, si hay que pasar la noche, hotel y traslado (art. 9). Si no te lo dan, guarda los tickets y reclámalos.</li></ul>
<p>Estos dos derechos no dependen de quién haga huelga.</p>
<h2>La compensación de 250–600 €: depende</h2>
<ul><li><strong>Si te avisan de la cancelación con 14 días o más</strong> (para el 11 de noviembre, el 28 de octubre o antes): no hay compensación fija.</li>
<li><strong>Si la huelga es del personal de la propia aerolínea</strong> (tripulación, pilotos, su personal de tierra): el TJUE considera que no es una circunstancia extraordinaria (asunto C-28/20, Airhelp contra SAS). Si te avisan con menos de 14 días, normalmente te corresponde la compensación.</li>
<li><strong>Si la huelga es de controladores, del aeropuerto o de empresas ajenas a la aerolínea:</strong> suele considerarse circunstancia extraordinaria y normalmente no hay compensación.</li>
<li><strong>Huelga general:</strong> no hay una sentencia del TJUE específica. Lo que cuenta es qué personal paró y por qué se canceló tu vuelo. Por eso es clave pedir el motivo por escrito.</li></ul>
<h2>Qué hacer si vuelas el 11 de noviembre</h2>
<ol><li>Revisa la app o el correo de tu aerolínea los días previos.</li>
<li>Si te cancelan, haz captura del aviso, anota la fecha en que te avisaron y pide el motivo por escrito.</li>
<li>Elige reembolso o vuelo alternativo y guarda todos los tickets de gastos.</li>
<li><a href="/">Comprueba gratis si te corresponde compensación</a> y genera la carta para reclamar tú mismo.</li>
<li>Si la aerolínea no responde en un mes o lo rechaza, reclama gratis en <a href="https://www.seguridadaerea.gob.es/index.php/es/ambitos/derechos-de-los-pasajeros/inicia-tu-reclamacion-con-aesa" rel="noopener">AESA</a>.</li></ol>
<p>Más detalle: <a href="/vuelo-cancelado-que-hacer/">vuelo cancelado, qué hacer</a> y <a href="/circunstancias-extraordinarias-vuelo/">circunstancias extraordinarias</a>.</p>""",
            "faq": [
                ("¿Hay vuelos el 11 de noviembre de 2026?", "Sí, la huelga no cierra los aeropuertos, pero puede haber cancelaciones y retrasos. Los servicios mínimos aún no se han publicado."),
                ("¿Me compensan si me cancelan el vuelo por la huelga general?", "Depende de cuándo te avisaron y de qué personal hizo huelga. Con aviso de 14 días o más, no. Si fue el personal de la propia aerolínea y te avisaron con menos, normalmente sí. El reembolso o vuelo alternativo y la asistencia te corresponden siempre."),
                ("¿Qué día es el límite de los 14 días para el 11 de noviembre?", "El 28 de octubre. Una cancelación comunicada ese día o antes no da derecho a compensación fija."),
            ],
        },
        "en": {
            "title": "Spain general strike 11 November: what it means for flights",
            "desc": "Spain's 24-hour general strike on 11 November 2026: refunds, meals and hotels, and when €250–600 / £220–520 compensation applies if your flight is cancelled.",
            "h1": "Spain general strike on 11 November: what it means for your flight",
            "lead": "Spain's two main unions, CCOO and UGT, have called a 24-hour nationwide general strike for Wednesday 11 November 2026. If you're flying that day, here's what you're entitled to if your flight is cancelled or delayed.",
            "body": """<h2>What we know (updated 26 October)</h2>
<ul><li><strong>Date:</strong> Wednesday 11 November 2026, 24 hours, across Spain.</li>
<li><strong>Called by:</strong> CCOO and UGT, backed by other unions.</li>
<li><strong>Airport minimum services:</strong> not published yet. Spain's Ministry of Transport sets them, usually a few days before. For reference, the 2012 general strike guaranteed 10% of mainland domestic flights, 50% of flights to and between the Balearic and Canary Islands, 20% of flights to the EU and 40% of other international flights. This year's may differ.</li></ul>
<p>Keep an eye on our <a href="/en/flight-strikes-spain-europe/">strike calendar</a>, updated from official sources.</p>
<h2>If your flight is cancelled: you always get this</h2>
<ul><li><strong>A refund within 7 days or a new flight</strong>, your choice (Art. 8 of EU261; the same applies under UK261).</li>
<li><strong>Care while you wait:</strong> meals, drinks and, if you're stuck overnight, a hotel and transfers (Art. 9). If the airline doesn't provide it, keep your receipts and claim them back.</li></ul>
<p>These two rights don't depend on who is on strike.</p>
<h2>€250–600 / £220–520 compensation: it depends</h2>
<ul><li><strong>Cancellation notified 14 days or more in advance</strong> (for 11 November, on or before 28 October): no fixed compensation.</li>
<li><strong>The airline's own staff on strike</strong> (cabin crew, pilots, its ground staff): the EU Court of Justice says this is not an extraordinary circumstance (case C-28/20, Airhelp v SAS). With less than 14 days' notice, compensation usually applies.</li>
<li><strong>Air traffic control, airport or other outside staff on strike:</strong> usually treated as extraordinary, so usually no compensation.</li>
<li><strong>General strike:</strong> there's no specific EU Court ruling. What matters is which staff stopped work and why your flight was cancelled, so ask the airline for the reason in writing.</li></ul>
<h2>What to do if you're flying on 11 November</h2>
<ol><li>Check your airline's app or emails in the days before.</li>
<li>If your flight is cancelled, screenshot the notice, note the date you were told and ask for the reason in writing.</li>
<li>Choose a refund or a new flight and keep every receipt.</li>
<li><a href="/en/">Check for free whether compensation applies</a> and generate a claim letter to send yourself.</li>
<li>If the airline refuses or doesn't reply, escalate for free: AESA for flights from Spain, or the airline's ADR scheme or the <a href="https://www.caa.co.uk/passengers-and-public/resolving-travel-problems/" rel="noopener">CAA</a> for UK flights.</li></ol>
<p>More detail: <a href="/en/flight-cancelled-what-to-do/">flight cancelled, what to do</a> and <a href="/en/extraordinary-circumstances-flight-delay/">extraordinary circumstances</a>.</p>""",
            "faq": [
                ("Will there be flights on 11 November 2026?", "Yes, the strike doesn't close airports, but cancellations and delays are possible. Minimum services haven't been published yet."),
                ("Do I get compensation if my flight is cancelled because of the general strike?", "It depends on when you were told and which staff went on strike. With 14 days' notice or more, no. If it was the airline's own staff and you were told with less notice, usually yes. A refund or new flight and care while you wait always apply."),
                ("What is the 14-day cut-off date for 11 November flights?", "28 October. A cancellation notified on or before that day carries no fixed compensation."),
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
