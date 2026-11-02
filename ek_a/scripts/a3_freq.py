from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # depo kökü (dil-psikolojisi-veri/)
EKA = ROOT / 'ek_a'
EXT, WORK, DER = EKA / 'data' / 'external', EKA / 'data' / 'work', EKA / 'data' / 'derived'
RES, FIG = EKA / 'results', EKA / 'figures'
WORK.mkdir(parents=True, exist_ok=True)
import json,re,math,collections,logging,statistics as st
logging.disable(logging.CRITICAL)
F={}
for line in open(EXT / 'frequencywords' / 'tr_full.txt',encoding='utf-8'):
    w,c=line.rsplit(' ',1); F[w]=int(c)
N=sum(F.values()); print('token',N,'type',len(F))
P={
 'ev':['ev','evler','eve','evde','evden','evim','evlerde','evlerinde','evimiz','evimde','evlerimizden'],
 'köy':['köy','köyler','köye','köyde','köyden','köyüm','köylerde','köylerinde','köyümüz','köyümde','köylerimizden'],
 'yol':['yol','yollar','yola','yolda','yoldan','yolum','yollarda','yollarında','yolumuz','yolumda','yollarımızdan'],
 'okul':['okul','okullar','okula','okulda','okuldan','okulum','okullarda','okullarında','okulumuz','okulumda','okullarımızdan'],
 'kitap':['kitap','kitaplar','kitaba','kitapta','kitaptan','kitabım','kitaplarda','kitaplarında','kitabımız','kitabımda','kitaplarımızdan'],
 'kapı':['kapı','kapılar','kapıya','kapıda','kapıdan','kapım','kapılarda','kapılarında','kapımız','kapımda','kapılarımızdan'],
 'araba':['araba','arabalar','arabaya','arabada','arabadan','arabam','arabalarda','arabalarında','arabamız','arabamda','arabalarımızdan']}
CELLS=['yalın','-lAr','-(y)A','-DA','-DAn','-(I)m','-lArDA','-lArIndA','-(I)mIz','-(I)mDA','-lArImIzDAn']
NSUF=[0,1,1,1,1,1,2,3,1,2,4]
grid={s:[F.get(f,0) for f in fs] for s,fs in P.items()}
for s in grid: print(s,grid[s])
# toplam log modeli: log(f+1) = kök + hücre
import itertools
Y=[[math.log10(v+1) for v in grid[s]] for s in P]
S=len(Y); C=len(CELLS); gm=st.mean(v for r in Y for v in r)
rm=[st.mean(r) for r in Y]; cm=[st.mean(Y[i][j] for i in range(S)) for j in range(C)]
sst=sum((v-gm)**2 for r in Y for v in r)
sse=sum((Y[i][j]-(rm[i]+cm[j]-gm))**2 for i in range(S) for j in range(C))
ss_row=C*sum((m-gm)**2 for m in rm); ss_col=S*sum((m-gm)**2 for m in cm)
print('R2 additive',1-sse/sst,'stem share',ss_row/sst,'cell share',ss_col/sst)
# hücre sıralamalarının kökler arası tutarlılığı: Kendall W
ranks=[]
for r in Y:
    order=sorted(range(C),key=lambda j:r[j]); rk=[0]*C
    for pos,j in enumerate(order): rk[j]=pos+1
    ranks.append(rk)
Rj=[sum(ranks[i][j] for i in range(S)) for j in range(C)]; Rbar=st.mean(Rj)
W=12*sum((x-Rbar)**2 for x in Rj)/(S**2*(C**3-C)); print('Kendall W',W)
# ek sayısına göre ortalama pay
share=collections.defaultdict(list)
for s in P:
    tot=sum(grid[s])
    for j in range(C): share[NSUF[j]].append(grid[s][j]/tot)
print({k:round(100*st.mean(v),2) for k,v in sorted(share.items())})
json.dump({'grid':grid,'cells':CELLS,'nsuf':NSUF,'N':N,'types':len(F),'R2':1-sse/sst,'stem':ss_row/sst,'cell':ss_col/sst,'W':W,'cm':cm},open(RES / 'a3_grid.json','w'),ensure_ascii=False)
