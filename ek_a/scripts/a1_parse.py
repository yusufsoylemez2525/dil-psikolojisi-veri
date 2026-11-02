# A.1: CHILDES Türkçe (Aksu, Altınkamış/Türkay) çocuk ve yetişkin söyleyişlerinin biçim bilimsel çözümlemesi
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # depo kökü (dil-psikolojisi-veri/)
EKA = ROOT / 'ek_a'
EXT, WORK, DER = EKA / 'data' / 'external', EKA / 'data' / 'work', EKA / 'data' / 'derived'
RES, FIG = EKA / 'results', EKA / 'figures'
WORK.mkdir(parents=True, exist_ok=True)
AT = '\x40'  # CHAT başlık satırı ve özel biçim işareti (U+0040); depoda e-posta taraması kolay olsun diye kaçış diziyle yazılmıştır
import re,glob,json,logging,sys,collections
logging.disable(logging.CRITICAL)
import zeyrek
DATA=str(EXT / 'childes-tr')
def age_months(a):
    m=re.match(r'(\d+);(\d+)?',a); 
    return int(m.group(1))*12+int(m.group(2) or 0) if m else None
def clean(utt):
    if '[- ' in utt: return []
    u=re.sub(r'(\S+) \[: ([^\]]+)\]',r'\2',utt)          # telaffuz düzeltmesi: hedef biçim
    u=re.sub(r'\[::[^\]]*\]','',u)                      # hata işaretli: çocuğun biçimi kalır
    u=re.sub(r'\[[^\]]*\]','',u); u=u.replace('<','').replace('>','')
    toks=[]
    for w in u.split():
        if w.startswith(('&','+','0')) or AT in w: continue
        if w in ('xxx','yyy','www'): continue
        w=w.replace('(','').replace(')','').replace('_',' ')
        w=re.sub(r"[.,?!;:\"„‡“”…]+",'',w).strip().lower().replace('i̇','i')
        if not w or not re.search(r'[a-zçğıöşü]',w): continue
        toks.extend(w.split())
    return toks
rows=[]
errs=[]
for corpus in ['Aksu','Turkay']:
    for f in sorted(glob.glob(f'{DATA}/{corpus}/*.cha')):
        if f.endswith(('2haf.cha','6fb.cha')): continue  # yinelenen oturum ve konuşucu kodlaması bozuk dosya (Çöltekin README)
        txt=open(f,encoding='utf-8').read()
        pm=re.search(AT + r'Participants:\s*CHI\s+(\S+)',txt); cname=pm.group(1) if pm else f
        m=re.search(AT + r'ID:\s*tur\|[^|]*\|CHI\|([^|]*)\|',txt)
        age=age_months(m.group(1)) if m else None
        for line in re.findall(r'^\*([A-Z]{3}):\t(.*(?:\n\t.*)*)',txt,flags=re.M):
            spk,utt=line; utt=utt.replace('\n\t',' ')
            if spk=='CHI':
                for e in re.findall(r'(\S+) \[:: ([^\]]+)\]',utt): errs.append((corpus,f.split('/')[-1],age,e[0],e[1]))
            toks=clean(utt)
            if toks: rows.append({'corpus':corpus,'file':f.split('/')[-1],'age':age,'spk':spk,'toks':toks,'child':cname})
types=sorted({t for r in rows for t in r['toks']})
print('utt',len(rows),'types',len(types),file=sys.stderr)
# Zeyrek 0.1.3, aynı sözcük için aday çözümlemelerin sırasını ve kimi adayları Python'un karma tohumuna (PYTHONHASHSEED)
# bağlı olarak değiştirebilmektedir. Kitaptaki değerleri üreten çözümleme sözlüğü data/derived/a1_zeyrek_cozumlemeleri.json
# dosyasındadır ve öntanımlı olarak bu dosya kullanılır. Yeniden çözümleme için: A1_YENIDEN_COZUMLE=1 ortam değişkeni.
import os
CACHE_F=DER / 'a1_zeyrek_cozumlemeleri.json'
if CACHE_F.exists() and not os.environ.get('A1_YENIDEN_COZUMLE'):
    cache=json.load(open(CACHE_F,encoding='utf-8'))
    missing=[w for w in types if w not in cache]
    assert not missing, ('çözümleme sözlüğünde olmayan sözcükler', missing[:10])
    res={w:cache[w] for w in types}
    types=[]
    print('çözümleme sözlüğü kullanıldı:',CACHE_F.name,file=sys.stderr)
else: res={}
an=zeyrek.MorphAnalyzer()
for i,w in enumerate(types):
    try: a=an._analyze_word(w) if hasattr(an,'_analyze_word') else an.analyze(w)[0]
    except Exception: a=[]
    res[w]=[str(x.formatted) for x in a] if a else []
json.dump({'rows':rows,'ana':res,'errs':errs},open(WORK / 'a1_parsed.json','w'),ensure_ascii=False)
print('done',sum(1 for w in res if not res[w] or res[w]==['Unk']),'unknown',file=sys.stderr)
