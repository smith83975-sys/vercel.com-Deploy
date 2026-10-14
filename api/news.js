const FEEDS=[
 {url:'https://news.google.com/rss/search?q=%22gold+price%22+OR+%22silver+price%22+OR+COMEX&hl=en-US&gl=US&ceid=US:en',name:'Google News',gn:true},
 {url:'https://news.google.com/rss/search?q=silver+market+OR+gold+market+when:2d&hl=en-US&gl=US&ceid=US:en',name:'Google News',gn:true},
 {url:'https://www.investing.com/rss/news_11.rss',name:'Investing.com',filter:true},
 {url:'https://www.fxstreet.com/rss/news',name:'FXStreet',filter:true}
];
const KW=/\b(gold|silver|bullion|precious metal|comex|xau|xag)\b/i;
const dec=s=>String(s||'').replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g,'$1').replace(/<[^>]+>/g,'').replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#39;|&apos;/g,"'").replace(/&#(\d+);/g,(m,n)=>String.fromCharCode(n)).trim();
const tag=(x,t)=>{const m=x.match(new RegExp('<'+t+'[^>]*>([\\s\\S]*?)</'+t+'>','i'));return m?dec(m[1]):''};
async function get(f){
 const ctl=new AbortController();const to=setTimeout(()=>ctl.abort(),6000);
 try{const r=await fetch(f.url,{headers:{'User-Agent':'Mozilla/5.0 VaultPulse news'},signal:ctl.signal});if(!r.ok)return[];
  const x=await r.text();return (x.match(/<item[\s\S]*?<\/item>/gi)||[]).map(it=>{
   let title=tag(it,'title'),source=f.name;const s=tag(it,'source');
   if(f.gn){if(s)source=s;const i=title.lastIndexOf(' - ');if(i>0&&(!s||title.endsWith(s)))title=title.slice(0,i)}
   let d=new Date(tag(it,'pubDate'));if(d>Date.now())d=new Date();return{title,source,link:tag(it,'link'),published:isNaN(d)?null:d.toISOString()}
  }).filter(i=>i.title&&/^https?:/.test(i.link)&&i.published&&KW.test(i.title))}
 catch(e){return[]}finally{clearTimeout(to)}}
module.exports=async(req,res)=>{
 const all=(await Promise.all(FEEDS.map(get))).flat();const seen=new Set(),out=[];
 all.sort((a,b)=>b.published.localeCompare(a.published));
 for(const i of all){const k=i.title.toLowerCase().replace(/[^a-z0-9]/g,'').slice(0,60);if(seen.has(k)||seen.has(i.link))continue;seen.add(k);seen.add(i.link);out.push(i);if(out.length>=30)break}
 res.setHeader('Content-Type','application/json; charset=utf-8');
 res.setHeader('Cache-Control',out.length?'public, s-maxage=300, stale-while-revalidate=600':'no-store');
 res.status(out.length?200:502).send(JSON.stringify({updated:new Date().toISOString(),count:out.length,items:out}));
};
