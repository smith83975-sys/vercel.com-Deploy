(function(){
const API='https://api.gold-api.com/price/';
const $=id=>document.getElementById(id);
const usd=n=>'$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
const src='<a href="https://gold-api.com" rel="noopener">gold-api.com</a>';
function scale(r){const el=$('gsr-scale');if(!el)return;if(!(r>0)){el.innerHTML='<p class="note">Scale unavailable — spot prices not loaded.</p>';el.setAttribute('aria-label','Balance scale unavailable: spot prices could not be loaded');return;}
const n=Math.round(r),tens=Math.floor(n/10),rem=n%10,rs=r.toFixed(1);let c='';
// right pan: stacks of 10 coins, plus a remainder stack
const stacks=[];for(let i=0;i<tens;i++)stacks.push(10);if(rem)stacks.push(rem);
const W=12,cols=stacks.length,x0=300-cols*W/2;
stacks.forEach((h,i)=>{for(let j=0;j<h;j++){const x=x0+i*W+W/2,y=118-j*4.2;c+='<ellipse cx="'+x+'" cy="'+y+'" rx="5.5" ry="2.4" fill="#c0c6cf" stroke="#7d848e" stroke-width=".6"/>';}});
el.innerHTML='<svg viewBox="0 0 400 200" width="100%" aria-hidden="true" focusable="false">'+
'<polygon points="185,190 215,190 204,40 196,40" fill="#555b66"/><rect x="160" y="188" width="80" height="6" rx="3" fill="#555b66"/>'+
'<rect x="60" y="38" width="280" height="5" rx="2.5" fill="#8a909a"/><circle cx="200" cy="40" r="7" fill="#d4af37"/>'+
'<line x1="100" y1="42" x2="70" y2="122" stroke="#8a909a"/><line x1="100" y1="42" x2="130" y2="122" stroke="#8a909a"/>'+
'<line x1="300" y1="42" x2="255" y2="122" stroke="#8a909a"/><line x1="300" y1="42" x2="345" y2="122" stroke="#8a909a"/>'+
'<path d="M55 122 h90 q-5 12 -45 12 q-40 0 -45 -12z" fill="#3a3f49"/><path d="M240 122 h120 q-6 12 -60 12 q-54 0 -60 -12z" fill="#3a3f49"/>'+
'<rect x="82" y="104" width="36" height="16" rx="3" fill="#d4af37" stroke="#9c7d1c"/><text x="100" y="116" font-size="8" text-anchor="middle" fill="#111" font-weight="700">1 oz</text>'+c+
'<text x="100" y="156" font-size="13" text-anchor="middle" fill="#d4af37" font-weight="700">1 oz gold</text>'+
'<text x="300" y="156" font-size="13" text-anchor="middle" fill="#c0c6cf" font-weight="700">≈'+rs+' oz silver</text>'+
'<text x="300" y="172" font-size="10" text-anchor="middle" fill="#999">each stack = 10 oz</text></svg>'+
'<p class="note">Equal value at today\'s spot prices: the beam is level because 1 oz of gold is worth about '+rs+' oz of silver.</p>';
el.setAttribute('aria-label','Balance scale: 1 ounce of gold balances about '+rs+' ounces of silver at current spot prices');}
function show(g,s,label){scale(g/s);$('gsr-value').textContent=(g/s).toFixed(2)+' : 1';$('gsr-prices').textContent='Gold '+usd(g)+' / oz · Silver '+usd(s)+' / oz';$('gsr-meta').innerHTML=label+' · Source: '+src;}
async function fallback(){try{const d=await (await fetch('data/latest.json',{cache:'no-store'})).json();const k=d.spot_last_known;if(k&&k.gold_usd&&k.silver_usd){show(k.gold_usd,k.silver_usd,'Live feed unavailable — last known value as of '+k.as_of.replace('T',' ').slice(0,16)+' UTC');return;}}catch(e){}
$('gsr-value').textContent='Unavailable';scale(0);$('gsr-prices').textContent='Spot prices could not be loaded.';$('gsr-meta').innerHTML='Source: '+src;}
async function load(){try{const [g,s]=await Promise.all(['XAU','XAG'].map(x=>fetch(API+x,{cache:'no-store'}).then(r=>{if(!r.ok)throw 0;return r.json()})));
if(!(g.price>0&&s.price>0))throw 0;const t=new Date(g.updatedAt||Date.now());
show(g.price,s.price,'Updated '+t.toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})+' (refreshes every 60s)');}catch(e){fallback();}}
load();setInterval(load,60000);
})();
