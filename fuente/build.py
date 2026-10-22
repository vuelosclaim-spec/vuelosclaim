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
  delay="Retraso al llegar al destino final", d=[("lt3", "Menos de 3 h"), ("3to4", "De 3 h a 4 h"), ("gt4", "Más de 4 h"), ("unknown", "No lo sé")],
  notice="Te avisaron de la cancelación con", n=[("gt14", "14 días o más"), ("7to14", "Entre 7 y 13 días"), ("lt7", "Menos de 7 días"), ("unknown", "No lo sé")],
  reroute="¿Te ofrecieron un vuelo alternativo?", rr=[("yes", "Sí"), ("no", "No"), ("unknown", "No lo sé")],
  rdep="El vuelo alternativo salía, respecto al original…", rd=[("le1", "Como mucho 1 h antes, o más tarde"), ("1to2", "Entre 1 y 2 h antes"), ("gt2", "Más de 2 h antes"), ("unknown", "No lo sé")],
  rarr="…y llegaba al destino", ra=[("lt2", "Menos de 2 h más tarde"), ("2to4", "Entre 2 y 4 h más tarde"), ("ge4", "4 h o más tarde"), ("unknown", "No lo sé")],
  accepted="¿Aceptaste el vuelo alternativo?", ac=[("yes", "Sí"), ("no", "No, pedí el reembolso")],
  denied="¿Cediste tu plaza?", dn=[("invol", "No, me la negaron"), ("vol", "Sí, voluntariamente"), ("unknown", "No lo tengo claro")],
  checkin="¿Te presentaste a tiempo a facturación y embarque?", ci=[("yes", "Sí"), ("no", "No"), ("unknown", "No lo sé")],
  dreason="Motivo de la denegación", dr=[("overbooking", "Overbooking u otro motivo de la aerolínea"), ("reasonable", "Salud, seguridad o documentación"), ("unknown", "No me lo explicaron")],
  cause="Motivo que te dio la aerolínea", c=[("unknown", "No me lo dijeron"), ("tech", "Avería técnica"), ("crew", "Falta o enfermedad de la tripulación"),
    ("strike_own", "Huelga del personal de la aerolínea"), ("strike_ext", "Huelga de controladores o del aeropuerto"), ("atc", "Restricción de control aéreo (ATC)"),
    ("weather", "Meteorología adversa"), ("security", "Seguridad (amenaza, cierre del espacio aéreo)"), ("bird", "Choque con un ave u objeto en la pista"),
    ("knock", "Retraso del vuelo anterior del avión")],
  empty="Elige origen y destino para ver el resultado.", error="No se ha podido cargar la lista de aeropuertos. Comprueba tu conexión y vuelve a intentarlo.", retry="Reintentar",
  example="Ejemplo editable", per="por pasajero", cta="Reclamar con AirHelp", cta_small="AirHelp es un servicio externo de reclamación: no cobra por adelantado y, si consigue la compensación, se queda un 35 % (IVA incluido), hasta un 50 % si hay que ir a juicio. No garantiza el resultado. Es un enlace de afiliado: VuelosClaim recibe una comisión, sin coste para ti.", cta_generic="Reclamar con una empresa", cta_small_generic="Servicio externo de reclamación: cobra una comisión si consigue la compensación y no garantiza el resultado. Enlace de afiliado.",
  self="Prefiero reclamar yo gratis: generar mi carta", l_lead="Rellena tus datos y te preparamos la carta. Se compone en tu navegador: no la enviamos ni la guardamos. No hace falta poner datos bancarios.",
  l_name="Nombre y apellidos", l_book="Código de reserva", l_flight="Número de vuelo", l_date="Fecha del vuelo", l_pax="Pasajeros en la reserva",
  l_text="Tu carta", copy="Copiar carta", dl="Descargar .txt",
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
  delay="Delay at your final destination", d=[("lt3", "Under 3 h"), ("3to4", "3 h to 4 h"), ("gt4", "Over 4 h"), ("unknown", "Not sure")],
  notice="You were told about the cancellation", n=[("gt14", "14 days or more ahead"), ("7to14", "7 to 13 days ahead"), ("lt7", "Under 7 days ahead"), ("unknown", "Not sure")],
  reroute="Were you offered an alternative flight?", rr=[("yes", "Yes"), ("no", "No"), ("unknown", "Not sure")],
  rdep="Compared with the original, the alternative left…", rd=[("le1", "Up to 1 h earlier, or later"), ("1to2", "1 to 2 h earlier"), ("gt2", "Over 2 h earlier"), ("unknown", "Not sure")],
  rarr="…and arrived", ra=[("lt2", "Under 2 h later"), ("2to4", "2 to 4 h later"), ("ge4", "4 h or more later"), ("unknown", "Not sure")],
  accepted="Did you accept the alternative flight?", ac=[("yes", "Yes"), ("no", "No, I took a refund")],
  denied="Did you give up your seat?", dn=[("invol", "No, I was refused"), ("vol", "Yes, voluntarily"), ("unknown", "Not sure")],
  checkin="Did you check in and get to the gate on time?", ci=[("yes", "Yes"), ("no", "No"), ("unknown", "Not sure")],
  dreason="Reason for refusing you", dr=[("overbooking", "Overbooking or another airline reason"), ("reasonable", "Health, safety or documents"), ("unknown", "Not explained")],
  cause="Reason the airline gave", c=[("unknown", "None given"), ("tech", "Technical fault"), ("crew", "Crew shortage or illness"),
    ("strike_own", "Airline staff strike"), ("strike_ext", "Air traffic control or airport strike"), ("atc", "Air traffic control restriction"),
    ("weather", "Bad weather"), ("security", "Security (threat, airspace closure)"), ("bird", "Bird strike or object on the runway"),
    ("knock", "Earlier flight by the same aircraft was late")],
  empty="Choose where you flew from and to.", error="The airport list could not load. Check your connection and try again.", retry="Try again",
  example="Editable example", per="per passenger", cta="Claim with AirHelp", cta_small="AirHelp is an independent claims service: nothing upfront and, if it wins, it keeps 35% (VAT included), up to 50% if the case goes to court. Results are not guaranteed. This is an affiliate link: VuelosClaim earns a commission at no cost to you.", cta_generic="Claim with a company", cta_small_generic="Independent claims service: it charges a commission if it wins and cannot guarantee the result. Affiliate link.",
  self="I'd rather claim myself for free: write my letter", l_lead="Fill in your details and we'll prepare the letter. It is put together in your browser: we don't send or store it. No bank details needed.",
  l_name="Full name", l_book="Booking reference", l_flight="Flight number", l_date="Flight date", l_pax="Passengers on the booking",
  l_text="Your letter", copy="Copy letter", dl="Download .txt",
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
  ("¿Y si tenía una escala?", "Si era una única reserva, cuenta el retraso con el que llegaste al destino final y la distancia en línea recta entre el origen y el destino final, no la suma de los tramos (Tribunal de Justicia de la UE, asunto C-559/16)."),
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
    links += [f'<a href="{LEGAL["about"][l]}">{s["f_about"]}</a>', f'<a href="{LEGAL["legal"][l]}">{s["f_legal"]}</a>', f'<a href="{LEGAL["privacy"][l]}">{s["f_privacy"]}</a>', f'<a href="{LEGAL["privacy"][l]}#cookies" data-consent-open>Cookies</a>']
    return (f'<footer class="foot"><div class="wrap"><p>{s["foot1"]}</p><p>{s["foot2"]}</p><p>{s["foot3"].format(d=UPDATED[l])}</p>'
            f'<nav>{"".join(links)}</nav></div></footer>')


def chips(name, items, checked):
    return "".join(f'<label><input type="radio" name="{name}" value="{v}"{" checked" if v == checked else ""}><span>{e(t).replace(" h", "&nbsp;h")}</span></label>' for v, t in items)


def calculator(l, airline_slug, dep, arr):
    s = S[l]
    opts = [f'<option value="">{s["al_unknown"]}</option>'] + [
        f'<option value="{a["slug"]}"{" selected" if a["slug"] == airline_slug else ""}>{e(a["name"])}</option>' for a in AIRLINES
    ] + [f'<option value="otra-ue">{s["al_eu"]}</option>', f'<option value="otra-no-ue">{s["al_noneu"]}</option>']
    return f"""<form class="calc" id="calc" novalidate>
<h2>{s["calc_h"]}</h2>
<div class="row2">
 <div class="field"><label for="from">{s["from_"]}</label><input type="text" id="from" data-code="{dep}" autocomplete="off" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="from-list" placeholder="{s["ph"]}"><ul class="ac" id="from-list" role="listbox" hidden></ul></div>
 <div class="field"><label for="to">{s["to"]}</label><input type="text" id="to" data-code="{arr}" autocomplete="off" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="to-list" placeholder="{s["ph"]}"><ul class="ac" id="to-list" role="listbox" hidden></ul></div>
</div>
<div class="field"><label for="airline">{s["airline"]}</label><select id="airline" name="airline">{"".join(opts)}</select></div>
<fieldset><legend>{s["what"]}</legend><div class="chips">{chips("what", s["w"], "delay")}</div></fieldset>
<fieldset id="grp-delay"><legend>{s["delay"]}</legend><div class="chips">{chips("delay", s["d"], "gt4")}</div></fieldset>
<fieldset id="grp-notice" hidden><legend>{s["notice"]}</legend><div class="chips">{chips("notice", s["n"], "unknown")}</div></fieldset>
<fieldset id="grp-reroute" hidden><legend>{s["reroute"]}</legend><div class="chips">{chips("reroute", s["rr"], "unknown")}</div></fieldset>
<fieldset id="grp-rdep" hidden><legend>{s["rdep"]}</legend><div class="chips chips-wide">{chips("rdep", s["rd"], "unknown")}</div></fieldset>
<fieldset id="grp-rarr" hidden><legend>{s["rarr"]}</legend><div class="chips chips-wide">{chips("rarr", s["ra"], "unknown")}</div></fieldset>
<fieldset id="grp-accepted" hidden><legend>{s["accepted"]}</legend><div class="chips">{chips("accepted", s["ac"], None)}</div></fieldset>
<fieldset id="grp-denied" hidden><legend>{s["denied"]}</legend><div class="chips">{chips("denied", s["dn"], "unknown")}</div></fieldset>
<fieldset id="grp-checkin" hidden><legend>{s["checkin"]}</legend><div class="chips">{chips("checkin", s["ci"], "unknown")}</div></fieldset>
<fieldset id="grp-dreason" hidden><legend>{s["dreason"]}</legend><div class="chips chips-wide">{chips("dreason", s["dr"], "unknown")}</div></fieldset>
<div class="field" id="grp-cause"><label for="cause">{s["cause"]}</label><select id="cause" name="cause">{"".join(f'<option value="{v}">{e(t)}</option>' for v, t in s["c"])}</select></div>
<div class="result" id="result" data-state="empty" aria-live="polite">
 <p class="empty-msg">{s["empty"]}</p>
 <p class="error-msg"><span data-error-text>{s["error"]}</span> <button type="button" class="btn btn-ghost btn-small" id="ac-retry">{s["retry"]}</button></p>
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
  <a class="btn btn-sign" href="{e(AFF_URL)}" rel="sponsored nofollow noopener" target="_blank" data-generic="{e(s["cta_generic"])}">{s["cta"]}</a>
  <small data-generic="{e(s["cta_small_generic"])}">{s["cta_small"]} <a href="{"/comparativa-empresas-reclamacion-vuelos/" if l == "es" else "/en/flight-compensation-companies-compared/"}">{"Compara con reclamar tú gratis" if l == "es" else "Compare with claiming yourself for free"}</a>.</small>
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
<tr><td>Más de 3.500 km fuera de la UE con 3 a 4 horas de retraso</td><td class="eur">300 €</td></tr>
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
<tr><td>Over 3,500 km (not within the EU), 3 to 4 hour delay</td><td class="eur">€300</td><td class="eur">£260</td></tr>
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
    claim = ""
    if l == "es":
        return (f'<section class="ref"><div class="wrap"><h2>Cuánto paga {n}: ejemplos con distancias reales</h2>'
                f'<p class="lead">El importe depende de la distancia del vuelo, no de lo que pagaste por el billete. Estos son ejemplos de trayectos de {n}, con la distancia calculada como manda el reglamento:</p>'
                f'<div class="board"><table><thead><tr><th>Trayecto</th><th>Distancia</th><th>Compensación por pasajero</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
                f'<h2 style="margin-top:32px">Cómo reclamar a {n}</h2>'
                f'<p>Primero reclama directamente a {n} por escrito, desde el formulario de reclamaciones de su web, con tu número de reserva y la tarjeta de embarque. '
                f'Pide expresamente la compensación del Reglamento (CE) 261/2004 además del reembolso o los gastos.</p>{claim}</div></section>')
    return (f'<section class="ref"><div class="wrap"><h2>What {n} pays: examples with real distances</h2>'
            f'<p class="lead">The amount depends on the flight distance, not the ticket price. Here are example {n} routes with the distance worked out the way the regulation requires (EU261 amounts):</p>'
            f'<div class="board"><table><thead><tr><th>Route</th><th>Distance</th><th>Compensation per passenger</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            f'<h2 style="margin-top:32px">How to claim from {n}</h2>'
            f'<p>Claim from {n} in writing first, through the claims form on its website, with your booking reference and boarding pass. '
            f'Ask explicitly for compensation under EU261 (or UK261) as well as any refund or expenses.</p>{claim}</div></section>')

# ---------------------------------------------------------------- airline claim sheet (data-driven, sourced)
AESA_CLAIM = "https://www.seguridadaerea.gob.es/index.php/es/ambitos/derechos-de-los-pasajeros/inicia-tu-reclamacion-con-aesa"
EURLEX = {"es": "https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32004R0261",
          "en": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32004R0261"}
UK_ADR_OK = {"AviationADR", "CEDR"}  # schemes approved by the CAA for airline disputes
GUIDES = {
    "es": [("/vuelo-cancelado-que-hacer/", "Vuelo cancelado: qué hacer"), ("/overbooking-compensacion/", "Overbooking"),
           ("/circunstancias-extraordinarias-vuelo/", "Circunstancias extraordinarias"), ("/huelgas-vuelos-espana/", "Huelgas"),
           ("/comparativa-empresas-reclamacion-vuelos/", "Reclamar tú o con una empresa"), ("/#preguntas", "Preguntas frecuentes")],
    "en": [("/en/flight-cancelled-what-to-do/", "Flight cancelled: what to do"), ("/en/denied-boarding-overbooking-compensation/", "Overbooking"),
           ("/en/extraordinary-circumstances-flight-delay/", "Extraordinary circumstances"), ("/en/flight-strikes-spain-europe/", "Strikes"),
           ("/en/flight-compensation-companies-compared/", "Claim yourself or use a company"), ("/en/uk-airports-to-spain-flight-delay-compensation/", "UK airports to Spain"),
           ("/en/#preguntas", "FAQ")],
}


def rules_rows(l, a):
    """Which rules apply to this airline's flights, by direction (Art. 3 Reg. 261/2004; CAA table for UK261)."""
    eu, uk = a["eu"], a["uk"]
    if l == "es":
        dep_eu = "Reglamento (CE) 261/2004, en euros, sea cual sea la aerolínea."
        if eu == "yes": in_eu = "Reglamento 261/2004: es una aerolínea comunitaria."
        elif eu == "mixed": in_eu = "Reglamento 261/2004 si lo operó su compañía europea; UK261 (en libras) si lo operó la británica."
        elif uk: in_eu = "No lo cubre el reglamento europeo, pero sí UK261 (en libras), por ser aerolínea británica."
        else: in_eu = "No está cubierto: ni el reglamento europeo ni UK261."
        dep_uk = "UK261, en libras, sea cual sea la aerolínea."
        in_uk = "UK261, en libras." if (eu in ("yes", "mixed") or uk) else "No está cubierto."
        head = ("Vuelo", "Norma que se aplica")
        labels = ("Sale de España, la UE, el EEE o Suiza", "Llega a la UE desde fuera de Europa", "Sale del Reino Unido", "Llega al Reino Unido desde fuera de Europa")
    else:
        dep_eu = "EU261, in euros, whatever the airline."
        if eu == "yes": in_eu = "EU261: it is an EU (Community) carrier."
        elif eu == "mixed": in_eu = "EU261 if its EU company operated it; UK261 (in pounds) if its UK company did."
        elif uk: in_eu = "Not EU261, but UK261 (in pounds) applies because it is a UK airline."
        else: in_eu = "Not covered by EU261 or UK261."
        dep_uk = "UK261, in pounds, whatever the airline."
        in_uk = "UK261, in pounds." if (eu in ("yes", "mixed") or uk) else "Not covered."
        head = ("Flight", "Rules that apply")
        labels = ("Departs Spain, the EU, the EEA or Switzerland", "Arrives in the EU from outside Europe", "Departs the UK", "Arrives in the UK from outside Europe")
    rows = "".join(f"<tr><td>{x}</td><td>{y}</td></tr>" for x, y in zip(labels, (dep_eu, in_eu, dep_uk, in_uk)))
    return f'<div class="board board-text"><table><thead><tr><th>{head[0]}</th><th>{head[1]}</th></tr></thead><tbody>{rows}</tbody></table></div>'


def airline_facts(l, a):
    n, eu, uk = e(a["name"]), a["eu"], a["uk"]
    claim = a.get("claim_" + l) or a.get("claim_es")
    note = a.get("note_" + l) or ""
    adr = a.get("adr_uk") if a.get("adr_uk") in UK_ADR_OK else None
    home_q = eu == "yes" or eu == "mixed" or uk
    if l == "es":
        q = [
            (f"¿{a['name']} cuenta como aerolínea europea para el reglamento?",
             {"yes": f"Sí. {a['name']} es una aerolínea de {a['country']} con licencia comunitaria, así que el reglamento también cubre sus vuelos que llegan a la UE desde fuera.",
              "mixed": f"Depende de la compañía del grupo que operó el vuelo ({a['country']}). Mira el código del vuelo en la tarjeta de embarque o pregúntalo a la aerolínea.",
              "no": f"No. {a['name']} es una aerolínea de {a['country']}. El reglamento europeo solo cubre sus vuelos que salen de la UE, el EEE o Suiza."}[eu]),
            (f"¿Dónde reclamo a {a['name']}?",
             f"En su canal oficial de reclamaciones (enlace más arriba), por escrito y guardando el justificante. {note}".strip()),
            (f"¿Y si mi vuelo con {a['name']} volvía a España desde fuera de Europa?",
             "Está cubierto por el reglamento europeo." if eu == "yes" else
             "Solo si lo operó su compañía europea; si lo operó la británica, se aplica UK261." if eu == "mixed" else
             "El reglamento europeo no lo cubre. Si es una aerolínea británica, puede aplicarse UK261." if uk else
             "No está cubierto por el reglamento europeo. Puede reclamarse el daño demostrado por el retraso según el Convenio de Montreal (art. 19)."),
        ]
        esc = (f'<li><strong>Vuelo que salió de España</strong> o que llegó a España desde fuera de la UE con aerolínea comunitaria: si {n} no responde en un mes o lo rechaza, '
               f'<a href="{AESA_CLAIM}" rel="noopener">reclama gratis ante AESA</a>. Tienes hasta un año desde tu reclamación a la aerolínea y su resolución es vinculante para la aerolínea.</li>'
               '<li><strong>Vuelo que salió de otro país de la UE</strong>: el organismo nacional de ese país.</li>'
               + (f'<li><strong>Vuelo que salió del Reino Unido</strong>: tras 8 semanas, {e(adr) + " (el organismo de resolución de conflictos al que está adherida)" if adr else "el organismo de resolución de conflictos de la aerolínea o, si no tiene, la CAA"}.</li>'))
        return (f'<section class="ref"><div class="wrap"><h2>Ficha para reclamar a {n}</h2>'
                f'<p><strong>Canal oficial:</strong> <a href="{e(claim)}" rel="nofollow noopener" target="_blank">reclamaciones de {n}</a>.{(" " + e(note)) if note else ""}</p>'
                f'<h3>Qué norma se aplica a los vuelos de {n}</h3>{rules_rows(l, a)}'
                f'<p class="lead">Cuenta la aerolínea que <em>operó</em> el vuelo, no la que vendió el billete. Fuente: art. 3 del <a href="{EURLEX["es"]}" rel="noopener">Reglamento (CE) 261/2004</a> y la <a href="{CAA_URL}" rel="noopener">CAA</a> para UK261.</p>'
                f'<h3>Si {n} no te paga</h3><ul>{esc}</ul>'
                f'<h3>Qué documentos preparar</h3><ul><li>Tarjeta de embarque y confirmación de la reserva.</li><li>Correos, SMS o avisos de {n} sobre el retraso o la cancelación, con su fecha.</li>'
                f'<li>El motivo que te dieron, mejor por escrito.</li><li>Tickets de comida, transporte u hotel que pagaste tú.</li></ul>'
                f'<h3>Plazos</h3><ul><li>En España, 5 años para reclamar a la aerolínea, según <a href="{AESA_URL}" rel="noopener">AESA</a>.</li>'
                f'<li>En Inglaterra y Gales, 6 años por vía judicial (Dawson contra Thomson, 2014).</li>'
                f'<li>En otros países decide su ley nacional (Tribunal de Justicia de la UE, asunto C-139/11).</li></ul>'
                f'<h3>Preguntas frecuentes sobre {n}</h3>' + "".join(f"<details><summary>{e(x)}</summary><p>{e(y)}</p></details>" for x, y in q)
                + '</div></section>')
    q = [
        (f"Does {a['name']} count as a European airline for EU261?",
         {"yes": f"Yes. {a['name']} is an airline from {a['country_en']} with an EU (Community) licence, so EU261 also covers its flights arriving in the EU from outside.",
          "mixed": f"It depends on which group company operated the flight ({a['country_en']}). Check the flight number on your boarding pass or ask the airline.",
          "no": f"No. {a['name']} is an airline from {a['country_en']}. EU261 only covers its flights departing the EU, the EEA or Switzerland."}[eu]),
        (f"Where do I claim from {a['name']}?",
         f"Through its official claims channel (link above), in writing, keeping proof that you sent it. {note}".strip()),
        (f"What about a {a['name']} flight into the UK from outside Europe?",
         "UK261 applies." if home_q else "It is not covered by UK261. Proven damage caused by the delay may be claimed under the Montreal Convention (Article 19)."),
    ]
    esc = (f'<li><strong>Flight departing the UK</strong>: after 8 weeks, {e(adr) + " (the dispute scheme it belongs to)" if adr else "the airline’s ADR scheme or, if it has none, the CAA"}.</li>'
           f'<li><strong>Flight departing Spain</strong>, or arriving in Spain from outside the EU with an EU airline: if {n} refuses or hasn’t replied within a month, '
           f'<a href="{AESA_CLAIM}" rel="noopener">claim for free with AESA</a> within a year of your claim to the airline; its decision binds the airline.</li>'
           '<li><strong>Flight departing another EU country</strong>: that country’s national enforcement body.</li>')
    return (f'<section class="ref"><div class="wrap"><h2>How to claim from {n}: key facts</h2>'
            f'<p><strong>Official channel:</strong> <a href="{e(claim)}" rel="nofollow noopener" target="_blank">{n} claims page</a>.{(" " + e(note)) if note else ""}</p>'
            f'<h3>Which rules cover {n} flights</h3>{rules_rows(l, a)}'
            f'<p class="lead">What counts is the airline that <em>operated</em> the flight, not the one that sold the ticket. Sources: Article 3 of <a href="{EURLEX["en"]}" rel="noopener">Regulation (EC) 261/2004</a> and the <a href="{CAA_URL}" rel="noopener">CAA</a> for UK261.</p>'
            f'<h3>If {n} won’t pay</h3><ul>{esc}</ul>'
            f'<h3>Documents to keep</h3><ul><li>Boarding pass and booking confirmation.</li><li>Emails, texts or notices from {n} about the delay or cancellation, with their dates.</li>'
            f'<li>The reason you were given, ideally in writing.</li><li>Receipts for food, transport or hotels you paid for.</li></ul>'
            f'<h3>Time limits</h3><ul><li>England and Wales: 6 years through the courts (Dawson v Thomson, 2014).</li>'
            f'<li>Spain: 5 years to claim from the airline, according to <a href="{AESA_URL}" rel="noopener">AESA</a>.</li>'
            f'<li>Elsewhere, national law decides (Court of Justice of the EU, Case C-139/11).</li></ul>'
            f'<h3>{n}: frequently asked questions</h3>' + "".join(f"<details><summary>{e(x)}</summary><p>{e(y)}</p></details>" for x, y in q)
            + '</div></section>')


def compact_refs(l):
    """Internal links shared by airline and airport pages, without repeating the generic rules blocks."""
    links = "".join(f'<li><a href="{u_airline(l, a)}">{e(a["name"])}</a></li>' for a in AIRLINES)
    aps = "".join(f'<li><a href="{u_airport(l, ap)}">{e(ap[2] if l == "es" else ap[3])}</a></li>' for ap in ES_AIRPORTS)
    guides_ = " · ".join(f'<a href="{u}">{t}</a>' for u, t in GUIDES[l])
    if l == "es":
        return (f'<section class="ref" id="aerolineas"><div class="wrap"><h2>Guías para reclamar</h2><p>{guides_}</p>'
                f'<h2 style="margin-top:32px">Compensación por aerolínea</h2><ul class="airlines">{links}</ul>'
                f'<h2 style="margin-top:32px">Vuelos que salen de aeropuertos españoles</h2><ul class="airlines">{aps}</ul></div></section>')
    ukl = "".join(f'<li><a href="{uk_airports.u_uk(s)}">{e(nm)}</a></li>' for _, s, nm, _ in uk_airports.UK)
    return (f'<section class="ref" id="aerolineas"><div class="wrap"><h2>Claim guides</h2><p>{guides_}</p>'
            f'<h2 style="margin-top:32px">Compensation by airline</h2><ul class="airlines">{links}</ul>'
            f'<h2 style="margin-top:32px">Flights from Spanish airports</h2><ul class="airlines">{aps}</ul>'
            f'<h2 style="margin-top:32px">Flights from UK airports to Spain</h2><ul class="airlines">{ukl}</ul></div></section>')


def airport_claim(l, name, code):
    n = e(name)
    if l == "es":
        return (f'<section class="ref"><div class="wrap"><h2>Dónde reclamar un vuelo de {n}</h2><ol class="steps">'
                f'<li>Reclama primero a la aerolínea que operó el vuelo, por escrito, con la tarjeta de embarque y la reserva.</li>'
                f'<li>Si no responde en un mes o lo rechaza: los vuelos que salen de {n} ({code}) se reclaman gratis ante <a href="{AESA_CLAIM}" rel="noopener">AESA</a>, hasta un año después de tu reclamación a la aerolínea. '
                f'También los que llegan a {n} desde fuera de la UE con una aerolínea comunitaria.</li>'
                f'<li>Si llegaste a {n} desde el Reino Unido, se aplica UK261: reclama al organismo de resolución de conflictos de la aerolínea o a la <a href="{CAA_URL}" rel="noopener">CAA</a>.</li></ol>'
                f'<p class="lead">Plazo para reclamar a la aerolínea en España: 5 años, según AESA. Fuente de las normas: <a href="{EURLEX["es"]}" rel="noopener">Reglamento (CE) 261/2004</a>, arts. 3, 7 y 16.</p></div></section>')
    return (f'<section class="ref"><div class="wrap"><h2>Where to claim a flight from {n}</h2><ol class="steps">'
            f'<li>Claim from the airline that operated the flight first, in writing, with your boarding pass and booking.</li>'
            f'<li>If it refuses or hasn’t replied within a month: flights departing {n} ({code}) can go to <a href="{AESA_CLAIM}" rel="noopener">AESA</a> for free, within a year of your claim to the airline. '
            f'So can flights into {n} from outside the EU on an EU airline.</li>'
            f'<li>Flights from the UK into {n} fall under UK261: after 8 weeks, use the airline’s ADR scheme or the <a href="{CAA_URL}" rel="noopener">CAA</a>.</li></ol>'
            f'<p class="lead">Time limit to claim from the airline in Spain: 5 years, according to AESA; in England and Wales, 6 years. Rules: <a href="{EURLEX["en"]}" rel="noopener">Regulation (EC) 261/2004</a>, Articles 3, 7 and 16.</p></div></section>')


def extra_jsonld(l, title, path):
    home = u_home(l)
    if path == home:
        data = [{"@context": "https://schema.org", "@type": "WebApplication", "name": ("Calculadora de compensación por retraso de vuelo" if l == "es" else "Flight delay compensation calculator"),
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
            f"{h}</style>\n{GA4}{ADSENSE}</head>\n<body>{b}{CONSENT}</body></html>\n")


GA_ID = "G-6JRCZVTNDG"
TP_SRC = "https://emrldtp.cc/NTgyNjYx.js?t=582661"  # Travelpayouts (same identifier as before)
# Before consent only the consent defaults are defined: gtag.js, the GA config and the Travelpayouts script are not loaded,
# so no request reaches Google Analytics or Travelpayouts until the visitor accepts (checked in test_navegador.js).
GA4 = ("<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
       "gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied'});</script>\n")

CONSENT = ("<div id=\"ck\" role=\"dialog\" aria-live=\"polite\" aria-label=\"Cookies\" style=\"display:none;position:fixed;left:12px;right:12px;bottom:12px;z-index:9999;max-width:560px;margin:0 auto;background:#111827;color:#fff;"
           "border-radius:12px;padding:14px 16px;font:14px/1.4 system-ui,sans-serif;box-shadow:0 8px 30px rgba(0,0,0,.3)\">"
           "<span id=\"ckt\"></span> <a id=\"ckl\" href=\"/privacidad/\" style=\"color:#facc15\">+info</a>"
           "<div style=\"margin-top:10px;display:flex;gap:8px;justify-content:flex-end\">"
           "<button id=\"ckn\" style=\"background:#facc15;color:#111827;border:0;border-radius:8px;padding:8px 14px;font-weight:700;cursor:pointer\"></button>"
           "<button id=\"cky\" style=\"background:#facc15;color:#111827;border:0;border-radius:8px;padding:8px 14px;font-weight:700;cursor:pointer\"></button></div></div>"
           "<script>(function(){var en=document.documentElement.lang==='en',k='vc_consent',ID='" + GA_ID + "',on=false,b=document.getElementById('ck');"
           "function get(){try{return localStorage.getItem(k)}catch(e){return null}}"
           "function put(v){try{localStorage.setItem(k,v)}catch(e){}}"
           "function add(src){var s=document.createElement('script');s.async=true;s.src=src;document.head.appendChild(s)}"
           "function start(){if(on)return;on=true;window['ga-disable-'+ID]=false;"
           "gtag('consent','update',{analytics_storage:'granted'});gtag('js',new Date());"
           "gtag('config',ID,{allow_google_signals:false,allow_ad_personalization_signals:false});"
           "add('https://www.googletagmanager.com/gtag/js?id='+ID);add('" + TP_SRC + "');window.vcAnalytics=true}"
           "function stop(){window.vcAnalytics=false;window['ga-disable-'+ID]=true;gtag('consent','update',{analytics_storage:'denied'});"
           "document.cookie.split(';').forEach(function(c){var n=c.split('=')[0].trim();if(/^_ga/.test(n)){['',location.hostname,'.'+location.hostname.replace(/^www\\./,'')].forEach(function(d){document.cookie=n+'=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/'+(d?';domain='+d:'')})}})}"
           "function show(){document.getElementById('ckt').textContent=en?'With your permission we use cookies to count visits and see which parts of the calculator are used, including clicks to the claims service. We never send what you type in the calculator or the letter.':"
           "'Con tu permiso usamos cookies para contar visitas y saber qué partes de la calculadora se usan, incluidos los clics al servicio de reclamación. Nunca enviamos lo que escribes en la calculadora ni en la carta.';"
           "document.getElementById('ckl').href=en?'/en/privacy/':'/privacidad/';"
           "document.getElementById('cky').textContent=en?'Accept':'Aceptar';document.getElementById('ckn').textContent=en?'Reject':'Rechazar';b.style.display='block'}"
           "document.getElementById('cky').onclick=function(){put('y');b.style.display='none';start()};"
           "document.getElementById('ckn').onclick=function(){put('n');b.style.display='none';if(on){stop();on=false}};"
           "document.addEventListener('click',function(e){var t=e.target.closest&&e.target.closest('[data-consent-open]');if(t){e.preventDefault();show()}});"
           "var v=get();if(v==='y')start();else if(!v)show()})();</script>\n")

ADSENSE_PUB = "ca-pub-1079386437086971"
ADSENSE = ('<meta name="msvalidate.01" content="D3B289B2220FF34999D4248924B46B3C">\n'
           f'<meta name="google-adsense-account" content="{ADSENSE_PUB}">\n'
           f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB}" crossorigin="anonymous"></script>\n')

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(content)


def out(path):
    return os.path.join(OUT, path.strip("/"), "index.html") if path != "/" else os.path.join(OUT, "index.html")


# ---------------------------------------------------------------- build
def _content_hash(doc):
    """Hash of what a reader sees (title, description, main content): lastmod only changes when this changes."""
    import hashlib
    parts = [re.search(r"<title>.*?</title>", doc, re.S), re.search(r'<meta name="description"[^>]*>', doc), re.search(r"<main.*?</main>", doc, re.S)]
    return hashlib.sha256("".join(m.group(0) for m in parts if m).encode()).hexdigest()


def _previous_lastmod():
    """lastmod and content hash of the pages currently in OUT (the committed site), read before rebuilding."""
    prev = {}
    try:
        sm = open(os.path.join(OUT, "sitemap.xml"), encoding="utf-8").read()
    except OSError:
        return prev
    for loc, lm in re.findall(r"<loc>" + re.escape(SITE_URL) + r"([^<]+)</loc><lastmod>([^<]+)</lastmod>", sm):
        try:
            prev[loc] = (lm, _content_hash(open(out(loc), encoding="utf-8").read()))
        except OSError:
            pass
    return prev


def build():
    import datetime
    previous = _previous_lastmod()
    today = os.environ.get("BUILD_DATE") or datetime.date.today().isoformat()
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
                    scope = (f"{n} es una aerolínea de {e(a['country'])}, fuera de la UE. El reglamento europeo cubre sus vuelos que salen de la UE, el EEE o Suiza, pero no los que llegan a la UE desde fuera."
                             + (" Sus vuelos que salen del Reino Unido, o que llegan allí desde fuera, se rigen por la norma británica UK261." if a["uk"] else ""))
                title = f"Compensación por retraso de {a['name']}: cuánto te toca" if len(a["name"]) <= 14 else f"Reclamar a {a['name']}: retraso y cancelación"
                desc = f"Retraso de 3 horas o más, cancelación u overbooking con {a['name']}: calcula si te pueden corresponder 250, 400 o 600 €, dónde reclamar y qué plazos hay."
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
                title = f"{a['name']} delay compensation: how much you can claim" if len(a["name"]) <= 14 else f"{a['name']} delay and cancellation compensation"
                desc = f"{a['name']} flight 3+ hours late, cancelled or overbooked? Check if you could claim up to €600 (EU261) or £520 (UK261), where to claim and time limits."
                h1 = f"{n} flight delayed or cancelled? Check what you're owed"
                lede = scope + " Enter your flight and we'll work out the amount."
            deep = ""
            if l == "en" and a["slug"] in uk_deep.META:
                m = uk_deep.META[a["slug"]]
                title, desc, h1 = m["title"], m["desc"], e(m["h1"])
                deep = uk_deep.section(a, AIRPORTS, km, NAMES["en"], AESA_URL, CAA_URL)
            body = hero(l, h1, lede, a["slug"], dep, arr) + deep + airline_section(l, a) + airline_facts(l, a) + compact_refs(l)
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
                title = f"Retraso vuelo aeropuerto {name_es.split('-')[0]}: cuánto te toca" if len(name_es) < 22 else f"Vuelo retrasado en {name_es}: compensación"
                desc = f"Calcula la compensación por un vuelo retrasado, cancelado o con overbooking en el aeropuerto de {name_es}: 250, 400 o 600 € por pasajero."
                h1 = f"Vuelo retrasado en {n}: calcula cuánto te toca"
                dep, arr = code, ("LHR" if code == "MAD" else "MAD")
                body = hero(l, h1, lede, "", dep, arr) + route_table(l, code, name_es) + airport_claim(l, name_es, code) + compact_refs(l)
            else:
                n = e(name_en)
                extra = " The Canary Islands count as part of the EU for these rules, exactly like mainland Spain." if code in CANARY else ""
                lede = (f"Every flight departing {n} airport is covered by EU261, whatever the airline, and pays up to €600.{extra} "
                        f"Flights from the UK into {n} are covered by UK261 and pay up to £520. Enter your flight and we'll work out the amount.")
                title = f"{name_en.split('-')[0].split(' (')[0]} airport flight delay compensation"
                desc = f"Delayed or cancelled flight at {name_en} airport? Check your compensation under EU261 or UK261: up to €600 or £520 per passenger."
                h1 = f"Flight delayed at {n} airport? Check what you're owed"
                dep, arr = code, ("LHR" if code != "MAN" else "LGW")
                body = hero(l, h1, lede, "", dep, "MAN") + route_table(l, code, name_en) + airport_claim(l, name_en, code) + compact_refs(l)
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
            "es": ("Política de privacidad", "<p>Las calculadoras funcionan en tu navegador: los datos de tu vuelo no se envían ni se guardan en nuestros servidores. Los datos que escribes para la carta de reclamación (nombre, código de reserva, número y fecha del vuelo, número de pasajeros) solo se usan en tu navegador para componer el texto: no se envían a nadie, no se guardan y desaparecen al cerrar la página. No pedimos datos bancarios.</p><h2 id=\"cookies\">Cookies y medición</h2><p>Solo si aceptas en el aviso de cookies, la web carga Google Analytics y el script de afiliación de Travelpayouts. Antes de aceptar, o si rechazas, no se cargan ni se les envía nada. Con tu permiso medimos de forma agregada: visitas, que se ha empezado y completado la calculadora, el tipo de incidencia (retraso, cancelación u overbooking), el resultado y el tramo de importe estimado, la apertura, copia o descarga de la carta y los clics en el enlace al servicio de reclamación. Nunca enviamos tu nombre, código de reserva, número de vuelo ni nada de lo que escribes. Las señales de Google y la personalización de anuncios de Analytics están desactivadas. Puedes cambiar tu elección cuando quieras en el enlace «Cookies» del pie de página.</p><p>Al pulsar un enlace de afiliado, el servicio de reclamación (por ejemplo, AirHelp, a través de Travelpayouts) puede usar cookies para registrar que vienes de esta web. La web muestra anuncios de Google AdSense: Google y sus socios pueden usar cookies para mostrar anuncios, personalizados o no según lo que elijas en el aviso de consentimiento. Más información en <a href=\"https://policies.google.com/technologies/ads?hl=es\" rel=\"noopener\">cómo usa Google las cookies en publicidad</a>.</p><p>Responsable: <strong>Salvador Fernández Lloris</strong>. Contacto: <strong>vuelosclaim@gmail.com</strong>.</p>"),
            "en": ("Privacy policy", "<p>The calculators run in your browser: your flight details are not sent to or stored on our servers. The details you type for the claim letter (name, booking reference, flight number and date, number of passengers) are only used in your browser to put the text together: they are not sent to anyone, not stored, and disappear when you close the page. We do not ask for bank details.</p><h2 id=\"cookies\">Cookies and measurement</h2><p>Only if you accept in the cookie notice does the site load Google Analytics and the Travelpayouts affiliate script. Before you accept, or if you reject, they are not loaded and nothing is sent to them. With your permission we measure, in aggregate: visits, that the calculator was started and completed, the type of problem (delay, cancellation or overbooking), the result and the estimated amount band, opening, copying or downloading the letter, and clicks on the link to the claims service. We never send your name, booking reference, flight number or anything you type. Google signals and ad personalisation in Analytics are switched off. You can change your choice at any time with the “Cookies” link at the bottom of the page.</p><p>When you click an affiliate link, the claims service (for example, AirHelp, via Travelpayouts) may use cookies to record that you came from this site. The site shows Google AdSense ads: Google and its partners may use cookies to serve ads, personalised or not depending on your choice in the consent notice. More at <a href=\"https://policies.google.com/technologies/ads\" rel=\"noopener\">how Google uses cookies in advertising</a>.</p><p>Controller: <strong>Salvador Fernández Lloris</strong>. Contact: <strong>vuelosclaim@gmail.com</strong>.</p>"),
        },
    }
    LEGAL_DESC = {
        "about": {"es": "Quién está detrás de VuelosClaim, cómo calculamos la compensación por retraso o cancelación de vuelos y qué fuentes oficiales usamos.",
                  "en": "Who runs VuelosClaim, how we calculate flight delay and cancellation compensation, and the official sources we rely on."},
        "legal": {"es": "Aviso legal de VuelosClaim: titular del sitio, contacto, carácter orientativo de las calculadoras y enlaces de afiliado.",
                  "en": "VuelosClaim legal notice: site owner, contact details, the indicative nature of the calculators and affiliate links."},
        "privacy": {"es": "Política de privacidad de VuelosClaim: qué datos se usan en la calculadora y la carta, cookies de analítica y anuncios, y contacto.",
                    "en": "VuelosClaim privacy policy: what data the calculator and claim letter use, analytics and advertising cookies, and contact details."},
    }
    for key, langs in legal_txt.items():
        alts = LEGAL[key]
        for l, (t, txt) in langs.items():
            other = "en" if l == "es" else "es"
            emit(l, alts[l], f"{head(l, t + ' · ' + BRAND, LEGAL_DESC[key][l], alts[l], alts)}\n{header(l, alts[other])}<main class=\"wrap prose\"><h1>{t}</h1>{txt}</main>{footer(l)}")

    def lastmod(u):
        h = _content_hash(open(out(u), encoding="utf-8").read())
        old = previous.get(u)
        return old[0] if old and old[1] == h else today
    sm = "".join(f"<url><loc>{SITE_URL}{u}</loc><lastmod>{lastmod(u)}</lastmod></url>" for u in urls)
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
