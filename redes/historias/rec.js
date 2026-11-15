const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file:///tmp/claude-0/historia2/anim.html');await p.evaluate(()=>document.fonts.ready);
await p.evaluate(()=>{render(0)});await p.waitForTimeout(500);
const N=+process.argv[2]||630;require('fs').mkdirSync('f',{recursive:true});
for(let i=0;i<N;i++){await p.evaluate(t=>render(t),i/30);await p.locator('canvas').screenshot({path:`f/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}
await b.close()})();
