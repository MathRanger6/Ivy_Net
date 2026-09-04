# Football Big Fish panel

| File | In Git? | Size |
|------|---------|------|
| `football_big_fish_player_season_panel.csv.zip` | Yes | ~28 MB |
| `football_big_fish_player_season_panel/football_big_fish_player_season_panel.csv` | **No** (gitignore) | ~178 MB |

**Local setup (Mac, after git pull):**

```bash
./scripts/pull_big_data.sh          # unzip zips → working CSV paths
# or from HPC if panels live on Rivanna:
# ./scripts/pull_big_data.sh from-hpc big-fish
```

Manual unzip (equivalent):

```bash
unzip -o football_big_fish_player_season_panel.csv.zip -d .
mv football_big_fish_player_season_panel.csv football_big_fish_player_season_panel/
```

GitHub rejects any single file over **100 MB** — the unzipped CSV must stay local / rsync only.
