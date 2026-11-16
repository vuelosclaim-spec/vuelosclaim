
const c=document.getElementById('c'),x=c.getContext('2d'),W=1080,H=1920;
const K={bg:'#0A0F1E',bg2:'#0E1630',bone:'#F2EDE4',amber:'#F5B700',red:'#E5484D',green:'#3DD68C',mut:'#8A93A8',line:'rgba(242,237,228,0.05)'};
// voice durations -> scene timeline
const PRE=0.2;let S=[];function timeline(VD,POST){S=[];let acc=0;VD.forEach((d,i)=>{S.push({a:acc,v:acc+PRE,b:acc+PRE+d+(POST[i]??0.35)});acc=S[i].b});window.TOTAL=acc;window.VSTART=S.map(s=>s.v);window.S=S}
let LAND=[];window.setLand=l=>LAND=l;
const cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),eo=t=>1-Math.pow(1-cl(t),3),eio=t=>{t=cl(t);return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2},
eb=t=>{t=cl(t);const s=1.6;return 1+(s+1)*Math.pow(t-1,3)+s*Math.pow(t-1,2)},lerp=(a,b,t)=>a+(b-a)*t;
function R(i){const s=Math.sin(i*127.1+311.7)*43758.5453;return s-Math.floor(s)}
function T(s,X,Y,f,sz,col,o={}){x.save();x.globalAlpha*=(o.a??1);x.font=`${sz}px ${f}`;x.fillStyle=col;x.textAlign=o.al||'center';x.textBaseline=o.bl||'middle';if(o.ls)x.letterSpacing=o.ls+'px';x.fillText(s,X,Y);x.restore()}
function rr(X,Y,w,h,r){x.beginPath();x.roundRect(X,Y,w,h,r)}
// ---------- background
const grain=document.createElement('canvas');grain.width=540;grain.height=960;{const g=grain.getContext('2d'),id=g.createImageData(540,960);for(let i=0;i<id.data.length;i+=4){const v=Math.random()*255;id.data[i]=id.data[i+1]=id.data[i+2]=v;id.data[i+3]=14}g.putImageData(id,0,0)}
function bg(t){const g=x.createRadialGradient(W/2,H*0.38,100,W/2,H*0.5,1300);g.addColorStop(0,K.bg2);g.addColorStop(1,K.bg);x.fillStyle=g;x.fillRect(0,0,W,H);
 x.strokeStyle=K.line;x.lineWidth=1;for(let gx=60;gx<W;gx+=60){x.beginPath();x.moveTo(gx+.5,0);x.lineTo(gx+.5,H);x.stroke()}for(let gy=60;gy<H;gy+=60){x.beginPath();x.moveTo(0,gy+.5);x.lineTo(W,gy+.5);x.stroke()}}
function chrome(t,si){T('VUELOSCLAIM',60,92,'GMB',26,K.bone,{al:'left',ls:4});T('CASO HIPOTÉTICO',60,128,'GM',22,K.mut,{al:'left',ls:3});
 T(String(si+1).padStart(2,'0')+' / '+String(S.length).padStart(2,'0'),W-60,92,'GM',26,K.amber,{al:'right',ls:3});
 x.fillStyle='rgba(242,237,228,.15)';x.fillRect(60,160,W-120,2);x.fillStyle=K.amber;x.fillRect(60,160,(W-120)*cl(t/TOTAL),2);
 const p=1+0.025*Math.sin(t*4.5);x.save();x.translate(W/2,1700);x.scale(p,p);rr(-235,-46,470,92,46);x.fillStyle=K.amber;x.fill();T('Enlace en la bio  ↑',0,3,'OUB',44,'#141414');x.restore();
 T('REGLAMENTO (CE) 261/2004',W/2,1812,'GM',22,K.mut,{ls:4})}
// ---------- objects
const AL=' ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
function flap(str,X,Y,cw,ch,p,col,seed){for(let i=0;i<str.length;i++){const st=cl(p*1.0-i*0.05);let ch_=str[i];if(st<1&&str[i]!==' ')ch_=AL[1+Math.floor(R(i+seed+Math.floor(p*40))*36)];
 const xx=X+i*(cw+5);rr(xx,Y,cw,ch,6);x.fillStyle='#05080F';x.fill();x.fillStyle='rgba(255,255,255,.07)';x.fillRect(xx,Y+ch/2-1,cw,2);
 T(ch_,xx+cw/2,Y+ch/2+3,'GMB',ch*0.66,st<1?'#B9C0CF':col)}}
function figure(X,Y,s,i,slump,t){x.save();x.translate(X,Y);const sl=slump;x.rotate((i%2?1:-1)*0.06*sl);
 x.fillStyle=K.bone;x.beginPath();x.arc(0,-s*1.62+sl*s*0.18,s*0.36,0,7);x.fill();rr(-s*0.42,-s*1.12+sl*s*0.12,s*0.84,s*1.12-sl*s*0.12,s*0.3);x.fill();
 if(i==0||i==1){x.fillStyle=K.amber;rr(s*0.55,-s*0.62,s*0.5,s*0.62,8);x.fill();x.fillStyle='#0A0F1E';x.fillRect(s*0.72,-s*0.74,s*0.16,s*0.12)}x.restore()}
function plane(X,Y,a,s,col){x.save();x.translate(X,Y);x.rotate(a);x.fillStyle=col||K.bone;x.beginPath();
 x.moveTo(s,0);x.quadraticCurveTo(s*0.9,-s*0.1,s*0.6,-s*0.1);x.lineTo(-s*0.85,-s*0.08);x.lineTo(-s,-s*0.42);x.lineTo(-s*1.08,-s*0.42);x.lineTo(-s*0.98,-s*0.05);x.lineTo(-s*0.98,s*0.05);x.lineTo(-s*1.08,s*0.42);x.lineTo(-s,s*0.42);x.lineTo(-s*0.85,s*0.08);x.lineTo(s*0.6,s*0.1);x.quadraticCurveTo(s*0.9,s*0.1,s,0);x.fill();
 x.beginPath();x.moveTo(s*0.25,-s*0.06);x.lineTo(-s*0.2,-s*0.95);x.lineTo(-s*0.38,-s*0.95);x.lineTo(-s*0.18,-s*0.06);x.closePath();x.fill();x.beginPath();x.moveTo(s*0.25,s*0.06);x.lineTo(-s*0.2,s*0.95);x.lineTo(-s*0.38,s*0.95);x.lineTo(-s*0.18,s*0.06);x.closePath();x.fill();x.restore()}
function coin(X,Y,r,rot,a){x.save();x.globalAlpha*=a;x.translate(X,Y);x.scale(Math.abs(Math.cos(rot))*0.85+0.15,1);x.fillStyle=K.amber;x.beginPath();x.arc(0,0,r,0,7);x.fill();x.strokeStyle='#B98900';x.lineWidth=5;x.beginPath();x.arc(0,0,r*0.78,0,7);x.stroke();T('€',0,3,'OUB',r*1.05,'#7A5A00');x.restore()}
function star(X,Y,r,col){x.fillStyle=col;x.beginPath();for(let i=0;i<10;i++){const a=i*Math.PI/5-Math.PI/2,q=i%2?r*0.42:r;x.lineTo(X+Math.cos(a)*q,Y+Math.sin(a)*q)}x.closePath();x.fill()}
function icon(kind,X,Y,s,a,col){x.save();x.globalAlpha*=a;x.translate(X,Y);x.strokeStyle=col;x.fillStyle=col;x.lineWidth=8;x.lineCap='round';x.lineJoin='round';
 if(kind==0){rr(-s*0.45,-s*0.35,s*0.7,s*0.8,10);x.stroke();x.beginPath();x.arc(s*0.32,s*0.05,s*0.2,-1.3,1.3);x.stroke();for(let i=0;i<3;i++){x.beginPath();x.moveTo(-s*0.3+i*s*0.2,-s*0.55);x.quadraticCurveTo(-s*0.2+i*s*0.2,-s*0.7,-s*0.3+i*s*0.2,-s*0.85);x.stroke()}}
 if(kind==1){x.beginPath();x.arc(0,0,s*0.5,0,7);x.stroke();x.beginPath();x.arc(0,0,s*0.3,0,7);x.stroke();x.beginPath();x.moveTo(-s*0.85,-s*0.5);x.lineTo(-s*0.85,s*0.55);x.stroke();x.beginPath();x.moveTo(s*0.85,-s*0.5);x.lineTo(s*0.85,s*0.55);x.stroke()}
 if(kind==2){x.beginPath();x.moveTo(-s*0.8,s*0.45);x.lineTo(-s*0.8,-s*0.5);x.stroke();x.beginPath();x.moveTo(-s*0.8,s*0.1);x.lineTo(s*0.8,s*0.1);x.lineTo(s*0.8,s*0.45);x.stroke();rr(-s*0.6,-s*0.25,s*0.4,s*0.3,10);x.fill();x.beginPath();x.moveTo(-s*0.1,-s*0.15);x.lineTo(s*0.75,-s*0.15);x.quadraticCurveTo(s*0.8,s*0.05,s*0.6,s*0.08);x.lineTo(-s*0.1,s*0.08);x.closePath();x.stroke()}
 x.restore()}
function sceneAlpha(t,i){const s=S[i];return cl((t-s.a)/0.28)*cl((s.b-t)/0.28)+(i==7?cl((t-s.a)/0.28)*(t>s.b-0.28?1:0):0)}

function run(SC){window.render=function(t){bg(t);let si=0;for(let i=0;i<S.length;i++){if(t>=S[i].a)si=i}
 for(let i=0;i<S.length;i++){const s=S[i];if(t<s.a-0.01||t>s.b+0.3)continue;let a=cl((t-s.a)/0.3);if(i<S.length-1)a*=cl((s.b-t)/0.3);if(a<=0)continue;x.save();x.globalAlpha=a;x.translate(0,(1-cl((t-s.a)/0.3))*40);SC[i](t-s.a,t,s.b-s.a);x.restore()}
 chrome(t,si);x.globalAlpha=1;x.drawImage(grain,(Math.floor(t*30)%7)*-20,(Math.floor(t*30)%5)*-20,W+140,H+100)}}
function big2(a,b,y,c1,c2,sz,p){x.save();x.translate(W/2,y);x.scale(p,p);T(a,0,-sz*0.48,'BS',sz,c1);T(b,0,sz*0.48,'BS',sz,c2);x.restore()}
