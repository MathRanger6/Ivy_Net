from pathlib import Path
from pathlib import Path

# Figure 1: vary one sigmoid parameter while holding the other fixed.
PERFORMANCE_RANGE = (-3.0, 3.0)
SHARPNESS_VALUES = (0.5, 2.0, 8.0)  # gamma: larger means a sharper transition.
FIXED_THRESHOLD = 0.0               # theta for the left panel.
THRESHOLD_VALUES = (-1.0, 0.0, 1.0) # theta: location of the half-relevance point.
FIXED_SHARPNESS = 2.0               # gamma for the right panel.

# Figure 2: each inner tuple is the fixed roster of one group.
GROUP_PERFORMANCES = ((2.6, 2.3, 2.0), (2.4, 1.4, 0.2), (2.1, -0.4, -0.8))
THETA = 1.0
GAMMA = 2.0
K = 3                              # Number selected globally, across all groups.
LAMBDA_RANGE = (0.0, 2.0)           # Only lambda varies within Figure 2.

SAVE_FIGURES = True
OUTPUT_DIRECTORY = Path('/Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/manuscript_figures/section_4_5')
# Change OUTPUT_DIRECTORY if running on another computer.

# Figure 3: align scarcity with a reference threshold from performance.
# Each K is a GLOBAL number of places among the same nine individuals.
SCARCITY_PLACES = (3, 1)
SCARCITY_GAMMA = 2.0
SCARCITY_LAMBDA = 2.0
# Illustrative rule: theta = empirical (1 - K/N) quantile of A.
# Linear interpolation is explicit; this rule is not a verified historical fit.
SCARCITY_QUANTILE_METHOD = 'linear'

import csv
import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

OUT = OUTPUT_DIRECTORY
from IPython.display import Image, display
from io import BytesIO
if SAVE_FIGURES:
    OUT.mkdir(parents=True, exist_ok=True)
COLORS = ['#2474A5', '#CE771C', '#33815C']
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.titleweight': 'bold', 'axes.labelsize': 12,
    'svg.fonttype': 'none', 'savefig.facecolor': 'white'})

def sigmoid(a, theta, gamma):
    return 1 / (1 + np.exp(-gamma * (np.asarray(a) - theta)))

def finish(fig, name):
    # Explicit PNG display works even when Cursor shows only a Figure label.
    preview = BytesIO()
    fig.savefig(preview, format='png', dpi=160, bbox_inches='tight')
    display(Image(data=preview.getvalue()))
    if SAVE_FIGURES:
        for suffix in ('png', 'svg'):
            path = OUT / f'{name}.{suffix}'
            fig.savefig(path, dpi=230, bbox_inches='tight')
            print('Saved:', path)
    plt.close(fig)

if len(GROUP_PERFORMANCES) != 3 or any(len(g) != 3 for g in GROUP_PERFORMANCES):
    raise ValueError('This teaching layout requires three groups of three people.')
if GAMMA <= 0 or FIXED_SHARPNESS <= 0 or any(g <= 0 for g in SHARPNESS_VALUES):
    raise ValueError('Sharpness values must be positive.')
if not 1 <= K <= 9:
    raise ValueError('K must be between 1 and 9.')
if not 0 <= LAMBDA_RANGE[0] < LAMBDA_RANGE[1]:
    raise ValueError('Use a nonnegative increasing lambda range.')

# Standalone Figure 3 calculation: does not depend on running Figures 1 or 2.
from matplotlib.patches import Patch
scar_A = np.array(GROUP_PERFORMANCES, dtype=float).ravel()
scar_groups = np.repeat(np.arange(len(GROUP_PERFORMANCES)), [len(g) for g in GROUP_PERFORMANCES])
scar_ids = np.array([f'P{i+1}' for i in range(len(scar_A))])
scar_N = len(scar_A)
if len(SCARCITY_PLACES) != 2 or any(not isinstance(k, int) or not 1 <= k < scar_N for k in SCARCITY_PLACES):
    raise ValueError('Choose two integer values of K, each between 1 and N-1.')
if SCARCITY_GAMMA <= 0 or SCARCITY_LAMBDA < 0:
    raise ValueError('Use gamma > 0 and lambda >= 0.')
scar_order0 = np.lexsort((np.arange(scar_N), -scar_A))
scar_rank0 = np.empty(scar_N, dtype=int)
scar_rank0[scar_order0] = np.arange(1, scar_N+1)
scar_records = []
fig3, axes3 = plt.subplots(2, 2, figsize=(12, 10), gridspec_kw={'height_ratios':[1,1.5]})
fig3.subplots_adjust(top=.82, bottom=.12, left=.075, right=.965, hspace=.44, wspace=.30)
for col, k in enumerate(SCARCITY_PLACES):
    q = k/scar_N
    threshold = float(np.quantile(scar_A, 1-q, method=SCARCITY_QUANTILE_METHOD))
    relevance = sigmoid(scar_A, threshold, SCARCITY_GAMMA)
    pressure = np.array([relevance[scar_groups==g].mean() for g in range(len(GROUP_PERFORMANCES))])
    adjusted = scar_A - SCARCITY_LAMBDA * pressure[scar_groups]
    order = np.lexsort((np.arange(scar_N), -adjusted))
    ranks = np.empty(scar_N, dtype=int)
    ranks[order] = np.arange(1,scar_N+1)
    before, after = set(scar_order0[:k]), set(order[:k])
    gained, lost = after-before, before-after
    d = len(gained)
    assert d == k-len(before & after) == len(lost)
    top, bottom = axes3[:,col]
    grid = np.linspace(min(scar_A)-.3, max(scar_A)+.3, 500)
    top.plot(grid, sigmoid(grid,threshold,SCARCITY_GAMMA), color='#555555', lw=2)
    for g,color in enumerate(COLORS):
        mask=scar_groups==g
        top.scatter(scar_A[mask],relevance[mask],color=color,s=45,zorder=4,edgecolors='white',lw=.6)
    top.axvline(threshold,color='#555555',ls=':',lw=1)
    top.axhline(.5,color='#AAAAAA',ls=':',lw=1)
    top.set(xlim=(grid[0],grid[-1]),ylim=(-.035,1.05),xlabel=r'Performance $A_h$',ylabel=r'Competitive relevance $v_h$')
    top.set_title(f'Available places: {k} for {scar_N} people ({100*q:.1f}%)\n'
                  +rf'Reference threshold $\theta={threshold:.3f}$',fontsize=12,pad=12)
    top.text(.025,.96,'Recalculated roster pressure\n'+'   '.join(f'C{g+1} = {c:.3f}' for g,c in enumerate(pressure)),
             transform=top.transAxes,va='top',fontsize=9,
             bbox={'facecolor':'white','edgecolor':'#DDDDDD','alpha':.95})
    top.grid(alpha=.12)
    bottom.axhspan(.5,k+.5,color='#EAF1F6',zorder=0)
    bottom.axhline(k+.5,color='#555555',ls='--',lw=1)
    bottom.text(.5,k+.57,'selection boundary',ha='center',va='top',fontsize=8,color='#555555',
                bbox={'facecolor':'white','edgecolor':'none','pad':1})
    for person in range(scar_N):
        color=COLORS[scar_groups[person]]
        bottom.plot([0,1],[scar_rank0[person],ranks[person]],color=color,lw=1.5,alpha=.8)
        for x,r,selected in [(0,scar_rank0[person],person in before),(1,ranks[person],person in after)]:
            bottom.scatter(x,r,s=55,facecolor=color if selected else 'white',edgecolor=color,zorder=4)
        bottom.text(-.045,scar_rank0[person],scar_ids[person],ha='right',va='center',color=color,fontsize=10)
        bottom.text(1.045,ranks[person],scar_ids[person],ha='left',va='center',color=color,fontsize=10)
    bottom.set(xlim=(-.22,1.22),ylim=(scar_N+.5,.5),ylabel='Rank (1 = highest)',
               xticks=[0,1],xticklabels=['Performance-only\nscore','Congestion-adjusted\nscore'],yticks=np.arange(1,scar_N+1))
    bottom.tick_params(axis='x',length=0)
    bottom.spines['bottom'].set_visible(False)
    bottom.set_title(f'{d} of {k} places replaced: D/K = {d/k:.1%}',fontsize=12,pad=13)
    gaintext=', '.join(scar_ids[i] for i in sorted(gained)) or 'none'
    losstext=', '.join(scar_ids[i] for i in sorted(lost)) or 'none'
    bottom.text(.5,-.19,f'Gain a place: {gaintext}   |   Lose a place: {losstext}',
                transform=bottom.transAxes,ha='center',fontsize=10)
    scar_records.append({'K':k,'N':scar_N,'selection_fraction':q,'theta':threshold,
        'gamma':SCARCITY_GAMMA,'lambda':SCARCITY_LAMBDA,'group_pressure':pressure.tolist(),
        'relevance':relevance.tolist(),'adjusted_scores':adjusted.tolist(),
        'benchmark_winners':scar_ids[scar_order0[:k]].tolist(),'adjusted_winners':scar_ids[order[:k]].tolist(),
        'replaced_places':d,'fraction_replaced':d/k})
fig3.suptitle('Scarcer opportunities, a higher relevance threshold',fontsize=17,y=.995)
fig3.text(.5,.947,rf'Same population in both columns; $\gamma={SCARCITY_GAMMA:g}$ and $\lambda={SCARCITY_LAMBDA:g}$ held fixed',
          ha='center',fontsize=11)
fig3.legend(handles=[Patch(color=c,label=f'Group {g+1}') for g,c in enumerate(COLORS)],
            loc='upper center',bbox_to_anchor=(.5,.932),ncol=3,frameon=False)
fig3.text(.5,.013,r'Illustrative rule: $\theta=Q_{1-K/N}(A)$ (linearly interpolated empirical quantile).'
          '\nFilled circles = selected; open circles = not selected. Shaded ranks receive places. No selection noise.',
          ha='center',fontsize=10)
finish(fig3, 'figure_4_5_3_scarcity_and_threshold')
if SAVE_FIGURES:
    (OUT/'figure_4_5_3_inputs_and_results.json').write_text(json.dumps({
        'purpose':'Illustrative aligned-threshold construction, not a historical calibration or empirical finding',
        'threshold_rule':'empirical quantile at 1 - K/N','quantile_method':SCARCITY_QUANTILE_METHOD,
        'group_performances':GROUP_PERFORMANCES,'tie_rule':'Lower person number first','scenarios':scar_records
    },indent=2)+'\n')
for row in scar_records:
    print(f"K={row['K']}: theta={row['theta']:.3f}; benchmark {row['benchmark_winners']}; "
          f"adjusted {row['adjusted_winners']}; {row['replaced_places']} replaced.")
