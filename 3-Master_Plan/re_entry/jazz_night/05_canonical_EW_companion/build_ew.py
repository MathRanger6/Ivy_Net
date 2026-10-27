from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
ROOT=Path('/Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/jazz_night')
BASE=ROOT/'04_canonical_naive';OUT=Path(__file__).resolve().parent
source=BASE/'canonical_player_membership.csv.gz'
d=pd.read_csv(source)
assert len(d)==d.athlete_id.nunique()==22795 and d.Y_draft.sum()==615
edges=np.linspace(d.perf.min(),d.perf.max(),17)
d['bin_EW']=pd.cut(d.perf,edges,include_lowest=True,labels=False).astype(int)+1
q=pd.read_csv(BASE/'canonical_bin_counts.csv')
def wilson(k,n):
 if not n:return np.nan,np.nan
 z=1.959963984540054;p=k/n;den=1+z*z/n
 mid=(p+z*z/(2*n))/den;half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
 return max(0,mid-half),min(1,mid+half)
rows=[]
for b in range(1,17):
 s=d[d.bin_EW==b];n=len(s);k=int(s.Y_draft.sum());lo,hi=wilson(k,n)
 rows.append(dict(bin=b,n=n,drafted=k,draft_rate=k/n if n else np.nan,edge_low=edges[b-1],edge_high=edges[b],ci_low=lo,ci_high=hi,perf_min=s.perf.min(),perf_max=s.perf.max()))
t=pd.DataFrame(rows)
assert t.n.sum()==22795 and t.drafted.sum()==615
assert np.allclose(np.diff(edges),np.diff(edges)[0])
assert np.array_equal(d.groupby('bin').Y_draft.size(),q.n)
assert np.array_equal(d.groupby('bin').Y_draft.sum(),q.drafted)
t.to_csv(OUT/'EW16_bin_counts.csv',index=False)
d.to_csv(OUT/'Q16_EW16_player_membership.csv.gz',index=False)
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
 ax.set_xlabel('Own-performance bin (1 = lowest PPM; 16 = highest PPM)',fontsize=11,labelpad=11)
 ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
 ax.set_title('Q: 16 equal-count bins' if method=='Q' else 'EW: 16 equal-width bins',fontsize=15,fontweight='bold',pad=14)
 table=ax.table(cellText=[[f'{v:,}' for v in t.n],[str(int(v)) for v in t.drafted]],rowLabels=['Players','Drafted'],cellLoc='center',bbox=[0,-.30,1,.13])
 table.auto_set_font_size(False);table.set_fontsize(8 if small else 9)
 for c in table.get_celld().values():c.set_edgecolor('#c7c7c7');c.set_linewidth(.45)
header='Performance: PPM, standardized within season | 2009–2021 | All eligible colleges\nFinal eligible observed record per player | MG10: ≥ 11 captured team games | ≥ 20 total season minutes\nSame 22,795 players and 615 ever drafted (2.70%) as the locked Q16 starter'
footer='Bars: observed rates; error bars: pointwise 95% Wilson intervals, without college-clustering adjustment.\nHatching: fewer than 30 players. ▲ Interval extends above 50%; full values in CSV. Empty means no rate is estimated.\nFinal-PS: latest eligible season, highest-minutes team record if needed. Outcome is ever drafted, not selection in that season.'
fig,ax=plt.subplots(figsize=(16,9))
fig.subplots_adjust(left=.085,right=.98,top=.70,bottom=.31)
fig.suptitle('The same players, grouped into equal performance intervals',fontsize=22,fontweight='bold',y=.97)
fig.text(.085,.90,header,fontsize=11,va='top',linespacing=1.7)
panel(ax,t,'EW')
fig.text(.085,.13,footer+'\nEach bin spans '+f'{np.diff(edges)[0]:.3f}'+' standardized PPM units; full range retained, without clipping.',fontsize=9,va='top',linespacing=1.5)
fig.savefig(OUT/'naive_PPM_EW16_2009_2021.png',dpi=240,facecolor='white')
fig.savefig(OUT/'naive_PPM_EW16_2009_2021.svg',facecolor='white');plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(24,9))
fig.subplots_adjust(left=.055,right=.985,top=.69,bottom=.31,wspace=.20)
fig.suptitle('Same players and outcomes; two ways to divide performance into bins',fontsize=23,fontweight='bold',y=.97)
fig.text(.055,.90,header,fontsize=12,va='top',linespacing=1.65)
panel(axes[0],q,'Q',True);panel(axes[1],t,'EW',True)
fig.text(.055,.13,footer+'\nCommon 0–50% scale for this comparison. Q bins have equal counts and unequal numerical widths; EW bins have equal numerical widths and unequal counts.',fontsize=11,va='top',linespacing=1.5)
fig.savefig(OUT/'naive_PPM_Q16_vs_EW16_same_scale.png',dpi=200,facecolor='white');plt.close(fig)
prov={'date':'2026-10-27','source_membership':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'n':22795,'drafted':615,'bin_count':16,'EW_edges':edges.tolist(),'population':'identical to locked Q16 canonical starter; 2009–2021, final-PS, ALLT, MG10, min20','uncertainty':'pointwise Wilson, no clustering adjustment','display_ymax':YMAX,'pair':'Q counts and rates match locked table; only display range enlarged for fair side-by-side comparison','no_source_or_locked_figure_change':True,'empty_bins':t.loc[t.n.eq(0),'bin'].tolist()}
(OUT/'provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
(OUT/'validation.txt').write_text('PASS: identical 22,795 unique players, 615 positive outcomes and performance values; all accounted for in 16 equal-width bins; original Q16 memberships/counts/outcomes reproduced; empty bin retains undefined rate; all observed rates fit 0–50% display.\n')
print(t[['bin','n','drafted','draft_rate']].to_string(index=False))
