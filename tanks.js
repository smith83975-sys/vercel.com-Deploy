fetch('data/tank.json').then(r=>r.json()).then(d=>{
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const M=n=>n>=1e6?(n/1e6).toFixed(2)+'M oz':Math.round(n).toLocaleString('en-US')+' oz';
  document.getElementById('tank-list').innerHTML=d.tanks.map(t=>{
    const del=t.mtd_contracts*t.oz_per_contract, reg=t.registered_oz;
    if(!reg) return `<div class="card tank-card"><h3>${esc(t.label)}</h3><p class="pending">Registered stock: data pending</p><p>Month-to-date deliveries: ${M(del)} (${t.mtd_contracts.toLocaleString('en-US')} contracts, as of ${esc(t.mtd_date)}).</p></div>`;
    const pct=del/reg*100, h=Math.max(pct,1.5);
    return `<div class="card tank-card"><h3>${esc(t.label)}</h3>
<div class="tank-wrap"><div class="tank ${esc(t.metal)}" role="img" aria-label="${esc(t.label)}: ${M(reg)} registered; month-to-date deliveries ${M(del)}, ${pct.toFixed(1)}% of registered">
<div class="fill"></div><div class="drain" style="height:${h.toFixed(1)}%"></div></div>
<ul class="tank-vals"><li><b>Registered:</b> ${t.registered_approx?'about ':''}${M(reg)}<br><span class="cite">as of ${esc(t.registered_date)}</span></li>
<li><b>Delivered MTD:</b> ${M(del)}<br><span class="cite">${t.mtd_contracts.toLocaleString('en-US')} × ${t.oz_per_contract.toLocaleString('en-US')} oz, as of ${esc(t.mtd_date)}</span></li></ul></div>
<p>October month-to-date deliveries equal about <b>${pct.toFixed(1)}%</b> of registered stock.</p>
<p class="calc-basis"><b>How this is calculated:</b> ${pct.toFixed(1)}% = ${M(del)} delivered (${t.mtd_contracts.toLocaleString('en-US')} contracts × ${t.oz_per_contract.toLocaleString('en-US')} oz, as of ${esc(t.mtd_date)}) ÷ ${M(reg)} registered (as of ${esc(t.registered_date)}, ${esc(t.registered_source)}).</p>
${t.mtd_note?`<p class="cite">${esc(t.mtd_note)}</p>`:''}
<p class="cite">Sources: <a href="${esc(t.registered_url)}" rel="nofollow">${esc(t.registered_source)}</a>; <a href="${esc(t.mtd_url)}" rel="nofollow">${esc(t.mtd_source)}</a>. Delivered metal often stays in COMEX vaults, so this is not a forecast of drawdown.</p></div>`;
  }).join('');
}).catch(()=>{document.getElementById('tank-list').innerHTML='<p class="pending">Tank data pending.</p>'});
