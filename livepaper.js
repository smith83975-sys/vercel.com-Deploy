(function(){
const $=id=>document.getElementById(id);
const usd=(n,dp=0)=>'$'+n.toLocaleString('en-US',{minimumFractionDigits:dp,maximumFractionDigits:dp});
let LP=null;
async function load(){try{if(!LP){LP=(await (await fetch('data/latest.json',{cache:'no-store'})).json()).live_paper;}
const [g,s]=await Promise.all(['XAU','XAG'].map(x=>fetch('https://api.gold-api.com/price/'+x,{cache:'no-store'}).then(r=>{if(!r.ok)throw 0;return r.json()})));
if(!(g.price>0&&s.price>0))throw 0;
const M=LP.m2.value_usd,go=LP.gold_reserve.troy_oz,so=LP.silver_basis.troy_oz;
const pg=M/(go*g.price),ps=M/(so*s.price);
$('lp-gold').textContent=pg.toFixed(2)+' to 1';$('lp-gold-imp').textContent='Implied gold price: '+usd(M/go)+' / oz (spot '+usd(g.price,2)+')';
$('lp-silver').textContent=ps.toFixed(2)+' to 1';$('lp-silver-imp').textContent='Implied silver price: '+usd(M/so)+' / oz (spot '+usd(s.price,2)+')';
$('lp-meta').textContent='Spot updated '+new Date(g.updatedAt||Date.now()).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})+' · refreshes every 60s';
window.VP_LIVE_PAPER={gold:pg,silver:ps};document.dispatchEvent(new Event('vp-live-paper'));
}catch(e){if($('lp-meta'))$('lp-meta').textContent='Live spot unavailable — showing the Debt Clock snapshot below.';}}
load();setInterval(load,60000);
})();
