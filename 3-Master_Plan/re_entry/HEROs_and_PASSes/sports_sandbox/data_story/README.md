# Data story mosaics (3×3)

Alex screening deck: descriptive BDP panels → CCT / F-HERO → HERO (bottom-right).

## MBB reigning hero

```bash
python sports/scripts/build_data_story_mosaic.py \
  --manifest 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/data_story/mbb_reigning_3x3_manifest.json
```

**Output:** `MBB_DATA_STORY_reigning_3x3.png`

**Panel map (read TL → BR):**

| | Who / cohort | Ability | Peer context |
|--|--------------|---------|--------------|
| **R1** | Cohort text | Â_i \| T̂_j | poolq_LOO dist |
| **R2** | Draft-mass ECDF | Interval overlap | Roster size |
| **R3** | CCT P1 (fixed Â · **LOO** ventiles) | **Elite pond** (top 7% Â · **LOO** pw4p7) | **HERO (Pass A pair)** |

**Panel 8 (Critical Keeper):** `ELITE_pond_loo_pw4p7_dft_min20_mg10_top7_ppm_11_21.png` — LOO twin; +DFT 11–21. Row 3 is **all LOO-axis** (panels 7–9).

**T̂_j keeper (parked):** `sports_sandbox/fhero/CCT_draft_rate_fixedAi_Tj_knbins_min20_ppm_top7_dft_low4_high7.png`

**09–21 last-ps ALLT LOO sibling:** `…/_DISPOSABLE_elite_pond_loo_twin/ELITE_pond_loo_pw4p7_allt_min20_mg10_top7_ppm_9_21_last_ps.png`

## Tenure PD29

**Built:** `../tenure_sandbox/data_story/TENURE_DATA_STORY_pd29_3x3.png`  
**Manifest:** `../tenure_sandbox/data_story/tenure_pd29_3x3_manifest.json`  
**Talk track:** `../tenure_sandbox/data_story/TENURE_DATA_STORY_plot_highlights.md`

Reigning hero = **PD29 decision cohort · dept pond LOO · cum pubs/career year · Q16** (Sep 2026). Panels 7–8 placeholder until `tenure_pass_a_congestion.py` (see highlights doc).
