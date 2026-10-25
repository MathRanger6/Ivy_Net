"""Entry 5: fixed top 3% and next 3% BPM bands; no outcome-driven cutoff selection."""
from pathlib import Path
import os,json,hashlib
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/ncaa_walkthrough_mpl')
os.environ.setdefault('XDG_CACHE_HOME','/private/tmp/ncaa_walkthrough_cache')
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent;W=HERE.parents[1]
cache=W/'manuscript_figures/section_4_5/roster_pressure_comparison/cache';source=cache/'last.pkl'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((cache/'source_manifest.json').read_text());assert sha(source)==m['cache_sha256']['last']
d=pd.read_pickle(source);assert len(d)==d.athlete_id.nunique()==22795 and d.Y_draft.sum()==615
coverage=d.assign(bpm_available=np.isfinite(d.BPM)).groupby('season').agg(players=('athlete_id','size'),bpm_available=('bpm_available','sum'),ever_drafted=('Y_draft','sum'))
coverage['bpm_missing']=coverage.players-coverage.bpm_available
coverage.to_csv(HERE/'bpm_coverage_by_season.csv')
a=d.loc[np.isfinite(d.BPM)].copy();assert len(a)==19289 and a.Y_draft.sum()==510
assert a.season.min()==2011 and a.season.max()==2021
# Pooled raw BPM rank, ties broken by original snapshot order. No draft outcomes enter ranking.
a['bpm_rank_desc']=a.BPM.rank(method='first',ascending=False).astype(int)
k1=int(np.ceil(.03*len(a)));k2=int(np.ceil(.06*len(a)))
a['bpm_band']=np.select([a.bpm_rank_desc<=k1,a.bpm_rank_desc<=k2],['Top 3%','Next 3%'],default='Other 94%')
assert k1==579 and k2-k1==579
selected=a.loc[a.bpm_rank_desc<=k2].sort_values('bpm_rank_desc').copy()
cols=['athlete_id','athlete_display_name','season','team_id','team_short_display_name','BPM','bpm_rank_desc','bpm_band','minutes','mp_sr','points','games_played','G','perf','Y_draft']
selected[cols].to_csv(HERE/'bpm_top_and_next_3pct_players.csv',index=False)
a[cols].sort_values('bpm_rank_desc').to_csv(HERE/'bpm_available_ranked_population.csv',index=False)
records=[]
for label in ['Top 3%','Next 3%']:
 g=selected.loc[selected.bpm_band==label];n=len(g);y=int(g.Y_draft.sum());p=y/n;z=1.959963984540054
 den=1+z*z/n;c=(p+z*z/(2*n))/den;h=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
 records.append(dict(band=label,n=n,ever_drafted=y,not_drafted=n-y,draft_rate=p,ci_low=c-h,ci_high=c+h,BPM_min=g.BPM.min(),BPM_max=g.BPM.max(),median_ESPN_minutes=g.minutes.median(),median_SR_minutes=g.mp_sr.median(),under50_ESPN=int((g.minutes<50).sum()),under100_ESPN=int((g.minutes<100).sum()),under100_SR=int((g.mp_sr<100).sum()),SR_minutes_missing=int(g.mp_sr.isna().sum()),ESPN_minutes_min=g.minutes.min(),SR_minutes_min=g.mp_sr.min(),rank_first=int(g.bpm_rank_desc.min()),rank_last=int(g.bpm_rank_desc.max())))
s=pd.DataFrame(records);s.to_csv(HERE/'bpm_band_summary.csv',index=False)
minute=[]
for label in ['Top 3%','Next 3%']:
 g=selected.loc[selected.bpm_band==label]
 for title,mask in [('Under 100',g.minutes<100),('100–499',g.minutes.between(100,499.999999)),('500 or more',g.minutes>=500)]:
  minute.append(dict(band=label,season_minutes=title,n=int(mask.sum()),ever_drafted=int(g.loc[mask,'Y_draft'].sum())))
mt=pd.DataFrame(minute);mt.to_csv(HERE/'bpm_band_minutes_counts.csv',index=False)
# Explicit audit of tied boundaries, preserving the user's rank-first quantile convention.
boundary=[]
for cutoff in [k1,k2]:
 val=float(a.loc[a.bpm_rank_desc==cutoff,'BPM'].iloc[0]);same=a[a.BPM==val]
 boundary.append(dict(rank=cutoff,BPM=val,tied_players=len(same),tie_rank_min=int(same.bpm_rank_desc.min()),tie_rank_max=int(same.bpm_rank_desc.max()),tied_before_or_at_cut=int((same.bpm_rank_desc<=cutoff).sum()),tied_after_cut=int((same.bpm_rank_desc>cutoff).sum())))
assert selected.athlete_id.nunique()==1158
assert mt.groupby('band').n.sum().eq(579).all()
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12})
fig,axs=plt.subplots(1,2,figsize=(13.5,7.2),gridspec_kw={'width_ratios':[1,1.2]})
fig.suptitle('BPM bands: draft outcomes and playing time',x=.075,y=.98,ha='left',fontsize=22,fontweight='bold')
fig.text(.075,.925,'2011–2021 | All eligible colleges | One saved final-season observation per player',fontsize=12.5)
fig.text(.075,.885,'19,289 players with BPM available | Pooled raw BPM ranks | No new minutes cutoff',fontsize=12)
x=np.arange(2);colors=['#245f8e','#779bb5'];ax=axs[0]
ax.bar(x,100*s.draft_rate,color=colors,width=.56)
ax.errorbar(x,100*s.draft_rate,yerr=[100*(s.draft_rate-s.ci_low),100*(s.ci_high-s.draft_rate)],fmt='none',ecolor='#333333',capsize=4)
for i,row in enumerate(s.itertuples()):ax.text(i,100*row.ci_high+2,f'{100*row.draft_rate:.1f}%\n{row.ever_drafted} / {row.n}',ha='center',fontsize=13)
ax.set_ylim(0,65);ax.set_ylabel('Players ever drafted (%)');ax.set_xticks(x,['Top 3%\nRanks 1–579','Next 3%\nRanks 580–1,158']);ax.set_title('Observed draft outcomes',fontweight='bold',pad=15)
ax=axs[1];bottom=np.zeros(2);cs=['#ca7c35','#a9bed0','#245f8e']
for label,col in zip(['Under 100','100–499','500 or more'],cs):
 vals=np.array([int(mt.loc[(mt.band==b)&(mt.season_minutes==label),'n'].iloc[0]) for b in s.band]);height=vals/579*100
 ax.bar(x,height,bottom=bottom,color=col,width=.56,label=label)
 for i in range(2):ax.text(i,bottom[i]+height[i]/2,str(vals[i]),ha='center',va='center',fontsize=13,color='white' if label=='500 or more' else '#111111')
 bottom+=height
ax.set_ylim(0,100);ax.set_ylabel('Share of each band (%)');ax.set_xticks(x,['Top 3%\n579 players','Next 3%\n579 players']);ax.set_title('Recorded season minutes',fontweight='bold',pad=15)
ax.legend(title='Total season minutes',loc='upper center',bbox_to_anchor=(.5,-.12),ncol=3,fontsize=10,frameon=False)
for ax in axs:
 ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
fig.text(.075,.09,'Rank bands are provisional: “Next 3%” is a candidate band of excellence, not a validated selection boundary.',fontsize=10.5)
fig.text(.075,.05,'Draft whiskers: pointwise 95% Wilson intervals, without college clustering. No significance tests. Minutes: saved ESPN totals.',fontsize=10)
fig.subplots_adjust(left=.075,right=.98,top=.79,bottom=.29,wspace=.37)
fig.savefig(HERE/'bpm_top_and_next_3pct.png',dpi=220,facecolor='white');plt.close(fig)
meta=dict(source=str(source),source_sha256=sha(source),source_inputs=m['inputs'],population='Frozen final-season cohort, restrict to finite BPM; no substitution of an earlier season for a missing final-season BPM',original_n=22795,original_ever_drafted=615,excluded_2009_2010_n=int((d.season<2011).sum()),excluded_2009_2010_drafted=int(d.loc[d.season<2011,'Y_draft'].sum()),excluded_2011_2021_missing_n=int(((d.season>=2011)&d.BPM.isna()).sum()),excluded_2011_2021_missing_drafted=int(d.loc[(d.season>=2011)&d.BPM.isna(),'Y_draft'].sum()),available_n=len(a),available_drafted=int(a.Y_draft.sum()),ranking='Pooled recorded raw BPM across available players, not season-specific percentile ranks or standardized BPM; descending rank method first, stable snapshot row order',cutoffs='ceil(0.03*N) and ceil(0.06*N); two nonoverlapping groups of 579',ties=boundary,minutes='Inherited minimum 20 ESPN season minutes; no added reliability floor. Report ESPN and Sports-Reference season minutes separately.',standardization='None newly applied to BPM; legacy PPM perf column retained only as a source field, not used for BPM ranking',outcome='Saved ever-drafted labels, not annual NBA draft probability',interpretation='Descriptive initial band inspection. No causal claim, no peer-environment curves, no significance tests, no 4-percent sweep.',script_sha256=sha(Path(__file__)))
(HERE/'bpm_band_provenance.json').write_text(json.dumps(meta,indent=2)+'\n')
print(s.to_string(index=False));print(mt.to_string(index=False));print('Boundary ties:',boundary)
