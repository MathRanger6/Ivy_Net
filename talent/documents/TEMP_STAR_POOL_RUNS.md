# Star vs Strong Pool: Run Guide (Print Copy)

This sheet is a step‑by‑step guide for running the model twice to compare **absolute performance** vs **relative rank** effects.
**Senior rater focus**: All examples below use `_snr` variables. Rater variants (`_rtr`) are available but should be used only when you explicitly want rater‑level nuance.

---

## What “run the model” means

Model fitting happens in **Cell 12**, specifically:
- **12.1** prepare data
- **12.3** fit full model
- **12.6/12.7** model‑based plots (optional)

**Note on pool metrics**: New pool‑rank variables (percentile + z‑score) are **computed in Cell 6D** (pool metrics). Cell 6C is pre‑pool prep only. Listing them in `COLUMN_CONFIG['oer_variables']` just makes them eligible for plots/filtering—it does not create them.

---



## RUN 1 — Absolute performance (pool strength via z‑score)

**Goal:** test whether absolute performance is affected by pool strength.

### Create the interaction term

In `INTERACTION_CONFIG` (pipeline_config.py), add:

```
INTERACTION_CONFIG['terms'] = [
  {
    'name': 'star_pool_interaction',
    'left': 'z_cum_tb_rcvd_ratio_snr',
    'right': 'z_tb_ratio_zpool_snr',
    'zscore': True,
  },
]
```

Then run **10.5** to create `z_star_pool_interaction`.

### Model variables (Cell 12)

Set in `pipeline_config.py`:

```
COLUMN_CONFIG['model_time_varying_cols'] = [
    'z_cum_tb_rcvd_ratio_snr',
    'z_tb_ratio_zpool_snr',
    'z_star_pool_interaction',
]
```

### CR plots (Cell 11, descriptive)

Add to `PLOT_CONFIG['plots']` (if you want descriptive curves):

- `z_cum_tb_rcvd_ratio_snr`
- `z_tb_ratio_zpool_snr`

### 12.7 interaction plots (Cell 12.7)

Set in `INTERACTION_CONFIG['plots']` (pipeline_config.py):

```
INTERACTION_CONFIG['plots'] = [
  {
    'name': 'abs_perf_vs_pool',
    'var_x': 'cum_tb_rcvd_ratio_snr',
    'var_y': 'tb_ratio_zpool_snr',
    'use_z': True,
  },
]
```

### Cells to run

1. **10.5** (create z_ columns + interaction)
2. **12.1 → 12.3** (fit)
3. **12.6/12.7** (plots)

---

## RUN 2 — Relative rank (within‑pool percentile)

**Goal:** test whether relative standing is affected by pool strength.

### Create the interaction term

In `INTERACTION_CONFIG` (pipeline_config.py), add:

```
INTERACTION_CONFIG['terms'] = [
  {
    'name': 'rank_pool_interaction',
    'left': 'z_tb_ratio_rank_pct_snr',
    'right': 'z_tb_ratio_zpool_snr',
    'zscore': True,
  },
]
```

Then run **10.5** to create `z_rank_pool_interaction`.

### Model variables (Cell 12)

```
COLUMN_CONFIG['model_time_varying_cols'] = [
    'z_tb_ratio_rank_pct_snr',
    'z_tb_ratio_zpool_snr',
    'z_rank_pool_interaction',
]
```

### CR plots (Cell 11, descriptive)

Add (if desired):
- `z_tb_ratio_rank_pct_snr`

### 12.7 interaction plots (Cell 12.7)

Set in `INTERACTION_CONFIG['plots']`:

```
INTERACTION_CONFIG['plots'] = [
  {
    'name': 'rank_vs_pool',
    'var_x': 'tb_ratio_rank_pct_snr',
    'var_y': 'tb_ratio_zpool_snr',
    'use_z': True,
  },
]
```

### Cells to run

1. **10.5**
2. **12.1 → 12.3**
3. **12.6/12.7**

---

## RUN 3 — Prestige vs cumulative TB (Z‑scores)

**Goal:** compare prestige exposure vs cumulative TB using standardized variables.

**Do we need two runs?**  
No. A single run with the interaction is appropriate here because you are comparing **prestige exposure** vs **cumulative TB** directly.  
You only need **two runs** when you are swapping in **alternative, highly collinear constructs** (e.g., cumulative TB vs rank‑normalized TB) that should not be in the same model.

### Create the interaction term

In `INTERACTION_CONFIG` (pipeline_config.py), add:

```
INTERACTION_CONFIG['terms'] = [
  {
    'name': 'prestige_tb_interaction',
    'left': 'z_prestige_mean',
    'right': 'z_cum_tb_rcvd_ratio_snr',
    'zscore': True,
  },
]
```

Then run **10.5** to create `z_prestige_tb_interaction`.

### Model variables (Cell 12)

```
COLUMN_CONFIG['model_time_varying_cols'] = [
    'z_prestige_mean',
    'z_cum_tb_rcvd_ratio_snr',
    'z_prestige_tb_interaction',
]
```

### CR plots (Cell 11, descriptive)

Add (if desired):
- `z_prestige_mean`
- `z_cum_tb_rcvd_ratio_snr`

### 12.7 interaction plots (Cell 12.7)

Set in `INTERACTION_CONFIG['plots']`:

```
INTERACTION_CONFIG['plots'] = [
  {
    'name': 'prestige_vs_cum_tb',
    'var_x': 'prestige_mean',
    'var_y': 'cum_tb_rcvd_ratio_snr',
    'use_z': True,
    'var_x_label': 'z_prestige_mean',
    'var_y_label': 'z_cum_tb_rcvd_ratio_snr',
  },
]
```

### Cells to run

1. **10.5**
2. **12.1 → 12.3**
3. **12.6/12.7**

---

## Interpretation key

- **Negative interaction** → “star in strong pool” gets **less** marginal benefit.
- **Positive interaction** → “star in strong pool” gets **more** marginal benefit.

