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
def dorothy(p,x,y,sc=1):
    """ORIGINAL cartoon Dorothy based on the public-domain 1900 book (blue-and-white checked gingham,
    pigtails, little basket, SILVER shoes). Not the 1939 film design: golden pigtails with pink ribbons,
    plain checked dress with a white collar, silver (not ruby) slippers. Feet at (0,0), ~300 units tall."""
    skin='#f7d3b8'; skin_s='#e9b996'; hair='#e2a94a'; hair_s='#c98a2c'; ink='#22262e'
    d=(f'<defs><pattern id="{p}ging" width="14" height="14" patternUnits="userSpaceOnUse">'
       f'<rect width="14" height="14" fill="#ffffff"/><rect width="7" height="14" fill="#5b8fe0" opacity=".55"/>'
       f'<rect width="14" height="7" fill="#5b8fe0" opacity=".55"/><rect width="7" height="7" fill="#2f63c4"/></pattern>'
       f'<linearGradient id="{p}slip" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="#d3d9e3"/><stop offset="1" stop-color="#8a94a5"/></linearGradient></defs>')
    g=d+'<ellipse cx="0" cy="2" rx="78" ry="10" fill="#000" opacity=".22"/>'
    # legs + socks
    g+=f'<rect x="-22" y="-84" width="13" height="74" rx="6" fill="{skin}"/><rect x="9" y="-84" width="13" height="74" rx="6" fill="{skin}"/>'
    g+='<rect x="-23" y="-34" width="15" height="24" rx="5" fill="#ffffff"/><rect x="8" y="-34" width="15" height="24" rx="5" fill="#ffffff"/>'
    # SILVER slippers (big, sparkly)
    for sx,fl in [(-17,-1),(17,1)]:
        g+=(f'<g transform="translate({sx},0) scale({fl*1.3},1.3)">'
            f'<path d="M-12,-16 C-12,-24 4,-24 10,-20 C20,-16 32,-14 34,-6 C36,2 26,3 14,3 L-6,3 C-14,3 -14,-6 -12,-16Z" fill="url(#{p}slip)" stroke="#5e6878" stroke-width="2.4"/>'
            f'<path d="M-4,-17 C2,-20 10,-18 14,-14" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round" opacity=".9"/>'
            f'<circle cx="22" cy="-10" r="3.2" fill="#eef1f6" stroke="#5e6878" stroke-width="1.2"/></g>')
    g+=spark(-36,-22,9,'#ffffff',1)+spark(44,-26,8,'#ffffff',1)+spark(4,-38,6,'#ffe9a8',1)+spark(-52,0,5,'#fff',.9)+spark(56,-2,6,'#fff',.95)
    # arms (behind dress edges)
    g+=f'<path d="M-30,-190 C-58,-196 -78,-222 -84,-252" stroke="{skin}" stroke-width="13" fill="none" stroke-linecap="round"/>'
    g+=f'<circle cx="-86" cy="-258" r="11" fill="{skin}"/>'  # waving hand
    g+=f'<path d="M30,-190 C46,-170 52,-150 56,-128" stroke="{skin}" stroke-width="13" fill="none" stroke-linecap="round"/>'
    # dress
    g+=(f'<path d="M-30,-200 C-36,-160 -58,-112 -66,-82 C-30,-72 30,-72 66,-82 C58,-112 36,-160 30,-200 C12,-208 -12,-208 -30,-200Z" fill="url(#{p}ging)" stroke="#1f4a99" stroke-width="2.6"/>'
        f'<path d="M-66,-82 C-30,-72 30,-72 66,-82 L64,-88 C30,-79 -30,-79 -64,-88Z" fill="#ffffff" opacity=".9"/>')
    # puff sleeves
    g+=f'<ellipse cx="-33" cy="-194" rx="15" ry="12" fill="url(#{p}ging)" stroke="#1f4a99" stroke-width="2.4"/><ellipse cx="33" cy="-194" rx="15" ry="12" fill="url(#{p}ging)" stroke="#1f4a99" stroke-width="2.4"/>'
    # white collar
    g+='<path d="M-24,-206 C-18,-190 -4,-190 0,-200 C4,-190 18,-190 24,-206 C10,-212 -10,-212 -24,-206Z" fill="#ffffff" stroke="#b8c2d2" stroke-width="1.6"/>'
    # basket in right hand
    g+=(f'<path d="M40,-140 C42,-176 84,-176 86,-140" stroke="#8a5a2b" stroke-width="5" fill="none"/>'
        f'<path d="M34,-140 L92,-140 L84,-108 C78,-100 48,-100 42,-108Z" fill="#c98c4a" stroke="#7a4d22" stroke-width="2.4"/>'
        f'<path d="M38,-128 L88,-128 M41,-117 L85,-117" stroke="#7a4d22" stroke-width="2"/>'
        f'<path d="M44,-140 C50,-152 60,-152 64,-140 Z" fill="#ffffff" opacity=".9"/><circle cx="74" cy="-145" r="7" fill="#e85d5d"/>'
        f'<circle cx="56" cy="-130" r="10" fill="{skin}"/>')
    # neck + head
    g+=f'<rect x="-8" y="-222" width="16" height="18" fill="{skin_s}"/>'
    # pigtails (behind head)
    for s in (-1,1):
        g+=(f'<path d="M{s*40},-262 C{s*72},-262 {s*84},-236 {s*78},-206 C{s*74},-190 {s*64},-196 {s*66},-212 C{s*68},-232 {s*58},-246 {s*40},-246Z" fill="{hair}" stroke="{hair_s}" stroke-width="2.2"/>'
            f'<path d="M{s*48},-262 l{s*14},-12 l{s*4},16 l{s*-4},16 l{s*-14},-12Z" fill="#ff7fa8" stroke="#d94f80" stroke-width="1.6"/>')
    g+=f'<circle cx="0" cy="-258" r="44" fill="{skin}"/>'
    # hair cap + bangs
    g+=(f'<path d="M-45,-258 C-48,-300 -20,-312 0,-312 C20,-312 48,-300 45,-258 C38,-276 26,-282 14,-276 C6,-288 -6,-288 -14,-276 C-26,-284 -40,-276 -45,-258Z" fill="{hair}" stroke="{hair_s}" stroke-width="2.2"/>')
    # face: big happy eyes + SMILE + blush
    g+=(f'<ellipse cx="-16" cy="-252" rx="5.6" ry="7.2" fill="{ink}"/><circle cx="-14" cy="-255" r="2.2" fill="#fff"/>'
        f'<ellipse cx="16" cy="-252" rx="5.6" ry="7.2" fill="{ink}"/><circle cx="18" cy="-255" r="2.2" fill="#fff"/>'
        f'<path d="M-15,-236 Q0,-220 15,-236 Q0,-228 -15,-236Z" fill="#c94a5a" stroke="{ink}" stroke-width="2.6" stroke-linejoin="round"/>'
        f'<ellipse cx="-30" cy="-236" rx="8" ry="4.6" fill="#ff8fab" opacity=".65"/><ellipse cx="30" cy="-236" rx="8" ry="4.6" fill="#ff8fab" opacity=".65"/>')
    return f'<g transform="translate({x},{y}) scale({sc})">{g}</g>'
def pup(p,x,y,sc=1):
    """Small generic cartoon dog (not any specific film dog)."""
    ink='#22262e'
    g=('<ellipse cx="0" cy="2" rx="34" ry="6" fill="#000" opacity=".2"/>'
       '<ellipse cx="0" cy="-20" rx="26" ry="16" fill="#3a3f4b"/>'
       '<rect x="-20" y="-12" width="8" height="14" rx="4" fill="#3a3f4b"/><rect x="12" y="-12" width="8" height="14" rx="4" fill="#3a3f4b"/>'
       '<path d="M-24,-26 q-14,-8 -12,-22" stroke="#3a3f4b" stroke-width="6" fill="none" stroke-linecap="round"/>'
       '<circle cx="22" cy="-40" r="17" fill="#3a3f4b"/>'
       '<ellipse cx="10" cy="-44" rx="6" ry="11" fill="#2a2e37" transform="rotate(20 10 -44)"/><ellipse cx="35" cy="-44" rx="6" ry="11" fill="#2a2e37" transform="rotate(-20 35 -44)"/>'
       '<circle cx="17" cy="-42" r="3" fill="#fff"/><circle cx="28" cy="-42" r="3" fill="#fff"/><circle cx="17.5" cy="-41.5" r="1.6" fill="'+ink+'"/><circle cx="28.5" cy="-41.5" r="1.6" fill="'+ink+'"/>'
       '<ellipse cx="23" cy="-33" rx="4" ry="3" fill="#111"/><path d="M19,-29 q4,4 8,0" stroke="#ff8fab" stroke-width="2" fill="none"/>')
    return f'<g transform="translate({x},{y}) scale({sc})">{g}</g>'
def scene2(p='h',vb='0 0 800 500',sc=1.0):
    """Ad scene: same sky/road/Emerald City/tornado/coins, with smiling Dorothy in silver slippers as focal point."""
    bg=(f'<rect width="800" height="500" fill="#141925"/><circle cx="560" cy="250" r="230" fill="url(#{p}glow)" opacity=".25"/>'
        +''.join(spark(x,y,r,'#fff',o) for x,y,r,o in [(80,60,6,.8),(200,120,4,.6),(330,40,5,.7),(720,70,6,.8),(650,160,3,.6),(470,90,4,.6),(40,200,3,.5),(760,220,4,.6)]))
    ground='<path d="M0,300 C200,270 600,270 800,300 L800,500 L0,500Z" fill="#1f3b2c"/><path d="M0,330 C250,300 550,305 800,335 L800,500 L0,500Z" fill="#244a35"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="Original cartoon: a smiling girl in a blue-and-white checked dress and sparkly silver shoes on a yellow brick road, with a green city, a little tornado and silver Oz coins">'
            +DEFS.format(p=p)+bg+ground+road(p,800,500,262)+city(p,494,262,.9)
            +tornado(p,712,92,.62)+coin(p,610,170,34)+coin(p,300,56,20,'Oz.')
            +'<circle cx="400" cy="330" r="150" fill="url(#'+p+'glow)" opacity=".5"/>'
            +pup(p,530,478,1.1*sc)+dorothy(p,374,472,1.32*sc)
            +''.join(spark(x,y,r,'#fff',.95) for x,y,r in [(290,440,7),(650,420,6),(560,300,5),(470,330,6)])+'</svg>')
