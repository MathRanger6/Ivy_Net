# Army re_entry — BDP + 3×3 data story (AWS port)

**Purpose:** Uniform **9-panel porch deck** for Army talent data — same layout as MBB, tenure, football, and Legends.

**Status:** v0 scaffold (panels 2–4, 6, 9 implemented; overlap + Act II probes 7–8 TBD).

---

## Folder layout

```text
talent/re_entry/
  README.md                    ← this file
  army_gallery_paths.py        ← output paths (local + repo sync targets)
  army_basic_plots.py          ← BDP panel generator (Layer 1)
  army_hero_slide_plot.py      ← panel 9 HERO bar chart
  build_army_data_story.py     ← wrapper → shared mosaic compositor (Layer 3)
  run_army_bdp_pipeline.sh     ← run all steps (repo root or AWS)
  manifests/
    army_run1_3x3_manifest.json
  output/                      ← default PNG output (gitignored large files OK)
    basic_data_plots/
    hero/
    act2/                      ← panels 7–8 (future)
    data_story/
```

After AWS run, copy PNGs to canonical deck home (optional):

`3-Master_Plan/re_entry/HEROs_and_PASSes/army_sandbox/`

---

## Prerequisites (AWS)

1. **520 pipeline** through **Cell 11** (Run 1 / `pipeline_config_17_1` recommended).
2. Feather exists: `./running_vars/df_pipeline_11_cox_analysis.feather`  
   (run Jupyter with **cwd = `talent/talent_pipeline/`**).

---

## Upload bundle (copy to AWS PDE)

| From repo | To AWS (same relative path under project) |
|-----------|-------------------------------------------|
| `talent/re_entry/*` | `talent/re_entry/` |
| `sports/scripts/build_data_story_mosaic.py` | `sports/scripts/` |
| `sports/scripts/story_page_layout.py` | `sports/scripts/` |
| `sports/scripts/hero_plot_style.py` | `sports/scripts/` |
| `sports/scripts/gallery_mathtext.py` | `sports/scripts/` |

---

## Run (AWS — cwd = `talent/talent_pipeline/`)

```bash
# From repo root:
bash talent/re_entry/run_army_bdp_pipeline.sh

# Or step by step:
python ../re_entry/army_basic_plots.py --all
python ../re_entry/army_hero_slide_plot.py
python ../re_entry/build_army_data_story.py
```

Outputs:

- `talent/re_entry/output/basic_data_plots/ARMY_BDP_*.png`
- `talent/re_entry/output/hero/ARMY_HERO_*.png`
- `talent/re_entry/output/data_story/ARMY_DATA_STORY_run1_3x3.png`

---

## 9-panel standard (cross-domain)

| # | Panel | Army v0 |
|---|--------|---------|
| 1 | Cohort (text) | manifest JSON |
| 2 | Â_i and T̂_j | `ARMY_BDP_Ai_Tj_run1.png` |
| 3 | LOO pool distribution | `ARMY_BDP_pool_minus_mean_loo_run1.png` |
| 4 | Outcome mass vs Â (ECDF) | `ARMY_BDP_promotion_mass_ecdf_run1.png` |
| 5 | Pool interval overlap | **TBD** (stub skipped in v0) |
| 6 | Pool size \|T_j\| | `ARMY_BDP_pool_size_run1.png` |
| 7–8 | Act II probes | **TBD** → `output/act2/` |
| 9 | HERO | `ARMY_HERO_ew8_pool_minus_mean_run1.png` |

**Column map (Run 1 · forward SNR):**

| Role | Column |
|------|--------|
| Officer id | `pid_pde` |
| Â (own performance) | `tb_ratio_fwd_snr` or `z_tb_ratio_fwd_snr` |
| T̂_j (pool mean, incl. self) | `pool_tb_ratio_mean_snr_fwd` |
| LOO peer X | `pool_minus_mean_snr_fwd` |
| Pool size | `pool_size_snr_fwd` |
| Outcome | `event` (1=promoted, 2=attrited, 0=censored) |

Grain: **last snapshot per officer** (Cell 11 rule).

---

## Sibling decks (already in repo)

| Domain | Mosaic |
|--------|--------|
| MBB | `sports_sandbox/data_story/MBB_DATA_STORY_reigning_3x3.png` |
| Tenure | `tenure_sandbox/data_story/TENURE_DATA_STORY_pd29_3x3.png` |
| Football | `football_sandbox/data_story/FOOTBALL_DATA_STORY_3x3.png` |
| Legends | `legends_sandbox/data_story/LEGENDS_DATA_STORY_3x3.png` |

Compositor: `sports/scripts/build_data_story_mosaic.py` (shared).

---

*Created 2026-09-17 — Army BDP AWS port.*
