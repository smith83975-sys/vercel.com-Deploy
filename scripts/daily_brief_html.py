#!/usr/bin/env python3
"""VaultPulse Daily Brief: builds markdown + MailerLite-ready HTML email from live data. Never sends.
Usage: python3 scripts/daily_brief_html.py [out.html] [out.md]"""
import json, sys, os, re, html, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from daily_brief import get, spot, SITE, ROOT, featured
import daily_brief

FORECAST = re.compile(r"\b(forecast|target|predict|outlook|could (hit|reach)|will (hit|reach)|to (hit|reach)|expects?|sees?|projection|price call|by 20\d\d|next year)\b", re.I)
TIPS = ["\"Registered\" COMEX metal has a warrant attached and can be delivered against futures; \"eligible\" metal meets exchange standards but isn't warranted.",
        "One COMEX silver contract (SI) is 5,000 oz; one standard gold contract (GC) is 100 oz.",
        "The gold/silver ratio tells you how many ounces of silver equal one ounce of gold. Historically it has ranged from about 12 to above 100.",
        "Spot price is for immediate delivery; coins and bars sell above spot, and the difference is called the premium."]
E = html.escape
GOLD, INK, CARD, MUTED = "#d4a937", "#0f1115", "#181b22", "#9aa3b2"
FONT = "font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;"

def headlines():
    try: items = get(SITE + "/api/news")["items"]
    except Exception: items = []
    seen, top = set(), []
    for it in items:
        k = it["title"].lower()[:60]
        if k in seen or FORECAST.search(it["title"]): continue
        seen.add(k); top.append(it)
        if len(top) == 5: break
    return top

def section(title):
    return f'<tr><td style="padding:28px 28px 10px;{FONT}font-size:13px;letter-spacing:2px;text-transform:uppercase;color:{GOLD};font-weight:700;">{title}</td></tr>'

def build():
    now = dt.datetime.now(dt.timezone.utc)
    top = headlines(); g, _ = spot("XAU"); s, _ = spot("XAG")
    tanks = {t["metal"]: t for t in json.load(open(os.path.join(ROOT, "data/tank.json")))["tanks"]}
    stamp = now.strftime('%Y-%m-%d %H:%M') + " UTC"
    subject = f"VaultPulse Daily Brief: your gold & silver catch-up for {now.strftime('%b %d')}"
    R = []
    # header
    R.append(f'''<tr><td style="background:{INK};padding:24px 28px;border-bottom:3px solid {GOLD};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
<td width="56" valign="middle"><img src="{SITE}/logo-email.png" width="48" height="48" alt="VaultPulse" style="display:block;border-radius:24px;border:0;"></td>
<td valign="middle" style="{FONT}padding-left:12px;"><div style="font-size:24px;font-weight:800;color:#ffffff;letter-spacing:.5px;">Vault<span style="color:{GOLD};">Pulse</span></div>
<div style="font-size:12px;color:{MUTED};letter-spacing:1px;text-transform:uppercase;">Daily Brief &middot; {now.strftime('%A, %b %d, %Y')}</div></td></tr></table></td></tr>''')
    # intro
    R.append(f'<tr><td style="padding:26px 28px 4px;{FONT}font-size:16px;line-height:1.6;color:#e8e8ea;"><b style="color:#fff;font-size:19px;">Good day, and thanks for reading! &#9728;&#65039;</b><br>Here\'s your quick, sourced look at what moved in gold and silver news today, plus a fresh check on the COMEX vaults. Grab a coffee; this takes two minutes.</td></tr>')
    # spot strip
    if g and s:
        cell = lambda lab, val, c: f'<td class="stack" width="33%" align="center" style="padding:14px 6px;{FONT}"><div style="font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:{MUTED};">{lab}</div><div style="font-size:22px;font-weight:800;color:{c};">{val}</div></td>'
        R.append(f'''<tr><td style="padding:18px 28px 0;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{CARD};border:1px solid #2a2f3a;border-radius:10px;"><tr>
{cell("Gold spot", f"${g:,.2f}", GOLD)}{cell("Silver spot", f"${s:,.2f}", "#c9d1dc")}{cell("Gold/Silver", f"{g/s:.1f}", "#ffffff")}
</tr><tr><td colspan="3" align="center" style="padding:0 10px 12px;{FONT}font-size:11px;color:{MUTED};">Per troy oz &middot; gold-api.com, {stamp}<br>How the ratio is calculated: {g/s:.1f} = ${g:,.2f} gold spot &divide; ${s:,.2f} silver spot (both gold-api.com, {stamp})</td></tr></table></td></tr>''')
    # featured (config: FEATURED in daily_brief.py)
    feats = featured(now)
    if feats: R.append(section("Featured"))
    for f in feats:
        R.append(f'''<tr><td style="padding:0 28px 4px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#2a2310;border:1px solid {GOLD};border-radius:10px;"><tr><td style="padding:16px 18px;{FONT}">
<div style="font-size:12px;letter-spacing:1.5px;text-transform:uppercase;color:{GOLD};font-weight:700;">&#10024; {E(f['label'])}</div>
<a href="{E(f['url'])}" style="display:block;color:#ffffff;text-decoration:none;font-size:18px;line-height:1.35;font-weight:800;padding:4px 0 6px;">{E(f['title'])}</a>
<div style="font-size:15px;line-height:1.55;color:#f3e6c0;">{E(f['blurb'])}</div>
<div style="padding-top:10px;"><a href="{E(f['url'])}" style="color:{GOLD};font-size:15px;font-weight:700;text-decoration:none;">{E(f['cta'])} &rarr;</a></div></td></tr></table></td></tr>''')
    # headlines
    R.append(section("Today's top headlines"))
    if top:
        for it in top:
            R.append(f'''<tr><td style="padding:0 28px 10px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{CARD};border-left:3px solid {GOLD};border-radius:6px;"><tr><td style="padding:14px 16px;{FONT}">
<a href="{E(it['link'])}" style="color:#ffffff;text-decoration:none;font-size:16px;line-height:1.4;font-weight:600;">{E(it['title'])}</a>
<div style="font-size:12px;color:{MUTED};padding-top:6px;">{E(it.get('source',''))} &rarr; <a href="{E(it['link'])}" style="color:{GOLD};text-decoration:none;">Read</a></div></td></tr></table></td></tr>''')
    else:
        R.append(f'<tr><td style="padding:0 28px;{FONT}color:{MUTED};font-size:14px;">The news feed was quiet when this brief was built. Check the live box on the site anytime.</td></tr>')
    # snapshot
    rows = []
    sv, gd = tanks.get("silver"), tanks.get("gold")
    if sv:
        rows.append(("COMEX silver", f"{sv['registered_oz']/1e6:.1f}M oz registered / {sv['total_oz']/1e6:.1f}M oz total", f"{sv['total_source']}, as of {sv['total_date']}. How it's calculated: total = {sv['registered_oz']/1e6:.2f}M oz registered + {sv['eligible_oz']/1e6:.2f}M oz eligible; registered share {100*sv['registered_oz']/sv['total_oz']:.1f}% = registered ÷ total."))
        rows.append(("Silver deliveries Oct MTD", f"{sv['mtd_contracts']:,} contracts (~{sv['mtd_contracts']*sv['oz_per_contract']/1e6:.2f}M oz)", f"{sv['mtd_source']}, as of {sv['mtd_date']}. How it's calculated: {sv['mtd_contracts']:,} contracts × {sv['oz_per_contract']:,} oz per contract."))
    if gd:
        rows.append(("COMEX gold registered", f"~{gd['registered_oz']/1e6:.1f}M oz", f"{gd['registered_source']}, as of {gd['registered_date']}"))
        rows.append(("Gold deliveries Oct MTD", f"{gd['mtd_contracts']:,} contracts (~{gd['mtd_contracts']*gd['oz_per_contract']/1e6:.2f}M oz)", f"{gd['mtd_source']}, as of {gd['mtd_date']}. How it's calculated: {gd['mtd_contracts']:,} contracts × {gd['oz_per_contract']:,} oz per contract."))
    R.append(section("Vault snapshot"))
    inner = "".join(f'<tr><td style="padding:12px 16px;border-bottom:1px solid #2a2f3a;{FONT}"><div style="font-size:12px;color:{MUTED};text-transform:uppercase;letter-spacing:1px;">{E(a)}</div><div style="font-size:16px;color:#fff;font-weight:700;padding:2px 0;">{E(b)}</div><div style="font-size:11px;color:{MUTED};">{E(c)}</div></td></tr>' for a, b, c in rows)
    R.append(f'<tr><td style="padding:0 28px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{CARD};border-radius:10px;border:1px solid #2a2f3a;">{inner}</table></td></tr>')
    # good to know
    tip = TIPS[now.toordinal() % len(TIPS)]
    R.append(f'<tr><td style="padding:24px 28px 0;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#2a2310;border:1px solid {GOLD};border-radius:10px;"><tr><td style="padding:16px 18px;{FONT}font-size:15px;line-height:1.55;color:#f3e6c0;"><b style="color:{GOLD};">&#128161; Good to know</b><br>{E(tip)}</td></tr></table></td></tr>')
    # CTA
    R.append(f'''<tr><td align="center" style="padding:28px 28px 8px;"><table role="presentation" cellpadding="0" cellspacing="0"><tr><td bgcolor="{GOLD}" style="border-radius:8px;">
<a href="{SITE}" style="display:inline-block;padding:14px 30px;{FONT}font-size:16px;font-weight:800;color:{INK};text-decoration:none;">See live news &amp; vault tanks &rarr;</a></td></tr></table>
<div style="{FONT}font-size:15px;color:#e8e8ea;padding-top:18px;">Thanks for being part of VaultPulse. See you tomorrow! &#129689;</div></td></tr>''')
    # footer
    R.append(f'''<tr><td style="padding:24px 28px 28px;border-top:1px solid #2a2f3a;{FONT}font-size:12px;line-height:1.6;color:{MUTED};" align="center">
<b style="color:#c9d1dc;">Not financial advice.</b> Headlines are from third-party sources and copied as published; VaultPulse doesn't endorse them. Figures are dated and sourced above.<br><br>
<a href="{{$url}}" style="color:{GOLD};">View in browser</a> &nbsp;&middot;&nbsp; <a href="{{$unsubscribe}}" style="color:{GOLD};">Unsubscribe</a> &nbsp;&middot;&nbsp; <a href="{SITE}" style="color:{GOLD};">vaultpulsehq.com</a></td></tr>''')
    pre = f"Gold ${g:,.2f} · Silver ${s:,.2f} · ratio {g/s:.1f} + today's top headlines" if g and s else "Today's gold & silver headlines and vault check"
    doc = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark light"><meta name="supported-color-schemes" content="dark light"><title>{E(subject)}</title>
<style>body{{margin:0;padding:0;}} @media (max-width:620px){{.wrap{{width:100%!important;}} .stack{{display:block!important;width:100%!important;}}}}</style></head>
<body style="margin:0;padding:0;background:#07080a;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">{E(pre)}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="#07080a" style="background:#07080a;"><tr><td align="center" style="padding:20px 8px;">
<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" bgcolor="{INK}" style="width:600px;max-width:600px;background:{INK};border-radius:12px;overflow:hidden;">
{"".join(R)}
</table></td></tr></table></body></html>'''
    return subject, doc, top

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/workspace/brief_today.html"
    md = sys.argv[2] if len(sys.argv) > 2 else "/workspace/brief_today.md"
    subject, doc, top = build()
    open(out, "w").write(doc)
    sys.argv = [sys.argv[0], md]; daily_brief.main()
    print(out, "|", subject)
