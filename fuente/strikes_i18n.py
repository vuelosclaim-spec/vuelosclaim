"""Italian, German and Portuguese versions of the strike calendar. Each row of strikes.STRIKES is translated here, keyed by
(start date, English description); test_mantenimiento.py fails if a row has no translation."""

# (start, EN what) -> {"it": (when, what, status), "de": (...), "pt": (...)}
ROWS = {
    ("2026-10-01", "Control tower staff (SAERCO), open-ended strike"): {
        "it": ("Fino al 30 nov", "Personale delle torri di controllo (SAERCO), sciopero a tempo indeterminato", "Con servizi minimi"),
        "de": ("Bis 30. Nov.", "Personal der Kontrolltürme (SAERCO), unbefristeter Streik", "Mit Mindestdiensten"),
        "pt": ("Até 30 nov", "Pessoal das torres de controlo (SAERCO), greve por tempo indeterminado", "Com serviços mínimos")},
    ("2026-10-01", "Groundforce ground handling at El Prat (CGT), open-ended"): {
        "it": ("Fino al 30 nov", "Handling di Groundforce a El Prat (CGT), a tempo indeterminato", "Con servizi minimi"),
        "de": ("Bis 30. Nov.", "Bodenabfertigung von Groundforce in El Prat (CGT), unbefristet", "Mit Mindestdiensten"),
        "pt": ("Até 30 nov", "Assistência em escala da Groundforce em El Prat (CGT), por tempo indeterminado", "Com serviços mínimos")},
    ("2026-10-01", "Barajas baggage system (Outsmart), stoppages 05:00–07:00 and 13:00–15:00"): {
        "it": ("Fino al 30 nov (lun, gio, ven, sab, dom)", "Sistema bagagli di Barajas (Outsmart), fermate 05:00–07:00 e 13:00–15:00", "Con servizi minimi"),
        "de": ("Bis 30. Nov. (Mo, Do, Fr, Sa, So)", "Gepäcksystem in Barajas (Outsmart), Arbeitsniederlegungen 05:00–07:00 und 13:00–15:00", "Mit Mindestdiensten"),
        "pt": ("Até 30 nov (seg, qui, sex, sáb, dom)", "Sistema de bagagens de Barajas (Outsmart), paragens 05:00–07:00 e 13:00–15:00", "Com serviços mínimos")},
    ("2026-11-20", "General strike in Italy (CGIL union)"): {
        "it": ("20 nov, intera giornata", "Sciopero generale in Italia (CGIL)", "Proclamato; non compare nel calendario del trasporto aereo, effetto sui voli non confermato"),
        "de": ("20. Nov., ganztägig", "Generalstreik in Italien (Gewerkschaft CGIL)", "Angekündigt; nicht im Kalender für den Luftverkehr, Auswirkung auf Flüge nicht bestätigt"),
        "pt": ("20 nov, todo o dia", "Greve geral em Itália (sindicato CGIL)", "Convocada; não consta do calendário do transporte aéreo, efeito nos voos não confirmado")},
    ("2026-11-21", "Italian air traffic control (ENAV), national strike (Filt CGIL and UGL TA)"): {
        "it": ("21 nov, 13:00–17:00", "Controllo del traffico aereo (ENAV), sciopero nazionale (Filt CGIL e UGL TA)", "Proclamato"),
        "de": ("21. Nov., 13:00–17:00", "Italienische Flugsicherung (ENAV), landesweiter Streik (Filt CGIL und UGL TA)", "Angekündigt"),
        "pt": ("21 nov, 13:00–17:00", "Controlo de tráfego aéreo de Itália (ENAV), greve nacional (Filt CGIL e UGL TA)", "Convocada")},
    ("2026-11-22", "Air traffic control (ENAV) at Malpensa"): {
        "it": ("22 nov, 24 h", "Controllo del traffico aereo (ENAV) a Malpensa", "Proclamato"),
        "de": ("22. Nov., 24 Std.", "Flugsicherung (ENAV) in Mailand-Malpensa", "Angekündigt"),
        "pt": ("22 nov, 24 h", "Controlo de tráfego aéreo (ENAV) em Malpensa", "Convocada")},
    ("2026-11-22", "Airport security staff (Sicuritalia IVRI)"): {
        "it": ("22 nov, 24 h", "Personale di sicurezza aeroportuale (Sicuritalia IVRI)", "Proclamato"),
        "de": ("22. Nov., 24 Std.", "Sicherheitspersonal des Flughafens (Sicuritalia IVRI)", "Angekündigt"),
        "pt": ("22 nov, 24 h", "Pessoal de segurança do aeroporto (Sicuritalia IVRI)", "Convocada")},
    ("2026-11-22", "Toscana Aeroporti, GH Toscana and Consulta ground staff (USB)"): {
        "it": ("22 nov, 24 h", "Personale di terra di Toscana Aeroporti, GH Toscana e Consulta (USB)", "Proclamato"),
        "de": ("22. Nov., 24 Std.", "Bodenpersonal von Toscana Aeroporti, GH Toscana und Consulta (USB)", "Angekündigt"),
        "pt": ("22 nov, 24 h", "Pessoal de terra da Toscana Aeroporti, GH Toscana e Consulta (USB)", "Convocada")},
    ("2026-12-19", "easyJet cabin crew based in Portugal (SNPVAC)"): {
        "it": ("19–23 dic", "Assistenti di volo di easyJet con base in Portogallo (SNPVAC)", "Proclamato; servizi minimi fissati dal governo portoghese"),
        "de": ("19.–23. Dez.", "Kabinenpersonal von easyJet mit Basis in Portugal (SNPVAC)", "Angekündigt; Mindestdienste von der portugiesischen Regierung festgelegt"),
        "pt": ("19–23 dez", "Tripulantes de cabine da easyJet com base em Portugal (SNPVAC)", "Convocada; serviços mínimos fixados pelo Governo português")},
}

WHERE = {
    "it": {"Barcelona-El Prat": "Barcellona-El Prat", "Madrid-Barajas": "Madrid-Barajas",
           "Jerez, A Coruña, Sevilla, Vigo, Fuerteventura, Lanzarote, La Palma, El Hierro, Madrid-Cuatro Vientos":
               "Jerez, A Coruña, Siviglia, Vigo, Fuerteventura, Lanzarote, La Palma, El Hierro, Madrid-Cuatro Vientos (Spagna)",
           "Leeds Bradford (Reino Unido)": "Leeds Bradford (Regno Unito)", "Bari (Italia)": "Bari", "Toda Italia": "Tutta Italia",
           "Milán-Malpensa (Italia)": "Milano Malpensa", "Venecia (Italia)": "Venezia", "Pisa y Florencia (Italia)": "Pisa e Firenze",
           "Lisboa, Oporto y Faro (Portugal)": "Lisbona, Porto e Faro (Portogallo)",
           "Toda España: posible impacto en tierra y en el transporte al aeropuerto": "Tutta la Spagna: possibile impatto a terra e sui trasporti per l'aeroporto"},
    "de": {"Barcelona-El Prat": "Barcelona-El Prat", "Madrid-Barajas": "Madrid-Barajas",
           "Jerez, A Coruña, Sevilla, Vigo, Fuerteventura, Lanzarote, La Palma, El Hierro, Madrid-Cuatro Vientos":
               "Jerez, A Coruña, Sevilla, Vigo, Fuerteventura, Lanzarote, La Palma, El Hierro, Madrid-Cuatro Vientos (Spanien)",
           "Leeds Bradford (Reino Unido)": "Leeds Bradford (Vereinigtes Königreich)", "Bari (Italia)": "Bari (Italien)", "Toda Italia": "Ganz Italien",
           "Milán-Malpensa (Italia)": "Mailand-Malpensa (Italien)", "Venecia (Italia)": "Venedig (Italien)", "Pisa y Florencia (Italia)": "Pisa und Florenz (Italien)",
           "Lisboa, Oporto y Faro (Portugal)": "Lissabon, Porto und Faro (Portugal)",
           "Toda España: posible impacto en tierra y en el transporte al aeropuerto": "Ganz Spanien: mögliche Auswirkungen am Boden und auf die Anreise zum Flughafen"},
    "pt": {"Barcelona-El Prat": "Barcelona-El Prat (Espanha)", "Madrid-Barajas": "Madrid-Barajas (Espanha)",
           "Jerez, A Coruña, Sevilla, Vigo, Fuerteventura, Lanzarote, La Palma, El Hierro, Madrid-Cuatro Vientos":
               "Jerez, Corunha, Sevilha, Vigo, Fuerteventura, Lanzarote, La Palma, El Hierro, Madrid-Cuatro Vientos (Espanha)",
           "Leeds Bradford (Reino Unido)": "Leeds Bradford (Reino Unido)", "Bari (Italia)": "Bari (Itália)", "Toda Italia": "Toda a Itália",
           "Milán-Malpensa (Italia)": "Milão-Malpensa (Itália)", "Venecia (Italia)": "Veneza (Itália)", "Pisa y Florencia (Italia)": "Pisa e Florença (Itália)",
           "Lisboa, Oporto y Faro (Portugal)": "Lisboa, Porto e Faro",
           "Toda España: posible impacto en tierra y en el transporte al aeropuerto": "Toda a Espanha: possível impacto em terra e no transporte para o aeroporto"},
}

KIND = {"it": {"airline": "Personale della compagnia", "atc": "Controllo del traffico aereo", "airport": "Aeroporto / handling", "general": "Sciopero generale"},
        "de": {"airline": "Personal der Fluggesellschaft", "atc": "Flugsicherung", "airport": "Flughafen / Bodenabfertigung", "general": "Generalstreik"},
        "pt": {"airline": "Pessoal da companhia", "atc": "Controlo de tráfego aéreo", "airport": "Aeroporto / assistência em escala", "general": "Greve geral"}}
COMP = {"it": {"airline": "Di norma sì", "atc": "Di norma no", "airport": "Dipende", "general": "Dipende"},
        "de": {"airline": "In der Regel ja", "atc": "In der Regel nein", "airport": "Kommt darauf an", "general": "Kommt darauf an"},
        "pt": {"airline": "Em regra, sim", "atc": "Em regra, não", "airport": "Depende", "general": "Depende"}}

# Messages of the "Am I owed anything?" checker: (no dates, notice after flight, >=14 days, own staff, ATC, other)
CHECK = {
    "it": ["Indica entrambe le date.", "La data dell'avviso è successiva al volo: controlla le date.",
           "Ti hanno avvisato con {d} giorni: nessuna compensazione fissa per la cancellazione, ma puoi comunque scegliere il rimborso completo o un volo alternativo.",
           "Avvisato con {d} giorni e lo sciopero era del personale della compagnia stessa: molto probabilmente ti spettano 250–600 € a passeggero, oltre al rimborso o a un volo alternativo.",
           "Avvisato con {d} giorni, ma gli scioperi del controllo aereo di solito sono circostanze eccezionali: è difficile ottenere la compensazione. Ti spettano comunque rimborso o volo alternativo, più pasti e albergo durante l'attesa.",
           "Avvisato con {d} giorni. Negli scioperi aeroportuali o generali dipende da se la compagnia poteva evitare la cancellazione: chiedile per iscritto la causa esatta. Rimborso o volo alternativo, più pasti e albergo, ti spettano in ogni caso."],
    "de": ["Bitte beide Daten eingeben.", "Das Datum der Mitteilung liegt nach dem Flug: Bitte prüfen Sie die Daten.",
           "Mitteilung {d} Tage vorher: keine feste Entschädigung für die Annullierung, aber Sie können volle Erstattung oder einen Ersatzflug wählen.",
           "Mitteilung {d} Tage vorher, und es streikte das eigene Personal der Fluggesellschaft: Ihnen stehen sehr wahrscheinlich 250–600 € pro Fluggast zu, dazu Erstattung oder Ersatzflug.",
           "Mitteilung {d} Tage vorher, aber Fluglotsenstreiks gelten meist als außergewöhnliche Umstände: Eine Entschädigung ist unwahrscheinlich. Erstattung oder Ersatzflug sowie Mahlzeiten und Hotel während der Wartezeit stehen Ihnen trotzdem zu.",
           "Mitteilung {d} Tage vorher. Bei Flughafen- oder Generalstreiks kommt es darauf an, ob die Fluggesellschaft die Annullierung hätte vermeiden können: Fragen Sie schriftlich nach der genauen Ursache. Erstattung oder Ersatzflug sowie Mahlzeiten und Hotel stehen Ihnen in jedem Fall zu."],
    "pt": ["Indique as duas datas.", "A data do aviso é posterior ao voo: verifique as datas.",
           "Foi avisado com {d} dias: não há indemnização fixa pelo cancelamento, mas pode escolher o reembolso total ou um voo alternativo.",
           "Avisado com {d} dias e a greve era do pessoal da própria companhia: muito provavelmente tem direito a 250–600 € por passageiro, além do reembolso ou de um voo alternativo.",
           "Avisado com {d} dias, mas as greves do controlo aéreo costumam ser circunstâncias extraordinárias: é difícil obter indemnização. Tem sempre direito a reembolso ou voo alternativo, e a refeições e hotel durante a espera.",
           "Avisado com {d} dias. Nas greves de aeroporto ou gerais, depende de a companhia ter podido evitar o cancelamento: peça-lhe por escrito a causa exata. Reembolso ou voo alternativo, e refeições e hotel, são-lhe sempre devidos."],
}

PAGE = {
    "it": dict(
        title="Scioperi aerei novembre–dicembre 2026: calendario e rimborsi",
        desc="Scioperi ENAV di novembre, sciopero generale in Spagna l'11 e easyJet Portogallo a dicembre: calendario con fonti ufficiali e quando spettano 250–600 €.",
        h1="Scioperi che colpiscono i voli: calendario e i tuoi diritti",
        lead="Aggiornato al {u}. Questi sono gli scioperi proclamati che possono colpire i voli da e per l'Italia, la Spagna e il Portogallo. Se il volo viene cancellato con meno di 14 giorni di preavviso, ciò che decide se ricevi 250–600 € è <strong>chi sciopera</strong>.",
        th="<th>Quando</th><th>Cosa e dove</th><th>Tipo</th><th>Compensazione?</th><th>Stato</th>",
        rules="""<h2>Mi pagano se cancellano il volo per sciopero?</h2>
<ul><li><strong>Sciopero del personale della compagnia</strong> (piloti, assistenti di volo): di norma <strong>sì</strong>. La Corte di giustizia dell'UE ha stabilito che non è una circostanza eccezionale (causa C-28/20).</li>
<li><strong>Sciopero del controllo del traffico aereo</strong> (ENAV): di norma <strong>no</strong>, perché la compagnia non può controllarlo.</li>
<li><strong>Sciopero aeroportuale, di handling o generale</strong>: <strong>dipende</strong> da se la compagnia poteva evitare la cancellazione. Chiedile la causa per iscritto.</li>
<li><strong>Sempre</strong>, qualunque sia lo sciopero: rimborso completo entro 7 giorni o volo alternativo, più pasti, bevande e albergo durante l'attesa.</li>
<li><strong>Se ti avvisano con 14 giorni o più</strong> di anticipo non c'è compensazione fissa per la cancellazione.</li></ul>
<p>In Italia, durante gli scioperi del trasporto aereo, i voli in partenza tra le 07:00 e le 10:00 e tra le 18:00 e le 21:00 sono di norma garantiti per legge (fasce di garanzia). Controlla comunque lo stato del tuo volo con la compagnia.</p>""",
        checker="""<h2>Mi spetta qualcosa? Verificalo</h2>
<form id="sk-form" class="sk"><label>Data del volo <input type="date" id="sk-flight" required></label>
<label>Data in cui ti hanno avvisato della cancellazione <input type="date" id="sk-notice" required></label>
<label>Chi scioperava? <select id="sk-kind"><option value="airline">Il personale della compagnia</option><option value="atc">Controllo del traffico aereo</option><option value="airport">Aeroporto o handling</option><option value="general">Sciopero generale</option></select></label>
<button class="btn btn-sign" type="submit">Verifica</button></form><p id="sk-out" class="lead" aria-live="polite"></p>
<p>Ritardo invece di cancellazione? <a href="/it/">Calcola l'importo esatto per la tua tratta</a>.</p>""",
        sources="Fonti",
        src_names=("Ministero dei Trasporti spagnolo, servizi minimi", "Ministero delle Infrastrutture e dei Trasporti, calendario degli scioperi", "CCOO, sciopero generale dell'11 novembre", "Unite, aeroporto di Leeds Bradford", "DGERT (Portogallo), servizi minimi easyJet"),
        none="Non ci sono più scioperi in corso in questo calendario. Consulta le fonti qui sotto per eventuali nuove proclamazioni.",
        faq_h="Domande frequenti", source="fonte", see=("Il tuo volo", "Calcola quanto ti spetta per la tua tratta, con lettera di reclamo gratuita:", "Calcolatore della compensazione"),
        faq=[("Mi rimborsano il biglietto se cancellano il volo per sciopero?", "Sì. Qualunque sia lo sciopero, puoi scegliere il rimborso completo del biglietto entro 7 giorni o un volo alternativo, e la compagnia deve darti pasti e albergo se devi aspettare."),
             ("Ricevo una compensazione se scioperano i controllori di volo?", "Di norma no: gli scioperi del controllo aereo sono considerati circostanze eccezionali. Hai comunque diritto al rimborso o a un volo alternativo e all'assistenza."),
             ("E se scioperano i piloti o gli assistenti di volo della compagnia?", "Allora di norma sì: la Corte di giustizia dell'UE considera che lo sciopero del personale della compagnia non è eccezionale, quindi ti spettano 250, 400 o 600 € se ti avvisano con meno di 14 giorni.")]),
    "de": dict(
        title="Streiks bei Flügen Nov.–Dez. 2026: Kalender und Entschädigung",
        desc="Fluglotsenstreiks in Italien, Generalstreik in Spanien am 11. November, easyJet Portugal im Dezember: Kalender mit amtlichen Quellen und wann 250–600 € zustehen.",
        h1="Streiks, die Flüge betreffen: Kalender und Ihre Rechte",
        lead="Stand: {u}. Diese angekündigten Streiks können Flüge nach und von Spanien, Italien und Portugal betreffen. Wird Ihr Flug weniger als 14 Tage vorher annulliert, entscheidet <strong>wer streikt</strong> darüber, ob Ihnen 250–600 € zustehen.",
        th="<th>Wann</th><th>Was und wo</th><th>Art</th><th>Entschädigung?</th><th>Status</th>",
        rules="""<h2>Bekomme ich Geld, wenn mein Flug wegen Streik annulliert wird?</h2>
<ul><li><strong>Streik des Personals der Fluggesellschaft</strong> (Piloten, Kabinenpersonal): in der Regel <strong>ja</strong>. Der Gerichtshof der EU hat entschieden, dass dies kein außergewöhnlicher Umstand ist (Rechtssache C-28/20).</li>
<li><strong>Fluglotsenstreik</strong>: in der Regel <strong>nein</strong>, weil die Fluggesellschaft ihn nicht beeinflussen kann.</li>
<li><strong>Streik am Flughafen, bei der Bodenabfertigung oder Generalstreik</strong>: <strong>kommt darauf an</strong>, ob die Fluggesellschaft die Annullierung hätte vermeiden können. Fragen Sie schriftlich nach der Ursache.</li>
<li><strong>Immer</strong>, egal bei welchem Streik: volle Erstattung innerhalb von 7 Tagen oder Ersatzflug sowie Mahlzeiten, Getränke und Hotel während der Wartezeit.</li>
<li><strong>Bei Mitteilung 14 Tage oder früher</strong> gibt es keine feste Entschädigung für die Annullierung.</li></ul>""",
        checker="""<h2>Steht mir etwas zu? Jetzt prüfen</h2>
<form id="sk-form" class="sk"><label>Flugdatum <input type="date" id="sk-flight" required></label>
<label>Datum der Mitteilung über die Annullierung <input type="date" id="sk-notice" required></label>
<label>Wer hat gestreikt? <select id="sk-kind"><option value="airline">Das Personal der Fluggesellschaft</option><option value="atc">Flugsicherung</option><option value="airport">Flughafen oder Bodenabfertigung</option><option value="general">Generalstreik</option></select></label>
<button class="btn btn-sign" type="submit">Prüfen</button></form><p id="sk-out" class="lead" aria-live="polite"></p>
<p>Verspätung statt Annullierung? <a href="/de/">Berechnen Sie hier den genauen Betrag für Ihre Strecke</a>.</p>""",
        sources="Quellen",
        src_names=("Spanisches Verkehrsministerium, Mindestdienste", "Italienisches Ministerium für Infrastruktur und Verkehr, Streikkalender", "CCOO, Generalstreik am 11. November", "Unite, Flughafen Leeds Bradford", "DGERT (Portugal), Mindestdienste easyJet"),
        none="In diesem Kalender laufen keine Streiks mehr. Prüfen Sie die Quellen unten auf neue Ankündigungen.",
        faq_h="Häufige Fragen", source="Quelle", see=("Ihr Flug", "Berechnen Sie, was Ihnen auf Ihrer Strecke zusteht, mit kostenlosem Anspruchsschreiben:", "Entschädigungsrechner"),
        faq=[("Bekomme ich mein Geld zurück, wenn mein Flug wegen Streik annulliert wird?", "Ja. Egal welcher Streik: Sie können die volle Erstattung des Tickets innerhalb von 7 Tagen oder einen Ersatzflug wählen, und die Fluggesellschaft muss Mahlzeiten und Hotel stellen, wenn Sie warten müssen."),
             ("Bekomme ich eine Entschädigung bei einem Fluglotsenstreik?", "In der Regel nicht: Fluglotsenstreiks gelten als außergewöhnliche Umstände. Erstattung oder Ersatzflug und Betreuung stehen Ihnen trotzdem zu."),
             ("Und wenn Piloten oder Kabinenpersonal der Fluggesellschaft streiken?", "Dann in der Regel ja: Der Gerichtshof der EU sieht einen Streik des eigenen Personals nicht als außergewöhnlich an, also stehen Ihnen 250, 400 oder 600 € zu, wenn die Mitteilung weniger als 14 Tage vorher kam.")]),
    "pt": dict(
        title="Greves nos voos novembro–dezembro 2026: calendário e direitos",
        desc="Greve da easyJet em Portugal de 19 a 23 de dezembro, controlo aéreo em Itália e greve geral em Espanha: calendário com fontes oficiais e quando recebe 250–600 €.",
        h1="Greves que afetam os voos: calendário e os seus direitos",
        lead="Atualizado a {u}. Estas são as greves convocadas que podem afetar voos de e para Portugal, Espanha e Itália. Se o voo for cancelado com menos de 14 dias de aviso, o que decide se recebe 250–600 € é <strong>quem faz greve</strong>.",
        th="<th>Quando</th><th>O quê e onde</th><th>Tipo</th><th>Indemnização?</th><th>Estado</th>",
        rules="""<h2>Pagam-me se o voo for cancelado por greve?</h2>
<ul><li><strong>Greve do pessoal da própria companhia</strong> (pilotos, tripulantes de cabine): em regra <strong>sim</strong>. O Tribunal de Justiça da UE decidiu que não é uma circunstância extraordinária (processo C-28/20).</li>
<li><strong>Greve do controlo de tráfego aéreo</strong>: em regra <strong>não</strong>, porque a companhia não a pode controlar.</li>
<li><strong>Greve no aeroporto, na assistência em escala ou greve geral</strong>: <strong>depende</strong> de a companhia ter podido evitar o cancelamento. Peça-lhe a causa por escrito.</li>
<li><strong>Sempre</strong>, seja qual for a greve: reembolso total no prazo de 7 dias ou voo alternativo, e refeições, bebidas e hotel durante a espera.</li>
<li><strong>Se for avisado com 14 dias ou mais</strong> de antecedência, não há indemnização fixa pelo cancelamento.</li></ul>
<p>A greve da easyJet de 19 a 23 de dezembro é do pessoal da própria companhia: veja <a href="/pt/greve-easyjet-portugal-dezembro/">datas, serviços mínimos e o que pode reclamar</a>.</p>""",
        checker="""<h2>Tenho direito a alguma coisa? Verifique</h2>
<form id="sk-form" class="sk"><label>Data do voo <input type="date" id="sk-flight" required></label>
<label>Data em que foi avisado do cancelamento <input type="date" id="sk-notice" required></label>
<label>Quem fez greve? <select id="sk-kind"><option value="airline">O pessoal da companhia</option><option value="atc">Controlo de tráfego aéreo</option><option value="airport">Aeroporto ou assistência em escala</option><option value="general">Greve geral</option></select></label>
<button class="btn btn-sign" type="submit">Verificar</button></form><p id="sk-out" class="lead" aria-live="polite"></p>
<p>Atraso em vez de cancelamento? <a href="/pt/">Calcule o montante exato para o seu percurso</a>.</p>""",
        sources="Fontes",
        src_names=("Ministério dos Transportes de Espanha, serviços mínimos", "Ministério das Infraestruturas e dos Transportes de Itália, calendário de greves", "CCOO, greve geral de 11 de novembro", "Unite, aeroporto de Leeds Bradford", "DGERT, serviços mínimos da greve da easyJet"),
        none="Já não há greves em curso neste calendário. Consulte as fontes abaixo para novas convocatórias.",
        faq_h="Perguntas frequentes", source="fonte", see=("O seu voo", "Calcule a que tem direito no seu percurso, com carta de reclamação gratuita:", "Calculadora de indemnização"),
        faq=[("Reembolsam-me o bilhete se o voo for cancelado por greve?", "Sim. Seja qual for a greve, pode escolher o reembolso total do bilhete no prazo de 7 dias ou um voo alternativo, e a companhia tem de lhe dar refeições e hotel se tiver de esperar."),
             ("Recebo indemnização se os controladores aéreos fizerem greve?", "Em regra, não: as greves do controlo aéreo são consideradas circunstâncias extraordinárias. Mantém o direito ao reembolso ou a um voo alternativo e à assistência."),
             ("E se fizerem greve os pilotos ou os tripulantes da companhia?", "Então, em regra, sim: o Tribunal de Justiça da UE considera que a greve do pessoal da própria companhia não é extraordinária, por isso tem direito a 250, 400 ou 600 € se for avisado com menos de 14 dias.")]),
}
UPDATED = {"it": "12 novembre 2026", "de": "12. November 2026", "pt": "12 de novembro de 2026"}
