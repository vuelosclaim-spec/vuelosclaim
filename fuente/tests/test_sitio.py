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
NOINDEX_OK = {"/widget/"}  # widget para incrustar: noindex a propósito, sin H1 ni canonical

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
