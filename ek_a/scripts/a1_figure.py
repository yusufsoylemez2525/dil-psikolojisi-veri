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
R=json.load(open(RES / 'a1_results.json'))
G=['Altınkamış (1;4-2;4)','Aksu 2;0-2;8','Aksu 3;0-3;8','Aksu 4;0-4;8']
T={'Altınkamış (1;4-2;4)':'Altınkamış derlemi, 1;4-2;4','Aksu 2;0-2;8':'Aksu-Koç derlemi, 2;0-2;8','Aksu 3;0-3;8':'Aksu-Koç derlemi, 3;0-3;8','Aksu 4;0-4;8':'Aksu-Koç derlemi, 4;0-4;8'}
K=['Prog1','Past','Narr','Aor','Fut','Imp','Opt']; L=['-(I)yor','-DI','-mIş','-Ar','-(y)AcAk','emir','-(y)A']
fig,axs=plt.subplots(2,2,figsize=(6.3,4.6),sharey=True); x=np.arange(len(K)); w=0.38
for ax,g in zip(axs.flat,G):
    c=R[g]['CHI']['tam']; a=R[g]['ADU']['tam']; cs=sum(c[k] for k in K); as_=sum(a[k] for k in K)
    ax.bar(x-w/2-0.01,[100*c[k]/cs for k in K],w,color='#3a3a3a',label='Çocuk',edgecolor='white',linewidth=0.6)
    ax.bar(x+w/2+0.01,[100*a[k]/as_ for k in K],w,color='#bdbdbd',label='Yetişkin girdisi',edgecolor='white',linewidth=0.6,hatch='////')
    ax.set_title(f"{T[g]} (ρ = {R[g]['rho_tam']:.2f})".replace('.',','),fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(L,fontsize=7)
    ax.spines[['top','right']].set_visible(False); ax.grid(axis='y',color='#e5e5e5',linewidth=0.5); ax.set_axisbelow(True)
for ax in axs[:,0]: ax.set_ylabel('Çekimli fiiller içindeki pay (%)')
h,l=axs[0,0].get_legend_handles_labels(); fig.legend(h,l,loc='lower center',ncol=2,frameon=False,bbox_to_anchor=(0.5,-0.01))
fig.tight_layout(rect=(0,0.05,1,1)); fig.savefig(FIG / 'sekil_A_1.png',dpi=200)
