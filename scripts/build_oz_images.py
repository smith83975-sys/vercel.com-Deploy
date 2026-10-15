#!/usr/bin/env python3
"""Renders oz-silver-card.png (1200x630 OG) and oz-silver-x.png (1600x900 X ad) with headless Chrome. Original art only (scripts/oz_art.py)."""
import sys,os,subprocess; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import oz_art
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS='*{box-sizing:border-box}body{margin:0;background:#0f1115;color:#e6e6e6;font-family:system-ui,"DejaVu Sans",sans-serif;overflow:hidden}.art svg{display:block;width:100%;height:auto}.logo{display:flex;align-items:center;gap:10px;font-weight:800;color:#fff}.logo img{border-radius:6px}.logo b{color:#d4af37}'
LOGO=lambda s: f'<div class="logo" style="font-size:{s}px"><img src="file://{R}/apple-touch-icon.png" width="{int(s*1.4)}" height="{int(s*1.4)}"><span>Vault<b>Pulse</b></span></div>'
card=f'''<html><head><style>{CSS}
.w{{position:relative;width:1200px;height:630px;background:linear-gradient(135deg,#0f1115,#151b28)}}.t{{position:absolute;left:44px;top:36px;width:540px}}
h1{{margin:22px 0 0;font-size:56px;line-height:1.06;color:#fff}}h1 .s{{color:#dfe4ec;text-shadow:0 0 18px rgba(255,255,255,.35)}}h1 .g{{color:#f2c94c}}
p{{margin:16px 0 0;font-size:26px;color:#c8ccd4;line-height:1.3}}.art{{position:absolute;right:0;bottom:0;width:640px;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 50px),linear-gradient(transparent 0,#000 60px);-webkit-mask-composite:source-in}}
.u{{position:absolute;left:44px;bottom:30px;font-size:22px;color:#9aa3b5;font-weight:700}}</style></head>
<body><div class="w"><div class="art">{oz_art.scene('c','200 0 600 500',ad=True)}</div><div class="t">{LOGO(26)}<h1>The Wizard of Oz and <span class="s">silver</span></h1><p>Silver shoes, a <span style="color:#f2c94c">gold</span> road, and Oz = ounce. The 1890s money allegory explained.</p></div><div class="u">vaultpulsehq.com/wizard-of-oz-silver</div></div></body></html>'''
x=f'''<html><head><style>{CSS}
.w{{position:relative;width:1600px;height:900px;background:linear-gradient(135deg,#0f1115,#151b28)}}
.art{{position:absolute;right:0;bottom:0;width:880px;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 60px),linear-gradient(transparent 0,#000 80px);-webkit-mask-composite:source-in}}
.t{{position:absolute;left:60px;top:54px;width:700px}}
h1{{margin:40px 0 0;font-size:84px;line-height:1.02;color:#fff;letter-spacing:-1px}}h1 .s{{display:block;color:#eef1f6;font-size:118px;text-shadow:0 0 26px rgba(255,255,255,.45)}}
.q{{margin:28px 0 0;font-size:36px;line-height:1.25;color:#e6e6e6;font-weight:700}}.q b{{color:#f2c94c}}.q i{{color:#eef1f6;font-style:normal;font-weight:900}}
.k{{margin-top:30px;font-size:34px;color:#d4af37;font-weight:800;border-left:6px solid #d4af37;padding:10px 18px;background:#1a1d24;border-radius:8px}}
.n{{margin-top:16px;font-size:24px;color:#9aa3b5}}.f{{position:absolute;left:60px;bottom:40px;font-size:32px;font-weight:800;color:#fff;background:#d4af37;color:#141925;padding:12px 22px;border-radius:40px}}
.sp{{position:absolute;color:#fff;font-size:40px}}</style></head>
<body><div class="w"><div class="art">{oz_art.scene('x','200 0 600 500',ad=True)}</div><div class="t">{LOGO(34)}
<h1>There's no place like&hellip;<span class="s">silver</span></h1>
<div class="q">Follow the <b>yellow brick road</b>? In the 1900 book, Dorothy's shoes were <i>SILVER</i>.</div>
<div class="k">The money story hidden in the Wizard of Oz</div><div class="n">A popular theory about the 1896 gold vs silver fight. Sourced.</div></div>
<div class="f">vaultpulsehq.com/wizard-of-oz-silver</div></div></body></html>'''
for name,h,w,hh in [('oz-silver-card',card,1200,630),('oz-silver-x',x,1600,900)]:
    p=f'/tmp/{name}.html'; open(p,'w').write(h)
    subprocess.run(['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--hide-scrollbars','--allow-file-access-from-files',f'--window-size={w},{hh}',f'--screenshot={R}/{name}.png','file://'+p],check=True,capture_output=True)
    print(name)
