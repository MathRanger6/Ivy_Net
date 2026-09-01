# Tenure HERO outputs (v0)

PNG, binned CSV, and provenance JSON from `tenure/scripts/tenure_pass_a_hero.py`.

| Artifact | Role |
|----------|------|
| `HERO_tenure_*_slide.png` | **MBB deck format** — single bar panel + LPM (matches sports HERO slides) |
| `HERO_tenure_*.png` | Stage 9 diagnostic — tenure + attrition, Wilson CI |
| `TENURE_HERO_slides_AUTO.pptx` | Intro + QTL v0 + last-ps cum LOO + own cum + **EW16/EW20** last-ps cum |

**Binning note:** Quantile (QTL) assigns ~equal **`n_all`** per bin; **`n_resolved`** still varies because censored (still-assistant) folks are uneven across LOO. Slide labels show `resolved/all` (e.g. `26/37`). EW has variable `n_all`; on-bar counts are resolved only (hue = density).

```bash
# v0 — spell-mean annual LOO
python tenure/scripts/tenure_pass_a_hero.py --output-tag q16_infHM_resolved_v0

# last-ps peer cumulative LOO (quantile)
python tenure/scripts/tenure_pass_a_hero.py --grain last_asst --pool-perf cumulative \
  --output-tag q16_lastps_loo_cum_infHM
python tenure/scripts/tenure_pass_a_hero.py --grain last_asst --pool-perf cumulative --n-bins 20 \
  --output-tag q20_lastps_loo_cum_infHM

# last-ps peer cumulative LOO (equal-width — hue + on-bar n)
python tenure/scripts/tenure_pass_a_hero.py --grain last_asst --pool-perf cumulative \
  --bin-method equal_width --output-tag ew16_lastps_loo_cum_infHM
python tenure/scripts/tenure_pass_a_hero.py --grain last_asst --pool-perf cumulative \
  --bin-method equal_width --n-bins 20 --output-tag ew20_lastps_loo_cum_infHM

# last-ps own cumulative pubs (ability)
python tenure/scripts/tenure_pass_a_hero.py --grain last_asst --x-metric own_cum \
  --output-tag q16_lastps_own_cum_infHM

python tenure/scripts/build_tenure_hero_slides.py
```

See [`../TENURE_HERO_Campaign_Plan.md`](../TENURE_HERO_Campaign_Plan.md) for spec.
