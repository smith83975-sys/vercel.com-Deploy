(function(){const $=id=>document.getElementById(id);const usd=(n,dp=0)=>'$'+n.toLocaleString('en-US',{minimumFractionDigits:dp,maximumFractionDigits:dp});
let LP=null,T=null,MS=null,V=null,sp={};
function render(){const p=Math.min(100,Math.max(1,+$('m1-num').value||30))/100;
[['gold','Gold',LP&&LP.gold_reserve.troy_oz,'#d4af37'],['silver','Silver',T&&T.total_oz,'#c0c6cf']].forEach(([m,N,oz,c])=>{const el=$('m1-'+m);
if(!LP||!LP.m1||!oz){el.innerHTML='<h3>'+N+'</h3><p class="note">Inputs unavailable.</p>';return;}
const imp=p*LP.m1.value_usd/oz,s=sp[m];const mult=s?imp/s:null;
const w=s?Math.max(1,100*Math.log10(s)/Math.log10(Math.max(imp,s))):0;
el.innerHTML='<h3>'+N+'</h3><div class="m1c-row"><span>Spot now</span><span class="m1c-big">'+(s?usd(s,2):'Unavailable')+'</span></div><div class="m1c-bar"><span style="width:'+w.toFixed(1)+'%;background:#7d848e"></span></div><div class="m1c-row"><span>Implied at '+Math.round(p*100)+'% of M1</span><span class="m1c-big" style="color:'+c+'">'+usd(imp)+'</span></div><div class="m1c-bar"><span style="width:100%;background:'+c+'"></span></div><div class="m1c-lbl">Bars on a log scale</div><div class="m1c-row"><span>Multiple of spot</span><span class="m1c-mult">'+(mult?mult.toLocaleString('en-US',{maximumFractionDigits:mult<100?1:0})+'×':'—')+'</span></div>';});}
async function spot(){const g=x=>fetch('https://api.gold-api.com/price/'+x,{cache:'no-store'}).then(r=>r.json()).then(j=>j.price>0?j.price:null).catch(()=>null);const [a,b]=await Promise.all([g('XAU'),g('XAG')]);sp={gold:a,silver:b};render();}
async function init(){try{const d=await (await fetch('/data/latest.json',{cache:'no-store'})).json();LP=d.live_paper;T=d.paper_to_metal.silver;MS=d.paper_to_metal.money_supply;V=d.paper_to_metal.vault;}catch(e){}
if(LP&&LP.m1&&T)$('m1-src').innerHTML='M1: '+usd(LP.m1.value_usd/1e9)+'B ('+LP.m1.month+', <a href="'+LP.m1.source+'">FRED M1SL</a>). US gold reserve: '+Math.round(LP.gold_reserve.troy_oz).toLocaleString('en-US')+' oz (as of '+LP.gold_reserve.as_of+', <a href="'+LP.gold_reserve.source+'">US Treasury</a>). COMEX silver: '+Math.round(T.total_oz).toLocaleString('en-US')+' oz total, registered + eligible (as of '+V.report_date+', CME warehouse reports via <a href="https://thevaultreport.com/comex">The Vault Report</a>). Spot: <a href="https://gold-api.com">gold-api.com</a>, refreshes every 60s.';
const r=$('m1-range'),n=$('m1-num');r.oninput=()=>{n.value=r.value;render()};n.oninput=()=>{const v=Math.min(100,Math.max(1,+n.value||1));r.value=v;render()};
render();spot();setInterval(spot,60000);}
init();})();
