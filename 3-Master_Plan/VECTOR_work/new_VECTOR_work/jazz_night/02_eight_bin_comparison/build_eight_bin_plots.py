"""Jazz night step 1: observed own-performance/draft rates; no model fitting."""
from pathlib import Path
import hashlib, json, argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

ROOT = Path('/Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE')
BASE = ROOT/'3-Master_Plan/VECTOR_work/new_VECTOR_work/manuscript_figures/section_4_5/roster_pressure_comparison'
SOURCE = BASE/'aligned_threshold_bands/runs/20261025_191833_184458/candidate_reference.csv.gz'
ARGS=argparse.ArgumentParser()
ARGS.add_argument('--metric',choices=['BPM','PPM'],required=True)
METRIC=ARGS.parse_args().metric
OUT = Path(__file__).resolve().parent / (METRIC.lower()+'_8bins')
OUT.mkdir(exist_ok=True)
NBINS = 8
YMAX = .35
KEYS = ['athlete_id','team_id','season']

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def wilson(k,n):
    if not n:
        return np.nan,np.nan
    z=1.959963984540054
    rate=k/n
    center=(rate+z*z/(2*n))/(1+z*z/n)
    half=z*np.sqrt(rate*(1-rate)/n+z*z/(4*n*n))/(1+z*z/n)
    return max(0,center-half),min(1,center+half)

def main():
    manifest=json.loads((BASE/'cache/source_manifest.json').read_text())
    for name in ['all','last']:
        assert sha(BASE/f'cache/{name}.pkl')==manifest['cache_sha256'][name]
    full=pd.read_pickle(BASE/'cache/all.pkl')
    last=pd.read_pickle(BASE/'cache/last.pkl')
    metric_col='BPM' if METRIC=='BPM' else 'ppm'
    roster=full.loc[full.season.between(2011,2021)&np.isfinite(full[metric_col])].copy()
    g=roster.groupby('season')[metric_col]
    roster['check_perf']=(roster[metric_col]-g.transform('mean'))/g.transform('std')
    expected=last.loc[last.season.between(2011,2021)&np.isfinite(last[metric_col])].copy()
    d=expected.drop(columns=['perf']).merge(roster[KEYS+['check_perf']],on=KEYS,how='left',validate='one_to_one',sort=False).rename(columns={'check_perf':'perf'})
    assert list(map(tuple,d[KEYS].to_numpy()))==list(map(tuple,expected[KEYS].to_numpy()))
    assert np.array_equal(d.Y_draft,expected.Y_draft)
    if METRIC=='BPM':
        baseline=pd.read_csv(SOURCE)
        assert list(map(tuple,d[KEYS].to_numpy()))==list(map(tuple,baseline[KEYS].to_numpy()))
        assert np.allclose(d.perf,baseline.perf,rtol=0,atol=1e-12)
        assert (len(d),int(d.Y_draft.sum()))==(19289,510)
    else:
        assert np.allclose(d.perf,expected.perf,rtol=0,atol=1e-12)
        assert (len(d),int(d.Y_draft.sum()))==(19803,520)
    assert len(d)==d.athlete_id.nunique()
    assert d.season.between(2011,2021).all() and d.minutes.ge(20).all()
    assert d.Y_draft.isin([0,1]).all() and np.isfinite(d.perf).all()
    # Retain source order for deterministic tie allocation; never use outcome to break ties.
    q=np.floor((d.perf.rank(method='first')-1)*NBINS/len(d)).astype(int)+1
    edges=np.linspace(d.perf.min(),d.perf.max(),NBINS+1)
    ew=pd.cut(d.perf,edges,include_lowest=True,labels=False).astype(int)+1
    d['bin_Q']=q;d['bin_EW']=ew
    tables={}
    for method in ['EW','Q']:
        rows=[]
        for b in range(1,NBINS+1):
            sub=d.loc[d['bin_'+method]==b]
            n=len(sub);k=int(sub.Y_draft.sum());lo,hi=wilson(k,n)
            rows.append(dict(method=method,bin=b,n=n,drafted=k,rate=k/n if n else np.nan,
                ci_low=lo,ci_high=hi,observed_min=sub.perf.min(),observed_max=sub.perf.max(),
                mean_performance=sub.perf.mean(),edge_low=edges[b-1] if method=='EW' else np.nan,
                edge_high=edges[b] if method=='EW' else np.nan,
                colleges=sub.team_id.nunique(),college_seasons=len(sub[['team_id','season']].drop_duplicates())))
        tables[method]=pd.DataFrame(rows)
        assert tables[method].n.sum()==len(d) and tables[method].drafted.sum()==int(d.Y_draft.sum())
    assert tables['Q'].n.max()-tables['Q'].n.min()<=1
    d[KEYS+['athlete_display_name','team_short_display_name','minutes',metric_col,'perf','Y_draft','bin_EW','bin_Q']].to_csv(OUT/'naive_candidate_membership.csv.gz',index=False)
    pd.concat(tables.values()).to_csv(OUT/'naive_bin_counts.csv',index=False)
    d.groupby('season').agg(players=('athlete_id','size'),drafted=('Y_draft','sum')).to_csv(OUT/'naive_counts_by_season.csv')
    split=d.groupby('perf').bin_Q.nunique()
    tievals=split[split>1].index
    d.loc[d.perf.isin(tievals),['perf','bin_Q']].value_counts().sort_index().rename('n').to_csv(OUT/'quantile_split_ties.csv')

    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    def panel(ax,t,method):
        x=t.bin.to_numpy(); good=t.n.gt(0)
        color='#347da3' if method=='EW' else '#7860a4'
        bars=ax.bar(x,t.rate.fillna(0),width=.8,color=color,alpha=.9,zorder=2)
        for bar,n in zip(bars,t.n):
            if n<30:bar.set_hatch('///');bar.set_alpha(.5)
        ax.errorbar(x[good],t.loc[good,'rate'],
            yerr=np.maximum(0,np.vstack([t.loc[good,'rate']-t.loc[good,'ci_low'],t.loc[good,'ci_high'].clip(upper=YMAX-.003)-t.loc[good,'rate']])),
            fmt='none',ecolor='#242424',elinewidth=1.3,capsize=4,zorder=3)
        clipped=t.n.gt(0)&t.ci_high.gt(YMAX)
        ax.scatter(t.loc[clipped,'bin'],np.full(clipped.sum(),YMAX-.004),marker='^',s=45,color='#242424',zorder=4)
        for row in t.loc[good].itertuples():
            label='0%' if row.drafted==0 else (f'{100*row.rate:.2f}%' if row.rate<.01 else f'{100*row.rate:.1f}%')
            ax.annotate(label,(row.bin-.12,row.rate),xytext=(-4,6),textcoords='offset points',ha='right',fontsize=10,fontweight='bold',color='#222222',zorder=5,bbox=dict(facecolor='white',edgecolor='none',alpha=.85,pad=.7))
        labels=[]
        for row in t.itertuples():
            lo,hi=(row.edge_low,row.edge_high) if method=='EW' else (row.observed_min,row.observed_max)
            labels.append(f'{row.bin}\n{lo:.2f} to\n{hi:.2f}')
            if row.n==0:
                ax.text(row.bin,.025,'Empty',ha='center',fontsize=9,color='#555555',rotation=90)
        ax.set_xticks(x,labels,fontsize=9)
        ax.set_xlim(.35,NBINS+.65);ax.set_ylim(0,YMAX)
        ax.set_yticks(np.arange(0,YMAX+.001,.05))
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        ax.set_ylabel('Observed ever-drafted proportion')
        ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
        ax.set_title((f'EW: {NBINS} equal-width bins' if method=='EW' else f'Q: {NBINS} equal-count quantile bins')+'\nOwn performance increases from left to right',fontweight='bold',fontsize=14,pad=12)
        ax.set_xlabel(f'Own-performance bin: {METRIC} z-score range (bin spacing is categorical)',labelpad=9)
        tab=ax.table(cellText=[[f'{v:,}' for v in t.n],[f'{v:,}' for v in t.drafted]],
            rowLabels=['Players','Drafted'],cellLoc='center',bbox=[0,-.43,1,.13])
        tab.auto_set_font_size(False);tab.set_fontsize(10)
        for cell in tab.get_celld().values():cell.set_edgecolor('#c7c7c7');cell.set_linewidth(.45)

    header=f'Performance: {METRIC}, standardized within season | 2011–2021 | All colleges\nMG10: team games > 10 | min=20: season minutes ≥ 20 | One final observed season per player'
    footer=f'N = {len(d):,} players; {int(d.Y_draft.sum()):,} ever drafted ({100*d.Y_draft.mean():.2f}%). Outcome: ever drafted, not draft in that season.\nBars: observed rates. Error bars: pointwise 95% Wilson intervals, without college-clustering adjustment.\nShared y-axis: 0–35%. ▲ Interval extends above 35%; full intervals retained in counts CSV.\nFull performance range retained. Hatching: fewer than 30 players. Quantile ties split in fixed source order.'
    for method,t in tables.items():
        fig,ax=plt.subplots(figsize=(14,8.4))
        fig.subplots_adjust(left=.105,right=.98,top=.72,bottom=.31)
        fig.suptitle('NCAA naïve plot: own performance and draft outcomes',y=.98,fontsize=19,fontweight='bold')
        fig.text(.105,.91,header,va='top',fontsize=11,linespacing=1.6)
        panel(ax,t,method)
        fig.text(.105,.08,footer,va='top',fontsize=9,linespacing=1.5)
        fig.savefig(OUT/f'naive_{METRIC}_2011_2021_MG10_min20_{method}{NBINS}.png',dpi=240,facecolor='white')
        plt.close(fig)
    fig,axes=plt.subplots(2,1,figsize=(15,13.8))
    fig.subplots_adjust(left=.105,right=.98,top=.83,bottom=.19,hspace=.87)
    fig.suptitle('NCAA naïve plot: two ways to bin the same players',y=.98,fontsize=21,fontweight='bold')
    fig.text(.105,.935,header,va='top',fontsize=12,linespacing=1.6)
    for ax,(method,t) in zip(axes,tables.items()):panel(ax,t,method)
    fig.text(.105,.067,footer,va='top',fontsize=10,linespacing=1.5)
    fig.savefig(OUT/f'naive_{METRIC}_EW{NBINS}_vs_Q{NBINS}.png',dpi=220,facecolor='white');plt.close(fig)
    provenance=dict(task='Jazz night step 1: empirical naive plot',date='2026-10-27',
        source=str(BASE/'cache/last.pkl'),source_sha256=sha(BASE/'cache/last.pkl'),source_manifest=manifest,
        script_sha256=sha(Path(__file__)),performance=f'{METRIC} z-score; sample SD within season on full eligible finite-metric roster',
        cohort='Inherited final-observed-season cohort; all colleges; no draftee-college restriction; one row per athlete',
        seasons=[2011,2021],min_total_season_minutes=20,min_team_games_exclusive=10,
        outcome='Ever drafted (existing lookup), not same-season selection',n=len(d),drafted=int(d.Y_draft.sum()),
        bin_count=NBINS,EW_edges=edges.tolist(),Q=f'rank-first floor((rank-1)*{NBINS}/N)+1; stable snapshot row order',
        quantile_distinct_values_split=int(len(tievals)),uncertainty='95% pointwise Wilson, binomial independence approximation; not college-cluster-adjusted or simultaneous',
        no_clipping=True,display_y_limits=[0,YMAX],display_ci_overflow='Upward triangles at 35%; full CI values retained in CSV',no_fitting=True,under100_minutes=int(d.minutes.lt(100).sum()),
        final_season_limit='Final observed season in source window, not necessarily final career season; 2021 right boundary retains active players',
        missing_metric='Missing final-row metric excluded; no fallback to earlier season',
        plotting='Categorical bin positions; numeric ranges shown; equal visual bar width does not indicate equal numeric bin width for Q')
    (OUT/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    (OUT/'validation.txt').write_text(f'PASS: frozen cache fingerprints; reconstructed {METRIC} standardization; candidate identities and outcomes; unique athletes; 2011–2021 and season minutes ≥20; each method totals {len(d)} and {int(d.Y_draft.sum())}; quantile counts differ by at most one.\n')
    print(pd.concat(tables.values())[['method','bin','n','drafted','rate','observed_min','observed_max']].to_string(index=False))
    print('Players under 100 season minutes:',provenance['under100_minutes'])
    print('Split quantile tie values:',len(tievals))

if __name__=='__main__':main()
