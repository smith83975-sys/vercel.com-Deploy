(function(){
const API='https://api.gold-api.com/price/';
const $=id=>document.getElementById(id);
const usd=n=>'$'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
const src='<a href="https://gold-api.com" rel="noopener">gold-api.com</a>';
function show(g,s,label){$('gsr-value').textContent=(g/s).toFixed(2)+' : 1';$('gsr-prices').textContent='Gold '+usd(g)+' / oz · Silver '+usd(s)+' / oz';$('gsr-meta').innerHTML=label+' · Source: '+src;}
async function fallback(){try{const d=await (await fetch('data/latest.json',{cache:'no-store'})).json();const k=d.spot_last_known;if(k&&k.gold_usd&&k.silver_usd){show(k.gold_usd,k.silver_usd,'Live feed unavailable — last known value as of '+k.as_of.replace('T',' ').slice(0,16)+' UTC');return;}}catch(e){}
$('gsr-value').textContent='Unavailable';$('gsr-prices').textContent='Spot prices could not be loaded.';$('gsr-meta').innerHTML='Source: '+src;}
async function load(){try{const [g,s]=await Promise.all(['XAU','XAG'].map(x=>fetch(API+x,{cache:'no-store'}).then(r=>{if(!r.ok)throw 0;return r.json()})));
if(!(g.price>0&&s.price>0))throw 0;const t=new Date(g.updatedAt||Date.now());
show(g.price,s.price,'Updated '+t.toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})+' (refreshes every 60s)');}catch(e){fallback();}}
load();setInterval(load,60000);
})();
