# VECTOR handoff — all text in one file (browser / ScholarGPT)

**For Charles:** Vector **cannot** open your Cursor workspace or `current_documents/` paths. Deliver this file by **uploading it** in the browser chat **or** pasting **its full contents**.  

**Figures are not inside this file.** In the same browser message, **attach** (or describe if attach fails):
1. **Army:** the **Q1–Q8 final CIF** bar chart PNG (eight bins, y-axis “Final CIF” or equivalent).  
2. **College:** the **mean draft rate by ventile** bar chart PNG (`Mean draft rate by ventile of poolq_loo…`, eight bins).

**For Vector:** Everything below is the **complete** evidence package (Army brief + Coda sync + Scout basketball brief). Draft the **email to Brian MacDonald** using Charles’s outline: **intro** (nested pools, middle hierarchy, elite-tier scarcity) → **paragraph 1 Army** → **paragraph 2 college** → **paragraph 3 interpretation + related work**. Keep **estimands distinct** (promotion CIF in bins vs mean draft rate in bins); claim **parallel qualitative shape**, not identical causal structure.

---

# PART 1 — Coda: Vector brief (Army evidence for Brian memo)

*(Source file: `Coda_Vector_Brief_Army_Evidence_For_Brian_Memo.md`)*

# Vector brief: Army evidence package (for Brian MacDonald message & paper)

**Prepared by:** Coda (Army data / `520` thread)  
**Audience:** Vector (drafting external memo) + Charles  
**Use:** Merge with **Scout’s** basketball brief so one coherent note to Yale / ESPN colleague.

---

## A. One-sentence bridge

We document a **hump-shaped** relationship between **leave-self-out peer pool quality** and **promotion** in a **rank-ordered internal labor market** (Army), then show a **similar qualitative shape** using **public** college basketball data and **NBA draft** incidence.

---

## B. Suggested **second paragraph** draft (Army only — Vector: edit for tone)

*Draft text; confirm numbers with Charles’s final tables.*

In the Army officer data, we study promotion to **Major** (with **attrition** as a competing risk in the full pipeline). Pool quality is constructed so that each officer’s **peer pool mean excludes that officer’s own contribution**—the same **leave-one-out** logic Charles uses verbally as “pool minus mean” (meaning **without** self in the mean). We summarize **promotion** outcomes within **ordered bins** of that pool measure. The **competing-risks** displays include **final promotion incidence** by bin; in the **eight-bin** panel shared with advisors, estimated **final promotion incidence** is **lowest** in the **lowest** pool-quality bins, **rises** through the **middle** of the distribution, and **falls** again in the **highest** pool-quality bins—consistent with **stronger payoffs to pool quality in the middle of the hierarchy** and **diminishing returns** (or **congestion**) when peer pools are extremely strong. Full estimation uses a **time-varying** survival panel and Cox-style modeling elsewhere in the dissertation pipeline; the **bar panel** is a **transparent stratified summary** intended to mirror how we **read** the basketball **draft-rate-by-ventile** figure.

---

## C. Interpretation hooks (third paragraph — Army-side angles for Vector)

Vector can blend these with Scout’s basketball interpretation:

1. **Congestion / scarce slots:** At the **top** of the peer-quality distribution, **relative rank** may matter more than **absolute** peer strength; **promotion rates** need not increase monotonically in pool quality.
2. **Signal vs noise:** Very high-quality pools may **compress** observable performance differences, weakening the **signal** of individual accomplishment for boards.
3. **Selection:** Officers sorted into **elite** peer groups may differ on **unobservables**; the figure is **descriptive** at the bin level unless the paper’s models **adjust** further.
4. **Non-transferable literal equality:** Army **final CIF** and college **mean draft rate** are **different estimands**; the claim is **parallel curvature**, not identical magnitudes or causal structure.

---

## D. “Anyone else?” (Vector: web / lit check, not Coda’s specialty)

Coda does not maintain a literature database here. **Vector** should run a targeted scan for:

- **Peer effects** and **tournament** / **rank** models in **labor** and **organizations**;
- **Sports** draft prediction and **teammate quality** (NBA combine, college analytics blogs, academic SSRN/RESTUD-style labor);
- **Relative performance** in **internal** labor markets (military, police, firms).

Charles’s Yale contact may know **ESPN-era** analogues (draft models, RPM/BPM contexts) even if academic cites are thin.

---

## E. Tenure / academia (forward pointer)

If the **third setting** is tenure: specify **pool** (department peers? field cohort?) and **leave-self-out** construction **before** coding. Army **OER pools** and basketball **rosters** are both **closed teams**; academia’s “team” boundary is **design-critical**.

---

## F. Files Vector should have alongside this note

- Scout’s **mirror** brief (basketball data, ppm, ventiles, filters, **2011–2021**, **min minutes**, **no team draftee restriction** for the figure Charles sent).
- Optional figures: Army **Q1–Q8** final CIF bar panel; college **mean Y_draft** by bin.

---

*End Vector brief (Army).*

---

# PART 2 — Coda: Post-replication sync (Scout & Vector)

*(Source file: `Coda_Summary_For_Scout_and_Vector_Post_Replication.md`)*

# Coda → Scout & Vector: Post-replication sync (Army thread)

**From:** Coda (Army / `520` Cox & competing-risks plotting thread with Charles)  
**Date:** 2026-04-02 (update as needed)  
**Purpose:** Align all three agents on what the Army side **did** and **showed**, now that Scout has reproduced the **inverted-U** pattern in college basketball.

---

## 1. Status

Charles and Scout replicated the **qualitative shape** of the Army finding in a **public, replicable** setting: draft propensity vs **leave-one-out teammate pool quality** in MBB. The parallel is **strategic and interpretive** (nested talent pools, congestion at the top), not a claim that promotion hazards equal draft odds.

---

## 2. Army setting (what Coda’s stack is built for)

- **Population:** U.S. Army officers observed after promotion to Captain; time-to-event is framed from that anchor through promotion to Major, attrition, or censoring (competing risks).
- **Core empirical pattern (paper / advisor narrative):** Upward mobility vs **peer pool quality** is **nonlinear**: stronger association in the **middle** of the pool-quality distribution, with **lower** estimated promotion incidence at the **highest** pool-quality bins—consistent with **scarce slots**, **congestion**, or **signal** stories at the elite tier.
- **Figure type Charles shared (CIF bar panel):** Eight ordered bins (**Q1–Q8**) on a **pool-quality** construct; **y-axis** = **final cumulative incidence** of **promotion** (promotion as the event of interest in the competing-risks display). The bars show a **rise** through the mid bins and a **drop** in the top bins (inverted-U / “elite tier” dip).

---

## 3. Pool-quality definition (Army — Charles’s clarification)

**Naming note:** “Pool minus mean” in Charles’s usage means **the pool mean computed without the officer’s own contribution** to that mean (leave-self-out / LOO logic on the rating pool), **not** “pool minus a fixed cohort mean” as a separate operation.

**Implementation detail:** Built from **OER / senior-rater** style inputs in the time-varying survival panel (`df_time_varying` → `df_cox`), with plotting in **`520_pipeline_cox_working.ipynb`** and **`cox_plot_helpers.py`**. For **competing-risks bar panels**, officers are **stratified** by binned pool quality; **within each bin** the display summarizes **promotion** incidence over follow-up (see earlier CR_AND_HR / pipeline notes: Cell-11-style curves are **nonparametric within-bin** summaries, not a Cox fit on pool inside that plot).

**What to stress to outsiders:** Each officer’s **bin** reflects **peers’** contributions to the pool measure **excluding self**; **own** rating is **not** averaged into **own** pool statistic by construction.

---

## 4. Code / document map (Army)

| Item | Role |
|------|------|
| `520_pipeline_cox_working.ipynb` | End-to-end Cox + Cell 11 plotting (KM / competing risks, binning, filters). |
| `cox_plot_helpers.py` | `plot_competing_risks_cif_bars`, palettes, `apply_unknown_group_by_filter`, etc. |
| `pipeline_config.py` / overrides (e.g. `pipeline_config_div_name.py`) | Plot specs, bin counts, filters. |
| `current_documents/Army_to_College_Basketball_Replication_Handoff.md` | Longer **replication design** handoff (still useful for history). |
| `current_documents/Agent_Read_First_Coda_Runbook.md` | Short runbook + copy-paste message to Scout. |

---

## 5. For Scout (what Coda needs you to mirror in prose)

Please keep your companion note **technical**: grain (**player–season**), **`poolq_loo`**, **`PERF_METRIC`** (e.g. **ppm**), **z-score within season** if used, **binning** (quantile vs equal-width, **n** bins), **winsorization**, **min minutes**, **team draftee restriction** on/off, **season window** (e.g. **2011–2021**), **`Y_draft`** definition (ever-draft v0), and **draft register / ESPN box** provenance. Charles’s **8-bin** college bar chart should be described **side-by-side** with the Army **Q1–Q8** panel for advisors.

---

## 6. For Vector (memo + Brian email)

- Use **`Coda_Vector_Brief_Army_Evidence_For_Brian_Memo.md`** (companion file) for **Army-only** bullets safe to merge with Scout’s basketball brief.
- Charles’s **intro** (nested pools, middle hierarchy, elite-tier scarcity) is the **shared frame** across Army and basketball; keep **estimands distinct** (promotion CIF in bins vs **mean draft rate** in bins).

---

## 7. Re: “Should Scout re-read the old Coda handoff only?”

**Recommendation:** Keep **`Army_to_College_Basketball_Replication_Handoff.md`** and the **runbook** as **reference** for pipeline archaeology and design intent. For **current alignment** after successful replication, **this file + `Coda_Vector_Brief_Army_Evidence_For_Brian_Memo.md`** are the **primary** updates—so Scout should read **those** in addition to (not instead of) the handoff if they need full Cox detail.

---

## 8. Next horizon (tenure / academia)

Charles noted a possible **third setting**: academic careers and tenure. Coda’s stack is **not** the vehicle for that; Vector + Charles should specify **grain** (person-year? department?), **pool** (LOO coauthor? department peers?), and **outcome** (tenure, placement). Army + basketball docs become **templates** for measurement discipline, not copy-paste code.

---

*End Coda summary.*

---

# PART 3 — Scout: Collegiate basketball background

*(Source file: `Scout_background_CBB_pool_quality_draft_rate.md`)*

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

## What Scout needs from CODA (for VECTOR)

- Exact **Army** estimand and sample: **Pool minus mean senior rater** definition, **CIF** horizon / competing risks setup, **Q1–Q8** bin definition, and **N** / event counts.
- One paragraph on **why** the college design is a **deliberate parallel** (nested pools, relative performance, scarcity at the top) without claiming identical institutions.

---

*Prepared for cross-sharing with CODA and VECTOR — Scout (college basketball / 530 pipeline).*

---

# END OF BUNDLE

If this bundle is updated, refresh the three source `.md` files in `current_documents/` separately and re-merge, or edit this file as the single source of truth for Vector.
