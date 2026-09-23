# NELS:88 education sandbox

Working outputs for **NELS:88** Big Fish / HERO screening (Alex Sep 2026).

| Item | Location |
|------|----------|
| Raw panel | [`datasets/nels88/nels88_big_fish_panel.csv`](../../../../datasets/nels88/nels88_big_fish_panel.csv) |
| Primer | [`../EDUCATION_dataset_primer.md`](../EDUCATION_dataset_primer.md) |
| All Big Fish datasets | [`../_DISPOSABLE_big_fish_datasets_assessment.md`](../_DISPOSABLE_big_fish_datasets_assessment.md) |

**Prefix:** `NELS88_*` (parallel to `FOOTBALL_*`, `LEGENDS_*`).

## Regenerate 3×3 deck

From repo root:

```bash
python scripts/big_fish_data_story.py --domain nels88 --mode all
```

**Output:** `data_story/NELS88_DATA_STORY_3x3.png`

**Panel 5** writes **H_sort** on school-interval overlap → `basic_data_plots/NELS88_team_interval_overlap_meta.json`

## Cohort

- Filter: `analytic_sample_min10 == 1` (~7.2k students)
- Pond: **school** (`school_id`)
- Â: `own_performance_z` (baseline test composite)
- Peer LOO: `peer_mean_z_loo` (Alex precomputed on sampled classmates)
- Y: `bachelors_or_higher_by_2000` (~36%)

**Interpretation:** Attainment screen — sorting + peer context, **not** scarce top-K selection (see primer).

## Folder layout

```
education_sandbox/nels88/
  README.md
  basic_data_plots/     ← NELS88_* BDP PNGs + overlap meta
  hero/                 ← HERO Q16 LOO porch
  act2/                 ← CCT + elite probes
  data_story/           ← 3×3 mosaic + manifest
```

## Modes

```bash
python scripts/big_fish_data_story.py --domain nels88 --mode bdp    # panels 2–6
python scripts/big_fish_data_story.py --domain nels88 --mode hero   # panel 9
python scripts/big_fish_data_story.py --domain nels88 --mode mosaic # rebuild PNG from manifest
```
