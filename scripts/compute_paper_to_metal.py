#!/usr/bin/env python3
"""Single source of truth for every paper-vs-metal figure on VaultPulse.

Reads the raw inputs already in data/latest.json (comex, open_interest,
live_paper, spot_last_known) and writes a derived `paper_to_metal` block back
into data/latest.json. Pages (app.js, livepaper.js, m1calc.js, papersources.js)
and scripts/build_seo_pages.py read ONLY this block for ratios, so nothing is
hardcoded in HTML/JS.

Rules baked in:
  * Silver (and gold) are measured against TOTAL COMEX vault metal
    (registered + eligible). Registered-only figures are kept as clearly
    labelled secondary values.
  * Every figure carries its as-of date and source. Missing inputs -> null,
    never a guess.

Run by the weekday refresh routine after it updates comex/open_interest, and
automatically at the start of scripts/build_seo_pages.py.
  python3 scripts/compute_paper_to_metal.py [--check]
"""
import json, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'data', 'latest.json')
OZ_PER_CONTRACT = {'silver': 5000, 'gold': 100}  # COMEX SI = 5,000 oz, GC = 100 oz
VAULT_SOURCES = [
    {'name': 'The Vault Report (republishes CME warehouse stocks)', 'url': 'https://thevaultreport.com/comex'},
    {'name': 'MetalCharts COMEX silver (cross-check)', 'url': 'https://metalcharts.org/comex/silver'},
    {'name': 'MetalCharts COMEX gold (cross-check)', 'url': 'https://metalcharts.org/comex/gold'},
    {'name': 'CME Group daily warehouse stock reports (original)', 'url': 'https://www.cmegroup.com/clearing/operations-and-deliveries/nymex-delivery-notices.html'},
]


def fmt_date(iso):
    if not iso:
        return None
    d = datetime.date.fromisoformat(iso[:10])
    return d.strftime('%b %-d, %Y')


def oi_as_of(oi):
    """Human label for the open-interest date. Prefer a parsed bulletin trade
    date; otherwise say plainly that only the fetch date is known."""
    td, fd = oi.get('trade_date'), oi.get('fetched_at')
    if td:
        return f"open interest as of CME bulletin trade date {fmt_date(td)}" + (f", fetched {fmt_date(fd)}" if fd else '')
    if fd:
        return f"open interest as of CME bulletin fetched {fmt_date(fd)}, trade date not shown in extract"
    return 'open interest date unknown'


def r(x, n):
    return None if x is None else round(x, n)


def compute(L):
    c, oi_all = L['comex'], L.get('open_interest') or {}
    lp, sp = L.get('live_paper') or {}, L.get('spot_last_known') or {}
    out = {
        'computed_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'computed_by': 'scripts/compute_paper_to_metal.py',
        'formula': {
            'paper_oz': 'open interest contracts x oz per contract (silver 5,000 oz; gold 100 oz)',
            'ratio_vs_total': 'paper oz / total COMEX vault oz (registered + eligible)  [headline]',
            'ratio_vs_registered': 'paper oz / registered oz  [secondary]',
            'coverage_total_pct': 'total vault oz / paper oz x 100',
            'implied_m2': 'M2 / metal oz (gold: US Treasury gold reserve; silver: total COMEX silver)',
            'm2_paper_ratio': 'implied price / spot (live in browser; stored value uses spot_last_known)',
        },
        'vault': {'report_date': c.get('report_date'), 'report_date_label': fmt_date(c.get('report_date')),
                  'source': c.get('source'), 'sources': VAULT_SOURCES},
        'open_interest': {k: oi_all.get(k) for k in ('trade_date', 'fetched_at', 'source', 'source_url')},
        'spot': {k: sp.get(k) for k in ('gold_usd', 'silver_usd', 'as_of', 'source', 'source_url')},
    }
    out['open_interest']['as_of_label'] = oi_as_of(oi_all)
    for m in ('silver', 'gold'):
        v, o = c.get(m) or {}, oi_all.get(m) or {}
        reg, eli, tot = v.get('registered_oz'), v.get('eligible_oz'), v.get('total_oz')
        if tot is None and reg is not None and eli is not None:
            tot = reg + eli
        n, opc = o.get('contracts'), o.get('oz_per_contract') or OZ_PER_CONTRACT[m]
        if o.get('oz_per_contract') and o['oz_per_contract'] != OZ_PER_CONTRACT[m]:
            raise SystemExit(f'{m}: oz_per_contract {o["oz_per_contract"]} != COMEX standard {OZ_PER_CONTRACT[m]}')
        paper = n * opc if n else None
        out[m] = {
            'oi_contracts': n, 'oz_per_contract': opc, 'paper_oz': paper,
            'registered_oz': reg, 'eligible_oz': eli, 'total_oz': tot,
            'ratio_vs_total': r(paper / tot, 4) if paper and tot else None,
            'ratio_vs_registered_secondary': r(paper / reg, 4) if paper and reg else None,
            'coverage_total_pct': r(100 * tot / paper, 2) if paper and tot else None,
            'coverage_registered_pct_secondary': r(100 * reg / paper, 2) if paper and reg else None,
            'vault_as_of': c.get('report_date'), 'oi_as_of_label': out['open_interest']['as_of_label'],
        }
    m2 = (lp.get('m2') or {}).get('value_usd'); m1 = (lp.get('m1') or {}).get('value_usd')
    goz = (lp.get('gold_reserve') or {}).get('troy_oz')
    s_tot, s_reg = out['silver']['total_oz'], out['silver']['registered_oz']
    ms = {
        'm2_usd': m2, 'm2_month': (lp.get('m2') or {}).get('month'), 'm2_source': (lp.get('m2') or {}).get('source'),
        'm1_usd': m1, 'm1_month': (lp.get('m1') or {}).get('month'), 'm1_source': (lp.get('m1') or {}).get('source'),
        'gold_reserve_oz': goz, 'gold_reserve_as_of': (lp.get('gold_reserve') or {}).get('as_of'),
        'gold_reserve_source': (lp.get('gold_reserve') or {}).get('source'),
        'silver_basis': 'total COMEX silver (registered + eligible)', 'silver_oz': s_tot, 'silver_as_of': c.get('report_date'),
        'implied_gold_m2_usd_per_oz': r(m2 / goz, 2) if m2 and goz else None,
        'implied_silver_m2_usd_per_oz': r(m2 / s_tot, 2) if m2 and s_tot else None,
        'implied_silver_m2_vs_registered_secondary': r(m2 / s_reg, 2) if m2 and s_reg else None,
    }
    g, s = sp.get('gold_usd'), sp.get('silver_usd')
    ms['m2_paper_ratio_gold_at_stored_spot'] = r(ms['implied_gold_m2_usd_per_oz'] / g, 2) if g and ms['implied_gold_m2_usd_per_oz'] else None
    ms['m2_paper_ratio_silver_at_stored_spot'] = r(ms['implied_silver_m2_usd_per_oz'] / s, 1) if s and ms['implied_silver_m2_usd_per_oz'] else None
    ms['stored_spot_as_of'] = sp.get('as_of')
    out['money_supply'] = ms
    return out


def main():
    L = json.load(open(PATH))
    # keep the label honest: silver basis is TOTAL COMEX silver
    lp = L.setdefault('live_paper', {})
    lp['silver_basis'] = {
        'source_file': 'data/latest.json (comex.silver.total_oz)',
        'definition': 'No official US silver reserve; implied silver = M2 / TOTAL COMEX silver oz (registered + eligible). '
                      'M2 / registered-only is shown only as a labelled secondary figure (paper_to_metal.money_supply).',
    }
    new = compute(L)
    if '--check' in sys.argv:
        old = L.get('paper_to_metal') or {}
        a = {k: v for k, v in old.items() if k != 'computed_at'}; b = {k: v for k, v in new.items() if k != 'computed_at'}
        sys.exit(0 if a == b else 1)
    L['paper_to_metal'] = new
    json.dump(L, open(PATH, 'w'), indent=2, ensure_ascii=False); open(PATH, 'a').write('\n')
    s = new['silver']
    print(f"paper_to_metal: silver {s['paper_oz']:,} paper oz / {s['total_oz']:,} total = {s['ratio_vs_total']} "
          f"(vs registered {s['ratio_vs_registered_secondary']}); {new['open_interest']['as_of_label']}; vaults {new['vault']['report_date']}")


if __name__ == '__main__':
    main()
