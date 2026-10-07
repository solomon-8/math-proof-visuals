#!/usr/bin/env python3
"""Validate rendered streams, decoded frames, subtitles, and numerical examples."""
import hashlib, importlib.util, json, subprocess
from decimal import Decimal, getcontext
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];EP=ROOT/'episodes'/'017'
spec=importlib.util.spec_from_file_location('render',ROOT/'video'/'render.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
DATA=r.DATA;duration=sum(s['duration'] for s in DATA['scenes'])
getcontext().prec=65
pi=Decimal('3.1415926535897932384626433832795028841971693993751058209749445923078')
numerics=[]
for p,q in [(22,7),(355,113)]:
    e=abs(pi-Decimal(p)/q);assert 0<e<1/Decimal(q*q)
    numerics.append({'p':p,'q':q,'absolute_error':str(e),'q_squared_times_error':str(e*q*q)})
result={'status':'passed','duration_seconds':duration,'independent_formal_compilation':False,'proof_validity_certified':False,'audio':'intentionally absent; no narration synthesized','numbers':numerics,'streams':{},'subtitle_cues':{},'decode_tests':{},'frame_tests':{},'sha256':{}}
for lang in ['zh','en']:
    r.write_srt(lang)
    for s in DATA['scenes']:
        for text in s[lang]['subtitle']:
            lines=r.wrap(text,26,1090,lang=='zh');assert len(lines)<=3
            assert all(r.font(26,False,lang=='zh').getlength(x)<=1090 for x in lines)
        assert r.text_img(s[lang]['title'],38,'fg',True,lang=='zh').width<=1164
    result['subtitle_cues'][lang]=sum(len(s[lang]['subtitle']) for s in DATA['scenes'])
    path=EP/'renders'/f'017_pi_exponent_{lang}_review.mp4'
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    vid=[s for s in probe['streams'] if s['codec_type']=='video'];aud=[s for s in probe['streams'] if s['codec_type']=='audio']
    assert len(vid)==1 and not aud
    v=vid[0];assert v['width']==1280 and v['height']==720 and v['codec_name']=='h264' and v['pix_fmt']=='yuv420p'
    assert v['avg_frame_rate']=='24/1';assert int(v['nb_frames'])==duration*24
    assert abs(float(probe['format']['duration'])-duration)<.05
    result['streams'][lang]={k:v[k] for k in ['codec_name','width','height','pix_fmt','avg_frame_rate','nb_frames','duration']}
    p=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','null','-'],capture_output=True,text=True)
    assert p.returncode==0 and not p.stderr,(p.returncode,p.stderr)
    result['decode_tests'][lang]='all frames decoded without error'
    tests=[];gt=0
    for i,s in enumerate(DATA['scenes']):
        tt=gt+s['duration']*.63
        out=EP/'frames'/f'decoded_{lang}_{i+1:02d}_{s["id"]}.png'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(tt),'-i',str(path),'-frames:v','1',str(out)],check=True)
        im=Image.open(out);assert im.size==(1280,720)
        # Avoid a blank or wholly dark captured frame; math/labels are bright.
        assert im.convert('L').getextrema()[1]>220
        tests.append({'scene':s['id'],'time_seconds':tt,'size':[1280,720],'nonblank':True});gt+=s['duration']
    result['frame_tests'][lang]=tests
    result['sha256'][path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
(ROOT/'video'/'qa'/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
