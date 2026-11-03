"""VuelosClaim Partners: registry of agencies/blogs with a branded widget (pilot).

Only partners added here by the VuelosClaim team get a branded widget. Nothing comes from the
embedding site at runtime: no URL parameters, HTML or CSS from the client are ever applied.
Each entry is validated when the site is built (validate()); an invalid entry stops the build.

Fields
- id:    lowercase letters, digits and hyphens (2–32). Becomes /widget/p/<id>/.
- name:  plain text shown as "Ofrecida por <name>" (max 40 characters, no markup characters).
- color: brand colour as #rrggbb. It is darkened/lightened automatically if needed so that
         buttons and links keep WCAG AA contrast (4.5:1) in light and dark mode.
- lang:  "es" or "en".
- logo:  optional file name inside fuente/partners_logos/ (.png, .svg or .webp, max 100 KB),
         reviewed by us before adding it.
- demo:  True only for the public demonstration entry (shows a "Demostración" badge).
"""
import os
import re

LOGO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "partners_logos")

PARTNERS = [
    # Public demonstration for the /partners/ landing. Not a customer.
    {"id": "demo", "name": "Agencia de ejemplo", "color": "#1f4e8c", "lang": "es", "logo": None, "demo": True},
]

ID_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,30}[a-z0-9])?$")
HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
NAME_RE = re.compile(r"^[^<>&\"'`{}\\\x00-\x1f]{1,40}$")
LOGO_EXT = (".png", ".svg", ".webp")
LIGHT_SURFACE, DARK_SURFACE = "#ffffff", "#142219"
LIGHT_INK, DARK_INK = "#ffffff", "#06140c"


def _rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def _hex(rgb):
    return "#" + "".join(f"{max(0, min(255, round(c))):02x}" for c in rgb)


def _lum(h):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in _rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _mix(a, b, t):
    """t=0 → a, t=1 → b."""
    return _hex(tuple(x + (y - x) * t for x, y in zip(_rgb(a), _rgb(b))))


def _fit(color, towards, checks):
    """Move color towards black/white in small steps until every (other, min_ratio) check passes."""
    for i in range(0, 101):
        c = _mix(color, towards, i / 100)
        if all(contrast(c, other) >= ratio for other, ratio in checks):
            return c
    raise ValueError(f"no accessible variant for {color}")


def palette(color):
    """CSS custom properties for a brand colour, accessible in light and dark mode."""
    light = _fit(color, "#000000", [(LIGHT_SURFACE, 4.5), (LIGHT_INK, 4.5)])
    dark = _fit(color, "#ffffff", [(DARK_SURFACE, 4.5), (DARK_INK, 4.5)])
    return {
        "light": {"--sign": light, "--sign-ink": LIGHT_INK, "--sign-soft": _mix(light, "#ffffff", 0.9)},
        "dark": {"--sign": dark, "--sign-ink": DARK_INK, "--sign-soft": _mix(dark, DARK_SURFACE, 0.82)},
    }


def validate(partners=None):
    """Return the validated list or raise ValueError describing every problem."""
    partners = PARTNERS if partners is None else partners
    errors, seen = [], set()
    for p in partners:
        pid = p.get("id", "")
        if not isinstance(pid, str) or not ID_RE.match(pid):
            errors.append(f"id no válido: {pid!r}")
        elif pid in seen:
            errors.append(f"id repetido: {pid}")
        seen.add(pid)
        name = p.get("name", "")
        if not isinstance(name, str) or not NAME_RE.match(name) or name != name.strip():
            errors.append(f"{pid}: nombre no válido (texto plano, 1–40 caracteres, sin < > & comillas ni llaves)")
        if not isinstance(p.get("color"), str) or not HEX_RE.match(p["color"]):
            errors.append(f"{pid}: color no válido, usa #rrggbb")
        if p.get("lang") not in ("es", "en"):
            errors.append(f"{pid}: idioma no válido, usa es o en")
        logo = p.get("logo")
        if logo is not None:
            path = os.path.join(LOGO_DIR, logo) if isinstance(logo, str) else ""
            if (not isinstance(logo, str) or os.path.basename(logo) != logo or not logo.lower().endswith(LOGO_EXT)
                    or not os.path.isfile(path)):
                errors.append(f"{pid}: logo no encontrado o formato no admitido ({', '.join(LOGO_EXT)})")
            elif os.path.getsize(path) > 100_000:
                errors.append(f"{pid}: logo de más de 100 KB")
        if not isinstance(p.get("demo", False), bool):
            errors.append(f"{pid}: demo debe ser True o False")
        extra = set(p) - {"id", "name", "color", "lang", "logo", "demo"}
        if extra:
            errors.append(f"{pid}: campos no admitidos {sorted(extra)}")
    if errors:
        raise ValueError("Registro de socios no válido:\n- " + "\n- ".join(errors))
    return partners
