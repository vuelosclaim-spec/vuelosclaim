"""Italian and German texts for the home page, header, footer and calculator (ES/EN stay in build.py).
Legal pages (about, legal notice, privacy) are linked in English: the owner's legal information is not translated.
"""

ENAC_URL = "https://www.enac.gov.it/passeggeri/diritti-dei-passeggeri/modalita-di-reclamo-per-negato-imbarco-cancellazione-ritardo/"
EVZ_ADR_URL = "https://www.evz.de/einkaufen-internet/odr-adr/schlichtungsstellen-deutschland/fernreise-nahverkehr.html"
EU_URL = {"it": "https://europa.eu/youreurope/citizens/travel/passenger-rights/air/index_it.htm",
          "de": "https://europa.eu/youreurope/citizens/travel/passenger-rights/air/index_de.htm"}
UPDATED = {"it": "7 ottobre 2026", "de": "7. Oktober 2026"}
HOME = {"it": "/it/", "de": "/de/"}
STRIKES = {"it": "/it/scioperi-aerei/", "de": "/de/streik-fluege/"}


def S(brand, aesa_url, caa_url):
    return {
     "it": dict(
      locale="it_IT", nav="Principale", nav_amounts="Importi", nav_airlines="Scioperi", nav_faq="Domande", switch="IT", switch_label="Italiano",
      foot1=f'{brand} è un calcolatore indicativo basato sul <a href="{EU_URL["it"]}" rel="noopener">Regolamento (CE) n. 261/2004</a>. Non è una consulenza legale e non sostituisce un avvocato.',
      foot2="Alcuni link sono di affiliazione: se usi un servizio tramite questi link, riceviamo una commissione senza costi per te. Questo non cambia mai il risultato del calcolatore.",
      foot3="Ultima revisione di importi e norme: {d}.", f_embed="", f_about="Chi siamo e fonti (in inglese)", f_legal="Note legali (in inglese)", f_privacy="Privacy (in inglese)",
      calc_h="Calcola la tua compensazione", from_="Partenza", to="Destinazione finale", ph="Città o codice", airline="Compagnia aerea",
      al_unknown="Non lo so / non è in elenco", al_eu="Altra compagnia europea", al_noneu="Altra compagnia non europea",
      via="Hai fatto scalo?", v=[("direct", "No, volo diretto"), ("same", "Sì, una prenotazione e la stessa compagnia"), ("mixed", "Sì, una prenotazione e compagnie diverse"), ("separate", "Sì, con prenotazioni separate")],
      fare="Il biglietto", fa=[("public", "L'ho pagato (anche con punti o in un pacchetto)"), ("staff", "Gratuito o con tariffa non pubblica (es. da dipendente)")],
      what="Che cosa è successo al tuo volo?", w=[("delay", "Ritardo"), ("cancel", "Cancellazione"), ("denied", "Overbooking")],
      delay="Ritardo all'arrivo alla destinazione finale", d=[("lt3", "Meno di 3 h"), ("3to4", "Da 3 h esatte a 4 h"), ("gt4", "Più di 4 h"), ("unknown", "Non lo so")],
      notice="Ti hanno avvisato della cancellazione con", n=[("gt14", "14 giorni o più"), ("7to14", "Tra 7 e 13 giorni"), ("lt7", "Meno di 7 giorni"), ("unknown", "Non lo so")],
      reroute="Ti hanno offerto un volo alternativo?", rr=[("yes", "Sì"), ("no", "No"), ("unknown", "Non lo so")],
      rdep="Il volo alternativo partiva, rispetto all'originale…", rd=[("le1", "Al massimo 1 h prima, o più tardi"), ("1to2", "Tra 1 e 2 h prima"), ("gt2", "Più di 2 h prima"), ("unknown", "Non lo so")],
      rarr="…e arrivava a destinazione", ra=[("lt2", "Meno di 2 h dopo"), ("2to4", "Tra 2 e 4 h dopo"), ("ge4", "4 h o più dopo"), ("unknown", "Non lo so")],
      accepted="Hai accettato il volo alternativo?", ac=[("yes", "Sì"), ("no", "No, ho chiesto il rimborso")],
      denied="Hai ceduto il tuo posto?", dn=[("invol", "No, me l'hanno negato"), ("vol", "Sì, volontariamente"), ("unknown", "Non mi è chiaro")],
      checkin="Ti sei presentato in tempo al check-in e all'imbarco?", ci=[("yes", "Sì"), ("no", "No"), ("unknown", "Non lo so")],
      dreason="Motivo del negato imbarco", dr=[("overbooking", "Overbooking o altro motivo della compagnia"), ("reasonable", "Salute, sicurezza o documenti"), ("unknown", "Non me l'hanno spiegato")],
      cause="Motivo indicato dalla compagnia", c=[("unknown", "Non me l'hanno detto"), ("tech", "Guasto tecnico"), ("crew", "Mancanza o malattia dell'equipaggio"),
        ("strike_own", "Sciopero del personale della compagnia"), ("strike_ext", "Sciopero dei controllori di volo o dell'aeroporto"), ("strike_sub", "Sciopero di un'impresa che lavora per la compagnia (handling, catering…)"), ("atc", "Restrizione del controllo del traffico aereo (ATC)"),
        ("weather", "Maltempo"), ("security", "Sicurezza (minaccia, chiusura dello spazio aereo)"), ("bird", "Impatto con un volatile o un oggetto sulla pista"),
        ("knock", "Ritardo del volo precedente dello stesso aereo")],
      empty="Scegli partenza e destinazione per vedere il risultato.", error="Non è stato possibile caricare l'elenco degli aeroporti. Controlla la connessione e riprova.", retry="Riprova",
      example="Esempio modificabile", per="a passeggero", cta="Reclama con AirHelp", cta_small="AirHelp è un servizio esterno di reclamo: non chiede nulla in anticipo e, se ottiene la compensazione, trattiene una percentuale (fino al 50 % se serve andare in tribunale). Non garantisce il risultato. È un link di affiliazione: VuelosClaim riceve una commissione senza costi per te.", cta_generic="Reclama con una società", cta_small_generic="Servizio esterno di reclamo: trattiene una commissione se ottiene la compensazione e non garantisce il risultato. Link di affiliazione.",
      cmp="Confronta con il reclamo gratuito fai da te",
      self="Preferisco reclamare da solo gratis: genera la mia lettera", l_lead="Compila i tuoi dati e prepariamo la lettera. Viene composta nel tuo browser: non la inviamo né la salviamo. Non servono dati bancari.",
      l_name="Nome e cognome", l_book="Codice di prenotazione", l_flight="Numero del volo", l_date="Data del volo", l_pax="Passeggeri nella prenotazione",
      l_text="La tua lettera", copy="Copia la lettera", dl="Scarica .txt",
      steps=["Inviala tramite il modulo reclami sul sito della compagnia aerea o per e-mail, allegando la carta d'imbarco.", "Conserva la prova dell'invio.",
             f'Se entro un mese non pagano o rifiutano: per i voli in partenza dall\'Italia puoi presentare reclamo gratuito all\'<a href="{ENAC_URL}" rel="noopener" target="_blank">ENAC</a>; per i voli dalla Spagna, ad <a href="{aesa_url}" rel="noopener" target="_blank">AESA</a>.'],
      eyebrow="Regolamento CE 261/2004",
      facts=[("250 €", "voli fino a 1.500 km"), ("400 €", "da 1.500 a 3.500 km, o oltre 1.500 km nell'UE"), ("600 €", "oltre 3.500 km")],
      skip="Vai al contenuto",
     ),
     "de": dict(
      locale="de_DE", nav="Hauptmenü", nav_amounts="Beträge", nav_airlines="Streiks", nav_faq="Fragen", switch="DE", switch_label="Deutsch",
      foot1=f'{brand} ist ein unverbindlicher Rechner auf Grundlage der <a href="{EU_URL["de"]}" rel="noopener">Verordnung (EG) Nr. 261/2004</a>. Er ist keine Rechtsberatung und ersetzt keinen Anwalt.',
      foot2="Einige Links sind Affiliate-Links: Wenn Sie darüber einen Dienst nutzen, erhalten wir eine Provision, ohne dass Ihnen Kosten entstehen. Das Ergebnis des Rechners ändert sich dadurch nie.",
      foot3="Letzte Prüfung der Beträge und Regeln: {d}.", f_embed="", f_about="Über uns und Quellen (Englisch)", f_legal="Impressum (Englisch)", f_privacy="Datenschutz (Englisch)",
      calc_h="Entschädigung berechnen", from_="Abflug", to="Endziel", ph="Stadt oder Code", airline="Fluggesellschaft",
      al_unknown="Weiß ich nicht / nicht aufgeführt", al_eu="Andere europäische Fluggesellschaft", al_noneu="Andere nichteuropäische Fluggesellschaft",
      via="Sind Sie umgestiegen?", v=[("direct", "Nein, Direktflug"), ("same", "Ja, eine Buchung, dieselbe Fluggesellschaft"), ("mixed", "Ja, eine Buchung, verschiedene Fluggesellschaften"), ("separate", "Ja, getrennte Buchungen")],
      fare="Ihr Ticket", fa=[("public", "Bezahlt (auch mit Meilen oder als Pauschalreise)"), ("staff", "Kostenlos oder nicht öffentlicher Tarif (z. B. Mitarbeiterticket)")],
      what="Was ist mit Ihrem Flug passiert?", w=[("delay", "Verspätung"), ("cancel", "Annullierung"), ("denied", "Überbuchung")],
      delay="Verspätung bei Ankunft am Endziel", d=[("lt3", "Unter 3 Std."), ("3to4", "Genau 3 bis 4 Std."), ("gt4", "Über 4 Std."), ("unknown", "Weiß ich nicht")],
      notice="Die Annullierung wurde Ihnen mitgeteilt", n=[("gt14", "14 Tage oder früher"), ("7to14", "7 bis 13 Tage vorher"), ("lt7", "Weniger als 7 Tage vorher"), ("unknown", "Weiß ich nicht")],
      reroute="Wurde Ihnen ein Ersatzflug angeboten?", rr=[("yes", "Ja"), ("no", "Nein"), ("unknown", "Weiß ich nicht")],
      rdep="Im Vergleich zum ursprünglichen Flug startete der Ersatzflug…", rd=[("le1", "Höchstens 1 Std. früher, oder später"), ("1to2", "1 bis 2 Std. früher"), ("gt2", "Mehr als 2 Std. früher"), ("unknown", "Weiß ich nicht")],
      rarr="…und kam an", ra=[("lt2", "Weniger als 2 Std. später"), ("2to4", "2 bis 4 Std. später"), ("ge4", "4 Std. oder mehr später"), ("unknown", "Weiß ich nicht")],
      accepted="Haben Sie den Ersatzflug angenommen?", ac=[("yes", "Ja"), ("no", "Nein, ich habe die Erstattung verlangt")],
      denied="Haben Sie Ihren Platz abgegeben?", dn=[("invol", "Nein, die Beförderung wurde verweigert"), ("vol", "Ja, freiwillig"), ("unknown", "Unklar")],
      checkin="Waren Sie rechtzeitig beim Check-in und am Gate?", ci=[("yes", "Ja"), ("no", "Nein"), ("unknown", "Weiß ich nicht")],
      dreason="Grund der Nichtbeförderung", dr=[("overbooking", "Überbuchung oder anderer Grund der Fluggesellschaft"), ("reasonable", "Gesundheit, Sicherheit oder Dokumente"), ("unknown", "Nicht erklärt")],
      cause="Von der Fluggesellschaft genannter Grund", c=[("unknown", "Kein Grund genannt"), ("tech", "Technischer Defekt"), ("crew", "Fehlende oder erkrankte Besatzung"),
        ("strike_own", "Streik des Personals der Fluggesellschaft"), ("strike_ext", "Streik der Fluglotsen oder des Flughafens"), ("strike_sub", "Streik eines für die Fluggesellschaft tätigen Unternehmens (Bodenabfertigung, Catering…)"), ("atc", "Beschränkung der Flugsicherung (ATC)"),
        ("weather", "Schlechtes Wetter"), ("security", "Sicherheit (Bedrohung, Luftraumsperrung)"), ("bird", "Vogelschlag oder Gegenstand auf der Piste"),
        ("knock", "Verspätung des vorherigen Flugs desselben Flugzeugs")],
      empty="Wählen Sie Abflug und Ziel, um das Ergebnis zu sehen.", error="Die Flughafenliste konnte nicht geladen werden. Prüfen Sie Ihre Verbindung und versuchen Sie es erneut.", retry="Erneut versuchen",
      example="Bearbeitbares Beispiel", per="pro Fluggast", cta="Mit AirHelp geltend machen", cta_small="AirHelp ist ein externer Dienst zur Durchsetzung von Fluggastrechten: keine Vorabkosten; bei Erfolg behält er einen Anteil ein (bis zu 50 %, wenn ein Gerichtsverfahren nötig ist). Kein garantiertes Ergebnis. Affiliate-Link: VuelosClaim erhält eine Provision, ohne Kosten für Sie.", cta_generic="Mit einem Dienstleister geltend machen", cta_small_generic="Externer Dienst: behält bei Erfolg eine Provision ein und kann das Ergebnis nicht garantieren. Affiliate-Link.",
      cmp="Mit der kostenlosen Selbstdurchsetzung vergleichen",
      self="Lieber selbst kostenlos: Anspruchsschreiben erstellen", l_lead="Geben Sie Ihre Daten ein, und wir bereiten das Schreiben vor. Es entsteht in Ihrem Browser: Wir senden und speichern es nicht. Bankdaten sind nicht nötig.",
      l_name="Vor- und Nachname", l_book="Buchungscode", l_flight="Flugnummer", l_date="Flugdatum", l_pax="Fluggäste in der Buchung",
      l_text="Ihr Schreiben", copy="Schreiben kopieren", dl=".txt herunterladen",
      steps=["Senden Sie es über das Beschwerdeformular auf der Website der Fluggesellschaft oder per E-Mail und fügen Sie die Bordkarte bei.", "Bewahren Sie einen Nachweis über den Versand auf.",
             f'Zahlt die Fluggesellschaft nicht innerhalb eines Monats oder lehnt sie ab: bei Flügen ab Deutschland kostenlos an die <a href="{EVZ_ADR_URL}" rel="noopener" target="_blank">Schlichtungsstelle (söp oder Bundesamt für Justiz)</a> wenden; bei Flügen ab Spanien an <a href="{aesa_url}" rel="noopener" target="_blank">AESA</a>.'],
      eyebrow="Verordnung (EG) 261/2004",
      facts=[("250 €", "Flüge bis 1.500 km"), ("400 €", "1.500 bis 3.500 km, oder über 1.500 km in der EU"), ("600 €", "über 3.500 km")],
      skip="Zum Inhalt springen",
     ),
    }


FAQ = {
 "it": [
  ("La compensazione è a persona o a prenotazione?", "A passeggero. Se viaggiavate in quattro su un volo fino a 1.500 km arrivato con più di 3 ore di ritardo, sono 4 × 250 € = 1.000 €."),
  ("Il ritardo si conta alla partenza o all'arrivo?", "All'arrivo: quando si apre almeno una porta dell'aereo alla destinazione finale."),
  ("Ho diritto anche se il biglietto era economico?", "Sì. L'importo dipende dalla distanza, non dal prezzo del biglietto."),
  ("Entro quanto tempo posso reclamare?", "Il regolamento non fissa un termine: si applica quello del paese in cui si agisce in giudizio, e in Italia i tribunali non applicano tutti lo stesso. Per sicurezza reclama il prima possibile: è anche più facile ottenere le prove."),
  ("E se avevo uno scalo?", "Se era un'unica prenotazione, conta il ritardo con cui sei arrivato alla destinazione finale e la distanza in linea retta tra partenza e destinazione finale, non la somma delle tratte (Corte di giustizia dell'UE, causa C-559/16)."),
 ],
 "de": [
  ("Gilt die Entschädigung pro Person oder pro Buchung?", "Pro Fluggast. Waren Sie zu viert auf einem Flug bis 1.500 km, der mit mehr als 3 Stunden Verspätung ankam, sind es 4 × 250 € = 1.000 €."),
  ("Zählt die Verspätung beim Abflug oder bei der Ankunft?", "Bei der Ankunft: wenn sich am Endziel mindestens eine Flugzeugtür öffnet."),
  ("Habe ich auch bei einem günstigen Ticket Anspruch?", "Ja. Der Betrag hängt von der Entfernung ab, nicht vom Ticketpreis."),
  ("Wie lange habe ich Zeit?", "Die Verordnung nennt keine Frist; es gilt die Verjährung des Landes, in dem geklagt wird. In Deutschland sind es 3 Jahre ab Ende des Jahres, in dem der Flug stattfand. Je früher Sie den Anspruch geltend machen, desto leichter sind Belege zu bekommen."),
  ("Und wenn ich umgestiegen bin?", "Bei einer einzigen Buchung zählt die Verspätung am Endziel und die Luftlinie zwischen Abflugort und Endziel, nicht die Summe der Teilstrecken (Gerichtshof der EU, Rechtssache C-559/16)."),
 ],
}

WHY = {
    "it": ("Perché usare VuelosClaim", [
        ("eur", "Davvero gratis", "Il calcolatore e la lettera non costano nulla. Ci finanziano la pubblicità e un link di affiliazione, sempre segnalato."),
        ("law", "Con la legge alla mano", "Ogni risultato cita l'articolo del regolamento o la sentenza della Corte di giustizia dell'UE che lo sostiene."),
        ("lock", "Nessun dato per calcolare", "Non chiediamo nome, e-mail o codice di prenotazione per dirti quanto ti spetta."),
        ("way", "Scegli tu la strada", "Reclama da solo con la lettera e tieni il 100 %, oppure affidati a un servizio che si fa pagare solo se vince.")]),
    "de": ("Warum VuelosClaim", [
        ("eur", "Wirklich kostenlos", "Rechner und Anspruchsschreiben kosten nichts. Wir finanzieren uns über Werbung und einen stets gekennzeichneten Affiliate-Link."),
        ("law", "Mit dem Gesetz in der Hand", "Jedes Ergebnis nennt den Artikel der Verordnung oder das Urteil des Gerichtshofs der EU, auf dem es beruht."),
        ("lock", "Keine Daten zum Berechnen", "Wir fragen weder Name noch E-Mail noch Buchungscode, um Ihnen zu sagen, was Ihnen zusteht."),
        ("way", "Sie entscheiden", "Machen Sie den Anspruch mit dem Schreiben selbst geltend und behalten Sie 100 %, oder beauftragen Sie einen Dienst, der nur im Erfolgsfall kassiert.")]),
}

HOME_TEXT = {
    "it": ("Volo in ritardo o cancellato: calcola il rimborso fino a 600 €",
           "Calcolatore gratuito per voli in ritardo, cancellati o in overbooking: 250, 400 o 600 € a passeggero secondo il Regolamento (CE) 261/2004. Con lettera di reclamo.",
           "Volo in ritardo o cancellato? Calcola quanto ti spetta",
           "Se sei arrivato con 3 ore o più di ritardo, il volo è stato cancellato o non ti hanno fatto imbarcare, la compagnia può doverti fino a 600 € a passeggero. Inserisci i dati del volo e lo calcoliamo in pochi secondi.",
           ("FCO", "BCN")),
    "de": ("Flug verspätet oder annulliert: bis 600 € Entschädigung",
           "Kostenloser Rechner für verspätete, annullierte oder überbuchte Flüge: 250, 400 oder 600 € pro Fluggast nach der Verordnung (EG) 261/2004. Mit Anspruchsschreiben.",
           "Flug verspätet oder annulliert? Berechnen Sie Ihre Entschädigung",
           "Sind Sie mit 3 Stunden oder mehr Verspätung angekommen, wurde Ihr Flug annulliert oder wurden Sie nicht befördert, schuldet Ihnen die Fluggesellschaft womöglich bis zu 600 € pro Fluggast. Geben Sie Ihren Flug ein, und wir berechnen es in Sekunden.",
           ("FRA", "PMI")),
}


def reference(l, faq_html, e):
    if l == "it":
        return f"""<section class="ref" id="cuanto"><div class="wrap">
<h2>Quanto ti spetta in base alla distanza</h2>
<p class="lead">È un importo fisso a passeggero e non dipende da quanto hai pagato il biglietto. Fonte: <a href="{EU_URL['it']}" rel="noopener">La tua Europa, Commissione europea</a>.</p>
<div class="board"><table><thead><tr><th>Distanza del volo</th><th>Compensazione</th></tr></thead><tbody>
<tr><td>Fino a 1.500 km (Roma–Parigi, Milano–Barcellona)</td><td class="eur">250 €</td></tr>
<tr><td>Oltre 1.500 km nell'UE, o da 1.500 a 3.500 km</td><td class="eur">400 €</td></tr>
<tr><td>Oltre 3.500 km fuori dall'UE (Roma–New York)</td><td class="eur">600 €</td></tr>
<tr><td>Oltre 3.500 km fuori dall'UE con 3–4 ore di ritardo</td><td class="eur">300 €</td></tr>
</tbody></table></div></div></section>
<section class="ref"><div class="wrap two">
<div><h3>Quando ti pagano</h3><ul>
<li>Arrivi alla destinazione finale con 3 ore o più di ritardo.</li><li>Il volo viene cancellato con meno di 14 giorni di preavviso.</li><li>Non ti fanno imbarcare per overbooking.</li>
<li>Il volo parte da un aeroporto dell'UE, dell'Islanda, della Norvegia o della Svizzera, oppure vi arriva con una compagnia europea.</li></ul></div>
<div><h3>Quando non ti pagano</h3><ul>
<li>Circostanze eccezionali che la compagnia può dimostrare: maltempo, sciopero dei controllori di volo o rischi per la sicurezza.</li>
<li>Ti hanno avvisato della cancellazione con 14 giorni o più di anticipo.</li><li>Il ritardo all'arrivo è stato inferiore a 3 ore.</li>
<li>I guasti tecnici e gli scioperi del personale della compagnia non la esonerano dal pagare.</li></ul></div>
</div></section>
<section class="ref"><div class="wrap"><h2>Come reclamare</h2><ol class="steps">
<li>Conserva la carta d'imbarco, la prenotazione e, se puoi, una foto del tabellone con il ritardo.</li>
<li>Reclama prima per iscritto alla compagnia, tramite il suo modulo reclami.</li>
<li>Se non risponde entro un mese o rifiuta, e il volo è partito dall'Italia, presenta reclamo gratuito all'<a href="{ENAC_URL}" rel="noopener">ENAC</a>.</li>
<li>Se preferisci non farlo da solo, una società di reclami se ne occupa senza costi anticipati e trattiene una percentuale se vince.</li>
</ol>
<p>Scioperi in programma in Italia, Spagna e Portogallo: <a href="{STRIKES['it']}">calendario degli scioperi aerei</a>.</p></div></section>
<section class="ref" id="preguntas"><div class="wrap"><h2>Domande frequenti</h2>{faq_html}</div></section>"""
    return f"""<section class="ref" id="cuanto"><div class="wrap">
<h2>Wie viel Ihnen je nach Entfernung zusteht</h2>
<p class="lead">Ein fester Betrag pro Fluggast, unabhängig vom Ticketpreis. Quelle: <a href="{EU_URL['de']}" rel="noopener">Ihr Europa, Europäische Kommission</a>.</p>
<div class="board"><table><thead><tr><th>Flugentfernung</th><th>Entschädigung</th></tr></thead><tbody>
<tr><td>Bis 1.500 km (Frankfurt–Paris, München–Rom)</td><td class="eur">250 €</td></tr>
<tr><td>Über 1.500 km innerhalb der EU, oder 1.500 bis 3.500 km</td><td class="eur">400 €</td></tr>
<tr><td>Über 3.500 km außerhalb der EU (Frankfurt–New York)</td><td class="eur">600 €</td></tr>
<tr><td>Über 3.500 km außerhalb der EU mit 3–4 Stunden Verspätung</td><td class="eur">300 €</td></tr>
</tbody></table></div></div></section>
<section class="ref"><div class="wrap two">
<div><h3>Wann Sie Geld bekommen</h3><ul>
<li>Sie kommen mit 3 Stunden oder mehr Verspätung am Endziel an.</li><li>Ihr Flug wird weniger als 14 Tage vorher annulliert.</li><li>Ihnen wird wegen Überbuchung die Beförderung verweigert.</li>
<li>Der Flug startet in der EU, in Island, Norwegen oder der Schweiz, oder er landet dort mit einer europäischen Fluggesellschaft.</li></ul></div>
<div><h3>Wann nicht</h3><ul>
<li>Außergewöhnliche Umstände, die die Fluggesellschaft nachweisen kann: Unwetter, Fluglotsenstreik oder Sicherheitsrisiken.</li>
<li>Die Annullierung wurde Ihnen 14 Tage oder früher mitgeteilt.</li><li>Die Ankunftsverspätung lag unter 3 Stunden.</li>
<li>Technische Defekte und Streiks des eigenen Personals befreien die Fluggesellschaft nicht von der Zahlung.</li></ul></div>
</div></section>
<section class="ref"><div class="wrap"><h2>So machen Sie Ihren Anspruch geltend</h2><ol class="steps">
<li>Bewahren Sie Bordkarte, Buchungsbestätigung und möglichst ein Foto der Anzeigetafel mit der Verspätung auf.</li>
<li>Wenden Sie sich zuerst schriftlich über das Beschwerdeformular an die Fluggesellschaft.</li>
<li>Antwortet sie nicht innerhalb eines Monats oder lehnt sie ab, können Sie sich bei Flügen ab Deutschland kostenlos an eine <a href="{EVZ_ADR_URL}" rel="noopener">Schlichtungsstelle (söp oder Bundesamt für Justiz)</a> wenden.</li>
<li>Wenn Sie es nicht selbst machen möchten, übernimmt ein Fluggastrechte-Dienstleister das ohne Vorabkosten und behält bei Erfolg einen Anteil ein.</li>
</ol>
<p>Geplante Streiks in Italien, Spanien und Portugal: <a href="{STRIKES['de']}">Streikkalender für Flüge</a>.</p></div></section>
<section class="ref" id="preguntas"><div class="wrap"><h2>Häufige Fragen</h2>{faq_html}</div></section>"""


CONSENT_TXT = {
    "it": ("Avviso sui cookie", "Maggiori informazioni", "Con il tuo permesso usiamo i cookie per contare le visite e sapere quali parti del calcolatore vengono usate, compresi i clic sul servizio di reclamo. Non inviamo mai ciò che scrivi nel calcolatore o nella lettera.", "Accetta", "Rifiuta"),
    "de": ("Cookie-Hinweis", "Mehr erfahren", "Mit Ihrer Erlaubnis verwenden wir Cookies, um Besuche zu zählen und zu sehen, welche Teile des Rechners genutzt werden, einschließlich Klicks auf den Durchsetzungsdienst. Was Sie in den Rechner oder das Schreiben eingeben, senden wir nie.", "Akzeptieren", "Ablehnen"),
}
