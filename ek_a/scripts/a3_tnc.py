from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # depo kökü (dil-psikolojisi-veri/)
EKA = ROOT / 'ek_a'
EXT, WORK, DER = EKA / 'data' / 'external', EKA / 'data' / 'work', EKA / 'data' / 'derived'
RES, FIG = EKA / 'results', EKA / 'figures'
WORK.mkdir(parents=True, exist_ok=True)
import json,math
G=json.load(open(RES / 'a3_grid.json'))
TNC={'ev':[11959,1396,10084,8565,3057,433,908,844,417,367,22],'köy':[5049,404,1556,1516,800,33,593,263,56,23,3],'yol':[25973,1851,7916]+[None]*8}
NT=50678199; NO=G['N']
def spear(x,y):
    def rk(v):
        s=sorted(range(len(v)),key=lambda i:v[i]); r=[0]*len(v); i=0
        while i<len(v):
            j=i
            while j+1<len(v) and v[s[j+1]]==v[s[i]]: j+=1
            for k in range(i,j+1): r[k if False else s[k]]=(i+j)/2+1
            i=j+1
        return r
    a,b=rk(x),rk(y); n=len(a); ma=sum(a)/n; mb=sum(b)/n
    return sum((p-ma)*(q-mb) for p,q in zip(a,b))/ (sum((p-ma)**2 for p in a)*sum((q-mb)**2 for q in b))**.5
xs=[];ys=[]
for s,v in TNC.items():
    for j,t in enumerate(v):
        if t is None: continue
        xs.append(t/NT*1e6); ys.append(G['grid'][s][j]/NO*1e6)
print('n',len(xs),'spearman',round(spear(xs,ys),3))
lx=[math.log10(x) for x in xs]; ly=[math.log10(y) for y in ys]; n=len(lx); mx=sum(lx)/n; my=sum(ly)/n
r=sum((a-mx)*(b-my) for a,b in zip(lx,ly))/(sum((a-mx)**2 for a in lx)*sum((b-my)**2 for b in ly))**.5
print('pearson log',round(r,3))
for s in ['ev','köy']:
    print(s,[round(t/NT*1e6,2) for t in TNC[s]])
    print(s,'OS',[round(v/NO*1e6,2) for v in G['grid'][s]])
