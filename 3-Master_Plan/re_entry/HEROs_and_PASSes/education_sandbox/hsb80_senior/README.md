# HS&B:80 Senior sandbox

Working outputs for **HS&B:80 Senior** Big Fish / HERO screening (Alex Sep 2026).

| Item | Location |
|------|----------|
| Raw panel | [`datasets/hsb80/hsb80_big_fish_panel.csv`](../../../../datasets/hsb80/hsb80_big_fish_panel.csv) |
| Primer | [`../EDUCATION_dataset_primer.md`](../EDUCATION_dataset_primer.md) |
| Sophomore deck (separate) | [`../hsb80_soph/README.md`](../hsb80_soph/README.md) |

**Prefix:** `HSB80SEN_*`

**Alex rule:** Analyze **Sophomore and Senior separately** — do not pool cohorts.

## Regenerate 3×3 deck

```bash
python scripts/big_fish_data_story.py --domain hsb80_senior --mode all
```

**Output:** `data_story/HSB80SEN_DATA_STORY_3x3.png`

## Cohort

- Filter: `analytic_sample_min5 == 1` and `cohort == Senior` (~9.9k students)
- Pond: **school** (`school_id`)
- Y: `bachelors_or_higher_by_1986` (~**17%**)
- Peer LOO: `peer_mean_z_loo`

**Interpretation:** Attainment screen at **1980 Senior** snapshot; still not draft-like selection.
