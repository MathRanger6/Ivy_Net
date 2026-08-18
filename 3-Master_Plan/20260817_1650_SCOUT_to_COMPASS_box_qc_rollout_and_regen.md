# SCOUT → COMPASS: Box QC rollout — complete session brief

**Date:** 2026-08-17  
**From:** SCOUT (for Charles)  
**To:** COMPASS  
**Purpose:** **This is the only document Charles needs to hand you.** Policy, investigation, code status, regen runbook, slide inventory, Alex talking points, and remaining engineering — all here.

**Charles’s ask:** Run figure/slide regeneration **with COMPASS** (sequenced below). Step 1 (upstream code) is **done**.

---

## 0. How COMPASS should use this doc

| Do | Don’t |
|----|--------|
| Work from **this file** as single source of truth | Scavenge `BOX_QC_panel_build_policy.md`, SCOUT Q&A memos, or PD22 todo unless Charles points you there |
| Execute **Phase A** first if Alex deadline is tight | Regenerate grandchild/PD17 stack before PD22 unless those PNGs are in the live deck |
| Update **§12 checklist** as steps complete | Edit frozen `mbb_df_player_box.csv` |

Supporting paths (reference only):

- `3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/` — PNG/JSON outputs
- `3-Master_Plan/re_entry/HEROs_and_PASSes/slides/auto/` — disposable AUTO decks
- `3-Master_Plan/re_entry/HEROs_and_PASSes/slides/` — HAND masters (Charles Change Picture)

---

## 1. Executive summary

While preparing **PD22** (Alex meeting, 17 Aug 2026 — justify `min_minutes = 20`), Charles found ESPN box junk inflating roster-size diagnostics (BYU 2018: **115** distinct athletes). SCOUT traced root cause to **Stage 1 box data**, not draft matching or `college_aliases`.

**Decisions (Charles approved 2026-08-17):**

1. Apply hygiene **upstream** at `panel_rebuild.build_from_box` — **do not** rewrite `mbb_df_player_box.csv`.
2. **Filter A:** drop `athlete_display_name.strip() == "-"` (175 rows, 2011–2021).
3. **Filter B:** drop team-seasons with **≤ 5** distinct games in box (keep **≥ 6**); removes fragmentary D-II/NAIA one-game cameos.
4. Defaults **ON** for all `conductor.prepare_panel()` calls unless a script opts out.
5. **Regenerate** affected PNGs + AUTO slides; Charles updates HAND decks.

**Step 1 (code) — ✅ done today.** Steps 2–7 (provenance wiring, slide bullet defaults, etc.) can run in parallel with regen.

---

## 2. Background — what triggered this (PD22)

Charles ran roster-size diagnostics (`pd22_raw_roster_size_distribution.py`) at `min_minutes=0`. Histogram had a long right tail; max **roster_n = 115** (BYU 2018).

| Field | Value |
|-------|--------|
| School | BYU (`team_id=252`) |
| Season | 2018 |
| Cause | **99** rows with `athlete_display_name == "-"` from **one game** (`400986852`, 2017-11-29 vs Utah Valley) |
| Normal BYU seasons | ~12–20 athletes |

Charles initially feared **college/draft alias adjudication** had merged schools into BYU. Checks said **no**:

- `datasets/mbb/DO_NOT_ERASE/college_aliases.csv` — no BYU rows
- Only one ESPN `team_id` with short name `"BYU"`
- `draft_athlete_match.csv` — 5 BYU rows, all `college = "BYU"`

**Separate issue (real names, zero minutes):** Some small schools list 50+ **real** players in one game with only ~10–15 getting minutes (Jarvis Christian, Webber International). Partially addressed by min-games filter when team has ≤5 games; Jarvis (3 games) may still appear. Per-game roster cap **not** implemented.

**Motivation chart (unchanged by QC):** `PD22_team_season_games_count_2011_2021.png` — bimodal distribution; **1,883** team-seasons (29%) have exactly **1** game in box. Justifies Filter B.

---

## 3. Investigation findings (ESPN dash placeholders)

### 3.1 Root cause — ESPN source, not transient scrape bug

- **No scrape logs** in repo for the five bad games. `ingest_box.py` is a **stub** (checks CSV exists only).
- **Live ESPN API re-fetch (2026-08-17)** on game `400986852`:

| Team | Live athletes | Live `"-"` names |
|------|-------------:|-----------------:|
| BYU (`252`) | 113 | **99** |
| Utah Valley (`3084`) | 16 | 0 |

Same `athlete_id` block as frozen CSV (4289042–4289141). **Re-scrape without filter reproduces junk.**

### 3.2 All five dash games (2011–2021)

| game_id | date | team with dash rows | dash | opponent dash |
|---------|------|---------------------|-----:|--------------:|
| 400986852 | 2017-11-29 | BYU | 99 | 0 |
| 400830589 | 2015-11-20 | Weber St | 45 | 0 |
| 400846817 | 2015-12-31 | Fort Valley St | 24 | 0 |
| 400990127 | 2017-11-19 | Kent State | 4 | 0 |
| 400990018 | 2017-11-30 | Delaware St | 3 | 0 |

Global: **175** dash rows, **0** with minutes > 0, **5** team-seasons, **5** games. One-sided bloat per game.

### 3.3 Pipeline separation (draft / aliases)

**Confirmed:** `college_aliases` and draft match **cannot** inflate `(team_id, season)` roster counts. They only set `Y_draft` via `athlete_id_draft_lookup.csv`. `team_id` comes from box CSV in `panel_rebuild.build_from_box`. Wrong team assignment would require hand-edited box or upstream ingest bug — not observed here.

---

## 4. Architecture — raw on disk, clean at spine choke point

```
mbb_df_player_box.csv          ← NEVER rewritten (audit / re-fetch forensics)
        │
        ▼
panel_rebuild.build_from_box   ← BOX QC HERE (single choke point)  ✅ implemented
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
| `ingest_box.py` (future) | On refresh write | Mirror dash filter when SDV ingest exists |
| **`panel_rebuild.build_from_box`** | **No** | **Policy enforcement (live)** |
| `panel_build.filter_panel` | No | Too late for roster/game hygiene |
| Individual PD22 scripts | No | Must not duplicate filters |

**Warning:** `use_prebuilt_panel_csv=True` **bypasses** QC. Default conductor path rebuilds from box.

---

## 5. The two filters — exact rules

Applied on **game-level rows**, **before** `(athlete_id, season, team_id)` aggregation.

### Filter A — dash placeholders

| | |
|--|--|
| **Rule** | Drop rows where `athlete_display_name.astype(str).str.strip() == "-"` |
| **Config** | `PipelineConfig.drop_dash_placeholder_names` default **`True`** |
| **Blast radius** | 175 game rows; BYU 2018 roster_n 115 → **16** (before min-minutes) |

### Filter B — low-game team-seasons

| | |
|--|--|
| **Rule** | After Filter A, count distinct `game_id` per `(team_id, season)`. Drop **all rows** for team-seasons with **`games_n <= 5`** |
| **Config** | `PipelineConfig.min_team_season_games` default **`5`** (`0` = off) |
| **Plain language** | Keep team-seasons with **≥ 6 games** in box |
| **Draft impact (hero min=20)** | Loses **1** drafted player-season (Derrick White @ UCCS 2014, 1 game); same athlete remains via Colorado 2017 |

### Order of operations in `build_from_box`

1. Read box (includes `game_id`)
2. Season window (`panel_season_min` / `max`)
3. **Box QC** (dash + min games)
4. Aggregate to player-season (`games` = count of game rows)
5. `min_minutes` on aggregated minutes
6. Attach `Y_draft` from lookup
7. Optional SR merge (`bpm_player_season_matched.csv`)

---

## 6. Code status (Step 1 — done 2026-08-17)

| File | Change |
|------|--------|
| `sports/sports_pipeline/config.py` | New fields with defaults above |
| `sports/sports_pipeline/panel_rebuild.py` | `_apply_box_qc()`, `last_box_qc_report`, `box_qc_provenance_lines()` |

**Legacy opt-out** (before/after appendix figures only):

```python
from sports_pipeline.config import PipelineConfig

cfg_raw = PipelineConfig(
    min_minutes=0.0,
    drop_dash_placeholder_names=False,
    min_team_season_games=0,
    panel_season_min=2011,
    panel_season_max=2021,
    restrict_teams_by_draftees=False,
)
```

**Default hero / PD21 / PD22** (implicit QC on):

```python
cfg = PipelineConfig(
    perf_metric=["ppm"],
    min_minutes=20.0,
    panel_season_min=2011,
    panel_season_max=2021,
    # drop_dash_placeholder_names=True,
    # min_team_season_games=5,
)
```

After each rebuild, inspect: `panel_rebuild.last_box_qc_report`

---

## 7. Measured impact (2011–2021, verified 2026-08-17)

| Metric | QC off (legacy) | QC on (defaults) |
|--------|----------------:|-----------------:|
| Dash rows dropped | 0 | **175** |
| Team-seasons dropped (≤5 games) | 0 | **2,692** |
| Box game rows dropped (low games) | 0 | **64,686** |
| Box rows read → after QC | 1,866,217 → 1,866,217 | 1,866,217 → **1,801,356** |
| Player-season rows (`min_minutes=0`) | **104,790** | **59,709** |
| Hero rows (`min_minutes=20`) | ~62,231 | **46,582** |
| Drafted hero rows | ~1,134 | **1,133** |

Re-run regen scripts and refresh this table if counts drift.

---

## 8. What did NOT change / not filtered yet

**Unchanged:**

- Frozen box CSV, draft match CSVs, `college_aliases`
- `min_minutes=20` hero lock (separate knob)
- `PD22_team_season_games_count_2011_2021.png` (raw box; motivation for Filter B)

**Not filtered yet:**

| Issue | Status |
|-------|--------|
| Real-name one-game roster dumps (Jarvis 62 listed, 13 played) | Partially mitigated; Jarvis has 3 games → still in panel |
| Per-game roster cap (>25 athletes/game) | Future optional QC |
| Exhibition / season-type exclusion | Needs schedule metadata |

---

## 9. Regeneration runbook — Charles + COMPASS

**SCOUT recommendation:** **Yes, run it all with COMPASS**, sequenced as below.

Legend: **🔴 Must regenerate** · **🟡 Check** · **🟢 Unchanged**

---

### Phase A — PD22 / Alex (🔴 do first; ~30–60 min compute)

**Why first:** Directly supports Alex meeting on minutes floor and roster policy.

**1. Regenerate PNGs + JSON** (repo root, `sports_net` env):

```bash
python sports/scripts/pd22_drafted_minutes_audit.py
python sports/scripts/pd22_raw_minutes_distribution.py
python sports/scripts/pd22_ppm_distribution.py
python sports/scripts/pd22_raw_roster_size_distribution.py
```

**2. Rebuild AUTO slides:**

```bash
python sports/scripts/build_pd22_drafted_minutes_audit_slide.py --slides-only
python sports/scripts/build_pd22_raw_minutes_distribution_slide.py --slides-only
python sports/scripts/build_pd22_ppm_distribution_slide.py --slides-only
python sports/scripts/build_pd22_ppm_full_vs_filtered_slide.py --slides-only
python sports/scripts/build_pd22_raw_roster_size_slide.py --slides-only
```

**3. Charles:** Change Picture (+ bullets) from AUTO → HAND PD22 deck.

| PNG (`pd22_minutes/`) | Generator script | AUTO deck (`slides/auto/`) |
|------------------------|------------------|----------------------------|
| `PD22_drafted_minutes_audit_2011_2021.png` | `pd22_drafted_minutes_audit.py` | `CHAR_PD22_drafted_minutes_audit_AUTO.pptx` |
| `PD22_raw_minutes_distribution_2011_2021.png` | `pd22_raw_minutes_distribution.py` | `CHAR_PD22_raw_minutes_distribution_AUTO.pptx` |
| `PD22_ppm_distribution_2011_2021.png` | `pd22_ppm_distribution.py` | `CHAR_PD22_ppm_distribution_AUTO.pptx` |
| `PD22_ppm_full_vs_filtered_2011_2021.png` | `pd22_ppm_distribution.py` | `CHAR_PD22_ppm_full_vs_filtered_AUTO.pptx` |
| `PD22_raw_roster_size_distribution_2011_2021.png` | `pd22_raw_roster_size_distribution.py` | `CHAR_PD22_raw_roster_size_distribution_AUTO.pptx` |

| PNG | Status | Notes |
|-----|--------|-------|
| `PD22_team_season_games_count_2011_2021.png` | **🟢** | Raw box histogram — **no regen needed** |
| | | Optional slide: `build_pd22_team_season_games_count_slide.py --slides-only` → `CHAR_PD22_team_season_games_count_AUTO.pptx` |

**Slide text COMPASS must flag for Charles:** Bullets saying “unfiltered box” / “min=0 rebuild” should read **“panel rebuild at min_minutes=0 **after box QC** (drop dash placeholders; team-season ≥6 games)”**. Otherwise Alex hears the wrong panel definition.

**Expected narrative shift:** BYU 115 tail gone; roster histogram interpretable; **min=20 defense unchanged**; 1 draft row lost (UCCS 2014 only).

---

### Phase B — PD21 ρ / H_sort (🔴 if in Alex deck)

```bash
python sports/scripts/pd21_rho_hsort_calibrate.py --fresh
python sports/scripts/build_pd21_rho_hsort_calibrate_slide.py
python sports/scripts/build_pd21_rho_hsort_timeseries_slide.py
```

| PNG (`pd21_rho/`) | AUTO deck |
|-------------------|-----------|
| `PD21_rho_hsort_calibrate_2011_2021_bracket.png` | `CHAR_PD21_rho_hsort_calibrate_AUTO.pptx` |
| `PD21_rho_hsort_calibrate_2011_2021_bracket_rho_hsort_timeseries.png` | `CHAR_PD21_rho_hsort_timeseries_AUTO.pptx` |
| `*_ppm0lt20_*` variants | `*_ppm0lt20_AUTO.pptx` (if used) |

**Check:** `PD21_rho_hsort_calibrate_2011_2021_fit.json` — ρ* may shift slightly (~25% fewer hero rows). Re-read before defending calibration.

**Slide bullets:** Add “box QC: drop dash, min 6 games/team-season” once provenance wired (Step 2); add manually in HAND until then.

---

### Phase C — Grandchild / empirical hero panel (🔴 if PNGs in deck; else skip for Alex deadline)

All call `prepare_panel` with `min_minutes=20` (directly or via `empirical_lc_distributions._prepare_panel()`).

```bash
python sports/scripts/empirical_lc_distributions.py
python sports/scripts/grandchild_ncaa_roster_size_distribution.py
python sports/scripts/grandchild_selection_inverted_u_diagnostic.py
python sports/scripts/grandchild_empirical_lc_compare.py
```

Then `--slides-only` on matching `build_*_slide.py` as needed.

| PNG (typical dir: `grandchild_assign/`) | Script | Slide builder |
|------------------------------------------|--------|---------------|
| `GRANDCHILD_ncaa_roster_size_distribution_2011_2021.png` | `grandchild_ncaa_roster_size_distribution.py` | `build_grandchild_ncaa_roster_size_slide.py` |
| `GRANDCHILD_ncaa_vs_lg_roster_size_compare_2011_2021.png` | same | same |
| `GRANDCHILD_selection_inverted_u_2011_2021.png` | `grandchild_selection_inverted_u_diagnostic.py` | `build_grandchild_league_analysis_slide.py` (partial) |
| `GRANDCHILD_empirical_lc_compare_2011_2021.png` | `grandchild_empirical_lc_compare.py` | `build_grandchild_empirical_lc_compare_slide.py` |
| `GRANDCHILD_league_lc_*.png` | `grandchild_league_lc_diagnostic.py` | league analysis deck |
| empirical LC / ai_tj / overlap / rho coverage | `empirical_*.py`, `pass_a_empirical_bundle.py` | matching `build_empirical_*_slide.py`, `build_pass_abc_slides.py` |

---

### Phase D — 🟢 skip for this sprint unless cited in HAND

| Item | Why skip |
|------|----------|
| PD20 temperature (`pd20_temperature/`, `build_pd20_hand_slides.py`) | Sim-only |
| λ / θ / γ characterization decks | Synthetic |
| `541_grandchild_rho_sweep.py`, rho WSS slides | Sim sweep |
| `hero_min_minutes_sensitivity_ladder.py` | **🟡** only if in HAND |
| Draft match / alias CSVs | Unaffected |

---

### HAND decks — manual audit (under `slides/`)

PPTX may not be in git. Open and check embedded PNGs:

| HAND file | Risk |
|-----------|------|
| Any deck with **PD22** figures | **🔴 High** |
| PD21 ρ calibration (HAND copy if separate from AUTO) | **🔴 High** |
| `CHAR_grandchild_league_analysis.pptx` | **🔴** if inverted-U / roster PNGs |
| `CHAR_PD17_HAND.pptx` | **🟡** empirical LC / overlap |
| `CHAR_PD20_HAND.pptx` | **🟢** |
| `CHAR_rho_characterization.pptx` / lambda / theta / gamma | **🟢** unless empirical PNGs pasted in |

**Rule:** If picture came from Phase A–C script → re-run script + slide builder → Change Picture in HAND.

---

## 10. Talking points for Alex (COMPASS can coach Charles)

1. **ESPN box has junk** — dash `"-"` placeholders and sparse one-game team-seasons. We filter at **panel build**; raw CSV preserved for audit.
2. **`min_minutes = 20`** is still the hero playing-time floor; box QC is **additional** hygiene for who counts as a team-season.
3. **Draft signal preserved:** 1,133 of 1,134 drafted hero rows remain after QC.
4. **BYU 115-man roster** was ESPN `"-"` placeholders in one game — **not** alias merge. With QC, BYU 2018 → 16 at min=0.
5. **Games-count histogram** explains Filter B: ~29% of team-seasons had only 1 game in ESPN box (small schools vs one D-I opponent).
6. **Model layering:** This is spine/environment hygiene — orthogonal to selection vs hero ([`BINDING_Selection_is_its_own_step.md`](BINDING_Selection_is_its_own_step.md)).

---

## 11. Remaining engineering (Steps 2–7) — not blocking Phase A

| Step | Task | Status | Owner |
|------|------|--------|-------|
| 1 | `PipelineConfig` + `build_from_box` QC | ✅ Done | SCOUT |
| 2 | Wire `box_qc_provenance_lines` into ventile provenance + `data_integrity` | ⬜ | SCOUT |
| 3 | `SPORTS_DATA_GAMEPLAN.md` § Stage 1 paragraph | ⬜ | SCOUT |
| 4 | PD22 JSON metadata: QC flags + drop counts | ⬜ | SCOUT |
| 4 | PD22 slide builders: default bullets mention box QC | ⬜ | SCOUT + Charles |
| 5 | Optional `--legacy-raw-box` CLI on PD22 (before/after appendix) | ⬜ | SCOUT if wanted |
| 6 | Regenerate §9 PNGs + AUTO; Charles HAND updates | ⬜ | **Charles + COMPASS** |
| 7 | `ingest_box.py` mirror on future SDV refresh | ⬜ | Later |

---

## 12. COMPASS coordination checklist

- [ ] Confirm Charles’s **live Alex deck** — which phases (A only vs A+B vs A+B+C)?
- [ ] Run Phase A commands; verify JSON summaries look sane
- [ ] Rebuild AUTO slides; Charles Change Picture into HAND
- [ ] Update slide bullets: **“after box QC”** not “unfiltered box”
- [ ] If PD21 in deck: `--fresh` calibrate + check `fit.json` ρ*
- [ ] Tick off §11 steps as SCOUT completes provenance wiring
- [ ] Do **not** edit `mbb_df_player_box.csv`

---

## 13. One-line ask from Charles

*Box QC is in code; run PD22 → PD21 → grandchild regen with COMPASS; annotate panel policy so Alex gets a coherent minutes/roster story.*

---

## 14. Code & output paths (quick index)

```
sports/sports_pipeline/config.py              # defaults
sports/sports_pipeline/panel_rebuild.py       # QC + last_box_qc_report
sports/sports_pipeline/conductor.py           # prepare_panel()
datasets/mbb/mbb_df_player_box.csv            # frozen — do not edit
3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/     # PD22 PNG/JSON
3-Master_Plan/re_entry/HEROs_and_PASSes/pd21_rho/         # PD21 PNG/JSON
3-Master_Plan/re_entry/HEROs_and_PASSes/grandchild_assign/ # empirical PNGs
3-Master_Plan/re_entry/HEROs_and_PASSes/slides/auto/      # AUTO pptx
3-Master_Plan/re_entry/HEROs_and_PASSes/slides/           # HAND pptx
```

---

*End of COMPASS session brief. Mirror updates here when regen completes or counts change.*
