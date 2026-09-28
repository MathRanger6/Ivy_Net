# Three-season mechanism experiment: source check and one decision

**Date:** September 27, 2026  
**Status:** Source preflight executed; simulations not started. Charles authorized the revised experiment, subject to the source-quality gate in the brief.

## Where we are and why this step was necessary

Our question remains whether a downturn can appear without preference for similar teammates, and whether that preference strengthens it. We proposed three separate seasons so the answer would not depend entirely on the 2015 player population.

First we checked whether 2014 and 2016 can support that comparison. Both have 351 teams with at least eleven captured games. That supports availability, but it does not prove that every team's official schedule is complete or every statistic is valid.

The check also found rows with points but no usable minutes. If we simply added those points to a season total without adding the missing minutes, we could exaggerate a player's points per minute (PPM). We therefore stopped before constructing final populations or running assignment simulations.

## What the source check found

In 2014:

- 182,737 source rows were read.
- 351 teams passed the captured-game coverage screen.
- 66 retained rows have recorded points and missing minutes, concentrated in four games.
- Another 45 retained rows have positive points and zero minutes.
- These 111 point/minute problem rows contain 736 recorded points. This is about 0.061% of all source rows for the season; it is not the fraction of players affected.
- Two additional rows describe J-Mychal Reese on both teams in the same game, each with 16 minutes and 10 points. He has six positive-minute appearances and 96 recorded minutes on team 245, versus one positive-minute appearance and 16 minutes on team 248. This is consistent with a copied opposing-team row rather than evidence of two distinct playing careers. That interpretation is based on internal source records, not external box-score verification.

In 2016:

- 182,524 source rows were read.
- 351 teams passed the captured-game coverage screen.
- 56 retained rows have recorded points and missing minutes, concentrated in three games.
- Another 44 retained rows have positive points and zero minutes.
- These 100 point/minute problem rows contain 518 recorded points, about 0.055% of all source rows for the season.
- No same-game cross-team player duplicates were found.

Across all flags, including the copied 2014 row, 104 athletes in 2014 and 87 in 2016 have flagged records on player-team pairs with at least twenty recorded minutes. These are provisional impact counts, before source treatment and canonical-team construction. The corresponding preliminary player-team counts are 4,248 and 4,234. They are not accepted final athlete populations. A small row fraction can still affect many individual season rates.

Expected no-play records with both points and minutes blank were distinguished from partial statistics. No unexpected double-blank records, negative/nonfinite numeric statistics, or same-team duplicate player-game keys were found after the coverage screen. The 81 entirely blank athlete-identity rows in 2014 were counted separately. No nonblank malformed identity rows were found.

## Recommendation: one bounded source decision

Extend the already accepted source fallback to these two new working copies:

1. Retain any already verified source corrections if applicable; do not invent missing minutes.
2. Where points are present but minutes are missing or zero and no verified correction is available, omit both statistics from season totals.
3. Preserve that game identifier for team coverage, and keep every omitted source-row identifier and original value in the audit.
4. Use the documented positive-played-games, then total-minutes canonical-team ordering. For the identified 2014 duplicate, this retains team 245; stop on any remaining unresolved tie or evidence of genuinely ambiguous played-team membership.
5. Recompute the twenty-minute eligibility floor and final PPM after treatment; then report the final number of athletes affected and any eligibility changes.

This recommendation avoids silently treating an invalid denominator as valid. It can still omit genuine playing time; it is a declared limitation, not a reconstruction of the missing facts. The independently recovered 2015 values remain in its accepted input. No broad new source-recovery campaign is proposed.

The brief required a pause for a substantive source decision. Charles's execution authorization did not itself choose how to handle these newly discovered rows. The immediate question is whether to extend this bounded fallback. No assignment or scoring experiment should run until it is settled.

## What will follow after that decision

Prepare each season separately with its own population and team capacities. Select approximately 2.7% under the same four assignment/scoring cases, with 100 paired repetitions per season. Keep the previously specified threshold, sharpness, and raw congestion unchanged. We will describe this as a mechanism experiment using a common scarcity scenario, not an annual draft prediction or a reproduced last-ps HERO.

Then report what congestion changes within each assignment condition and whether the descriptive curve pattern recurs across seasons. Changes in selected people alone are not proof of a downturn, and simulation repetitions are not new observed college careers.

## Files and checks

All paths below are relative to assort_analysis/.

- Source-check driver: code/three_season_mechanism_v1/ASSORT_20260927_three_season_preflight_v1.py
- Source-check execution record: docs/run_records/ASSORT_20260927_three_season_mechanism_v1_preflight.json
- Row-level flags, identity diagnostics, and multi-team candidates: data/three_season_mechanism_v1/preflight/
- Governing proposed design: docs/decisions/ASSORT_20260927_return_to_assortativity_brief.md

The source check recorded the raw-file hash before and after; they matched. The execution record records the driver hash, library versions, and hashes for all eight CSV audit artifacts. Outputs are isolated from previous work. No raw source, prior simulation, or historical figure was changed. The numerical simulation has not started.

