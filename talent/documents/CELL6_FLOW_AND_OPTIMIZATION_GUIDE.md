# Pool Metrics Flow (Cells 5–6)

This guide replaces the old CELL 6A/B/C/D flow.

## Cell 5: Pool means / minus‑means / sizes
- **Input:** `df_pipeline_04a_basic_metrics`
- **Output:** `df_pipeline_05_pool_means`
- **Function:** `add_pool_means_and_sizes()`
- **Notes:** Computes both forward and backward pool metrics.

## Cell 6: Pool ranks / percentiles / z‑scores
- **Input:** `df_pipeline_05_pool_means`
- **Output:** `df_pipeline_06_pool_ranks`
- **Function:** `add_pool_ranks_pct_zscores()`

## Why split?
- Each step is checkpointed for troubleshooting.
- Pool calculations are isolated from OER assignment.
