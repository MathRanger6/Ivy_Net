"""Four controlled descriptive mosaics. No significance tests."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pd46_panel7 import REPO
HERE=Path(__file__).resolve().parent
OUT=HERE/'printable_mosaics'

def build():
    for p in [REPO/'sports',REPO/'sports/scripts']:sys.path.insert(0,str(p))
    from pass_a_congestion_conditional import CctSpec,_prepare_panel
    from sports_pipeline.panel_build import assign_poolq_bin_labels
    OUT.mkdir(exist_ok=True)
    data={};metadata={'clipping':'NONE on both axes; raw means of within-season standardized performance.',
        'quantile_ties':'Original rank-first method: equal values can split by original row order. Charles explicitly chose this on October 15, 2026.',
        'pending':'Compare rank-first quantiles against tie-preserving quantiles later. Do not silently change method.',
        'population':'All eligible player-team-season rows, colleges represented by an ever-drafted player in each window. At least 20 player minutes; more than 10 team-season games (legacy implementation).',
        'outcome':'Ever drafted, not drafted that season. Repeated people retained.',
        'squid_jackal':'Original 16-quantile-bin proxies: Squid displayed bins 6-8; Jackal bins 14-16. Pooled positive rows / total rows. Applied descriptively to both axes/bands here; not permanent player labels.',
        'historical_panel8':'Original mixed-width plot uses 4 wider bins below the median and 7 narrower bins above. Its orange means fine upper-region bins, not the Panel 7 Jackal proxy. No mixed-width compression in these four mosaics.',
        'inference':'No statistical tests executed; no p-values shown.', 'runs':{}}
    for start in [2011,2009]:
        print(f'Preparing {start}-2021 populations and raw means',flush=True)
        spec=CctSpec(season_min=start,season_max=2021,min_minutes=20,min_team_season_games=10,winsor_lo=.01,winsor_hi=.99,n_bins=16,ai_lo=2.,ai_hi=3.,dft=True)
        full=_prepare_panel(spec)
        g=full.groupby(['team_id','season']).perf
        full['T_j']=g.transform('mean')
        full['LOO_raw']=(g.transform('sum')-full.perf)/(g.transform('count')-1)
        assert np.isfinite(full[['T_j','LOO_raw']]).all().all()
        cut=float(full.perf.quantile(.93))
        for panel in [7,8]:
            b=full.loc[full.perf.between(2,3) if panel==7 else full.perf.ge(cut)].copy()
            expected={(7,2011):(425,143),(7,2009):(534,175),(8,2011):(1237,330),(8,2009):(1546,418)}
            assert (len(b),int(b.Y_draft.sum()))==expected[panel,start]
            data[panel,start]=b
            metadata['runs'][f'{panel}_{start}']={'rows':len(b),'positive_rows':int(b.Y_draft.sum()),'own_cutoff':cut if panel==8 else [2,3],
                'sha256':hashlib.sha256(pd.util.hash_pandas_object(b[['athlete_id','team_id','season','perf','T_j','LOO_raw','Y_draft']],index=False).values.tobytes()).hexdigest()}
    figures={};all_rows=[];summaries=[];ranges=[]
    with PdfPages(OUT/'ALL_FOUR_printable_mosaics.pdf') as book:
        for panel in [7,8]:
            lo=min(data[panel,s][['T_j','LOO_raw']].min().min() for s in [2011,2009])
            hi=max(data[panel,s][['T_j','LOO_raw']].max().max() for s in [2011,2009])
            edges=np.linspace(lo,hi,17)
            metadata[f'panel{panel}_shared_EW_edges']=edges.tolist()
            for method in ['quantile','EW']:
                fig,axes=plt.subplots(2,2,figsize=(11,8.5),sharex=True,sharey=True)
                title=f'PANEL {panel} BAND | '+('Own-performance z = 2 to 3' if panel==7 else 'Own-performance TOP 7%')
                fig.suptitle(title+'\n'+('QUANTILE: 16 near-equal-count bins; rank-first ties' if method=='quantile' else 'EW: 16 equal-width bins; identical boundaries in all four plots'),fontsize=12,fontweight='bold',y=.97)
                for row,start in enumerate([2011,2009]):
                    b=data[panel,start]
                    for col,(axis,label) in enumerate([('LOO_raw','LOO: focal player EXCLUDED'),('T_j','T_j: focal player INCLUDED')]):
                        ax=axes[row,col];z=b.copy()
                        z['quantile_bin']=assign_poolq_bin_labels(z[axis],16,'quantile').astype(int)+1
                        if method=='quantile':z['bin']=z['quantile_bin']
                        else:z['bin']=pd.cut(z[axis],edges,include_lowest=True,labels=False).astype(int)+1
                        t=z.groupby('bin').agg(n=('Y_draft','size'),positive=('Y_draft','sum'),x=(axis,'mean'),xmin=(axis,'min'),xmax=(axis,'max')).reindex(range(1,17))
                        t[['n','positive']]=t[['n','positive']].fillna(0)
                        if method=='EW':t['x']=(edges[:-1]+edges[1:])/2
                        t['pct']=100*t.positive/t.n.replace(0,np.nan)
                        t=t.reset_index();t['panel']=panel;t['start']=start;t['axis']=axis;t['method']=method;all_rows.append(t)
                        ax.plot(t.x,t.pct,'o-',color='#44515b',lw=1,ms=3)
                        sq=z[z.quantile_bin.isin([6,7,8])];ja=z[z.quantile_bin.isin([14,15,16])]
                        sn,sy=len(sq),int(sq.Y_draft.sum());jn,jy=len(ja),int(ja.Y_draft.sum())
                        note=f'Quantile groups: Squid {sy}/{sn} ({100*sy/sn:.1f}%) | Jackal {jy}/{jn} ({100*jy/jn:.1f}%)'
                        for group,bins,color,subset in [('Squid',[6,7,8],'#20854b',sq),('Jackal',[14,15,16],'#bf660d',ja)]:
                            low,high=float(subset[axis].min()),float(subset[axis].max())
                            if method=='quantile':
                                q=t[t.bin.isin(bins)];ax.scatter(q.x,q.pct,color=color,s=25,zorder=4)
                                ranges.append(dict(panel=panel,start=start,axis=axis,group=group,xmin=low,xmax=high,n=len(subset),positive=int(subset.Y_draft.sum())))
                            else:
                                ax.axvspan(low,high,color=color,alpha=.12,zorder=0)
                                ax.axvline(low,color=color,alpha=.5,lw=.6,ls=':')
                                ax.axvline(high,color=color,alpha=.5,lw=.6,ls=':')
                                ax.text((low+high)/2,.94,group,transform=ax.get_xaxis_transform(),ha='center',va='top',color=color,fontsize=8,fontweight='bold')
                        if method=='quantile':
                            summaries.append(dict(panel=panel,start=start,axis=axis,squid_n=sn,squid_positive=sy,jackal_n=jn,jackal_positive=jy))
                        for i,r in enumerate(t.itertuples()):
                            if r.n>0:ax.annotate(f'{int(r.positive)}/{int(r.n)}',(r.x,r.pct),xytext=(0,6+14*(i%3)),textcoords='offset points',ha='center',fontsize=5.8)
                        ax.set_title(f'{start}-2021 | {label}\nn = {len(b):,} rows; ever-drafted-positive = {int(b.Y_draft.sum()):,}',fontsize=9,fontweight='bold',pad=9)
                        ax.set_ylim(0,112);ax.set_xlim(lo-.04,hi+.04);ax.set_yticks([0,25,50,75,100]);ax.tick_params(labelsize=8,labelbottom=True)
                        ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False)
                        ax.set_xlabel('Mean standardized performance (z score)',fontsize=8,labelpad=2)
                        if col==0:ax.set_ylabel('Ever-drafted observations (%)',fontsize=8)
                        ax.text(.5,-.23,note,transform=ax.transAxes,ha='center',fontsize=7)
                footer='NO CLIPPING on either axis. Means use the full eligible roster before selecting the own-score band.\nCounts above points: positive rows / all rows. Repeated player-seasons retained; no significance tests.\nSame axes on all four mosaics; NO coarse/fine bin compression. Empty EW bins have no estimated rate.'
                if method=='quantile':footer+='\nGreen = Squid proxy (bins 6-8); orange = Jackal proxy (14-16). These are bin-based comparisons, not player types.'
                else:footer+='\nShading = score ranges of quantile-defined Squid (6-8) and Jackal (14-16); totals retain exact quantile membership.\nShading shows member min-to-max scores; tied boundary scores may include nonmembers. EW points can straddle these ranges.'
                fig.text(.5,.025,footer,ha='center',fontsize=7.5)
                # Shared x limits across own-score bands, too, after all figures are built below.
                fig.subplots_adjust(left=.075,right=.98,top=.84,bottom=.20,hspace=.68,wspace=.18)
                figures[f'panel{panel}_{method}']=fig
        global_lo=min(d[['T_j','LOO_raw']].min().min() for d in data.values())-.04
        global_hi=max(d[['T_j','LOO_raw']].max().max() for d in data.values())+.04
        for name,fig in figures.items():
            for ax in fig.axes:ax.set_xlim(global_lo,global_hi)
            fig.savefig(OUT/(name+'.png'),dpi=240,facecolor='white')
            fig.savefig(OUT/(name+'.pdf'),facecolor='white');book.savefig(fig)
    pd.concat(all_rows,ignore_index=True).to_csv(OUT/'all_bin_counts.csv',index=False)
    pd.DataFrame(ranges).to_csv(OUT/'squid_jackal_score_ranges.csv',index=False)
    metadata['EW_overlays']='Quantile-group member min-to-max score ranges, calculated separately per panel/window/axis; counts retain exact rank-first membership. Shading cannot separate tied boundary values.'
    pd.DataFrame(summaries).to_csv(OUT/'squid_jackal_quantile_counts.csv',index=False)
    (OUT/'methods_and_provenance.json').write_text(json.dumps(metadata,indent=2))
    (OUT/'READ_ME_methods_and_next_steps.md').write_text('''# Printable comparisons

Print ALL_FOUR_printable_mosaics.pdf: four landscape US-letter pages. Individual PDF and high-resolution PNG versions are alongside it. Original figures and statistical results are untouched.

Rows: 2011-2021 then 2009-2021. Columns: LOO (self excluded), then T_j (self included). Two own-performance definitions, each shown with quantile and equal-width bins. All means are calculated on full eligible rosters before filtering own performance. Both axes are UNCLIPPED. This deliberately differs from the historical winsorized LOO curves. Quantile boundaries are recalculated in each panel; EW boundaries are common across the four panels of each mosaic. No coarse/fine binning in this set. All four mosaics have matching display axes.

## Squid and Jackal source definitions

sports/scripts/pass_a_congestion_conditional.py defines SQUID_VENT_16=(5,6,7) and JACKAL_VENT_16=(13,14,15), zero-indexed, corresponding to displayed bins 6-8 and 14-16. _pool_summary pools positive rows and total rows before calculating the rate. These are proxies within a matched own-performance band, not permanent player identities. The new quantile mosaics apply those region definitions descriptively to both axes and performance bands. On EW plots, shaded bands show the minimum-to-maximum peer scores of those same quantile-defined groups. Green denotes Squid and orange denotes Jackal. Counts and rates below the plots retain exact quantile membership, not overlapping EW-bin membership. Each range is recomputed for its own window, performance band, and peer measure. Shading cannot distinguish members from nonmembers sharing a tied boundary score; an EW point may pool observations inside and outside a shaded range. Exact extents and group counts are saved in squid_jackal_score_ranges.csv.

The original Panel 8 mixed-width version uses four lower and seven upper intervals. Its orange color labels finer upper-region bins, not the original Panel 7 Jackal category. Compression means fewer wider lower intervals, not deletion of the lower observations. Historical source figures remain available separately.

## DO NOT FORGET: compare quantile tie handling later

Charles explicitly requested the original rank-first quantile method on October 15, 2026. Equal x values may be split across bins according to existing row order to keep counts nearly equal. Later compare this with tie-preserving quantiles, particularly for T_j where teammates share the same value. Do not silently substitute the alternative. The task is recorded here and in notebook Section 4G.

## Limits

These are descriptive plots with unchanged own-score and population definitions. Repeated player-team-seasons are observations; outcomes are ever-drafted labels, not annual selection. No new significance tests were run. The within-window college restriction is outcome based. Data identity and historical coverage qualifications from the preceding audits still apply.
''')
    print(OUT,flush=True)
    return figures
if __name__=='__main__':build()
