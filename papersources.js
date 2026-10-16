/* Paper-vs-metal: OI card + Sources block. Every number comes from
   data/latest.json -> paper_to_metal (written by scripts/compute_paper_to_metal.py).
   Same render code runs in the browser and at build time (node) for the static fallback. */
(function(root){
const esc=t=>String(t==null?'':t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const N=n=>n==null?'n/a':Math.round(n).toLocaleString('en-US');
const Moz=n=>n==null?'n/a':(n/1e6).toFixed(2)+'M oz';
const X=(n,dp)=>n==null?'n/a':n.toFixed(dp==null?2:dp);
const A=(u,t)=>u?'<a href="'+esc(u)+'" rel="noopener">'+esc(t)+'</a>':esc(t);
const D=iso=>{if(!iso)return 'n/a';const d=new Date(iso.slice(0,10)+'T12:00:00Z');return d.toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric',timeZone:'UTC'});};
const T=n=>n==null?'n/a':'$'+(n/1e12).toFixed(2)+' trillion';
function oiCard(p){const s=p.silver,g=p.gold;
 if(!s||s.ratio_vs_total==null)return '<h3>Paper futures vs vault silver</h3><p class="note">Open interest or vault totals unavailable in our data file, so no ratio is shown.</p>';
 return '<h3>Paper futures vs vault silver</h3><div class="pm-ratio">'+X(s.ratio_vs_total)+' to 1</div>'+
 '<p class="pm-oi-sub">'+Moz(s.paper_oz)+' of COMEX silver futures open interest vs '+Moz(s.total_oz)+' of total vault silver (registered + eligible).</p>'+
 '<p class="note">Secondary: '+X(s.ratio_vs_registered_secondary)+' to 1 vs registered silver only ('+Moz(s.registered_oz)+'). Gold: '+X(g&&g.ratio_vs_total)+' to 1 vs total vault gold. Vaults as of '+D(p.vault.report_date)+'; '+esc(p.open_interest.as_of_label)+'.</p>'+
 '<p class="calc-basis"><b>How this is calculated:</b> '+X(s.ratio_vs_total)+' to 1 = '+Moz(s.paper_oz)+' COMEX silver open interest ('+N(s.oi_contracts)+' contracts × '+N(s.oz_per_contract)+' oz; '+A(p.open_interest.source_url,'CME Daily Bulletin Sec. 02B')+', '+esc(p.open_interest.as_of_label)+') ÷ '+Moz(s.total_oz)+' total COMEX silver ('+N(s.registered_oz)+' registered + '+N(s.eligible_oz)+' eligible; CME Group warehouse report via The Vault Report, '+D(p.vault.report_date)+'). Secondary '+X(s.ratio_vs_registered_secondary)+' to 1 = '+Moz(s.paper_oz)+' ÷ '+Moz(s.registered_oz)+' registered.'+(g&&g.ratio_vs_total!=null?' Gold '+X(g.ratio_vs_total)+' to 1 = '+N(g.oi_contracts)+' contracts × '+N(g.oz_per_contract)+' oz = '+Moz(g.paper_oz)+' ÷ '+Moz(g.total_oz)+' total vault gold.':'')+'</p>'+
 '<p class="note">Most futures are closed or rolled before delivery, so this describes market structure, not unmet claims. Not a forecast.</p>';}
function sources(p){const s=p.silver||{},g=p.gold||{},o=p.open_interest||{},v=p.vault||{},m=p.money_supply||{},sp=p.spot||{};
 const vs=(v.sources||[]).reduce((a,x)=>(a[x.url]=x,a),{});
 const tvr='https://thevaultreport.com/comex',mcs='https://metalcharts.org/comex/silver',mcg='https://metalcharts.org/comex/gold',cme='https://www.cmegroup.com/clearing/operations-and-deliveries/nymex-delivery-notices.html';
 return '<h3>Sources</h3><ul class="pm-src-list">'+
 '<li><b>COMEX vault stocks</b> (report date '+D(v.report_date)+'): silver '+N(s.registered_oz)+' registered + '+N(s.eligible_oz)+' eligible = '+N(s.total_oz)+' oz total; gold '+N(g.total_oz)+' oz total. '+
  A(vs[tvr]?tvr:null,'The Vault Report')+', cross-checked with '+A(vs[mcs]?mcs:null,'MetalCharts silver')+' / '+A(vs[mcg]?mcg:null,'MetalCharts gold')+'. Original: '+A(vs[cme]?cme:null,'CME Group warehouse reports')+'.</li>'+
 '<li><b>Open interest</b>: silver '+N(s.oi_contracts)+' contracts × '+N(s.oz_per_contract)+' oz = '+N(s.paper_oz)+' oz; gold '+N(g.oi_contracts)+' × '+N(g.oz_per_contract)+' oz. '+A(o.source_url,'CME Daily Bulletin, Section 02B')+'; '+esc(o.as_of_label)+'.</li>'+
 '<li><b>Money supply &amp; gold reserve:</b> M2 '+T(m.m2_usd)+' ('+esc(m.m2_month)+', '+A(m.m2_source,'FRED M2SL')+'); M1 '+T(m.m1_usd)+' ('+esc(m.m1_month)+', '+A(m.m1_source,'FRED M1SL')+'); US gold reserve '+N(m.gold_reserve_oz)+' oz (as of '+D(m.gold_reserve_as_of)+', '+A(m.gold_reserve_source,'US Treasury')+').</li>'+
 '<li><b>Spot</b>: '+A(sp.source_url,sp.source||'gold-api.com')+', live in your browser (stored fallback as of '+esc((sp.as_of||'').replace('T',' ').slice(0,16))+' UTC; approximate spot, not COMEX settlement).</li></ul>'+
 '<p class="pm-formula"><b>Formula:</b> Paper oz = open interest contracts × 5,000 oz; ratio = paper oz ÷ total COMEX silver (registered + eligible). Implied price = M2 ÷ metal oz; paper to metal = implied price ÷ spot.</p>'+
 '<p class="note">Computed from <a href="/data/latest.json">latest.json</a> (paper_to_metal, updated '+esc((p.computed_at||'').slice(0,10))+'). Not financial advice or a prediction.</p>';}
const api={oiCard,sources};
if(typeof module!=='undefined'&&module.exports){module.exports=api;return;}
root.VPpaper=api;
fetch('/data/latest.json',{cache:'no-store'}).then(r=>r.json()).then(d=>{const p=d.paper_to_metal;if(!p)return;
 const a=document.getElementById('pm-oi'),b=document.getElementById('pm-sources');if(a)a.innerHTML=oiCard(p);if(b)b.innerHTML=sources(p);}).catch(()=>{});
})(this);
