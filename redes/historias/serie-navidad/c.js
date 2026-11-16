timeline([6.747,2.319,7.314,6.436,3.44],[0.35,0.35,0.5,0.5,0.9]);
const SC=[
(lt,t)=>{const V=lt-PRE;rr(60,250,960,360,26);x.fillStyle='rgba(5,8,15,.75)';x.fill();x.strokeStyle='rgba(245,183,0,.35)';x.lineWidth=2;x.stroke();
 T('SALIDAS',100,300,'GMB',28,K.amber,{al:'left',ls:6});T('DEPARTURES',980,300,'GM',24,K.mut,{al:'right',ls:6});flap('MADRID',100,340,52,80,lt*2.2,K.bone,1);T('→',470,380,'GMB',54,K.amber);flap('PARIS',530,340,52,80,lt*2.2-0.2,K.bone,7);
 const bl=V>1.9&&Math.floor(t*3)%2==0;flap('CANCELADO',100,470,52,80,lt*2.4,bl?'#6B1D20':K.red,40);
 big2('¿BONO','O DINERO?',820,K.bone,K.amber,190,eb((lt-0.3)/0.5));const a=eo((V-5.5)/0.5);if(a>0)voucher(W/2,1250+(1-a)*400,0.9,'100 €')},
(lt,t)=>{const V=lt-PRE;voucher(W/2,620,1.05+0.03*Math.sin(t*4),'100 €');const a=eb((V-1.0)/0.35);x.save();x.translate(W/2,1080);x.scale(a,a);x.fillStyle=K.amber;x.beginPath();x.moveTo(0,-130);x.lineTo(140,110);x.lineTo(-140,110);x.closePath();x.fill();T('!',0,30,'BS',170,'#141414');x.restore();T('PERO OJO',W/2,1300,'BS',120,K.amber,{a:eo((V-1.2)/0.3)})},
(lt,t)=>{const V=lt-PRE;T('SIN CIRCUNSTANCIAS EXTRAORDINARIAS',W/2,330,'GMB',32,K.mut,{ls:3,a:eo(V/0.4)});const tv=Math.round(250*eo((V-3.9)/0.8)),s=eb((V-3.8)/0.4);
 x.save();x.translate(W/2,700);x.scale(s,s);T(tv+' €',0,0,'BS',300,K.green);x.restore();T('por persona · hasta 1.500 km',W/2,900,'IS',60,K.bone,{a:eo((V-4.8)/0.4)});
 stamp(W/2,1150,'EN DINERO',K.green,V-6.5,110,-0.06);for(let i=0;i<16;i++){const st=6.5+R(i)*0.8;if(V>st){coin(100+R(i+3)*880,lerp(180,1600,Math.pow(cl((V-st)/1.1),1.7)),28,V*7+i,1-cl((V-st-0.9)/0.3))}}},
(lt,t)=>{const V=lt-PRE;voucher(W/2,480,0.8,'100 €');stamp(W/2,760,'SOLO SI TÚ LO ACEPTAS',K.red,V-1.0,80,-0.04);T('Art. 7.3 del Reglamento 261/2004',W/2,900,'GM',26,K.mut,{a:eo((V-1.6)/0.4),ls:2});
 option(W/2-235,1220,'Reembolso','O BIEN','coin',eo((V-4.4)/0.4));option(W/2+235,1220,'Otro vuelo','A TU ELECCIÓN','plane',eo((V-5.6)/0.4))},
(lt,t)=>{const V=lt-PRE;cta(V,t,'NO FIRMES NADA','sin comprobarlo antes')}];
run(SC);
