# ASSORT — Initial execution stop and source-data findings

**Last synced:** 2026-09-25  
**Status:** Construction attempted; experiment not run. Scientific choices pending.

The first implementation attempt read the frozen 2015 game file and stopped during population construction. It made no changes to the source file or shared repository code. The new driver and all diagnostic files are confined to this investigation workspace.

## What the source checks established

- The 2015 source has 182,657 game-level rows. Seven rows have no athlete identifier, name, minutes, or points; the established panel builder also drops rows without an athlete identifier.
- After the eleven-captured-game coverage rule, 351 teams remain.
- The source contains expected no-play roster records with both minutes and points missing. After coverage and canonical-team filtering, 58,624 such records remain. They are flagged as not played and contribute nothing to either season total. The first failed audit treated them as anomalies; that audit was superseded and moved to `archive/`.
- There are 105 retained rows with minutes missing while points are recorded. One hundred otherwise eligible athletes are affected, across ten teams and six games. Those 100 source rows contain 757 recorded points. The current shared panel builder sums the points and skips missing minutes. That behavior could raise their calculated points-per-minute ability. The driver stops and preserves row-level and athlete-level audits rather than adopting that behavior silently.
- The agreed games-first canonical-team rule produces 4,263 eligible athletes, three fewer than the earlier 4,266 target. Sherron Dorsey-Walker has 13 Iowa State captured records and 39 minutes, versus 18 Oakland no-play records; Deonte Burton has 16 Marquette records and 129 minutes, versus 21 Iowa State no-play records; Semi Ojeleye has nine Duke records and 63 minutes, versus 14 SMU no-play records. Games-first assigns each to the zero-minute destination and then excludes them at the twenty-minute floor. Their records look consistent with transfers or changes in roster listing, but this audit does not establish transfer dates.

## Choices to settle one at a time

1. Whether canonical team should continue to prioritize all captured roster records, including no-play records, or prioritize games with positive recorded minutes before using total minutes. The latter would retain the three athletes on their observed playing teams and appears consistent with the original target of 4,266. This is a proposed correction, not an adopted decision.
2. How to treat a game row with recorded points and missing minutes. The cleanest narrow option is to exclude that entire game row from the points-per-minute numerator and denominator while retaining its game identifier for team-season coverage, then recompute eligibility and ability. Other choices include recovering the minutes from a reliable source or retaining the historical sum behavior with its stated bias. No option has been selected.

The canonical-team decision comes first because it determines the eligible population. The partial-stat decision follows. After both are settled, construction must rerun, verify the population and capacities, and only then begin the 100 paired assignment repetitions.

## Diagnostics

- `data/ASSORT_20260925_v1_canonical_team_audit.csv`
- `data/ASSORT_20260925_v1_partial_stat_rows.csv`
- `data/ASSORT_20260925_v1_eligible_partial_stat_athletes.csv`
- `data/ASSORT_20260925_v1_population_audit_needs_review.json`

The 100 paired repetitions have **not** run, and no experimental result is available.

