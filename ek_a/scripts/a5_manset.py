# A.5 eki: 2025 manşetlerinde yüklem türü ve sıfat-fiil yapıları (Hürriyet, Sabah, Milliyet)
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # depo kökü (dil-psikolojisi-veri/)
EKA = ROOT / 'ek_a'
EXT, WORK, DER = EKA / 'data' / 'external', EKA / 'data' / 'work', EKA / 'data' / 'derived'
RES, FIG = EKA / 'results', EKA / 'figures'
WORK.mkdir(parents=True, exist_ok=True)
import csv, re, json, collections, logging, sys
logging.disable(logging.CRITICAL)
import zeyrek
an = zeyrek.MorphAnalyzer()
R = list(csv.DictReader(open(EXT / 'manset' / 'manset.tsv'), delimiter='\t'))
import hashlib
# Başlık kimliği: "tarih|gazete|başlık" dizgesinin SHA-1 özetinin ilk 12 karakteri. Depoda başlık metni bulunmadığından
# elle verilen kararlar (DROP ve a5_manset_final.py'deki OV) bu kimliklerle tutulur.
def hid(r): return hashlib.sha1(f"{r['tarih']}|{r['gazete']}|{r['baslik'].strip()}".encode('utf-8')).hexdigest()[:12]
# Sayfa içi sıra: aynı tarih ve gazetenin TSV'deki satırları içinde (spotlar dahil) 1'den başlayan sıra
_c = collections.Counter()
for r in R: _c[(r['tarih'], r['gazete'])] += 1; r['sayfa_sira'] = _c[(r['tarih'], r['gazete'])]
# Manşet bloğundaki ara başlık sayılan 4 satır (2025-10-15 Hürriyet 2 satır, 2025-09-15 Milliyet 2 satır) dışarıda bırakılır
DROP = {'29f255117b77', '6b227cdf9449', 'f234d41da84a', '780b921d3547'}
H = [r for r in R if r['duzey'] != 'spot' and hid(r) not in DROP]
TAM = {'Past', 'Narr', 'Prog1', 'Prog2', 'Fut', 'Aor', 'Neces', 'Imp', 'Opt', 'Cond', 'Desr'}
PART = {'PresPart', 'PastPart', 'FutPart', 'NarrPart', 'AorPart'}
CACHE = {}
def ana(w):
    if w not in CACHE:
        try: CACHE[w] = [str(x.formatted) for x in an.analyze(w)[0]]
        except Exception: CACHE[w] = []
    return CACHE[w]
def toks(s):
    s = s.replace('’', "'").replace('‘', "'")
    out = []
    for w in s.split():
        w = w.strip("'\"“”!?.,:;…()")
        w = re.sub(r"^'|'$", '', w)
        if w: out.append(w)
    return out
def low(w): return w.replace('İ', 'i').replace('I', 'ı').lower()
def segs(f):
    body = f.split('] ', 1)[1] if '] ' in f else f
    return body
def is_finite(f):
    b = segs(f)
    if '|Zero→Verb' in b or 'Zero→Verb' in b: return False
    if not f.split(']')[0].split(':')[-1].startswith('Verb') and '→Verb' not in b: return False
    last = b.split('|')[-1]
    return any(':' + t in last or '+' + t in last for t in TAM) and '→Noun' not in last and '→Adj' not in last
def is_part(f):
    b = segs(f); last = b.split('|')[-1]
    return any(p in last for p in PART)
def is_cop(f):
    b = segs(f)
    if 'Zero→Verb' not in b: return False
    tail = b.split('Zero→Verb', 1)[1]
    ov = [s.split(':')[1] for s in tail.split('+')[1:] if ':' in s and s.split(':')[0] != '']
    return bool(ov) and ov != ['A3pl']
QP = {'mı', 'mi', 'mu', 'mü', 'mıdır', 'midir', 'mudur', 'müdür'}
def plain_noun(A):
    return any(re.match(r'^\[[^:]+:(Noun|Adj)[^\]]*\] [^|]*\+A3sg$', f) or re.match(r'^\[[^:]+:(Noun|Adj)[^\]]*\] [^|+]*:(Noun|Adj)(\+A3sg)?$', f) for f in A)
def final_class(w):
    lw = low(w)
    if lw in ('var', 'yok', 'değil', 'değildir', 'vardır', 'yoktur'): return 'K'
    A = ana(lw)
    if any(is_finite(f) for f in A): return 'F?' if plain_noun(A) else 'F'
    if any(is_part(f) and re.search(r'(FutPart|NarrPart|AorPart)→Adj$', segs(f)) for f in A) and re.search(r'(acak|ecek|mış|miş|muş|müş|maz|mez)$', lw): return 'F'
    if any(is_cop(f) for f in A): return 'K'
    if not A: return 'N?'
    cases = set()
    for f in A:
        m = re.findall(r':(Dat|Loc|Abl|Ins|Acc|Gen|Equ)\b', segs(f).split('|')[-1])
        cases.add(m[-1] if m else 'Nom')
    if cases == {'Nom'} or 'Nom' in cases and len(cases) == 1: return 'N'
    if 'Nom' not in cases: return 'D:' + '/'.join(sorted(cases))
    return 'N/D:' + '/'.join(sorted(cases - {'Nom'}))
rows = []
for r in H:
    head = r['baslik']
    if ':' in head:
        a, b = head.split(':', 1)
        head = b if len(a.split()) <= 2 else a
    T = toks(head)
    soru = False
    if len(T) > 1 and low(T[-1]) in QP: T = T[:-1]; soru = True
    soru = soru or head.strip().endswith('?')
    fc = final_class(T[-1]) if T else 'N?'
    anyfin = any(final_class(t) == 'F' for t in T[:-1])
    parts = []
    for i, t in enumerate(T[:-1]):
        A = ana(low(t))
        if A and any(is_part(f) for f in A) and not any(is_finite(f) for f in A):
            parts.append(t)
    accs = [t for t in T[:-1] if any(re.search(r':Acc\b', segs(f).split('|')[-1]) for f in ana(low(t)))]
    rows.append(dict(id=hid(r), sayfa_sira=r['sayfa_sira'], kaynak_url=r.get('kaynak_url', ''), tarih=r['tarih'], gazete=r['gazete'], duzey=r['duzey'], baslik=r['baslik'], son=T[-1] if T else '',
                     sinif=fc, soru=soru, ic_fiil=anyfin, sifatfiil=parts, belirtme=accs, tirnak=r['baslik'].strip()[:1] in "'\"‘“"))
json.dump(rows, open(WORK / 'manset_auto.json', 'w'), ensure_ascii=False, indent=0)
c = collections.Counter(x['sinif'].split(':')[0] for x in rows)
print(len(rows), c)
for k in ['N?']:
    print(k, [x['baslik'] for x in rows if x['sinif'] == k])
