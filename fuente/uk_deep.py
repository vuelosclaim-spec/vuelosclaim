"""Deeper, airline-specific English content for the UK holiday airlines (TUI, Jet2, easyJet).

These pages get most of the site's Google impressions, so they carry extra unique content:
UK261 vs EU261 worked examples, refusal reasons, step-by-step claim and a page-level FAQ.
"""
import json
from html import escape as e

UK_ROUTES = {
    "tui": [("MAN", "TFS"), ("BHX", "PMI"), ("LGW", "ACE"), ("NCL", "ALC")],
    "jet2": [("MAN", "ALC"), ("LBA", "AGP"), ("BHX", "PMI"), ("GLA", "LPA")],
    "easyjet": [("LGW", "AGP"), ("BRS", "ALC"), ("LTN", "PMI"), ("EDI", "TFS")],
    "ryanair": [("STN", "AGP"), ("MAN", "ALC"), ("EDI", "PMI"), ("BHX", "TFS")],
    "wizz-air": [("LTN", "ALC"), ("LGW", "MAD"), ("BHX", "BCN"), ("LTN", "AGP")],
    "klm": [("LHR", "AMS"), ("MAN", "AMS"), ("EDI", "AMS"), ("BHX", "AMS")],
}

META = {
    "tui": dict(
        title="TUI Delay Compensation Claim: £220–£520 per Passenger",
        desc="Delayed 3+ hours with TUI? You're owed £220–£520 (UK261) or €250–€600 (EU261) per person, even on a package holiday. Free calculator and claim guide.",
        h1="TUI flight delayed or cancelled? Check what you can claim",
    ),
    "jet2": dict(
        title="Jet2 Delay Compensation Claim: £220–£520 per Passenger",
        desc="Delayed 3+ hours with Jet2 or Jet2holidays? Claim £220–£520 (UK261) or €250–€600 (EU261) per person. Free calculator, refusal reasons and how to claim.",
        h1="Jet2 flight delayed or cancelled? Check what you can claim",
    ),
    "easyjet": dict(
        title="easyJet Delay Compensation Claim: £220–£520 per Passenger",
        desc="Delayed 3+ hours with easyJet? You're owed £220–£520 (UK261) or €250–€600 (EU261) per person. Free calculator, when easyJet can refuse, and how to claim.",
        h1="easyJet flight delayed or cancelled? Check what you can claim",
    ),
}

META.update({
    "ryanair": dict(
        title="Ryanair Delay Compensation Claim: €250–€600 / £220–£520",
        desc="Ryanair flight delayed 3+ hours or cancelled? Claim €250–€600 (EU261) or £220–£520 (UK261) per person. Free calculator, ATC refusals and how to claim.",
        h1="Ryanair flight delayed or cancelled? Check what you can claim",
    ),
    "wizz-air": dict(
        title="Wizz Air Delay Compensation: €250–€600 per Passenger",
        desc="Wizz Air flight delayed 3+ hours, cancelled or rescheduled? Claim €250–€600 (EU261) or £220–£520 (UK261). Free calculator and step-by-step guide.",
        h1="Wizz Air flight delayed or cancelled? Check what you can claim",
    ),
    "klm": dict(
        title="KLM Delay Compensation: EU261 Claims and Missed Connections",
        desc="KLM flight delayed, cancelled or missed your connection in Amsterdam? Claim up to €600 under EU261. Free calculator, connections and overbooking.",
        h1="KLM flight delayed or missed connection? Check what you can claim",
    ),
})

TEXT = {
    "tui": dict(
        intro=("TUI flies most of its UK customers as part of a package holiday, and that often makes people think the flight "
               "isn't covered. It is: the flight rules apply on top of your package rights. If your TUI flight landed 3 hours "
               "or more late, was cancelled less than 14 days before departure, or you were bumped, you can claim a fixed amount per passenger."),
        who=("Flights operated by TUI Airways (the UK airline) from a UK airport fall under UK261 and pay in pounds. "
             "Flights back from Spain, Portugal, Greece or any EU airport fall under EU261 and pay in euros. TUI fly flights "
             "operated from Germany, Belgium or the Netherlands are EU airlines, so EU261 covers them in both directions within Europe."),
        quirk=("<strong>Vouchers:</strong> TUI may offer holiday credit instead of money. Compensation under UK261/EU261 is owed "
               "in cash (or bank transfer); you only have to accept a voucher if you agree to it in writing."),
        claim_where="TUI's online customer claim form on its website (look for the flight delay or compensation claim section)",
        faq=[
            ("Can I claim TUI delay compensation on a package holiday?",
             "Yes. A package holiday does not remove your flight compensation rights. If the TUI flight arrived 3 hours or more late and the cause was within TUI's control, you can claim £220–£520 (UK261) or €250–€600 (EU261) per passenger, on top of any package-holiday rights."),
            ("How long does a TUI flight need to be delayed to get compensation?",
             "At least 3 hours late at the final destination, measured when the aircraft doors open. Shorter delays don't qualify for compensation, although from 2 hours TUI must offer food and drink."),
            ("Are TUI flights covered by EU261?",
             "Flights from any EU airport, including the return from Spain, are covered by EU261. Flights departing the UK are covered by UK261, the British version with the same rules paid in pounds."),
            ("TUI refused my claim. What now?",
             "Ask TUI for the specific reason in writing. Technical faults and crew problems are not valid reasons. If they still refuse, escalate to the ADR scheme TUI belongs to or to the UK Civil Aviation Authority (UK departures), or to AESA for flights departing Spain. Both routes are free."),
        ],
    ),
    "jet2": dict(
        intro=("Jet2.com operates every Jet2holidays flight, so whether you booked flight-only or a package, the same compensation "
               "rules apply. If your Jet2 flight landed 3 hours or more late, was cancelled at short notice or overbooked, "
               "you are owed a fixed amount per passenger regardless of what you paid for the ticket."),
        who=("Jet2 is a UK airline. Its flights out of the UK are covered by UK261 (paid in pounds). Its flights back to the UK from "
             "Spain, the Canaries, the Balearics or any other EU airport are covered by EU261 (paid in euros), because EU261 applies to "
             "every flight departing the EU, whatever the airline."),
        quirk=("<strong>Common refusal reason:</strong> Jet2 often cites air traffic control restrictions. ATC strikes and slot restrictions "
               "can be genuine extraordinary circumstances, but a delay knocked on from an earlier technical fault or a crew shortage is not. "
               "Ask Jet2 which flight the problem started on and why."),
        claim_where="Jet2's online flight delay claim form on its website, in the help and customer services section",
        faq=[
            ("How much compensation does Jet2 pay for a delayed flight?",
             "It depends on distance, not ticket price: £220 up to 1,500 km, £350 for 1,500–3,500 km and £520 above that (UK261), or €250/€400/€600 under EU261. Most Jet2 routes to Spain pay £220 or £350, and Canary Islands routes £350 / €400."),
            ("Does Jet2holidays count for EU261 compensation?",
             "Yes. Jet2holidays flights are operated by Jet2.com, so the normal UK261 and EU261 rules apply as for a flight-only booking."),
            ("How long do I have to claim from Jet2?",
             "In the UK you generally have up to 6 years (5 in Scotland) through the courts; for flights departing Spain the limit is 5 years. Claiming as soon as possible is easier, while you still have your boarding pass and booking details."),
            ("Jet2 refused my compensation. What can I do?",
             "Ask for the exact reason in writing. Technical problems and staff shortages don't count as extraordinary circumstances. If Jet2 maintains the refusal, escalate for free to the ADR scheme it belongs to or the UK Civil Aviation Authority, or to AESA for flights departing Spain."),
        ],
    ),
    "easyjet": dict(
        intro=("easyJet flies more routes between the UK and Spain than almost anyone, and it publishes its own EU261 claim process. "
               "If your easyJet flight arrived 3 hours or more late, was cancelled less than 14 days before departure, or you were "
               "denied boarding, you can claim a fixed amount per passenger, plus meals and hotel if you were stranded."),
        who=("easyJet operates through three airlines: easyJet UK, easyJet Europe (Austria) and easyJet Switzerland. Flights departing the UK are "
             "covered by UK261 in pounds. Flights departing Spain or any EU airport are covered by EU261 in euros. Flights into the EU from the UK "
             "are also covered by EU261 when operated by easyJet Europe, an EU airline."),
        quirk=("<strong>Expenses vs compensation:</strong> easyJet handles expense claims (meals, hotel, transport) separately from fixed "
               "compensation. You can claim both: keep every receipt and ask explicitly for the EU261/UK261 compensation as well."),
        claim_where="easyJet's EU261 compensation claim form on its website, under Help → Claims",
        faq=[
            ("When can I claim compensation from easyJet?",
             "When your flight arrived 3 or more hours late, was cancelled less than 14 days before departure, or you were bumped, and the cause was within easyJet's control (technical faults and crew issues count as within its control)."),
            ("How much compensation for a cancelled easyJet flight?",
             "£220–£520 under UK261 or €250–€600 under EU261 per passenger, depending on distance, plus a refund or rebooking. If easyJet reroutes you and you arrive close to the original time, the amount can be halved."),
            ("Are easyJet flights covered by EU261?",
             "All easyJet flights departing an EU airport are covered by EU261. Flights departing the UK are covered by UK261, the UK version of the same rules."),
            ("easyJet rejected my claim. What next?",
             "Ask for the reason in writing. If you disagree, escalate for free to the ADR scheme easyJet belongs to or the UK Civil Aviation Authority for UK departures, or to AESA for flights departing Spain."),
        ],
    ),
}

TEXT.update({
    "ryanair": dict(
        intro=("Ryanair carries more passengers in Europe than any other airline, and it pays EU261 compensation through its own online form "
               "once a claim is valid. If your Ryanair flight reached its destination 3 hours or more late, was cancelled less than 14 days "
               "before departure, or you were denied boarding, you can claim a fixed amount per passenger whatever you paid for the ticket."),
        who=("Most Ryanair flights are operated by Ryanair DAC, an Irish and therefore EU airline, so EU261 covers them in both directions "
             "within Europe, including flights from the UK into Spain. Flights departing the UK are also covered by UK261. Group airlines such "
             "as Buzz, Malta Air and Lauda Europe are EU airlines too. You get one payment per flight, not one under each set of rules."),
        quirk=("<strong>Common refusal reason:</strong> Ryanair often cites air traffic control. French or Spanish ATC strikes and slot "
               "restrictions can be genuine extraordinary circumstances, but a delay caused by a technical fault, missing crew or a late "
               "aircraft from an earlier problem of its own is not. Ask Ryanair in writing for the specific cause."),
        claim_where="Ryanair's EU261 compensation claim form on its website (Help Centre, under claims)",
        faq=[
            ("How much does Ryanair pay for a delayed flight?",
             "It depends on the distance, not the fare: €250 up to 1,500 km, €400 from 1,500 to 3,500 km and €600 beyond, or £220/£350/£520 under UK261 for flights from the UK. Most Ryanair routes between the UK and Spain pay €250–€400."),
            ("Does Ryanair pay compensation for ATC delays?",
             "Not when the delay was genuinely caused by air traffic control restrictions or an ATC strike. But if ATC is only part of the story, and the knock-on came from an earlier technical or crew problem, compensation is still owed. Ask for the cause in writing."),
            ("How long does Ryanair take to pay compensation?",
             "Valid claims are often answered within weeks, but it varies. If Ryanair hasn't resolved your claim after 8 weeks, escalate for free to the enforcement body of the country the flight departed from, for example AESA for Spain."),
            ("Ryanair rejected my claim. What can I do?",
             "Check the reason they gave against the rules: technical faults, crew shortages and Ryanair's own staff strikes don't count as extraordinary. Then escalate for free to the national enforcement body of the departure country, or the CAA for flights from the UK."),
        ],
    ),
    "wizz-air": dict(
        intro=("Wizz Air often reschedules flights by hours or moves them to another day, and many passengers accept the change without "
               "knowing a cash payment may be owed. If your Wizz Air flight arrived 3 hours or more late, was cancelled or significantly "
               "rescheduled less than 14 days before departure, or you were denied boarding, you can claim a fixed amount per passenger."),
        who=("Wizz Air flies under three airlines: Wizz Air Hungary and Wizz Air Malta, which are EU airlines, and Wizz Air UK. Flights "
             "departing Spain or any EU airport are covered by EU261 in euros; flights departing the UK by UK261 in pounds. A flight into "
             "the EU operated by Wizz Air Hungary or Malta is covered by EU261 too."),
        quirk=("<strong>Schedule changes:</strong> moving your flight by several hours with less than 14 days' notice counts as a cancellation "
               "under EU261, so compensation can apply even if you flew on the new time. Keep the email Wizz Air sent you about the change, "
               "and claim the compensation in cash rather than accepting WIZZ credit unless you want it."),
        claim_where="Wizz Air's online claim form on its website (Help Centre, under refunds and compensation)",
        faq=[
            ("How much compensation does Wizz Air pay?",
             "€250 for flights up to 1,500 km, €400 from 1,500 to 3,500 km and €600 beyond (or £220/£350/£520 for flights from the UK), per passenger, if you arrive 3+ hours late or are cancelled at short notice."),
            ("Wizz Air moved my flight. Can I claim?",
             "If they told you less than 14 days before departure and the new times are several hours different, it can count as a cancellation with compensation. You can also choose a full refund instead of the new flight."),
            ("Do I have to accept WIZZ credit?",
             "No. Compensation and refunds under EU261 are owed in money. Credit is only an option if you agree to it."),
            ("Wizz Air didn't answer my claim. What next?",
             "After 8 weeks, escalate for free to the enforcement body of the country the flight departed from (AESA for Spain) or the CAA for flights from the UK."),
        ],
    ),
    "klm": dict(
        intro=("KLM is a Dutch, and therefore EU, airline, so EU261 protects its passengers on every flight departing Europe and on its "
               "flights into Europe from anywhere in the world. Most KLM trips change planes in Amsterdam, which makes missed connections "
               "the most common claim: what counts is how late you arrive at your final destination."),
        who=("Because KLM is an EU airline, EU261 covers its flights from the UK to Amsterdam and onward, its flights from Spain, and its "
             "long-haul flights back into Europe. Flights departing the UK are also covered by UK261. On a single booking with a connection, "
             "the delay is measured at the final destination, and the distance is the whole journey from your first departure."),
        quirk=("<strong>Missed connections:</strong> if a late first flight makes you miss your connection in Amsterdam and you reach your "
               "final destination 3+ hours late, compensation is based on the full journey distance, for example up to €600 to the US. "
               "On journeys over 3,500 km, an arrival 3 to 4 hours late pays half (€300)."),
        claim_where="KLM's online EU261 compensation claim form on its website (Customer Support, under claims)",
        faq=[
            ("How much compensation does KLM pay for a delay?",
             "€250 up to 1,500 km, €400 from 1,500 to 3,500 km (and all intra-EU flights over 1,500 km), €600 above 3,500 km. Long-haul delays of 3 to 4 hours pay €300. For flights from the UK, UK261 pays the same in pounds."),
            ("Can I claim from KLM for a missed connection?",
             "Yes, if both flights were on one booking and you reached your final destination 3 or more hours late because of something within KLM's control. The amount is based on the whole journey distance."),
            ("Does EU261 cover KLM flights from outside Europe?",
             "Yes. Because KLM is an EU airline, its flights into Europe are covered, for example New York to Amsterdam. Non-EU airlines are only covered on flights departing Europe."),
            ("Does KLM pay for overbooking?",
             "If you're denied boarding against your will, you're owed the same fixed compensation immediately, plus a refund or rerouting, and meals or a hotel while you wait."),
        ],
    ),
})


def _uk_amount(d):
    return 220 if d <= 1500 else 350 if d <= 3500 else 520


def _eu_amount(d):
    return 250 if d <= 1500 else 400 if d <= 3500 else 600


NAME_FIX = {"ACE": "Lanzarote", "LTN": "London Luton", "TFS": "Tenerife South", "LPA": "Gran Canaria", "STN": "London Stansted"}


def section(a, airports, km, names, aesa_url, caa_url):
    slug = a["slug"]
    t, n = TEXT[slug], e(a["name"])
    rows = []
    for uk, es in UK_ROUTES[slug]:
        if uk not in airports or es not in airports:
            continue
        d = km(airports[uk], airports[es])
        nu = e(NAME_FIX.get(uk) or names.get(uk) or airports[uk][2])
        ns = e(NAME_FIX.get(es) or names.get(es) or airports[es][2])
        rows.append(f"<tr><td>{nu} ⇄ {ns}</td><td>{d:,} km</td><td>£{_uk_amount(d)}</td><td>€{_eu_amount(d)}</td></tr>")
    faq_html = "".join(f"<h3>{e(q)}</h3><p>{e(ans)}</p>" for q, ans in t["faq"])
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in t["faq"]]}
    return f"""<section class="ref"><div class="wrap">
<h2>Can I claim compensation from {n}?</h2>
<p>{t['intro']}</p>
<ul>
<li><strong>Delay:</strong> 3 hours or more at your final destination (measured when the doors open, not when you land).</li>
<li><strong>Cancellation:</strong> told less than 14 days before departure.</li>
<li><strong>Overbooking:</strong> denied boarding against your will.</li>
<li><strong>Cause within the airline's control:</strong> technical faults, crew shortages and the airline's own staff strikes all count.</li>
</ul>
<h2 style="margin-top:32px">UK261 or EU261? Which rules cover your {n} flight</h2>
<p>{t['who']}</p>
<div class="board"><table><thead><tr><th>Example route</th><th>Distance</th><th>Leaving the UK (UK261)</th><th>Flying back (EU261)</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<p class="lead" style="margin-top:12px">Amounts per passenger, including children. Example routes; distances are great-circle as the rules require. You get one payment per flight, not both.</p>
<h2 style="margin-top:32px">When {n} can refuse (and when it can't)</h2>
<p>The airline doesn't have to pay if the delay was caused by <strong>extraordinary circumstances</strong>: severe weather, air traffic control strikes or restrictions, airport security problems, bird strikes or political unrest. It <strong>cannot</strong> refuse because of a technical fault found before or during the flight, a lack of crew, or a strike by its own staff.</p>
<p>{t['quirk']}</p>
<h2 style="margin-top:32px">How to claim from {n}, step by step</h2>
<ol>
<li><strong>Check the amount</strong> with the calculator above (it uses the real distance of your route).</li>
<li><strong>Gather your proof:</strong> booking reference, boarding passes and, if you can, a screenshot of the arrival time.</li>
<li><strong>Claim directly and for free</strong> through {t['claim_where']}. Ask explicitly for "compensation under UK261 / EU261 Article 7", not just expenses.</li>
<li><strong>Wait up to 8 weeks.</strong> If {n} refuses or doesn't answer, escalate for free: the airline's ADR scheme or the <a href="{caa_url}" rel="noopener">CAA</a> for UK departures, or <a href="{aesa_url}" rel="noopener">AESA</a> for flights departing Spain.</li>
<li><strong>Prefer not to deal with it?</strong> A claims company does it for you on a no-win, no-fee basis (typically 25–35% plus VAT).</li>
</ol>
<p>Flying from a regional airport? See <a href="/en/uk-airports-to-spain-flight-delay-compensation/">what every UK airport to Spain route pays</a>.</p>
<h2 style="margin-top:32px">{n} compensation: common questions</h2>
{faq_html}
</div></section>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>"""
