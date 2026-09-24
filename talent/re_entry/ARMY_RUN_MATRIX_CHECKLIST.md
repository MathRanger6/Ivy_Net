# Army pool sensitivity — complete run matrix checklist

**Purpose:** Compare how **pool membership rules**, **excluding zero–talent-board peers**, and **peer context metric on plots** change **sorting index (panel 5, H_sort)** and **promotion-rate porch (panel 9, HERO)**.

**Where you work:** AWS **520 root** — the folder named `Network_1P_shell/` that contains:

- `big_dfs/`
- `520_pipeline_cox_working.ipynb`
- `pipeline_config.py`
- `talent/re_entry/` (plot scripts and manifest)
- `scripts/backup_rename_suffix.sh`

**What you compare for Alex (assortativity priority):**

- Panel **5** — read **H_sort** in the overlap plot title.
- Panel **9** — read **HERO** porch shape (promotion rate vs peer-context bins).
- Record values in the **results table** at the end of this document.

---

## Vocabulary (read once)

| Plain English | Setting or column name |
|---------------|------------------------|
| **Legacy pool grain** | `POOL_GROUPING_MODE = 'legacy'` — peers share the same HRC snapshot date and the same senior-rater identifier (`snr_rater_bwd`). |
| **Eval-thru pool grain** | `POOL_GROUPING_MODE = 'active_at_eval_thru'` — peers are senior-rater officers whose OER evaluation window **covers this row’s OER completion date** (`eval_thru_dt_bwd`). |
| **Keep zero–TB peers in pool** | `POOL_EXCLUDE_PEER_TB_ZERO = False` |
| **Drop zero–TB peers from pool mean and size** | `POOL_EXCLUDE_PEER_TB_ZERO = True` — removes **peers** with `tb_ratio == 0` from pool statistics; **does not** remove the rated officer from the cohort. |
| **Straight leave-one-out pond level (T̂_j)** | Feather column `pool_tb_ratio_mean_snr_fwd` — mean senior-rater pool talent, leave-one-out. |
| **Minus-mean peer context** | Feather column `pool_minus_mean_snr_fwd` — own talent minus pool mean. |
| **Z-scored minus-mean (HERO default for minus-mean runs)** | Feather column `z_pool_minus_mean_snr_fwd` |
| **Live feather file plots read** | `big_dfs/df_pipeline_11_cox_analysis.feather` |
| **Data story mosaic output** | `talent/re_entry/output/data_story/ARMY_DATA_STORY_run1_3x3.png` |

**Plot tag `_run1` in filenames:** All five runs write PNGs with suffix `_run1` in the filename. That is a **plot tag**, not “Run 1 only.” Each sensitivity run **overwrites** the top-level PNGs until you **backup** into a subfolder.

---

## Five runs — overview

| Run label | Pool grain | Zero–TB peers | Peer metric on plots | Re-run notebook? |
|-----------|------------|---------------|----------------------|------------------|
| **Run 1** | legacy | keep | straight leave-one-out pond level | **Yes** |
| **Run 2** | eval-thru | keep | straight leave-one-out pond level | **Yes** |
| **Run 3** | eval-thru | exclude from pool | straight leave-one-out pond level | **Yes** |
| **Run 4** (optional) | legacy (from archived feather) | keep | minus-mean | **No** — plots only |
| **Run 5** (optional) | eval-thru (from archived feather) | keep | minus-mean | **No** — plots only |

**Feather archives you must save after notebook runs:**

| Archive file | Create after |
|--------------|--------------|
| `big_dfs/df_pipeline_11_run1_legacy.feather` | Run 1 notebook |
| `big_dfs/df_pipeline_11_run2_thru.feather` | Run 2 notebook |
| `big_dfs/df_pipeline_11_run3_thru_nozero.feather` | Run 3 notebook |

Plot backup (`backup_rename_suffix.sh`) **does not** copy feathers. You must run the **`cp`** commands in each run’s save step.

---

## Shared reference — plot script lines

These files live under `talent/re_entry/` on AWS.

### Straight leave-one-out pond level (Runs 1, 2, 3)

| File | Line | Must read |
|------|------|-----------|
| `army_basic_plots.py` | 42 | `COL_LOO = "pool_tb_ratio_mean_snr_fwd"` |
| `army_hero_slide_plot.py` | 44 | `plot_var = "pool_tb_ratio_mean_snr_fwd"` |
| `army_act2_probes.py` | 55 | `COL_LOO_Z = "z_pool_tb_ratio_mean_snr_fwd"` *(column usually missing → Act II z-scores `COL_LOO` from basic plots)* |

**HERO command-line flag (Runs 1–3):**

```bash
python talent/re_entry/army_hero_slide_plot.py --plot-var pool_tb_ratio_mean_snr_fwd
```

**Manifest panel 9 path (Runs 1–3):**

```text
talent/re_entry/output/hero/ARMY_HERO_ew8_pool_tb_ratio_mean_snr_fwd_run1.png
```

**Do not** use `--plot-var pool_tb_ratio_mean_snr_fwd_run1.png` — that is a filename, not a column name.

**Do not** use `z_pool_tb_ratio_mean_snr_fwd` for Runs 1–3 unless you add that column via a separate Cell 10.5 config path.

### Minus-mean peer context (Runs 4, 5)

| File | Line | Must read |
|------|------|-----------|
| `army_basic_plots.py` | 42 | `COL_LOO = "pool_minus_mean_snr_fwd"` |
| `army_hero_slide_plot.py` | 44 | `plot_var = "z_pool_minus_mean_snr_fwd"` |
| `army_act2_probes.py` | 55 | `COL_LOO_Z = "z_pool_minus_mean_snr_fwd"` |

**HERO command-line flag (Runs 4, 5):**

```bash
python talent/re_entry/army_hero_slide_plot.py --plot-var z_pool_minus_mean_snr_fwd
```

**Manifest panel 9 path (Runs 4, 5):**

```text
talent/re_entry/output/hero/ARMY_HERO_ew8_z_pool_minus_mean_snr_fwd_run1.png
```

### Plot pipeline commands (every run that builds plots)

Run from `Network_1P_shell/`:

```bash
python talent/re_entry/army_basic_plots.py --all
python talent/re_entry/army_act2_probes.py --plot all_probes
python talent/re_entry/army_hero_slide_plot.py --plot-var <COLUMN_NAME>
python talent/re_entry/build_army_data_story.py
```

Use **`python`**, not **`bash`**, for `build_army_data_story.py`.

Success lines:

- `Wrote talent/re_entry/output/hero/ARMY_HERO_ew8_...`
- `Wrote talent/re_entry/output/data_story/ARMY_DATA_STORY_run1_3x3.png`

### Manifest file

Path: `talent/re_entry/manifests/army_run1_3x3_manifest.json`

Edit panel 9 `"path"` to match the HERO PNG filename **exactly** before running `build_army_data_story.py`.

Panels 2–8 paths in the manifest stay the same; scripts overwrite top-level PNGs.

### Notebook cell order (every run that re-runs the notebook)

Open `520_pipeline_cox_working.ipynb`. Run in order:

1. **Cell 0** — reloads `pipeline_config.py`
2. **Cell 5** — pool means (watch log for `POOL_GROUPING_MODE`)
3. **Cell 6** — or if Cell 6 fails, run in terminal:  
   `cp big_dfs/df_pipeline_05_pool_means.feather big_dfs/df_pipeline_06_pool_ranks.feather`
4. **Cell 7**
5. **Cell 8**
6. **Cell 9**
7. **Cell 10**
8. **Cell 10.5**
9. **Cell 11** — writes `big_dfs/df_pipeline_11_cox_analysis.feather`

### Feather column check (after Cell 11)

```bash
python3 -c "import pandas as pd; df=pd.read_feather('big_dfs/df_pipeline_11_cox_analysis.feather'); print('pool_tb_ratio_mean_snr_fwd', 'YES' if 'pool_tb_ratio_mean_snr_fwd' in df.columns else 'MISSING')"
```

For Runs 4 and 5 also check:

```bash
python3 -c "import pandas as pd; df=pd.read_feather('big_dfs/df_pipeline_11_cox_analysis.feather'); print('z_pool_minus_mean_snr_fwd', 'YES' if 'z_pool_minus_mean_snr_fwd' in df.columns else 'MISSING')"
```

---

# RUN 1 · Legacy pool grain · straight leave-one-out · keep zero–TB peers

**What this run isolates:** Baseline **legacy** pool definition with **pond-level** peer context on plots.

---

## Run 1 — Step 1 · Open terminal on AWS

```bash
cd /path/to/Network_1P_shell
conda activate TALNET39
date
ls -lh big_dfs/df_pipeline_11_cox_analysis.feather
```

The last line is optional; it shows whether an old feather exists before you rebuild.

---

## Run 1 — Step 2 · Edit `pipeline_config.py`

Open `pipeline_config.py` at 520 root. Set these lines **exactly**:

```python
POOL_GROUPING_MODE = 'legacy'
POOL_EXCLUDE_PEER_TB_ZERO = False
CELL5_POOL_MEANS = True
CELL6_POOL_RANKS = True
```

Save the file.

Also confirm these lines exist (needed by Cell 5; add if missing):

```python
POOL_ANCHOR_COL = 'eval_thru_dt_bwd'
POOL_EVAL_STRT_COL = 'eval_strt_dt_bwd'
POOL_EVAL_THRU_COL = 'eval_thru_dt_bwd'
```

---

## Run 1 — Step 3 · Edit plot scripts (straight leave-one-out)

**File:** `talent/re_entry/army_basic_plots.py` — **line 42:**

```python
COL_LOO = "pool_tb_ratio_mean_snr_fwd"
```

**File:** `talent/re_entry/army_hero_slide_plot.py` — **line 44:**

```python
plot_var = "pool_tb_ratio_mean_snr_fwd"
```

**File:** `talent/re_entry/army_act2_probes.py` — **line 55** (optional but recommended for consistent panels 7–8):

```python
COL_LOO_Z = "z_pool_tb_ratio_mean_snr_fwd"
```

Save all edited files.

---

## Run 1 — Step 4 · Run notebook cells

Open `520_pipeline_cox_working.ipynb`.

Run **Cell 0**, then **Cell 5**, **Cell 6** (or the `cp` fallback), **Cell 7**, **Cell 8**, **Cell 9**, **Cell 10**, **Cell 10.5**, **Cell 11**.

In the Cell 5 log, confirm:

```text
POOL_GROUPING_MODE='legacy'
```

---

## Run 1 — Step 5 · Check feather columns

```bash
python3 -c "import pandas as pd; df=pd.read_feather('big_dfs/df_pipeline_11_cox_analysis.feather'); print('pool_tb_ratio_mean_snr_fwd', 'YES' if 'pool_tb_ratio_mean_snr_fwd' in df.columns else 'MISSING')"
```

Expect: **`YES`**.

---

## Run 1 — Step 6 · Edit manifest panel 9

Open `talent/re_entry/manifests/army_run1_3x3_manifest.json`.

Set panel 9 `"path"` to:

```text
talent/re_entry/output/hero/ARMY_HERO_ew8_pool_tb_ratio_mean_snr_fwd_run1.png
```

Save the manifest.

---

## Run 1 — Step 7 · Run plot scripts and mosaic

```bash
python talent/re_entry/army_basic_plots.py --all
python talent/re_entry/army_act2_probes.py --plot all_probes
python talent/re_entry/army_hero_slide_plot.py --plot-var pool_tb_ratio_mean_snr_fwd
python talent/re_entry/build_army_data_story.py
```

---

## Run 1 — Step 8 · Verify Run 1

```bash
grep POOL_GROUPING_MODE pipeline_config.py
ls -l talent/re_entry/output/hero/ARMY_HERO_ew8_pool_tb_ratio_mean_snr_fwd_run1.png
ls -l talent/re_entry/output/data_story/ARMY_DATA_STORY_run1_3x3.png
```

In the basic plots log, find:

```text
Overlap pool grain: POOL_GROUPING_MODE='legacy'
```

Open panel 5 — note **H_sort**. Open panel 9 — note porch shape.

Compare mosaic to standalone PNGs at **top level** under `talent/re_entry/output/` (not backup subfolders).

---

## Run 1 — Step 9 · Archive feather and plots before Run 2

**Save feather (required for Run 4 later):**

```bash
cp big_dfs/df_pipeline_11_cox_analysis.feather big_dfs/df_pipeline_11_run1_legacy.feather
```

**Save plots:**

```bash
bash scripts/backup_rename_suffix.sh _run1_legacy --all-output
```

---

# RUN 2 · Eval-thru pool grain · straight leave-one-out · keep zero–TB peers

**What this run isolates:** Same plot peer metric as Run 1, but **eval-thru** pool grain — tests **assortativity / H_sort** effect of pool definition.

---

## Run 2 — Step 1 · Open terminal on AWS

```bash
cd /path/to/Network_1P_shell
conda activate TALNET39
date
```

---

## Run 2 — Step 2 · Edit `pipeline_config.py`

```python
POOL_GROUPING_MODE = 'active_at_eval_thru'
POOL_EXCLUDE_PEER_TB_ZERO = False
CELL5_POOL_MEANS = True
CELL6_POOL_RANKS = True
```

Save the file.

---

## Run 2 — Step 3 · Edit plot scripts (straight leave-one-out)

**File:** `talent/re_entry/army_basic_plots.py` — **line 42:**

```python
COL_LOO = "pool_tb_ratio_mean_snr_fwd"
```

**File:** `talent/re_entry/army_hero_slide_plot.py` — **line 44:**

```python
plot_var = "pool_tb_ratio_mean_snr_fwd"
```

**File:** `talent/re_entry/army_act2_probes.py` — **line 55:**

```python
COL_LOO_Z = "z_pool_tb_ratio_mean_snr_fwd"
```

Save all edited files.

---

## Run 2 — Step 4 · Run notebook cells

Open `520_pipeline_cox_working.ipynb`.

Run **Cell 0**, **Cell 5**, **Cell 6** (or `cp` fallback), **Cell 7**, **Cell 8**, **Cell 9**, **Cell 10**, **Cell 10.5**, **Cell 11**.

In the Cell 5 log, confirm:

```text
POOL_GROUPING_MODE='active_at_eval_thru'
```

---

## Run 2 — Step 5 · Check feather columns

```bash
python3 -c "import pandas as pd; df=pd.read_feather('big_dfs/df_pipeline_11_cox_analysis.feather'); print('pool_tb_ratio_mean_snr_fwd', 'YES' if 'pool_tb_ratio_mean_snr_fwd' in df.columns else 'MISSING')"
```

Expect: **`YES`**.

---

## Run 2 — Step 6 · Edit manifest panel 9

Open `talent/re_entry/manifests/army_run1_3x3_manifest.json`.

Set panel 9 `"path"` to:

```text
talent/re_entry/output/hero/ARMY_HERO_ew8_pool_tb_ratio_mean_snr_fwd_run1.png
```

Save the manifest.

---

## Run 2 — Step 7 · Run plot scripts and mosaic

```bash
python talent/re_entry/army_basic_plots.py --all
python talent/re_entry/army_act2_probes.py --plot all_probes
python talent/re_entry/army_hero_slide_plot.py --plot-var pool_tb_ratio_mean_snr_fwd
python talent/re_entry/build_army_data_story.py
```

---

## Run 2 — Step 8 · Verify Run 2

```bash
grep POOL_GROUPING_MODE pipeline_config.py
ls -l talent/re_entry/output/hero/ARMY_HERO_ew8_pool_tb_ratio_mean_snr_fwd_run1.png
ls -l talent/re_entry/output/data_story/ARMY_DATA_STORY_run1_3x3.png
```

In the basic plots log, find:

```text
Overlap pool grain: POOL_GROUPING_MODE='active_at_eval_thru'
```

Compare panel 5 **H_sort** and panel 9 porch to Run 1 backup in `talent/re_entry/output/*/run1_legacy/`.

---

## Run 2 — Step 9 · Archive feather and plots before Run 3

**Save feather (required for Run 5 later):**

```bash
cp big_dfs/df_pipeline_11_cox_analysis.feather big_dfs/df_pipeline_11_run2_thru.feather
```

**Save plots:**

```bash
bash scripts/backup_rename_suffix.sh _run2_thru --all-output
```

---

# RUN 3 · Eval-thru pool grain · straight leave-one-out · exclude zero–TB peers

**What this run isolates:** Same **eval-thru** grain as Run 2, but peers with **talent board ratio equal to zero** are dropped from pool mean and pool size.

---

## Run 3 — Step 1 · Open terminal on AWS

```bash
cd /path/to/Network_1P_shell
conda activate TALNET39
date
```

---

## Run 3 — Step 2 · Edit `pipeline_config.py`

```python
POOL_GROUPING_MODE = 'active_at_eval_thru'
POOL_EXCLUDE_PEER_TB_ZERO = True
CELL5_POOL_MEANS = True
CELL6_POOL_RANKS = True
```

Save the file.

---

## Run 3 — Step 3 · Edit plot scripts (straight leave-one-out)

**File:** `talent/re_entry/army_basic_plots.py` — **line 42:**

```python
COL_LOO = "pool_tb_ratio_mean_snr_fwd"
```

**File:** `talent/re_entry/army_hero_slide_plot.py` — **line 44:**

```python
plot_var = "pool_tb_ratio_mean_snr_fwd"
```

**File:** `talent/re_entry/army_act2_probes.py` — **line 55:**

```python
COL_LOO_Z = "z_pool_tb_ratio_mean_snr_fwd"
```

Save all edited files.

---

## Run 3 — Step 4 · Run notebook cells

Open `520_pipeline_cox_working.ipynb`.

Run **Cell 0**, **Cell 5**, **Cell 6** (or `cp` fallback), **Cell 7**, **Cell 8**, **Cell 9**, **Cell 10**, **Cell 10.5**, **Cell 11**.

In the Cell 5 log, confirm:

```text
POOL_GROUPING_MODE='active_at_eval_thru'
```

and, if printed:

```text
POOL_EXCLUDE_PEER_TB_ZERO=True
```

---

## Run 3 — Step 5 · Check feather columns

```bash
python3 -c "import pandas as pd; df=pd.read_feather('big_dfs/df_pipeline_11_cox_analysis.feather'); print('pool_tb_ratio_mean_snr_fwd', 'YES' if 'pool_tb_ratio_mean_snr_fwd' in df.columns else 'MISSING')"
```

Expect: **`YES`**.

Optional pool-size diagnostic:

```bash
python -u talent/re_entry/army_pool_size_probe.py
```

---

## Run 3 — Step 6 · Edit manifest panel 9

Open `talent/re_entry/manifests/army_run1_3x3_manifest.json`.

Set panel 9 `"path"` to:

```text
talent/re_entry/output/hero/ARMY_HERO_ew8_pool_tb_ratio_mean_snr_fwd_run1.png
```

Save the manifest.

---

## Run 3 — Step 7 · Run plot scripts and mosaic

```bash
python talent/re_entry/army_basic_plots.py --all
python talent/re_entry/army_act2_probes.py --plot all_probes
python talent/re_entry/army_hero_slide_plot.py --plot-var pool_tb_ratio_mean_snr_fwd
python talent/re_entry/build_army_data_story.py
```

---

## Run 3 — Step 8 · Verify Run 3

Panel 5 title should include **`exclude tb_ratio=0 peers`**.

Compare panel 5 **H_sort** and panel 9 porch to Run 2 backup in `talent/re_entry/output/*/run2_thru/`.

Panel 2 left histogram may still show a spike at own talent equal to zero — that is **own performance**, not the pool-exclusion toggle.

---

## Run 3 — Step 9 · Archive feather and plots

**Save feather:**

```bash
cp big_dfs/df_pipeline_11_cox_analysis.feather big_dfs/df_pipeline_11_run3_thru_nozero.feather
```

**Save plots:**

```bash
bash scripts/backup_rename_suffix.sh _run3_thru_nozero --all-output
```

---

# RUN 4 · Legacy pool grain · minus-mean plots · plot-only (no notebook)

**What this run isolates:** **Minus-mean** peer context on plots, using the **same feather as Run 1** (legacy grain). **Do not re-run the notebook** unless the Run 1 archive is missing.

---

## Run 4 — Step 1 · Open terminal on AWS

```bash
cd /path/to/Network_1P_shell
conda activate TALNET39
date
ls -lh big_dfs/df_pipeline_11_run1_legacy.feather
```

If the archive file **does not exist**, stop and complete **Run 1** through **Run 1 Step 9** first.

---

## Run 4 — Step 2 · Restore Run 1 feather into the live slot

Plot scripts always read **`big_dfs/df_pipeline_11_cox_analysis.feather`**. After Run 3, that file holds Run 3 data. Copy the Run 1 archive **back**:

```bash
cp big_dfs/df_pipeline_11_run1_legacy.feather big_dfs/df_pipeline_11_cox_analysis.feather
```

**Direction:** `run1_legacy` → `cox_analysis` (restore, not save).

---

## Run 4 — Step 3 · `pipeline_config.py`

**No edit required** for plot-only Run 4 — pool columns are already in the restored feather.

---

## Run 4 — Step 4 · Edit plot scripts (minus-mean)

**File:** `talent/re_entry/army_basic_plots.py` — **line 42:**

```python
COL_LOO = "pool_minus_mean_snr_fwd"
```

**File:** `talent/re_entry/army_hero_slide_plot.py` — **line 44:**

```python
plot_var = "z_pool_minus_mean_snr_fwd"
```

**File:** `talent/re_entry/army_act2_probes.py` — **line 55:**

```python
COL_LOO_Z = "z_pool_minus_mean_snr_fwd"
```

Save all edited files.

---

## Run 4 — Step 5 · Do not run the notebook

Skip Cells 0 through 11.

---

## Run 4 — Step 6 · Check feather columns

```bash
python3 -c "import pandas as pd; df=pd.read_feather('big_dfs/df_pipeline_11_cox_analysis.feather'); print('z_pool_minus_mean_snr_fwd', 'YES' if 'z_pool_minus_mean_snr_fwd' in df.columns else 'MISSING')"
```

Expect: **`YES`**. If **MISSING**, the Run 1 notebook did not reach **Cell 10.5** — re-run Run 1 notebook, then repeat Run 1 archive and restore steps.

---

## Run 4 — Step 7 · Edit manifest panel 9

Open `talent/re_entry/manifests/army_run1_3x3_manifest.json`.

Set panel 9 `"path"` to:

```text
talent/re_entry/output/hero/ARMY_HERO_ew8_z_pool_minus_mean_snr_fwd_run1.png
```

Save the manifest.

---

## Run 4 — Step 8 · Run plot scripts and mosaic

```bash
python talent/re_entry/army_basic_plots.py --all
python talent/re_entry/army_act2_probes.py --plot all_probes
python talent/re_entry/army_hero_slide_plot.py --plot-var z_pool_minus_mean_snr_fwd
python talent/re_entry/build_army_data_story.py
```

---

## Run 4 — Step 9 · Verify Run 4

Panel 5 **H_sort** should **match Run 1** (same legacy grain in feather — only panels 3, 7, 8, 9 peer axes change).

Panel 9 porch may differ from Run 1 straight leave-one-out HERO.

---

## Run 4 — Step 10 · Archive plots

```bash
bash scripts/backup_rename_suffix.sh _run4_legacy_minusmean --all-output
```

---

# RUN 5 · Eval-thru pool grain · minus-mean plots · plot-only (no notebook)

**What this run isolates:** **Minus-mean** peer context on plots, using the **same feather as Run 2** (eval-thru grain, keep zero–TB peers). **Do not re-run the notebook** unless the Run 2 archive is missing.

---

## Run 5 — Step 1 · Open terminal on AWS

```bash
cd /path/to/Network_1P_shell
conda activate TALNET39
date
ls -lh big_dfs/df_pipeline_11_run2_thru.feather
```

If the archive file **does not exist**:

1. Re-run **Run 2** notebook (Run 2 Steps 2–4), then  
2. Run **Run 2 Step 9** feather save:  
   `cp big_dfs/df_pipeline_11_cox_analysis.feather big_dfs/df_pipeline_11_run2_thru.feather`

---

## Run 5 — Step 2 · Restore Run 2 feather into the live slot

```bash
cp big_dfs/df_pipeline_11_run2_thru.feather big_dfs/df_pipeline_11_cox_analysis.feather
```

**Direction:** `run2_thru` → `cox_analysis` (restore, not save).

---

## Run 5 — Step 3 · `pipeline_config.py`

**No edit required** for plot-only Run 5 — pool columns are already in the restored feather.

For consistent panel 5 **labels** only (optional, does not change feather):

```python
POOL_GROUPING_MODE = 'active_at_eval_thru'
POOL_EXCLUDE_PEER_TB_ZERO = False
```

---

## Run 5 — Step 4 · Edit plot scripts (minus-mean)

**File:** `talent/re_entry/army_basic_plots.py` — **line 42:**

```python
COL_LOO = "pool_minus_mean_snr_fwd"
```

**File:** `talent/re_entry/army_hero_slide_plot.py` — **line 44:**

```python
plot_var = "z_pool_minus_mean_snr_fwd"
```

**File:** `talent/re_entry/army_act2_probes.py` — **line 55:**

```python
COL_LOO_Z = "z_pool_minus_mean_snr_fwd"
```

Save all edited files.

---

## Run 5 — Step 5 · Do not run the notebook

Skip Cells 0 through 11.

---

## Run 5 — Step 6 · Check feather columns

```bash
python3 -c "import pandas as pd; df=pd.read_feather('big_dfs/df_pipeline_11_cox_analysis.feather'); print('z_pool_minus_mean_snr_fwd', 'YES' if 'z_pool_minus_mean_snr_fwd' in df.columns else 'MISSING')"
```

Expect: **`YES`**.

---

## Run 5 — Step 7 · Edit manifest panel 9

Open `talent/re_entry/manifests/army_run1_3x3_manifest.json`.

Set panel 9 `"path"` to:

```text
talent/re_entry/output/hero/ARMY_HERO_ew8_z_pool_minus_mean_snr_fwd_run1.png
```

Save the manifest.

---

## Run 5 — Step 8 · Run plot scripts and mosaic

```bash
python talent/re_entry/army_basic_plots.py --all
python talent/re_entry/army_act2_probes.py --plot all_probes
python talent/re_entry/army_hero_slide_plot.py --plot-var z_pool_minus_mean_snr_fwd
python talent/re_entry/build_army_data_story.py
```

---

## Run 5 — Step 9 · Verify Run 5

Panel 5 **H_sort** should **match Run 2** (same eval-thru grain in feather).

Compare panel 9 to Run 4 — minus-mean at **eval-thru** grain vs minus-mean at **legacy** grain.

Compare panel 9 to Run 2 — minus-mean vs straight leave-one-out at **eval-thru** grain.

---

## Run 5 — Step 10 · Archive plots

```bash
bash scripts/backup_rename_suffix.sh _run5_thru_minusmean --all-output
```

---

# Results table — fill in for Alex

| Run | Pool grain | Exclude zero–TB peers? | Peer metric on plots | H_sort (panel 5) | HERO porch note (panel 9) |
|-----|------------|------------------------|----------------------|------------------|---------------------------|
| 1 legacy | `legacy` | no | straight leave-one-out | | |
| 2 eval-thru | `active_at_eval_thru` | no | straight leave-one-out | | |
| 3 eval-thru no-zero | `active_at_eval_thru` | yes | straight leave-one-out | | |
| 4 legacy minus-mean | `legacy` (archived feather) | no | minus-mean | | |
| 5 eval-thru minus-mean | `active_at_eval_thru` (archived feather) | no | minus-mean | | |

---

# Common mistakes

| Symptom | Cause | Fix |
|---------|-------|-----|
| HERO error: column not in feather `...run1.png` | Passed filename to `--plot-var` | Use column name only, e.g. `pool_tb_ratio_mean_snr_fwd` |
| HERO error: `z_pool_tb_ratio_mean_snr_fwd` missing | Wrong column for Runs 1–3 | Use `pool_tb_ratio_mean_snr_fwd` |
| Mosaic `FileNotFoundError` on panel 9 | Manifest path ≠ HERO output filename | Edit manifest `"path"` to match exactly |
| Mosaic panels do not match standalone PNGs | Viewing backup subfolder PNGs | Open top-level `talent/re_entry/output/...` only |
| Mosaic build ran but looks old | Ran `bash build_army_data_story.py` | Use `python talent/re_entry/build_army_data_story.py` |
| Run 4 wrong grain | Forgot feather restore | `cp run1_legacy.feather → cox_analysis.feather` |
| Run 5 wrong grain | Missing or wrong archive | Save Run 2 feather in Run 2 Step 9; restore in Run 5 Step 2 |
| Changed `pipeline_config.py` but feather unchanged | Did not re-run Cell 5–11 | Re-run notebook after config change |
| Panel 1 shows N=39,517 but panel 2 shows n≈15,977 | Different filters (cohort vs analysis sample) | Expected — not a compositor bug |
| Panel 2 zero spike after Run 3 exclude | Own talent zero, not peer exclusion | Expected — toggle drops **peers** with TB=0 only |

---

# Related documents

- Pool mode detail: `talent/re_entry/rating_window_mode_explanation.md`
- Straight leave-one-out mosaic notes: `talent/re_entry/STRAIGHT_LOO_MOSAIC_AWS_GUIDE.md`

---

*Updated 2026-09-24 — full cold-start rewrite, no cross-run shorthand.*
