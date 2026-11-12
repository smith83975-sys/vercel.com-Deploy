#!/usr/bin/env python3
"""Chart for X: COMEX vs LBMA vs Shanghai vs ETF holdings, from data/beyond_comex.json + data/latest.json.
Usage: python3 scripts/beyond_comex_chart.py /workspace/beyond_comex_YYYYMMDD.png"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import beyond_comex_page as B, calc_basis as CB
L = json.load(open('data/latest.json')); BX = json.load(open('data/beyond_comex.json'))
R = [r for r in B.rows(L, BX) if r['status'] == 'ok']
SHORT = {'comex': 'COMEX vaults, total', 'lbma': 'London vaults (LBMA)', 'shfe': 'Shanghai SHFE, warranted', 'sge': 'Shanghai SGE vaults',
         'slv': 'SLV trust', 'pslv': 'PSLV trust', 'gld': 'GLD trust'}
SRC = {'comex': 'CME via The Vault Report', 'lbma': 'LBMA', 'shfe': 'SHFE', 'sge': 'SGE', 'slv': 'iShares', 'pslv': 'Sprott', 'gld': 'SPDR'}
BG, FG, GOLD, SIL, MUTED = '#0f1115', '#e8e8e8', '#d4af37', '#b8c4d0', '#8f97a3'
fig, axes = plt.subplots(2, 1, figsize=(12, 7.6), dpi=150, gridspec_kw={'height_ratios': [6, 4]}); fig.patch.set_facecolor(BG)
for ax, metal, col in ((axes[0], 'silver', SIL), (axes[1], 'gold', GOLD)):
    rs = sorted([r for r in R if r['metal'] == metal], key=lambda r: r['oz'])
    ys = range(len(rs)); vals = [r['oz'] / 1e6 for r in rs]; mx = max(vals)
    ax.barh(ys, vals, color=col, height=0.62)
    for y, r in zip(ys, rs):
        if r['key'] == 'comex':
            ax.barh(y, r['reg_oz'] / 1e6, color='#c0392b', height=0.62)
            if r['reg_oz'] / 1e6 > mx * 0.08: ax.text(r['reg_oz'] / 1e6 / 2, y, 'registered', color='white', va='center', ha='center', fontsize=7.5)
        asof = r.get('as_of_label') or CB.D(r['as_of'])
        asof = asof.replace('end of ', 'end ').replace('week ending ', 'wk to ')
        reg = f" ({r['reg_oz']/1e6:,.2f}M registered)" if r['key'] == 'comex' else ''
        ax.text(r['oz'] / 1e6 + mx * 0.01, y, f"{r['oz']/1e6:,.2f}M oz{reg}  ·  {SRC[r['key']]}, {asof}", va='center', color=FG, fontsize=8.5)
    ax.set_yticks(list(ys)); ax.set_yticklabels([SHORT[r['key']] for r in rs], color=FG, fontsize=9.5)
    ax.set_xlim(0, mx * 1.62); ax.set_facecolor(BG); ax.tick_params(colors=MUTED, labelsize=8)
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_xlabel('million troy oz', color=MUTED, fontsize=8)
    ax.set_title(metal.capitalize(), color=col, loc='left', fontsize=13, fontweight='bold')
fig.suptitle('Beyond COMEX: who else reports the metal', color=GOLD, fontsize=17, fontweight='bold', x=0.02, ha='left', y=0.985)
fig.text(0.02, 0.935, "Each source on its own date. Don't add rows: SLV/GLD London bars are inside the LBMA total. SHFE counts warranted metal only.",
         color=MUTED, fontsize=9, ha='left')
fig.text(0.02, 0.012, 'Red = COMEX registered [warranted, deliverable vs futures]. oz = tonnes × 32,150.7466 (LBMA); kg × 32.1507466 (SHFE, SGE).', color=MUTED, fontsize=8, ha='left')
fig.text(0.98, 0.012, '@VaultPulseHQ · vaultpulsehq.com/beyond-comex', color=GOLD, fontsize=9.5, ha='right', fontweight='bold')
fig.tight_layout(rect=(0, 0.035, 1, 0.925), h_pad=2.2)
out = sys.argv[1] if len(sys.argv) > 1 else 'beyond_comex.png'
fig.savefig(out, facecolor=BG); print('wrote', out)
