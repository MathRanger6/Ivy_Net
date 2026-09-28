# Return to the assortativity question: a bounded experiment brief

**Date:** September 27, 2026  
**Status:** Recovered decisions and proposed first stage. Documentation only; no experiment executed or newly authorized by this brief.


## Revised proposal after Charles's selection-rate and season questions

**This section replaces the proposed one-season, 1% first stage below.** Earlier text is retained as proposal history, not current execution instructions. No revised experiment is authorized or executed.

The reigning data-story manifest reports 615 ever-drafted athletes among 22,795 last-ps observations: approximately 2.698%. Charles's recollection of 2.7% is correct for that historical population. The completed audit diagnostic instead counted 45 annual draftees among 4,267 players (approximately 1.055%), or 105 ever-drafted players in the same single-season roster (approximately 2.461%). These are different outcomes and denominators. The historical calibration's 1,133 positive player-season labels among 46,306 rows is another quantity, not a unique-career count. Sources are the reigning data-story manifest, calibration JSON, and saved empirical-selection summary.

Recommend a fixed **2.7% selection scenario**, explicitly motivated by the reigning career-outcome proportion. Applying this rate to all players in each simulated season does not reproduce a last-ps population or assert that 2.7% actually enter the draft each year. It provides one shared scarcity setting for the controlled mechanism comparison.

Recommend **2014, 2015, and 2016 as three separate season experiments**, chosen in advance around the already audited 2015 anchor, conditional on source coverage and bounded quality checks. Do not pool their rosters into one artificial season. Preserve each season's population and capacities across its own four assignment/scoring cases. Use 100 paired repetitions per season. The same athlete can appear in multiple seasons; these are not three independent samples of careers.

One season can support a conditional mechanism result. Repeating its simulated assignments reduces uncertainty about that simulation, not uncertainty about whether other real seasons behave similarly. Additional seasons test stability across populations; they do not automatically create statistical significance. Tail events can remain sparse. No claim about statistical power is established by choosing three seasons.

Retain the four cases, raw congestion, assignment preference zero/one, and congestion weight zero/one. Use each season's standardized PPM and 99th ability percentile as its fixed viability threshold, with sharpness ten. The threshold is separate from the 2.7% selection budget; do not silently move it to the 97.3rd percentile. Select the nearest integer to 0.027 times that season's N under the recorded rounding rule (115 for the accepted 2015 N of 4,267).

Report each season separately: congestion-induced winner changes, measured sorting, and descriptive selection-rate curves with congestion off/on. Assess recurrence across assignments and seasons; do not treat repetitions or repeated athlete-seasons as independent empirical evidence. A formal downturn test would require a separately specified criterion; the current proposal remains descriptive.

Before requesting execution, inspect 2014 and 2016 source availability and construction compatibility read-only. The 2015 canonical-team correction is not automatically valid for genuine transfers or anomalies in other seasons. Report any substantive data decision rather than opening a general source-cleaning project. This availability/compatibility check is the immediate next preparatory step, not permission to rebuild data or run simulations.

**Primary source:** 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/data_story/mbb_reigning_3x3_manifest.json, cohort panel (615 / 22,795). Historical counts were inspected in the manifest, not independently reconstructed this turn.

## Our question

Can congestion produce a downturn in selection rates when assignment has no preference for grouping similar-ability players? Does preferential grouping strengthen or change that pattern?

Keep three tasks separate: this mechanism question is primary; performance measures and player-pool sensitivity are supporting measurement work; matching individual draftees is a separate diagnostic. Charles needs to understand and explain the next step before execution. Interesting side findings do not automatically expand this task.

## What we already decided

The September 25 decision record specified the same 2015 players and observed roster capacities across simulated conditions; points per minute standardized once; 100 paired repetitions; assignment preference zero versus one; congestion weight zero versus one; and deterministic selection of exactly the highest K scores without clipping or post-score randomness.

It also specified two selection fractions, 1% and 10%, and two congestion representations, raw and standardized against one fixed observed-roster reference. The viability threshold is the frozen ability distribution's 99th percentile, and the transition sharpness is 10. These are declared scenario choices, not the fitted parameters used in the recent draft-identity diagnostic.

The original primary outcome was changes in the selected people. A sixteen-bin outcome display was secondary. Changing winners alone does not establish a downturn. The old plan explicitly did not fit a quadratic or formally classify an inverted-U. We must preserve that limit rather than silently promote the old design into a definitive necessity test.

## The proposed first stage: four cases

To reduce scope, I recommend starting with the previously chosen 1% selection fraction and raw congestion. Keep the 10% and fixed-reference-standardized versions documented but parked. This staging is a new recommendation requiring Charles's agreement; it does not erase the earlier choices.

For each of 100 paired repetitions, construct two assignments with the same players, capacities, arrival order, and coupled random draws:

1. Assignment without similarity preference; score by ability alone.
2. The same no-preference assignment; score by ability minus congestion.
3. Assignment with similarity preference; score by ability alone.
4. The same preference assignment; score by ability minus congestion.

Without similarity preference, each remaining seat has equal assignment probability. Teams with more vacant seats therefore have a greater chance of receiving a player. With preference, similarity to current teammates affects assignment. Measure the resulting sorting in both conditions: zero preference does not guarantee exactly zero measured sorting.

The two congestion-off cases are essential controls. An apparent curve could reflect how people are grouped even before congestion changes anybody's score. Ability-only winners must be identical across assignments, although their peer environments can differ.

## Population and fixed ingredients

The later source-audited population contains 4,267 players on 351 teams, replacing the provisional counts in the September 25 construction document. The audit resolved canonical teams using positive verified playing appearances, then minutes, and incorporated documented source recoveries and exclusions. The old games-first construction must not be restarted unchanged.

Proposed input: the newly built, accepted rotation-audit population, with provenance checks. It is an input prepared during this investigation, not an old sweep. All eligible players remain in assignment and peer measurement; no top-ten or five-minute restriction is introduced. At 1%, the accepted nearest-integer rule yields 43 selections.

Use full-team smooth congestion including the focal player, fixed ability scores, the same congestion formula, and the same selection rule throughout. Raw score is ability minus congestion when congestion is enabled. This first stage does not use the recent fitted gamma, lambda, or temperature.

These are hypothetical selections among a fixed population. Draft labels are not used to choose simulated winners. Last-ps versus all-ps becomes essential for an empirical HERO comparison, which this stage does not attempt.

## What we will look at

Report how many winners change when congestion is switched on, separately for each assignment rule. Also display selection rates against leave-one-out teammate ability with congestion on and off, using the previously specified sixteen approximately equal-count bins and assignment-to-assignment variation.

The bins describe relative peer-quality positions and may span different numerical ranges between assignments. Show the actual peer-quality coordinates. This is not the reigning equal-width empirical HERO.

A downturn appearing without similarity preference, absent from its congestion-off control and recurring across assignments, would be evidence against requiring preferential assignment in this tested setting. A stronger downturn with preference would support a shaping role.

A downturn appearing only with preference would support a conditional role for preference in this comparison, not universal necessity. No clear downturn would mean these settings have not demonstrated the phenomenon. Raw congestion might be weak relative to ability; that result alone would not eliminate the mechanism.

The current display permits descriptive assessment, not a formal inverted-U verdict. We should not search bin counts or fit curves after looking at results to manufacture a desired shape. If a formal shape conclusion becomes necessary, define its criterion before a separately authorized analysis.

## Stop and interpret

Do not add another performance metric, filter, fitted-parameter replay, new season, or parameter sweep to this first stage. After the four-case results, stop and explain what changed, what did not, and what remains unknown. Charles decides whether a parked comparison is needed.

The immediate decision is whether to accept this reduced first stage. After agreement, present the concrete implementation/run scope before execution. Existing authorization for the completed draft-identity diagnostic is not authorization for this experiment.

## Source trail

Paths below are relative to assort_analysis/.

- Original decisions: docs/decisions/ASSORT_20260925_experiment_choices_and_rationale.md
- Original implementation specification: docs/decisions/ASSORT_20260925_construction_specification_and_source_audit.md
- Historical stop: docs/source_review/ASSORT_20260925_initial_execution_stop.md
- Later accepted population and source corrections: docs/results/ASSORT_20260927_rotation_audit_v1_report.md
- Population artifact: outputs/rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_players.csv.gz
- Population execution record: docs/run_records/ASSORT_20260927_rotation_audit_v1_run_record.json
- Separate draft-identity diagnostic: docs/results/ASSORT_20260927_empirical_selection_replay_v1_report.md
- SCOUT's population review, with specific points challenged in our discussion: docs/source_review/ASSORT_20260927_SCOUT_response_selection_population_and_reigning_alignment.md

This brief recovers documented decisions and proposes staging. It does not independently reproduce earlier numerical results.
