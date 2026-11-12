# 512 & 520 pipeline — cell inventory (columns in / out)

**Last synced:** 2026-11-10

**Audience:** Charles, PDE export conversations, dissertation empirics (Chapter 3).

**Standalone:** Per-cell purpose, required columns, creates, and checkpoint feathers for `512_oer_int_working.ipynb` and `520_pipeline_cox_working.ipynb` (canonical: `talent/talent_pipeline/`).

**Source notebooks:** `512_oer_int_working.ipynb`, `520_pipeline_cox_working.ipynb`; config: `pipeline_config.py` (Run 1 mirror: `pipeline_config_17_1.py` on AWS exports).

---

## Legend

| Tag | Meaning |
|-----|---------|
| **Req** | Required if the cell runs (default / typical Run 1) |
| **Opt** | Only when config enables the feature (`filtering_params`, `PRESTIGE_CONFIG`, `DIVISION_CONFIG`, etc.) |
| **Diss** | Needed for current Ch.3 HERO / mosaic / CIF **bars** (prestige / sex / division exploratory work out of scope) |
| **Carry** | All upstream columns remain unless the cell explicitly drops rows or strips column names |

**Production spine**

```text
502 → 520 Cells 1–11     ;   512 Cells 2–3 → df_oer_enriched → 520 Cell 4
```

---

## Part A — Notebook 512 (OER preparation)

| Cell | What it does | Input | Columns required | Creates (main) | Output feather |
|------|----------------|-------|------------------|----------------|----------------|
| **0** | Run `sql_scripts/pipeline.sql` to build raw OER from PDE tables | PostgreSQL | SQL-defined | **`df_oer`** | `df_oer` |
| **1** | Short master pulls for UIC lookup at eval dates | DB tables or cached feathers | **`pid_pde`, `snpsht_dt`, `asg_uic_pde`, `rank_pde`** on `master_pde`; ref master uses `asg_uic` | `df_short_master_pde`, `df_short_master`; loads **`df_lu_uic_1to1`** | same names |
| **2** | Curate OER eval table | **`df_oer`** | **`rated_ofcr`, `eval_strt_dt`, `eval_thru_dt`, `rater`, `snr_rater`, `rater_box`, `snr_rater_box`, `rated_rank`** (+ dedup keys, box code fields) | Deduped/scrubbed rows; **`fy`, `rated_days`**, cleaned box labels; drops bad dates / ranks / missing ids | **`df_oer_scrubbed`** |
| **3** | **Production handoff to 520** — map rater/SNR to assignment UIC at `eval_thru_dt` | **`df_oer_scrubbed`**, **`df_short_master_pde`** | OER: **`rater`, `snr_rater`, `eval_thru_dt`**; master: **`pid_pde`, `snpsht_dt`, `asg_uic_pde`** | **`rater_asg_uic_pde`, `snr_rater_asg_uic_pde`** | **`df_oer_enriched`** ← **520 Cell 4 loads this** |
| **4** | Legacy: `join_oer_to_snapshots` on full master | `df_master_pde_base`, `df_oer_enriched` | Full snapshot master + OER columns | Wide joined master (old path) | `df_master_pde_joined` |
| **5** | Legacy performance-model columns | joined master | experiment-specific | extra model cols | varies |
| **6** | Troubleshooting from intermediates | saved feathers | — | — | — |

### 512 → 520: columns Cell 4 actually uses

After `CLEAN_OER_COLS` and `running_vars/oer_cols_keep.json` (defaults in `pipeline_config.py`):

`rated_ofcr`, `eval_strt_dt`, `eval_thru_dt`, `rater`, `snr_rater`, `rater_box`, `snr_rater_box`, `eval_id` (plus optional UIC cols if still in keep-list — **not used for SNR pools** in current 520).

**`compo` in 512:** not used.

---

## Part B — Notebook 520 (snapshots → HERO → survival frame)

Each stage **carries** prior columns plus new ones (wide table). Cells 1–2 may **drop** names listed in `snap_cols_clean.json` (education / occupation junk columns in default config).

| Cell | What it does | Reads | Columns required | Creates (main) | Checkpoint |
|------|----------------|-------|------------------|----------------|------------|
| **0** | Imports, `pipeline_config`, cell logging; optional lookup tables | config | None on data | — | — |
| **1** | Load snapshot panel | **`df_502_base`** (typical) or `df_pipeline_01_raw` | **Diss:** `pid_pde`, `snpsht_dt`, `rank_pde`, `dor_cpt`, `dor_maj`, `yg`, `occ_crer_grp_cd`; **Opt:** `prestige_*`, `asg_uic_pde`, demographics | — | **`df_pipeline_01_raw`** |
| **2** | Commissioned ranks; drop officers with problematic MOS; column scrub | `01` | **`rank_pde`**; **`occ_crer_grp_cd`** if job filter runs | — (subset) | **`df_pipeline_02_base`** |
| **3** | Attach **`yg`** | `02` | **`ofcr_apnt_dt`** if yg missing; **`compo` only** when building yg via `build_yg_dict_501` (`compo_filter='R'`) — **skipped if yg already on 502** | **`yg`** | **`df_pipeline_03_base`** |
| **4** | Paint OER on each snapshot; cumulative TB metrics | **`03`**, **`df_oer_enriched`** | Snaps: **`pid_pde`, `snpsht_dt`**; OER: `CELL6_COLUMN_MAPPING` fields | Fwd/bwd rater/SNR ids and dates; **`cum_*`**, **`tb_ratio_fwd/bwd_*`** (rtr + snr) | **`df_pipeline_04a_basic_metrics`** |
| **5** | Pool LOO means, minus-means, sizes | `04a` | **`snpsht_dt`**, **`snr_rater_bwd`** (plus anchor cols per `POOL_GROUPING_MODE`), **`tb_ratio_*_snr`** | **`pool_tb_ratio_mean_*`, `pool_minus_mean_*`, `pool_size_*`** | **`df_pipeline_05_pool_means`** |
| **6** | Pool ranks / percentiles / z (or pass-through copy of 05) | `05` | Same pool keys + TB ratios | **`pool_tb_ratio_rank_*`, `*_rank_pct_*`, `pool_tb_ratio_zpool_*`** if ranks run | **`df_pipeline_06_pool_ranks`** |
| **7** | Time-varying enrichment | `06` | **Diss:** `snpsht_dt`, `pid_pde`, **`occ_crer_grp_cd`**; **Opt:** **`asg_uic_pde`, `fy`** for prestige/div | **`fy`** (if missing), **`job_code`**, **`prestige_unit`, `prestige_sum`**; **Opt:** **`div_name`**, division metrics | **`df_pipeline_07_time_varying`** |
| **8** | Static / officer-level fields | `07` | **Opt:** `pn_sex_cd`, `dor_cpt`, `date_birth_pde`, `mrtl_stat_cd`, **`rank_pde`, `job_code`** | **`sex`**, **`age_cpt`**, **`married`**, **`final_job_code`**, **`job_code_changed`** | **`df_pipeline_08_combined`** |
| **9** | Study cohort filters (`filtering_params`) | `08` | **`snpsht_dt`**; **`yg`**; **`occ_crer_grp_cd` or `job_code`**; **`sex`** if gender filters on; **`rank_pde`** for “other job at CPT” rule; **Opt:** **`div_name`, `prestige_unit`** | — (row subset) | **`df_pipeline_09_filtered`** |
| **10** | Person–time intervals + **`event`** (competing risks) | `09` | **`pid_pde`, `snpsht_dt`, `dor_cpt`, `dor_maj`**; **`sex`, `yg`**; time-varying OER/pool cols per `COLUMN_CONFIG` | **`start_time`, `stop_time`, `event`** (0=censored, 1=promoted, 2=attrited); carries TV metrics onto intervals | **`df_pipeline_10_cox_ready`** |
| **10.5** | Z-scores + interaction terms (mainly for Cox) | `10` | Columns in `RUN_SCALE` / model lists | **`z_*`**, **`*_sq`**, interactions (e.g. `star_pool_interaction`) | **`df_pipeline_10_5_cox_zscored`** |
| **11** | Plot prep, CIF bars (simple proportions), save analysis slice | `10` (sometimes uses `10_5` columns in plots) | **Diss:** **`pid_pde`, `stop_time`, `event`** + HERO plot variables | Officer-level **`df_analysis`**; PNGs | **`df_pipeline_11_cox_analysis`** |
| **12** (+12.1–8) | CoxPH, partial effects, model curves | **`10_5`** preferred | Interval rows + **`z_*`** model columns | Fits / diagnostic plots (not required for diss bars) | in-memory / plot files |

**Event coding (Cell 10):** `dor_maj` → event 1; last snapshot before study end → attrition (2); else censored (0). Time origin: days from **`dor_cpt`**.

---

## Part C — Column flow (export / sensitivity)

| Topic | Where it enters | Needed when? |
|--------|-----------------|--------------|
| **`compo`** | Master / 502 | **Cell 3 only** if recalculating `yg` without 502; not Cell 2, 7, 9, 10 on typical Run 1 |
| **`asg_uic_pde`** | Master / 502 | **Cell 7** prestige (optional); **Cell 9** division filters (usually off); **not** for OER SNR pools |
| **`occ_crer_grp_cd` / `job_code`** | Master | **Cells 2, 9** filtering; **Cell 7** builds `job_code` |
| **`dor_cpt`, `dor_maj`** | 502 | **Cell 10** — **Diss** |
| **`rater`, `snr_rater` → `snr_rater_bwd`** | `df_oer_enriched` via Cell 4 | **Cells 5–6** pools — **Diss** |
| **`sex`, prestige, `div_name`** | Cells 7–8 | **Cell 9** if filters enabled; omit from export if filters frozen and out of Ch.3 scope |

### Quick answers

- **Cell 2** does **not** need **`compo`**.
- **Cell 7** does **not** need **`compo`**; it may need **`asg_uic_pde`** + **`fy`** for prestige (often already on `df_502_base`).
- **`compo`** matters mainly for **`yg`** reconstruction in **Cell 3** when not loading 502’s `yg`.

---

## Part D — Dissertation-minimal export (`df_pipeline_11`)

**Run on Vantage through Cell 11** (Cell 12 optional). Primary PDE export artifact: **`df_pipeline_11_cox_analysis.feather`**.

**Include (HERO / mosaic / `talent/re_entry/army_basic_plots.py`):**

- Keys / outcome: `pid_pde`, `start_time`, `stop_time`, `event`
- Pool / performance: `tb_ratio_fwd_snr`, `pool_tb_ratio_mean_snr_fwd`, `pool_minus_mean_snr_fwd`, `pool_size_snr_fwd`
- Z-columns if already computed: `z_tb_ratio_fwd_snr`, `z_pool_minus_mean_snr_fwd` (or recompute on Mac from raw metrics)
- Overlap panel: `snpsht_dt`, `snr_rater_bwd`, `eval_thru_dt_bwd`

**Typically exclude from scrubbed export:** global `pid_pde` / rater ids (re-ambiguate per project), `asg_uic_pde`, `div_name`, prestige fields, sex/race, free text, raw cumulative counts if ratios are exported.

**Optional second file:** `df_pipeline_10_5_cox_zscored.feather` only if Cell 12 Cox work resumes.

---

## Part E — Cell 9 filters (config-driven)

Defined in `pipeline_config.py` → `filtering_params`. Columns touched:

| Filter block | Uses columns |
|--------------|----------------|
| `filter_dates` | `snpsht_dt` |
| `filter_job_codes` | `occ_crer_grp_cd`, `job_code`, `rank_pde`, `pid_pde` |
| `filter_gender` | `sex` (from Cell 8) |
| `filter_ygs` | `yg` |
| `filter_divisions` | `div_name`, `prestige_unit` (optional) |

---

## Part F — OER metric blocks created in 520 (reference)

**Cell 4 (per snapshot row):**  
`rtr_rater_fwd/bwd`, `snr_rater_fwd/bwd`, `rtr_rater_box_*`, `snr_rater_box_*`, `eval_strt_dt_*`, `eval_thru_dt_*`, `eval_id_*`, `cum_evals_fwd/bwd_*`, `cum_tb_fwd/bwd_*`, `tb_ratio_fwd/bwd_rtr`, `tb_ratio_fwd/bwd_snr`.

**Cell 5–6 (pools, both rtr and snr, fwd and bwd suffixes):**  
`pool_tb_ratio_mean_*`, `pool_minus_mean_*`, `pool_size_*`; optionally `pool_tb_ratio_rank_*`, `pool_tb_ratio_rank_pct_*`, `pool_tb_ratio_zpool_*`.

**HERO axis (Run 1, forward SNR):** own `tb_ratio_fwd_snr`; peer context `pool_minus_mean_snr_fwd` (LOO minus pool mean).

---

## PDF conversion (Charles)

From repo root:

```bash
./scripts/convert_single_md_to_pdf.sh talent/documents/512_520_CELL_COLUMN_INVENTORY.md
```

Use `pdf_styles_narrow.css` if tables need more horizontal room.

---

*Thread context: PDE re-ambiguated export; March run of record `TALENT_NET_export_20260320-1000`; Ch.3 disposable log: `3-Master_Plan/re_entry/_DISPOSABLE_Ch3_data_empirics_thread.md`.*
