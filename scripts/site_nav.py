"""Single source of truth for VaultPulse site navigation.
Used by build_seo_pages.py for generated pages AND to inject the same nav into
hand-written pages (index, flow, sponsor) and to generate 404.html.
Edit PAGES / RELATED here, then run: python3 scripts/build_seo_pages.py"""
import re
CSSV='20261015nav'
# key, url, pill label (short), footer/card label (long), icon, one-line description
PAGES=[
 ('silver-squeeze-tracker','/silver-squeeze-tracker','Silver Tracker','Silver squeeze tracker','📊','Registered silver, deliveries, paper ratio and premiums in one view'),
 ('comex-silver-inventory','/comex-silver-inventory','Silver Inventory','COMEX silver inventory','🥈','Registered vs eligible silver in COMEX vaults, dated'),
 ('silver-premiums','/silver-premiums','Premiums','Silver &amp; gold premiums','🏷️','What coins and bars cost over spot, by dealer'),
 ('paper-to-metal','/paper-to-metal','Paper vs Metal','Paper to metal (M1/M2)','📜','US money supply vs gold and silver ounces'),
 ('silver-manipulation-history','/silver-manipulation-history','Manipulation','Silver manipulation history','🕵️','Bank fines, convictions and dismissed claims, sourced'),
 ('gold-silver-ratio','/gold-silver-ratio','Gold/Silver Ratio','Gold/silver ratio','⚖️','Live ratio plus its history from AD 1 to today'),
 ('comex-gold-inventory','/comex-gold-inventory','Gold Inventory','COMEX gold inventory','🥇','Registered and eligible gold in COMEX vaults'),
 ('comex-force-majeure','/comex-force-majeure','Force Majeure','COMEX force majeure','⚠️','What force majeure would mean for COMEX delivery'),
 ('gold-silver-news','/gold-silver-news','News','Gold &amp; silver news','📰','Live gold and silver headline stream with alerts'),
 ('flow','/flow','Deliveries','Deliveries tracker','🚚','Issues, stops and big COMEX stock moves, daily'),
 ('m1-calc','/#m1-calc','M1 Calculator','Spot vs M1 calculator','🧮','What spot would be at any % M1 money backing'),
 ('what-is-money','/what-is-money','What is Money','What is money?','💵','Plain-English guide: barter to gold, silver and fiat'),
 ('wizard-of-oz-silver','/wizard-of-oz-silver','Wizard of Oz','The Wizard of Oz and silver','🌪️','The 1890s gold vs silver fight hidden in a fairy tale'),
 ('sponsor','/sponsor','Sponsor','Sponsor VaultPulse','🤝','Reach silver and gold stackers from $400/month'),
]
EXTRA={'home':('/','Home','Home','🏠','The full VaultPulse dashboard'),
       'watch':('/#watch','Video','Watch: What is VaultPulse?','▶️','A 74-second funny, sourced explainer'),
       'newsletter':('/#newsletter','Daily Brief','Free daily brief','✉️','Gold and silver news in your inbox, free')}
BY={k:(u,s,l,i,d) for k,u,s,l,i,d in PAGES}; BY.update(EXTRA)
FOOT=['home','watch']+[p[0] for p in PAGES[:-1]]+['newsletter','sponsor']
RELATED={
 'home':['silver-squeeze-tracker','comex-silver-inventory','silver-manipulation-history','silver-premiums'],
 'silver-squeeze-tracker':['comex-silver-inventory','silver-premiums','paper-to-metal','silver-manipulation-history'],
 'comex-silver-inventory':['silver-squeeze-tracker','flow','silver-premiums','paper-to-metal'],
 'silver-premiums':['silver-squeeze-tracker','comex-silver-inventory','gold-silver-ratio','gold-silver-news'],
 'paper-to-metal':['m1-calc','gold-silver-ratio','comex-silver-inventory','comex-gold-inventory'],
 'silver-manipulation-history':['silver-squeeze-tracker','comex-silver-inventory','paper-to-metal','gold-silver-news'],
 'gold-silver-ratio':['paper-to-metal','comex-silver-inventory','comex-gold-inventory','gold-silver-news'],
 'comex-gold-inventory':['comex-silver-inventory','flow','gold-silver-ratio','comex-force-majeure'],
 'comex-force-majeure':['comex-silver-inventory','comex-gold-inventory','flow','gold-silver-news'],
 'gold-silver-news':['silver-squeeze-tracker','comex-force-majeure','gold-silver-ratio','newsletter'],
 'flow':['silver-squeeze-tracker','comex-silver-inventory','comex-gold-inventory','comex-force-majeure'],
 'sponsor':['silver-squeeze-tracker','gold-silver-news','silver-manipulation-history','newsletter'],
 'what-is-money':['m1-calc','paper-to-metal','silver-squeeze-tracker','comex-silver-inventory'],
 'wizard-of-oz-silver':['what-is-money','gold-silver-ratio','silver-squeeze-tracker','comex-silver-inventory'],
 '404':['home','silver-squeeze-tracker','comex-silver-inventory','gold-silver-news'],
}
NAVJS='<script>(function(){var u=document.querySelector(".vp-pills");if(!u)return;var w=u.parentNode,a=u.querySelector("[aria-current]");if(a&&u.scrollWidth>u.clientWidth&&a.offsetLeft+a.offsetWidth>u.clientWidth-40)u.scrollLeft=a.offsetLeft-16;function f(){w.classList.toggle("at-end",u.scrollLeft+u.clientWidth>=u.scrollWidth-4)}u.addEventListener("scroll",f,{passive:true});addEventListener("resize",f);f()})()</script>'
def nav(active):
    cur=lambda k:' aria-current="page"' if k==active else ''
    pills=''.join(f'<li><a class="vp-pill{" silver" if i<5 else ""}" href="{u}"{cur(k)}>{s}</a></li>' for i,(k,u,s,l,ic,d) in enumerate(PAGES))
    return (f'<div class="vp-nav" id="top-nav"><div class="vp-bar"><a class="vp-logo" href="/"{cur("home")} aria-label="VaultPulse home">'
            f'<img src="/favicon-32.png" width="28" height="28" alt=""><span>Vault<b>Pulse</b></span></a>'
            f'<a class="vp-cta" href="/#newsletter">✉️ Free Daily Brief</a></div>'
            f'<nav class="vp-pills-wrap" aria-label="VaultPulse pages"><ul class="vp-pills">{pills}</ul></nav></div>{NAVJS}')
def keep(key,title='Keep exploring'):
    cards=''.join(f'<a class="vp-card" href="{BY[k][0]}"><span class="vp-ic" aria-hidden="true">{BY[k][3]}</span><span class="vp-ct"><b>{BY[k][2]}</b><small>{BY[k][4]}</small></span><span class="vp-go" aria-hidden="true">→</span></a>' for k in RELATED[key])
    return f'<section class="vp-keep" aria-label="{title}"><h2>{title}</h2><div class="vp-cards">{cards}</div></section>'
CUR=' aria-current="page"'
def foot(active=None):
    btn=''.join(f'<a href="{BY[k][0]}"{CUR if k==active else ""}><span aria-hidden="true">{BY[k][3]}</span> {BY[k][2]}</a>' for k in FOOT)
    return f'<nav class="vp-foot" aria-label="All VaultPulse pages"><h2>All VaultPulse pages</h2><div class="vp-foot-grid">{btn}</div></nav>'
def css_link(t): return re.sub(r'<link rel="stylesheet" href="/?style\.css(\?v=[^"]*)?">',f'<link rel="stylesheet" href="/style.css?v={CSSV}">',t)
def _put(t,tag,block,insert):
    b=f'<!--vp:{tag}-->{block}<!--/vp:{tag}-->'; pat=re.compile(rf'<!--vp:{tag}-->.*?<!--/vp:{tag}-->',re.S)
    return pat.sub(lambda m:b,t,count=1) if pat.search(t) else insert(t,b)
def apply_hand(t,key):
    """Inject shared nav/keep/foot into a hand-written page; idempotent; strips legacy navs."""
    t=re.sub(r'<nav class="site-nav">.*?</nav>\s*','',t,flags=re.S)
    t=re.sub(r'<aside class="card silver-strip">.*?</aside>\s*','',t,flags=re.S)
    t=re.sub(r'<nav class="foot-nav"[^>]*>.*?</nav>','',t,flags=re.S)
    def ins_nav(t,b):
        m=re.search(r'<div class="sponsor">.*?</div>\n?',t,re.S)
        if m: return t[:m.end()]+b+'\n'+t[m.end():]
        return t.replace('<body>','<body>\n'+b,1)
    t=_put(t,'nav',nav(key),ins_nav)
    t=_put(t,'keep',keep(key),lambda t,b:t.replace('</main>',b+'\n</main>',1))
    t=_put(t,'foot',foot(key),lambda t,b:t.replace('<footer>','<footer>'+b,1))
    return css_link(t)
def page404():
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | VaultPulse</title><meta name="robots" content="noindex"><link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" href="/favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="stylesheet" href="/style.css?v={CSSV}"></head>
<body>
{nav(None)}
<header><h1>Page not found</h1><p>That page doesn't exist. Try one of these:</p></header>
<main>{keep('404','Popular pages')}</main>
<footer>{foot()}<p><b>Not financial advice.</b></p></footer>
</body></html>
'''
