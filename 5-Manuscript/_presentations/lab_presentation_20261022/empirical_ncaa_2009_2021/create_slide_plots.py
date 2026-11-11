from pathlib import Path
import json, hashlib, os
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/ncaa_slide_mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
OUT=Path(__file__).resolve().parent
BASE=OUT.parents[1]/'manuscript_figures/section_4_5/year_window_comparison'
specs=[
 (9,'All performance levels','All eligible teams; one final-season observation per player',
 '16 equal-width bins (EW)',22795,615,8),
 (7,'High performers: own performance z = 2 to 3','Teams with a draftee in 2009–2021; all qualifying player-seasons',
 '16 quantile bins',534,175,65),
 (8,'High performers: top 7% by own performance','Teams with a draftee in 2009–2021; all qualifying player-seasons',
 'Piecewise EW bins: 4 below the peer median + 7 above',1546,418,65)]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':16,'axes.labelsize':18,'xtick.labelsize':15,'ytick.labelsize':15})
records=[]
for num,title,pop,binlabel,expected_n,expected_y,ymax in specs:
 source=BASE/f'panel_{num}_2009_2021_bins.csv';t=pd.read_csv(source)
 assert int(t.n.sum())==expected_n and int(t.drafted.sum())==expected_y
 assert np.allclose(t.rate,t.drafted/t.n)
 fig,ax=plt.subplots(figsize=(16,9));fig.patch.set_facecolor('white')
 fig.suptitle(f'Panel {num} | {title}',x=.07,y=.97,ha='left',fontsize=25,fontweight='bold',color='#173c59')
 fig.text(.07,.91,f'NCAA 2009–2021 | {binlabel}',fontsize=18)
 fig.text(.07,.865,pop,fontsize=16)
 count=(f'{expected_n:,} players; {expected_y:,} ever drafted' if num==9 else
        f'{expected_n:,} player-seasons; {expected_y:,} rows belonging to ever-drafted players')
 fig.text(.07,.825,count,fontsize=15,color='#444444')
 color='#276c97'
 ax.plot(t.center,100*t.rate,color=color,lw=2.6,zorder=3)
 for row in t.itertuples():
  ax.errorbar(row.center,100*row.rate,yerr=[[100*(row.rate-row.ci_low)],[100*(row.ci_high-row.rate)]],fmt='o',ms=7,mfc='white' if row.n<30 else color,mec=color,mew=1.6,ecolor=color,elinewidth=1.4,capsize=4,zorder=4)
  ax.text(row.center,-.105,str(int(row.n)),transform=ax.get_xaxis_transform(),ha='center',va='top',fontsize=11)
 ax.text(-.015,-.105,'n',transform=ax.transAxes,ha='right',va='top',fontsize=12)
 ax.set_xlim(-.65,.65);ax.set_ylim(0,ymax)
 ax.set_ylabel('Players ever drafted (%)' if num==9 else 'Player-seasons with ever-drafted status (%)')
 ax.set_xlabel('Mean teammate performance (LOO; focal player excluded)\nPoints per minute, standardized within season',labelpad=41)
 ax.grid(axis='y',alpha=.22);ax.spines[['top','right']].set_visible(False)
 note='Pointwise 95% Wilson intervals; no team-clustering adjustment. Counts under points; open markers: n < 30.'
 fig.text(.07,.069,note,fontsize=12,color='#444444')
 extra=('One observation per player.' if num==9 else 'Repeated players across seasons; intervals do not adjust for repeated observations.')
 fig.text(.07,.04,extra+' Descriptive associations, not causal effects or annual draft probabilities.',fontsize=12,color='#444444')
 fig.subplots_adjust(left=.095,right=.975,top=.775,bottom=.255)
 name=f'ncaa_panel_{num}_2009_2021_loo.png'
 fig.savefig(OUT/name,dpi=220,facecolor='white');plt.close(fig)
 t.to_csv(OUT/f'panel_{num}_plotted_bins.csv',index=False)
 records.append({'panel':num,'file':name,'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'n':expected_n,'positive_rows':expected_y,'population':pop,'binning':binlabel,'y_axis_max_percent':ymax,'note':'Original saved bin counts and Wilson intervals retained; no new significance tests. LOO mean raw performance, not sigmoid roster pressure.'})
(OUT/'provenance.json').write_text(json.dumps(records,indent=2))
print(json.dumps(records,indent=2))
