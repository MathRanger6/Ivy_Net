"""Reproducible mathematical illustrations, not empirical results or fitted inputs.
Run with sports_net Python. Outputs are written alongside this script.
No manuscript or data-acquisition files are read or modified.
"""
from pathlib import Path
import csv
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

OUT = Path(__file__).resolve().parent
COLORS = ['#2474A5', '#CE771C', '#33815C']
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.titleweight': 'bold', 'axes.labelsize': 12,
    'svg.fonttype': 'none', 'savefig.facecolor': 'white'})

def sigmoid(a, theta, gamma):
    return 1 / (1 + np.exp(-gamma * (np.asarray(a) - theta)))

def finish(fig, name):
    for suffix in ('png', 'svg'):
        fig.savefig(OUT / f'{name}.{suffix}', dpi=230, bbox_inches='tight')
    plt.close(fig)

# Figure 1: vary one parameter at a time.
x = np.linspace(-3, 3, 1001)
fig, axs = plt.subplots(1, 2, figsize=(11, 4.8), sharey=True)
for gamma, color in zip([0.5, 2, 8], COLORS):
    axs[0].plot(x, sigmoid(x, 0, gamma), color=color, lw=2.5,
                label=rf'$\gamma={gamma:g}$')
axs[0].axvline(0, color='#888888', ls=':', lw=1)
axs[0].scatter([0], [.5], color='black', s=25, zorder=5)
axs[0].set_title(r'A   Change sharpness $\gamma$; hold $\theta=0$', loc='left', fontsize=12)
axs[0].legend(loc='upper left', frameon=False)
for theta, color in zip([-1, 0, 1], COLORS):
    axs[1].plot(x, sigmoid(x, theta, 2), color=color, lw=2.5,
                label=rf'$\theta={theta:g}$')
    axs[1].scatter([theta], [.5], color=color, s=25, zorder=5)
axs[1].set_title(r'B   Move threshold $\theta$; hold $\gamma=2$', loc='left', fontsize=12)
axs[1].legend(loc='upper left', frameon=False)
for ax in axs:
    ax.axhline(.5, color='#AAAAAA', ls=':', lw=1, zorder=0)
    ax.set(xlim=(-3,3), ylim=(-.025,1.025), xlabel=r'Individual performance $A_h$')
    ax.grid(alpha=.14)
axs[0].set_ylabel(r'Competitive relevance $v_h$')
fig.suptitle('How performance becomes competitively relevant', fontsize=16, y=1.02)
fig.text(.5, -.01, r'$v_h=\{1+\exp[-\gamma(A_h-\theta)]\}^{-1}$'
         '\nIllustrative inputs. Competitive relevance is not a selection probability.', ha='center', fontsize=11)
fig.tight_layout(rect=(0,.07,1,.98))
finish(fig, 'figure_4_5_1_competitive_relevance')

# Figure 2: fixed population, full-group sigmoid mean, then global deterministic top K.
A = np.array([2.6, 2.3, 2.0, 2.4, 1.4, .2, 2.1, -.4, -.8])
groups = np.repeat(np.arange(3), 3)
ids = np.array([f'P{i}' for i in range(1, 10)])
theta, gamma, K = 1.0, 2.0, 3
v = sigmoid(A, theta, gamma)
C = np.array([v[groups == g].mean() for g in range(3)])
lo, hi = 0.0, 2.0

def scores(lam):
    return A - lam * C[groups]

def winners(lam):
    # Higher score first, then lower person number at an exact boundary tie.
    return set(np.lexsort((np.arange(len(A)), -scores(lam)))[:K])

# Compute every actual crossing rather than infer winners from a plotting grid.
crossings = []
for i in range(len(A)):
    for h in range(i+1, len(A)):
        dc = C[groups[i]] - C[groups[h]]
        if abs(dc) > 1e-12:
            lam = (A[i] - A[h]) / dc
            if lo < lam < hi:
                crossings.append((float(lam), i, h))
breaks = sorted({lo, hi, *(p[0] for p in crossings)})
changes = [p for p in crossings if winners(p[0]-1e-7) != winners(p[0]+1e-7)]
assert len(changes) == 1
change_lam, i, h = changes[0]
assert {i,h} == {1,6}  # P7 replaces P2.
inside_lam = next(lam for lam,i,h in crossings if {i,h} == {0,3})
assert winners(inside_lam-1e-7) == winners(inside_lam+1e-7)
assert all(len(winners((a+b)/2)) == K for a,b in zip(breaks[:-1], breaks[1:]))

fig, (ax, strip) = plt.subplots(2, 1, figsize=(11, 9.5), sharex=True,
                              gridspec_kw={'height_ratios':[3.5,2.0], 'hspace':.27})
ls = np.linspace(lo, hi, 601)
for person in range(len(A)):
    ax.plot(ls, A[person] - ls*C[groups[person]], color=COLORS[groups[person]],
            lw=1.3, alpha=.45)
    # Bold portions mark membership in the top-K set on each open interval.
    for left,right in zip(breaks[:-1],breaks[1:]):
        if person in winners((left+right)/2):
            ax.plot([left,right], [scores(left)[person],scores(right)[person]],
                    color=COLORS[groups[person]], lw=3.5)
# Separate labels where endpoint scores are close, keeping a leader to each line.
endpoint = scores(hi)
label_y = endpoint.copy()
order = np.argsort(endpoint)
for previous, current in zip(order[:-1], order[1:]):
    label_y[current] = max(label_y[current], label_y[previous] + .17)
for person in range(len(A)):
    ax.plot([hi, hi+.045], [endpoint[person], label_y[person]],
            color=COLORS[groups[person]], lw=.7)
    ax.text(hi+.05, label_y[person], ids[person], color=COLORS[groups[person]],
            fontsize=9, va='center')
ax.set_ylabel(r'Adjusted score $S_i$')
ax.set_title('A   Scores change continuously; bold segments identify the three winners',
             loc='left', fontsize=12, pad=12)
ax.set_ylim(-1.8, 3.45)
ax.grid(alpha=.15)
for lam, pair, text, xytext in [
    (change_lam,(1,6),'P7 replaces P2\nin the selected three',(.14,3.05)),
    (inside_lam,(0,3),'P4 overtakes P1;\nboth remain selected',(1.0,2.85))]:
    y = scores(lam)[pair[0]]
    ax.scatter([lam],[y],s=48,facecolor='white',edgecolor='#222222',zorder=8)
    ax.annotate(text, xy=(lam,y), xytext=xytext, fontsize=10,
                arrowprops={'arrowstyle':'->','color':'#333333'},
                bbox={'facecolor':'white','edgecolor':'none','alpha':.95})
for person in range(len(A)):
    strip.broken_barh([(lo,hi-lo)], (person-.32,.64), facecolors='#EEEEEE')
    for left,right in zip(breaks[:-1],breaks[1:]):
        if person in winners((left+right)/2):
            strip.broken_barh([(left,right-left)], (person-.32,.64),
                             facecolors=COLORS[groups[person]])
strip.axvline(change_lam, ls=':', color='#555555', lw=1)
strip.set_yticks(range(len(A)), [f'{p}   (A = {a:g})' for p,a in zip(ids,A)])
strip.invert_yaxis()
strip.set_xlabel(r'Penalty strength $\lambda$')
strip.set_title('B   Who receives the three places? Colored = selected; gray = not selected',
                loc='left', fontsize=12, pad=12)
strip.set_xlim(lo,hi+.13)
strip.set_xticks(np.arange(0,2.01,.25))
strip.spines['left'].set_visible(False)
strip.tick_params(axis='y', length=0, labelsize=9)
fig.suptitle('Changing scores does not always change the winners', fontsize=16, y=.99)
fig.legend(handles=[Patch(color=c, label=rf'Group {g+1}: $C_{g+1}={C[g]:.3f}$')
                    for g,c in enumerate(COLORS)], loc='upper center',
           bbox_to_anchor=(.5,.957), ncol=3, frameon=False)
fig.subplots_adjust(top=.87,bottom=.13,left=.15,right=.93)
fig.text(.5,.025, r'$S_i=A_i-\lambda C_{g(i)}$; '
         r'$C_j=\frac{1}{3}\sum_{h:g(h)=j}\{1+\exp[-2(A_h-1)]\}^{-1}$'
         '\nFixed illustrative population: 3 groups of 3; global deterministic top 3; no selection noise.',
         ha='center', fontsize=10)
finish(fig, 'figure_4_5_2_scores_and_winners')

with (OUT/'illustrative_population.csv').open('w',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['person','group','performance_A','competitive_relevance_v','roster_pressure_C'])
    writer.writerows(zip(ids,groups+1,A,v,C[groups]))
(OUT/'illustration_settings.json').write_text(json.dumps({
    'purpose':'Mathematical illustration, not empirical data or fitted parameter values',
    'theta':theta,'gamma':gamma,'K':K,'lambda_range':[lo,hi],
    'boundary_tie_rule':'Lower person number first',
    'membership_change_lambda':change_lam,
    'within_selected_crossing_lambda':inside_lam,
    'winner_sets': [{'lambda_interval':[a,b], 'winners':sorted(ids[list(winners((a+b)/2))])}
                    for a,b in zip(breaks[:-1],breaks[1:])]
}, indent=2)+'\n')
(OUT/'figure_captions.txt').write_text(
    'Suggested placement: immediately after the corresponding explanation in Section 4.5.\n\n'
    'FIGURE 1. How the threshold and transition sharpness determine competitive relevance. '
    'Panel A holds theta at zero and varies gamma; all curves pass through relevance one half at the threshold. '
    'Panel B holds gamma at two and varies theta, shifting the transition along the performance axis. '
    'Performance is expressed in illustrative units. These curves define competitive relevance, not a probability of selection.\n\n'
    'FIGURE 2. Continuous score changes and discrete changes in the selected set. '
    'Nine illustrative individuals belong to three fixed groups of three. The threshold is theta=1 and gamma=2. '
    'Roster pressure is computed as the full-group mean of competitive relevance, including the focal individual, '
    'and held fixed as lambda varies. Scores are then used to select the global top three. '
    'In Panel A, group colors distinguish the three shared congestion values; parallel lines within each group '
    'reflect the common penalty. Bold segments indicate selected individuals. Panel B shows membership directly. '
    f'P7 replaces P2 at lambda approximately {change_lam:.3f}. '
    f'At lambda approximately {inside_lam:.3f}, P4 overtakes P1, but both remain selected. '
    'At an exact tie, lower person number takes precedence; the colored interval widths cannot depict an isolated endpoint. '
    'The inputs were chosen to illustrate these distinctions and are not empirical estimates.\n')
print(f'Created both figures (PNG and SVG), captions, inputs, and settings in {OUT}')
print(f'Membership changes at lambda={change_lam:.6f}; within-selected crossing at {inside_lam:.6f}')
