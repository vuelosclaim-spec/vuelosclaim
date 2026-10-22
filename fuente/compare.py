"""Comparison page (ES + EN): claims companies' fees vs claiming yourself. Bottom-of-funnel, alternative-page playbook.
Fees verified 20 Oct 2026 on each company's own site. Update FEES + UPDATED when they change.
"""
import json
from html import escape as e

UPDATED = {"es": "20 de octubre de 2026", "en": "20 October 2026"}
SRC = {
    "airhelp": "https://www.airhelp.com/en-int/ota/mytrip/price-list/",
    "reclamador": "https://www.reclamador.es/aerolineas/condiciones-generales/",
    "flightright": "https://www.flightright.com/costs",
}
PATHS = {"es": "/comparativa-empresas-reclamacion-vuelos/", "en": "/en/flight-compensation-companies-compared/"}

# key, name, base fee min/max as share of compensation (VAT included; vat_added=True means VAT is on top and we apply local rate),
# court surcharge text, raw text ES, raw text EN
FEES = [
    ("diy", None, 0, 0, False),
    ("reclamador", "Reclamador", 0.25, 0.25, True),
    ("flightright", "Flightright", 0.20, 0.30, True),
    ("airhelp", "AirHelp", 0.35, 0.35, False),
]
VAT = {"es": 0.21, "en": 0.20}

T = {
    "es": {
        "title": "AirHelp, Reclamador o Flightright: comisiones comparadas (2026)",
        "desc": "Cuánto se queda cada empresa de reclamación de vuelos: AirHelp 35%, Reclamador 25% + IVA, Flightright 20–30% + IVA. Y cuánto te queda si reclamas tú gratis.",
        "h1": "AirHelp, Reclamador, Flightright o reclamar tú: cuánto te queda de verdad",
        "lead": "Actualizado el {u}. Las empresas de reclamación cobran solo si ganan, pero se quedan entre una cuarta parte y la mitad de tu compensación. Aquí están sus comisiones, sacadas de sus propias webs, y lo que te llega a ti en cada caso.",
        "th": "<th>Opción</th><th>Comisión</th><th>Si va a juicio</th><th>De 250 € te quedan</th><th>De 400 €</th><th>De 600 €</th>",
        "rows": {
            "diy": ("Reclamar tú (formulario de la aerolínea + AESA)", "0 €", "Juicio verbal sin abogado hasta 2.000 €", ),
            "reclamador": ("Reclamador", "25% + IVA (30,25%)", "+15% + IVA (48,4% en total)"),
            "flightright": ("Flightright", "20–30% + IVA (24–36%)", "+14% si intervienen abogados"),
            "airhelp": ("AirHelp", "35% IVA incluido", "+15% (50% en total)"),
        },
        "calc_h": "Calcula lo que te llega",
        "calc_amt": "Compensación por persona",
        "calc_pax": "Pasajeros",
        "calc_btn": "Calcular",
        "you": "Te llega",
        "fee": "Comisión",
        "body": """<h2>¿Merece la pena pagar a una empresa?</h2>
<p>Depende de tu tiempo y de cómo responda la aerolínea. Reclamar tú es gratis y en muchos casos basta con el formulario de la aerolínea: si el retraso fue por una avería, falta de tripulación o huelga de su propia plantilla, la aerolínea no puede alegar circunstancias extraordinarias. Si no contesta en un mes o lo rechaza, puedes ir a <a href="https://www.seguridadaerea.gob.es/index.php/es/ambitos/derechos-de-los-pasajeros/inicia-tu-reclamacion-con-aesa" rel="noopener">AESA</a>, también gratis, y como último paso a un juicio verbal, que hasta 2.000 € no necesita abogado ni procurador.</p>
<p>Una empresa compensa sobre todo si no quieres ocuparte, si la aerolínea ya te ha dicho que no o si sois varios pasajeros y prefieres que lo lleve otro. A cambio, en una familia de cuatro con 400 € cada uno, la comisión puede pasar de 480 €.</p>
<h2>Qué mirar antes de firmar con cualquiera</h2>
<ul><li><strong>Si el IVA va incluido o no.</strong> Un 25% + IVA es en realidad un 30,25%.</li>
<li><strong>El recargo si va a juicio.</strong> Con todas sube a cerca del 50%.</li>
<li><strong>Si te cobran si cancelas.</strong> Algunas cobran si te echas atrás después de que hayan reclamado.</li>
<li><strong>No firmes con dos a la vez</strong> ni reclames tú por tu cuenta mientras una empresa lleva el caso.</li></ul>
<h2>Nuestra recomendación</h2>
<p>Primero comprueba cuánto te toca y reclama tú con nuestra carta gratuita. Si la aerolínea no paga o no tienes tiempo, entonces pásaselo a una empresa. <a href="/">Calcula tu compensación aquí</a>.</p>""",
        "disc": "Transparencia: si eliges AirHelp desde nuestros enlaces, nos llevamos una comisión de afiliado. No cambia lo que pagas ni los datos de esta tabla, que salen de las webs de cada empresa.",
        "cta_diy": "Calcular y reclamar gratis",
        "cta_aff": "Que lo lleve AirHelp",
        "faq": [
            ("¿Cuánto cobra AirHelp?", "Un 35% de la compensación con IVA incluido, y un 15% adicional si hace falta ir a juicio (50% en total). Solo cobra si consigue el dinero."),
            ("¿Cuánto cobra Reclamador?", "Un 25% más IVA (30,25%) si se resuelve sin juicio, y un 15% más IVA adicional si se presenta demanda. Solo cobra si gana."),
            ("¿Cuánto cobra Flightright?", "Normalmente entre el 20% y el 30% más IVA, y un 14% adicional si intervienen abogados. Solo cobra si gana."),
            ("¿Puedo reclamar sin empresa y sin abogado?", "Sí. Reclamas en el formulario de la aerolínea, después en AESA si no te pagan, y en un juicio verbal sin abogado si la cantidad no supera 2.000 €."),
        ],
        "src": "Fuentes: <a href=\"{a}\">tarifas de AirHelp</a> (versión del 11 de agosto de 2026) · <a href=\"{r}\">condiciones generales de Reclamador</a> · <a href=\"{f}\">costes de Flightright</a>. El IVA se calcula al 21%.",
    },
    "en": {
        "title": "AirHelp vs Flightright vs claiming yourself: fees compared (2026)",
        "desc": "How much each flight compensation company keeps: AirHelp 35%, Flightright 20–30% + VAT, Reclamador 25% + VAT. And what you keep if you claim yourself for free.",
        "h1": "AirHelp, Flightright, Reclamador or DIY: what you actually keep",
        "lead": "Updated {u}. Claims companies only charge if they win, but they keep between a quarter and half of your compensation. Here are their fees, taken from their own websites, and what reaches your bank account.",
        "th": "<th>Option</th><th>Fee</th><th>If it goes to court</th><th>Of €250 you keep</th><th>Of €400</th><th>Of €600</th>",
        "rows": {
            "diy": ("Claim yourself (airline form + CAA/AESA)", "£0 / €0", "Small claims court, no lawyer needed"),
            "reclamador": ("Reclamador", "25% + VAT (30%)", "+15% + VAT (48% total)"),
            "flightright": ("Flightright", "20–30% + VAT (24–36%)", "+14% if lawyers are involved"),
            "airhelp": ("AirHelp", "35% incl. VAT", "+15% (50% total)"),
        },
        "calc_h": "Work out what you'd receive",
        "calc_amt": "Compensation per passenger",
        "calc_pax": "Passengers",
        "calc_btn": "Calculate",
        "you": "You receive",
        "fee": "Fee",
        "body": """<h2>Is a claims company worth it?</h2>
<p>It depends on your time and on how the airline responds. Claiming yourself is free and often all it takes is the airline's own compensation form: if the delay was down to a technical fault, crew shortage or the airline's own staff striking, the airline can't rely on extraordinary circumstances. If they say no or don't answer (8 weeks for UK flights, one month for flights from Spain), escalate for free to the airline's ADR scheme or the <a href="https://www.caa.co.uk/passengers-and-public/resolving-travel-problems/" rel="noopener">CAA</a> for flights from the UK, or <a href="https://www.seguridadaerea.gob.es/en" rel="noopener">AESA</a> for flights from Spain. Small claims court is the last step and doesn't need a lawyer.</p>
<p>A company makes most sense if you don't want to deal with it, the airline has already refused, or there are several of you and you'd rather hand it over. The trade-off: for a family of four on £350 each, the fee can be more than £480.</p>
<h2>What to check before signing up</h2>
<ul><li><strong>Whether VAT is included.</strong> 25% + VAT is really 30%.</li>
<li><strong>The court surcharge.</strong> With all of them it goes up to around 50%.</li>
<li><strong>Cancellation charges.</strong> Some charge if you pull out after they've contacted the airline.</li>
<li><strong>Don't sign with two companies</strong> or claim yourself while a company is handling it.</li></ul>
<h2>Our advice</h2>
<p>Check what you're owed first and claim yourself with our free letter. If the airline won't pay or you don't have time, then hand it to a company. <a href="/en/">Work out your compensation here</a>.</p>""",
        "disc": "Transparency: if you choose AirHelp through our links we earn an affiliate commission. It doesn't change what you pay or the figures in this table, which come from each company's own website.",
        "cta_diy": "Calculate and claim for free",
        "cta_aff": "Let AirHelp handle it",
        "faq": [
            ("How much does AirHelp charge?", "35% of your compensation including VAT, plus an extra 15% if legal action is needed (50% in total). It only charges if it gets your money."),
            ("How much does Flightright charge?", "Usually 20% to 30% plus VAT, plus an extra 14% if lawyers have to get involved. It only charges if it wins."),
            ("Can I claim flight compensation without a company?", "Yes. Use the airline's compensation form, then escalate to its ADR scheme, the CAA or AESA if it refuses, and small claims court as a last resort. All of it can be done without a lawyer."),
            ("Do claims companies get more money than claiming yourself?", "They get the same fixed amount the law sets (£220–£520 or €250–€600 per person); they can't get more. The difference is they deduct their fee from it."),
        ],
        "src": "Sources: <a href=\"{a}\">AirHelp price list</a> (version of 11 August 2026) · <a href=\"{r}\">Reclamador terms</a> · <a href=\"{f}\">Flightright costs</a>. VAT worked out at 20%.",
    },
}


def _keep(l, key, amt):
    for k, _, lo, hi, vat_added in FEES:
        if k == key:
            m = 1 + VAT[l] if vat_added else 1
            return round(amt * (1 - hi * m)), round(amt * (1 - lo * m))


def build(ctx):
    for l, other in (("es", "en"), ("en", "es")):
        t = T[l]
        rows = ""
        for k, *_ in FEES:
            name, fee, court = t["rows"][k]
            cells = []
            for amt in (250, 400, 600):
                a, b = _keep(l, k, amt)
                cells.append(f"<td class=\"eur\">{a} €</td>" if a == b else f"<td class=\"eur\">{a}–{b} €</td>")
            rows += f"<tr><td><strong>{name}</strong></td><td>{fee}</td><td>{court}</td>{''.join(cells)}</tr>"
        rates = {k: [lo * ((1 + VAT[l]) if v else 1), hi * ((1 + VAT[l]) if v else 1)] for k, _, lo, hi, v in FEES}
        names = {k: t["rows"][k][0] for k, *_ in FEES}
        cur = "€" if l == "es" else "£/€"
        opts = "".join(f"<option value=\"{v}\">{v} {'€' if l == 'es' else ('£' if v in (220, 350, 520) else '€')}</option>"
                       for v in ((250, 400, 600) if l == "es" else (220, 350, 520, 250, 400, 600)))
        calc = f"""<h2>{t['calc_h']}</h2>
<form id="cmp-form" class="sk"><label>{t['calc_amt']} <select id="cmp-amt">{opts}</select></label>
<label>{t['calc_pax']} <input type="number" id="cmp-pax" min="1" max="9" value="2"></label>
<button class="btn btn-sign" type="submit">{t['calc_btn']}</button></form>
<div id="cmp-out" aria-live="polite"></div>
<script>(function(){{var R={json.dumps(rates)},N={json.dumps(names, ensure_ascii=False)};
function f(x){{return Math.round(x).toLocaleString()}}
document.getElementById('cmp-form').addEventListener('submit',function(ev){{ev.preventDefault();
var a=+document.getElementById('cmp-amt').value,p=Math.max(1,+document.getElementById('cmp-pax').value||1),tot=a*p,h='<div class="board"><table><thead><tr><th></th><th>{t['fee']}</th><th>{t['you']}</th></tr></thead><tbody>';
for(var k in R){{var lo=tot*R[k][0],hi=tot*R[k][1];h+='<tr><td>'+N[k]+'</td><td>'+(lo==hi?f(lo):f(lo)+'–'+f(hi))+'</td><td class="eur"><strong>'+(lo==hi?f(tot-lo):f(tot-hi)+'–'+f(tot-lo))+'</strong></td></tr>'}}
document.getElementById('cmp-out').innerHTML=h+'</tbody></table></div>'}});}})();</script>"""
        faq_html = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in t["faq"])
        faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]}
        home = "/" if l == "es" else "/en/"
        body = f"""<div class="wrap prose"><h1>{t['h1']}</h1><p class="lead">{t['lead'].format(u=UPDATED[l])}</p>
<div class="board"><table><thead><tr>{t['th']}</tr></thead><tbody>{rows}</tbody></table></div>
<p><a class="btn btn-sign" href="{home}">{t['cta_diy']}</a> <a class="btn" href="{e(ctx['AFF_URL'])}" rel="sponsored nofollow noopener" target="_blank">{t['cta_aff']}</a></p>
<p><small>{t['disc']}</small></p>
{calc}
{t['body']}
<h2>{'Preguntas frecuentes' if l == 'es' else 'Common questions'}</h2>{faq_html}
<p><small>{t['src'].format(a=SRC['airhelp'], r=SRC['reclamador'], f=SRC['flightright'])}</small></p></div>
<style>.sk{{display:grid;gap:12px;max-width:520px;margin:12px 0}}.sk label{{display:grid;gap:4px;font-weight:600}}.sk input,.sk select{{font:inherit;padding:10px;border:1px solid var(--line);border-radius:8px;background:transparent;color:inherit}}</style>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>"""
        ctx["emit"](l, PATHS[l], ctx["page"](l, t["title"], t["desc"], PATHS[l], body, PATHS, PATHS[other]))
    return list(PATHS.values())
