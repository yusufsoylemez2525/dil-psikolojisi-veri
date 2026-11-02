# Ek A: üçüncü taraf ham veriye gerek duymadan, yalnız results/ ve data/derived/ dosyalarından
# Tablo A.1, A.4-A.9, A.11 ve A.12'yi CSV olarak üretir (results/tablo_A*.csv) ve ekrana yazar.
# Metindeki türetilmiş birkaç sayı da (ör. Spearman ρ = 0,85 ve 0,81; Kendall W; sürçme sıklığının sözcük karşılığı) denetlenir.
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # depo kökü (dil-psikolojisi-veri/)
EKA = ROOT / 'ek_a'
EXT, WORK, DER = EKA / 'data' / 'external', EKA / 'data' / 'work', EKA / 'data' / 'derived'
RES, FIG = EKA / 'results', EKA / 'figures'
import csv, json, math, statistics as st, collections
def tr(x, d=2):
    return f'{x:.{d}f}'.replace('.', ',') if isinstance(x, (int, float)) else str(x)
def write(name, header, rows):
    with open(RES / name, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh); w.writerow(header); w.writerows(rows)
    print('\n' + name); print(' | '.join(header)); [print(' | '.join(str(x) for x in r)) for r in rows]

# ---------------- Tablo A.1
A1 = json.load(open(RES / 'a1_results.json')); IS = json.load(open(RES / 'a1_island_child_results.json'))['seed1']
G = ['Altınkamış (1;4-2;4)', 'Aksu 2;0-2;8', 'Aksu 3;0-3;8', 'Aksu 4;0-4;8']
rows = []
# Altınkamış derleminde tek çocuk ozge1.cha'da "Ozge", öteki dosyalarda "Target_Child" adıyla kayıtlı olduğundan
# a1_results.json'daki ad sayımı 2 verir; çocuk sayısı a1_island_child.py'deki düzeltilmiş kimlikle (1) alınır.
nchild = lambda g: IS[g]['children'] if g.startswith('Altınkamış') else A1[g]['CHI']['children']
rows.append(['Çocuk (çocuk-kesit) / oturum'] + [f"{nchild(g)} / {A1[g]['CHI']['files']}" for g in G])
rows.append(['Çocuk söyleyişi'] + [A1[g]['CHI']['utts'] for g in G])
rows.append(['Ortalama söyleyiş uzunluğu, sözcük (yetişkin)'] + [f"{tr(A1[g]['CHI']['mlu_w'])} ({tr(A1[g]['ADU']['mlu_w'])})" for g in G])
rows.append(['Sözcük başına biçim birimi (yetişkin)'] + [f"{tr(A1[g]['CHI']['morph_per_word'])} ({tr(A1[g]['ADU']['morph_per_word'])})" for g in G])
rows.append(['Çekimli fiil belirteci / ayrı fiil'] + [f"{A1[g]['CHI']['verb_tokens']} / {A1[g]['CHI']['verb_lemmas']}" for g in G])
rows.append(['Kullanılan ZGK eki (7 ek içinde)'] + [A1[g]['CHI']['tam_types'] for g in G])
rows.append(['Girdiyle sıra ilişkisi, fiil ekleri (rho)'] + [tr(A1[g]['rho_tam']) for g in G])
rows.append(['Girdiyle sıra ilişkisi, durum ekleri (rho)'] + [tr(A1[g]['rho_case']) for g in G])
rows.append(['Fiil başına ayrı çekimli biçim, çocuk düzeyinde: çocuk / eşitlenmiş girdi (çift)'] +
            [f"{tr(IS[g]['child'], 1)} / {tr(IS[g]['adult'], 1)} ({IS[g]['pairs']})" for g in G])
write('tablo_A1.csv', ['olcut'] + G, rows)

# ---------------- Tablo A.4 ve metindeki sıklık ölçüleri
A3 = json.load(open(RES / 'a3_grid.json')); grid, cells, NO = A3['grid'], A3['cells'], A3['N']
# Türkçe Ulusal Derlemi 3.0 web arayüzü sayımları (a3_tnc.py ile aynı; erişim 1 Kasım 2026)
TNC = {'ev': [11959, 1396, 10084, 8565, 3057, 433, 908, 844, 417, 367, 22], 'köy': [5049, 404, 1556, 1516, 800, 33, 593, 263, 56, 23, 3],
       'yol': [25973, 1851, 7916] + [None] * 8}
NT = 50678199
sh = {j: [100 * grid[s][j] / sum(grid[s]) for s in grid] for j in range(len(cells))}
order = sorted(range(len(cells)), key=lambda j: -st.mean(sh[j]))
rows = [[cells[j], A3['nsuf'][j], f"{tr(st.mean(sh[j]), 2 if st.mean(sh[j]) < 0.1 else 1)} ({tr(min(sh[j]), 2 if min(sh[j]) < 0.1 else 1)}-{tr(max(sh[j]), 2 if max(sh[j]) < 0.1 else 1)})",
         TNC['ev'][j], TNC['köy'][j]] for j in order]
write('tablo_A4.csv', ['hucre', 'ek_sayisi', '7_adda_ortalama_pay_alt_yazi_yuzde', 'ev_TUD', 'koy_TUD'], rows)
def spear(x, y):
    def rk(v):
        s = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v); i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[s[j + 1]] == v[s[i]]: j += 1
            for k in range(i, j + 1): r[s[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    a, b = rk(x), rk(y); n = len(a); ma, mb = sum(a) / n, sum(b) / n
    return sum((p - ma) * (q - mb) for p, q in zip(a, b)) / (sum((p - ma) ** 2 for p in a) * sum((q - mb) ** 2 for q in b)) ** .5
def pairs(nouns):
    xs, ys = [], []
    for s in nouns:
        for j, t in enumerate(TNC[s]):
            if t is not None: xs.append(t / NT * 1e6); ys.append(grid[s][j] / NO * 1e6)
    return xs, ys
x25, y25 = pairs(['ev', 'köy', 'yol']); x22, y22 = pairs(['ev', 'köy'])
print(f"\nTUD-alt yazı ortak biçimler: n={len(x25)} rho={spear(x25, y25):.2f}; ev+köy n={len(x22)} rho={spear(x22, y22):.2f}")
print(f"Toplamsal model R2={A3['R2']:.2f} (hücre {A3['cell']:.2f}, ad {A3['stem']:.2f}); Kendall W={A3['W']:.2f}; alt yazı derlemi {NO} sözcük, {A3['types']} yazılış")
F = json.load(open(RES / 'a3_forms.json'))
print('Ad başına gerçekleşen çekimli biçim:', {k: v['types'] for k, v in F.items()}, '; en çok 2 kez geçen biçim payı %:',
      {k: round(100 * v['lowshare']) for k, v in F.items()}, '; belirteçlerin %90ını karşılayan biçim:', {k: v['k90'] for k, v in F.items()})

# ---------------- Tablo A.5 ve A.6
A4 = json.load(open(RES / 'a4_results.json'))
TOP = {r['uyarici']: r for r in csv.DictReader(open(DER / 'tud_esdizim_ozet.tsv', encoding='utf-8'), delimiter='\t')}
L = {'P': 'D', 'S': 'M', 'T': 'T'}
by = collections.OrderedDict()
for r in A4: by.setdefault(r['uyarici'], []).append(r)
fmt = lambda n: f'{n:,}'.replace(',', '.')
rows = [[f"{s} ({fmt(int(rs[0]['F']))})", ', '.join(f"{r['yanit']} ({fmt(r['rank']) if r['rank'] else 'yok'}, {L[r['tur']]})" for r in rs),
         TOP[s]['en_guclu_4_icerik_esdizimi']] for s, rs in sorted(by.items(), key=lambda kv: kv[0].replace('ç', 'c~'))]
write('tablo_A5.csv', ['uyarici_derlem_sikligi', 'cagrisim_yanitlari_esdizim_sirasi_iliski_turu', 'en_guclu_icerik_sozcugu_esdizimleri'], rows)
def summ(sub, lab):
    rk = [r['rank'] if r['rank'] else 2501 for r in sub]  # listede olmayan yanıt listenin sonuna (2.501) konur
    md = st.median(rk); md = int(md) if md == int(md) else md
    return [lab, len(sub), sum(1 for r in sub if r['rank']), sum(1 for r in sub if r['rank'] and r['rank'] <= 100), md]
rows = [summ([r for r in A4 if r['tur'] == t], n) for t, n in (('P', 'Dizisel'), ('S', 'Dizimsel'), ('T', 'Tematik'))]
rows += [summ([r for r in A4 if r['sira'] == k], n) for k, n in ((1, 'En sık yanıt'), (2, 'İkinci sıradaki yanıt'), (3, 'Üçüncü sıradaki yanıt'))]
rows.append(summ(A4, 'Toplam'))
write('tablo_A6.csv', ['yanit_grubu', 'cift', 'esdizim_listesinde', 'ilk_100_sirada', 'ortanca_sira'], rows)

# ---------------- Tablo A.7
A5 = json.load(open(RES / 'a5_results.json'))
K = [('çekimli yüklem', 'çekimli yüklem', 'Çekimli yüklem'), ('ilgi cümleciği (sıfat-fiil)', 'ad niteleyen sıfat-fiil', 'Adı niteleyen sıfat-fiil (ilgi cümlesi)'),
     ('sıfat-fiil (öteki)', 'öteki sıfat-fiil', 'Öteki sıfat-fiil kullanımları'), ('ad-fiil tümleci', None, 'Ad-fiil tümleci'), ('zarf-fiil', None, 'Zarf-fiil')]
na, nm, ny = sum(A5['all'].values()), sum(A5['amb']['-mIş'].values()), sum(A5['amb']['-(y)AcAk'].values())
c = lambda v, n: f'{v} (%{tr(100 * v / n, 1)})'
rows = [[lab, c(A5['all'][a], na), c(A5['amb']['-mIş'][b], nm) if b else '-', c(A5['amb']['-(y)AcAk'][b], ny) if b else '-'] for a, b, lab in K]
rows.append(['Toplam', na, nm, ny])
write('tablo_A7.csv', ['yapi_turu', 'belirtme_durumlu_nesnenin_fiili', 'mIs_ile_biten_fiil', 'yAcAk_ile_biten_fiil'], rows)
an = sum(A5['after_nom'].values())
print(f"Önünde yalın özne bulunan nesne: {an}, ana yükleme bağlanan %{100 * A5['after_nom']['çekimli yüklem'] / an:.1f}")

# ---------------- Tablo A.8 (başlık metni olmadan, kod dosyasından)
M = list(csv.DictReader(open(DER / 'manset_kodlar.tsv', encoding='utf-8'), delimiter='\t'))
GZ = ['Hürriyet', 'Sabah', 'Milliyet']
LB = [('F', 'Çekimli fiil'), ('K', 'Ek-fiil ya da var, yok, değil'), ('D', 'Durum ekli ad (yüklemi düşmüş)'), ('N', 'Yalın ya da iyelik ekli ad')]
rows = [[lab] + [sum(1 for x in M if x['gazete'] == g and x['son_oge'] == k) for g in GZ] +
        [f"{sum(1 for x in M if x['son_oge'] == k)} (%{tr(100 * sum(1 for x in M if x['son_oge'] == k) / len(M), 1)})"] for k, lab in LB]
rows.append(['Toplam'] + [sum(1 for x in M if x['gazete'] == g) for g in GZ] + [len(M)])
write('tablo_A8.csv', ['basligin_son_ogesi', 'Hurriyet', 'Sabah', 'Milliyet', 'Toplam'], rows)
ms = [x for x in M if x['duzey'] == 'manşet']
print(f"Sayfa sayısı {len({(x['tarih'], x['gazete']) for x in M})}; manşet {len(ms)}, yüklemsiz (D+N) manşet {sum(x['son_oge'] in 'DN' for x in ms)}; "
      f"yüklemsiz başlık payı %{tr(100 * sum(x['son_oge'] in 'DN' for x in M) / len(M), 1)}")

# ---------------- Tablo A.9 (tezde yayımlanan ortancalar) ve metindeki oranlar
A9 = [r for r in csv.DictReader(open(DER / 'altiparmak2015_ortancalar.csv', encoding='utf-8')) if r['kosul'] == 'hazırlıksız']
write('tablo_A9.csv', ['akicisizlik_turu', '4-8', '18-23', '33-50', '50+', 'p'],
      [[r['akicisizlik_turu'], r['yas_4_8'], r['yas_18_23'], r['yas_33_50'], r['yas_50_ustu'], r['p_kruskal_wallis']] for r in A9])
for name in ('Uzatma', 'Tereddüt'):
    r = next(x for x in A9 if x['akicisizlik_turu'] == name); ext = [float(r['yas_4_8']), float(r['yas_50_ustu'])]; mid = [float(r['yas_18_23']), float(r['yas_33_50'])]
    q = [e / m for e in ext for m in mid]; print(f'{name}: uç grupların orta gruplara oranı {min(q):.1f}-{max(q):.1f} kat')
r = next(x for x in A9 if x['akicisizlik_turu'] == 'Dil sürçmesi'); ad = [float(r[k]) for k in ('yas_18_23', 'yas_33_50', 'yas_50_ustu')]
print(f'Yetişkinlerde sürçme: {min(ad)}-{max(ad)} / 100 sözcük = {100 / max(ad):.0f}-{100 / min(ad):.0f} sözcükte bir')

# ---------------- Tablo A.11
A6 = json.load(open(RES / 'a6_results.json')); CL = json.load(open(RES / 'a6_cluster_results.json'))
AG = ['Aksu-Koç 2;0-2;8', 'Aksu-Koç 3;0-3;8', 'Aksu-Koç 4;0-4;8']
MS = [('form', 'En az bir ortak sözcük biçimi'), ('lemma', 'Aynı fiil gövdesi'), ('tam', 'Aynı ZGK eki'), ('tam_dl', 'Gövde farklıyken aynı ZGK eki')]
def ob(d): return f"{tr(100 * d['k'] / d['n'], 1)} / {tr(100 * d['E'] / d['n'], 1)}"
def pool(k, m):
    ds = [A6[k][g]['1'][m] for g in AG]; return {x: sum(d[x] for d in ds) for x in ('n', 'k', 'E')}
rows = [[lab] + [ob(A6['AC'][g]['1'][m]) for g in AG] + [ob(pool('AC_s', m))] for m, lab in MS]
rows.append(['Çift sayısı (bütün / fiilli / gövdesi farklı)'] + [' / '.join(str(A6['AC'][g]['1'][m]['n']) for m in ('form', 'lemma', 'tam_dl')) for g in AG] +
            [' / '.join(str(pool('AC_s', m)['n']) for m in ('form', 'lemma', 'tam_dl'))])
write('tablo_A11.csv', ['benzerlik_olcusu'] + AG + ['soru_olmayan_yetiskin_soyleyisinden_sonra'], rows)
p = CL['pooled']; print(f"Soru olmayan, gövde farklı: {p['obs']} / {p['base']}; z bağımsız {p['z_independent']}, z kümeli {p['z_cluster']}, %95 GA {p['boot_ci95']}, {p['children']} çocuk")
for g in AG: print(' ', g, CL[g]['pairs'], 'çift', CL[g]['obs'], '/', CL[g]['base'], 'z', CL[g]['z_independent'], CL[g]['z_cluster'])
ca = pool('CA', 'lemma'), pool('CA', 'tam_dl'); print(f"Çocuk -> yetişkin: gövde {ob(ca[0])}, gövde farklıyken ZGK {ob(ca[1])}")
alt = A6['AC']['Altınkamış 1;4-2;4']['1']['form']; print(f"Altınkamış ortak sözcük biçimi: {ob(alt)}; fiilli çift {A6['AC']['Altınkamış 1;4-2;4']['1']['lemma']['n']}")

# ---------------- Tablo A.12
A7 = json.load(open(RES / 'a7_results.json'))
LBL = {'564M': '564 milyon', '1,7B': '1,7 milyar', '2,9B': '2,9 milyar', '4,5B': '4,5 milyar'}
pv = lambda p: '< 0,001' if p < 0.001 else tr(p, 2)
rows = [[LBL[k], f"{tr(m['b'])} ({tr(m['se'])}; {pv(m['p'])})", f"{tr(m['b_prev'])} ({tr(m['se_prev']) if 'se_prev' in m else '-'}; {pv(m['p_prev'])})", tr(100 * m['dr2'], 1)]
        for k, m in A7['models'].items()]
write('tablo_A12.csv', ['xglm_buyuklugu', 'saskirticilik_ms_bit_SH_p', 'onceki_sozcugun_saskirticiligi_ms_bit_SH_p', 'aciklanan_ek_varyans_yuzde_puan'], rows)
print(f"Sözcük {A7['n_items']} / {A7['n_all']}, okur {A7['readers']}, metin {A7['texts']}; temel model R2 {A7['r2_base']:.2f}; karma model b={A7['mixed']['b']:.2f} (SH {A7['mixed']['se']:.2f}, n={A7['mixed']['n']}); "
      f"karesel terim p={A7['quad']['p2']:.2f}, ek R2 {100 * A7['quad']['dr2']:.1f} puan; r(uzunluk,s)={A7['corr_len_s']:.2f}, r(sıklık,s)={A7['corr_zipf_s']:.2f}; çok birimli sözcük %{100 * A7['multi_share']:.0f}")
print('Şekil A.4a aralıkları (ortalama şaşırtıcılık bit, ortalama süre ms, sözcük):', [(round(b['s'], 1), round(b['gaze'], 1), b['n']) for b in A7['bins']])
