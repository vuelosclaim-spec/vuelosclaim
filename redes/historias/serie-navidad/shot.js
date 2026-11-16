const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [v,mode,...ts]=process.argv.slice(2);const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto(`file:///tmp/claude-0/vids/${v}.html`);await p.evaluate(async()=>{for(const f of ['BS','GM','GMB','IS','OU','OUB'])await document.fonts.load('40px '+f)});
const info=await p.evaluate(()=>({T:TOTAL,V:VSTART}));fs.writeFileSync(`${v}.timing.json`,JSON.stringify(info));
if(mode==='all'){fs.rmSync(`f_${v}`,{recursive:true,force:true});fs.mkdirSync(`f_${v}`);const N=Math.ceil(info.T*30);for(let i=0;i<N;i++){await p.evaluate(t=>render(t),i/30);await p.locator('canvas').screenshot({path:`f_${v}/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92})}}
else{let i=0;const tt=ts.length?ts.map(Number):info.V.map((s,k)=>(info.V[k+1]??info.T)-0.4);for(const t of tt){await p.evaluate(t=>render(t),t);await p.locator('canvas').screenshot({path:`p_${v}_${i++}.png`})}}
console.log(v,JSON.stringify(info),errs.join('|'));await b.close()})();
