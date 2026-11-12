#!/usr/bin/env python3
"""Fetch 'Beyond COMEX' holdings from sources COMEX does not control and write data/beyond_comex.json.

Separate from the weekday COMEX refresh on purpose: it never touches data/latest.json, and a
failure here can't break the daily ops run. Run it, then rebuild pages:
  python3 scripts/fetch_beyond_comex.py && python3 scripts/build_seo_pages.py

Rules: every figure is parsed from the source document itself (no estimates). If a source
can't be fetched or parsed, its entry gets status "unavailable" with the reason; any value
from an earlier successful run is kept under "last_verified" with its own as-of date.
Needs: curl, pdftotext/pdfinfo (poppler-utils), openpyxl.
"""
import json, os, re, subprocess, sys, html, datetime, tempfile, traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'beyond_comex.json')
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
OZ_PER_KG = 32.1507466     # troy oz per kilogram (1 g = 0.0321507466 troy oz, LBMA's factor)
OZ_PER_TONNE = 32150.7466
TMP = tempfile.mkdtemp(prefix='bcx_')
NOW = datetime.datetime.now(datetime.timezone.utc)
MON = {m: i for i, m in enumerate(['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'], 1)}

def get(url, name, timeout=60):
    p = os.path.join(TMP, name)
    r = subprocess.run(['curl', '-sL', '-A', UA, '--max-time', str(timeout), '-o', p, '-w', '%{http_code}', url],
                       capture_output=True, text=True)
    code = r.stdout.strip()
    if r.returncode != 0: raise RuntimeError(f'download failed or timed out (curl exit {r.returncode}) for {url}')
    if code != '200': raise RuntimeError(f'HTTP {code} from {url}')
    return p

def text_of(p):
    s = open(p, errors='ignore').read()
    s = re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S)
    t = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' | ', s)))
    return re.sub(r'(\|\s*)+', '| ', t)

def pdftext(p, first=None, last=None):
    a = ['pdftotext', '-layout']
    if first: a += ['-f', str(first)]
    if last: a += ['-l', str(last)]
    return subprocess.run(a + [p, '-'], capture_output=True, text=True, check=True).stdout

def pdfpages(p):
    o = subprocess.run(['pdfinfo', p], capture_output=True, text=True, check=True).stdout
    return int(re.search(r'Pages:\s+(\d+)', o).group(1))

def num(s): return float(s.replace(',', ''))

def dmy(s):  # '11-November-2026' / 'Nov 11, 2026' / 'November 11, 2026' / '12 November 2026' -> ISO
    s = s.strip()
    for f in ('%d-%B-%Y', '%b %d, %Y', '%B %d, %Y', '%d %B %Y', '%d-%b-%Y'):
        try: return datetime.datetime.strptime(s, f).date().isoformat()
        except ValueError: pass
    raise ValueError('unparsed date ' + s)

# ---------------------------------------------------------------- sources
def lbma():
    url = 'https://www.lbma.org.uk/prices-and-data/london-vault-data'
    t = text_of(get(url, 'lbma.html'))
    m = re.search(r'As at end (\w+) (\d{4}), the amount of gold held in London vaults was ([\d,.]+) tonnes \(a ([\d.]+)% (increase|decrease) on previous month\)', t)
    n = re.search(r'There were also ([\d,.]+) tonnes of silver \(a ([\d.]+)% (increase|decrease) on previous month\)', t)
    if not (m and n): raise RuntimeError('LBMA page layout changed: monthly summary sentence not found')
    month, year = m.group(1), int(m.group(2))
    mi = datetime.datetime.strptime(month[:3], '%b').month
    last = (datetime.date(year + (mi == 12), mi % 12 + 1, 1) - datetime.timedelta(days=1)).isoformat()
    sign = lambda w: 1 if w == 'increase' else -1
    gt, st = num(m.group(3)), num(n.group(1))
    base = dict(source='LBMA London Vault Data (monthly, one month in arrears; includes Bank of England gold)', source_url=url,
                as_of=last, as_of_label=f'end of {month} {year}', frequency='monthly',
                conversion=f'oz = tonnes × {OZ_PER_TONNE:,} (LBMA conversion factor 1 g = 0.0321507465 troy oz)')
    return {'gold': dict(base, tonnes=gt, oz=round(gt * OZ_PER_TONNE), mom_change_pct=sign(m.group(5)) * float(m.group(4)), status='ok'),
            'silver': dict(base, tonnes=st, oz=round(st * OZ_PER_TONNE), mom_change_pct=sign(n.group(3)) * float(n.group(2)), status='ok')}

def shfe():
    errs = []
    for back in range(0, 8):
        d = (NOW.astimezone(datetime.timezone(datetime.timedelta(hours=8))).date() - datetime.timedelta(days=back))
        if d.weekday() >= 5: continue
        ds = d.strftime('%Y%m%d')
        url = f'https://www.shfe.com.cn/data/tradedata/future/stockdata/dailystock_{ds}/ZH/all.html'
        try: t = text_of(get(url, f'shfe_{ds}.html', 40))
        except Exception as e: errs.append(str(e)); continue
        t = re.sub(r'(\|\s*)+', '| ', t)
        if d.isoformat() not in t: errs.append(f'{ds}: page date missing'); continue
        g = re.search(r'黄金 \| 单位：千克 \| 上期所指定交割金库 \| ([\d,]+) \| (-?[\d,]+)', t)
        s = re.search(r'白银 \| 单位：千克 \|.*?总计 \| ([\d,]+) \| (-?[\d,]+)', t)
        if not (g and s): errs.append(f'{ds}: gold/silver rows not found'); continue
        base = dict(source='Shanghai Futures Exchange daily warrant stock report (仓单日报), warranted metal in SHFE delivery warehouses',
                    source_url=url, as_of=d.isoformat(), frequency='daily (business days, Beijing time)',
                    scope='Warranted (deliverable) stock only, comparable to COMEX registered, not to COMEX total',
                    conversion=f'oz = kg × {OZ_PER_KG}')
        gk, sk = num(g.group(1)), num(s.group(1))
        return {'gold': dict(base, kg=gk, oz=round(gk * OZ_PER_KG), day_change_kg=num(g.group(2)), status='ok'),
                'silver': dict(base, kg=sk, oz=round(sk * OZ_PER_KG), day_change_kg=num(s.group(2)), status='ok')}
    raise RuntimeError('no SHFE daily report parsed in the last 8 days: ' + '; '.join(errs[-3:]))

def sge():
    lst = 'https://www.sge.com.cn/sjzx/hqzb'
    t = open(get(lst, 'sge_list.html', 90), errors='ignore').read()
    pdfs = re.findall(r'href="(https://www\.sge\.com\.cn/upload/file/(\d{6})/(\d{2})/[0-9a-f]+\.pdf)"', t)
    if not pdfs: raise RuntimeError('SGE weekly report list: no PDF links found')
    url, ym, dd = pdfs[0]
    p = get(url, 'sge_week.pdf', 120); x = pdftext(p)
    m = re.search(r'指定仓库库存周报.*?白银\s+([\d,.]+)\s+(-?[\d,.]+)\s+([\d,.]+)', x, re.S)
    w = re.search(r'(\d{1,2})月(\d{1,2})日\s*-\s*(\d{1,2})月(\d{1,2})日', x)
    if not m: raise RuntimeError('SGE weekly PDF: silver vault inventory row not found')
    pub = f'{ym[:4]}-{ym[4:]}-{dd}'
    end = datetime.date(int(ym[:4]) - (int(w.group(3)) > int(ym[4:])), int(w.group(3)), int(w.group(4))).isoformat() if w else None
    sk = num(m.group(3))
    return {'silver': dict(status='ok', kg=sk, oz=round(sk * OZ_PER_KG), week_change_kg=num(m.group(2)), prior_week_kg=num(m.group(1)),
                           as_of=end or pub, as_of_label=(f'week ending {end}' if end else f'published {pub}'), published=pub,
                           source='Shanghai Gold Exchange weekly market report (行情周报), designated-warehouse inventory table (指定仓库库存周报)',
                           source_url=url, list_url=lst, frequency='weekly (published Mondays)',
                           scope='Silver in SGE designated warehouses. SGE does not publish a gold vault total in this report.',
                           conversion=f'oz = kg × {OZ_PER_KG}')}

def gld():
    page = 'https://www.spdrgoldshares.com/usa/gld/'
    arch = 'https://api.spdrgoldshares.com/api/v1/historical-archive?product=gld&exchange=NYSE&lang=en'
    import openpyxl
    wb = openpyxl.load_workbook(get(arch, 'gld.xlsx', 90), read_only=True, data_only=True)
    ws = wb['US GLD Historical Archive']; rows = [r for r in ws.iter_rows(values_only=True) if r and r[0]]
    hdr = list(rows[0]); last = [r for r in rows[1:] if isinstance(r[hdr.index('Total Ounces of Gold in the Trust')], (int, float))][-1]
    out = dict(status='ok', oz=float(last[hdr.index('Total Ounces of Gold in the Trust')]), tonnes=float(last[hdr.index('Tonnes of Gold')]),
               as_of=dmy(str(last[0])), source='SPDR Gold Shares (GLD) historical archive, "Total Ounces of Gold in the Trust"',
               source_url=page, data_url=arch, frequency='daily', bar_lists=[])
    for name, url, fn in [('JPMorgan (London)', 'https://emea-markets.jpmorgan.com/metalicsWebAppJanus/publicUnauthenticated/SPDR_GOLD_TRUST_JPM_BARLIST.pdf', 'gld_jpm.pdf'),
                          ('HSBC', 'https://api.spdrgoldshares.com/api/v1/barlist?underlying=gld', 'gld_hsbc.pdf')]:
        try:
            x = pdftext(get(url, fn, 120), 1, 1)
            if 'As at:' in x:
                d = dmy(re.search(r'As at:\s*(\S+)', x).group(1)); m = re.search(r'Total :\s+(\d+)\s+([\d,.]+)\s+([\d,.]+)', x)
                bars, fine = int(m.group(1)), num(m.group(3))
            else:
                d = dmy(re.search(r'As Of C\.O\.B:\s+(\d{1,2} \w+ \d{4})', x).group(1))
                bars = int(re.search(r'Total Allocated Bar Count:\s+(\d+)', x).group(1)); fine = num(re.search(r'Total Allocated Fine Weight:\s+([\d,.]+)', x).group(1))
            out['bar_lists'].append(dict(custodian=name, url=url, as_of=d, bars=bars, fine_oz=fine, status='ok'))
        except Exception as e:
            out['bar_lists'].append(dict(custodian=name, url=url, status='unavailable', reason=str(e)[:200]))
    return out

def slv():
    page = 'https://www.ishares.com/us/products/239855/ishares-silver-trust-fund'
    t = text_of(get(page, 'slv.html', 60))
    m = re.search(r'Ounces in Trust \| ([\d,.]+) \| as of (?:\| )?(\w{3} \d{1,2}, \d{4})', t)
    n = re.search(r'Tonnes in Trust \| ([\d,.]+) \| as of (?:\| )?(\w{3} \d{1,2}, \d{4})', t)
    if not m: raise RuntimeError('iShares SLV page: "Ounces in Trust" not found')
    out = dict(status='ok', oz=num(m.group(1)), tonnes=num(n.group(1)) if n else None, as_of=dmy(m.group(2)),
               source='iShares Silver Trust (SLV) product page, "Ounces in Trust" (trade-date basis)', source_url=page, frequency='daily', bar_lists=[])
    bl = 'https://emea-markets.jpmorgan.com/metalicsWebAppJanus/publicUnauthenticated/BONY_SLV.pdf'
    try:
        x = pdftext(get(bl, 'slv_bar.pdf', 300), 1, 1)
        d = dmy(re.search(r'As at:\s*(\S+)', x).group(1)); mm = re.search(r'Total :\s+(\d+)\s+([\d,.]+)', x)
        out['bar_lists'].append(dict(custodian='JPMorgan (London)', url=bl, as_of=d, bars=int(mm.group(1)), fine_oz=num(mm.group(2)), status='ok'))
    except Exception as e:
        out['bar_lists'].append(dict(custodian='JPMorgan (London)', url=bl, status='unavailable', reason=str(e)[:200]))
    return out

def pslv():
    page = 'https://sprott.com/investment-strategies/physical-bullion-trusts/silver/'
    t = text_of(get(page, 'pslv.html', 60))
    m = re.search(r'As of (\w+ \d{1,2}, \d{4}).{0,600}?Total Oz\. of Silver \| ([\d,]+)', t)
    if not m: raise RuntimeError('Sprott PSLV page: "Total Oz. of Silver" not found')
    out = dict(status='ok', oz=num(m.group(2)), as_of=dmy(m.group(1)), source='Sprott Physical Silver Trust (PSLV) page, "Total Oz. of Silver"',
               source_url=page, frequency='daily', custodian='Royal Canadian Mint', bar_lists=[])
    bl = 'https://sprott.com/media/2doppccg/pslv-bar-list.pdf'
    try:
        p = get(bl, 'pslv_bar.pdf', 300); n = pdfpages(p); x = pdftext(p, max(1, n - 1), n)
        d = dmy(re.search(r'Silver Bar List\s+(\w+ \d{1,2}, \d{4})', x).group(1))
        out['bar_lists'].append(dict(custodian='Royal Canadian Mint', url=bl, as_of=d, bars=int(num(re.search(r'Total number of bars\s+([\d,]+)', x).group(1))),
                                     fine_oz=num(re.search(r'Total ounces available in the fund\s+([\d,.]+)', x).group(1)), status='ok'))
    except Exception as e:
        out['bar_lists'].append(dict(custodian='Royal Canadian Mint', url=bl, status='unavailable', reason=str(e)[:200]))
    return out

SOURCES = {'lbma': lbma, 'shfe': shfe, 'sge': sge, 'gld': gld, 'slv': slv, 'pslv': pslv}

def main(only=None):
    prev = json.load(open(OUT)) if os.path.exists(OUT) else {}
    res = dict(prev); res['fetched_at'] = NOW.strftime('%Y-%m-%dT%H:%M:%SZ'); res['fetched_by'] = 'scripts/fetch_beyond_comex.py'
    res['oz_per_kg'] = OZ_PER_KG; res['oz_per_tonne'] = OZ_PER_TONNE
    for k, fn in SOURCES.items():
        if only and k not in only: continue
        try:
            v = fn(); v['checked_at'] = res['fetched_at']; res[k] = v; print('ok', k)
        except Exception as e:
            old = prev.get(k) or {}
            keep = old.get('last_verified') if old.get('status') == 'unavailable' else (old if old else None)
            res[k] = dict(status='unavailable', reason=str(e)[:300], checked_at=res['fetched_at'], last_verified=keep)
            print('UNAVAILABLE', k, e, file=sys.stderr); traceback.print_exc(limit=1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(res, open(OUT, 'w'), indent=1, ensure_ascii=False); open(OUT, 'a').write('\n')
    print('wrote', OUT)

if __name__ == '__main__':
    main(set(sys.argv[1:]) or None)
