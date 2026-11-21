# Guion: (escena, texto_voz, texto_subtítulo)
import json, subprocess, os
from kokoro_onnx import Kokoro
import soundfile as sf
K = Kokoro('/tmp/claude-0/kk/kokoro-v1.0.onnx', '/tmp/claude-0/kk/voices-v1.0.bin')
os.chdir('/tmp/claude-0/v2')
G = [
 (0, "¿Te cancelan el vuelo en Navidad?", "¿Te cancelan el vuelo en Navidad?"),
 (1, "Imagina: es veintitrés de diciembre.", "Imagina: es 23 de diciembre."),
 (1, "Lucía vuela de Barcelona a Roma", "Lucía vuela de Barcelona a Roma"),
 (1, "para cenar en Nochebuena con su familia.", "para cenar en Nochebuena con su familia."),
 (2, "Llega al aeropuerto, mira el panel...", "Llega al aeropuerto, mira el panel..."),
 (2, "y su vuelo aparece cancelado.", "y su vuelo aparece cancelado."),
 (3, "En el mostrador le ofrecen un bono.", "En el mostrador le ofrecen un bono."),
 (3, "Pero Lucía no tiene por qué aceptarlo.", "Pero Lucía no tiene por qué aceptarlo."),
 (4, "Puede elegir el reembolso del billete en siete días,", "Puede elegir el reembolso del billete en 7 días,"),
 (4, "u otro vuelo a Roma lo antes posible.", "u otro vuelo a Roma lo antes posible."),
 (5, "Mientras espera, la aerolínea debe darle comida y bebida.", "Mientras espera, la aerolínea debe darle comida y bebida."),
 (5, "Y si tiene que pasar la noche, hotel y traslado.", "Y si tiene que pasar la noche, hotel y traslado."),
 (6, "Y como la avisaron con menos de catorce días,", "Y como la avisaron con menos de 14 días,"),
 (6, "si no hay circunstancias extraordinarias,", "si no hay circunstancias extraordinarias,"),
 (6, "normalmente le corresponden doscientos cincuenta euros.", "normalmente le corresponden 250 euros."),
 (6, "En dinero, no en bonos.", "En dinero, no en bonos."),
 (7, "Lucía llegó a la cena.", "Lucía llegó a la cena."),
 (7, "Y guardó la tarjeta de embarque y los tiques para reclamar.", "Y guardó la tarjeta de embarque y los tiques para reclamar."),
 (8, "¿Te ha pasado algo así en Navidad?", "¿Te ha pasado algo así en Navidad?"),
 (8, "Cuéntalo en comentarios.", "Cuéntalo en comentarios."),
 (8, "Y calcula cuánto te corresponde en VuelosClaim punto eu.", "Y calcula cuánto te corresponde en VuelosClaim.eu"),
]
GAP = 0.18; SCENE_GAP = 0.45; LEAD = 0.25
t = LEAD; segs = []; prev = None
for i, (sc, tts, sub) in enumerate(G):
    f = f'p_{i:02d}.wav'
    a, sr = K.create(tts, voice='em_alex', speed=1.05, lang='es'); sf.write(f, a, sr)
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)
    if prev is not None and sc != prev: t += SCENE_GAP
    words = sub.split(); w = [len(x) + 2 for x in words]; tot = sum(w)
    # piper adds ~0.2s silence at end; spread words over d-0.25
    span = max(0.3, d - 0.1); acc = 0; wt = []
    for x, ww in zip(words, w):
        wt.append([x, round(t + span * acc / tot, 3)]); acc += ww
    segs.append({'sc': sc, 'f': f, 'start': round(t, 3), 'end': round(t + d, 3), 'words': wt})
    t += d + GAP; prev = sc
scenes = {}
for s in segs:
    scenes.setdefault(s['sc'], [s['start'], s['end']]); scenes[s['sc']][1] = s['end']
sc_list = sorted(scenes)
bounds = []
for k, sc in enumerate(sc_list):
    a = 0 if k == 0 else (scenes[sc_list[k-1]][1] + scenes[sc][0]) / 2
    bounds.append([sc, round(a, 3)])
total = round(segs[-1]['end'] + 2.6, 3)
json.dump({'segs': segs, 'bounds': bounds, 'total': total}, open('timing.json', 'w'), ensure_ascii=False)
print(total, bounds)
