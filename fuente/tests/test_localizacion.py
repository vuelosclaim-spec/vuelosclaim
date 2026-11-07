#!/usr/bin/env python3
"""Evita publicar instrucciones incorrectas sobre recursos IT/DE/PT."""
from pathlib import Path
import sys
SRC = (Path(__file__).resolve().parents[1] / "i18n.py").read_text(encoding="utf-8")
checks = {
    "IT: indicación de seis semanas": "sei settimane" in SRC,
    "DE: plazo de dos meses": "zwei Monaten" in SRC,
    "IT: sin un mes incorrecto": "entro un mese" not in SRC,
    "DE: sin plazo erróneo de un mes": "innerhalb eines Monats" not in SRC,
    "IT: enlace al organismo ENAC": "https://www.enac.gov.it/" in SRC,
    "DE: enlace a organismo público": "https://www.bundesregierung.de/" in SRC,
    "PT: seis semanas antes de acudir a la ANAC": "6 semanas" in SRC,
    "PT: enlace a la ANAC": "https://www.anac.pt/" in SRC,
    "PT: plazo de 3 años ante la ANAC (gov.pt)": "até 3 anos" in SRC,
    "PT: páginas legales señaladas en inglés": "Aviso legal (em inglês)" in SRC and "Privacidade (em inglês)" in SRC,
    "Idiomas y páginas legales claramente en inglés": "Note legali (in inglese)" in SRC and "Privacy (in inglese)" in SRC,
}
for name, passed in checks.items():
    print(("OK" if passed else "ERROR") + ": " + name)
sys.exit(0 if all(checks.values()) else 1)
