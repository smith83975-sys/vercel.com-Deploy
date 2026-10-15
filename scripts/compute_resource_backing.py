#!/usr/bin/env python3
"""HYPOTHETICAL 'What backs a dollar?' figures for VaultPulse.

Reads curated, dated quantities from data/resources.json, money supply (M1/M2),
the US gold reserve, COMEX silver and stored spot from data/latest.json, and
fetches WTI, Henry Hub and copper prices from FRED (falls back to the last
stored price, with its own date, if FRED can't be reached). Writes one
`resource_backing` block into data/latest.json. resbacking.js and
scripts/build_seo_pages.py read ONLY that block, so no value or ratio is
hardcoded in HTML/JS.

Illustration only: resources in the ground are not liquid, many are privately
owned, and this is not a valuation or prediction. Not financial advice.

  python3 scripts/compute_resource_backing.py [--offline]
"""
import csv, io, json, os, subprocess, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LATEST = os.path.join(ROOT, 'data', 'latest.json')
RES = os.path.join(ROOT, 'data', 'resources.json')
QTY_MULT = {'barrels': 1, 'billion cubic feet': 1e6, 'million short tons': 1e6, 'thousand metric tons': 1e3,
            'metric tons': 1, 'troy oz': 1}  # -> base units: bbl, Mcf, short ton, metric ton, troy oz


def fred_latest(series):
    url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}'
    # plain curl: FRED's CDN stalls some custom urllib user agents
    txt = subprocess.run(['curl', '-sS', '--fail', '-m', '25', url], capture_output=True, text=True, check=True).stdout
    rows = list(csv.reader(io.StringIO(txt)))
    for d, v in reversed(rows[1:]):
        try:
            return float(v), d
        except ValueError:
            continue
    raise ValueError(f'{series}: no numeric value')


def dig(obj, path):
    for k in path.split('.'):
        obj = (obj or {}).get(k)
    return obj


def main():
    L = json.load(open(LATEST)); R = json.load(open(RES))
    old = (L.get('resource_backing') or {}).get('prices') or {}
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    sp = L.get('spot_last_known') or {}; lp = L.get('live_paper') or {}
    prices = {
        'spot_silver': {'label': 'Silver spot', 'unit': '$/troy oz', 'value': sp.get('silver_usd'), 'as_of': sp.get('as_of'),
                        'source_name': 'gold-api.com (stored; live in browser)', 'source_url': sp.get('source_url') or 'https://gold-api.com'},
        'spot_gold': {'label': 'Gold spot', 'unit': '$/troy oz', 'value': sp.get('gold_usd'), 'as_of': sp.get('as_of'),
                      'source_name': 'gold-api.com (stored; live in browser)', 'source_url': sp.get('source_url') or 'https://gold-api.com'},
    }
    for key, p in R['prices'].items():
        q = {k: p[k] for k in ('label', 'unit', 'source_name', 'source_url')}
        if p.get('fred_series'):
            q['series'] = p['fred_series']
            try:
                if '--offline' in sys.argv:
                    raise RuntimeError('offline')
                v, d = fred_latest(p['fred_series']); q.update(value=v, as_of=d, retrieved_at=now)
            except Exception as e:  # keep last known value with ITS date; never guess
                prev = old.get(key) or {}
                q.update(value=prev.get('value'), as_of=prev.get('as_of'), retrieved_at=prev.get('retrieved_at'),
                         stale_note=f'FRED fetch failed ({type(e).__name__}); showing last stored value')
        else:
            q.update(value=p.get('value'), as_of=p.get('as_of'))
        prices[key] = q

    ozt = R['troy_oz_per_metric_ton']; mcf = R['mmbtu_per_mcf']
    items = []
    for it in R['items']:
        o = {k: it.get(k) for k in ('id', 'group', 'name', 'ownership', 'quantity_unit', 'source_name', 'source_url', 'note')}
        o['default_on'] = it.get('default_on', True)
        if 'value_usd' in it:  # published valuation (land)
            o.update(quantity=None, quantity_label='published value estimate', price=None, price_key=None,
                     value_usd=it['value_usd'], as_of=it['as_of'], value_basis=f"published estimate in {it['value_year']} dollars (not updated)")
            items.append(o); continue
        if it.get('quantity_from'):
            qty = dig(L, it['quantity_from'])
            as_of = {'comex.silver.total_oz': (L.get('comex') or {}).get('report_date'),
                     'live_paper.gold_reserve.troy_oz': (lp.get('gold_reserve') or {}).get('as_of')}.get(it['quantity_from'])
        else:
            qty, as_of = it['quantity'], it['as_of']
        p = prices[it['price']]; pv = p.get('value')
        base = qty * QTY_MULT[it['quantity_unit']] if qty is not None else None
        if it.get('to_oz') and base is not None:
            base_units, base = 'troy oz', base * ozt
        else:
            base_units = {'barrels': 'barrels', 'billion cubic feet': 'Mcf', 'million short tons': 'short tons',
                          'thousand metric tons': 'metric tons', 'troy oz': 'troy oz', 'metric tons': 'metric tons'}[it['quantity_unit']]
        factor = mcf if it['price'] == 'henry_hub' else 1  # $/MMBtu x MMBtu per Mcf
        val = base * pv * factor if (base is not None and pv is not None) else None
        o.update(quantity=qty, as_of=as_of, base_quantity=base, base_unit=base_units, price_key=it['price'],
                 price=pv, price_unit=p['unit'], price_as_of=p.get('as_of'), conversion=(f'x {mcf} MMBtu per Mcf' if factor != 1 else None),
                 value_usd=round(val, 0) if val is not None else None, value_basis='quantity x price')
        items.append(o)

    m1 = (lp.get('m1') or {}); m2 = (lp.get('m2') or {})
    def totals(sel):
        t = sum(i['value_usd'] for i in items if sel(i) and i['value_usd'] is not None)
        return {'value_usd': round(t, 0),
                'per_m1_dollar': round(t / m1['value_usd'], 4) if m1.get('value_usd') else None,
                'per_m2_dollar': round(t / m2['value_usd'], 4) if m2.get('value_usd') else None,
                'pct_of_m1': round(100 * t / m1['value_usd'], 1) if m1.get('value_usd') else None,
                'pct_of_m2': round(100 * t / m2['value_usd'], 1) if m2.get('value_usd') else None}
    out = {
        'computed_at': now, 'computed_by': 'scripts/compute_resource_backing.py', 'inputs_file': 'data/resources.json',
        'hypothetical': True,
        'disclaimer': 'HYPOTHETICAL. Resources in the ground are not liquid, many are privately owned, and this is an illustration, not a valuation or prediction. Not financial advice.',
        'formula': {'value': 'quantity x current price (gas: dry Bcf x 1,000,000 Mcf x 1.036 MMBtu/Mcf x Henry Hub; metals: metric tons x 32,150.7 troy oz x spot)',
                    'land': 'published BEA working-paper estimate, 2009 dollars, not updated',
                    'coverage': 'selected resource value / money supply (M1 or M2) x 100; per dollar = selected value / money supply'},
        'money_supply': {'m1_usd': m1.get('value_usd'), 'm1_month': m1.get('month'), 'm1_source': m1.get('source'),
                         'm2_usd': m2.get('value_usd'), 'm2_month': m2.get('month'), 'm2_source': m2.get('source')},
        'prices': prices, 'items': items,
        'totals': {'default': totals(lambda i: i['default_on']), 'federal_only': totals(lambda i: i['ownership'] == 'federal'),
                   'silver_only': totals(lambda i: i['group'] == 'silver' and i['default_on'])},
        'context': R.get('context'), 'left_out': R.get('left_out'),
        'conversions': {'troy_oz_per_metric_ton': ozt, 'troy_oz_source': R['troy_oz_per_metric_ton_source'],
                        'mmbtu_per_mcf': mcf, 'mmbtu_source': R['mmbtu_per_mcf_source']},
    }
    L['resource_backing'] = out
    json.dump(L, open(LATEST, 'w'), indent=2, ensure_ascii=False); open(LATEST, 'a').write('\n')
    d = out['totals']['default']
    print(f"resource_backing: default set ${d['value_usd']/1e12:.2f}T = {d['pct_of_m2']}% of M2, {d['pct_of_m1']}% of M1; "
          f"federal only ${out['totals']['federal_only']['value_usd']/1e12:.2f}T")


if __name__ == '__main__':
    main()
