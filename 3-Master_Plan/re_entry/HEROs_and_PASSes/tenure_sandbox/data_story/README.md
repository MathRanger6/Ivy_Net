# Tenure data story mosaics (3×3)

Alex screening deck: PD29 decision cohort BDP → CCT / elite pond (TBD) → HERO (bottom-right).

## PD29 deck (current)

```bash
python sports/scripts/build_data_story_mosaic.py \
  --manifest 3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/data_story/tenure_pd29_3x3_manifest.json
```

**Output:** `TENURE_DATA_STORY_pd29_3x3.png`  
**Talk track:** `TENURE_DATA_STORY_plot_highlights.md`

**Reigning lock:** Q16 · decision cohort · dept pond LOO · cum pubs/career year · `HERO_tenure_q16_decision_dept_loo_infHM_slide.png`

### Panel map (read TL → BR)

| | Who / cohort | Ability | Peer context |
|--|--------------|---------|--------------|
| **R1** | Cohort text | Â_i \| T̂_j | dept LOO hist \| ECDF |
| **R2** | Tenure-mass ECDF | Dept interval overlap | Dept roster \|T_j\| |
| **R3** | CCT z∈[1,2] Q8 | Elite top 20% PW3+5 | **HERO** (dept LOO Q16) |

Panels 7–8: `tenure_sandbox/act2/` · script `tenure/scripts/tenure_pass_a_congestion.py`

### Regen BDP + mosaic

```bash
python tenure/scripts/tenure_basic_plots.py --mode pd29
python tenure/scripts/tenure_pass_a_decision_hero.py
python tenure/scripts/tenure_pass_a_congestion.py --plot all_probes
python sports/scripts/build_data_story_mosaic.py \
  --manifest 3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/data_story/tenure_pd29_3x3_manifest.json
```

MBB sibling deck: `../sports_sandbox/data_story/MBB_DATA_STORY_reigning_3x3.png`
