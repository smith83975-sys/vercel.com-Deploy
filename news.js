(function(){const el=document.getElementById('news-list'),meta=document.getElementById('news-meta');
const x=t=>String(t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const ago=s=>{const m=Math.max(0,Math.round((Date.now()-new Date(s))/60000));if(m<1)return'just now';if(m<60)return m+' min ago';const h=Math.round(m/60);if(h<24)return h+' hr ago';const d=Math.round(h/24);return d+(d==1?' day ago':' days ago')};
let items=[];const draw=()=>{el.innerHTML=items.slice(0,10).map(i=>'<li><a href="'+x(i.link)+'" target="_blank" rel="noopener noreferrer">'+x(i.title)+'</a><span class="cite">'+x(i.source)+' · '+ago(i.published)+'</span></li>').join('')};
function load(){fetch('/api/news',{cache:'no-store'}).then(r=>{if(!r.ok)throw 0;return r.json()}).then(d=>{if(!d.items||!d.items.length)throw 0;items=d.items;draw();meta.textContent='Updated '+new Date(d.updated).toLocaleTimeString()+' · refreshes every 3 min'}).catch(()=>{if(!items.length)el.innerHTML='<li class="note">News unavailable right now. Try again shortly.</li>'})}
load();setInterval(load,180000);setInterval(()=>items.length&&draw(),60000)})();
