# Straight-LOO mosaic on AWS — step-by-step

**Goal:** Rebuild the Run 1 **3×3 data story** so peer context on panels **1, 3, 7, 8, 9** uses **straight LOO pond level** (`pool_tb_ratio_mean_snr_fwd` / `z_pool_tb_ratio_mean_snr_fwd`) — basketball `poolq_loo` analog — instead of **relative standing** (`pool_minus_mean_snr_fwd` / `z_pool_minus_mean_snr_fwd`).

**Unchanged panels:** 2 (already shows T̂_j = straight LOO), 4, 5, 6.

**Run from:** 520 root (`Network_1P_shell/` or equivalent — folder with `big_dfs/`, `pipeline_config.py`, `520_pipeline_cox_working.ipynb`, `talent/re_entry/`).

---

## YOU ARE HERE

| Step | Task | Status |
|------|------|--------|
| 0 | Baseline upload + `active_at_eval_thru` BDP complete | ☐ |
| 1 | Choose Path A (mosaic-only) or Path B (z in feather) | ☐ |
| 2 | Edit `talent/re_entry/*.py` (+ optional manifest) | ☐ |
| 3 | Path B only: edit `pipeline_config_17_1.py` + Cells 10.5–11 | ☐ |
| 4 | Probes → BDP pipeline → mosaic | ☐ |
| 5 | Compare PNGs to minus-mean baseline | ☐ |

---

## 0. Prerequisites (do this first)

Complete the **baseline** upload from [`AWS_UPLOAD_CHECKLIST.md`](AWS_UPLOAD_CHECKLIST.md):

1. `POOL_GROUPING_MODE = 'active_at_eval_thru'` in `pipeline_config.py`
2. `POOL_EXCLUDE_PEER_TB_ZERO = False` (baseline; TB-zero sensitivity is a separate pass)
3. Cells **0 → 11** already run; feather exists:
   ```bash
   ls -lh big_dfs/df_pipeline_11_cox_analysis.feather
   ```
4. Baseline minus-mean mosaic saved (for side-by-side):
   ```bash
   cp talent/re_entry/output/data_story/ARMY_DATA_STORY_run1_3x3.png \
      talent/re_entry/output/data_story/ARMY_DATA_STORY_run1_3x3_minus_mean.png
   ```

---

## 1. Choose your path

| | **Path A — mosaic-only** | **Path B — z in feather (recommended)** |
|---|--------------------------|----------------------------------------|
| **Notebook re-run** | None (if columns already in feather) | **Cell 10.5 → Cell 11** |
| **HERO x-axis** | Raw `pool_tb_ratio_mean_snr_fwd` or on-the-fly z in Act II | `z_pool_tb_ratio_mean_snr_fwd` from Cell 10.5 |
| **Cox / CR plots** | Unchanged (still minus-mean Run 1) | Run profile switches to straight LOO |
| **Time on AWS** | ~5–15 min (plots only) | ~30–90 min (+ standardize export) |

**Recommendation:** Path B if Alex should see **z-scored** pond level (parity with current `z_pool_minus_mean` HERO). Path A for a quick visual before committing to a new Run profile.

---

## 2. Quick column probe (both paths)

From 520 root:

```bash
python3 - <<'PY'
import pandas as pd
p = "big_dfs/df_pipeline_11_cox_analysis.feather"
df = pd.read_feather(p)
cols = [
    "tb_ratio_fwd_snr",
    "pool_tb_ratio_mean_snr_fwd",
    "pool_minus_mean_snr_fwd",
    "z_tb_ratio_fwd_snr",
    "z_pool_minus_mean_snr_fwd",
    "z_pool_tb_ratio_mean_snr_fwd",
    "pool_size_snr_fwd",
]
for c in cols:
    ok = c in df.columns
    n = df[c].notna().sum() if ok else 0
    print(f"  {c}: {'YES' if ok else 'MISSING'}  n={n:,}")
PY
```

- **`pool_tb_ratio_mean_snr_fwd`** should be **YES** after any successful Cell 5+ run.
- **`z_pool_tb_ratio_mean_snr_fwd`** is **MISSING** until Path B (Cell 10.5 with updated standardize list).

Pool-size sanity (unchanged by LOO metric choice):

```bash
python -u talent/re_entry/army_pool_size_probe.py
```

---

## 3. Path B — notebook + Run profile (z column in feather)

### 3a. Confirm Cell 0 loads Run 1 override

Open `520_pipeline_cox_working.ipynb` → **Cell 0** (session/import cell).

| Cell 0 line | Check |
|-------------|-------|
| **L57** `pip_config_file = '...'` | Must resolve to **`pipeline_config_17_1`** on AWS (not `pipeline_config_div_name` unless that file mirrors Run 1). |
| **L166** (after run) | Prints `STANDARDIZE_CONFIG['cols']` — note current list. |

Re-run **Cell 0** after any edit to `pip_config_file`.

### 3b. Edit `pipeline_config_17_1.py` (520 root)

Replace **pool minus mean** with **straight LOO mean** in the Run 1 profile:

| Line | From | To |
|------|------|-----|
| **34** `tv_vars` | `[TB_RATIO_SNR_COL, POOL_MINUS_MEAN_SNR_COL]` | `[TB_RATIO_SNR_COL, POOL_TB_RATIO_MEAN_SNR_COL]` |
| **35** `quadratic_bases` | `[TB_RATIO_SNR_COL, POOL_MINUS_MEAN_SNR_COL]` | `[TB_RATIO_SNR_COL, POOL_TB_RATIO_MEAN_SNR_COL]` |
| **36** `combined_effect_base` | `POOL_MINUS_MEAN_SNR_COL` | `POOL_TB_RATIO_MEAN_SNR_COL` |
| **40** `var_y_label` | `'Pool minus mean'` | `'Pool LOO mean (T̂_j)'` |

**CR plot block (lines 77–81):** auto-updates on next Cell 0 reload because `_cr_var_pool` uses `POOL_MINUS_MEAN_SNR_COL` today — after the swap it becomes `z_pool_tb_ratio_mean_snr_fwd` when `RUN_SCALE='z'`.

Optional semantic alias in `pipeline_config.py` (lines **258–259**):

```python
POOL_CONTEXT_SNR_COL = POOL_TB_RATIO_MEAN_SNR_COL  # was POOL_MINUS_MEAN_SNR_COL
```

Not required for the mosaic; documents the Run fork.

### 3c. Notebook run order (Path B)

| Order | Notebook cell | What it does |
|-------|---------------|--------------|
| 1 | **Cell 0** | Reload configs; verify `STANDARDIZE_CONFIG['cols']` includes `pool_tb_ratio_mean_snr_fwd` |
| 2 | **Cell 10.5** | Creates `z_pool_tb_ratio_mean_snr_fwd` (+ interaction/quadratic chain) |
| 3 | **Cell 11** | Re-exports `big_dfs/df_pipeline_11_cox_analysis.feather` |

**Do not re-run Cell 5** unless you changed pool grain or `POOL_EXCLUDE_*` — straight LOO mean already exists in the feather from Cell 5.

Re-run the **column probe** (§2); expect `z_pool_tb_ratio_mean_snr_fwd: YES`.

---

## 4. Edit plotting scripts (both paths)

All paths below: edit files under `talent/re_entry/` on AWS (same paths as Mac).

### 4a. `army_basic_plots.py` — Panel 3

| Line | Change |
|------|--------|
| **42** | `COL_LOO = "pool_tb_ratio_mean_snr_fwd"` (was `pool_minus_mean_snr_fwd`) |
| **631** | x-label → `pool_tb_ratio_mean_snr_fwd (LOO pond level)` |
| **633** | title → `Peer pool quality (straight LOO mean)` |
| **646** | x-label → `pool_tb_ratio_mean_snr_fwd` |

**Note:** Output filename stays `ARMY_BDP_pool_minus_mean_loo_run1.png` (stem at line **653**) — content changes; manifest path unchanged. Optional: change stem to `_pool_tb_ratio_mean_loo_` and update manifest panel 3 path.

### 4b. `army_act2_probes.py` — Panels 7 & 8

| Line | Change |
|------|--------|
| **55** | `COL_LOO_Z = "z_pool_tb_ratio_mean_snr_fwd"` |
| **59** | In `OER_CHECK_COLS`, keep both raw columns; order does not matter |

Fallback behavior (lines **247–250**): if z column missing, Act II z-scores **`COL_LOO`** within the filtered panel. So Path A works when **42** in `army_basic_plots.py` is synced and you set `COL_LOO` import — Act II imports `COL_LOO` from `army_basic_plots`, so **4a must be done first**.

### 4c. `army_hero_slide_plot.py` — Panel 9

| Line | Path A | Path B |
|------|--------|--------|
| **44** `plot_var` | `"pool_tb_ratio_mean_snr_fwd"` | `"z_pool_tb_ratio_mean_snr_fwd"` |

Or pass at runtime (no default edit):

```bash
./talent/re_entry/army_hero_slide_plot.py --plot-var z_pool_tb_ratio_mean_snr_fwd
```

Expected output: `talent/re_entry/output/hero/ARMY_HERO_ew8_z_pool_tb_ratio_mean_snr_fwd_run1.png`

---

## 5. Manifest (panels 1 & 9 + footer)

**Option 1 — overwrite default manifest** (`manifests/army_run1_3x3_manifest.json`):

| Field | New value |
|-------|-----------|
| `title` | `... straight LOO pond (T̂_j) ...` |
| `subtitle` / `footer` | Replace `z_pool_minus_mean` → `z_pool_tb_ratio_mean_snr_fwd` |
| Panel 1 line **Peer X:** | `z_pool_tb_ratio_mean_snr_fwd (straight LOO HERO)` |
| Panel 1 **Reigning tag:** | `ew8_z_pool_tb_ratio_mean_snr_fwd_run1` |
| Panel 9 `path` | `.../ARMY_HERO_ew8_z_pool_tb_ratio_mean_snr_fwd_run1.png` |
| `verdict.hero_reigning` | `ew8_z_pool_tb_ratio_mean_snr_fwd_run1` |
| `verdict.peer_pool` | `senior-rater straight LOO mean (forward SNR)` |

**Option 2 — side-by-side deck (recommended):** Copy manifest to `manifests/army_run1_3x3_straight_loo_manifest.json`, edit copy only, build with:

```bash
./talent/re_entry/build_army_data_story.py \
  --manifest talent/re_entry/manifests/army_run1_3x3_straight_loo_manifest.json
```

Output: set `"output_png"` in that manifest (e.g. `ARMY_DATA_STORY_run1_3x3_straight_loo.png`).

Panel 3 path: unchanged unless you renamed the BDP stem in §4a.

---

## 6. Run order on AWS

From 520 root, after script edits (and Path B feather refresh):

```bash
chmod +x talent/re_entry/*.py talent/re_entry/*.sh

# 1 — pool probe (informational; same feather)
python -u talent/re_entry/army_pool_size_probe.py

# 2 — BDP panels 2–6 + panel 3 + Act II + HERO
bash talent/re_entry/run_army_bdp_pipeline.sh
```

**Or stepwise** (easier to debug):

```bash
./talent/re_entry/army_basic_plots.py --all
./talent/re_entry/army_act2_probes.py --plot all_probes
./talent/re_entry/army_hero_slide_plot.py --plot-var z_pool_tb_ratio_mean_snr_fwd   # Path B
# ./talent/re_entry/army_hero_slide_plot.py --plot-var pool_tb_ratio_mean_snr_fwd  # Path A
./talent/re_entry/build_army_data_story.py
# add --manifest ... if using straight_loo manifest copy
```

**Do not need** for this mosaic fork: Cell 12 Cox refit (unless you want CR/Cox slides aligned with Path B profile).

---

## 7. Success checklist

| Artifact | Straight LOO expected |
|----------|----------------------|
| Panel 3 PNG | Histogram centered on **positive** pond TB levels (not mean ≈ 0 like minus-mean) |
| Panel 7 | `ARMY_CCT_promotion_rate_pool_loo_run1_z1_2_q8.png` — bins use pond z, not minus-mean z |
| Panel 8 | `ARMY_ELITE_pond_loo_pw3p5_run1_top20.png` |
| Panel 9 | `ARMY_HERO_ew8_z_pool_tb_ratio_mean_snr_fwd_run1.png` |
| Mosaic | `ARMY_DATA_STORY_run1_3x3_straight_loo.png` (or overwritten default) |

Spot-check panel 9 sidecar JSON:

```bash
cat talent/re_entry/output/hero/ARMY_HERO_ew8_z_pool_tb_ratio_mean_snr_fwd_run1.json | head -20
```

Confirm `"plot_var": "z_pool_tb_ratio_mean_snr_fwd"`.

---

## 8. What each panel uses (reference)

| Panel | Variable after switch |
|-------|----------------------|
| 1 | Text only |
| 2 | `tb_ratio_fwd_snr` vs `pool_tb_ratio_mean_snr_fwd` (no change) |
| 3 | **`pool_tb_ratio_mean_snr_fwd`** |
| 4 | `tb_ratio_fwd_snr` only |
| 5 | Pool overlap on `z_tb_ratio_fwd_snr` + membership |
| 6 | `pool_size_snr_fwd` |
| 7–8 | **`z_pool_tb_ratio_mean_snr_fwd`** (or on-the-fly z of raw LOO mean) |
| 9 | **`z_pool_tb_ratio_mean_snr_fwd`** (or raw) |

---

## 9. Rollback

1. Restore `COL_LOO` / `COL_LOO_Z` / `plot_var` in the three `.py` files.
2. Restore `pipeline_config_17_1.py` `tv_vars` to `POOL_MINUS_MEAN_SNR_COL` if Path B was applied; re-run Cell 10.5 + 11.
3. Re-run `run_army_bdp_pipeline.sh` with original manifest.
4. Baseline PNG: `ARMY_DATA_STORY_run1_3x3_minus_mean.png` (§0).

---

## 10. Notebook cell index map (Mac canonical `520_pipeline_cox_working.ipynb`)

| Display label | Notebook cell index | Key lines |
|---------------|----------------------|-----------|
| Cell 0 (imports / config) | **2** | L57 `pip_config_file`; L175 pool toggles |
| **CELL 5** pool means | **20** | L15–34 `add_pool_means_and_sizes(...)` |
| **CELL 10.5** standardize | **48** | L9–11 `STANDARDIZE_CONFIG` |
| **CELL 11** Cox export | **53** | L95–98 reads standardize cols |

Cell 5 already writes **`pool_tb_ratio_mean_*`** and **`pool_minus_mean_*`** together; switching the mosaic does **not** require re-running Cell 5.

---

## Thread log

- **2026-09-21** — Initial guide: Path A/B, file line refs, AWS run order, probes, manifest fork.
