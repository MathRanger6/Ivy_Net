"""Reproduce the saved canonical own-performance plot, with a reusable visual style."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
ROOT=Path('/Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE')
BASE=ROOT/'3-Master_Plan/VECTOR_work/new_VECTOR_work/manuscript_figures/section_4_5/roster_pressure_comparison/cache'
REF=ROOT/'3-Master_Plan/re_entry/HEROs_and_PASSes/pass_a/PASS_A_binned_draft_rate_ability_q16_allt_min20_mg10_9_21_last_ps.csv'
OUT=Path(__file__).resolve().parent
STYLE=json.loads((OUT/'plot_style.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wilson(k,n):
 z=1.959963984540054;p=k/n;den=1+z*z/n
 mid=(p+z*z/(2*n))/den;half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
 return max(0,mid-half),min(1,mid+half)
manifest=json.loads((BASE/'source_manifest.json').read_text())
for key in ['all','last']:assert sha(BASE/f'{key}.pkl')==manifest['cache_sha256'][key]
a=pd.read_pickle(BASE/'last.pkl').copy();roster=pd.read_pickle(BASE/'all.pkl')
assert (len(a),int(a.Y_draft.sum()),a.athlete_id.nunique())==(22795,615,22795)
assert a.season.between(2009,2021).all() and a.minutes.ge(20).all()
g=roster.groupby('season').ppm
assert np.allclose(roster.perf,(roster.ppm-g.transform('mean'))/g.transform('std'),rtol=0,atol=1e-12)
a['vent']=np.floor((a.perf.rank(method='first')-1)*16/len(a)).astype(int)
t=a.groupby('vent').agg(n=('Y_draft','size'),draft_rate=('Y_draft','mean'),perf_mean=('perf','mean'),perf_median=('perf','median')).reset_index()
ref=pd.read_csv(REF)
for col in ref.columns:assert np.allclose(t[col],ref[col],rtol=0,atol=1e-12),col
assert np.diff(t.draft_rate).min()>=0
extra=a.groupby('vent').agg(drafted=('Y_draft','sum'),perf_min=('perf','min'),perf_max=('perf','max')).reset_index()
t=t.merge(extra,on='vent',validate='one_to_one')
t['bin']=t.vent+1
t[['ci_low','ci_high']]=[wilson(k,n) for k,n in zip(t.drafted,t.n)]
assert t.n.sum()==22795 and t.drafted.sum()==615
assert t.n.max()-t.n.min()<=1
t.to_csv(OUT/'canonical_bin_counts.csv',index=False)
a[['athlete_id','team_id','season','athlete_display_name','minutes','ppm','perf','Y_draft','vent']].assign(bin=a.vent+1).to_csv(OUT/'canonical_player_membership.csv.gz',index=False)
shutil.copy2(REF,OUT/'source_canonical_ability_bins.csv')
plt.rcParams.update({'font.family':STYLE['font_family'],'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=STYLE['figure_size_inches'])
fig.subplots_adjust(left=.085,right=.98,top=.72,bottom=.31)
x=t.bin.to_numpy();color=STYLE['observed_color'];ymin,ymax=STYLE['y_limits']
assert ymax>t.draft_rate.max(),'Increase the display maximum to show every observed rate.'
bars=ax.bar(x,t.draft_rate,width=.76,color=color,alpha=.92,zorder=2)
for b,n in zip(bars,t.n):
 if n<STYLE['thin_n']:b.set_hatch('///');b.set_alpha(.5)
if STYLE['show_wilson_intervals']:
 upper=t.ci_high.clip(upper=ymax-.001)
 ax.errorbar(x,t.draft_rate,yerr=np.maximum(0,np.vstack([t.draft_rate-t.ci_low,upper-t.draft_rate])),fmt='none',ecolor='#303030',elinewidth=1.2,capsize=3,zorder=3)
 clipped=t.ci_high.gt(ymax)
 ax.scatter(x[clipped],np.full(clipped.sum(),ymax-.001),marker='^',color='#303030',s=35,zorder=4)
if STYLE['show_rate_labels']:
 for row in t.itertuples():
  label='0%' if row.drafted==0 else (f'{100*row.draft_rate:.2f}%' if row.draft_rate<.01 else f'{100*row.draft_rate:.1f}%')
  ax.annotate(label,(row.bin-.12,row.draft_rate),xytext=(-1,6),textcoords='offset points',ha='right',fontsize=9,fontweight='bold',zorder=5,bbox=dict(facecolor='white',edgecolor='none',alpha=.85,pad=.3))
ax.set_xticks(x);ax.set_xlim(.4,16.6);ax.set_ylim(ymin,ymax)
ax.set_yticks(np.arange(ymin,ymax+.0001,STYLE['y_tick_step']));ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=1))
ax.set_ylabel('Observed ever-drafted proportion',fontsize=12)
ax.set_xlabel('Own-performance quantile bin (1 = lowest PPM; 16 = highest PPM)',fontsize=12,labelpad=12)
ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
if STYLE['show_counts']:
 tab=ax.table(cellText=[[f'{n:,}' for n in t.n],[str(int(k)) for k in t.drafted]],rowLabels=['Players','Drafted'],cellLoc='center',bbox=[0,-.30,1,.13])
 tab.auto_set_font_size(False);tab.set_fontsize(9)
 for cell in tab.get_celld().values():cell.set_edgecolor('#c7c7c7');cell.set_linewidth(.45)
fig.suptitle(STYLE['title'],fontsize=22,fontweight='bold',y=.97)
fig.text(.085,.895,'Performance: PPM, standardized within season | 2009–2021 | 16 equal-count quantile bins',fontsize=13)
fig.text(.085,.855,'All eligible colleges | Team captured games ≥ 11 (MG10) | Total recorded season minutes ≥ 20',fontsize=11)
fig.text(.085,.815,'One final eligible observed record per player | 22,795 players; 615 ever drafted (2.70%)',fontsize=11)
footer=('Bars: observed rates. Error bars: pointwise 95% Wilson intervals; no college-clustering adjustment.\n'
        'Final-PS = latest eligible season; highest-minutes team record if multiple teams. Outcome is ever drafted, not draft in that season.\n'
        'Quantile spacing shows rank groups, not equal PPM intervals. No own-performance clipping; full bin ranges are saved in the counts file.')
fig.text(.085,.13,footer,fontsize=10,va='top',linespacing=1.65)
fig.savefig(OUT/'canonical_naive_PPM_Q16_2009_2021.png',dpi=STYLE['dpi'],facecolor='white')
fig.savefig(OUT/'canonical_naive_PPM_Q16_2009_2021.svg',facecolor='white')
plt.close(fig)
prov={'date':'2026-10-27','reference_csv':str(REF),'reference_csv_sha256':sha(REF),'cache_sha256':manifest['cache_sha256'],'n_players':22795,'ever_drafted':615,'seasons':[2009,2021],'metric':'PPM standardized within season on eligible full roster with sample SD','population':'all colleges, final eligible observed season; maximum minutes team if needed','min_total_recorded_season_minutes':20,'min_team_captured_games_exclusive':10,'outcome':'ever drafted','bins':16,'binning':'floor((rank(method=first)-1)*16/N); no tying together or outcome-based ordering','reference_reproduction':'all counts, rates, performance means and medians match within 1e-12','display_style':STYLE,'script_sha256':sha(Path(__file__)),'no_model_fit':True,'comparison_limit':'Different years and bin count from earlier Jazz 2011–2021/Q8; this reproduces the chosen historical anchor, not a one-factor comparison.'}
(OUT/'provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
(OUT/'validation.txt').write_text('PASS: source fingerprints; within-season PPM standardization; 22,795 unique players and 615 drafted; all 16 original bin counts, rates, performance means and medians; complete membership accounting; rates nondecreasing; all observed values within displayed y range.\n')
print('Exact canonical reproduction verified. Highest bin:',int(t.iloc[-1].drafted),'/',int(t.iloc[-1].n),'=',t.iloc[-1].draft_rate)
