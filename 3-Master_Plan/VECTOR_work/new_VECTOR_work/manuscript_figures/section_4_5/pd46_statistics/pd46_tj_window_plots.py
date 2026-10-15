"""Descriptive T_j versions of Panels 7/8; original LOO outputs untouched."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pd46_panel7 import REPO
HERE=Path(__file__).resolve().parent
OUT=HERE/'tj_window_comparison_figures'

def build():
    for p in [REPO/'sports',REPO/'sports/scripts']:sys.path.insert(0,str(p))
    from pass_a_congestion_conditional import CctSpec,_prepare_panel,_attach_t_j_hat,_tj_piecewise_tail_edges,_assign_tj_bin_labels
    OUT.mkdir(exist_ok=True)
    tables={};meta={'axis':'T_j = mean standardized performance of full eligible team-season roster, including focal player, computed before own-score filtering.',
        'clipping':'Raw full-team means from existing _attach_t_j_hat helper; no additional clipping. Original LOO plots use winsorized LOO means.',
        'quantiles':'Panel 7 uses 16 empirical quantile intervals; equal values kept together, counts may differ. Unlike original rank-first LOO bins, ties are not split.',
        'inference':'Descriptive only. No significance tests rerun. Highlighted peak and tail are visual markers.',
        'runs':{}}
    for start in [2011,2009]:
        spec=CctSpec(season_min=start,season_max=2021,min_minutes=20,min_team_season_games=10,winsor_lo=.01,winsor_hi=.99,n_bins=16,ai_lo=2.,ai_hi=3.,dft=True)
        print(f'Building T_j: {start}-2021',flush=True)
        full=_attach_t_j_hat(_prepare_panel(spec))
        assert full.groupby(['team_id','season']).T_j_hat.nunique().max()==1
        cut=float(full.perf.quantile(.93))
        for panel in [7,8]:
            b=full.loc[full.perf.between(2,3) if panel==7 else full.perf.ge(cut)].copy()
            if panel==7:
                edges=np.unique(b.T_j_hat.quantile(np.linspace(0,1,17)).to_numpy())
            else:edges,_=_tj_piecewise_tail_edges(b.T_j_hat,n_low=4,n_high=7,split_q=.5)
            b['bin']=_assign_tj_bin_labels(b.T_j_hat,edges).astype(int)+1
            assert b.groupby(['team_id','season'])['bin'].nunique().max()==1
            t=b.groupby('bin').agg(n=('Y_draft','size'),drafts=('Y_draft','sum'),x=('T_j_hat','mean')).reindex(range(1,len(edges))).reset_index()
            t['pct']=100*t.drafts/t.n
            expected={(7,2011):(425,143),(7,2009):(534,175),(8,2011):(1237,330),(8,2009):(1546,418)}
            assert (len(b),int(b.Y_draft.sum()))==expected[panel,start]
            t.to_csv(OUT/f'panel{panel}_{start}_2021_tj_bins.csv',index=False)
            tables[panel,start]=t
            meta['runs'][f'{panel}_{start}']={'rows':len(b),'positive_rows':int(b.Y_draft.sum()),'cutoff':cut if panel==8 else [2,3], 'edges':edges.tolist(),
                'cohort_sha256':hashlib.sha256(pd.util.hash_pandas_object(b[['athlete_id','season','team_id','perf','T_j_hat','Y_draft','bin']],index=False).values.tobytes()).hexdigest()}
    figs={}
    for panel in [7,8]:
        fig,axes=plt.subplots(1,2,figsize=(16,8.5),sharex=True,sharey=True)
        pair=[tables[panel,start] for start in [2011,2009]]
        xmin=min(t.x.min() for t in pair)-.05;xmax=max(t.x.max() for t in pair)+.05
        ymax=min(110,max(60,max(t.pct.max() for t in pair)+18))
        for col,(start,ax,t) in enumerate(zip([2011,2009],axes,pair)):
            n=int(t.bin.max());tail=t[t.bin>n-2];candidates=t[t.bin<=n-2].dropna(subset=['pct']);peak=candidates.sort_values(['pct','bin'],ascending=[False,True]).iloc[0]
            tailrate=100*tail.drafts.sum()/tail.n.sum()
            ax.plot(t.x,t.pct,'o-',color='#545c65',lw=1.6,ms=4)
            ax.scatter([peak.x],[peak.pct],s=95,color='#236ca0',label=f'Highest pre-tail bin: {int(peak.bin)}',zorder=4)
            ax.scatter(tail.x,tail.pct,s=65,color='#b33750',label=f'Final bins: {n-1}-{n}',zorder=4)
            ax.hlines(tailrate,tail.x.min()-.015,tail.x.max()+.015,color='#b33750',ls='--')
            for k,r in enumerate(t.itertuples()):
                if pd.notna(r.x):
                    ax.annotate(f'{int(r.drafts)}/{int(r.n)}',(r.x,r.pct),xytext=(0,9+(k%2)*9),textcoords='offset points',ha='center',fontsize=8)
                    ax.text(r.x,-.12,str(r.bin),transform=ax.get_xaxis_transform(),ha='center',fontsize=8)
            ax.set_title(f'{start}-2021'+(' : ORIGINAL WINDOW' if start==2011 else ' : EXPANDED WINDOW')+f'\n{int(t.n.sum()):,} observations; {int(t.drafts.sum()):,} ever-drafted-positive rows',fontsize=12,fontweight='bold',pad=16)
            ax.set(xlim=(xmin,xmax),ylim=(0,ymax));ax.grid(axis='y',alpha=.2);ax.legend(loc='upper left',fontsize=9)
            ax.set_xlabel(r'$T_j$: full-team mean performance (z score), including focal player',fontsize=10,labelpad=43)
            ax.spines[['top','right']].set_visible(False)
            fig.text(.30 if col==0 else .77,.17,f'Highlighted peak {peak.pct:.1f}%  |  Pooled tail {tailrate:.1f}%',ha='center',fontsize=11,fontweight='bold')
        axes[0].set_ylabel('Observations with an ever-drafted outcome (%)',fontsize=11)
        label='Own-performance z = 2 to 3; 16 quantile intervals, ties kept together' if panel==7 else 'Own-performance top 7%; 4 lower and 7 upper team-mean intervals'
        fig.suptitle(f'PANEL {panel} WITH FULL-TEAM MEAN T_j, INCLUDING THE FOCAL PLAYER\n{label}',fontsize=15,y=.98,va='top')
        fig.text(.5,.05,'Counts: ever-drafted-positive rows / all player-team-season rows. Small numbers below axes identify bins.\nTeam means use the full eligible roster before filtering own performance. Same observations as the LOO comparisons.\nDescriptive curves only; no new p-values. Bins are rebuilt for T_j. Team means are not additionally winsorized.',ha='center',fontsize=10)
        fig.subplots_adjust(left=.07,right=.985,top=.78,bottom=.34,wspace=.14)
        fig.savefig(OUT/f'panel{panel}_tj_windows_side_by_side.png',dpi=180,facecolor='white');figs[panel]=fig
    (OUT/'provenance.json').write_text(json.dumps(meta,indent=2))
    return figs
if __name__=='__main__':build()
