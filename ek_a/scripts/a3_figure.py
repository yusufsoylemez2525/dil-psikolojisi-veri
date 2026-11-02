from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # depo kökü (dil-psikolojisi-veri/)
EKA = ROOT / 'ek_a'
EXT, WORK, DER = EKA / 'data' / 'external', EKA / 'data' / 'work', EKA / 'data' / 'derived'
RES, FIG = EKA / 'results', EKA / 'figures'
WORK.mkdir(parents=True, exist_ok=True)
import json,matplotlib,math
matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
plt.rcParams['font.family']='DejaVu Serif'; plt.rcParams['font.size']=8
G=json.load(open(RES / 'a3_grid.json')); N=G['N']
cells=G['cells']; grid=G['grid']
order=sorted(range(len(cells)),key=lambda j:-G['cm'][j])
fig,ax=plt.subplots(figsize=(6.3,3.6))
marks=['o','s','^','D','v','P','X']; grays=['#000000','#333333','#555555','#777777','#999999','#444444','#666666']
styles=['-','--','-.',':','-','--','-.']
for k,(s,v) in enumerate(grid.items()):
    y=[math.log10(v[j]/N*1e6) if v[j]>0 else np.nan for j in order]
    ax.plot(range(len(order)),y,marker=marks[k],linestyle=styles[k],color=grays[k],linewidth=1,markersize=4,label=s)
ax.set_xticks(range(len(order))); ax.set_xticklabels([cells[j] for j in order],rotation=40,ha='right',fontsize=7)
ax.set_ylabel('Milyon sözcükte sıklık (log10)')
ax.spines[['top','right']].set_visible(False); ax.grid(axis='y',color='#e5e5e5',linewidth=0.5); ax.set_axisbelow(True)
ax.legend(ncol=7,frameon=False,loc='upper center',bbox_to_anchor=(0.5,1.12),fontsize=7,handlelength=2.2)
fig.tight_layout(); fig.savefig(FIG / 'sekil_A_2.png',dpi=200)
