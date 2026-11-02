from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # depo kökü (dil-psikolojisi-veri/)
EKA = ROOT / 'ek_a'
EXT, WORK, DER = EKA / 'data' / 'external', EKA / 'data' / 'work', EKA / 'data' / 'derived'
RES, FIG = EKA / 'results', EKA / 'figures'
WORK.mkdir(parents=True, exist_ok=True)
import json,logging,collections,math,re
logging.disable(logging.CRITICAL)
import zeyrek
an=zeyrek.MorphAnalyzer()
F={}
for line in open(EXT / 'frequencywords' / 'tr_full.txt',encoding='utf-8'):
    w,c=line.rsplit(' ',1); F[w]=int(c)
STEMS={'ev':['ev'],'köy':['köy'],'yol':['yol'],'okul':['okul'],'kitap':['kitap','kitab'],'kapı':['kapı'],'araba':['araba']}
out={}
for lem,pref in STEMS.items():
    cands=[w for w in F if any(w.startswith(p) for p in pref) and w.isalpha()]
    forms={}
    for w in cands:
        try: res=an.analyze(w)[0]
        except Exception: continue
        ok=[r for r in res if r.lemma==lem and r.pos=='Noun' and set(re.findall(r'\|[^:+|]*:?(\w+)→',r.formatted))<= {'Rel','o','Zero'}]
        if ok: forms[w]=F[w]
    toks=sum(forms.values()); fr=sorted(forms.values(),reverse=True)
    cum=0;k90=0
    for i,v in enumerate(fr):
        cum+=v
        if cum>=0.9*toks: k90=i+1;break
    low=sum(1 for v in fr if v<=2)
    out[lem]=dict(types=len(forms),tokens=toks,k90=k90,low=low,lowshare=low/len(forms),top=sorted(forms.items(),key=lambda x:-x[1])[:5],
                 maxsuf=max(forms,key=lambda w:len(w)))
    print(lem,len(cands),out[lem]['types'],toks,'k90',k90,'<=2',low,round(100*low/len(forms),1),out[lem]['top'][:3],out[lem]['maxsuf'])
json.dump(out,open(RES / 'a3_forms.json','w'),ensure_ascii=False,indent=1)
