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
base='gaze ~ len + zipf + prev_len + prev_zipf'
r0=smf.ols(base,data=keep).fit()
res={'n_items':len(keep),'n_all':len(it),'readers':int(tr.subid.nunique()),'texts':int(tr.trialid.nunique()),'r2_base':r0.rsquared,'models':{}}
for c,lab in [('s_bit','564M'),('s_1.7_bit','1,7B'),('s_2.9_bit','2,9B'),('s_4.5_bit','4,5B')]:
    f=base+f' + Q("{c}") + Q("prev_{c}")'
    r=smf.ols(f,data=keep).fit()
    res['models'][lab]={'dr2':r.rsquared-r0.rsquared,'b':r.params[f'Q("{c}")'],'se':r.bse[f'Q("{c}")'],'p':r.pvalues[f'Q("{c}")'],'b_prev':r.params[f'Q("prev_{c}")'],'se_prev':r.bse[f'Q("prev_{c}")'],'p_prev':r.pvalues[f'Q("prev_{c}")']}
    print(lab,{k:round(v,4) for k,v in res['models'][lab].items()})
rf=smf.ols(base+' + s_bit + prev_s_bit',data=keep).fit()
print(rf.summary().tables[1])
# doğrusallık: ikinci dereceden terim
rq=smf.ols(base+' + s_bit + I(s_bit**2) + prev_s_bit',data=keep).fit()
res['quad']={'b2':rq.params['I(s_bit ** 2)'],'p2':rq.pvalues['I(s_bit ** 2)'],'dr2':rq.rsquared-rf.rsquared}
print('quad',res['quad'])
# okur düzeyi karma model: okur için rastgele kesişim
fx2=fx.merge(items[['trialid','ianum','prev_len','prev_zipf','prev_s_bit']],on=['trialid','ianum'])
fx2=fx2[(fx2.ianum>1)&(~fx2.punct)&(fx2.zipf>0)&fx2.prev_s_bit.notna()].copy()
mm=smf.mixedlm('Q("firstrun.dur") ~ len + zipf + prev_len + prev_zipf + s_bit + prev_s_bit',data=fx2,groups=fx2['subid']).fit()
res['mixed']={'b':mm.params['s_bit'],'se':mm.bse['s_bit'],'p':mm.pvalues['s_bit'],'n':len(fx2),'b_len':mm.params['len'],'b_zipf':mm.params['zipf'],'b_prev':mm.params['prev_s_bit'],'p_prev':mm.pvalues['prev_s_bit']}
print('mixed',res['mixed'])
# kümelere göre ortalamalar (şekil)
keep['bin']=pd.cut(keep.s_bit,bins=[0,2,4,6,8,10,12,14,16,20,40],right=False)
bins=keep.groupby('bin',observed=True).agg(gaze=('gaze','mean'),sd=('gaze','std'),n=('gaze','size'),s=('s_bit','mean')).reset_index()
res['bins']=bins[['s','gaze','sd','n']].to_dict('records')
print(bins)
res['corr_len_s']=keep[['len','s_bit']].corr().iloc[0,1]; res['corr_zipf_s']=keep[['zipf','s_bit']].corr().iloc[0,1]
res['multi_share']=float(items.m.mean()); res['mean_len']=float(items.len.mean())
res['wordfreq']=md.version('wordfreq')
res['skip_mean']=float(tr.skip.mean()); res['gaze_mean']=float(fx['firstrun.dur'].mean())
print({k:res[k] for k in ['corr_len_s','corr_zipf_s','multi_share','mean_len','wordfreq','skip_mean','gaze_mean']})
json.dump(res,open(RES / 'a7_results.json','w'),ensure_ascii=False,indent=1,default=float)
