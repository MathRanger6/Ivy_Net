# Army pool sensitivity — run matrix (for dummies)

**Goal:** See how **pool grain**, **TB-zero exclusion**, and **straight LOO vs minus-mean** change **H_sort** (panel 5) and **HERO porch** (panel 9).

**Always work from AWS 520 root** (`Network_1P_shell/` — folder with `big_dfs/`, `520_pipeline_cox_working.ipynb`, `talent/re_entry/`).

**Vocabulary (one time):**

| Plain English | Config / column |
|---------------|-----------------|
| **Pool grain = LEGACY** | `POOL_GROUPING_MODE = 'legacy'` — peers = same snapshot × same SNR rater |
| **Pool grain = THRU** | `POOL_GROUPING_MODE = 'active_at_eval_thru'` — peers active at OER **eval thru** date |
| **Keep TB zeros in pool** | `POOL_EXCLUDE_PEER_TB_ZERO = False` |
| **Drop TB-zero peers from pool mean** | `POOL_EXCLUDE_PEER_TB_ZERO = True` |
| **Straight LOO (T̂_j)** — basketball-style pond level | Column `pool_tb_ratio_mean_snr_fwd` |
| **Minus-mean** — player minus team mean | Column `pool_minus_mean_snr_fwd` / HERO `z_pool_minus_mean_snr_fwd` |

**Five runs (3 notebook + 2 plot-only):**

| Run | Grain | TB zeros in pool? | Peer X in plots | Notebook re-run? |
|-----|-------|-------------------|-----------------|------------------|
| **1 · LEGACY** | legacy | keep | straight LOO | **Yes** |
| **2 · THRU** | active_at_eval_thru | keep | straight LOO | **Yes** |
| **3 · THRU_NOZERO** | active_at_eval_thru | exclude | straight LOO | **Yes** |
| **4 · LEGACY_MINUS** (optional) | legacy | keep | minus-mean | **No** — reuse Run 1 feather |
| **5 · THRU_MINUS** (optional) | thru | keep | minus-mean | **No** — reuse Run 2 feather |

**What to compare for Alex (PD41):** Panel **5** title line (`H_sort=…`) and panel **9** porch shape. Write numbers in the table at the bottom of this file.

---

# RUN 1 · LEGACY · straight LOO · keep TB zeros

**What this run means:** Old pool definition + peer pond **level** (not minus-mean). Baseline reference.

## 1a · RUN these commands in the terminal (AWS)

```bash
cd /path/to/Network_1P_shell
conda activate TALNET39
date
ls -lh big_dfs/df_pipeline_11_cox_analysis.feather
```

(The last line is optional — just confirms whether an old feather exists before you rebuild it in step 1d.)

## 1b · EDIT `pipeline_config.py` at 520 root, then SAVE

Change these lines to these exact values:

```python
POOL_GROUPING_MODE = 'legacy'
POOL_EXCLUDE_PEER_TB_ZERO = False
CELL5_POOL_MEANS = True
CELL6_POOL_RANKS = True
```

Save the file.

## 1c · EDIT two plot scripts on AWS, then SAVE (do not run anything yet)

**Purpose:** Tell the plot code to use **straight LOO pond level**, not minus-mean and not the missing z-column.

**EDIT file 1:** open `talent/re_entry/army_basic_plots.py` in JupyterLab.

Go to **line 42**.

Change the line so it reads exactly:

```python
COL_LOO = "pool_tb_ratio_mean_snr_fwd"
```

Save the file.

**EDIT file 2:** open `talent/re_entry/army_hero_slide_plot.py`.

Go to **line 44**.

Change the line so it reads exactly:

```python
plot_var = "pool_tb_ratio_mean_snr_fwd"
```

Save the file.

**SKIP file 3:** do **not** edit `army_act2_probes.py` for Run 1.

**Do not** set `plot_var` to `z_pool_tb_ratio_mean_snr_fwd` — that column is not in the feather unless you later run Path B (Cell 10.5 with a config change).

**Nothing to check in this step** — only edit and save the two files above.

## 1d · RUN notebook cells in this order (JupyterLab)

Open `520_pipeline_cox_working.ipynb`.

RUN **Cell 0** (reloads config from step 1b).

RUN **Cell 5** (pool means — in the log, confirm you see `POOL_GROUPING_MODE='legacy'`).

RUN **Cell 6** (pass-through is OK) **OR** if Cell 6 errors, RUN this in the terminal instead:

```bash
cp big_dfs/df_pipeline_05_pool_means.feather big_dfs/df_pipeline_06_pool_ranks.feather
```

RUN **Cell 7**.

RUN **Cell 8**.

RUN **Cell 9**.

RUN **Cell 10**.

RUN **Cell 10.5**.

RUN **Cell 11** (writes `big_dfs/df_pipeline_11_cox_analysis.feather`).

## 1e · RUN this check in the terminal (after Cell 11)

```bash
python3 - <<'PY'
import pandas as pd
df = pd.read_feather("big_dfs/df_pipeline_11_cox_analysis.feather")
for c in ["pool_tb_ratio_mean_snr_fwd", "pool_minus_mean_snr_fwd", "z_pool_minus_mean_snr_fwd"]:
    print(c, "YES" if c in df.columns else "MISSING")
PY
```

Expect `pool_tb_ratio_mean_snr_fwd: YES`.

## 1f · RUN these plot commands in the terminal, then EDIT the manifest, then RUN mosaic

RUN:

```bash
python talent/re_entry/army_basic_plots.py --all
python talent/re_entry/army_act2_probes.py --plot all_probes
python talent/re_entry/army_hero_slide_plot.py --plot-var pool_tb_ratio_mean_snr_fwd
```

EDIT **`manifests/army_run1_3x3_manifest.json`**: set panel 9 `"path"` to exactly:

```text
talent/re_entry/output/hero/ARMY_HERO_ew8_pool_tb_ratio_mean_snr_fwd_run1.png
```

Save the manifest.

RUN:

```bash
python talent/re_entry/build_army_data_story.py
```

## 1g · RUN these checks — did Run 1 work?

```bash
grep POOL_GROUPING_MODE pipeline_config.py
ls -l talent/re_entry/output/hero/ARMY_HERO_ew8_pool_tb_ratio_mean_snr_fwd_run1.png
ls -l talent/re_entry/output/data_story/ARMY_DATA_STORY_run1_3x3.png
```

In the **BDP log**, find the line:

```text
Overlap pool grain: POOL_GROUPING_MODE='legacy'
```

Open panel 5 PNG — note **H_sort** in the title.

Open panel 9 — note porch shape.

## 1h · RUN this backup command before you start Run 2

Also RUN (saves feather for optional Run 4 later):

```bash
cp big_dfs/df_pipeline_11_cox_analysis.feather big_dfs/df_pipeline_11_run1_legacy.feather
```

```bash
bash scripts/backup_rename_suffix.sh _run1_legacy --all-output
```

---

# RUN 2 · THRU · straight LOO · keep TB zeros

**What this run means:** Same peer metric as Run 1, but **eval-thru pool grain** — isolates **grain / assortativity** effect.

## 2a · Before you start

```bash
cd /path/to/Network_1P_shell
```

## 2b · `pipeline_config.py`

```python
POOL_GROUPING_MODE = 'active_at_eval_thru'
POOL_EXCLUDE_PEER_TB_ZERO = False
CELL5_POOL_MEANS = True
CELL6_POOL_RANKS = True
```

Save.

## 2c · Plot scripts

**Same as Run 1** — straight LOO (`pool_tb_ratio_mean_snr_fwd`).

No change if you already set Run 1 values.

## 2d · Notebook cells

Same order as Run 1: **0 → 5 → 6 (or cp) → 7 → 8 → 9 → 10 → 10.5 → 11**.

Watch Cell 5 log for `POOL_GROUPING_MODE='active_at_eval_thru'`.

## 2e · Feather sanity check

Same probe as Run 1e.

## 2f · CLI

Same as Run 1f.

Manifest panel 9 path unchanged (same HERO filename).

## 2g · Checks

```bash
grep POOL_GROUPING_MODE pipeline_config.py
```

BDP log must show:

```text
Overlap pool grain: POOL_GROUPING_MODE='active_at_eval_thru'
```

Compare **H_sort** and **HERO porch** to Run 1 backup in `output/*/run1_legacy/`.

## 2h · Save before Run 3

**Feather first** (Run 5 plot-only needs this archive — same pattern as Run 1 → Run 4):

```bash
cp big_dfs/df_pipeline_11_cox_analysis.feather big_dfs/df_pipeline_11_run2_thru.feather
```

**Then** plot backup:

```bash
bash scripts/backup_rename_suffix.sh _run2_thru --all-output
```

---

# RUN 3 · THRU · straight LOO · exclude TB-zero peers

**What this run means:** Same grain as Run 2, but peers with **tb_ratio == 0** dropped from pool mean/size.

## 3a · Before you start

```bash
cd /path/to/Network_1P_shell
```

## 3b · `pipeline_config.py`

```python
POOL_GROUPING_MODE = 'active_at_eval_thru'
POOL_EXCLUDE_PEER_TB_ZERO = True
CELL5_POOL_MEANS = True
CELL6_POOL_RANKS = True
```

Save.

## 3c · Plot scripts

**Same as Run 1** — straight LOO. No change.

## 3d · Notebook cells

Same order: **0 → 5 → 6 (or cp) → 7 → 8 → 9 → 10 → 10.5 → 11**.

Cell 5 log should mention `POOL_EXCLUDE_PEER_TB_ZERO=True` if enabled in code.

## 3e · Feather sanity check

Same as Run 1e.

Optional:

```bash
python -u talent/re_entry/army_pool_size_probe.py
```

## 3f · CLI

Same as Run 1f.

## 3g · Checks

Compare **H_sort** and **HERO** to Run 2 backup (`_run2_thru`).

## 3h · Save

**Feather first:**

```bash
cp big_dfs/df_pipeline_11_cox_analysis.feather big_dfs/df_pipeline_11_run3_thru_nozero.feather
```

**Then** plot backup:

```bash
bash scripts/backup_rename_suffix.sh _run3_thru_nozero --all-output
```

---

# RUN 4 · LEGACY · minus-mean (optional · plot-only)

**What this run means:** Old **relative standing** peer X on the **same feather as Run 1**. No notebook.

## 4a · Before you start

Restore Run 1 feather — plot scripts read **`big_dfs/df_pipeline_11_cox_analysis.feather`**, which after Run 3 is **thru + nozero**, not legacy.

**SAVE after Run 1 notebook** (section 1h — archive legacy grain):

```bash
cp big_dfs/df_pipeline_11_cox_analysis.feather big_dfs/df_pipeline_11_run1_legacy.feather
```

**RESTORE before Run 4 plots** (copy archived Run 1 **back** into the live slot):

```bash
cp big_dfs/df_pipeline_11_run1_legacy.feather big_dfs/df_pipeline_11_cox_analysis.feather
```

If `df_pipeline_11_run1_legacy.feather` does not exist, re-run the Run 1 notebook first, then SAVE, then RESTORE as above.

## 4b · `pipeline_config.py`

**No change required** for plots (feather already built).

## 4c · Plot scripts — minus-mean

**`army_basic_plots.py` line 42:**

```python
COL_LOO = "pool_minus_mean_snr_fwd"
```

**`army_hero_slide_plot.py` line 44:**

```python
plot_var = "z_pool_minus_mean_snr_fwd"
```

Save.

## 4d · Notebook

**Skip** — use Run 1 feather (RESTORE in **4a** if you already ran Runs 2–3).

## 4e · Feather check

```bash
python3 - <<'PY'
import pandas as pd
df = pd.read_feather("big_dfs/df_pipeline_11_cox_analysis.feather")
print("z_pool_minus_mean_snr_fwd", "YES" if "z_pool_minus_mean_snr_fwd" in df.columns else "MISSING")
PY
```

## 4f · CLI

```bash
python talent/re_entry/army_basic_plots.py --all
python talent/re_entry/army_act2_probes.py --plot all_probes
python talent/re_entry/army_hero_slide_plot.py --plot-var z_pool_minus_mean_snr_fwd
```

Manifest panel 9:

```text
talent/re_entry/output/hero/ARMY_HERO_ew8_z_pool_minus_mean_snr_fwd_run1.png
```

```bash
python talent/re_entry/build_army_data_story.py
```

## 4g · Checks

Panel 5 **H_sort** should match Run 1 (same grain — only peer X axis changed on panels 3/7/8/9).

Panel 9 porch may look **different** from Run 1 even though grain is the same.

## 4h · Save

```bash
bash scripts/backup_rename_suffix.sh _run4_legacy_minusmean --all-output
```

---

# RUN 5 · THRU · minus-mean (optional · plot-only)

**What this run means:** Minus-mean peer X on **Run 2 thru feather**.

## 5a · Restore Run 2 feather

**RESTORE** (archived Run 2 → live slot plots read):

```bash
cp big_dfs/df_pipeline_11_run2_thru.feather big_dfs/df_pipeline_11_cox_analysis.feather
```

That archive must exist from **Run 2h** (`cox_analysis` → `run2_thru`). If you skipped 2h feather save, either:

- Re-run the **Run 2 notebook** (2b config), SAVE again with the **2h** `cp`, then proceed; or  
- Check `ls -lh big_dfs/df_pipeline_11_run2_thru.feather` — you may have saved it without the checklist telling you.

## 5b · `pipeline_config.py`

No notebook change.

## 5c · Plot scripts

**Same minus-mean settings as Run 4c.**

## 5d · Notebook

**Skip.**

## 5e · Feather check

Same as Run 4e.

## 5f · CLI

Same as Run 4f.

## 5g · Checks

Panel 5 **H_sort** should match Run 2.

Compare panel 9 to Run 4 — shows minus-mean vs straight LOO at **thru** grain.

## 5h · Save

```bash
bash scripts/backup_rename_suffix.sh _run5_thru_minusmean --all-output
```

---

# After all runs — fill this in for Alex

| Run | Grain | TB zero excl? | Peer X | H_sort (panel 5) | HERO porch note |
|-----|-------|---------------|--------|------------------|-----------------|
| 1 legacy | legacy | no | straight LOO | | |
| 2 thru | active_at_eval_thru | no | straight LOO | | |
| 3 thru nozero | active_at_eval_thru | yes | straight LOO | | |
| 4 legacy minus | legacy | no | minus-mean | | |
| 5 thru minus | active_at_eval_thru | no | minus-mean | | |

**Feather archive cheat sheet** (each SAVE is in that run’s **·h** section):

| After run | SAVE command |
|-----------|----------------|
| Run 1 | `cp ..._cox_analysis.feather ..._run1_legacy.feather` ( **1h** ) |
| Run 2 | `cp ..._cox_analysis.feather ..._run2_thru.feather` ( **2h** ) |
| Run 3 | `cp ..._cox_analysis.feather ..._run3_thru_nozero.feather` ( **3h** ) |

---

# Common mistakes (read when tired)

- **Run 5 needs `run2_thru.feather`** — SAVE in **2h**, RESTORE in **5a**. Plot backup alone (`backup_rename_suffix.sh`) does **not** save feathers.
- HERO fails with `Column not in feather: z_pool_tb_ratio_mean_snr_fwd` → use **`pool_tb_ratio_mean_snr_fwd`** for straight LOO (Runs 1–3).
- Mosaic fails `FileNotFoundError` → manifest panel 9 path must **exactly match** HERO output filename.
- Changed `pipeline_config.py` but **did not re-run Cell 5→11** → feather still old grain.
- Cell 0 loads `pipeline_config_div_name` → OK (it imports `pipeline_config`).
- Straight LOO scripts + legacy feather = **valid**; thru feather + minus-mean manifest = **broken names** only.

---

*Created 2026-09-22 — COMPOSER for Charles AWS sensitivity matrix.*
