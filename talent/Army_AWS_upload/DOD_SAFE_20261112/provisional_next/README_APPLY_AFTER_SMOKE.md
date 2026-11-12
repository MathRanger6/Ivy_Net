# Provisional — do **not** copy over live Vantage files for smoke

**Purpose:** Side-by-side copies for **diff-and-paste** after B1–B3 smoke (HERO quick grid + feather column check).

## Workflow on virtual desktop

1. **Smoke:** deploy only **`../ship_shape/`** (see `ship_shape/README_UPLOAD.md`).
2. Run Cells **0–11** with `pipeline_config_div_name` + smoke HERO (`army_hero_grid_runner.py --quick`).
3. **If smoke passes:** open this folder on the VDI and compare each file below to the **live** file at 520 workspace root (WinMerge, `diff`, or Jupyter diff).
4. Paste **only** hunks you intend to keep — or replace whole file when you trust the zip copy.

## Files in this folder

| File | Why it might change next |
|------|---------------------------|
| `pipeline_config.py` | `STANDARDIZE_CONFIG`, pool column names |
| `pipeline_config_div_name.py` | Cox profile + extra z cols + **future Cell 11 CR for B1–B3** |
| `add_cum_oer_metrics_mod_working.py` | Cell 5 pool mean/loo/minus_loo |
| `cox_plot_helpers.py` | CR / CIF bar behavior |
| `520_pipeline_cox_working.ipynb` | Cells 10.5 / 11 / 12 if notebook edits needed |

## `drafts/` (optional — not deployed)

- `pipeline_config_div_name_CR_B123_draft.py` — **Phase 4 sketch:** extra CR plot entries for `z_pool_mean_snr_fwd`, `z_pool_loo_snr_fwd`, `z_pool_minus_loo_snr_fwd` (and bwd). Merge into live `pipeline_config_div_name.py` after HERO histograms look right.

## Cursor canonical path

Edits belong in git under `talent/talent_pipeline/` and `talent/re_entry/`; refresh `ship_shape/` + this folder before the next zip.
