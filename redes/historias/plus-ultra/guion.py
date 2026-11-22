import asyncio, edge_tts, os, json, subprocess
G = [
 (0, "¿Y si tu aerolínea deja de volar?", "¿Y si tu aerolínea deja de volar?"),
 (1, "Imagina: Carmen tiene billete con Plus Ultra.", "Imagina: Carmen tiene billete con Plus Ultra."),
 (1, "Madrid–Caracas, para pasar la Navidad con su madre.", "Madrid–Caracas, para pasar la Navidad con su madre."),
 (2, "Y un día le llega la noticia:", "Y un día le llega la noticia:"),
 (2, "Plus Ultra ha dejado de volar.", "Plus Ultra ha dejado de volar."),
 (2, "Miles de pasajeros se quedan sin vuelo.", "Miles de pasajeros se quedan sin vuelo."),
 (3, "¿Y su dinero? ¿Lo ha perdido?", "¿Y su dinero? ¿Lo ha perdido?"),
 (3, "No. Para la ley, su vuelo está cancelado.", "No. Para la ley, su vuelo está cancelado."),
 (4, "Carmen puede elegir el reembolso del billete en siete días,", "Carmen puede elegir el reembolso del billete en 7 días,"),
 (4, "u otro vuelo a Caracas lo antes posible.", "u otro vuelo a Caracas lo antes posible."),
 (5, "Y si la avisaron con menos de catorce días,", "Y si la avisaron con menos de 14 días,"),
 (5, "como el vuelo pasa de tres mil quinientos kilómetros,", "como el vuelo pasa de 3.500 kilómetros,"),
 (5, "pueden corresponderle seiscientos euros por pasajero.", "pueden corresponderle 600 euros por pasajero."),
 (6, "¿Y si la aerolínea no paga?", "¿Y si la aerolínea no paga?"),
 (6, "Reclama por escrito y guarda la respuesta.", "Reclama por escrito y guarda la respuesta."),
 (6, "Si compraste en una agencia, reclama también a la agencia.", "Si compraste en una agencia, reclama también a la agencia."),
 (6, "Si pagaste con tarjeta, pregunta a tu banco por la devolución del cargo.", "Si pagaste con tarjeta, pregunta a tu banco por la devolución del cargo."),
 (7, "Carmen reclamó por escrito ese mismo día,", "Carmen reclamó por escrito ese mismo día,"),
 (7, "y guardó el billete y todos los correos.", "y guardó el billete y todos los correos."),
 (8, "¿Tenías billete con Plus Ultra?", "¿Tenías billete con Plus Ultra?"),
 (8, "Cuéntalo en comentarios.", "Cuéntalo en comentarios."),
 (8, "Y calcula cuánto te corresponde en VuelosClaim punto eu.", "Y calcula cuánto te corresponde en VuelosClaim.eu"),
]
GAP=0.12; SCENE_GAP=0.35; LEAD=0.2
async def tts(text, f):
    c=edge_tts.Communicate(text,"es-ES-AlvaroNeural",rate="+6%",proxy=os.environ.get("HTTPS_PROXY"),boundary="WordBoundary")
    wb=[]
    with open(f+".mp3","wb") as o:
        async for ch in c.stream():
            if ch["type"]=="audio": o.write(ch["data"])
            elif ch["type"]=="WordBoundary": wb.append((ch["offset"]/1e7, ch["text"]))
    subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',f+'.mp3','-af','silenceremove=start_periods=1:start_threshold=-50dB','-ar','44100','-ac','1',f+'.wav'],check=True)
    d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f+'.wav'],capture_output=True,text=True).stdout)
    return d, wb
async def main():
    t=LEAD; segs=[]; prev=None
    for i,(sc,txt,sub) in enumerate(G):
        f=f'p_{i:02d}'; d,wb=await tts(txt,f)
        if prev is not None and sc!=prev: t+=SCENE_GAP
        words=sub.split(); off0=wb[0][0] if wb else 0
        if len(wb)==len(words): wt=[[w,round(t+max(0,o-off0),3)] for w,(o,_) in zip(words,wb)]
        else:
            span=max(0.3,d-0.1); L=[len(w)+2 for w in words]; tot=sum(L); acc=0; wt=[]
            for w,l in zip(words,L): wt.append([w,round(t+span*acc/tot,3)]); acc+=l
        segs.append({'sc':sc,'f':f+'.wav','start':round(t,3),'end':round(t+d,3),'words':wt})
        t+=d+GAP; prev=sc
    sc_={}
    for s in segs: sc_.setdefault(s['sc'],[s['start'],s['end']]); sc_[s['sc']][1]=s['end']
    L=sorted(sc_); bounds=[[sc,0 if k==0 else round((sc_[L[k-1]][1]+sc_[sc][0])/2,3)] for k,sc in enumerate(L)]
    total=round(segs[-1]['end']+2.4,3)
    json.dump({'segs':segs,'bounds':bounds,'total':total},open('timing.json','w'),ensure_ascii=False)
    # mix narration
    inputs=[];flt=[]
    for k,s in enumerate(segs): inputs+=['-i',s['f']]; flt.append(f'[{k}]adelay={int(s["start"]*1000)}|{int(s["start"]*1000)}[a{k}]')
    flt.append(''.join(f'[a{k}]' for k in range(len(segs)))+f'amix=inputs={len(segs)}:normalize=0,apad=whole_dur={total}[out]')
    subprocess.run(['ffmpeg','-nostdin','-v','error','-y',*inputs,'-filter_complex',';'.join(flt),'-map','[out]','-ar','44100','-ac','2','voz.wav'],check=True)
    print(total,bounds)
asyncio.run(main())
