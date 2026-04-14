## Decision Chart: Raw vs Z-Score vs Rank vs Pool Diff

Use this chart to pick the right form of a metric for modeling and plots.

### Step 1: What question are you answering?
- **Context**: “How strong is the pool overall?” → use **pool mean** (raw).
- **Relative advantage**: “How far above/below the pool am I?” → use **pool diff** (raw).
- **Ordering**: “Where do I stand in the pool?” → use **rank/pct** (raw).
- **Direct performance**: “What is my TB rate?” → use **tb_ratio** (raw).

### Step 2: Do you need cross-variable comparability?
- **No** → stay raw.
- **Yes** → z-score **after** all feature construction (squares/interactions).

### Step 3: Do you need curvature (U-shape)?
- **No** → keep linear term only.
- **Yes** → add quadratic: `x_sq = x_raw ** 2` (then optional z-score).

### Step 4: Plotting rule
Always plot **raw x** for interpretability, even if the model uses z-scores.

### Step 5: Collinearity-aware modeling order
When using tb ratio, pool minus mean, and pool rank together:
1) Run single-variable PE plots first (one at a time).
2) Then run paired models to check suppression:
   - `tb_ratio_* + pool_minus_mean_*`
   - `tb_ratio_* + pool_rank_pct_*`
   - `pool_minus_mean_* + pool_rank_pct_*`
3) Finally run the full model with all three.
If shapes flatten or flip, interpret curves as **conditional** effects.

---

## Quick Reference Table

| Metric Type | Default Form | Use Z-Score? | Notes |
|---|---|---|---|
| Individual TB ratio | Raw (0–1) | Only if comparing coefficients | Interpretable x-axis |
| Pool mean | Raw (0–1) | Rarely | Context effect |
| Pool minus mean (exclude-self mean) | Raw | Rarely | Context without self |
| Pool diff (individual − mean) | Raw (centered at 0) | Optional | Positive = above mean |
| Pool rank / percentile | Raw (0–1) | Usually no | Monotonic ordering |

---

## Quadratic Rule (Always)
1. Build from raw: `x_sq = x_raw ** 2`
2. Then z-score if needed
3. Plot combined effect on raw x-axis

---

## Quadratic Config (Quick Use)
Base defaults live in `pipeline_config.py`, run overrides in `pip_config_file`.

Simple:
```
QUADRATIC_CONFIG = {
    'enabled': True,
    'bases': [TB_RATIO_SNR_COL, POOL_MINUS_MEAN_SNR_COL],
    'default_zscore': False,
}
```

Advanced:
```
QUADRATIC_CONFIG = {
    'enabled': True,
    'terms': [
        {'base': POOL_MINUS_MEAN_SNR_COL, 'name': f\"{POOL_MINUS_MEAN_SNR_COL}_sq\", 'zscore': True},
    ],
}
```

---

## Raw-First Default (Current)
The pipeline currently defaults to:
- Raw variables for model inputs
- Z-scores computed but **not used** in the model
- Interactions built from raw variables
- Plots use raw variables by default

Override this in `pip_config_file` only when you want a z-score–first run.

