from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
BASE=Path('/Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE')
S=BASE/'3-Master_Plan/re_entry/HEROs_and_PASSes'
paths=[S/'basic_data_plots/CCT_draft_rate_ai_band_poolq_loo_min20_ppm_z2_3_dft.json',S/'sports_sandbox/_DISPOSABLE_elite_pond_loo_twin/ELITE_pond_loo_pw4p7_dft_min20_mg10_top7_ppm_11_21.json']
fig,axes=plt.subplots(1,2,figsize=(15.5,7.3),sharey=True)
for ax,path,title,color in zip(axes,paths,['A. Own performance: 2 to 3 standard deviations above the mean','B. Own performance: top 7%'],['#356d95','#b24b36']):
 d=json.loads(path.read_text());rows=d['bins'];x=np.array([r['poolq_loo_mean'] for r in rows]);y=np.array([r['draft_rate']*100 for r in rows]);lo=np.array([r['ci_lo']*100 for r in rows]);hi=np.array([r['ci_hi']*100 for r in rows]);n=sum(r['n'] for r in rows);yes=sum(r['drafts'] for r in rows)
 ax.plot(x,y,color=color,lw=1.7)
 for xx,yy,ll,hh,r in zip(x,y,lo,hi,rows):
  ax.errorbar(xx,yy,yerr=[[max(0,yy-ll)],[max(0,hh-yy)]],fmt='o',ms=5,mfc='white' if r['n']<30 else color,mec=color,ecolor=color,capsize=3,lw=1)
  ax.text(xx,-.12,str(r['n']),transform=ax.get_xaxis_transform(),ha='center',va='top',fontsize=8)
 ax.set_title(title+f'\n{n:,} player-season observations; {yes:,} with an ever-drafted outcome',fontsize=11,fontweight='bold',pad=15)
 ax.set_xlabel('Mean teammate performance (within-season z score)\nFocal player excluded',labelpad=39)
 ax.set_ylabel('Observations with an ever-drafted outcome (%)')
 ax.text(-.015,-.12,'n',transform=ax.transAxes,ha='right',va='top',fontsize=8)
 ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False);ax.set_xlim(-.65,.65);ax.set_ylim(0,80)
fig.suptitle('Selection across peer environments within two high-performance bands',fontsize=17,y=.97)
fig.text(.5,.905,'2011–2021 | Teams represented by at least one ever-drafted player | All eligible player-seasons',ha='center',fontsize=11)
fig.text(.5,.035,'Panel A: 16 quantile bins. Panel B: 4 lower-region bins and 7 finer upper-region bins. Bin boundaries differ between panels.\nCounts below points are player-seasons, not distinct players. Open circles: fewer than 30 observations.\nBars: pointwise 95% Wilson intervals, without adjustment for repeated players or team clustering. Descriptive associations.',ha='center',fontsize=10)
fig.subplots_adjust(left=.075,right=.98,top=.76,bottom=.29,wspace=.22)
out=BASE/'3-Master_Plan/VECTOR_work/new_VECTOR_work/manuscript_figures/section_4_5'
fig.savefig(out/'figure_4_5_4_original_mosaic_panels_7_8.png',dpi=220,facecolor='white')
print(out/'figure_4_5_4_original_mosaic_panels_7_8.png')
