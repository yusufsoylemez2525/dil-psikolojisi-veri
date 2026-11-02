# A.6: CHILDES Türkçe derlemlerinde yetişkin ile çocuk arasındaki söyleyişler arası hizalanma
# Ölçüler: sözcük biçimi paylaşımı, fiil gövdesi paylaşımı, zaman-görünüş-kip (ZGK) eki eşleşmesi
# Taban çizgisi: aynı oturumda hedeften en az 10 söyleyiş uzaktaki rastgele söyleyişler
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # depo kökü (dil-psikolojisi-veri/)
EKA = ROOT / 'ek_a'
EXT, WORK, DER = EKA / 'data' / 'external', EKA / 'data' / 'work', EKA / 'data' / 'derived'
RES, FIG = EKA / 'results', EKA / 'figures'
WORK.mkdir(parents=True, exist_ok=True)
AT = '\x40'  # CHAT başlık satırı ve özel biçim işareti (U+0040); depoda e-posta taraması kolay olsun diye kaçış diziyle yazılmıştır
import re, glob, json, random, collections, sys
DATA = str(EXT / 'childes-tr')
D = json.load(open(WORK / 'a1_parsed.json'))
ANA = D['ana']
TAM = {'Past','Narr','Prog1','Prog2','Fut','Aor','Imp','Opt','Neces','Cond','Desr'}
ADULT_ROLES = {'Investigator','Mother','Adult','Father','Grandmother','Grandfather','Uncle','Aunt','Teacher'}

def age_months(a):
    m = re.match(r'(\d+);(\d+)?', a)
    return int(m.group(1))*12 + int(m.group(2) or 0) if m else None

def clean(utt):
    if '[- ' in utt: return []
    u = re.sub(r'(\S+) \[: ([^\]]+)\]', r'\2', utt)
    u = re.sub(r'\[::[^\]]*\]', '', u)
    u = re.sub(r'\[[^\]]*\]', '', u); u = u.replace('<','').replace('>','')
    toks = []
    for w in u.split():
        if w.startswith(('&','+','0')) or AT in w: continue
        if w in ('xxx','yyy','www'): continue
        w = w.replace('(','').replace(')','').replace('_',' ')
        w = re.sub(r"[.,?!;:\"„‡“”…]+", '', w).strip().lower().replace('i̇','i')
        if not w or not re.search(r'[a-zçğıöşü]', w): continue
        toks.extend(w.split())
    return toks

def parse(fmt):
    m = re.match(r'\[([^:]+):([^\]]+)\]\s*(.*)$', fmt)
    if not m: return None
    lemma, pos, body = m.groups()
    tags = []
    for s in re.split(r'[+]', body.replace('|','+')):
        tags.append((s.split(':',1)[1] if ':' in s else s).split('→')[0])
    der = re.findall(r'→(\w+)', body)
    return {'lemma': lemma, 'pos': pos, 'fpos': der[-1] if der else pos, 'nder': body.count('|'), 'tags': tags}

CACHE = {}
def info(w):
    if w in CACHE: return CACHE[w]
    cands = [c for c in (parse(f) for f in ANA.get(w, []) if f != 'Unk') if c]
    r = {'interj': bool(cands) and all(c['pos'] == 'Interj' for c in cands)}
    if cands:
        mn = min(c['nder'] for c in cands); cc = [c for c in cands if c['nder'] == mn]
        if all(c['fpos'] == 'Verb' and c['nder'] == 0 for c in cc):
            tams = {tuple(sorted(set(c['tags']) & TAM)) for c in cc}
            lem = {c['lemma'] for c in cc}
            if len(tams) == 1 and len(lem) == 1 and list(tams)[0]:
                r.update(verb=True, lemma=lem.pop(), tam='+'.join(list(tams)[0]))
    CACHE[w] = r; return r

def group(corpus, age):
    if corpus == 'Turkay': return 'Altınkamış 1;4-2;4'
    return 'Aksu-Koç 2;0-2;8' if age < 36 else ('Aksu-Koç 3;0-3;8' if age < 48 else 'Aksu-Koç 4;0-4;8')

# --- söyleyişleri sırasıyla oku
sessions = []
for corpus in ['Aksu', 'Turkay']:
    for f in sorted(glob.glob(f'{DATA}/{corpus}/*.cha')):
        if f.endswith(('2haf.cha', '6fb.cha')): continue
        txt = open(f, encoding='utf-8').read()
        roles = {}
        pm = re.search(AT + r'Participants:\s*(.*)', txt)
        for part in pm.group(1).split(','):
            p = part.split()
            if p: roles[p[0]] = p[-1]
        m = re.search(AT + r'ID:\s*tur\|[^|]*\|CHI\|([^|]*)\|', txt)
        age = age_months(m.group(1)) if m else None
        utts = []
        for spk, utt in re.findall(r'^\*([A-Z]{3}):\t(.*(?:\n\t.*)*)', txt, flags=re.M):
            utt = utt.replace('\n\t', ' ')
            who = 'CHI' if spk == 'CHI' else ('ADU' if roles.get(spk) in ADULT_ROLES else 'OTH')
            body = re.sub(r'\x15[^\x15]*\x15', '', utt)
            q = bool(re.search(r'\?\s*$', body.strip())) or '+/?' in body or '+..?' in body
            toks = [t for t in clean(utt) if not info(t)['interj']]
            if not toks: continue
            verbs = [info(t) for t in toks if info(t).get('verb')]
            fv = verbs[-1] if verbs else None
            utts.append({'who': who, 'toks': toks, 'q': q,
                         'forms': set(toks), 'lemma': fv['lemma'] if fv else None, 'tam': fv['tam'] if fv else None})
        sessions.append({'file': f.split('/')[-1], 'corpus': corpus, 'age': age, 'g': group(corpus, age), 'utts': utts})

def m_form(p, t): return bool(p['forms'] & t['forms'])
def m_lemma(p, t): return p['lemma'] is not None and t['lemma'] is not None and p['lemma'] == t['lemma']
def m_tam(p, t): return p['tam'] == t['tam']
def ok_tam(p, t): return p['tam'] is not None and t['tam'] is not None
def ok_tam_dl(p, t): return ok_tam(p, t) and p['lemma'] != t['lemma']
def ok_verb(p, t): return t['lemma'] is not None and p['lemma'] is not None
MEAS = {
    'form':   (lambda p,t: True,  m_form),
    'lemma':  (ok_verb,           m_lemma),
    'tam':    (ok_tam,            m_tam),
    'tam_dl': (ok_tam_dl,         m_tam),
}
random.seed(7)
K = 40
def run(direction, lagmax=1, qfilter=None):
    """direction 'AC': yetişkin -> çocuk; 'CA': çocuk -> yetişkin"""
    src, tgt = ('ADU', 'CHI') if direction == 'AC' else ('CHI', 'ADU')
    out = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0, 0.0, 0.0]))
    for s in sessions:
        U = s['utts']; n = len(U)
        srcidx = [i for i, u in enumerate(U) if u['who'] == src]
        for i, t in enumerate(U):
            if t['who'] != tgt: continue
            # birincil: hemen önceki söyleyiş (lag 1) kaynak konuşucuya ait olmalı
            for lag in range(1, lagmax + 1):
                j = i - lag
                if j < 0: break
                p = U[j]
                if p['who'] != src: continue
                if lag == 1 and qfilter is not None and p['q'] != qfilter: continue
                far = [k for k in srcidx if abs(k - i) >= 10]
                if len(far) < 5: continue
                samp = random.sample(far, min(K, len(far)))
                for name, (ok, mt) in MEAS.items():
                    if lagmax > 1 and name not in ('form', 'tam_dl'): continue
                    if not ok(p, t): continue
                    bs = [U[k] for k in samp if ok(U[k], t)]
                    if not bs: continue
                    pb = sum(mt(b, t) for b in bs) / len(bs)
                    c = out[(s['g'], lag)][name]
                    c[0] += 1; c[1] += mt(p, t); c[2] += pb; c[3] += pb * (1 - pb)
    res = {}
    for (g, lag), d in out.items():
        res.setdefault(g, {})[lag] = {name: {'n': c[0], 'k': c[1], 'E': c[2], 'V': c[3],
                                             'obs': c[1] / c[0] if c[0] else None,
                                             'base': c[2] / c[0] if c[0] else None} for name, c in d.items()}
    return res

R = {'AC': run('AC'), 'CA': run('CA'), 'AC_q': run('AC', qfilter=True), 'AC_s': run('AC', qfilter=False),
     'AC_lag': run('AC', lagmax=12)}
G = ['Altınkamış 1;4-2;4', 'Aksu-Koç 2;0-2;8', 'Aksu-Koç 3;0-3;8', 'Aksu-Koç 4;0-4;8']
def fmt(d):
    if not d or d['obs'] is None or not d['base']: return '-'
    return f"{100*d['obs']:.1f}/{100*d['base']:.1f} (x{d['obs']/d['base']:.1f}, n={d['n']})"
for k in ['AC', 'CA', 'AC_q', 'AC_s']:
    print('==', k)
    for g in G:
        if g in R[k]:
            print(' ', g, ' | '.join(f"{m}: {fmt(R[k][g][1].get(m))}" for m in MEAS))
def pooled(k, groups, m, lag=1):
    n = kk = E = V = 0
    for g in groups:
        d = R[k].get(g, {}).get(lag, {}).get(m)
        if d: n += d['n']; kk += d['k']; E += d['E']; V += d['V']
    return n, kk, E, V
print('== pooled Aksu (n, obs%, base%, z)')
for k in ['AC', 'AC_s', 'AC_q', 'CA']:
    for m in MEAS:
        n, kk, E, V = pooled(k, G[1:], m)
        print(k, m, n, round(100*kk/n,1), round(100*E/n,1), round((kk-E)/V**.5,1) if V else None)
# lag profile pooled over Aksu-Koç groups
print('== lag (Aksu pooled)')
for lag in range(1, 13):
    row = []
    for m in ('form', 'tam_dl'):
        n = o = b = 0
        for g in G[1:]:
            d = R['AC_lag'].get(g, {}).get(lag, {}).get(m)
            if d and d['obs'] is not None: n += d['n']; o += d['obs'] * d['n']; b += d['base'] * d['n']
        row.append(f"{m}: {100*o/n:.1f}/{100*b/n:.1f} n={n}" if n else f"{m}: -")
    print(lag, ' | '.join(row))
# oturum / konuşucu sayıları
for g in G:
    S = [s for s in sessions if s['g'] == g]
    print(g, 'oturum', len(S), 'çocuk söyleyişi', sum(u['who'] == 'CHI' for s in S for u in s['utts']),
          'yetişkin', sum(u['who'] == 'ADU' for s in S for u in s['utts']),
          'yetişkin soru oranı', round(sum(u['q'] for s in S for u in s['utts'] if u['who'] == 'ADU') / max(1, sum(u['who'] == 'ADU' for s in S for u in s['utts'])), 3))
json.dump({k: {g: {str(l): v for l, v in d.items()} for g, d in R[k].items()} for k in R},
          open(RES / 'a6_results.json', 'w'), ensure_ascii=False, indent=1)
