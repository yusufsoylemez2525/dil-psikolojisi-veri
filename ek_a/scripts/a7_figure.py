from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # depo kökü (dil-psikolojisi-veri/)
EKA = ROOT / 'ek_a'
EXT, WORK, DER = EKA / 'data' / 'external', EKA / 'data' / 'work', EKA / 'data' / 'derived'
RES, FIG = EKA / 'results', EKA / 'figures'
WORK.mkdir(parents=True, exist_ok=True)
import json,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
plt.rcParams['font.family']='DejaVu Serif'; plt.rcParams['font.size']=8
R=json.load(open(RES / 'a7_results.json'))
fig,(a1,a2)=plt.subplots(1,2,figsize=(6.3,2.9),gridspec_kw={'width_ratios':[1.7,1]})
b=R['bins']; x=[d['s'] for d in b]; y=[d['gaze'] for d in b]; se=[d['sd']/np.sqrt(d['n']) for d in b]
a1.errorbar(x,y,yerr=[1.96*s for s in se],fmt='o',color='#333333',ms=4,capsize=2,lw=0.8)
for xi,yi,d in zip(x,y,b): a1.annotate(str(d['n']),(xi,yi),textcoords='offset points',xytext=(4,-9),fontsize=6,color='#666666')
a1.set_xlabel('Şaşırtıcılık (bit, XGLM 564M)'); a1.set_ylabel('İlk geçiş süresi (ms)')
a1.spines[['top','right']].set_visible(False); a1.grid(axis='y',color='#e5e5e5',lw=0.5); a1.set_axisbelow(True)
labs=list(R['models'].keys()); dr=[100*R['models'][k]['dr2'] for k in labs]
a2.bar(range(len(labs)),dr,color='#7a7a7a',width=0.6,edgecolor='white')
for i,v in enumerate(dr): a2.text(i,v+0.05,f'{v:.1f}'.replace('.',','),ha='center',fontsize=7)
a2.set_xticks(range(len(labs))); a2.set_xticklabels(['0,56','1,7','2,9','4,5']); a2.set_xlabel('XGLM büyüklüğü (milyar parametre)')
a2.set_ylabel('Açıklanan ek varyans (yüzde puan)'); a2.set_ylim(0,max(dr)*1.3)
a2.spines[['top','right']].set_visible(False); a2.grid(axis='y',color='#e5e5e5',lw=0.5); a2.set_axisbelow(True)
a1.set_title('a. Şaşırtıcılık aralıklarına göre ortalama süre',fontsize=8); a2.set_title('b. Model büyüklüğüne göre katkı',fontsize=8)
import matplotlib.ticker as mt
for ax in (a1,a2): ax.yaxis.set_major_formatter(mt.FuncFormatter(lambda v,p: (f'{v:g}').replace('.',',')))
fig.tight_layout(); fig.savefig(FIG / 'sekil_A_4.png',dpi=200)
print(R['r2_base'])
