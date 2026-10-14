(function(){
function svg(metal,ratio,per,date){
const a=14*Math.PI/180,L=110,cx=200,cy=40; // beam tilts down on the right (paper)
const lx=cx-L*Math.cos(a),ly=cy-L*Math.sin(a),rx=cx+L*Math.cos(a),ry=cy+L*Math.sin(a);
const n=Math.round(ratio),full=Math.floor(n/per),rem=n%per;
const items=[];for(let i=0;i<full;i++)items.push(per);if(rem)items.push(rem);
let bills='';const cols=Math.min(6,items.length),bw=15,bh=7;
items.forEach((v,i)=>{const col=i%cols,row=Math.floor(i/cols);const x=rx-cols*bw/2+col*bw,y=ry+76-row*(bh+1);
const w=v===per?bw-2:Math.max(4,(bw-2)*v/per);
bills+='<rect x="'+x.toFixed(1)+'" y="'+y.toFixed(1)+'" width="'+w.toFixed(1)+'" height="'+bh+'" rx="1" fill="#5f9a5a" stroke="#2f5a2c" stroke-width=".6"/>'+(v===per?'<rect x="'+(x+5).toFixed(1)+'" y="'+y.toFixed(1)+'" width="3" height="'+bh+'" fill="#e8e2c8"/>':'');});
const gold=metal==='gold';
const obj=gold?'<rect x="'+(lx-18)+'" y="'+(ly+64)+'" width="36" height="16" rx="3" fill="#d4af37" stroke="#9c7d1c"/>':'<circle cx="'+lx+'" cy="'+(ly+72)+'" r="9" fill="#c0c6cf" stroke="#7d848e"/>';
const pan=(x,y,w)=>'<line x1="'+x+'" y1="'+y+'" x2="'+(x-w/2)+'" y2="'+(y+82)+'" stroke="#8a909a"/><line x1="'+x+'" y1="'+y+'" x2="'+(x+w/2)+'" y2="'+(y+82)+'" stroke="#8a909a"/><path d="M'+(x-w/2-5)+' '+(y+82)+' h'+(w+10)+' q-5 10 -'+(w/2+5)+' 10 q-'+(w/2)+' 0 -'+(w/2+5)+' -10z" fill="#3a3f49"/>';
const r2=ratio.toFixed(2);
return '<svg viewBox="0 0 400 230" width="100%" aria-hidden="true" focusable="false">'+
'<polygon points="185,215 215,215 204,40 196,40" fill="#555b66"/><rect x="160" y="213" width="80" height="6" rx="3" fill="#555b66"/>'+
'<line x1="'+lx.toFixed(1)+'" y1="'+ly.toFixed(1)+'" x2="'+rx.toFixed(1)+'" y2="'+ry.toFixed(1)+'" stroke="#8a909a" stroke-width="5" stroke-linecap="round"/><circle cx="200" cy="40" r="7" fill="#d4af37"/>'+
pan(lx.toFixed(1)*1,ly,70)+pan(rx.toFixed(1)*1,ry,110)+obj+bills+
'<text x="'+lx.toFixed(0)+'" y="'+(ly+112).toFixed(0)+'" font-size="12" text-anchor="middle" fill="'+(gold?'#d4af37':'#c0c6cf')+'" font-weight="700">$1 of '+metal+'</text>'+
'<text x="'+rx.toFixed(0)+'" y="'+(ry+112).toFixed(0)+'" font-size="12" text-anchor="middle" fill="#7fbf7a" font-weight="700">$'+r2+' of paper</text>'+
'<text x="'+rx.toFixed(0)+'" y="'+(ry+126).toFixed(0)+'" font-size="9" text-anchor="middle" fill="#999">each bundle = $'+per+'</text></svg>'+
'<p class="note" style="text-align:center"><strong>$1 of '+metal+' : $'+r2+' of paper</strong> · US Debt Clock snapshot, '+date+'</p>';}
function draw(d){const dc=d&&d.debt_clock;const box=document.getElementById('debt-scales');if(!box||!dc)return;
const L=window.VP_LIVE_PAPER;const live=!!L;const date=live?'live, our calculation':'US Debt Clock snapshot, '+new Date(dc.retrieved_at).toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric',timeZone:'UTC'});
const mk=(metal,r,per)=>{if(!(r>0))return '';return '<div class="card debt-scale" role="img" aria-label="Balance scale tipped heavily toward paper: $1 of '+metal+' against $'+r.toFixed(2)+' of paper money, per '+date+'. Illustration only, not financial advice."><h3>Paper vs '+metal+'</h3>'+svg(metal,r,per,date)+'</div>';};
box.innerHTML=live?mk('gold',L.gold,2)+mk('silver',L.silver,100):mk('gold',dc.paper_to_gold_ratio,10)+mk('silver',dc.paper_to_silver_ratio,50);}
let D=null;fetch('data/latest.json',{cache:'no-store'}).then(r=>r.json()).then(d=>{D=d;draw(d)}).catch(()=>{});document.addEventListener('vp-live-paper',()=>{if(D)draw(D)});
})();
