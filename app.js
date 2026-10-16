const M=n=>(n/1e6).toFixed(2)+'M oz', P='<span class="pending">pending</span>';
const N=n=>Math.round(n).toLocaleString('en-US')+' oz';
const DT=iso=>{if(!iso)return 'date n/a';const d=new Date(String(iso).slice(0,10)+'T12:00:00Z');return isNaN(d)?String(iso):d.toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric',timeZone:'UTC'});};
const CB=(t,l)=>'<p class="calc-basis"><b>'+(l||'How this is calculated')+':</b> '+t+'</p>';
const VS='CME Group warehouse report via The Vault Report';
const $=id=>document.getElementById(id)||{innerHTML:''};
fetch('data/latest.json').then(r=>r.json()).then(d=>{
 const c=d.comex;
 $('comexCite').innerHTML=`Report date: <b>${c.report_date}</b>. Source: <a href="${c.source_url}">${c.source}</a>`;
 const PM=d.paper_to_metal||{};$('oiCite').innerHTML=`Open interest: <a href="${d.open_interest.source_url}">CME Daily Bulletin, Section 02B</a>; ${(PM.open_interest||{}).as_of_label||'date unknown'}.`;
 $('cards').innerHTML='';$('scores').innerHTML='';
 ['silver','gold'].forEach(m=>{
  const s=c[m], ch=s.registered_change_oz, oi=d.open_interest[m], pm=PM[m];
  $('cards').innerHTML+=`<div class="card"><h3>${m[0].toUpperCase()+m.slice(1)}</h3>
   <div>Registered</div><div class="big">${M(s.registered_oz)}</div>
   <div>Eligible: <b>${M(s.eligible_oz)}</b> · Total: <b>${M(s.total_oz)}</b></div>
   <div>Registered share: ${(100*s.registered_oz/s.total_oz).toFixed(1)}%</div>
   <div>Change vs ${s.change_vs}: <span class="${ch>=0?'up':'down'}">${ch>=0?'+':''}${(ch/1e3).toFixed(1)}K oz</span></div>
   <div class="cite">${s.precision_note} Data as of ${c.report_date}.</div>
   ${CB(`Total ${N(s.total_oz)} = ${N(s.registered_oz)} registered + ${N(s.eligible_oz)} eligible. Registered share ${(100*s.registered_oz/s.total_oz).toFixed(1)}% = ${N(s.registered_oz)} ÷ ${N(s.total_oz)}. Change ${ch>=0?'+':''}${ch.toLocaleString('en-US')} oz = ${N(s.registered_oz)} (${DT(c.report_date)}) − ${N(s.registered_oz-ch)} (${DT(s.change_vs)}). Source: ${VS}.`)}</div>`;
  // score
  let inv=null,cov=null;
  const h=s.history_registered_moz;
  if(h){const v=Object.values(h),x=s.registered_oz/1e6;inv=100-100*v.filter(y=>y<=x+1e-9).length/v.length;}
  if(pm&&pm.coverage_total_pct!=null){const c2=pm.coverage_total_pct;cov={pct:c2,reg:pm.coverage_registered_pct_secondary,comp:100-Math.min(100,c2)};}
  const parts=[inv,cov&&cov.comp].filter(v=>v!=null), score=parts.reduce((a,b)=>a+b,0)/parts.length;
  $('scores').innerHTML+=`<div class="card"><h3>${m} tightness</h3><div class="big">${score.toFixed(0)}/100 ${parts.length<2?'<span class="pending">(partial)</span>':''}</div>
   <div>Inventory component: ${inv==null?P+' (no daily history held yet)':inv.toFixed(0)+(h?` (${Object.keys(h).length}-day window)`:'')}</div>
   <div>Coverage: ${cov?'total vault metal = '+cov.pct.toFixed(1)+'% of OI ounces → component '+cov.comp.toFixed(0):P}</div>
   ${cov&&cov.reg!=null?`<div class="cite">Secondary: registered only = ${cov.reg.toFixed(1)}% of OI ounces.</div>`:''}
   <div class="cite">OI ${pm?pm.oi_contracts.toLocaleString():'n/a'} contracts × ${pm?pm.oz_per_contract.toLocaleString():'n/a'} oz; ${PM.open_interest?PM.open_interest.as_of_label:''}. Vaults as of ${c.report_date}.</div>
   ${CB((parts.length<2?`score ${score.toFixed(0)} = the one available component (partial; no daily registered history held for ${m} yet).`:`score ${score.toFixed(0)} = average of ${parts.map(v=>v.toFixed(0)).join(' and ')}.`)+(inv!=null?` Inventory ${inv.toFixed(0)} = 100 − percentile of today's ${(s.registered_oz/1e6).toFixed(2)}M oz registered within ${Object.keys(h).length} daily readings (${DT(Object.keys(h).sort()[0])} to ${DT(Object.keys(h).sort().slice(-1)[0])}, ${VS}).`:'')+(cov?` Coverage ${cov.comp.toFixed(0)} = 100 − min(100, ${cov.pct.toFixed(1)}%), where ${cov.pct.toFixed(1)}% = ${N(s.total_oz)} total vault ${m} ÷ ${N(pm.paper_oz)} open interest (${pm.oi_contracts.toLocaleString('en-US')} contracts × ${pm.oz_per_contract.toLocaleString('en-US')} oz, CME Daily Bulletin Sec. 02B; ${PM.open_interest.as_of_label}).`:''))}</div>`;
 });
 const p=d.premiums; $('premCite').innerHTML=`Checked ${p.checked_at}. Source: ${p.source}.`;
 const tb=document.querySelector('#prem tbody')||{innerHTML:''};
 p.items.forEach(it=>{
  if(!it.dealers.length){tb.innerHTML+=`<tr><td>${it.product}</td><td colspan="4">${P}: ${it.pending}</td></tr>`;return;}
  it.dealers.forEach(x=>{const pr=x.price-it.spot;
   tb.innerHTML+=`<tr><td><a href="${it.url}">${it.product}</a></td><td>${x.dealer}${x.note?' ('+x.note+')':''}</td><td>$${x.price.toLocaleString(undefined,{minimumFractionDigits:2})}</td><td>$${it.spot.toLocaleString()}</td><td>+$${pr.toFixed(2)} (${(100*pr/it.spot).toFixed(1)}%)<br><small class="calc-basis">= $${x.price.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2})} − $${it.spot.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2})}; ÷ spot ref.</small></td></tr>`;});
 });
}).catch(e=>{$('comexCite').innerHTML=P+': data failed to load ('+e+')';});
