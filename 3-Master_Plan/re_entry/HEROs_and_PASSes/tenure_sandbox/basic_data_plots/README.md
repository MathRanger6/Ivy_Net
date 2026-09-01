# Tenure basic data plots — inference porch (infHM)

**Population:** Same as Q16/Q20 HERO — HIGH/MEDIUM OpenAlex, assistant rows, LOO computable (796 persons · 2,396 asst-years).

**Generate:**

```bash
python tenure/scripts/tenure_basic_plots.py
python tenure/scripts/build_tenure_basic_plots_slides.py
```

**Deck:** `TENURE_BDP_slides_AUTO.pptx` (title + 4 plot slides)

| Plot | PNG | Role |
|------|-----|------|
| Pool interval overlap | `TENURE_pool_interval_overlap_infHM.png` | MBB PD17 analog — uni×year peer windows on pubs z |
| poolq_LOO | `TENURE_poolq_loo_distribution_infHM.png` | HERO x-axis grain (person-level mean) |
| Own pubs | `TENURE_pubs_year_distribution_infHM.png` | Individual output vs peer context |
| Pool size | `TENURE_pool_size_loo_distribution_infHM.png` | LOO peer count distribution |

Each PNG has matching `*_meta.json`. Overlap also writes `*_uni_year.csv`.
