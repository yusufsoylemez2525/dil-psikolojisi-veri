from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # depo kökü (dil-psikolojisi-veri/)
EKA = ROOT / 'ek_a'
EXT, WORK, DER = EKA / 'data' / 'external', EKA / 'data' / 'work', EKA / 'data' / 'derived'
RES, FIG = EKA / 'results', EKA / 'figures'
WORK.mkdir(parents=True, exist_ok=True)
import pandas as pd, numpy as np, re, json, math, importlib.metadata as md
import wordfreq, statsmodels.formula.api as smf
d=pd.read_csv(EXT / 'meco' / 'meco_xglm',low_memory=False)
tr=d[d.lang=='tr'].copy()
LN2=math.log(2)
def clean(w):
    w=str(w); w=re.sub(r"[^\wçğıöşüÇĞİÖŞÜâîû'’]+","",w).replace('’',"'")
    return w.replace('I','ı').replace('İ','i').lower()
tr['clean']=tr['ia'].map(clean)
tr['punct']=tr['ia'].astype(str).str.contains(r"[.,;:!?\"“”()…]")
tr['len']=tr['clean'].str.len()
fq={w:wordfreq.zipf_frequency(w,'tr') for w in tr['clean'].unique()}
tr['zipf']=tr['clean'].map(fq)
for c in ['s','s_1.7','s_2.9','s_4.5']: tr[c+'_bit']=tr[c]/LN2
items=tr.drop_duplicates(['trialid','ianum'])[['trialid','ianum','ia','clean','punct','len','zipf','m','s_bit','s_1.7_bit','s_2.9_bit','s_4.5_bit']].sort_values(['trialid','ianum']).copy()
for c in ['len','zipf','s_bit','s_1.7_bit','s_2.9_bit','s_4.5_bit']:
    items['prev_'+c]=items.groupby('trialid')[c].shift(1)
# okuma ölçüleri: ilk geçişte bakılan sözcüklerde ilk geçiş süresi (gaze duration)
fx=tr[(tr['firstrun.skip']==0)&tr['firstrun.dur'].notna()]
g=fx.groupby(['trialid','ianum'])['firstrun.dur'].agg(['mean','count']).rename(columns={'mean':'gaze','count':'nfix'}).reset_index()
sk=tr.groupby(['trialid','ianum'])['skip'].mean().rename('skiprate').reset_index()
it=items.merge(g,on=['trialid','ianum'],how='left').merge(sk,on=['trialid','ianum'],how='left')
keep=it[(it.ianum>1)&(~it.punct)&(it.zipf>0)&(it.nfix>=10)&it.prev_s_bit.notna()].copy()
print('sözcük',len(it),'çözümlemede',len(keep),'okur',tr.subid.nunique(),'metin',tr.trialid.nunique())

s1=it[it.ianum>1]; s2=s1[~s1.punct]; s3=s2[s2.zipf>0]; s4=s3[(s3.nfix>=10)&s3.prev_s_bit.notna()]
print('steps',len(it),len(s1),len(s2),len(s3),len(s4))
print('r skip~s (s3)',round(s3[['skiprate','s_bit']].corr().iloc[0,1],3),'all',round(it[['skiprate','s_bit']].corr().iloc[0,1],3))
rf=smf.ols('gaze ~ len + zipf + prev_len + prev_zipf + s_bit + prev_s_bit',data=keep).fit(); print(rf.params.round(2))
import statsmodels.formula.api as smf2
keep['trial']=keep.trialid.astype(str)
rc=smf.ols('gaze ~ len + zipf + prev_len + prev_zipf + s_bit + prev_s_bit',data=keep).fit(cov_type='cluster',cov_kwds={'groups':keep['trialid']})
print('cluster-by-text se',round(rc.bse['s_bit'],3),round(rc.pvalues['s_bit'],5))
print('items share multi',round(items.m.mean(),3),len(items))
