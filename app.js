const M=n=>(n/1e6).toFixed(2)+'M oz', P='<span class="pending">pending</span>';
const $=id=>document.getElementById(id)||{innerHTML:''};
fetch('data/latest.json').then(r=>r.json()).then(d=>{
 const c=d.comex;
 $('comexCite').innerHTML=`Report date: <b>${c.report_date}</b>. Source: <a href="${c.source_url}">${c.source}</a>`;
 $('oiCite').innerHTML=`Open interest source: <a href="${d.open_interest.source_url}">${d.open_interest.source}</a>`;
 $('cards').innerHTML='';$('scores').innerHTML='';
 ['silver','gold'].forEach(m=>{
  const s=c[m], ch=s.registered_change_oz, oi=d.open_interest[m];
  $('cards').innerHTML+=`<div class="card"><h3>${m[0].toUpperCase()+m.slice(1)}</h3>
   <div>Registered</div><div class="big">${M(s.registered_oz)}</div>
   <div>Eligible: <b>${M(s.eligible_oz)}</b> · Total: <b>${M(s.total_oz)}</b></div>
   <div>Registered share: ${(100*s.registered_oz/s.total_oz).toFixed(1)}%</div>
   <div>Change vs ${s.change_vs}: <span class="${ch>=0?'up':'down'}">${ch>=0?'+':''}${(ch/1e3).toFixed(1)}K oz</span></div>
   <div class="cite">${s.precision_note} Data as of ${c.report_date}.</div></div>`;
  // score
  let inv=null,cov=null;
  const h=s.history_registered_moz;
  if(h){const v=Object.values(h),x=s.registered_oz/1e6;inv=100-100*v.filter(y=>y<=x+1e-9).length/v.length;}
  if(oi){const c2=100*s.registered_oz/(oi.contracts*oi.oz_per_contract);cov={pct:c2,comp:100-Math.min(100,c2)};}
  const parts=[inv,cov&&cov.comp].filter(v=>v!=null), score=parts.reduce((a,b)=>a+b,0)/parts.length;
  $('scores').innerHTML+=`<div class="card"><h3>${m} tightness</h3><div class="big">${score.toFixed(0)}/100 ${parts.length<2?'<span class="pending">(partial)</span>':''}</div>
   <div>Inventory component: ${inv==null?P+' (no daily history held yet)':inv.toFixed(0)+(h?` (${Object.keys(h).length}-day window)`:'')}</div>
   <div>Coverage: ${cov?cov.pct.toFixed(1)+'% of OI ounces → component '+cov.comp.toFixed(0):P}</div>
   <div class="cite">OI ${oi.contracts.toLocaleString()} contracts × ${oi.oz_per_contract} oz. Registered as of ${c.report_date}.</div></div>`;
 });
 const p=d.premiums; $('premCite').innerHTML=`Checked ${p.checked_at}. Source: ${p.source}.`;
 const tb=document.querySelector('#prem tbody')||{innerHTML:''};
 p.items.forEach(it=>{
  if(!it.dealers.length){tb.innerHTML+=`<tr><td>${it.product}</td><td colspan="4">${P}: ${it.pending}</td></tr>`;return;}
  it.dealers.forEach(x=>{const pr=x.price-it.spot;
   tb.innerHTML+=`<tr><td><a href="${it.url}">${it.product}</a></td><td>${x.dealer}${x.note?' ('+x.note+')':''}</td><td>$${x.price.toLocaleString(undefined,{minimumFractionDigits:2})}</td><td>$${it.spot.toLocaleString()}</td><td>+$${pr.toFixed(2)} (${(100*pr/it.spot).toFixed(1)}%)</td></tr>`;});
 });
}).catch(e=>{$('comexCite').innerHTML=P+': data failed to load ('+e+')';});
