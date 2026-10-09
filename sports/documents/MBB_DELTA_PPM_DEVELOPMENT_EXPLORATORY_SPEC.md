# MBB — ΔPPM development vs team context (exploratory spec)

**Status:** Charles request **2026-10-08** — document before code.  
**Audience:** Charles, model chapter, COMPASS / implementation.  
**Related:** [`MBB_FIRST_SEASON_AT_SCHOOL_SORT_DECISIONS.md`](MBB_FIRST_SEASON_AT_SCHOOL_SORT_DECISIONS.md) (first@school PPM definition); Scholar VECTOR **\(A^{\mathrm{final}} = B^{\mathrm{entry}} + \Delta(\mathrm{environment})\)** framing; [`3-Master_Plan/BINDING_Selection_is_its_own_step.md`](../../3-Master_Plan/BINDING_Selection_is_its_own_step.md).

---

## One-sentence estimand

Among players with **≥2 recorded player-seasons**, describe how **college development** \(\Delta z = z(\mathrm{metric})_{\mathrm{last\,PS}} - z(\mathrm{metric})_{\mathrm{first\,PS}}\) (chronological first/last PS **any team**; within-season z each year, then subtract; v1 metric PPM) associates with **exit-year team / peer context** (\(\hat{T}_j\), LOO pool quality, viable-peer congestion) and optionally **`Y_draft`** — **associational**, not causal congestion or hero replacement.

---

## Motivation

- MBB has **no** high-school / recruiting **\(B_i\)** in the downloaded stack.
- We **do** have **first season at school** and **last player-season (last-ps)** production from ESPN box → panel.
- Reigning hero plots **`P(Y=1)` vs `poolq_loo`** at a **single time slice**; they do **not** measure **within-player development**.
- This exploratory track asks: does **visible PPM growth** over a college spell **co-vary** with playing on **stronger teams** (\(\hat{T}_j\)) or **more congested viable-peer ponds** (`L_C` at last-ps)? Minutes enter as **opportunity** controls or companion plots.

This is **not** assignment-time assortativity (**\(H_{\mathrm{sort}}^{\mathrm{entry}}\)**). It is **post-assignment** \(\Delta A\) vs **exit-year** context.

---

## Core quantities

### Development (player, within school)

| Symbol / column | Definition |
|-----------------|------------|
| **`season_first`** | **Locked O3:** `min(season)` over all panel rows for `athlete_id` (earliest **recorded** player-season), **any `team_id`**. |
| **`season_last`** | **Locked O3:** `max(season)` over all panel rows for `athlete_id` (latest recorded player-season), **any `team_id`**. |
| **`ppm_first`**, **`ppm_last`** | PPM on those rows (before z); if multiple rows tie on min/max season, take the row with lexicographically smallest `team_id` (document in code). |
| **`delta_dev`** | **Locked O1:** within-season z of the chosen metric on **first** and **last chronological** PS rows, then **subtract** (`z_last - z_first`). v1 column e.g. **`delta_ppm_z`** when metric is PPM. |
| **`minutes_first`**, **`minutes_last`** | Minutes on first and last rows; optional **`delta_minutes`**. |

**Multi-metric sweep (later, same recipe):** PPM, BPM, OBPM, DBPM — each via `assign_perf_from_metric` → within-season z → Δ on first/last@school. SR merge required for BPM family.

### Peer / team context (attach to **last chronological PS row**)

Computed with **same-season `perf`** (within-season z of active metric) and existing LOO / Tier 1 machinery — **not** freshman PPM for teammates. **All x-axes use `season_last`** on **`(team_id, season)` of that row** (transfers: exit pond may differ from freshman team).

**Locked O2 (2026-10-08, Charles “C+”):** v1 runs **three separate x-axis settings** (script/CLI parameter `roster_x` or equivalent), not one combined plot:

| Setting | Column / construction | Interpretation |
|---------|----------------------|----------------|
| **`T_j`** | **\(\hat{T}_j\)** = mean `perf` on `(team_id, season_last)` over roster rows **after analysis filters** (min minutes, mg10, etc.). **Always includes self** in the mean. | Team strength in exit year on the **filtered** pond. |
| **`poolq_loo`** | `poolq_loo` on player’s **last chronological** row | LOO mean teammate `perf` — **quality**, separate from \(\hat{T}_j\). |
| **`congestion_viable`** | LOO **share** of teammates with `perf > θ` (`congestion_crowding` / `tier1_mechanism_variables`, `crowding_mode="share"`) | Viable-peer **congestion** (**\(L_C\)** hard share). **Three θ variants (O5)** — separate columns / plots. |

Optional sensitivity (not v1 default): smooth **`pool_c_smooth_loo`** (σ(γ(A−θ))) per θ variant.

### Viability cutline θ — **O5 locked: all three** (Charles 2026-10-08)

Compute **`congestion_viable`** three times on the **same** filtered panel (same `perf` scale). Record θ in provenance.

| ID | Rule | Code / label |
|----|------|----------------|
| **`theta_drafted_median`** | Median `perf` among **drafted** player-seasons (same mask as `viability_theta_drafted_perf(..., stat="median")`) | `congestion_viable_drafted_med` |
| **`theta_global_median`** | Median `perf` over **all** player-season rows in the analysis window **after** mg/minutes filters (before collapsing to one row per athlete) | `congestion_viable_global_med` |
| **`theta_fixed_zero`** | **θ = 0** (fixed); meaningful because `perf` is **within-season z** | `congestion_viable_z0` |

CLI: `--congestion-theta drafted_median|global_median|fixed_zero|all` with **`all`** the v1 default (nine figures: 3 x-settings × 3 θ only affects congestion panels → 3 + 3 + 3 = 7 unique x types... actually T_j and poolq once each, congestion 3 times = 5 plot types per metric, or 3 congestion + 1 Tj + 1 LOO = 5 plots per sweep).

When **`--congestion-theta all`**, emit **three** Δz vs congestion scatter (or binned) panels, one per θ row in the table above.

### Outcome (descriptive overlay)

| Field | Use |
|-------|-----|
| **`Y_draft`** | Color, facet, or separate panels — **outcome**, not regressor for “development mechanism” claims. |

---

## Analysis grain

**Locked O3 (2026-10-08):** **One row per `athlete_id`.**

- **`season_first`** = earliest recorded player-season (**any team**).
- **`season_last`** = latest recorded player-season (**any team**).
- Require **`season_first < season_last`** (exclude one-and-done / single-season careers for Δz).
- **Transfers:** Δz spans **whole college spell** in the panel (freshman team → final team); peer x-axes come from the **last** row’s team-season only (~**5%** of in-panel draftees multi-team; see exploratory count 2026-10-08).

**Later (not v1):** within-school spells only; exclude or flag transfers; longest spell at one program.

**Relation to reigning hero last-ps:** Same **`season_last`** as global `max(season)` per athlete when the panel is complete — aligns draft **`Y`** overlay with hero cross-section, but Δ still uses **first** PS which may be at another school.

---

## Filters — **CLI options, not hardcoded** (Charles 2026-10-08)

All filters are **arguments** on the development script (defaults below = **reigning-style preset**, overridable per run). **`provenance.json`** must echo **every** flag and **N** after each step.

Optional convenience: **`--preset reigning`** sets the default column in one shot; explicit flags always win.

### Season / panel spine

| CLI flag | Default (preset) | Role |
|----------|------------------|------|
| `--season-min`, `--season-max` | 2009, 2021 | Restrict `season` before LOO / collapse. |
| `--use-prebuilt-panel-csv` | off (rebuild from box) | Same as `PipelineConfig.use_prebuilt_panel_csv`. |
| `--drop-dash-placeholder-names` / `--no-drop-dash` | on | Box QC (`panel_rebuild`). |

### Playing time & team-season quality

| CLI flag | Default (preset) | Role |
|----------|------------------|------|
| `--min-minutes` | 20 | Drop **player-season** rows with `minutes <` floor before LOO (Pass A `filter_panel`). |
| `--endpoint-minutes` | `both` | **`both`**: same floor on chronological **first and last** PS (default = `--min-minutes`). **`last-only`**: gate **last PS only**; first PS may be below floor (use with `--min-minutes 0` or `--ppm-zero-below-minutes` if freshman low-minute rows must stay in panel for LOO). |
| `--min-minutes-first`, `--min-minutes-last` | inherit mode / `--min-minutes` | Explicit overrides on **first / last** endpoint rows (win over `--endpoint-minutes`). |
| `--min-team-season-games` | 10 | Drop entire `(team_id, season)` with ≤ this many games (`filter_team_seasons_min_games`). |
| `--ppm-zero-below-minutes` | off (`None`) | **PD21 / PD22 mode:** if set (e.g. 20), **do not** drop low-minute rows; **zero raw `ppm`** when `minutes <` threshold, then recompute `perf` + LOO (`pd21_rho_hsort_calibrate.prepare_calibration_panel`). **Mutually exclusive** with using `--min-minutes` as a row drop — script must error if both active. |

### Pool / LOO hygiene

| CLI flag | Default (preset) | Role |
|----------|------------------|------|
| `--winsor-lo`, `--winsor-hi` | 0.01, 0.99 | `poolq_winsor_quantiles` on `poolq_loo` after LOO. |
| `--no-poolq-winsor` | off | Pass `None` for winsor (matches some BDP “no winsor” plots). |

### Population / draft labeling (for `Y_draft` overlay & θ)

| CLI flag | Default (preset) | Role |
|----------|------------------|------|
| `--y-draft-mode` | `ever` | `ever` vs `season` (Pass A). |
| `--dft` | off | +DFT: keep only player-seasons on teams with ≥1 draftee (`pass_a_empirical_bundle._apply_dft`). |
| `--restrict-teams-by-draftees` | off | Hero preset uses ALLT; optional `PipelineConfig.restrict_teams_by_draftees`. |

### Δz-specific (always applied unless disabled)

| CLI flag | Default | Role |
|----------|---------|------|
| `--require-two-seasons` | on | Drop athletes with `season_first == season_last`. |
| `--exclude-transfer-spells` | off | Later: drop multi-`team_id` careers; not v1 unless flag added. |

### Performance column for LOO / Δ

| CLI flag | Default (preset) | Role |
|----------|------------------|------|
| `--perf-metric` | `ppm` | Also **`points`** (season total, ESPN box), `minutes`, `bpm`, `obpm`, `dbpm`, … (`assign_perf_from_metric`). |
| `--no-perf-zscore-within-season` | off | If set, skip within-season z before LOO (non-default). |

**Reference implementations:** `pass_a_empirical_bundle.add_hero_spec_args`, `pd21_rho_hsort_calibrate.prepare_calibration_panel`, `panel_build.filter_panel`, `y_draft_mode.filter_team_seasons_min_games`.

Report **N** after each filter (survival table in provenance + optional `survival.csv`).

---

## Figures (v1)

**Not** replacements for reigning HERO PNGs. Write under a disposable sandbox, e.g.  
`sports_sandbox/_DISPOSABLE_delta_ppm_development/` or `sports/exports/delta_ppm_dev/`.

1. **Scatter or hexbin:** **`delta_dev`** (Δz, y) vs **`T_j`** (x), colored by `Y_draft`.
2. **Same y**, x = **`poolq_loo`** (parameter setting).
3. **Same y**, x = **`congestion_viable`** — **three panels** (O5: drafted median θ, global median θ, θ = 0).
4. **Companion:** `delta_minutes` vs same three x settings, or Δz vs x **within ventiles of `minutes_first`**.
5. **Optional binned means:** ventiles of x → mean Δz ± CI.
6. **Default overlays (v1.3):** **pooled** quadratic OLS \(\Delta \sim x + x^2\) on **all athletes** (`--fit-curves pooled-quadratic`, default). Optional **`split-quadratic`**: separate curves for `Y_draft=0` vs `1`. `--no-fit-curves` for scatter only. Coefficients in `provenance.json` → `meta.quadratic_fits_delta_dev` (`all` or `Y_draft_*` keys).
7. **Marginal Δ readout (v1.2):** each scatter has a **right-margin histogram** of \(\Delta\) plus a **summary box** (N, mean, P(\(\Delta\)>0), by `Y_draft`); standalone `delta_dev_marginal_{metric}.png`; stats in `meta.delta_dev_summary`.

**Caption boilerplate:** Associational; exit-year peer measures on **filtered** rosters; \(\hat{T}_j\) **includes self**; Δz confounded by role, minutes, selection; not HS talent; not causal congestion on draft; fitted curves are **descriptive**, not causal peer effects.

---

## What this is NOT

- Not **\(B_i\)** or recruiting rank.
- Not **\(H_{\mathrm{sort}}^{\mathrm{entry}}\)**.
- Not the **hero** estimand (`P(Y=1)` binned on `poolq_loo` only).
- Not **score** **`S_i = A_i - \lambda L_C`** — unless a later explicit extension puts \(\Delta\) into an outcome equation with new auth.

---

## Implementation sketch (when authorized)

**Script:** `sports/scripts/mbb_delta_dev_exploratory.py`

```bash
PYTHONPATH=sports python sports/scripts/mbb_delta_dev_exploratory.py --preset reigning
PYTHONPATH=sports python sports/scripts/mbb_delta_dev_exploratory.py --ppm-zero-below-minutes 20 --min-minutes 0
```

1. `prepare_panel` → full player-season panel (box rebuild or 530 CSV).
2. `apply_perf_metric_for_analysis` on all rows (for LOO on last season).
3. Build **`first_last_chronological`** table: per `athlete_id`, join rows at `min(season)` and `max(season)` → `delta_dev`, minutes.
4. Attach **`poolq_loo`**, \(\hat{T}_j\), congestion on **last chronological** `(team_id, season)`.
5. Apply filters per **CLI** (not hardcoded); write **`delta_dev_panel.csv`** + PNGs + **`provenance.json`** (all flags, θ triple, survival N).

**Reuse:** `panel_build`, `y_draft_mode.restrict_to_last_season_rows` (for Mode B), `tier1_mechanism_vars`, BDP-style \(\hat{T}_j\) from `bdp_ai_tj_distributions` if already standardized.

**Do not** overwrite `player_season_panel_530.csv` or reigning `pass_a/` artifacts.

---

## Open decisions (Charles)

| # | Question | Default if silent |
|---|----------|-------------------|
| O1 | Raw vs z for Δ development | **Locked:** within-season **z each season, then subtract** (Charles 2026-10-08); extend to BPM / OBPM / DBPM later |
| O2 | X-axes for peer context | **Locked:** three settings — **`T_j`** (mean `perf`, **includes self**, **post-filter** roster), **`poolq_loo`**, **`congestion_viable`** (LOO share above θ) |
| O3 | Grain for first / last PS | **Locked:** chronological **global** first & last PS per athlete (**any team**); one row per athlete; transfer drill-down later |
| O4 | Congestion x-axis | **Locked under O2:** **`congestion_viable`** (hard LOO share); smooth σ optional sensitivity |
| O5 | θ for viable peers | **Locked:** run **all three** — drafted median, global median (filtered panel), fixed **θ = 0** on within-season z `perf` |

---

## Thread log

| Date | Entry |
|------|--------|
| 2026-10-08 | Initial spec from Charles: ΔPPM first@school → last@school vs \(\hat{T}_j\), LOO, congestion; minutes as opportunity; scatter with `Y_draft`; exploratory only. |
| 2026-10-08 | **O1 locked:** Δ = within-season z(metric) at last − z at first@school; plan PPM then BPM / OBPM / DBPM same pattern. |
| 2026-10-08 | **O2 locked (C+):** All three x settings; \(\hat{T}_j\) includes self on filtered exit-season roster; LOO and viable-above-θ separate parameters. |
| 2026-10-08 | **O3 locked:** first PS = earliest recorded season (any team); last PS = latest; one row per athlete; transfer filters deferred. |
| 2026-10-08 | **O5 locked:** all three θ rules for `congestion_viable` (drafted median, global median, fixed 0). |
| 2026-10-08 | Filters: all reigning-style knobs as **CLI options** (mg, min minutes, winsor, DFT, ppm-zero-below-minutes, etc.); `--preset reigning` optional. |
| 2026-10-08 | **Implemented** `mbb_delta_dev_exploratory.py`; smoke run reigning preset → ~16k athletes, `delta_dev_panel.csv` + PNGs + `provenance.json` / `survival.csv` under `--out-dir`. |
