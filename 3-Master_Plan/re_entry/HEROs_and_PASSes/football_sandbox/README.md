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

**Position filter (football only):** trailing args or `--positions`. LOO recomputed among teammates in those groups. Outputs land in `football_sandbox/pos_<GROUPS>/` (does not overwrite the full cohort deck).

```bash
python scripts/big_fish_data_story.py --domain football --mode hero QB RB_FB
python scripts/big_fish_data_story.py --domain football --positions WR_TE DB --mode perf-story
```

Valid `position_group` values: `DB`, `WR_TE`, `DL_EDGE`, `LB`, `RB_FB`, `QB`, `K`, `P` (aliases: `WR`→`WR_TE`, `RB`→`RB_FB`, etc.).

**Team mean T̂_j on panels 7–9** (instead of teammate LOO — useful when position-filtered LOO is too sparse):

```bash
python scripts/big_fish_data_story.py --domain football --mode all DB --team-mean
python scripts/big_fish_data_story.py --domain football --mode hero DB --team-mean
```

→ `football_sandbox/pos_DB/peer_tj/` (separate from LOO outputs in `pos_DB/`).

Panel **5** (team interval overlap) prints **H_sort** on the suptitle and in `FOOTBALL_team_interval_overlap_meta.json` (same recipe as MBB/tenure; needs `sports/541_grandchild_homophily_assign.py`).

## Folder layout

```
football_sandbox/
  README.md
  basic_data_plots/     ← FOOTBALL_BDP_*.png
  hero/                 ← HERO porch (Q16 LOO bins)
  act2/                 ← CCT z∈[1,2] · elite top 20%
  data_story/           ← 3×3 mosaic + manifest
```
