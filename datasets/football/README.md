# Football Big Fish panel

| File | In Git? | Size |
|------|---------|------|
| `football_big_fish_player_season_panel.csv.zip` | Yes | ~28 MB |
| `football_big_fish_player_season_panel/football_big_fish_player_season_panel.csv` | **No** (gitignore) | ~178 MB |

**Local setup:** unzip the archive once; scripts read the CSV from this folder.

```bash
unzip -o football_big_fish_player_season_panel.csv.zip
```

GitHub rejects any single file over **100 MB** — the unzipped CSV must stay local / rsync only.
