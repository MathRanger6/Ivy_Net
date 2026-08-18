# PD22 — Minutes filter & panel policy

Alex (Aug 17 2026): justify playing-time floor and panel policy (drop vs PPM-zero) before defending ρ calibration.

**Todo list:** [`PD22_minutes_panel_investigation_todo.md`](PD22_minutes_panel_investigation_todo.md)

**Box QC policy (dash `"-"` drop + min 11 games/team-season; default `min_team_season_games=10`):** [`BOX_QC_panel_build_policy.md`](BOX_QC_panel_build_policy.md)

## Item 1 — Drafted-player retention audit

```bash
# Full audit (panel rebuild + CSV + JSON + PNG) — ~few min
python sports/scripts/pd22_drafted_minutes_audit.py

# Custom threshold ladder
python sports/scripts/pd22_drafted_minutes_audit.py --thresholds 0 5 10 15 20

# Regenerate figure only (after CSV exists)
python sports/scripts/pd22_drafted_minutes_audit.py --plot-only
```

**Outputs**

| File | Content |
|------|---------|
| `PD22_drafted_minutes_audit_2011_2021.csv` | All `Y_draft=1` player-seasons, sorted by minutes |
| `PD22_drafted_minutes_threshold_table_2011_2021.csv` | Retained/lost counts vs floor |
| `PD22_drafted_minutes_audit_2011_2021.json` | Summary + artifact paths |
| `PD22_drafted_minutes_audit_2011_2021.png` | Empirical cumulative distribution function (ECDF) + retention curve |

## AUTO slide (item 1)

```bash
# Audit + slide
python sports/scripts/build_pd22_drafted_minutes_audit_slide.py

# Slide only (after audit artifacts exist)
python sports/scripts/build_pd22_drafted_minutes_audit_slide.py --slides-only
```

Writes `slides/auto/CHAR_PD22_drafted_minutes_audit_AUTO.pptx` — copy into HAND (Change Picture + bullets).

## Item 2 — Raw panel minutes distribution

```bash
# Full run (panel rebuild + CSV + JSON + PNG) — ~few min
python sports/scripts/pd22_raw_minutes_distribution.py

# Regenerate figure only (after CSV exists)
python sports/scripts/pd22_raw_minutes_distribution.py --plot-only
```

**Outputs**

| File | Content |
|------|---------|
| `PD22_raw_minutes_distribution_2011_2021.csv` | `minutes`, `Y_draft` for every player-season |
| `PD22_raw_minutes_distribution_2011_2021.json` | Summary percentiles + below-floor shares |
| `PD22_raw_minutes_distribution_2011_2021.png` | ECDF (all vs ever-draft) + low-minute histogram |

## AUTO slide (item 2)

```bash
# Distribution + slide
python sports/scripts/build_pd22_raw_minutes_distribution_slide.py

# Slide only (after artifacts exist)
python sports/scripts/build_pd22_raw_minutes_distribution_slide.py --slides-only
```

Writes `slides/auto/CHAR_PD22_raw_minutes_distribution_AUTO.pptx` — copy into HAND (Change Picture + bullets).

## Items 3–4 — PPM distribution (filtered-out vs hero ASSIGN input)

```bash
# Full run (two panel rebuilds + CSV + JSON + PNG) — ~few min
python sports/scripts/pd22_ppm_distribution.py

# Regenerate figure only (after CSV exists)
python sports/scripts/pd22_ppm_distribution.py --plot-only
```

**Outputs**

| File | Content |
|------|---------|
| `PD22_ppm_distribution_2011_2021.csv` | `role` = filtered_out / hero_raw / hero_assign |
| `PD22_ppm_distribution_2011_2021.json` | Summary + panel spec |
| `PD22_ppm_distribution_2011_2021.png` | Left: sub-20-min raw PPM; right: hero raw PPM + ASSIGN z |
| `PD22_ppm_full_vs_filtered_2011_2021.png` | Overlay: full-panel vs sub-20-min raw PPM (same bins, log *y*) |

## Raw panel roster size (min=0 vs min-20 drop)

**Before box QC (motivation — BYU tail, dash placeholders):**

```bash
python sports/scripts/pd22_raw_roster_size_distribution.py --before-qc-only
python sports/scripts/build_pd22_raw_roster_size_before_qc_slide.py
python sports/scripts/build_pd22_raw_roster_size_before_qc_slide.py --slides-only
```

| File | Content |
|------|---------|
| `PD22_raw_roster_size_distribution_before_qc_2011_2021.png` | Legacy raw box (QC off) vs min-20 drop |
| `PD22_raw_roster_size_by_team_season_*_before_qc_raw.csv` | Per team-season counts (includes 115 BYU spike) |

**After box QC (post-filter panel):**

```bash
python sports/scripts/pd22_raw_roster_size_distribution.py --after-qc-only
python sports/scripts/build_pd22_raw_roster_size_after_qc_slide.py --slides-only
```

| File | Content |
|------|---------|
| `PD22_raw_roster_size_distribution_after_qc_2011_2021.png` | Box-QC panel (min=0) vs min-20 drop |
| `PD22_raw_roster_size_by_team_season_*_after_qc_raw.csv` | Per team-season counts after dash + min-games filters |

AUTO decks: `slides/auto/CHAR_PD22_raw_roster_size_distribution_before_qc_AUTO.pptx` (HAND first), then `_after_qc_AUTO.pptx`.

**Note:** “Empirical roster caps” (team-size multiset) are separate from this figure. Item 4 right = raw PPM vs **PPM z within season** on the min-20 hero panel (PD21 ASSIGN ability input).

## AUTO slide (items 3–4)

```bash
python sports/scripts/build_pd22_ppm_distribution_slide.py
python sports/scripts/build_pd22_ppm_distribution_slide.py --slides-only
```

Writes `slides/auto/CHAR_PD22_ppm_distribution_AUTO.pptx` — copy into HAND (Change Picture + bullets).

## AUTO slide (PPM overlay — full vs sub-20)

```bash
python sports/scripts/build_pd22_ppm_full_vs_filtered_slide.py --slides-only
python sports/scripts/build_pd22_ppm_full_vs_filtered_slide.py --plot-only
python sports/scripts/build_pd22_ppm_full_vs_filtered_slide.py
```

Writes `slides/auto/CHAR_PD22_ppm_full_vs_filtered_AUTO.pptx`.

## AUTO slide (raw roster size — backup)

See **Raw panel roster size** above for before/after QC commands. Legacy alias `build_pd22_raw_roster_size_slide.py` → after-QC deck.

## AUTO slide (team-season games count — backup)

**Raw box (motivation — before filter):**

```bash
python sports/scripts/build_pd22_team_season_games_count_slide.py --slides-only
```

**Figure:** `PD22_team_season_games_count_2011_2021.png` → `slides/auto/CHAR_PD22_team_season_games_count_AUTO.pptx`

**After box QC (post-filter — pairs with roster/minutes diagnostics):**

```bash
python sports/scripts/pd22_team_season_games_count.py --after-qc-only
python sports/scripts/build_pd22_team_season_games_count_after_qc_slide.py --slides-only
```

**Figure:** `PD22_team_season_games_count_after_qc_2011_2021.png` → `slides/auto/CHAR_PD22_team_season_games_count_after_qc_AUTO.pptx`

Regenerate both histograms: `python sports/scripts/pd22_team_season_games_count.py`
