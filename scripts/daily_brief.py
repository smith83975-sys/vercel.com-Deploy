#!/usr/bin/env python3
"""VaultPulse Daily Brief generator. Builds a markdown email draft; never sends.
Usage: python3 scripts/daily_brief.py [out.md]"""
import json, sys, os, urllib.request, datetime as dt
FORECAST = __import__("re").compile(r"\b(forecast\w*|target\w*|predict\w*|outlook\w*|could (hit|reach)|will (hit|reach)|to (hit|reach)|expects?|sees?|projection|price call|by 20\d\d|next year|(under|over)valued|silver (generation|economy|anniversary|medal\w*|screen))\b", 2)
SITE = "https://vaultpulsehq.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Featured block: edit this list to swap what's promoted in the brief (empty list = no block).
# "until" (YYYY-MM-DD, optional) hides an item after that date; "from" (optional) hides it before that date.
FEATURED = [
    {"label": "Notable move",
     "title": "Gold deliveries jump to 552 contracts on Oct 16",
     "blurb": "552 GC contracts × 100 oz = 55,200 oz (~1.72 t) delivered on Oct 16; that one day is 552 ÷ 1,767 = ~31% of calendar-October GC deliveries through Oct 16. JP Morgan Securities' customer account issued 543; biggest stoppers Barclays (customer) 200, JP Morgan (customer) 120, BMO (house) 100. Silver quiet at 18 SI contracts. Source: CME Group daily Issues and Stops report, Oct 16, 2026, via The Vault Report.",
     "url": SITE + "/flow",
     "cta": "See COMEX deliveries",
     "from": "2026-10-19", "until": "2026-10-19"},
    {"label": "Today in metals",
     "title": "Warsh keeps his cards close in Bangkok",
     "blurb": "Fed Chair Kevin Warsh told the IMF's Kristalina Georgieva he doesn't \"prejudge meetings,\" giving no hint on the Oct 27-28 decision, while noting \"a synchronous tightening\" by central banks worldwide. The Bloomberg dollar index slipped 0.2% and gold rose 0.2% to about $4,180 after his remarks (Bloomberg); silver was $57.81, up 0.7%, at 04:33 GMT (Reuters).",
     "url": "https://finance.yahoo.com/economy/policy/articles/feds-warsh-gives-no-hint-040051405.html",
     "cta": "Read the Reuters report",
     "until": "2026-10-16"},
    {"label": "New on VP",
     "title": "Silver manipulation history",
     "blurb": "What's proven, what isn't, with official sources: 12 dated cases from CFTC, DOJ and court records, sorted into proven, alleged and dismissed.",
     "url": SITE + "/silver-manipulation-history",
     "cta": "Read the case history",
     "until": "2026-11-15"},
    {"label": "New on VP",
     "title": "Is silver a \"Tier 1\" asset?",
     "blurb": "No. \"Tier 1\" is a type of bank capital. Gold's actual status is a 0% risk weight on allocated bullion under Basel rule CRE20.110, and silver isn't on that list. We found no BIS proposal to change that (checked Oct 17, 2026). Our explainer covers what such a change would touch mechanically, along with the big unknowns, with rule text for every claim.",
     "url": SITE + "/bis-silver-tier1",
     "cta": "Read the explainer",
     "from": "2026-10-18", "until": "2026-10-18"},
]
def featured(now=None):
    d = (now or dt.datetime.now(dt.timezone.utc)).strftime("%Y-%m-%d")
    return [f for f in FEATURED if (not f.get("until") or d <= f["until"]) and (not f.get("from") or d >= f["from"])]
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "VaultPulse-brief/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r: return json.load(r)
def spot(sym):
    try: d = get(f"https://api.gold-api.com/price/{sym}"); return float(d["price"]), d.get("updatedAt", "")
    except Exception: return None, None
def main():
    now = dt.datetime.now(dt.timezone.utc); today = now.strftime("%A, %b %d, %Y")
    try: items = get(SITE + "/api/news")["items"]
    except Exception: items = []
    seen, top = set(), []
    for it in items:
        k = it["title"].lower()[:60]
        if k in seen or FORECAST.search(it["title"]): continue
        seen.add(k); top.append(it)
        if len(top) == 5: break
    g, gt = spot("XAU"); s, st = spot("XAG")
    tanks = {t["metal"]: t for t in json.load(open(os.path.join(ROOT, "data/tank.json")))["tanks"]}
    L = [f"**Subject:** VaultPulse Daily Brief: your gold & silver catch-up for {now.strftime('%b %d')}", "",
         "Good day, and thanks for reading!", "",
         "Here's your quick, sourced look at what moved in gold and silver news today, plus a fresh check on the COMEX vaults. Grab a coffee; this takes two minutes.", ""]
    feats = featured(now)
    if feats: L.append("## Featured")
    for f in feats:
        L += [f"**{f['label']}: {f['title']}.** {f['blurb']} [{f['cta']}]({f['url']})", ""]
    L += ["## Today's top headlines"]
    if top:
        for i, it in enumerate(top, 1): L.append(f"{i}. [{it['title']}]({it['link']}) ({it['source']})")
    else: L.append("_The news feed was quiet when this brief was built. Check the live box on the site anytime._")
    L += ["", "## Vault snapshot"]
    if g and s:
        L.append(f"- **Gold spot:** ${g:,.2f}/oz; **Silver spot:** ${s:,.2f}/oz (gold-api.com, {now.strftime('%Y-%m-%d %H:%M')} UTC)")
        L.append(f"- **Gold/silver ratio:** {g/s:.1f} = ${g:,.2f} gold spot ÷ ${s:,.2f} silver spot (both gold-api.com, {now.strftime('%Y-%m-%d %H:%M')} UTC)")
    sv, gd = tanks.get("silver"), tanks.get("gold")
    if sv:
        L.append(f"- **COMEX silver:** {sv['registered_oz']/1e6:.1f}M oz registered, {sv['total_oz']/1e6:.1f}M oz total in all vaults ({sv['total_source']}, as of {sv['total_date']}); total = {sv['registered_oz']/1e6:.2f}M registered + {sv['eligible_oz']/1e6:.2f}M eligible, registered share {100*sv['registered_oz']/sv['total_oz']:.1f}% = registered ÷ total")
        L.append(f"- **Silver deliveries Oct MTD:** {sv['mtd_contracts']:,} contracts (~{sv['mtd_contracts']*sv['oz_per_contract']/1e6:.2f}M oz = {sv['mtd_contracts']:,} × {sv['oz_per_contract']:,} oz) ({sv['mtd_source']}, as of {sv['mtd_date']})")
    if gd:
        L.append(f"- **COMEX gold registered:** ~{gd['registered_oz']/1e6:.1f}M oz ({gd['registered_source']}, as of {gd['registered_date']})")
        L.append(f"- **Gold deliveries Oct MTD:** {gd['mtd_contracts']:,} contracts (~{gd['mtd_contracts']*gd['oz_per_contract']/1e6:.2f}M oz = {gd['mtd_contracts']:,} × {gd['oz_per_contract']:,} oz) ({gd['mtd_source']}, as of {gd['mtd_date']})")
    tips = ["\"Registered\" COMEX metal has a warrant attached and can be delivered against futures; \"eligible\" metal meets exchange standards but isn't warranted.",
            "One COMEX silver contract (SI) is 5,000 oz; one standard gold contract (GC) is 100 oz.",
            "The gold/silver ratio tells you how many ounces of silver equal one ounce of gold. Historically it has ranged from about 12 to above 100.",
            "Spot price is for immediate delivery; coins and bars sell above spot, and the difference is called the premium."]
    L += ["", "## Good to know", tips[now.toordinal() % len(tips)], "",
          f"Live news, vault tanks and the full ratio history are on the site: [{SITE.replace('https://','')}]({SITE})", "",
          "Thanks for being part of VaultPulse. See you tomorrow!", "", "---",
          "_Not financial advice. Headlines are from third-party sources; VaultPulse doesn't endorse them. Figures are dated and sourced above._"]
    out = sys.argv[1] if len(sys.argv) > 1 else "/workspace/brief_today.md"
    open(out, "w").write("\n".join(L) + "\n"); print(out)
if __name__ == "__main__": main()
