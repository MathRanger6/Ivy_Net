from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
J=Path('/Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/jazz_night')
O=Path(__file__).resolve().parent
B=J/'04_canonical_naive'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
d=pd.read_csv(B/'canonical_player_membership.csv.gz')
t=pd.read_csv(B/'canonical_bin_counts.csv').sort_values('bin').reset_index(drop=True)
N=len(d);K=int(d.Y_draft.sum())
assert N==d.athlete_id.nunique()==22795 and K==615
assert np.isfinite(d.perf).all() and d.Y_draft.isin([0,1]).all()
# Outcome establishes capacity only. Stable source order breaks exact performance ties.
d['performance_rank']=d.perf.rank(method='first',ascending=False).astype(int)
d['topK_selected']=d.performance_rank.le(K).astype(int)
t['topK_selected']=d.groupby('bin').topK_selected.sum().reindex(t.bin).to_numpy()
t['topK_rate']=t.topK_selected/t.n
assert np.array_equal(d.groupby('bin').size().to_numpy(),t.n)
assert np.array_equal(d.groupby('bin').Y_draft.sum().to_numpy(),t.drafted)
assert d.topK_selected.sum()==K and t.topK_selected.sum()==K
assert t.iloc[-1].topK_selected==615 and t.iloc[:-1].topK_selected.sum()==0
assert t.iloc[-1].drafted==228 and t.iloc[:-1].drafted.sum()==387
ranked=d.sort_values('performance_rank')
cut=float(ranked.iloc[K-1].perf);below=float(ranked.iloc[K].perf)
t.to_csv(O/'observed_vs_topK_bin_counts.csv',index=False)
d.to_csv(O/'player_membership_and_topK.csv.gz',index=False)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(16,9))
fig.subplots_adjust(left=.105,right=.98,top=.69,bottom=.33)
x=t.bin.to_numpy();w=.34
ax.bar(x-.19,t.draft_rate,width=w,color='#347da3',label='Observed ever drafted',zorder=3)
ax.bar(x+.19,t.topK_rate,width=w,color='#d27a24',label='Deterministic top-K benchmark',zorder=3)
ax.errorbar(x-.19,t.draft_rate,yerr=np.maximum(0,np.vstack([t.draft_rate-t.ci_low,t.ci_high-t.draft_rate])),fmt='none',ecolor='#303030',elinewidth=1,capsize=2,zorder=4)
for row in t.itertuples():
 if row.drafted:
  label=f'{row.draft_rate:.1%}' if row.draft_rate>=.01 else f'{row.draft_rate:.2%}'
  ax.annotate(label,(row.bin-.19,row.ci_high),xytext=(-1,4),textcoords='offset points',ha='center',fontsize=9,fontweight='bold',color='#245c7b')
ax.annotate(f'{t.iloc[-1].topK_rate:.1%}',(16.19,t.iloc[-1].topK_rate),xytext=(0,6),textcoords='offset points',ha='center',fontsize=11,fontweight='bold',color='#9d5310')
ax.text(2.2,.305,'Top-K selects nobody in bins 1–15.\nThe data contain 387 drafted players in those bins.',fontsize=12,linespacing=1.6,bbox={'facecolor':'#f4f6f8','edgecolor':'none','pad':10})
ax.set_xticks(x);ax.set_xlim(.4,16.7);ax.set_ylim(0,.5)
ax.set_yticks(np.arange(0,.501,.1));ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=0))
ax.set_ylabel('Proportion drafted / selected',fontsize=12)
ax.set_xlabel('Own-performance quantile bin (1 = lowest PPM; 16 = highest PPM)',fontsize=12,labelpad=10)
ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
ax.legend(loc='upper left',frameon=False,fontsize=11)
tab=ax.table(cellText=[[f'{int(v):,}' for v in t.n],[str(int(v)) for v in t.drafted],[str(int(v)) for v in t.topK_selected]],rowLabels=['Players','Observed drafted','Top-K selected'],cellLoc='center',bbox=[0,-.40,1,.18])
tab.auto_set_font_size(False);tab.set_fontsize(8.5)
for (r,c),cell in tab.get_celld().items():
 cell.set_edgecolor('#c7c7c7');cell.set_linewidth(.45)
 if r==1:cell.set_facecolor('#edf5f9')
 if r==2:cell.set_facecolor('#fcf2e8')
fig.suptitle('Does selecting the highest-performing players reproduce the observed pattern?',fontsize=19,fontweight='bold',y=.97)
fig.text(.105,.90,'Performance: PPM, standardized within season | 2009–2021 | Same 16 quantile bins as JN-01',fontsize=12)
fig.text(.105,.86,'All eligible colleges | ≥ 11 captured team games (MG10) | ≥ 20 total season minutes | Final eligible record per player',fontsize=10.5)
fig.text(.105,.82,'N = 22,795 players | K = 615 in both cases (2.70%) | SCORE: Sᵢ = Aᵢ → SELECT: the highest 615 scores',fontsize=12)
fig.text(.105,.77,'Pooled descriptive benchmark across years; not a reconstruction of annual NBA drafts.',fontsize=11,color='#555555')
footer='Observed bars: ever-drafted outcomes; error bars: pointwise 95% Wilson intervals, without college-clustering adjustment.\nBenchmark bars: exact fractions selected by the fixed top-K rule; no simulation or uncertainty interval.\nTop-K is binary for each player. Its 43.2% in the highest bin reflects 615 selected out of 1,424 players in that bin.\nFinal-PS: latest eligible season, highest-minutes team record if needed. Same bins and source data as the locked PPM starter.'
fig.text(.105,.135,footer,fontsize=9,va='top',linespacing=1.5)
for ext in ['png','svg']:fig.savefig(O/f'JN02_PPM_observed_vs_topK_Q16.{ext}',dpi=240,facecolor='white')
plt.close(fig)
prov={'date':'2026-10-27','status':'ready for review, not locked','source_hashes':{p.name:sha(p) for p in [B/'canonical_player_membership.csv.gz',B/'canonical_bin_counts.csv']},'N':N,'K':K,'score':'S_i=A_i; A_i=within-season standardized PPM','selection':'one pooled descriptive ranking, descending performance, top 615; stable source-order tie break, never outcome-based','years':[2009,2021],'binning':'existing locked Q16 memberships retained exactly','boundary_selected_perf':cut,'boundary_unselected_perf':below,'tie_at_cutoff':cut==below,'top_bin_observed':228,'top_bin_benchmark':615,'top_bin_n':1424,'observed_below_top_bin':387,'model_fitted':False,'simulated':False,'scope':'pooled descriptive benchmark, not annual selection pools; not proof of intrinsic randomness','y_limits':[0,.5]}
(O/'provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
(O/'validation.txt').write_text('PASS: exact locked membership, bins, observed counts and rates; 22,795 unique players; 615 observed outcomes and exactly 615 benchmark selections; ranking uses only performance/source order; all selected in bin 16; 228 observed in bin 16 and 387 below; all values and observed intervals within 0–50%.\n')
print(json.dumps(prov,indent=2))
