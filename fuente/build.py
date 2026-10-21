#!/usr/bin/env python3
"""Genera la web estática bilingüe (ES en /, EN en /en/) en ../docs y una vista previa local en ./preview.

Cambia aquí el dominio y el enlace de afiliado cuando los tengas:
  SITE_URL=https://vuelosclaim.eu AFF_URL=https://... python3 build.py
"""
import html, json, math, os, re, shutil, unicodedata
import uk_deep
import uk_airports
import strikes
import compare
import guides

SITE_URL = os.environ.get("SITE_URL", "https://vuelosclaim.eu")
AFF_URL = os.environ.get("AFF_URL", "https://airhelp.tpx.gr/Ow8vczQM")  # Travelpayouts AirHelp; backup Compensair: https://compensair.tpx.gr/Ev5bFUPY
BRAND = "VuelosClaim"
AESA_URL = "https://www.seguridadaerea.gob.es/es/ambitos/derechos-de-los-pasajeros"
CAA_URL = "https://www.caa.co.uk/air-passengers/travel-problems-and-rights/flight-delays-and-cancellations/"
EU_URL = {"es": "https://europa.eu/youreurope/citizens/travel/passenger-rights/air/index_es.htm",
          "en": "https://europa.eu/youreurope/citizens/travel/passenger-rights/air/index_en.htm"}
UPDATED = {"es": "7 de octubre de 2026", "en": "7 October 2026"}

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
# La web se genera en docs/ (carpeta que publica GitHub Pages). BUILD_OUT permite generarla en otro sitio (pruebas).
SRC = os.path.join(ROOT, "src")
OUT = os.environ.get("BUILD_OUT", os.path.join(REPO, "docs"))
PREV = os.path.join(ROOT, "preview")
CSS = open(os.path.join(SRC, "style.css"), encoding="utf-8").read()
JS = open(os.path.join(SRC, "app.js"), encoding="utf-8").read()
AIRLINES = json.load(open(os.path.join(ROOT, "data", "airlines.json"), encoding="utf-8"))
AIRPORTS = {a[0]: a for a in json.load(open(os.path.join(ROOT, "data", "airports.min.json"), encoding="utf-8"))}
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800'
         '&family=IBM+Plex+Mono:wght@500;600;700&family=Public+Sans:wght@400;500;700&display=swap">')
ICON = ('<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="192x192" href="/img/icon-192.png">'
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest"><meta name="theme-color" content="#13213c">')
OGIMG = ('<meta property="og:image" content="https://vuelosclaim.eu/img/og-image.png"><meta property="og:image:width" content="1200">'
         '<meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:site" content="@vuelosclaim">')
ORG_LD = ('<script type="application/ld+json">' + __import__("json").dumps([
    {"@context": "https://schema.org", "@type": "Organization", "@id": "https://vuelosclaim.eu/#org", "name": "VuelosClaim",
     "url": "https://vuelosclaim.eu/", "logo": {"@type": "ImageObject", "url": "https://vuelosclaim.eu/img/vuelosclaim-logo.png", "width": 400, "height": 400},
     "email": "vuelosclaim@gmail.com", "sameAs": ["https://x.com/vuelosclaim", "https://www.facebook.com/profile.php?id=61595233574765"]},
    {"@context": "https://schema.org", "@type": "WebSite", "@id": "https://vuelosclaim.eu/#website", "name": "VuelosClaim", "url": "https://vuelosclaim.eu/",
     "publisher": {"@id": "https://vuelosclaim.eu/#org"}, "inLanguage": ["es", "en"]}]) + '</script>')
e = html.escape


def slugify(s):
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


# ---------------------------------------------------------------- data
ES_AIRPORTS = [  # code, ES slug, ES name, EN name
    ("MAD", "madrid-barajas", "Madrid-Barajas", "Madrid-Barajas"), ("BCN", "barcelona-el-prat", "Barcelona-El Prat", "Barcelona-El Prat"),
    ("PMI", "palma-de-mallorca", "Palma de Mallorca", "Palma de Mallorca"), ("AGP", "malaga", "Málaga-Costa del Sol", "Malaga"),
    ("ALC", "alicante-elche", "Alicante-Elche", "Alicante"), ("LPA", "gran-canaria", "Gran Canaria", "Gran Canaria"),
    ("TFS", "tenerife-sur", "Tenerife Sur", "Tenerife South"), ("TFN", "tenerife-norte", "Tenerife Norte", "Tenerife North"),
    ("VLC", "valencia", "Valencia", "Valencia"), ("IBZ", "ibiza", "Ibiza", "Ibiza"), ("SVQ", "sevilla", "Sevilla", "Seville"),
    ("BIO", "bilbao", "Bilbao", "Bilbao"), ("ACE", "lanzarote", "Lanzarote", "Lanzarote"), ("FUE", "fuerteventura", "Fuerteventura", "Fuerteventura"),
    ("MAH", "menorca", "Menorca", "Menorca"), ("SCQ", "santiago-de-compostela", "Santiago de Compostela", "Santiago de Compostela"),
    ("GRO", "girona", "Girona", "Girona"), ("OVD", "asturias", "Asturias", "Asturias"), ("VGO", "vigo", "Vigo", "Vigo"),
    ("SDR", "santander", "Santander", "Santander"), ("XRY", "jerez", "Jerez", "Jerez"), ("GRX", "granada", "Granada", "Granada"),
    ("LEI", "almeria", "Almería", "Almeria"), ("RMU", "murcia", "Región de Murcia", "Murcia"), ("REU", "reus", "Reus", "Reus"),
    ("ZAZ", "zaragoza", "Zaragoza", "Zaragoza"), ("SPC", "la-palma", "La Palma", "La Palma"),
]
CANARY = {"LPA", "TFS", "TFN", "ACE", "FUE", "SPC"}
EXAMPLES = {
    "es": {"iberia": ("MAD", "JFK"), "air-europa": ("MAD", "MIA"), "binter": ("LPA", "MAD"), "air-nostrum": ("VLC", "SVQ"),
           "british-airways": ("MAD", "LHR"), "jet2": ("ALC", "MAN"), "emirates": ("MAD", "DXB"), "turkish-airlines": ("BCN", "IST"),
           "tap": ("MAD", "LIS"), "ryanair": ("VLC", "BGY"), "vueling": ("BCN", "AMS"), "easyjet": ("BCN", "GVA"), "tui": ("PMI", "BHX"),
           "wizz-air": ("BCN", "BUD"), "norwegian": ("AGP", "OSL"), "lufthansa": ("MAD", "FRA"), "air-france": ("MAD", "CDG"),
           "klm": ("BCN", "AMS"), "transavia": ("ALC", "ORY"), "volotea": ("BIO", "VCE"), "ita-airways": ("MAD", "FCO"),
           "iberia-express": ("MAD", "TFN")},
    "en": {"jet2": ("MAN", "ALC"), "easyjet": ("LGW", "AGP"), "tui": ("BHX", "PMI"), "british-airways": ("LHR", "MAD"),
           "ryanair": ("STN", "AGP"), "vueling": ("LGW", "BCN"), "wizz-air": ("LTN", "ALC"), "iberia": ("LHR", "MAD"),
           "iberia-express": ("MAD", "TFN"), "air-europa": ("MAD", "MIA"), "binter": ("LPA", "MAD"), "norwegian": ("AGP", "OSL")},
}
NAMES = {
    "es": {"LHR": "Londres-Heathrow", "LGW": "Londres-Gatwick", "MAN": "Mánchester", "BHX": "Birmingham", "EDI": "Edimburgo",
           "CDG": "París-Charles de Gaulle", "AMS": "Ámsterdam", "FCO": "Roma-Fiumicino", "BER": "Berlín", "LIS": "Lisboa",
           "DUB": "Dublín", "ZRH": "Zúrich", "ATH": "Atenas", "IST": "Estambul", "JFK": "Nueva York-JFK", "MIA": "Miami",
           "CUN": "Cancún", "BOG": "Bogotá", "EZE": "Buenos Aires", "MAD": "Madrid", "BCN": "Barcelona", "PMI": "Palma de Mallorca",
           "LPA": "Gran Canaria", "CMN": "Casablanca", "DXB": "Dubái"},
    "en": {"LHR": "London Heathrow", "LGW": "London Gatwick", "STN": "London Stansted", "MAN": "Manchester", "BHX": "Birmingham",
           "BRS": "Bristol", "EDI": "Edinburgh", "GLA": "Glasgow", "NCL": "Newcastle", "LBA": "Leeds Bradford", "EMA": "East Midlands",
           "BFS": "Belfast", "DUB": "Dublin", "CDG": "Paris CDG", "AMS": "Amsterdam", "BER": "Berlin", "JFK": "New York JFK",
           "MAD": "Madrid", "BCN": "Barcelona", "PMI": "Palma de Mallorca", "LPA": "Gran Canaria", "DXB": "Dubai"},
}
for _c, _s, _es, _en in ES_AIRPORTS:
    NAMES["es"].setdefault(_c, _es); NAMES["en"].setdefault(_c, _en)
for _c, _es, _en in [("DUS", "Düsseldorf", "Düsseldorf"), ("CGN", "Colonia", "Cologne"), ("HAM", "Hamburgo", "Hamburg"), ("FRA", "Fráncfort", "Frankfurt"),
                     ("MUC", "Múnich", "Munich"), ("CPH", "Copenhague", "Copenhagen"), ("OSL", "Oslo", "Oslo"), ("ARN", "Estocolmo", "Stockholm"),
                     ("BRU", "Bruselas", "Brussels"), ("PDL", "Ponta Delgada (Azores)", "Ponta Delgada (Azores)"), ("OPO", "Oporto", "Porto"),
                     ("PUJ", "Punta Cana", "Punta Cana"), ("HAV", "La Habana", "Havana"), ("CCS", "Caracas", "Caracas"), ("ZRH", "Zúrich", "Zurich"),
                     ("ATH", "Atenas", "Athens"), ("LIS", "Lisboa", "Lisbon"), ("CUN", "Cancún", "Cancun"), ("VIE", "Viena", "Vienna"), ("WAW", "Varsovia", "Warsaw"), ("HEL", "Helsinki", "Helsinki"), ("RIX", "Riga", "Riga"), ("KEF", "Reikiavik", "Reykjavik"), ("SAW", "Estambul-Sabiha Gökçen", "Istanbul Sabiha Gökçen"), ("LAX", "Los Ángeles", "Los Angeles"), ("MCO", "Orlando", "Orlando"), ("BOS", "Boston", "Boston"), ("SYY", "Stornoway", "Stornoway"), ("KOI", "Kirkwall", "Kirkwall"), ("GLA", "Glasgow", "Glasgow"), ("EDI", "Edimburgo", "Edinburgh")]:
    NAMES["es"].setdefault(_c, _es); NAMES["en"].setdefault(_c, _en)
DESTS = {
    "es": ["MAD", "BCN", "PMI", "LPA", "LIS", "LHR", "CDG", "AMS", "FCO", "BER", "DUB", "ZRH", "ATH", "IST", "CMN", "DXB", "JFK", "MIA", "CUN", "BOG", "EZE"],
    "en": ["LHR", "LGW", "STN", "MAN", "BHX", "BRS", "EMA", "LBA", "NCL", "EDI", "GLA", "BFS", "DUB", "MAD", "BCN", "PMI", "AMS", "BER", "CDG", "DXB", "JFK"],
}
UKC = {"GB", "GG", "JE", "IM"}

# ---------------------------------------------------------------- URLs
def u_home(l): return "/" if l == "es" else "/en/"
def u_airline(l, a): return f"/compensacion-retraso-{a['slug']}/" if l == "es" else f"/en/{a['slug']}-delay-compensation/"
def u_airport(l, ap): return f"/retraso-vuelo-aeropuerto-{ap[1]}/" if l == "es" else f"/en/{slugify(ap[3])}-airport-flight-delay/"
LEGAL = {"about": {"es": "/quienes-somos/", "en": "/en/about/"}, "legal": {"es": "/aviso-legal/", "en": "/en/legal-notice/"},
         "privacy": {"es": "/privacidad/", "en": "/en/privacy/"}}

# ---------------------------------------------------------------- strings
S = {
 "es": dict(
  locale="es_ES", nav="Principal", nav_amounts="Importes", nav_airlines="Aerolíneas", nav_faq="Preguntas", switch="EN", switch_label="English",
  foot1=f'{BRAND} es una calculadora orientativa basada en el <a href="{EU_URL["es"]}" rel="noopener">Reglamento (CE) 261/2004</a>. No es asesoramiento legal ni sustituye a un abogado.',
  foot2="Algunos enlaces son de afiliado: si contratas un servicio a través de ellos, recibimos una comisión sin coste para ti. Eso no cambia el resultado de la calculadora.",
  foot3="Última revisión de importes y normas: {d}.", f_embed="Pon la calculadora en tu web", f_about="Quiénes somos y fuentes", f_legal="Aviso legal", f_privacy="Privacidad",
  calc_h="Calcula tu compensación", from_="Origen", to="Destino final", ph="Ciudad o código", airline="Aerolínea",
  al_unknown="No lo sé / no aparece", al_eu="Otra aerolínea europea", al_noneu="Otra aerolínea no europea",
  what="Qué pasó", w=[("delay", "Retraso"), ("cancel", "Cancelación"), ("denied", "Overbooking")],
  delay="Retraso al llegar al destino", d=[("lt3", "Menos de 3 h"), ("3to4", "De 3 a 4 h"), ("gt4", "Más de 4 h")],
  notice="Te avisaron con", n=[("lt7", "Menos de 7 días"), ("7to14", "7 a 14 días"), ("gt14", "Más de 14 días")],
  cause="Motivo que te dieron", c=[("unknown", "No me lo dijeron"), ("tech", "Problema técnico"), ("strike", "Huelga de la aerolínea"), ("extra", "Tiempo, controladores o seguridad")],
  empty="Elige origen y destino para ver el resultado.", error="No se ha podido cargar la lista de aeropuertos. Recarga la página.",
  example="Ejemplo editable", per="por pasajero", cta="Reclámalo sin coste por adelantado", cta_small="Lo gestiona una empresa de reclamaciones y solo cobra si ganas.",
  self="Prefiero reclamar yo gratis: generar mi carta", l_lead="Rellena tus datos y te preparamos la carta. Todo se queda en tu navegador: no guardamos nada.",
  l_name="Nombre y apellidos", l_book="Código de reserva", l_flight="Número de vuelo", l_date="Fecha del vuelo", l_pax="Pasajeros en la reserva",
  l_iban="IBAN para el pago (opcional)", l_text="Tu carta", copy="Copiar carta", dl="Descargar .txt",
  steps=["Envíala por el formulario de reclamaciones de la web de tu aerolínea o por correo, con la tarjeta de embarque adjunta.", "Guarda el justificante de envío.",
         f'Si en un mes no te pagan o te lo rechazan, reclama gratis ante <a href="{AESA_URL}" rel="noopener" target="_blank">AESA</a> (vuelos que salen de España).'],
  eyebrow="Reglamento CE 261/2004",
  facts=[("250 €", "vuelos de hasta 1.500 km"), ("400 €", "de 1.500 a 3.500 km, o más de 1.500 km dentro de la UE"), ("600 €", "más de 3.500 km")],
 ),
 "en": dict(
  locale="en_GB", nav="Main", nav_amounts="Amounts", nav_airlines="Airlines", nav_faq="FAQ", switch="ES", switch_label="Español",
  foot1=f'{BRAND} is an indicative calculator based on <a href="{EU_URL["en"]}" rel="noopener">Regulation (EC) 261/2004</a> and its UK version (UK261). It is not legal advice.',
  foot2="Some links are affiliate links: if you use a service through them, we earn a commission at no cost to you. This never changes the calculator's result.",
  foot3="Amounts and rules last reviewed: {d}.", f_embed="", f_about="About us and sources", f_legal="Legal notice", f_privacy="Privacy",
  calc_h="Check your compensation", from_="From", to="Final destination", ph="City or airport code", airline="Airline",
  al_unknown="Not sure / not listed", al_eu="Another European airline", al_noneu="Another non-European airline",
  what="What happened", w=[("delay", "Delay"), ("cancel", "Cancellation"), ("denied", "Overbooking")],
  delay="Delay on arrival", d=[("lt3", "Under 3 h"), ("3to4", "3 to 4 h"), ("gt4", "Over 4 h")],
  notice="You were told", n=[("lt7", "Under 7 days ahead"), ("7to14", "7 to 14 days ahead"), ("gt14", "Over 14 days ahead")],
  cause="Reason given", c=[("unknown", "None given"), ("tech", "Technical problem"), ("strike", "Airline staff strike"), ("extra", "Weather, ATC or security")],
  empty="Choose where you flew from and to.", error="The airport list could not load. Please refresh the page.",
  example="Editable example", per="per passenger", cta="Claim it with no upfront cost", cta_small="Handled by a flight claims company that only charges if you win.",
  self="I'd rather claim myself for free: write my letter", l_lead="Fill in your details and we'll prepare the letter. Everything stays in your browser: we store nothing.",
  l_name="Full name", l_book="Booking reference", l_flight="Flight number", l_date="Flight date", l_pax="Passengers on the booking",
  l_iban="IBAN or bank details (optional)", l_text="Your letter", copy="Copy letter", dl="Download .txt",
  steps=["Send it through your airline's online claim form or by email, attaching your boarding pass.", "Keep proof that you sent it.",
         f'If the airline refuses or does not pay within a month: for flights from Spain, complain for free to <a href="{AESA_URL}" rel="noopener" target="_blank">AESA</a>; for flights from the UK, use the airline\'s ADR scheme or the <a href="{CAA_URL}" rel="noopener" target="_blank">CAA</a>.'],
  eyebrow="EU261 and UK261",
  facts=[("€250 / £220", "flights up to 1,500 km"), ("€400 / £350", "1,500 to 3,500 km, or over 1,500 km within the EU"), ("€600 / £520", "over 3,500 km")],
 ),
}

FAQ = {
 "es": [
  ("¿La compensación es por persona o por reserva?", "Por pasajero. Si viajabais cuatro en un vuelo de hasta 1.500 km con más de 3 horas de retraso, son 4 × 250 € = 1.000 €."),
  ("¿El retraso se cuenta en la salida o en la llegada?", "En la llegada: cuando se abre al menos una puerta del avión en el destino final."),
  ("¿Tengo derecho aunque el billete fuera barato?", "Sí. El importe depende de la distancia, no del precio del billete."),
  ("¿Cuánto tiempo tengo para reclamar?", "En España, los tribunales aplican en general un plazo de 5 años desde el vuelo. Cuanto antes reclames, más fácil es conseguir las pruebas."),
  ("¿Y si tenía una escala?", "Si era una única reserva, cuenta el retraso con el que llegaste al destino final y la distancia total entre origen y destino."),
 ],
 "en": [
  ("Is compensation per person or per booking?", "Per passenger. If four of you were on a flight of up to 1,500 km that arrived over 3 hours late under EU261, that is 4 × €250 = €1,000."),
  ("Which rules apply to my flight between Spain and the UK?", "Flights departing Spain are covered by EU261 and paid in euros, whatever the airline. Flights departing the UK are covered by UK261 and paid in pounds, whatever the airline."),
  ("Is the delay measured on departure or arrival?", "On arrival: when at least one aircraft door opens at your final destination."),
  ("Do cheap tickets count?", "Yes. The amount depends on flight distance, not on what you paid."),
  ("How long do I have to claim?", "It depends on the country whose courts hear the claim: in Spain it is generally 5 years, and in England and Wales 6 years. Claiming early makes evidence easier to get."),
 ],
}


# ---------------------------------------------------------------- building blocks
def head(l, title, desc, path, alts=None):
    canon = SITE_URL + path
    hl = ""
    if alts:
        hl = "".join(f'<link rel="alternate" hreflang="{k}" href="{SITE_URL}{v}">' for k, v in alts.items())
        hl += f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}{alts.get("es", path)}">'
    return (f"<title>{e(title)}</title>\n<meta name=\"description\" content=\"{e(desc)}\">\n<link rel=\"canonical\" href=\"{canon}\">{hl}\n"
            f"<meta property=\"og:title\" content=\"{e(title)}\"><meta property=\"og:description\" content=\"{e(desc)}\"><meta property=\"og:type\" content=\"website\">"
            f"<meta property=\"og:url\" content=\"{canon}\"><meta property=\"og:locale\" content=\"{S[l]['locale']}\">\n{OGIMG}\n{ICON}\n{ORG_LD if path in ('/', '/en/') else ''}\n{FONTS}\n<style>{CSS}</style>")


def header(l, alt_path):
    s, h = S[l], u_home(l)
    sw = f'<a class="lang" href="{alt_path}" hreflang="{"en" if l == "es" else "es"}" aria-label="{s["switch_label"]}">{s["switch"]}</a>' if alt_path else ""
    return (f'<header class="top"><div class="wrap"><a class="brand" href="{h}"><span class="brand-mark" aria-hidden="true">€</span>{BRAND}</a>'
            f'<nav aria-label="{s["nav"]}"><a href="{h}#cuanto">{s["nav_amounts"]}</a><a href="{h}#aerolineas">{s["nav_airlines"]}</a><a href="{h}#preguntas">{s["nav_faq"]}</a>{sw}</nav></div></header>')


def footer(l):
    s = S[l]
    links = []
    if l == "es":
        links.append('<a href="/huelgas-vuelos-espana/">Huelgas de vuelos</a>'); links.append('<a href="/comparativa-empresas-reclamacion-vuelos/">AirHelp vs Reclamador</a>'); links.append('<a href="/vuelo-cancelado-que-hacer/">Vuelo cancelado</a>'); links.append('<a href="/overbooking-compensacion/">Overbooking</a>'); links.append('<a href="/circunstancias-extraordinarias-vuelo/">Circunstancias extraordinarias</a>')
        links.append(f'<a href="/insertar-calculadora/">{s["f_embed"]}</a>')
    else:
        links.append('<a href="/en/flight-strikes-spain-europe/">Flight strikes</a>'); links.append('<a href="/en/flight-compensation-companies-compared/">AirHelp vs Flightright</a>'); links.append('<a href="/en/flight-cancelled-what-to-do/">Flight cancelled</a>'); links.append('<a href="/en/denied-boarding-overbooking-compensation/">Overbooking</a>'); links.append('<a href="/en/extraordinary-circumstances-flight-delay/">Extraordinary circumstances</a>')
        links.append(f'<a href="{uk_airports.HUB}">UK airports to Spain</a>')
    links += [f'<a href="{LEGAL["about"][l]}">{s["f_about"]}</a>', f'<a href="{LEGAL["legal"][l]}">{s["f_legal"]}</a>', f'<a href="{LEGAL["privacy"][l]}">{s["f_privacy"]}</a>']
    return (f'<footer class="foot"><div class="wrap"><p>{s["foot1"]}</p><p>{s["foot2"]}</p><p>{s["foot3"].format(d=UPDATED[l])}</p>'
            f'<nav>{"".join(links)}</nav></div></footer>')


def chips(name, items, checked):
    return "".join(f'<label><input type="radio" name="{name}" value="{v}"{" checked" if v == checked else ""}><span>{e(t).replace(" h", "&nbsp;h")}</span></label>' for v, t in items)


def calculator(l, airline_slug, dep, arr):
    s = S[l]
    opts = [f'<option value="">{s["al_unknown"]}</option>'] + [
        f'<option value="{a["slug"]}"{" selected" if a["slug"] == airline_slug else ""}>{e(a["name"])}</option>' for a in AIRLINES
    ] + [f'<option value="otra-ue">{s["al_eu"]}</option>', f'<option value="otra-no-ue">{s["al_noneu"]}</option>']
    iban_ph = "ES00 0000 0000 0000 0000 0000" if l == "es" else "GB00 XXXX 0000 0000 0000 00"
    return f"""<form class="calc" id="calc" novalidate>
<h2>{s["calc_h"]}</h2>
<div class="row2">
 <div class="field"><label for="from">{s["from_"]}</label><input type="text" id="from" data-code="{dep}" autocomplete="off" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="from-list" placeholder="{s["ph"]}"><ul class="ac" id="from-list" role="listbox" hidden></ul></div>
 <div class="field"><label for="to">{s["to"]}</label><input type="text" id="to" data-code="{arr}" autocomplete="off" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="to-list" placeholder="{s["ph"]}"><ul class="ac" id="to-list" role="listbox" hidden></ul></div>
</div>
<div class="field"><label for="airline">{s["airline"]}</label><select id="airline" name="airline">{"".join(opts)}</select></div>
<fieldset><legend>{s["what"]}</legend><div class="chips">{chips("what", s["w"], "delay")}</div></fieldset>
<fieldset id="grp-delay"><legend>{s["delay"]}</legend><div class="chips">{chips("delay", s["d"], "gt4")}</div></fieldset>
<fieldset id="grp-notice" hidden><legend>{s["notice"]}</legend><div class="chips">{chips("notice", s["n"], "lt7")}</div></fieldset>
<fieldset><legend>{s["cause"]}</legend><div class="chips">{chips("cause", s["c"], "unknown")}</div></fieldset>
<div class="result" id="result" data-state="empty" aria-live="polite">
 <p class="empty-msg">{s["empty"]}</p>
 <p class="error-msg">{s["error"]}</p>
 <div class="ticket">
  <div class="ticket-main">
   <div class="ticket-meta"><span data-route>—</span><span data-km>—</span><span>{s["example"]}</span></div>
   <p class="ticket-head" data-headline></p>
   <ul class="why" data-lines></ul>
  </div>
  <div class="ticket-stub"><div class="amount" data-amount>—</div><div class="stub-label">{s["per"]}</div></div>
 </div>
 <div class="care" data-care hidden></div>
 <div class="cta" data-cta>
  <a class="btn btn-sign" href="{e(AFF_URL)}" rel="sponsored nofollow noopener" target="_blank">{s["cta"]}</a>
  <small>{s["cta_small"]}</small>
  <button type="button" class="btn btn-ghost" id="letter-open" aria-expanded="false" aria-controls="letter">{s["self"]}</button>
 </div>
 <div class="care" data-where hidden></div>
 <div class="letter" id="letter" hidden>
  <p class="letter-lead">{s["l_lead"]}</p>
  <div class="row2">
   <div class="field"><label for="l-name">{s["l_name"]}</label><input type="text" id="l-name" autocomplete="name"></div>
   <div class="field"><label for="l-booking">{s["l_book"]}</label><input type="text" id="l-booking" autocomplete="off" placeholder="X7K2PQ"></div>
   <div class="field"><label for="l-flight">{s["l_flight"]}</label><input type="text" id="l-flight" autocomplete="off" placeholder="VY1234"></div>
   <div class="field"><label for="l-date">{s["l_date"]}</label><input type="date" id="l-date"></div>
   <div class="field"><label for="l-pax">{s["l_pax"]}</label><input type="number" id="l-pax" min="1" max="9" value="1"></div>
   <div class="field"><label for="l-iban">{s["l_iban"]}</label><input type="text" id="l-iban" autocomplete="off" placeholder="{iban_ph}"></div>
  </div>
  <label class="sr" for="letter-text">{s["l_text"]}</label>
  <textarea id="letter-text" rows="14" readonly></textarea>
  <div class="letter-actions"><button type="button" class="btn btn-sign" id="letter-copy">{s["copy"]}</button><button type="button" class="btn btn-ghost" id="letter-dl">{s["dl"]}</button></div>
  <p class="letter-msg" id="letter-msg" aria-live="polite"></p>
  <ol class="steps small">{"".join(f"<li>{x}</li>" for x in s["steps"])}</ol>
 </div>
</div>
</form>"""


def hero(l, h1, lede, airline_slug, dep, arr):
    s = S[l]
    facts = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in s["facts"])
    return (f'<section class="hero"><div class="wrap hero-grid"><div><span class="eyebrow">{s["eyebrow"]}</span><h1>{h1}</h1>'
            f'<p class="lede">{lede}</p><ul class="facts{" facts-wide" if l == "en" else ""}">{facts}</ul></div>{calculator(l, airline_slug, dep, arr)}</div></section>')


def faq_html(l):
    return "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in FAQ[l])


def faq_jsonld(l):
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ[l]]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"


def reference_sections(l, compact=False):
    full = _reference_sections(l)
    if not compact:
        return full
    full = re.sub(r'<section class="ref"><div class="wrap"><h2>(Cómo reclamar|How to claim)</h2>.*?</section>\n', '', full, flags=re.S)
    more = ('<p style="margin-top:24px"><a href="/#preguntas">Preguntas frecuentes sobre reclamar un vuelo</a></p>' if l == 'es'
            else '<p style="margin-top:24px"><a href="/en/#preguntas">Frequently asked questions about flight compensation</a></p>')
    return re.sub(r'<section class="ref" id="preguntas">.*?</section>', '<section class="ref"><div class="wrap">' + more + '</div></section>', full, flags=re.S)


def _reference_sections(l):
    links = "".join(f'<li><a href="{u_airline(l, a)}">{e(a["name"])}</a></li>' for a in AIRLINES)
    aps = "".join(f'<li><a href="{u_airport(l, ap)}">{e(ap[2] if l == "es" else ap[3])}</a></li>' for ap in ES_AIRPORTS)
    if l == "es":
        return f"""<section class="ref" id="cuanto"><div class="wrap">
<h2>Cuánto te corresponde según la distancia</h2>
<p class="lead">Es una cantidad fija por pasajero, no depende de lo que pagaste por el billete. Fuente: <a href="{EU_URL['es']}" rel="noopener">Tu Europa, Comisión Europea</a>.</p>
<div class="board"><table><thead><tr><th>Distancia del vuelo</th><th>Compensación</th></tr></thead><tbody>
<tr><td>Hasta 1.500 km (Madrid–París, Valencia–Ámsterdam)</td><td class="eur">250 €</td></tr>
<tr><td>Más de 1.500 km dentro de la UE, o de 1.500 a 3.500 km</td><td class="eur">400 €</td></tr>
<tr><td>Más de 3.500 km fuera de la UE (Madrid–Nueva York)</td><td class="eur">600 €</td></tr>
<tr><td>Más de 3.500 km con 3 a 4 horas de retraso</td><td class="eur">300 €</td></tr>
</tbody></table></div></div></section>
<section class="ref"><div class="wrap two">
<div><h3>Cuándo te pagan</h3><ul>
<li>Llegas al destino final con 3 horas o más de retraso.</li><li>Te cancelan el vuelo con menos de 14 días de aviso.</li><li>No te dejan embarcar por overbooking.</li>
<li>El vuelo sale de un aeropuerto de la UE, Islandia, Noruega o Suiza (incluidas Canarias), o llega a uno de ellos con una aerolínea europea.</li></ul></div>
<div><h3>Cuándo no te pagan</h3><ul>
<li>Circunstancias extraordinarias que la aerolínea pueda demostrar: meteorología adversa, huelga de controladores aéreos o riesgos de seguridad.</li>
<li>Te avisaron de la cancelación con 14 días o más.</li><li>El retraso al llegar fue de menos de 3 horas.</li>
<li>Los problemas técnicos y las huelgas del personal de la aerolínea no la libran de pagar.</li></ul></div>
</div></section>
<section class="ref"><div class="wrap"><h2>Cómo reclamar</h2><ol class="steps">
<li>Guarda la tarjeta de embarque, la reserva y, si puedes, una captura del panel con el retraso.</li>
<li>Reclama primero a la aerolínea por escrito, desde su formulario de reclamaciones.</li>
<li>Si no contesta en un mes o te lo rechaza, y el vuelo salió de España, reclama gratis ante <a href="{AESA_URL}" rel="noopener">AESA</a>.</li>
<li>Si prefieres no hacerlo tú, una empresa de reclamaciones lo lleva sin coste por adelantado y se queda un porcentaje si gana.</li>
</ol></div></section>
<section class="ref" id="aerolineas"><div class="wrap"><h2>Compensación por aerolínea</h2><ul class="airlines">{links}</ul>
<h2 style="margin-top:32px">Vuelos que salen de aeropuertos españoles</h2><ul class="airlines">{aps}</ul></div></section>
<section class="ref" id="preguntas"><div class="wrap"><h2>Preguntas frecuentes</h2>{faq_html(l)}</div></section>"""
    return f"""<section class="ref" id="cuanto"><div class="wrap">
<h2>How much you can claim</h2>
<p class="lead">A fixed amount per passenger based on flight distance, not ticket price. Flights from Spain and the rest of the EU follow EU261 (euros); flights from the UK follow UK261 (pounds). Sources: <a href="{EU_URL['en']}" rel="noopener">Your Europe, European Commission</a> and <a href="{CAA_URL}" rel="noopener">UK Civil Aviation Authority</a>.</p>
<div class="board"><table><thead><tr><th>Flight distance</th><th>EU261 (from Spain/EU)</th><th>UK261 (from the UK)</th></tr></thead><tbody>
<tr><td>Up to 1,500 km (Madrid–Paris)</td><td class="eur">€250</td><td class="eur">£220</td></tr>
<tr><td>1,500 to 3,500 km (Manchester–Malaga)</td><td class="eur">€400</td><td class="eur">£350</td></tr>
<tr><td>Over 3,500 km (London–New York)</td><td class="eur">€600</td><td class="eur">£520</td></tr>
<tr><td>Over 3,500 km, 3 to 4 hour delay</td><td class="eur">€300</td><td class="eur">£260</td></tr>
</tbody></table></div></div></section>
<section class="ref"><div class="wrap two">
<div><h3>When you get paid</h3><ul>
<li>You reach your final destination 3 or more hours late.</li><li>Your flight is cancelled with less than 14 days' notice.</li><li>You are denied boarding because of overbooking.</li>
<li>The flight departs from the EU, Iceland, Norway, Switzerland (Canary and Balearic Islands included) or the UK, or arrives there with an EU or UK airline.</li></ul></div>
<div><h3>When you don't</h3><ul>
<li>Extraordinary circumstances the airline can prove: severe weather, air traffic control strikes or security risks.</li>
<li>You were told about the cancellation 14 or more days in advance.</li><li>Your arrival delay was under 3 hours.</li>
<li>Technical faults and strikes by the airline's own staff do not exempt it from paying.</li></ul></div>
</div></section>
<section class="ref"><div class="wrap"><h2>How to claim</h2><ol class="steps">
<li>Keep your boarding pass, booking confirmation and, if possible, a photo of the departures board.</li>
<li>Claim from the airline in writing first, using its online claim form.</li>
<li>If it refuses or does not reply within a month: flights from Spain can go to <a href="{AESA_URL}" rel="noopener">AESA</a> for free; flights from the UK can go to the airline's ADR scheme or the <a href="{CAA_URL}" rel="noopener">CAA</a>.</li>
<li>If you'd rather not do it yourself, a claims company handles it with no upfront cost and keeps a percentage if it wins.</li>
</ol></div></section>
<section class="ref" id="aerolineas"><div class="wrap"><h2>Compensation by airline</h2><ul class="airlines">{links}</ul>
<h2 style="margin-top:32px">Flights from Spanish airports</h2><ul class="airlines">{aps}</ul></div></section>
<section class="ref" id="preguntas"><div class="wrap"><h2>Frequently asked questions</h2>{faq_html(l)}</div></section>"""


def km(a, b):
    r = math.pi / 180
    dlat, dlon = (b[4] - a[4]) * r, (b[5] - a[5]) * r
    h = math.sin(dlat / 2) ** 2 + math.cos(a[4] * r) * math.cos(b[4] * r) * math.sin(dlon / 2) ** 2
    return round(2 * 6371 * math.asin(math.sqrt(h)))


def tier(d, intra, t):
    return t[0] if d <= 1500 else t[1] if (intra or d <= 3500) else t[2]


def route_table(l, code, name):
    o = AIRPORTS[code]
    rows = []
    for dc in DESTS[l]:
        if dc == code or dc not in AIRPORTS:
            continue
        b = AIRPORTS[dc]
        d = km(o, b)
        out_eur = tier(d, b[6] == 1, (250, 400, 600))
        dname = e(NAMES[l].get(dc, dc))
        if l == "es":
            rows.append((d, f'<tr><td>{dname} ({dc})</td><td>{d:,} km'.replace(",", ".") + f'</td><td class="eur">{out_eur} €</td></tr>'))
        else:
            if b[3] in UKC:
                back = f"£{tier(d, False, (220, 350, 520))}"
            elif b[6] == 1:
                back = f"€{tier(d, True, (250, 400, 600))}"
            else:
                back = f"€{out_eur}*"
            rows.append((d, f'<tr><td>{dname} ({dc})</td><td>{d:,} km</td><td class="eur">€{out_eur}</td><td class="eur">{back}</td></tr>'))
    rows.sort()
    body = "".join(r for _, r in rows)
    if l == "es":
        return f"""<section class="ref"><div class="wrap"><h2>Cuánto te toca desde {e(name)} según el destino</h2>
<p class="lead">Distancia en línea recta desde el aeropuerto de {e(name)} ({code}) y compensación por pasajero con 3 horas o más de retraso al llegar. Calculado con el método del reglamento (ruta ortodrómica).</p>
<div class="board"><table><thead><tr><th>Destino</th><th>Distancia</th><th>Compensación</th></tr></thead><tbody>{body}</tbody></table></div></div></section>"""
    return f"""<section class="ref"><div class="wrap"><h2>{e(name)} flight delays: what each route pays</h2>
<p class="lead">Great-circle distance from {e(name)} airport ({code}) and compensation per passenger for an arrival delay of 3 hours or more. Flights out of {e(name)} follow EU261; flights from the UK into {e(name)} follow UK261.</p>
<div class="board"><table><thead><tr><th>Route</th><th>Distance</th><th>From {e(name)}</th><th>To {e(name)}</th></tr></thead><tbody>{body}</tbody></table></div>
<p class="lead" style="margin-top:12px">* Only if the flight into Spain is operated by an EU airline.</p></div></section>"""


# Example routes per airline for the unique "worked examples" section (distances computed, not claimed schedules)
AL_ROUTES = {
    "ryanair": [("MAD", "DUB"), ("AGP", "STN"), ("PMI", "BGY")],
    "vueling": [("BCN", "FCO"), ("BCN", "LGW"), ("SVQ", "BCN")],
    "iberia": [("MAD", "BCN"), ("MAD", "JFK"), ("MAD", "BOG")],
    "iberia-express": [("MAD", "TFN"), ("MAD", "PMI"), ("MAD", "LHR")],
    "air-europa": [("MAD", "PMI"), ("MAD", "AMS"), ("MAD", "MIA")],
    "volotea": [("BIO", "VCE"), ("OVD", "PMI"), ("VLC", "NTE")],
    "binter": [("LPA", "TFN"), ("LPA", "MAD"), ("TFN", "LIS")],
    "air-nostrum": [("VLC", "SVQ"), ("MAD", "OVD"), ("BCN", "BIO")],
    "easyjet": [("BCN", "GVA"), ("AGP", "LGW"), ("MAD", "BRS")],
    "tui": [("PMI", "BHX"), ("TFS", "MAN"), ("ALC", "AMS")],
    "wizz-air": [("BCN", "BUD"), ("MAD", "OTP"), ("ALC", "LTN")],
    "transavia": [("ALC", "ORY"), ("AGP", "AMS"), ("PMI", "RTM")],
    "lufthansa": [("MAD", "FRA"), ("BCN", "MUC"), ("AGP", "FRA")],
    "air-france": [("MAD", "CDG"), ("BCN", "CDG"), ("VLC", "CDG")],
    "klm": [("BCN", "AMS"), ("MAD", "AMS"), ("AGP", "AMS")],
    "tap": [("MAD", "LIS"), ("BCN", "OPO"), ("MAD", "GRU")],
    "ita-airways": [("MAD", "FCO"), ("BCN", "FCO"), ("MAD", "LIN")],
    "norwegian": [("AGP", "OSL"), ("ALC", "ARN"), ("BCN", "CPH")],
    "british-airways": [("MAD", "LHR"), ("BCN", "LHR"), ("AGP", "LGW")],
    "jet2": [("ALC", "MAN"), ("AGP", "LBA"), ("PMI", "BHX")],
    "turkish-airlines": [("BCN", "IST"), ("MAD", "IST"), ("AGP", "IST")],
    "emirates": [("MAD", "DXB"), ("BCN", "DXB"), ("MAD", "DXB")],
    "canaryfly": [("LPA", "TFN"), ("LPA", "ACE"), ("TFN", "SPC")],
    "iberojet": [("MAD", "PUJ"), ("MAD", "CUN"), ("MAD", "HAV")],
    "plus-ultra": [("MAD", "CCS")],
    "eurowings": [("PMI", "DUS"), ("BCN", "CGN"), ("AGP", "HAM")],
    "condor": [("PMI", "FRA"), ("TFS", "FRA"), ("LPA", "MUC")],
    "aer-lingus": [("MAD", "DUB"), ("BCN", "DUB"), ("AGP", "DUB")],
    "sas": [("AGP", "CPH"), ("ALC", "OSL"), ("BCN", "ARN")],
    "swiss": [("MAD", "ZRH"), ("BCN", "ZRH"), ("AGP", "ZRH")],
    "brussels-airlines": [("BCN", "BRU"), ("MAD", "BRU"), ("AGP", "BRU")],
    "aegean": [("BCN", "ATH"), ("MAD", "ATH")],
    "azores-airlines": [("PDL", "LIS"), ("PDL", "OPO")],
    "level": [("BCN", "JFK"), ("BCN", "EZE"), ("BCN", "BOS")],
    "wamos-air": [("MAD", "CUN"), ("MAD", "PUJ")],
    "world2fly": [("MAD", "PUJ"), ("MAD", "CUN"), ("MAD", "HAV")],
    "virgin-atlantic": [("LHR", "JFK"), ("MAN", "MCO"), ("LHR", "LAX")],
    "loganair": [("GLA", "SYY"), ("EDI", "KOI")],
    "austrian": [("MAD", "VIE"), ("BCN", "VIE"), ("AGP", "VIE")],
    "lot": [("MAD", "WAW"), ("BCN", "WAW")],
    "finnair": [("MAD", "HEL"), ("BCN", "HEL"), ("AGP", "HEL")],
    "airbaltic": [("BCN", "RIX"), ("AGP", "RIX")],
    "icelandair": [("MAD", "KEF"), ("BCN", "KEF")],
    "pegasus": [("BCN", "SAW"), ("MAD", "SAW")],
}
SPANISH = {"vueling", "iberia", "iberia-express", "air-europa", "volotea", "binter", "air-nostrum", "canaryfly", "iberojet", "plus-ultra", "level", "wamos-air", "world2fly"}


def eu_amount(d, intra, h4=False):
    full = tier(d, intra, (250, 400, 600))
    return full // 2 if (h4 and full == 600) else full


def airline_section(l, a):
    rows, seen = [], set()
    for o, dcode in AL_ROUTES.get(a["slug"], []):
        if (o, dcode) in seen or o not in AIRPORTS or dcode not in AIRPORTS:
            continue
        seen.add((o, dcode))
        A, B = AIRPORTS[o], AIRPORTS[dcode]
        d = km(A, B)
        uk = A[3] == "GB"
        intra = (not uk) and A[6] == 1 and B[6] == 1
        full = tier(d, intra, (220, 350, 520)) if uk else eu_amount(d, intra)
        long_haul = (not intra) and d > 3500
        nA, nB = e(NAMES[l].get(o) or AIRPORTS[o][2]), e(NAMES[l].get(dcode) or AIRPORTS[dcode][2])
        hi, lo = (520, 260) if uk else (600, 300)
        if l == "es":
            cur = lambda x: f"{x} £" if uk else f"{x} €"
            note = f"{cur(lo)} si llegas con entre 3 y 4 h de retraso; {cur(hi)} a partir de 4 h" if long_haul else f"{cur(full)} con 3 h o más de retraso"
            rows.append(f"<tr><td>{nA} → {nB}</td><td>{d:,} km".replace(",", ".") + f"</td><td>{note}</td></tr>")
        else:
            cur = lambda x: f"£{x}" if uk else f"€{x}"
            note = f"{cur(lo)} for 3–4 h late; {cur(hi)} from 4 h" if long_haul else f"{cur(full)} for 3 h or more"
            rows.append(f"<tr><td>{nA} → {nB}</td><td>{d:,} km</td><td>{note}</td></tr>")
    n, slug = e(a["name"]), a["slug"]
    if l == "es":
        if slug in SPANISH:
            claim = (f"<p>{n} es española, así que si no te contesta en un mes o rechaza tu reclamación puedes ir gratis a <a href=\"{AESA_URL}\" rel=\"noopener\">AESA</a> "
                     f"tanto si el vuelo salía de España como si llegaba a España desde fuera de la UE.</p>")
        elif a["eu"] == "no" and not a["uk"]:
            claim = (f"<p>{n} no es europea: solo puedes reclamarle por el reglamento europeo si el vuelo <strong>salía</strong> de un aeropuerto de la UE "
                     f"(por ejemplo, Madrid–{e(NAMES['es'].get(AL_ROUTES[slug][0][1]) or AIRPORTS[AL_ROUTES[slug][0][1]][2])}). La vuelta a España con {n} no está cubierta.</p>")
        else:
            claim = (f"<p>Si el vuelo de {n} salía de España, el organismo que puede ayudarte gratis es <a href=\"{AESA_URL}\" rel=\"noopener\">AESA</a>. "
                     f"Si salía de otro país de la UE, te corresponde el organismo de ese país.</p>")
        if a["uk"]:
            claim += f"<p>En los vuelos de {n} que salen del Reino Unido se aplica la norma británica (UK261), que paga en libras: 220, 350 o 520 £.</p>"
        return (f'<section class="ref"><div class="wrap"><h2>Cuánto paga {n}: ejemplos con distancias reales</h2>'
                f'<p class="lead">El importe depende de la distancia del vuelo, no de lo que pagaste por el billete. Estos son ejemplos de trayectos de {n}, con la distancia calculada como manda el reglamento:</p>'
                f'<div class="board"><table><thead><tr><th>Trayecto</th><th>Distancia</th><th>Compensación por pasajero</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
                f'<h2 style="margin-top:32px">Cómo reclamar a {n}</h2>'
                f'<p>Primero reclama directamente a {n} por escrito, desde el formulario de reclamaciones de su web, con tu número de reserva y la tarjeta de embarque. '
                f'Pide expresamente la compensación del Reglamento (CE) 261/2004 además del reembolso o los gastos.</p>{claim}</div></section>')
    if slug in SPANISH:
        claim = f"<p>{n} is a Spanish airline, so if it ignores you for a month or rejects the claim you can escalate to <a href=\"{AESA_URL}\" rel=\"noopener\">AESA</a>, Spain's aviation authority, for free.</p>"
    elif a["eu"] == "no" and not a["uk"]:
        claim = f"<p>{n} is not a European airline, so EU261 only covers its flights <strong>departing</strong> the EU (for example, Madrid to {e(NAMES['en'].get(AL_ROUTES[slug][0][1]) or AIRPORTS[AL_ROUTES[slug][0][1]][2])}). Its flights into Spain are not covered.</p>"
    else:
        claim = f"<p>For a {n} flight departing Spain, the enforcement body is <a href=\"{AESA_URL}\" rel=\"noopener\">AESA</a>; for one departing the UK, the airline's ADR scheme or the <a href=\"{CAA_URL}\" rel=\"noopener\">CAA</a>.</p>"
    if a["uk"]:
        claim += f"<p>On {n} flights departing the UK, UK261 applies and pays £220, £350 or £520 instead of euros.</p>"
    return (f'<section class="ref"><div class="wrap"><h2>What {n} pays: examples with real distances</h2>'
            f'<p class="lead">The amount depends on the flight distance, not the ticket price. Here are example {n} routes with the distance worked out the way the regulation requires (EU261 amounts):</p>'
            f'<div class="board"><table><thead><tr><th>Route</th><th>Distance</th><th>Compensation per passenger</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            f'<h2 style="margin-top:32px">How to claim from {n}</h2>'
            f'<p>Claim from {n} in writing first, through the claims form on its website, with your booking reference and boarding pass. '
            f'Ask explicitly for compensation under EU261 (or UK261) as well as any refund or expenses.</p>{claim}</div></section>')


def extra_jsonld(l, title, path):
    home = u_home(l)
    if path == home:
        data = [{"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": SITE_URL + home, "inLanguage": l},
                {"@context": "https://schema.org", "@type": "WebApplication", "name": ("Calculadora de compensación por retraso de vuelo" if l == "es" else "Flight delay compensation calculator"),
                 "url": SITE_URL + home, "applicationCategory": "TravelApplication", "operatingSystem": "Any", "inLanguage": l,
                 "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}}]
    else:
        data = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": BRAND, "item": SITE_URL + home},
            {"@type": "ListItem", "position": 2, "name": title.split(":")[0], "item": SITE_URL + path}]}]
    return "".join(f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>' for d in data)


def page(l, title, desc, path, body, alts, alt_path, data_url="/data/airports.min.json"):
    cfg = {"lang": l, "dataUrl": data_url, "airlines": [{"slug": a["slug"], "eu": a["eu"], "uk": a["uk"], "name": a["name"], "claim": a.get("claim_" + l), "note": a.get("note_" + l), "adr": a.get("adr_uk")} for a in AIRLINES]}
    return (f"{head(l, title, desc, path, alts)}\n{header(l, alt_path)}\n<main>{body}</main>\n{footer(l)}\n{faq_jsonld(l) if path == u_home(l) else ''}\n{extra_jsonld(l, title, path)}\n"
            f"<script>window.CTT={json.dumps(cfg, ensure_ascii=False)};</script>\n<script>{JS}</script>")


def full_doc(inner, l):
    h, b = inner.split("</style>", 1)
    return (f'<!doctype html>\n<html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f"{h}</style>\n{GA4}{TP_SCRIPT}{ADSENSE}</head>\n<body>{b}{CONSENT}</body></html>\n")


GA4 = ("<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
       "gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',wait_for_update:500});"
       "gtag('js',new Date());gtag('config','G-6JRCZVTNDG');</script>\n"
       '<script async src="https://www.googletagmanager.com/gtag/js?id=G-6JRCZVTNDG"></script>\n')

CONSENT = ("<div id=\"ck\" style=\"display:none;position:fixed;left:12px;right:12px;bottom:12px;z-index:9999;max-width:560px;margin:0 auto;background:#111827;color:#fff;"
           "border-radius:12px;padding:14px 16px;font:14px/1.4 system-ui,sans-serif;box-shadow:0 8px 30px rgba(0,0,0,.3)\">"
           "<span id=\"ckt\"></span> <a href=\"/privacidad/\" style=\"color:#facc15\">+info</a>"
           "<div style=\"margin-top:10px;display:flex;gap:8px;justify-content:flex-end\">"
           "<button id=\"ckn\" style=\"background:transparent;color:#fff;border:1px solid #6b7280;border-radius:8px;padding:6px 12px;cursor:pointer\"></button>"
           "<button id=\"cky\" style=\"background:#facc15;color:#111827;border:0;border-radius:8px;padding:6px 12px;font-weight:700;cursor:pointer\"></button></div></div>"
           "<script>(function(){var en=document.documentElement.lang==='en',k='vc_consent',v=null;try{v=localStorage.getItem(k)}catch(e){}"
           "function g(a){gtag('consent','update',{analytics_storage:a?'granted':'denied'})}"
           "if(v){g(v==='y');return}var b=document.getElementById('ck');"
           "document.getElementById('ckt').textContent=en?'We use analytics cookies to count visits.':'Usamos cookies de analítica para contar visitas.';"
           "document.getElementById('cky').textContent=en?'Accept':'Aceptar';document.getElementById('ckn').textContent=en?'Reject':'Rechazar';"
           "function s(a){try{localStorage.setItem(k,a?'y':'n')}catch(e){}g(a);b.style.display='none'}"
           "document.getElementById('cky').onclick=function(){s(true)};document.getElementById('ckn').onclick=function(){s(false)};b.style.display='block'})();</script>\n")

ADSENSE_PUB = "ca-pub-1079386437086971"
ADSENSE = ('<meta name="msvalidate.01" content="D3B289B2220FF34999D4248924B46B3C">\n'
           f'<meta name="google-adsense-account" content="{ADSENSE_PUB}">\n'
           f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB}" crossorigin="anonymous"></script>\n')

# Travelpayouts site verification / tracking
TP_SCRIPT = ('<script nowprocket data-noptimize="1" data-cfasync="false" data-wpfc-render="false" seraph-accel-crit="1" data-no-defer="1" data-cmp-ab="2">\n'
             '  (function () {\n      var script = document.createElement("script");\n      script.async = 1;\n'
             '      script.setAttribute("data-cmp-ab","2");\n      script.src = \'https://emrldtp.cc/NTgyNjYx.js?t=582661\';\n'
             '      document.head.appendChild(script);\n  })();\n</script>\n')


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(content)


def out(path):
    return os.path.join(OUT, path.strip("/"), "index.html") if path != "/" else os.path.join(OUT, "index.html")


# ---------------------------------------------------------------- build
def build():
    shutil.rmtree(OUT, ignore_errors=True)
    shutil.rmtree(PREV, ignore_errors=True)
    for d in (OUT, PREV):
        os.makedirs(os.path.join(d, "data"))
        shutil.copy(os.path.join(ROOT, "data", "airports.min.json"), os.path.join(d, "data", "airports.min.json"))
    urls = []

    def emit(l, path, html_inner):
        write(out(path), full_doc(html_inner, l))
        urls.append(path)

    # Home
    homes = {"es": "/", "en": "/en/"}
    T = {
        "es": ("Reclamar vuelo retrasado o cancelado: calcula cuánto te toca",
               "Calcula gratis la compensación por retraso, cancelación u overbooking de tu vuelo: 250, 400 o 600 € por pasajero según el reglamento europeo.",
               "Reclamar un vuelo retrasado o cancelado: calcula cuánto te toca",
               "Si llegaste con 3 horas o más de retraso, te cancelaron el vuelo o no te dejaron embarcar, la aerolínea puede deberte hasta 600 € por pasajero. Mete tu vuelo y lo calculamos en segundos.",
               ("MAD", "BER")),
        "en": ("Flight delay compensation calculator for Spain and the UK",
               "Free calculator for delayed, cancelled or overbooked flights to and from Spain: up to €600 under EU261 or £520 under UK261 per passenger.",
               "Delayed or cancelled flight to or from Spain? Check what you're owed",
               "If you arrived 3 or more hours late, your flight was cancelled or you were bumped, the airline may owe you up to €600 or £520 per passenger. Enter your flight and we'll work it out in seconds.",
               ("MAN", "AGP")),
    }
    for l in ("es", "en"):
        title, desc, h1, lede, (dep, arr) = T[l]
        other = "en" if l == "es" else "es"
        body = hero(l, e(h1), lede, "", dep, arr) + reference_sections(l)
        p = page(l, title, desc, homes[l], body, homes, homes[other])
        emit(l, homes[l], p)
        if l == "es":
            write(os.path.join(PREV, "index.html"), page(l, title, desc, "/", body, homes, homes[other], "data/airports.min.json")
                  .replace(f"<title>{e(title)}</title>", "<title>VuelosClaim</title>", 1))

    # Airlines
    for a in AIRLINES:
        alts = {"es": u_airline("es", a), "en": u_airline("en", a)}
        n = e(a["name"])
        for l in ("es", "en"):
            other = "en" if l == "es" else "es"
            dep, arr = EXAMPLES[l].get(a["slug"], EXAMPLES["es"].get(a["slug"], ("MAD", "BER")))
            if l == "es":
                if a["eu"] == "yes":
                    scope = f"{n} es una aerolínea de {e(a['country'])}, así que el reglamento europeo cubre todos sus vuelos que salen de Europa y también los que llegan a Europa desde fuera."
                elif a["eu"] == "mixed":
                    scope = f"{n} vuela con varias compañías de su grupo ({e(a['country'])}). Sus vuelos que salen de Europa están siempre cubiertos; en los que llegan desde fuera, depende de qué compañía lo operó."
                else:
                    scope = f"{n} es una aerolínea de {e(a['country'])}, fuera de la UE. El reglamento europeo cubre sus vuelos que salen de un aeropuerto europeo, pero no los que llegan a Europa desde fuera."
                title = f"Compensación por retraso de {a['name']}: cuánto te toca"
                desc = f"Calcula cuánto te debe {a['name']} por un retraso de más de 3 horas, una cancelación u overbooking: 250, 400 o 600 € por pasajero."
                h1 = f"Retraso o cancelación con {n}: calcula cuánto te toca"
                lede = scope + " Mete tu vuelo y te decimos el importe."
            else:
                if a["eu"] == "yes":
                    scope = f"{n} is an airline from {e(a['country_en'])}, so EU261 covers all its flights departing Europe and its flights arriving in Europe from outside."
                elif a["eu"] == "mixed":
                    scope = f"{n} flies through several group airlines ({e(a['country_en'])}). Flights departing Spain or the rest of the EU are always covered by EU261; flights from the UK are covered by UK261."
                else:
                    scope = f"{n} is an airline from {e(a['country_en'])}. Its flights departing Spain or the rest of the EU are covered by EU261, and its flights departing the UK by UK261."
                if a["uk"]:
                    scope += f" On a {n} flight from the UK to Spain, you claim in pounds under UK261; on the flight back from Spain, in euros under EU261."
                title = f"{a['name']} delay compensation: how much you can claim"
                desc = f"Check what {a['name']} owes you for a delay of over 3 hours, a cancellation or overbooking: up to €600 (EU261) or £520 (UK261) per passenger."
                h1 = f"{n} flight delayed or cancelled? Check what you're owed"
                lede = scope + " Enter your flight and we'll work out the amount."
            deep = ""
            if l == "en" and a["slug"] in uk_deep.META:
                m = uk_deep.META[a["slug"]]
                title, desc, h1 = m["title"], m["desc"], e(m["h1"])
                deep = uk_deep.section(a, AIRPORTS, km, NAMES["en"], AESA_URL, CAA_URL)
            body = hero(l, h1, lede, a["slug"], dep, arr) + deep + airline_section(l, a) + reference_sections(l, True)
            emit(l, alts[l], page(l, title, desc, alts[l], body, alts, alts[other]))

    # Airports
    for ap in ES_AIRPORTS:
        code, _, name_es, name_en = ap
        alts = {"es": u_airport("es", ap), "en": u_airport("en", ap)}
        for l in ("es", "en"):
            other = "en" if l == "es" else "es"
            if l == "es":
                n = e(name_es)
                extra = " Canarias forma parte de la UE a estos efectos, así que se aplica igual que en la Península." if code in CANARY else ""
                lede = (f"Cualquier vuelo que sale del aeropuerto de {n} está cubierto por el reglamento europeo, sea cual sea la aerolínea.{extra} "
                        f"Si llegas a {n} desde fuera de Europa, solo está cubierto si vuelas con una aerolínea europea. Mete tu vuelo y te decimos el importe.")
                title = f"Retraso vuelo aeropuerto {name_es.split('-')[0]}: cuánto te toca"
                desc = f"Calcula la compensación por un vuelo retrasado, cancelado o con overbooking en el aeropuerto de {name_es}: 250, 400 o 600 € por pasajero."
                h1 = f"Vuelo retrasado en {n}: calcula cuánto te toca"
                dep, arr = code, ("LHR" if code == "MAD" else "MAD")
                body = hero(l, h1, lede, "", dep, arr) + route_table(l, code, name_es) + reference_sections(l, True)
            else:
                n = e(name_en)
                extra = " The Canary Islands count as part of the EU for these rules, exactly like mainland Spain." if code in CANARY else ""
                lede = (f"Every flight departing {n} airport is covered by EU261, whatever the airline, and pays up to €600.{extra} "
                        f"Flights from the UK into {n} are covered by UK261 and pay up to £520. Enter your flight and we'll work out the amount.")
                title = f"{name_en.split('-')[0].split(' (')[0]} airport flight delay compensation"
                desc = f"Delayed or cancelled flight at {name_en} airport? Check your compensation under EU261 or UK261: up to €600 or £520 per passenger."
                h1 = f"Flight delayed at {n} airport? Check what you're owed"
                dep, arr = code, ("LHR" if code != "MAN" else "LGW")
                body = hero(l, h1, lede, "", dep, "MAN") + route_table(l, code, name_en) + reference_sections(l, True)
            emit(l, alts[l], page(l, title, desc, alts[l], body, alts, alts[other]))

    # UK airports -> Spain (EN programmatic pages)
    uk_urls = uk_airports.build({
        "AIRPORTS": AIRPORTS, "km": km,
        "es_names": {ap[0]: ap[3] for ap in ES_AIRPORTS},
        "es_url": {ap[0]: u_airport("en", ap) for ap in ES_AIRPORTS},
        "page": page, "hero": hero, "reference_sections": reference_sections, "emit": emit,
        "AESA_URL": AESA_URL, "CAA_URL": CAA_URL})

    strike_urls = strikes.build({"emit": emit, "page": page})
    cmp_urls = compare.build({"emit": emit, "page": page, "AFF_URL": AFF_URL})
    cmp_urls += guides.build({"emit": emit, "page": page})

    # Widget for blogs (ES) + page explaining how to embed it
    wcfg = {"lang": "es", "dataUrl": "/data/airports.min.json", "airlines": [{"slug": a["slug"], "eu": a["eu"], "uk": a["uk"], "name": a["name"], "claim": a.get("claim_es"), "note": a.get("note_es"), "adr": a.get("adr_uk")} for a in AIRLINES]}
    winner = (f"<title>Calculadora de compensación de vuelos · {BRAND}</title><meta name=\"robots\" content=\"noindex\">{FONTS}<style>{CSS}</style>"
              f"<div class=\"embed\">{calculator('es', '', 'MAD', 'BER')}<p class=\"embed-foot\">Calculadora de <a href=\"{SITE_URL}/\" target=\"_blank\" rel=\"noopener\">{BRAND}</a> · Reglamento CE 261/2004</p></div>"
              f"<script>window.CTT={json.dumps(wcfg, ensure_ascii=False)};</script><script>{JS}</script>")
    write(os.path.join(OUT, "widget", "index.html"), full_doc(winner, "es"))
    code_snip = (f'<iframe src="{SITE_URL}/widget/" title="Calculadora de compensación por retraso de vuelo" '
                 f'style="width:100%;max-width:560px;height:960px;border:0" loading="lazy"></iframe>\n'
                 f'<p><a href="{SITE_URL}/">Calculadora de compensación por retraso de vuelo</a> de {BRAND}</p>')
    ins_body = f"""<div class="wrap prose"><h1>Pon la calculadora en tu web, gratis</h1>
<p>Si tienes un blog de viajes, una web de chollos de vuelos o una agencia, puedes insertar nuestra calculadora para que tus lectores sepan al momento si les deben 250, 400 o 600 €. Es gratis, no lleva publicidad y no recoge datos de tus lectores.</p>
<h2>Cómo insertarla</h2><p>Copia este código y pégalo en tu página, en modo HTML:</p>
<label class="sr" for="embed-code">Código para insertar</label><textarea id="embed-code" rows="5" readonly onclick="this.select()">{e(code_snip)}</textarea>
<h2>¿Tienes enlace de afiliado de una empresa de reclamaciones?</h2><p>Puedes usar el tuyo en el botón "Reclámalo sin coste". Añade al final de la dirección del iframe <code>?aff=</code> seguido de tu enlace (AirHelp, AirAdvisor, Compensair, Flightright, Skyrefund o Reclamador). Las comisiones de tus lectores son tuyas.</p>
<p>¿Dudas o quieres una versión con tus colores? Escríbenos a <strong>vuelosclaim@gmail.com</strong>.</p></div>"""
    emit("es", "/insertar-calculadora/", f"{head('es', 'Inserta la calculadora en tu web · ' + BRAND, 'Inserta gratis en tu blog la calculadora de compensación por retraso o cancelación de vuelos.', '/insertar-calculadora/')}\n{header('es', None)}<main>{ins_body}</main>{footer('es')}")

    # Legal pages (both languages)
    legal_txt = {
        "about": {
            "es": ("Quiénes somos y fuentes", f"<p>{BRAND} es un proyecto independiente con sede en Valencia que explica en lenguaje claro los derechos de los pasajeros aéreos y calcula cuánto te corresponde. No somos una aerolínea ni un despacho de abogados.</p><h2>Cómo calculamos</h2><p>Aplicamos el Reglamento (CE) n.º 261/2004 y, para vuelos que salen del Reino Unido, su versión británica (UK261): medimos la distancia ortodrómica entre los aeropuertos con datos de OurAirports y aplicamos los tramos de 250, 400 y 600 € (220, 350 y 520 £), la reducción del 50 % en vuelos de más de 3.500 km con 3 a 4 horas de retraso, los plazos de aviso de las cancelaciones y la doctrina del Tribunal de Justicia de la UE sobre retrasos (asunto Sturgeon) y huelgas del personal propio.</p><h2>Fuentes</h2><ul><li><a href=\"{EU_URL['es']}\">Comisión Europea: derechos de los pasajeros aéreos</a></li><li><a href=\"https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32004R0261\">Reglamento (CE) n.º 261/2004 en EUR-Lex</a></li><li><a href=\"{AESA_URL}\">AESA: derechos de los pasajeros</a></li><li><a href=\"{CAA_URL}\">CAA: retrasos y cancelaciones (Reino Unido)</a></li><li><a href=\"https://ourairports.com/data/\">OurAirports: datos de aeropuertos</a></li></ul><p>Última revisión: {UPDATED['es']}. Si ves un error, escríbenos a <strong>vuelosclaim@gmail.com</strong>.</p>"),
            "en": ("About us and sources", f"<p>{BRAND} is an independent project based in Valencia, Spain, that explains air passenger rights in plain language and calculates what you're owed. We are not an airline or a law firm.</p><h2>How we calculate</h2><p>We apply Regulation (EC) No 261/2004 and, for flights departing the UK, its UK version (UK261). We measure the great-circle distance between airports using OurAirports data and apply the €250, €400 and €600 tiers (£220, £350 and £520), the 50% reduction for flights over 3,500 km delayed 3 to 4 hours, the cancellation notice periods and EU Court of Justice case law on delays (Sturgeon) and airline staff strikes.</p><h2>Sources</h2><ul><li><a href=\"{EU_URL['en']}\">European Commission: air passenger rights</a></li><li><a href=\"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32004R0261\">Regulation (EC) No 261/2004 on EUR-Lex</a></li><li><a href=\"{CAA_URL}\">UK Civil Aviation Authority: delays and cancellations</a></li><li><a href=\"{AESA_URL}\">AESA (Spanish aviation authority): passenger rights</a></li><li><a href=\"https://ourairports.com/data/\">OurAirports: airport data</a></li></ul><p>Last reviewed: {UPDATED['en']}. Spotted a mistake? Email us at <strong>vuelosclaim@gmail.com</strong>.</p>"),
        },
        "legal": {
            "es": ("Aviso legal", f"<p>{BRAND} ofrece calculadoras gratuitas con información orientativa. Los resultados se basan en el Reglamento (CE) 261/2004 y en la información que introduces, y no constituyen asesoramiento jurídico.</p><p>Titular del sitio: <strong>Salvador Fernández Lloris, NIF 24444246F</strong>. Contacto: <strong>vuelosclaim@gmail.com</strong>.</p><p>Esta web contiene enlaces de afiliado. Si contratas un servicio a través de ellos, el titular puede recibir una comisión. Esto no tiene coste para ti ni modifica los resultados de las calculadoras.</p>"),
            "en": ("Legal notice", f"<p>{BRAND} provides free calculators with indicative information. Results are based on Regulation (EC) 261/2004, UK261 and the details you enter, and are not legal advice.</p><p>Site owner: <strong>Salvador Fernández Lloris, tax ID 24444246F</strong>. Contact: <strong>vuelosclaim@gmail.com</strong>.</p><p>This site contains affiliate links. If you use a service through them, the owner may earn a commission. This costs you nothing and does not change the calculators' results.</p>"),
        },
        "privacy": {
            "es": ("Política de privacidad", "<p>Las calculadoras funcionan en tu navegador: los datos de tu vuelo no se envían ni se guardan en nuestros servidores.</p><p>La web usa el script de afiliación de Travelpayouts para atribuir las visitas que llegan a los servicios de reclamación (por ejemplo, AirHelp). Al pulsar un enlace de afiliado, ese servicio puede usar cookies para registrar que vienes de esta web. La web usa Google Analytics para contar visitas de forma agregada (solo si aceptas en el aviso de cookies) y muestra anuncios de Google AdSense: Google y sus socios pueden usar cookies para mostrar anuncios, personalizados o no según lo que elijas en el aviso de consentimiento. Más información en <a href=\"https://policies.google.com/technologies/ads?hl=es\" rel=\"noopener\">cómo usa Google las cookies en publicidad</a>.</p><p>Responsable: <strong>Salvador Fernández Lloris</strong>. Contacto: <strong>vuelosclaim@gmail.com</strong>.</p>"),
            "en": ("Privacy policy", "<p>The calculators run in your browser: your flight details are not sent to or stored on our servers.</p><p>The site uses the Travelpayouts affiliate script to attribute visits sent to claims services (for example, AirHelp). When you click an affiliate link, that service may use cookies to record that you came from this site. The site uses Google Analytics to count visits in aggregate (only if you accept in the cookie notice) and shows Google AdSense ads: Google and its partners may use cookies to serve ads, personalised or not depending on your choice in the consent notice. More at <a href=\"https://policies.google.com/technologies/ads\" rel=\"noopener\">how Google uses cookies in advertising</a>.</p><p>Controller: <strong>Salvador Fernández Lloris</strong>. Contact: <strong>vuelosclaim@gmail.com</strong>.</p>"),
        },
    }
    for key, langs in legal_txt.items():
        alts = LEGAL[key]
        for l, (t, txt) in langs.items():
            other = "en" if l == "es" else "es"
            emit(l, alts[l], f"{head(l, t + ' · ' + BRAND, t, alts[l], alts)}\n{header(l, alts[other])}<main class=\"wrap prose\"><h1>{t}</h1>{txt}</main>{footer(l)}")

    fresh = {f"/en/{s}-delay-compensation/" for s in uk_deep.META} | set(uk_urls) | set(strike_urls)
    fresh2 = set(cmp_urls) | {u for a in AIRLINES if a['slug'] in ('canaryfly','iberojet','plus-ultra','eurowings','condor','aer-lingus','sas','swiss','brussels-airlines','aegean','azores-airlines','level','wamos-air','world2fly','virgin-atlantic','loganair','austrian','lot','finnair','airbaltic','icelandair','pegasus') for u in (u_airline('es', a), u_airline('en', a))}
    sm = "".join(f"<url><loc>{SITE_URL}{u}</loc><lastmod>{'2026-10-20' if u in fresh2 else '2026-10-19' if u in fresh else '2026-10-07'}</lastmod></url>" for u in urls)
    write(os.path.join(OUT, "sitemap.xml"), f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    os.makedirs(os.path.join(OUT, "img"), exist_ok=True)
    for fn in ("vuelosclaim-logo.png", "vuelosclaim-banner.png", "og-image.png", "icon-192.png", "icon-512.png"):
        shutil.copy(os.path.join(ROOT, "src_static", fn), os.path.join(OUT, "img", fn))
    for fn in ("favicon.ico", "apple-touch-icon.png", "favicon-48.png"):
        shutil.copy(os.path.join(ROOT, "src_static", fn), os.path.join(OUT, fn))
    write(os.path.join(OUT, "site.webmanifest"), json.dumps({"name": "VuelosClaim", "short_name": "VuelosClaim", "icons": [
        {"src": "/img/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/img/icon-512.png", "sizes": "512x512", "type": "image/png"}],
        "theme_color": "#13213c", "background_color": "#13213c", "display": "browser"}))
    _k=open(os.path.join(ROOT,"src_static","indexnow.key")).read().strip(); write(os.path.join(OUT, _k+".txt"), _k)
    write(os.path.join(OUT, "CNAME"), "vuelosclaim.eu\n"); write(os.path.join(OUT, ".nojekyll"), "")
    write(os.path.join(OUT, "ads.txt"), "google.com, pub-1079386437086971, DIRECT, f08c47fec0942fa0\n")
    write(os.path.join(OUT, "robots.txt"), f"User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /\n\nUser-agent: ClaudeBot\nAllow: /\n\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    write(os.path.join(OUT, "llms.txt"), f"""# {BRAND}

> Free calculator for flight delay, cancellation and overbooking compensation under EU Regulation 261/2004 (EU261) and its UK version (UK261), focused on flights to and from Spain. Spanish at /, English at /en/.

## Key pages

- [Calculadora (español)]({SITE_URL}/)
- [Calculator (English)]({SITE_URL}/en/)
- [About and sources]({SITE_URL}/en/about/)

## Rules summary

- EU261 (flights departing the EU, or arriving in the EU with an EU airline): €250 up to 1,500 km; €400 for 1,500-3,500 km or intra-EU over 1,500 km; €600 over 3,500 km (€300 if delayed 3-4 hours)
- UK261 (flights departing the UK, or arriving in the UK with a UK or EU airline): £220 / £350 / £520
- Due for arrival delays of 3+ hours, cancellations with under 14 days' notice, or involuntary denied boarding, unless the airline proves extraordinary circumstances

Last reviewed: {UPDATED['en']}
""")
    print(f"{len(urls)} páginas en {OUT}")


if __name__ == "__main__":
    build()
