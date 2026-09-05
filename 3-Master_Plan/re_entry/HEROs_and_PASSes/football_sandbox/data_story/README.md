# Football data story mosaic (3×3)

Alex screening deck: descriptive BDP panels → scaled Act II (exploratory) → HERO porch (bottom-right).

```bash
python scripts/big_fish_data_story.py --domain football --mode all
```

**Output:** `FOOTBALL_DATA_STORY_3x3.png`  
**Manifest:** `football_3x3_manifest.json`  
**Talk track:** `FOOTBALL_DATA_STORY_plot_highlights.md`

**Panel map (read TL → BR):**

| | Who / cohort | Ability | Peer context |
|--|--------------|---------|--------------|
| **R1** | Cohort text | Â_i \| T̂_j | Team LOO dist |
| **R2** | Draft-mass ECDF | Interval overlap | Roster size |
| **R3** | CCT (z ∈ [1,2] · Q8 LOO) | Elite pond (top 20% · PW5) | HERO (Q16 LOO) |

**Cohort:** FBS eligible analysis · N = 70,633 · draft rate ≈ 2.7% (sparse Y — read Act II cautiously).
