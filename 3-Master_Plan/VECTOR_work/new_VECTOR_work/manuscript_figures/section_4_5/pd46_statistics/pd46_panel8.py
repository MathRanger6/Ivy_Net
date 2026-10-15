"""Original Panel 8, with its original 11 bins and top-7% population."""
import hashlib
import json
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pd46_panel7 import REPO, dependency_groups, test_fixed_tail
SOURCE=REPO/'3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/_DISPOSABLE_elite_pond_loo_twin/ELITE_pond_loo_pw4p7_dft_min20_mg10_top7_ppm_11_21.json'

def load_panel8():
    for folder in [REPO/'sports',REPO/'sports/scripts']:
        sys.path.insert(0,str(folder))
    from pass_a_congestion_conditional import CctSpec,_prepare_panel
    spec=CctSpec(season_min=2011,season_max=2021,min_minutes=20,min_team_season_games=10,
        winsor_lo=.01,winsor_hi=.99,ai_lo=None,ai_hi=None,ai_top_pct=7.,dft=True)
    print('Rebuilding original Panel 8 from local files.',flush=True)
    full=_prepare_panel(spec)
    b=spec.apply_ai_band(full).copy()
    ref=json.loads(SOURCE.read_text())
    cut=full.perf.quantile(.93)
    if not np.isclose(cut,ref['ai_perf_cut'],rtol=0,atol=1e-12):
        raise ValueError('Own-performance threshold differs from original Panel 8.')
    edges=np.array(ref['bin_edges']);x=b.poolq_loo.to_numpy()
    bins=np.searchsorted(edges,x,side='right')-1
    bins[x==edges[-1]]=len(edges)-2
    b['curve_bin']=bins+1
    counts=b.groupby('curve_bin').agg(n=('Y_draft','size'),drafts=('Y_draft','sum'))
    if (len(b)!=ref['band_n'] or counts.index.tolist()!=list(range(1,12))
        or counts.n.tolist()!=[r['n'] for r in ref['bins']]
        or counts.drafts.tolist()!=[r['drafts'] for r in ref['bins']]):
        raise ValueError('Panel 8 does not reproduce all original bin counts.')
    if b[['athlete_id','team_id','season','Y_draft']].isna().any().any() or b.duplicated(['athlete_id','season']).any():
        raise ValueError('Missing identities or duplicate player-season records.')
    if not b.Y_draft.isin([0,1]).all() or (b.groupby('athlete_id').Y_draft.nunique()>1).any():
        raise ValueError('Inconsistent ever-drafted outcome.')
    b,groups=dependency_groups(b)
    cols=['athlete_id','season','team_id','perf','poolq_loo','Y_draft','curve_bin']
    meta=dict(panel=8,years=[2011,2021],own_band='Top 7%',cutoff=float(cut),
        source=str(SOURCE),source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        cohort_sha256=hashlib.sha256(pd.util.hash_pandas_object(b[cols],index=False).values.tobytes()).hexdigest(),
        rows=len(b),distinct_players=int(b.athlete_id.nunique()),positive_rows=int(b.Y_draft.sum()),
        colleges=int(b.team_id.nunique()),dependence_groups=int(b.dependence_group.nunique()),
        bin_edges=edges.tolist(),peak_bin=int((counts.drafts/counts.n).idxmax()),
        population='All eligible player-seasons; colleges represented by an ever-drafted player; minimum 20 minutes and 10 team-season games.',
        outcome='Ever-drafted status, repeated across eligible seasons; not annual selection.',
        binning='Original 4 lower-region and 7 upper-region equal-width intervals.',
        code_sha256=hashlib.sha256(__import__('pathlib').Path(__file__).read_bytes()).hexdigest())
    print(f'All 11 original bins verified: {len(b)} player-seasons.',flush=True)
    return b,groups,meta

def preview(b):
    t=b.groupby('curve_bin').agg(n=('Y_draft','size'),drafts=('Y_draft','sum'),x=('poolq_loo','mean')).reset_index()
    t['rate']=100*t.drafts/t.n
    fig,ax=plt.subplots(figsize=(11,6))
    ax.plot(t.x,t.rate,'o-',color='#434343')
    ax.scatter(t.loc[t.curve_bin==7,'x'],t.loc[t.curve_bin==7,'rate'],s=100,color='#427ca5',label='Peak: bin 7')
    ax.scatter(t.loc[t.curve_bin.isin([10,11]),'x'],t.loc[t.curve_bin.isin([10,11]),'rate'],s=75,color='#ae394e',label='Tail: bins 10-11')
    for r in t.itertuples():
        ax.annotate(f'Bin {r.curve_bin}: {r.drafts}/{r.n}',(r.x,r.rate),xytext=(0,10),textcoords='offset points',ha='center',fontsize=8)
    ax.set(title='Panel 8: peak bin 7 versus the final two bins\n2011-2021; own performance in the top 7%',xlabel='Leave-one-out mean teammate performance (z score)',ylabel='Player-season observations with ever-drafted status (%)',ylim=(0,45))
    ax.legend();ax.grid(axis='y',alpha=.2)
    fig.text(.5,.02,'Original 11 bins. Labels count player-seasons, not distinct players.\nCorrection compares each of bins 1-9 against the same pooled tail. Final bin has only 9 observations.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.08,1,1))
    return fig,t
