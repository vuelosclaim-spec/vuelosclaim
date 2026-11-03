"""Commercial pilot landing for VuelosClaim Partners (ES/EN).

No sign-up, checkout, customer tracking or unimplemented customization is offered as live.
"""
from html import escape as e
from urllib.parse import quote

PATHS = {"es": "/partners/", "en": "/en/partners/"}


def build(ctx):
    emit, head, header, footer = (ctx[k] for k in ("emit", "head", "header", "footer"))
    brand = ctx["brand"]
    for l in ("es", "en"):
        es = l == "es"
        title = ("VuelosClaim para agencias y blogs de viajes" if es else
                 "VuelosClaim for travel agencies and blogs")
        desc = ("Integra gratuitamente una calculadora de derechos aéreos. "
                "Solicita información de una futura versión con tu marca." if es else
                "Embed a free flight compensation calculator. Ask about a future branded version.")
        h1 = ("Una calculadora útil para tus viajeros" if es else
              "A useful calculator for your travellers")
        lead = ("Pon nuestra calculadora en tu web y ayuda a tus visitantes a conocer sus posibles derechos ante retrasos y cancelaciones. "
                "El widget estándar ya está disponible gratis. La personalización y las estadísticas están en fase piloto." if es else
                "Add our calculator to your website and help visitors understand possible rights after delays or cancellations. "
                "The standard widget is already available for free. Branding and statistics are pilot features, not yet live.")
        mail = "mailto:vuelosclaim@gmail.com?subject=" + quote("Piloto VuelosClaim Partners" if es else "VuelosClaim Partners pilot")
        plans = [
            ("Gratis", "0 €", "Disponible" if es else "Available",
             "Widget estándar y enlace de atribución. Sin personalización de marca." if es else
             "Standard widget with attribution link. No custom branding."),
            ("Pro", "9,90 €", "Precio objetivo · piloto" if es else "Target price · pilot",
             "Nombre, color y logo de tu agencia en el widget: lo configuramos nosotros durante el piloto. Aún no se aceptan pagos." if es else
             "Your agency's name, colour and logo in the widget: we set it up for you during the pilot. Payments are not yet accepted."),
            ("Premium", "19,90 €", "Precio objetivo · piloto" if es else "Target price · pilot",
             "Se estudian estadísticas agregadas y soporte prioritario. Sin panel activo." if es else
             "Planned aggregate statistics and priority support. No live dashboard."),
        ]
        cards = "".join(
            '<article class="partner-plan"><h3>' + e(name) + '</h3><p class="partner-price">' + e(price) +
            ('<small> / ' + ('mes + IVA' if es else 'month + VAT') + '</small>' if name != "Gratis" else '') +
            '</p><p><strong>' + e(state) + '</strong></p><p>' + e(note) + '</p></article>'
            for name, price, state, note in plans
        )
        link = "/insertar-calculadora/"
        path = PATHS[l]
        other = PATHS["en" if es else "es"]
        snippet = ('<iframe src="https://vuelosclaim.eu/widget/" title="Calculadora de derechos aéreos" '
                   'loading="lazy" style="border:0;width:100%;max-width:560px;height:960px"></iframe>')
        body = f'''<div class="wrap prose partner-page">
<h1>{e(h1)}</h1>
<p class="lead">{e(lead)}</p>
<p><a class="btn btn-sign" href="{e(mail)}">{'Pedir información del piloto' if es else 'Enquire about the pilot'}</a>
<a href="{link}">{'Usar el widget gratuito' if es else 'Get the free widget'}</a></p>
<h2>{'Planes previstos' if es else 'Planned plans'}</h2>
<div class="partner-plans">{cards}</div>
<p><small>{'Precios orientativos, no se ofrece contratación ni pago todavía. Las características de pago requieren desarrollo y validación comercial.' if es else 'Indicative prices only; no paid subscription or checkout is available yet. Paid features require development and commercial validation.'}</small></p>
<h2>{'Prueba el widget que ya funciona' if es else 'Try the working widget'}</h2>
<p>{'Esta es la calculadora gratuita real. No incluye marca blanca ni estadísticas por empresa.' if es else 'This is the existing free calculator. White-label features and agency analytics are not available yet.'}</p>
<div class="partner-demo"><iframe title="{'Demostración de la calculadora' if es else 'Calculator demo'}" src="/widget/" loading="lazy"></iframe></div>
<h2>{'Ejemplo con la marca de una agencia' if es else 'Example with an agency brand'}</h2>
<p>{'Así se ve el widget con el nombre y el color de una agencia. «Agencia de ejemplo» es una demostración, no un cliente. La marca la damos de alta nosotros: tu web no puede cambiarla ni ocultar la atribución a VuelosClaim.' if es else 'This is how the widget looks with an agency name and colour. "Agencia de ejemplo" is a demo, not a customer. We set up the branding for you; the embedding site cannot change it or hide the VuelosClaim attribution.'}</p>
<div class="partner-demo"><iframe title="{'Demostración del widget con marca' if es else 'Branded widget demo'}" src="/widget/p/demo/" loading="lazy"></iframe></div>
<h2>{'Código para tu web' if es else 'Embed code for your site'}</h2>
<p>{'Copia este HTML para insertar la versión gratuita.' if es else 'Copy this HTML to embed the free version.'}</p>
<label for="partners-code">{'Código de inserción' if es else 'Embed HTML'}</label>
<textarea id="partners-code" readonly rows="4" onclick="this.select()">{e(snippet)}</textarea>
<h2>{'Para agencias y portales' if es else 'For agencies and travel publishers'}</h2>
<p>{'Ofrecemos una prueba inicial para evaluar integración y necesidades, sin prometer resultados, clientes ni comisiones. Indica el nombre de tu web y qué necesitas en tu correo.' if es else 'We can discuss a pilot to evaluate integration and requirements; there is no promise of leads, compensation or affiliate income. Tell us about your website and needs by email.'}</p>
<p><a class="btn btn-sign" href="{e(mail)}">{'Contactar por correo' if es else 'Email us'}</a></p>
<p><small>{'La estimación es orientativa; no garantiza indemnización. El widget incluye enlaces de afiliación sujetos a sus avisos y a tus obligaciones legales al integrarlo.' if es else 'The estimate is indicative, not guaranteed compensation. The widget contains affiliate links with disclosures; publishers remain responsible for their own legal obligations when embedding it.'}</small></p>
</div>
<style>
.partner-page{{padding-block:34px 70px}}
.partner-page .lead{{max-width:72ch}}
.partner-page h2{{margin-top:36px}}
.partner-plans{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}}
.partner-plan{{border:1px solid var(--line);border-radius:12px;padding:18px;min-width:0}}
.partner-plan h3{{margin:0}}
.partner-price{{font-size:1.65rem;font-weight:800;margin:12px 0}}
.partner-price small{{font-size:.72rem;font-weight:400}}
.partner-demo{{max-width:570px;border:1px solid var(--line);border-radius:12px;overflow:hidden}}
.partner-demo iframe{{width:100%;height:960px;border:0;display:block}}
.partner-page textarea{{display:block;width:100%;max-width:700px;min-height:110px;padding:12px}}
@media(max-width:720px){{.partner-plans{{grid-template-columns:1fr}}}}
</style>'''
        html = (f'{head(l, title + " · " + brand, desc, path, PATHS)}\n'
                f'{header(l, other, PATHS)}<main id="main" tabindex="-1">{body}</main>{footer(l)}')
        emit(l, path, html)
    return PATHS
