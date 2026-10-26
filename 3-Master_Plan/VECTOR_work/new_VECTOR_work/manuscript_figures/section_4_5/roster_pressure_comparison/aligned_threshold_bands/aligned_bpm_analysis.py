"""Named BPM experiment: one performance scale/reference for theta and bands.

Preserves the baseline notebooks and run pointers. Empirical outcomes only.
"""
from pathlib import Path
from datetime import datetime
import sys,json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent)) if str(HERE.parent) not in sys.path else None
import bpm_roster_pressure_analysis as base
from roster_pressure_analysis import KEYS,AXES,add_roster_pressure

DEFAULTS=dict(theta_quantile=.98,gamma=6.,upper_band_end=.10,lower_band_end=.30,
              n_bins=16,thin_n=30,show_squid_jackal=True)

def settings_checked(settings):
    cfg={**DEFAULTS,**(settings or {})}
    tail=round(1-cfg['theta_quantile'],12)
    if not 0<tail<cfg['upper_band_end']<cfg['lower_band_end']<1:
        raise ValueError('Require 0 < top fraction (1 - theta_quantile) < upper_band_end < lower_band_end < 1.')
    if not isinstance(cfg['n_bins'],int) or cfg['n_bins']<2:
        raise ValueError('n_bins must be an integer >= 2.')
    return cfg

def make_cohorts(sources,cfg):
    # This reuses the baseline's season standardization and available rosters.
    roster,_=base.prepare_roster(sources['all'],cfg)
    wanted=sources['last'][KEYS]
    reference=wanted.merge(roster,on=KEYS,how='inner',sort=False,validate='one_to_one')
    assert len(reference)==reference.athlete_id.nunique()==19289
    assert int(reference.Y_draft.sum())==510
    theta=float(reference.perf.quantile(cfg['theta_quantile']))
    # Recalculate on complete available rosters, not only reference candidates.
    roster=add_roster_pressure(roster,theta,cfg['gamma'])
    roster['theta']=theta
    reference=wanted.merge(roster,on=KEYS,how='inner',sort=False,validate='one_to_one')
    reference['performance_rank']=reference.perf.rank(ascending=False,method='first').astype(int)
    fractions=[round(1-cfg['theta_quantile'],12),cfg['upper_band_end'],cfg['lower_band_end']]
    cutranks=[int(np.ceil(q*len(reference))) for q in fractions]
    a,b,c=cutranks
    reference['band']=np.select([reference.performance_rank<=a,reference.performance_rank<=b,
                                 reference.performance_rank<=c],['top','middle','lower'],default='outside')
    labels={'top':f'Top {100*fractions[0]:g}% of BPM z',
            'middle':f'Top {100*fractions[1]:g}% excluding top {100*fractions[0]:g}%',
            'lower':f'Top {100*fractions[2]:g}% excluding top {100*fractions[1]:g}%'}
    cohorts={name:reference.loc[reference.band==name].copy() for name in labels}
    excluded={}
    for name,frame in cohorts.items():
        good=frame[AXES].notna().all(axis=1)
        excluded[name]=int((~good).sum())
        cohorts[name]=frame.loc[good].copy()
    boundary=[]
    for fraction,rank in zip(fractions,cutranks):
        value=float(reference.loc[reference.performance_rank==rank,'perf'].iloc[0])
        tied=reference.loc[reference.perf==value]
        boundary.append(dict(top_fraction=fraction,rank=rank,performance=value,tied_observations=len(tied),
                             tied_at_or_above_rank=int(tied.performance_rank.le(rank).sum()),
                             tied_below_rank=int(tied.performance_rank.gt(rank).sum())))
    meta=dict(labels=labels,threshold=theta,thresholds={name:theta for name in cohorts},
              candidate_n=len(reference),candidate_k=int(reference.Y_draft.sum()),
              candidate_above_theta=int(reference.perf.gt(theta).sum()),
              candidate_equal_theta=int(reference.perf.eq(theta).sum()),
              roster_n=len(roster),roster_above_theta=int(roster.perf.gt(theta).sum()),
              excluded_undefined_loo=excluded,rank_boundaries=cutranks,top_fractions=fractions,
              boundary_ties=boundary,
              top_band_matches_strict_above_theta=set(reference.loc[reference.band=='top','athlete_id'])==set(reference.loc[reference.perf>theta,'athlete_id']))
    return cohorts,reference,roster,meta

def draw(out,cohorts,meta,tables,regions,cfg,method,names,axes,filename):
    nr,nc=len(names),len(axes)
    fig=plt.figure(figsize=(6.4*nc,5.1*nr+2.0))
    grid=fig.add_gridspec(nr*2,nc,height_ratios=[3.3,1]*nr,hspace=.95,wspace=.22,
                         left=.06,right=.98,top=(.72 if nr==1 else .81),bottom=.14)
    colors=dict(top='#735394',middle='#b45d32',lower='#356d95')
    for ri,name in enumerate(names):
        c=cohorts[name];above=int(c.perf.gt(meta['threshold']).sum())
        ylim=max(35.,min(100.,max(float(tables[method,name,a].rate.max()*100) for a in axes)+10))
        for ci,axis in enumerate(axes):
            ax=fig.add_subplot(grid[ri*2,ci]);ca=fig.add_subplot(grid[ri*2+1,ci])
            r=regions.loc[(regions.method==method)&(regions.cohort==name)&(regions.axis==axis)] if len(regions) else regions
            base.draw_panel(ax,ca,tables[method,name,axis],r,colors[name],cfg,method,ylim)
            ax.set_title(f'{meta["labels"][name]}\n{base.AXLABEL[axis]}\nN={len(c):,}, D={int(c.Y_draft.sum()):,} | unique final-season players\nOwn performance > θ: {above:,}/{len(c):,} ({100*above/len(c):.1f}%)',fontsize=10,fontweight='bold',pad=10)
            ax.set_xlabel(('Equal-count quantile' if method=='quantile' else 'Equal-width')+' bin, low to high',fontsize=9)
    fig.suptitle('BPM: aligned threshold and performance bands',fontsize=20,fontweight='bold',y=.98)
    fig.text(.06,(.91 if nr==1 else .93),f'Performance: BPM, standardized within season | 2011–2021 | {method} binning | No clipping or tail compression',fontsize=12)
    footer=[f'γ = {cfg["gamma"]:g}; θ = {meta["threshold"]:.4f}, the {100*cfg["theta_quantile"]:g}th percentile of FINAL-SEASON CANDIDATES, not roster observations.',
        f'One reference for θ and bands: N = {meta["candidate_n"]:,}, K = {meta["candidate_k"]:,}, K/N = {100*meta["candidate_k"]/meta["candidate_n"]:.2f}%. K is ever drafted, not an annual quota.',
        f'Actual candidates above θ: {meta["candidate_above_theta"]:,}; equal to θ: {meta["candidate_equal_theta"]:,}. Pressure is still computed on full available team-season rosters.',
        f'N = players; D = ever drafted; G = distinct college-seasons. Hatching: N < {cfg["thin_n"]}. Bands use rank-first ties; missing BPM is omitted.',
        ('Squid = quantile bins 6–8; Jackal = 14–16 on each axis. EW annotations retain those quantile memberships.' if cfg['show_squid_jackal'] and cfg['n_bins']==16 else 'Squid/Jackal summaries disabled.'),
        'At least 20 recorded season minutes; more than 10 team games. No new minutes cutoff, fitted parameters, or significance tests.']
    for j,line in enumerate(footer):fig.text(.06,.107-j*.016,line,fontsize=8.8)
    fig.savefig(out/f'{filename}.png',dpi=180,facecolor='white')
    return fig

def run(settings=None):
    cfg=settings_checked(settings);sources,manifest=base.load_frozen_sources()
    cohorts,reference,roster,meta=make_cohorts(sources,cfg)
    out=HERE/'runs'/datetime.now().strftime('%Y%m%d_%H%M%S_%f');out.mkdir(parents=True)
    plan=json.loads((HERE/'experiment_plan.json').read_text())
    baseline=Path(plan['baseline_run'])
    old=pd.read_csv(baseline/'all_players.csv.gz')
    assert np.array_equal(old.athlete_id,reference.athlete_id)
    assert np.array_equal(old.Y_draft,reference.Y_draft)
    assert np.allclose(old.perf,reference.perf)
    reference.to_csv(out/'candidate_reference.csv.gz',index=False)
    roster.to_csv(out/'available_roster.csv.gz',index=False)
    pd.DataFrame(meta['boundary_ties']).to_csv(out/'band_boundary_ties.csv',index=False)
    summary=[]
    for name,c in cohorts.items():
        c.to_csv(out/f'{name}_players.csv.gz',index=False)
        summary.append(dict(cohort=name,label=meta['labels'][name],observations=len(c),drafted=int(c.Y_draft.sum()),rate=float(c.Y_draft.mean()),
            above_theta=int(c.perf.gt(meta['threshold']).sum()),equal_theta=int(c.perf.eq(meta['threshold']).sum()),
            below_theta=int(c.perf.lt(meta['threshold']).sum()),colleges=c.team_id.nunique(),team_seasons=c.team_season_key.nunique(),
            under100_minutes=int(c.minutes.lt(100).sum()),missing_teammates=int(c.missing_teammates.gt(0).sum()),
            min_performance=float(c.perf.min()),max_performance=float(c.perf.max())))
    pd.DataFrame(summary).to_csv(out/'cohort_summary.csv',index=False)
    tables,regions,memberships,edges=base.build_tables(cohorts,cfg)
    pd.concat(tables.values(),ignore_index=True).to_csv(out/'bin_counts.csv',index=False)
    regions.to_csv(out/'squid_jackal_counts.csv',index=False)
    memberships.to_csv(out/'bin_membership.csv.gz',index=False)
    overlap=pd.crosstab(old.band_rank.le(int(np.ceil(.02*len(old)))).map({True:'baseline_top2',False:'baseline_other'}),reference.band)
    overlap.to_csv(out/'baseline_top2_membership_overlap.csv')
    p=dict(settings=cfg,**meta,plan=plan,source_manifest=manifest,baseline_run=str(baseline),
           module_hash=base.sha(__file__),helper_hash=base.sha(base.__file__),
           pressure_helper_hash=base.sha(HERE.parent/'roster_pressure_analysis.py'),
           reference_definition='Same 19,289 final-season candidates as baseline, ranked by within-season standardized BPM; theta calculated on those same values',
           pressure_definition='Sigmoid applied to full available eligible rosters before selecting any band; no averaging only among final-season candidates',
           actual_settings_differ_from_plan=cfg!=DEFAULTS,
           equal_width_edges={k:v.tolist() for k,v in edges.items()})
    (out/'provenance.json').write_text(json.dumps(p,indent=2)+'\n')
    with PdfPages(out/'Aligned_BPM_printable_comparisons.pdf') as pdf:
        for method in ['quantile','EW']:
            fig=draw(out,cohorts,meta,tables,regions,cfg,method,list(cohorts),AXES,f'aligned_BPM_mosaic_{method}')
            pdf.savefig(fig);plt.close(fig)
            for name in cohorts:
                fig=draw(out,cohorts,meta,tables,regions,cfg,method,[name],['rp_shared','rp_loo'],f'aligned_BPM_HERO_{name}_{method}')
                pdf.savefig(fig);plt.close(fig)
    (HERE/'latest_run.json').write_text(json.dumps({'run_directory':str(out),'settings':cfg},indent=2)+'\n')
    print(pd.DataFrame(summary).to_string(index=False));print('Aligned BPM experiment:',out)
    return out

def load_latest(settings):
    cfg=settings_checked(settings);s=json.loads((HERE/'latest_run.json').read_text());out=Path(s['run_directory'])
    p=json.loads((out/'provenance.json').read_text())
    if p['settings']!=cfg or p['module_hash']!=base.sha(__file__) or p['helper_hash']!=base.sha(base.__file__) or p['pressure_helper_hash']!=base.sha(HERE.parent/'roster_pressure_analysis.py'):
        raise ValueError('Settings or code changed. Rebuild this experiment, then Run All.')
    _,manifest=base.load_frozen_sources()
    if p['source_manifest']!=manifest:raise ValueError('Frozen source manifest changed. Audit and rebuild.')
    return out

if __name__=='__main__':run()
