from PIL import Image, ImageDraw, ImageFont
import math, os, subprocess

W, H, FPS = 1080, 1920, 30
F = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
def font(w, s): return ImageFont.truetype(F % w, s)
NAVY, WHITE, MUTED = (11, 22, 48), (255, 255, 255), (170, 182, 210)
RED, GREEN, AMBER, BLUE = (239, 68, 68), (34, 197, 94), (251, 191, 36), (59, 130, 246)
OUT = "/tmp/claude-0/historia/frames"; os.makedirs(OUT, exist_ok=True)

# scenes: (start, end)
S = [(0, 2.6), (2.6, 5.6), (5.6, 10.4), (10.4, 15.2), (15.2, 20.0)]
DUR = S[-1][1]

def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3

def ctext(d, y, txt, f, fill, alpha=1, dy=0):
    w = d.textlength(txt, font=f)
    c = tuple(int(NAVY[i] + (fill[i] - NAVY[i]) * alpha) for i in range(3))
    d.text(((W - w) / 2, y + dy), txt, font=f, fill=c)

def wrap(d, txt, f, maxw):
    lines, cur = [], ""
    for w in txt.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def block(d, y, txt, f, fill, a, dy=0, lh=1.25, maxw=900):
    for i, ln in enumerate(wrap(d, txt, f, maxw)):
        ctext(d, y + i * f.size * lh, ln, f, fill, a, dy)

def pill(d, t):
    f = font("Bold", 46); txt = "Enlace en la bio ↑"
    w = d.textlength(txt, font=f); x = (W - w) / 2; y = 1640 + 8 * math.sin(t * 4)
    d.rounded_rectangle((x - 40, y - 22, x + w + 40, y + 70), 46, fill=BLUE)
    d.text((x, y - 4), txt, font=f, fill=WHITE)
    fs = font("Medium", 30); ctext(d, 1790, "Caso hipotético · Reglamento (CE) 261/2004", fs, MUTED)

def board(d, t, y0):
    # departure-board row
    d.rounded_rectangle((90, y0, 990, y0 + 200), 24, fill=(20, 33, 66))
    d.text((130, y0 + 30), "PEKÍN → MADRID", font=font("ExtraBold", 64), fill=WHITE)
    on = int(t * 3) % 2 == 0
    d.text((130, y0 + 112), "RETRASO 5 H", font=font("Black", 56), fill=RED if on else (120, 40, 50))
    d.text((720, y0 + 118), "4 billetes", font=font("SemiBold", 44), fill=AMBER)

def frame(t):
    im = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(im)
    d.text((70, 90), "vuelosclaim.eu", font=font("Bold", 40), fill=MUTED)
    if t < S[0][1]:
        a = ease(t / 0.35)
        ctext(d, 330, "IMAGINA:", font("Black", 96), AMBER, a, 40 * (1 - a))
        block(d, 470, "volvéis de vacaciones en China", font("Bold", 66), WHITE, ease((t - .2) / .4))
        if t > .5: board(d, t, 720)
    elif t < S[1][1]:
        lt = t - S[1][0]; board(d, t, 360)
        a = ease(lt / .4)
        block(d, 700, "¿Cuánto dinero os deben?", font("ExtraBold", 92), WHITE, a, 30 * (1 - a))
        if lt > 1.1: block(d, 1000, "La respuesta depende de UNA cosa…", font("SemiBold", 54), AMBER, ease((lt - 1.1) / .4))
    elif t < S[2][1]:
        lt = t - S[2][0]; a = ease(lt / .4)
        block(d, 300, "Si volabais con una aerolínea EUROPEA", font("ExtraBold", 70), WHITE, a)
        if lt > .9:
            b = ease((lt - .9) / .4)
            ctext(d, 640, "600 € × 4", font("Black", 120), GREEN, b, 30 * (1 - b))
        if lt > 1.8:
            c = ease((lt - 1.8) / .4)
            n = int(2400 * c)
            ctext(d, 820, f"= {n:,} €".replace(",", "."), font("Black", 170), GREEN, c)
        if lt > 2.8: block(d, 1120, "Más de 3.500 km y más de 4 h de retraso: el importe máximo", font("Medium", 44), MUTED, ease((lt - 2.8) / .4))
    elif t < S[3][1]:
        lt = t - S[3][0]; a = ease(lt / .4)
        block(d, 300, "Si volabais con una aerolínea CHINA", font("ExtraBold", 70), WHITE, a)
        if lt > .9:
            b = ease((lt - .9) / .3); sh = 12 * math.sin(lt * 40) * (1 - b)
            ctext(d, 620, "0 €", font("Black", 260), RED, b, sh)
        if lt > 2.0: block(d, 980, "El reglamento europeo no cubre los vuelos que llegan a la UE con aerolíneas de fuera de la UE.", font("Medium", 48), WHITE, ease((lt - 2.0) / .4))
    else:
        lt = t - S[4][0]; a = ease(lt / .4)
        block(d, 330, "Mismo vuelo. Mismo retraso.", font("ExtraBold", 74), WHITE, a)
        if lt > .8: block(d, 560, "Depende de la aerolínea que lo operó.", font("ExtraBold", 74), AMBER, ease((lt - .8) / .4))
        if lt > 1.8: block(d, 930, "Compruébalo gratis en 1 minuto", font("Bold", 62), GREEN, ease((lt - 1.8) / .4))
    if t >= 1.0: pill(d, t)
    return im

n = int(DUR * FPS)
for i in range(n):
    frame(i / FPS).save(f"{OUT}/{i:04d}.png")

# simple background music: soft pad + pulse, then mux
subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
    "-framerate", str(FPS), "-i", f"{OUT}/%04d.png",
    "-f", "lavfi", "-i",
    f"aevalsrc='0.10*sin(2*PI*220*t)*(0.6+0.4*sin(2*PI*0.5*t))+0.07*sin(2*PI*277.18*t)+0.06*sin(2*PI*329.63*t)+0.12*sin(2*PI*55*t)*exp(-6*mod(t,0.5))|0.10*sin(2*PI*220*t)*(0.6+0.4*sin(2*PI*0.5*t))+0.07*sin(2*PI*277.18*t)+0.06*sin(2*PI*329.63*t)+0.12*sin(2*PI*55*t)*exp(-6*mod(t,0.5))':s=44100:d={DUR}",
    "-af", f"afade=t=in:d=0.5,afade=t=out:st={DUR-1}:d=1",
    "-c:v", "libx264", "-profile:v", "main", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2", "-shortest", "-movflags", "+faststart",
    "/home/claude/videos/historia-china.mp4"], check=True)
print("ok")
