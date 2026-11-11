# Request to SCOUT: recover the basketball data lessons before we rediscover them

**Last synced:** 2026-10-27  
**From:** Charles and his manuscript/Jazz night collaborator  
**To:** SCOUT  
**Status:** Request prepared for Charles to hand off; awaiting a new response.

## What Charles needs

We are rebuilding a clear empirical starting point for the manuscript, and Charles wants us to benefit from everything you already learned together. Please recover the data lessons, the decisions made in response, their reasoning, and which outputs actually implement those decisions. We particularly need the history of fragmentary one-game team-seasons and players appearing under multiple teams. Please do not treat this as a fresh exploratory sweep.

Please write a self-contained response in the same directory as this request, named `20261027_SCOUT_Response_MBB_Lessons_for_Jazz_Night.md`. Use headings and plain explanations, with exact repository paths and relevant functions or configuration settings to substantiate decisions. Distinguish Charles-approved decisions, implemented defaults, exploratory alternatives, superseded choices, and unresolved questions. If this request's description is wrong, correct it explicitly.

## The work we are doing now

The current question is the empirical naïve plot: own performance versus the observed proportion labeled ever drafted. This is not a congestion-axis HERO plot or a fitted model. We are deliberately pausing before choosing further filters or model extensions.

Products are under `3-Master_Plan/re_entry/jazz_night/`. The chronological walkthrough is being assembled as `Jazz_Night_Experimental_Walkthrough.md` there. The separate manuscript outline is `3-Master_Plan/re_entry/Jazz_night.md`.

The current settings are 2011–2021; all colleges; MG10 interpreted as more than 10 captured team-season games; at least 20 total recorded season minutes; PPM standardized within season on the eligible full roster; eight equal-width and eight equal-count quantile bins. Performance values are not clipped in these own-performance plots. Final-PS is the existing one-final-observed-record-per-player subset. We then added an all-PS comparison using the same frozen roster snapshot, without silently changing its records or labels.

The immediate sources are `3-Master_Plan/VECTOR_work/new_VECTOR_work/manuscript_figures/section_4_5/roster_pressure_comparison/cache/all.pkl`, `last.pkl`, and `source_manifest.json`. Source hashes match that manifest. This verifies snapshot identity, not completeness of all historical cleaning decisions.

Current 2011–2021 PPM totals:

- Final-PS: 19,803 records and unique players; 520 ever-drafted labels.
- All-PS: 46,306 athlete/team/season records, 46,233 unique athlete/seasons, the same 19,803 players, and 1,133 positive records belonging to the same 520 ever-drafted players.
- Seventy-three athlete/seasons, involving 71 players, have two team records. These were retained and explicitly flagged, not presumed genuine transfers or removed. The exact rows are in `3-Master_Plan/re_entry/jazz_night/03_ppm_all_vs_final_ps/multi_team_player_seasons_audit.csv`.
- PPM final-PS bin counts/rates match the preceding Jazz night output exactly. All-PS repeats each player's ever-drafted label across retained records; it does not measure annual draft events.

## Earlier records we have already located

Please build on these rather than making Charles repeat their history:

1. `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260925_SCOUT_response_data_hygiene_and_model_history.md`.
2. `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260927_SCOUT_response_selection_population_and_reigning_alignment.md`.
3. `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260927_SCOUT_response_performance_metric_provenance.md`.
4. `3-Master_Plan/re_entry/SCOUT_and_COMPASS/SCOUT_and_COMPASS_Q_and_A.md` and the box-quality policy it cites.

The September 25 response already records the progression from no team coverage filter to MG5 and then MG10, production exclusion of sub-20-minute records rather than setting their PPM to zero, derivation of PPM after box filtering, and differences between the cleaned HERO and older curves. The September 27 response warns that the ASSORT canonical-team audit population is not identical to the HERO pipeline population. What we need now is the consolidated history plus an explicit assessment of which rules apply to the current Jazz night sources.

## 1. One-game and partial-season records

What precisely was wrong: a player's one-game contribution on a valid full team-season, a team's entire season represented by one captured game, placeholder rows, or some combination? Explain the examples that led to the discovery, the adopted remedy, and any known residual problems. Confirm the exact MG10 rule, its position in the build sequence, and why a 20-minute minimum alone did not solve the issue.

Which counts and figure changes demonstrated that the remedy worked? Which older plots became inappropriate evidence after cleaning? Please keep claims about particular HERO tails attached to their exact cohort and axis; do not generalize them to every band or the current own-performance plots.

## 2. Players appearing under multiple teams

What decisions did Charles make about genuine multi-team seasons, identity collisions, erroneous team assignments, duplicate game records, and transfers across different seasons? Was a canonical team selected by minutes or another rule, were records merged or dropped, or were team spells retained? Identify deterministic tie-breaking rules and whether they apply before or after the season, minutes, or team-coverage filters.

Crucially: was a rule adopted only for the ASSORT audit or also for production HERO/BOE analysis? Does last-PS choose the largest-minute team in the latest season, the last sorted row, or something else? Which implementation is authoritative now?

Please assess the 73 current two-team athlete/seasons against that history. Are we intentionally preserving the HERO definition, or missing an approved correction? A rule existing elsewhere in the repository is not sufficient evidence that it has been applied to these pickle snapshots. Do not silently change those sources.

## 3. Performance, minutes, standardization, and missingness

Summarize decisions about total season minutes versus minutes per game; a minimum number of player appearances versus captured team games; dropping low-minute records versus zeroing their PPM; and ratio-of-season-totals PPM versus averages of game ratios. Identify the order of quality filters, aggregation, PPM calculation, standardization, and peer-measure calculation.

What did earlier comparisons establish about PPM, BPM and related measures, and what remained unresolved? Include extreme small-minute values, Sports-Reference matching coverage, missing final-row metrics, and whether clipping/winsorization affected performance, the peer axis, or display only. Please distinguish a choice made for data validity from one made because a curve looked preferable.

## 4. Candidate populations and outcome timing

Recover the rationale for all-PS versus last/final-PS, all colleges versus draftee colleges, 2009 versus 2011 starts, and one focal record versus a full roster for environment calculations. Clarify window-end censoring and how ties within the final season are handled.

Explain ever-drafted versus season-specific labels, repeated positive records, draft matching gaps, and why a pooled ever-drafted proportion is not automatically the annual K/N. Which empirical own-performance, HERO and BOE comparisons were intended to share populations, and which deliberately did not?

## 5. What we can safely reuse

Please provide a compact list of the authoritative sources, cleaned panels, configurations and plotting entry points. Identify obsolete exports, caches, misleading filenames or stale documentation that can recreate an old problem. A file named “reigning” or “cleaned” is not enough; tell us its scope and lineage.

For each important lesson, give: what we discovered; what was decided and why; where it is implemented; evidence that it was applied; exceptions; and whether our present Jazz night source follows it. Please include other material data lessons beyond the examples above. If evidence is missing, label that gap rather than reconstructing an undocumented decision as fact.

## Requested conclusion

End with three short lists: **settled decisions to carry forward**, **current-source discrepancies requiring attention**, and **genuinely open choices for Charles**. Recommend the smallest necessary reconciliation before further plotting. We are not asking for new sweeps, a population replacement, manuscript edits, or a search for settings that produce a downturn.
