from pathlib import Path
import sys,json,hashlib
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))
from create_section_4_5_4_figure import load_verified_cohort,count_bins,REPO
OUT=BASE/'year_window_comparison';OUT.mkdir(exist_ok=True)
S=REPO/'3-Master_Plan/re_entry/HEROs_and_PASSes'
paths=[S/'basic_data_plots/CCT_draft_rate_ai_band_poolq_loo_min20_ppm_z2_3_dft.json',S/'sports_sandbox/data_story/_compare_0921/CCT_draft_rate_ai_band_poolq_loo_min20_ppm_z2_3_dft.json',S/'sports_sandbox/_DISPOSABLE_elite_pond_loo_twin/ELITE_pond_loo_pw4p7_dft_min20_mg10_top7_ppm_11_21.json',S/'sports_sandbox/data_story/_compare_0921/ELITE_pond_loo_pw4p7_dft_min20_mg10_top7_ppm_9_21.json']
def saved(p):
 d=json.loads(p.read_text());t=pd.DataFrame(d['bins']);assert t.n.sum()==d['band_n'];assert t.drafts.sum()==d.get('band_drafts',d.get('total_drafts'))
 return t.rename(columns={'poolq_loo_mean':'center','draft_rate':'rate','ci_lo':'ci_low','ci_hi':'ci_high','drafts':'drafted'}),d

def build():
 panel,edges=load_verified_cohort();short=panel.loc[panel.season.between(2011,2021)].copy()
 tables=[count_bins(panel,edges,'Panel 9 original'),count_bins(short,edges,'Panel 9 changed')]
 metas=[]
 for p in paths:
  t,d=saved(p);tables.append(t);metas.append(d)
 labels=['Panel 9: 2009–2021 (original)','Panel 9: 2011–2021 (changed)','Panel 7: 2011–2021 (original)','Panel 7: 2009–2021 (changed)','Panel 8: 2011–2021 (original)','Panel 8: 2009–2021 (changed)']
 desc=['All eligible teams; one final-season observation per player; all performance levels. Same 16 equal-width boundaries.',
 'Teams with a draftee in the window; all player-seasons; own performance z between 2 and 3. 16 quantile bins.',
 'Teams with a draftee in the window; all player-seasons; top 7% by own performance. 4 lower + 7 upper peer bins.']
 fig,axes=plt.subplots(3,2,figsize=(16,15));colors=['#356d95','#b24b36'];plt.rcParams.update({'font.size':10})
 summary=[]
 for row in range(3):
  pair=tables[row*2:row*2+2];upper=max(t.ci_high.max()*100 for t in pair)*1.12
  xmin=min(t.center.min() for t in pair);xmax=max(t.center.max() for t in pair)
  for col,t in enumerate(pair):
   ix=2*row+col;ax=axes[row,col];color=colors[col];n=int(t.n.sum());y=int(t.drafted.sum())
   ax.plot(t.center,t.rate*100,color=color,lw=1.7)
   for _,v in t.iterrows():
    if v.n:ax.errorbar(v.center,100*v.rate,yerr=[[max(0,100*(v.rate-v.ci_low))],[max(0,100*(v.ci_high-v.rate))]],fmt='o',ms=4.5,mfc='white' if v.n<30 else color,mec=color,ecolor=color,capsize=2,lw=.8)
    ax.text(v.center,-.11,str(int(v.n)),transform=ax.get_xaxis_transform(),ha='center',va='top',fontsize=8)
   unit='players' if row==0 else 'player-seasons';outcome='ever drafted' if row==0 else 'ever-drafted-positive rows'
   ax.set_title(labels[ix]+f'\n{n:,} {unit}; {y:,} {outcome}',fontsize=12,fontweight='bold',pad=10)
   ax.set_ylim(0,upper);ax.set_xlim(xmin-.045,xmax+.045);ax.set_ylabel('Ever-drafted outcome (%)');ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False)
   ax.text(-.02,-.11,'n',transform=ax.transAxes,ha='right',va='top',fontsize=8)
   ax.set_xlabel('Mean other-teammate performance (within-season z score)',labelpad=32)
   summary.append({'plot':labels[ix],'n':n,'positive_rows':y,'unit':unit})
   t.to_csv(OUT/f'panel_{[9,9,7,7,8,8][ix]}_{[2009,2011,2011,2009,2011,2009][ix]}_2021_bins.csv',index=False)
 for yy,txt in zip([.924,.632,.340],desc):fig.text(.5,yy,txt,ha='center',fontsize=11)
 fig.suptitle('Changing the year window, retaining each panel’s population rules',fontsize=18,y=.985)
 fig.text(.5,.015,'Matched axes within each row. Counts below points. Open circles: fewer than 30 observations. Bars: pointwise 95% Wilson intervals.\nPanels 7–8 retain repeated player-seasons; intervals are not cluster-adjusted. Their bin boundaries and team eligibility are recalculated by window.\nPanel 8 top-7% cutoff: z = 1.4936 (2011–2021), 1.4997 (2009–2021). Panel 9 retains the original peer scaling and bin boundaries.',ha='center',fontsize=10)
 fig.subplots_adjust(left=.07,right=.98,top=.88,bottom=.105,hspace=.72,wspace=.19)
 fig.savefig(OUT/'mosaic_panels_9_7_8_year_comparison.png',dpi=180,facecolor='white')
 for row,num in enumerate([9,7,8]):
  # Crop a separate row from the complete figure for comfortable viewing in chat.
  from PIL import Image
  im=Image.open(OUT/'mosaic_panels_9_7_8_year_comparison.png');W,H=im.size
  ranges=[(.065,.351),(.357,.647),(.648,.965)]
  lo,hi=ranges[row];im.crop((0,int(H*lo),W,int(H*hi))).save(OUT/f'panel_{num}_year_comparison.png')
 (OUT/'provenance.json').write_text(json.dumps({'summary':summary,'saved_sources':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],'panel9_method':'Verified original 2009–2021 last-season cohort, then retain seasons 2011–2021; retain original peer scaling, winsorization and bin boundaries.','panels7_8_method':'Read previously saved year-window reruns. Keep original rules, not a fixed set of teams, cutoff or bin edges.','panel8_cutoffs':[metas[2]['ai_perf_cut'],metas[3]['ai_perf_cut']]},indent=2))
 print(json.dumps(summary,indent=2),flush=True)
 return fig,summary
if __name__=='__main__':build()
