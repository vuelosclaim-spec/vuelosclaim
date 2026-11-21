const c=document.getElementById('c'),x=c.getContext('2d'),W=1080,H=1920;
const TM=window.TIMING,TOTAL=TM.total;window.TOTAL=TOTAL;
const OL='#1E2A33',SKIN='#F1C79C',CREAM='#F3E3C3',YEL='#F7D046',RED='#D64541',GRN='#0d6b3b';
const cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),eo=t=>1-Math.pow(1-cl(t),3),lerp=(a,b,t)=>a+(b-a)*t;
const eb=t=>{t=cl(t);const s=1.7;return 1+(s+1)*Math.pow(t-1,3)+s*Math.pow(t-1,2)};
function R(i){const s=Math.sin(i*127.1+311.7)*43758.5453;return s-Math.floor(s)}
function rr(X,Y,w,h,r){x.beginPath();x.roundRect(X,Y,w,h,r)}
function shape(fill,lw=4){x.fillStyle=fill;x.fill();x.strokeStyle=OL;x.lineWidth=lw;x.stroke()}
function box(X,Y,w,h,fill,r=6,lw=4){rr(X,Y,w,h,r);shape(fill,lw)}
function T(s,X,Y,f,col,o={}){x.save();x.globalAlpha*=(o.a??1);x.font=f;x.textAlign=o.al||'center';x.textBaseline='middle';if(o.ls)x.letterSpacing=o.ls+'px';
 if(o.sh){x.fillStyle='rgba(0,0,0,.45)';x.fillText(s,X+o.sh,Y+o.sh)}if(o.st){x.lineJoin='round';x.strokeStyle=o.stc||'#000';x.lineWidth=o.st;x.strokeText(s,X,Y)}x.fillStyle=col;x.fillText(s,X,Y);x.restore()}
// ---------- personaje
function person(X,Y,s,o={}){const t=o.t||0;x.save();x.translate(X,Y);x.scale(s*(o.flip?-1:1),s);
 const ph=o.walk?Math.sin(t*9):0,bob=o.walk?Math.abs(Math.sin(t*9))*6:Math.sin(t*2.2+(o.seed||0))*2,jump=o.jump?Math.abs(Math.sin(t*7))*30:0;x.translate(0,-bob-jump);
 x.fillStyle='rgba(0,0,0,.18)';x.beginPath();x.ellipse(6,6+bob+jump,85,15,0,0,7);x.fill();
 x.lineCap='round';x.strokeStyle=OL;x.lineWidth=7;
 x.beginPath();x.moveTo(-14,-105);x.lineTo(-14+ph*22,0);x.stroke();x.beginPath();x.moveTo(14,-105);x.lineTo(14-ph*22,0);x.stroke();
 x.fillStyle=OL;x.beginPath();x.ellipse(-14+ph*22+8,0,16,7,0,0,7);x.fill();x.beginPath();x.ellipse(14-ph*22+8,0,16,7,0,0,7);x.fill();
 // brazos
 const aL=o.aL??(o.walk?0.25+ph*0.35:0.18),aR=o.aR??(o.walk?-0.25-ph*0.35:-0.18);x.lineWidth=7;
 x.beginPath();x.moveTo(-38,-205);x.lineTo(-38+Math.sin(aL)*-95,-205+Math.cos(aL)*95);x.stroke();
 x.beginPath();x.moveTo(38,-205);const hx=38+Math.sin(-aR)*95,hy=-205+Math.cos(aR)*95;x.lineTo(hx,hy);x.stroke();window._hand=[hx,hy];
 // cuerpo
 rr(-46,-228,92,130,28);shape(o.c||'#3E6FA0',5);if(o.zip){x.strokeStyle='rgba(0,0,0,.25)';x.lineWidth=3;x.beginPath();x.moveTo(0,-220);x.lineTo(0,-105);x.stroke()}
 if(o.scarf){rr(-40,-236,80,22,10);shape(o.scarf,4)}
 // cabeza
 const hy0=-292;if(o.hair=='long'){rr(-58,hy0-40,116,110,40);shape(o.hc||'#3B2418',5)}
 x.beginPath();x.arc(0,hy0,56,0,7);shape(o.skin||SKIN,5);
 x.save();x.beginPath();x.arc(0,hy0,56,0,7);x.clip();x.fillStyle=o.hc||'#3B2418';x.beginPath();x.ellipse(o.hair=='bald'?0:6,hy0-46,66,34,o.hair=='long'?-0.15:0.1,0,7);if(o.hair!='bald')x.fill();x.restore();
 if(o.hair!='bald'){x.strokeStyle=OL;x.lineWidth=5;x.beginPath();x.arc(0,hy0,56,Math.PI*1.08,Math.PI*1.92);x.stroke()}
 if(o.hat){x.fillStyle=o.hat;rr(-46,hy0-78,92,26,8);shape(o.hat,4);rr(-56,hy0-56,112,12,6);shape(o.hat,4)}
 // ojos
 const blink=((t+(o.seed||0))%3.4)<0.12;const ey=hy0-4;
 if(o.eyes=='wide'&&!blink){for(const ex of[-19,19]){x.beginPath();x.arc(ex,ey,13,0,7);shape('#fff',3);x.fillStyle=OL;x.beginPath();x.arc(ex+2,ey+2,5,0,7);x.fill()}}
 else if(blink){x.strokeStyle=OL;x.lineWidth=4;for(const ex of[-19,19]){x.beginPath();x.moveTo(ex-8,ey);x.lineTo(ex+8,ey);x.stroke()}}
 else{for(const ex of[-19,19]){x.fillStyle=OL;x.beginPath();x.arc(ex,ey+2,5.5,0,7);x.fill();x.strokeStyle=OL;x.lineWidth=4;x.beginPath();x.moveTo(ex-10,ey-6);x.lineTo(ex+9,ey-5);x.stroke()}}
 if(o.brow=='sad'){x.lineWidth=4;x.beginPath();x.moveTo(-28,ey-14);x.lineTo(-12,ey-20);x.moveTo(28,ey-14);x.lineTo(12,ey-20);x.stroke()}
 // boca
 x.strokeStyle=OL;x.lineWidth=4;const my=hy0+26;
 if(o.mouth=='o'){x.beginPath();x.ellipse(0,my,9,12+Math.sin(t*12)*2,0,0,7);shape('#7A2E2E',3)}
 else if(o.mouth=='smile'){x.beginPath();x.arc(0,my-8,16,0.2,Math.PI-0.2);x.stroke()}
 else if(o.mouth=='talk'){x.beginPath();x.ellipse(0,my,10,3+Math.abs(Math.sin(t*14))*7,0,0,7);shape('#7A2E2E',3)}
 else if(o.mouth=='sad'){x.beginPath();x.arc(0,my+10,13,Math.PI+0.3,-0.3);x.stroke()}
 else{x.beginPath();x.moveTo(-10,my);x.lineTo(10,my);x.stroke()}
 x.restore()}
// ---------- escenarios
function floor(top,col1,col2){const g=x.createLinearGradient(0,top,0,H);g.addColorStop(0,col1);g.addColorStop(1,col2);x.fillStyle=g;x.fillRect(0,top,W,H-top);
 x.strokeStyle='rgba(30,42,51,.25)';x.lineWidth=2;for(let i=-6;i<=6;i++){x.beginPath();x.moveTo(W/2+i*60,top);x.lineTo(W/2+i*420,H);x.stroke()}
 for(let k=1;k<7;k++){const y=top+Math.pow(k/7,1.8)*(H-top);x.beginPath();x.moveTo(0,y);x.lineTo(W,y);x.stroke()}
 x.strokeStyle=OL;x.lineWidth=5;x.beginPath();x.moveTo(0,top);x.lineTo(W,top);x.stroke()}
function wall(top,bot,col){x.fillStyle=col;x.fillRect(0,top,W,bot-top);const g=x.createLinearGradient(0,0,0,430);g.addColorStop(0,'#1B2731');g.addColorStop(1,'#34454F');x.fillStyle=g;x.fillRect(0,0,W,430);x.fillStyle='#1E2A33';x.fillRect(0,426,W,8);for(const lx of[180,540,900]){x.fillStyle='rgba(255,244,214,.9)';rr(lx-70,404,140,14,7);x.fill()}}
function garland(y,t){x.strokeStyle='#2E6B45';x.lineWidth=12;x.beginPath();for(let i=0;i<=4;i++){const X=i*270;if(i==0)x.moveTo(X,y);else x.quadraticCurveTo(X-135,y+60,X,y)}x.stroke();
 for(let i=0;i<16;i++){const X=i*70+20,yy=y+Math.sin((X%270)/270*Math.PI)*45;const on=Math.floor(t*3+i)%3==0;x.fillStyle=['#E5484D','#F7D046','#4FA3E0'][i%3];x.globalAlpha=on?1:0.55;x.beginPath();x.arc(X,yy+8,8,0,7);x.fill()}x.globalAlpha=1}
function tree(X,Y,s,t){x.save();x.translate(X,Y);x.scale(s,s);box(-18,-40,36,40,'#7A4E2C',4);for(let k=0;k<3;k++){x.beginPath();x.moveTo(0,-300+k*80);x.lineTo(-110+k*-15,-40-((2-k)*80));x.lineTo(110+k*15,-40-((2-k)*80));x.closePath();shape('#2F7A4E',5)}
 for(let i=0;i<9;i++){const on=Math.floor(t*2.5+i)%2;x.fillStyle=['#E5484D','#F7D046','#4FA3E0'][i%3];x.globalAlpha=on?1:0.5;x.beginPath();x.arc((R(i)-0.5)*150,-80-R(i+4)*190,10,0,7);x.fill()}x.globalAlpha=1;
 star(0,-305,26,YEL);x.restore()}
function star(X,Y,r,col){x.beginPath();for(let i=0;i<10;i++){const a=i*Math.PI/5-Math.PI/2,q=i%2?r*0.45:r;x.lineTo(X+Math.cos(a)*q,Y+Math.sin(a)*q)}x.closePath();shape(col,3)}
function suitcase(X,Y,s,col){x.save();x.translate(X,Y);x.scale(s,s);x.strokeStyle=OL;x.lineWidth=6;x.beginPath();x.moveTo(-20,-150);x.lineTo(-20,-200);x.lineTo(20,-200);x.lineTo(20,-150);x.stroke();box(-55,-150,110,150,col||'#4F8A8B',14,5);x.strokeStyle='rgba(0,0,0,.25)';x.lineWidth=4;x.beginPath();x.moveTo(-25,-140);x.lineTo(-25,-10);x.moveTo(25,-140);x.lineTo(25,-10);x.stroke();x.restore()}
function gift(X,Y,s){x.save();x.translate(X,Y);x.scale(s,s);box(-40,-70,80,70,'#D64541',6,4);x.fillStyle=YEL;x.fillRect(-8,-70,16,70);x.fillRect(-40,-42,80,14);x.strokeStyle=OL;x.lineWidth=3;x.strokeRect(-40,-70,80,70);x.beginPath();x.ellipse(-14,-80,14,9,-0.4,0,7);x.ellipse(14,-80,14,9,0.4,0,7);shape(YEL,3);x.restore()}
function windowSky(X,Y,w,h,t,plane){box(X,Y,w,h,'#9CC9E3',4,6);x.save();rr(X,Y,w,h,4);x.clip();x.fillStyle='#fff';for(let i=0;i<3;i++){const cx=X+((i*170+t*14)%(w+120))-60,cy=Y+40+i*35;x.beginPath();x.arc(cx,cy,18,0,7);x.arc(cx+22,cy-8,22,0,7);x.arc(cx+46,cy,18,0,7);x.fill()}
 if(plane){const px=X+((t*60)%(w+200))-100;x.fillStyle='#fff';x.strokeStyle=OL;x.lineWidth=3;x.beginPath();x.ellipse(px,Y+h*0.62,45,9,-0.15,0,7);x.fill();x.stroke();x.beginPath();x.moveTo(px-5,Y+h*0.62);x.lineTo(px-25,Y+h*0.62+22);x.lineTo(px+8,Y+h*0.62);x.fill();x.stroke()}x.restore();
 x.strokeStyle=OL;x.lineWidth=6;x.beginPath();x.moveTo(X+w/2,Y);x.lineTo(X+w/2,Y+h);x.stroke()}
function board(X,Y,w,t,cancel){box(X,Y,w,300,'#13202B',10,6);T('SALIDAS · DEPARTURES',X+w/2,Y+38,'900 26px Inter',YEL,{ls:4});
 const rows=[['10:15','PARÍS','EN HORA',0],['10:40','ROMA',cancel?'CANCELADO':'EN HORA',1],['11:05','LONDRES','EMBARQUE',0]];
 rows.forEach((r,i)=>{const y=Y+100+i*72;x.fillStyle=i==1&&cancel?'rgba(214,69,65,.18)':'rgba(255,255,255,.05)';x.fillRect(X+20,y-28,w-40,58);
  T(r[0],X+40,y,'700 34px Inter','#E8E1D0',{al:'left'});T(r[1],X+190,y,'800 34px Inter','#E8E1D0',{al:'left'});
  const bl=r[3]&&cancel&&Math.floor(t*3)%2==0;T(r[2],X+w-40,y,'900 34px Inter',r[3]&&cancel?(bl?'#FF8A85':RED):'#7CD39A',{al:'right'})})}
function counter(X,Y,w){box(X,Y,w,190,'#C9B48E',8,5);box(X-10,Y-24,w+20,30,'#8C6E48',6,5);T('ATENCIÓN AL PASAJERO',X+w/2,Y+60,'900 30px Inter','#4B3A22',{ls:2})}
function voucher(X,Y,s,rot,a){if(a<=0)return;x.save();x.globalAlpha*=a;x.translate(X,Y);x.rotate(rot);x.scale(s,s);box(-170,-95,340,190,'#FBE7A1',14,5);x.setLineDash([10,8]);x.strokeStyle='#8C6E48';x.lineWidth=3;rr(-152,-78,304,156,10);x.stroke();x.setLineDash([]);
 T('BONO',0,-30,'900 54px Inter','#4B3A22');T('100 €',0,34,'900 58px Inter','#4B3A22');x.restore()}
function sign(X,Y,line1,line2,col,a){if(a<=0)return;x.save();x.globalAlpha*=a;x.translate(X,Y+(1-a)*60);x.strokeStyle=OL;x.lineWidth=8;x.beginPath();x.moveTo(0,0);x.lineTo(0,330);x.stroke();box(-185,-110,370,170,col,16,5);T(line1,0,-50,'900 46px Inter','#fff',{sh:3});T(line2,0,10,'800 30px Inter','#fff');x.restore()}
function coin(X,Y,r,rot,a){if(a<=0)return;x.save();x.globalAlpha*=a;x.translate(X,Y);x.scale(Math.abs(Math.cos(rot))*0.85+0.15,1);x.beginPath();x.arc(0,0,r,0,7);shape('#F2B705',4);T('€',0,3,`900 ${r*1.1}px Inter`,'#8A6400');x.restore()}
function table(X,Y,w,col){box(X,Y,w,26,col||'#9A6B43',6,5);x.strokeStyle=OL;x.lineWidth=8;x.beginPath();x.moveTo(X+30,Y+26);x.lineTo(X+30,Y+170);x.moveTo(X+w-30,Y+26);x.lineTo(X+w-30,Y+170);x.stroke()}
function cup(X,Y,t){box(X-26,Y-60,52,60,'#fff',8,4);x.strokeStyle='rgba(30,42,51,.5)';x.lineWidth=4;for(let i=0;i<2;i++){x.beginPath();x.moveTo(X-8+i*16,Y-70);x.quadraticCurveTo(X+(Math.sin(t*3+i)*10)-8+i*16,Y-90,X-8+i*16,Y-110);x.stroke()}}
function sandwich(X,Y){x.beginPath();x.moveTo(X-60,Y);x.lineTo(X+60,Y);x.lineTo(X,Y-60);x.closePath();shape('#E8C27A',4);x.fillStyle='#6DBE5A';x.fillRect(X-40,Y-12,80,8)}
function bed(X,Y,a){if(a<=0)return;x.save();x.globalAlpha*=a;x.translate(X,Y);box(-170,-70,340,70,'#F3EFE6',10,5);box(-170,-130,40,130,'#8C6E48',6,5);box(-120,-95,90,40,'#fff',14,4);box(-30,-90,190,30,'#4F8A8B',10,4);T('HOTEL',0,-180,'900 44px Inter','#fff',{sh:3});x.restore()}
function phone(X,Y,s,a){if(a<=0)return;x.save();x.globalAlpha*=a;x.translate(X,Y);x.scale(s,s);box(-40,-75,80,150,'#222',12,4);box(-32,-62,64,118,'#9CD3F0',6,2);T('✓',0,-5,'900 44px Inter',GRN);x.restore()}
function pass(X,Y,s,a){if(a<=0)return;x.save();x.globalAlpha*=a;x.translate(X,Y);x.rotate(-0.08);x.scale(s,s);box(-170,-80,340,160,'#fff',12,5);T('BCN → FCO',-20,-25,'900 40px Inter',OL);T('23 DIC',-20,25,'700 26px Inter','#56606a');for(let i=0;i<8;i++){x.fillStyle=OL;x.fillRect(110+i*7,-50,i%3?3:5,100)}x.restore()}
// ---------- cámara y textos
function headline(k,title,lt,col){const a=eo(lt/0.35),s=lerp(1.15,1,eb(lt/0.45));if(k)T(k,W/2,232,'900 30px Inter',CREAM,{a:a*0.75,ls:3});
 x.save();x.translate(W/2,318);x.scale(s,s);let sz=104;x.font=`900 ${sz}px Inter`;while(x.measureText(title).width>960&&sz>40){sz-=4;x.font=`900 ${sz}px Inter`}T(title,0,0,`900 ${sz}px Inter`,col||CREAM,{a,sh:5});x.restore()}
function tagHipo(){T('CASO HIPOTÉTICO',W/2,140,'800 24px Inter','rgba(255,255,255,.75)',{ls:5})}
function pill(Y,sz){x.font=`700 ${sz}px Inter`;const w=x.measureText('Enlace en la bio ↑').width+80,h=sz+44;rr(W/2-w/2,Y-h/2,w,h,h/2);x.fillStyle='#fff';x.fill();T('Enlace en la bio ↑',W/2,Y+2,`700 ${sz}px Inter`,GRN)}
function subs(t){for(const s of TM.segs){if(t<s.start-0.05||t>s.end+0.15)continue;if(s.sc==0)return;
  const ws=s.words;let chunks=[],cur=[];for(const w of ws){cur.push(w);const len=cur.map(q=>q[0]).join(' ').length;if(len>=20||cur.length>=4){chunks.push(cur);cur=[]}}if(cur.length)chunks.push(cur);
  let ch=chunks[0];for(const c2 of chunks){if(t>=c2[0][1]-0.02)ch=c2}
  x.font='900 66px Inter';const parts=ch.map(q=>q[0]);const full=parts.join(' ');const tw=x.measureText(full).width*1.12;let sz=66;if(tw>980)sz=Math.floor(66*980/tw);x.font=`900 ${sz}px Inter`;
  const fw=ch.reduce((a,q)=>a+x.measureText(q[0]).width,0)+sz*0.34*(ch.length-1);let X=W/2-fw/2;let curi=0;ch.forEach((q,i)=>{if(t>=q[1])curi=i});
  ch.forEach((q,i)=>{const w=x.measureText(q[0]).width;const on=i==curi;const sc=on?1.06:1;x.save();x.translate(X+w/2,1520);x.scale(sc,sc);T(q[0],0,0,`900 ${sz}px Inter`,on?YEL:'#fff',{st:12});x.restore();X+=w+sz*0.34});return}}
// ---------- escenas
const SC={
0:(lt,t)=>{x.fillStyle='#10221a';x.fillRect(0,0,W,H);for(let i=0;i<70;i++){x.fillStyle='rgba(255,255,255,'+(0.15+R(i)*0.35)+')';x.beginPath();x.arc((R(i+1)*W+Math.sin(t+i)*20)%W,(R(i+2)*H+t*(60+R(i)*60))%H,2+R(i+3)*4,0,7);x.fill()}
 const s=lerp(1.25,1,eb(lt/0.35));x.save();x.translate(W/2,660);x.scale(s,s);T('¿TE CANCELAN',0,-80,'900 118px Inter','#fff');T('EL VUELO',0,60,'900 118px Inter','#fff');x.restore();
 T('EN NAVIDAD?',W/2,860,'900 118px Inter',YEL,{a:eo((lt-0.2)/0.3)});
 const p=lt-0.9;if(p>0){const k=lerp(2.4,1,eo(p/0.22));x.save();x.translate(W/2,1150);x.rotate(-0.1);x.scale(k,k);x.strokeStyle=RED;x.lineWidth=14;rr(-390,-95,780,190,24);x.stroke();T('CANCELADO',0,8,'900 118px Inter',RED);x.restore()}},
1:(lt,t)=>{wall(0,1060,'#E9DCC2');x.fillStyle='#2F6B73';x.fillRect(0,880,W,40);windowSky(80,500,420,340,t,true);windowSky(580,500,420,340,t+5,false);garland(445,t);floor(1060,'#B8C3C8','#7F8E96');
 tree(900,1300,0.9,t);const wx=lerp(-120,470,eo(lt/3.2));person(wx,1420,1.25,{t,walk:lt<3.2,c:'#C8453C',hair:'long',scarf:'#F2EDE4',mouth:lt>3.2?'smile':'flat',seed:1});suitcase(wx+150,1420,0.95,'#4F8A8B');gift(wx-130,1420,0.9);
 headline('23 DE DICIEMBRE','RUMBO A ROMA',lt)},
2:(lt,t)=>{wall(0,1080,'#DCE3E4');x.fillStyle='#2F6B73';x.fillRect(0,1000,W,30);garland(445,t);board(90,560,900,t,lt>2.2);floor(1080,'#AEB9BE','#76858D');
 const shock=lt>2.6;person(360,1460,1.3,{t,c:'#C8453C',hair:'long',scarf:'#F2EDE4',mouth:shock?'o':'flat',eyes:shock?'wide':'',aL:shock?2.6:0.18,aR:shock?-2.6:-0.18,seed:1});suitcase(560,1460,1,'#4F8A8B');
 person(800,1380,0.95,{t,c:'#6B7F3A',hair:'short',mouth:shock?'sad':'flat',brow:shock?'sad':'',seed:2});person(950,1400,0.9,{t,c:'#7A5C99',hair:'bald',hc:'#5a3b2a',mouth:shock?'o':'flat',seed:3});
 headline('PANEL DE SALIDAS',lt>2.2?'¡CANCELADO!':'¿EN HORA?',lt>2.2?lt-2.2:lt,lt>2.2?'#FF8A85':CREAM)},
3:(lt,t)=>{wall(0,1100,'#E4D7BD');garland(445,t);x.fillStyle='#2F6B73';x.fillRect(0,700,W,26);floor(1100,'#B4BFC3','#7B8A92');
 person(760,1250,1.15,{t,c:'#2F4D6B',hair:'short',hat:'#2F4D6B',mouth:lt<2.6?'talk':'flat',aR:lt>0.6&&lt<2.8?-1.4:-0.18,seed:4});counter(470,1150,560);
 const v=eo((lt-0.8)/0.4);const vx=lerp(660,560,v),vy=lerp(1110,1080,v);voucher(lt>2.6?lerp(vx,700,eo((lt-2.6)/0.5)):vx,vy,0.85,-0.1,v);
 if(lt>3.2){x.save();x.strokeStyle=RED;x.lineWidth=14;x.lineCap='round';const k=eo((lt-3.2)/0.35),X0=560,Y0=1080;x.beginPath();x.moveTo(X0-150,Y0-80);x.lineTo(X0-150+300*k,Y0-80+160*k);x.stroke();x.restore()}
 person(250,1480,1.3,{t,c:'#C8453C',hair:'long',scarf:'#F2EDE4',mouth:lt>2.8?'smile':'flat',aR:lt>3?-2.2:-0.18,seed:1});
 headline('EN EL MOSTRADOR','¿UN BONO?',lt)},
4:(lt,t)=>{wall(0,1050,'#D7E1DE');garland(445,t);floor(1050,'#B4BFC3','#7B8A92');
 sign(290,760,'REEMBOLSO','EN 7 DÍAS',GRN,eo((lt-0.6)/0.4));sign(790,760,'OTRO VUELO','LO ANTES POSIBLE','#2F6B9E',eo((lt-3.0)/0.4));
 const look=lt<3?-1:1;person(540,1500,1.3,{t,c:'#C8453C',hair:'long',scarf:'#F2EDE4',flip:look>0,mouth:'smile',aR:-1.1,seed:1});suitcase(700,1500,1,'#4F8A8B');
 T('Art. 8 · Reglamento (CE) 261/2004',W/2,1640,'700 30px Inter','rgba(30,42,51,.75)',{a:eo((lt-1)/0.4)});headline('ARTÍCULO 8','TÚ ELIGES',lt)},
5:(lt,t)=>{wall(0,1060,'#EADFCB');garland(445,t);floor(1060,'#C2B59B','#8F826A');
 const night=eo((lt-4.0)/0.6);table(140,1180,420);sandwich(260,1180);cup(450,1180,t);
 person(330,1480,1.2,{t,c:'#C8453C',hair:'long',scarf:'#F2EDE4',mouth:lt<4.0?'smile':'flat',seed:1});
 if(night>0){x.fillStyle=`rgba(20,30,60,${0.35*night})`;x.fillRect(0,0,W,1060);x.fillStyle=`rgba(255,240,180,${night})`;x.beginPath();x.arc(900,560,50,0,7);x.fill()}
 bed(790,1300,night);T('Art. 9 · a cargo de la aerolínea',W/2,1640,'700 30px Inter','rgba(30,42,51,.8)',{a:eo((lt-1)/0.4)});
 headline('ARTÍCULO 9',lt<4.0?'COMIDA Y BEBIDA':'Y HOTEL',lt<4.0?lt:lt-4.0)},
6:(lt,t)=>{wall(0,1080,'#DCE6DA');garland(445,t);floor(1080,'#B4BFC3','#7B8A92');
 const rain=lt>7.4;person(540,1500,1.4,{t,c:'#C8453C',hair:'long',scarf:'#F2EDE4',mouth:rain?'smile':'flat',eyes:rain?'wide':'',jump:rain&&lt<9.9,aL:rain?2.5:0.18,aR:rain?-2.5:-0.18,seed:1});
 if(rain)for(let i=0;i<22;i++){const st=7.4+R(i)*2.2;if(lt>st)coin(80+R(i+11)*920,lerp(380,1500,Math.pow(cl((lt-st)/1.4),1.6)),34,lt*7+i,1-cl((lt-st-1.2)/0.3))}
 const tv=Math.round(250*eo((lt-7.4)/0.9));if(lt>7.4){x.save();x.translate(W/2,620);const s=eb((lt-7.4)/0.4);x.scale(s,s);T(tv+' €',0,0,'900 230px Inter','#2E9E5B',{st:14,stc:'#fff'});x.restore();
  T('por persona · vuelos de hasta 1.500 km',W/2,780,'800 34px Inter',OL,{a:eo((lt-8.4)/0.4)});T('Arts. 5 y 7 del Reglamento 261/2004',W/2,830,'700 28px Inter','rgba(30,42,51,.7)',{a:eo((lt-8.7)/0.4)})}
 else{T('AVISO: MENOS DE 14 DÍAS',W/2,620,'900 56px Inter',RED,{a:eo((lt-0.4)/0.4)})}
 headline(lt<7.4?'SIN CIRCUNSTANCIAS EXTRAORDINARIAS':'NORMALMENTE',lt<7.4?'¿COMPENSACIÓN?':'EN DINERO',lt<7.4?lt:lt-7.4)},
7:(lt,t)=>{wall(0,1060,'#5B3B3B');x.fillStyle='#4A2E2E';for(let i=0;i<8;i++)x.fillRect(i*140,430,70,630);garland(445,t);windowSky(640,520,340,280,t,false);
 x.fillStyle='rgba(10,20,50,.55)';x.fillRect(640,520,340,280);floor(1060,'#8C6A4A','#5E452F');tree(160,1080,0.85,t);
 person(330,1330,1.0,{t,c:'#3E6FA0',hair:'short',hc:'#888',mouth:'smile',seed:5});person(820,1330,1.0,{t,c:'#7A5C99',hair:'long',hc:'#6b4b3a',mouth:'smile',seed:6});
 box(160,1260,760,40,'#F3EFE6',8,5);for(const cx of[300,540,780]){x.beginPath();x.ellipse(cx,1255,60,16,0,0,7);shape('#fff',3)}
 for(const cx of[420,660]){box(cx-8,1180,16,70,'#fff',4,3);x.fillStyle='#F7B731';x.beginPath();x.ellipse(cx,1168+Math.sin(t*8+cx)*2,8,14,0,0,7);x.fill()}
 const enter=eo(lt/1.2);person(lerp(1200,560,enter),1520,1.25,{t,walk:lt<1.2,c:'#C8453C',hair:'long',scarf:'#F2EDE4',mouth:'smile',aR:lt>1.6?-1.9:-0.18,seed:1});
 if(lt>1.6){const h=window._hand;pass(lerp(1200,560,enter)+h[0]*1.25+40,1520+h[1]*1.25-40,0.55,eo((lt-1.6)/0.3))}
 headline('NOCHEBUENA','¡LLEGÓ A LA CENA!',lt)},
8:(lt,t)=>{SC[7](lt+3,t);x.fillStyle=`rgba(8,14,24,${0.82*eo(lt/0.5)})`;x.fillRect(0,0,W,H);
 const a1=eo((lt-0.1)/0.4);x.save();x.translate(W/2,560);x.scale(lerp(1.2,1,eb(lt/0.4)),lerp(1.2,1,eb(lt/0.4)));T('¿TE HA PASADO',0,-60,'900 104px Inter','#fff',{a:a1});T('ALGO ASÍ?',0,60,'900 104px Inter',YEL,{a:a1});x.restore();
 T('Cuéntalo en comentarios',W/2,760,'800 54px Inter',CREAM,{a:eo((lt-2.6)/0.4)});
 const a3=eo((lt-4.3)/0.5);x.save();x.globalAlpha*=a3;x.font='900 120px Inter';const w1=x.measureText('VuelosClaim').width,w2=x.measureText('.eu').width,X0=W/2-(w1+w2)/2;
 T('VuelosClaim',X0,1020,'900 120px Inter',CREAM,{al:'left'});T('.eu',X0+w1,1020,'900 120px Inter','#E0B44C',{al:'left'});x.restore();
 T('CALCULA GRATIS CUÁNTO TE CORRESPONDE',W/2,1120,'800 28px Inter','rgba(255,255,255,.7)',{a:a3,ls:3})}};
window.render=function(t){let sc=0,st=0;for(const [k,a] of TM.bounds){if(t>=a){sc=k;st=a}}const lt=t-st;
 x.save();const z=sc==0||sc==8?1:lerp(1.05,1,eo(lt/0.5))*(1+0.012*lt/6);x.translate(W/2,H/2);x.scale(z,z);x.translate(-W/2,-H/2);SC[sc](lt,t);x.restore();
 if(sc>0&&sc<8)tagHipo();
 subs(t);
 if(sc==0)pill(1480,56);else pill(1790,40);
 // grano
 x.fillStyle='rgba(0,0,0,0.04)';x.fillRect(0,0,W,H)}
