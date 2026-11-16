const {chromium}=require('playwright');
const BP=[[0,0],[6.4,3.4],[10.0,7.4],[16.4,11.8],[19.15,12.8],[21.3,15.8],[29.6,21]];
function m(r){for(let i=1;i<BP.length;i++){if(r<=BP[i][0]){const[a0,b0]=BP[i-1],[a1,b1]=BP[i];return b0+(b1-b0)*(r-a0)/(a1-a0)}}return 21}
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file:///tmp/claude-0/historia2/anim.html');await p.evaluate(()=>document.fonts.ready);await p.evaluate(()=>render(0));await p.waitForTimeout(500);
require('fs').rmSync('f3',{recursive:true,force:true});require('fs').mkdirSync('f3');
const N=Math.round(29.6*30);for(let i=0;i<N;i++){await p.evaluate(t=>render(t),m(i/30));await p.locator('canvas').screenshot({path:`f3/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}
await b.close()})();
