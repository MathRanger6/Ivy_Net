λ sweep CSV archive (Aug 2026)
===============================

Superseded per-arm CSVs from sort_chop_lambda_diagnostic.py runs:
  - 16-quantile (default gallery bins)
  - N=600 / K=60 scale probe
  - N=5600 / K=100 (K/N ≈ 1.8% selectivity)
  - legacy 5-arm labels (lambda_025, lambda_055, lambda_075)
  - filenames without _N*_K* suffix

Canonical set kept in parent folder:
  PASS_C_sort_chop_lambda_*_100quantile_poolmean_N5600_K560.csv
  (matches PASS_C_sort_chop_lambda_sweep.png @ 100 bins, K/N=10%)

Regenerate:
  GALLERY_HERO_BINS=100 python sports/scripts/sort_chop_lambda_diagnostic.py
