from pathlib import Path
import os,json,hashlib
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/ncaa_slide_mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
OUT=Path(__file__).resolve().parent
REPO=next(p for p in OUT.parents if (p/'sports/scripts/pass_a_congestion_conditional.py').exists())
source=REPO/'3-Master_Plan/re_entry/HEROs_and_PASSes/pass_a/PASS_A_binned_draft_rate_ability_q16_allt_min20_mg10_9_21_last_ps.csv'
t=pd.read_csv(source)
y=t.n*t.draft_rate
assert np.allclose(y,np.rint(y),atol=1e-8)
t['drafted']=np.rint(y).astype(int)
assert t.n.sum()==22795 and t.drafted.sum()==615
z=1.959963984540054
p=t.drafted/t.n;den=1+z*z/t.n;c=(p+z*z/(2*t.n))/den;h=z*np.sqrt(p*(1-p)/t.n+z*z/(4*t.n*t.n))/den
t['ci_low']=np.maximum(0,c-h);t['ci_high']=np.minimum(1,c+h)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':16,'axes.labelsize':18,'xtick.labelsize':15,'ytick.labelsize':15})
fig,ax=plt.subplots(figsize=(16,9));fig.patch.set_facecolor('white')
fig.suptitle('Own performance and draft outcomes',x=.07,y=.97,ha='left',fontsize=25,fontweight='bold',color='#173c59')
fig.text(.07,.91,'NCAA 2009–2021 | 16 quantile bins of own performance',fontsize=18)
fig.text(.07,.865,'All eligible teams; one final-season observation per player',fontsize=16)
fig.text(.07,.825,'22,795 players; 615 ever drafted',fontsize=15,color='#444444')
color='#276c97'
ax.errorbar(t.perf_mean,100*t.draft_rate,yerr=[np.maximum(0,100*(t.draft_rate-t.ci_low)),np.maximum(0,100*(t.ci_high-t.draft_rate))],fmt='o-',color=color,lw=2.6,ms=7,mew=1.6,elinewidth=1.4,capsize=4)
for r in t.itertuples():ax.text(r.perf_mean,-.105,str(int(r.n)),transform=ax.get_xaxis_transform(),ha='center',va='top',fontsize=11)
ax.text(-.015,-.105,'n',transform=ax.transAxes,ha='right',va='top',fontsize=12)
ax.set_xlim(-2.15,2.45);ax.set_ylim(0,20)
ax.set_ylabel('Players ever drafted (%)')
ax.set_xlabel('Own performance\nPoints per minute, standardized within season',labelpad=41)
ax.grid(axis='y',alpha=.22);ax.spines[['top','right']].set_visible(False)
fig.text(.07,.069,'Pointwise 95% Wilson intervals; no team-clustering adjustment. Counts under points.',fontsize=12,color='#444444')
fig.text(.07,.04,'Observed outcomes across own-performance bins; not simulated deterministic top-K selection.',fontsize=12,color='#444444')
fig.subplots_adjust(left=.095,right=.975,top=.775,bottom=.255)
fig.savefig(OUT/'ncaa_naive_2009_2021_own_performance.png',dpi=220,facecolor='white');plt.close(fig)
t.to_csv(OUT/'naive_plotted_bins.csv',index=False)
(OUT/'naive_provenance.json').write_text(json.dumps({'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'n':22795,'drafted':615,'bins':16,'binning':'quantile','axis':'own within-season PPM z score; bin mean','uncertainty':'Pointwise 95% Wilson from integer counts recovered and checked against saved rates; not cluster-adjusted','note':'Saved empirical rates unchanged; visual styling matches panels 9, 7, 8.'},indent=2))
print(OUT/'ncaa_naive_2009_2021_own_performance.png')
