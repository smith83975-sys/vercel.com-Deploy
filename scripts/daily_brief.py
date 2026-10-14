#!/usr/bin/env python3
"""VaultPulse Daily Brief generator. Builds a markdown email draft; never sends.
Usage: python3 scripts/daily_brief.py [out.md]"""
import json, sys, os, urllib.request, datetime as dt
FORECAST = __import__("re").compile(r"\b(forecast|target|predict|outlook|could (hit|reach)|will (hit|reach)|to (hit|reach)|expects?|sees?|projection|price call|by 20\d\d|next year)\b", 2)
SITE = "https://vaultpulse-weld.vercel.app"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
         "Here's your quick, sourced look at what moved in gold and silver news today, plus a fresh check on the COMEX vaults. Grab a coffee; this takes two minutes.", "",
         "## Today's top headlines"]
    if top:
        for i, it in enumerate(top, 1): L.append(f"{i}. [{it['title']}]({it['link']}) ({it['source']})")
    else: L.append("_The news feed was quiet when this brief was built. Check the live box on the site anytime._")
    L += ["", "## Vault snapshot"]
    if g and s:
        L.append(f"- **Gold spot:** ${g:,.2f}/oz; **Silver spot:** ${s:,.2f}/oz (gold-api.com, {now.strftime('%Y-%m-%d %H:%M')} UTC)")
        L.append(f"- **Gold/silver ratio:** {g/s:.1f} (our calculation from the spot prices above)")
    sv, gd = tanks.get("silver"), tanks.get("gold")
    if sv:
        L.append(f"- **COMEX silver:** {sv['registered_oz']/1e6:.1f}M oz registered, {sv['total_oz']/1e6:.1f}M oz total in all vaults ({sv['total_source']}, as of {sv['total_date']})")
        L.append(f"- **Silver deliveries Oct MTD:** {sv['mtd_contracts']:,} contracts (~{sv['mtd_contracts']*sv['oz_per_contract']/1e6:.2f}M oz) ({sv['mtd_source']}, as of {sv['mtd_date']})")
    if gd:
        L.append(f"- **COMEX gold registered:** ~{gd['registered_oz']/1e6:.1f}M oz ({gd['registered_source']}, as of {gd['registered_date']})")
        L.append(f"- **Gold deliveries Oct MTD:** {gd['mtd_contracts']:,} contracts (~{gd['mtd_contracts']*gd['oz_per_contract']/1e6:.2f}M oz) ({gd['mtd_source']}, as of {gd['mtd_date']})")
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
