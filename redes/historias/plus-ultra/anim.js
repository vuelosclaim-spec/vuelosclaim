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

// ---------- Plus Ultra
const CAR={c:'#2E8B7A',hair:'long',hc:'#2B1B14',scarf:'#F3E3C3',seed:1};
function segRel(sc,i){const ss=TM.segs.filter(s=>s.sc==sc);const b=TM.bounds.find(q=>q[0]==sc)[1];return ss[Math.min(i,ss.length-1)].start-b}
function home(t,night){const g=x.createLinearGradient(0,0,0,1080);g.addColorStop(0,'#F0E2C8');g.addColorStop(1,'#E4CFAE');x.fillStyle=g;x.fillRect(0,0,W,1080);
 const g2=x.createLinearGradient(0,0,0,430);g2.addColorStop(0,'#1B2731');g2.addColorStop(1,'#34454F');x.fillStyle=g2;x.fillRect(0,0,W,430);x.fillStyle='#1E2A33';x.fillRect(0,426,W,8);x.fillStyle='#C9A77C';x.fillRect(0,980,W,100);windowSky(600,520,380,300,t,true);if(night){x.fillStyle='rgba(10,20,50,.55)';x.fillRect(600,520,380,300)}
 box(80,540,160,200,'#B5835A',8,5);x.fillStyle='#E9C46A';x.beginPath();x.arc(160,640,48,0,7);x.fill();
 floor(1080,'#A9805B','#7A5A3E');x.fillStyle='rgba(0,0,0,.08)';x.beginPath();x.ellipse(540,1460,420,60,0,0,7);x.fill()}
function sofa(X,Y){box(X-230,Y-170,460,110,'#5B7FA6',30,5);box(X-260,Y-90,520,90,'#4E6F93',24,5);box(X-270,Y-150,60,150,'#4E6F93',20,5);box(X+210,Y-150,60,150,'#4E6F93',20,5)}
function bigPhone(X,Y,s,a,t,news){if(a<=0)return;x.save();x.globalAlpha*=a;x.translate(X,Y);x.scale(s,s);box(-170,-300,340,600,'#1C1F24',40,6);box(-150,-260,300,520,'#EAF2F6',18,3);
 T('12:41',0,-230,'700 26px Inter','#56606a');if(news>0){x.save();x.globalAlpha*=news;x.translate(0,lerp(-40,0,eo(news)));box(-135,-190,270,200,'#fff',18,3);
 T('ÚLTIMA HORA',-110,-160,'900 22px Inter',RED,{al:'left',ls:2});T('Plus Ultra',-110,-118,'900 34px Inter',OL,{al:'left'});T('deja de volar',-110,-80,'900 34px Inter',OL,{al:'left'});
 T('Vuelos suspendidos',-110,-38,'600 22px Inter','#56606a',{al:'left'});x.restore()}
 for(let i=0;i<3;i++){box(-135,40+i*70,270,52,'#D7E3EA',12,0)}x.restore()}
function board2(X,Y,w,t,cancel){box(X,Y,w,300,'#13202B',10,6);T('SALIDAS · DEPARTURES',X+w/2,Y+38,'900 26px Inter',YEL,{ls:4});
 const rows=[['11:30','LISBOA','EN HORA',0],['12:55','CARACAS',cancel?'CANCELADO':'EN HORA',1],['13:20','LIMA',cancel?'CANCELADO':'EN HORA',1]];
 rows.forEach((r,i)=>{const y=Y+100+i*72;x.fillStyle=r[3]&&cancel?'rgba(214,69,65,.18)':'rgba(255,255,255,.05)';x.fillRect(X+20,y-28,w-40,58);
  T(r[0],X+40,y,'700 34px Inter','#E8E1D0',{al:'left'});T(r[1],X+190,y,'800 34px Inter','#E8E1D0',{al:'left'});
  const bl=r[3]&&cancel&&Math.floor(t*3)%2==0;T(r[2],X+w-40,y,'900 34px Inter',r[3]&&cancel?(bl?'#FF8A85':RED):'#7CD39A',{al:'right'})})}
function ticket(X,Y,s,a,rot){if(a<=0)return;x.save();x.globalAlpha*=a;x.translate(X,Y);x.rotate(rot||-0.08);x.scale(s,s);box(-180,-85,360,170,'#fff',12,5);
 T('MAD → CCS',-25,-30,'900 44px Inter',OL);T('PLUS ULTRA · 24 DIC',-25,22,'700 24px Inter','#56606a');for(let i=0;i<8;i++){x.fillStyle=OL;x.fillRect(120+i*7,-55,i%3?3:5,110)}x.restore()}
function checklist(X,Y,w,items,shown){box(X,Y,w,120+items.length*120,'#FFFDF6',18,5);
 items.forEach((it,i)=>{const a=eo(shown[i]);if(a<=0)return;const y=Y+110+i*120;x.save();x.globalAlpha*=a;x.translate(lerp(40,0,a),0);
  x.beginPath();x.arc(X+70,y,34,0,7);shape(GRN,4);T('✓',X+70,y+2,'900 40px Inter','#fff');T(it[0],X+125,y-18,'900 40px Inter',OL,{al:'left'});T(it[1],X+125,y+26,'600 28px Inter','#56606a',{al:'left'});x.restore()})}
function laptop(X,Y,s,sent){x.save();x.translate(X,Y);x.scale(s,s);box(-150,-190,300,190,'#2A2F36',12,5);box(-135,-175,270,160,sent?'#D9F2E2':'#EAF2F6',6,2);
 if(sent){T('✓',0,-120,'900 60px Inter',GRN);T('ENVIADO',0,-60,'900 30px Inter',GRN)}else{for(let i=0;i<4;i++){x.fillStyle='#B8C6CE';x.fillRect(-110,-155+i*30,200-i*30,12)}}
 box(-190,0,380,24,'#9AA5AD',8,4);x.restore()}
const SC={
0:(lt,t)=>{x.fillStyle='#10221a';x.fillRect(0,0,W,H);for(let i=0;i<70;i++){x.fillStyle='rgba(255,255,255,'+(0.15+R(i)*0.35)+')';x.beginPath();x.arc((R(i+1)*W+Math.sin(t+i)*20)%W,(R(i+2)*H+t*(60+R(i)*60))%H,2+R(i+3)*4,0,7);x.fill()}
 const s=lerp(1.25,1,eb(lt/0.35));x.save();x.translate(W/2,600);x.scale(s,s);T('¿Y SI TU',0,-90,'900 112px Inter','#fff');T('AEROLÍNEA',0,40,'900 124px Inter',YEL);x.restore();
 T('DEJA DE VOLAR?',W/2,800,'900 112px Inter','#fff',{a:eo((lt-0.35)/0.3)});
 const p=lt-1.1;if(p>0){const k=lerp(2.4,1,eo(p/0.22));x.save();x.translate(W/2,1130);x.rotate(-0.1);x.scale(k,k);x.strokeStyle=RED;x.lineWidth=14;rr(-400,-95,800,190,24);x.stroke();T('SIN VUELO',0,8,'900 124px Inter',RED);x.restore()}},
1:(lt,t)=>{home(t,true);garland(445,t);tree(880,1260,0.85,t);sofa(330,1260);
 const wx=lerp(-120,520,eo(lt/2.6));person(wx,1500,1.3,{...CAR,t,walk:lt<2.6,mouth:lt>2.6?'smile':'flat'});suitcase(wx+165,1500,1,'#C8453C');gift(wx-140,1500,0.85);
 const s1=segRel(1,1);ticket(780,760,0.95,eo((lt-s1+0.3)/0.4),-0.06);
 headline('NAVIDAD EN FAMILIA','MADRID → CARACAS',lt)},
2:(lt,t)=>{home(t,false);sofa(540,1300);const s1=segRel(2,1),s2=segRel(2,2);const news=cl((lt-s1+0.2)/0.4),shock=lt>s1+0.3;
 person(300,1520,1.3,{...CAR,t,mouth:shock?'o':'flat',eyes:shock?'wide':'',aR:-1.7,brow:shock?'sad':''});
 bigPhone(700,860,1.05,eo(lt/0.4),t,news);
 if(lt>s2){const a=eo((lt-s2)/0.4);for(let i=0;i<9;i++){const px=120+i*105;x.save();x.globalAlpha*=a;x.translate(px,1820);x.scale(0.32,0.32);person(0,0,1,{t,c:['#7A5C99','#6B7F3A','#3E6FA0','#C8453C'][i%4],hair:['short','long','bald'][i%3],mouth:'sad',brow:'sad',seed:i+3});x.restore()}
  T('MILES DE PASAJEROS SIN VUELO',W/2,1660,'900 40px Inter',RED,{a,st:8,stc:'#fff'})}
 headline('ÚLTIMA HORA',news>0.5?'PLUS ULTRA DEJA DE VOLAR':'UN MENSAJE…',news>0.5?lt-s1:lt,news>0.5?'#FF8A85':CREAM)},
3:(lt,t)=>{wall(0,1080,'#DCE3E4');x.fillStyle='#2F6B73';x.fillRect(0,1000,W,30);board2(90,560,900,t,true);floor(1080,'#AEB9BE','#76858D');
 const s1=segRel(3,1);const ok=lt>s1;person(380,1470,1.3,{...CAR,t,mouth:ok?'smile':'sad',brow:ok?'':'sad',aL:ok?0.18:2.4,aR:ok?-1.2:-2.4});suitcase(580,1470,1,'#C8453C');
 if(ok)T('Art. 5 · Reglamento (CE) 261/2004',W/2,1640,'700 30px Inter','rgba(30,42,51,.75)',{a:eo((lt-s1-0.4)/0.4)});
 headline(ok?'PARA LA LEY':'¿Y MI DINERO?',ok?'ES UNA CANCELACIÓN':'¿LO HE PERDIDO?',ok?lt-s1:lt,ok?'#7CD39A':CREAM)},
4:(lt,t)=>{wall(0,1050,'#D7E1DE');floor(1050,'#B4BFC3','#7B8A92');const s1=segRel(4,1);
 sign(290,760,'REEMBOLSO','EN 7 DÍAS',GRN,eo((lt-0.5)/0.4));sign(790,760,'OTRO VUELO','LO ANTES POSIBLE','#2F6B9E',eo((lt-s1)/0.4));
 person(540,1500,1.3,{...CAR,t,flip:lt>s1,mouth:'smile',aR:-1.1});suitcase(700,1500,1,'#C8453C');
 T('Art. 8 · Reglamento (CE) 261/2004',W/2,1640,'700 30px Inter','rgba(30,42,51,.75)',{a:eo((lt-1)/0.4)});headline('ARTÍCULO 8','ELIGE CARMEN',lt)},
5:(lt,t)=>{wall(0,1080,'#DCE6DA');floor(1080,'#B4BFC3','#7B8A92');const s1=segRel(5,1),s2=segRel(5,2);const rain=lt>s2;
 person(540,1500,1.4,{...CAR,t,mouth:rain?'smile':'flat',eyes:rain?'wide':'',jump:rain&&lt<s2+2.5,aL:rain?2.5:0.18,aR:rain?-2.5:-0.18});
 if(rain)for(let i=0;i<24;i++){const st=s2+R(i)*2;if(lt>st)coin(80+R(i+11)*920,lerp(380,1500,Math.pow(cl((lt-st)/1.4),1.6)),34,lt*7+i,1-cl((lt-st-1.2)/0.3))}
 if(rain){const tv=Math.round(600*eo((lt-s2)/0.9));x.save();x.translate(W/2,640);const s=eb((lt-s2)/0.4);x.scale(s,s);T(tv+' €',0,0,'900 230px Inter','#2E9E5B',{st:14,stc:'#fff'});x.restore();
  T('por pasajero · vuelos de más de 3.500 km',W/2,800,'800 34px Inter',OL,{a:eo((lt-s2-1)/0.4)});T('Art. 7 · si no hay circunstancias extraordinarias',W/2,850,'700 28px Inter','rgba(30,42,51,.7)',{a:eo((lt-s2-1.3)/0.4)})}
 else{T('AVISO: MENOS DE 14 DÍAS',W/2,600,'900 56px Inter',RED,{a:eo((lt-0.4)/0.4)});if(lt>s1){T('MADRID → CARACAS',W/2,720,'900 60px Inter',OL,{a:eo((lt-s1)/0.4)});T('MÁS DE 3.500 KM',W/2,800,'900 50px Inter','#2F6B9E',{a:eo((lt-s1-0.3)/0.4)})}}
 headline(rain?'NORMALMENTE':'¿COMPENSACIÓN?',rain?'HASTA 600 €':'¿TAMBIÉN?',rain?lt-s2:lt)},
6:(lt,t)=>{wall(0,1080,'#E4D7BD');floor(1080,'#B4BFC3','#7B8A92');const s=[1,2,3].map(i=>segRel(6,i));
 checklist(110,520,860,[['Reclama por escrito','y guarda la respuesta'],['Reclama a la agencia','si compraste con ella'],['Pregunta a tu banco','si pagaste con tarjeta']],s.map(v=>(lt-v+0.1)/0.4));
 person(540,1560,1.15,{...CAR,t,mouth:lt<s[0]?'sad':'talk',brow:lt<s[0]?'sad':'',aR:-1.3});
 headline('¿Y SI NO PAGA?','QUÉ HACER',lt)},
7:(lt,t)=>{home(t,true);garland(445,t);tree(880,1260,0.85,t);table(140,1240,460,'#9A6B43');const s1=segRel(7,1);const sent=lt>1.8;
 laptop(370,1240,1,sent);person(700,1520,1.25,{...CAR,t,mouth:sent?'smile':'flat',aL:sent?2.4:0.18,aR:sent?-2.4:-0.18,jump:sent&&lt<3.2});
 ticket(330,880,0.75,eo((lt-s1)/0.4),0.05);
 headline('ESE MISMO DÍA',sent?'RECLAMACIÓN ENVIADA':'CARMEN RECLAMA',sent?lt-1.8:lt,sent?'#2E9E5B':CREAM)},
8:(lt,t)=>{SC[7](lt+4,t);x.fillStyle=`rgba(8,14,24,${0.82*eo(lt/0.5)})`;x.fillRect(0,0,W,H);
 const a1=eo((lt-0.1)/0.4);x.save();x.translate(W/2,560);x.scale(lerp(1.2,1,eb(lt/0.4)),lerp(1.2,1,eb(lt/0.4)));T('¿TENÍAS BILLETE',0,-60,'900 96px Inter','#fff',{a:a1});T('CON PLUS ULTRA?',0,60,'900 96px Inter',YEL,{a:a1});x.restore();
 const s1=segRel(8,1),s2=segRel(8,2);T('Cuéntalo en comentarios',W/2,760,'800 54px Inter',CREAM,{a:eo((lt-s1)/0.4)});
 const a3=eo((lt-s2-0.6)/0.5);x.save();x.globalAlpha*=a3;x.font='900 120px Inter';const w1=x.measureText('VuelosClaim').width,w2=x.measureText('.eu').width,X0=W/2-(w1+w2)/2;
 T('VuelosClaim',X0,1020,'900 120px Inter',CREAM,{al:'left'});T('.eu',X0+w1,1020,'900 120px Inter','#E0B44C',{al:'left'});x.restore();
 T('CALCULA GRATIS CUÁNTO TE CORRESPONDE',W/2,1120,'800 28px Inter','rgba(255,255,255,.7)',{a:a3,ls:3})}};
window.render=function(t){let sc=0,st=0;for(const [k,a] of TM.bounds){if(t>=a){sc=k;st=a}}const lt=t-st;
 x.save();const z=sc==0||sc==8?1:lerp(1.05,1,eo(lt/0.5))*(1+0.012*lt/6);x.translate(W/2,H/2);x.scale(z,z);x.translate(-W/2,-H/2);SC[sc](lt,t);x.restore();
 if(sc>0&&sc<8)tagHipo();
 subs(t);
 if(sc==0)pill(1480,56);else pill(1790,40);
 x.fillStyle='rgba(0,0,0,0.04)';x.fillRect(0,0,W,H)}
