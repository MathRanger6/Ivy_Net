# Tier 1 roadmap (SCOUT / VECTOR) — living checklist

**Location:** `sports/documents/tier_1_roadmap.md` (alongside other sports-facing notes; not a duplicate of theory memos in `5-Manuscript`.)

**Notebook:** `sports/535_sports_tier_1.ipynb`

**Purpose:** Single place for the mechanical pipeline, the `df` column contract after each stage, and **CELL 0** switches. Update this file as CELL 4+ and modeling land.

**Contract (what “must be true” for implementation):** this file + the **module docstrings / function contracts** in `sports_pipeline/tier1_mechanism_vars.py` and `sports_pipeline/panel_build.py` (especially LOO / `poolq_loo` behavior). Manuscripts in `5-Manuscript` are **design intent and exposition**, not the execution contract unless we explicitly mirror a rule here.

**Related theory (`5-Manuscript`, stay at source — link, don’t copy):**

- `Vector_to_Scout_Tier1_Modeling_Direction.md` — main Tier 1 modeling direction.
- `tier_1_model.md` — model layer notes.
- `2026_0430_Paper7_feedback.md` — theory vs minimal model; scarcity.

Optional depth (broader VECTOR notes): `Vector_Master_Theory_and_Modeling_Notes*.md`, `Vector_Questions_and_Modeling_Thoughts.md`, `Vector_Evans_Reaction_and_Theoretical_Expansion_Notes.md` — pull excerpts into this roadmap only when a line becomes a **coded rule** or sample definition.

---

## Pipeline (numbered)

1. **Load the panel** — `load_panel(CFG)` → `df` from `player_season_panel_530.csv` at **workspace root** `datasets/mbb/` (via `sports_pipeline.paths.panel_530_csv()`, same as **530** conductor).

2. **Set `perf` from a metric** — e.g. PPM via `assign_perf_from_metric(df, PERF_METRIC)` with `PERF_METRIC` defined in **CELL 0**.

3. **Recompute legacy `poolq_loo` (and `poolq_sq`)** — `recompute_teammate_loo_pool_quality(...)`.

   **Why recompute instead of trusting the CSV?**

   - LOO pool quality must be built off the **`perf` you just chose**; a saved `poolq_loo` may reflect an older or different `perf` definition.
   - Optional **winsor** on `poolq_loo` via `CFG.poolq_winsor_quantiles` is applied in this step when set.

   **Comparison:** `poolq_loo` (legacy) and **`congestion_quality`** (Tier 1) can differ slightly when some roster rows have missing `perf`; the Tier 1 helper uses only rows with valid `perf` in the `(team_id, season)` group for denominators. See `sports_pipeline/tier1_mechanism_vars.py` module docstring.

4. **Add Tier 1 mechanism columns** — `add_tier1_mechanism_variables(...)`:

   - `congestion_quality` — LOO **mean** teammate `perf` (valid \(Q\) for Tier 1).
   - `congestion_crowding` — LOO **sum** teammate `perf`.
   - `congestion_crowding_weighted` — optional weighted variant (minutes × `perf` logic); gated by **CELL 0** `COMPUTE_WEIGHTED_CROWDING`.
   - If `MIN_MINUTES_TIER1` is set in **CELL 0**, rows below that **minutes** threshold are dropped **before** group stats.

5. **CELL 4 — Tier 1 EDA** (notebook): On a sample with valid **`PRIMARY_POOL_MODE`** pool column, **`congestion_crowding`**, **`minutes`**, **`Y_draft`**: descriptive `describe()`; **binned** mean draft vs Q using **`assign_poolq_bin_labels`** with **`CFG.ventiles`** and **`CFG.poolq_binning`** (530-style); numpy **LPM** `Y ~ 1 + Q + Q²`; multivariate linear `Y ~ 1 + Q + Q² + C + minutes` when Q is quality (if Q is crowding, **omit duplicate C**); **PD-style** predicted curve over a Q grid with C and minutes at sample medians (linear approx, clipped to [0,1]).

---

## `df` column contract (Tier 1–relevant)

**After steps 1–3 (after notebook CELL 2):**

- Required for assertions in the notebook: `Y_draft`, `poolq_loo`, `minutes`.
- Always present after recompute (when inputs allow): **`perf`**, **`poolq_loo`**, **`poolq_sq`**.
- Plus **all other columns** from the 530 CSV (identifiers such as `athlete_id`, `team_id`, `season`, and any merges from 530).

**After step 4 (after notebook CELL 3):**

- Same as above, **plus**: `congestion_quality`, `congestion_crowding`, and usually `congestion_crowding_weighted` (or NaNs if weighted path is off / invalid inputs).

---

## CELL 0 — variables / boolean switches (current)

| Kind | Name | Role |
|------|------|------|
| Run gate | `RUN_CELL1` | Environment · imports · panel path |
| Run gate | `RUN_CELL2` | Load panel · PPM · legacy `poolq_loo` |
| Run gate | `RUN_CELL3` | Tier 1 mechanism variables |
| Run gate | `RUN_CELL4` | Tier 1 EDA (bins, LPM, PDP-style Q grid) |
| Knob | `PERF_METRIC` | Passed to `assign_perf_from_metric` (default `"ppm"`) |
| Knob | `MIN_MINUTES_TIER1` | Optional row filter before Tier 1 group stats; `None` = full sample |
| Knob | `PRIMARY_POOL_MODE` | `"quality"` vs `"crowding"` for `tier1_primary_pool_column` (regressions later) |
| Knob | `COMPUTE_WEIGHTED_CROWDING` | Whether to build `congestion_crowding_weighted` |

*Pattern matches **`540_tenure_pipeline.ipynb`** CELL 0: one switchboard, re-run after changes.*

---

## Next (placeholder)

- **CELL 5+:** proper logit / `statsmodels`; cluster SEs; season or team FE; richer PDP; export figures to `CFG.exports_dir` if you want parity with **530** PNG exports.

---

## Changelog

| Date | Note |
|------|------|
| 2026-05-06 | **CELL 4** in 535: binned draft vs Q, quadratic LPM, C + minutes controls, PDP-style Q grid; `RUN_CELL4` in CELL 0. |
| 2026-05-06 | `paths.project_root` = Ivy_Net workspace root so `datasets/mbb/` matches 530 output (not `sports/datasets/mbb/`). |
| 2026-05-05 | File lives under `sports/documents/`; contract vs theory section + links to `5-Manuscript`. |
| 2026-03-31 | Initial file: pipeline steps, recompute rationale, `df` contract, CELL 0 table. |
