#!/usr/bin/env python3
"""Validaciones offline de URLs de reclamación: no comprueba disponibilidad en Internet."""
import ipaddress
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors = []
count = 0

def check(label, raw):
    global count
    count += 1
    try:
        u = urlsplit(raw)
    except ValueError as exc:
        errors.append(f"{label}: URL inválida ({exc})")
        return
    host = u.hostname or ""
    if u.scheme != "https" or not host:
        errors.append(f"{label}: se exige URL HTTPS con dominio")
    if u.username is not None or u.password is not None:
        errors.append(f"{label}: URL incluye credenciales")
    if u.fragment:
        # Un fragmento es válido y no representa un riesgo de seguridad.
        pass
    if host == "localhost" or host.endswith((".localhost", ".local", ".internal")):
        errors.append(f"{label}: destino interno no autorizado")
    try:
        ipaddress.ip_address(host.strip("[]"))
    except ValueError:
        if "." not in host:
            errors.append(f"{label}: no parece un dominio público")
    else:
        errors.append(f"{label}: se exige un dominio público, no una IP")
    if "\\" in raw or any(ord(ch) < 32 for ch in raw):
        errors.append(f"{label}: URL contiene caracteres de control o barras invertidas")

airlines = json.loads((ROOT / "data/airlines.json").read_text(encoding="utf-8"))
for airline in airlines:
    slug = airline.get("slug", "?")
    for lang in ("es", "en"):
        check(f"{slug}/claim_{lang}", airline.get(f"claim_{lang}", ""))

claims = json.loads((ROOT / "data/airline_claims.json").read_text(encoding="utf-8"))
for slug, record in claims.items():
    if slug.startswith("_"):
        continue
    for field in ("sources", "forms"):
        for i, item in enumerate(record.get(field, [])):
            check(f"{slug}/{field}/{i}", item.get("url", ""))

for e in errors:
    print("ERROR:", e)
print(f"URLs revisadas: {count}; errores: {len(errors)}")
sys.exit(bool(errors))
