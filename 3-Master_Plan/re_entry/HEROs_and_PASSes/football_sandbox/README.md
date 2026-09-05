# Football sandbox (FBS / NFL draft)

Working outputs for **college football** Big Fish / HERO analysis.

| Item | Location |
|------|----------|
| Raw panel | [`datasets/football/football_big_fish_player_season_panel/football_big_fish_player_season_panel.csv`](../../../datasets/football/football_big_fish_player_season_panel/football_big_fish_player_season_panel.csv) |
| Column map | [`datasets/football/README.md`](../../../datasets/football/README.md) |
| All Big Fish datasets | [`../_DISPOSABLE_big_fish_datasets_assessment.md`](../_DISPOSABLE_big_fish_datasets_assessment.md) |

**Status (2026-09-04):** 3×3 data story deck built (eligible cohort, N ≈ 70,633, draft rate ≈ 2.7%).

**Prefix:** `FOOTBALL_*` / `football_*` (parallel to `LEGENDS_*`, `MBB_*`, `TENURE_*`).

## Regenerate deck

```bash
python scripts/big_fish_data_story.py --domain football --mode all
```

**Output:** `data_story/FOOTBALL_DATA_STORY_3x3.png`  
**Talk track:** `data_story/FOOTBALL_DATA_STORY_plot_highlights.md`

**Perf metric story (6 rows · Q16 + EW16):**

```bash
python scripts/big_fish_data_story.py --domain football --mode perf-story
```

→ `data_story/FOOTBALL_PERF_METRIC_STORY.png` (Alex vol/eff + DIY recruit/PPA/usage z + composite)

## Folder layout

```
football_sandbox/
  README.md
  basic_data_plots/     ← FOOTBALL_BDP_*.png
  hero/                 ← HERO porch (Q16 LOO bins)
  act2/                 ← CCT z∈[1,2] · elite top 20%
  data_story/           ← 3×3 mosaic + manifest
```
