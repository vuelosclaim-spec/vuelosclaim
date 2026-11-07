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
<p>Antes de denegar el embarque, la aerolínea tiene que pedir voluntarios. Si te ofreces, cobras lo que negocies (dinero, vale, puntos) más reembolso o vuelo alternativo, <strong>pero no la compensación fija</strong>. Solo merece la pena si lo que te ofrecen supera lo que te correspondería si te dejaran en tierra, y mejor en dinero que en vale.</p>
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
            "title": "Huelga 11 noviembre: vuelos, servicios mínimos y tus derechos",
            "desc": "¿Vuelas el 11N? Servicios mínimos en aeropuertos, qué hacer si cancelan tu vuelo y cuándo te corresponden 250–600 €. Actualizado el 3 de noviembre.",
            "h1": "Huelga general del 11 de noviembre: qué pasa con tu vuelo",
            "lead": "CCOO y UGT han convocado una huelga general de 24 horas en toda España el miércoles 11 de noviembre de 2026. Si vuelas ese día, esto es lo que te corresponde si tu vuelo se cancela o se retrasa.",
            "body": """<h2>Lo que se sabe (actualizado el 3 de noviembre)</h2>
<ul><li><strong>Fecha:</strong> miércoles 11 de noviembre de 2026, 24 horas, en toda España.</li>
<li><strong>Convocan:</strong> CCOO y UGT, con el apoyo de otros sindicatos. Han pedido al Ministerio de Transportes negociar los servicios mínimos tomando como base los de las huelgas generales de 2010 y 2012.</li>
<li><strong>Cancelaciones anunciadas:</strong> a 3 de noviembre no hemos encontrado cancelaciones anunciadas por Aena ni por las aerolíneas para ese día. Si tu aerolínea cancela tu vuelo a partir de ahora, ya será con menos de 14 días de aviso.</li>
<li><strong>Servicios mínimos en aeropuertos:</strong> a 3 de noviembre, aún sin publicar en la <a href="https://www.transportes.gob.es/aviacion-civil/informacion-util-al-pasajero/huelga-servicios-minimos" rel="noopener">página oficial del Ministerio de Transportes</a>. Los fija el Ministerio de Transportes, normalmente pocos días antes. Como referencia, en la huelga general de 2012 se garantizó el 10 % de los vuelos peninsulares, el 50 % de los enlaces con Baleares y Canarias, el 20 % de los vuelos a la UE y el 40 % del resto de internacionales. Los de 2026 pueden ser distintos.</li></ul>
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
<p>Más detalle: <a href="/vuelo-cancelado-que-hacer/">vuelo cancelado, qué hacer</a>, <a href="/circunstancias-extraordinarias-vuelo/">circunstancias extraordinarias</a> y <a href="/huelga-vueling/">¿hay huelga de Vueling?</a></p>""",
            "faq": [
                ("¿Hay vuelos el 11 de noviembre de 2026?", "Sí, la huelga no cierra los aeropuertos, pero puede haber cancelaciones y retrasos. A 3 de noviembre, los servicios mínimos aún no se han publicado."),
                ("¿Cuándo se publican los servicios mínimos?", "Los fija el Ministerio de Transportes, normalmente pocos días antes de la huelga, y los publica en su página de resoluciones de servicios mínimos."),
                ("¿Me compensan si me cancelan el vuelo por la huelga general?", "Depende de cuándo te avisaron y de qué personal hizo huelga. Con aviso de 14 días o más, no. Si fue el personal de la propia aerolínea y te avisaron con menos, normalmente sí. El reembolso o vuelo alternativo y la asistencia te corresponden siempre."),
                ("¿Qué día es el límite de los 14 días para el 11 de noviembre?", "El 28 de octubre. Una cancelación comunicada ese día o antes no da derecho a compensación fija."),
            ],
        },
        "en": {
            "title": "Spain strike 11 November: flights, minimum services, rights",
            "desc": "Flying on Wednesday 11 November? Status of Spain's airport minimum services, what to do if your flight is cancelled and when €250–600 applies. Updated 3 November.",
            "h1": "Spain general strike on 11 November: what it means for your flight",
            "lead": "Spain's two main unions, CCOO and UGT, have called a 24-hour nationwide general strike for Wednesday 11 November 2026. If you're flying that day, here's what you're entitled to if your flight is cancelled or delayed.",
            "body": """<h2>What we know (updated 3 November)</h2>
<ul><li><strong>Date:</strong> Wednesday 11 November 2026, 24 hours, across Spain.</li>
<li><strong>Called by:</strong> CCOO and UGT, backed by other unions. They have asked the Ministry of Transport to negotiate minimum services based on those of the 2010 and 2012 general strikes.</li>
<li><strong>Announced cancellations:</strong> as of 3 November we haven't found any cancellations announced by Aena or airlines for that day. If your airline cancels from now on, it will be with less than 14 days' notice.</li>
<li><strong>Airport minimum services:</strong> as of 3 November, not yet published on the <a href="https://www.transportes.gob.es/aviacion-civil/informacion-util-al-pasajero/huelga-servicios-minimos" rel="noopener">Ministry of Transport's official page</a>. Spain's Ministry of Transport sets them, usually a few days before. For reference, the 2012 general strike guaranteed 10% of mainland domestic flights, 50% of flights to and between the Balearic and Canary Islands, 20% of flights to the EU and 40% of other international flights. This year's may differ.</li></ul>
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
<p>More detail: <a href="/en/flight-cancelled-what-to-do/">flight cancelled, what to do</a>, <a href="/en/extraordinary-circumstances-flight-delay/">extraordinary circumstances</a> and <a href="/en/vueling-strike/">is there a Vueling strike?</a></p>""",
            "faq": [
                ("Will there be flights on 11 November 2026?", "Yes, the strike doesn't close airports, but cancellations and delays are possible. As of 3 November, minimum services haven't been published yet."),
                ("When are minimum services published?", "Spain's Ministry of Transport sets them, usually a few days before the strike, and publishes them on its minimum services page."),
                ("Do I get compensation if my flight is cancelled because of the general strike?", "It depends on when you were told and which staff went on strike. With 14 days' notice or more, no. If it was the airline's own staff and you were told with less notice, usually yes. A refund or new flight and care while you wait always apply."),
                ("What is the 14-day cut-off date for 11 November flights?", "28 October. A cancellation notified on or before that day carries no fixed compensation."),
            ],
        },
    },
    {
        "paths": {"es": "/huelga-easyjet-portugal-diciembre/", "en": "/en/easyjet-portugal-strike-december/", "pt": "/pt/greve-easyjet-portugal-dezembro/"},
        "es": {
            "title": "Huelga easyJet Portugal 19–23 diciembre: tus derechos",
            "desc": "Huelga de tripulantes de easyJet en Lisboa, Oporto y Faro del 19 al 23 de diciembre de 2026: reembolso, asistencia y cuándo te corresponden 250–600 €.",
            "h1": "Huelga de easyJet en Portugal del 19 al 23 de diciembre: qué te deben",
            "lead": "El sindicato portugués de tripulantes SNPVAC ha convocado huelga del personal de cabina de easyJet con base en Portugal del sábado 19 al miércoles 23 de diciembre de 2026, en plena Navidad. Al ser una huelga de la propia plantilla de la aerolínea, si te cancelan con poco aviso normalmente te corresponde compensación.",
            "body": """<h2>Lo que se sabe (actualizado el 27 de octubre)</h2>
<ul><li><strong>Fechas:</strong> del 19 al 23 de diciembre de 2026, ambos incluidos.</li>
<li><strong>Quién:</strong> tripulantes de cabina de easyJet con base en <strong>Lisboa, Oporto y Faro</strong>, convocados por el SNPVAC.</li>
<li><strong>Servicios mínimos:</strong> los ha fijado el Gobierno portugués (<a href="https://www.dgert.gov.pt/despacho-sm-n-o-51-25-09-easyjet_snpvac-greve-de-3-a-6-de-outubro-e-de-19-a-23-dezembro" rel="noopener">despacho de la DGERT</a>), con protección reforzada por la Navidad y para los enlaces con Madeira. El texto no publica una lista de vuelos garantizados.</li>
<li><strong>Precedente:</strong> en la huelga del 2 al 6 de octubre, el sindicato habló de 370 vuelos cancelados, la mayoría antes de empezar la huelga (<a href="https://www.rtp.pt/noticias/economia/greve-dos-tripulantes-da-easyjet-originou-o-cancelamento-de-370-voos-diz-sindicato_n1769960" rel="noopener">RTP</a>). easyJet dijo que canceló de forma preventiva para dar más previsibilidad.</li></ul>
<p>Afecta sobre todo a los vuelos que operan tripulaciones de esas tres bases, es decir, los que salen de Lisboa, Oporto o Faro o vuelven a ellas. Los vuelos de easyJet con tripulaciones de otras bases, como las españolas, en principio no están convocados. Revisa siempre tu reserva. La convocatoria puede cambiar o desconvocarse: sigue el <a href="/huelgas-vuelos-espana/">calendario de huelgas</a>.</p>
<h2>Si te cancelan el vuelo: siempre tienes estos derechos</h2>
<ul><li><strong>Reembolso en 7 días o vuelo alternativo</strong>, a tu elección (art. 8 del Reglamento 261/2004).</li>
<li><strong>Asistencia mientras esperas:</strong> comida, bebida y, si hay que pasar la noche, hotel y traslado (art. 9). Si no te lo dan, guarda los tickets y reclámalos.</li></ul>
<h2>La compensación de 250–600 €: aquí normalmente sí</h2>
<p>El Tribunal de Justicia de la UE dice que la huelga del personal de la propia aerolínea <strong>no es una circunstancia extraordinaria</strong> (asunto C-28/20, Airhelp contra SAS). Por eso, si te cancelan con menos de 14 días de aviso o llegas con más de 3 horas de retraso por la huelga, normalmente te corresponde la compensación:</p>
<ul><li><strong>250 €</strong> hasta 1.500 km (por ejemplo, la mayoría de vuelos entre Portugal y España).</li>
<li><strong>400 €</strong> entre 1.500 y 3.500 km, o cualquier vuelo más largo dentro de la UE.</li>
<li><strong>600 €</strong> a partir de 3.500 km fuera de la UE.</li></ul>
<h2>La fecha clave: 14 días antes de tu vuelo</h2>
<p>Si easyJet te avisa de la cancelación con 14 días o más de antelación, no hay compensación fija (sí reembolso o vuelo alternativo):</p>
<ul><li>Vuelo el <strong>19 de diciembre</strong>: un aviso el 5 de diciembre o antes no da compensación.</li>
<li>Vuelo el <strong>23 de diciembre</strong>: un aviso el 9 de diciembre o antes no da compensación.</li></ul>
<p>Guarda el correo o el SMS del aviso con su fecha: es lo que decide si cobras.</p>
<h2>Qué hacer si vuelas con easyJet esos días</h2>
<ol><li>Revisa la app o el correo de easyJet en las semanas previas.</li>
<li>Si te cancelan, haz captura del aviso y anota la fecha en que te avisaron.</li>
<li>Elige reembolso o vuelo alternativo y guarda todos los tickets de gastos.</li>
<li><a href="/">Calcula gratis cuánto te corresponde</a> con la distancia de tu ruta y genera la carta para reclamar tú mismo.</li>
<li>Reclama a easyJet por su formulario (mira <a href="/compensacion-retraso-easyjet/">cómo reclamar a easyJet</a>). Si no responde o lo rechaza, acude al organismo del país de salida: la ANAC en Portugal o <a href="https://www.seguridadaerea.gob.es/index.php/es/ambitos/derechos-de-los-pasajeros/inicia-tu-reclamacion-con-aesa" rel="noopener">AESA</a> en España.</li></ol>
<p>Más detalle: <a href="/vuelo-cancelado-que-hacer/">vuelo cancelado, qué hacer</a>.</p>""",
            "faq": [
                ("¿Cuándo es la huelga de easyJet en Portugal?", "Del sábado 19 al miércoles 23 de diciembre de 2026. La convoca el SNPVAC para los tripulantes de cabina con base en Lisboa, Oporto y Faro."),
                ("¿Me pagan compensación si easyJet cancela mi vuelo por la huelga?", "Normalmente sí, si te avisan con menos de 14 días: la huelga de la propia plantilla no es circunstancia extraordinaria (TJUE, C-28/20). Son 250, 400 o 600 € según la distancia, además del reembolso o vuelo alternativo."),
                ("¿Y si me avisan con más de 14 días?", "Entonces no hay compensación fija, pero sí puedes elegir el reembolso completo o un vuelo alternativo. Para un vuelo el 19 de diciembre, el límite es el 5 de diciembre."),
            ],
        },
        "pt": {
            "title": "Greve easyJet 19–23 dezembro: os seus direitos e indemnização",
            "desc": "Greve dos tripulantes da easyJet em Lisboa, Porto e Faro de 19 a 23 de dezembro de 2026: reembolso, assistência e quando tem direito a 250–600 €.",
            "h1": "Greve da easyJet de 19 a 23 de dezembro: o que lhe devem",
            "lead": "O SNPVAC convocou greve dos tripulantes de cabine da easyJet com base em Portugal de sábado, 19, a quarta-feira, 23 de dezembro de 2026, em pleno Natal. Como é uma greve do pessoal da própria companhia, se o seu voo for cancelado com pouco aviso, em regra tem direito a indemnização.",
            "body": """<h2>O que se sabe (atualizado a 7 de novembro)</h2>
<ul><li><strong>Datas:</strong> de 19 a 23 de dezembro de 2026, inclusive.</li>
<li><strong>Quem:</strong> tripulantes de cabine da easyJet com base em <strong>Lisboa, Porto e Faro</strong>, convocados pelo SNPVAC.</li>
<li><strong>Serviços mínimos:</strong> fixados pelo Governo (<a href="https://www.dgert.gov.pt/despacho-sm-n-o-51-25-09-easyjet_snpvac-greve-de-3-a-6-de-outubro-e-de-19-a-23-dezembro" rel="noopener">despacho da DGERT</a>), com proteção reforçada para as deslocações de Natal e para as ligações à Madeira. O despacho não publica uma lista de voos garantidos.</li>
<li><strong>Precedente:</strong> na greve de 2 a 6 de outubro, o sindicato falou em 370 voos cancelados, a maioria antes de a greve começar (<a href="https://www.rtp.pt/noticias/economia/greve-dos-tripulantes-da-easyjet-originou-o-cancelamento-de-370-voos-diz-sindicato_n1769960" rel="noopener">RTP</a>). A easyJet disse que cancelou de forma preventiva para dar mais previsibilidade aos passageiros.</li></ul>
<p>Afeta sobretudo os voos operados por tripulações destas três bases, ou seja, os que partem de Lisboa, Porto ou Faro ou regressam a estes aeroportos. Os voos da easyJet com tripulações de outras bases, como as do Reino Unido ou de Espanha, em princípio não estão abrangidos. Confirme sempre a sua reserva. A greve pode mudar ou ser desconvocada: acompanhe o <a href="/pt/greves-voos/">calendário de greves</a>.</p>
<h2>Se o voo for cancelado: tem sempre estes direitos</h2>
<ul><li><strong>Reembolso no prazo de 7 dias ou voo alternativo</strong>, à sua escolha (art. 8.º do Regulamento 261/2004).</li>
<li><strong>Assistência durante a espera:</strong> refeições, bebidas e, se tiver de passar a noite, hotel e transporte (art. 9.º). Se não lhe derem nada, guarde os recibos e reclame-os.</li></ul>
<h2>A indemnização de 250–600 €: aqui, em regra, sim</h2>
<p>O Tribunal de Justiça da UE decidiu que a greve do pessoal da própria companhia <strong>não é uma circunstância extraordinária</strong> (processo C-28/20, Airhelp contra SAS). Por isso, se o voo for cancelado com menos de 14 dias de aviso ou chegar com mais de 3 horas de atraso por causa da greve, em regra tem direito a:</p>
<ul><li><strong>250 €</strong> até 1500 km (por exemplo, Lisboa–Madrid ou Porto–Paris).</li>
<li><strong>400 €</strong> entre 1500 e 3500 km, ou qualquer voo mais longo dentro da UE (por exemplo, Lisboa–Londres ou Faro–Berlim).</li>
<li><strong>600 €</strong> a partir de 3500 km fora da UE.</li></ul>
<h2>A data-chave: 14 dias antes do voo</h2>
<p>Se a easyJet o avisar do cancelamento com 14 dias ou mais de antecedência, não há indemnização fixa (mas tem direito a reembolso ou voo alternativo):</p>
<ul><li>Voo a <strong>19 de dezembro</strong>: um aviso até 5 de dezembro, inclusive, não dá indemnização.</li>
<li>Voo a <strong>23 de dezembro</strong>: um aviso até 9 de dezembro, inclusive, não dá indemnização.</li></ul>
<p>Guarde o e-mail ou a SMS do aviso, com a data: é isso que decide se recebe.</p>
<h2>O que fazer se voar com a easyJet nesses dias</h2>
<ol><li>Consulte a aplicação e o e-mail da easyJet nas semanas anteriores.</li>
<li>Se o voo for cancelado, faça uma captura do aviso e anote a data em que foi informado.</li>
<li>Escolha o reembolso ou o voo alternativo e guarde todos os recibos de despesas.</li>
<li><a href="/pt/">Calcule gratuitamente quanto lhe é devido</a> com a distância do seu percurso e gere a carta para reclamar sozinho.</li>
<li>Reclame à easyJet pelo formulário da companhia. Se não responder em 6 semanas ou recusar, reclame gratuitamente à <a href="https://www.anac.pt/vPT/Passageiros/DireitosPassageiro/comoapresentarumaqueixa/Paginas/Comoapresentarumareclamacao.aspx" rel="noopener">ANAC</a> (voos com partida de Portugal; até 3 anos a contar da data do voo) ou à <a href="https://www.seguridadaerea.gob.es/index.php/es/ambitos/derechos-de-los-pasajeros/inicia-tu-reclamacion-con-aesa" rel="noopener">AESA</a> se o voo partiu de Espanha.</li></ol>""",
            "faq": [
                ("Quando é a greve da easyJet em Portugal?", "De sábado, 19, a quarta-feira, 23 de dezembro de 2026. Foi convocada pelo SNPVAC para os tripulantes de cabine com base em Lisboa, Porto e Faro."),
                ("Recebo indemnização se a easyJet cancelar o meu voo por causa da greve?", "Em regra, sim, se for avisado com menos de 14 dias: a greve do pessoal da própria companhia não é uma circunstância extraordinária (TJUE, C-28/20). São 250, 400 ou 600 € consoante a distância, além do reembolso ou do voo alternativo."),
                ("E se me avisarem com mais de 14 dias?", "Nesse caso não há indemnização fixa, mas pode escolher o reembolso total ou um voo alternativo. Para um voo a 19 de dezembro, o limite é 5 de dezembro."),
            ],
        },
        "en": {
            "title": "easyJet Portugal strike 19–23 December: your rights",
            "desc": "easyJet cabin crew strike in Lisbon, Porto and Faro on 19–23 December 2026: refunds, meals and hotels, and when €250–600 compensation applies.",
            "h1": "easyJet Portugal strike on 19–23 December: what you're owed",
            "lead": "Portugal's cabin crew union SNPVAC has called a strike by easyJet cabin crew based in Portugal from Saturday 19 to Wednesday 23 December 2026, right over Christmas. Because it's the airline's own staff striking, a short-notice cancellation usually means you're owed compensation.",
            "body": """<h2>What we know (updated 27 October)</h2>
<ul><li><strong>Dates:</strong> 19 to 23 December 2026 inclusive.</li>
<li><strong>Who:</strong> easyJet cabin crew based in <strong>Lisbon, Porto and Faro</strong>, called by SNPVAC.</li>
<li><strong>Minimum services:</strong> set by the Portuguese government (<a href="https://www.dgert.gov.pt/despacho-sm-n-o-51-25-09-easyjet_snpvac-greve-de-3-a-6-de-outubro-e-de-19-a-23-dezembro" rel="noopener">DGERT order</a>), with extra protection for Christmas travel and for Madeira. The order doesn't publish a list of protected flights.</li>
<li><strong>Precedent:</strong> during the 2–6 October strike, the union said 370 flights were cancelled, most of them before the strike started (<a href="https://www.rtp.pt/noticias/economia/greve-dos-tripulantes-da-easyjet-originou-o-cancelamento-de-370-voos-diz-sindicato_n1769960" rel="noopener">RTP</a>). easyJet said it cancelled early to give passengers more certainty.</li></ul>
<p>It mainly affects flights crewed from those three bases, so flights leaving from or returning to Lisbon, Porto or Faro. easyJet flights crewed from other bases, such as the UK or Spain, are not part of this strike, but check your booking. Strikes can change or be called off: follow our <a href="/en/flight-strikes-spain-europe/">strike calendar</a>.</p>
<h2>If your flight is cancelled: you always get this</h2>
<ul><li><strong>A refund within 7 days or a new flight</strong>, your choice (Art. 8 of EU261).</li>
<li><strong>Care while you wait:</strong> meals, drinks and, if you're stuck overnight, a hotel and transfers (Art. 9). Keep your receipts if the airline doesn't provide it.</li></ul>
<h2>€250–600 compensation: usually yes here</h2>
<p>The EU Court of Justice ruled that a strike by the airline's own staff is <strong>not an extraordinary circumstance</strong> (case C-28/20, Airhelp v SAS). So if your flight is cancelled with less than 14 days' notice, or you arrive more than 3 hours late because of the strike, you're usually owed:</p>
<ul><li><strong>€250</strong> up to 1,500 km.</li>
<li><strong>€400</strong> from 1,500 to 3,500 km, or any longer flight within the EU.</li>
<li><strong>€600</strong> beyond 3,500 km outside the EU.</li></ul>
<h2>The key date: 14 days before your flight</h2>
<p>If easyJet tells you about the cancellation 14 days or more before departure, there's no fixed compensation (you still get a refund or new flight):</p>
<ul><li>Flight on <strong>19 December</strong>: notice on or before 5 December means no compensation.</li>
<li>Flight on <strong>23 December</strong>: notice on or before 9 December means no compensation.</li></ul>
<p>Keep the cancellation email or text with its date: it decides whether you get paid.</p>
<h2>What to do if you're flying easyJet on those days</h2>
<ol><li>Check the easyJet app and your emails in the weeks before.</li>
<li>If you're cancelled, screenshot the notice and note the date you were told.</li>
<li>Choose a refund or new flight and keep every receipt.</li>
<li><a href="/en/">Work out what you're owed for free</a> using your route's distance, and generate a claim letter to send yourself.</li>
<li>Claim through easyJet's form (see <a href="/en/easyjet-delay-compensation/">how to claim from easyJet</a>). If it refuses or doesn't reply, go to the body in the country you flew from: ANAC in Portugal, AESA in Spain, or the airline's ADR scheme or the CAA for flights from the UK.</li></ol>
<p>More detail: <a href="/en/flight-cancelled-what-to-do/">flight cancelled, what to do</a>.</p>""",
            "faq": [
                ("When is the easyJet strike in Portugal?", "From Saturday 19 to Wednesday 23 December 2026. SNPVAC called it for cabin crew based in Lisbon, Porto and Faro."),
                ("Will I get compensation if easyJet cancels my flight because of the strike?", "Usually yes, if you're told less than 14 days before: an airline's own staff strike is not extraordinary (CJEU, C-28/20). It's €250, €400 or €600 depending on distance, on top of a refund or new flight."),
                ("What if I'm told more than 14 days before?", "Then there's no fixed compensation, but you can still choose a full refund or a new flight. For a 19 December flight, the cut-off is 5 December."),
            ],
        },
    },
    {
        "paths": {"es": "/huelga-vueling/", "en": "/en/vueling-strike/"},
        "es": {
            "title": "Huelga Vueling 2026: ¿hay huelga convocada? Tus derechos",
            "desc": "¿Hay huelga de Vueling en 2026? Estado a 3 de noviembre según Transportes, cómo afecta la huelga general del 11N y qué te corresponde si cancelan tu vuelo.",
            "h1": "¿Hay huelga de Vueling en 2026?",
            "lead": "A 3 de noviembre de 2026 no hay ninguna huelga de la plantilla de Vueling (pilotos ni tripulantes de cabina) con servicios mínimos publicados por el Ministerio de Transportes. Pero hay otras huelgas que sí pueden afectar a tu vuelo de Vueling.",
            "body": """<h2>Lo que se sabe (actualizado el 3 de noviembre)</h2>
<ul><li><strong>Huelga de la plantilla de Vueling:</strong> no figura ninguna en las <a href="https://www.transportes.gob.es/aviacion-civil/informacion-util-al-pasajero/huelga-servicios-minimos" rel="noopener">resoluciones de servicios mínimos del Ministerio de Transportes</a>, que es donde se publican todas las huelgas del sector aéreo en España. Si se convoca, la añadiremos al <a href="/huelgas-vuelos-espana/">calendario de huelgas</a>.</li>
<li><strong>Huelga general del 11 de noviembre:</strong> afecta a todo el país, también a los vuelos de Vueling. Mira <a href="/huelga-general-11-noviembre-vuelos/">qué pasa con tu vuelo el 11N</a>.</li>
<li><strong>Otras huelgas en aeropuertos hasta el 30 de noviembre:</strong> el handling de Groundforce en El Prat (CGT) y el control de torre de SAERCO (USCA y CCOO) tienen huelgas indefinidas con servicios mínimos. Afectan a las aerolíneas y aeropuertos que trabajan con esas empresas; pregunta a Vueling si tu vuelo puede verse afectado.</li></ul>
<p>Un precedente: entre noviembre de 2022 y enero de 2023, los tripulantes de cabina de Vueling (sindicato Stavla) convocaron huelga los viernes, domingos, lunes y festivos.</p>
<h2>Si Vueling cancela tu vuelo: siempre tienes estos derechos</h2>
<ul><li><strong>Reembolso en 7 días o vuelo alternativo</strong>, a tu elección (art. 8 del Reglamento 261/2004).</li>
<li><strong>Asistencia mientras esperas:</strong> comida, bebida y, si hay que pasar la noche, hotel y traslado (art. 9). Si no te lo dan, guarda los tickets y reclámalos.</li></ul>
<h2>¿Y la compensación de 250–600 €?</h2>
<ul><li><strong>Huelga de pilotos o tripulantes de Vueling:</strong> normalmente sí, si te avisan con menos de 14 días. El Tribunal de Justicia de la UE dice que la huelga de la propia plantilla no es una circunstancia extraordinaria (asunto C-28/20).</li>
<li><strong>Huelga de controladores o de empresas ajenas a Vueling:</strong> normalmente no, porque se considera circunstancia extraordinaria.</li>
<li><strong>Huelga general:</strong> no hay una sentencia específica. Depende de qué personal paró y por qué se canceló tu vuelo. Pide el motivo por escrito.</li>
<li><strong>Retraso de más de 3 horas</strong> por una huelga de la propia plantilla: mismos importes que una cancelación.</li></ul>
<h2>Qué hacer</h2>
<ol><li>Revisa la app y el correo de Vueling los días previos al vuelo.</li>
<li>Si te cancelan, haz captura del aviso, anota la fecha y pide el motivo por escrito.</li>
<li><a href="/">Comprueba gratis si te corresponde compensación</a> y genera la carta para reclamar tú mismo (mira también <a href="/compensacion-retraso-vueling/">cómo reclamar a Vueling</a>).</li>
<li>Si Vueling no responde en un mes o lo rechaza, reclama gratis en <a href="https://www.seguridadaerea.gob.es/index.php/es/ambitos/derechos-de-los-pasajeros/inicia-tu-reclamacion-con-aesa" rel="noopener">AESA</a>.</li></ol>""",
            "faq": [
                ("¿Hay huelga de Vueling en noviembre o diciembre de 2026?", "A 3 de noviembre de 2026 no hay ninguna huelga de la plantilla de Vueling con servicios mínimos publicados por el Ministerio de Transportes. Sí hay una huelga general en toda España el 11 de noviembre y otras huelgas en aeropuertos hasta el 30 de noviembre."),
                ("¿Me paga Vueling si cancela mi vuelo por la huelga general del 11N?", "Depende de cuándo te avisaron y de qué personal paró. El reembolso o vuelo alternativo y la asistencia te corresponden siempre. La compensación de 250–600 € depende del motivo concreto de la cancelación."),
                ("¿Y si hacen huelga los tripulantes o pilotos de Vueling?", "Entonces normalmente sí te corresponde compensación si te avisan con menos de 14 días: la huelga de la propia plantilla no es circunstancia extraordinaria (TJUE, C-28/20)."),
            ],
        },
        "en": {
            "title": "Vueling strike 2026: is one called? Your rights",
            "desc": "Is there a Vueling strike in 2026? Status on 3 November from Spain's Ministry of Transport, how the 11 November general strike affects flights, and what you're owed.",
            "h1": "Is there a Vueling strike in 2026?",
            "lead": "As of 3 November 2026, there is no strike by Vueling's own staff (pilots or cabin crew) with minimum services published by Spain's Ministry of Transport. But other strikes can still affect your Vueling flight.",
            "body": """<h2>What we know (updated 3 November)</h2>
<ul><li><strong>Strike by Vueling staff:</strong> none appears in the <a href="https://www.transportes.gob.es/aviacion-civil/informacion-util-al-pasajero/huelga-servicios-minimos" rel="noopener">Ministry of Transport's minimum services orders</a>, where every aviation strike in Spain is published. If one is called, we'll add it to our <a href="/en/flight-strikes-spain-europe/">strike calendar</a>.</li>
<li><strong>General strike on 11 November:</strong> it covers the whole country, Vueling flights included. See <a href="/en/spain-general-strike-11-november-flights/">what it means for your flight</a>.</li>
<li><strong>Other airport strikes until 30 November:</strong> Groundforce ground handling at Barcelona El Prat (CGT) and SAERCO control tower staff (USCA and CCOO) have open-ended strikes with minimum services. They affect the airlines and airports that use those companies; ask Vueling whether your flight could be affected.</li></ul>
<p>A precedent: between November 2022 and January 2023, Vueling cabin crew (Stavla union) went on strike on Fridays, Sundays, Mondays and public holidays.</p>
<h2>If Vueling cancels your flight: you always get this</h2>
<ul><li><strong>A refund within 7 days or a new flight</strong>, your choice (Art. 8 of EU261).</li>
<li><strong>Care while you wait:</strong> meals, drinks and, if you're stuck overnight, a hotel and transfers (Art. 9). Keep your receipts if the airline doesn't provide it.</li></ul>
<h2>What about €250–600 compensation?</h2>
<ul><li><strong>Vueling pilots or cabin crew on strike:</strong> usually yes, with less than 14 days' notice. The EU Court of Justice says an airline's own staff strike is not an extraordinary circumstance (case C-28/20).</li>
<li><strong>Air traffic control or outside companies on strike:</strong> usually no, as it's treated as extraordinary.</li>
<li><strong>General strike:</strong> there's no specific ruling. It depends on which staff stopped work and why your flight was cancelled. Ask for the reason in writing.</li>
<li><strong>Delays over 3 hours</strong> caused by the airline's own staff striking: the same amounts as a cancellation.</li></ul>
<h2>What to do</h2>
<ol><li>Check the Vueling app and your emails in the days before you fly.</li>
<li>If you're cancelled, screenshot the notice, note the date and ask for the reason in writing.</li>
<li><a href="/en/">Check for free whether compensation applies</a> and generate a claim letter to send yourself (see also <a href="/en/vueling-delay-compensation/">how to claim from Vueling</a>).</li>
<li>If Vueling refuses or doesn't reply, escalate for free to AESA for flights from Spain, or to the airline's ADR scheme or the CAA for flights from the UK.</li></ol>""",
            "faq": [
                ("Is there a Vueling strike in November or December 2026?", "As of 3 November 2026, there is no strike by Vueling's own staff with minimum services published by Spain's Ministry of Transport. There is a nationwide general strike on 11 November and other airport strikes until 30 November."),
                ("Will Vueling compensate me if my flight is cancelled by the 11 November general strike?", "It depends on when you were told and which staff stopped work. A refund or new flight and care while you wait always apply. €250–600 compensation depends on the actual reason for the cancellation."),
                ("What if Vueling's cabin crew or pilots strike?", "Then you're usually owed compensation if you're told less than 14 days before: an airline's own staff strike is not extraordinary (CJEU, C-28/20)."),
            ],
        },
    },
]


def build(ctx):
    urls = []
    for g in G:
        P = g["paths"]
        for l in [x for x in ("es", "en", "pt") if x in g]:
            other = "en" if l == "es" else "es"
            t = g[l]
            faq_html = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in t["faq"])
            ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]}
            home = {"es": "/", "en": "/en/", "pt": "/pt/"}[l]
            cta = {"es": "Calcular mi compensación", "en": "Work out my compensation", "pt": "Calcular a minha indemnização"}[l]
            body = f"""<div class="wrap prose"><h1>{t['h1']}</h1><p class="lead">{t['lead']}</p>
<p><a class="btn btn-sign" href="{home}">{cta}</a></p>
{t['body']}
<h2>{ {"es": "Preguntas frecuentes", "en": "Common questions", "pt": "Perguntas frequentes"}[l] }</h2>{faq_html}</div>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>"""
            ctx["emit"](l, P[l], ctx["page"](l, t["title"], t["desc"], P[l], body, P, P[other]))
            urls.append(P[l])
    return urls
