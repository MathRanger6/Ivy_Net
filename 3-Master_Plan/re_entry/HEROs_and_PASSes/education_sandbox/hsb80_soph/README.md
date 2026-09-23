# HS&B:80 Sophomore sandbox

Working outputs for **HS&B:80 Sophomore** Big Fish / HERO screening (Alex Sep 2026).

| Item | Location |
|------|----------|
| Raw panel | [`datasets/hsb80/hsb80_big_fish_panel.csv`](../../../../datasets/hsb80/hsb80_big_fish_panel.csv) |
| Primer | [`../EDUCATION_dataset_primer.md`](../EDUCATION_dataset_primer.md) |
| Senior deck (separate) | [`../hsb80_senior/README.md`](../hsb80_senior/README.md) |

**Prefix:** `HSB80SOPH_*`

**Alex rule:** Analyze **Sophomore and Senior separately** — do not pool cohorts.

## Regenerate 3×3 deck

```bash
python scripts/big_fish_data_story.py --domain hsb80_soph --mode all
```

**Output:** `data_story/HSB80SOPH_DATA_STORY_3x3.png`

## Cohort

- Filter: `analytic_sample_min5 == 1` and `cohort == Sophomore` (~12.2k students)
- Pond: **school** (`school_id`)
- Y: `bachelors_or_higher_by_1986` (~**7%** — early follow-up for BA)
- Peer LOO: `peer_mean_z_loo`

**Interpretation:** Attainment screen at **1980 Sophomore** snapshot; low BA rate partly reflects young 1986 follow-up.
