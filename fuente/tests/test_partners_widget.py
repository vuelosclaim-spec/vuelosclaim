#!/usr/bin/env python3
"""Registro de socios y widgets con marca (VuelosClaim Partners).

Comprueba que el registro rechaza datos peligrosos o inválidos, que la paleta generada cumple
el contraste AA en modo claro y oscuro para cualquier color, y que cada página de socio
generada en docs/ es noindex, está fuera del sitemap y mantiene la atribución y el aviso de afiliación.
"""
from html import escape
from pathlib import Path
import os
import random
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "fuente"))
import partners_registry as R  # noqa: E402

errors = []


def bad(entry, why):
    try:
        R.validate([entry])
        errors.append(f"debería rechazarse ({why}): {entry}")
    except ValueError:
        pass


ok = {"id": "agencia-sol", "name": "Viajes Sol", "color": "#c0392b", "lang": "es", "logo": None, "demo": False}
try:
    R.validate([ok])
except ValueError as ex:
    errors.append(f"entrada válida rechazada: {ex}")

bad({**ok, "id": "Agencia"}, "mayúsculas en id")
bad({**ok, "id": "../x"}, "id con ruta")
bad({**ok, "id": "-x"}, "id que empieza por guion")
bad({**ok, "name": "<script>alert(1)</script>"}, "HTML en el nombre")
bad({**ok, "name": "Viajes \"Sol\""}, "comillas en el nombre")
bad({**ok, "name": "x" * 41}, "nombre largo")
bad({**ok, "name": " Viajes"}, "espacios sobrantes")
bad({**ok, "color": "red"}, "color no hexadecimal")
bad({**ok, "color": "#fff;}body{display:none"}, "CSS en el color")
bad({**ok, "lang": "fr"}, "idioma no admitido")
bad({**ok, "logo": "../../docs/index.html"}, "logo fuera de la carpeta")
bad({**ok, "logo": "no-existe.png"}, "logo inexistente")
bad({**ok, "css": "body{}"}, "campo no admitido")
bad({**ok, "demo": "yes"}, "demo no booleano")
try:
    R.validate([ok, dict(ok)])
    errors.append("id repetido aceptado")
except ValueError:
    pass

# Contraste AA (4,5:1) para cualquier color de marca, en claro y oscuro
rnd = random.Random(261)
colors = ["#ffffff", "#000000", "#ffff00", "#00ff00", "#7fd6a4", "#1f4e8c", "#0d6b3b"] + [
    "#%06x" % rnd.randrange(0, 0xFFFFFF + 1) for _ in range(300)]
for c in colors:
    pal = R.palette(c)
    lt, dk = pal["light"], pal["dark"]
    for name, val, other in (("claro/superficie", lt["--sign"], R.LIGHT_SURFACE), ("claro/texto botón", lt["--sign"], lt["--sign-ink"]),
                             ("oscuro/superficie", dk["--sign"], R.DARK_SURFACE), ("oscuro/texto botón", dk["--sign"], dk["--sign-ink"])):
        if R.contrast(val, other) < 4.5:
            errors.append(f"{c}: contraste {name} {R.contrast(val, other):.2f}")

# Páginas generadas
sitemap = (ROOT / "docs" / "sitemap.xml").read_text(encoding="utf-8")
if "/widget/p/" in sitemap:
    errors.append("las páginas de socio no deben estar en el sitemap")
partners = R.validate()
if not any(p.get("demo") for p in partners):
    errors.append("falta la entrada de demostración usada en /partners/")
for p in partners:
    f = ROOT / "docs" / "widget" / "p" / p["id"] / "index.html"
    if not f.is_file():
        errors.append(f"falta {f.relative_to(ROOT)}")
        continue
    html = f.read_text(encoding="utf-8")
    home = "https://vuelosclaim.eu/" + ("" if p["lang"] == "es" else "en/")
    needles = ['<meta name="robots" content="noindex">', f'<strong>{escape(p["name"])}</strong>', f'href="{home}"',
               "enlaces de afiliación" if p["lang"] == "es" else "affiliate links", f'lang="{p["lang"]}"', "window.CTT="]
    if p.get("demo"):
        needles.append("Demostración" if p["lang"] == "es" else "Demo")
    for n in needles:
        if n not in html:
            errors.append(f"{p['id']}: falta {n!r}")
    if "googlesyndication" in html:
        errors.append(f"{p['id']}: el widget de socio no debe llevar AdSense")
    if p.get("logo") and not any((f.parent / ("logo" + e)).is_file() for e in R.LOGO_EXT):
        errors.append(f"{p['id']}: logo no copiado")
generated = {d.name for d in (ROOT / "docs" / "widget" / "p").iterdir() if d.is_dir()}
extra = generated - {p["id"] for p in partners}
if extra:
    errors.append(f"páginas de socios sin registro: {sorted(extra)}")
landing = (ROOT / "docs" / "partners" / "index.html").read_text(encoding="utf-8")
if 'src="/widget/p/demo/"' not in landing:
    errors.append("la landing de Partners debe mostrar la demostración con marca")

for e in errors:
    print("ERROR:", e)
print(f"Widget de socios: {len(partners)} socios, {len(colors)} colores probados,", "OK" if not errors else f"{len(errors)} errores")
sys.exit(bool(errors))
