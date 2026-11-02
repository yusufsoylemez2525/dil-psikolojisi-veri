# A.1 ek: fiil adacığı sınaması çocuk düzeyinde (son tur, Hakem II Z1)
# Her çocuğun fiil biçimleri yalnız o çocuğun kendi oturumlarındaki yetişkin girdisiyle karşılaştırılır.
# a1_analyze.py'deki info() ve group() aynen kullanılır; a1_results.json'a dokunulmaz.
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # depo kökü (dil-psikolojisi-veri/)
EKA = ROOT / 'ek_a'
EXT, WORK, DER = EKA / 'data' / 'external', EKA / 'data' / 'work', EKA / 'data' / 'derived'
RES, FIG = EKA / 'results', EKA / 'figures'
WORK.mkdir(parents=True, exist_ok=True)
import json,random,statistics as st,collections,math,sys,io,contextlib
src=open(Path(__file__).with_name('a1_analyze.py'),encoding='utf-8').read()
head=src.split("G=['Altınkamış")[0]   # yalnız tanımlar (parse, info, group)
ns={'__file__': str(Path(__file__).with_name('a1_analyze.py'))}; exec(head,ns)
rows,info,group=ns['rows'],ns['info'],ns['group']
G=['Altınkamış (1;4-2;4)','Aksu 2;0-2;8','Aksu 3;0-3;8','Aksu 4;0-4;8']
# Altınkamış derleminde ozge1.cha dosyasının Participants başlık satırında ad alanı "Ozge", ötekilerde "Target_Child"; ID satırı ve doğum tarihi aynı tek kız çocuk
def cid(r): return 'Ozge' if r['corpus']=='Turkay' else r['child']
def run(seed,NREP=500):
    random.seed(seed); out={}
    for g in G:
        sub=[r for r in rows if group(r)==g]
        kids=sorted({cid(r) for r in sub if r['spk']=='CHI'})
        pairs=[]; per_child={}
        for k in kids:
            files={r['file'] for r in sub if cid(r)==k}
            cv=collections.defaultdict(list); av=collections.defaultdict(list)
            for r in sub:
                if r['file'] not in files: continue
                d=cv if r['spk']=='CHI' else av
                for t in r['toks']:
                    i=info(t)
                    if i.get('verb'): d[i['lemma']].append(i['form'])
            pv=[]
            for lem,forms in cv.items():
                n=len(forms)
                if n>=4 and len(av.get(lem,[]))>=n:
                    ch=len(set(forms)); ad=st.mean(len(set(random.sample(av[lem],n))) for _ in range(NREP))
                    pv.append((k,lem,n,ch,ad))
            pairs+=pv
            if pv: per_child[k]=(st.mean(p[3] for p in pv),st.mean(p[4] for p in pv),len(pv))
        if not pairs: out[g]=None; continue
        diffs=[p[3]-p[4] for p in pairs]
        gt=sum(d>0 for d in diffs); lt=sum(d<0 for d in diffs)
        # işaret sınaması (iki yönlü, bağlar dışarıda)
        nn=gt+lt; ps=min(1,2*sum(math.comb(nn,i) for i in range(0,min(gt,lt)+1))/2**nn) if nn else None
        cg=sum(v[0]>v[1] for v in per_child.values()); cl=sum(v[0]<v[1] for v in per_child.values())
        out[g]=dict(children=len(per_child),pairs=len(pairs),child=st.mean(p[3] for p in pairs),adult=st.mean(p[4] for p in pairs),
                    diff=st.mean(diffs),gt=gt,lt=lt,sign_p=ps,children_gt=cg,children_lt=cl,
                    per_child={k:[round(a,3),round(b,3),n] for k,(a,b,n) in per_child.items()})
    return out
res={'seed1':run(1)}
# tohum duyarlılığı: girdi yeniden örneklemesindeki rastlantı
sens={g:[] for g in G}
for s in range(2,22):
    o=run(s,NREP=200)
    for g in G:
        if o[g]: sens[g].append(round(o[g]['adult'],3))
res['adult_mean_range_seeds2_21']={g:[min(v),max(v)] for g,v in sens.items() if v}
# Yayımlanan dosyada CHILDES'taki çocuk adları yerine kesit içi takma kimlikler (K01, K02, ...) kullanılır.
for g in G:
    r=res['seed1'][g]
    if r: r['per_child']={'K%02d'%(i+1):v for i,(k,v) in enumerate(sorted(r['per_child'].items()))}
res['note']='Çocuk düzeyi: her çocuk-fiil çifti yalnız o çocuğun oturumlarındaki yetişkin girdisiyle eşitlenir (ölçüt: çocukta en az 4 belirteç, girdide en az aynı sayı, 500 yineleme, tohum 1).'
json.dump(res,open(RES / 'a1_island_child_results.json','w'),ensure_ascii=False,indent=1)
for g in G:
    r=res['seed1'][g]
    if r: print(g,{k:(round(v,3) if isinstance(v,float) else v) for k,v in r.items() if k!='per_child'})
print(res['adult_mean_range_seeds2_21'])
