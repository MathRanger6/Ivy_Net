"""Jazz night controlled branch: PPM all records versus final observed record."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
ROOT=Path('/Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE')
JAZZ=ROOT/'3-Master_Plan/VECTOR_work/new_VECTOR_work/jazz_night'
BASE=ROOT/'3-Master_Plan/VECTOR_work/new_VECTOR_work/manuscript_figures/section_4_5/roster_pressure_comparison/cache'
OUT=Path(__file__).resolve().parent
KEYS=['athlete_id','team_id','season']
NBINS=8
YMAX=.35

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wilson(k,n):
    if n==0:return np.nan,np.nan
    z=1.959963984540054;p=k/n;den=1+z*z/n
    mid=(p+z*z/(2*n))/den;half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return max(0,mid-half),min(1,mid+half)

manifest=json.loads((BASE/'source_manifest.json').read_text())
for name in ['all','last']:assert sha(BASE/f'{name}.pkl')==manifest['cache_sha256'][name]
full=pd.read_pickle(BASE/'all.pkl');last=pd.read_pickle(BASE/'last.pkl')
a=full.loc[full.season.between(2011,2021)&np.isfinite(full.ppm)].copy()
g=a.groupby('season').ppm
z=(a.ppm-g.transform('mean'))/g.transform('std')
assert np.allclose(a.perf,z,rtol=0,atol=1e-12)
a['perf']=z
f=last.loc[last.season.between(2011,2021)&np.isfinite(last.ppm)].copy()
f=f.drop(columns='perf').merge(a[KEYS+['perf']],on=KEYS,how='left',sort=False,validate='one_to_one')
assert f.athlete_id.is_unique
assert set(a.athlete_id)==set(f.athlete_id)
assert a.groupby('athlete_id').Y_draft.nunique().eq(1).all()
assert not a.duplicated(KEYS).any()
assert np.array_equal(f.season.to_numpy(),f.athlete_id.map(a.groupby('athlete_id').season.max()).to_numpy())
old_members=pd.read_csv(JAZZ/'02_eight_bin_comparison/ppm_8bins/naive_candidate_membership.csv.gz')
assert list(map(tuple,f[KEYS].to_numpy()))==list(map(tuple,old_members[KEYS].to_numpy()))
assert np.allclose(f.perf,old_members.perf,rtol=0,atol=1e-12)
assert np.array_equal(f.Y_draft,old_members.Y_draft)
frames={'final_ps':f,'all_ps':a}
edges=np.linspace(a.perf.min(),a.perf.max(),NBINS+1)
assert np.allclose(edges,np.linspace(f.perf.min(),f.perf.max(),NBINS+1),rtol=0,atol=1e-12)
tables={};summary={}
for cohort,d in frames.items():
    assert d.minutes.ge(20).all() and d.Y_draft.isin([0,1]).all()
    d['bin_EW']=pd.cut(d.perf,edges,include_lowest=True,labels=False).astype(int)+1
    d['bin_Q']=np.floor((d.perf.rank(method='first')-1)*NBINS/len(d)).astype(int)+1
    summary[cohort]={'records':len(d),'unique_players':d.athlete_id.nunique(),'positive_records':int(d.Y_draft.sum()),'unique_drafted_players':d.loc[d.Y_draft.eq(1),'athlete_id'].nunique(),'rate':float(d.Y_draft.mean()),'unique_player_seasons':len(d[['athlete_id','season']].drop_duplicates())}
    d[KEYS+['athlete_display_name','team_short_display_name','minutes','ppm','perf','Y_draft','bin_EW','bin_Q']].to_csv(OUT/f'{cohort}_membership.csv.gz',index=False)
    for method in ['EW','Q']:
        rows=[]
        for b in range(1,NBINS+1):
            s=d[d['bin_'+method]==b];n=len(s);k=int(s.Y_draft.sum());lo,hi=wilson(k,n)
            rows.append(dict(cohort=cohort,method=method,bin=b,n=n,positive_records=k,unique_players=s.athlete_id.nunique(),unique_drafted_players=s.loc[s.Y_draft.eq(1),'athlete_id'].nunique(),rate=k/n if n else np.nan,ci_low=lo,ci_high=hi,observed_min=s.perf.min(),observed_max=s.perf.max(),edge_low=edges[b-1] if method=='EW' else np.nan,edge_high=edges[b] if method=='EW' else np.nan))
        t=pd.DataFrame(rows);tables[(cohort,method)]=t
        assert t.n.sum()==len(d) and t.positive_records.sum()==int(d.Y_draft.sum())
        if method=='Q':assert t.n.max()-t.n.min()<=1
    d.groupby('season').agg(records=('athlete_id','size'),unique_players=('athlete_id','nunique'),positive_records=('Y_draft','sum')).to_csv(OUT/f'{cohort}_season_counts.csv')
    split=d.groupby('perf').bin_Q.nunique()
    d.loc[d.perf.isin(split[split>1].index),['perf','bin_Q']].value_counts().sort_index().rename('n').to_csv(OUT/f'{cohort}_quantile_split_ties.csv')
old=pd.read_csv(JAZZ/'02_eight_bin_comparison/ppm_8bins/naive_bin_counts.csv')
for method in ['EW','Q']:
    new=tables[('final_ps',method)];ref=old[old.method==method]
    for col in ['n','rate','ci_low','ci_high','observed_min','observed_max']:
        assert np.allclose(new[col],ref[col],rtol=0,atol=1e-12)
    assert np.array_equal(new.positive_records,ref.drafted)
pd.concat(tables.values()).to_csv(OUT/'bin_counts.csv',index=False)
multi=a[a.duplicated(['athlete_id','season'],keep=False)]
multi[KEYS+['athlete_display_name','team_short_display_name','minutes','ppm','perf','Y_draft']].to_csv(OUT/'multi_team_player_seasons_audit.csv',index=False)

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
def panel(ax,cohort,method):
    t=tables[(cohort,method)];x=t.bin.to_numpy();good=t.n.gt(0)
    color='#347da3' if method=='EW' else '#7860a4'
    bars=ax.bar(x,t.rate.fillna(0),width=.8,color=color,alpha=.9,zorder=2)
    for bar,n in zip(bars,t.n):
        if n<30:bar.set_hatch('///');bar.set_alpha(.5)
    ax.errorbar(x[good],t.loc[good,'rate'],yerr=np.maximum(0,np.vstack([t.loc[good,'rate']-t.loc[good,'ci_low'],t.loc[good,'ci_high'].clip(upper=YMAX-.003)-t.loc[good,'rate']])),fmt='none',ecolor='#242424',elinewidth=1.2,capsize=3,zorder=3)
    cut=t.ci_high.gt(YMAX)&good
    ax.scatter(t.loc[cut,'bin'],np.full(cut.sum(),YMAX-.004),marker='^',s=40,color='#242424',zorder=4)
    for row in t[good].itertuples():
        label='0%' if row.positive_records==0 else (f'{100*row.rate:.2f}%' if row.rate<.01 else f'{100*row.rate:.1f}%')
        ax.annotate(label,(row.bin-.08,row.rate),xytext=(-2,6),textcoords='offset points',ha='right',fontsize=10,fontweight='bold',bbox=dict(facecolor='white',edgecolor='none',alpha=.85,pad=.4),zorder=5)
    labels=[]
    for row in t.itertuples():
        lo,hi=(row.edge_low,row.edge_high) if method=='EW' else (row.observed_min,row.observed_max)
        labels.append(f'{row.bin}\n{lo:.2f} to\n{hi:.2f}')
    ax.set_xticks(x,labels,fontsize=9);ax.set_xlim(.35,8.65);ax.set_ylim(0,YMAX)
    ax.set_yticks(np.arange(0,YMAX+.001,.05));ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=0))
    ax.set_ylabel('Share of records with ever-drafted = yes')
    ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
    name='Final-PS: one final observed record per player' if cohort=='final_ps' else 'All-PS: all eligible player–team–season records'
    s=summary[cohort]
    ax.set_title(f'{name}\n{s["records"]:,} records; {s["positive_records"]:,} positive ({100*s["rate"]:.2f}%)',fontsize=13,fontweight='bold',pad=12)
    ax.set_xlabel('PPM z-score ranges; own performance increases left to right',labelpad=10,fontsize=10)
    tab=ax.table(cellText=[[f'{v:,}' for v in t.n],[f'{v:,}' for v in t.positive_records]],rowLabels=['Records','Ever drafted'],cellLoc='center',bbox=[0,-.43,1,.13])
    tab.auto_set_font_size(False);tab.set_fontsize(10)
    for cell in tab.get_celld().values():cell.set_edgecolor('#c7c7c7');cell.set_linewidth(.45)
header='Performance: PPM, standardized within season | 2011–2021 | All colleges | Team games > 10 | Season minutes ≥ 20\nBoth views contain the same 19,803 players, including 520 ever-drafted players; all-PS counts their repeated records.'
footer='Outcome is ever drafted, not selection in that season. “Ever drafted” counts below bars are positive records, not distinct draft events.\nError bars: descriptive 95% Wilson intervals treating records as independent; NOT adjusted for repeated players or colleges.\n▲ Interval extends above 35%; full intervals in CSV. Hatching: fewer than 30 records. No performance clipping.\nAll-PS retains 73 player-seasons recorded under two teams in the inherited source; see the comparison notes and audit.'
for method in ['EW','Q']:
    fig,axes=plt.subplots(1,2,figsize=(22,8.8))
    fig.subplots_adjust(left=.07,right=.98,bottom=.34,top=.73,wspace=.25)
    title='8 equal-width bins — identical numerical boundaries' if method=='EW' else '8 quantile bins — equal counts within each view; numerical boundaries differ'
    fig.suptitle('PPM: final-season versus all-season records\n'+title,fontsize=20,fontweight='bold',y=.98)
    fig.text(.07,.87,header,fontsize=11,va='top',linespacing=1.6)
    for ax,c in zip(axes,frames):panel(ax,c,method)
    fig.text(.07,.12,footer,fontsize=10,va='top',linespacing=1.5)
    fig.savefig(OUT/f'PPM_{method}8_final_vs_all_PS.png',dpi=200,facecolor='white');plt.close(fig)
fig,axes=plt.subplots(2,2,figsize=(22,15.5))
fig.subplots_adjust(left=.07,right=.98,bottom=.20,top=.82,hspace=.95,wspace=.25)
fig.suptitle('PPM: final-season versus all-season records',fontsize=23,fontweight='bold',y=.98)
fig.text(.07,.935,header,fontsize=12,va='top',linespacing=1.6)
for ri,method in enumerate(['EW','Q']):
    for ax,c in zip(axes[ri],frames):panel(ax,c,method)
    y=axes[ri,0].get_position().y1+.052
    fig.text(.07,y,('EW: 8 equal-width bins, identical boundaries' if method=='EW' else 'Q: 8 equal-count bins per view, different numerical boundaries'),fontsize=15,fontweight='bold')
fig.text(.07,.075,footer,fontsize=11,va='top',linespacing=1.5)
fig.savefig(OUT/'PPM_8bins_final_vs_all_PS_mosaic.png',dpi=200,facecolor='white');plt.close(fig)
provenance={'date':'2026-10-27','question':'Only change final-PS to all-PS, keep PPM, filters and 8 bins','source_cache_hashes':manifest['cache_sha256'],'source_cache':str(BASE),'script_sha256':sha(Path(__file__)),'summary':summary,'settings':{'seasons':[2011,2021],'min_total_season_minutes':20,'min_team_games_exclusive':10,'colleges':'all','performance':'PPM standardized with sample SD on full eligible within-season roster, same z-scores for both views','outcome':'inherited ever-drafted lookup','EW_edges':edges.tolist(),'Q':'rank-first equal counts separately within each cohort; source-order tie allocation','display_y_limits':[0,YMAX],'uncertainty':'pointwise Wilson row-independence approximation; does not account for repeated players or college clustering'},'multi_team_player_seasons':multi.groupby(['athlete_id','season']).ngroups,'multi_team_players':multi.athlete_id.nunique(),'multiple_team_interpretation':'Inherited records retained; do not assume transfers or data errors without further audit','no_model_fitting':True,'no_significance_test':True,'baseline_preserved':str(JAZZ/'02_eight_bin_comparison')}
(OUT/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
(OUT/'validation.txt').write_text('PASS: frozen source hashes; same unique-player set and ever-drafted labels; unique athlete/team/season keys; same season z-scores; final rows in latest eligible season; exact prior final-PS bin counts/rates/intervals; identical EW boundaries; Q counts differ by at most one; every record and positive accounted for.\n')
print(json.dumps(summary,indent=2))
print(pd.concat(tables.values())[['cohort','method','bin','n','positive_records','rate']].to_string(index=False))
