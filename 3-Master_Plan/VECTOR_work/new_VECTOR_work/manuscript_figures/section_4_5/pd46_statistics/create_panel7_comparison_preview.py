"""Show candidate contrasts on saved, verified original panel 7; no significance tests."""
from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
REPO=next(p for p in HERE.parents if (p/'sports/scripts/pass_a_congestion_conditional.py').exists())
SOURCE=REPO/'3-Master_Plan/re_entry/HEROs_and_PASSes/basic_data_plots/CCT_draft_rate_ai_band_poolq_loo_min20_ppm_z2_3_dft.json'

def make_preview():
    d=json.loads(SOURCE.read_text());r=d['bins']
    x=np.array([v['poolq_loo_mean'] for v in r]); y=np.array([v['draft_rate']*100 for v in r])
    fig,ax=plt.subplots(figsize=(12,6.5))
    ax.axvspan((x[6]+x[7])/2,(x[7]+x[8])/2,color='#427ca5',alpha=.2,label='Peak: bin 8')
    ax.axvspan((x[7]+x[8])/2,(x[9]+x[10])/2,color='#e59b35',alpha=.19,label='Immediately following: bins 9-10')
    ax.axvspan((x[13]+x[14])/2,x[-1]+.055,color='#ae394e',alpha=.15,label='Right-hand tail: bins 15-16')
    ax.plot(x,y,'o-',color='#30373e',lw=1.8)
    for k,(xx,yy,v) in enumerate(zip(x,y,r)):
        ax.annotate(f'{v["drafts"]}/{v["n"]}',(xx,yy),xytext=(0,8),textcoords='offset points',ha='center',fontsize=9)
        ax.text(xx,-.09,str(k+1),transform=ax.get_xaxis_transform(),ha='center',fontsize=9)
    ax.text(x[0]-.025,-.09,'Bin',transform=ax.get_xaxis_transform(),ha='right',fontsize=9)
    ax.set_ylim(0,75);ax.set_xlim(x[0]-.045,x[-1]+.055)
    ax.set_ylabel('Player-season observations with an ever-drafted outcome (%)')
    ax.set_xlabel('Mean other-teammate performance (z score)',labelpad=35)
    ax.set_title('Original panel 7: locate the decline before choosing the comparison\nOwn performance from 2 to 3 standard deviations above the mean',pad=14)
    ax.legend(loc='upper left',fontsize=9)
    ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False)
    fig.text(.5,.025,'2011-2021; colleges represented by at least one ever-drafted player; original 16 quantile bins.\nLabels are positive outcome rows / player-season rows, NOT counts of distinct drafted players.\nDescriptive preview; uncertainty bars omitted for clarity. No significance test is run by this script.',ha='center',fontsize=9)
    fig.subplots_adjust(bottom=.26,top=.85,left=.09,right=.98)
    return fig

if __name__=='__main__':
    fig=make_preview();out=HERE/'panel7_comparison_preview.png'
    fig.savefig(out,dpi=170);print(out)
