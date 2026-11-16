const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file:///tmp/claude-0/historia3/anim.html');await p.evaluate(async()=>{for(const f of ['BS','GM','GMB','IS','OU','OUB'])await document.fonts.load('40px '+f)});
await p.evaluate(l=>setLand(l),JSON.parse(fs.readFileSync('/tmp/claude-0/historia3/land.json')));
const info=await p.evaluate(()=>({T:TOTAL,V:VSTART}));fs.writeFileSync('timing.json',JSON.stringify(info));
fs.rmSync('f',{recursive:true,force:true});fs.mkdirSync('f');const N=Math.ceil(info.T*30);
for(let i=0;i<N;i++){await p.evaluate(t=>render(t),i/30);await p.locator('canvas').screenshot({path:`f/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:93});}
await b.close()})();
