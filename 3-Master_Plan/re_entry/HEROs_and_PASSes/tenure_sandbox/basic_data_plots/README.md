# Tenure basic data plots (BDP)

**Population (v0):** HIGH/MEDIUM OpenAlex inference filter, LOO computable, excluding transferred.

**Decision cohort plots (`--mode pd29`):** All resolved (tenure + attrition, incl. OTT) at last assistant year; same inference filter; excluding transferred.

**Generate:**

```bash
python tenure/scripts/tenure_basic_plots.py              # v0 infHM (default)
python tenure/scripts/tenure_basic_plots.py --mode pd29    # decision cohort
python tenure/scripts/tenure_basic_plots.py --mode all     # both
python tenure/scripts/build_tenure_basic_plots_slides.py
```

**Deck:** `TENURE_BDP_slides_AUTO.pptx` — v0 slides + decision cohort section

Rebuild panel first if outcome flags changed:
```bash
python tenure/tenure_pipeline/rebuild_panel_stages.py
python tenure/tenure_pipeline/build_decision_year_cohort.py
```

### v0 (infHM)

| Plot | PNG | Role |
|------|-----|------|
| Pool interval overlap | `TENURE_pool_interval_overlap_infHM.png` | Uni×year peer windows on pubs |
| poolq_LOO | `TENURE_poolq_loo_distribution_infHM.png` | Person-level mean peer rank |
| Own pubs | `TENURE_pubs_year_distribution_infHM.png` | Publication rate distribution |
| Pool size | `TENURE_pool_size_loo_distribution_infHM.png` | LOO peer count |
| LOO by outcome | `TENURE_poolq_loo_by_outcome_infHM.png` | By tenure / attrition / censored |
| … | see `manifest.json` | Full v0 catalog |

### Decision cohort (pd29 — all resolved, no asst_time filter)

| Plot | PNG | Role |
|------|-----|------|
| Assistant time at exit | `TENURE_decision_asst_time_exit_pd29.png` | 391 resolved; band 5–6 shaded as reference only |
| Own career pubs rate | `TENURE_pubs_career_rate_pd29.png` | Alex Â — `pubs_per_career_year` at decision year |
| Own career by outcome | `TENURE_pubs_career_rate_by_outcome_pd29.png` | Tenured vs attrition (ability slice) |
| **Dept pond LOO** | `TENURE_dept_loo_career_rate_pd29.png` | HERO peer-context X (389/391) |
| Dept LOO by outcome | `TENURE_dept_loo_career_rate_by_outcome_pd29.png` | Marginal peer environment by outcome |
| Zero annual / + career | `TENURE_annual_zero_tenured_pd29.png` | Tenured with zero `pubs_year` but positive career rate |

Optional diagnostic slice: `--asst-time-min 5 --asst-time-max 6`

Each PNG has matching `*_meta.json`.
