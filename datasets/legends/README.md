# League of Legends — esports panel (PD29)

**Source:** Alex Gates · Paper Directions 29 (Sep 2, 2026) · Oracle’s Elixir–derived  
**Notes:** [`transcripts/PD29_notes.md`](../../transcripts/PD29_notes.md)

## Files

| File | Size | Role |
|------|------|------|
| `lol_big_fish_player_split_panel.csv` | ~69 MB | **Working copy** (unzipped locally; **not in Git** — see gitignore) |
| `lol_big_fish_player_split_panel.csv.zip` | ~21 MB | **Tracked in Git** — unzip after clone/pull |

**Grain:** one row = **player × team × league × year × split × position** stint (`player_period_id`).  
**N:** 66,752 rows · **84 columns** · years **2015–2026**.

## Panel snapshot

| Field | Count / note |
|-------|----------------|
| `league_tier` | developmental 33,986 · top 19,624 · other 13,142 |
| `top_tier_debut_within_1y` | True 3,052 · False 63,700 |
| `top_tier_debut_within_2y` | True 4,456 · False 62,296 |
| `eligible_developmental_cohort` | True 15,983 |
| Positions | top / jng / mid / bot / sup (~13k each) |

## HERO / pond frame (COMPASS v0 read)

| Our term | Legends column(s) | Note |
|----------|-------------------|------|
| **Unit** | `player_period_id` | Player stint on a dev (or other) team in a split |
| **Pond** | `teamid`, `teamname`, `team_roster_players` | Team roster context; Alex noted **more swapping** than MBB |
| **Own Â** | `own_performance_index` or z-rate cols (`z_damage_per_min`, …) | 79.6% populated when components exist |
| **Peer context (LOO analog)** | `teammate_mean_performance_excl_self` | 91.7% populated — primary pond LOO candidate |
| **Same-role peer** | `same_role_mean_performance_excl_self` | 26.6% — sparse; role-specific slice |
| **Y (advancement)** | `top_tier_debut_within_1y` / `_2y` | Dev → **top-tier** league promotion window |
| **Censor / follow-up** | `full_1y_followup`, `full_2y_followup` | Use before treating False Y as failure |
| **Tier filter** | `league_tier`, `eligible_developmental_cohort` | Restrict HERO to **developmental** rows first |

**Not yet wired:** scripts, `legends_sandbox/`, LOO recompute on raw match rows — this README is ingest + map only.

---

## Column map (84)

### Keys & stint metadata

| Column | % fill | Meaning |
|--------|--------|---------|
| `player_period_id` | 100 | Unique stint key |
| `playerid`, `playername` | 100 | Oracle’s Elixir player |
| `teamid`, `teamname` | 100 | Team (pond) |
| `league` | 100 | League code (LPL, LCK, LDL, …) |
| `league_tier` | 100 | `developmental` \| `top` \| `other` |
| `year`, `split` | 100 | Season timing (split names vary by league) |
| `position` | 100 | top / jng / mid / bot / sup |
| `period_start`, `period_end` | 100 | Stint date bounds |
| `games`, `minutes`, `wins`, `win_rate` | 100 | Volume in stint |

### Performance index & pond context (HERO-facing)

| Column | % fill | Meaning |
|--------|--------|---------|
| `own_performance_index` | 79.6 | Alex composite own-performance index |
| `teammate_mean_performance_excl_self` | 91.7 | Mean teammate index excl. self (**pond LOO candidate**) |
| `same_role_mean_performance_excl_self` | 26.6 | Same-role teammates excl. self |
| `relative_performance_vs_team` | 79.6 | Own minus team mean |
| `relative_performance_vs_same_role` | 15.8 | Own minus same-role mean |
| `team_roster_players` | 100 | Roster size in pond |
| `same_role_player_count` | 100 | Same-role count |
| `same_role_total_player_games` | 100 | Same-role game count |
| `role_starter_share` | 100 | Starter share in role |
| `performance_components_available` | 100 | Flag: index/z cols valid when True |

### Promotion / top-tier outcome

| Column | % fill | Meaning |
|--------|--------|---------|
| `eligible_developmental_cohort` | 100 | In dev-to-pro analysis cohort |
| `prior_top_tier_before_period` | 100 | Already top-tier before stint |
| `first_top_tier_date` | 56.9 | Debut date (if ever) |
| `first_top_tier_league`, `first_top_tier_teamid`, `first_top_tier_teamname` | 56.9 | Where they debuted top-tier |
| `days_to_top_tier_from_period_end` | 56.9 | Days from stint end to top debut |
| `top_tier_debut_within_1y` | 100 | **Y₁** — promoted within 1 year |
| `top_tier_debut_within_2y` | 100 | **Y₂** — promoted within 2 years |
| `top_tier_debut_during_period_or_2y` | 100 | Debut during stint or +2y window |
| `full_1y_followup`, `full_2y_followup` | 100 | Follow-up window complete (censor check) |

### Raw box stats (Oracle’s Elixir aggregates for stint)

| Column | % fill | Meaning |
|--------|--------|---------|
| `kills`, `deaths`, `assists` | 100 | Counts |
| `damagetochampions`, `totalgold`, `earnedgold`, `goldspent`, `total_cs` | ~100 | Totals |
| `damageshare`, `earnedgoldshare`, `kill_participation` | ~100 | Shares |
| `wardsplaced`, `wardskilled`, `controlwardsbought`, `visionscore` | ~97–100 | Vision |
| `golddiffat10/15`, `xpdiffat10/15`, `csdiffat10/15` | 92.2 | Lane diffs @10/@15 |
| `*_per_30`, `damage_per_min`, `earned_gold_per_min`, `cs_per_min`, `vision_score_per_min`, `wards_*_per_min` | ~97–100 | Rate stats |

### Z-scored rates (within-period norm)

| Column | % fill | Meaning |
|--------|--------|---------|
| `z_damage_per_min`, `z_earned_gold_per_min`, `z_kda_ratio`, `z_kill_participation` | ~80 | Normalized own rates |
| `z_vision_score_per_min` | 71.3 | Vision z |
| `z_gold_diff_15`, `z_xp_diff_15`, `z_cs_diff_15` | ~73.4 | Lane-diff z @15 |

### Provenance

| Column | % fill | Meaning |
|--------|--------|---------|
| `playoff_games`, `complete_games` | 100 | Game completeness |
| `source_url` | 54.1 | Match history link (when present) |
| `source_file_year` | 100 | Source season file |
| `data_cutoff_date` | 100 | `2026-09-01` |
| `source_dataset_url` | 100 | Oracle’s Elixir downloads |
| `league_tier_mapping_version` | 100 | `manual_v1_2026-09-02` |

---

## Repo layout (naming)

| Item | Path |
|------|------|
| Raw data | `datasets/legends/` (this folder) |
| Scripts (future) | `legends/scripts/` |
| Sandbox | [`3-Master_Plan/re_entry/HEROs_and_PASSes/legends_sandbox/`](../3-Master_Plan/re_entry/HEROs_and_PASSes/legends_sandbox/) — active thread: `_DISPOSABLE_legends_hero_thread.md` |
| All Big Fish datasets | [`_DISPOSABLE_big_fish_datasets_assessment.md`](../3-Master_Plan/re_entry/HEROs_and_PASSes/_DISPOSABLE_big_fish_datasets_assessment.md) |

Prefix code outputs **`legends_*`** / **`LEGENDS_*`** — parallel to `tenure/`, `sports/`, `talent/`.

## Quick load (Python)

```python
import pandas as pd
from pathlib import Path

path = Path("datasets/legends/lol_big_fish_player_split_panel.csv")
df = pd.read_csv(path, low_memory=False)  # NUL-safe in pandas
dev = df[df["league_tier"] == "developmental"]
```

After `git pull`, if the CSV is missing: `./scripts/pull_big_data.sh` (unzip from tracked `.zip`).
