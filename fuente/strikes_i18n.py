"""Italian and German versions of the strike calendar. Each row of strikes.STRIKES is translated here, keyed by
(start date, English description); test_mantenimiento.py fails if a row has no translation."""

# (start, EN what) -> {"it": (when, what, status), "de": (when, what, status)}
ROWS = {
    ("2026-10-01", "Control tower staff (SAERCO), open-ended strike"): {
        "it": ("Fino al 30 nov", "Personale delle torri di controllo (SAERCO), sciopero a tempo indeterminato", "Con servizi minimi"),
        "de": ("Bis 30. Nov.", "Personal der Kontrolltürme (SAERCO), unbefristeter Streik", "Mit Mindestdiensten")},
    ("2026-10-01", "Groundforce ground handling at El Prat (CGT), open-ended"): {
        "it": ("Fino al 30 nov", "Handling di Groundforce a El Prat (CGT), a tempo indeterminato", "Con servizi minimi"),
        "de": ("Bis 30. Nov.", "Bodenabfertigung von Groundforce in El Prat (CGT), unbefristet", "Mit Mindestdiensten")},
    ("2026-10-01", "Barajas baggage system (Outsmart), stoppages 05:00–07:00 and 13:00–15:00"): {
        "it": ("Fino al 30 nov (lun, gio, ven, sab, dom)", "Sistema bagagli di Barajas (Outsmart), fermate 05:00–07:00 e 13:00–15:00", "Con servizi minimi"),
        "de": ("Bis 30. Nov. (Mo, Do, Fr, Sa, So)", "Gepäcksystem in Barajas (Outsmart), Arbeitsniederlegungen 05:00–07:00 und 13:00–15:00", "Mit Mindestdiensten")},
    ("2026-10-23", "Airport staff, including air traffic controllers (Unite)"): {
        "it": ("23 ott – 2 nov", "Personale aeroportuale, compresi i controllori di volo (Unite)", "Sospeso durante le trattative mediate da Acas"),
        "de": ("23. Okt. – 2. Nov.", "Flughafenpersonal einschließlich Fluglotsen (Unite)", "Ausgesetzt während der Verhandlungen unter Vermittlung von Acas")},
    ("2026-11-06", "Air traffic control (ENAV) at Bari airport"): {
        "it": ("6 nov, 13:00–17:00", "Controllo del traffico aereo (ENAV) all'aeroporto di Bari", "Proclamato"),
        "de": ("6. Nov., 13:00–17:00", "Flugsicherung (ENAV) am Flughafen Bari", "Angekündigt")},
    ("2026-11-06", "Italian air traffic control (ENAV), national strike (Filt CGIL and UGL TA)"): {
        "it": ("6 nov, 13:00–17:00", "Controllo del traffico aereo (ENAV), sciopero nazionale (Filt CGIL e UGL TA)", "Non confermato: non compare in tutti i calendari; gli stessi sindacati ne hanno proclamato un altro il 21 nov"),
        "de": ("6. Nov., 13:00–17:00", "Italienische Flugsicherung (ENAV), landesweiter Streik (Filt CGIL und UGL TA)", "Nicht bestätigt: nicht in allen Kalendern; dieselben Gewerkschaften haben einen weiteren Streik am 21. Nov. angekündigt")},
    ("2026-11-11", "General strike in Spain (CCOO and UGT unions)"): {
        "it": ("11 nov, 24 h", "Sciopero generale in Spagna (CCOO e UGT)", "Proclamato; servizi minimi negli aeroporti non ancora pubblicati"),
        "de": ("11. Nov., 24 Std.", "Generalstreik in Spanien (Gewerkschaften CCOO und UGT)", "Angekündigt; Mindestdienste an Flughäfen noch nicht veröffentlicht")},
    ("2026-11-20", "General strike in Italy (CGIL union)"): {
        "it": ("20 nov, intera giornata", "Sciopero generale in Italia (CGIL)", "Proclamato; non compare nel calendario del trasporto aereo, effetto sui voli non confermato"),
        "de": ("20. Nov., ganztägig", "Generalstreik in Italien (Gewerkschaft CGIL)", "Angekündigt; nicht im Kalender für den Luftverkehr, Auswirkung auf Flüge nicht bestätigt")},
    ("2026-11-21", "Italian air traffic control (ENAV), national strike (Filt CGIL and UGL TA)"): {
        "it": ("21 nov, 13:00–17:00", "Controllo del traffico aereo (ENAV), sciopero nazionale (Filt CGIL e UGL TA)", "Proclamato"),
        "de": ("21. Nov., 13:00–17:00", "Italienische Flugsicherung (ENAV), landesweiter Streik (Filt CGIL und UGL TA)", "Angekündigt")},
    ("2026-11-22", "Air traffic control (ENAV) at Malpensa"): {
        "it": ("22 nov, 24 h", "Controllo del traffico aereo (ENAV) a Malpensa", "Proclamato"),
        "de": ("22. Nov., 24 Std.", "Flugsicherung (ENAV) in Mailand-Malpensa", "Angekündigt")},
    ("2026-11-22", "Airport security staff (Sicuritalia IVRI)"): {
        "it": ("22 nov, 24 h", "Personale di sicurezza aeroportuale (Sicuritalia IVRI)", "Proclamato"),
        "de": ("22. Nov., 24 Std.", "Sicherheitspersonal des Flughafens (Sicuritalia IVRI)", "Angekündigt")},
    ("2026-12-19", "easyJet cabin crew based in Portugal (SNPVAC)"): {
        "it": ("19–23 dic", "Assistenti di volo di easyJet con base in Portogallo (SNPVAC)", "Proclamato; servizi minimi fissati dal governo portoghese"),
        "de": ("19.–23. Dez.", "Kabinenpersonal von easyJet mit Basis in Portugal (SNPVAC)", "Angekündigt; Mindestdienste von der portugiesischen Regierung festgelegt")},
}

WHERE = {
    "it": {"Barcelona-El Prat": "Barcellona-El Prat", "Madrid-Barajas": "Madrid-Barajas",
           "Jerez, A Coruña, Sevilla, Vigo, Fuerteventura, Lanzarote, La Palma, El Hierro, Madrid-Cuatro Vientos":
               "Jerez, A Coruña, Siviglia, Vigo, Fuerteventura, Lanzarote, La Palma, El Hierro, Madrid-Cuatro Vientos (Spagna)",
           "Leeds Bradford (Reino Unido)": "Leeds Bradford (Regno Unito)", "Bari (Italia)": "Bari", "Toda Italia": "Tutta Italia",
           "Milán-Malpensa (Italia)": "Milano Malpensa", "Venecia (Italia)": "Venezia",
           "Lisboa, Oporto y Faro (Portugal)": "Lisbona, Porto e Faro (Portogallo)",
           "Toda España: posible impacto en tierra y en el transporte al aeropuerto": "Tutta la Spagna: possibile impatto a terra e sui trasporti per l'aeroporto"},
    "de": {"Barcelona-El Prat": "Barcelona-El Prat", "Madrid-Barajas": "Madrid-Barajas",
           "Jerez, A Coruña, Sevilla, Vigo, Fuerteventura, Lanzarote, La Palma, El Hierro, Madrid-Cuatro Vientos":
               "Jerez, A Coruña, Sevilla, Vigo, Fuerteventura, Lanzarote, La Palma, El Hierro, Madrid-Cuatro Vientos (Spanien)",
           "Leeds Bradford (Reino Unido)": "Leeds Bradford (Vereinigtes Königreich)", "Bari (Italia)": "Bari (Italien)", "Toda Italia": "Ganz Italien",
           "Milán-Malpensa (Italia)": "Mailand-Malpensa (Italien)", "Venecia (Italia)": "Venedig (Italien)",
           "Lisboa, Oporto y Faro (Portugal)": "Lissabon, Porto und Faro (Portugal)",
           "Toda España: posible impacto en tierra y en el transporte al aeropuerto": "Ganz Spanien: mögliche Auswirkungen am Boden und auf die Anreise zum Flughafen"},
}

KIND = {"it": {"airline": "Personale della compagnia", "atc": "Controllo del traffico aereo", "airport": "Aeroporto / handling", "general": "Sciopero generale"},
        "de": {"airline": "Personal der Fluggesellschaft", "atc": "Flugsicherung", "airport": "Flughafen / Bodenabfertigung", "general": "Generalstreik"}}
COMP = {"it": {"airline": "Di norma sì", "atc": "Di norma no", "airport": "Dipende", "general": "Dipende"},
        "de": {"airline": "In der Regel ja", "atc": "In der Regel nein", "airport": "Kommt darauf an", "general": "Kommt darauf an"}}

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
}
UPDATED = {"it": "27 ottobre 2026", "de": "27. Oktober 2026"}
