# Tier 1 roadmap (SCOUT / VECTOR) — living checklist

**Location:** `sports/documents/tier_1_roadmap.md` (alongside other sports-facing notes; not a duplicate of theory memos in `5-Manuscript`.)

**Notebook:** `sports/535_sports_tier_1.ipynb`

**Purpose:** Single place for the mechanical pipeline, the `df` column contract after each stage, and **CELL 0** switches. Update this file as CELL 4+ and modeling land.

**Contract (what “must be true” for implementation):** this file + the **module docstrings / function contracts** in `sports_pipeline/tier1_mechanism_vars.py` and `sports_pipeline/panel_build.py` (especially LOO / `poolq_loo` behavior). Manuscripts in `5-Manuscript` are **design intent and exposition**, not the execution contract unless we explicitly mirror a rule here.

**Related theory (`5-Manuscript`, stay at source — link, don’t copy):**

- `Vector_to_Scout_Tier1_Modeling_Direction.md` — main Tier 1 modeling direction.
- `tier_1_model.md` — model layer notes.
- `Tier1_Brifing_Outline.md` — outline answering Alex's May 5 briefing guidance: model components, assumptions, fitting plan, and turning point.
- `2026_0430_Paper7_feedback.md` — theory vs minimal model; scarcity.

Optional depth (broader VECTOR notes): `Vector_Master_Theory_and_Modeling_Notes*.md`, `Vector_Questions_and_Modeling_Thoughts.md`, `Vector_Evans_Reaction_and_Theoretical_Expansion_Notes.md` — pull excerpts into this roadmap only when a line becomes a **coded rule** or sample definition.

---

## Where We Have Been / Where We Are Going

Keep this section open while working in `535_sports_tier_1.ipynb`. Green items are done/validated; black/default items are next work or open decisions.

### Done / Validated

- <span style="color: green;">DONE — Mechanical notebook structure:</span> `535_sports_tier_1.ipynb` now follows the named-cell pattern: markdown header, then code cell with matching first comment line.
- <span style="color: green;">DONE — CELL 0 switchboard:</span> run gates and main knobs live in CELL 0 (`RUN_CELL1`–`RUN_CELL4`, `PERF_METRIC`, `PRIMARY_POOL_MODE`, `COMPUTE_WEIGHTED_CROWDING`, etc.).
- <span style="color: green;">DONE — 530 source-of-truth workflow:</span> exact 530 reproduction requires running `530_sports_pipeline.ipynb` from scratch with `use_prebuilt_panel_csv=False` and `export_panel_after_run=True`, then loading the refreshed `datasets/mbb/player_season_panel_530.csv` in 535.
- <span style="color: green;">DONE — Reproduced the reduced-form phenomenon:</span> with the refreshed 530 panel, `poolq_loo` binned bars reproduce the inverted-U / top-bin-drop pattern.
- <span style="color: green;">DONE — Plot-style switch:</span> CELL 4 supports `CELL4_EDA_PLOT_STYLE = "poolq_line"` vs `"bins_bars_520"` so we can compare quality-scale lines with 530-style bin-index bars.
- <span style="color: green;">DONE — Tier 1 mechanism variables:</span> CELL 3 creates `congestion_quality`, `congestion_crowding`, and, when enabled, `congestion_crowding_weighted`.
- <span style="color: green;">DONE — Weighted crowding behavior made explicit:</span> when `PRIMARY_POOL_MODE = "crowding"` and `COMPUTE_WEIGHTED_CROWDING = True`, CELL 4 plots `congestion_crowding_weighted`; when the boolean is false, it plots plain `congestion_crowding`.
- <span style="color: green;">DONE — First Tier 1 EDA pass:</span> binned bars for `congestion_quality`, plain `congestion_crowding`, and weighted crowding have been compared against the original `poolq_loo` pattern.

### Next / TODO

- TODO — Decide the Tier 1 core variables: likely start with `congestion_quality` and plain `congestion_crowding`; treat `congestion_crowding_weighted` as exploratory unless it earns a clearer interpretation.
- TODO — Fix or demote the right-panel dashed model curve: current clipped LPM / PD-style curves can be misleading; print unclipped predictions and coefficients before trusting the curve.
- TODO — Add a cleaner CELL 5 regression block: start with `Y_draft ~ Q + Q² + C + minutes`, then test `Q + C + Q*C + minutes` and appropriate robustness specs.
- TODO — Decide binning defaults by purpose: use `equal_width` when matching a 530 export slug; use `quantile` first for Tier 1 mechanism diagnostics so bins are populated.
- TODO — Add export behavior for 535 figures/tables only after the Tier 1 specs settle enough to save reproducible outputs.
- TODO — Update theory language after EDA: distinguish reduced-form `poolq_loo` from mechanism variables (`quality`, `crowding`, weighted crowding).

---

## Pipeline (numbered)

1. **Load the panel** — `load_panel(CFG)` → `df` from `player_season_panel_530.csv` at **workspace root** `datasets/mbb/` (via `sports_pipeline.paths.panel_530_csv()`). For exact 530 reproduction, refresh this CSV first by running **530** from scratch with `use_prebuilt_panel_csv=False` and `export_panel_after_run=True`.

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

5. **CELL 4 — Tier 1 EDA** (notebook): On a sample with valid **`PRIMARY_POOL_MODE`** pool column, **`congestion_crowding`**, **`minutes`**, **`Y_draft`**: descriptive `describe()`; **binned** mean draft vs Q using **`assign_poolq_bin_labels`** with **`CFG.ventiles`** and **`CFG.poolq_binning`**; numpy **LPM** `Y ~ 1 + Q + Q²`; multivariate linear `Y ~ 1 + Q + Q² + C + minutes` when Q is quality (if Q is crowding, **omit duplicate C**); **PD-style** predicted curve over a Q grid with C and minutes at sample medians (linear approx, clipped to [0,1]). When `PRIMARY_POOL_MODE="crowding"` and `COMPUTE_WEIGHTED_CROWDING=True`, the binned Q variable is `congestion_crowding_weighted`; otherwise it is plain `congestion_crowding`.

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
| ------ | ------ | ------ |
| Run gate | `RUN_CELL1` | Environment · imports · panel path |
| Run gate | `RUN_CELL2` | Load panel · PPM · legacy `poolq_loo` |
| Run gate | `RUN_CELL3` | Tier 1 mechanism variables |
| Run gate | `RUN_CELL4` | Tier 1 EDA (bins, LPM, PDP-style Q grid) |
| Knob | `PERF_METRIC` | Passed to `assign_perf_from_metric` (default `"ppm"`) |
| Knob | `CELL4_MATCH_530_VENTILE` | `True` = 530-style `poolq_loo`; `False` = Tier 1 mechanism variable path |
| Knob | `CELL4_EDA_PLOT_STYLE` | `"poolq_line"` vs `"bins_bars_520"` |
| Knob | `MIN_MINUTES_TIER1` | Optional row filter before Tier 1 group stats; `None` = full sample |
| Knob | `PRIMARY_POOL_MODE` | `"quality"` vs `"crowding"` for Tier 1 CELL 4 path |
| Knob | `COMPUTE_WEIGHTED_CROWDING` | Whether to build `congestion_crowding_weighted`; when `PRIMARY_POOL_MODE="crowding"`, `True` makes CELL 4 plot weighted crowding |

*Pattern matches **`540_tenure_pipeline.ipynb`** CELL 0: one switchboard, re-run after changes.*

---

## Next (placeholder)

- **CELL 5+:** proper logit / `statsmodels`; cluster SEs; season or team FE; richer PDP; export figures to `CFG.exports_dir` if you want parity with **530** PNG exports.

---

## Changelog

| Date | Note |
| ------ | ------ |
| 2026-05-06 | Added manuscript briefing outline link for Alex's May 5 guidance: model components, assumptions, fitting plan, and \(Q^*\) turning point. |
| 2026-05-05 | Added “Where We Have Been / Where We Are Going” dashboard; documented 530 source-of-truth workflow and weighted-crowding CELL 4 behavior. |
| 2026-05-06 | **CELL 4** in 535: binned draft vs Q, quadratic LPM, C + minutes controls, PDP-style Q grid; `RUN_CELL4` in CELL 0. |
| 2026-05-06 | `paths.project_root` = Ivy_Net workspace root so `datasets/mbb/` matches 530 output (not `sports/datasets/mbb/`). |
| 2026-05-05 | File lives under `sports/documents/`; contract vs theory section + links to `5-Manuscript`. |
| 2026-03-31 | Initial file: pipeline steps, recompute rationale, `df` contract, CELL 0 table. |
