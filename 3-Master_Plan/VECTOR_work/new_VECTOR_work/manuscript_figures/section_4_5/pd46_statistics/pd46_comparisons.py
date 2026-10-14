"""PD46 exploratory draft-rate comparisons. Local data only; no model refitting."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from create_section_4_5_4_figure import load_verified_cohort, REF_CSV, ELITE_META


def prepare(panel, settings):
    """Define peer regions using all eligible players, then filter own performance."""
    lo, hi = settings['years']
    if not 2009 <= lo <= hi <= 2021:
        raise ValueError('Use years within the verified 2009-2021 source window.')
    p = panel.loc[panel.season.between(lo, hi)].copy()
    if p.empty or p.athlete_id.duplicated().any():
        raise ValueError('Expected a nonempty cohort with exactly one row per player.')
    if not p.Y_draft.isin([0, 1]).all():
        raise ValueError('Draft outcome must be zero or one.')
    pct = settings['top_percent']
    a, b = settings['peer_percentiles']
    if not 0 < pct <= 100 or not 0 < a < b < 100:
        raise ValueError('Check top_percent and the two increasing peer_percentiles.')
    cut = float(p.perf.quantile(1-pct/100))
    qlo, qhi = p.poolq_loo.quantile([a/100, b/100]).to_numpy()
    if qlo >= qhi:
        raise ValueError('Peer quantile boundaries coincide. Choose distinct boundaries.')
    band = p.loc[p.perf >= cut].copy()
    d = band.loc[band.poolq_loo >= qlo].copy()
    # Boundary ties stay together: the upper boundary belongs to the strongest group.
    d['tail'] = (d.poolq_loo >= qhi).astype(int)
    labels = {0: f'Comparison: peer percentiles {a:g} to {b:g}',
              1: f'Strongest: peer percentiles {b:g} to 100'}
    rows = []
    for k, label in labels.items():
        g = d.loc[d['tail'] == k]
        rows.append(dict(group=label, players=len(g), ever_drafted=int(g.Y_draft.sum()),
                         draft_rate_percent=100*g.Y_draft.mean(), colleges=g.team_id.nunique(),
                         mean_own_performance=g.perf.mean(), mean_peer_performance=g.poolq_loo.mean()))
    columns = ['athlete_id','season','team_id','perf','poolq_loo','Y_draft']
    meta = dict(settings=json.loads(json.dumps(settings)), cohort_players=len(p),
                performance_cutoff=cut, peer_cutoffs=[float(qlo),float(qhi)], band_players=len(band),
                cohort_hash=hashlib.sha256(pd.util.hash_pandas_object(p[columns],index=False).values.tobytes()).hexdigest(),
                source_csv=str(REF_CSV), source_metadata=str(ELITE_META),
                source_csv_sha256=hashlib.sha256(REF_CSV.read_bytes()).hexdigest(),
                population='One final observed season per player; all eligible teams; minimum 20 minutes and 10 team-season games.',
                outcome='Ever drafted, not draft in this season.',
                scaling='Original within-season performance standardization and peer winsorization retained when restricting years.',
                regions='Player-weighted peer quantiles in the full eligible cohort, before filtering own performance. Ties kept together.',
                inference='Exploratory after inspecting related plots. No correction for historical searches. No causal interpretation.')
    return p, band, d, pd.DataFrame(rows), meta


def compare(d, adjusted=False):
    """Risk difference via OLS; college-cluster sandwich SE and t(G-1) inference.

    Unadjusted OLS with intercept and a binary group indicator equals the raw
    difference of proportions. College clusters encompass multiple seasons.
    Independence between colleges is an approximation, not a randomization claim.
    """
    import statsmodels.formula.api as smf
    from scipy.stats import t
    if set(d['tail'].unique()) != {0, 1}:
        raise ValueError('Both comparison groups must contain players.')
    g = d.team_id.nunique()
    if g < 3 or d.groupby('tail').team_id.nunique().min() < 2:
        raise ValueError('Too few colleges for even an exploratory clustered comparison.')
    formula = 'Y_draft ~ tail + perf + C(season)' if adjusted else 'Y_draft ~ tail'
    model = smf.ols(formula, data=d)
    if np.linalg.matrix_rank(model.exog) < model.exog.shape[1]:
        raise ValueError('Regression columns are redundant; review the selected population.')
    if len(d) <= model.exog.shape[1] + 1:
        raise ValueError('Insufficient observations for this specification.')
    fit = model.fit(cov_type='cluster', cov_kwds={'groups':d.team_id, 'use_correction':True})
    estimate, se = float(fit.params['tail']), float(fit.bse['tail'])
    if not np.isfinite(se) or se <= 0:
        raise ValueError('Uncertainty cannot be estimated reliably for these data.')
    df = g-1
    margin = float(t.ppf(.975,df))*se
    p = float(2*t.sf(abs(estimate/se),df))
    return pd.DataFrame([dict(comparison='Own performance and season adjusted' if adjusted else 'Raw rate difference',
        tail_minus_comparison_pp=100*estimate, ci95_low_pp=100*(estimate-margin),
        ci95_high_pp=100*(estimate+margin), two_sided_p=p, colleges=g, players=len(d),
        standard_error_pp=100*se, t_degrees_of_freedom=df,
        caution='Exploratory; few clusters in either region or highly unequal cluster sizes can make inference unreliable.')])


def region_plot(summary):
    fig, ax = plt.subplots(figsize=(9,5))
    ax.bar(range(2),summary.draft_rate_percent,color=['#427ca5','#ae394e'],width=.55)
    ax.set_xticks(range(2),summary.group.str.replace(': ',':\n',regex=False))
    for i,r in summary.iterrows():
        ax.annotate(f'{int(r.ever_drafted)}/{int(r.players)} players\n{int(r.colleges)} colleges',
                    (i,r.draft_rate_percent),xytext=(0,7),textcoords='offset points',ha='center')
    ax.set_ylim(0,max(5,summary.draft_rate_percent.max()*1.35))
    ax.set_ylabel('Players ever drafted (%)')
    ax.set_title('First comparison: draft rates in two defined peer environments')
    ax.spines[['top','right']].set_visible(False)
    fig.tight_layout()
    return fig


def resolution_plots(p, band, settings):
    """All requested resolutions; no peak selection or significance search."""
    counts = settings['plot_bin_counts']
    if not counts or any(not isinstance(n,int) or n < 2 for n in counts):
        raise ValueError('plot_bin_counts must contain integers of at least two.')
    fig, axes = plt.subplots(len(counts),2,figsize=(13,4*len(counts)),squeeze=False,sharey=True)
    tables=[]
    for row,n in enumerate(counts):
        for col,method in enumerate(['Equal width','Quantiles']):
            edges = (np.linspace(p.poolq_loo.min(),p.poolq_loo.max(),n+1) if col==0
                     else np.unique(p.poolq_loo.quantile(np.linspace(0,1,n+1))))
            if len(edges)<3:
                raise ValueError('Not enough distinct peer scores for plotting.')
            categories=pd.cut(band.poolq_loo,edges,include_lowest=True,labels=False)
            rows=[]
            for k in range(len(edges)-1):
                z=band.loc[categories==k]
                rows.append(dict(method=method,requested_bins=n,actual_bins=len(edges)-1,bin=k+1,
                    left=edges[k],right=edges[k+1],players=len(z),ever_drafted=int(z.Y_draft.sum()),
                    colleges=z.team_id.nunique(),peer_center=(edges[k]+edges[k+1])/2,
                    draft_rate_percent=100*z.Y_draft.mean()))
            table=pd.DataFrame(rows);tables.append(table)
            ax=axes[row,col]
            ax.plot(table.peer_center,table.draft_rate_percent,'o-',color='#ae394e')
            for r in rows:
                if r['players']:
                    ax.annotate(str(r['players']),(r['peer_center'],r['draft_rate_percent']),xytext=(0,6),textcoords='offset points',ha='center',fontsize=8)
            a,b=p.poolq_loo.quantile(np.array(settings['peer_percentiles'])/100)
            ax.axvspan(a,b,color='#427ca5',alpha=.12,label='Comparison region')
            ax.axvspan(b,p.poolq_loo.max(),color='#ae394e',alpha=.1,label='Strongest region')
            ax.set_title(f'{method}: {len(edges)-1} bins | top {settings["top_percent"]:g}% own performance')
            ax.set_xlabel('Mean other-teammate performance (z score)')
            ax.set_ylabel('Players ever drafted (%)');ax.grid(alpha=.2)
    axes[0,0].legend(fontsize=8)
    fig.suptitle('Resolution check: numbers show players per bin; shading keeps the comparison fixed',y=1.002)
    fig.tight_layout()
    return fig,pd.concat(tables,ignore_index=True)


def college_thirds(d, seed):
    """Descriptive partition, not independent confirmation or a new search."""
    teams=np.array(sorted(d.team_id.unique(),key=str))
    np.random.default_rng(seed).shuffle(teams)
    allocation={team:k%3+1 for k,team in enumerate(teams)}
    rows=[]
    for part in [1,2,3]:
        z=d.loc[d.team_id.map(allocation)==part]
        rates=z.groupby('tail').Y_draft.mean()
        rows.append(dict(subset=part,colleges=z.team_id.nunique(),
            comparison_players=int((z['tail']==0).sum()),strongest_players=int((z['tail']==1).sum()),
            comparison_drafted=int(z.loc[z['tail']==0,'Y_draft'].sum()),strongest_drafted=int(z.loc[z['tail']==1,'Y_draft'].sum()),
            tail_minus_comparison_pp=100*(rates.get(1,np.nan)-rates.get(0,np.nan))))
    return pd.DataFrame(rows)


def save_run(meta, tables, figures):
    out=HERE/'runs'/datetime.now().astimezone().strftime('%Y%m%d_%H%M%S_%f')
    out.mkdir(parents=True,exist_ok=False)
    for name,table in tables.items():
        table.to_csv(out/f'{name}.csv',index=False)
    for name,fig in figures.items():
        fig.savefig(out/f'{name}.png',dpi=180,bbox_inches='tight')
    meta={**meta,'saved_at':datetime.now().astimezone().isoformat(),
          'completed_tables':list(tables),'completed_figures':list(figures),
          'analysis_code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (out/'settings_and_provenance.json').write_text(json.dumps(meta,indent=2)+'\n')
    print('Saved aggregate results, settings, and provenance:',out)
    return out


def highlighted_original_curve(p, band, reference_edges, settings):
    """Preserve the original 16 equal-width bins; overlay individual-level regions."""
    from create_section_4_5_4_figure import count_bins
    table = count_bins(band, reference_edges, 'Top own-performance band')
    a, b = settings['peer_percentiles']
    qlo, qhi = p.poolq_loo.quantile([a/100, b/100]).to_numpy()
    blue = band.loc[(band.poolq_loo >= qlo) & (band.poolq_loo < qhi)]
    red = band.loc[band.poolq_loo >= qhi]
    fig, ax = plt.subplots(figsize=(12.5,7.3))
    ax.axvspan(qlo, qhi, color='#427ca5', alpha=.19,
               label=f'Comparison: peer percentiles {a:g}-{b:g}')
    ax.axvspan(qhi, reference_edges[-1], color='#ae394e', alpha=.13,
               label=f'Strongest: peer percentiles {b:g}-100')
    ax.axvline(qlo,color='#427ca5',lw=1.3,ls=':')
    ax.axvline(qhi,color='#ae394e',lw=1.3,ls=':')
    ax.plot(table.center,table.rate*100,'o-',color='#30373e',lw=2,
            label='Original 16 equal-width-bin curve')
    for _,r in table.iterrows():
        if r.n:
            ax.annotate(f'{int(r.drafted)}/{int(r.n)}',(r.center,100*r.rate),
                        xytext=(0,9),textcoords='offset points',ha='center',fontsize=9)
    for frame, left, right, color in [(blue,qlo,qhi,'#427ca5'),(red,qhi,reference_edges[-1],'#ae394e')]:
        rate=100*frame.Y_draft.mean()
        ax.hlines(rate,left,right,colors=color,ls='--',lw=2)
        ax.text((left+right)/2,35,
            f'{int(frame.Y_draft.sum())}/{len(frame)} drafted\nCombined rate: {rate:.1f}%',
            ha='center',va='center',color=color,fontweight='bold',fontsize=11)
    peak=table.loc[table.rate.idxmax()]
    peak_region = ('RED range' if peak.center >= qhi else 'BLUE range' if peak.center >= qlo else 'unshaded range')
    ax.annotate(f'Highest observed bin\ncenter in the {peak_region}',
        xy=(peak.center,100*peak.rate),xytext=(-145,34),textcoords='offset points',
        arrowprops={'arrowstyle':'->','color':'#30373e'},fontsize=10,ha='center')
    ax.set_ylim(0,40)
    ax.set_xlim(reference_edges[0]-.025,reference_edges[-1]+.025)
    ax.set_xlabel('Mean teammate performance (z score; focal player excluded)',fontsize=11)
    ax.set_ylabel('Players ever drafted (%)',fontsize=11)
    years=settings['years']
    ax.set_title(f'Where the first test falls on the original curve\nTop {settings["top_percent"]:g}% by own performance | {years[0]}-{years[1]} | one observation per player',fontsize=14,pad=16)
    ax.legend(loc='upper left',fontsize=9,framealpha=.95)
    ax.grid(axis='y',alpha=.15);ax.spines[['top','right']].set_visible(False)
    fig.text(.5,.045,'Point labels: drafted / players in each original bin. Dashed lines: combined rates within the shaded ranges.\nPercentile boundaries can split an original bin; combined rates use player records, not averages of plotted points.\nDescriptive display; uncertainty bars omitted here for clarity. No statistical test has been run.',ha='center',fontsize=9)
    fig.subplots_adjust(bottom=.22,top=.85,left=.08,right=.98)
    return fig, table


def peak_tail_test(band, edges, *, repetitions=9999, seed=46, account_grouping=True):
    """One-sided, single-step max-t college-cluster multiplier bootstrap.

    For k=1,...,14, D_k = rate(bin k) - rate(bins k+1,k+2 pooled).
    College influence psi_gk sums residual/N contributions from both sides.
    SE_k^2 = G/(G-1) sum_g psi_gk^2. Centered multiplier draws are
    Z*_bk = sqrt(G/(G-1)) sum_g w_bg psi_gk / SE_k, w_bg in {-1,+1}.
    The SAME college weights apply to every contrast, preserving their dependence.
    Adjusted p_k = (1 + count(max_j Z*_bj >= D_k/SE_k))/(B+1).
    This is an asymptotic influence-function bootstrap, NOT an exact permutation
    test, not a pairs bootstrap, and not a fitted all-bins-equal outcome simulation.
    It holds observed memberships, score cutoffs and bin edges fixed.
    """
    from create_section_4_5_4_figure import count_bins
    edges = np.asarray(edges, dtype=float)
    if len(edges) != 17 or not np.all(np.isfinite(edges)) or not np.all(np.diff(edges) > 0):
        raise ValueError('This test requires the 17 ordered edges of the original 16-bin curve.')
    if not isinstance(repetitions, (int,np.integer)) or repetitions < 999:
        raise ValueError('Use at least 999 bootstrap repetitions; the default is 9999.')
    if band.empty or band[['team_id','poolq_loo','Y_draft']].isna().any().any():
        raise ValueError('Missing college, peer score or outcome. Review the population.')
    if not band.Y_draft.isin([0,1]).all() or band.athlete_id.duplicated().any():
        raise ValueError('Require binary outcomes and one row per athlete.')
    x = band.poolq_loo.to_numpy(float)
    bins = np.searchsorted(edges,x,side='right')-1
    bins[x == edges[-1]] = 15
    if ((bins < 0) | (bins > 15)).any():
        raise ValueError('Some players fall outside the original bin edges.')
    colleges, ids = pd.factorize(band.team_id if account_grouping else band.athlete_id, sort=True)
    G = len(ids)
    if G < 3:
        raise ValueError('Too few colleges to estimate uncertainty.')
    y = band.Y_draft.to_numpy(float)
    psi = np.zeros((G,14))
    rows = []
    for k in range(14):
        left = bins == k
        right = (bins == k+1) | (bins == k+2)
        n1,n2 = int(left.sum()),int(right.sum())
        if n1 == 0 or n2 == 0:
            raise ValueError(f'Comparison {k+1} has an empty side. Cannot evaluate all 14; no comparisons were silently omitted.')
        p1,p2 = float(y[left].mean()),float(y[right].mean())
        individual = np.zeros(len(band))
        individual[left] = (y[left]-p1)/n1
        individual[right] = -(y[right]-p2)/n2
        psi[:,k] = np.bincount(colleges,weights=individual,minlength=G)
        c1,c2 = len(np.unique(colleges[left])),len(np.unique(colleges[right]))
        event1 = len(np.unique(colleges[left & (y==1)]))
        event2 = len(np.unique(colleges[right & (y==1)]))
        flags=[]
        if min(c1,c2)<30:
            flags.append('Fewer than 30 colleges on at least one side; approximate inference may be imprecise')
        if min(event1,event2)<10:
            flags.append('Drafted players represented in fewer than 10 colleges on at least one side')
        rows.append(dict(start_bin=k+1,comparison=f'Bin {k+1} vs bins {k+2}+{k+3}',
            first_players=n1,first_drafted=int(y[left].sum()),first_colleges=c1,
            following_players=n2,following_drafted=int(y[right].sum()),following_colleges=c2,
            first_event_colleges=event1,following_event_colleges=event2,
            first_rate_percent=100*p1,following_rate_percent=100*p2,
            decline_pp=100*(p1-p2),warning='; '.join(flags)))
    se = np.sqrt(G/(G-1)*np.sum(psi**2,axis=0))
    if (se <= 0).any() or not np.isfinite(se).all():
        raise ValueError('At least one comparison has zero or invalid estimated uncertainty. Cannot claim a 14-comparison adjustment.')
    table = pd.DataFrame(rows)
    observed = table.decline_pp.to_numpy()/100/se
    rng = np.random.default_rng(seed)
    maxima = np.empty(repetitions)
    unadjusted_exceed = np.zeros(14,dtype=int)
    scaled = np.sqrt(G/(G-1))*psi/se
    print(f'Peak-to-tail test: evaluating all 14 locations with {repetitions:,} bootstrap repetitions.',flush=True)
    for start in range(0,repetitions,500):
        stop = min(start+500,repetitions)
        weights = rng.choice([-1.,1.],size=(stop-start,G))
        z = weights @ scaled
        maxima[start:stop] = z.max(axis=1)
        unadjusted_exceed += (z >= observed).sum(axis=0)
    adjusted = (1+(maxima[:,None] >= observed).sum(axis=0))/(repetitions+1)
    critical = float(np.quantile(maxima,.95,method='higher'))
    table['standard_error_pp'] = 100*se
    table['standardized_decline'] = observed
    table['unadjusted_one_sided_p'] = (1+unadjusted_exceed)/(repetitions+1)
    table['adjusted_one_sided_p_all14'] = adjusted
    table['simultaneous95_lower_bound_pp'] = table.decline_pp-100*critical*se
    table['adjusted_p_monte_carlo_se_approx'] = np.sqrt(adjusted*(1-adjusted)/repetitions)
    target = table.loc[table.start_bin==14].copy()
    bins_table = count_bins(band,edges,'Original performance band')
    highest = int(bins_table.loc[bins_table.rate.idxmax(),'bin'])
    meta = dict(method='Single-step one-sided max-t college-cluster Rademacher multiplier bootstrap',
        repetitions=int(repetitions),seed=int(seed),family_size=14,target_start_bin=14,
        contrast='First bin rate minus pooled rate in the next two bins; positive means decline',
        family='Every start bin 1 through 14, each versus its next two bins pooled by players',
        original_bin_edges=edges.tolist(),highest_observed_bin=highest,
        target_is_an_observed_maximum=bool(np.isclose(bins_table.rate.iloc[13],bins_table.rate.max())),
        colleges_in_band=G,critical_value_95=critical,
        global_family_p=float((1+np.sum(maxima>=observed.max()))/(repetitions+1)),
        maximum_standardized_decline_start_bin=int(table.loc[table.standardized_decline.idxmax(),'start_bin']),
        variance_correction='G/(G-1), where G counts colleges in the performance band; no further N/(N-p) correction',
        bootstrap='Centered linearized rate differences, common college signs across all comparisons, fixed original standard errors',
        interval='95% simultaneous ONE-SIDED lower bounds; not two-sided confidence intervals; rounding/Monte Carlo may affect boundary decisions',
        scope='Adjusts location search within this fixed 14-comparison family only. Historical band/year/bin-count/tail-width searches are not covered.',
        assumptions='Approximate independence across colleges and adequate effective college/event counts. No own-performance or season adjustment.',
        warnings='Sparse events and few contributing colleges can impair the approximation. Diagnostic thresholds 30 and 10 are cautions, not validity guarantees.')
    meta['account_grouping'] = bool(account_grouping)
    meta['colleges_in_band'] = int(band.team_id.nunique())
    meta['uncertainty_units'] = G
    if not account_grouping:
        meta['method'] = 'One-sided max-t independent-player Rademacher multiplier bootstrap'
        meta['assumptions'] = 'Each final-season player is independent; no allowance for shared college circumstances.'
        meta['variance_correction'] = 'N/(N-1) for N independent players'
    print('Finished. The detailed table retains all 14 comparisons, not just the most favorable one.',flush=True)
    return target,table,meta


def explain_peak_tail(target, metadata):
    """Plain-English report, deliberately avoiding a binary proof/no-proof verdict."""
    r=target.iloc[0]
    print('\nOUR CHOSEN COMPARISON: bin 14 versus bins 15 and 16 combined')
    if not metadata['target_is_an_observed_maximum']:
        print(f'NOTE: With the current settings, bin 14 is NOT the highest bin. The highest is bin {metadata["highest_observed_bin"]}. The target has not been silently moved.')
    print(f'Bin 14: {r.first_drafted:.0f}/{r.first_players:.0f} drafted ({r.first_rate_percent:.1f}%).')
    print(f'Last two bins: {r.following_drafted:.0f}/{r.following_players:.0f} drafted ({r.following_rate_percent:.1f}%).')
    print(f'Observed decline: {r.decline_pp:+.2f} percentage points. Positive means the last two bins have a lower rate.')
    print(f'P-value allowing for all 14 possible comparison locations: {r.adjusted_one_sided_p_all14:.4f}.')
    print(f'Approximate Monte Carlo standard error of that p-value: {r.adjusted_p_monte_carlo_se_approx:.4f}.')
    print(f'95% simultaneous one-sided lower bound on the decline: {r.simultaneous95_lower_bound_pp:+.2f} percentage points.')
    if r.adjusted_one_sided_p_all14 < .05:
        print('INTERPRETATION: Evidence of a decline at this location remains at the conventional 5% level after the 14-location adjustment, subject to the assumptions and sparse-data cautions below.')
    else:
        print('INTERPRETATION: This test does not establish a decline at this location at the conventional 5% level after accounting for the 14-location search. It does not establish that the decline is zero.')
    print('The lower bound allows for inspecting all 14 locations. A positive bound supports a decline; a bound at or below zero does not establish one.')
    print(f'Colleges represented: {r.first_colleges:.0f} in bin 14; {r.following_colleges:.0f} in the last two bins (some may appear on both sides).')
    if r.warning:
        print('CAUTION:',r.warning)
    print('This remains exploratory. Earlier choices of years, performance bands, bin counts, and tail width are not included in this adjustment. It is not proof of congestion or causation.')


def peak_tail_plot(band, edges):
    """Display the actual tested bins, not the earlier percentile regions."""
    from create_section_4_5_4_figure import count_bins
    t=count_bins(band,edges,'Current own-performance band')
    fig,ax=plt.subplots(figsize=(12,6))
    ax.axvspan(edges[13],edges[14],alpha=.2,color='#427ca5',label='Bin 14: chosen peak location')
    ax.axvspan(edges[14],edges[16],alpha=.16,color='#ae394e',label='Bins 15 + 16: pooled comparison')
    ax.plot(t.center,t.rate*100,'o-',color='#30373e')
    for _,r in t.iterrows():
        if r.n:
            ax.annotate(f'{int(r.drafted)}/{int(r.n)}',(r.center,r.rate*100),xytext=(0,8),textcoords='offset points',ha='center',fontsize=9)
    ax.hlines(100*t.rate.iloc[13],edges[13],edges[14],color='#427ca5',ls='--')
    last=t.iloc[14:16]
    ax.hlines(100*last.drafted.sum()/last.n.sum(),edges[14],edges[16],color='#ae394e',ls='--')
    ax.set_ylim(0,max(35,t.rate.max()*100+10))
    ax.set_xlabel('Mean teammate performance (z score; focal player excluded)')
    ax.set_ylabel('Players ever drafted (%)')
    ax.set_title('Chosen peak-to-tail comparison on the original 16-bin curve')
    ax.legend(loc='upper left');ax.grid(axis='y',alpha=.15)
    fig.text(.5,.02,'Point labels: drafted / players. Dashed segments show the two tested rates.\nThe test adjusts for all 14 possible starting bins, not only the highlighted comparison.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.09,1,1])
    return fig


def four_way_results(grouped, independent, *, repeated_rows=False):
    """Hold the effect fixed; show exactly which uncertainty/search assumptions change."""
    rows=[]
    for label,t in [('OFF: each player-season independent' if repeated_rows else 'OFF: each player independent',independent),
                    ('ON: colleges + repeated players' if repeated_rows else 'ON: colleges',grouped)]:
        r=t.iloc[0]
        for adjust,column in [('OFF','unadjusted_one_sided_p'),('ON: 14 locations','adjusted_one_sided_p_all14')]:
            rows.append({'Grouping allowance':label,'Peak-location adjustment':adjust,
                'Observed decline (percentage points)':r.decline_pp,
                'Standard error (percentage points)':r.standard_error_pp,
                'One-sided p-value':r[column]})
    return pd.DataFrame(rows)


def distinct_bin_counts(frame, regions):
    """Count combined regions directly, never sum distinct counts across bins.

    Season is observation season, not necessarily actual draft year. Positive
    outcome means ever drafted. This does not infer contemporaneous teammates
    across different years or infer independent units from college-season counts.
    """
    records=[]
    for label,bins in regions.items():
        z=frame.loc[frame.curve_bin.isin(bins)];yes=z.loc[z.Y_draft==1]
        records.append({'Region':label,'All player-season rows':len(z),
            'All distinct players':z.athlete_id.nunique(),
            'All distinct colleges':z.team_id.nunique(),
            'All distinct college-seasons':len(z[['team_id','season']].drop_duplicates()),
            'Ever-drafted rows':len(yes),'Distinct drafted players':yes.athlete_id.nunique(),
            'Colleges with drafted players':yes.team_id.nunique(),
            'College-seasons with drafted players':len(yes[['team_id','season']].drop_duplicates()),
            'Distinct drafted player-seasons':len(yes[['athlete_id','season']].drop_duplicates())})
    return pd.DataFrame(records)


def show_requested_comparison(grouped,independent,counts,*,repeated_rows=False):
    from IPython.display import display
    four=four_way_results(grouped,independent,repeated_rows=repeated_rows)
    print('\nTHE SAME DECLINE, FOUR STATISTICAL VERSIONS')
    display(four.round(4))
    print('OFF / OFF is the result without either adjustment. ON / ON includes both. All four use the same observed rates.')
    if repeated_rows:
        print('Grouping OFF treats repeated seasons of the same player as independent rows; it does not turn them into distinct people.')
    print('Unadjusted p-values do not account for selecting the peak after looking at the graph. These remain exploratory comparisons.')
    print('\nDRAFTED PLAYERS: DISTINCT PEOPLE, COLLEGES, AND COLLEGE-SEASONS')
    display(counts[['Region','Ever-drafted rows','Distinct drafted players',
                    'Colleges with drafted players','College-seasons with drafted players']])
    print('A college in two seasons counts twice in college-seasons. Three drafted teammates at that college in one season count as three players but ONE college-season.')
    print('Combined-region counts are deduplicated across all included bins. Season means the observation season, not necessarily the draft year.')
    print('\nDENOMINATORS: EVERYONE IN EACH REGION, DRAFTED OR NOT')
    display(counts[['Region','All player-season rows','All distinct players','All distinct colleges','All distinct college-seasons']])
    return four
