#!/usr/bin/env python3
"""Alta, listado y baja de agencias en VuelosClaim Partners (widget con marca).

Ejemplos:
  python3 fuente/alta_socio.py --nombre "Viajes Sol" --color "#c0392b" --idioma es --logo ~/logo-sol.png
  python3 fuente/alta_socio.py --nombre "Sun Travel" --color "#0b5394" --acento "#f1c232" --idioma en --compilar
  python3 fuente/alta_socio.py --listar
  python3 fuente/alta_socio.py --baja viajes-sol

Qué hace el alta:
  1. Crea el id a partir del nombre (o usa --id) y comprueba que no exista.
  2. Revisa el logo (PNG o WebP de verdad, máximo 100 KB; SVG no se admite porque puede llevar contenido activo)
     y lo copia como fuente/partners_logos/<id>.<ext>.
  3. Valida la entrada con las mismas reglas que el resto del registro (partners_registry.validate) y la
     guarda en fuente/partners.json. Si algo falla, no se modifica nada.
     Nunca sobrescribe un archivo existente. Si falla cualquier paso, incluido el guardado, se retira el logo
     copiado y el registro queda como estaba.
  4. Imprime el código de inserción para la agencia. Con --compilar regenera docs/ (python3 fuente/build.py).
No toca el motor de cálculo, la afiliación ni el consentimiento. La marca nunca se toma de la web de la agencia.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import partners_registry as R  # noqa: E402

SITE = "https://vuelosclaim.eu"
MAX_LOGO = 100_000


def slug(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:32].strip("-")
    return s


def check_logo(path):
    """Return the file extension if the logo is acceptable, else raise ValueError."""
    if not os.path.isfile(path):
        raise ValueError(f"no encuentro el logo: {path}")
    ext = os.path.splitext(path)[1].lower()
    if ext not in R.LOGO_EXT:
        raise ValueError(f"formato de logo no admitido ({ext or 'sin extensión'}); usa {', '.join(R.LOGO_EXT)}")
    size = os.path.getsize(path)
    if size > MAX_LOGO:
        raise ValueError(f"el logo pesa {size // 1024} KB; máximo {MAX_LOGO // 1000} KB")
    if not R.logo_is_valid(path):
        raise ValueError(f"el archivo {ext} no es un {ext[1:].upper()} válido")
    return ext


def save(partners, data_path):
    tmp = data_path + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(partners, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(tmp, data_path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def embed_code(pid, lang):
    title = "Calculadora de compensación por retraso de vuelo" if lang == "es" else "Flight delay compensation calculator"
    return (f'<iframe src="{SITE}/widget/p/{pid}/" title="{title}" '
            f'style="width:100%;max-width:560px;height:960px;border:0" loading="lazy"></iframe>')


def alta(name, color, lang="es", logo=None, accent=None, pid=None, data_path=R.DATA, logo_dir=R.LOGO_DIR):
    partners = R.load(data_path)
    name = (name or "").strip()
    pid = pid or slug(name)
    if any(p.get("id") == pid for p in partners):
        raise ValueError(f"ya existe una agencia con id «{pid}»; usa --id para elegir otro")
    color = (color or "").strip().lower()
    accent = accent.strip().lower() if accent else None
    entry = {"id": pid, "name": name, "color": color, "accent": accent, "lang": lang, "logo": None, "demo": False}
    ext = check_logo(logo) if logo else None
    if ext:
        entry["logo"] = pid + ext
    # Never overwrite an existing file, even one not in the registry (from ChatGPT, PR #40)
    os.makedirs(logo_dir, exist_ok=True)
    dest = os.path.join(logo_dir, entry["logo"]) if ext else None
    if dest and os.path.exists(dest):
        raise ValueError(f"ya existe un archivo para el logo de «{pid}»")
    copied = False
    try:
        if dest:
            with open(logo, "rb") as source, open(dest, "xb") as target:  # 'xb': fails if another process created it
                copied = True
                shutil.copyfileobj(source, target)
        R.validate(partners + [entry], logo_dir=logo_dir)
        save(partners + [entry], data_path)  # the JSON is replaced atomically
    except BaseException:
        # Rollback: only the logo this call created is removed
        if copied and dest:
            try:
                os.remove(dest)
            except FileNotFoundError:
                pass
        raise
    return entry


def baja(pid, data_path=R.DATA, logo_dir=R.LOGO_DIR):
    partners = R.load(data_path)
    match = [p for p in partners if p.get("id") == pid]
    if not match:
        raise ValueError(f"no existe la agencia «{pid}»")
    if match[0].get("demo"):
        raise ValueError("la demostración se usa en /partners/; no se da de baja con este comando")
    save([p for p in partners if p.get("id") != pid], data_path)
    if match[0].get("logo"):
        path = os.path.join(logo_dir, match[0]["logo"])
        if os.path.exists(path):
            os.remove(path)  # recuperable desde el historial de git
    return match[0]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Alta, listado y baja de agencias en VuelosClaim Partners.")
    ap.add_argument("--nombre", help="nombre visible de la agencia (texto plano, máximo 40 caracteres)")
    ap.add_argument("--color", help="color principal #rrggbb (se ajusta solo para mantener el contraste)")
    ap.add_argument("--acento", help="color secundario #rrggbb opcional (borde de la franja de marca)")
    ap.add_argument("--idioma", choices=("es", "en"), default="es")
    ap.add_argument("--logo", help="ruta a un PNG o WebP de hasta 100 KB (opcional)")
    ap.add_argument("--id", help="id del widget; por defecto, se crea a partir del nombre")
    ap.add_argument("--compilar", action="store_true", help="regenerar docs/ al terminar")
    ap.add_argument("--listar", action="store_true", help="mostrar las agencias registradas")
    ap.add_argument("--baja", metavar="ID", help="dar de baja una agencia")
    a = ap.parse_args(argv)
    try:
        if a.listar:
            for p in R.validate(R.load()):
                print(f"{p['id']:<24} {p['name']:<40} {p['color']} {p.get('accent') or '-':<8} {p['lang']} "
                      f"{p.get('logo') or 'sin logo'}{' (demo)' if p.get('demo') else ''}  {SITE}/widget/p/{p['id']}/")
            return 0
        if a.baja:
            p = baja(a.baja)
            print(f"Baja de «{p['name']}» ({p['id']}).")
        else:
            if not a.nombre or not a.color:
                ap.error("para dar de alta hacen falta --nombre y --color")
            p = alta(a.nombre, a.color, a.idioma, a.logo, a.acento, a.id)
            print(f"Alta de «{p['name']}» con id «{p['id']}».")
            print(f"Widget: {SITE}/widget/p/{p['id']}/  (disponible tras compilar, fusionar y publicar)")
            print("Código para la agencia:\n" + embed_code(p["id"], p["lang"]))
        if a.compilar:
            subprocess.run([sys.executable, os.path.join(HERE, "build.py")], check=True)
        else:
            print("Siguiente paso: python3 fuente/build.py y abrir una PR.")
        return 0
    except ValueError as ex:
        print(f"ERROR: {ex}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
