# Competing risks: own TB “high / med / low” (advisor add-on)

## What you asked for

- Keep **pool** definition and **timeline** (Cox / Cell 11 setup) the **same** as the current inverted-U work.
- **Stratify officers** by **their own** TB ratio into **three** groups (tertiles: low, medium, high on the column you pick, default **`z_tb_ratio_fwd_snr`** from the **last** interval per officer).
- For **each** stratum, run the same **competing-risks** figure (and, when enabled, the **promotion** and **attrition CIF bar** panels) so you get **up to three** parallel sets: **3 × (CR curve + CIF bar pair)** for each `plot_spec` in `PLOT_CONFIG` with `plot_type: competing_risks`.

## How it is implemented

1. **`pipeline_config.py` → `CR_TB_STRATIFY_CONFIG`**
   - Set **`"enabled": True`** to turn the add-on on.
   - Adjust **`tb_stratify_col`** if your advisor wants raw TB ratio instead of z (e.g. `tb_ratio_fwd_snr`).
   - **`stratum_method`:** `"quantile"` (roughly equal officer counts per stratum via `pd.qcut`) or **`"equal_width"`** (equal range on the TB/z scale via `pd.cut`).

2. **`talent_pipeline/cr_tb_stratify.py`**
   - Adds **`_cr_tb_stratum`** to a copy of `df_analysis` (per-officer stratum from **last** row by `stop_time`, mapped to all intervals).
   - **`run_tb_stratified_cr_after_main`**: re-runs only **`competing_risks`** specs; appends **`_low_tb` / `_med_tb` / `_high_tb`** to each plot `name`.
   - **Filenames:** inserts **`_tbq_`** (quantile) or **`_tbew_`** (equal width) + stratum token so strata do not overwrite each other.
   - **Titles / metadata:** sets **`cr_tb_stratify_title_suffix`** (shown via `format_plot_title` / config box in `cox_plot_helpers.py`).

3. **`520_pipeline_cox_working.ipynb` Cell 11**
   - The **main** loop is **unchanged** (your current inverted-U run still happens once on the full sample).
   - **After** the main loop, if **`CR_TB_STRATIFY_CONFIG["enabled"]`**, the notebook calls the add-on. Counts are printed: **`TB-stratified CR add-on: X created, Y skipped`**.

## How to use

1. Confirm **`tb_stratify_col`** exists on the Cox / analysis frame (and has reasonable coverage on last-snapshot rows).
2. Set **`CR_TB_STRATIFY_CONFIG["enabled"] = True`**, save, **`reload_pipeline_config()`** in 520 (or restart kernel) if you use that pattern.
3. Run **Cell 11** as usual. Outputs go to the same **`PLOT_CONFIG['plot_dir']`**, with stratum and method tokens in the filename stem.

## Interpreting results

- **Own-TB strata** restrict **which officers** enter each rerun; **within-panel pool bins** still come from the plot spec’s **`variable`** / **`n_bins`** (usually pool-quality, not own-TB bins).
- **Within a stratum**, the **x** axis (pool bins) is the same construction as the pooled plot; the **y** (final CIF / bar height) is for that **subgroup** only.
- **Sample size** can shrink a lot in each stratum; sparse bins may be **skipped** (see `prepare_plot_data` / `min_group_size`).
- See **`CR_Red_Line_Flow_Explanation.md`** for how Cell 11 builds CR curves (last row per officer for plot bins; cumulative not instantaneous).

## Army AWS upload (when deploying)

Upload these live files (vs export `TALENT_NET_export_20260421-0802`): `520_pipeline_cox_working.ipynb`, `pipeline_config.py`, `cox_plot_helpers.py`, **`cr_tb_stratify.py`** (new).

## Optional separate notebook

A standalone notebook is **not required**: toggling the config and re-running Cell 11 is enough. If you later want a **notebook-only** experiment without opening the full 520, we can add a small **`521_*.ipynb`** that loads a saved `df_cox` feather and calls the same functions.

---

*CODA, April 2026 — updated with `stratum_method`, filename/title labeling.*
