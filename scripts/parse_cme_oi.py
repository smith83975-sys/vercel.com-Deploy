#!/usr/bin/env python3
"""Update data/latest.json open_interest from a CME Daily Bulletin Section 02B
(Exchange Summary Volume & Open Interest, Metals) PDF or its pdftotext output.

  python3 scripts/parse_cme_oi.py Section02B.pdf      # or .txt
  python3 scripts/parse_cme_oi.py --fetch             # try CME directly (often HTTP 403)

Records: silver (SI) and gold (GC) futures open interest, fetched_at (today,
UTC) and trade_date when the bulletin header shows one (e.g. "Tue, Oct 13, 2026"
or "10/13/2026"). If a value can't be parsed, the existing value is KEPT and the
script says so; it never invents numbers. Afterwards run
scripts/compute_paper_to_metal.py (build_seo_pages.py does this automatically).
"""
import json, os, re, subprocess, sys, datetime, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'data', 'latest.json')
URL = 'https://www.cmegroup.com/daily_bulletin/current/Section02B_Summary_Volume_And_Open_Interest_Metals_Futures_And_Options.pdf'


def text_of(path):
    if path.lower().endswith('.pdf'):
        return subprocess.run(['pdftotext', '-layout', path, '-'], capture_output=True, text=True, check=True).stdout
    return open(path, encoding='utf-8', errors='replace').read()


def parse_trade_date(t):
    head = t[:3000]
    m = re.search(r'(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*,?\s+([A-Z][a-z]{2})[a-z]*\.?\s+(\d{1,2}),?\s+(\d{4})', head)
    if m:
        return datetime.datetime.strptime(f'{m[1]} {m[2]} {m[3]}', '%b %d %Y').date().isoformat()
    m = re.search(r'TRADE DATE[:\s]+(\d{1,2})/(\d{1,2})/(\d{2,4})', head, re.I) or re.search(r'\b(\d{1,2})/(\d{1,2})/(20\d{2})\b', head)
    if m:
        y = int(m[3]); y = y + 2000 if y < 100 else y
        return datetime.date(y, int(m[1]), int(m[2])).isoformat()
    return None


def parse_oi(t, code, names):
    """Find the futures summary row for a product and return its open interest
    (taken as the last integer on the row, which is the OI column in 02B)."""
    for line in t.splitlines():
        u = line.upper()
        if re.search(rf'\b{code}\b', u) and any(n in u for n in names) and 'OPT' not in u:
            nums = [int(x.replace(',', '')) for x in re.findall(r'\d[\d,]{2,}', line)]
            if nums:
                return nums[-1]
    return None


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == '--fetch':
        src = '/tmp/cme_02b.pdf'
        req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            open(src, 'wb').write(urllib.request.urlopen(req, timeout=30).read())
        except Exception as e:
            sys.exit(f'CME fetch failed ({e}); open_interest left unchanged.')
    else:
        src = a[0]
    t = text_of(src)
    L = json.load(open(PATH)); o = L['open_interest']
    td = parse_trade_date(t)
    got = {'silver': parse_oi(t, 'SI', ['SILVER']), 'gold': parse_oi(t, 'GC', ['GOLD'])}
    for m, v in got.items():
        if v:
            o[m]['contracts'] = v
        else:
            print(f'WARNING: {m} open interest not parsed; kept {o[m]["contracts"]}')
    if any(got.values()):
        o['fetched_at'] = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
        o['trade_date'] = td
        o['trade_date_note'] = 'Parsed from bulletin header.' if td else 'Trade date not found in bulletin header.'
    json.dump(L, open(PATH, 'w'), indent=2, ensure_ascii=False); open(PATH, 'a').write('\n')
    print(f'open_interest: silver {o["silver"]["contracts"]}, gold {o["gold"]["contracts"]}, trade_date {o.get("trade_date")}, fetched {o.get("fetched_at")}')


if __name__ == '__main__':
    main()
