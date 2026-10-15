/* HYPOTHETICAL "What backs a dollar?" calculator. Every number comes from
   data/latest.json -> resource_backing (written by scripts/compute_resource_backing.py
   from data/resources.json + FRED/EIA/USGS/Treasury/BEA inputs). Nothing is hardcoded here.
   The same render code runs at build time (node) for the static fallback. */
(function(root){
const esc=t=>String(t==null?'':t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const A=(u,t)=>u?'<a href="'+esc(u)+'" rel="noopener">'+esc(t)+'</a>':esc(t);
const big=n=>{if(n==null)return 'n/a';const a=Math.abs(n);return a>=1e12?'$'+(n/1e12).toFixed(2)+'T':a>=1e9?'$'+(n/1e9).toFixed(1)+'B':a>=1e6?'$'+(n/1e6).toFixed(1)+'M':'$'+Math.round(n).toLocaleString('en-US');};
const num=n=>n==null?'n/a':Number(n).toLocaleString('en-US',{maximumFractionDigits:2});
const usd=(n,dp)=>n==null?'n/a':'$'+Number(n).toLocaleString('en-US',{minimumFractionDigits:dp,maximumFractionDigits:dp});
const pf=x=>x==null?'n/a':(x>0&&x<0.01?x.toPrecision(2):x.toFixed(2));
const day=s=>!s?'n/a':/^\d{4}-\d{2}-\d{2}/.test(s)?s.slice(0,10):s;
const OWN={federal:'Federal',national:'National total',private:'Private'};
const COL={silver:'#c0c6cf',gold:'#d4af37',oil:'#7a5c3e',gas:'#4f8fbf',coal:'#555',minerals:'#b87333',land:'#5f9a5a'};
function val(i,live){if(live&&i.base_unit==='troy oz'&&(i.price_key==='spot_silver'||i.price_key==='spot_gold')){const s=live[i.price_key==='spot_silver'?'silver':'gold'];if(s)return i.base_quantity*s;}return i.value_usd;}
function priceOf(i,live){if(live&&i.price_key&&live[i.price_key==='spot_silver'?'silver':i.price_key==='spot_gold'?'gold':'']){return {v:live[i.price_key==='spot_silver'?'silver':'gold'],d:'live'};}return {v:i.price,d:day(i.price_as_of)};}
function qty(i){if(i.quantity==null)return 'Published estimate';const q=num(i.quantity)+' '+esc(i.quantity_unit);return i.base_unit==='troy oz'&&i.quantity_unit!=='troy oz'?q+' ('+(i.base_quantity/1e6).toFixed(2)+'M oz)':q;}
function compute(rb,st,live){const ms=rb.money_supply,K={m1:['M1',ms.m1_usd,ms.m1_month,ms.m1_source,'FRED'],m2:['M2',ms.m2_usd,ms.m2_month,ms.m2_source,'FRED'],debt:['national debt',ms.debt_usd,ms.debt_date,ms.debt_source,'US Treasury, Debt to the Penny']}[st.m]||[],M=K[1];let tot=0,ag=0;const rows=rb.items.map(i=>{const v=val(i,live),on=!!st.on[i.id];if(on&&v!=null){tot+=v;if(i.group==='silver')ag+=v;}return {i,v,on};});return {rows,tot,ag,M,lab:K[0],month:K[2],src:K[3],srcn:K[4],debt:st.m==='debt'};}
function body(rb,st,live){const c=compute(rb,st,live);const pct=c.M?100*c.tot/c.M:null,per=c.M?c.tot/c.M:null,agp=c.M?100*c.ag/c.M:null;
 let h='<div class="rb-head"><div class="rb-big">'+(pct==null?'n/a':pct.toFixed(1)+'%')+'</div><div>of '+(c.debt?'the national debt (total public debt outstanding)':c.lab)+' covered by the resources ticked below: <b>'+big(c.tot)+'</b> vs '+c.lab+' <b>'+big(c.M)+'</b> ('+(c.debt?'as of ':'')+esc(c.month)+', '+A(c.src,c.srcn)+'). That is <b>'+(per==null?'n/a':usd(per,2))+'</b> of resources per '+(c.debt?'dollar of debt':c.lab+' dollar')+'.</div></div>';
 if(c.debt&&rb.revaluation_note)h+='<p class="note"><b>Hypothetical.</b> '+esc(rb.revaluation_note.text.replace('usdebtclock.org','__U__')).replace('__U__',A(rb.revaluation_note.url,rb.revaluation_note.name))+' Selling or pledging these resources is not how US debt is paid, and most are not federally owned.</p>';
 h+='<p class="rb-silver"><b>Silver first:</b> the silver rows ticked add up to '+big(c.ag)+', or '+(agp==null?'n/a':pf(agp)+'%')+' of '+c.lab+'. The US government has no official silver reserve; the US Mint holds working stocks for coins.</p>';
 if(c.tot>0){h+='<div class="rb-bar" role="img" aria-label="Breakdown of selected resource value">';c.rows.filter(r=>r.on&&r.v>0).forEach(r=>{const w=100*r.v/c.tot;h+='<span title="'+esc(r.i.name)+': '+big(r.v)+'" style="width:'+w.toFixed(2)+'%;background:'+(COL[r.i.group]||'#888')+'"></span>';});h+='</div>';
  const g={};c.rows.filter(r=>r.on&&r.v>0).forEach(r=>{g[r.i.group]=(g[r.i.group]||0)+r.v;});h+='<p class="rb-legend">'+Object.keys(g).map(k=>'<span><i style="background:'+(COL[k]||'#888')+'"></i>'+esc(k)+' '+(100*g[k]/c.tot).toFixed(1)+'%</span>').join(' ')+'</p>';}
 if(c.rows.some(r=>r.on&&r.i.group==='land'))h+='<p class="note">Land rows are a published 2009 estimate (BEA working paper), not updated to today, and cover the lower 48 states only. Untick them to compare only resources priced today.</p>';
 return h;}
function table(rb,st,live){const c=compute(rb,st,live);let h='<div class="rb-tw"><table class="rb-t"><thead><tr><th>Include</th><th>Resource</th><th>Owner</th><th>Quantity (as of)</th><th>Price (as of)</th><th>Value</th><th>Source</th></tr></thead><tbody>';
 c.rows.forEach(r=>{const i=r.i,p=priceOf(i,live);h+='<tr'+(r.on?'':' class="rb-off"')+'><td data-l="Include"><input type="checkbox" class="rb-cb" data-id="'+esc(i.id)+'"'+(r.on?' checked':'')+' aria-label="Include '+esc(i.name)+'"></td><td data-l="Resource"><b>'+esc(i.name)+'</b><br><small>'+esc(i.note||'')+'</small></td><td data-l="Owner">'+esc(OWN[i.ownership]||i.ownership)+'</td><td data-l="Quantity">'+qty(i)+'<br><small>'+esc(i.as_of)+'</small></td><td data-l="Price">'+(i.price_key?usd(p.v,2)+' '+esc((i.price_unit||'').replace('$',''))+(i.conversion?' '+esc(i.conversion):'')+'<br><small>'+esc(p.d)+'</small>':'<small>'+esc(i.value_basis)+'</small>')+'</td><td data-l="Value"><b>'+big(r.v)+'</b>'+(c.M&&r.v?'<br><small>'+pf(100*r.v/c.M)+'% of '+c.lab+'</small>':'')+'</td><td data-l="Source">'+A(i.source_url,i.source_name)+'</td></tr>';});
 return h+'</tbody></table></div>';}
function sources(rb){const pr=rb.prices||{},cx=rb.context||{},cv=rb.conversions||{};const ms=rb.money_supply||{};let h='<details class="rb-src" open><summary><b>Prices, conversions &amp; what we left out</b></summary><ul class="pm-src-list">';
 h+='<li><b>Money supply &amp; debt</b>: M2 '+big(ms.m2_usd)+' ('+esc(ms.m2_month)+', '+A(ms.m2_source,'FRED M2SL')+'); M1 '+big(ms.m1_usd)+' ('+esc(ms.m1_month)+', '+A(ms.m1_source,'FRED M1SL')+'); total public debt outstanding '+big(ms.debt_usd)+' (as of '+esc(ms.debt_date)+', '+A(ms.debt_source,ms.debt_source_name)+'; '+big(ms.debt_held_public_usd)+' held by the public + '+big(ms.debt_intragov_usd)+' intragovernmental)'+(ms.debt_stale_note?' <em>'+esc(ms.debt_stale_note)+'</em>':'')+'.</li>';
 Object.keys(pr).forEach(k=>{const p=pr[k];h+='<li><b>'+esc(p.label)+'</b>: '+usd(p.value,2)+' '+esc((p.unit||'').replace('$',''))+' (as of '+esc(day(p.as_of))+'), '+A(p.source_url,p.source_name)+(p.stale_note?' <em>'+esc(p.stale_note)+'</em>':'')+'.</li>';});
 h+='<li><b>Conversions</b>: 1 metric ton = '+num(cv.troy_oz_per_metric_ton)+' troy oz ('+A(cv.troy_oz_source&&cv.troy_oz_source.url,'USGS')+'); 1 Mcf natural gas = '+num(cv.mmbtu_per_mcf)+' MMBtu ('+A(cv.mmbtu_source&&cv.mmbtu_source.url,'EIA')+').</li>';
 if(cx.source_url)h+='<li><b>Federal land context</b>: '+(cx.federal_acres_five_agencies/1e6).toFixed(1)+'M acres managed by five federal agencies, about '+(cx.federal_acres_total_est/1e6).toFixed(0)+'M acres in all (as of '+esc(cx.as_of)+', '+A(cx.source_url,cx.source_name)+'). '+esc(cx.federal_mineral_estate_note||'')+'</li>';
 (rb.left_out||[]).forEach(x=>{h+='<li><b>Left out: '+esc(x.name)+'</b>. '+esc(x.reason)+'</li>';});
 h+='</ul><p class="pm-formula"><b>Formula:</b> value = quantity × price ('+esc(rb.formula&&rb.formula.value)+'). Land = '+esc(rb.formula&&rb.formula.land)+'. Coverage = selected value ÷ M1, M2 or total public debt.</p><p class="note">Computed from <a href="/data/latest.json">latest.json</a> (resource_backing, updated '+esc((rb.computed_at||'').slice(0,10))+'), inputs in <a href="/data/resources.json">resources.json</a>.</p></details>';return h;}
function defaults(rb){const on={};rb.items.forEach(i=>on[i.id]=!!i.default_on);return {m:'m2',on};}
function render(rb,st,live){st=st||defaults(rb);
 return '<h3>What backs a dollar? Silver, gold, oil, land &amp; more <span class="rb-hyp">HYPOTHETICAL</span></h3>'+
 '<p class="rb-warn"><b>Hypothetical.</b> '+esc(String(rb.disclaimer||'').replace(/^HYPOTHETICAL\.\s*/,''))+' "Federal" rows are owned by the US government; "National total" rows are everything in the US, mostly owned by companies, states, tribes and individuals.</p>'+
 '<div class="rb-ctl" role="group" aria-label="Calculator options"><label><input type="radio" name="rb-m" value="m2"'+(st.m==='m2'?' checked':'')+'> vs M2</label><label><input type="radio" name="rb-m" value="m1"'+(st.m==='m1'?' checked':'')+'> vs M1</label><label><input type="radio" name="rb-m" value="debt"'+(st.m==='debt'?' checked':'')+'> vs national debt</label><button type="button" class="rb-btn" data-set="all">Tick all</button><button type="button" class="rb-btn" data-set="federal">Federal only</button><button type="button" class="rb-btn" data-set="default">Reset</button></div>'+
 '<div class="rb-body">'+body(rb,st,live)+'</div>'+table(rb,st,live)+sources(rb);}
const api={render,defaults};
if(typeof module!=='undefined'&&module.exports){module.exports=api;return;}
root.VPres=api;
const el=document.getElementById('rb-card');if(!el)return;let RB=null,ST=null,LIVE=null;
function draw(){el.innerHTML=render(RB,ST,LIVE);}
el.addEventListener('change',e=>{const t=e.target;if(!RB)return;if(t.classList.contains('rb-cb')){ST.on[t.dataset.id]=t.checked;draw();}else if(t.name==='rb-m'){ST.m=t.value;draw();}});
el.addEventListener('click',e=>{const b=e.target.closest('.rb-btn');if(!b||!RB)return;const s=b.dataset.set;if(s==='default')ST=defaults(RB);else RB.items.forEach(i=>ST.on[i.id]=s==='all'?true:i.ownership==='federal');draw();});
async function spot(){const g=x=>fetch('https://api.gold-api.com/price/'+x,{cache:'no-store'}).then(r=>r.json()).then(j=>j.price>0?j.price:null).catch(()=>null);const [a,b]=await Promise.all([g('XAU'),g('XAG')]);if(a&&b){LIVE={gold:a,silver:b};if(RB)draw();}}
fetch('/data/latest.json',{cache:'no-store'}).then(r=>r.json()).then(d=>{if(!d.resource_backing)return;RB=d.resource_backing;ST=defaults(RB);draw();spot();setInterval(spot,60000);}).catch(()=>{});
})(this);
