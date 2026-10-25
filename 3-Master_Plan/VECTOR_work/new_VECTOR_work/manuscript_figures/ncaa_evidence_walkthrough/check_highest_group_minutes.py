"""Audit exposure within the exact 178-player upper group; no new cohort filters."""
from pathlib import Path
import hashlib,json
import pandas as pd
import numpy as np
HERE=Path(__file__).resolve().parent;W=HERE.parents[1]
c=W/'manuscript_figures/section_4_5/roster_pressure_comparison/cache'
p=c/'last.pkl';m=json.loads((c/'source_manifest.json').read_text())
assert hashlib.sha256(p.read_bytes()).hexdigest()==m['cache_sha256']['last']
d=pd.read_pickle(p);assert len(d)==d.athlete_id.nunique()==22795
b=np.floor((d.perf.rank(method='first')-1)*16/len(d)).astype(int)+1
t=d.loc[b==16].copy();s=np.floor((t.perf.rank(method='first')-1)*8/len(t)).astype(int)+1
h=t.loc[s==8].copy();assert len(h)==178 and h.Y_draft.sum()==37
assert np.allclose(h.ppm,h.points/h.minutes)
h['recorded_minutes_per_game_played']=h.minutes/h.games_played
h['season_minutes_band']=pd.cut(h.minutes,[0,50,100,500,1000,np.inf],right=False,labels=['20–49','50–99','100–499','500–999','1000+'])
summ=h.groupby('season_minutes_band',observed=False).agg(players=('athlete_id','size'),ever_drafted=('Y_draft','sum'),median_recorded_games_played=('games_played','median')).reset_index()
assert summ.players.sum()==178 and summ.ever_drafted.sum()==37
summ.to_csv(HERE/'highest_group_minutes_summary.csv',index=False)
cols=['athlete_id','athlete_display_name','season','team_id','team_short_display_name','minutes','points','games_played','recorded_minutes_per_game_played','ppm','perf','Y_draft','season_minutes_band']
h.sort_values('perf',ascending=False)[cols].to_csv(HERE/'highest_group_player_minutes.csv',index=False)
meta=dict(source=str(p),source_sha256=m['cache_sha256']['last'],n=178,ever_drafted=37,season_minutes_min=float(h.minutes.min()),season_minutes_median=float(h.minutes.median()),season_minutes_max=float(h.minutes.max()),under50=int((h.minutes<50).sum()),under100=int((h.minutes<100).sum()),under100_ever_drafted=int(h.loc[h.minutes<100,'Y_draft'].sum()),atleast100_n=int((h.minutes>=100).sum()),atleast100_ever_drafted=int(h.loc[h.minutes>=100,'Y_draft'].sum()),interpretation='Recorded season totals in saved input, not externally verified complete participation histories. No raw source repair, restandardization, rebinning or permanent threshold change.',script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(HERE/'highest_group_minutes_provenance.json').write_text(json.dumps(meta,indent=2)+'\n')
print(summ.to_string(index=False));print(meta)
