# Competing risks: own TB “high / med / low” (advisor add-on)

## What you asked for

- Keep **pool** definition and **timeline** (Cox / Cell 11 setup) the **same** as the current inverted-U work.
- **Stratify officers** by **their own** TB ratio into **three** groups (tertiles: low, medium, high on the column you pick, default **`z_tb_ratio_fwd_snr`** from the **last** interval per officer).
- For **each** stratum, run the same **competing-risks** figure (and, when enabled, the **promotion** and **attrition CIF bar** panels) so you get **up to three** parallel sets: **3 × (CR curve + CIF bar pair)** for each `plot_spec` in `PLOT_CONFIG` with `plot_type: competing_risks`.

## How it is implemented

1. **`pipeline_config.py` → `CR_TB_STRATIFY_CONFIG`**
   - Set **`"enabled": True`** to turn the add-on on.
   - Adjust **`tb_stratify_col`** if your advisor wants raw TB ratio instead of z (e.g. `tb_ratio_fwd_snr`).

2. **`talent_pipeline/cr_tb_stratify.py`**
   - Adds **`_cr_tb_stratum`** to a copy of `df_analysis` (per-officer tertile, mapped to all intervals).
   - **`run_tb_stratified_cr_after_main`**: re-runs only **`competing_risks`** specs; appends **`_low_tb` / `_med_tb` / `_high_tb`** to each plot `name` and filename.

3. **`520_pipeline_cox_working.ipynb` Cell 11**
   - The **main** loop is **unchanged** (your current inverted-U run still happens once on the full sample).
   - **After** the main loop, if **`CR_TB_STRATIFY_CONFIG["enabled"]`**, the notebook calls the add-on. Counts are printed: **`TB-stratified CR add-on: X created, Y skipped`**.

## How to use

1. Confirm **`tb_stratify_col`** exists on the Cox / analysis frame (and has reasonable coverage on last-snapshot rows).
2. Set **`CR_TB_STRATIFY_CONFIG["enabled"] = True`**, save, **`reload_pipeline_config()`** in 520 (or restart kernel) if you use that pattern.
3. Run **Cell 11** as usual. Outputs go to the same **`PLOT_CONFIG['plot_dir']`**, with **`_low_tb` / `_med_tb` / `_high_tb`** in the filename stem.

## Interpreting results

- **Within a stratum**, the **x** axis (pool bins) is the same construction as the pooled plot; the **y** (final CIF / bar height) is **no longer** a population average—it is the subgroup of officers in that own-TB tertile.
- **Sample size** can shrink a lot in each stratum; sparse bins may be **skipped** (see `prepare_plot_data` / `min_group_size`).

## Optional separate notebook

A standalone notebook is **not required**: toggling the config and re-running Cell 11 is enough. If you later want a **notebook-only** experiment without opening the full 520, we can add a small **`521_*.ipynb`** that loads a saved `df_cox` feather and calls the same functions.

---

*Coda, April 2026.*
