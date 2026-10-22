"""English landing pages for UK airports -> Spain routes (programmatic SEO, locations playbook).

Each page: real great-circle distances to Spain's main holiday airports, UK261 (outbound, £) and
EU261 (return, €) amounts, computed stats for that airport, regional claim time limits, internal links
to the Spanish airport pages and the UK airline pages.
"""
import json
from html import escape as e

UK = [  # code, slug, display name, region
    ("MAN", "manchester", "Manchester", "eng"), ("LGW", "london-gatwick", "London Gatwick", "eng"),
    ("STN", "london-stansted", "London Stansted", "eng"), ("LTN", "london-luton", "London Luton", "eng"),
    ("LHR", "london-heathrow", "London Heathrow", "eng"), ("BHX", "birmingham", "Birmingham", "eng"),
    ("BRS", "bristol", "Bristol", "eng"), ("EMA", "east-midlands", "East Midlands", "eng"),
    ("LBA", "leeds-bradford", "Leeds Bradford", "eng"), ("NCL", "newcastle", "Newcastle", "eng"),
    ("LPL", "liverpool", "Liverpool", "eng"), ("EDI", "edinburgh", "Edinburgh", "sco"),
    ("GLA", "glasgow", "Glasgow", "sco"), ("BFS", "belfast", "Belfast International", "ni"),
]
ES_DEST = ["AGP", "ALC", "PMI", "TFS", "LPA", "ACE", "FUE", "IBZ", "MAH", "BCN", "MAD", "VLC", "SVQ", "RMU", "GRO", "REU"]
CANARY = {"TFS", "LPA", "ACE", "FUE"}


def u_uk(slug):
    return f"/en/{slug}-to-spain-flight-delay-compensation/"


HUB = "/en/uk-airports-to-spain-flight-delay-compensation/"


def _uk(d):
    return 220 if d <= 1500 else 350 if d <= 3500 else 520


def _eu(d):
    return 250 if d <= 1500 else 400 if d <= 3500 else 600


def build(ctx):
    """ctx: dict with AIRPORTS, km, es_names (code->EN name), es_url (code->EN Spanish airport URL), page, hero,
    reference_sections, emit, AESA_URL, CAA_URL"""
    A, km = ctx["AIRPORTS"], ctx["km"]
    hub_rows = []
    for code, slug, name, region in UK:
        if code not in A:
            continue
        rows, data = [], []
        for dc in ES_DEST:
            if dc not in A:
                continue
            d = km(A[code], A[dc])
            data.append((d, dc))
        data.sort()
        for d, dc in data:
            dn = e(ctx["es_names"].get(dc, A[dc][2]))
            link = ctx["es_url"].get(dc)
            cell = f'<a href="{link}">{dn}</a>' if link else dn
            rows.append(f"<tr><td>{cell} ({dc})</td><td>{d:,} km</td><td class=\"eur\">£{_uk(d)}</td><td class=\"eur\">€{_eu(d)}</td></tr>")
        n220 = sum(1 for d, _ in data if d <= 1500)
        n350 = len(data) - n220
        near_d, near_c = data[0]
        far_d, far_c = data[-1]
        nm = lambda c: e(ctx["es_names"].get(c, A[c][2]))
        canary_ds = [d for d, c in data if c in CANARY]
        limit = ("5 years in Scotland" if region == "sco" else "6 years in Northern Ireland" if region == "ni" else "6 years in England and Wales")
        n = e(name)
        if n220 and n350:
            split = (f"From {n}, {n220} of the {len(data)} Spanish airports below are within 1,500 km, so a 3-hour delay pays <strong>£220</strong> on the way out; "
                     f"the other {n350}, including all the Canary Islands, are further and pay <strong>£350</strong>.")
        elif n350:
            split = f"Every Spanish airport below is more than 1,500 km from {n}, so a 3-hour delay on the way out pays <strong>£350</strong> per passenger, and <strong>€400</strong> on the way back."
        else:
            split = f"Every Spanish airport below is within 1,500 km of {n}, so a 3-hour delay pays <strong>£220</strong> out and <strong>€250</strong> back."
        canary_note = (f" The Canaries are the longest trips at around {min(canary_ds):,}–{max(canary_ds):,} km, and they still sit in the middle band because they're under 3,500 km."
                       if canary_ds else "")
        intro = (f"{split} The shortest route is {nm(near_c)} ({near_d:,} km) and the longest {nm(far_c)} ({far_d:,} km).{canary_note} "
                 f"It doesn't matter whether you flew Jet2, easyJet, Ryanair, TUI or anyone else, or whether it was a package holiday: the amount depends only on the distance.")
        faq = [
            (f"How much compensation for a delayed flight from {name} to Spain?",
             f"If you arrive 3 hours or more late and the cause was within the airline's control, UK261 pays £220 for Spanish airports within 1,500 km of {name} and £350 for those further away, such as the Canary Islands. On the return flight from Spain, EU261 pays €250 or €400."),
            (f"Which rules apply to my flight back from Spain to {name}?",
             "EU261, because it departs an EU airport. It applies to every airline, so the return leg pays in euros even on a UK airline like Jet2 or easyJet."),
            ("How long do I have to claim?",
             f"Through the courts, generally {limit}. For the flight home from Spain, the Spanish time limit is 5 years. Airlines' own forms accept older claims, but the sooner the better."),
            ("Who do I complain to if the airline refuses?",
             f"For the outbound flight from {name}: the airline's ADR scheme, or the UK Civil Aviation Authority if it isn't in one. For the flight back from Spain: AESA, Spain's aviation authority. Both are free."),
        ]
        faq_html = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faq)
        faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
        body_extra = f"""<section class="ref"><div class="wrap">
<h2>{n} to Spain: what each route pays</h2>
<p>{intro}</p>
<div class="board"><table><thead><tr><th>Destination</th><th>Distance from {n}</th><th>Outbound (UK261)</th><th>Return (EU261)</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<p class="lead" style="margin-top:12px">Per passenger, children included, for an arrival delay of 3+ hours, a cancellation with less than 14 days' notice, or denied boarding. One payment per flight.</p>
<h2 style="margin-top:32px">Delayed out of {n}? What to do at the airport</h2>
<ul><li><strong>2+ hours late:</strong> the airline must give you food and drink vouchers and a way to communicate.</li>
<li><strong>Overnight:</strong> hotel and transfers. If they don't arrange it, book something reasonable and keep every receipt.</li>
<li><strong>5+ hours:</strong> you can choose not to fly and get a full refund (but then there's no delay compensation).</li>
<li><strong>Get proof:</strong> a photo of the departures board and your boarding pass; ask staff for the reason in writing.</li></ul>
<h2 style="margin-top:32px">Claiming for a {n}–Spain flight</h2>
<p>Claim directly with the airline first, using its online EU261/UK261 compensation form; it's free. If it refuses or doesn't answer, escalate for free: after 8 weeks, <a href="{ctx['CAA_URL']}" rel="noopener">the CAA</a> or the airline's ADR scheme for flights out of {n}; after a month, <a href="{ctx['AESA_URL']}" rel="noopener">AESA</a> for flights home from Spain. Airline guides: <a href="/en/jet2-delay-compensation/">Jet2</a>, <a href="/en/easyjet-delay-compensation/">easyJet</a>, <a href="/en/tui-delay-compensation/">TUI</a>, <a href="/en/ryanair-delay-compensation/">Ryanair</a>.</p>
<h2 style="margin-top:32px">Common questions</h2>
{faq_html}
<p style="margin-top:24px"><a href="{HUB}">All UK airports to Spain →</a></p>
</div></section>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>"""
        path = u_uk(slug)
        rng = f"£{_uk(near_d)}–£{_uk(far_d)}" if _uk(near_d) != _uk(far_d) else f"£{_uk(far_d)}"
        erng = f"€{_eu(near_d)}–€{_eu(far_d)}" if _eu(near_d) != _eu(far_d) else f"€{_eu(far_d)}"
        title = f"{name} to Spain flight delay compensation: {rng}"
        if len(title) > 58:
            title = f"{name} to Spain delay compensation: {rng}"
        desc = f"{name}–Spain flight delayed 3+ hours or cancelled? Every route's payout: {rng} out (UK261), {erng} back (EU261), real distances."
        h1 = f"Delayed flight between {n} and Spain? Here's what you're owed"
        lede = f"Pick your route below or enter your flight: we use the real distance from {n} to work out your compensation under UK261 and EU261."
        body = ctx["hero"]("en", h1, lede, "", code, "AGP") + body_extra + ctx["reference_sections"]("en", True)
        alts = {"en": path}
        ctx["emit"]("en", path, ctx["page"]("en", title, desc, path, body, alts, None))
        hub_rows.append(f'<li><a href="{path}">{n} to Spain</a> — £{_uk(near_d)}–£{_uk(far_d)} out, €{_eu(near_d)}–€{_eu(far_d)} back</li>')

    hub_body = f"""<div class="wrap prose"><h1>UK airports to Spain: flight delay compensation by airport</h1>
<p>Flights between the UK and Spain are covered twice over: UK261 on the way out (paid in pounds) and EU261 on the way back (paid in euros). Pick your UK airport to see what every Spanish route pays, using real distances.</p>
<ul>{''.join(hub_rows)}</ul>
<h2>Why the amount depends on your UK airport</h2>
<p>Compensation is set by the great-circle distance of the flight, not the ticket price: £220 / €250 up to 1,500 km and £350 / €400 from 1,500 to 3,500 km. Barcelona, Girona or Madrid can fall either side of the 1,500 km line depending on where you fly from: from London they pay the lower band, from Scotland or Northern Ireland the higher one. Every Canary Islands route from the UK is in the £350 / €400 band.</p>
<h2>When you're owed it</h2>
<p>You arrive 3 hours or more late, your flight is cancelled with less than 14 days' notice, or you're denied boarding, and the cause was within the airline's control. Technical faults, crew shortages and the airline's own staff strikes don't get it off the hook; bad weather and air traffic control strikes usually do. Package holidays are covered too.</p>
<p>Or go straight to the <a href="/en/">compensation calculator</a>.</p></div>"""
    alts = {"en": HUB}
    ctx["emit"]("en", HUB, ctx["page"]("en", "UK airports to Spain: flight delay compensation guide",
                                        "Delay compensation for every UK airport to Spain route: £220–£350 under UK261 and €250–€400 under EU261, with real distances.",
                                        HUB, hub_body, alts, None))
    return [u_uk(s) for _, s, _, _ in UK] + [HUB]
