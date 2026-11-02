from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # depo kökü (dil-psikolojisi-veri/)
EKA = ROOT / 'ek_a'
EXT, WORK, DER = EKA / 'data' / 'external', EKA / 'data' / 'work', EKA / 'data' / 'derived'
RES, FIG = EKA / 'results', EKA / 'figures'
WORK.mkdir(parents=True, exist_ok=True)
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np, matplotlib.ticker as mt
plt.rcParams['font.family'] = 'DejaVu Serif'; plt.rcParams['font.size'] = 8
R = json.load(open(RES / 'a6_results.json'))['AC_lag']
G = ['Aksu-Koç 2;0-2;8', 'Aksu-Koç 3;0-3;8', 'Aksu-Koç 4;0-4;8']
fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.8))
titles = {'form': 'a. En az bir ortak sözcük biçimi', 'tam_dl': 'b. Fiil gövdesi farklıyken aynı ZGK eki'}
for ax, m in zip(axes, ['form', 'tam_dl']):
    L = list(range(1, 13)); obs = []; base = []; ci = []
    for lag in L:
        n = k = E = 0
        for g in G:
            d = R[g][str(lag)][m]; n += d['n']; k += d['k']; E += d['E']
        p = k / n; obs.append(100 * p); base.append(100 * E / n); ci.append(196 * np.sqrt(p * (1 - p) / n))
    ax.errorbar(L, obs, yerr=ci, fmt='o-', color='#333333', ms=3.5, lw=0.9, capsize=2, label='Gözlenen')
    ax.plot(L, base, '--', color='#888888', lw=0.9, label='Taban çizgisi')
    ax.set_xticks(L); ax.set_xlabel('Yetişkin söyleyişinin uzaklığı (söyleyiş)')
    ax.set_ylabel('Eşleşme oranı (yüzde)'); ax.set_ylim(0, max(obs) * 1.15)
    ax.set_title(titles[m], fontsize=8)
    ax.spines[['top', 'right']].set_visible(False); ax.grid(axis='y', color='#e5e5e5', lw=0.5); ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(mt.FuncFormatter(lambda v, p: (f'{v:g}').replace('.', ',')))
    print(m, [round(o, 1) for o in obs], [round(b, 1) for b in base])
h, l = axes[0].get_legend_handles_labels(); axes[0].legend(h[::-1], l[::-1], frameon=False, fontsize=7)
fig.tight_layout(); fig.savefig(FIG / 'sekil_A_3.png', dpi=200)
