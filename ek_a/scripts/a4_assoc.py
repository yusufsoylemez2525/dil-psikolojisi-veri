# A.4: Yapıcı (2015) çağrışımlarının TUD yazılı derlemindeki eşdizim listelerinde (±5 pencere, log-olabilirlik sırası) konumu
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # depo kökü (dil-psikolojisi-veri/)
EKA = ROOT / 'ek_a'
EXT, WORK, DER = EKA / 'data' / 'external', EKA / 'data' / 'work', EKA / 'data' / 'derived'
RES, FIG = EKA / 'results', EKA / 'figures'
WORK.mkdir(parents=True, exist_ok=True)
import re, glob, json, csv, statistics as st, logging, collections
logging.disable(logging.CRITICAL)
import zeyrek
an = zeyrek.MorphAnalyzer()
D = str(EXT / 'tnc_esdizim')
Y = {r['uyarici']: r for r in csv.DictReader(open(DER / 'yapici2015_secilen_uyaricilar.tsv'), delimiter='\t')}
# İlişki türü: P = dizisel (eş anlam, zıt anlam, eş düzey, üst/alt kavram, parça-bütün), S = dizimsel (nitelik ya da eylem), T = tematik
REL = {
 ('beyaz','siyah'):'P',('beyaz','ak'):'P',('beyaz','temiz'):'T',('beyaz','temizlik'):'T',
 ('savaş','barış'):'P',('savaş','ölüm'):'T',('savaş','kan'):'T',
 ('gazete','haber'):'T',('gazete','dergi'):'P',('gazete','okumak'):'S',
 ('göz','görmek'):'S',('göz','organ'):'P',('göz','yeşil'):'S',('göz','kulak'):'P',
 ('ses','müzik'):'T',('ses','gürültü'):'P',('ses','duymak'):'S',
 ('kız','erkek'):'P',('kız','güzel'):'S',('kız','bayan'):'P',
 ('gün','zaman'):'P',('gün','güneş'):'T',('gün','gece'):'P',
 ('çocuk','bebek'):'P',('çocuk','sevimli'):'S',('çocuk','sevgi'):'T',('çocuk','mutluluk'):'T',
 ('iyi','kötü'):'P',('iyi','güzel'):'P',('iyi','melek'):'T',
 ('ev','yuva'):'P',('ev','huzur'):'T',('ev','araba'):'P',
 ('arkadaş','dost'):'P',('arkadaş','kardeş'):'P',('arkadaş','dostluk'):'T',
 ('hayat','yaşam'):'P',('hayat','ölüm'):'P',('hayat','zor'):'S',('hayat','su'):'T',
 ('kitap','okumak'):'S',('kitap','bilgi'):'T',('kitap','dost'):'T',('kitap','edebiyat'):'T',
 ('anne','sevgi'):'T',('anne','baba'):'P',('anne','can'):'T',('anne','aşk'):'T',('anne','herşey'):'T',
 ('genç','yaşlı'):'P',('genç','dinamik'):'S',('genç','ergen'):'P',
 ('el','yabancı'):'P',('el','parmak'):'P',('el','ayak'):'P',
 ('masa','sandalye'):'P',('masa','yemek'):'T',('masa','tahta'):'T',
 ('sabah','güneş'):'T',('sabah','uyku'):'T',('sabah','akşam'):'P',
 ('para','güç'):'T',('para','herşey'):'T',('para','zenginlik'):'T',
}
VERB = {'okumak', 'görmek', 'duymak'}
EXCL = {'göre', 'sevgili', 'bilgisayar', 'yaşamak', 'yaşamaya', 'yaşamayı', 'yaşamış', 'güçlü', 'ergenlik'}
def ok_form(form, resp):
    if form in EXCL: return False
    if resp == 'herşey': return form == 'herşey'
    if form == resp: return True
    if resp not in VERB and form.startswith(resp) and re.fullmatch(r'(lar|ler)?(ı|i|u|ü|ın|in|un|ün|a|e|da|de|ta|te|dan|den|tan|ten|la|le|dır|dir|tır|tir|dur|dür|tur|tür)?', form[len(resp):]): return True
    A = [str(x.formatted) for x in an.analyze(form)[0]] if form else []
    for f in A:
        m = re.match(r'\[([^:\]]+):([^\],]+)', f)
        if not m: continue
        lem, pos = m.group(1).lower().replace('i̇', 'i'), m.group(2)
        if resp in VERB:
            if lem == resp and pos == 'Verb': return True
        else:
            body = f.split('] ', 1)[1] if '] ' in f else f
            if lem == resp and '|' not in body: return True
    return False
rows = []
for fp in sorted(glob.glob(D + '/*.txt')):
    stim = fp.split('/')[-1][:-4]
    L = open(fp).read().strip().split('\n')
    m = re.search(r'F (\S+) N (\d+) minLL ([\d.]+)', L[0]); F, N = m.group(1), int(m.group(2))  # baştaki 'Q <sözcük>' öneki varsa atlanır
    top = L[1][4:].split()
    resp_lines = {l.split(' >> ')[0]: (l.split(' >> ')[1] if ' >> ' in l else '') for l in L[2:]}
    y = Y[stim]
    for pos, col in ((1, 'tr1'), (2, 'tr2'), (3, 'tr3')):
        for resp in [x.strip().lower().replace('i̇', 'i') for x in y[col].split('/')]:
            resp = {'her şey': 'herşey'}.get(resp, resp)
            if (stim, resp) not in REL or resp == 'herşey': continue
            items = []
            for it in resp_lines.get(resp, '').split(' ; '):
                p = it.split()
                if len(p) >= 6:
                    rk, form, o, f, ll, ld = int(p[0]), ' '.join(p[1:-4]), int(p[-4]), p[-3], float(p[-2]), float(p[-1])
                    if ok_form(form, resp): items.append((rk, form, o, ll, ld))
            best = min(items) if items else None
            rows.append(dict(uyarici=stim, sira=pos, yanit=resp, tur=REL[(stim, resp)], F=F,
                             rank=best[0] if best else None, form=best[1] if best else None,
                             o=best[2] if best else 0, ld=best[4] if best else None))
json.dump(rows, open(RES / 'a4_results.json', 'w'), ensure_ascii=False, indent=0)
print('uyarıcı', len({r['uyarici'] for r in rows}), 'çift', len(rows))
for r in rows: print(r['uyarici'], r['sira'], r['yanit'], r['tur'], r['rank'], r['form'], r['o'], r['ld'])
def summ(sub, lab):
    n = len(sub); found = [r for r in sub if r['rank']]
    t100 = sum(1 for r in found if r['rank'] <= 100)
    rk = [r['rank'] if r['rank'] else 2501 for r in sub]
    print(f"{lab}: n={n} listede={len(found)} ({100*len(found)/n:.0f}%) ilk100={t100} ({100*t100/n:.0f}%) ortanca sıra={st.median(rk)}")
summ(rows, 'HEPSİ')
for t in 'PST': summ([r for r in rows if r['tur'] == t], t)
for p in (1, 2, 3): summ([r for r in rows if r['sira'] == p], f'sıra{p}')
