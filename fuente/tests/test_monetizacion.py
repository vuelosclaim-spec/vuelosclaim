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

# Protección de confianza: cualquier comparativa monetizada tiene que dejar clara
# la comisión de afiliado y ofrecer una vía para reclamar sin intermediario.
for rel, disclosure, diy in (
    ("comparativa-empresas-reclamacion-vuelos/index.html", "comisión de afiliado", "Calcular y reclamar gratis"),
    ("en/flight-compensation-companies-compared/index.html", "affiliate commission", "Calculate and claim for free"),
):
    page = DOCS / rel
    if not page.is_file():
        errors.append(f"Falta la comparativa: {rel}")
        continue
    content = page.read_text(encoding="utf-8")
    if disclosure not in content:
        errors.append(f"{rel}: falta transparencia sobre la comisión de afiliación")
    if diy not in content:
        errors.append(f"{rel}: falta la alternativa de reclamación gratuita")
    if ("Dos formas de reclamar: tú decides" if rel.startswith("comparativa-") else "Two ways to claim: your choice") not in content:
        errors.append(f"{rel}: falta el texto comparativo de las dos vías de reclamación")


# La calculadora debe mantener visible la alternativa gratuita junto a AirHelp.
# El servicio externo nunca debe ser la única vía ofrecida al pasajero.
for rel in ("index.html", "en/index.html"):
    page = DOCS / rel
    if not page.is_file():
        errors.append(f"Falta la portada: {rel}")
        continue
    content = page.read_text(encoding="utf-8")
    for marker in ('data-cta', 'id="letter-open"', 'rel="sponsored nofollow noopener"'):
        if marker not in content:
            errors.append(f"{rel}: falta opción de reclamación o enlace seguro ({marker})")
    if "data-generic=" not in content:
        errors.append(f"{rel}: falta texto neutral para otros proveedores")


for error in errors:
    print("ERROR:", error)
print(f"Auditoría de monetización: {pages} HTML, {count} enlaces sponsored, {len(errors)} errores")
print("Nota: no valida redirecciones, atribución ni comisiones reales de Travelpayouts.")
sys.exit(bool(errors))
