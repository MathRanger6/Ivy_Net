# AWS upload checklist — Army BDP v0.3

Submit from **520 root** layout (`Network_1P_shell/` or equivalent). After upload, run from that same folder.

## Files to include

### `talent/re_entry/` (whole folder)

- `army_gallery_paths.py` — paths + auto import bootstrap
- `army_basic_plots.py` — panels 2–4, 5, 6
- `army_act2_probes.py` — panels 7–8 (CCT + elite pond)
- `army_hero_slide_plot.py` — panel 9 (CR-aligned defaults)
- `build_army_data_story.py` — mosaic wrapper
- `run_army_bdp_pipeline.sh` — one-shot runner
- `army_pool_size_probe.py` — pool-size + TB-zero sensitivity probe
- `manifests/army_run1_3x3_manifest.json`
- `README.md`, `AWS_UPLOAD_CHECKLIST.md` (this file)
- `output/*/.gitkeep` (empty dirs OK)

### `sports/scripts/` (minimum)

| File | Used by |
|------|---------|
| `build_data_story_mosaic.py` | mosaic (updated REPO fallback) |
| `story_page_layout.py` | mosaic |
| `hero_plot_style.py` | BDP + HERO |
| `empirical_team_interval_overlap.py` | Panel 5 overlap |
| `hero_gallery_paths.py` | Required import for overlap module |
| `interval_overlap_paths.py` | Required import for overlap module |
| `gallery_mathtext.py` | Panel 5 overlap + Act II mathtext |
| `plot_provenance.py` | Act II bin badges (Q8, PW 3+5) |

Optional (H_sort line in overlap title):

| `sports/541_grandchild_homophily_assign.py` | Realized sorting index |

## Also submit when pool-grain work is active

| File | Why |
|------|-----|
| `pipeline_config.py` | `POOL_GROUPING_MODE`, `POOL_EVAL_*`, `POOL_ANCHOR_COL`, `POOL_EXCLUDE_PEER_TB_ZERO`, eval dates in `base_time_varying_cols` |
| `add_cum_oer_metrics_mod_working.py` | Cell 5 anchor pools (`active_at_eval_thru`, **`active_at_snapshot`** snpsht_dt merge fix), peer TB-zero exclusion |
| `520_pipeline_cox_working.ipynb` | Cell 5: `pool_grouping_mode`, eval cols, `exclude_peer_tb_zero` + log lines (Mac canonical) |

## Do NOT re-submit unless changed

`big_dfs/*.feather` — regenerate on AWS after config/code updates.

## After upload — three commands (520 root)

```bash
bash talent/re_entry/run_army_bdp_pipeline.sh
```

Or:

```bash
./talent/re_entry/army_basic_plots.py --all
./talent/re_entry/army_hero_slide_plot.py
./talent/re_entry/build_army_data_story.py
```

Make scripts executable if needed: `chmod +x talent/re_entry/*.py talent/re_entry/*.sh`

## Success artifacts

- `talent/re_entry/output/data_story/ARMY_DATA_STORY_run1_3x3.png`
- `talent/re_entry/output/act2/ARMY_CCT_promotion_rate_pool_loo_run1_z1_2_q8.png`
- `talent/re_entry/output/act2/ARMY_ELITE_pond_loo_pw3p5_run1_top20.png`
- `talent/re_entry/output/hero/ARMY_HERO_ew8_z_pool_minus_mean_snr_fwd_run1.png`

## Mosaic — nothing else required

Compositor needs only the manifest JSON + panel PNG paths + `story_page_layout.py`. Panel PNGs must exist before running `build_army_data_story.py`.

## Panel 5 (overlap) — assortativity diagnostic

Uses **all snapshot rows** in the feather (not last-snapshot-only). Pool unit follows **`POOL_GROUPING_MODE`** in `pipeline_config.py` (same toggle as Cell 5). Performance axis = `z_tb_ratio_fwd_snr` when present.

**Cell 11 export columns** (in `base_time_varying_cols`, not Cox formula):

```python
'snr_rater_bwd',
'eval_strt_dt_bwd',
'eval_thru_dt_bwd',
```

For `active_at_eval_thru`, re-run **Cell 0 → Cell 11** after adding eval dates, then BDP. Confirm columns in `df_pipeline_11_cox_analysis.feather` before overlap.

Four subplots match MBB/tenure: coverage curve, span histogram, interval sample, full stack. High vertical coverage at a performance level ⇒ **assortative overlap** (many pools share that talent band).
