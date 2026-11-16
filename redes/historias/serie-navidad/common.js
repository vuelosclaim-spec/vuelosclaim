function card(X,Y,w,h,col){rr(X,Y,w,h,26);x.fillStyle=col||K.bone;x.fill()}
function voucher(cx,cy,s,val){x.save();x.translate(cx,cy);x.scale(s,s);x.rotate(-0.05);rr(-300,-150,600,300,24);const g=x.createLinearGradient(-300,-150,300,150);g.addColorStop(0,'#F5B700');g.addColorStop(1,'#F2EDE4');x.fillStyle=g;x.fill();
 x.setLineDash([10,10]);x.strokeStyle='#141414';x.lineWidth=3;rr(-280,-130,560,260,16);x.stroke();x.setLineDash([]);T('BONO',-250,-80,'GMB',40,'#141414',{al:'left',ls:8});T(val,0,30,'BS',150,'#141414');T('CANJEABLE EN VUELOS',0,110,'GM',22,'#3a3a3a',{ls:4});x.restore()}
function stamp(cx,cy,txt,col,p,sz,rot){if(p<=0)return;const s=lerp(2.6,1,eo(p/0.2));const sh=p<0.5?Math.sin(p*90)*12*(0.5-p):0;x.save();x.translate(cx+sh,cy);x.rotate(rot??-0.08);x.scale(s,s);x.font=`${sz}px BS`;const w=x.measureText(txt).width+80;
 x.strokeStyle=col;x.lineWidth=10;rr(-w/2,-sz*0.62,w,sz*1.24,22);x.stroke();T(txt,0,sz*0.05,'BS',sz,col);x.restore()}
function option(cx,cy,title,sub,kind,a){if(a<=0)return;x.save();x.globalAlpha*=a;x.translate(cx,cy+(1-a)*40);rr(-220,-170,440,340,30);x.fillStyle='rgba(61,214,140,.10)';x.fill();x.strokeStyle=K.green;x.lineWidth=3;x.stroke();
 if(kind=='plane')plane(0,-60,-0.3,70,K.bone);else coin(0,-60,62,0.2,1);T(title,0,60,'OUB',48,K.bone);T(sub,0,115,'GM',24,K.mut,{ls:2});x.restore()}
function cta(V,t,line1,line2){const a=eb(V/0.4);x.save();x.translate(W/2,560);x.scale(a,a);T(line1,0,0,'BS',130,K.bone);x.restore();if(line2)T(line2,W/2,700,'IS',64,K.amber,{a:eo((V-0.6)/0.4)});
 const c2=eb((V-1.2)/0.45),p=1+0.035*Math.sin(t*5)*cl(V-1.6);x.save();x.translate(W/2,1000);x.scale(c2*p,c2*p);rr(-400,-95,800,190,95);x.fillStyle=K.green;x.fill();T('Compruébalo gratis →',0,4,'OUB',66,'#06281A');x.restore();
 T('vuelosclaim.eu',W/2,1180,'GM',36,K.bone,{a:eo((V-1.8)/0.4),ls:3})}
function court(cx,cy,s,col){x.save();x.translate(cx,cy);x.fillStyle=col;x.beginPath();x.moveTo(-s,-s*0.45);x.lineTo(0,-s);x.lineTo(s,-s*0.45);x.closePath();x.fill();for(let i=0;i<5;i++){x.fillRect(-s*0.85+i*s*0.4,-s*0.38,s*0.16,s*0.95)}x.fillRect(-s*1.05,s*0.6,s*2.1,s*0.16);x.restore()}
