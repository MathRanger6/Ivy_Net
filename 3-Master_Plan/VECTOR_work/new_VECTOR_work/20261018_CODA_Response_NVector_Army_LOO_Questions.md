# CODA response — Army peer measures & LOO (for NVector audit)

**In reply to:** [`20261018_NVector_Questions_for_CODA_LOO.md`](20261018_NVector_Questions_for_CODA_LOO.md)  
**Prepared from:** Mac repo code, configs, manifests, and re_entry checklists only — **not** from live AWS feather timestamps or Charles’s 2026 AVD matrix screenshots unless noted.  
**Legend:** **Verified (repo)** · **Verified (Charles run, not in git)** · **Uncertain / needs AWS path + date**

**For NVector — read this before drafting the next document.** The follow-on doc should be an **audit conclusion**, not a rerun: lock vocabulary (pond LOO mean vs own−mean vs z-scored), split **inferential** (March Cox/CR + `pipeline_config_17_1`) from **descriptive** (2026 BDP matrix / H_sort), and label anything that still needs Charles’s AWS paths or PNG spot-checks as **open** rather than smoothing over it. Charles can paste matrix **H_sort** rows and confirm Path B Cox when available; until then, do not promote straight LOO to co-equal authority with Run 1 Cox in Chapter 4 prose.

---

## Short answer Charles can use in Chapter 4 framing

- **Column math has been consistent since March 2026 export:** `pool_minus_mean_* = own_tb_ratio − LOO pool mean`; `pool_tb_ratio_mean_*` is the **peer LOO mean** (T̂-style pond level). Older prose that called `pool_minus_mean` “the peer mean” was **wording error**, not a different formula in that archive.
- **Authoritative Cox / competing-risk (CR) story in git** still targets **`z_pool_minus_mean_snr_fwd`** (own minus LOO, z-scored) via `pipeline_config_17_1.py` Run 1 — **not** straight LOO.
- **Straight LOO BDP / HERO** is documented and runnable (`ARMY_RUN_MATRIX_CHECKLIST.md`, `STRAIGHT_LOO_MOSAIC_AWS_GUIDE.md`) but **Mac plot defaults** (`army_hero_slide_plot.py`, `army_basic_plots.py` `COL_LOO`) still default to **minus-mean** until intentionally switched per run checklist.
- **Do not cite figure filenames alone:** sandbox manifest maps March AWS names to canonical slots; `ARMY_combined_effect_pool_minus_mean_stdz.png` is a **renamed** Cell 12.6A export keyed off `combined_effect_base`, not proof the x-axis is minus-mean in every pixel.

---

### 1 · Which Army result is authoritative now

| Layer | **Verified (repo)** | Status |
|--------|---------------------|--------|
| **Cox + CR + partial/combined-effect figures (flipbook / Brian memo era)** | Notebook `talent/talent_pipeline/520_pipeline_cox_working.ipynb` + profile **`pipeline_config_17_1.py`** (Run 1: TB ratio + **pool minus mean**, z-scaled, interaction). Provenance table: `3-Master_Plan/re_entry/HEROs_and_PASSes/army_sandbox/EXTRACT_MANIFEST.txt` → sources under `talent/Army_AWS_download/TALENT_NET_export_20260320-1000/`. | **March 20–25, 2026 AWS export** is the last **checked-in** end-to-end Cox/CR artifact set. |
| **Pool construction code** | Current: `talent/talent_pipeline/add_cum_oer_metrics_mod_working.py` + `pipeline_config.py` (`POOL_GROUPING_MODE`, etc.). March archive helper matches minus-mean formula (see Q2). | Mac **ahead** of old PDE on `active_at_eval_thru` / snapshot modes; not all fixes uploaded to AVD. |
| **BDP 3×3 mosaic (panels 2–9 porch)** | Scripts under `talent/re_entry/`; matrix spec `talent/re_entry/ARMY_RUN_MATRIX_CHECKLIST.md`. | **Verified (Charles run, not in git):** Runs 1–5+ optional 6–8 on Army Virtual Desktop (2026-09+) replace **descriptive** mosaic/HERO for sensitivity; **do not automatically replace** Cell 12 Cox exports unless Path B straight-LOO profile refit was executed. |
| **Counts & year window** | CR plot slug in manifest: `2002-2022`, `noOER` filters in filename. Exact **N officers / person-years** for latest AVD feather: **Uncertain** — require `df_pipeline_11_cox_analysis.feather` probe on AWS or archived `run*_*.feather`. | |

**CODA recommendation:** Treat **March Run-1 Cox/CR bundle** as authoritative for **inferential** claims until a **documented** straight-LOO Cox refit (Path B in STRAIGHT_LOO guide) is checked in with new `cox_results/` outputs. Treat **2026 matrix BDP PNGs** as authoritative for **descriptive** H_sort / porch sensitivity under stated `POOL_GROUPING_MODE`.

---

### 2 · What exactly is the horizontal variable

**Verified (repo) — definitions in Cell 5 helper** (`add_cum_oer_metrics_mod_working.py`, `_add_pool_mean_size` and anchor path):

| Column | Formula (senior-rater SNR forward example) |
|--------|---------------------------------------------|
| `pool_tb_ratio_mean_snr_fwd` | LOO mean of peers’ `tb_ratio_fwd_snr` in pool: \(\(\bar T_{-i}\)\) with optional `exclude_self`, `pool_min_size`, optional drop peers with TB=0. |
| `pool_minus_mean_snr_fwd` | **`tb_ratio_fwd_snr − pool_tb_ratio_mean_snr_fwd`** (own minus LOO peer mean). |
| `z_pool_minus_mean_snr_fwd` | Z-score of **`pool_minus_mean_snr_fwd`** per Cell 10.5 `STANDARDIZE_CONFIG` (same cohort as Cox panel unless winsorize toggled). |
| `z_tb_ratio_fwd_snr` | Z-score of **own** cumulative SNR TB ratio forward. |

**Own rating entering minus-mean:** `tb_ratio_fwd_snr` (cumulative SNR talent-board ratio on the snapshot row, forward mode in pool code).

**Older prose:** Memos that describe `pool_minus_mean` as “peer quality” or “peer mean” are **incorrect labels**; March **code** already used own − mean. No evidence in repo that a different preparation **overwrote** the column with the mean — check memos in `talent/documents/Coda_*` as **superseded wording**, not superseded math.

**By figure class (repo defaults):**

| Output | Typical x / peer axis | Verified? |
|--------|------------------------|-----------|
| Cell 11 CR CIF bars (Run 1 profile) | `z_pool_minus_mean_snr_fwd` when `RUN_SCALE='z'` | Yes — `pipeline_config_17_1.py` |
| `army_hero_slide_plot.py` default | `z_pool_minus_mean_snr_fwd` | Yes — file header + `plot_var` |
| Matrix Runs 1–3, 6–8 HERO | `pool_tb_ratio_mean_snr_fwd` when scripts edited per checklist | Conditional on AWS script state |
| Matrix Runs 4–5 HERO | `z_pool_minus_mean_snr_fwd` | Conditional |
| Panel 2 BDP “T̂_j” | `pool_tb_ratio_mean_snr_fwd` via `COL_TJ` | Yes — `army_basic_plots.py` |
| Panel 1/3/7/8 LOO context | **`COL_LOO` default** = `pool_minus_mean_snr_fwd` on Mac until checklist edit | Yes — defaults; straight LOO is **opt-in** |

**Naming trap in BDP code:** `COL_TJ` = straight LOO mean; `COL_LOO` = minus-mean — opposite of some basketball “LOO” shorthand. Checklist uses “straight LOO” = **`pool_tb_ratio_mean_snr_fwd`**.

---

### 3 · Was the straight LOO change completed

**Verified (repo):**

- **Guide exists:** `talent/re_entry/STRAIGHT_LOO_MOSAIC_AWS_GUIDE.md` (Path A plot-only vs Path B Cell 10.5 + Cox).
- **Run matrix encodes completed workflow:** Runs 1–3 notebook + straight LOO plots; Runs 4–5 plot-only minus-mean off archived feathers (`ARMY_RUN_MATRIX_CHECKLIST.md`).
- **Mac defaults NOT flipped globally:** `army_basic_plots.py` line 42 `COL_LOO = "pool_minus_mean_snr_fwd"`; `army_hero_slide_plot.py` `plot_var = "z_pool_minus_mean_snr_fwd"`.

**Verified (Charles run, not in git) — per conversation log:** Runs 1–5 executed on old PDE; optional 6–8 specified for pool-grain exploration.

**Uncertain:** Whether **Path B** (Cox/CR refit on `z_pool_tb_ratio_mean_snr_fwd` or raw straight LOO quadratics) was ever finished and saved under `cox_results/`. No straight-LOO `pipeline_config_*` profile checked in as canonical replacement for `pipeline_config_17_1.py`.

**CODA answer:** **Plot-level straight LOO — partially completed** on AWS per matrix; **Cox-level straight LOO — not established in repo** as replacement for March Run 1.

---

### 4 · Who belongs to each officer’s pool

**Verified (repo) — authoritative toggles in `pipeline_config.py`:**

| Knob | Typical authoritative value (matrix Run 2+) | Meaning |
|------|-----------------------------------------------|---------|
| Rater | **`snr_rater_bwd`** for SNR forward pools | Senior rater backward identity on snapshot row |
| Value pooled | `tb_ratio_fwd_snr` | Peer **own** TB ratio in pool stats |
| `POOL_GROUPING_MODE` | `active_at_eval_thru` (matrix default); sensitivity: `legacy`, `active_at_snapshot`, `rating_window` | See `rating_window_mode_explanation.md` |
| `POOL_EXCLUDE_PEER_TB_ZERO` | False baseline; True in Run 3 / 8 | Drops **peers** with TB=0 from mean/size only |
| `POOL_EXCLUDE_SELF` | True in LOO path | Exclude self from peer mean (standard LOO) |
| `pool_min_size` | 3 (plot scripts + config) | Below → NaN pool stats |
| Anchor modes | Eval-thru: peer OER window covers **`eval_thru_dt_bwd`**; snapshot: covers **`snpsht_dt`** | Cell 5 `_add_pool_mean_size_active_at_anchor` |

**Legacy “large pools”:** `legacy` = same `snpsht_dt` × same `snr_rater_bwd` (~median pool ~23 in docs) — **not repaired** in legacy mode; **replaced by eval-thru** in recommended runs, not retroactively patched in March Cox feather without re-run.

**Rank / job filters:** Cell 2 commissioned ranks + job-code exclusions in notebook (see Cell 2 logs on AWS). **Uncertain:** exact N after filters without feather.

---

### 5 · What outcome does each plot estimate

**Verified (repo):**

| Output | What height means | Source |
|--------|-------------------|--------|
| **`army_hero_slide_plot.py` default** (`outcome_mode = "last_event"`) | **Last-interval event indicator:** `event == 1` on last snapshot row (promotion on terminal interval for promoted officers) — **binned mean**, not Cox-predicted | `army_hero_slide_plot.py` |
| **`ever_promoted` CLI flag** | Officer-level ever promoted | same file |
| **Cell 11 CR CIF bars** | **Cumulative incidence** from competing-risks fit; competing events per Cox model setup; horizon / censoring from `stop_time` / `event` coding in Cell 10–11 | `520_pipeline_cox_working.ipynb`, `RUN_CR_PLOT_DEFAULTS` (`x_max_days`: 4500) |
| **Act II CCT / elite panels** | Binned promotion rate vs pool LOO axis (descriptive) | `army_act2_probes.py` |

**Do not conflate:** HERO porch (descriptive bin means) vs CR CIF bars (model-based CIF) vs hazard-ratio surfaces (interaction / partial effects).

---

### 6 · What supports the strongest or most robust finding

**Verified (repo):** March export includes CR curves, CIF bars, `competing_risks_analysis_stdz`, `model_comparison_stdz`, interaction CIF (`EXTRACT_MANIFEST.txt`). Run 1 model adjusts for **`z_tb_ratio_fwd_snr`**, **`z_pool_minus_mean_snr_fwd`**, quadratics, **`star_pool_interaction`**, **`div_name`**.

**Uncertain / not in repo without re-open:** Formal test that peak-and-downturn **survives** straight-LOO x-axis on **same** Cox specification; side-by-side coefficient table minus-mean vs straight LOO. Matrix checklist **explicitly** separates descriptive reruns from Cox refit.

**CODA:** State March **adjusted Cox + CR** as primary inferential evidence; straight LOO as **documented sensitivity** for BDP/H_sort unless Path B completed.

---

### 7 · Which Cox specification was fit

**Verified (repo) — `pipeline_config_17_1.py`:**

- **Time-varying:** `tb_ratio_fwd_snr`, `pool_minus_mean_snr_fwd` → z-scored when `RUN_SCALE='z'`.
- **Quadratics:** both bases squared (z-scored squares if RUN_SCALE z).
- **Interaction:** `star_pool_interaction` (product term as configured in expand_run_profile).
- **Extra TV:** `div_name` (dummies).
- **Combined-effect plot (Cell 12.6A):** `combined_effect_base`: **`pool_minus_mean_snr_fwd`** → file pattern `combined_effect_{base}_stdz.png`.

**How to read combined-effect curve:** Marginal visualization of **own + peer-relative** terms tied to the **quadratic base** chosen in config (minus-mean), holding other model terms at profile defaults — **not** a single-variable LOO peer mean effect.

**Saved model summary:** Expected under AWS `cox_results/` from March run — **not duplicated in git** as CSV in this search. Notebook Cell 12 outputs reference `partial_effects_plots{fig_save_suffix}.png`.

**Promotion outcome:** Competing-risks promotion vs separation/retirement per Cell 10 event coding (standard 520 pipeline).

---

### 8 · Unit-level results & rationale for LOO

**Verified (repo):** `pipeline_config_div_name.py` / division CR plots (`ARMY_tb_by_division_cif_b1.png` in manifest) use **division as group-by**, not battalion/brigade self-excluded performance means.

**Uncertain:** Completed battalion/brigade analyses with genuine LOO performance means — **not found** in indexed army_sandbox manifest; 525 PDF mentioned as future mechanism work in handoff doc.

**LOO rationale (repo + binding plan):** LOO removes **own** contribution to peer pool mean; minus-mean further expresses **relative standing** vs pond. Basketball analog documented in STRAIGHT_LOO guide (pond level vs relative). No single dated “LOO decision memo” located in this pass — **VECTOR / COMPASS binding:** score ≠ select; pool metric choice is **measurement**, not Hero generative model.

---

### 9 · Figure naming discrepancy

**Verified (repo) — `EXTRACT_MANIFEST.txt`:**

| Canonical (sandbox) | AWS source label | CODA read |
|---------------------|------------------|-----------|
| `ARMY_partial_effects_pool_minus_mean.png` | `combined_effect_z_pool_minus_mean_snr_fwd_stdz.png` | **Partial/combined pool-minus-mean effect** (z-scored peer-relative axis in model). |
| `ARMY_combined_effect_pool_minus_mean_stdz.png` | regex `combined_effect.*pool_minus_mean` | **Same family** as Cell 12.6A export; filename reflects **`combined_effect_base`**, not every trace on the figure. |

If `ARMY_combined_effect_pool_minus_mean_stdz.png` **visually** plots `z_tb_ratio_fwd_snr`, that is consistent with a **multi-term** combined-effect or **wrong file copied into sandbox** — **Uncertain without opening PNG + matching `cox_results` filename timestamp**.

**Citation rule:** Cite **model variable name + run profile** (`pipeline_config_17_1`) for scientific claims; use sandbox **canonical name** only as flipbook slot ID. Prefer **`EXTRACT_MANIFEST` AWS label** when tracing back to notebook output.

---

## Outstanding items for Charles (close the audit)

1. AWS: path + date for feather backing **current** favorite HERO mosaic (Run 2 vs minus-mean baseline).  
2. Confirm whether **Path B** straight-LOO Cox was ever saved.  
3. Open `ARMY_combined_effect_pool_minus_mean_stdz.png` vs `cox_results/combined_effect_*` on AWS to resolve Q9 visual mismatch.  
4. Paste **H_sort + N** from results table in `ARMY_RUN_MATRIX_CHECKLIST.md` into this thread for NVector.

---

*CODA draft 2026-10-18 — repo-only; no new analysis run.*
