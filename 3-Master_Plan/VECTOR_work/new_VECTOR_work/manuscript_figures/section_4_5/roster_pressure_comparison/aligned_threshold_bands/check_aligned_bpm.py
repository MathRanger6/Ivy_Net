from pathlib import Path
import sys,json
import numpy as np
import pandas as pd
E=Path(__file__).resolve().parent
sys.path.insert(0,str(E));import aligned_bpm_analysis as a
sources,_=a.base.load_frozen_sources();cfg=a.settings_checked({})
c,ref,roster,meta=a.make_cohorts(sources,cfg)
assert [len(c[k]) for k in ['top','middle','lower']]==[386,1543,3858]
assert sum(len(x) for x in c.values())==len(set().union(*(set(x.athlete_id) for x in c.values())))==5787
assert meta['threshold']==ref.perf.quantile(.98)
assert meta['top_band_matches_strict_above_theta']
groups=roster.groupby(['team_id','season'])
v=1/(1+np.exp(-cfg['gamma']*(roster.perf-meta['threshold'])))
roster['check_v']=v
for _,g in roster.groupby(['team_id','season']):
 assert np.allclose(g.rp_shared,g.check_v.mean())
 assert np.allclose(g.rp_loo,(g.check_v.sum()-g.check_v)/(len(g)-1))
c2,r2,_,m2=a.make_cohorts(sources,{**cfg,'gamma':2})
assert ref.band.equals(r2.band) and meta['threshold']==m2['threshold']
out=a.load_latest(cfg);counts=pd.read_csv(out/'bin_counts.csv')
for (method,name,axis),t in counts.groupby(['method','cohort','axis']):
 assert t.n.sum()==len(c[name])
 assert t.positive_rows.sum()==c[name].Y_draft.sum()
print('PASS: reference, disjoint bands, theta alignment, independent roster averages, gamma-invariant bands and all bin totals.')
