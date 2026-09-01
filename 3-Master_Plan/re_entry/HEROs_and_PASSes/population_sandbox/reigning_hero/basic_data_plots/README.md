# Reigning hero — basic data plots (porch)

Diagnostics for the **slide 12** population. Lock: [`../README.md`](../README.md).

## Build

```bash
# repo root
python sports/scripts/reigning_hero_basic_plots.py

# or
zsh 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/reigning_hero/reigning_hero_basic_plots.zsh
```

Subset: `--only overlap ai_tj ai_loo tj_loo hsort_dist ability_residuals draft_rate team_games minutes team_size`

## Slides (auto deck)

After plots are built:

```bash
python sports/scripts/build_reigning_hero_basic_plots_slides.py
# or
zsh 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/reigning_hero/reigning_hero_basic_plots_slides.zsh
```

Outputs:

- `REIGNING_BDP_slides_AUTO.pptx` — intro + 18 porch plots (see `REIGNING_BDP_slides_summary.md`)
- `REIGNING_BDP_slides_summary.md` — slide index table
- `manifest.json` — plot keys, slide_index, PNG presence

## Outputs (Aug 2026)

| # | Plot | File stem | Rows |
|---|------|-----------|------|
| 1 | Interval overlap 09–21 | `REIGNING_team_interval_overlap_mg10_min20_09_21` | all-ps |
| 2 | Â_i \| T̂_j | `REIGNING_BDP_Ai_Tj_mg10_min20_09_21_ppm_lastps` | last-ps |
| 3 | Â_i \| poolq_loo | `REIGNING_BDP_Ai_poolq_loo_mg10_min20_09_21_ppm_lastps` | last-ps |
| 3b | **T̂_j vs poolq_loo overlay** | `REIGNING_BDP_Tj_vs_poolq_loo_mg10_min20_09_21_ppm_lastps` | last-ps |
| 4 | APGMS + ARGMS draft rate | `REIGNING_BDP_draft_rate_{APGMS,ARGMS}_mg10_min20_09_21` | ALLT + orange +DFT |
| 5 | **Team games per season** | `REIGNING_BDP_team_games_mg10_min20_09_21` | team-season (box, after QC) |
| 5b | **Player + team mean minutes** | `REIGNING_BDP_minutes_player_team_mg10_min20_09_21` | all-ps |
| 6 | Team roster size | `REIGNING_BDP_team_size_mg10_min20_09_21` | all-ps |

Lock: mg10 · min20 · 09_21 · ALLT · winsor 0.01–0.99 (poolq_loo plot only).

## Naming

Prefix `REIGNING_` — not `FIXED_HERO`.
