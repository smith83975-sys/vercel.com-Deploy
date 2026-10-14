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
s+='<text x="84" y="'+(y(12)-9)+'" font-size="10" fill="#d4af37" text-anchor="middle">Rome ~12</text>';
const pk=d.annual.reduce((a,b)=>b.ratio>a.ratio?b:a);s+='<text x="'+x(pk.year)+'" y="'+(y(pk.ratio)-6)+'" font-size="10" fill="#ddd" text-anchor="middle">'+pk.year+': '+pk.ratio+'</text>';
const last=d.annual[d.annual.length-1];
if(live){s+='<circle cx="'+x(2026)+'" cy="'+y(live)+'" r="5" fill="#4caf50"/><text x="'+(x(2026)-6)+'" y="'+(y(live)-8)+'" font-size="10" fill="#8d8" text-anchor="end">Now ≈'+live.toFixed(1)+'</text>';}
s+='</svg><p class="note">Grey line: annual averages 1687–'+last.year+'. Gold dots: official/mint ratios (Roman value approximate). Green dot: today\'s live spot ratio. The time axis is broken between AD 1 and 1687 because there is no continuous sourced series for that gap. Annual averages hide short spikes and dips (for example single days in 1980 or 2020).</p>';
el.innerHTML=s;
const A=Object.fromEntries(d.annual.map(a=>[a.year,a.ratio])),src=d.annual_source,mw='<a href="'+src.url+'" rel="noopener">MeasuringWorth</a>';
let li=d.milestones.map(m=>'<li><b>'+(m.year<1000?'~AD '+m.year:m.year)+' — '+m.label+(m.ratio?': '+(m.approximate?'~':'')+m.ratio+':1':'')+'</b> ('+m.kind+(m.kind?'':'')+'). '+m.text+' <a href="'+m.url+'" rel="noopener">Source</a></li>').join('').replace(/ \(undefined\)/g,'');
[[1900,'Market ratio after silver demonetization'],[1940,'Highest annual average in the series'],[1968,'Lowest annual average since 1900'],[1980,'Silver boom year (annual average)'],[1991,'Silver slump'],[2011,'Silver rally'],[2020,'Pandemic year'],[last.year,'Latest full year']].forEach(([yr,t])=>{if(A[yr])li+='<li><b>'+yr+' — '+t+': '+A[yr]+':1</b> (annual average). Source: '+mw+'</li>';});
if(live)li+='<li><b>Today — live: ≈'+live.toFixed(2)+':1</b> (spot). See the <a href="#ratio">live ratio card</a>; source <a href="https://gold-api.com" rel="noopener">gold-api.com</a>.</li>';
list.innerHTML=li;})();
