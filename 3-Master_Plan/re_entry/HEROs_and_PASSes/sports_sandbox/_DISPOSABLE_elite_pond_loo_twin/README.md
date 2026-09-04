# Elite pond LOO twin (disposable probe)

**Question:** Same as Critical Keeper panel 8, but bin **poolq_LOO** (not T̂_j) within **top 7% Â**.

```bash
# Reigning-aligned (09–21 · last-ps · ALLT)
python sports/scripts/pass_a_congestion_conditional.py --plot fixed_ai_loo_knbins \
  --ai-top-pct 7 --panel-rows last-ps --season-min 2009 --season-max 2021 \
  --tj-n-low 4 --tj-n-high 7 --out-dir 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/_DISPOSABLE_elite_pond_loo_twin

# +DFT 11–21 (apples-to-apples with T̂_j keeper window/pop)
python sports/scripts/pass_a_congestion_conditional.py --plot fixed_ai_loo_knbins \
  --ai-top-pct 7 --dft --season-min 2011 --season-max 2021 \
  --tj-n-low 4 --tj-n-high 7 --out-dir 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/_DISPOSABLE_elite_pond_loo_twin
```

| Run | N band | Downturn | Read |
|-----|--------|----------|------|
| 09–21 last-ps ALLT | 1,596 | YES (last bin 9.7%, n=31) | Rising LOO tail then **elite LOO dip** in bin 11 |
| 11–21 +DFT all-ps | 1,237 | YES (plateau 25.4% → tail 14.1%) | **Stronger** tail drop than T̂_j keeper on same pop/window |

Plot family label: **Elite pond (LOO)** — not CCT P1 (quantile ventiles) or F-HERO (T̂_j).

**In use:** panel 8 of `sports_sandbox/data_story/MBB_DATA_STORY_reigning_3x3.png` (+DFT 11–21 file).
