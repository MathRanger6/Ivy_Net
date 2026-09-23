# COMPOSER handoff to VECTOR — 2026-09-22

**Agent:** COMPOSER (Cursor IDE implementation agent — pair programming with Charles)  
**Audience:** VECTOR (ChatGPT Work, repo-connected)  
**Prepared:** 2026-09-22  
**Scope:** Implementation and debugging history I share with Charles in Cursor — **not** COMPASS planning prose, **not** manuscript narrative, **not** CODA/SCOUT/PEER domain personas unless noted as overlap.

**Evidence types used:** Repository files I read for this handoff; SpecStory session exports under `.specstory/history/`; Cursor agent transcript `00296962-6477-402f-a044-1dc7cd8fb3dc` (Army straight-LOO / mosaic thread, summarized 2026-09-22); conversation summary Charles pasted from a parallel COMPASS thread (Cell 6 pass-through — **conversation evidence, not independently re-run**).

**What I did not do for this handoff:** Execute notebooks, run pipeline cells, inspect AWS-only artifacts, or verify PNG outputs on Charles’s Army environment.

---

## 1. My role and our working relationship

### What COMPOSER is

COMPOSER is Charles’s **default Cursor Agent** for **hands-on implementation**: editing Python modules and notebooks, scaffolding scripts, debugging AWS runs, wiring cross-domain plot infrastructure, and maintaining repo hygiene (paths, checklists, backup utilities). I operate under binding rules in [`AGENTS.md`](../../../AGENTS.md) and [`.cursor/rules/`](../../../.cursor/rules/).

### Primary domains we have worked on together

| Domain | My typical responsibilities | Boundaries |
|--------|----------------------------|------------|
| **Army / talent pipeline (`talent/`)** | `520_pipeline_cox_working.ipynb` cells; `pipeline_config*.py`; `add_cum_oer_metrics_mod_working.py` pool metrics; Cell 11 export columns; AWS upload bundles | I do **not** own scientific claim language or Alex-facing story order — that is COMPASS / VECTOR |
| **Army re_entry BDP + 3×3 mosaic (`talent/re_entry/`)** | Fork tenure/MBB modular plot pattern; manifest JSON; mosaic wrapper; Act II probes; HERO slide script | Figures are **Layer A empirical porch** — not causal peer effects ([`3-Master_Plan/BINDING_Selection_is_its_own_step.md`](../../BINDING_Selection_is_its_own_step.md)) |
| **Cross-domain mosaic infrastructure (`sports/scripts/`)** | Reuse `build_data_story_mosaic.py`, overlap helpers, hero styling — Army consumes these | SCOUT owns MBB domain logic; I port patterns |
| **Notebook workflow** | `EditNotebook` burn-slot protocol; Cell 10 debug gating; incremental-write rules for long I/O loops | Structural notebook moves require Charles approval per [`.cursor/rules/notebook-blank-edit.mdc`](../../../.cursor/rules/notebook-blank-edit.mdc) |
| **Repo utilities** | e.g. [`scripts/backup_rename_suffix.sh`](../../../scripts/backup_rename_suffix.sh) for `_21s` output backups | Not dissertation science |

### Overlap with other agents

| Agent | Overlap |
|-------|---------|
| **CODA** | Army/talent is CODA’s roster domain ([`3-Master_Plan/COMPASS_AGENT_IDENTITY.md`](../../COMPASS_AGENT_IDENTITY.md)). Much of my Army implementation work **is** CODA-domain code; CODA should produce a separate handoff for scientific framing I do not cover here. |
| **SCOUT** | MBB `tenure_basic_plots.py` / mosaic manifests were the **template** for `talent/re_entry/army_basic_plots.py` (SpecStory: `.specstory/history/2025-11-17_17-43-36-0500-coda.md`, ~lines 20943–21899). |
| **COMPASS** | Sequencing, disposable threads, VECTOR packaging ([`3-Master_Plan/VECTOR_work/handoff_upload_no_repo/`](../handoff_upload_no_repo/)), PD41 priority reads ([`transcripts/PD41_notes.md`](../../../transcripts/PD41_notes.md)). Charles sometimes pasted COMPASS replies into my thread by mistake (Cell 6 pass-through screenshot, 2026-09-22). |
| **PEER** | Minimal direct work in my threads; tenure BDP pattern only as template. |
| **VECTOR** | 2026-09-22 repo path inventory session: `.specstory/history/2026-09-22_13-01-18-0400-map-repo-paths-for.md`. |

### Charles’s working preferences (implementation)

- **One step at a time** on AWS — single next action, wait for “done” or screenshot before long multi-step dumps (conversation transcript, 2026-09-21–22).
- **Mac repo vs AWS execution** — Mac is often canonical for code edits; feathers and plots are generated on Army AWS (`Network_1P_shell/` 520 root). **Mac and AWS can diverge** until Charles uploads and re-runs.
- **Do not commit/push** unless explicitly asked.

---

## 2. Chronological research history

History below is **non-linear** where the repo and conversations show pivots, not a clean arc.

### Phase A — Army pipeline stabilization on AWS (2025, ongoing)

**Trigger:** Charles uploaded PDE code to Army AWS; needed to debug why `div_name` was mostly `"Unknown"` (~43k officers) while only ~3–4k plotted with known division.

**Sources:** `.specstory/history/2025-11-17_17-43-36-0500-coda.md` (session labeled “coda” but executed in Cursor as implementation work).

**Developments:**

- Traced `div_name` merge through Cell 7 / Cell 11 and `py_503_hierarchies.py` `[DIV_DEBUG]` hooks.
- Documented that **502 loads prebuilt** `df_uic_hierarchy` from `big_dfs/` while **503 rebuilds** from `hierarchy_data/FMS_Web/WDARFF_15-26` — stale hierarchy file ⇒ bad `div_name` (agent transcript `00296962`, user images ~1465+).
- Fixed **indentation bug** in senior-rater pool block of [`talent/talent_pipeline/add_cum_oer_metrics_mod_working.py`](../../../talent/talent_pipeline/add_cum_oer_metrics_mod_working.py) (transcript ~1365) — caused NaNs in pool metrics when mis-scoped.
- **Cell 6C memory failures** on optimized pool path (`MemoryError` ~1.38 GiB) — workaround discussed: `CELL6C_OPTIMIZE = False`, dtype cleanup, or rerun from earlier checkpoint (transcript ~1466).
- **Cell 10** legacy column spelling (`cum_tb_rcvd_ratio_*` vs `cum_tb_recvd_ratio_*`) handled in notebook (transcript ~496–499).

**Direction change:** Division-name debugging was **important for stratified plots** but **not blocking** the Run 1 porch deck focused on SNR pools and `tb_ratio_fwd_snr`.

### Phase B — Army 9-panel BDP / data-story port (Sep 2025)

**Trigger:** Charles wanted to **adapt modular BDP + mosaic code** (MBB/tenure pattern) for upload to AWS — not merely find existing Army PNGs (SpecStory coda.md ~20943: *“lets make a folder called talent/re_entry”*).

**Developments:**

- Created [`talent/re_entry/`](../../../talent/re_entry/) with:
  - `army_basic_plots.py` (panels 2–6)
  - `army_act2_probes.py` (panels 7–8, scaled from MBB/tenure Act II)
  - `army_hero_slide_plot.py` (panel 9)
  - `build_army_data_story.py` → delegates to [`sports/scripts/build_data_story_mosaic.py`](../../../sports/scripts/build_data_story_mosaic.py)
  - `manifests/army_run1_3x3_manifest.json`
  - `run_army_bdp_pipeline.sh`, `AWS_UPLOAD_CHECKLIST.md`, `README.md`
- **Default peer context for Run 1 mosaic:** `z_pool_minus_mean_snr_fwd` (minus-mean LOO relative standing) — documented in [`talent/re_entry/README.md`](../../../talent/re_entry/README.md) and manifest panel 1 / panel 9 paths.
- Panel 5 (pool interval overlap) wired to shared overlap module; requires eval date columns in Cell 11 export ([`talent/re_entry/AWS_UPLOAD_CHECKLIST.md`](../../../talent/re_entry/AWS_UPLOAD_CHECKLIST.md) § Panel 5).

**Scientific framing (documented elsewhere, not invented here):** Hero porch = promotion rate vs peer environment; **environment ≠ advancement** per binding doc.

### Phase C — Pool grain upgrade: `active_at_eval_thru` (Sep 2026)

**Trigger:** Align Army peer pools with Alex slide / OER write-time anchor (`eval_thru_dt_bwd`) instead of legacy snapshot groupby.

**Repository evidence:**

- [`talent/talent_pipeline/pipeline_config.py`](../../../talent/talent_pipeline/pipeline_config.py) lines 115–122: `POOL_GROUPING_MODE = 'active_at_eval_thru'` with documented modes.
- [`add_cum_oer_metrics_mod_working.py`](../../../talent/talent_pipeline/add_cum_oer_metrics_mod_working.py): `add_pool_means_and_sizes()` branch for anchor modes (~line 500+); merge-based peer sets vs flat groupby.

**Cell 6 blocker:** `add_pool_ranks_pct_zscores()` raises `NotImplementedError` for anchor modes because ranks need anchor-based peer groups, not implemented.

**Resolution (Option B pass-through):** Lines 611–618 return `df_in.copy()` with log message — **preserves Cell 5 means/sizes; skips rank/zpool columns**. Charles also used manual `cp df_pipeline_05 → df_pipeline_06` on AWS (conversation summary, 2026-09-21 — **reported, not re-verified by me**).

**Empirical note from Charles’s PD41 screen:** Pool-grain rerun moved **HERO porch shape** more than **H_sort point estimate** ([`transcripts/PD41_notes.md`](../../../transcripts/PD41_notes.md) § Army H_sort, ~0.255 → ~0.279). A separate AWS thru run logged **H_sort = 0.131** (conversation summary, 2026-09-21 — **conflicts with PD41 table; see §7**).

### Phase D — Straight-LOO mosaic pivot (Sep 21–22, 2026)

**Trigger:** Basketball analog — use **straight LOO pond mean** (`pool_tb_ratio_mean_snr_fwd`, T̂_j) on mosaic panels 1, 3, 7, 8, 9 instead of **minus-mean** (`pool_minus_mean_snr_fwd` = A_i − LOO peer mean).

**Terminology (Charles lock in thread):**

| Label | Column | Meaning |
|-------|--------|---------|
| Own performance Â | `tb_ratio_fwd_snr` | Officer’s own TB |
| Straight LOO T̂_j | `pool_tb_ratio_mean_snr_fwd` | LOO mean of peers’ TB (`POOL_EXCLUDE_SELF=True`) |
| Minus-mean | `pool_minus_mean_snr_fwd` | Â − LOO peer mean |

**Work documented in:** [`talent/re_entry/STRAIGHT_LOO_MOSAIC_AWS_GUIDE.md`](../../../talent/re_entry/STRAIGHT_LOO_MOSAIC_AWS_GUIDE.md).

**Path A vs Path B:**

- **Path A (mosaic-only):** Re-point plot scripts + manifest; HERO can use raw `pool_tb_ratio_mean_snr_fwd` (on-the-fly z in Act II if needed).
- **Path B (feather z column):** Add `z_pool_tb_ratio_mean_snr_fwd` via Cell 10.5 + `pipeline_config_17_1.py` `tv_vars` swap — **not completed on Mac repo** as of this handoff.

**AWS run (Charles-reported, 2026-09-21 night):** Cells 0→11 with `active_at_eval_thru`; BDP + Act II + HERO succeeded with `--plot-var pool_tb_ratio_mean_snr_fwd`; mosaic **failed** on manifest still pointing to `ARMY_HERO_ew8_z_pool_minus_mean_snr_fwd_run1.png` ([`build_army_data_story.py`](../../../talent/re_entry/build_army_data_story.py) loads manifest after optional cohort refresh — does not fix panel 9 path).

**Sep 22 morning:** Charles ran **legacy** `POOL_GROUPING_MODE` comparison to inspect plots (conversation, 2026-09-22) — **outcome not verified in repo** (PNGs typically not tracked).

### Phase E — Notebook noise / debug hygiene (Sep 2026)

- Cell 10 per-officer `DIV_DEBUG` spam — removed/gated in [`talent/talent_pipeline/520_pipeline_cox_working.ipynb`](../../../talent/talent_pipeline/520_pipeline_cox_working.ipynb) (session marker line 82: `2026-09-21 17:11 — Cell 10 DIV_DEBUG loop fix`).
- [`talent/talent_pipeline/pipeline_config_div_name.py`](../../../talent/talent_pipeline/pipeline_config_div_name.py) line 169: `debug_division = False`.
- Cell 7 debug prints gated on `DIVISION_CONFIG.get('debug_division')` (notebook ~1825).

### Phase F — VECTOR repo onboarding support (Sep 22, 2026)

- Updated [`3-Master_Plan/VECTOR_work/handoff_upload_no_repo/MANIFEST_upload_to_VECTOR.md`](../handoff_upload_no_repo/MANIFEST_upload_to_VECTOR.md) for **Mode B repo-connected** VECTOR (PD41 notes § post-call repo work).
- Repo path inventory session for VECTOR (SpecStory `2026-09-22_13-01-18-0400-map-repo-paths-for.md`).
- **This handoff document** — assignment from Charles, 2026-09-22.

---

## 3. Work actually completed

Legend: **Impl** = code/config exists in repo; **Empirical** = Charles reported a successful run; **Doc** = prose/checklist only.

### Army re_entry modular plot pipeline — **Impl**

| Artifact | Path | Notes |
|----------|------|-------|
| BDP generator | [`talent/re_entry/army_basic_plots.py`](../../../talent/re_entry/army_basic_plots.py) | Mac defaults still `COL_LOO = "pool_minus_mean_snr_fwd"` (lines 41–42) — **minus-mean on Mac** |
| Act II probes | [`talent/re_entry/army_act2_probes.py`](../../../talent/re_entry/army_act2_probes.py) | `COL_LOO_Z = "z_pool_minus_mean_snr_fwd"` (line 55) on Mac |
| HERO slide | [`talent/re_entry/army_hero_slide_plot.py`](../../../talent/re_entry/army_hero_slide_plot.py) | Default `plot_var = "z_pool_minus_mean_snr_fwd"` (line 44) on Mac |
| Mosaic wrapper | [`talent/re_entry/build_army_data_story.py`](../../../talent/re_entry/build_army_data_story.py) | Cohort text refresh for panel 1 only (`_refresh_cohort_text`) |
| Manifest | [`talent/re_entry/manifests/army_run1_3x3_manifest.json`](../../../talent/re_entry/manifests/army_run1_3x3_manifest.json) | Panel 9 path still minus-mean HERO filename on Mac |
| One-shot runner | [`talent/re_entry/run_army_bdp_pipeline.sh`](../../../talent/re_entry/run_army_bdp_pipeline.sh) | **Impl** |
| Pool probe | [`talent/re_entry/army_pool_size_probe.py`](../../../talent/re_entry/army_pool_size_probe.py) | **Impl** |
| Path bootstrap | [`talent/re_entry/army_gallery_paths.py`](../../../talent/re_entry/army_gallery_paths.py) | **Impl** |

**Empirical (Charles-reported, AWS, 2026-09-18–21):** Full BDP pipeline run producing `ARMY_BDP_*.png`, Act II PNGs, HERO with straight LOO raw var — **not in git**; see [`AWS_UPLOAD_CHECKLIST.md`](../../../talent/re_entry/AWS_UPLOAD_CHECKLIST.md) success artifact list (still lists minus-mean HERO name).

### Pipeline pool grain + Cell 6 pass-through — **Impl**

| Artifact | Path |
|----------|------|
| Pool grouping config | [`talent/talent_pipeline/pipeline_config.py`](../../../talent/talent_pipeline/pipeline_config.py) — `POOL_GROUPING_MODE = 'active_at_eval_thru'` |
| Anchor pool means | [`add_cum_oer_metrics_mod_working.py`](../../../talent/talent_pipeline/add_cum_oer_metrics_mod_working.py) — `add_pool_means_and_sizes()` |
| Cell 6 pass-through | Same file, lines 611–618 |
| Div debug default off | [`pipeline_config_div_name.py`](../../../talent/talent_pipeline/pipeline_config_div_name.py) |

### Notebook fixes — **Impl**

| Change | Path |
|--------|------|
| Cell 10 DIV_DEBUG removal / Cell 7 gating | [`talent/talent_pipeline/520_pipeline_cox_working.ipynb`](../../../talent/talent_pipeline/520_pipeline_cox_working.ipynb) |

**Note:** Canonical notebook path on Mac is under `talent/talent_pipeline/`; AWS 520 root may use a copy at repo root — **path layout may differ between environments** (see §7).

### Operational docs and utilities — **Doc / Impl**

| Item | Path |
|------|------|
| Straight-LOO AWS guide | [`talent/re_entry/STRAIGHT_LOO_MOSAIC_AWS_GUIDE.md`](../../../talent/re_entry/STRAIGHT_LOO_MOSAIC_AWS_GUIDE.md) |
| Upload checklist | [`talent/re_entry/AWS_UPLOAD_CHECKLIST.md`](../../../talent/re_entry/AWS_UPLOAD_CHECKLIST.md) |
| Output backup script | [`scripts/backup_rename_suffix.sh`](../../../scripts/backup_rename_suffix.sh) — `_21s` subfolder backups |

### Shared mosaic compositor (pre-existing, Army consumes) — **Impl**

| Item | Path |
|------|------|
| 3×3 compositor | [`sports/scripts/build_data_story_mosaic.py`](../../../sports/scripts/build_data_story_mosaic.py) |
| Layout presets | [`sports/scripts/story_page_layout.py`](../../../sports/scripts/story_page_layout.py) |

### What is **not** independently verified as complete

- Final `ARMY_DATA_STORY_run1_3x3.png` with straight-LOO panel 9 (mosaic build failed on path mismatch per conversation).
- Side-by-side legacy vs `active_at_eval_thru` plot comparison Charles started 2026-09-22.
- Path B `z_pool_tb_ratio_mean_snr_fwd` in feather.
- Full Cell 6 rank/zpool columns for anchor grain.

---

## 4. Proposed but unfinished work

| Item | Source | Status |
|------|--------|--------|
| **Fix manifest panel 9 + title/footer** for straight LOO | [`STRAIGHT_LOO_MOSAIC_AWS_GUIDE.md`](../../../talent/re_entry/STRAIGHT_LOO_MOSAIC_AWS_GUIDE.md) § manifest; conversation 2026-09-21 | AWS editor fix may exist; **Mac manifest unchanged** |
| **Sync Mac plot script defaults** to straight LOO | Same guide § script edits | Deferred intentionally (AWS-first) |
| **Label pass** — plots must say LOO exclude-self vs minus-mean vs own TB | Conversation summary, parked | Not started in repo |
| **Path B** — `z_pool_tb_ratio_mean_snr_fwd` via Cell 10.5 + `pipeline_config_17_1.py` | STRAIGHT_LOO guide §3 | Proposed; not implemented on Mac |
| **CR plots with straight LOO** | STRAIGHT_LOO guide; `PLOT_CONFIG` / `tv_vars` | Parked |
| **Cell 6 ranks for anchor modes** | `NotImplementedError` → pass-through | Proper implementation not scoped |
| **Army BDP filename stem** `pool_minus_mean_loo` → `pool_tb_ratio_mean_loo` | STRAIGHT_LOO guide optional | Cosmetic; manifest path unchanged if skipped |
| **div_name coverage** improvement (503 rebuild → 502 refresh) | SpecStory / transcript | Ongoing background; ~8% non-null reported |
| **Cell 6C memory-safe optimized path** | Transcript ~1466 | Workaround documented; not refactored |
| **Mac → AWS upload** of latest `add_cum_oer_metrics_mod_working.py`, notebook, configs | Conversation summary | Charles action |
| **Education college pond / prestige probe (1 day)** | [`transcripts/PD41_notes.md`](../../../transcripts/PD41_notes.md) P1 | Alex priority; not COMPOSER implementation scope |

---

## 5. Negative results and abandoned approaches

| Result | Evidence | Reason documented |
|--------|----------|-------------------|
| **Cell 6 ranks for anchor pool grain** | `add_pool_ranks_pct_zscores` pass-through, lines 611–618 | Rank logic assumes flat `groupby` keys; anchor modes use merge-based peer sets — **not implemented** |
| **Mosaic build with stale manifest** | `FileNotFoundError` for `ARMY_HERO_ew8_z_pool_minus_mean_snr_fwd_run1.png` while straight-LOO PNG existed under different name | Manifest path not updated on disk before run (conversation + screenshot, 2026-09-21) |
| **`z_pool_tb_ratio_mean_snr_fwd` in feather without Path B** | STRAIGHT_LOO guide §2 column probe | Column absent until standardize list + Cell 10.5 rerun |
| **High `div_name` assignment rate** | `[DIV_DEBUG]` ~7.97% non-null after merge (notebook output cited in transcript) | UIC lookup coverage / FY mismatch / stale hierarchy — **not fixed to high coverage** |
| **Cell 6C optimized pool metrics at full scale** | `MemoryError` (transcript) | Large object-dtype frame index — use non-optimized path or dtype cleanup |
| **Minus-mean as long-run peer X for basketball parity** | Straight-LOO pivot Sep 2026 | Charles chose straight LOO (`pool_tb_ratio_mean_snr_fwd`) for mosaic peer context to match MBB `poolq_loo` analog — minus-mean not abandoned globally (still in feather and Cox Run 1 profile) |
| **Self-contained VECTOR zip-only onboarding** | [`00_READ_ME_FIRST_FOR_VECTOR.md`](../handoff_upload_no_repo/00_READ_ME_FIRST_FOR_VECTOR.md) header still says “no repo access” | **Superseded** by repo-connected VECTOR (Charles assignment 2026-09-22; [`MANIFEST_upload_to_VECTOR.md`](../handoff_upload_no_repo/MANIFEST_upload_to_VECTOR.md) Mode B) |

---

## 6. Current state as of September 22, 2026

### Within my implementation remit

| Category | State |
|----------|-------|
| **Verified artifacts (repo)** | `talent/re_entry/*` module; pool-grain code in `pipeline_config.py` + `add_cum_oer_metrics_mod_working.py`; Cell 6 pass-through; STRAIGHT_LOO guide; backup script |
| **Documented empirical findings** | PD41: assortativity screen across domains ([`transcripts/PD41_notes.md`](../../../transcripts/PD41_notes.md)); Army porch changed with pool grain more than H_sort delta — **Alex meeting notes, not re-plotted by me** |
| **Working hypotheses** | Straight LOO is the correct peer X for cross-domain porch parity; `active_at_eval_thru` is the preferred pool grain for Army scientific anchor; legacy grain retained for comparison runs |
| **Unfinished implementation** | Mac/AWS sync on straight-LOO defaults; mosaic completion; label pass; Path B z column; anchor ranks |
| **Reported but unverified by me** | AWS straight-LOO HERO monotonic ~0.42→~0.92 bins 1–6; `_21s` backups; legacy rerun Sep 22 AM |

### Alex / COMPASS priority context (PD41 — not my assignment, but gates story)

From [`transcripts/PD41_notes.md`](../../../transcripts/PD41_notes.md):

- **P0:** Nail assortativity — “biggest blocker”
- **P1:** Education one-day college/prestige probe
- **P2:** Narrative restructure / new PowerPoint by EOW/weekend
- **Primary trio:** Army · MBB · Tenure still anchor domains

### Dependencies

- **Feather:** `big_dfs/df_pipeline_11_cox_analysis.feather` on AWS 520 root — all re_entry scripts read via `army_gallery_paths`.
- **Cell 11 columns:** `eval_strt_dt_bwd`, `eval_thru_dt_bwd`, `snr_rater_bwd` for panel 5 overlap ([`AWS_UPLOAD_CHECKLIST.md`](../../../talent/re_entry/AWS_UPLOAD_CHECKLIST.md)).
- **Shared sports scripts** must be co-uploaded with `talent/re_entry/`.

### Outstanding technical questions

1. Does Charles want **Path A or Path B** as the canonical Run 1 peer X going forward?
2. Should **Mac repo** straight-LOO script edits land before or after AWS mosaic sign-off?
3. Is **legacy vs `active_at_eval_thru`** comparison sufficient for Alex’s assortativity P0, or is a written H_sort + porch delta table required?

---

## 7. Contradictions, uncertainty, and unresolved decisions

| Issue | Sources | Conflict | Resolution evidence needed |
|-------|---------|----------|----------------------------|
| **Army H_sort after pool-grain rerun** | PD41 notes (~0.255→~0.279); AWS thru run summary (H_sort **0.131**) | Large discrepancy | Charles to confirm which feather/config produced each; grep `H_sort` from BDP overlap PNG titles or `army_basic_plots.py` logs for both `21s` and current runs |
| **Mac vs AWS script defaults** | Mac `army_*.py` minus-mean; AWS straight-LOO edits per conversation | Same filenames, different `COL_LOO` / `plot_var` | Diff AWS vs Mac files or Charles confirmation of upload state |
| **Manifest panel 9 path** | Mac JSON: `z_pool_minus_mean_snr_fwd`; AWS editor screenshot showed `pool_tb_ratio_mean_snr_fwd` | Mosaic failure vs fixed buffer | `grep HERO talent/re_entry/manifests/army_run1_3x3_manifest.json` on AWS |
| **HERO default in README vs straight-LOO run** | [`README.md`](../../../talent/re_entry/README.md) line 85; STRAIGHT_LOO guide | Doc lag | Update README when Charles locks peer X |
| **Notebook path** | Mac: `talent/talent_pipeline/520_pipeline_cox_working.ipynb`; AWS checklist: `520 root` | Upload bundle ambiguity | Confirm which path is canonical on AWS |
| **Cell 6 completion** | Pass-through vs manual `cp 05→06` | Functionally equivalent for means; ranks missing either way | Cell 11 column list from both paths |
| **Is mosaic “done”?** | Charles reported BDP/HERO OK; mosaic failed | Partial deliverable | Successful `build_army_data_story.py` exit + output PNG |
| **COMPASS vs COMPOSER thread** | Cell 6 pass-through pasted from COMPASS conversation | Same code exists on Mac — **verified** at lines 611–618 | No scientific conflict; attribution only |

### Questions requiring Charles’s confirmation

1. Did the **legacy run (Sep 22 AM)** complete through mosaic, and where are PNGs (`21s` subfolders vs top-level)?
2. Is **straight LOO raw** or **z-scored straight LOO** the target for panel 9 for Alex?
3. Should I (COMPOSER) **sync Mac** `army_*` scripts and manifest to straight LOO after AWS sign-off?

---

## 8. Annotated repository reading list

Prioritized for understanding **COMPOSER’s shared implementation work**. VECTOR should still read COMPASS-curated pack first ([`MANIFEST_upload_to_VECTOR.md`](../handoff_upload_no_repo/MANIFEST_upload_to_VECTOR.md) §1–2).

| Priority | Path | Type | Why read | Start here |
|----------|------|------|----------|------------|
| **1** | [`AGENTS.md`](../../../AGENTS.md) | Binding ops | Notebook rules, COMPASS identity, commit policy | Always-on section |
| **2** | [`3-Master_Plan/BINDING_Selection_is_its_own_step.md`](../../BINDING_Selection_is_its_own_step.md) | Binding science | Environment ≠ advancement; hero ≠ generative score | § Three separations |
| **3** | [`talent/re_entry/README.md`](../../../talent/re_entry/README.md) | Implementation spec | Army 9-panel deck, run commands, defaults | § Run, § 9-panel standard |
| **4** | [`talent/re_entry/AWS_UPLOAD_CHECKLIST.md`](../../../talent/re_entry/AWS_UPLOAD_CHECKLIST.md) | Implementation record | Upload bundle, Cell 11 columns, panel 5 | § Also submit when pool-grain work is active |
| **5** | [`talent/re_entry/STRAIGHT_LOO_MOSAIC_AWS_GUIDE.md`](../../../talent/re_entry/STRAIGHT_LOO_MOSAIC_AWS_GUIDE.md) | Working plan | Active Sep 2026 pivot; Path A/B | § YOU ARE HERE table |
| **6** | [`talent/talent_pipeline/pipeline_config.py`](../../../talent/talent_pipeline/pipeline_config.py) | Technical spec | `POOL_GROUPING_MODE`, pool constants | Lines ~115–123 |
| **7** | [`talent/talent_pipeline/add_cum_oer_metrics_mod_working.py`](../../../talent/talent_pipeline/add_cum_oer_metrics_mod_working.py) | Implementation | Pool means + Cell 6 pass-through | `add_pool_means_and_sizes`, `add_pool_ranks_pct_zscores` |
| **8** | [`talent/re_entry/build_army_data_story.py`](../../../talent/re_entry/build_army_data_story.py) | Implementation | Mosaic wrapper; cohort refresh limits | `_refresh_cohort_text` |
| **9** | [`sports/scripts/build_data_story_mosaic.py`](../../../sports/scripts/build_data_story_mosaic.py) | Shared infra | Cross-domain compositor | Module docstring / CLI |
| **10** | [`transcripts/PD41_notes.md`](../../../transcripts/PD41_notes.md) | Current-status (Alex) | Sep 22 priorities; H_sort screen | § Headline, § Alex ask |
| **11** | [`3-Master_Plan/VECTOR_work/handoff_upload_no_repo/MANIFEST_upload_to_VECTOR.md`](../handoff_upload_no_repo/MANIFEST_upload_to_VECTOR.md) | Orientation | Repo-connected VECTOR rules | Mode B, Repository orientation |
| **12** | [`3-Master_Plan/re_entry/00_READ_ME_FIRST.md`](../../re_entry/00_READ_ME_FIRST.md) | Historical context | Charles re-entry — scientific layers | § Your only reading list |
| **13** | `.specstory/history/2025-11-17_17-43-36-0500-coda.md` | Conversation archive | Army BDP port genesis; div_name; Cell 6C | Search `talent/re_entry`, `army_basic_plots` |
| **14** | `.specstory/history/2026-09-22_13-01-18-0400-map-repo-paths-for.md` | Conversation archive | Repo path inventory for VECTOR | Full session |
| **15** | [`scripts/backup_rename_suffix.sh`](../../../scripts/backup_rename_suffix.sh) | Utility | Output backup convention | Header comments |

### SpecStory sessions most relevant to COMPOSER ↔ Charles (Army implementation)

| Session file | Date | Topic |
|--------------|------|-------|
| `2025-11-17_17-43-36-0500-coda.md` | 2025-11-17 | AWS div_name, Cell 6 pool metrics, **talent/re_entry scaffold** |
| Agent transcript `00296962-6477-402f-a044-1dc7cd8fb3dc` | 2026-09-21–22 | Straight-LOO mosaic, Cell 6 pass-through, mosaic manifest failure, legacy comparison |
| `2026-09-22_13-01-18-0400-map-repo-paths-for.md` | 2026-09-22 | VECTOR repo inventory |

**Exclude from routine reading:** `.specstory/history/debug/` (raw JSON per [`MANIFEST_upload_to_VECTOR.md`](../handoff_upload_no_repo/MANIFEST_upload_to_VECTOR.md)).

### Artifacts VECTOR should not expect in repo

- Army **restricted** raw data, credentials, full feather files (large, AWS-local).
- Generated PNGs under `talent/re_entry/output/` (often gitignored or empty except `.gitkeep`).
- Unapproved debug logs.

---

## Appendix — Evidence legend

| Tag | Meaning |
|-----|---------|
| **[Repo]** | Verified by reading file in workspace |
| **[Conv]** | Charles ↔ COMPOSER conversation or summarized transcript |
| **[SpecStory]** | `.specstory/history/*.md` export |
| **[PD41]** | [`transcripts/PD41_notes.md`](../../../transcripts/PD41_notes.md) |
| **[Infer]** | Reasonable inference — flag for Charles confirmation |

---

*End of COMPOSER handoff. For scientific sequencing and story outline, read COMPASS and VECTOR curated materials; for Army domain science beyond implementation, await CODA handoff.*
