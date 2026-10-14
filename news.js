(function(){const el=document.getElementById('news-list'),box=document.getElementById('news-box'),meta=document.getElementById('news-meta');
const x=t=>String(t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const ago=s=>{const m=Math.max(0,Math.round((Date.now()-new Date(s))/60000));if(m<1)return'just now';if(m<60)return m+' min ago';const h=Math.round(m/60);if(h<24)return h+' hr ago';const d=Math.round(h/24);return d+(d==1?' day ago':' days ago')};
const MAJOR=/force majeure|\bdefaults?\b|delivery failure|failed deliver|\bhalt(s|ed)?\b|suspend|margin (hike|raise|increase)|(hike|raise)s? margin|emergency|record high|all[- ]time high|\bcrash|plunge|\bsoar|\bsurge|squeeze|shortage/i;
const NOTE=/\bslip|\bfall|\bfell\b|\bdrop|\bjump|\brall(y|ies|ied)|\bcpi\b|\bfed\b|federal reserve|tariff|\bslump|\bspike|\btumble|\bdip|\bslid|\bdeclin|\bsell-off|\bsink/i;
const ico=t=>MAJOR.test(t)?'<span class="ico" title="Major event (keyword)">🚨</span>':NOTE.test(t)?'<span class="ico" title="Notable move (keyword)">⚠️</span>':'';
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;if(reduce)box.classList.add('static');
let items=[],seen=new Set(),first=true,fresh=new Set(),paused=false,pos=0;
const li=(i,dup)=>'<li '+(dup?'aria-hidden="true" ':'')+'class="'+(fresh.has(i.link)&&!dup?'fresh':'')+'"><a href="'+x(i.link)+'" target="_blank" rel="noopener noreferrer"'+(dup?' tabindex="-1"':'')+'>'+(fresh.has(i.link)?'<span class="tag-new">NEW</span>':'')+ico(i.title)+x(i.title)+'</a><span class="cite">'+x(i.source)+' · '+ago(i.published)+'</span></li>';
const draw=()=>{const l=items.slice(0,30);let h=l.map(i=>li(i)).join('');
 if(!reduce&&l.length)h+='<li class="sep" aria-hidden="true"></li>'+l.map(i=>li(i,1)).join('');el.innerHTML=h};
function load(){fetch('/api/news',{cache:'no-store'}).then(r=>{if(!r.ok)throw 0;return r.json()}).then(d=>{if(!d.items||!d.items.length)throw 0;
 const nw=d.items.filter(i=>!seen.has(i.link));if(!first&&nw.length){nw.forEach(i=>fresh.add(i.link));pos=0;setTimeout(()=>{nw.forEach(i=>fresh.delete(i.link));draw()},120000)}
 d.items.forEach(i=>seen.add(i.link));first=false;items=d.items;draw();meta.textContent='Updated '+new Date(d.updated).toLocaleTimeString()+' · checks every 75 s'})
 .catch(()=>{if(!items.length)el.innerHTML='<li class="note">News unavailable right now. Try again shortly.</li>'})}
['mouseenter','touchstart','focusin'].forEach(e=>box.addEventListener(e,()=>paused=true,{passive:true}));
['mouseleave','touchend','focusout'].forEach(e=>box.addEventListener(e,()=>paused=false,{passive:true}));
if(!reduce){let last=performance.now();const step=t=>{const dt=t-last;last=t;if(!paused&&items.length){pos+=Math.min(dt,100)*0.025;const sep=el.querySelector('.sep');const half=sep?sep.offsetTop:el.scrollHeight;if(half>0&&pos>=half)pos-=half;el.style.transform='translateY('+(-pos)+'px)'}requestAnimationFrame(step)};requestAnimationFrame(step)}
load();setInterval(load,75000);setInterval(()=>items.length&&draw(),60000)})();
