(function(){
const $=id=>document.getElementById(id);
const usd=(n,dp=0)=>'$'+n.toLocaleString('en-US',{minimumFractionDigits:dp,maximumFractionDigits:dp});
function svg(metal,ratio,per){
const a=14*Math.PI/180,L=150,cx=230,cy=50;
const lx=cx-L*Math.cos(a),ly=cy-L*Math.sin(a),rx=cx+L*Math.cos(a),ry=cy+L*Math.sin(a);
const n=Math.round(ratio),full=Math.floor(n/per),rem=n%per;const items=[];for(let i=0;i<full;i++)items.push(per);if(rem)items.push(rem);
let bills='';const cols=Math.min(7,items.length),bw=18,bh=8;
items.forEach((v,i)=>{const col=i%cols,row=Math.floor(i/cols);const x=rx-cols*bw/2+col*bw,y=ry+86-row*(bh+1);const w=v===per?bw-2:Math.max(4,(bw-2)*v/per);
bills+='<rect x="'+x.toFixed(1)+'" y="'+y.toFixed(1)+'" width="'+w.toFixed(1)+'" height="'+bh+'" rx="1" fill="#5f9a5a" stroke="#2f5a2c" stroke-width=".6"/>';});
const gold=metal==='gold';
const obj=gold?'<rect x="'+(lx-22)+'" y="'+(ly+72)+'" width="44" height="20" rx="3" fill="#d4af37" stroke="#9c7d1c"/>':'<circle cx="'+lx+'" cy="'+(ly+82)+'" r="11" fill="#c0c6cf" stroke="#7d848e"/>';
const pan=(x,y,w)=>'<line x1="'+x+'" y1="'+y+'" x2="'+(x-w/2)+'" y2="'+(y+94)+'" stroke="#8a909a"/><line x1="'+x+'" y1="'+y+'" x2="'+(x+w/2)+'" y2="'+(y+94)+'" stroke="#8a909a"/><path d="M'+(x-w/2-5)+' '+(y+94)+' h'+(w+10)+' q-5 12 -'+(w/2+5)+' 12 q-'+(w/2)+' 0 -'+(w/2+5)+' -12z" fill="#3a3f49"/>';
const r2=ratio.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
return '<svg viewBox="0 0 460 280" aria-hidden="true" focusable="false"><polygon points="214,262 246,262 234,50 226,50" fill="#555b66"/><rect x="190" y="260" width="80" height="7" rx="3" fill="#555b66"/>'+
'<line x1="'+lx.toFixed(1)+'" y1="'+ly.toFixed(1)+'" x2="'+rx.toFixed(1)+'" y2="'+ry.toFixed(1)+'" stroke="#8a909a" stroke-width="6" stroke-linecap="round"/><circle cx="230" cy="50" r="8" fill="#d4af37"/>'+
pan(+lx.toFixed(1),ly,80)+pan(+rx.toFixed(1),ry,130)+obj+bills+
'<text x="'+lx.toFixed(0)+'" y="'+(ly+130).toFixed(0)+'" font-size="17" text-anchor="middle" fill="'+(gold?'#d4af37':'#c0c6cf')+'" font-weight="700">$1 of '+metal+'</text>'+
'<text x="'+rx.toFixed(0)+'" y="'+(ry+130).toFixed(0)+'" font-size="17" text-anchor="middle" fill="#7fbf7a" font-weight="700">$'+r2+' of paper</text>'+
'<text x="'+rx.toFixed(0)+'" y="'+(ry+148).toFixed(0)+'" font-size="12" text-anchor="middle" fill="#999">each bundle = $'+per+'</text></svg>';}
function tiers(m,oz,sp){const el=$('lp-'+m+'-tiers');if(!el)return;const M=PM&&PM.money_supply&&PM.money_supply.m2_usd;const nm=m==='gold'?'gold':'silver';
let h='<p class="pm-tiers-intro">If '+nm+' backed X% of the money supply, the price per ounce would need to be… <em>(hypothetical, not a prediction, not financial advice)</em></p><table class="pm-tier-table"><thead><tr><th>Backing</th><th>Implied price</th><th>vs spot</th></tr></thead><tbody>';
[30,40,50,100].forEach(p=>{let v='Unavailable',x='Unavailable';if(M&&oz>0){const i=p/100*M/oz;v=usd(i)+' /oz';if(sp&&sp.price>0)x=(i/sp.price).toLocaleString('en-US',{maximumFractionDigits:i/sp.price<100?1:0})+'x spot';}h+='<tr><td>'+p+'%</td><td>'+v+'</td><td>'+x+'</td></tr>';});
el.innerHTML=h+'</tbody></table>';}
let LP=null,PM=null;
async function load(){
try{if(!PM){const d=await (await fetch('/data/latest.json',{cache:'no-store'})).json();LP=d.live_paper;PM=d.paper_to_metal;}}catch(e){}
const MS=PM&&PM.money_supply;if(MS&&MS.implied_gold_m2_usd_per_oz){$('lp-gold-imp').textContent=usd(MS.implied_gold_m2_usd_per_oz)+' /oz';}
const get=x=>fetch('https://api.gold-api.com/price/'+x,{cache:'no-store'}).then(r=>{if(!r.ok)throw 0;return r.json()}).then(j=>{if(!(j.price>0))throw 0;return j}).catch(()=>null);
const [g,s]=await Promise.all([get('XAU'),get('XAG')]);
const set=(m,sp,oz)=>{if(sp&&MS&&oz){const r=MS.m2_usd/(oz*sp.price);$('lp-'+m).textContent=r.toFixed(2)+' to 1';$('lp-'+m+'-spot').textContent=usd(sp.price,2)+' /oz';const el=$('lp-'+m+'-scale');el.innerHTML=svg(m,r,m==='gold'?2:100);el.setAttribute('aria-label','Balance scale tipped toward paper: $1 of '+m+' against $'+r.toFixed(2)+' of paper money (live, our calculation). Illustration only.');}
else{$('lp-'+m).textContent='Unavailable';$('lp-'+m+'-spot').textContent='Unavailable';$('lp-'+m+'-scale').innerHTML='<p class="note" style="text-align:center">Scale unavailable: live spot price could not be loaded.</p>';}};
if(MS){set('gold',g,MS.gold_reserve_oz);
const T=PM.silver,V=PM.vault;
if(T&&T.total_oz>0&&MS.implied_silver_m2_usd_per_oz){const si=MS.implied_silver_m2_usd_per_oz;$('lp-silver-imp').textContent=usd(si)+' /oz';$('lp-reg-oz').textContent=Math.round(T.total_oz).toLocaleString('en-US')+' oz total ('+Math.round(T.registered_oz).toLocaleString('en-US')+' registered + '+Math.round(T.eligible_oz).toLocaleString('en-US')+' eligible)';$('lp-reg-src').innerHTML='as of '+V.report_date+', CME warehouse reports via <a href="https://thevaultreport.com/comex">The Vault Report</a>';
if(s){const r=si/s.price;$('lp-silver').textContent=Math.round(r).toLocaleString('en-US')+' to 1';$('lp-silver-spot').textContent=usd(s.price,2)+' /oz';const el=$('lp-silver-scale');el.innerHTML=svg('silver',r,100);el.setAttribute('aria-label','Balance scale tipped toward paper: $1 of silver in all COMEX vaults against $'+Math.round(r).toLocaleString('en-US')+' of paper money (live, our calculation). Illustration only.');}
else set('silver',null,0);}
else{$('lp-silver-imp').textContent='Unavailable';$('lp-reg-oz').textContent='Unavailable';set('silver',null,0);}}
tiers('gold',MS&&MS.gold_reserve_oz,g);tiers('silver',PM&&PM.silver&&PM.silver.total_oz,s);
$('lp-meta').textContent=(g&&s)?'Spot updated '+new Date(g.updatedAt||Date.now()).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})+' · refreshes every 60s':'Live spot unavailable right now. Ratios and spot are not shown rather than estimated; retrying every 60s.';
}
load();setInterval(load,60000);
})();
