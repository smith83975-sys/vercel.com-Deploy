// Build-time static fallback for the resource-backing card (same code as the browser).
const fs=require('fs'),path=require('path');const R=require(path.join(__dirname,'..','resbacking.js'));
const rb=JSON.parse(fs.readFileSync(path.join(__dirname,'..','data','latest.json'),'utf8')).resource_backing;
process.stdout.write(R.render(rb));
