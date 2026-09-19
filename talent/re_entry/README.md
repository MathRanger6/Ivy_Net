# Army re_entry — BDP + 3×3 data story (AWS port)

**Purpose:** Uniform **9-panel porch deck** for Army talent data — same layout as MBB, tenure, football, and Legends.

**Status:** v0.3 — panels 2–9 live (Act II CCT + elite pond scaled from tenure/MBB).

---

## AWS folder layout (520 root = e.g. `Network_1P_shell`)

```text
Network_1P_shell/                 ← Jupyter cwd (520 notebook here)
├── 520_pipeline_cox_working.ipynb
├── pipeline_config.py
├── big_dfs/
│   └── df_pipeline_11_cox_analysis.feather   ← Cell 11 input
├── talent/
│   └── re_entry/                   ← this folder
└── sports/
    └── scripts/                    ← compositor (2 files required)
        ├── build_data_story_mosaic.py
        └── story_page_layout.py
```

**No `PYTHONPATH` needed** — scripts bootstrap paths automatically when run from 520 root.

---

## Submit / upload bundle

| Path | Required |
|------|----------|
| `talent/re_entry/*` (all `.py`, `.sh`, `manifests/`, `output/.gitkeep`) | Yes |
| `sports/scripts/build_data_story_mosaic.py` | Yes |
| `sports/scripts/story_page_layout.py` | Yes |
| `sports/scripts/hero_plot_style.py` | Yes (BDP + HERO panels) |
| `sports/scripts/empirical_team_interval_overlap.py` | Yes (panel 5 overlap) |
| `sports/scripts/gallery_mathtext.py` | Yes (panel 5 mathtext) |
| `sports/scripts/plot_provenance.py` | Yes (Act II bin badges) |
| `sports/541_grandchild_homophily_assign.py` | Optional (H_sort in overlap title) |

**Mosaic compositor** only imports `story_page_layout.py` — not `hero_plot_style`.

---

## Run (from 520 root)

**One shot:**

```bash
bash talent/re_entry/run_army_bdp_pipeline.sh
```

**Or step by step:**

```bash
./talent/re_entry/army_basic_plots.py --all
./talent/re_entry/army_act2_probes.py --plot all_probes
./talent/re_entry/army_hero_slide_plot.py
./talent/re_entry/build_army_data_story.py
```

**Outputs:**

- `talent/re_entry/output/basic_data_plots/ARMY_BDP_*.png`
- `talent/re_entry/output/act2/ARMY_CCT_*.png` · `ARMY_ELITE_*.png`
- `talent/re_entry/output/hero/ARMY_HERO_ew10_z_pool_minus_mean_snr_fwd_run1.png`
- `talent/re_entry/output/data_story/ARMY_DATA_STORY_run1_3x3.png`

---

## Prerequisites

1. **520** through **Cell 11** (`pipeline_config_17_1` or your Run 1 config).
2. Feather at **`./big_dfs/df_pipeline_11_cox_analysis.feather`** (via `load_feather` / `store_feather`).
3. **Panel 5:** `pipeline_config.py` must include **`snr_rater_bwd`** in `base_time_varying_cols` so Cell 11 exports the senior-rater pool key (see `AWS_UPLOAD_CHECKLIST.md`).

---

## HERO defaults (Cell 11 CR CIF-bar aligned)

Edit one line in `army_hero_slide_plot.py`:

```python
plot_var = "z_pool_minus_mean_snr_fwd"
```

Defaults: **EW10**, min pool **3**, zero-OER + NaN filters, **last-event** promotion coding.

Porch-deck mode: `./talent/re_entry/army_hero_slide_plot.py --outcome ever_promoted --n-bins 12`

---

## 9-panel standard

| # | Panel | Army v0 |
|---|--------|---------|
| 1 | Cohort (text) | auto-refresh from BDP manifest |
| 2 | Â_i and T̂_j | `ARMY_BDP_Ai_Tj_run1.png` |
| 3 | LOO pool distribution | `ARMY_BDP_pool_minus_mean_loo_run1.png` |
| 4 | Promotion mass vs Â | `ARMY_BDP_promotion_mass_ecdf_run1.png` |
| 5 | Pool interval overlap | `ARMY_BDP_pool_interval_overlap_run1.png` |
| 6 | Pool size \|T_j\| | `ARMY_BDP_pool_size_run1.png` |
| 7 | CCT (fixed Â z∈[1,2], Q8 LOO) | `ARMY_CCT_promotion_rate_pool_loo_run1_z1_2_q8.png` |
| 8 | Elite pond (top 20% Â, PW 3+5 LOO) | `ARMY_ELITE_pond_loo_pw3p5_run1_top20.png` |
| 9 | HERO | `ARMY_HERO_ew10_z_pool_minus_mean_snr_fwd_run1.png` |

Compositor: `sports/scripts/build_data_story_mosaic.py` (shared with MBB/tenure).

---

*Updated 2026-09-18 — path bootstrap, big_dfs, CR-aligned HERO.*
