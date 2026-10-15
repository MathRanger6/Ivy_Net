"""Original mosaic panel 7: selected bin 8 versus fixed tail bins 15-16.

Read-only cohort reconstruction; inferential runs require explicit notebook call.
"""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pd46_comparisons import HERE
sys.path.insert(0,str(HERE.parent))
from create_section_4_5_4_figure import REPO
SOURCE=REPO/'3-Master_Plan/re_entry/HEROs_and_PASSes/basic_data_plots/CCT_draft_rate_ai_band_poolq_loo_min20_ppm_z2_3_dft.json'


def load_panel7():
    for folder in [REPO/'sports',REPO/'sports/scripts']:
        sys.path.insert(0,str(folder))
    from pass_a_congestion_conditional import CctSpec,_prepare_panel
    from sports_pipeline.panel_build import assign_poolq_bin_labels
    spec=CctSpec(season_min=2011,season_max=2021,min_minutes=20,min_team_season_games=10,
                 winsor_lo=.01,winsor_hi=.99,n_bins=16,ai_lo=2.,ai_hi=3.,dft=True)
    print('Rebuilding ORIGINAL panel 7 from local files; no network requests.',flush=True)
    full=_prepare_panel(spec)
    b=spec.apply_ai_band(full).copy()
    b['curve_bin']=assign_poolq_bin_labels(b.poolq_loo,16,'quantile').astype(int)+1
    ref=json.loads(SOURCE.read_text())
    counts=b.groupby('curve_bin').agg(rows=('Y_draft','size'),positive=('Y_draft','sum'))
    if (len(full)!=ref['panel_n'] or len(b)!=ref['band_n']
        or counts.rows.tolist()!=[r['n'] for r in ref['bins']]
        or counts.positive.tolist()!=[r['drafts'] for r in ref['bins']]):
        raise ValueError('Rebuilt panel 7 does not match the original source. Stop for source review.')
    if b[['athlete_id','team_id','season','Y_draft']].isna().any().any() or b.duplicated(['athlete_id','season']).any():
        raise ValueError('Missing identity fields or duplicate player-season rows require review.')
    if not b.Y_draft.isin([0,1]).all() or (b.groupby('athlete_id').Y_draft.nunique()>1).any():
        raise ValueError('Expected consistent binary ever-drafted labels within each player.')
    b,groups=dependency_groups(b)
    cols=['athlete_id','season','team_id','perf','poolq_loo','Y_draft','curve_bin']
    meta=dict(panel='Original mosaic panel 7',years=[2011,2021],own_performance_band=[2,3],
        min_minutes=20,min_team_season_games=10,source_file=str(SOURCE),
        source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        cohort_sha256=hashlib.sha256(pd.util.hash_pandas_object(b[cols],index=False).values.tobytes()).hexdigest(),
        rows=len(b),distinct_players=b.athlete_id.nunique(),positive_rows=int(b.Y_draft.sum()),
        distinct_drafted_players=b.loc[b.Y_draft==1,'athlete_id'].nunique(),
        colleges=b.team_id.nunique(),dependence_groups=b.dependence_group.nunique(),
        players_at_multiple_colleges=int((b.groupby('athlete_id').team_id.nunique()>1).sum()),
        population='All eligible player-seasons, restricted to colleges represented by an ever-drafted player in source window.',
        bins='Original within-band rank-based quantile bins; ties follow historical row-order convention.',
        outcome='Ever-drafted label repeated for each included player-season; rates weight player-seasons, not distinct players.',
        dependence='Colleges linked by a shared player IN THIS ANALYSIS BAND are merged into a connected component. All rows from a college stay together across years. Different components are assumed approximately independent.',
        verified_original_bin_counts=True)
    print(f'Verified all 16 bins: {len(b)} rows, {meta["distinct_players"]} players, {meta["positive_rows"]} positive rows, {meta["distinct_drafted_players"]} distinct drafted players.',flush=True)
    print(f'{meta["colleges"]} colleges become {meta["dependence_groups"]} dependence groups after linking {meta["players_at_multiple_colleges"]} multi-college players.',flush=True)
    return b,groups,meta


def dependency_groups(b):
    """Connected college groups contain every repeated athlete and college cluster."""
    b=b.copy();parent={t:t for t in b.team_id.unique()}
    def root(t):
        while parent[t]!=t:
            parent[t]=parent[parent[t]];t=parent[t]
        return t
    for _,g in b.groupby('athlete_id'):
        teams=list(g.team_id.unique())
        for t in teams[1:]:parent[root(t)]=root(teams[0])
    representatives=sorted({root(t) for t in parent},key=str)
    labels={t:i+1 for i,t in enumerate(representatives)}
    b['dependence_group']=b.team_id.map(lambda t:labels[root(t)])
    records=[]
    for group,z in b.groupby('dependence_group'):
        records.append(dict(group=int(group),colleges=z.team_id.nunique(),
            college_names='; '.join(sorted(z.team_short_display_name.dropna().astype(str).unique())),
            player_seasons=len(z),distinct_players=z.athlete_id.nunique()))
    return b,pd.DataFrame(records)


def preview(b):
    t=b.groupby('curve_bin').agg(n=('Y_draft','size'),drafts=('Y_draft','sum'),
        x=('poolq_loo','mean'),distinct_players=('athlete_id','nunique'),colleges=('team_id','nunique')).reset_index()
    t['rate']=t.drafts/t.n
    x=t.x.to_numpy()
    fig,ax=plt.subplots(figsize=(12,6.5))
    ax.axvspan((x[6]+x[7])/2,(x[7]+x[8])/2,color='#427ca5',alpha=.2,label='Chosen peak: bin 8')
    ax.axvspan((x[13]+x[14])/2,x[-1]+.055,color='#ae394e',alpha=.15,label='Fixed tail: bins 15-16')
    ax.plot(t.x,t.rate*100,'o-',color='#30373e')
    for _,r in t.iterrows():
        ax.annotate(f'{int(r.drafts)}/{int(r.n)}',(r.x,100*r.rate),xytext=(0,8),textcoords='offset points',ha='center',fontsize=9)
        ax.text(r.x,-.09,str(int(r.curve_bin)),transform=ax.get_xaxis_transform(),ha='center',fontsize=9)
    tail=b.loc[b.curve_bin.isin([15,16])]
    ax.hlines(tail.Y_draft.mean()*100,(x[13]+x[14])/2,x[-1]+.055,color='#ae394e',ls='--')
    ax.set_ylim(0,75);ax.set_xlim(x[0]-.04,x[-1]+.055)
    ax.set_ylabel('Player-season rows with an ever-drafted outcome (%)')
    ax.set_xlabel('Mean other-teammate performance (z score)',labelpad=33)
    ax.set_title('Panel 7: bin 8 versus the fixed final two bins\n2011-2021; own performance z score from 2 to 3')
    ax.legend(loc='upper left');ax.grid(axis='y',alpha=.2)
    fig.text(.5,.025,'Original 16 quantile bins; eligible colleges represented by an ever-drafted player.\nLabels: positive rows / player-season rows. Repeated seasons are retained. Bin numbers appear below the axis.\nShading identifies the target comparison; the adjustment considers each of bins 1-14 against the same fixed tail.',ha='center',fontsize=9)
    fig.subplots_adjust(bottom=.26,top=.85,left=.09,right=.98)
    return fig,t


def test_fixed_tail(b,*,repetitions=9999,seed=46,account_grouping=True,n_bins=16,target_bin=8):
    """Same centered max-t principle as 4A, but fixed tail and connected clusters."""
    if not isinstance(repetitions,(int,np.integer)) or repetitions<999:
        raise ValueError('Use at least 999 repetitions.')
    family_size=n_bins-2
    tail_bins=[n_bins-1,n_bins]
    if not 1 <= target_bin <= family_size:
        raise ValueError('Target must precede the fixed final two bins.')
    if set(b.curve_bin.unique())!=set(range(1,n_bins+1)):
        raise ValueError('All original bins must be represented.')
    for key in ['athlete_id','team_id']:
        if (b.groupby(key).dependence_group.nunique()>1).any():
            raise ValueError('Dependence grouping splits a player or college.')
    codes,labels=pd.factorize(b.dependence_group if account_grouping else np.arange(len(b)),sort=True);G=len(labels)
    if G<3:raise ValueError('Too few independent groups.')
    y=b.Y_draft.to_numpy(float);binid=b.curve_bin.to_numpy()
    right=np.isin(binid,tail_bins);nr=int(right.sum());pr=y[right].mean()
    psi=np.zeros((G,family_size));records=[]
    for j in range(family_size):
        left=binid==j+1;n=int(left.sum());pl=y[left].mean()
        v=np.zeros(len(b));v[left]=(y[left]-pl)/n;v[right]=-(y[right]-pr)/nr
        psi[:,j]=np.bincount(codes,weights=v,minlength=G)
        a,bside=b.loc[left],b.loc[right]
        ca,cb=a.dependence_group.nunique(),bside.dependence_group.nunique()
        ea=a.loc[a.Y_draft==1,'dependence_group'].nunique()
        eb=bside.loc[bside.Y_draft==1,'dependence_group'].nunique()
        flags=[]
        if min(ca,cb)<30:flags.append('Fewer than 30 dependence groups on at least one side')
        if min(ea,eb)<10:flags.append('Positive outcomes in fewer than 10 dependence groups on at least one side')
        records.append(dict(start_bin=j+1,comparison=f'Bin {j+1} vs bins {tail_bins[0]}+{tail_bins[1]}',
            first_rows=n,first_positive_rows=int(y[left].sum()),first_distinct_players=a.athlete_id.nunique(),
            first_distinct_drafted_players=a.loc[a.Y_draft==1,'athlete_id'].nunique(),
            tail_rows=nr,tail_positive_rows=int(y[right].sum()),tail_distinct_players=bside.athlete_id.nunique(),
            tail_distinct_drafted_players=bside.loc[bside.Y_draft==1,'athlete_id'].nunique(),
            first_dependence_groups=ca,tail_dependence_groups=cb,
            shared_players=len(set(a.athlete_id)&set(bside.athlete_id)),
            first_rate_percent=100*pl,tail_rate_percent=100*pr,decline_pp=100*(pl-pr),warning='; '.join(flags)))
    t=pd.DataFrame(records);se=np.sqrt(G/(G-1)*np.sum(psi**2,axis=0))
    if not np.isfinite(se).all() or (se<=0).any():raise ValueError('Invalid uncertainty for one or more contrasts; no comparisons omitted.')
    obs=t.decline_pp.to_numpy()/100/se;scaled=np.sqrt(G/(G-1))*psi/se
    rng=np.random.default_rng(seed);maxima=np.empty(repetitions);single=np.zeros(family_size,dtype=int)
    print(f'{repetitions:,} centered bootstrap draws across all {family_size} fixed-tail comparisons.',flush=True)
    for start in range(0,repetitions,500):
        stop=min(start+500,repetitions)
        noise=rng.choice([-1.,1.],size=(stop-start,G))@scaled
        maxima[start:stop]=noise.max(axis=1);single+=(noise>=obs).sum(axis=0)
    t['standard_error_pp']=100*se
    t['unadjusted_one_sided_p']=(single+1)/(repetitions+1)
    t[f'adjusted_one_sided_p_all{family_size}']=(1+(maxima[:,None]>=obs).sum(axis=0))/(repetitions+1)
    critical=float(np.quantile(maxima,.95,method='higher'))
    t['simultaneous95_lower_bound_pp']=t.decline_pp-critical*100*se
    t['monte_carlo_se_approx']=np.sqrt(t[f'adjusted_one_sided_p_all{family_size}']*(1-t[f'adjusted_one_sided_p_all{family_size}'])/repetitions)
    method=dict(target=f'Bin {target_bin} versus bins {tail_bins[0]}+{tail_bins[1]} pooled',family=f'Each bin 1-{family_size} versus the SAME fixed final two bins pooled',family_size=family_size,
        repetitions=int(repetitions),seed=int(seed),dependence_groups=G,critical_value_95=critical,
        method='One-sided single-step max-t Rademacher cluster multiplier bootstrap of centered rate-difference influence functions',
        correction='G/(G-1); original standard errors retained in bootstrap; empirical higher 95th percentile for lower bounds',
        assumptions='Approximate independence between connected college groups; adequate effective group/event counts; conditions on original bins and outcome-filtered cohort.',
        limitations='Exploratory; no adjustment for historical window, band, bin-count, tail-width, panel choice or outcome-based college inclusion. No causal or whole-shape claim.',
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    method['account_grouping']=bool(account_grouping)
    method['dependence_groups']=int(b.dependence_group.nunique())
    method['uncertainty_units']=G
    if not account_grouping:
        method['method']='One-sided max-t independent-ROW Rademacher multiplier bootstrap'
        method['assumptions']='Every player-season row is independent, including repeated rows for the same player. Diagnostic only; no college or repeated-player dependence allowance.'
        method['correction']='N/(N-1) for N independent rows'
    return t.loc[t.start_bin==target_bin].copy(),t,method


def explain(chosen):
    r=chosen.iloc[0]
    print('\nPANEL 7: BIN 8 COMPARED WITH THE LAST TWO BINS')
    print(f'Peak: {r.first_positive_rows:.0f}/{r.first_rows:.0f} positive player-season rows ({r.first_rate_percent:.1f}%).')
    print(f'Tail: {r.tail_positive_rows:.0f}/{r.tail_rows:.0f} positive player-season rows ({r.tail_rate_percent:.1f}%).')
    print(f'These represent {r.first_distinct_players:.0f} distinct players at the peak and {r.tail_distinct_players:.0f} in the tail; {r.shared_players:.0f} appear on both sides.')
    print(f'Observed decline: {r.decline_pp:.2f} percentage points. Positive means lower rates in the tail.')
    print(f'Unadjusted for peak search, but allowing repeated players and college grouping: p = {r.unadjusted_one_sided_p:.4f}.')
    print(f'Adjusted for all 14 possible peak locations: p = {r.adjusted_one_sided_p_all14:.4f}.')
    print(f'95% simultaneous ONE-SIDED lower bound: {r.simultaneous95_lower_bound_pp:+.2f} percentage points.')
    if r.adjusted_one_sided_p_all14<.05:
        print('The decline meets the conventional 5% threshold after this peak-location adjustment, under the stated assumptions. This remains exploratory evidence.')
    else:
        print('The decline does not meet the conventional 5% threshold after this peak-location adjustment. This does not establish that the decline is absent.')
    print('CAUTION:',r.warning or 'Statistical approximations still apply.')
    print('The outcome is repeated ever-drafted status, not annual selection. This does not establish causation or the complete inverted-U shape.')
