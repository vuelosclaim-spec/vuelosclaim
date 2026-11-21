const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [mode,...ts]=process.argv.slice(2);const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///tmp/claude-0/v2/v.html');await p.evaluate(async()=>{for(const w of ['700','800','900'])await document.fonts.load(w+' 40px Inter')});
const T=await p.evaluate(()=>window.TOTAL);
if(mode==='all'){fs.rmSync('f',{recursive:true,force:true});fs.mkdirSync('f');const N=Math.ceil(T*30);for(let i=0;i<N;i++){await p.evaluate(t=>render(t),i/30);await p.locator('canvas').screenshot({path:`f/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:90})}}
else{let i=0;for(const t of ts){await p.evaluate(t=>render(+t),t);await p.locator('canvas').screenshot({path:`p_${i++}.png`})}}
console.log(T,errs.join('|'));await b.close()})();
