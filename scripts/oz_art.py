"""Original VaultPulse cartoon art for /wizard-of-oz-silver (drawn from scratch as SVG).
No film imagery: silver book-style shoes with cute faces, a yellow brick road, a little tornado, an 'Oz.' ounce coin."""
import math
DEFS='''<defs>
<linearGradient id="{p}ag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".45" stop-color="#d9dee6"/><stop offset="1" stop-color="#8f99a8"/></linearGradient>
<linearGradient id="{p}sole" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7d8696"/><stop offset="1" stop-color="#4f5664"/></linearGradient>
<linearGradient id="{p}road" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7d96b"/><stop offset="1" stop-color="#e8b923"/></linearGradient>
<linearGradient id="{p}tw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8b93a3"/><stop offset=".5" stop-color="#c9ced8"/><stop offset="1" stop-color="#7a8292"/></linearGradient>
<radialGradient id="{p}coin" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="#cfd5de"/><stop offset="1" stop-color="#8a94a3"/></radialGradient>
<radialGradient id="{p}glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffffff" stop-opacity=".55"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
</defs>'''
def spark(x,y,r,c='#fff',o=1):
    k=r*.28
    return f'<path d="M{x},{y-r} Q{x+k},{y-k} {x+r},{y} Q{x+k},{y+k} {x},{y+r} Q{x-k},{y+k} {x-r},{y} Q{x-k},{y-k} {x},{y-r}Z" fill="{c}" opacity="{o}"/>'
def road(p,w=800,h=500,top=250):
    """Yellow brick road in perspective, winding to a little green paper-money city."""
    s=f'<path d="M{w*.30},{h} C{w*.36},{h*.78} {w*.62},{h*.70} {w*.56},{top+30} C{w*.53},{top+10} {w*.57},{top} {w*.60},{top} L{w*.64},{top} C{w*.62},{top+12} {w*.62},{top+30} {w*.66},{top+50} C{w*.80},{h*.74} {w*.70},{h*.86} {w*.86},{h} Z" fill="url(#{p}road)" stroke="#c99a12" stroke-width="2"/>'
    rows=''
    for i in range(1,14):
        t=i/14; y=h-(h-top)*(1-(1-t)**1.6)
        rows+=f'<line x1="0" y1="{y:.1f}" x2="{w}" y2="{y:.1f}" stroke="#c99a12" stroke-width="{2.2*(1-t)+.6:.1f}"/>'
        n=int(3+t*6)
        for j in range(n+1): 
            x=j*w/n+((i%2)*w/(2*n)); rows+=f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y+ (h-top)*.06*(1-t)+3:.1f}" stroke="#c99a12" stroke-width="{2*(1-t)+.5:.1f}"/>'
    clip=f'<clipPath id="{p}rc">{s.replace("fill=","data-f=")}</clipPath>'
    return f'{clip}{s}<g clip-path="url(#{p}rc)">{rows}</g>'
def city(p,x,y,sc=1):
    b=''
    for i,(dx,hh,ww) in enumerate([(-34,40,16),(-18,62,18),(0,86,20),(20,58,18),(36,38,16)]):
        b+=f'<rect x="{dx-ww/2}" y="{-hh}" width="{ww}" height="{hh}" rx="3" fill="{"#2fae6a" if i%2 else "#38c97c"}" stroke="#1d7a47" stroke-width="1.5"/><path d="M{dx-ww/2},{-hh} L{dx},{-hh-12} L{dx+ww/2},{-hh}Z" fill="#2fae6a" stroke="#1d7a47" stroke-width="1.5"/>'
    b+='<text x="0" y="-26" text-anchor="middle" font-size="22" font-weight="900" fill="#e9fff1" font-family="DejaVu Sans,sans-serif">$</text>'
    return f'<g transform="translate({x},{y}) scale({sc})" opacity=".95">{b}</g>'
def shoe(p,x,y,sc=1,flip=False,wink=False):
    f=-1 if flip else 1
    face=(f'<path d="M66,30 q6,-5 12,0" stroke="#22262e" stroke-width="3.2" fill="none" stroke-linecap="round"/>' if wink else
          '<ellipse cx="72" cy="31" rx="5" ry="6.5" fill="#22262e"/><circle cx="74" cy="28.5" r="2" fill="#fff"/>')
    g=(f'<ellipse cx="78" cy="70" rx="72" ry="7" fill="#000" opacity=".18"/>'
       f'<path d="M12,60 L14,76 L34,76 L36,62Z" fill="url(#{p}sole)" stroke="#4f5664" stroke-width="2"/>'
       f'<path d="M6,48 C2,24 18,10 40,14 C52,16 60,20 76,20 C104,20 132,26 148,40 C158,49 156,62 140,64 L22,64 C12,64 8,58 6,48Z" fill="url(#{p}ag)" stroke="#6c7686" stroke-width="2.5"/>'
       f'<path d="M8,56 C10,62 14,66 24,66 L140,66 C152,66 158,60 156,54 C150,62 142,62 132,62 L24,62 C16,62 10,60 8,56Z" fill="url(#{p}sole)"/>'
       f'<path d="M14,40 C16,24 30,18 44,22 C54,26 50,36 40,40 C30,44 18,46 14,40Z" fill="#5a6372" opacity=".85"/>'
       f'<path d="M30,26 C40,22 48,26 46,32" stroke="#fff" stroke-width="3" fill="none" opacity=".7" stroke-linecap="round"/>'
       f'{face}<ellipse cx="96" cy="31" rx="5" ry="6.5" fill="#22262e"/><circle cx="98" cy="28.5" r="2" fill="#fff"/>'
       f'<path d="M78,42 q9,8 18,0" stroke="#22262e" stroke-width="3" fill="none" stroke-linecap="round"/>'
       f'<ellipse cx="64" cy="44" rx="7" ry="4" fill="#ff8fab" opacity=".6"/><ellipse cx="110" cy="44" rx="7" ry="4" fill="#ff8fab" opacity=".6"/>'
       f'<path d="M118,30 C130,30 140,36 146,44" stroke="#fff" stroke-width="2.5" fill="none" opacity=".75" stroke-linecap="round"/>'
       +spark(52,22,7,'#ffe27a',1)+spark(124,52,5,'#fff',.95)+spark(40,52,4,'#fff',.9))
    return f'<g transform="translate({x},{y}) scale({sc*f},{sc})">{g}</g>'
def tornado(p,x,y,sc=1):
    rings=''
    for i in range(9):
        w=88-i*9; yy=i*15; dx=math.sin(i*.8)*6
        rings+=f'<ellipse cx="{dx:.1f}" cy="{yy}" rx="{w}" ry="{10-i*.5:.1f}" fill="url(#{p}tw)" stroke="#6d7585" stroke-width="2"/>'
    face='<ellipse cx="-16" cy="30" rx="5" ry="6.5" fill="#22262e"/><circle cx="-14" cy="27.5" r="2" fill="#fff"/><ellipse cx="14" cy="30" rx="5" ry="6.5" fill="#22262e"/><circle cx="16" cy="27.5" r="2" fill="#fff"/><path d="M-9,44 q9,8 18,0" stroke="#22262e" stroke-width="3" fill="none" stroke-linecap="round"/><ellipse cx="-30" cy="42" rx="6" ry="3.5" fill="#ff8fab" opacity=".6"/><ellipse cx="30" cy="42" rx="6" ry="3.5" fill="#ff8fab" opacity=".6"/>'
    whoosh='<path d="M-110,10 q-20,30 0,60" stroke="#9aa3b5" stroke-width="3" fill="none" stroke-linecap="round" opacity=".7"/><path d="M110,-4 q22,30 4,64" stroke="#9aa3b5" stroke-width="3" fill="none" stroke-linecap="round" opacity=".7"/>'
    return f'<g transform="translate({x},{y}) scale({sc})">{whoosh}{rings}{face}</g>'
def coin(p,x,y,r=40,txt='1 Oz.'):
    return (f'<g transform="translate({x},{y})"><circle r="{r}" fill="url(#{p}coin)" stroke="#6c7686" stroke-width="3"/><circle r="{r*.8}" fill="none" stroke="#8a94a3" stroke-width="2" stroke-dasharray="3 4"/>'
            f'<text y="{r*.18}" text-anchor="middle" font-size="{r*.5:.0f}" font-weight="900" fill="#3d4450" font-family="DejaVu Sans,sans-serif">{txt}</text>'
            f'<text y="{r*.56}" text-anchor="middle" font-size="{r*.2:.0f}" font-weight="700" fill="#4f5664" font-family="DejaVu Sans,sans-serif">SILVER</text></g>')
def scene(p='h',vb='0 0 800 500',sky=True,ad=False):
    """Full scene: night-ish sky, road to a green paper city, tornado, coins, two silver shoes."""
    bg=(f'<rect width="800" height="500" fill="#141925"/><circle cx="560" cy="250" r="230" fill="url(#{p}glow)" opacity=".25"/>'
        +''.join(spark(x,y,r,'#fff',o) for x,y,r,o in [(80,60,6,.8),(200,120,4,.6),(330,40,5,.7),(720,70,6,.8),(650,160,3,.6),(470,90,4,.6),(40,200,3,.5),(760,220,4,.6)])) if sky else ''
    ground='<path d="M0,300 C200,270 600,270 800,300 L800,500 L0,500Z" fill="#1f3b2c"/><path d="M0,330 C250,300 550,305 800,335 L800,500 L0,500Z" fill="#244a35"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="Cartoon: two smiling silver shoes on a yellow brick road, a little tornado and a 1 Oz. silver coin">'
            +DEFS.format(p=p)+bg+ground+road(p,800,500,262)+city(p,494,262,.9)+(tornado(p,705,95,.7)+coin(p,330,120,40)+coin(p,560,60,22,'Oz.') if ad else tornado(p,150,110,.85)+coin(p,690,150,42)+coin(p,300,95,24,'Oz.'))
            +shoe(p,240,350,1.25)+shoe(p,600,372,1.25,True,True)
            +''.join(spark(x,y,r,'#fff',.95) for x,y,r in [(232,345,9),(455,338,7),(612,360,10),(395,420,6),(560,470,8),(420,470,5)])+'</svg>')
