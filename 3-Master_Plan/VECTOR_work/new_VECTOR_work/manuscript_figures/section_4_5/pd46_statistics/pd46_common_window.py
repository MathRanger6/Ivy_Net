"""2009-2021 extension of original Panels 7 and 8; no network access."""
from pathlib import Path
from datetime import datetime
import sys,json,hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pd46_panel7 import REPO,dependency_groups,test_fixed_tail
from pd46_comparisons import four_way_results,distinct_bin_counts
HERE=Path(__file__).resolve().parent

def build_full():
    for p in [REPO/'sports',REPO/'sports/scripts']:sys.path.insert(0,str(p))
    from pass_a_congestion_conditional import CctSpec,_prepare_panel
    spec=CctSpec(season_min=2009,season_max=2021,min_minutes=20,min_team_season_games=10,
        winsor_lo=.01,winsor_hi=.99,n_bins=16,ai_lo=2.,ai_hi=3.,dft=True)
    return _prepare_panel(spec)

def run(full=None,repetitions=9999,seed=46):
    for p in [REPO/'sports',REPO/'sports/scripts']:sys.path.insert(0,str(p))
    from pass_a_congestion_conditional import _tj_piecewise_tail_edges,_assign_tj_bin_labels
    from sports_pipeline.panel_build import assign_poolq_bin_labels
    from sports_pipeline import paths
    if full is None:full=build_full()
    out=HERE/'runs'/datetime.now().strftime('common_window_%Y%m%d_%H%M%S');out.mkdir()
    source=REPO/'3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/data_story/_compare_0921'
    refs={7:source/'CCT_draft_rate_ai_band_poolq_loo_min20_ppm_z2_3_dft.json',8:source/'ELITE_pond_loo_pw4p7_dft_min20_mg10_top7_ppm_9_21.json'}
    cutoff=float(full.perf.quantile(.93))
    outputs={};meta={'years':[2009,2021],'repetitions':repetitions,'seed':seed,'panels':{},
        'definitions':'Panel 7 own-score z in [2,3]; Panel 8 pooled top 7%. Eligibility and bins recomputed by original rules over expanded window.',
        'coverage_limit':'Internal coverage and measurement consistency support exploration; not a certification of complete historical schedules or draft linkage.',
        'pipeline_game_filter':'More than 10 distinct recorded games per team-season (actual legacy implementation); at least 20 total player minutes.',
        'selection':'Highest observed rate among pre-tail bins; retain the original target if tied, otherwise lowest tied bin. Family includes every pre-tail bin versus same pooled tail.',
        'limitations':'Exploratory one-sided tests; no correction for historical window/panel/band/binning searches. All eligible player-team-seasons retained; ever-drafted label, not annual selection. Grouping is connected colleges across years and repeated players, not only contemporaneous teammates.',
        'input_files':{},'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    for p in [paths.player_box_csv(),paths.draft_lookup_csv()]:
        h=hashlib.sha256()
        with p.open('rb') as f:
            for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
        meta['input_files'][str(p)]=h.hexdigest()
    for panel in [7,8]:
        b=full.loc[full.perf.between(2,3) if panel==7 else full.perf.ge(cutoff)].copy()
        if panel==7:
            n=16;b['curve_bin']=assign_poolq_bin_labels(b.poolq_loo,16,'quantile').astype(int)+1;edges=None
        else:
            n=11;edges,_=_tj_piecewise_tail_edges(b.poolq_loo,n_low=4,n_high=7,split_q=.5)
            b['curve_bin']=_assign_tj_bin_labels(b.poolq_loo,edges).astype(int)+1
        t=b.groupby('curve_bin').agg(n=('Y_draft','size'),drafts=('Y_draft','sum'),x=('poolq_loo','mean')).reset_index()
        t['rate']=t.drafts/t.n
        ref=json.loads(refs[panel].read_text())
        if t.n.tolist()!=[r['n'] for r in ref['bins']] or t.drafts.tolist()!=[r['drafts'] for r in ref['bins']]:
            raise ValueError(f'Panel {panel} differs from saved 2009-2021 reconstruction.')
        if b.duplicated(['athlete_id','season','team_id']).any() or b[['athlete_id','season','team_id','Y_draft']].isna().any().any():raise ValueError('Invalid source identities')
        if not b.Y_draft.isin([0,1]).all() or (b.groupby('athlete_id').Y_draft.nunique()>1).any():raise ValueError('Invalid draft outcomes')
        b,groups=dependency_groups(b)
        candidates=t.loc[t.curve_bin<=n-2]
        tied=candidates.loc[candidates.rate==candidates.rate.max(),'curve_bin'].astype(int).tolist()
        original_target=8 if panel==7 else 7
        peak=original_target if original_target in tied else min(tied)
        grouped,alltests,method=test_fixed_tail(b,n_bins=n,target_bin=peak,repetitions=repetitions,seed=seed)
        independent,_,imethod=test_fixed_tail(b,n_bins=n,target_bin=peak,repetitions=repetitions,seed=seed,account_grouping=False)
        four=four_way_results(grouped,independent,repeated_rows=True,family_size=n-2)
        counts=distinct_bin_counts(b,{f'Peak bin {peak}':[peak],f'Tail bins {n-1}-{n}':[n-1,n],'Combined':[peak,n-1,n]})
        for label,frame in [('bins',t),('chosen',grouped),('all_comparisons',alltests),('independent',independent),('four_versions',four),('counts',counts)]:frame.to_csv(out/f'panel{panel}_{label}.csv',index=False)
        cols=['athlete_id','season','team_id','perf','poolq_loo','Y_draft','curve_bin']
        meta['panels'][panel]={'rows':len(b),'distinct_players':int(b.athlete_id.nunique()),'colleges':int(b.team_id.nunique()),
            'peak':peak,'tied_peak_bins':tied,'family_size':n-2,'cutoff':cutoff if panel==8 else [2,3],
            'multi_college_player_seasons':int((b.groupby(['athlete_id','season']).team_id.nunique()>1).sum()),
            'cohort_sha256':hashlib.sha256(pd.util.hash_pandas_object(b[cols],index=False).values.tobytes()).hexdigest(),
            'reference':str(refs[panel]),'reference_sha256':hashlib.sha256(refs[panel].read_bytes()).hexdigest(),
            'edges':None if edges is None else edges.tolist(),'grouped':method,'independent':imethod}
        outputs[panel]={'four':four,'counts':counts,'chosen':grouped,'bins':t}
        print(f'Panel {panel}: {len(b)} records; peak {peak}; tail {n-1}-{n}',flush=True)
        print(four.to_string(index=False),flush=True)
    fig,axes=plt.subplots(1,2,figsize=(15,6))
    for ax,panel in zip(axes,[7,8]):
        t=outputs[panel]['bins'];r=outputs[panel]['chosen'].iloc[0];peak=int(r.start_bin);n=len(t)
        ax.plot(t.x,100*t.rate,'o-',color='#444444')
        for mask,color,label in [(t.curve_bin==peak,'#427ca5',f'Peak bin {peak}'),(t.curve_bin>n-2,'#ae394e',f'Tail bins {n-1}-{n}')]:ax.scatter(t.loc[mask,'x'],100*t.loc[mask,'rate'],color=color,s=75,label=label,zorder=4)
        for r in t.itertuples():ax.annotate(f'{r.drafts}/{r.n}',(r.x,100*r.rate),xytext=(0,9),textcoords='offset points',ha='center',fontsize=8)
        ax.set(title=f'Panel {panel}: '+('own-score z = 2 to 3' if panel==7 else 'own-score top 7%'),xlabel='Leave-one-out teammate mean (z score)',ylabel='Observations with ever-drafted outcome (%)',ylim=(0,65))
        ax.legend();ax.grid(axis='y',alpha=.2)
    fig.suptitle('Common 2009-2021 window; original population and binning rules',fontsize=15)
    fig.text(.5,.02,'All eligible player-team-seasons; colleges represented by an ever-drafted player. Labels are positive rows / all rows.\nPanel 7: 16 quantile bins. Panel 8: 4 lower + 7 upper bins. Numerical cutoffs and boundaries are recomputed.',ha='center',fontsize=10)
    fig.tight_layout(rect=(0,.10,1,.94));fig.savefig(out/'common_window_comparison.png',dpi=180)
    (out/'provenance.json').write_text(json.dumps(meta,indent=2))
    return out,outputs,fig
