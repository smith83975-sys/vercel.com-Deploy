#!/usr/bin/env python3
"""'How this is calculated' lines for every derived VaultPulse figure.

Each function returns plain text: result = formula with every input value, its
source and its data date, all read from data/latest.json and data/tank.json.
No number is typed in here. Used by scripts/build_seo_pages.py (static pages)
and scripts/daily_brief*.py (newsletter). The browser scripts (app.js,
livepaper.js, papersources.js, m1calc.js, ratio.js, tanks.js, resbacking.js)
build the same lines from the same fields for their live values."""
import datetime, html

VAULT_SRC = 'CME Group warehouse report via The Vault Report'
OI_SRC = 'CME Daily Bulletin Sec. 02B'
FRED = {'m1': 'FRED M1SL', 'm2': 'FRED M2SL'}


def D(iso):
    """'2026-10-14' -> 'Oct 14, 2026'; non-ISO strings pass through."""
    if not iso:
        return 'date n/a'
    try:
        return datetime.date.fromisoformat(str(iso)[:10]).strftime('%b %-d, %Y')
    except ValueError:
        return str(iso)


def M(iso_month):
    try:
        return datetime.date.fromisoformat(iso_month + '-01').strftime('%b %Y')
    except Exception:
        return str(iso_month)


def ts(iso):
    return (iso or '').replace('T', ' ')[:16] + ' UTC' if iso else 'time n/a'


def oz(n):
    return f"{round(n):,} oz"


def moz(n, dp=2):
    return f"{n/1e6:,.{dp}f}M oz"


def usd(n, dp=2):
    return f"${n:,.{dp}f}"


def tr(n):
    return f"${n/1e12:,.2f}T"


def oi_date(L):
    oi = L['open_interest']
    if oi.get('trade_date'):
        return f"trade date {D(oi['trade_date'])}"
    return f"fetched {D(oi.get('fetched_at'))}, trade date not shown"


def vault(L):
    return f"{VAULT_SRC}, {D(L['comex']['report_date'])}"


def reg_share(L, m):
    s = L['comex'][m]
    return (f"{100*s['registered_oz']/s['total_oz']:.1f}% = {oz(s['registered_oz'])} registered ÷ "
            f"{oz(s['total_oz'])} total (registered + eligible) COMEX {m} ({vault(L)}).")


def total(L, m):
    s = L['comex'][m]
    return (f"Total {oz(s['total_oz'])} = {oz(s['registered_oz'])} registered + {oz(s['eligible_oz'])} eligible "
            f"({vault(L)}; eligible/total rounded to 0.01M oz by the source).")


def day_change(L, m):
    s = L['comex'][m]
    ch = s['registered_change_oz']
    prev = s['registered_oz'] - ch
    approx = ' Gold figures are rounded to 0.01M oz, so the change is approximate.' if m == 'gold' else ''
    return (f"{ch:+,} oz = {oz(s['registered_oz'])} registered on {D(L['comex']['report_date'])} − "
            f"{oz(prev)} on {D(s['change_vs'])} ({VAULT_SRC}).{approx}")


def hist_change(L, m='silver'):
    h = L['comex'][m].get('history_registered_moz')
    if not h:
        return None
    k = sorted(h)
    a, b = h[k[0]], h[k[-1]]
    return (f"{100*(b/a-1):+.1f}% = {b:.2f}M oz registered ({D(k[-1])}) ÷ {a:.2f}M oz ({D(k[0])}) − 1 "
            f"(daily registered history in latest.json, {VAULT_SRC}).")


def paper_oz(L, m):
    p = L['paper_to_metal'][m]
    return (f"{moz(p['paper_oz'],1)} = {p['oi_contracts']:,} open contracts × {p['oz_per_contract']:,} oz per contract "
            f"({OI_SRC}, {oi_date(L)}).")


def ratio_total(L, m):
    p = L['paper_to_metal'][m]
    return (f"{p['ratio_vs_total']:.2f} to 1 = {moz(p['paper_oz'],1)} COMEX {m} futures open interest "
            f"({p['oi_contracts']:,} contracts × {p['oz_per_contract']:,} oz; {OI_SRC}, {oi_date(L)}) ÷ "
            f"{moz(p['total_oz'],1)} total COMEX {m} stocks, registered + eligible ({vault(L)}).")


def ratio_reg(L, m):
    p = L['paper_to_metal'][m]
    return (f"{p['ratio_vs_registered_secondary']:.2f} to 1 = {moz(p['paper_oz'],1)} open interest (same as above) ÷ "
            f"{moz(p['registered_oz'],2)} registered COMEX {m} ({vault(L)}).")


def premium(L, item, dealer):
    pr = dealer['price'] - item['spot']
    return (f"+{usd(pr)} ({100*pr/item['spot']:.1f}%) = {usd(dealer['price'])} {dealer['dealer']} price − "
            f"{usd(item['spot'])} spot reference, ÷ {usd(item['spot'])} (both bullion-compare.com, checked "
            f"{D(L['premiums']['checked_at'])}).")


def gsr(gold, silver, when, src='gold-api.com'):
    return f"{gold/silver:.1f} = {usd(gold)} gold spot ÷ {usd(silver)} silver spot ({src}, {when})."


def gsr_stored(L):
    sp = L['spot_last_known']
    return gsr(sp['gold_usd'], sp['silver_usd'], 'stored ' + ts(sp['as_of']), sp.get('source', 'gold-api.com'))


def _reserve(L, m):
    ms = L['paper_to_metal']['money_supply']
    if m == 'gold':
        return f"{oz(ms['gold_reserve_oz'])} US gold reserve (US Treasury, as of {D(ms['gold_reserve_as_of'])})"
    return f"{oz(ms['silver_oz'])} total COMEX silver, registered + eligible ({vault(L)})"


def implied(L, m, money='m2', pct=100):
    ms = L['paper_to_metal']['money_supply']
    mv = ms[money + '_usd']
    o = ms['gold_reserve_oz'] if m == 'gold' else ms['silver_oz']
    pre = f"{pct}% × " if pct != 100 else ''
    return (f"{usd(pct/100*mv/o,0)}/oz = {pre}{tr(mv)} {money.upper()} ({M(ms[money+'_month'])}, {FRED[money]}) ÷ "
            f"{_reserve(L, m)}.")


def m2_ratio_stored(L, m):
    ms = L['paper_to_metal']['money_supply']
    sp = L['paper_to_metal']['spot']
    imp = ms['implied_gold_m2_usd_per_oz' if m == 'gold' else 'implied_silver_m2_usd_per_oz']
    s = sp['gold_usd' if m == 'gold' else 'silver_usd']
    return (f"{imp/s:,.{2 if imp/s<100 else 0}f} to 1 = {usd(imp,0)} implied price (above) ÷ {usd(s)} {m} spot "
            f"({sp['source']}, stored {ts(sp['as_of'])}; live spot replaces it in your browser).")


def mtd(t):
    return (f"≈{moz(t['mtd_contracts']*t['oz_per_contract'])} = {t['mtd_contracts']:,} contracts × "
            f"{t['oz_per_contract']:,} oz (CME Metals Issues and Stops MTD report, as of {D(t['mtd_date'])}).")


def mtd_pct(t):
    d = t['mtd_contracts'] * t['oz_per_contract']
    return (f"{100*d/t['registered_oz']:.1f}% = {moz(d)} delivered month-to-date ({D(t['mtd_date'])}) ÷ "
            f"{moz(t['registered_oz'])} registered ({D(t['registered_date'])}, {t['registered_source']}).")


def stock_value(L):
    g, s = L['comex']['gold'], L['comex']['silver']
    sp = L['spot_last_known']
    gv, sv = g['total_oz'] * sp['gold_usd'], s['total_oz'] * sp['silver_usd']
    return (f"{gv/sv:.1f}x = ({moz(g['total_oz'])} gold × {usd(sp['gold_usd'])}) ÷ ({moz(s['total_oz'])} silver × "
            f"{usd(sp['silver_usd'])}) = ${gv/1e9:,.1f}B ÷ ${sv/1e9:,.1f}B (vaults: {vault(L)}; spot: "
            f"{sp['source']}, stored {ts(sp['as_of'])}).")


def rb_total(L, which='default', vs='m2'):
    rb = L['resource_backing']
    t = rb['totals'][which]
    ms = rb['money_supply']
    n = sum(1 for i in rb['items'] if (i['default_on'] if which == 'default' else i['ownership'] == 'federal'))
    label = 'every resource ticked by default' if which == 'default' else 'federally owned rows only'
    if vs == 'debt':
        den = f"{tr(ms['debt_usd'])} total public debt (US Treasury Debt to the Penny, {D(ms['debt_date'])})"
        pct = t['pct_of_debt']
    else:
        den = f"{tr(ms[vs+'_usd'])} {vs.upper()} ({M(ms[vs+'_month'])}, {FRED[vs]})"
        pct = t['pct_of_' + vs]
    return (f"{pct}% = {tr(t['value_usd'])} ({label}: {n} rows, each quantity × dated price, listed in the "
            f"calculator table) ÷ {den}.")


def rb_row(i):
    if i.get('quantity') is None or i.get('price') is None:
        return f"{i['value_basis']} ({i['source_name']})"
    conv = f" {i['conversion']}" if i.get('conversion') else ''
    return (f"{i['base_quantity']:,.0f} {i['base_unit']} × {usd(i['price'])} {i['price_unit'].replace('$','')}{conv} "
            f"(price as of {D(i['price_as_of']) if str(i.get('price_as_of','')).startswith('20') and len(str(i['price_as_of']))>=10 else i.get('price_as_of')})")


def html_line(text, label='How this is calculated'):
    return f'<p class="calc-basis"><b>{label}:</b> {html.escape(text)}</p>'


def html_list(items, summary='How these figures are calculated', open_=False):
    lis = ''.join(f'<li>{html.escape(t)}</li>' for t in items if t)
    return f'<details class="calc-basis"{" open" if open_ else ""}><summary>{summary}</summary><ul>{lis}</ul></details>'
