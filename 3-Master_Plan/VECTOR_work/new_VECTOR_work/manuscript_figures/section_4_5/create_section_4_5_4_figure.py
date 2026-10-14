"""Matched basketball panels for Section 4.5.4. Read local sources; no scraping.

Reconstruct the historical final-season cohort with the original loader and
check its totals and original overall bins before making a new comparison.
Never infer new bin counts from already aggregated, incompatible histograms.
"""
from pathlib import Path
import sys
import json
import hashlib
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p/'sports/scripts/pass_a_congestion_conditional.py').exists())
SOURCE = REPO/'3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox'
REF_CSV = SOURCE/'hero/PASS_A_binned_draft_rate_poolq_loo_ew16_allt_min20_mg10_09_21_last_ps_perm_loo_ever_lastps_ew16.csv'
ELITE_META = SOURCE/'_DISPOSABLE_elite_pond_loo_twin/ELITE_pond_loo_pw4p7_allt_min20_mg10_top7_ppm_9_21_last_ps.json'


def count_bins(frame, edges, label):
    x = frame['poolq_loo'].to_numpy(float)
    # Left-closed intervals, with the maximum included in the final interval.
    bins = np.searchsorted(edges, x, side='right')-1
    bins[x == edges[-1]] = len(edges)-2
    if ((bins < 0) | (bins >= len(edges)-1)).any():
        raise ValueError('Observed peer scores outside shared bin range')
    result = []
    for k in range(len(edges)-1):
        g = frame.iloc[np.flatnonzero(bins == k)]
        n, y = len(g), int(g['Y_draft'].sum())
        rate = y/n if n else np.nan
        if n:
            z = 1.959963984540054
            den = 1+z*z/n
            center = (rate+z*z/(2*n))/den
            half = z*np.sqrt(rate*(1-rate)/n+z*z/(4*n*n))/den
            low, high = center-half, center+half
        else:
            low = high = np.nan
        result.append(dict(panel=label, bin=k+1, left=edges[k], right=edges[k+1],
            center=(edges[k]+edges[k+1])/2, n=n, drafted=y, rate=rate,
            ci_low=low, ci_high=high, team_seasons=len(g[['team_id','season']].drop_duplicates())))
    return pd.DataFrame(result)


def load_verified_cohort():
    for p in (REPO/'sports/scripts', REPO/'sports'):
        if str(p) not in sys.path:
            sys.path.insert(0,str(p))
    from pass_a_congestion_conditional import CctSpec, _prepare_panel
    spec = CctSpec(season_min=2009, season_max=2021, min_minutes=20.,
        min_team_season_games=10, winsor_lo=.01, winsor_hi=.99,
        n_bins=16, ai_lo=None, ai_hi=None, ai_top_pct=7., perf_metric='ppm',
        poolq_binning='equal_width', dft=False, y_draft_mode='ever', panel_rows='last-ps')
    print('Reconstructing saved-specification basketball cohort from local data...', flush=True)
    panel = _prepare_panel(spec)
    use = panel.dropna(subset=['perf','poolq_loo','Y_draft','team_id','season']).copy()
    cut = spec.ai_perf_cut(use)
    band = spec.apply_ai_band(use)
    expected = json.loads(ELITE_META.read_text())
    actual = (len(use), int(use.Y_draft.sum()), len(band), int(band.Y_draft.sum()))
    if actual != (22795,615,1596,246) or not np.isclose(cut,expected['ai_perf_cut'],rtol=0,atol=1e-10):
        raise ValueError(f'Source cohort changed: {actual}, cutoff={cut}. Expected 22795/615 and 1596/246. Stop for source review; do not relabel as the old candidates.')
    ref = pd.read_csv(REF_CSV)
    reference_edges = np.r_[ref.edge_lo.iloc[0], ref.edge_hi.to_numpy()]
    check = count_bins(use,reference_edges,'all')
    if not np.array_equal(check.n,ref.n) or not np.array_equal(check.drafted,ref.drafts):
        raise ValueError('Rebuilt counts do not reproduce the saved overall panel. Stop for source review.')
    print('Verified historical cohort totals, top-7% cutoff, and all 16 original overall bin counts.',flush=True)
    return use, reference_edges


def make_figure(panel, reference_edges, *, top_percent=7., n_bins=16,
                share_y=False, thin_n=30, save=True, output_dir=HERE):
    if not 0 < top_percent < 100 or not isinstance(n_bins,int) or n_bins < 2:
        raise ValueError('Choose 0 < top_percent < 100 and integer n_bins >= 2')
    if thin_n < 1:
        raise ValueError('thin_n must be positive')
    # Derive boundaries once from full-cohort peer range, NEVER separately by panel.
    edges = reference_edges.copy() if n_bins == 16 else np.linspace(reference_edges[0], reference_edges[-1],n_bins+1)
    cut = float(panel.perf.quantile(1-top_percent/100))
    elite = panel.loc[panel.perf >= cut]
    frames = [panel,elite]
    labels = ['All eligible players',f'Top {top_percent:g}% by own performance']
    tables = [count_bins(f,edges,label) for f,label in zip(frames,labels)]
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
    fig,axes = plt.subplots(1,2,figsize=(15.6,7.5),sharex=True,sharey=share_y)
    colors = ['#356d95','#b24b36']
    maxupper = max(t.ci_high.max()*100 for t in tables)
    for ax,t,f,label,color in zip(axes,tables,frames,labels,colors):
        valid = t.n > 0
        ax.plot(t.center,t.rate*100,color=color,lw=1.7,zorder=2)
        for _,r in t.loc[valid].iterrows():
            ax.errorbar(r.center,r.rate*100,
                yerr=[[max(0,(r.rate-r.ci_low)*100)],[max(0,(r.ci_high-r.rate)*100)]],
                fmt='o',ms=5,mfc='white' if r.n<thin_n else color,mec=color,
                ecolor=color,elinewidth=1,capsize=2,zorder=3)
        ax.set_title(f'{label}\n{len(f):,} players; {int(f.Y_draft.sum()):,} ever drafted',pad=13,fontweight='bold')
        ax.set_ylabel('Players ever drafted (%)')
        ax.set_xlabel('Average teammate performance (within-season z score)\nFocal player excluded',labelpad=58)
        ax.set_ylim(0, (maxupper if share_y else t.ci_high.max()*100)*1.12)
        ax.grid(axis='y',alpha=.2)
        ax.spines[['top','right']].set_visible(False)
        ax.set_xticks(edges[::max(1,n_bins//5)])
        ax.tick_params(axis='x',labelsize=9)
        for _,r in t.iterrows():
            ax.text(r.center,-.13,f'{int(r.n)}\n{int(r.team_seasons)}',
                transform=ax.get_xaxis_transform(),ha='center',va='top',fontsize=7)
        ax.text(-.02,-.13,'Players\nTeam-seasons',transform=ax.transAxes,
                ha='right',va='top',fontsize=7)
    fig.suptitle('Selection across peer environments: the full cohort and a performance band',fontsize=16,y=.97)
    scale_note = 'Shared vertical scale.' if share_y else 'Different vertical scales; compare their labels.'
    fig.text(.5,.025,f'2009–2021 final-season cohort. Shared {n_bins} equal-width peer bins. {scale_note}\n'
        f'Bars: descriptive 95% Wilson intervals, not adjusted for team clustering. Open circles: fewer than {thin_n} players. Empty bins have no rate.',
        ha='center',fontsize=9)
    fig.subplots_adjust(left=.075,right=.98,top=.82,bottom=.32,wspace=.24)
    data = pd.concat(tables,ignore_index=True)
    meta = dict(created=datetime.now().astimezone().isoformat(),top_percent=top_percent,
        performance_cutoff=cut,n_bins=n_bins,edges=edges.tolist(),share_y=share_y,thin_n=thin_n,
        all_n=len(panel),all_drafted=int(panel.Y_draft.sum()),band_n=len(elite),band_drafted=int(elite.Y_draft.sum()),
        axis='Mean other-teammate within-season points-per-minute z score; NOT full-group T_j',
        outcome='Ever drafted label attached to final observed season; not annual draft probability',
        peer_winsor_quantiles=[.01,.99],cohort='2009-2021, min20 minutes, mg10, all teams, last-ps',
        original_overall_counts_verified=True,source_csv=str(REF_CSV),source_band_metadata=str(ELITE_META),
        reference_csv_sha256=hashlib.sha256(REF_CSV.read_bytes()).hexdigest(),
        cohort_sha256=hashlib.sha256(pd.util.hash_pandas_object(panel[['athlete_id','season','team_id','perf','poolq_loo','Y_draft']],index=False).values.tobytes()).hexdigest(),
        uncertainty='Pointwise 95% Wilson; no cluster correction; descriptive, not causal',
        note='Bin boundaries fixed from full cohort before filtering performance. Historical band-specific piecewise bins replaced.')
    paths=[]
    if save:
        output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
        stem=f'figure_4_5_4_basketball_shared_ew{n_bins}_top{top_percent:g}'
        for ext in ['png','svg','pdf']:
            path=output_dir/f'{stem}.{ext}';fig.savefig(path,dpi=220,facecolor='white');paths.append(path)
        data.to_csv(output_dir/f'{stem}_bins.csv',index=False)
        (output_dir/f'{stem}_provenance.json').write_text(json.dumps(meta,indent=2)+'\n')
        print('Saved:',paths[0],flush=True)
    return fig,data,meta,paths

if __name__=='__main__':
    p,e=load_verified_cohort()
    make_figure(p,e)
