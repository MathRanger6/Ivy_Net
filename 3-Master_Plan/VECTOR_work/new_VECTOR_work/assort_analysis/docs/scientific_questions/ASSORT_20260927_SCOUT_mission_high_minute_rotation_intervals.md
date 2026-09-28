# SCOUT mission: Do high-minute rotations still show broad basketball performance intervals?

**Prepared by VECTOR for Charles and SCOUT, September 27, 2026.**

**Status:** Historical mission, completed version-two extension, and a final editorial request. SCOUT executed both interval versions. VECTOR independently checked the version-two saved hashes, random memberships, widths, and sorting indices. The **last section** now asks SCOUT for two presentation corrections only. No further analytical run is requested. The earlier instructions remain as a record of how the diagnostic was specified and corrected.

## The question, in ordinary language

Our existing men's basketball interval plots show substantial overlap among teams when each team's interval runs from its lowest to highest eligible player's season points per minute. Charles asks whether that picture changes when the interval describes the players who actually occupied most of a team's captured court time. We must **keep all currently eligible players** in the reference population and in any separate congestion analysis. The proposed ten-player rule changes only this descriptive interval calculation; it is not a new eligibility rule, a declaration that the other players lack talent, or a change to the historical basketball analysis.

For example, on a team with twelve eligible players, the new interval uses the ten with the most total captured season minutes. The two omitted from that interval remain in the full-player interval and in the saved player population. One of them might be a talented player with little playing time—the very situation that motivated Charles's congestion question. Thus call the new quantity the **high-minute rotation interval**, not the team's latent-talent interval.

The diagnostic should answer three linked questions: How much do intervals and between-team overlap change? How much change would occur merely because any ten players were selected instead of the whole team? How many teams and players does this rule actually affect?

## Source and provenance boundary

Use **season 2015 only** for the first, bounded comparison. The starting player file is the accepted, source-rebuilt audit at:

`3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/outputs/rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_players.csv.gz`

Its construction, source-recovery decisions, and hashes are documented in:

- `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/results/ASSORT_20260927_rotation_audit_v1_report.md`
- `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/run_records/ASSORT_20260927_rotation_audit_v1_run_record.json`
- `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/decisions/ASSORT_20260927_rotation_audit_decisions.md`

This file was rebuilt from the frozen game records, rather than copied from an older exported panel. It incorporates the accepted game coverage, source-minute recovery, canonical-team choice, and twenty-total-minute eligibility floor. The accepted population is **4,267 unique players on 351 teams**, with **9–18 eligible players per team**. SCOUT should verify these counts and the saved file hash before using it. The relevant saved columns are `athlete_id`, `team_id`, `minutes` (total verified captured season minutes), `points_per_minute`, and `ability_standardized` (the 2015 eligible-population points-per-minute standard score). Preserve the saved player values and team assignments. Do **not** recompute a separate standardization after taking the top ten or a random ten.

The existing plot code is a **method reference**, especially its interval and coverage calculations:

`sports/scripts/empirical_team_interval_overlap.py`

Its `_team_intervals` function takes the within-team minimum, maximum, and mean of standardized player performance. Its coverage curve counts how many team intervals contain each horizontal-axis value. However, its `run_diagnostic` writes to historical `HEROs_and_PASSes/empirical_pd17/` destinations and prepares an older hero-path panel. **Do not run that entry point, overwrite its figures, or compare a new top-ten plot directly with its archived all-player plot as if the populations were identical.** Recompute all three cases from the *same accepted 2015 player file*. Source code can be consulted or safely reused, but any new driver and outputs belong inside `assort_analysis/`.

## The three prechosen cases

Let $a_i$ be player $i$'s saved `ability_standardized`, $m_i$ their saved season total `minutes`, and $P_j$ all accepted 2015 players on team $j$. For any chosen subset $Q_j$, draw its interval and mean marker as

$$
I_j(Q_j)=\left[\min_{i\in Q_j}a_i,\ \max_{i\in Q_j}a_i\right],
\qquad
\overline a_j(Q_j)=\frac{1}{|Q_j|}\sum_{i\in Q_j}a_i.
$$

Use the following cases on the same 351 teams:

1. **All eligible players:** $Q_j=P_j$. This is the newly computed, matched 2015 reference—not a reused archived figure.
2. **Ten highest-minute players:** Set $k_j=\min(10,|P_j|)$. Select exactly $k_j$ by descending total captured season minutes, breaking equal-minute ties by ascending numeric `athlete_id`. For teams with ten or fewer eligible players, this case is identical to the all-player case. Record how many teams have more than ten, exactly ten, and fewer than ten; never drop a team merely because it has fewer than ten.
3. **Random players, matched in number:** For each team independently, select $k_j$ members uniformly *without replacement* from its own $P_j$. Repeat this entire within-team draw **100 times** with one recorded seed and random-number-generator implementation. Retain all 351 teams in every repetition. This is a reference for selecting fewer players, **not** a random reassignment of players between teams and **not** the prior sorting-index shuffle experiment. A team with $|P_j|\leq10$ is necessarily unchanged in every repetition.

Ten is an initial, fixed descriptive choice. Do not optimize it for the most attractive plot or automatically run eight, five, or other values. The 100 random draws are sufficient for a compact reference, not a claim of precise tail probabilities.

## What to calculate and display

For each team, save its original eligible-player count, $k_j$, omitted-player count, original interval endpoints and width, high-minute interval endpoints and width, both subset means, total minutes represented by the high-minute group, and that group's share of eligible-player captured minutes. Preserve identifiers of the ten selected players and the omitted players, or save a separate player-level selection table keyed by `team_id` and `athlete_id`. This allows us to inspect whether a surprising interval change comes from one exceptional rate. Also count how often the original minimum or maximum player is omitted. Do not treat omission as evidence of low talent.

For each case, calculate the interval width $W_j=\max a_i-\min a_i$. On **one fixed horizontal grid built from the all-player interval endpoints**, calculate coverage

$$
C(x)=\sum_j {\bf1}\{x\in I_j\}.
$$

Use the same teams, horizontal range, grid points, and vertical coverage scale for all cases. Because every high-minute or random interval is a subset of its all-player interval, its width and its coverage at every fixed $x$ **cannot exceed** the corresponding all-player values. Some narrowing is guaranteed by construction. A side-by-side picture without the random reference would not establish that playing-time selection explains the broad original ranges.

Provide one readable comparison figure showing the three coverage views (the random view can be a median curve with a descriptive range across its 100 draws) on a common scale. Provide a paired width display for all-player versus high-minute intervals, with the random-ten width reference, and a small set of **identical, preselected team identifiers** in the all-player and high-minute interval panels. Keep each team's row position/order fixed by its all-player mean so movement is not disguised by re-sorting. Label all axes as **standardized observed season points per minute**. If a red dot marks a mean, label it as the mean of the players *included in that displayed interval*; the high-minute dot is not the full-team mean. Layout is SCOUT's choice so long as these comparison properties hold.

The numeric report should include team and player denominators; counts of affected and unaffected teams; distributions of omitted-player counts and minute shares; distributions of widths and paired width changes; and the maximum and mean coverage on the common grid for all-player, high-minute, and random cases. Preserve per-draw random aggregate summaries and the seed so the reference can be reproduced. Do not report a classical confidence interval or a $p$-value from the 100 within-team draws: they condition on this particular observed roster and serve as a sample-size reference, not uncertainty about all basketball seasons.

## Integrity checks and stopping conditions

- Match the saved input's checksum to the accepted audit run record. Confirm one 2015 row per athlete, finite points per minute, finite standardized scores, nonnegative finite season minutes, and 4,267 players on 351 teams. Any mismatch requires an explanation before plotting.
- Confirm that the high-minute and random selections contain only players from their own original team, with exactly $k_j$ unique athletes per team; all-player, high-minute, and every random draw must contain the same 351 team identifiers.
- Confirm the standard scores, team assignments, and original eligible-player file never change. The all-player intervals must equal a direct group-by calculation of saved `ability_standardized`.
- Confirm each high-minute interval is contained within its all-player interval, and its width and coverage never exceed the all-player result at the shared grid points. Apply the same check to random draws. Check deterministic tie resolution and reproducibility from the recorded seed.
- If a source column, team identity, or saved hash differs from this mission, **stop and ask Charles/VECTOR**; do not silently substitute an older panel, rebuild under new rules, fill missing values, or trim a team to force ten.

This was originally a descriptive interval test without a new sorting-index calculation. **Charles's September 27 follow-up explicitly adds the bounded sorting-index calculation in the final section below.** Do not refit the assignment model, make draft-outcome curves, modify the congestion calculation, change the twenty-minute eligibility rule, or search multiple rotation sizes in this pass. Those would answer different questions and require separate decisions.

## Isolated implementation and handoff back

Place a new diagnostic driver under `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/code/` and new outputs under a clearly named `outputs/rotation_core_intervals_2015/` directory. Put the readable result under `docs/results/` and its execution record under `docs/run_records/`. Save the exact input and code hashes, configuration, seed, library versions, checks performed, output paths, and output hashes. Do not edit or overwrite the frozen source data, the saved rotation audit, shared `sports/` code, or historical interval plots.

Return to Charles and VECTOR with: (1) paths to the implementation, figure, team/player comparison, random-draw summary, result narrative, and run record; (2) the substantive findings in plain language; (3) any deviations from this mission; and (4) what the test **does not** establish. VECTOR and Charles will then inspect whether the implementation meets the intent before deciding what the result means for the broader basketball investigation.

The intended reading is conditional. If the high-minute intervals remain broadly overlapping, this particular rotation restriction did not remove the observed overlap. If they narrow about as much as random ten-player intervals, the apparent improvement is largely consistent with the smaller interval sample. If they narrow substantially more than the random reference, playing-time selection is associated with the original interval breadth. **None** of these results alone tells us whether underlying player talent is assortatively assigned, whether congestion affects draft selection, or whether points per minute accurately measures talent.

## September 27 follow-up: correct the random comparison and add the sorting index

**Charles's instruction:** After reviewing SCOUT's first result with VECTOR, Charles requested that this memo direct SCOUT to make the statistical corrections identified in that review **and** calculate the overall sorting index ($H_{\mathrm{sort}}$) for the ten-highest-minute group and the random-ten groups. Treat this as **version two of the same 2015 diagnostic**, with new filenames and a new run record; preserve all version-one code, figures, tables, and prose as the historical first pass. Do not broaden the player population, rotation sizes, seasons, or scientific question.

### What the first pass established, and what needs repair

The version-one [report](../results/ASSORT_20260927_rotation_core_intervals_v1_report.md), [driver](../../code/ASSORT_20260927_rotation_core_intervals_v1.py), and [run record](../run_records/ASSORT_20260927_rotation_core_intervals_v1_run_record.json) use the accepted 4,267-player, 351-team source. Their saved hashes and the top-ten selections passed VECTOR's read-only checks. The top-ten group contains **3,501 players** and omits 766 from the *interval calculation*. Mean interval width is **3.280** using everyone and **2.855** using the ten highest-minute players. The figure still shows extensive central overlap. Original lower endpoints were omitted on **182** teams with more than ten players; upper endpoints on **30**. This asymmetry is about *observed points per minute*, not underlying talent.

Two statistical bookkeeping changes are needed before the three-case comparison is final:

1. **Use one random selection per team per repetition for every statistic.** Version one generated one set of random ten-player selections for widths and a separate set for coverage. Both obeyed the sampling rule, but a row of random widths and a coverage curve with the same repetition number did not describe the same players. In version two, construct the 100 team-wise random subsets once. From each *same* set of selected athlete identifiers, compute team endpoints, team widths, that repetition's coverage curve, and that repetition's overall sorting index. Save the selected identifiers or equivalent auditable membership data for every team and repetition. Use a recorded seed and deterministic team/athlete ordering. The version-two draws need not numerically match either independently generated version-one stream; do not present them as identical draws.
2. **Compare like with like when reporting scalar summaries.** Version one's reported random width **3.24** is the mean across teams of each team's *median* across draws. That is a legitimate but different statistic from an all-team mean width in one draw. VECTOR's read-only calculation from the saved version-one random-width table found that the **mean across the 100 draw-level, all-team mean widths was about 3.095** (individual draw means ranged approximately 3.042–3.140). The fixed high-minute mean was 2.855. Version two should make its headline three-way width comparison: all-team mean width for everyone; all-team mean width for the fixed top-ten group; and the **mean of the 100 all-team mean widths** for random ten. Save every draw-level mean. A mean of team-level random medians may appear as a separately labeled secondary statistic, but must not stand in for the draw-level aggregate.

Apply the same care to coverage. At each horizontal-axis location, a pointwise median over 100 coverage curves is appropriate for the **curve**; a scalar comparison of mean coverage should first average over the fixed grid *within each repetition*, then summarize those 100 repetition-level values. The mean over the grid of a pointwise-median curve is a different operation and must be labeled if shown. “Mean coverage” means mean over the **specified fixed grid**, not the number of teams at a typical basketball ability level. Maximum coverage may remain 351 even as interval widths narrow; report it without suggesting that unchanged maximum alone settles the question.

Keep the graphics and prose scientifically literal: say **observed standardized season points per minute**, **measured performance interval**, or **high-minute rotation interval**. Do not call the min–max range a latent “talent window,” its width an “ability spread,” or the ten-player mean the full team's $\hat T_j$. The saved variable name `ability_standardized` is a code field; its name does not validate points per minute as talent. State explicitly that many low-minute players remain in the underlying accepted player file and that playing time can itself be affected by coaching, role, and congestion.

### Calculate $H_{\mathrm{sort}}$ on exactly those same player groups

For any case with $N$ selected players on $J$ nonempty teams, compute **one overall index across all included teams and players**, not the mean of separate team indices:

$$
H_{\mathrm{sort}}
=1-\frac{\sum_{i\in Q}(a_i-\overline a_{g(i),Q})^2}
         {\sum_{i\in Q}(a_i-\overline a_Q)^2}.
$$

Here $Q$ is the case's selected player population, $a_i$ is the saved `ability_standardized` value, $g(i)$ is the unchanged team identifier, $\overline a_{g(i),Q}$ is the **unweighted mean of included players on that team**, and $\overline a_Q$ is the **unweighted mean of all included players**. Each included player contributes once regardless of minutes. Do not restandardize within a case, weight by minutes, average team-wise index values, or change team assignments. Validate that the denominator is positive and finite. The same index computed from the corresponding raw `points_per_minute` values should agree up to numerical precision because a common affine transformation leaves this index unchanged.

- **All eligible:** Recompute $H_{\mathrm{sort}}$ once from all 4,267 saved players as an integrity check. It should reproduce the accepted 2015 value of approximately **0.06194** in the [earlier sorting report](../results/ASSORT_20260927_sorting_sensitivity_v1_report.md). Explain any discrepancy before continuing.
- **Ten highest-minute players:** Compute and report one $H_{\mathrm{sort}}$ from the fixed 3,501-player selection on the same 351 teams. This is the numerical answer Charles requested for the high-minute group.
- **Random ten within each original team:** Compute one overall $H_{\mathrm{sort}}$ for each of the **same 100 random selections used for that repetition's widths and coverage**. Save all 100 values and report their mean, median, minimum, maximum, and central descriptive percentiles, plus the fixed top-ten value relative to them. There is no single intrinsic “random ten” value; its distribution depends on which ten players were selected on each team. These random draws keep players on their observed teams and are **not** a random-assignment null.

For a cross-check, calculate the index independently using the explicit sum-of-squares formula and the repository's `realized_sorting_index_H_sort` in `sports/541_grandchild_homophily_assign.py` or the `empirical_h_sort` routine in `sports/scripts/pd21_rho_hsort_calibrate.py`. Agree within numerical tolerance for the all-player case, fixed top-ten case, and at least several random repetitions; record which routine and tolerance were used. This is a mathematical validation, not a request to run the old plotting entry point or alter shared code.

**Keep the two kinds of reference distinct.** The 100 within-team random-ten selections show what happens when the *same observed rosters* supply equally many randomly chosen members instead of their highest-minute members. The random-**assignment** expectation holds a case's values and fixed team capacities but reallocates values across team slots. Its analytical expected index is $(J-1)/(N-1)$: approximately **0.0820** for 351 teams and 4,267 players, and exactly **0.1000** for 351 teams and 3,501 selected players. Report these expectations as **context for the change in sample size**, and optionally report each observed index minus its case's expectation. Do not call the within-team random-ten distribution an assignment null, reuse the earlier 3,928-player five-minute-group value as if it were the top-ten value, or claim a significance level from these 100 descriptive subset draws. No new random-assignment simulation is requested.

### Version-two output and acceptance checklist

Write a new isolated driver and version-two outputs under the existing `assort_analysis/code/`, `outputs/rotation_core_intervals_2015/`, `docs/results/`, and `docs/run_records/` directories. Use a clear `_v2` stem; **do not overwrite version one** or the accepted input. In addition to the earlier team and figure outputs, save a table of random-selected athlete identifiers by repetition and team (or an equivalently auditable membership record), a table with **one row per random repetition** giving its all-team mean width, mean coverage over the fixed grid, and overall $H_{\mathrm{sort}}$, and a comparison summary with the full and top-ten indices. Record output and code hashes, seed, software versions, and checks in the new run record.

Before reporting, verify the following in code and record the results:

1. Each random repetition has the same 351 teams, exactly $k_j=\min(10,|P_j|)$ **distinct** players from each original team, and therefore the same 3,501-player total and team-capacity vector as the fixed high-minute case. The selected identifiers used for width, coverage, and $H_{\mathrm{sort}}$ are identical *within* each repetition.
2. The full-case $H_{\mathrm{sort}}$ agrees with the accepted 2015 result; direct and repository implementations agree for the checked cases. Full, fixed top-ten, and random cases use the identical frozen player values and original team labels.
3. Every subset interval is contained in its team's full interval. Each repetition's coverage curve is at or below the all-player coverage curve at every fixed-grid point. The random coverage summaries and random width summaries are derived from their matching saved membership records.
4. The figure and report distinguish means of draw-level aggregate quantities from means of team-level medians; the text describes mean coverage as a grid average and avoids equating observed points per minute with latent talent.

Return a short narrative in this order: what was kept fixed; what version two corrected; the three interval results on a matched basis; the full, fixed top-ten, and random-ten sorting-index results; what those two comparisons jointly show about *measured points per minute*; and what remains unknown about underlying talent, assignment, and congestion. Stop after this bounded correction and extension. Do not fit a new model, change performance metrics or eligibility rules, draw draft-outcome curves, or begin new sweeps.

## Final editorial request after VECTOR's version-two review — no new analysis

Charles asked VECTOR to pass along the following small corrections to SCOUT before we leave this diagnostic. VECTOR's read-only verification found that the version-two code and saved outputs match their recorded hashes; all 100 saved random membership groups have 3,501 distinct players on the same 351 teams, and independently recomputed widths and sorting indices match the per-draw table. The substantive numerical findings stand. **Do not rerun the driver, create a third analysis version, change the random seed, or alter the figures or analytical tables for this request.**

1. In `docs/results/ASSORT_20260927_rotation_core_intervals_v2_report.md`, replace the sentence fragment saying random within-team tens are “mostly still below” the **0.1000 random-assignment expectation** with **“all 100 are below”**. The saved random-ten sorting-index range is approximately **0.06984–0.09359**, so none reaches 0.1000. Preserve the distinction: the 100 draws select players *within observed teams*; the 0.1000 value is the analytical expectation under a different operation, random *reassignment across teams* with the same 3,501-player size and team capacities. Neither comparison establishes a significance level or latent-talent sorting.
2. In the short message or summary Charles reads in Cursor, use plain-text **“sorting index (H_sort)”** in headings and table labels if Cursor displays literal dollar signs and LaTeX commands. Keep properly delimited LaTeX in the saved Markdown report where it renders for Charles's PDF workflow. This is a display fix, not a change to the mathematical definition or numeric values.

The version-two run record lists a hash and byte count for the report. **If the report text changes, update only that report entry's hash and byte count in the run record**, and add a dated note that the adjustment is editorial and that no analytical code or outputs were rerun. Leave the code and numerical-output hashes untouched. Return the corrected report path and a one-sentence confirmation of the editorial changes, then stop. Charles and VECTOR will move to the separate question of whether points per minute is an appropriate performance measure.
