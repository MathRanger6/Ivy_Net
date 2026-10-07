# Run composition scenarios from the notebook

Open notebooks/01_composition_opportunity_rules.ipynb, using the sports_net
Python kernel. Start Jupyter in lg_exploration/ or its notebooks/ folder.

## Your scenario cell

SCENARIOS is a list of tuples: (teams, players per team, repetitions).
For example, (100, 20, 30) specifies 100 teams of 20 and 30 assignments per rho.
CHANCE_RULE is a separate shared variable: 'one', 'seats', or 'both'. It applies
to every tuple. 'one' selects one opportunity per open team; 'seats' selects
remaining-seat opportunities. 'both' runs paired versions of every scenario.
Population size is calculated as teams times players per team. Duplicate tuples
are rejected.

TALENT_DISTRIBUTION selects 'normal' (N(0,1)), 'uniform' (Uniform(0,1)),
'beta' (Beta(2,2)), or 'weibull'
(scale 1). WEIBULL_SHAPE starts at 2.0 and is editable. TALENT_SCALE defaults to
 'theoretical_mean_sd': subtract the distribution's theoretical mean and divide
by its theoretical SD, without forcing realized sample moments. 'original' uses
native draws directly. Original draws and transformed talent are both saved.
Theoretical scaling makes rho comparable in population-SD units across laws;
using native units changes the effective strength of the same numerical rho.
Uniform(0,1) has mean 1/2 and SD sqrt(1/12). Beta has mean 1/2 and SD
sqrt(1/20). Weibull(k) has mean Gamma(1+1/k) and variance
Gamma(1+2/k) minus the squared mean. Normal needs no transformation.

Edit RHO_VALUES in the shared-controls cell. Seeds, THETA_QUANTILE and output
root are also visible there. Set RUN_EXPERIMENT=True, then Run All to execute or
resume. Leave it False to review completed scenarios. Running the settings
validation/export cell alone does not run assignments.

The notebook exports settings/composition_scenarios.json for the CLI and small
validation checks. This is a generated snapshot, not a second editable interface.
The prior composition_first.json is a legacy snapshot; it no longer controls
this notebook or its validation rho grid.

## Reproducibility and saved output

Each selected tuple runs the rule(s) selected by CHANCE_RULE. Matching rules and dimensions
share their talent vector, arrival orders and random uniforms. Same law, scale, parameters, seed and M
means identical players. Different M values have different-length populations;
only identical M values reuse the full vector exactly.

The runner saves and validates a division after every assignment. Run directories
include tuple dimensions and a scientific run ID. Restart with the same settings
to reuse complete units; partial/error state is retained. A matching normal/theoretical-scale original
paired-experiment checkpoint is verified and copied into the scenario directory
without regenerating it or mutating the original. Do not run concurrent processes
on the same scenario output.

Each tuple receives six plot types: team means, team variances, division summaries,
first-assignment roster compositions, team contender counts and focal-player
contender teammate counts. All selected complete tuples are included in an actual
H_sort comparison. Matching 'one' and 'seats' dimensions and repetitions also get
a paired-difference plot; pairing inputs are verified before differencing.

Distribution plots keep the same rho colors across scenarios. Error bars/shading
represent one assignment SD conditional on one population. Team variance uses
ddof=0; H_sort is division-level. Contender counts use the population quantile,
strictly A > theta, and exclude self for focal-player rival counts. This remains
a descriptive diagnostic, without SCORE, SELECT or MLE.

## Plot filenames

PNG and SVG names identify the metric, rule, J, r, repetitions, talent law/scale, rho grid, seeds,
theta quantile and a unique digest. A matching JSON file saves the complete
parameters. For long grids or many comparison tuples, compact count/range tokens
and the digest keep filenames below ordinary filesystem limits; the JSON retains
every exact value. Scenario plots are beneath their individual run directories;
comparison plots are under results/composition_scenarios/comparisons/.

## Optional CLI using the notebook-exported settings

From this folder in the sports_net environment:

~~~sh
PYTHONPATH=code python -B -m lg_composition.scenarios
~~~

This previews settings only. To explicitly execute and plot:

~~~sh
PYTHONPATH=code python -B -m lg_composition.scenarios --run --plots
~~~

Charles controls all scientific execution. Leo adds code and performs small
implementation checks unless explicitly asked to execute research analysis.

## Small validation checks

~~~sh
PYTHONPATH=code MPLBACKEND=Agg python -B code/test_scenarios.py -v
PYTHONPATH=code MPLBACKEND=Agg python -B code/test_composition.py -v
PYTHONPATH=code python -B code/test_contender.py -v
~~~

These use tiny populations with the notebook-exported rho grid. They check tuple
routing, reproducibility, resume, original-checkpoint compatibility, count
identities and parameter-named plot export. No full notebook sweep is launched.

Code, notebooks and small configuration snapshots belong in Git. Generated
results are ignored. Configure an explicit rsync scope before larger runs.
Variable realized roster sizes have a separate uncapped section; changing a fixed-roster tuple's
players-per-team value here changes prescribed equal sizes only.

The separate variable-roster extension starts uncapped with 2,000 players and 100 teams fixed,
allowing zero-member final teams. It is not controlled by these fixed-roster tuples.

## Empirical population preview

The notebook shows a player-distribution figure before its assignment-run cell,
even with RUN_EXPERIMENT=False. Original draws and assignment-scale talent are
shown side by side as empirical density histograms, with realized mean and SD.
TALENT_HIST_BINS is an editable notebook plotting control. Each scenario/rule
pools all M players over all repetitions exactly once per repetition, without
adding copies for rho values. Because one fixed population is reused, this pool
contains M*repetitions appearances of M distinct players. It is not a pool of
independent fresh talent samples. Preview files use the usual parameter-rich
PNG/SVG/JSON names and include the histogram bin count in the metric name.

## Unique talent previews and notebook imports

Talent previews are now deduplicated by population size and repetition count.
The shared distribution, scaling, shape and seed apply to every scenario. Choosing
both rules no longer doubles identical previews; different team dimensions with
the same M and repetitions also share one preview. Titles and filename population
tokens are independent of rule. All assignment/composition plots remain selected
by scenario and rule. The validation cell now loads and refreshes local imports
itself, preserving the user's separate scenario and controls cells.

## Population switch approved by Charles

POPULATION_MODE='same' is the default: retain one population across repetitions.
'fresh' generates new talent per repetition via SeedSequence([population_seed,
3, repetition]). Talent streams are independent of assignment streams and paired
across rules and rho values for each repetition. Histogram previews pool exactly
these populations without extra rule/rho copies. Normal/same preserves legacy
scientific identities; fresh mode has separate checkpoints. Contender thresholds
use each population's realized quantile, fixed across its rules/rho values.
Fresh-mode variability bars include population and assignment variation; same
mode remains conditional on one fixed population. No research sweeps were run.

## Uncapped extension: Charles runs the experiments

The notebook has a self-contained uncapped section. Edit its single complete
settings cell, then execute the uncapped cells in order. No earlier cells are
needed. RUN_EXPERIMENT controls the earlier section;
RUN_UNCAPPED controls this extension. Leave the latter False until ready to run.

Edit UNCAPPED_N_PLAYERS (2,000), UNCAPPED_N_TEAMS (100) and
UNCAPPED_REPETITIONS (30). Team sizes are outcomes, with no prescribed sizes or
roster caps. The same settings cell
contains UNCAPPED_TALENT_DISTRIBUTION (normal, uniform, beta or weibull), talent scaling,
Weibull shape, histogram bins, rhos, population mode, seeds and contender threshold.
These UNCAPPED_ controls are independent of the earlier fixed-roster settings. There is no
cap or minimum; CHANCE_RULE has no effect here. At each arrival every team has
one homophily-based opportunity. UNCAPPED_INITIAL_CENTROIDS defaults to 'population_mean' (realized Abar).
Use a finite number to set the same initial centroid for every team, or a list of
exactly J values to set individual starting signals in team order. Values use
assignment-talent units, after any chosen scaling. All teams still start empty;
no pseudoplayers or extra centroid weight are introduced. A first member replaces
the initial signal, later signals are member means, and an empty team retains its
chosen initial signal. In fresh mode Abar changes per repetition; custom signals
stay fixed across repetitions.

UNCAPPED_TEAM_ATTRACTOR selects 'mean' or 'sum'. In either mode, the initial
centroid is one imaginary attachment value for an empty team. The first real
player replaces it completely. Thereafter, mean mode uses the mean of actual
members, while sum mode uses the sum of actual member talents. The imaginary
value never contributes to a final mean, sum, roster size or player count. The
notebook currently selects 'mean'. This choice changes the scientific run ID and
requires its own assignments; it is not a plotting-only switch.

UNCAPPED_SEATS_OPTION=False gives every team one opportunity. True gives team j
exactly n_j+1 opportunities: one base opportunity plus one for each actual
member. All n_j+1 copies use the same current team attractor; with the notebook's
current mean setting, they all use the current team mean. Thus multiplicity
provides BA-style preferential attachment while the mean supplies the homophily
target. At rho=0 this is a symmetric Pólya process, P(j)=(n_j+1)/(players already
assigned+J). Empty teams retain one opportunity and can receive a first member.
The notebook currently sets UNCAPPED_SEATS_OPTION=True. This differs from the
fixed-roster remaining-seats rule: that multiplicity falls as capacity is
consumed, while this one rises with realized membership.

Validation saves settings/uncapped_rosters.json without running assignments.
The next cell previews talent draws across all repetitions when you run it.
Set RUN_UNCAPPED=True and execute the uncapped run cell to run/resume. Completed
results are stored under results/uncapped_rosters/. The plot cell only reads
verified complete checkpoints; it never assigns teams.

The first figure shows roster-size probabilities and cumulative fractions,
including size-zero teams, with one color per rho and ±1 repetition SD shading.
The rho=0 reference is calculated analytically: binomial with one opportunity
per team, or Pólya/Beta-binomial with the n_j+1 option. Further charts show
empty teams/largest roster/size SD, player-weighted H_sort and variance components,
occupied-team composition CDFs, and strict-threshold contender distributions.
Empty-team means and variances are undefined; singleton variance is zero.
The average roster size remains exactly M/J, independent of the distribution.

Plots have parameter-named PNG/SVG files and exact JSON sidecars. The division
summary CSV and roster_size_distributions.csv provide numerical frequencies by
rho and repetition. No experiment was executed to implement this extension.

The older validation scripts above invoke tiny assignment simulations. Leo will
not execute those under Charles's current no-experiments instruction. The new
code/test_uncapped_formulas.py uses only hand-constructed fixtures and exact math.
Finite-cap excess-capacity experiments remain unimplemented and undecided.

Every uncapped plot, including the talent preview, displays initial T_j(0) values
for all teams. Equal adjacent values are labeled by team ranges; heterogeneous
lists are displayed in full. Fresh mode shows the target T_j(0)=Abar, without
listing realized population means for each repetition. PNG/SVG filenames identify T0Abar, a common custom value, or T0perteam; exact
per-team values are retained in JSON sidecars and checkpoints. Changing the
centroid specification creates a separate scientific run identity.

## Temporarily show only roster distributions

UNCAPPED_ROSTER_PLOTS_ONLY=True in the uncapped settings cell keeps the A_i
talent preview and the roster-size PMF/CDF. It skips size-summary, sorting,
composition and contender figures. Set False to restore all plots. Rerun settings,
validation/import and plot cells to apply it; no new assignments are required
for completed settings. The switch is a plotting option, outside scientific
settings and run identities. Previously saved plot files are retained.

## Printed team sizes and hub circles

Roster-only mode also includes a descending text list and filled-circle roster
view, one actual division per rho. UNCAPPED_ROSTER_DISPLAY_REPETITION selects
the assignment to display (1 = first; up to UNCAPPED_REPETITIONS). Lists include
all teams and zeros, print after the distribution figure, and are also saved as
ranked_team_sizes_rep-NNN.txt in the run folder. Circle area is proportional to
actual team membership, with a shared scale across rho. Empty teams have zero
area and are counted in each panel title. The sorted grid is only a display
layout. No automatic hub cutoff is imposed. Distribution curves still aggregate
all repetitions. Replotting another saved repetition does not rerun assignment.

An adjacent circle figure uses the identical panel and grid design but sizes
circle area by the absolute team mean. Red circles have positive means, blue
circles have negative means, and gray circles have means of zero. The area scale
is shared across rho panels. Empty teams have undefined means and no circles.

The final circle figure shows only the numerically highest selected rho. Circle
area is proportional to membership, while a symmetric diverging color scale is
centered at zero: increasingly dark red indicates a higher positive team mean,
increasingly dark blue a more negative mean, and near-white a mean near zero.
A colorbar reports the assignment-talent units. Teams remain sorted by size.

When UNCAPPED_N_TEAMS is 15 or less, plotting automatically adds a wide
team-mean evolution figure for UNCAPPED_ROSTER_DISPLAY_REPETITION. The x-axis is
assignment round, beginning with round 1 for the first arriving player. Every
team keeps one color across all rho panels. Its line begins when its first real
member arrives because an empty team has no observed mean; dots identify rounds
when that team receives a player. Between arrivals its mean remains unchanged.
The histories are reconstructed from saved memberships and arrival order, so
plotting them does not rerun assignment. Above 15 teams the figure is omitted.
