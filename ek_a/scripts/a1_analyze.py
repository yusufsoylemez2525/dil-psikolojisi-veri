from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # depo kökü (dil-psikolojisi-veri/)
EKA = ROOT / 'ek_a'
EXT, WORK, DER = EKA / 'data' / 'external', EKA / 'data' / 'work', EKA / 'data' / 'derived'
RES, FIG = EKA / 'results', EKA / 'figures'
WORK.mkdir(parents=True, exist_ok=True)
import json,re,random,collections,statistics as st
D=json.load(open(WORK / 'a1_parsed.json'))
rows,ANA,errs=D['rows'],D['ana'],D['errs']
TAM={'Past','Narr','Prog1','Prog2','Fut','Aor','Imp','Opt','Neces','Cond','Desr'}
CASE={'Acc','Dat','Loc','Abl','Gen','Ins'}
def parse(fmt):
    m=re.match(r'\[([^:]+):([^\]]+)\]\s*(.*)$',fmt)
    if not m: return None
    lemma,pos,body=m.groups()
    groups=body.split('|')
    final=groups[-1]
    segs=re.split(r'[+]',body.replace('|','+'))
    tags=[];overt=0
    for s in segs:
        if ':' in s:
            surf,tag=s.split(':',1); tag=tag.split('→')[0]; tags.append(tag)
            if surf: overt+=1
        else: tags.append(s.split('→')[0])
    fpos=pos
    der=re.findall(r'→(\w+)',body)
    if der: fpos=der[-1]
    return {'lemma':lemma,'pos':pos,'fpos':fpos,'nder':body.count('|'),'tags':tags,'overt':overt-1,'body':body}
CACHE={}
def info(w):
    if w in CACHE: return CACHE[w]
    cands=[parse(f) for f in ANA.get(w,[]) if f!='Unk']
    cands=[c for c in cands if c]
    r={'known':bool(cands)}
    if cands:
        mn=min(c['nder'] for c in cands); cc=[c for c in cands if c['nder']==mn]
        # fiil
        if all(c['fpos']=='Verb' and c['nder']==0 for c in cc):
            tams={tuple(sorted(set(c['tags'])&TAM)) for c in cc}
            lem={c['lemma'] for c in cc}
            if len(tams)==1 and len(lem)==1 and list(tams)[0]:
                r.update(verb=True,lemma=lem.pop(),tam='+'.join(list(tams)[0]),
                         form='+'.join(t for t in cc[0]['tags'][1:] ),overt=cc[0]['overt'])
        if all(c['fpos']=='Noun' for c in cc):
            cases={tuple(sorted(set(c['tags'])&CASE)) for c in cc}
            if len(cases)==1: r['case']=('+'.join(list(cases)[0]) or 'Nom')
        r['overt_word']=min(c['overt'] for c in cc)
    CACHE[w]=r; return r
def group(r):
    if r['corpus']=='Turkay': return 'Altınkamış (1;4-2;4)'
    a=r['age']; 
    return 'Aksu 2;0-2;8' if a<36 else ('Aksu 3;0-3;8' if a<48 else 'Aksu 4;0-4;8')
G=['Altınkamış (1;4-2;4)','Aksu 2;0-2;8','Aksu 3;0-3;8','Aksu 4;0-4;8']
out={}
random.seed(1)
def spearman(x,y):
    def rk(v):
        s=sorted(range(len(v)),key=lambda i:v[i]); r=[0]*len(v); i=0
        while i<len(v):
            j=i
            while j+1<len(v) and v[s[j+1]]==v[s[i]]: j+=1
            for k in range(i,j+1): r[s[k]]=(i+j)/2+1
            i=j+1
        return r
    a,b=rk(x),rk(y); ma,mb=st.mean(a),st.mean(b)
    num=sum((p-ma)*(q-mb) for p,q in zip(a,b)); den=(sum((p-ma)**2 for p in a)*sum((q-mb)**2 for q in b))**.5
    return num/den if den else float('nan')
TAMS=['Prog1','Past','Narr','Aor','Fut','Imp','Opt']
CASES=['Nom','Acc','Dat','Loc','Abl','Gen','Ins']
for g in G:
    sub=[r for r in rows if group(r)==g]
    res={}
    for who in ['CHI','ADU']:
        R=[r for r in sub if (r['spk']=='CHI')==(who=='CHI')]
        toks=[t for r in R for t in r['toks']]
        I=[info(t) for t in toks]
        verbs=[(t,i) for t,i in zip(toks,I) if i.get('verb')]
        tamc=collections.Counter(); 
        for t,i in verbs:
            for x in i['tam'].split('+'): tamc[x]+=1
        casec=collections.Counter(i['case'] for i in I if 'case' in i)
        mlu_w=len(toks)/len(R)
        morph=sum(1+i.get('overt_word',0) for i in I if i['known'])/max(1,sum(1 for i in I if i['known']))
        res[who]=dict(children=len({r['child'] for r in R}),files=len({r['file'] for r in R}),utts=len(R),tokens=len(toks),known=sum(i['known'] for i in I)/len(I),mlu_w=mlu_w,morph_per_word=morph,
            verb_tokens=len(verbs),verb_lemmas=len({i['lemma'] for t,i in verbs}),
            overt_per_verb=st.mean(i['overt'] for t,i in verbs) if verbs else 0,
            tam={k:tamc[k] for k in TAMS},case={k:casec[k] for k in CASES},
            tam_types=sum(1 for k in TAMS if tamc[k]>0))
        res[who]['_verbs']=collections.defaultdict(list)
        for t,i in verbs: res[who]['_verbs'][i['lemma']].append(i['form'])
    # girdiyle ilişki
    c,a=res['CHI'],res['ADU']
    res['rho_tam']=spearman([c['tam'][k] for k in TAMS],[a['tam'][k] for k in TAMS])
    res['rho_case']=spearman([c['case'][k] for k in CASES],[a['case'][k] for k in CASES])
    # fiil adacığı testi: çocukta >=4 belirteç alan fiiller, yetişkinden aynı sayıda örneklem
    cv,av=c['_verbs'],a['_verbs']; vals=[]
    for lem,forms in cv.items():
        n=len(forms)
        if n>=4 and len(av.get(lem,[]))>=n:
            ch=len(set(forms))
            ad=st.mean(len(set(random.sample(av[lem],n))) for _ in range(500))
            vals.append((lem,n,ch,ad))
    res['island']=dict(nverbs=len(vals),child=st.mean(v[2] for v in vals) if vals else None,adult=st.mean(v[3] for v in vals) if vals else None,
                       ratio=(sum(v[2] for v in vals)/sum(v[3] for v in vals)) if vals else None, verbs=sorted(vals,key=lambda v:-v[1])[:8])
    for who in ['CHI','ADU']: del res[who]['_verbs']
    out[g]=res
# Hata işaretli biçimler CHILDES çeviri yazısından alınan sözcükler olduğundan yayımlanan sonuç dosyasına yazılmaz,
# yalnız yerel çalışma klasörüne (data/work, depoya girmez) yazılır.
json.dump(errs,open(WORK / 'a1_hata_bicimleri.json','w'),ensure_ascii=False,indent=1)
json.dump(out,open(RES / 'a1_results.json','w'),ensure_ascii=False,indent=1)
for g in G:
    r=out[g]; c,a=r['CHI'],r['ADU']
    print(f"\n== {g}")
    print(f" çocuk({c['children']} çocuk, {c['files']} dosya): söyleyiş {c['utts']}, sözcük {c['tokens']}, tanınan %{100*c['known']:.0f}, MLUw {c['mlu_w']:.2f}, biçim/sözcük {c['morph_per_word']:.2f}, fiil {c['verb_tokens']}/{c['verb_lemmas']} lemma, ek/fiil {c['overt_per_verb']:.2f}, ZGK türü {c['tam_types']}")
    print(f" yetişkin: söyleyiş {a['utts']}, sözcük {a['tokens']}, tanınan %{100*a['known']:.0f}, MLUw {a['mlu_w']:.2f}, biçim/sözcük {a['morph_per_word']:.2f}, fiil {a['verb_tokens']}/{a['verb_lemmas']}, ek/fiil {a['overt_per_verb']:.2f}, ZGK türü {a['tam_types']}")
    print(' TAM ç',c['tam']); print(' TAM y',a['tam']); print(' CASE ç',c['case']); print(' CASE y',a['case'])
    print(f" rho TAM {r['rho_tam']:.2f} rho CASE {r['rho_case']:.2f}  island {r['island']['nverbs']} fiil, çocuk {r['island']['child']}, yetişkin {r['island']['adult']}, oran {r['island']['ratio']}")
    print('  ', [(v[0],v[1],v[2],round(v[3],1)) for v in r['island']['verbs']])
print('\nhatalar',len(errs)); [print(' ',e) for e in errs]
