#!/bin/zsh
# Disposable perf-metric EDA — run from repo root.
export PYTHONPATH="sports"
python3 sports/scripts/perf_metric_rho_eda.py "$@"
# LOO-shape promotion gate (COMPASS):
# python3 sports/scripts/perf_metric_loo_shape_batch.py "$@"
