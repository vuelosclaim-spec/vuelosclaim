#!/usr/bin/env python3
"""Alta de agencias con fuente/alta_socio.py: validaciones, logo seguro y prueba de extremo a extremo.

Trabaja siempre sobre copias temporales: nunca modifica fuente/partners.json ni docs/ del repositorio.
"""
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zlib
import struct

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "fuente"
sys.path.insert(0, str(SRC))
import alta_socio as A  # noqa: E402

errors = []


def png(w=8, h=8):
    raw = b"".join(b"\x00" + b"\x1f\x4e\x8c" * w for _ in range(h))
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")


def expect_error(fn, why):
    try:
        fn()
        errors.append(f"debería fallar: {why}")
    except ValueError:
        pass


with tempfile.TemporaryDirectory() as t:
    t = Path(t)
    data, logos = t / "partners.json", t / "logos"
    shutil.copyfile(SRC / "partners.json", data)
    logos.mkdir()
    good = t / "logo.png"; good.write_bytes(png())
    fake = t / "fake.png"; fake.write_bytes(b"<html>no soy un png</html>")
    big = t / "big.png"; big.write_bytes(png() + b"\x00" * 120_000)
    svg_ok = t / "ok.svg"; svg_ok.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect width="10" height="10" fill="#c00"/></svg>')
    svg_bad = t / "bad.svg"; svg_bad.write_text('<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>')
    svg_ext = t / "ext.svg"; svg_ext.write_text('<svg xmlns="http://www.w3.org/2000/svg"><image href="https://evil.test/x.png"/></svg>')
    svg_on = t / "on.svg"; svg_on.write_text('<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"></svg>')
    kw = {"data_path": str(data), "logo_dir": str(logos)}
    before = data.read_text(encoding="utf-8")

    e = A.alta("Viajes Sol Ñandú", "#C0392B", "es", str(good), "#F1C232", **kw)
    if e["id"] != "viajes-sol-nandu" or e["color"] != "#c0392b" or e["accent"] != "#f1c232" or e["logo"] != "viajes-sol-nandu.png":
        errors.append(f"alta con datos inesperados: {e}")
    if not (logos / "viajes-sol-nandu.png").is_file():
        errors.append("el logo no se ha copiado")
    reg = json.loads(data.read_text(encoding="utf-8"))
    if [p["id"] for p in reg] != ["demo", "viajes-sol-nandu"]:
        errors.append(f"registro inesperado: {[p['id'] for p in reg]}")
    webp = t / "logo.webp"; webp.write_bytes(b"RIFF\x10\x00\x00\x00WEBPVP8 " + b"\x00" * 8)
    A.alta("Sun Travel", "#0b5394", "en", str(webp), **kw)
    if not (logos / "sun-travel.webp").is_file():
        errors.append("el logo WebP no se ha copiado")

    snapshot = data.read_text(encoding="utf-8"), sorted(os.listdir(logos))
    expect_error(lambda: A.alta("Viajes Sol Ñandú", "#c0392b", **kw), "id repetido")
    expect_error(lambda: A.alta("Otra", "#c0392b", logo=str(fake), **kw), "PNG falso")
    expect_error(lambda: A.alta("Otra", "#c0392b", logo=str(big), **kw), "logo de más de 100 KB")
    expect_error(lambda: A.alta("Otra", "#c0392b", logo=str(svg_ok), **kw), "SVG (no admitido aunque parezca limpio)")
    expect_error(lambda: A.alta("Otra", "#c0392b", logo=str(svg_bad), **kw), "SVG con script")
    expect_error(lambda: A.alta("Otra", "#c0392b", logo=str(svg_ext), **kw), "SVG con recurso externo")
    expect_error(lambda: A.alta("Otra", "#c0392b", logo=str(svg_on), **kw), "SVG con evento")
    expect_error(lambda: A.alta("Otra", "#c0392b", logo=str(t / "no-existe.png"), **kw), "logo inexistente")
    expect_error(lambda: A.alta("<b>Mala</b>", "#c0392b", logo=str(good), **kw), "nombre con HTML")
    expect_error(lambda: A.alta("Otra", "rojo", **kw), "color no válido")
    expect_error(lambda: A.alta("Otra", "#c0392b", accent="#fff;x", **kw), "color secundario no válido")
    expect_error(lambda: A.alta("Otra", "#c0392b", lang="fr", **kw), "idioma no válido")
    expect_error(lambda: A.alta("Otra", "#c0392b", pid="../x", **kw), "id con ruta")
    expect_error(lambda: A.baja("demo", **kw), "baja de la demostración")
    expect_error(lambda: A.baja("no-existe", **kw), "baja inexistente")
    if (data.read_text(encoding="utf-8"), sorted(os.listdir(logos))) != snapshot:
        errors.append("un alta fallida ha dejado cambios en el registro o en los logos")

    # Fallo al guardar el registro después de copiar el logo: no debe quedar nada
    real_save = A.save
    def broken_save(*_a, **_k):
        raise OSError("disco lleno (simulado)")
    A.save = broken_save
    try:
        A.alta("Guardado Roto", "#c0392b", logo=str(good), **kw)
        errors.append("un fallo al guardar debería propagarse")
    except OSError:
        pass
    finally:
        A.save = real_save
    if (logos / "guardado-roto.png").exists() or "guardado-roto" in data.read_text(encoding="utf-8"):
        errors.append("un fallo al guardar ha dejado el logo o la entrada")
    # Un logo manipulado después del alta se detecta al compilar
    tampered = logos / "sun-travel.webp"; saved = tampered.read_bytes(); tampered.write_bytes(b"<svg onload=alert(1)>")
    try:
        A.R.validate(A.R.load(str(data)), logo_dir=str(logos))
        errors.append("el registro acepta un logo cuyo contenido no es WebP")
    except ValueError:
        pass
    tampered.write_bytes(saved)

    A.baja("viajes-sol-nandu", **kw)
    if "viajes-sol-nandu" in data.read_text(encoding="utf-8") or (logos / "viajes-sol-nandu.png").exists():
        errors.append("la baja no ha quitado la entrada o el logo")

    # Extremo a extremo: alta con el comando real en una copia de fuente/ y compilación en una carpeta temporal
    work = t / "repo"
    shutil.copytree(SRC, work / "fuente", ignore=shutil.ignore_patterns("__pycache__", "tests"))
    env = dict(os.environ, BUILD_OUT=str(t / "out"))
    r = subprocess.run([sys.executable, str(work / "fuente" / "alta_socio.py"), "--nombre", "Viajes Sol", "--color", "#c0392b",
                        "--acento", "#f1c232", "--logo", str(good), "--compilar"], capture_output=True, text=True, env=env)
    if r.returncode:
        errors.append(f"alta por comando falló: {r.stderr[-400:]}")
    else:
        if "/widget/p/viajes-sol/" not in r.stdout or "<iframe" not in r.stdout:
            errors.append("el comando no imprime la dirección y el código de inserción")
        page = t / "out" / "widget" / "p" / "viajes-sol" / "index.html"
        if not page.is_file():
            errors.append("la compilación no ha generado el widget de la nueva agencia")
        else:
            html = page.read_text(encoding="utf-8")
            for n in ("<strong>Viajes Sol</strong>", "--brand-accent:#f1c232", 'src="logo.png"', 'content="noindex"'):
                if n not in html:
                    errors.append(f"widget generado sin {n!r}")
            if not (page.parent / "logo.png").is_file():
                errors.append("el logo no se ha publicado junto al widget")
    r = subprocess.run([sys.executable, str(work / "fuente" / "alta_socio.py"), "--listar"], capture_output=True, text=True)
    if r.returncode or "viajes-sol" not in r.stdout or "demo" not in r.stdout:
        errors.append("--listar no muestra las agencias")
    r = subprocess.run([sys.executable, str(work / "fuente" / "alta_socio.py"), "--nombre", "X<script>", "--color", "#c0392b"], capture_output=True, text=True)
    if r.returncode != 1 or "ERROR" not in r.stderr:
        errors.append("un alta inválida por comando debe terminar con error")

if (SRC / "partners.json").read_text(encoding="utf-8") != before:
    errors.append("la prueba ha modificado el registro real")

for e in errors:
    print("ERROR:", e)
print("Alta de agencias:", "OK" if not errors else f"{len(errors)} errores")
sys.exit(bool(errors))
