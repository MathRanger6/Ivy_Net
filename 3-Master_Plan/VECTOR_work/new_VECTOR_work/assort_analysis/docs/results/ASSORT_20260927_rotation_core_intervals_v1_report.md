# High-minute rotation intervals vs all-eligible intervals (2015)

**Status:** Executed September 27, 2026 per [SCOUT mission](../scientific_questions/ASSORT_20260927_SCOUT_mission_high_minute_rotation_intervals.md). Internal integrity checks passed; Charles/VECTOR review pending.

## Answer in ordinary language

On the accepted **4,267-player / 351-team** 2015 file, team talent **windows** (min to max standardized season points per minute among eligible players) **still overlap heavily** under all three constructions. Restricting each interval to the **ten highest-minute players** **narrows** windows compared with the full eligible roster — **expected**, because subsets are nested inside the full interval.

The informative comparison is **high-minute vs random ten**. Mean interval width falls from **3.28** (all players) to **2.86** (high-minute) but only to **3.24** for the **median** of within-team random ten-player draws (100 draws, seed **20260927**). High-minute top ten capture a **median ~97.6%** of eligible captured minutes. So playing-time selection **is associated with narrower ability spread** on this axis — **more** than picking ten random eligible players — but **coverage curves remain broad** (mean coverage on the shared grid: **155** teams at a typical point for all-player vs **136** high-minute vs **147** random-median).

This is **descriptive** only. It does **not** establish latent talent assortativity, congestion in draft selection, or that omitted low-minute players lack talent.

## What was held fixed

- Input: [rotation audit players](../../outputs/rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_players.csv.gz) (SHA-256 verified against [audit run record](../run_records/ASSORT_20260927_rotation_audit_v1_run_record.json)).
- Saved `ability_standardized` and team assignments — **not** re-standardized.
- Same **351** teams in all cases; **315** teams with **>10** eligible players (**9** with 9 players → $k_j=9$, interval unchanged vs all).

## Headline numbers

| Quantity | All eligible | Top 10 minutes | Random 10 (median width per team) |
|----------|-------------:|---------------:|----------------------------------:|
| Mean interval width | 3.28 | 2.86 | 3.24 |
| Median width | 3.24 | 2.84 | 3.20 |
| Mean coverage on shared grid | 155.4 | 135.2 | 146.8 |
| Max coverage on grid | 351 | 351 | 351 |

**Extremes omitted from high-minute interval (among teams with >10 players):** original roster **min** ability player dropped on **182** teams; original **max** dropped on **30** teams — omission is **not** a statement about talent.

## Deviations from mission

None. Rotation size **10**, **100** random draws, tie-break **ascending athlete_id**, preselected panel team_ids at ranks `[0, 32, …, 350]` in all-player mean order (listed in [summary JSON](../../outputs/rotation_core_intervals_2015/ASSORT_20260927_rotation_core_intervals_v1_summary.json)).

## Artifacts

| Role | Path |
|------|------|
| Driver | [`code/ASSORT_20260927_rotation_core_intervals_v1.py`](../../code/ASSORT_20260927_rotation_core_intervals_v1.py) |
| Figure | [`outputs/rotation_core_intervals_2015/ASSORT_20260927_rotation_core_intervals_v1_comparison.png`](../../outputs/rotation_core_intervals_2015/ASSORT_20260927_rotation_core_intervals_v1_comparison.png) |
| Team table | [`..._teams.csv`](../../outputs/rotation_core_intervals_2015/ASSORT_20260927_rotation_core_intervals_v1_teams.csv) |
| Player selections | [`..._player_selections.csv`](../../outputs/rotation_core_intervals_2015/ASSORT_20260927_rotation_core_intervals_v1_player_selections.csv) |
| Coverage grid | [`..._coverage_grid.csv`](../../outputs/rotation_core_intervals_2015/ASSORT_20260927_rotation_core_intervals_v1_coverage_grid.csv) |
| Random widths | [`..._random_draw_team_widths.csv`](../../outputs/rotation_core_intervals_2015/ASSORT_20260927_rotation_core_intervals_v1_random_draw_team_widths.csv) |
| Summary JSON | [`..._summary.json`](../../outputs/rotation_core_intervals_2015/ASSORT_20260927_rotation_core_intervals_v1_summary.json) |
| Run record | [`docs/run_records/ASSORT_20260927_rotation_core_intervals_v1_run_record.json`](../run_records/ASSORT_20260927_rotation_core_intervals_v1_run_record.json) |

## What this test does not establish

- Whether rosters are assortatively assigned in latent talent.
- Whether congestion changes draft winners.
- Whether points per minute equals talent.
- Whether a different rotation size (8, 5, …) would tell a different story — not run in this pass.
