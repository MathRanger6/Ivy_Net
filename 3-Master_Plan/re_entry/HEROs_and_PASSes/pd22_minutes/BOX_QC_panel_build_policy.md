# Box QC at panel build — policy, implementation, and regeneration guide

**Date:** 2026-08-17  
**Audience:** Charles, SCOUT, future you  
**Status:** Step 1 of rollout **implemented** (see §8 checklist)

> **COMPASS handoff:** Everything Charles needs to tell COMPASS lives in one place:  
> [`3-Master_Plan/20260817_1650_SCOUT_to_COMPASS_box_qc_rollout_and_regen.md`](../../../20260817_1650_SCOUT_to_COMPASS_box_qc_rollout_and_regen.md)  
> This file is a technical mirror / maintainer copy; update both if policy changes.

---

## 1. Why this document exists

Charles and SCOUT traced two ESPN box-data problems while preparing **PD22** (Alex meeting — justify `min_minutes = 20`):

| Problem | Symptom | Example |
|---------|---------|---------|
| **Dash placeholders** | `athlete_display_name == "-"` | BYU 2018: 99 fake rows, one game → roster_n 115 |
| **Fragmentary coverage** | Small schools with ≤5 games in box | Webber Int 2014: 1 game, 52 listed players; 1,883 team-seasons have exactly 1 game |

Draft matching and `college_aliases` did **not** cause these. They originate in **Stage 1 box data** (`datasets/mbb/mbb_df_player_box.csv`).

**Decision (2026-08-17):** Apply hygiene **upstream at panel build**, not by editing the frozen CSV. Defaults ON for all scripts that call `conductor.prepare_panel()` unless they explicitly opt out.

**Related memos:**

- `3-Master_Plan/20260817_1606_Charles_to_SCOUT_espn_dash_placeholder_rows.md` (questions)
- `3-Master_Plan/20260817_1610_SCOUT_to_COMPASS_espn_dash_placeholder_rows.md` (SCOUT answers)
- `3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/PD22_minutes_panel_investigation_todo.md` (PD22 sprint)

---

## 2. Design principle: raw on disk, clean at the spine choke point

```
mbb_df_player_box.csv          ← NEVER rewritten (audit / re-fetch forensics)
        │
        ▼
panel_rebuild.build_from_box   ← BOX QC HERE (single choke point)
        │
        ▼
panel_build (perf, poolq_loo)  ← min_minutes, draftee filters (unchanged role)
        │
        ▼
PD21 / PD22 / Grandchild / 530 ventiles
```

| Layer | Mutate frozen CSV? | Role |
|-------|-------------------|------|
| `mbb_df_player_box.csv` | **No** | Immutable Stage 1 truth |
| `ingest_box.py` (future) | On refresh write | Should mirror dash filter when SDV ingest exists |
| **`panel_rebuild.build_from_box`** | **No** | **Current policy enforcement** |
| `panel_build.filter_panel` | No | Analysis subset only — too late for roster/game hygiene |
| Individual PD22 scripts | No | Must not duplicate filters |

---

## 3. The two filters (exact rules)

Applied on **game-level rows**, **before** `(athlete_id, season, team_id)` aggregation.

### 3a. Drop dash placeholder names

- **Rule:** Remove rows where `athlete_display_name.astype(str).str.strip() == "-"`.
- **Config:** `PipelineConfig.drop_dash_placeholder_names` (default **`True`**).
- **Rationale:** ESPN still serves these today (live API check on game `400986852`); 175 rows in 2011–2021; all 0/NaN minutes; not real athletes.
- **Blast radius:** 175 game rows; BYU 2018 roster_n 115 → 16 (before min-minutes filter).

### 3b. Drop low-game team-seasons

- **Rule:** After dash filter, count distinct `game_id` per `(team_id, season)`. Drop **all rows** for team-seasons with **`games_n <= 10`** (keep **`>= 11`**).
- **Config:** `PipelineConfig.min_team_season_games` (default **`10`** as of 2026-08-17 evening; was 5). Set **`0`** to disable.
- **Rationale:** ~29% of team-seasons had exactly 1 game in box (D-II/NAIA cameos vs one D-I opponent). Not a “season” for roster-size or pool-quality interpretation.
- **Draft impact at min_minutes=20 (min_g=10):** Same as min_g=5 — still **1,133** drafted hero rows; **0** additional draft loss vs min_g=5.

### 3c. Order of operations in `build_from_box`

1. Read box (+ `game_id`)
2. Season window (`panel_season_min` / `max`)
3. **Box QC** (dash + min games)
4. Aggregate to player-season
5. `min_minutes` on aggregated minutes
6. Attach `Y_draft` from lookup (does **not** touch `team_id`)
7. Optional SR merge

---

## 4. Measured impact (2011–2021 window, 2026-08-17 run)

| Metric | QC off (legacy) | QC on (defaults) |
|--------|----------------:|-----------------:|
| Dash rows dropped | 0 | **175** |
| Team-seasons dropped (≤5 games) | 0 | **2,692** |
| Box game rows dropped (low games) | 0 | **64,686** |
| Box rows after QC | 1,866,217 | **1,801,356** |
| Player-season rows (`min_minutes=0`) | **104,790** | **59,709** |
| Hero rows (`min_minutes=20`) | ~62,231 | **46,582** |
| Drafted rows (hero) | ~1,134 | **1,133** |

QC report is stored in `panel_rebuild.last_box_qc_report` after each `build_from_box` call.

**Provenance helper:** `panel_rebuild.box_qc_provenance_lines(cfg)` — for ventile exports and integrity reports (Step 2).

---

## 5. Configuration reference

```python
from sports_pipeline.config import PipelineConfig

# Default hero / PD21 / PD22 (box QC on)
cfg = PipelineConfig(
    perf_metric=["ppm"],
    min_minutes=20.0,
    panel_season_min=2011,
    panel_season_max=2021,
    # implicit defaults:
    # drop_dash_placeholder_names=True,
    # min_team_season_games=5,
)

# Legacy “true raw box” comparison (opt-in only)
cfg_raw = PipelineConfig(
    min_minutes=0.0,
    drop_dash_placeholder_names=False,
    min_team_season_games=0,
)
```

**Important:** `use_prebuilt_panel_csv=True` **bypasses** `build_from_box`. Prebuilt CSVs must be rebuilt after policy change, or QC will not apply.

---

## 6. What is NOT filtered (yet)

| Issue | Status |
|-------|--------|
| One-game **real-name** roster dumps (Jarvis 62 players, 13 played) | Partially mitigated by min-games filter if team has ≤5 games; Jarvis has 3 games — still in panel |
| Per-game roster cap (>25 athletes listed) | **Not implemented** — future optional QC |
| Exhibition / season-type exclusion | **Not implemented** — needs schedule metadata |

---

## 7. Plots and slides — regeneration inventory

Anything that calls `conductor.prepare_panel()` without opting out of box QC will change when figures are **re-run**. Slides embed PNGs and bullet text; **both** may need updates.

Legend: **🔴 Must regenerate** · **🟡 Check / likely minor** · **🟢 Unchanged**

### 7a. PD22 — Alex minutes meeting (🔴 primary)

| PNG / artifact | Script | AUTO slide | HAND deck | Text / notes |
|----------------|--------|------------|-----------|--------------|
| `pd22_minutes/PD22_raw_roster_size_distribution_before_qc_2011_2021.png` | `pd22_raw_roster_size_distribution.py --before-qc-only` | `slides/auto/CHAR_PD22_raw_roster_size_distribution_before_qc_AUTO.pptx` | Copy into HAND **first** | **🟢** Legacy raw box — frozen motivation (BYU 115 tail); **do not regen** when QC changes |
| `pd22_minutes/PD22_raw_roster_size_distribution_after_qc_2011_2021.png` | `pd22_raw_roster_size_distribution.py --after-qc-only` | `slides/auto/CHAR_PD22_raw_roster_size_distribution_after_qc_AUTO.pptx` | Copy into HAND after before-QC slide | **🔴** Max roster tail changes when QC policy changes |
| `pd22_minutes/PD22_raw_minutes_distribution_2011_2021.png` | `pd22_raw_minutes_distribution.py` | `CHAR_PD22_raw_minutes_distribution_AUTO.pptx` | HAND | **🔴** Row counts shift (~45k fewer player-seasons at min=0 |
| `pd22_minutes/PD22_ppm_distribution_2011_2021.png` | `pd22_ppm_distribution.py` | `CHAR_PD22_ppm_distribution_AUTO.pptx` | HAND | **🔴** Full + hero PPM histograms |
| `pd22_minutes/PD22_ppm_full_vs_filtered_2011_2021.png` | `pd22_ppm_distribution.py` | `CHAR_PD22_ppm_full_vs_filtered_AUTO.pptx` | HAND | **🔴** Overlay |
| `pd22_minutes/PD22_drafted_minutes_audit_2011_2021.png` | `pd22_drafted_minutes_audit.py` | `CHAR_PD22_drafted_minutes_audit_AUTO.pptx` | HAND | **🟡** Built at min=0; 1 draft row may drop from denominator — re-run and check JSON |
| `pd22_minutes/PD22_team_season_games_count_2011_2021.png` | ad hoc / future script | — | — | **🟢** Computed from **raw box**, not panel — still valid as motivation for filter |

**PD22 regen commands (repo root):**

```bash
python sports/scripts/pd22_drafted_minutes_audit.py
python sports/scripts/pd22_raw_minutes_distribution.py
python sports/scripts/pd22_ppm_distribution.py
python sports/scripts/pd22_raw_roster_size_distribution.py --after-qc-only

python sports/scripts/build_pd22_drafted_minutes_audit_slide.py --slides-only
python sports/scripts/build_pd22_raw_minutes_distribution_slide.py --slides-only
python sports/scripts/build_pd22_ppm_distribution_slide.py --slides-only
python sports/scripts/build_pd22_ppm_full_vs_filtered_slide.py --slides-only
python sports/scripts/build_pd22_raw_roster_size_after_qc_slide.py --slides-only
```

Then **Change Picture** (+ bullets) into your HAND PD22 deck.

---

### 7b. PD21 — ρ / H_sort calibration (🔴)

| PNG / artifact | Script | AUTO slide |
|----------------|--------|------------|
| `pd21_rho/PD21_rho_hsort_calibrate_2011_2021_bracket.png` | `pd21_rho_hsort_calibrate.py` | `CHAR_PD21_rho_hsort_calibrate_AUTO.pptx` |
| `pd21_rho/PD21_rho_hsort_calibrate_2011_2021_bracket_rho_hsort_timeseries.png` | same | `CHAR_PD21_rho_hsort_timeseries_AUTO.pptx` |
| `pd21_rho/PD21_rho_hsort_sensitivity_*.png` | `pd21_rho_hsort_sensitivity.py` | (if used in HAND) |
| `*_ppm0lt20_*` variants | `--ppm-zero-below-minutes 20` | `*_ppm0lt20_AUTO.pptx` |

**Regen:**

```bash
python sports/scripts/pd21_rho_hsort_calibrate.py --fresh
python sports/scripts/build_pd21_rho_hsort_calibrate_slide.py
python sports/scripts/build_pd21_rho_hsort_timeseries_slide.py
```

Slide bullets cite “2011–2021 hero MBB · min 20 min · empirical roster caps” — add **“box QC: drop dash, min 6 games/team-season”** after Step 2 provenance wiring.

---

### 7c. Grandchild / empirical hero panel (🔴)

All use `prepare_panel` with `min_minutes=20` (directly or via `empirical_lc_distributions._prepare_panel()`).

| PNG (under `grandchild_assign/` or `empirical_pd17/`) | Script | Slide builder |
|------------------------------------------------------|--------|---------------|
| `GRANDCHILD_ncaa_roster_size_distribution_2011_2021.png` | `grandchild_ncaa_roster_size_distribution.py` | `build_grandchild_ncaa_roster_size_slide.py` |
| `GRANDCHILD_ncaa_vs_lg_roster_size_compare_2011_2021.png` | same | same |
| `GRANDCHILD_selection_inverted_u_2011_2021.png` | `grandchild_selection_inverted_u_diagnostic.py` | `build_grandchild_league_analysis_slide.py` (partial) |
| `GRANDCHILD_empirical_lc_compare_2011_2021.png` | `grandchild_empirical_lc_compare.py` | `build_grandchild_empirical_lc_compare_slide.py` |
| `GRANDCHILD_league_lc_*.png` | `grandchild_league_lc_diagnostic.py` | league analysis deck |
| `empirical_lc_distributions` PNGs | `empirical_lc_distributions.py` | `build_empirical_lc_distributions_slide.py` |
| `empirical_ai_tj_distributions` PNGs | `empirical_ai_tj_distributions.py` | `build_empirical_ai_tj_distributions_slide.py` |
| Team interval overlap PNGs | `empirical_team_interval_overlap.py` | `build_empirical_team_interval_overlap_slide.py` |
| Rho coverage overlay | `empirical_rho_coverage_overlay.py` | `build_empirical_rho_coverage_slide.py` |
| Pass A ventile bundle | `pass_a_empirical_bundle.py` | `build_pass_abc_slides.py` |

**Regen (core chain):**

```bash
python sports/scripts/empirical_lc_distributions.py
python sports/scripts/grandchild_ncaa_roster_size_distribution.py
python sports/scripts/grandchild_selection_inverted_u_diagnostic.py
python sports/scripts/grandchild_empirical_lc_compare.py
python sports/scripts/pd21_rho_hsort_calibrate.py --fresh
```

Then rebuild associated AUTO slides with `--slides-only` where PNGs already exist.

---

### 7d. Sensitivity / ladder (🟡)

| Script | Notes |
|--------|-------|
| `hero_min_minutes_sensitivity_ladder.py` | **🟡** Re-run if cited in HAND |
| `build_alex_minutes_filter_light_slides.py` | **🟡** Uses ladder outputs |

---

### 7e. Likely unchanged (🟢)

| Item | Why |
|------|-----|
| PD20 temperature sweep (`pd20_temperature/`) | Simulation diagnostics, not box panel |
| `build_pd20_hand_slides.py` | PD20 sim figures |
| Sim input / λ / θ / γ characterization decks | Synthetic draws, not ESPN panel |
| `541_grandchild_rho_sweep.py` / rho WSS slides | Sim sweep |
| `PD22_team_season_games_count_2011_2021.png` | Raw box histogram (motivation chart) |
| Draft match CSVs / `college_aliases` | Unaffected |

---

### 7f. HAND decks to open and audit manually

PPTX may not be in git. On disk under `3-Master_Plan/re_entry/HEROs_and_PASSes/slides/`:

| HAND file | Risk |
|-----------|------|
| Any deck with **PD22** figures | **🔴 High** |
| `CHAR_PD21_rho_hsort_calibrate` (HAND if separate from AUTO) | **🔴 High** |
| `CHAR_grandchild_league_analysis.pptx` | **🔴** if embeds inverted-U / roster PNGs |
| `CHAR_PD17_HAND.pptx` | **🟡** empirical LC / overlap slides |
| `CHAR_PD20_HAND.pptx` | **🟢** |
| `CHAR_rho_characterization.pptx` / lambda / theta / gamma HAND | **🟢** unless empirical PNGs pasted in |

**Rule of thumb:** If the slide picture came from a script in §7a–7c, re-run that script + slide builder, then Change Picture in HAND.

---

## 8. Implementation checklist (rollout steps)

| Step | Task | Status |
|------|------|--------|
| **1** | `PipelineConfig`: `drop_dash_placeholder_names`, `min_team_season_games` | ✅ Done 2026-08-17 |
| **1** | `panel_rebuild.build_from_box`: apply QC + `last_box_qc_report` | ✅ Done 2026-08-17 |
| **2** | `panel_build` ventile provenance: call `box_qc_provenance_lines` | ⬜ Pending |
| **2** | `data_integrity.summarize_data_integrity`: box QC drop counts | ⬜ Pending |
| **3** | `SPORTS_DATA_GAMEPLAN.md` § Stage 1: policy paragraph | ⬜ Pending |
| **3** | `pd22_minutes/README.md`: point to this doc | ⬜ Pending |
| **4** | PD22 scripts: write box QC flags into JSON metadata | ⬜ Pending |
| **4** | PD22 slide builders: update bullet text (“box QC applied”) | ⬜ Pending |
| **5** | Optional `--legacy-raw-box` CLI on PD22 for before/after figure | ⬜ Pending |
| **6** | Regenerate §7a–7c PNGs + AUTO slides; Charles updates HAND | ⬜ Pending (Charles) |
| **7** | `ingest_box.py` (future): mirror dash filter on refresh | ⬜ When ingest ported |

---

## 9. Talking points for Alex

1. **Frozen ESPN box has junk** (dash placeholders + fragmentary small-school coverage). We filter at panel build; raw CSV preserved.
2. **`min_minutes = 20`** remains the hero playing-time floor; box QC is **additional** hygiene for who counts as a team-season at all.
3. **Draft signal preserved:** 1,133 of 1,134 drafted hero rows remain after QC.
4. **BYU 115-man roster** was dash placeholders, not alias merge — now 16 at min=0 with QC.
5. **Roster-size backup slide** should be regenerated; tail was dominated by box artifacts.

---

## 10. Code locations

| File | Purpose |
|------|---------|
| `sports/sports_pipeline/config.py` | Defaults |
| `sports/sports_pipeline/panel_rebuild.py` | QC implementation + provenance helper |
| `sports/sports_pipeline/conductor.py` | `prepare_panel()` entry |
| `sports/documents/SPORTS_DATA_GAMEPLAN.md` | Architecture contract (to update) |

---

*Maintained with PD22 / COMPASS. Update §4 counts if box CSV or defaults change.*
