# Scout — Collegiate basketball background (for CODA, VECTOR, Brian MacDonald memo)

**Purpose.** Handoff summary of the **530** college-basketball pipeline and the **nonparametric ventile / bin** evidence that mirrors the **inverted-U / middle-tier payoff** pattern from the Army officer setting, using a **transparent, replicable** public-data design.

---

## Research question (aligned with Army)

Whether **upward mobility** (here: **NBA draft incidence**) depends on **relative standing within nested talent pools**, with **stronger marginal payoffs to pool quality in the middle of the hierarchy** and **flattening or reversal at the elite tail** where slots are scarce—analogous to promotion pressure and rank scarcity in a closed military ladder.

---

## Outcome and key regressor (college side)

- **Outcome:** `Y_draft` — **ever drafted** (binary at the player-season level; flag from NBA draft register linked to ESPN athlete ids via the project’s draft lookup).
- **Peer pool quality:** `poolq_loo` — **leave-one-out mean teammate performance** within **(team_id, collegiate season)** after choosing a **performance measure** copied into `perf`. LOO excludes the focal player so the regressor is not mechanically own performance.
- **Specification for the figure:** **`perf` = points per minute (`ppm`)** from **ESPN game-level box** aggregated to player-season-team totals.
- **Curvature / parametric check (elsewhere in pipeline):** quadratic **LPM** in `poolq_loo` and `poolq_sq` on the same filtered sample (not shown on the bar chart export).

---

## Data sources

1. **ESPN / sportsdataverse-style game-level box** → player-season-team panel (minutes, points, team, season, athlete id).
2. **NBA draft register** (`nbaplayersdraft`) + **draft–athlete match** → `athlete_id_draft_lookup` → **`Y_draft`**.
3. **Sports Reference BPM merge** (optional for other `perf_metric` runs); **not** required for the **PPM-only** figure described here.

---

## Sample and cleaning choices (for the basketball plot referenced)

| Choice | Setting |
|--------|--------|
| Collegiate seasons | **2011–2021** (panel construction and analysis window aligned in the run) |
| Minutes filter | **`min_minutes = 1`** (drop player-seasons below 1 minute before ventiles/LPM) |
| Team draftee restriction | **Off** — `restrict_teams_by_draftees=False` (no requirement that the team roster include a drafted player) |
| Binning on `poolq_loo` | **`poolq_binning = equal_width`**, **`ventiles = 8`** (eight equal-width bins on the observed range of `poolq_loo`) |
| Winsorization | **`poolq_winsor_quantiles = (0.05, 0.95)`** — after LOO, **`poolq_loo` clipped** to the 5th and 95th **empirical quantiles** of `poolq_loo` on the panel at that step (documented in ventile metadata); then `poolq_sq = poolq_loo²` |
| Ventile figure style | **`ventile_eda_plot_style = "bins_bars_520"`** — **bar chart only** vs bin index (1 = lowest teammate pool quality), y-axis **from zero**; full provenance block under the plot + `.txt` sidecar |

**Scale (typical of the reported run):** on the order of **~83k player-seasons** and **~45k unique athletes** in the modeling sample after filters; **~1.1k** player-seasons with `Y_draft=1` (order of magnitude **~1.4%** mean draft rate on the sample—exact counts in the exported provenance).

---

## Result (visual)

**Mean `Y_draft` by ventile of `poolq_loo` (PPM-based LOO):** draft rate **rises** from low to middle–upper bins, then **falls in the top bin** (8), producing a **hump-shaped** bin profile consistent with **stronger payoffs in the middle of the peer-quality distribution** and **weaker marginal returns (or selection) at the elite teammate-pool tail**.

---

## Reproducibility

Pipeline code: **`sports_pipeline/`** + **`530_sports_pipeline.ipynb`**. Exports: dated **`inverted_u_ventiles_*.png`**, **`binned_draft_rate_ventiles_*.csv`**, **`ventile_eda_provenance_*.txt`** under the configured **`exports_dir`**; filename slug encodes perf metric, binning (`_poolqeqwidth` for equal-width), optional z-score, team-draftee restriction, winsor (in metadata text), and bar style (`_ventilebars520` when used).

---

## Army parallel (for VECTOR — see Coda’s docs for detail)

Coda has supplied the matching **Army** thread for memos and Brian’s note:

- **`Coda_Summary_For_Scout_and_Vector_Post_Replication.md`** — estimand, leave-self-out pool definition (“pool minus mean” = mean **without** self), **Q1–Q8** final **promotion CIF** bars, competing-risks context.
- **`Coda_Vector_Brief_Army_Evidence_For_Brian_Memo.md`** — draft paragraphs + interpretation hooks.
- **`Vector_Browser_Package_FULL_TEXT.md`** — single browser upload for Vector with **Scout + Coda** text inlined.

**Parallel claim:** nested pools, relative standing, **hump / tail dip** in both settings — **not** identical magnitudes, institutions, or causal estimands.

---

*Prepared for cross-sharing with CODA and VECTOR — Scout (college basketball / 530 pipeline).*
