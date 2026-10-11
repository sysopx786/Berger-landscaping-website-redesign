# Usage: edit src (folder with photos + manifest.csv) and out, then run.
import glob,os,csv,json
from PIL import Image,ImageOps,ImageEnhance
src='/home/claude/zipx'; out='/home/claude/site/img'
rows=list(csv.DictReader(open(src+'/manifest.csv')))
meta=[]
for r in rows:
    f=r['web_file']; base=f.rsplit('-src',1)[0]  # berger-beds-01
    im=ImageOps.exif_transpose(Image.open(os.path.join(src,f))).convert('RGB')
    # subtle cool grade: slight desat + tiny blue lift
    im=ImageEnhance.Color(im).enhance(0.92)
    r_,g_,b_=im.split(); b_=b_.point(lambda v:min(255,int(v*1.02+2))); r_=r_.point(lambda v:int(v*0.985))
    im=Image.merge('RGB',(r_,g_,b_))
    w,h=im.size
    for W in (640,1280):
        t=im.copy(); t.thumbnail((W,W))
        t.save(f'{out}/{base}-{W}.webp','WEBP',quality=74,method=6)
    t=im.copy(); t.thumbnail((1024,1024)); t.save(f'{out}/{base}-1024.jpg','JPEG',quality=78,optimize=True,progressive=True)
    t2=im.copy(); t2.thumbnail((1280,1280))
    meta.append(dict(id=base,cat=r['category'],w=t2.width,h=t2.height,alt=r['alt_text'],orig=r['original_file']))
json.dump(meta,open('photos.json','w'),indent=1)
print(len(meta))
