timeline([8.418,7.837,6.485,9.213,2.937,6.467],[0.4,0.4,0.45,0.6,0.35,1.2]);
function snow(t,n,a){x.save();x.globalAlpha*=a;x.fillStyle=K.bone;for(let i=0;i<n;i++){const sp=40+R(i)*70,X=(R(i+3)*W+Math.sin(t*0.8+i)*30)%W,Y=((R(i+7)*H+t*sp)%H);x.globalAlpha=a*(0.15+R(i+9)*0.35);x.beginPath();x.arc(X,Y,2+R(i+5)*4,0,7);x.fill()}x.restore()}
function pass(cx,cy,s,a){if(a<=0)return;x.save();x.globalAlpha*=a;x.translate(cx,cy);x.rotate(-0.06);x.scale(s,s);
 rr(-360,-170,720,340,28);x.fillStyle=K.bone;x.fill();x.setLineDash([12,10]);x.strokeStyle='#8A93A8';x.lineWidth=3;x.beginPath();x.moveTo(170,-150);x.lineTo(170,150);x.stroke();x.setLineDash([]);
 T('TARJETA DE EMBARQUE',-330,-120,'GMB',24,'#3a3a3a',{al:'left',ls:3});T('BCN',-330,-30,'BS',110,'#141414',{al:'left'});T('→',-130,-30,'GMB',50,'#B98900');T('FCO',-70,-30,'BS',110,'#141414',{al:'left'});
 T('23 DIC  ·  ASIENTO 14C',-330,80,'GM',28,'#3a3a3a',{al:'left',ls:2});for(let i=0;i<14;i++){x.fillStyle='#141414';x.fillRect(200+i*10,-110,i%3?4:7,200)}x.restore()}
function receipt(cx,cy,s,a){if(a<=0)return;x.save();x.globalAlpha*=a;x.translate(cx,cy);x.rotate(0.07);x.scale(s,s);x.fillStyle='#FFFFFF';x.beginPath();x.moveTo(-150,-210);x.lineTo(150,-210);for(let i=0;i<=10;i++)x.lineTo(150-i*30,210+(i%2?14:0));x.closePath();x.fill();
 T('TIQUE',0,-160,'GMB',30,'#141414',{ls:6});['Bocadillo   6,50','Agua        2,20','Taxi       24,00'].forEach((l,i)=>T(l,0,-80+i*55,'GM',26,'#3a3a3a'));x.fillStyle='#141414';x.fillRect(-120,110,240,3);T('GUARDAR',0,160,'GMB',30,K.red,{ls:4});x.restore()}
const SC=[
(lt,t)=>{const V=lt-PRE;snow(t,60,1);
 big2('¿CANCELADO','EN NAVIDAD?',520,K.bone,K.amber,170,eb((lt-0.05)/0.45));
 const pa=eo((V-0.6)/0.4);x.save();x.globalAlpha*=pa;rr(60,800,960,330,26);x.fillStyle='rgba(5,8,15,.8)';x.fill();x.strokeStyle='rgba(245,183,0,.35)';x.lineWidth=2;x.stroke();
 T('SALIDAS',100,850,'GMB',28,K.amber,{al:'left',ls:6});T('DEPARTURES',980,850,'GM',24,K.mut,{al:'right',ls:6});
 flap('BARCELONA',100,890,52,80,(V-0.6)*2.2,K.bone,1);T('→',680,930,'GMB',54,K.amber);flap('ROMA',740,890,52,80,(V-0.8)*2.2,K.bone,7);
 flap('23 DIC',100,1010,52,80,(V-1.0)*2.2,K.bone,30);const ch=V>6.9;const bl=ch&&Math.floor(t*3)%2==0;
 flap(ch?'CANCELADO':'EN HORA  ',470,1010,52,80,ch?(V-6.9)*2.5:(V-1.0)*2.2,ch?(bl?'#7A1F22':K.red):K.green,50);x.restore();
 T('Caso hipotético · Barcelona–Roma',W/2,1240,'OU',38,K.mut,{a:eo((V-1)/0.4)});
 stamp(W/2,1420,'CANCELADO',K.red,(V-7.3)/1.2,110,-0.06)},
(lt,t)=>{const V=lt-PRE;const vo=eo(V/0.4)*(1-eo((V-2.6)/0.5));if(vo>0){x.save();x.globalAlpha*=vo;voucher(W/2,760,1.1,'?');x.restore();
  T('¿Lo primero que te ofrezcan?',W/2,1080,'IS',62,K.bone,{a:vo});if(V>1.6){x.save();x.globalAlpha*=vo;x.strokeStyle=K.red;x.lineWidth=14;x.lineCap='round';const k=eo((V-1.6)/0.4);x.beginPath();x.moveTo(W/2-330,760-170);x.lineTo(W/2-330+660*k,760-170+340*k);x.stroke();x.restore()}}
 T('TÚ ELIGES',W/2,330,'BS',120,K.amber,{a:eo((V-2.8)/0.4)});
 option(W/2,640,'Reembolso','EN 7 DÍAS','coin',eo((V-3.6)/0.4));option(W/2,1060,'Otro vuelo','LO ANTES POSIBLE','plane',eo((V-5.2)/0.4));
 T('art. 8 · Reglamento (CE) 261/2004',W/2,1320,'GM',28,K.mut,{a:eo((V-5.8)/0.4),ls:1})},
(lt,t)=>{const V=lt-PRE;T('MIENTRAS ESPERAS',W/2,330,'BS',120,K.amber,{a:eo(V/0.4)});
 const rows=[[1,'Comida',1.0],[0,'Bebida',2.0],[2,'Hotel y traslado',3.6]];
 rows.forEach(([k,lab,st],i)=>{const a=eo((V-st)/0.4);if(a<=0)return;const Y=600+i*230;x.save();x.globalAlpha*=a;x.translate((1-a)*-80,0);rr(140,Y-90,800,180,30);x.fillStyle='rgba(242,237,228,.06)';x.fill();x.strokeStyle='rgba(61,214,140,.6)';x.lineWidth=3;x.stroke();
  icon(k,270,Y,90,1,K.green);T(lab,390,Y+4,'OUB',58,K.bone,{al:'left'});T('✓',880,Y+4,'OUB',64,K.green);x.restore()});
 T('art. 9 · gratis, a cargo de la aerolínea',W/2,1330,'GM',28,K.mut,{a:eo((V-4.2)/0.4),ls:1});
 const h=(V*0.9)%12;x.save();x.translate(W/2,1500);x.globalAlpha*=eo((V-0.5)/0.4)*0.8;x.strokeStyle=K.mut;x.lineWidth=4;x.beginPath();x.arc(0,0,60,0,7);x.stroke();x.strokeStyle=K.amber;x.lineWidth=6;x.lineCap='round';
  x.beginPath();x.moveTo(0,0);x.lineTo(Math.sin(h/12*6.283)*35,-Math.cos(h/12*6.283)*35);x.stroke();x.beginPath();x.moveTo(0,0);x.lineTo(Math.sin(V*2)*50,-Math.cos(V*2)*50);x.stroke();x.restore()},
(lt,t)=>{const V=lt-PRE;T('AVISO < 14 DÍAS',W/2,330,'GMB',44,K.red,{ls:5,a:eo(V/0.4)});
 T('sin circunstancias extraordinarias',W/2,410,'IS',56,K.bone,{a:eo((V-1.8)/0.4)});
 const tv=Math.round(250*eo((V-4.6)/0.9));const s=eb((V-4.5)/0.4);x.save();x.translate(W/2,760);x.scale(s,s);T(tv+' €',0,0,'BS',300,K.green);x.restore();
 T('por persona · en dinero',W/2,970,'IS',66,K.bone,{a:eo((V-6.6)/0.4)});
 T('vuelos de hasta 1.500 km · arts. 5 y 7 del Reglamento 261/2004',W/2,1100,'GM',26,K.mut,{a:eo((V-7.0)/0.4)});
 T('normalmente: depende del motivo de la cancelación',W/2,1160,'GM',26,K.mut,{a:eo((V-7.2)/0.4)});
 for(let i=0;i<14;i++){const st=4.7+R(i)*1.4;if(V>st){coin(100+R(i+11)*880,lerp(180,1600,Math.pow(cl((V-st)/1.3),1.7)),28,V*7+i,1-cl((V-st-1.1)/0.3))}}},
(lt,t)=>{const V=lt-PRE;T('GUARDA',W/2,330,'BS',150,K.amber,{a:eo(V/0.3)});pass(W/2,720,eb((V-0.1)/0.4),eo(V/0.3));receipt(W/2+170,1160,eb((V-1.0)/0.4)*0.9,eo((V-1.0)/0.3))},
(lt,t)=>{const V=lt-PRE;snow(t,40,0.8);cta(V,t,'¿TE HA PASADO?','Cuéntalo en comentarios')}];
run(SC);
