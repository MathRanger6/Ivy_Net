# OER Metrics Overview (Current Pipeline)

## Core Functions
- `assign_oer_to_snapshots_fast()` → creates individual fwd/bwd metrics (Cell 4)
- `add_pool_means_and_sizes()` → pool means/minus-means/sizes (Cell 5)
- `add_pool_ranks_pct_zscores()` → pool ranks/pct/z-scores (Cell 6)

## Outputs
- Cell 4 → `df_pipeline_04a_basic_metrics`
- Cell 5 → `df_pipeline_05_pool_means`
- Cell 6 → `df_pipeline_06_pool_ranks`
