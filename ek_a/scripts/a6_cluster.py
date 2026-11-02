# A.6 ek: hizalanma farkının çocuk düzeyinde kümelenmiş sınaması (son tur, Hakem II Z2)
# a6_align.py'deki oturum okuma ve ölçüler aynen kullanılır; çiftler aynı sırayla ve aynı tohumla (7) üretilir.
# a6_results.json'a dokunulmaz; çıktı a6_cluster_results.json.
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # depo kökü (dil-psikolojisi-veri/)
EKA = ROOT / 'ek_a'
EXT, WORK, DER = EKA / 'data' / 'external', EKA / 'data' / 'work', EKA / 'data' / 'derived'
RES, FIG = EKA / 'results', EKA / 'figures'
WORK.mkdir(parents=True, exist_ok=True)
import json,random,collections,math,re
src=open(Path(__file__).with_name('a6_align.py'),encoding='utf-8').read()
head=src.split("R = {'AC'")[0]
ns={'__file__': str(Path(__file__).with_name('a6_align.py'))}; exec(head,ns)
sessions,MEAS,K=ns['sessions'],ns['MEAS'],ns['K']
# dosya -> çocuk adı (a1_parsed.json; Altınkamış tek çocuk)
D=json.load(open(WORK / 'a1_parsed.json'))
f2c={r['file']:('Ozge' if r['corpus']=='Turkay' else r['child']) for r in D['rows']}
def run_pairs(direction,qfilter=None):
    src,tgt=('ADU','CHI') if direction=='AC' else ('CHI','ADU')
    P=[]
    for s in sessions:
        U=s['utts']; srcidx=[i for i,u in enumerate(U) if u['who']==src]
        for i,t in enumerate(U):
            if t['who']!=tgt: continue
            j=i-1
            if j<0: continue
            p=U[j]
            if p['who']!=src: continue
            if qfilter is not None and p['q']!=qfilter: continue
            far=[k for k in srcidx if abs(k-i)>=10]
            if len(far)<5: continue
            samp=random.sample(far,min(K,len(far)))
            for name,(ok,mt) in MEAS.items():
                if not ok(p,t): continue
                bs=[U[k] for k in samp if ok(U[k],t)]
                if not bs: continue
                pb=sum(mt(b,t) for b in bs)/len(bs)
                if name=='tam_dl': P.append((s['g'],f2c[s['file']],int(mt(p,t)),pb))
    return P
random.seed(7)
run_pairs('AC'); run_pairs('CA'); run_pairs('AC',True)   # a6_align.py ile aynı rastgele sıra
P=[p for p in run_pairs('AC',False) if not p[0].startswith('Alt')]
def stats(P,label):
    n=len(P); k=sum(p[2] for p in P); E=sum(p[3] for p in P); V=sum(p[3]*(1-p[3]) for p in P)
    z_ind=(k-E)/V**.5
    cl=collections.defaultdict(lambda:[0,0.0,0])
    for g,c,o,pb in P: cl[c][0]+=o; cl[c][1]+=pb; cl[c][2]+=1
    C=len(cl); res=[v[0]-v[1] for v in cl.values()]
    Vcl=C/(C-1)*sum(r*r for r in res)
    z_cl=(k-E)/Vcl**.5
    random.seed(11); keys=list(cl); bs=[]
    for _ in range(5000):
        smp=[cl[random.choice(keys)] for _ in keys]
        nn=sum(v[2] for v in smp); bs.append(100*(sum(v[0] for v in smp)-sum(v[1] for v in smp))/nn)
    bs.sort()
    return dict(label=label,pairs=n,children=C,obs=round(100*k/n,2),base=round(100*E/n,2),diff=round(100*(k-E)/n,2),
                z_independent=round(z_ind,2),z_cluster=round(z_cl,2),boot_ci95=[round(bs[124],1),round(bs[4874],1)])
out={'pooled':stats(P,'Aksu-Koç, üç kesit, soru olmayan yetişkin söyleyişinden sonra, gövde farklıyken ZGK eki')}
for g in ['Aksu-Koç 2;0-2;8','Aksu-Koç 3;0-3;8','Aksu-Koç 4;0-4;8']:
    out[g]=stats([p for p in P if p[0]==g],g)
out['note']='z_independent: çiftler bağımsız, Poisson-binom varyansı; z_cluster: çocuk düzeyinde kümeye dayanıklı (sandviç) varyans, C/(C-1) düzeltmesi; boot_ci95: çocuklar yerine koyarak 5.000 kez yeniden örneklenmiş fark (yüzde puan), tohum 11.'
json.dump(out,open(RES / 'a6_cluster_results.json','w'),ensure_ascii=False,indent=1)
for k,v in out.items(): print(k,v)
