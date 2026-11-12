"""Body HTML for /beyond-comex, built from data/beyond_comex.json (scripts/fetch_beyond_comex.py)
plus the COMEX and premium blocks already in data/latest.json. No number is typed in here."""
import html, datetime
import calc_basis as CB

E = html.escape
def D(iso): return CB.D(iso)
def moz(n): return f"{n/1e6:,.2f}M oz"
def a(url, t): return f'<a href="{E(url)}" rel="noopener">{t}</a>'

def _unavail(v, label):
    lv = v.get('last_verified') or {}
    tail = ''
    if lv:
        tail = ' Last verified figure is shown in the table with its own date.'
    return f'<p class="note"><b>{label}: unavailable</b> (checked {CB.ts(v.get("checked_at"))}): {E(v.get("reason","no reason recorded"))}.{tail}</p>'

def rows(L, BX):
    """Flat list of (key, metal, label, oz, as_of, scope, src_name, url, calc, status) used by page + chart."""
    out = []
    c = L['comex']; rd = c['report_date']
    for m in ('silver', 'gold'):
        x = c[m]
        out.append(dict(key='comex', metal=m, label='COMEX vaults (total)', oz=x['total_oz'], reg_oz=x['registered_oz'], as_of=rd,
                        scope=f"Registered + eligible. Registered [warranted, deliverable vs futures]: {moz(x['registered_oz'])}.",
                        src='CME Group warehouse report via The Vault Report', url=c['source_url'], calc=None, status='ok'))
    def g(k): 
        v = BX.get(k) or {}
        if v.get('status') == 'unavailable' and v.get('last_verified'): return v['last_verified'], v
        return v, v
    lb, lbs = g('lbma')
    for m in ('silver', 'gold'):
        x = lb.get(m)
        if x and x.get('status') == 'ok':
            out.append(dict(key='lbma', metal=m, label='London vaults (LBMA)', oz=x['oz'], as_of=x['as_of'], as_of_label=x.get('as_of_label'),
                            scope='All London custodian vaults incl. Bank of England gold; includes metal held for London-vaulted ETFs.',
                            src='LBMA London Vault Data', url=x['source_url'],
                            calc=f"{x['oz']:,} oz = {x['tonnes']:,.0f} tonnes (LBMA, end {D(x['as_of'])}) × {BX['oz_per_tonne']:,} oz per tonne.", status='stale' if lbs.get('status')=='unavailable' else 'ok'))
    sh, shs = g('shfe')
    for m in ('silver', 'gold'):
        x = sh.get(m)
        if x and x.get('status') == 'ok':
            out.append(dict(key='shfe', metal=m, label='Shanghai Futures Exchange (warranted)', oz=x['oz'], as_of=x['as_of'],
                            scope='Warranted (deliverable) stock only, so compare with COMEX registered, not COMEX total.',
                            src='SHFE daily warrant report', url=x['source_url'],
                            calc=f"{x['oz']:,} oz = {x['kg']:,.0f} kg (SHFE, {D(x['as_of'])}) × {BX['oz_per_kg']} oz per kg.", status='stale' if shs.get('status')=='unavailable' else 'ok'))
    sg, sgs = g('sge')
    x = sg.get('silver')
    if x and x.get('status') == 'ok':
        out.append(dict(key='sge', metal='silver', label='Shanghai Gold Exchange vaults', oz=x['oz'], as_of=x['as_of'], as_of_label='week ending '+D(x['as_of']),
                        scope='Silver in SGE designated warehouses (weekly report).', src='SGE weekly report', url=x['source_url'],
                        calc=f"{x['oz']:,} oz = {x['kg']:,.0f} kg (SGE weekly report, week ending {D(x['as_of'])}) × {BX['oz_per_kg']} oz per kg.", status='stale' if sgs.get('status')=='unavailable' else 'ok'))
    for k, m, label, src in (('slv', 'silver', 'iShares Silver Trust (SLV)', 'iShares'), ('pslv', 'silver', 'Sprott Physical Silver Trust (PSLV)', 'Sprott'),
                             ('gld', 'gold', 'SPDR Gold Shares (GLD)', 'SPDR Gold Shares')):
        x, xs = g(k)
        if x and x.get('status') == 'ok':
            out.append(dict(key=k, metal=m, label=label, oz=x['oz'], as_of=x['as_of'], scope='Metal the trust reports holding; published bar list linked below.',
                            src=src, url=x['source_url'], calc=None, status='stale' if xs.get('status')=='unavailable' else 'ok'))
    return out

def body(L, BX):
    R = rows(L, BX)
    unav = ''.join(_unavail(BX[k], n) for k, n in (('lbma','LBMA'),('shfe','SHFE'),('sge','SGE'),('slv','SLV'),('gld','GLD'),('pslv','PSLV'))
                   if (BX.get(k) or {}).get('status') == 'unavailable')
    def table(metal):
        trs = ''
        for r in [r for r in R if r['metal'] == metal]:
            asof = r.get('as_of_label') or D(r['as_of'])
            stale = ' <span class="note">(last verified; latest fetch failed)</span>' if r['status'] == 'stale' else ''
            trs += (f'<tr><td data-l="Where"><b>{E(r["label"])}</b><br><span class="note">{E(r["scope"])}</span></td>'
                    f'<td data-l="Ounces">{r["oz"]:,.0f} oz<br><span class="note">{moz(r["oz"])}</span>{stale}</td>'
                    f'<td data-l="As of">{E(asof)}</td><td data-l="Source">{a(r["url"], E(r["src"]))}</td></tr>')
            if r['calc']: trs += f'<tr><td colspan="4">{CB.html_line(r["calc"])}</td></tr>'
        return f'<div style="overflow-x:auto"><table class="bcx"><thead><tr><th>Where</th><th>Holdings</th><th>As of</th><th>Source</th></tr></thead><tbody>{trs}</tbody></table></div>'

    # bar lists
    bl = ''
    for k, name in (('slv','SLV'),('gld','GLD'),('pslv','PSLV')):
        v = BX.get(k) or {}
        for b in v.get('bar_lists', []):
            if b.get('status') == 'ok':
                bl += f'<li><b>{name}</b>, {E(b["custodian"])}: {a(b["url"], "bar list (PDF)")}, {b["bars"]:,} bars, {b["fine_oz"]:,.3f} fine oz as of {D(b["as_of"])}.</li>'
            else:
                bl += f'<li><b>{name}</b>, {E(b["custodian"])}: {a(b["url"], "bar list (PDF)")}, unavailable when checked: {E(b.get("reason",""))}.</li>'
    gld = BX.get('gld') or {}; blsum = ''
    gb = [b for b in gld.get('bar_lists', []) if b.get('status') == 'ok']
    if gld.get('status') == 'ok' and len(gb) == 2:
        s = sum(b['fine_oz'] for b in gb)
        blsum = CB.html_line(f"GLD bar lists add up to {s:,.3f} oz = {gb[0]['fine_oz']:,.3f} ({gb[0]['custodian']}, {D(gb[0]['as_of'])}) + {gb[1]['fine_oz']:,.3f} ({gb[1]['custodian']}, {D(gb[1]['as_of'])}), vs {gld['oz']:,.2f} oz the trust reports for {D(gld['as_of'])}. GLD says bar lists are on a settlement-date basis and its website figure on a trade-date basis, so small gaps are expected.", 'Bar list check')
    slvv = BX.get('slv') or {}; sb = [b for b in slvv.get('bar_lists', []) if b.get('status') == 'ok']
    if slvv.get('status') == 'ok' and sb:
        blsum += CB.html_line(f"SLV bar list {sb[0]['fine_oz']:,.1f} oz ({D(sb[0]['as_of'])}, accounting basis) vs {slvv['oz']:,.1f} oz on the iShares page ({D(slvv['as_of'])}, trade-date basis): difference {sb[0]['fine_oz']-slvv['oz']:+,.1f} oz.", 'Bar list check')

    # premiums
    P = L['premiums']; sp = L['spot_last_known']; prow = ''
    for it in P['items']:
        for d in it.get('dealers', []):
            pr = d['price'] - it['spot']
            prow += (f'<tr><td data-l="Product">{E(it["product"])}</td><td data-l="Dealer">{E(d["dealer"])}</td><td data-l="Price">{CB.usd(d["price"])}</td>'
                     f'<td data-l="Spot ref.">{CB.usd(it["spot"])}</td><td data-l="Premium">+{CB.usd(pr)} ({100*pr/it["spot"]:.1f}%)</td></tr>')
    return f'''<section><p>Every COMEX number on VaultPulse starts with COMEX: the vaults report their own counts to CME, and CME publishes them. Cross-checking republished copies only shows the copies agree. This page adds holdings published by <strong>organisations COMEX doesn't control</strong>: the London Bullion Market Association, two Shanghai exchanges, and the largest silver and gold trusts, plus the retail premiums people actually pay. Each figure shows its own source, link and date, because they are published on different schedules.</p><p class="note">Data checked {CB.ts(BX.get("fetched_at"))}. Holdings are not added together: the same bar can appear in more than one row (for example, SLV's and GLD's London bars are also inside the LBMA London total).</p>{unav}</section>
<section id="bcx-silver"><h2>Silver: COMEX vs London vs Shanghai vs trusts</h2>{table('silver')}</section>
<section id="bcx-gold"><h2>Gold: COMEX vs London vs Shanghai vs GLD</h2>{table('gold')}</section>
<section id="bar-lists"><h2>ETF bar lists: the most granular public record</h2><p>The big trusts publish every bar they hold, with serial number, refiner, weight and fineness. Anyone can download them and check for duplicates or totals.</p><ul>{bl}</ul>{blsum}</section>
<section id="bcx-premiums"><h2>Physical premiums: real transaction prices</h2><p>Premiums are what dealers actually charge for coins over the spot price. They are prices people pay, not a vault's own count, which makes them the hardest of these numbers to dress up.</p><div style="overflow-x:auto"><table><thead><tr><th>Product</th><th>Dealer</th><th>Price</th><th>Spot ref.</th><th>Premium</th></tr></thead><tbody>{prow}</tbody></table></div>{CB.html_line("Premium = dealer price − the spot reference in the same row; % = that difference ÷ the spot reference. Prices and spot references from "+P["source"].split(" (")[0]+", checked "+D(P["checked_at"])+".")}<p class="note">Spot for comparison: silver {CB.usd(sp["silver_usd"])}, gold {CB.usd(sp["gold_usd"])} ({a(sp["source_url"], E(sp["source"]))}, {CB.ts(sp["as_of"])}). Full dealer table: <a href="/silver-premiums">premiums page</a>.</p></section>
<section id="bcx-limits" class="card"><h2>What each source can and can't prove</h2><ul>
<li><b>COMEX (CME):</b> daily and detailed by vault, but the depositories report their own counts, and it doesn't say who owns the metal or whether eligible metal is for sale.</li>
<li><b>LBMA London vaults:</b> covers every major London vault, including the Bank of England's gold. It is monthly, published about five business days after month end, and is an aggregate of what the vaults report. It includes metal already counted by London-vaulted ETFs.</li>
<li><b>Shanghai (SHFE, SGE):</b> independent of CME and frequent (SHFE daily, SGE weekly), but they are exchange-reported, and SHFE counts only warranted metal, so it is closer to COMEX registered than to COMEX total.</li>
<li><b>ETF bar lists (SLV, GLD, PSLV):</b> the most granular public record, bar by bar, with periodic counts by outside inspectors. They are still published by the trusts and their custodians, and they show only the trust's own metal.</li>
<li><b>Premiums:</b> real prices paid at dealers, so the hardest to fake, but they reflect retail coins and bars, not wholesale vaults.</li>
<li>None of these is an independent, bar-by-bar public audit of all the metal. Every source is self-reported to some degree.</li></ul>
<p class="note">Not financial advice. No predictions: these figures describe holdings on the dates shown.</p></section>'''
