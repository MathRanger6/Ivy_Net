# Tenure HERO outputs (v0 + PD29 decision cohort)

PNG, binned CSV, and provenance JSON from `tenure/scripts/tenure_pass_a_hero.py` (v0) and `tenure_pass_a_decision_hero.py` (PD29).

| Artifact | Role |
|----------|------|
| `HERO_tenure_*_slide.png` | **MBB deck format** — single bar panel + LPM (matches sports HERO slides) |
| `HERO_tenure_*.png` | Stage 9 diagnostic — tenure + attrition, Wilson CI |
| `TENURE_HERO_slides_AUTO.pptx` | Intro + QTL v0 + LAST-PS cum LOO + own cum + EW16/EW20 + **PD29 decision cohort** |

Each `*_slide.png` has a **yellow badge** (top-right): **ASST-PS** vs **LAST-PS** vs **DECISION**. Deck subtitles repeat window + stat from provenance.

**Regenerate slides after plot styling changes:**
```bash
python tenure/scripts/build_tenure_hero_slides.py --regenerate-slides
```

**Binning note:** Quantile (QTL) assigns ~equal **`n_all`** per bin; **`n_resolved`** still varies because censored (still-assistant) folks are uneven across LOO. Slide labels show `resolved/all` (e.g. `26/37`). EW has variable `n_all`; on-bar counts are resolved only (hue = density).

```bash
# v0 — ASST-PS mean peer LOO (annum)
python tenure/scripts/tenure_pass_a_hero.py --output-tag q16_infHM_resolved_v0

# LAST-PS cum peer LOO (quantile)
python tenure/scripts/tenure_pass_a_hero.py --window last_ps --stat cum \
  --output-tag q16_lastps_loo_cum_infHM
python tenure/scripts/tenure_pass_a_hero.py --window last_ps --stat cum --n-bins 20 \
  --output-tag q20_lastps_loo_cum_infHM

# LAST-PS cum peer LOO (equal-width — hue + on-bar n)
python tenure/scripts/tenure_pass_a_hero.py --window last_ps --stat cum \
  --bin-method equal_width --output-tag ew16_lastps_loo_cum_infHM
python tenure/scripts/tenure_pass_a_hero.py --window last_ps --stat cum \
  --bin-method equal_width --n-bins 20 --output-tag ew20_lastps_loo_cum_infHM

# LAST-PS own cumulative pubs (ability)
python tenure/scripts/tenure_pass_a_hero.py --window last_ps --x-metric own_cum \
  --output-tag q16_lastps_own_cum_infHM

# PD29 — decision cohort (all resolved infHM, dept pond at decision year)
python tenure/scripts/tenure_pass_a_decision_hero.py
python tenure/scripts/tenure_pass_a_decision_hero.py --n-bins 8 --output-tag q8_decision_dept_loo_infHM
python tenure/scripts/tenure_pass_a_decision_hero.py --n-bins 10 --output-tag q10_decision_dept_loo_infHM
python tenure/scripts/tenure_pass_a_decision_hero.py --x-metric own_career \
  --output-tag q16_decision_own_career_infHM
python tenure/scripts/tenure_pass_a_decision_hero.py --x-metric own_career --n-bins 8 \
  --output-tag q8_decision_own_career_infHM
python tenure/scripts/tenure_pass_a_decision_hero.py --x-metric own_career --n-bins 10 \
  --output-tag q10_decision_own_career_infHM

python tenure/scripts/build_tenure_hero_slides.py
```

### PD29 decision HERO (2026-09-02)

| Tag | X axis | Bins | N (resolved) |
|-----|--------|------|--------------|
| `q16_decision_dept_loo_infHM` | Dept pond LOO | 16 | 389 |
| `q8_decision_dept_loo_infHM` | Dept pond LOO | 8 | 389 |
| `q10_decision_dept_loo_infHM` | Dept pond LOO | 10 | 389 |
| `q16_decision_own_career_infHM` | Own career rate | 16 | 280 |
| `q8_decision_own_career_infHM` | Own career rate | 8 | 280 |
| `q10_decision_own_career_infHM` | Own career rate | 10 | 280 |

See [`../TENURE_HERO_Campaign_Plan.md`](../TENURE_HERO_Campaign_Plan.md) for spec.
