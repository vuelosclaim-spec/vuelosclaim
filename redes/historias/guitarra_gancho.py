from PIL import Image, ImageDraw, ImageFont
F='/usr/share/fonts/opentype/inter/Inter-Bold.otf'; FB='/usr/share/fonts/opentype/inter/Inter-Black.otf'
import os
if not os.path.exists(FB): FB=F
W,H=1080,1920
def pill(d,cx,cy,txt,size=46):
    f=ImageFont.truetype(F,size); w=d.textlength(txt,font=f); pw,ph=w+80,size+44
    d.rounded_rectangle([cx-pw/2,cy-ph/2,cx+pw/2,cy+ph/2],radius=ph/2,fill='white')
    d.text((cx,cy),txt,font=f,fill='#0d6b3b',anchor='mm')
im=Image.new('RGB',(W,H),'#10221a'); d=ImageDraw.Draw(im)
f=ImageFont.truetype(FB,120)
y=640
for line in ['¿TE RECHAZAN','LA RECLAMACIÓN?']:
    ff=f
    while d.textlength(line,font=ff)>960: ff=ImageFont.truetype(FB,ff.size-4)
    d.text((W/2,y),line,font=ff,fill='white',anchor='mm'); y+=150
st=Image.new('RGBA',(820,220),(0,0,0,0)); sd=ImageDraw.Draw(st)
sd.rounded_rectangle([10,10,810,210],radius=24,outline='#e53935',width=14)
sd.text((410,112),'RECHAZADA',font=ImageFont.truetype(FB,108),fill='#e53935',anchor='mm')
st=st.rotate(-6,expand=True,resample=Image.BICUBIC)
im.paste(st,((W-st.width)//2,1060),st)
pill(d,W/2,1480,'Enlace en la bio ↑',56)
im.save('hook.png')
ov=Image.new('RGBA',(W,H),(0,0,0,0)); pill(ImageDraw.Draw(ov),W/2,1790,'Enlace en la bio ↑',40); ov.save('pill.png')
