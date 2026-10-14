fetch('data/entries.json').then(r=>r.json()).then(d=>{
  const es=[...d.entries].sort((a,b)=>b.data_date.localeCompare(a.data_date));
  const newest=new Date(es[0].data_date), cut=(d.archive_after_days||10)*864e5;
  const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const card=e=>`<article class="entry" id="${esc(e.id)}"><span class="tag ${esc(e.metal)}">${esc(e.metal)}</span><span class="tag">${esc(e.type)}</span>
<h3>${esc(e.headline)}</h3><p><b>What moved:</b> ${esc(e.moved)}</p><p><b>Roughly how much:</b> ${esc(e.amount)}</p><p><b>Context:</b> ${esc(e.context)}</p>
<p class="cite">Data date: ${esc(e.data_date)} · Source: <a href="${esc(e.source_url)}" rel="nofollow">${esc(e.source)}</a></p></article>`;
  const live=es.filter(e=>newest-new Date(e.data_date)<=cut), old=es.filter(e=>newest-new Date(e.data_date)>cut);
  document.getElementById('latest-list').innerHTML=live.map(card).join('');
  document.getElementById('archive-list').innerHTML=old.length?old.map(card).join(''):'<p class="note">Nothing archived yet.</p>';
  const u=document.getElementById('upd');if(u)u.textContent='Last updated '+d.updated+'.';
}).catch(()=>{document.getElementById('latest-list').innerHTML='<p class="pending">Could not load entries.</p>'});
