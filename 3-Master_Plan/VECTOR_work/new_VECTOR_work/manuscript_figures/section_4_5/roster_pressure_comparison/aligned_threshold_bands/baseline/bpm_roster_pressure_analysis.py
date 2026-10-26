"""BPM companion to the frozen PPM shared/LOO analysis.

Observed outcomes only. No fitting, simulated selection, or significance tests.
The new bands retain Entry 5's raw-BPM membership; environmental calculations
use BPM standardized within season on the eligible, available full rosters.
"""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.special import expit
from roster_pressure_analysis import KEYS, GROUPS, AXES, add_roster_pressure, bin_table, fixed_edges

HERE = Path(__file__).resolve().parent
DEFAULTS = dict(theta_quantile=.97, gamma=6., n_bins=16, thin_n=30,
                band_mode='top_next', band_fraction=.03, show_squid_jackal=True)
AXLABEL = {'loo_performance': 'LOO mean BPM z-score\nFocal player excluded',
           'rp_shared': 'Shared roster pressure\nFocal player included',
           'rp_loo': 'LOO roster pressure\nFocal player excluded'}
COLORS = ['#356d95', '#735394', '#b45d32']

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load_frozen_sources():
    cache = HERE / 'cache'
    manifest = json.loads((cache / 'source_manifest.json').read_text())
    sources = {}
    for name in ['all', 'dft', 'last']:
        p = cache / f'{name}.pkl'
        if sha(p) != manifest['cache_sha256'][name]:
            raise ValueError(f'{name} snapshot changed. Audit source changes before continuing.')
        sources[name] = pd.read_pickle(p)
        assert not sources[name].duplicated(KEYS).any()
    assert len(sources['last']) == sources['last'].athlete_id.nunique() == 22795
    assert int(sources['last'].Y_draft.sum()) == 615
    return sources, manifest

def prepare_roster(source, settings):
    full_n = source.groupby(GROUPS, sort=False).size().rename('eligible_roster_n')
    roster = source.loc[np.isfinite(source.BPM)].copy()
    g = roster.groupby('season').BPM
    roster['perf'] = (roster.BPM - g.transform('mean')) / g.transform('std')
    assert np.isfinite(roster.perf).all()
    assert np.allclose(roster.groupby('season').perf.mean(), 0, atol=1e-12)
    assert np.allclose(roster.groupby('season').perf.std(), 1)
    theta = float(roster.perf.quantile(settings['theta_quantile']))
    roster = add_roster_pressure(roster, theta, settings['gamma'])
    roster = roster.join(full_n, on=GROUPS)
    roster['missing_teammates'] = roster.eligible_roster_n - roster.roster_n
    roster['team_season_key'] = roster.team_id.astype(str) + ':' + roster.season.astype(str)
    roster['theta'] = theta
    return roster, theta

def build_cohorts(sources, settings):
    all_roster, theta = prepare_roster(sources['all'], settings)
    # A left-to-right merge preserves the frozen final-season order for rank ties.
    last = sources['last'][KEYS].merge(all_roster, on=KEYS, how='inner', sort=False, validate='one_to_one')
    assert len(last) == last.athlete_id.nunique() == 19289
    assert int(last.Y_draft.sum()) == 510
    available_last = sources['last'].loc[np.isfinite(sources['last'].BPM)]
    assert np.array_equal(last.athlete_id, available_last.athlete_id)
    assert np.allclose(last.BPM, available_last.BPM)
    last['band_rank'] = last.BPM.rank(ascending=False, method='first').astype(int)
    q = settings['band_fraction']
    k1, k2 = int(np.ceil(q * len(last))), int(np.ceil(2*q*len(last)))
    if settings['band_mode'] == 'top_next':
        cohorts = {'all': last, 'top': last.loc[last.band_rank <= k1].copy(),
                   'next': last.loc[last.band_rank.between(k1+1, k2)].copy()}
        labels = {'all': 'All performance levels', 'top': f'Top {100*q:g}% of raw BPM',
                  'next': f'Next {100*q:g}% of raw BPM'}
        if q == .03:
            expected = pd.read_csv(HERE.parents[1] / 'ncaa_evidence_walkthrough/bpm_available_ranked_population.csv')
            a = last.sort_values('band_rank')
            assert np.array_equal(a.athlete_id.to_numpy(), expected.athlete_id.to_numpy())
            assert (len(cohorts['top']), int(cohorts['top'].Y_draft.sum())) == (579, 249)
            assert (len(cohorts['next']), int(cohorts['next'].Y_draft.sum())) == (579, 112)
        thresholds = {name: theta for name in cohorts}
        units = {name: 'unique players; saved final season' for name in cohorts}
    elif settings['band_mode'] == 'historical':
        dft, dft_theta = prepare_roster(sources['dft'], settings)
        cut = float(dft.perf.quantile(.93))
        cohorts = {'all': last, 'z2_3': dft.loc[dft.perf.between(2,3)].copy(),
                   'top7': dft.loc[dft.perf >= cut].copy()}
        labels = {'all': 'All performance levels', 'z2_3': 'Own BPM z = 2 to 3',
                  'top7': 'Own BPM at or above 93rd percentile'}
        thresholds = {'all':theta, 'z2_3':dft_theta, 'top7':dft_theta}
        units = {'all': 'unique players; saved final season',
                 'z2_3':'player-seasons; draftee colleges', 'top7':'player-seasons; draftee colleges'}
    else:
        raise ValueError('band_mode must be top_next or historical')
    excluded = {}
    for name, c in cohorts.items():
        good = c[AXES].notna().all(axis=1)
        excluded[name] = int((~good).sum())
        cohorts[name] = c.loc[good].copy()
    coverage = sources['last'].assign(bpm_available=np.isfinite(sources['last'].BPM)).groupby('season').agg(
        players=('athlete_id','size'), bpm_available=('bpm_available','sum'), ever_drafted=('Y_draft','sum'))
    meta = dict(labels=labels, units=units, thresholds=thresholds, excluded_undefined_loo=excluded,
                roster_rows=len(all_roster), final_players=len(last), final_drafted=int(last.Y_draft.sum()),
                final_players_with_missing_teammates=int(last.missing_teammates.gt(0).sum()),
                final_missing_teammates_max=int(last.missing_teammates.max()),
                nominal_top_ranks=[1,k1], nominal_next_ranks=[k1+1,k2])
    return cohorts, meta, coverage

def build_tables(cohorts, settings):
    n = settings['n_bins']
    rp = np.concatenate([c[['rp_shared','rp_loo']].to_numpy().ravel() for c in cohorts.values()])
    peer = np.concatenate([c.loo_performance.to_numpy() for c in cohorts.values()])
    edges = {'rp_shared':fixed_edges(rp,n), 'rp_loo':fixed_edges(rp,n), 'loo_performance':fixed_edges(peer,n)}
    tables, region_frames, membership = {}, [], []
    for method in ['quantile','EW']:
        for name,c in cohorts.items():
            for axis in AXES:
                t,r,u = bin_table(c,axis,method,n,edges[axis] if method=='EW' else None)
                t = t.assign(cohort=name,axis=axis,method=method)
                tables[method,name,axis] = t
                if len(r): region_frames.append(r.assign(cohort=name,axis=axis,method=method))
                membership.append(u[KEYS+['Y_draft','bin','quantile_bin']].assign(cohort=name,axis=axis,method=method))
    return tables, (pd.concat(region_frames,ignore_index=True) if region_frames else pd.DataFrame()), pd.concat(membership,ignore_index=True), edges

def draw_panel(ax, count_ax, t, regions, color, settings, method, ylim):
    n = settings['n_bins'];x = np.arange(1,n+1)
    bars=ax.bar(x,100*t.rate,color=color,width=.85)
    for patch,row in zip(bars,t.itertuples()):
        if row.n < settings['thin_n']: patch.set_hatch('///');patch.set_alpha(.55)
    if settings['show_squid_jackal'] and n == 16:
        if method=='quantile':
            for lo,hi,col in [(5.5,8.5,'#20854b'),(13.5,16.5,'#bf660d')]:
                ax.axvspan(lo,hi,color=col,alpha=.10,zorder=0)
        words=[]
        for row in regions.itertuples():
            words.append(f'{row.group}: {row.positive_rows}/{row.n} = {100*row.rate:.1f}%')
        ax.text(.02,.97,'\n'.join(words),transform=ax.transAxes,va='top',fontsize=8,
                bbox=dict(facecolor='white',alpha=.9,edgecolor='none'))
    ax.set_ylim(0,ylim);ax.set_xlim(.35,n+.65);ax.set_xticks(x);ax.tick_params(axis='x',labelsize=8)
    ax.set_ylabel('Ever-drafted observations (%)',fontsize=10)
    ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True);ax.spines[['top','right']].set_visible(False)
    count_ax.axis('off')
    vals=[[str(int(v)) for v in t[col]] for col in ['n','positive_rows','team_seasons']]
    table=count_ax.table(cellText=vals,rowLabels=['N','D','G'],colLabels=[str(i) for i in x],
                         loc='center',cellLoc='center',bbox=[0,0,1,1])
    table.auto_set_font_size(False);table.set_fontsize(7)
    for cell in table.get_celld().values():cell.set_linewidth(.25);cell.set_edgecolor('#cccccc')

def draw(out, cohorts, meta, tables, regions, settings, method, names, axes, filename):
    nr,nc=len(names),len(axes)
    fig=plt.figure(figsize=(6.4*nc,5.1*nr+2.0))
    grid=fig.add_gridspec(nr*2,nc,height_ratios=[3.3,1.0]*nr,hspace=.95,wspace=.22,
                          left=.06,right=.98,top=(.72 if nr==1 else .81),bottom=.14)
    for ri,name in enumerate(names):
        c=cohorts[name]
        above_theta = int(c.perf.gt(meta['thresholds'][name]).sum())
        threshold_report = f'Own performance > θ: {above_theta:,}/{len(c):,} ({100*above_theta/len(c):.1f}%)'
        ylim=max(35.,min(100.,max(float(tables[method,name,a].rate.max()*100) for a in axes)+10))
        for ci,axis in enumerate(axes):
            ax=fig.add_subplot(grid[2*ri,ci]);ca=fig.add_subplot(grid[2*ri+1,ci])
            reg=regions.loc[(regions.method==method)&(regions.cohort==name)&(regions.axis==axis)] if len(regions) else regions
            draw_panel(ax,ca,tables[method,name,axis],reg,COLORS[list(cohorts).index(name)],settings,method,ylim)
            ax.set_title(f'{meta["labels"][name]}\n{AXLABEL[axis]}\nN={len(c):,}, D={int(c.Y_draft.sum()):,} | {meta["units"][name]}\n{threshold_report}',fontsize=10,fontweight='bold',pad=10)
            ax.set_xlabel(('Equal-count quantile' if method=='quantile' else 'Equal-width')+' bin, low to high',fontsize=9)
    fig.suptitle('BPM and observed draft outcomes: '+('HERO comparison' if nc==2 else 'environment mosaic'),fontsize=20,fontweight='bold',y=.98)
    fig.text(.06,(.91 if nr==1 else .93),f'Performance: BPM, standardized within season | 2011–2021 | {method} binning | No clipping or tail compression',fontsize=12)
    th='; '.join(f'{name}: {meta["thresholds"][name]:.3f}' for name in names)
    f=[f'γ = {settings["gamma"]:g}; θ = {100*settings["theta_quantile"]:g}th percentile of eligible roster BPM z-scores ({th}).',
       f'Available final-season population: K = {meta["final_drafted"]:,}, N = {meta["final_players"]:,}, K/N = {100*meta["final_drafted"]/meta["final_players"]:.2f}%. θ is chosen independently of K/N.',
       ('Bands: pooled raw BPM ranks from Entry 5. Roster pressure uses season-standardized BPM.' if settings['band_mode']=='top_next' else 'Historical band definitions on BPM; high bands use draftee-college player-seasons.'),
       f'N = observations; D = ever-drafted observations; G = distinct college-seasons. Hatching: N < {settings["thin_n"]}. Missing teammate BPM is omitted, never zero-filled.',
       ('Squid = quantile bins 6–8; Jackal = 14–16, independently per axis. EW annotations use those same quantile memberships.' if settings['show_squid_jackal'] and settings['n_bins']==16 else 'Squid/Jackal summaries disabled.'),
       'Inherited eligibility: at least 20 recorded season minutes and more than 10 team games. K is ever drafted, not an annual quota. No significance tests.']
    for j,line in enumerate(f):fig.text(.06,.107-j*.016,line,fontsize=8.8)
    fig.savefig(out/f'{filename}.png',dpi=180,facecolor='white')
    return fig

def run(settings=None):
    cfg={**DEFAULTS,**(settings or {})}
    if not 0 < cfg['theta_quantile'] < 1 or not 0 < cfg['band_fraction'] < .5:
        raise ValueError('Quantile/fraction settings outside allowed ranges')
    if not isinstance(cfg['n_bins'],int) or cfg['n_bins'] < 2:
        raise ValueError('n_bins must be an integer >= 2')
    sources,manifest=load_frozen_sources()
    cohorts,meta,coverage=build_cohorts(sources,cfg)
    tables,regions,membership,edges=build_tables(cohorts,cfg)
    out=HERE/'bpm_runs'/datetime.now().strftime('%Y%m%d_%H%M%S_%f');out.mkdir(parents=True)
    coverage.to_csv(out/'coverage_by_season.csv')
    summary=[]
    for name,c in cohorts.items():
        c.to_csv(out/f'{name}_players.csv.gz',index=False)
        people=c.groupby('athlete_id').Y_draft.max()
        above = c.perf.gt(meta['thresholds'][name])
        equal = c.perf.eq(meta['thresholds'][name])
        summary.append(dict(cohort=name,label=meta['labels'][name],observations=len(c),drafted_observations=int(c.Y_draft.sum()),
            rate=float(c.Y_draft.mean()),distinct_players=c.athlete_id.nunique(),distinct_drafted_players=int(people.sum()),
            colleges=c.team_id.nunique(),team_seasons=c.team_season_key.nunique(),
            under100_minutes=int(c.minutes.lt(100).sum()),with_missing_teammates=int(c.missing_teammates.gt(0).sum()),
            theta=meta['thresholds'][name],above_theta_observations=int(above.sum()),
            above_theta_fraction=float(above.mean()),equal_theta_observations=int(equal.sum()),
            below_theta_observations=int((~above & ~equal).sum()),
            distinct_players_above_theta=c.loc[above,'athlete_id'].nunique(),
            mean_rp_shared=float(c.rp_shared.mean()),mean_rp_loo=float(c.rp_loo.mean())))
    pd.DataFrame(summary).to_csv(out/'cohort_summary.csv',index=False)
    pd.concat(tables.values(),ignore_index=True).to_csv(out/'bin_counts.csv',index=False)
    regions.to_csv(out/'squid_jackal_counts.csv',index=False)
    membership.to_csv(out/'bin_membership.csv.gz',index=False)
    provenance=dict(settings=cfg,**meta,source_manifest=manifest,module_sha256=sha(__file__),
        helper_sha256=sha(HERE/'roster_pressure_analysis.py'),
        performance='BPM, standardized within season using sample SD (ddof=1), available eligible full rosters before focal selection',
        new_band_basis='Pooled raw BPM, descending rank-first ties, frozen final-season source order',
        above_theta_report='Focal observations actually plotted with own season-standardized BPM strictly greater than theta; equality excluded. Unique players in top_next mode; observations in historical high-band mode.',
        missingness='No BPM in 2009–2010; missing focal BPM excluded, missing teammate BPM omitted from means; singleton LOO excluded from BOTH sides',
        interpretation='Descriptive empirical outcome plots; no score, SELECT, causal effect, significance test, or fitted parameters',
        equal_width_edges={k:v.tolist() for k,v in edges.items()})
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    with PdfPages(out/'BPM_printable_comparisons.pdf') as pdf:
        for method in ['quantile','EW']:
            fig=draw(out,cohorts,meta,tables,regions,cfg,method,list(cohorts),AXES,f'BPM_mosaic_{method}')
            pdf.savefig(fig);plt.close(fig)
            for name in cohorts:
                fig=draw(out,cohorts,meta,tables,regions,cfg,method,[name],['rp_shared','rp_loo'],f'BPM_HERO_{name}_{method}')
                pdf.savefig(fig);plt.close(fig)
    (HERE/'latest_bpm_run.json').write_text(json.dumps({'run_directory':str(out),'settings':cfg},indent=2)+'\n')
    print(pd.DataFrame(summary).to_string(index=False))
    print('Saved BPM results:',out)
    return out

def load_latest(settings):
    state=json.loads((HERE/'latest_bpm_run.json').read_text());out=Path(state['run_directory'])
    p=json.loads((out/'provenance.json').read_text())
    if p['settings'] != {**DEFAULTS,**settings} or p['module_sha256'] != sha(__file__) or p['helper_sha256'] != sha(HERE/'roster_pressure_analysis.py'):
        raise ValueError('Settings or analysis changed. Set REBUILD_FIGURES=True and run again.')
    _,manifest=load_frozen_sources()
    if p['source_manifest'] != manifest:raise ValueError('Source manifest changed. Rebuild.')
    return out

if __name__=='__main__':
    run()
