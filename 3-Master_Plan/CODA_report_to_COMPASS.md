# CODA → COMPASS: Handoff Report (Army / Talent Domain)

> **Rename (2026-06-11):** Formerly `CODA_report_to_master_planner.md`; planning agent is **COMPASS**. See [COMPASS_AGENT_IDENTITY.md](COMPASS_AGENT_IDENTITY.md).

**Agent:** **CODA** (Cursor agent; Army officer talent / OER / Cox–competing-risks research)  
**Domain root:** `./talent/` (canonical code: `talent/talent_pipeline/`; symlink at repo root: `talent_pipeline/` → same tree)  
**Report date:** 2026-06-08 (refresh for COMPASS feed-in)  
**Prepared for:** Charles Levine → future **COMPASS** agent (Cursor)  
**Charles’s explicit instruction (2026-06-08):** This report feeds the COMPASS. **Do not** begin drafting the cross-project master plan until Charles **assigns** that agent and asks for planning work. CODA/SCOUT/PEER/VECTOR should only **report status** until then.

---

## 0. What this document is (and is not)

### What it is
- A **ground-truth status snapshot** of the Army/talent lane as CODA understands it after the **April 2026** thread (AWS sync, TB-stratified CR add-on, pool-size concerns, documentation).
- A **research narrative** (§2) for a COMPASS with **zero prior context**: ranks, promotions, pool quality, competing risks, Cox models, and the **inverted-U** finding — plus how Army links to SCOUT and PEER.
- A **file map** so the COMPASS can navigate without re-deriving context from chat logs.
- A **list of open questions** where Charles’s intent is not fully locked — CODA prefers explicit answers over assumptions.
- Pointers to **SCOUT** (basketball), **PEER** (tenure), and **VECTOR** (manuscript) without claiming authority over those domains.

### What it is not
- **Not** the master plan itself.
- **Not** a commit to merge Army code paths with sports/tenure implementations (those are parallel settings with shared *ideas*, different estimands and data).
- **Not** a guarantee that every local file has been pushed to Army AWS live — Charles transcribes/uploads manually; see §4.

---

## 1. Thesis frame (why CODA exists in this repo)

Charles’s dissertation uses **three empirical settings** under one mechanism story:

| Setting | Agent (Charles’s naming) | Repo home | Outcome / mobility | Pool-quality construct |
|--------|---------------------------|-----------|---------------------|-------------------------|
| 1 — Army | **CODA** | `talent/` | Promotion to Major vs attrition (competing risks) | Senior-rater / OER pool minus mean (LOO-style), binned for CIF panels |
| 2 — Basketball | **SCOUT** | `sports/` | NBA draft (ever-draft v0, etc.) | LOO teammate pool quality (`poolq_loo`, generative extensions) |
| 3 — Academia | **PEER** | `tenure/` | Tenure (Asst → Assoc) | LOO department prestige / pub intensity bins |

**CODA’s job:** Make the Army pipeline **correct, documented, advisor-ready**, and **honest about estimands** (what a CIF bar *means* vs what a Cox HR *means*). The inverted-U / “middle pool wins, elite pool dips” narrative is the **qualitative target** linking all three settings; Army is the **most mature** quantitative stack (520 Cox + Cell 11 plotting).

**VECTOR’s job (for COMPASS awareness):** Turn cross-setting evidence into manuscript prose (`1-Various_PDE_and_Chat_stuff/5-Manuscript/` — e.g. `Vector_to_Scout_Tier1_Modeling_Direction.md`, `PEER_Status_Update_for_VECTOR_2026-06-03.md`, Dakota committee brief). CODA supplies Army methods/results bullets; does not own VECTOR’s outline.

---

## 2. Army research program — zero-background primer

*This section is for a COMPASS who has never seen the Army data or Charles’s dissertation thread. Status, files, and open tasks are in §3 onward.*

### 2.1 Research question (plain English)

Charles studies whether **the quality of your peer rating pool** — the average performance of other officers evaluated by the same senior rater around the same time — predicts **upward mobility** (promotion) in a hierarchical performance system. The surprise is not a simple “better pool → always better outcomes” story. The empirical signature is an **inverted U**: promotion probability **rises** as pool quality increases through the middle of the distribution, then **falls** at the very highest pool-quality tiers (“elite pool” dip). That pattern is the **qualitative target** linking Army (Setting 1), college basketball draft (Setting 2, SCOUT), and academic tenure (Setting 3, PEER).

**Mechanism hypotheses (still being articulated — see `Publication_Plan.md`):** scarce promotion slots, congestion among high performers, signal dilution when everyone in the pool is strong, or comparative standing effects. Army is the **most mature** quantitative implementation; basketball has **replicated** the shape; tenure is **preliminary**.

### 2.2 Setting, ranks, and outcomes

| Element | Army implementation |
|--------|---------------------|
| **Population** | U.S. Army officers, typically **Combat Support / Combat Service Support** cohorts in year groups such as **2002–2012** (run-specific filters in `pipeline_config*.py`) |
| **Rank anchor** | Observation begins after promotion to **Captain (CPT)**; time-to-event is measured from that career anchor |
| **Primary mobility outcome** | Promotion to **Major (MAJ)** |
| **Competing outcome** | **Attrition** (separation before MAJ promotion — officers who attrite are no longer at risk for promotion) |
| **Performance signal** | Officer Evaluation Reports (OERs); **top block (TB)** share — how often an officer receives the highest rating category |
| **Pool construct** | **Senior-rater pool**: officers sharing the same senior rater (and snapshot timing) form a reference peer set. **Pool quality** ≈ mean TB of peers in that pool, computed **leave-one-out** (officer’s own rating excluded from the pool mean Charles calls “pool minus mean”) |
| **Data** | Proprietary Army personnel snapshots + OER records; **cannot be shared publicly**. Pipeline: **502** (snapshots) → **512** (OER assignment) → **520** (pool metrics, survival, plots, Cox) |

**Why ranks matter:** The dissertation is about **advancement under constrained distinction** — who gets promoted when slots are scarce and everyone is rated relative to peers. CPT→MAJ is the canonical Army mobility run; attrition is treated as a **competing event**, not ignored censoring.

### 2.3 Two analysis layers (do not conflate them)

Charles uses **two complementary tools** on the same underlying panel. COMPASS and VECTOR must keep estimands distinct in manuscript language.

#### Layer A — Cell 11: Competing-risks **descriptive** plots (signature figures)

- **What:** Nonparametric **cumulative incidence function (CIF)** curves and **CIF bar panels** (e.g. **Q1–Q8** ordered bins on pool quality).
- **Y-axis (promotion bars):** **Final cumulative incidence** of promotion to MAJ — the share of officers in each pool-quality bin who have been promoted by end of follow-up, treating attrition as a competing risk in the display.
- **Signature finding:** Bars **rise** through mid bins, then **drop** in top bins → **inverted U** / elite-tier dip. Holds with **8 and 25** equal-width bins in Army runs.
- **Honest implementation notes** (see `CR_Red_Line_Flow_Explanation.md`, §6.2 below): plot bins use each officer’s **last snapshot** for the binned variable; Cell 11 CIF uses a **simple cumulative proportion** estimator, not full Aalen–Johansen with dynamic risk sets. These are **within-bin empirical summaries**, not Cox-fitted curves.

#### Layer B — Cell 12: **Cox proportional hazards** models (inferential)

- **Software:** `scikit-survival` (`sksurv`) — `CoxPHSurvivalAnalysis`, concordance, partial effects.
- **Event framing:** **Cause-specific Cox** for promotion: officers who attrite are censored at attrition time for the promotion model (and vice versa for attrition models). Cell **12.5** fits **separate** promotion and attrition Cox models and compares coefficients.
- **Competing-risks literature:** Fine–Gray **subdistribution hazard** models are part of the standard toolkit Charles knows; the **current 520 stack implements cause-specific Cox + empirical CIF**, not Fine–Gray regression in code. If manuscript claims Fine–Gray explicitly, confirm implementation first or frame as related estimand family.
- **Typical covariates (example run — CS/CSS, YG 2002–2012):** standardized **own TB ratio** (forward, senior-rater context), standardized **pool minus mean** (forward), **quadratic** terms on both, and **TB × pool interaction**. Documented in `Pertinent_Thoughts.md` § Cox Model Results.

**Example Cox findings (promotion model, one documented run):**

| Predictor | Direction / shape | Illustrative magnitude |
|-----------|-------------------|-------------------------|
| Own TB ratio (z) | Strong **positive** on promotion hazard | HR ≈ **10.4** per SD |
| Pool minus mean (z) | **Negative** on promotion hazard (comparative/competitive) | HR ≈ **0.34** per SD |
| Squared terms (TB, pool) | Significant **negative** quadratics | Supports **curvature** / inverted-U shape in hazard scale |
| TB × pool interaction | Significant | Effect of own performance depends on pool context |

All terms significant at conventional levels in that run (p < 0.001). Squared terms and interaction justify the **nonlinear** story that the CIF bar panels visualize descriptively.

**Conceptual bridge:** Cell 11 answers “what does the **binned promotion curve** look like by pool quality?” Cell 12 answers “controlling for own performance and time, what are the **hazard ratios** and **partial effect curves**?” See `CR_AND_HR_FOR_DUMMIES.md` for CIF vs hazard vs HR in plain English.

### 2.4 Key constructs glossary (Army)

| Term | Meaning |
|------|---------|
| **TB (top block)** | Highest OER rating category; often summarized as forward-looking TB **ratio** or share |
| **Senior rater (SNR)** | Senior evaluator whose pool defines peer reference set |
| **Pool minus mean** | LOO pool mean TB — peers’ average excluding self (Charles’s naming; not “minus a fixed cohort mean”) |
| **OPM** | Own performance measure relative to pool (pipeline has multiple fwd/bwd variants) |
| **Competing risks** | Promotion and attrition compete; one precludes the other |
| **CIF** | Cumulative incidence of an event by time t |
| **Inverted U** | Mobility rises with pool quality, then falls at top pool-quality bins |

### 2.5 Cross-domain replication status (June 2026)

| Setting | Agent | Outcome | Pool construct | Inverted-U status |
|---------|-------|---------|----------------|-------------------|
| Army officers | **CODA** | CPT→MAJ promotion (vs attrition) | Senior-rater LOO pool TB | **Established** — CIF bars + Cox quadratics |
| College basketball | **SCOUT** | NBA draft (ever-draft) | LOO teammate pool quality (`poolq_loo`) | **Replicated** qualitative shape |
| Academic tenure | **PEER** | Asst → Assoc tenure | LOO dept pub intensity / prestige | **Preliminary** (stage 9, dirty-OK) |

Charles’s dissertation bar requires **all three settings** in one manuscript (§10). The parallel is **strategic** (nested talent pools, congestion at the top), not a claim that promotion hazards equal draft odds or tenure probabilities.

**Primary cross-agent docs:** `Publication_Plan.md` §0, `Coda_Summary_For_Scout_and_Vector_Post_Replication.md`, `5-Manuscript/advancement_under_constrained_distinction_dakota_feedback_v03.rtf`.

### 2.6 Advisor-facing extensions (April 2026)

- **Own-TB stratified CR reruns** (`cr_tb_stratify.py`): same pool-binned inverted-U plots, but restricted to tertiles of **own** TB (low/med/high performers). Tests whether the pool-quality pattern differs by own rating level. Default **off**; see `CR_TB_STRATIFY_Advisor_Three_Panels.md`.
- **525 / UIC work (planned):** Link pools to divisions, brigades, battalions — which units and senior raters consistently run high-TB pools. Not April 2026 focus; see `525_plans.md`.

### 2.7 Where to read more (research, not just status)

| Document | Content |
|----------|---------|
| `talent/documents/Publication_Plan.md` | Research summary, inverted-U, replication status, mechanism/venues roadmap |
| `talent/documents/CR_AND_HR_FOR_DUMMIES.md` | CIF vs Cox vs HR; quadratics; competing risks worked examples |
| `talent/documents/520_PIPELINE_COX_OVERVIEW.md` | Full 520 pipeline map (Cells 1–12) |
| `talent/documents/Pertinent_Thoughts.md` | Cox result prose, senior-rater pool algorithm notes |
| `talent/documents/advisor_brief_twofold_status.md` | Advisor-facing status (525 vs publication) |
| `talent/documents/Coda_Vector_Brief_Army_Evidence_For_Brian_Memo.md` | Army bullets for VECTOR / committee |
| `.specstory/history/` | Portable chat logs if prose detail is missing from markdown |

---

## 3. Current status — Army / talent (high level)

### Established / working
- **`520_pipeline_cox_working.ipynb`:** End-to-end pipeline from filtered snapshots through Cox-ready intervals, Cell 10.5 z-score/quadratic/interaction, Cell 11 KM + **competing risks** + **CIF bar panels**, Cell 12 Cox models.
- **Inverted-U style figures:** Pool-quality binned CR + final CIF bars (e.g. Q1–Q8) are the advisor-facing signature plot type.
- **Run profiles / overrides:** `pipeline_config.py` + overrides such as `pipeline_config_19_1.py`, `pipeline_config_div_name.py` via `pip_config_file` / `expand_run_profile()`.
- **Documentation cluster** under `talent/documents/` (see §7).

### Recently completed (April 2026 thread — CODA + Charles)
1. **AWS export overlay:** Files from `talent/Army_AWS_download/TALENT_NET_export_20260421-0802/` copied into `talent/talent_pipeline/`; TB-stratify pieces re-merged afterward.
2. **Pre-overlay backup:** Full `talent/` tree copied to `obsolete_files/talent_pre_bar_stratify/talent/`.
3. **Ground-truth policy (Charles decision):** Everything **outside** `Army_AWS_download/` is authoritative for local work; AWS folder is **comparison snapshot only** until Charles uploads to live Army environment.
4. **Advisor add-on — own-TB stratified CR reruns:** `cr_tb_stratify.py` + `CR_TB_STRATIFY_CONFIG` + Cell 11 hook. Re-runs **competing_risks** (+ CIF bars when enabled) for low/med/high **own TB** strata (last snapshot per officer). Default **`enabled: False`**.
5. **`stratum_method`:** `quantile` (equal-N tertiles) vs `equal_width` (equal range on TB/z scale) — implemented in `cr_tb_stratify.py`; config key in `pipeline_config.py`.
6. **Plot labeling / filenames for TB-stratify runs:** `cr_tb_stratify_title_suffix` on titles/metadata; filename tokens `_tbq_` / `_tbew_` + stratum to avoid overwrites.
7. **Interpretation doc:** `CR_Red_Line_Flow_Explanation.md` — plain English for Cell 11 CR curve construction (last row per officer for plot bins; cumulative not instantaneous).
8. **Pool-size concern documented:** `Pertinent_Thoughts.md` § Senior Rater Pools — `pool_size_snr_*` can exceed 100 under current `(snapshot_date, snr_col)` grouping; likely **definition vs intuition**, not necessarily bad data.

### Not done / open
- **Upload to Army AWS live** of the 4-file change set (Charles action).
- **Enable and validate TB stratify on AWS** (`CR_TB_STRATIFY_CONFIG["enabled"] = True`, run Cell 11, check “TB-stratified CR add-on: X created, Y skipped”).
- **Senior rater pool algorithm audit** — Charles believes >100 pool sizes may be impossible for “true” boards; code groups differently (see §6).
- **`525` / UIC consistency work** (`525_plans.md`) — still planned, not CODA’s April focus.
- **Formal master plan** — explicitly deferred until Charles assigns COMPASS.

---

## 4. AWS upload checklist (Charles → live Army coding environment)

Compared byte-for-byte to `TALENT_NET_export_20260421-0802`, these **live** files differ and should be uploaded:

| File | Role |
|------|------|
| `520_pipeline_cox_working.ipynb` | Cell 11 + TB-stratify hook |
| `pipeline_config.py` | `CR_TB_STRATIFY_CONFIG` (+ rest of config) |
| `cox_plot_helpers.py` | TB-stratify title suffix in `format_plot_title` / config text |
| `cr_tb_stratify.py` | **New module** (not in export folder) |

**Unchanged vs export (example Charles asked about):** `cox_plt_chnge.py` — identical; no upload needed for that file.

**After upload:** Note in lab notebook: aligned to export **20260421-0802** + TB-stratify add-on + `stratum_method`.

---

## 5. Workflow constraints (critical for COMPASS)

### Army AWS environment
- Charles often **transcribes by hand** into a locked-down JupyterLab on Army AWS (no casual copy/paste).
- Local Cursor repo is the **authoring** environment; AWS is **deployment**.
- SpecStory history (`.specstory/history/`) is intentionally tracked for **portable agent conversations** — Charles does **not** want SpecStory history ignored in git.

### Git / branches (Charles learning git — April 2026)
- Local `main` and `origin/main` had **diverged** around Rivanna workspace + SpecStory `.gitignore` commits vs later talent commits.
- Charles prefers **feature branches** for focused work; avoid mixing Rivanna workspace tweaks with science PRs when possible.
- CODA does **not** own repo-wide git policy — flag for COMPASS if cross-agent commit hygiene matters.

### Config reload pattern
- Cell 0 / `reload_pipeline_config()` — changes to `pipeline_config*.py` require reload or kernel restart before Cells 10+.

---

## 6. Technical deep dives the COMPASS should know

### 6.1 Own-TB stratification (advisor add-on)

**Intent:** Same pool binning and timeline as main CR plots, but **restrict officers** to tertiles of **own** TB (default `z_tb_ratio_fwd_snr` on **last** interval per `pid_pde`). Produces up to **3×** parallel CR + CIF bar outputs per `competing_risks` plot spec.

**Docs:** `talent/documents/CR_TB_STRATIFY_Advisor_Three_Panels.md`

**Enable:**
```python
CR_TB_STRATIFY_CONFIG["enabled"] = True
# optional: CR_TB_STRATIFY_CONFIG["stratum_method"] = "equal_width"
```

### 6.2 Cell 11 CR curves — estimand honesty

**Key implementation facts** (see `CR_Red_Line_Flow_Explanation.md`):
- `prepare_plot_data` collapses to **`groupby('pid_pde').last()`** before binning the plotted variable → **final snapshot** OPM/TB for **plot_group** assignment.
- `calculate_cif` uses a **simple cumulative proportion** estimator, **not** full Aalen–Johansen with dynamic risk sets.
- **Own-TB strata** (add-on) filter **which officers** enter each rerun; **within-panel pool bins** still come from the plot spec’s `variable` / `n_bins`.

COMPASS should ensure manuscript language matches **implemented** estimands, not idealized “snapshot 11 landmark” language unless the data pipeline is changed to that.

### 6.3 Senior rater pool size > 100

**Charles concern:** Pool sizes over 100 seem impossible for real senior rater boards.

**CODA code reality** (`add_cum_oer_metrics_mod_working.py`):
- Pools grouped by **`[snapshot_date_col, snr_col]`** on the long snapshot frame.
- `pool_size_*` with `exclude_self=True` reflects effective denominator for pool mean.
- Large sizes can occur if `snr_col` is broad (org/UIC/key), many officers share snapshot date, or many rows survive joins — **not** necessarily “one OER board headcount.”

**Documented in:** `talent/documents/Pertinent_Thoughts.md` (§ Senior Rater Pools, code-linked notes).

**Recommended audit when Charles returns:** Tabulate top `pool_size_snr_fwd`; for each group report `snr_col`, date, `nunique(pid_pde)`, `yg`, `div_name`; confirm `CELL6_COLUMN_MAPPING` for `snr_col`.

**Cross-domain note for COMPASS:** SCOUT and PEER have their own pool definitions (`poolq_loo`, dept LOO prestige). Harmonize **language** (“reference peer set at time t”) not necessarily **identical code**.

### 6.4 Cell 10 warning about missing model TV columns

Message like: `Model-only time-varying missing from snapshot data: ['z_tb_ratio_fwd_snr', ...]`

**Usually expected:** z-scores, squares, interactions are created in **Cell 10.5**, not on raw snapshots in Cell 10. Run 10.5 before Cell 12 model fitting.

---

## 7. CODA document inventory (updated April 2026)

| Document | Purpose | Updated this thread? |
|----------|---------|----------------------|
| `talent/documents/Pertinent_Thoughts.md` | Dissertation ideas + **Senior Rater Pools** section | Yes |
| `talent/documents/CR_TB_STRATIFY_Advisor_Three_Panels.md` | TB-stratify feature guide | Yes (this pass) |
| `talent/documents/CR_Red_Line_Flow_Explanation.md` | Cell 11 CR / red-line flow | Yes (created earlier) |
| `talent/documents/README_Talent_Layout_Symlinks_And_AWS_Export.md` | Paths, AWS vs ground truth | Yes (this pass) |
| `talent/documents/Coda_Summary_For_Scout_and_Vector_Post_Replication.md` | Cross-agent sync (Army side) | Yes (this pass) |
| `talent/documents/CONVERSATION_HANDOFF.md` | Technical handoff for new CODA threads | Yes (April section) |
| `talent/documents/advisor_brief_twofold_status.md` | Advisor-facing status | Partially current |
| `talent/documents/Agent_Read_First_Coda_Runbook.md` | Scout replication runbook (historical) | Reference only |
| `talent/documents/520_PIPELINE_COX_OVERVIEW.md` | Pipeline map | Yes (June 2026) — Cell 11 optional own-TB stratify add-on |
| `talent/documents/Army_to_College_Basketball_Replication_Handoff.md` | Long replication design | Historical reference |

**Manuscript-facing Army brief for VECTOR:** `talent/documents/Coda_Vector_Brief_Army_Evidence_For_Brian_Memo.md`

---

## 8. Code map (talent_pipeline essentials)

| Path | Role |
|------|------|
| `501_working.ipynb` … `512_oer_int_working.ipynb` | Ingest, OER, hierarchies |
| `520_pipeline_cox_working.ipynb` | **Main** Cox + plotting conductor |
| `pipeline_config.py` | Base flags, `PLOT_CONFIG`, `CR_TB_STRATIFY_CONFIG`, run profile hooks |
| `pipeline_config_19_1.py`, `pipeline_config_div_name.py`, … | Overrides (`from pipeline_config import *`) |
| `add_cum_oer_metrics_mod_working.py` | Fwd/bwd TB, **pool means/sizes/ranks/z** |
| `join_oer_to_snapshots_working.py` | OER ↔ snapshot join |
| `cox_plot_helpers.py` | Plot filenames, CIF bars, titles |
| `cr_tb_stratify.py` | TB-stratified CR add-on |
| `py_503_hierarchies.py` | UIC / hierarchy helpers |

**AWS snapshot (not ground truth):** `talent/Army_AWS_download/TALENT_NET_export_20260421-0802/`

---

## 9. Sister agents — what CODA knows (read their reports, don’t merge code blindly)

| Agent | Report / gameplan (examples) | CODA relationship |
|-------|-------------------------------|-------------------|
| **SCOUT** | `sports/documents/SPORTS_DATA_GAMEPLAN.md`, `Pertinent_Thoughts_Scout.md` | Replication setting; inverted-U in draft vs `poolq_loo`; generative congestion score work |
| **PEER** | `tenure/documents/TENURE_DATA_GAMEPLAN.md`, `5-Manuscript/PEER_Status_Update_for_VECTOR_2026-06-03.md` | Setting 3; stage 9 preliminary inverted-U; Cox wiring in progress; not using 520 |
| **VECTOR** | `1-Various_PDE_and_Chat_stuff/5-Manuscript/*.md` | Manuscript integration; use Army brief + Scout/PEER status docs |

**Expected parallel reports for COMPASS:** Charles asked each agent for `{AGENT}_report_to_COMPASS.md` in `./3-Master_Plan/`. This file is **CODA’s** contribution.

---

## 10. Charles answers & open items (COMPASS feed-in)

**Recorded 2026-06-08; COMPASS update 2026-06-11.** Charles locked **Summer–Fall 2026** manuscript target and **default deferral** of 525/TB-stratify/pool audit unless elevated. CODA parallel-track ranking (§10 deferred rows) **still open**.

### Answered (use as constraints)

| # | Topic | Charles’s answer |
|---|--------|------------------|
| 1 | COMPASS agent | **Probably brand-new** Cursor agent |
| 2 | Manuscript structure | **One manuscript** (all settings) |
| 3 | Defense / dissertation bar | **All three settings** required (not Army-only minimum) |
| 4 | Master plan deliverable format | Charles will **instruct COMPASS directly** |
| 5 | Wait for all four agent reports? | Charles will **instruct COMPASS directly** |
| 11 | VECTOR canonical outline | **`Vector_to_Scout_Tier1_Modeling_Direction.md` is not necessarily THE canonical file** — wait for **VECTOR’s report** |
| 12 | Refresh `520_PIPELINE_COX_OVERVIEW.md` | **Yes** — TB-stratify documented as optional Cell 11 add-on (done June 2026) |

### Deferred — ask again when Charles finalizes CODA domain

- **6** Pool harmonization (language vs code-aligned LOO)
- **7** Pool-size >100 audit vs manuscript disclaimer
- **8** Army AWS upload cadence / TB-stratify upload status
- **9** TB-stratify default on vs off for routine runs
- **10** Priority: 525/UIC vs pool audit

### Still open (not answered above)

- **SpecStory + git** policy confirmation
- **Rivanna / workspace** files on science commits vs separate
- **Hard defense date** (if COMPASS needs a timeline anchor)

---

## 11. Suggested first tasks for COMPASS

*Several items below are **done** (2026-06-11); CODA parallel-track ranking still open.*

1. Inventory all four `{AGENT}_report_to_COMPASS.md` files + VECTOR manuscript outlines.
2. Build a **single timeline** (data ready → figure ready → manuscript section ready) per setting.
3. Resolve **pool definition harmonization** across Army / SCOUT / PEER (shared glossary).
4. Align **VECTOR** section outline with actual figure availability (Army strongest, tenure preliminary, basketball replicated).
5. Git hygiene: branch strategy, what belongs on `main`, SpecStory policy.

---

## 12. Agent identity note

This report was authored by **CODA** in the Cursor session covering Army talent work with Charles (TB stratify, AWS overlay, CR interpretation, pool-size concerns, Pertinent Thoughts updates). If Charles intended a different agent name for this thread, relabel this file accordingly.

---

*End CODA handoff. COMPASS active — see `20260611_0826_COMPASS_to_CODA_questions.md` for open Army sequencing items.*
