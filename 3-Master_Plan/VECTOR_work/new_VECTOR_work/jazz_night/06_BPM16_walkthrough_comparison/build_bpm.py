from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
OUT=Path(__file__).resolve().parent
ROOT=Path('/Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE')
J=ROOT/'3-Master_Plan/VECTOR_work/new_VECTOR_work/jazz_night'
BASE=ROOT/'3-Master_Plan/VECTOR_work/new_VECTOR_work/manuscript_figures/section_4_5/roster_pressure_comparison/cache'
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((BASE/'source_manifest.json').read_text())
for key in ['all','last']:assert sha(BASE/(key+'.pkl'))==manifest['cache_sha256'][key]
full=pd.read_pickle(BASE/'all.pkl');last=pd.read_pickle(BASE/'last.pkl')
KEYS=['athlete_id','team_id','season']
assert len(last)==last.athlete_id.nunique()==22795 and last.Y_draft.sum()==615
roster=full.loc[full.season.between(2009,2021)&np.isfinite(full.BPM)].copy()
g=roster.groupby('season').BPM
roster['bpm_z']=(roster.BPM-g.transform('mean'))/g.transform('std')
expected=last.loc[np.isfinite(last.BPM)].copy()
d=expected.drop(columns=['perf']).merge(roster[KEYS+['bpm_z']],on=KEYS,how='left',validate='one_to_one',sort=False).rename(columns={'bpm_z':'perf'})
assert list(map(tuple,d[KEYS].to_numpy()))==list(map(tuple,expected[KEYS].to_numpy()))
assert np.array_equal(d.Y_draft,expected.Y_draft)
assert len(d)==d.athlete_id.nunique()==19289 and d.Y_draft.sum()==510
assert d.season.min()==2011 and d.season.max()==2021 and np.isfinite(d.perf).all()
assert d.minutes.ge(20).all()
prior=pd.read_csv(J/'02_eight_bin_comparison/bpm_8bins/naive_candidate_membership.csv.gz')
assert list(map(tuple,d[KEYS].to_numpy()))==list(map(tuple,prior[KEYS].to_numpy()))
assert np.allclose(d.perf,prior.perf,rtol=0,atol=1e-12)
d['bin_Q']=np.floor((d.perf.rank(method='first')-1)*16/len(d)).astype(int)+1
edges=np.linspace(d.perf.min(),d.perf.max(),17)
d['bin_EW']=pd.cut(d.perf,edges,include_lowest=True,labels=False).astype(int)+1
def wilson(k,n):
 if not n:return np.nan,np.nan
 z=1.959963984540054;p=k/n;den=1+z*z/n
 mid=(p+z*z/(2*n))/den;half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
 return max(0,mid-half),min(1,mid+half)
tables={}
for method in ['Q','EW']:
 rows=[]
 for b in range(1,17):
  s=d[d['bin_'+method]==b];n=len(s);k=int(s.Y_draft.sum());lo,hi=wilson(k,n)
  rows.append(dict(method=method,bin=b,n=n,drafted=k,draft_rate=k/n if n else np.nan,ci_low=lo,ci_high=hi,perf_min=s.perf.min(),perf_max=s.perf.max(),edge_low=edges[b-1] if method=='EW' else np.nan,edge_high=edges[b] if method=='EW' else np.nan))
 t=pd.DataFrame(rows);tables[method]=t
 assert t.n.sum()==19289 and t.drafted.sum()==510
 assert t.draft_rate.max()<.5
 t.to_csv(OUT/(method+'16_bin_counts.csv'),index=False)
assert tables['Q'].n.max()-tables['Q'].n.min()<=1
assert np.allclose(np.diff(edges),np.diff(edges)[0])
d[KEYS+['minutes','BPM','perf','Y_draft','bin_Q','bin_EW']].to_csv(OUT/'BPM_Q16_EW16_player_membership.csv.gz',index=False)
excluded=last.loc[~np.isfinite(last.BPM)]
assert len(excluded)==3506 and excluded.Y_draft.sum()==105
excluded[KEYS+['minutes','BPM','Y_draft']].to_csv(OUT/'missing_BPM_final_records.csv.gz',index=False)
coverage=last.assign(BPM_available=np.isfinite(last.BPM)).groupby('season').agg(final_players=('athlete_id','size'),BPM_available=('BPM_available','sum'),ever_drafted=('Y_draft','sum'))
coverage['BPM_drafted']=d.groupby('season').Y_draft.sum().reindex(coverage.index,fill_value=0)
coverage.to_csv(OUT/'coverage_by_season.csv')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
YMAX=.50
def panel(ax,t,method,small=False):
 valid=t.n.gt(0);x=t.bin.to_numpy()
 bars=ax.bar(x,t.draft_rate.fillna(0),width=.76,color='#347da3',alpha=.92,zorder=2)
 for bar,n in zip(bars,t.n):
  if n<30:bar.set_hatch('///');bar.set_alpha(.5)
 low=t.loc[valid,'draft_rate']-t.loc[valid,'ci_low']
 high=t.loc[valid,'ci_high'].clip(upper=YMAX-.004)-t.loc[valid,'draft_rate']
 ax.errorbar(x[valid],t.loc[valid,'draft_rate'],yerr=np.maximum(0,np.vstack([low,high])),fmt='none',ecolor='#303030',elinewidth=1.15,capsize=3,zorder=3)
 clip=valid&t.ci_high.gt(YMAX)
 ax.scatter(x[clip],np.full(clip.sum(),YMAX-.004),marker='^',s=40,color='#303030',zorder=4)
 for row in t.itertuples():
  if not row.n:
   ax.text(row.bin,.013,'Empty',ha='center',rotation=90,fontsize=9);continue
  label='0%' if row.drafted==0 else (f'{100*row.draft_rate:.2f}%' if row.draft_rate<.01 else f'{100*row.draft_rate:.1f}%')
  ax.annotate(label,(row.bin-.08,row.draft_rate),xytext=(-1,6),textcoords='offset points',ha='right',fontsize=8 if small else 9,fontweight='bold',zorder=5,bbox=dict(facecolor='white',edgecolor='none',alpha=.85,pad=.3))
 ax.set_xticks(x);ax.set_xlim(.4,16.6);ax.set_ylim(0,YMAX)
 ax.set_yticks(np.arange(0,.501,.10));ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=0))
 ax.set_ylabel('Observed ever-drafted proportion',fontsize=11)
 ax.set_xlabel('Own-performance bin (1 = lowest BPM; 16 = highest BPM)',fontsize=11,labelpad=11)
 ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
 ax.set_title('Q: 16 equal-count bins' if method=='Q' else 'EW: 16 equal-width bins',fontsize=15,fontweight='bold',pad=14)
 table=ax.table(cellText=[[f'{v:,}' for v in t.n],[str(int(v)) for v in t.drafted]],rowLabels=['Players','Drafted'],cellLoc='center',bbox=[0,-.30,1,.13])
 table.auto_set_font_size(False);table.set_fontsize(8 if small else 9)
 for c in table.get_celld().values():c.set_edgecolor('#c7c7c7');c.set_linewidth(.45)

header='Performance: BPM, standardized within season | 2011–2021 | BPM unavailable for 2009–2010\nFinal eligible record per player | All eligible colleges | MG10: ≥ 11 captured team games | ≥ 20 total season minutes\n19,289 players; 510 ever drafted (2.64%) | 514 additional final records in 2011–2021 lack BPM and are excluded'
footer='Bars: observed rates; error bars: pointwise 95% Wilson intervals, without college-clustering adjustment.\nHatching: fewer than 30 players. ▲ Interval extends above 50%; full values in CSV. Empty means no rate is estimated.\nFinal-PS: latest eligible season, highest-minutes team record if needed. Outcome is ever drafted, not selection in that season.'
for method in ['Q','EW']:
 fig,ax=plt.subplots(figsize=(16,9));fig.subplots_adjust(left=.085,right=.98,top=.70,bottom=.31)
 fig.suptitle('Own performance and the observed chance of being drafted',fontsize=22,fontweight='bold',y=.97)
 fig.text(.085,.90,header,fontsize=10.5,va='top',linespacing=1.7)
 panel(ax,tables[method],method)
 note='Q bins divide ranked performance into nearly equal counts; tied values may be split in source order.' if method=='Q' else f'Each bin spans {np.diff(edges)[0]:.3f} standardized BPM units; full range retained, without clipping.'
 fig.text(.085,.13,footer+'\n'+note,fontsize=9,va='top',linespacing=1.5)
 for ext in ['png','svg']:fig.savefig(OUT/f'naive_BPM_{method}16_available_2011_2021.{ext}',dpi=240,facecolor='white')
 plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(24,9));fig.subplots_adjust(left=.055,right=.985,top=.69,bottom=.31,wspace=.20)
fig.suptitle('BPM: the same players and outcomes, grouped two ways',fontsize=23,fontweight='bold',y=.97)
fig.text(.055,.90,header,fontsize=12,va='top',linespacing=1.65)
panel(axes[0],tables['Q'],'Q',True);panel(axes[1],tables['EW'],'EW',True)
fig.text(.055,.13,footer+'\nCommon 0–50% scale. Q bins have equal counts and unequal numerical widths; EW bins have equal numerical widths and unequal counts.',fontsize=11,va='top',linespacing=1.5)
fig.savefig(OUT/'naive_BPM_Q16_vs_EW16_same_scale.png',dpi=200,facecolor='white');plt.close(fig)
prov={'date':'2026-10-27','metric':'BPM','requested_window':[2009,2021],'available_window':[2011,2021],'n':len(d),'ever_drafted':int(d.Y_draft.sum()),'excluded_missing_BPM':len(excluded),'excluded_drafted':int(excluded.Y_draft.sum()),'source_hashes':manifest['cache_sha256'],'source_directory':str(BASE),'standardization':'sample SD (ddof=1) within season over eligible finite-BPM all-PS roster; before final-PS subset','final_records':'retain canonical selected final record; exclude missing BPM, never substitute earlier season','Q_rule':'floor((rank(method=first)-1)*16/N)+1; source-order ties split; outcomes never used','EW_edges':edges.tolist(),'uncertainty':'pointwise Wilson 95%, no college-clustering adjustment','display_ymax':.5,'comparison':'available-data comparison, not matched-player metric-only test','scope':'walkthrough only; locked PPM figures and JN_progression unchanged'}
(OUT/'provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
(OUT/'validation.txt').write_text('PASS: frozen source hashes; 19,289 unique final-record players, 510 ever drafted; exact membership/outcome and standardized BPM match earlier Jazz BPM cohort; 3,506 missing final records excluded without fallback; every included player accounted for in both 16-bin tables; Q counts differ by at most 1; equal EW interval widths; empty bin has undefined rate; all observed rates fit 0–50%.\n')
print(pd.concat(tables.values())[['method','bin','n','drafted','draft_rate']].to_string(index=False))
