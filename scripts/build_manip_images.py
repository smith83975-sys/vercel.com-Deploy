#!/usr/bin/env python3
"""Renders silver-manipulation-card.png (1200x630 OG) and silver-manipulation-x.png (1600x900 X infographic) with headless Chrome."""
import sys,os,subprocess; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import manip_art
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS='*{box-sizing:border-box}body{margin:0;background:#0f1115;color:#e6e6e6;font-family:system-ui,"DejaVu Sans",sans-serif;overflow:hidden}'
card=f'''<html><head><style>{CSS}
.w{{width:1200px;height:630px;padding:34px 44px 0;background:linear-gradient(#0f1115,#141925)}}h1{{margin:0;color:#d4af37;font-size:58px;line-height:1.05}}
p{{margin:10px 0 0;font-size:27px;color:#ccc}}.art{{position:absolute;left:0;bottom:0;width:1200px}}.art svg{{display:block}}.u{{position:absolute;right:40px;top:40px;font-size:22px;color:#9aa3b5;font-weight:700}}</style></head>
<body><div class="w"><div class="u">vaultpulsehq.com</div><h1>Silver manipulation history</h1><p>Proven · Alleged · Dismissed: fines, convictions &amp; court records</p></div>
<div class="art">{manip_art.hero('k','0 70 800 230')}</div><div style="position:absolute;right:16px;bottom:8px;font-size:16px;color:#888;font-style:italic">Illustration: satire</div></body></html>'''
rows=[('2020','JPMorgan pays <b>$920.2M</b> (CFTC + DOJ) for spoofing metals &amp; Treasury futures, 2008–16'),
 ('2023','2 ex-JPMorgan metals traders sent to prison · convictions <b>upheld 2025</b>'),
 ('2020','Scotiabank: <b>$60.4M</b> for gold &amp; silver spoofing (2008–16)'),
 ('2018–19','Deutsche <b>$30M</b> · UBS <b>$15M</b> · HSBC <b>$1.6M</b> (2018) · Merrill <b>~$25M</b> (2019)'),
 ('2013','CFTC closes its 5-year silver probe: <b>no charges</b>')]
li=''.join(f'<li><span class="d">{d}</span><span>{t}</span></li>' for d,t in rows)
x=f'''<html><head><style>{CSS}
.w{{position:relative;width:1600px;height:900px;padding:44px 56px;background:linear-gradient(135deg,#0f1115,#151b28)}}
h1{{margin:0 0 22px;color:#d4af37;font-size:62px;line-height:1.05;width:1000px}}ul{{list-style:none;margin:0;padding:0;width:1010px}}
li{{display:flex;gap:22px;font-size:31px;line-height:1.25;padding:12px 0;border-bottom:1px solid #2a2f3a}}li b{{color:#fff}}
.d{{flex:0 0 140px;color:#c0c6cf;font-weight:800}}.bl{{margin-top:24px;width:1010px;font-size:36px;font-weight:800;line-height:1.25;background:#1a1d24;border-left:6px solid #d4af37;padding:14px 20px;border-radius:8px}}
.ok{{color:#ff8a80}}.no{{color:#9ecbff}}.art{{position:absolute;right:30px;top:40px;width:500px}}.art svg{{display:block}}
.f{{position:absolute;left:56px;bottom:26px;font-size:28px;color:#aaa}}.sat{{position:absolute;right:40px;top:520px;width:480px;text-align:center;font-size:28px;color:#888;font-style:italic}}</style></head>
<body><div class="w"><h1>Silver Manipulation: What's Actually Proven</h1><ul>{li}</ul>
<div class="bl">Short-term spoofing: <span class="ok">proven</span>. A decades-long price cap: <span class="no">not proven</span>.</div>
<div class="art">{manip_art.caught('x')}</div><div class="sat">Illustration: satire</div>
<div class="f">Sources: CFTC, DOJ, court records · <b style="color:#d4af37">vaultpulsehq.com/silver-manipulation-history</b></div></div></body></html>'''
for name,h,w,hh in [('silver-manipulation-card',card,1200,630),('silver-manipulation-x',x,1600,900)]:
    p=f'/tmp/{name}.html'; open(p,'w').write(h)
    subprocess.run(['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--hide-scrollbars',f'--window-size={w},{hh}',f'--screenshot={R}/{name}.png','file://'+p],check=True,capture_output=True)
    print(name)
