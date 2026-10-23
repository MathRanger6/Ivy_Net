"""Entry 3: subdivide the exact saved own-performance bin, without changing cohort."""
from pathlib import Path
import os, json, hashlib
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/ncaa_walkthrough_mpl')
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
W=HERE.parents[1]
cache=W/'manuscript_figures/section_4_5/roster_pressure_comparison/cache'
source=cache/'last.pkl'
manifest=json.loads((cache/'source_manifest.json').read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(source)==manifest['cache_sha256']['last']
d=pd.read_pickle(source)
assert len(d)==d.athlete_id.nunique()==22795
assert d.Y_draft.isin([0,1]).all() and int(d.Y_draft.sum())==615
assert np.isfinite(d.perf).all()
d['original_bin']=np.floor((d.perf.rank(method='first')-1)*16/len(d)).astype(int)+1
refpath=W/'lab_presentation_20261022/empirical_ncaa_2009_2021/naive_plotted_bins.csv'
ref=pd.read_csv(refpath)
check=d.groupby('original_bin').agg(n=('perf','size'),drafted=('Y_draft','sum'),perf_mean=('perf','mean'))
assert np.array_equal(check.n,ref.n) and np.array_equal(check.drafted,ref.drafted)
assert np.allclose(check.perf_mean,ref.perf_mean,rtol=0,atol=1e-12)
top=d.loc[d.original_bin==16].copy()
top['subbin']=np.floor((top.perf.rank(method='first')-1)*8/len(top)).astype(int)+1
s=top.groupby('subbin').agg(n=('perf','size'),drafted=('Y_draft','sum'),z_min=('perf','min'),z_max=('perf','max'),z_mean=('perf','mean')).reset_index()
assert s.n.tolist()==[178]*8 and s.drafted.sum()==228
s['not_drafted']=s.n-s.drafted
s['rate']=s.drafted/s.n
s['full_cohort_percentile_low']=100*(len(d)-len(top)+s.n.cumsum()-s.n)/len(d)
s['full_cohort_percentile_high']=100*(len(d)-len(top)+s.n.cumsum())/len(d)
z=1.959963984540054
c=(s.rate+z*z/(2*s.n))/(1+z*z/s.n)
h=z*np.sqrt(s.rate*(1-s.rate)/s.n+z*z/(4*s.n*s.n))/(1+z*z/s.n)
s['ci_low']=c-h;s['ci_high']=c+h
splits=[]
for k in range(1,8):
 a=top.loc[top.subbin==k,'perf'].max();b=top.loc[top.subbin==k+1,'perf'].min()
 splits.append(bool(a==b))
s.to_csv(HERE/'highest_bin_counts.csv',index=False)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12})
fig,ax=plt.subplots(figsize=(13.5,7.6))
fig.suptitle('Inside the highest own-performance bin',x=.075,ha='left',y=.98,fontsize=22,fontweight='bold')
fig.text(.075,.925,'NCAA 2009–2021 | All eligible colleges | One final season per player',fontsize=13)
fig.text(.075,.885,'Performance: PPM, standardized within season | Original bin: 228 / 1,424 ever drafted (16.0%)',fontsize=12)
colors=plt.cm.Blues(np.linspace(.45,.85,8))
ax.bar(s.subbin,s.rate*100,color=colors,width=.72,zorder=2)
ax.errorbar(s.subbin,s.rate*100,yerr=[(s.rate-s.ci_low)*100,(s.ci_high-s.rate)*100],fmt='none',ecolor='#253747',capsize=4,lw=1.2,zorder=3)
for row in s.itertuples():
 ax.text(row.subbin,row.ci_high*100+1.1,f'{row.rate*100:.1f}%\n{row.drafted} / {row.n}',ha='center',va='bottom',fontsize=12)
ax.axhline(100*228/1424,color='#555555',ls='--',lw=1,label='Original bin average: 16.0%',zorder=1)
ax.set_ylim(0,35);ax.set_ylabel('Players ever drafted (%)')
ax.set_xticks(s.subbin,[f'{r.subbin}\n{r.z_min:.2f}–{r.z_max:.2f}' for r in s.itertuples()])
ax.set_xlabel('Eight equal-count quantile groups, ordered from lower to higher own performance\nObserved performance z-score range shown under each group',labelpad=13)
ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.18,zorder=0);ax.set_axisbelow(True)
ax.legend(loc='upper left',frameon=False,fontsize=11)
fig.text(.075,.075,'Each bar contains 178 distinct players; labels show ever drafted / total. This is a zoom of the original top ~6.25%.',fontsize=11)
fig.text(.075,.04,'No performance clipping. Whiskers: descriptive 95% Wilson intervals, without college clustering. No significance tests.',fontsize=10.5)
fig.subplots_adjust(left=.075,right=.985,top=.81,bottom=.245)
fig.savefig(HERE/'highest_bin_draft_rates.png',dpi=220,facecolor='white');plt.close(fig)
meta=dict(source=str(source),source_sha256=sha(source),source_inputs=manifest['inputs'],original_bins=str(refpath),original_bins_sha256=sha(refpath),original_16_bins_exact_counts_and_means_verified=True,population='2009–2021 all eligible colleges, final-season snapshot, min 20 recorded season minutes, more than 10 team-season games',performance='PPM standardized within season; frozen historical values retained',outcome='Ever drafted, not annual draft probability',whole_cohort_n=len(d),whole_cohort_drafted=int(d.Y_draft.sum()),top_bin_n=len(top),top_bin_drafted=int(top.Y_draft.sum()),subbins=8,binning='Equal-count rank-first within exact original bin 16; stable source order breaks ties',tie_split_at_new_boundaries=splits,clipping='None to own performance',uncertainty='Pointwise Wilson 95%, no college-clustering correction; no significance tests',script_sha256=sha(Path(__file__)))
(HERE/'highest_bin_provenance.json').write_text(json.dumps(meta,indent=2)+'\n')
print(s[['subbin','n','drafted','not_drafted','rate','z_min','z_max']].to_string(index=False))
print('Tied values split at new boundaries:',splits)
