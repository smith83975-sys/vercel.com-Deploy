(async function(){
const el=document.getElementById('gsr-hist'),list=document.getElementById('gsr-eras');if(!el)return;
let d;try{d=await (await fetch('data/ratio_history.json',{cache:'no-store'})).json();}catch(e){el.innerHTML='<p class="note">History data could not be loaded.</p>';return;}
let live=null;try{const [g,s]=await Promise.all(['XAU','XAG'].map(x=>fetch('https://api.gold-api.com/price/'+x).then(r=>r.json())));if(g.price>0&&s.price>0)live=g.price/s.price;}catch(e){}
const W=800,H=330,L=44,B=290,T=20,ymax=110,y=v=>B-(v/ymax)*(B-T);
// ancient panel x 44..124, break, modern panel 150..780 for 1687..2026
const xa=yr=>84,x=yr=>150+(yr-1687)/(2026-1687)*630;
let s='<svg viewBox="0 0 '+W+' '+H+'" width="100%" role="img" aria-label="Chart of the gold-to-silver ratio from the Roman era to today">';
for(let v=0;v<=ymax;v+=20){s+='<line x1="'+L+'" x2="780" y1="'+y(v)+'" y2="'+y(v)+'" stroke="#2a2f38"/><text x="'+(L-6)+'" y="'+(y(v)+4)+'" font-size="11" fill="#999" text-anchor="end">'+v+'</text>';}
s+='<text x="135" y="'+(B+4)+'" font-size="16" fill="#777" text-anchor="middle">//</text>';
[1700,1750,1800,1850,1900,1950,2000].forEach(t=>s+='<text x="'+x(t)+'" y="'+(B+18)+'" font-size="11" fill="#999" text-anchor="middle">'+t+'</text>');
s+='<text x="84" y="'+(B+18)+'" font-size="11" fill="#999" text-anchor="middle">AD 1</text>';
const p=d.annual.map((a,i)=>(i?'L':'M')+x(a.year).toFixed(1)+' '+y(a.ratio).toFixed(1)).join(' ');
s+='<path d="'+p+'" fill="none" stroke="#c0c6cf" stroke-width="1.6"/>';
d.milestones.forEach(m=>{if(m.ratio==null){s+='<line x1="'+x(m.year)+'" x2="'+x(m.year)+'" y1="'+T+'" y2="'+B+'" stroke="#a55" stroke-dasharray="3 3"/><text x="'+(x(m.year)+4)+'" y="'+(T+10)+'" font-size="10" fill="#c88">'+m.year+' silver demonetized</text>';return;}
const cx=m.year<1687?xa():x(m.year);s+='<circle cx="'+cx+'" cy="'+y(m.ratio)+'" r="4.5" fill="#d4af37"><title>'+m.label+': ~'+m.ratio+':1</title></circle>';});
const rome=d.milestones.find(m=>m.year<1687&&m.ratio),ow=d.annual.find(a=>a.year===1873);
// Roman figure: helmet with crest, toga. Local coords: feet at (0,0), ~78 tall.
const roman='<g class="fig"><path d="M-8 -64 q8 -14 16 0" fill="#b23a3a"/><path d="M-9 -60 q9 -10 18 0 v6 h-18z" fill="#d4af37"/><circle cx="0" cy="-52" r="7" fill="#e0b98f"/><path d="M-9 -55 h18 v3 h-18z" fill="#d4af37"/><path d="M-13 -42 q13 -6 26 0 l4 40 h-34z" fill="#e8e2d0"/><path d="M-12 -40 l24 26 v4 l-26 -26z" fill="#b23a3a" opacity=".85"/><rect x="-7" y="-2" width="5" height="2" fill="#7a5a2e"/><rect x="2" y="-2" width="5" height="2" fill="#7a5a2e"/><line x1="17" y1="-70" x2="17" y2="0" stroke="#8a6a3a" stroke-width="2"/><path d="M14 -70 l3 -7 l3 7z" fill="#c0c6cf"/></g>';
// Cowboy: wide-brim hat, bandana, vest, boots.
const cowboy='<g class="fig"><path d="M-16 -60 q16 5 32 0 q-2 4 -16 5 q-14 -1 -16 -5z" fill="#8b5a2b"/><path d="M-8 -60 q0 -12 8 -12 q8 0 8 12z" fill="#8b5a2b"/><rect x="-8" y="-62" width="16" height="2.5" fill="#d4af37"/><circle cx="0" cy="-50" r="7" fill="#e0b98f"/><path d="M-7 -45 l7 7 l7 -7z" fill="#b23a3a"/><path d="M-12 -42 h24 l2 22 h-28z" fill="#5a7a9a"/><path d="M-12 -42 h7 v22 h-9z M12 -42 h-7 v22 h9z" fill="#6b4423"/><rect x="-12" y="-21" width="24" height="3" fill="#3a2a1a"/><circle cx="0" cy="-19.5" r="1.6" fill="#d4af37"/><path d="M-10 -18 h8 v14 h-8z M2 -18 h8 v14 h-8z" fill="#2f4a66"/><path d="M-11 -5 h10 v5 h-12z M1 -5 h10 l2 5 h-12z" fill="#4a2e18"/><rect x="-16" y="-41" width="4" height="18" rx="2" fill="#5a7a9a"/><rect x="12" y="-41" width="4" height="18" rx="2" fill="#5a7a9a"/></g>';
function fig(art,fx,fy,dx,dy,cap,sub){return '<line x1="'+fx+'" y1="'+(fy+2)+'" x2="'+dx+'" y2="'+(dy-6)+'" stroke="#d4af37" stroke-width="1" stroke-dasharray="2 3" opacity=".7"/><ellipse cx="'+fx+'" cy="'+fy+'" rx="14" ry="2.5" fill="#000" opacity=".35"/><g transform="translate('+fx+' '+fy+')">'+art+'</g><text x="'+fx+'" y="'+(fy-100)+'" font-size="12" font-weight="700" fill="#d4af37" text-anchor="middle">'+cap+'</text><text x="'+fx+'" y="'+(fy-87)+'" font-size="9.5" fill="#aaa" text-anchor="middle">'+sub+'</text>';}
if(rome)s+=fig(roman,84,y(rome.ratio)-26,84,y(rome.ratio),'Rome ~'+rome.ratio+':1','~AD '+rome.year);
if(ow)s+=fig(cowboy,450,y(ow.ratio)-34,x(1873),y(ow.ratio),'Old West ~'+Math.round(ow.ratio)+':1',ow.year+' avg '+ow.ratio);
const pk=d.annual.reduce((a,b)=>b.ratio>a.ratio?b:a);s+='<text x="'+x(pk.year)+'" y="'+(y(pk.ratio)-6)+'" font-size="10" fill="#ddd" text-anchor="middle">'+pk.year+': '+pk.ratio+'</text>';
const last=d.annual[d.annual.length-1];
if(live){s+='<circle cx="'+x(2026)+'" cy="'+y(live)+'" r="5" fill="#4caf50"/><rect x="'+(x(2026)-70)+'" y="'+(y(live)+10)+'" width="66" height="16" rx="8" fill="#16301a" stroke="#4caf50"/><text x="'+(x(2026)-37)+'" y="'+(y(live)+22)+'" font-size="10.5" font-weight="700" fill="#8d8" text-anchor="middle">Today ≈'+live.toFixed(1)+'</text>';}
s+='</svg><p class="note">Grey line: annual averages 1687–'+last.year+'. Gold dots: official/mint ratios (Roman value approximate). Figures mark the Roman era and the American Old West (1873 annual average); illustrations are ours. Green dot: today\'s live spot ratio. The time axis is broken between AD 1 and 1687 because there is no continuous sourced series for that gap. Annual averages hide short spikes and dips (for example single days in 1980 or 2020).</p>';
el.innerHTML=s;
const A=Object.fromEntries(d.annual.map(a=>[a.year,a.ratio])),src=d.annual_source,mw='<a href="'+src.url+'" rel="noopener">MeasuringWorth</a>';
let li=d.milestones.map(m=>'<li><b>'+(m.year<1000?'~AD '+m.year:m.year)+' — '+m.label+(m.ratio?': '+(m.approximate?'~':'')+m.ratio+':1':'')+'</b> ('+m.kind+(m.kind?'':'')+'). '+m.text+' <a href="'+m.url+'" rel="noopener">Source</a></li>').join('').replace(/ \(undefined\)/g,'');
[[1900,'Market ratio after silver demonetization'],[1940,'Highest annual average in the series'],[1968,'Lowest annual average since 1900'],[1980,'Silver boom year (annual average)'],[1991,'Silver slump'],[2011,'Silver rally'],[2020,'Pandemic year'],[last.year,'Latest full year']].forEach(([yr,t])=>{if(A[yr])li+='<li><b>'+yr+' — '+t+': '+A[yr]+':1</b> (annual average). Source: '+mw+'</li>';});
if(live)li+='<li><b>Today — live: ≈'+live.toFixed(2)+':1</b> (spot). See the <a href="#ratio">live ratio card</a>; source <a href="https://gold-api.com" rel="noopener">gold-api.com</a>.</li>';
list.innerHTML=li;})();
