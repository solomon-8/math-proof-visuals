#!/usr/bin/env python3
"""Original vector-style mathematical animatic; Pillow + NumPy + FFmpeg.
No external network, source-repository modification, music, or voice cloning.
"""
from __future__ import annotations
import argparse, functools, io, json, math, os, subprocess
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR', '/tmp/math-explain-mpl')
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from matplotlib import mathtext, font_manager

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / 'episodes' / '017'
DATA = json.loads((EP / 'script.json').read_text())
W,H=1280,720
C={'bg':'#09131e','panel':'#102434','fg':'#eef3f4','muted':'#94acbd','teal':'#66e2ce','orange':'#ffbc7b','purple':'#bca5fa','line':'#294354','red':'#ff918a'}
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
CJK='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
CJK_BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def rgb(c):
    if isinstance(c, tuple): return c
    c=C.get(c,c).lstrip('#');return tuple(int(c[i:i+2],16) for i in (0,2,4))
def mix(a,b,t): return tuple(round(x+(y-x)*t) for x,y in zip(rgb(a),rgb(b)))
def ease(t): t=max(0,min(1,t));return t*t*(3-2*t)
@functools.lru_cache(256)
def font(size,bold=False,zh=False): return ImageFont.truetype(CJK_BOLD if zh and bold else CJK if zh else BOLD if bold else FONT,size,index=2 if zh else 0)
@functools.lru_cache(500)
def text_img(s,size=30,color='fg',bold=False,zh=False):
    f=font(size,bold,zh);box=f.getbbox(s)
    im=Image.new('RGBA',(max(1,box[2]-box[0]+4), max(1,box[3]-box[1]+5)))
    ImageDraw.Draw(im).text((2-box[0],2-box[1]),s,font=f,fill=rgb(color)+(255,))
    return im
@functools.lru_cache(200)
def formula_img(s,size=32,color='fg'):
    b=io.BytesIO(); mathtext.math_to_image('$'+s+'$',b,prop=font_manager.FontProperties(size=size,math_fontfamily='dejavusans'),dpi=100,format='png',color=C.get(color,color))
    im=Image.open(b).convert('RGBA')
    # Matplotlib emits an opaque white canvas; make it transparent without losing colored glyph antialiasing.
    arr=np.array(im); alpha=255-arr[:,:,:3].min(axis=2)
    target=np.array(rgb(color),dtype=float)
    # Reconstruct foreground color; alpha is relative to white and chosen color.
    max_delta=max(255-target.min(),1)
    alpha=np.clip(alpha.astype(float)*255/max_delta,0,255).astype('uint8')
    arr[:,:,:3]=target.astype('uint8');arr[:,:,3]=alpha
    return Image.fromarray(arr)

class Canvas:
    def __init__(self,im): self.im=im;self.d=ImageDraw.Draw(im)
    def text(self,s,x,y,size=30,color='fg',bold=False,zh=False,anchor='left',opacity=1):
        a=text_img(s,size,color,bold,zh)
        if anchor=='center':x-=a.width/2
        elif anchor=='right':x-=a.width
        if opacity<1:a=a.copy();a.putalpha(a.getchannel('A').point(lambda v:int(v*max(0,opacity))))
        self.im.alpha_composite(a,(round(x),round(y)))
    def formula(self,s,x,y,size=32,color='fg',anchor='center',opacity=1):
        a=formula_img(s,size,color)
        if anchor=='center':x-=a.width/2
        if opacity<1:a=a.copy();a.putalpha(a.getchannel('A').point(lambda v:int(v*max(0,opacity))))
        self.im.alpha_composite(a,(round(x),round(y)))
    def line(self,xy,color='line',width=2):self.d.line(xy,fill=rgb(color),width=width)
    def dot(self,x,y,r=5,color='teal'):self.d.ellipse((x-r,y-r,x+r,y+r),fill=rgb(color))
    def box(self,xy,color='panel',outline=None,r=18):self.d.rounded_rectangle(xy,radius=r,fill=rgb(color),outline=rgb(outline) if outline else None,width=2)
    def arrow(self,a,b,color='teal',width=3):
        self.line([a,b],color,width);ang=math.atan2(b[1]-a[1],b[0]-a[0]);l=10
        pts=[b,(b[0]-l*math.cos(ang-.5),b[1]-l*math.sin(ang-.5)),(b[0]-l*math.cos(ang+.5),b[1]-l*math.sin(ang+.5))]
        self.d.polygon(pts,fill=rgb(color))

Y,X=np.mgrid[0:H,0:W]; glow=np.maximum(0,1-np.sqrt(((X-650)/900)**2+((Y-280)/560)**2))
bg=np.zeros((H,W,3),dtype=np.uint8)
for i,(a,b) in enumerate(zip(rgb('bg'),(17,40,55))):bg[:,:,i]=a+(b-a)*glow
BG=Image.fromarray(bg).convert('RGBA')
d=ImageDraw.Draw(BG)
for x in range(0,W,64):d.line((x,0,x,H),fill=(17,34,46,255))
for y in range(0,H,64):d.line((0,y,W,y),fill=(17,34,46,255))

@functools.lru_cache(200)
def wrap(s,size=26,maxw=1090,zh=False,avoid_orphans=False):
    f=font(size,False,zh); units=list(s) if zh else s.split(' ');lines=[];cur=''
    for u in units:
        cand=cur+('' if zh or not cur else ' ')+u
        if f.getlength(cand)>maxw and cur:lines.append(cur);cur=u
        else:cur=cand
    if cur:lines.append(cur)
    if zh and avoid_orphans:
        # Keep closing punctuation and tiny trailing fragments with a clause.
        for i in range(1,len(lines)):
            if lines[i] and (lines[i][0] in '，。！？：；、）”》' or len(lines[i])<6):
                previous=lines[i-1]
                cuts=[j+1 for j,ch in enumerate(previous) if ch in '，。！？：；' and j>=len(previous)//2]
                cut=cuts[-1] if cuts else max(1,len(previous)-max(6-len(lines[i]),1))
                candidate=previous[cut:]+lines[i]
                if candidate and f.getlength(candidate)<=maxw:
                    lines[i-1]=previous[:cut];lines[i]=candidate
    return lines


def subtitle(c,scene,lang,t):
    subs=scene[lang]['subtitle']
    if scene.get('_cues'):
        active=next((cue for cue in scene['_cues'] if cue['start']<=t<cue['end']),None)
        displayed=subs[active['subtitle_index']] if active else ''
    else:
        idx=min(int(t/scene['duration']*len(subs)),len(subs)-1)
        displayed=subs[idx]
    lines=wrap(displayed,26,1090,lang=='zh',bool(scene.get('_cues')))
    assert len(lines)<=3,(scene['id'],lang,lines)
    c.box((58,562,1222,683),'#07111c',outline='#203546',r=14)
    y=578+(3-len(lines))*17
    for line in lines:c.text(line,640,y,size=26,zh=lang=='zh',anchor='center');y+=34


def header(c,scene,lang,index,t,global_t,total,voiced=False):
    zh=lang=='zh'
    c.text('017 / '+('数学可视化' if zh else 'MATHEMATICAL EXPLORATIONS'),58,25,16,'teal',True,zh)
    status=('未独立验证 · AI 合成旁白' if zh else 'NOT INDEPENDENTLY VERIFIED · AI NARRATION') if voiced else ('审稿样片 · 未独立验证 · 无配音' if zh else 'REVIEW COPY · NOT INDEPENDENTLY VERIFIED · NO VOICE')
    c.text(status,1222,27,14,'muted',False,zh,'right')
    c.text(scene[lang]['title'],58,77,38,'fg',True,zh)
    c.text(scene[lang]['label'],640,525,18,'muted',False,zh,'center')
    c.line([(58,701),(1222,701)],'line',3)
    c.line([(58,701),(58+1164*global_t/total,701)],'teal',3)
    c.text(f'{index+1:02d} / {len(DATA["scenes"]):02d}',1220,689,11,'muted',False,False,'right')


def scene_draw(c,s,lang,t,voiced=False):
    zh=lang=='zh';u=t/s['duration'];a=ease(min(t/2,1));sid=s['id']
    T=lambda en,zh_s:zh_s if zh else en
    if sid=='hook':
        cx,cy,r=288,330,115
        c.d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=rgb('line'),width=3)
        pts=[(cx+r*math.cos(-math.pi/2+k*2*math.pi/150),cy+r*math.sin(-math.pi/2+k*2*math.pi/150)) for k in range(int(150*ease(min(t/4,1)))+1)]
        if len(pts)>1:c.line(pts,'teal',5)
        c.formula(r'\pi',cx,278,72,'teal')
        c.formula(r'\pi\;\approx\;\frac{p}{q}',830,228,51)
        c.formula(r'\left|\pi-\frac{p}{q}\right|',860,342,36,'orange')
        c.text(T('error =','误差＝'),672,358,29,'orange',False,zh,anchor='right')
        c.text(T('a finite fraction · an infinite question','有限的分数，无穷的问题'),830,455,22,'muted',False,zh,'center')
    elif sid=='examples':
        for i,(p,q,err,col) in enumerate([(22,7,'0.001264489…','orange'),(355,113,'0.000000266764…','teal')]):
            y=186+i*154;c.box((65,y,1215,y+137))
            c.formula(r'\frac{%s}{%s}'%(p,q),162,y+20,37,col)
            c.text('q = '+str(q),165,y+91,18,'muted',False,False,'center')
            c.text(T('absolute error','绝对误差'),345,y+23,18,'muted',False,zh)
            c.text(err,345,y+62,34,col,True)
            x0=845;x1=1130;c.line([(x0,y+80),(x1,y+80)],'line',3)
            c.dot(x0,y+80,6,'fg');c.dot(x0+(x1-x0)*a,y+80,7,col)
            c.text('π',x0,y+42,22,'fg',False,False,'center')
            c.text(f'{p}/{q}',x1,y+42,22,col,False,False,'center')
            c.line([(x0,y+99),(x0+(x1-x0)*a,y+99)],col,2)
    elif sid=='scales':
        x0,y0,x1,y1=190,469,1100,194
        c.arrow((x0,y0),(1150,y0),'muted',2);c.arrow((x0,y0),(x0,160),'muted',2)
        xp=lambda v:x0+(x1-x0)*v/3
        yp=lambda v:y1-(y0-y1)*v/8
        for i in range(4):
            xx=xp(i);c.line([(xx,y0),(xx,y1)],'line',1);c.formula('10^{%s}'%i,xx,y0+12,16,'muted')
        for k in [0,-2,-4,-6,-8]:
            yy=yp(k);c.line([(x0,yy),(x1,yy)],'line',1);c.formula('10^{%s}'%k,x0-43,yy-10,15,'muted')
        a=ease(min(t/7,1))
        for exp,col in [(2,'teal'),(2.5,'purple')]:
            c.line([(xp(0),yp(0)),(xp(3*a),yp(-exp*3*a))],col,3)
            c.formula(r'q^{-%s}'%exp,1145,yp(-exp*3)-15,24,col)
            if t>7:
                scan=3*((t-7)/11);c.dot(xp(scan),yp(-exp*scan),5,col)
        for p,q,col in [(22,7,'orange'),(355,113,'orange')]:
            err=abs(math.pi-p/q);xx=xp(math.log10(q));yy=yp(math.log10(err))
            c.dot(xx,yy,7,col);c.text(f'{p}/{q}',xx+15,yy-15,22,col)
        c.text('q',1215,y0-12,23,'fg');c.text(T('error','误差'),90,160,20,'muted',False,zh)
    elif sid=='definition':
        c.formula(r'\mu(x)=\sup\left\{\nu>0:\;0<\left|x-\frac{p}{q}\right|<q^{-\nu}\right\}',640,189,32)
        c.text(T('for infinitely many reduced fractions','对无穷多个约分后的分数成立'),640,280,27,'teal',True,zh,'center')
        c.arrow((210,408),(1070,408),'line',3)
        count=15
        for i in range(count):
            x=230+i*52;frac=(i+1)/count
            if frac<min(1,u*2+.2):c.dot(x,408,5+2*math.sin(t+i),'teal')
        c.text('…',1105,383,43,'teal')
        c.text(T('one good fraction','一个好分数'),270,455,23,'orange',False,zh,'center')
        c.text(T('an infinite pattern','无穷多个的规律'),880,455,23,'teal',False,zh,'center')
    elif sid=='pigeonhole':
        N=8;x0,x1,yy=135,1145,220
        for i in range(N):c.box((x0+i*(x1-x0)/N,yy,x0+(i+1)*(x1-x0)/N-5,yy+76),'panel','line',8)
        alpha=math.sqrt(2);vals=[(j*alpha)%1 for j in range(N+1)];bucket={}
        pair=None
        for j,v in enumerate(vals):
            b=int(v*N)
            if b in bucket:pair=(bucket[b],j)
            else:bucket[b]=j
        for j,v in enumerate(vals):
            if j<=int(ease(min(t/7,1))*N):
                col='orange' if pair and j in pair else 'teal';xx=x0+v*(x1-x0)
                c.dot(xx,yy+38,6,col);c.text(str(j),xx,yy+9 if j%2==0 else yy+55,15,col,False,False,'center')
        c.text(T('N boxes, N + 1 fractional parts','N 个格子，N＋1 个小数部分'),640,157,24,'muted',False,zh,'center')
        c.formula(r'1\leq q\leq N,\qquad |qx-p|<\frac{1}{N}',640,334,31,'orange',opacity=ease((t-4)/2))
        c.formula(r'\left|x-\frac{p}{q}\right|<\frac{1}{qN}\leq\frac{1}{q^2}',640,414,36,'teal',opacity=ease((t-10)/2))
        c.text(T('Illustration: N = 8, x = √2','图示：N＝8，x＝√2'),1180,313,14,'muted',False,zh,'right')
    elif sid=='quantifiers':
        steps=[(r'\forall\,\nu>2',T('choose an exponent','任选指数')),(r'\exists\,Q=Q(\nu)\geq2',T('a dependent threshold','存在依赖 ν 的阈值')),(r'\forall\,p,q\in\mathbb{Z},\;q\geq Q',T('every numerator; large denominators','所有分子；足够大的分母'))]
        for i,(f,label) in enumerate(steps):
            xx=248+i*395;c.box((65+i*395,174,430+i*395,312),outline='teal' if int(t//8)==i else 'line')
            c.formula(f,xx,196,25,'teal' if i==0 else 'orange' if i==1 else 'fg',opacity=ease((t-i*3)/1))
            c.text(label,xx,268,18,'muted',False,zh,'center')
            if i<2:c.arrow((439+i*395,245),(450+i*395,245),'muted',2)
        c.formula(r'\left|\pi-\frac{p}{q}\right|\;\geq\;q^{-\nu}',640,345,49,'teal',opacity=ease((t-8)/1))
        c.text(T('Q is not an explicit numerical cutoff here','这里的 Q，不是已给出的具体数值'),640,465,23,'orange',False,zh,'center')
    elif sid=='caveat':
        c.box((70,183,605,474));c.box((635,183,1210,474))
        c.formula(r'\left|\pi-\frac{355}{113}\right|<\frac{1}{113^2}',336,226,31,'orange')
        c.text(T('q² × error ≈ 0.003406 < 1','q² × 误差 ≈ 0.003406 < 1'),335,323,22,'fg',False,zh,'center')
        c.text(T('A concrete counterexample','一个具体反例'),335,401,23,'orange',True,zh,'center')
        c.formula(r'\nu>2\quad\neq\quad\nu=2',920,226,34,'teal')
        c.text(T('Every ν has its own Q','每个 ν，可以有自己的 Q'),920,323,23,'fg',False,zh,'center')
        c.text(T('No uniform c/q² conclusion','不能推出统一的 c／q² 下界'),920,401,23,'muted',False,zh,'center')
    elif sid=='roadmap':
        labels=[(T('exceptional fractions','超常的好近似'),r'\left|\pi-\frac{p_i}{q_i}\right|<q_i^{-\nu}'),(T('separated scales','分离的尺度'),r'q_1\ll q_2\ll\cdots'),(T('interpolation','多变量插值'),r'\det M\neq0')]
        for i,(title,f) in enumerate(labels):
            xx=240+i*400;c.box((65+i*400,235,415+i*400,420),outline='line')
            c.text(title,xx,259,23,'muted',False,zh,'center');c.formula(f,xx,327,27,'teal' if i==2 else 'orange')
            if i<2:
                c.arrow((427+i*400,327),(452+i*400,327),'teal',3)
                c.dot(428+i*400+23*((t/2)%1),327,5,'orange')
        c.text(T('Assume one fixed ν > 2 works for unbounded q','假设一个固定的 ν > 2，允许无界的好分母 q'),640,165,23,'fg',False,zh,'center')
    elif sid=='determinant':
        c.formula(r'D\cdot\det M\in\mathbb{Z}[i]\setminus\{0\}',365,178,30)
        c.formula(r'|\det M|\geq\frac{1}{D}',365,263,36,'orange')
        c.text(T('arithmetic lower bound','算术下界'),365,351,24,'orange',False,zh,'center')
        c.formula(r'|\det M|<\frac{1}{D}',952,263,36,'teal')
        c.text(T('claimed analytic upper bound','论文声称的解析上界'),952,351,24,'teal',False,zh,'center')
        xx=640; y=440;c.line([(190,y),(1090,y)],'line',3)
        cut=650;c.line([(cut,y-36),(cut,y+28)],'orange',3);c.formula(r'1/D',cut,y+38,23,'orange')
        c.arrow((1060,y),(cut+25,y),'orange',5)
        c.arrow((220,y),(cut-25,y),'teal',5)
        c.text(T('no overlap','没有交集'),640,198,21,'red',True,zh,'center')
        dotx=1040-475*ease((t-3)/13);c.dot(dotx,y-21,8,'teal')
    elif sid=='bottleneck':
        cx,cy=280,300
        entries=[[1,2,3],[2,4,6]] if t<9 else [[1,2,3],[1,2,3]]
        for i,row in enumerate(entries):
            for j,v in enumerate(row):c.text(str(v),cx+j*80,cy+i*65,39,'orange',False,False,'center')
        if t>=9:c.text(T('row 2 ÷ 2','第 2 行 ÷ 2'),570,379,18,'teal',False,zh,'center')
        c.line([(235,280),(219,280),(219,417),(235,417)],'muted',2);c.line([(491,280),(507,280),(507,417),(491,417)],'muted',2)
        c.text(T('3 unknowns · 2 constraints','3 个未知数 · 2 个约束'),365,199,24,'muted',False,zh,'center')
        c.text(T('rank = 1, not 2','秩为 1，而不是 2'),365,455,24,'orange',True,zh,'center')
        c.box((660,215,1170,462),outline='line')
        c.text(T('The crucial extra theorem','必须额外证明'),915,241,25,'fg',True,zh,'center')
        c.text(T('full rank at special centers','特殊中心处的满秩性'),915,309,26,'teal',False,zh,'center')
        c.text(T('thresholds independent of centers','阈值不依赖中心位置'),915,375,23,'teal',False,zh,'center')
    elif sid=='status':
        rows=[(T('Checked','已检查'),T('displayed statement + quantifiers','所展示命题与量词'),'teal'),(T('Not run','未执行'),T('independent Lean compilation','独立 Lean 编译'),'orange'),(T('Not established','未确立'),T('full proof validity / peer-review acceptance','整份证明正确性／同行评审认可'),'muted')]
        for i,(l,r,col) in enumerate(rows):
            yy=187+i*103;c.box((105,yy,1175,yy+83),outline='line');c.dot(145,yy+41,6,col)
            c.text(l,175,yy+25,23,col,True,zh);c.text(r,515,yy+25,23,'fg',False,zh)
    elif sid=='outro':
        c.text(T('REPOSITORY CLAIM','仓库主张'),640,157,17,'orange',True,zh,'center')
        c.formula(r'\mu(\pi)=2',640,197,50,'teal')
        c.text(T('Every exponent above 2. Eventually.','每个大于 2 的指数，都有一个“从此以后”。'),640,298,31,'fg',True,zh,'center')
        c.text(T('Source: openai/math · OpenAI · 24 September 2026','来源：openai/math · OpenAI · 2026 年 9 月 24 日'),640,399,20,'muted',False,zh,'center')
        credit=T('Original visual explanation · AI-synthesized narration','原创视觉讲解 · AI 合成旁白') if voiced else T('Original visual explanation · subtitle-only review copy','原创视觉讲解 · 无配音审稿样片')
        c.text(credit,640,446,21,'orange',False,zh,'center')


def frame(scene,lang,t,index,global_t,total,voiced=False):
    im=BG.copy();c=Canvas(im);header(c,scene,lang,index,t,global_t,total,voiced)
    visual_scene=scene
    visual_t=t
    if voiced and scene.get('_review_duration'):
        visual_scene=dict(scene,duration=scene['_review_duration'])
        visual_t=t/scene['duration']*scene['_review_duration']
    scene_draw(c,visual_scene,lang,visual_t,voiced);subtitle(c,scene,lang,t)
    if not voiced:
        fade=min(ease(t/.45),ease((scene['duration']-t)/.45))
        if fade<1:im=Image.blend(BG,im,fade)
    return im.convert('RGB')

def srt_time(t):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
def write_srt(lang):
    t=0;rows=[];i=1
    for s in DATA['scenes']:
        subs=s[lang]['subtitle'];dur=s['duration']/len(subs)
        for sub in subs:
            rows.append(f'{i}\n{srt_time(t)} --> {srt_time(t+dur)}\n{sub}\n');i+=1;t+=dur
    (EP/'subtitles'/f'017.{lang}.srt').write_text('\n'.join(rows))

def render(lang,fps=24,only_frames=False):
    total=sum(s['duration'] for s in DATA['scenes']);out=EP/'renders'/f'017_pi_exponent_{lang}_review.mp4'
    write_srt(lang)
    if not only_frames:
        cmd=['ffmpeg','-y','-hide_banner','-loglevel','warning','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart','-metadata',f'title=Episode 017 ({lang}) - subtitle-only review animatic','-metadata','comment=Repository claim; not independently compiled or fully verified. Original visuals; no narration.',str(out)]
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    gt=0
    for k,s in enumerate(DATA['scenes']):
        mid=s['duration']*.63
        im=frame(s,lang,mid,k,gt+mid,total);im.save(EP/'frames'/f'{lang}_{k+1:02d}_{s["id"]}.png')
        if not only_frames:
            for j in range(round(s['duration']*fps)):
                im=frame(s,lang,j/fps,k,gt+j/fps,total);proc.stdin.write(im.tobytes())
        print(f'{lang}: scene {k+1}/{len(DATA["scenes"])} {s["id"]}',flush=True);gt+=s['duration']
    # Useful poster deliberately avoids presenting the claim as established fact.
    im=frame(DATA['scenes'][0],lang,7,0,7,total);im.save(EP/'renders'/f'017_{lang}_cover.png')
    if not only_frames:
        proc.stdin.close();code=proc.wait()
        if code:raise RuntimeError(f'ffmpeg exited {code}')
        print(out,flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--language',choices=['en','zh','both'],default='both');ap.add_argument('--fps',type=int,default=24);ap.add_argument('--frames-only',action='store_true');args=ap.parse_args()
    for lang in (['zh','en'] if args.language=='both' else [args.language]):render(lang,args.fps,args.frames_only)
