# A.5: UD Türkçe IMST'de belirtme durumlu nesnenin bağlı olduğu fiilin yapı türü
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # depo kökü (dil-psikolojisi-veri/)
EKA = ROOT / 'ek_a'
EXT, WORK, DER = EKA / 'data' / 'external', EKA / 'data' / 'work', EKA / 'data' / 'derived'
RES, FIG = EKA / 'results', EKA / 'figures'
WORK.mkdir(parents=True, exist_ok=True)
import glob,collections,json,re
D=str(EXT / 'UD_Turkish-IMST')
sents=[]
for f in sorted(glob.glob(D+'/*.conllu')):
    cur=[];meta={}
    for line in open(f,encoding='utf-8'):
        line=line.rstrip('\n')
        if line.startswith('# text ='): meta['text']=line[9:]
        elif line.startswith('# sent_id'): meta['id']=line.split('=')[1].strip()
        elif not line:
            if cur: sents.append((meta,cur)); cur=[];meta={}
        elif not line.startswith('#'):
            c=line.split('\t')
            if '-' in c[0] or '.' in c[0]: continue
            feats=dict(x.split('=',1) for x in c[5].split('|')) if c[5]!='_' else {}
            cur.append({'id':int(c[0]),'form':c[1],'lemma':c[2],'upos':c[3],'feats':feats,'head':int(c[6]) if c[6]!='_' else 0,'dep':c[7]})
print('cümle',len(sents),'sözcük',sum(len(s) for _,s in sents))
def clause_type(v,toks):
    vf=v['feats'].get('VerbForm','Fin')
    d=v['dep'].split(':')[0]
    if vf=='Part' and d in ('acl','amod','nmod'): return 'ilgi cümleciği (sıfat-fiil)'
    if vf=='Part': return 'sıfat-fiil (öteki)'
    if vf=='Vnoun': return 'ad-fiil tümleci'
    if vf=='Conv': return 'zarf-fiil'
    return 'çekimli yüklem'
C=collections.Counter(); C_init=collections.Counter(); C_after_nom=collections.Counter()
examples=collections.defaultdict(list)
for meta,toks in sents:
    byid={t['id']:t for t in toks}
    for t in toks:
        if t['feats'].get('Case')=='Acc' and t['upos'] in ('NOUN','PROPN','PRON') and t['dep'].startswith('obj'):
            h=byid.get(t['head'])
            if not h or h['upos'] not in ('VERB','AUX'): continue
            ct=clause_type(h,toks); C[ct]+=1
            # ortam: cümle başındaki yalın ad öbeğinden sonra gelen belirtme durumlu nesne
            words=[x for x in toks if x['upos']!='PUNCT']
            first=words[0] if words else None
            prev_noms=[x for x in toks if x['id']<t['id'] and x['upos'] in ('NOUN','PROPN') and x['feats'].get('Case')=='Nom' and x['dep'].startswith('nsubj')]
            if prev_noms:
                C_after_nom[ct]+=1
                if ct.startswith('ilgi') and len(meta.get('text',''))<120:
                    examples['nom_acc_rel'].append((meta['id'],meta['text'],prev_noms[0]['form'],t['form'],h['form']))
                if ct=='çekimli yüklem' and len(meta.get('text',''))<90:
                    examples['nom_acc_fin'].append((meta['id'],meta['text'],prev_noms[0]['form'],t['form'],h['form']))
# ilgi cümleciği yükleminin hemen önündeki öğe nesne mi?
tot=sum(C.values()); tn=sum(C_after_nom.values())
print('\nBelirtme durumlu nesnenin bağlı olduğu fiil (tümü):',tot)
for k,v in C.most_common(): print(f'  {k}: {v} (%{100*v/tot:.1f})')
print('\nÖncesinde yalın özne bulunan belirtme durumlu nesneler:',tn)
for k,v in C_after_nom.most_common(): print(f'  {k}: {v} (%{100*v/tn:.1f})')
for k in examples: 
    print('\n',k,len(examples[k]))
    for e in examples[k][:12]: print('  ',e)
# Örnek cümleler (IMST metni) yalnız yerel çalışma klasörüne yazılır; yayımlanan sonuç dosyası yalnız sayımları içerir.
json.dump(examples,open(WORK / 'a5_ornek_cumleler.json','w'),ensure_ascii=False,indent=1)
json.dump({'all':C,'after_nom':C_after_nom},open(RES / 'a5_results.json','w'),ensure_ascii=False,indent=1)
# Biçimce hem çekimli fiil hem sıfat-fiil olabilen -mIş ve -(y)AcAk sonlu fiiller
amb=collections.defaultdict(collections.Counter); ambex=collections.defaultdict(list)
for meta,toks in sents:
    byid={t['id']:t for t in toks}
    for i,t in enumerate(toks):
        if t['upos'] not in ('VERB','AUX'): continue
        f=t['form'].lower()
        for lab,rx in [('-mIş',r'(mış|miş|muş|müş)$'),('-(y)AcAk',r'(acak|ecek)$')]:
            if re.search(rx,f):
                vf=t['feats'].get('VerbForm','Fin'); d=t['dep'].split(':')[0]
                if vf=='Part' and d in ('acl','amod'): k='ad niteleyen sıfat-fiil'
                elif vf=='Part': k='öteki sıfat-fiil'
                elif vf=='Fin' or d in ('root','conj','parataxis'): k='çekimli yüklem'
                else: k='öteki'
                amb[lab][k]+=1
                if k=='ad niteleyen sıfat-fiil' and len(meta.get('text',''))<80: ambex[lab].append(meta['text'])
print('\nSonu -mIş ve -(y)AcAk olan fiil biçimleri')
for lab,c in amb.items():
    n=sum(c.values()); print(' ',lab,n,{k:f'{v} (%{100*v/n:.1f})' for k,v in c.most_common()})
    for e in ambex[lab][:6]: print('     ',e)
R=json.load(open(RES / 'a5_results.json')); R['amb']=amb; json.dump(R,open(RES / 'a5_results.json','w'),ensure_ascii=False,indent=1)
