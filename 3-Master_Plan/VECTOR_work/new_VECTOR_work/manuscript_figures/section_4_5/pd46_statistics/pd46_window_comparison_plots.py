"""Side-by-side saved, verified season-window results. No statistical reruns."""
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
HERE=Path(__file__).resolve().parent
OUT=HERE/'window_comparison_figures'

def build():
    OUT.mkdir(exist_ok=True)
    paths={7:[HERE/'runs/20261014_190006_722614/panel7_bins.csv',HERE/'runs/common_window_20261015_110901/panel7_bins.csv'],
           8:[HERE/'runs/panel8_20261015_103422/panel8_bins.csv',HERE/'runs/common_window_20261015_110901/panel8_bins.csv']}
    figs={}
    for panel,files in paths.items():
        fig,axes=plt.subplots(1,2,figsize=(16,8.5),sharex=True,sharey=True)
        for index,(ax,path) in enumerate(zip(axes,files)):
            t=pd.read_csv(path);t['pct']=100*t.drafts/t.n
            peak=8 if panel==7 or index==1 else 7
            last=int(t.curve_bin.max());tail=t[t.curve_bin>last-2]
            r=t[t.curve_bin==peak].iloc[0];tail_rate=100*tail.drafts.sum()/tail.n.sum()
            ax.plot(t.x,t.pct,'o-',color='#545c65',lw=1.6,ms=4.5)
            ax.scatter([r.x],[r.pct],s=105,color='#236ca0',zorder=4,label=f'Tested peak: bin {peak}')
            ax.scatter(tail.x,tail.pct,s=70,color='#b33750',zorder=4,label=f'Tail: bins {last-1}-{last}')
            ax.hlines(tail_rate,float(tail.x.min())-.025,float(tail.x.max())+.025,color='#b33750',ls='--',lw=2)
            if panel==7 and index==1:
                tie=t[t.curve_bin==2].iloc[0]
                ax.scatter([tie.x],[tie.pct],s=105,facecolors='none',edgecolors='#236ca0',lw=2,zorder=4)
                ax.annotate('Tied peak',(tie.x,tie.pct),xytext=(0,31),textcoords='offset points',ha='center',color='#236ca0',fontsize=9)
            for row in t.itertuples():
                ax.annotate(f'{row.drafts}/{row.n}',(row.x,row.pct),xytext=(0,10),textcoords='offset points',ha='center',fontsize=8)
                ax.text(row.x,-.12,str(row.curve_bin),transform=ax.get_xaxis_transform(),ha='center',fontsize=8,color='#555555')
            period='2011-2021: ORIGINAL WINDOW' if index==0 else '2009-2021: TWO EARLIER SEASONS INCLUDED'
            ax.set_title(period+f'\n{int(t.n.sum()):,} observations; {int(t.drafts.sum()):,} ever-drafted-positive rows',fontsize=12,fontweight='bold',pad=15)
            ax.set_xlim(-.65,.65);ax.set_ylim(0,70 if panel==7 else 45)
            ax.set_xlabel('Leave-one-out mean teammate performance (z score)',fontsize=10,labelpad=43)
            ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False)
            ax.legend(loc='upper right',fontsize=9)
            fig.text(.30 if index==0 else .77,.17,f'Tested peak {r.pct:.1f}%  |  Pooled tail {tail_rate:.1f}%  |  Decline {r.pct-tail_rate:.1f} points',ha='center',fontsize=11,fontweight='bold')
        axes[0].set_ylabel('Observations with an ever-drafted outcome (%)',fontsize=11)
        band='Own-performance z scores from 2 to 3; 16 quantile peer bins' if panel==7 else 'Top 7% of own performance; 4 lower-region and 7 upper-region peer bins'
        fig.suptitle(f'PANEL {panel}: SAME DEFINITIONS, DIFFERENT SEASON WINDOWS\n{band}',fontsize=15,y=.98,va='top')
        foot='Small numbers below the axes are bin numbers. Counts above points: ever-drafted-positive rows / all player-team-season rows. Repeated people are retained.\nSame axes within each pair. Bin boundaries and eligible colleges are recomputed for each window.'
        if panel==8:foot+=' Own-score cutoff: 1.4936 to 1.4997.'
        fig.text(.5,.055,foot,ha='center',fontsize=10)
        fig.subplots_adjust(left=.07,right=.985,top=.78,bottom=.34,wspace=.14)
        fig.savefig(OUT/f'panel{panel}_windows_side_by_side.png',dpi=180,facecolor='white')
        figs[panel]=fig
    return figs
if __name__=='__main__':build()
