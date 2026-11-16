timeline([6.589,3.613,4.797,4.375,3.204,4.41],[0.35,0.35,0.5,0.6,0.35,0.9]);
const SC=[
(lt,t)=>{const V=lt-PRE;rr(60,250,960,360,26);x.fillStyle='rgba(5,8,15,.75)';x.fill();x.strokeStyle='rgba(245,183,0,.35)';x.lineWidth=2;x.stroke();
 T('SALIDAS',100,300,'GMB',28,K.amber,{al:'left',ls:6});T('DEPARTURES',980,300,'GM',24,K.mut,{al:'right',ls:6});
 flap('MADRID',100,340,52,80,lt*2.2,K.bone,1);T('→',470,380,'GMB',54,K.amber);flap('TENERIFE',530,340,52,80,lt*2.2-0.2,K.bone,7);
 const ch=V>5.5;flap(ch?'16 00':'18 00',100,470,52,80,ch?(V-5.5)*2.5:lt*2.2,ch?K.amber:K.bone,30);T(':',214,512,'GMB',54,ch?K.amber:K.bone);
 const bl=V>5.6&&Math.floor(t*3)%2==0;flap(ch?'ADELANTADO':'EN HORA   ',430,470,52,80,ch?(V-5.5)*2.5:lt*2.2,bl?'#6B5200':K.amber,50);
 big2('¿TE DEBEN','DINERO?',840,K.bone,K.amber,190,eb((lt-0.3)/0.5));
 const a=eo((V-4.0)/0.4);if(a>0){x.save();x.globalAlpha*=a;rr(W/2-270,1140,540,110,55);x.strokeStyle=K.red;x.lineWidth=4;x.stroke();T('AVISO: 5 DÍAS ANTES',W/2,1197,'GMB',38,K.red,{ls:3});x.restore()}
 T('Caso hipotético · Madrid–Tenerife',W/2,1360,'OU',38,K.mut,{a:eo((V-1)/0.4)})},
(lt,t)=>{const V=lt-PRE;x.save();x.translate(W/2,620);x.strokeStyle='rgba(242,237,228,.2)';x.lineWidth=3;x.beginPath();x.arc(0,0,280,0,7);x.stroke();
 for(let i=0;i<12;i++){const a=i/12*Math.PI*2;x.strokeStyle=K.bone;x.lineWidth=5;x.beginPath();x.moveTo(Math.sin(a)*250,-Math.cos(a)*250);x.lineTo(Math.sin(a)*275,-Math.cos(a)*275);x.stroke()}
 const k=eio(V/1.4),a0=6/12*Math.PI*2,a1=a0-k*(2/12)*Math.PI*2;x.strokeStyle=K.amber;x.lineWidth=16;x.lineCap='round';x.beginPath();x.arc(0,0,305,a0-Math.PI/2,a1-Math.PI/2,true);x.stroke();
 x.lineWidth=12;x.beginPath();x.moveTo(0,0);x.lineTo(Math.sin(a1)*170,-Math.cos(a1)*170);x.stroke();x.restore();
 x.save();x.translate(W/2,620);x.scale(eb((V-0.4)/0.4),eb((V-0.4)/0.4));T('−2 H',0,10,'BS',210,K.amber);x.restore();
 for(let i=0;i<7;i++){const X=W/2-3*130+i*130,on=i<5,a=eo((V-1.6-i*0.08)/0.3);rr(X-50,1060,100,100,14);x.fillStyle=on?`rgba(229,72,77,${0.8*a})`:`rgba(242,237,228,${0.12*a})`;x.fill();T(String(i+1),X,1112,'GMB',40,on?K.bone:K.mut,{a})}
 T('menos de una semana de aviso',W/2,1240,'IS',62,K.bone,{a:eo((V-2.2)/0.4)})},
(lt,t)=>{const V=lt-PRE;court(W/2,520,150,K.bone);T('TRIBUNAL DE JUSTICIA DE LA UE',W/2,720,'GMB',32,K.mut,{ls:4,a:eo((V-0.5)/0.4)});T('Sentencia de 21-12-2021',W/2,770,'GM',28,K.mut,{a:eo((V-0.8)/0.4)});
 T('ADELANTO > 1 H',W/2,960,'BS',140,K.amber,{a:eo((V-1.6)/0.4)});T('=',W/2,1080,'BS',100,K.bone,{a:eo((V-2.3)/0.3)});stamp(W/2,1230,'CANCELACIÓN',K.red,V-3.0,120,-0.05)},
(lt,t)=>{const V=lt-PRE;T('AVISO < 7 DÍAS',W/2,330,'GMB',38,K.red,{ls:5,a:eo(V/0.4)});const tv=Math.round(400*eo((V-2.7)/0.8));const s=eb((V-2.6)/0.4);
 x.save();x.translate(W/2,720);x.scale(s,s);T(tv+' €',0,0,'BS',300,K.green);x.restore();T('por persona',W/2,930,'IS',70,K.bone,{a:eo((V-3.6)/0.4)});
 T('1.500–3.500 km  ·  art. 7 del Reglamento 261/2004',W/2,1080,'GM',28,K.mut,{a:eo((V-3.9)/0.4),ls:1});
 for(let i=0;i<14;i++){const st=2.8+R(i)*1.2;if(V>st){coin(100+R(i+11)*880,lerp(180,1600,Math.pow(cl((V-st)/1.2),1.7)),28,V*7+i,1-cl((V-st-1)/0.3))}}},
(lt,t)=>{const V=lt-PRE;T('ADEMÁS, TÚ ELIGES',W/2,330,'GMB',40,K.amber,{ls:6,a:eo(V/0.4)});option(W/2,700,'Reembolso','EN 7 DÍAS','coin',eo((V-1.2)/0.4));option(W/2,1130,'Otro vuelo','LO ANTES POSIBLE','plane',eo((V-2.2)/0.4))},
(lt,t)=>{const V=lt-PRE;cta(V,t,'GUARDA EL AVISO','con su fecha')}];
run(SC);
