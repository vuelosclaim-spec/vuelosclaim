#!/usr/bin/env python3
"""Pruebas del sitio generado (docs/) y de los datos, solo con la librería estándar.

Uso: python3 fuente/tests/test_sitio.py [carpeta_del_sitio]
Errores (rompen la validación): enlaces internos rotos, canonical, hreflang, JSON-LD, sitemap, H1, datos.
Avisos (no rompen): títulos > 65 caracteres y descripciones > 165.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FUENTE = os.path.dirname(HERE)
SITE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(os.path.dirname(FUENTE), "docs")
BASE = "https://vuelosclaim.eu"
NOINDEX_OK = {"/widget/", "/404.html"}  # widget para incrustar: noindex a propósito, sin H1 ni canonical

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def load_site():
    pages, files = {}, set()
    for dp, _, fn in os.walk(SITE):
        for f in fn:
            rel = "/" + os.path.relpath(os.path.join(dp, f), SITE).replace(os.sep, "/")
            files.add(rel)
            if f.endswith(".html"):
                url = rel[: -len("index.html")] if rel.endswith("/index.html") else rel
                with open(os.path.join(dp, f), encoding="utf-8") as fh:
                    pages[url] = fh.read()
    return pages, files


def check_site():
    pages, files = load_site()
    if len(pages) < 100:
        err(f"Solo hay {len(pages)} páginas en {SITE}: ¿se ha generado el sitio?")
    sitemap = set(re.findall(r"<loc>" + re.escape(BASE) + r"([^<]+)</loc>", open(os.path.join(SITE, "sitemap.xml"), encoding="utf-8").read()))
    titles, descs = {}, {}
    for url, s in pages.items():
        for href in re.findall(r'href="(/[^"#?]*)', s):
            if href not in pages and href not in files:
                err(f"Enlace interno roto en {url}: {href}")
        if 'id="l-iban"' in s or re.search(r"IBAN", s):
            err(f"La página {url} todavía pide o menciona el IBAN")
        if 'id="calc"' in s:
            m = re.search(r'"dataUrl": "([^"]+)"', s)
            if not m or (m.group(1) if m.group(1).startswith("/") else "/" + m.group(1)) not in files:
                err(f"La calculadora de {url} apunta a una lista de aeropuertos inexistente: {m.group(1) if m else 'ninguna'}")
            if 'id="ac-retry"' not in s:
                err(f"La calculadora de {url} no tiene botón para reintentar la carga")
        if url in NOINDEX_OK:
            continue
        t = re.search(r"<title>(.*?)</title>", s, re.S)
        d = re.search(r'<meta name="description" content="([^"]*)"', s)
        if not t:
            err(f"Sin <title>: {url}")
        else:
            titles.setdefault(t.group(1), []).append(url)
            if len(html.unescape(t.group(1))) > 65:
                warnings.append(f"Título de {len(html.unescape(t.group(1)))} caracteres: {url}")
        if not d:
            err(f"Sin meta description: {url}")
        else:
            descs.setdefault(d.group(1), []).append(url)
            if len(html.unescape(d.group(1))) > 165:
                warnings.append(f"Descripción de {len(html.unescape(d.group(1)))} caracteres: {url}")
        can = re.search(r'<link rel="canonical" href="([^"]+)"', s)
        if not can or can.group(1) != BASE + url:
            err(f"Canonical incorrecto en {url}: {can.group(1) if can else 'ninguno'}")
        if len(re.findall(r"<h1[\s>]", s)) != 1:
            err(f"No hay exactamente un H1 en {url}")
        for lang, target in re.findall(r'hreflang="([^"]+)" href="' + re.escape(BASE) + r'([^"]+)"', s):
            if target not in pages:
                err(f"hreflang {lang} de {url} apunta a una página inexistente: {target}")
            elif lang != "x-default" and url not in re.findall(r'hreflang="[^"]+" href="' + re.escape(BASE) + r'([^"]+)"', pages[target]):
                err(f"hreflang no recíproco: {url} -> {target}")
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                json.loads(block)
            except ValueError as e:
                err(f"JSON-LD inválido en {url}: {e}")
        if url not in sitemap and "noindex" not in s:
            err(f"Página indexable fuera del sitemap: {url}")
    # Datos estructurados FAQ: cada pregunta debe estar visible en la página (requisito de Google)
    for url, s in pages.items():
        visible = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", s, flags=re.S)))
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                data = json.loads(block)
            except ValueError:
                continue
            for d in (data if isinstance(data, list) else [data]):
                if d.get("@type") == "FAQPage":
                    for q in d.get("mainEntity", []):
                        if q.get("name") not in visible:
                            err(f"Pregunta del marcado FAQ no visible en {url}: {q.get('name')}")
        if len(re.findall(r'"@type": "WebSite"', s)) > 1:
            err(f"Más de un WebSite en los datos estructurados de {url}")
    # lastmod: fecha ISO válida y no futura
    import datetime
    sm_txt = open(os.path.join(SITE, "sitemap.xml"), encoding="utf-8").read()
    for lm in re.findall(r"<lastmod>([^<]+)</lastmod>", sm_txt):
        try:
            if datetime.date.fromisoformat(lm) > datetime.date.today() + datetime.timedelta(days=1):
                err(f"lastmod en el futuro: {lm}")
        except ValueError:
            err(f"lastmod no válido: {lm}")
    # Accesibilidad: el enlace «Saltar al contenido» de cada página tiene destino, y el aviso de cookies no es un diálogo sin foco
    for url, s in pages.items():
        if 'href="#main"' in s and 'id="main"' not in s:
            err(f"{url}: el enlace para saltar al contenido no tiene destino (#main)")
        if 'id="ck" role="dialog"' in s:
            err(f"{url}: el aviso de cookies usa role=dialog sin gestionar el foco")
    # Rendimiento: fuentes propias (sin petición bloqueante a Google Fonts), AdSense diferido y aeropuertos del ejemplo incrustados
    fonts_dir = os.path.join(SITE, "fonts")
    for url, s in pages.items():
        if "fonts.googleapis.com" in s:
            err(f"{url}: vuelve a cargar Google Fonts desde fuera (bloquea el renderizado)")
        for fn in set(re.findall(r"/fonts/([\w.-]+\.woff2)", s)):
            if not os.path.exists(os.path.join(fonts_dir, fn)):
                err(f"{url}: fuente inexistente /fonts/{fn}")
        if len(re.findall(r'rel="preload"[^>]*as="font"', s)) > 2:
            err(f"{url}: más de 2 fuentes precargadas")
        if re.search(r'<script[^>]+src="https://pagead2\.googlesyndication\.com', s):
            err(f"{url}: AdSense se carga con una etiqueta directa en vez del cargador diferido")
        if 'id="calc"' in s and '"seed": [[' not in s:
            err(f"{url}: la calculadora no lleva incrustados los aeropuertos del ejemplo")
    # Huelgas: cada fila con fecha de fin para ocultarla cuando pase
    for url in ("/huelgas-vuelos-espana/", "/en/flight-strikes-spain-europe/"):
        if url in pages and re.search(r"<tbody><tr>|</tr><tr>", pages[url]):
            err(f"Hay huelgas sin fecha de fin (data-end) en {url}")
    # AdSense: nunca en el widget (se inserta en webs ajenas) ni en la 404; donde se carga, enlace para gestionar el consentimiento publicitario
    for url, s in pages.items():
        has_ads = "adsbygoogle.js" in s
        if url in ("/widget/", "/404.html") and has_ads:
            err(f"{url} no debe cargar AdSense")
        if has_ads and "data-ads-consent" not in s:
            err(f"{url} carga AdSense sin enlace para gestionar el consentimiento publicitario")
    nf = pages.get("/404.html", "")
    if not nf or 'name="robots" content="noindex"' not in nf or "/404.html" in sitemap:
        err("Falta la página 404 propia, no es noindex o está en el sitemap")
    for url in sitemap:
        if url not in pages:
            err(f"El sitemap incluye una página que no existe: {url}")
    for kind, seen in (("Título", titles), ("Descripción", descs)):
        for text, urls in seen.items():
            if len(urls) > 1:
                err(f"{kind} duplicado en {', '.join(urls)}")
    return len(pages)


def check_data():
    airports = {a[0] for a in json.load(open(os.path.join(FUENTE, "data", "airports.min.json"), encoding="utf-8"))}
    airlines = json.load(open(os.path.join(FUENTE, "data", "airlines.json"), encoding="utf-8"))
    slugs = [a["slug"] for a in airlines]
    for s in {x for x in slugs if slugs.count(x) > 1}:
        err(f"Aerolínea repetida: {s}")
    for a in airlines:
        for key in ("slug", "name", "eu", "uk"):
            if key not in a:
                err(f"Aerolínea {a.get('slug')} sin campo {key}")
        if a.get("eu") not in ("yes", "no", "mixed", "unknown"):
            err(f"Aerolínea {a['slug']}: valor eu no válido ({a.get('eu')})")
        for key in ("claim_es", "claim_en"):
            if not str(a.get(key, "")).startswith("https://"):
                err(f"Aerolínea {a['slug']}: {key} debe empezar por https://")
    # Cada página de aerolínea enlaza su canal oficial y explica plazos y fuentes
    pages, _ = load_site()
    for a in airlines:
        for l, u in (("es", f"/compensacion-retraso-{a['slug']}/"), ("en", f"/en/{a['slug']}-delay-compensation/")):
            pg = pages.get(u, "")
            if html.escape(a["claim_" + l]) not in pg and a["claim_" + l] not in pg:
                err(f"{u} no enlaza el canal oficial de {a['name']}")
            if ("Plazos" if l == "es" else "Time limits") not in pg or "eur-lex.europa.eu" not in pg:
                err(f"{u} no muestra plazos o la fuente legal")
    # El canal oficial no puede ser la portada corporativa (error corregido: Binter, World2fly, Iberia Express).
    # Excepción: subdominios dedicados solo a reclamaciones.
    HOME_OK = {"eu261expenseclaim.ryanair.com"}
    for a in airlines:
        for key in ("claim_es", "claim_en"):
            m = re.fullmatch(r"https://([^/]+)/?([a-z]{2}(-[a-z]{2})?/?)?", a[key])
            if m and m.group(1) not in HOME_OK:
                err(f"Aerolínea {a['slug']}: {key} es una portada, no una página de reclamaciones ({a[key]})")
    # Fichas comprobadas en la web oficial (data/airline_claims.json): fecha, fuentes, ES/EN sincronizados y visibles
    claims = {k: v for k, v in json.load(open(os.path.join(FUENTE, "data", "airline_claims.json"), encoding="utf-8")).items() if not k.startswith("_")}
    for slug, c in claims.items():
        if slug not in slugs:
            err(f"airline_claims.json: aerolínea inexistente {slug}")
            continue
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", c.get("checked", "")):
            err(f"airline_claims.json: {slug} sin fecha de comprobación")
        if not c.get("sources") or not c.get("forms"):
            err(f"airline_claims.json: {slug} sin fuentes o sin canal")
        for x in c.get("sources", []) + c.get("forms", []):
            if not x["url"].startswith("https://"):
                err(f"airline_claims.json: {slug} con URL no segura {x['url']}")
        for part in ("steps", "follow"):
            if len(c.get(part + "_es", [])) != len(c.get(part + "_en", [])):
                err(f"airline_claims.json: {slug} con {part} distinto en español e inglés")
        if bool(c.get("caveat_es")) != bool(c.get("caveat_en")):
            err(f"airline_claims.json: {slug} con aviso solo en un idioma")
        for l, u, h in (("es", f"/compensacion-retraso-{slug}/", "paso a paso"), ("en", f"/en/{slug}-delay-compensation/", "step by step")):
            pg = pages.get(u, "")
            if h not in pg:
                err(f"{u} no muestra la ficha paso a paso comprobada")
            for f in c["forms"]:
                if html.escape(f["url"]) not in pg and f["url"] not in pg:
                    err(f"{u} no enlaza {f['url']}")
            for x in c["steps_" + l]:
                if html.escape(x, quote=False) not in pg and html.escape(x) not in pg:
                    err(f"{u} no muestra el paso: {x[:50]}")
    # Ningún texto con estadísticas o tiempos inventados: los plazos de respuesta solo si se atribuyen a la aerolínea
    for slug, c in claims.items():
        for l in ("es", "en"):
            for x in c["follow_" + l]:
                if re.search(r"\d+ (días|days|semanas|weeks)", x) and not re.search(r"(indica|publica|says|states)", x):
                    err(f"airline_claims.json: {slug} da un plazo sin atribuirlo a la aerolínea: {x[:60]}")
    sys.path.insert(0, FUENTE)
    import build  # noqa: E402  (solo lee datos; no genera el sitio)
    for slug, routes in build.AL_ROUTES.items():
        if slug not in slugs:
            err(f"AL_ROUTES tiene rutas de una aerolínea que no existe: {slug}")
        for o, d in routes:
            for code in (o, d):
                if code not in airports:
                    err(f"Ruta de {slug} con aeropuerto desconocido: {code}")
    return len(airlines)


if __name__ == "__main__":
    n_pages = check_site()
    n_airlines = check_data()
    for w in warnings:
        print("AVISO ", w)
    for e in errors:
        print("ERROR ", e)
    print(f"\nSitio: {n_pages} páginas, {n_airlines} aerolíneas; {len(errors)} errores, {len(warnings)} avisos")
    sys.exit(1 if errors else 0)
