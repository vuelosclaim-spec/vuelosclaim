timeline([3.791,6.428,13.356,5.692,3.879],[0.35,0.5,0.6,0.5,0.9]);
function sizer(cx,cy,w,h,col){x.strokeStyle=col;x.lineWidth=10;x.strokeRect(cx-w/2,cy-h/2,w,h);x.fillStyle='rgba(242,237,228,.06)';x.fillRect(cx-w/2,cy-h/2,w,h)}
function backpack(cx,cy,w,h,col){rr(cx-w/2,cy-h/2,w,h,38);x.fillStyle=col;x.fill();rr(cx-w*0.32,cy-h*0.05,w*0.64,h*0.4,20);x.fillStyle='rgba(0,0,0,.18)';x.fill();x.strokeStyle='rgba(0,0,0,.35)';x.lineWidth=8;x.beginPath();x.arc(cx,cy-h/2,w*0.18,Math.PI,0);x.stroke()}
const SC=[
(lt,t)=>{const V=lt-PRE;big2('¿CABE TU','MOCHILA?',470,K.bone,K.amber,190,eb((lt-0.2)/0.5));T('PUERTA B12',W/2,700,'GMB',34,K.mut,{ls:8});
 sizer(W/2,1080,400,300,K.bone);const d=eo((V-0.5)/1.6),sh=V>2.1&&V<2.8?Math.sin(V*60)*10:0;backpack(W/2+sh,lerp(760,1040,d),400,360,K.amber);
 if(V>2.1){stamp(W/2,1360,'NO CABE',K.red,V-2.1,90,0.05)}},
(lt,t)=>{const V=lt-PRE;sizer(W/2,700,400,300,K.bone);backpack(W/2,660,400,360,K.amber);x.strokeStyle=K.red;x.lineWidth=6;x.beginPath();x.moveTo(W/2-200,470);x.lineTo(W/2+200,470);x.stroke();
 T('+5 CM',W/2,390,'BS',110,K.red,{a:eo(V/0.3)});
 const a=eo((V-5.0)/0.4);if(a>0){x.save();x.translate(W/2,1200);x.rotate(Math.sin(t*3)*0.06*a);x.globalAlpha*=a;rr(-230,-120,460,240,30);x.fillStyle=K.red;x.fill();x.beginPath();x.arc(-170,-60,16,0,7);x.fillStyle=K.bg;x.fill();T('65 €',30,10,'BS',170,K.bone);x.restore()}
 T('Ejemplo: Volotea, maleta a cabina sin contratar',W/2,1400,'OU',36,K.mut,{a:eo((V-5.6)/0.4)})},
(lt,t)=>{const V=lt-PRE;T('BOLSO GRATIS BAJO EL ASIENTO',W/2,300,'GMB',34,K.amber,{ls:4,a:eo(V/0.4)});
 const rows=[[2.4,'Ryanair · Vueling · Volotea','40 × 30 × 20',[40,30,20]],[8.0,'easyJet','45 × 36 × 20',[45,36,20]],[10.2,'Iberia · Air Europa','40 × 30 × 15',[40,30,15]]];
 rows.forEach((r,i)=>{const a=eo((V-r[0])/0.5);if(a<=0)return;const y=520+i*380,sc=7.5;const w=r[3][1]*sc,h=r[3][0]*sc,dep=r[3][2]*sc*0.45;x.save();x.globalAlpha*=a;
  const X=130,Y=y-h/2+(1-a)*30;x.fillStyle='rgba(245,183,0,.15)';x.beginPath();x.moveTo(X+w,Y);x.lineTo(X+w+dep,Y-dep*0.6);x.lineTo(X+w+dep,Y+h-dep*0.6);x.lineTo(X+w,Y+h);x.closePath();x.fill();
  x.beginPath();x.moveTo(X,Y);x.lineTo(X+dep,Y-dep*0.6);x.lineTo(X+w+dep,Y-dep*0.6);x.lineTo(X+w,Y);x.closePath();x.fill();x.strokeStyle=K.amber;x.lineWidth=4;x.strokeRect(X,Y,w,h);
  T(r[2],X+w+dep+40,y-20,'BS',90,K.bone,{al:'left'});T(r[1],X+w+dep+40,y+60,'OUB',34,K.mut,{al:'left'});x.restore()})},
(lt,t)=>{const V=lt-PRE;T('DESDE EL 23-10-2027',W/2,330,'GMB',36,K.green,{ls:5,a:eo(V/0.4)});const s=eb((V-0.6)/0.5);x.save();x.translate(W/2,600);x.scale(s,s);T('2027',0,0,'BS',300,K.bone);x.restore();
 backpack(W/2,1000,300,225,K.green);stamp(W/2,1000,'GRATIS',K.bone,V-3.2,90,-0.1);T('40 × 30 × 15 cm en todas las aerolíneas',W/2,1230,'OU',40,K.bone,{a:eo((V-2.4)/0.4)});
 T('Reglamento (UE) 2026/2202',W/2,1300,'GM',26,K.mut,{a:eo((V-2.8)/0.4),ls:2})},
(lt,t)=>{const V=lt-PRE;cta(V,t,'¿CABE TU MALETA?','compruébalo antes de volar')}];
run(SC);
