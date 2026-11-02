# Elle denetlenmiş son sınıflama: F çekimli fiil, K ek-fiil ya da var/yok/değil, D durum ekli adla biten yüklemsiz, N yalın ya da iyelik ekli adla biten yüklemsiz
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # depo kökü (dil-psikolojisi-veri/)
EKA = ROOT / 'ek_a'
EXT, WORK, DER = EKA / 'data' / 'external', EKA / 'data' / 'work', EKA / 'data' / 'derived'
RES, FIG = EKA / 'results', EKA / 'figures'
WORK.mkdir(parents=True, exist_ok=True)
import json, collections, csv
R = json.load(open(WORK / 'manset_auto.json'))
# Elle düzeltme kararları başlık kimliğiyle (a5_manset.py'deki hid()) verilir; başlık metinleri depoda yer almaz.
OV = {
 # F? kararları
 'f85993392580': 'N',
 'd00abf7581c4': 'N',
 '92027897fcdd': 'N',
 '3577428ff427': 'N',
 'cd117468183c': 'N',
 '28a38cfff53b': 'N',
 '02cf90ed0796': 'N',
 'd83c2dc5863d': 'N',
 '67e3b8564b75': 'N',
 '8c91b7e8bf64': 'N',
 # K düzeltmeleri
 '5e99e52f8a3b': 'N',
 '5bcc8f70c1a5': 'N',
 '23d40cffc45e': 'N',
 # N içinde çekimli fiil ya da ek-fiil taşıyanlar
 'ea5809e23999': 'F',
 '113a2680825f': 'F',
 'e888578bdcf0': 'F',
 '3dad9af05cb0': 'F',
 'af4b098efdc4': 'F',
 '0ab013f8d492': 'F',
 'a4ddd8b671cd': 'K',
 'e3ac73ecd865': 'D',
 'e490fe5de39e': 'N',
 '2cf157a21ae3': 'N',
 '5eed94e925d7': 'N',
 '07a8542ac4aa': 'D',
 'd1d1efe3e38c': 'N',
 '08e28cbf62ee': 'N',
 # N/D içinde durum ekli yüklem
 '8ad2aabc90a8': 'D',
 '605c972cfba1': 'D',
 '3d7369fcf88d': 'D',
}
out = []
for x in R:
    c = x['sinif']
    if x['id'] in OV: c = OV[x['id']]
    elif c == 'F?': c = 'F'
    elif c.startswith('N/D'): c = 'N'
    elif c.startswith('D'): c = 'D'
    x['son_sinif'] = c; out.append(x)
json.dump(out, open(WORK / 'manset_final.json', 'w'), ensure_ascii=False, indent=0)
# Başlık metni içermeyen kod dosyası (depoda yayımlanan türetilmiş veri)
F = ['id', 'tarih', 'gazete', 'duzey', 'sayfa_sira', 'kaynak_url', 'son_oge_oto', 'son_oge', 'elle_duzeltme', 'soru', 'ic_fiil',
     'tirnak', 'n_sifatfiil_aday', 'n_belirtme_aday']
with open(DER / 'manset_kodlar.tsv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh, delimiter='\t'); w.writerow(F)
    for x in out:
        w.writerow([x['id'], x['tarih'], x['gazete'], x['duzey'], x['sayfa_sira'], x['kaynak_url'], x['sinif'], x['son_sinif'],
                    int(x['id'] in OV), int(x['soru']), int(x['ic_fiil']), int(x['tirnak']), len(x['sifatfiil']), len(x['belirtme'])])
G = ['Hürriyet', 'Sabah', 'Milliyet']
tab = {g: collections.Counter(x['son_sinif'] for x in out if x['gazete'] == g) for g in G}
tot = collections.Counter(x['son_sinif'] for x in out)
for c in 'FKDN':
    print(c, [tab[g][c] for g in G], tot[c], round(100 * tot[c] / len(out), 1))
print('n', [sum(tab[g].values()) for g in G], len(out))
m = [x for x in out if x['duzey'] == 'manşet']
print('manşet', collections.Counter(x['son_sinif'] for x in m))
print('tırnaklı', sum(x['tirnak'] for x in out), collections.Counter(x['son_sinif'] for x in out if x['tirnak']))
