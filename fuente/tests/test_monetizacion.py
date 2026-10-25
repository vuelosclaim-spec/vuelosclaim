#!/usr/bin/env python3
"""Auditoría offline de enlaces de afiliación de docs/. No mide conversiones reales."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import sys

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
JS = ROOT / "fuente/src/app.js"
errors = []
count = 0
pages = 0

class Links(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
    def handle_starttag(self, tag, attrs):
        global count
        if tag != "a":
            return
        a = dict(attrs)
        rel = set((a.get("rel") or "").lower().split())
        if "sponsored" not in rel:
            return
        count += 1
        url = a.get("href") or ""
        parsed = urlsplit(url)
        if parsed.scheme != "https" or not parsed.hostname:
            errors.append(f"{self.path}: enlace sponsored sin HTTPS válido: {url}")
        if parsed.username or parsed.password:
            errors.append(f"{self.path}: el enlace incluye credenciales")
        if "nofollow" not in rel:
            errors.append(f"{self.path}: falta rel=nofollow")
        if a.get("target") == "_blank" and "noopener" not in rel:
            errors.append(f"{self.path}: enlace externo sin noopener")

if not DOCS.is_dir():
    errors.append("No existe docs/; generar primero la web")
else:
    for file in DOCS.rglob("*.html"):
        pages += 1
        parser = Links(file.relative_to(ROOT))
        try:
            parser.feed(file.read_text(encoding="utf-8"))
        except (ValueError, UnicodeError) as exc:
            errors.append(f"{file}: HTML ilegible: {exc}")

if not JS.is_file() or 'track("affiliate_click"' not in JS.read_text(encoding="utf-8"):
    errors.append("No se encuentra el evento affiliate_click en la calculadora")
if count == 0:
    errors.append("No se ha detectado ningún enlace sponsored; revisar monetización")

for error in errors:
    print("ERROR:", error)
print(f"Auditoría de monetización: {pages} HTML, {count} enlaces sponsored, {len(errors)} errores")
print("Nota: no valida redirecciones, atribución ni comisiones reales de Travelpayouts.")
sys.exit(bool(errors))
