// Build-time static fallback: prints {"oi":html,"sources":html} using the same code as the browser.
const fs=require('fs'),path=require('path');const R=require(path.join(__dirname,'..','papersources.js'));
const p=JSON.parse(fs.readFileSync(path.join(__dirname,'..','data','latest.json'),'utf8')).paper_to_metal;
process.stdout.write(JSON.stringify({oi:R.oiCard(p),sources:R.sources(p)}));
