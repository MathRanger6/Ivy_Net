# LG exploration decision log

## 6 October 2026

Agent nickname: Leo, chosen at Charles's request.

Charles clarified that remaining seats supply opportunities, not a preference
for large teams. Homophily is the only preference. Use “remaining-seat
opportunities” versus “one opportunity per open team” in scientific captions.

Charles approved the first composition demonstration in successive discussion:

- Total capacity equals population size, holding final team sizes identical.
- 2,000 players, 100 teams, 20 seats per team.
- Homophily rho = 0, 0.5, 1, 2, 4.
- One fixed standard-normal population, 30 paired assignments per rho.
- Reuse arrival orders and underlying uniform draws between the two rules.

Both rules use actual-member centroids and identical empty-team initialization.
The seat-opportunity rule is LG. The team-opportunity rule is a separately
labeled alternative, even though this first experiment also fixes final sizes.
This demonstration has no scoring, selection, or MLE stage.

The notebook is the execution interface. Charles controls running it. Leo
performs only small correctness, plotting and resume checks during preparation.
At initial preparation, the full experiment (300 saved divisions) awaited
notebook execution. Complete saved results were subsequently found and verified;
additional diagnostics reuse them without reassignment.

## Explicit implementation conventions

Seeds 6102026 (population) and 6102027 (assignment) are reproducible engineering
choices, exposed in settings rather than empirical estimates. Streams for
arrival order and inverse-CDF choices are separate and independent of scheduling.
Their inputs are shared across rho as well as between opportunity rules.

Normal draws retain their realized sample moments; theoretical N(0,1) scaling
requires no further transformation. Original draws are preserved.

Within-team variances use the population convention (ddof=0). Distribution
curves average empirical CDFs across complete divisions. Shading and error bars
show one standard deviation across assignments, conditional on this one
population, rather than confidence intervals obtained by pooling players or teams.

The roster heatmap displays repetition 1, selected before observing results.
Each panel orders teams separately by mean talent and members by talent; team
rank is not a shared team identity.

Shifted log weights implement the declared normalized kernels without the
legacy all-underflow fallback. The five approved rho values are unchanged.
The random-grouping expected H_sort is (J-1)/(M-1) for this equal-size, random
arrival, rho=0 design; a small exact-enumeration check verifies both mechanisms.

No scientific output from validation runs should be presented as the approved
2,000-player experiment. Validation files are explicitly named under
results/validation/.

## Plot addition requested by Charles

Charles requested an additional plot of both models' actual H_sort values on
the same axes. The notebook now includes a dedicated comparison versus rho,
with individual-division dots, mean lines, and one-assignment-SD bars. The paired
difference plot remains. This presentation-only addition loads saved divisions
and leaves the scientific assignment module and checkpoint identities unchanged.

## Contender-count diagnostic approved by Charles

### Execution preference clarified

Charles clarified that he will very rarely ask Leo to compute scientific results
and show them in chat. Requests for a plot ordinarily mean add the code to the
working notebook, expose editable parameters, and let Charles run it. Do not
execute experiments or scientific plotting diagnostics, or present newly computed
results, unless Charles explicitly asks for that execution. Small code/formula
validation remains distinct from executing his research analysis. The contender
diagnostic now has a dedicated parameter cell immediately before its plotting
cell. This preference governs future work and supersedes any earlier assumption
that requesting a plot authorized Leo to compute and display it.

Charles requested a count of actual draft contenders on a player's team and
approved a cut at the realized population's 90th percentile. The contender
definition is strictly A > theta, using linear quantile interpolation. Theta is
frozen across all existing saved assignments. It is an exploratory threshold,
not an estimated draft requirement.

Two new figures show team contender counts and focal-player-excluded contender
teammate counts. The latter separates contenders from other players. Fractions
are computed per division and averaged over assignments, with one assignment-SD
shading. The diagnostic stores its threshold, implementation hash, source run ID,
division summaries, and full discrete distributions in a separate output folder.

In the approved population there are 200 contenders, hence mean contenders per
team is always 2. Mean contender teammates across all players is always 1.9.
These fixed averages do not constrain the conditional distributions for
contenders versus everyone else. This hard-count diagnostic does not change the
existing SCORE equation's smooth, self-included mean congestion.

## Notebook ownership of the rho grid

Charles requested that rho be changed exclusively through the notebook. The
notebook settings cell is the editable source; executing it validates and exports
settings/composition_first.json as a generated snapshot for CLI use and small
validation checks. The duplicate sweep grid in test_composition.py is removed.
Tests retain deliberately small populations and assignment counts, inherit the
notebook-exported rho grid, and derive expected division counts from its length.
Fixed rho values in individual formula checks remain mathematical test inputs,
not a second sweep configuration. The scientific assignment implementation and
existing checkpoint identities are unchanged.

## Notebook scenario tuples and plot filenames

Charles requested a scenario cell listing tuples of the form
('one', 100, 20, 30): rule, team count, players per team, assignment repetitions.
'one' selects one opportunity per open team; 'seats' selects remaining-seat
opportunities. Each tuple executes only its named rule. Shared RHO_VALUES, seeds
and theta quantile remain editable exclusively in the notebook. M is J*r.
The active generated snapshot is now settings/composition_scenarios.json.

Matching tuples across rules share talent, arrival orders and choice draws;
paired differences require matching dimensions and repetitions. Separate output
directories and resumable units prevent tuples from overwriting one another.
The unchanged original scientific kernel and matching original checkpoints are
reused read-only. Changing M changes the population length; identical M with the
same seed retains the identical talent vector.

Each plot filename identifies its metric and scientific settings, with a unique
digest and full JSON sidecar. Long lists use compact count/range tokens in names.
All selected complete scenarios receive individual diagnostics and an actual
H_sort comparison; eligible rule pairs also receive paired differences.
Charles controls execution. Only tiny validation cases are run by Leo.

Variable realized roster sizes follow this interface update and remain unimplemented.

## Still open

Excess-capacity experiments and large-cap convergence remain follow-ups. Their
cap grids and other settings are unapproved. SCORE scaling/clipping, thresholds,
selection settings and MLE choices remain open. No HPC submission, synchronization
or broad sweep is authorized by these files.

## Shared rule and talent-law controls; variable-roster starting dimensions

Charles revised the tuple interface: CHANCE_RULE is now one, seats or both for
all scenarios. SCENARIOS contains (teams, players per team, repetitions), without
a rule field. TALENT_DISTRIBUTION selects standard normal, Beta(2,2) or Weibull.
Charles approved an editable Weibull shape starting at 2.0. Weibull scale is 1.
Theoretical mean/SD scaling is the default; original-scale mode remains visible.
Raw draws are saved separately, and no realized sample standardization is used.
The normal scientific kernel and historical normal checkpoint identities remain
unchanged. Other laws/scales have separate scientific identities and validated
checkpoints. Plot names and sidecars include the law and scale.

Charles confirmed that the variable-roster extension holds M=2,000 and J=100
fixed, and allows final team sizes of zero. This does not imply any particular
cap rule or a minimum roster size. The cap decision remains the next scientific
question, before implementing that separate extension. No full research run was
executed during this update; only small implementation checks were performed.

## Empirical distribution preview requested by Charles

Charles requested an empirical player-distribution plot at the beginning of each
run, including all players across repetitions. The notebook now previews native
and assignment-scale draws side by side before its assignment cell, with editable
histogram bins and empirical mean/SD. Pooling includes M player appearances per
repetition, not duplicate copies for rho settings. Captions explicitly distinguish
M*repetitions appearances from M distinct players in this fixed-population design.
No fresh-population-per-repetition scientific change is implied. The preview is
saved with plot type, bin count and all existing parameter identifiers.

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

## Uncapped variable-roster extension approved

Charles chose uncapped assignment as the first variable-roster extension, with
M=2,000 and J=100 initially; empty final teams are permitted. Only homophily
controls preference. All teams stay eligible and have one opportunity per
arrival; there is no finite remaining-seat multiplier. Empty-team attachment
signals start and stay at the population mean until a first member arrives.
The original fixed-roster scientific kernel remains unchanged.

The notebook now has separate editable uncapped dimensions, repetition count and
RUN_UNCAPPED=False. Rhos, population mode (same by default), talent law/scaling,
seeds and theta reuse the existing notebook controls. Generated snapshots are
not a second settings interface. The runner saves resumable divisions and the
plotter reads completed checkpoints without assigning players.

Charles explicitly instructed Leo not to run experiments. Implementation means
writing code for Charles to execute. Verification for this extension is limited
to syntax and hand-constructed formula/plot fixtures; no populations were drawn,
assignments simulated or research results generated by Leo during this update.

Primary plots show roster-size PMFs and CDFs, all teams including zero, one color
per rho, averaged equally over repetitions. Additional summaries report empty
teams, largest rosters and size SD. M/J remains the mean, not a constraint on any
individual team. The rho=0 binomial reference is exact math, not a simulated run.
Unequal-size H_sort uses player-weighted between/within variance. Empty observed
means/variances are undefined; singleton variance is zero. Contender peer totals
use sum_j contenders_j*(n_j-1), avoiding the fixed-roster conservation formula.

## One complete uncapped settings cell

Charles requested all roster-size controls in one place in the uncapped section,
including team size, number of teams and the A_i distribution. The section is now
self-contained: no earlier import or shared-controls cells are required. Its
UNCAPPED_ settings independently control talent law/scale/Weibull shape, rho list,
repetitions, population mode (same by default), seeds, theta, histogram bins and
output directory. Fixed-roster settings remain unchanged.

Because realized rosters are uncapped, UNCAPPED_MEAN_TEAM_SIZE sets the population
average rather than prescribing individual rosters. Total players are derived
as UNCAPPED_MEAN_TEAM_SIZE * UNCAPPED_N_TEAMS (initially 20*100=2,000). Changing
either dimension changes total population; no minimum or maximum is imposed on
individual teams. RUN_UNCAPPED remains False. Only settings wiring, syntax and
notebook format were checked; no populations or assignments were generated.

## Hub exploration: empty starts and configurable initial centroids

Charles clarified that the purpose is to inspect whether hub teams emerge with
no roster limits or seeded roster head starts. The confusing mean-team-size input
was removed; total players (initially 2,000) and team count (100) are direct inputs.
Initial attachment centroids now default to realized Abar, with a notebook option
for a common numerical value or one value per team. Values are in assignment
talent units. First arrivals replace the starting signal exactly; subsequent
centroids are actual member means. Empty teams retain their initial signal.
No pseudo-members, counts or degree/size preference are introduced.

Every uncapped plot displays the starting T_j(0) values for all teams. Custom
lists use full team-range labels without omitting values; fresh default draws
show each repetition's realized Abar. Exact vectors are saved and validated in
checkpoints and plot sidecars. Settings and source changes isolate new runs from
old checkpoints. Only hand-built formula/plot fixtures and syntax/settings checks
are permitted for Leo; no experimental populations or assignments were generated.

## Temporary roster-only display

Charles requested only roster-size distributions for now. The uncapped settings
cell now has UNCAPPED_ROSTER_PLOTS_ONLY=True. This skips the population preview
and returns the roster-size PMF/CDF figure before constructing other diagnostics.
False restores all figures. Plot selection does not alter scientific settings
or checkpoint identities, so completed assignments can be replotted directly.
No experiments were run; verification uses a manually specified roster fixture.

## Fresh-mode plot captions: target only

Charles requested that fresh-mode plots show only the initial-centroid target,
without the realized values per repetition. Default captions now display
T_j(0)=Abar for all teams; numerical custom targets remain displayed by team.
Exact realized initial vectors remain in checkpoints and plot sidecars. This is
a plotting-only change and does not change assignments or scientific run IDs.
No experiments were run; caption checks use manually supplied values.

## Keep A_i preview in roster-only mode

Charles requested that roster-only mode retain the empirical A_i distribution.
The uncapped population-preview cell now always displays it when Charles runs
that cell. Other team diagnostics remain hidden by the roster-only switch.
Only notebook syntax/format checks were performed; no experiments were run.

## Descending rosters and circle view requested

Charles requested a descending list of actual team sizes after the distribution,
outside the plot, and a large filled-circle view to see large/small teams. Both
are added to roster-only mode. An editable, one-based display repetition chooses
one actual division per rho (default first repetition); aggregated distributions
continue to use all repetitions. Circle AREA, not radius, is proportional to
membership, with a common scale across rho panels and deterministic sorted grid.
Zero-member teams are listed and counted, with zero circle area. No hub threshold
is assumed. Text lists and parameter-named circle plots are saved. Checks use
only manually specified roster sizes; no experiments were run.

## Team-mean circle view

Charles requested a second circle figure identical to the member-size view.
Because assignment-scale team means can be negative, he approved circle area
proportional to absolute team mean, with color distinguishing sign: red positive,
blue negative and gray zero. The scale is shared across rho panels and teams are
ordered by descending absolute mean. Empty teams remain absent because their
observed means are undefined. Verification uses only hand-built fixtures.

## Highest-rho combined circle view

Charles requested a final circle figure showing only the highest selected rho,
with circle area proportional to roster size and color representing the team
mean. A symmetric zero-centered RdBu scale preserves sign and comparability:
dark red is strongly positive, dark blue strongly negative, and near-white near
zero. A colorbar gives assignment-talent units. Teams are ordered by roster size;
empty teams have no circles and remain counted in the title. Verification uses a
hand-built fixture; no experiment was run.

## Ranked roster tuple display

Charles requested (team size, team mean) tuples in the descending lists. Means
are actual member means in assignment-talent units, formatted to three decimal
places and kept aligned with their sizes during sorting. Empty teams display
(0, undefined). This changes only displayed/saved text; no experiments were run.

## Mean-versus-sum attachment attractor

Charles requested a setting that replaces the team-mean attachment signal with
the team talent sum. UNCAPPED_TEAM_ATTRACTOR now selects 'mean' or 'sum', and the
notebook currently selects 'sum'. Every empty team begins with one imaginary
value equal to its configured initial centroid. The first actual player replaces
that value completely. Subsequent arrivals produce either the actual-member mean
or actual-member sum. Thus the imaginary value supplies an initial signal but no
player, roster head start or persistent additive term. The selected mode is part
of settings, titles, filenames and scientific run identity. Only deterministic
formula and settings checks were performed; no experiment was run.

## Uniform talent option

Charles requested Uniform as an A_i distribution choice. Both notebook sections
now accept 'uniform', defined as Uniform(0,1). Original scale retains draws on
[0,1]; theoretical mean/SD scaling uses mean 1/2 and SD sqrt(1/12). Labels,
filenames, settings validation and scientific identities distinguish this law.
Only theoretical-moment and syntax checks were run; no population was drawn.

The first Uniform preview exposed a live-kernel reload defect: the notebook
accepted and labeled 'uniform', while the cached older draw_population function
fell through to its former Weibull branch. The uncapped validation and population
preview cells now reload talent.py before uncapped.py and uncapped_plots.py. This
ensures the displayed law and generator are the same without requiring a kernel
restart. The pictured mean 0.878 and values above 1 confirm that preview was not
Uniform(0,1) and should be discarded.

## Team-mean evolution for small J

Charles requested a wide round-by-round view when the uncapped model has at most
15 teams. One panel per rho reconstructs actual team means after every incoming
player, using a consistent color for each labeled team. Round 1 is the first
arrival. An empty team has no observed mean, so its line starts with its first
real member; markers show the rounds when it receives later members, and the
line remains flat between those events. The selected display repetition controls
the figure. It is omitted automatically above 15 teams. Reconstruction uses only
saved ability, membership and arrival-order arrays; no assignment is rerun.

## Uncapped one-plus-members opportunity option

Charles approved UNCAPPED_SEATS_OPTION=True as one base opportunity per team plus
one additional opportunity per actual member: team j has n_j+1 copies. Every
copy uses the same current team attractor. The notebook selects the team mean,
so multiplicity creates BA-style preferential attachment without making the
homophily target drift as a raw sum can. Empty teams retain one chance. At rho=0
the rule is P(j)=(n_j+1)/(assigned players+J), a symmetric Pólya process. This is
not the fixed-roster remaining-seats rule: that multiplicity falls as capacity is
consumed, while this one rises with realized membership. Settings, titles,
filenames, checkpoints and theoretical rho=0 roster references distinguish the
option. Only deterministic probability checks were performed; no experiment ran.

## 2026-11-10: Review of A-bar versus equally spaced initialization

Charles explicitly authorized new experiments for this review. The saved-run
inventory contains 58 historical metadata records. No matched historical pair
isolated A-bar versus equally spaced initialization. Recomputed team sizes,
means, and H_sort from 800 checkpoints across three key historical runs agree
with their saved results (see verified_historical_metrics.json).

The historical capped, one-opportunity, normal-talent A-bar run with 100 teams
of 20 players had mean H_sort approximately 0.050 at rho=0 and 0.787 at rho=4.
Thus common initial signals did not prevent substantial sorting. Historical
uncapped Beta runs with initial signals 0, 0.1, ..., 0.9 had rho=4 H_sort of
0.070 on the original scale versus 0.862 on the theoretically standardized
scale. This is not an initialization comparison: scale changes both effective
homophily strength and the placement of that numerical initial-signal grid.

New paired comparison: 2,000 players, 10 teams capped at 200, one opportunity
per nonfull team, actual-member mean attractor, first member replaces the
initial signal. Compare common realized A-bar with equally spaced signals
from realized minimum to maximum talent. Use 30 assignment repetitions,
rho=[0,0.5,1,2,4], and one fixed population each for standard normal and
theoretically standardized Beta(2,2). Arrival orders and choice uniforms are
paired between initializers. All capacities were filled; rho=0 assignments
were identical between initializers. The A-bar branch at repetition zero for
each law/rho exactly matched the existing fixed-roster assignment routine.

At rho=4, mean H_sort was 0.738 (A-bar) versus 0.658 (spaced) for normal talent,
and 0.769 versus 0.763 for Beta talent. A-bar therefore generated hierarchy
without requiring spaced starts; spaced starts were not consistently superior.
Under A-bar at rho=4, a random player on a lower-mean team exceeded a random
player on the next-higher-mean team about 28% (normal) or 29% (Beta) of the time,
averaged over adjacent teams ranked within each division. Hierarchy coexisted
with player-level overlap. H_sort itself is a variance ratio, not an overlap
percentage. These findings are conditional on the two fixed populations and
equal capacities; they do not validate a choice for empirical unequal rosters.
The chapter's initialization choice remains open pending Charles's decision.

Reproduction: code/review_initialization.py --run-paired.
Evidence: results/initialization_review_20261110/; paired run:
paired-e01d2b753f4c (specification, checkpoints, metrics, PNG and PDF).

## 2026-11-10: Proposed assignment chapter experiment plan

Status: proposed for Charles's review; this entry authorizes no new simulations.
Current conversation decisions supersede the October handoff where they differ.
The chapter briefly introduces the final model, builds from simple mechanisms
through controlled experiments, and returns to the final specification.
Hierarchy and player-level overlap are primary; individual experiments may
emphasize roster concentration. SCORE and SELECT receive a brief bridge only.

### Agreed common design

N=2,000; J=100; capped baseline capacities=20 each; standard-normal A_i.
All teams start empty at realized A-bar. The first member replaces this signal;
subsequent attraction uses the mean of actual members. Each nonfull team gets
one opportunity. Remaining-seat multiplicity is an alternative toggle.
Use rho=[0,0.5,1,2,4], with additional values proposed only after inspecting
transitions. Do not assume H_sort increases monotonically at high rho.
Initial comparisons use 30 paired assignment repetitions; principal comparisons
expand to 100. Reuse already compatible 100-repetition results rather than
discarding 70. Fresh-population validation uses 30 independent populations,
with 10 paired assignments per population per selected setting.

Pair populations, arrival orders, and choice uniforms between alternatives
within each repetition. The same random inputs do not imply identical teams.
Keep population and assignment seeds separate. For fresh populations, calculate
paired contrasts within population and summarize over populations; do not
treat all 300 assignments as 300 independent population draws.

### Proposed comparisons and figures

E1 Baseline homophily and emergent hierarchy
Vary rho only. Plot ranked final team mean (y) against within-division team
rank (x), one color per rho; pair with H_sort versus rho and an overlap
diagnostic versus rho. Show the rho=0 reference: (J-1)/(N-1)=99/1999.
Rank teams separately within each realization; named-team averages across
repetitions can conceal a hierarchy that emerges with different identities.
Use a predesignated repetition for distribution examples, not a cherry-picked
most hierarchical realization. Normal one-opportunity 100-repetition results
already exist at precisely this N/J/capacity/rho grid.

E2 Initialization
Compare A-bar with linspace(min A,max A,J), changing nothing else, across rho.
Plot both H_sort curves and both adjacent-team mixing curves on common axes.
At selected rho, show ranked means and population-supported within-team
distributions. The 10-team capped paired review is valid supporting evidence,
but a matched 100-team comparison is missing. Trajectories for 100 teams need
a readable supplementary display rather than silently changing J to 10.

E3 Opportunity rule under fixed rosters
Compare one opportunity per nonfull team with remaining-seat opportunities,
using the same population, capacities, centroids, orders, uniforms, and rho.
Plot actual H_sort and overlap for both rules; paired differences are secondary.
Both 100-repetition baseline runs exist. Metadata matches; before publication,
verify pairing and recompute metrics for the seat branch as well as the
previously checked one-opportunity branch. This may need analysis of saved
checkpoints, not new assignment simulations.

E4 Distribution shape
Compare normal, Beta(2,2), uniform(0,1), and Weibull(shape=2,scale=1), transformed
using theoretical mean and SD. Retain original draws. Beta is the priority
alternative, not an established empirical fit. Plot one curve per law for
H_sort versus rho and overlap versus rho, preceded by input-distribution
panels. Means/SDs are matched theoretically, not forced equal in each sample.
Common population quantiles across laws are a proposed coupling for new runs;
otherwise use explicit independent population streams and shared assignment
draws. Do not label different laws as the same population.
Normal and Weibull capped runs exist; full matched provenance and Beta/uniform
coverage require checking. A completed four-law controlled comparison has not
been established by the inventory.

E5 Removing the cap
Compare cap20 with no cap at fixed N=2,000 and J=100, mean attraction,
A-bar initialization and one opportunity per eligible team. Vary only capping
within each rho. Use roster PMF/CDF or survival curves with colors for rho,
and companion H_sort/overlap summaries. The capped roster distribution is a
point mass at 20. Report empty teams, largest-team share, top-10-team share,
and roster-size Gini. Empty teams count in size diagnostics but have no
observed mean; singleton within-team variance is zero.
Historical uncapped normal N=2,000/J=100 runs exist, but compatibility and
paired seeds with the chapter baseline remain to be established.

E6 Adding membership reinforcement
Within the uncapped mean-attractor model, compare one opportunity with n_j+1
opportunities, leaving every copy at the same team mean. Plot roster survival
curves, concentration versus rho, and the highest-rho circle display with area
proportional to membership and a common diverging mean-color scale.
Label this as a distinct reinforcement extension. Neither remaining-seat
weighting nor homophily alone is this mechanism. Large teams do not establish
a power law or equivalence to BA: team count is fixed here.
Existing reinforcement runs use other distributions or team counts; the
matched normal N=2,000/J=100 comparison is missing.

E7 Mean versus sum attraction
Within the uncapped, one-opportunity model compare mean with sum, across rho,
holding the initial empty-team signal at A-bar in both branches. The first
member replaces it in both. Compare H_sort, overlap, and roster concentration;
show attractor trajectories for a prespecified readable subset if needed.
Always calculate final team means separately from sum attractors.
Historical examples often change scale, initial signals, or team count as
well; they do not isolate this toggle at our baseline. The old initial value
of 1 is a separate choice, not silently bundled with changing the attractor.

E8 Units and scaling
Use a compact analytic demonstration and a deterministic equivalence check
rather than a full simulation sweep. For mean attraction, shifting every A_i
and initial signal equally preserves distances; multiplying them by a>0
requires rho_new=rho_old/a to preserve probabilities. Compare original versus
standardized values at unchanged rho only as an explicit units comparison.
Sum attraction is not generally translation invariant because its shift grows
with membership. This explains why original-scale historical results cannot
be pooled indiscriminately with standardized results.

### Measurement and uncertainty

H_sort is one player-weighted between/total variance ratio per division,
not an overlap fraction. Complement it with mean within-team variance and
adjacent-team inversion: sort nonempty teams by final actual-member mean,
calculate P(A_lower>A_upper) for independently drawn members of each adjacent
pair (half weight for ties), and average across pairs. State pair weighting;
compare with rho=0 rather than declaring 0.5 an exact finite-sample baseline.
This diagnostic describes ranking overlap, not the area of intersecting
densities. Also show selected team distributions so the reader can see shapes.

Use consistent rho colors from light at zero to dark at maximum. On plots with
rho on x, color identifies the toggle or distribution instead. Use common axes,
bins, and color limits within comparisons. Label curves as repetition means
and bands explicitly as variation (SD) or uncertainty intervals, never both.
Distinguish conditional assignment variation from variation across populations.
Save inputs, assignments, configuration/source hashes, summaries, and plot
filenames identifying settings. Save an A_i plot once per unique population
configuration, not once per opportunity-rule branch.

### Reuse and remaining evidence

Historical inventory: results/initialization_review_20261110/historical_inventory.json.
Previously recomputed checks:
results/initialization_review_20261110/verified_historical_metrics.json.
Exact normal baseline:
results/composition_scenarios/one_J100_r20_reps100/composition-96667ec378b7-d39e35e837ee.
Remaining-seat counterpart:
results/composition_scenarios/seats_J100_r20_reps100/composition-96667ec378b7-d39e35e837ee.
Both metadata records declare 500 complete divisions (5 rho x 100 assignments)
and shared population/order/uniform pairing. The earlier checkpoint review
validated the one-opportunity branch. A saved completion flag is not by itself
full scientific validation of every output.
Paired initialization evidence:
results/initialization_review_20261110/paired-e01d2b753f4c
uses 10 teams capped at 200, not the chapter baseline.
Inventory records include duplicated copies/settings and older schemas;
58 records must not be described as 58 independent experiments.

### Staging and chapter allocation

First audit/replot reusable E1/E3 checkpoints, then run only missing E2 and E4
comparisons after approval. Next isolate the uncapped E5-E7 mechanisms.
Promote central comparisons to 100 assignments, then validate the main claims
with 30 populations x 10 assignments. Extra rho values are adaptive exploratory
follow-ups; confirm any highlighted transition in fresh populations.

Proposed 28-34 page allocation: 3 pages for the final-model preview and notation;
3 for measurement/design; 7-9 for baseline, initialization and opportunity rule;
4-5 for shapes and units; 6-8 for caps, reinforcement and sum attraction;
3-4 for robustness, return to final model, and the short SCORE/SELECT bridge.
Aim for 8-10 main multi-panel figures, with detailed checks in supplementary
material. This is a planning budget, not a rendered page count.

Optional later comparisons, not required for the first chapter pass:
- Equal roster sizes r=[10,20,40,80] at fixed N, with J=N/r explicitly changing
  and a separate random reference for each J.
- Common excess caps [20,40,100,400,2000,20000] at fixed N,J, comparing one
  versus remaining-seat opportunity rules. This isolates capacity effects and
  illustrates convergence as a common cap becomes very large. Excess capacity
  is a separate variable-roster model; the fixed-roster engine must not be
  used by merely changing a cap setting.
- Empirical cap-vector check after the league/cohort and eligible population
  are selected; preserve total N and compare against an appropriately matched
  equal-size reference. No empirical input has been chosen for this plan.

The existing model manuscript uses remaining-seat multiplicity in its displayed
ASSIGN equation. Reconciliation with the selected one-opportunity baseline is
an eventual manuscript task; the source manuscript remains untouched.

## 2026-11-11: Roster-size sweep promoted to core chapter experiment

Charles selected option B: include the equal-roster-size sweep in the main
experiment plan rather than treating it as an optional later comparison.
Keep N=2,000 and reuse the same players across settings, with J=N/r. Thus this
comparison changes the partition size and number of teams together; it does
not isolate roster size at fixed J. Retain A-bar initialization, mean attraction,
one opportunity per nonfull team, and the agreed rho grid and repetition stages.
Proposed figures: H_sort versus rho with a colored line per roster size,
corresponding random references (J-1)/(N-1), excess above those references,
and adjacent-team overlap. Ranked-mean comparisons should use relative team
rank because J differs. Exact roster-size grid remains to be confirmed.
No new simulations or changes to notebook settings were made for this update.

### Approved grid and completed saved-evidence stage

Charles confirmed r=[10,20,40,80,100], J=[200,100,50,25,20], N=2,000,
and authorized verifying/replotting existing results before missing experiments
in stages. The remaining roster-grid decision above is now resolved.
code/chapter_saved_review.py and notebooks/02_chapter_saved_review.ipynb
provide reproducible analysis of saved checkpoints without assignment simulation.
All 1,000 checkpoints in the matched normal baseline one/seats runs passed
complete-grid, ID, capacity, population-seed, arrival-order and choice-uniform
checks. Recomputed means, variances and H_sort agree with stored values;
H_sort also agrees with saved CSV summaries. This is a checkpoint audit, not
a replay proving every historical assignment choice followed its kernel.
At rho=4: one H_sort=0.787119; seats=0.808762; paired difference=0.021642
with conditional SE=0.001661. Adjacent-team inversion is 0.468238 versus
0.466369. Adjacent ranks among 100 teams need not be widely separated even
when total between-team sorting is strong. These are conditional results for
one fixed normal population; they are not fresh-population robustness results.
Derived PNG/PDF figures and audit_report.json, including source hashes, are
in results/chapter_saved_review_20261111. Hierarchy and opportunity figures
were visually inspected; script and notebook cells compile. No historical
results or working-notebook settings were changed. Inventory finds only r=20
among the approved N=2,000 capped roster sizes; r=10,40,80,100 remain new work.

### Completed five-size paired roster sweep

Charles authorized running the missing roster sizes and plotting all five.
code/chapter_roster_sweep.py and notebooks/03_chapter_roster_sizes.ipynb now
provide resumable execution with visible roster/rho/repetition/seed settings.
Run results/chapter_roster_sweep/102f2dbd3ce8 contains 750 divisions: 600 new
assignments for r=10,40,80,100 and 150 imported r=20 assignments (first 30
repetitions at each rho). Same normal population, arrival orders and uniforms
are paired across all settings. Source kernel hashes match the imported run.
Every roster filled its capacity. Independent final means agree with online
centroids for new assignments. Re-execution for a caption correction resumed
all 750 checkpoints, checked their inputs, and generated zero new assignments.
PNG/PDF figures show all five sizes together: H_sort, excess above random,
within-team variance, adjacent-team inversion, and ranked means by rho.
One unique input-population plot is included. Figure layouts were inspected.
At rho=4, H_sort means for r=10,20,40,80,100 are respectively
0.797576,0.787248,0.780129,0.781744,0.769165. Lower/moderate rho displays larger
size differences. Interpret adjacent-team inversion alongside changing J:
adjacent ranks span different portions of the team distribution. All findings
are conditional on one fixed population, with 30 assignment repetitions.

