"""Original satirical SVG art for /silver-manipulation-history: generic cartoon 'thief bankers'.
No real people, no bank names or logos. Style matches the Roman/cowboy figures in ratiohistory.js."""
NAVY='#1f2a44'; SKIN='#e0b98f'
def defs(p):
    return (f'<defs><pattern id="ps{p}" width="5" height="10" patternUnits="userSpaceOnUse"><rect width="5" height="10" fill="{NAVY}"/>'
            f'<line x1="1" y1="0" x2="1" y2="10" stroke="#9aa3b8" stroke-width=".55" opacity=".8"/></pattern>'
            f'<linearGradient id="bar{p}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eef1f5"/><stop offset="1" stop-color="#8d96a6"/></linearGradient>'
            f'<radialGradient id="spot{p}" cx=".5" cy=".55" r=".5"><stop offset="0" stop-color="#fff6c8" stop-opacity=".28"/><stop offset="1" stop-color="#fff6c8" stop-opacity="0"/></radialGradient></defs>')
def _sack(x,y,s=1,p=''):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 0 C-22 -4 -32 14 -24 30 C-18 42 2 40 4 26 C6 16 6 6 0 0z" fill="#cfc8b6" stroke="#8a826e" stroke-width="1.2"/>'
            f'<path d="M-3 1 q3 -5 6 0" fill="none" stroke="#8a826e" stroke-width="2"/>'
            f'<text x="-10" y="26" font-family="Georgia,serif" font-size="13" font-weight="700" fill="#4a4a4a" text-anchor="middle">Ag</text></g>')
def _bars(x,y,p):
    b=''.join(f'<path d="M{3*i%6} {-7*i} h24 l-3 -6 h-18z" fill="url(#bar{p})" stroke="#7b8494" stroke-width=".7"/>' for i in range(3))
    return f'<g transform="translate({x} {y})">{b}<text x="13" y="-2" font-size="4" fill="#555" text-anchor="middle">999</text></g>'
def banker(prop,p,stache=True):
    legs=(f'<path d="M-3 -42 L-11 -22 L-22 -7" stroke="{NAVY}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
          f'<path d="M4 -42 L15 -25 L13 -6" stroke="{NAVY}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
          f'<ellipse cx="-22" cy="-4" rx="7" ry="3.2" fill="#0a0a0a" transform="rotate(-28 -22 -4)"/><ellipse cx="18" cy="-3" rx="8" ry="3.2" fill="#0a0a0a"/>')
    torso=(f'<path d="M-11 -40 Q0 -36 11 -40 L19 -80 Q7 -88 -3 -84 Z" fill="url(#ps{p})" stroke="#11182a" stroke-width="1"/>'
           '<path d="M7 -85 L16 -82 L11 -69 Z" fill="#f2f2f2"/><path d="M11.5 -82 L13.5 -79 L11 -70 L9.5 -79Z" fill="#b23a3a"/>'
           '<path d="M-1 -60 h6" stroke="#d4af37" stroke-width="1"/>')
    head=(f'<circle cx="13" cy="-97" r="10" fill="{SKIN}"/><circle cx="23.5" cy="-94" r="2.4" fill="#d29e72"/>'
          + ('<path d="M15 -91 q4 -3 9 0 q-4 2 -9 0z" fill="#3a2a1a"/>' if stache else '<path d="M16 -89 q3 2 6 0" stroke="#7a4a30" stroke-width="1" fill="none"/>')
          + '<path d="M3 -101 h20 a3 3 0 0 1 0 6 h-20 a3 3 0 0 1 0-6z" fill="#111"/><circle cx="14" cy="-98" r="2" fill="#fff"/><circle cx="20" cy="-98" r="2" fill="#fff"/>'
          '<circle cx="15" cy="-98" r="1" fill="#111"/><circle cx="21" cy="-98" r="1" fill="#111"/>'
          '<path d="M3 -99 q-6 -1 -11 -6 M3 -97 q-6 2 -10 7" stroke="#111" stroke-width="2" fill="none" stroke-linecap="round"/>'
          '<g transform="rotate(-7 13 -106)"><rect x="1" y="-108" width="25" height="3" rx="1.5" fill="#0b0b0b"/><rect x="5" y="-127" width="17" height="20" rx="1" fill="#141414"/><rect x="5" y="-111" width="17" height="3" fill="#6a1f1f"/></g>')
    arm=lambda d: f'<path d="{d}" stroke="{NAVY}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    hand=lambda x,y: f'<circle cx="{x}" cy="{y}" r="3.6" fill="{SKIN}"/>'
    if prop=='sack':
        back=_sack(-8,-92,1,p)+arm('M3 -78 L-6 -89')+hand(-7,-90)
        front=arm('M14 -78 L26 -68 L34 -73')+hand(35,-73)+'<circle cx="-36" cy="-40" r="3" fill="#c0c6cf"/><circle cx="-44" cy="-22" r="2.6" fill="#c0c6cf"/>'
    elif prop=='bars':
        back=''; front=arm('M4 -76 L16 -62 L22 -60')+_bars(20,-58,p)+arm('M15 -79 L27 -66 L42 -62')+hand(22,-60)+hand(43,-61)
    else:  # spoof ticket
        back=_sack(-10,-66,.62,p)+arm('M2 -78 L-6 -68 L-9 -66')+hand(-10,-66)
        front=(arm('M15 -80 L28 -94 L33 -108')+'<g transform="rotate(8 55 -122)"><rect x="30" y="-136" width="52" height="27" rx="2" fill="#f4f1e6" stroke="#999"/>'
               '<text x="56" y="-123" font-family="system-ui,sans-serif" font-size="11" font-weight="800" fill="#c62828" text-anchor="middle">SPOOF</text>'
               '<text x="56" y="-114" font-family="system-ui,sans-serif" font-size="5.2" fill="#555" text-anchor="middle">SELL 2,000 · CANCEL</text></g>'+hand(33,-109))
    return f'<g class="banker">{back}{legs}{torso}{front}{head}</g>'
def _fig(x,y,s,art): return f'<ellipse cx="{x+4*s}" cy="{y}" rx="{24*s}" ry="{3.5*s}" fill="#000" opacity=".45"/><g transform="translate({x} {y}) scale({s})">{art}</g>'
def hero(p='h',viewbox='0 0 800 300'):
    stars=''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".55"/>' for x,y,r in [(760,40,1),(330,62,.8),(420,24,1.2),(520,48,.8),(600,20,1),(680,90,.8),(770,120,1),(230,90,.7),(470,80,.7)])
    vault=('<rect x="26" y="86" width="178" height="214" fill="#1d2230" stroke="#2c3344"/><text x="115" y="112" font-family="Georgia,serif" font-size="15" letter-spacing="4" fill="#9aa3b5" text-anchor="middle">VAULT</text>'
           '<circle cx="115" cy="200" r="64" fill="#07090d" stroke="#3a4152" stroke-width="5"/>'
           + ''.join(_bars(85+26*(i%3)+ (13 if i>2 else 0),236-(18 if i>2 else 0),p) for i in range(5))
           + '<ellipse cx="190" cy="200" rx="17" ry="64" fill="#6d7588" stroke="#aab2c3" stroke-width="2"/><circle cx="190" cy="200" r="9" fill="#9aa3b5"/>'
           '<path d="M190 182 v36 M174 200 h32" stroke="#4a5263" stroke-width="3" transform="rotate(20 190 200)"/>')
    trail=''.join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#c0c6cf" opacity="{o}"/>' for x,y,o in [(222,286,.9),(246,288,.8),(392,287,.9),(412,286,.7),(560,287,.8)])
    sneak=''.join(f'<path d="M{x} {y} q-10 6 -18 0" stroke="#7a8296" stroke-width="1.5" fill="none" opacity=".6"/>' for x,y in [(262,200),(258,214),(430,190),(426,204),(600,196),(596,210)])
    return (f'<svg viewBox="{viewbox}" width="100%" role="img" aria-label="Satirical cartoon: three masked bankers in pinstripe suits and top hats tiptoe away from an open vault with silver bars, a sack marked Ag and a ticket reading SPOOF" xmlns="http://www.w3.org/2000/svg">{defs(p)}'
            f'<rect width="800" height="300" rx="12" fill="#141925"/><circle cx="232" cy="44" r="20" fill="#e8e6da" opacity=".9"/><circle cx="225" cy="39" r="4" fill="#cfccbd"/><circle cx="238" cy="52" r="3" fill="#cfccbd"/>{stars}'
            f'{vault}<rect x="0" y="288" width="800" height="12" fill="#1a1d24"/>{trail}{sneak}'
            f'{_fig(298,288,1.55,banker("bars",p,False))}{_fig(468,288,1.55,banker("sack",p,True))}{_fig(636,288,1.55,banker("spoof",p,True))}</svg>')
def caught(p='c'):
    return (f'<svg viewBox="0 0 200 190" width="100%" role="img" aria-label="Satirical cartoon: a masked banker with a sack marked Ag caught in a spotlight, stamped FINED" xmlns="http://www.w3.org/2000/svg">{defs(p)}'
            f'<rect width="200" height="190" rx="10" fill="#141925"/><ellipse cx="100" cy="120" rx="95" ry="80" fill="url(#spot{p})"/>'
            f'{_fig(74,176,1.18,banker("sack",p,True))}'
            '<g transform="rotate(-14 157 40)"><rect x="118" y="24" width="78" height="30" rx="4" fill="none" stroke="#e53935" stroke-width="3"/>'
            '<text x="157" y="47" font-family="system-ui,sans-serif" font-size="19" font-weight="900" fill="#e53935" text-anchor="middle" letter-spacing="2">FINED</text></g></svg>')
