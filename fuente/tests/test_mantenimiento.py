#!/usr/bin/env python3
"""Validación offline del calendario de huelgas: coherencia de datos, no veracidad de fuentes."""
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import strikes

OFFICIAL = ("transportes.gob.es", "mitma.gob.es", "boe.es", "aena.es", "enaire.es", "mit.gov.it", "enav.it", "enac.gov.it",
            "ccoo.es", "ugt.es", "usca.es", "unitetheunion.org", "gmb.org.uk", "caa.co.uk", "gov.uk", "dgac.fr", "ecologie.gouv.fr")
errors = []
warnings = []
seen = set()
today = dt.date.today()
updated = dt.date.fromisoformat(strikes.UPDATED["iso"])

if updated > today:
    errors.append("La fecha UPDATED es futura")
if (today - updated).days > 30:
    warnings.append("Calendario sin revisión declarada en más de 30 días")

for i, item in enumerate(strikes.STRIKES, 1):
    if len(item) != 10:
        errors.append(f"Entrada {i}: se esperaban 10 campos")
        continue
    start, label_es, label_en, desc_es, desc_en, where, kind, status_es, status_en, url = item
    try:
        first = dt.date.fromisoformat(start)
        last = dt.date.fromisoformat(strikes.end_date(item))
        if last < first:
            errors.append(f"Entrada {i}: fin anterior al inicio")
    except (ValueError, KeyError, TypeError) as exc:
        errors.append(f"Entrada {i}: fecha incorrecta: {exc}")
        continue
    if kind not in strikes.KIND["es"] or kind not in strikes.KIND["en"]:
        errors.append(f"Entrada {i}: categoría no reconocida")
    if not url.startswith("https://"):
        errors.append(f"Entrada {i}: fuente sin HTTPS")
    # Solo fuentes oficiales: ministerios, aeropuertos, proveedores de control aéreo o el sindicato convocante
    host = url.split("/")[2].lower()
    if not any(host == d or host.endswith("." + d) for d in OFFICIAL):
        errors.append(f"Entrada {i}: fuente no oficial ({host})")
    if where not in getattr(strikes, "WHERE_EN", {}):
        errors.append(f"Entrada {i}: ubicación sin traducción al inglés ({where})")
    if not all([label_es, label_en, desc_es, desc_en, where, status_es, status_en]):
        errors.append(f"Entrada {i}: traducción o estado vacío")
    identity = (start, desc_es.strip().casefold(), where.strip().casefold())
    if identity in seen:
        errors.append(f"Entrada {i}: posible duplicado")
    seen.add(identity)
    if last < today:
        warnings.append(f"Entrada {i}: huelga vencida el {last}; comprobar limpieza editorial")

for msg in warnings:
    print("AVISO:", msg)
for msg in errors:
    print("ERROR:", msg)
print(f"Comprobadas {len(strikes.STRIKES)} entradas: {len(errors)} errores, {len(warnings)} avisos")
sys.exit(bool(errors))
