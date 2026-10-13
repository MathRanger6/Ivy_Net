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

# Figure 4 (Section 4.6.2): an actual seeded sequential assignment.
ASSIGNMENT_PERFORMANCES = (-1.5, -0.9, -0.3, 0.3, 0.9, 1.5)
ASSIGNMENT_CAPACITIES = (3, 3)  # Two groups for this step-by-step layout.
ASSIGNMENT_RHO = 2.0           # Similarity preference; 0 gives uniform remaining-slot allocation.
ASSIGNMENT_SEED = 42           # Controls both arrival order and assignment draws.

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

# Figure 4: calculate probabilities BEFORE each draw; show group states AFTER it.
assignment_a = np.asarray(ASSIGNMENT_PERFORMANCES, dtype=float)
assignment_capacity = np.asarray(ASSIGNMENT_CAPACITIES)
if len(assignment_capacity) != 2 or any(assignment_capacity <= 0) or not np.all(assignment_capacity == assignment_capacity.astype(int)):
    raise ValueError('This layout requires two positive integer group capacities.')
if assignment_capacity.sum() != len(assignment_a) or not np.all(np.isfinite(assignment_a)):
    raise ValueError('Total capacity must equal the number of finite performance values.')
if not np.isfinite(ASSIGNMENT_RHO) or ASSIGNMENT_RHO < 0:
    raise ValueError('Use a finite nonnegative rho.')
assignment_rng = np.random.default_rng(ASSIGNMENT_SEED)
arrival_order = assignment_rng.permutation(len(assignment_a))
assignment_mean = float(assignment_a.mean())
remaining = assignment_capacity.astype(int).copy()
centroids = np.full(2, assignment_mean)
rosters = [[], []]
history = [{'step':0, 'rosters':[[],[]], 'centroids':centroids.tolist(), 'remaining':remaining.tolist()}]
for step, person in enumerate(arrival_order, 1):
    before_centroids = centroids.copy()
    before_remaining = remaining.copy()
    # Log weights preserve the mathematical probabilities at large finite rho.
    log_weights = np.full(2, -np.inf)
    eligible = remaining > 0
    log_weights[eligible] = np.log(remaining[eligible]) - ASSIGNMENT_RHO*np.abs(assignment_a[person]-centroids[eligible])
    weights = np.exp(log_weights - np.max(log_weights))
    probabilities = weights/weights.sum()
    chosen = int(assignment_rng.choice(2, p=probabilities))
    rosters[chosen].append(int(person))
    remaining[chosen] -= 1
    centroids[chosen] = assignment_a[rosters[chosen]].mean()
    history.append({'step':step,'person':int(person),'chosen_group':chosen,
        'before_centroids':before_centroids.tolist(),'before_remaining':before_remaining.tolist(),
        'probabilities':probabilities.tolist(),'rosters':[r.copy() for r in rosters],
        'centroids':centroids.tolist(),'remaining':remaining.tolist()})
assert np.all(remaining == 0)
assert sorted(p for r in rosters for p in r) == list(range(len(assignment_a)))
for event in history[1:]:
    assert np.isclose(sum(event['probabilities']),1)
    for g in range(2):
        expected = assignment_a[event['rosters'][g]].mean() if event['rosters'][g] else assignment_mean
        assert np.isclose(event['centroids'][g], expected)

nrows=len(history)
fig4, assignment_axes = plt.subplots(nrows,3, figsize=(12,1.15*nrows+2.0),
    gridspec_kw={'width_ratios':[1.15,1.65,1.65]})
fig4.subplots_adjust(top=.84,bottom=.09,left=.035,right=.985,hspace=.25,wspace=.16)
span = max(float(np.ptp(assignment_a)), 1.0)
xmin,xmax = min(assignment_a)-.18*span,max(assignment_a)+.18*span
for row,event in enumerate(history):
    info=assignment_axes[row,0];info.axis('off')
    if row==0:
        info.text(0,.65,'START: empty groups',weight='bold',fontsize=11)
        info.text(0,.17,rf'Both centroids start at $\bar A={assignment_mean:.1f}$',fontsize=10)
    else:
        person=event['person']; probs=event['probabilities']
        info.text(0,.79,f"Step {row}: P{person+1} arrives, A = {assignment_a[person]:.1f}",weight='bold',fontsize=10)
        info.text(0,.43,f'Before draw: p₁ = {probs[0]:.3f}, p₂ = {probs[1]:.3f}',fontsize=9)
        info.text(0,.07,f"Draw → Group {event['chosen_group']+1}",fontsize=10,color=COLORS[event['chosen_group']])
    for g in range(2):
        ax=assignment_axes[row,g+1];color=COLORS[g]
        ax.set(xlim=(xmin,xmax),ylim=(-.6,1.2),yticks=[])
        for spine in ax.spines.values():spine.set_visible(False)
        ax.axhline(0,color='#BBBBBB',lw=.7)
        if row and event['chosen_group']==g:ax.set_facecolor('#EFF4F7')
        for person in event['rosters'][g]:
            ax.scatter(assignment_a[person],0,color=color,s=45,zorder=3)
            ax.text(assignment_a[person],.22,f'P{person+1}',ha='center',fontsize=9,color=color)
        centroid=event['centroids'][g]
        ax.scatter(centroid,-.32,marker='D',s=42,edgecolor=color,
                   facecolor=color if event['rosters'][g] else 'white',zorder=4)
        if row and event['chosen_group']==g:
            old=event['before_centroids'][g]
            desc=rf'$T_{g+1}: {old:.2f}\;\rightarrow\;{centroid:.2f}$'
        else:desc=rf'$T_{g+1}={centroid:.2f}$'
        count=len(event['rosters'][g]);cap=int(assignment_capacity[g])
        ax.text(.015,.92,desc,transform=ax.transAxes,va='top',fontsize=10)
        ax.text(.985,.92,f'{count}/{cap} members; {event["remaining"][g]} places left',
                transform=ax.transAxes,ha='right',va='top',fontsize=9)
        if row==0:ax.set_title(f'Group {g+1}: state after each step',fontsize=12,color=color,pad=13)
        if row==nrows-1:
            ax.set_xlabel(r'Performance $A$ (circles); centroid $T_j$ (diamond)',fontsize=9)
            ax.tick_params(axis='x',labelsize=8,length=3)
        else:ax.set_xticks([])
fig4.suptitle('Assign one individual, then update the chosen group’s centroid',fontsize=16,y=.99)
fig4.text(.5,.94,rf'One reproducible realization: $\rho={ASSIGNMENT_RHO:g}$; capacities {tuple(ASSIGNMENT_CAPACITIES)}; seed {ASSIGNMENT_SEED}',
          ha='center',fontsize=11)
fig4.text(.5,.89,'Read downward. Probabilities use the preceding row; shaded cells show the group receiving the arrival.',
          ha='center',fontsize=10)
fig4.text(.5,.022,'An empty group uses the population mean only as a reference. Its first member replaces that reference.'
          '\nEach later centroid is the mean of actual members. Full groups have zero assignment probability.',
          ha='center',fontsize=10)
finish(fig4,'figure_4_6_2_sequential_assignment')
if SAVE_FIGURES:
    (OUT/'figure_4_6_2_assignment_trace.json').write_text(json.dumps({
        'purpose':'Illustrative seeded assignment, not an empirical estimate',
        'performance_values':assignment_a.tolist(),'capacities':assignment_capacity.tolist(),
        'rho':ASSIGNMENT_RHO,'seed':ASSIGNMENT_SEED,'population_mean':assignment_mean,
        'arrival_order':[f'P{i+1}' for i in arrival_order],'history':history},indent=2)+'\n')
print('Arrival order:', ' → '.join(f'P{i+1}' for i in arrival_order))
print('Final memberships:', [[f'P{i+1}' for i in group] for group in rosters])
print('Final centroids:', centroids)
