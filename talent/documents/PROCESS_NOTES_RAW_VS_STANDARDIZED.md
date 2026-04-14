## Process Notes: Raw Ratios to Interpretable Cox Graphs

These notes outline a practical workflow for turning raw performance metrics
(ratios, pool means, pool ranks) into interpretable Cox plots and model inputs.
The goal is consistent interpretation across runs while preserving flexibility.

### 1) Start With Raw Metrics (0–1 scale)
Raw values preserve immediate meaning:
- `tb_ratio_*` and `pool_tb_ratio_mean_*` are ratios from 0–1.
- Pool ranks/percentiles are also on 0–1.
- Pool differences live around 0 if centered.

Use raw when:
- You want the x-axis to be directly interpretable (e.g., 0.20 = 20%).
- You want stable meaning across models and papers.

### 2) Choose the Pool Signal You Want
These are different constructs:
- **Pool mean**: “How strong is the pool overall?” (context).
- **Pool minus mean (exclude-self mean)**: “What is the pool average without me?” (context).
- **Pool diff (individual minus mean)**: “How far above/below the pool am I?” (signal).
- **Pool rank / percentile**: “Where do I stand in the pool?” (ordering).

Recommendation:
- Use **pool mean** for context.
- Use **pool diff** for relative performance.
- Use **rank/pct** when you want monotonic, non-parametric ordering.

### 3) Quadratic Terms: Square Raw First
Quadratic effects should be built from raw values:
1. `x_raw` (ratio or centered diff)
2. `x_sq = x_raw ** 2`
3. Optionally standardize `x_sq` (if needed for model stability)

Why:
- Squaring raw preserves interpretability (0–1 stays 0–1).
- Squaring after z-scoring creates harder-to-interpret magnitudes.

### 4) Standardization: When and Why
Use **raw** when:
- You want the x-axis to carry direct meaning.
- You want to compare across studies or contexts without rescaling.

Use **z-scores** when:
- You want coefficient comparability across variables.
- You are combining variables in interactions with different scales.

Important rule:
**Raw → square → then (optional) z-score**.

### 5) Pool Metrics: Raw vs Standardized
Recommended default usage:
- Pool mean: raw.
- Pool minus mean (exclude-self mean): raw.
- Pool diff: raw (centered around 0).
- Pool rank/percentile: raw (0–1).

Standardize only when:
- You need to compare effect sizes across different metric types.
- Your model combines variables with incompatible scales.

### 5A) Rank vs Percentile (when pool sizes vary)
If pool sizes vary greatly, **percentile** is the better default.

Why percentile works better:
- Comparable across pool sizes (0.8 always means top 20%).
- Stable scaling in pooled models.
- Easier to interpret across units and time.

When raw rank can still help:
- Pools are uniform in size.
- You want absolute position (e.g., “3rd out of 12”).
- You are doing within-pool diagnostics only.

Default for this pipeline:
- Use **percentile rank** as the standard pool position metric.

### 6) Partial Effects Plots (PE)
Goal: show hazard ratio vs meaningful x-axis values.

Best practice:
- Plot **raw x** even if the model uses z-scores internally.
- Evaluate predictions at raw values, then transform to z-scores internally.

For quadratic PE plots:
- Plot combined effect: `β1 * x + β2 * x^2`.
- Mark turning points if they fall within the observed range.

### 7) Recommended Default Path
- Use raw ratios and pool means for interpretation.
- Use pool diff for above/below mean signal.
- Use rank/pct for monotonic ordering.
- Add quadratic only when CIF bars show curvature.
- Standardize only after feature construction (squares/interactions).

### Quadratic Decision Rule (Quick)
Add a quadratic term when:
- CIF bars or CR plots show a U-shape or inverted-U.
- Theory suggests effect direction changes at extremes.
- Linear vs quadratic model comparison shows better fit.

Do not add a quadratic when:
- The relationship is monotonic and stable.
- The quadratic flips sign across minor data changes.

Key reminder:
Quadratics belong in the **model**, not just the plot. PE plots only show the
shape that the model already assumes.

### Spline vs Quadratic (Decision Rule)
Use **quadratic** when:
- The curve is roughly U-shaped or inverted-U.
- You want a simple, stable, easy-to-interpret shape.
- You are still validating signal strength and direction.

Use **splines** when:
- The curve is clearly non-linear but **not** U-shaped.
- You see **plateaus**, **thresholds**, or **multiple bends**.
- The quadratic turning point shifts a lot across runs.

Practical workflow:
1) Start with quadratic for your main variables.
2) If the fit is poor or the shape is asymmetric, switch that variable to splines.
3) Keep splines **targeted** to the variables that truly need them.

### How to Configure Quadratics (Pipeline Settings)
Quadratics are controlled in config, with base defaults in `pipeline_config.py`
and run-specific overrides in a `pip_config_file`.

#### Simple mode (most common)
Provide a list of base columns to square:
```
QUADRATIC_CONFIG = {
    'enabled': True,
    'bases': [TB_RATIO_SNR_COL, POOL_MINUS_MEAN_SNR_COL],
    'default_zscore': False,
}
```

#### Advanced mode (full control)
Define explicit terms with names and per-term z-scoring:
```
QUADRATIC_CONFIG = {
    'enabled': True,
    'terms': [
        {'base': POOL_MINUS_MEAN_SNR_COL, 'name': f\"{POOL_MINUS_MEAN_SNR_COL}_sq\", 'zscore': True},
    ],
}
```

### Example Guide: Collinearity-Aware Workflow
Use this order when building partial effects plots for tb ratio, pool minus mean,
and pool rank in the same run.

#### Calculation Order
1) Individual TB ratio (raw)
2) Pool mean (raw, inclusive)
3) Pool minus mean (raw, exclude-self mean)
4) Pool diff (raw: `tb_ratio - pool_minus_mean`)
5) Pool rank / percentile (raw, 0–1)

#### Modeling / Partial Effects Order
Start with single-variable PE plots:
- `tb_ratio_*` alone
- `pool_minus_mean_*` alone
- `pool_rank_pct_*` alone

Then test paired models:
- `tb_ratio_* + pool_minus_mean_*`
- `tb_ratio_* + pool_rank_pct_*`
- `pool_minus_mean_* + pool_rank_pct_*`

Finally, run the full model:
- `tb_ratio_* + pool_minus_mean_* + pool_rank_pct_*`

If the full model flattens or flips a shape, treat the PE curves as **conditional**
effects and interpret them as “holding the other variables constant.”

### Interaction + PE Workflow (Practical)
Use this sequence so PE plots stay informative and interaction plots stay meaningful.

1) **Main effects only**
   - Fit and plot PE curves for each variable alone.
2) **Paired models**
   - Add one additional variable at a time to detect suppression.
3) **Full model with interaction**
   - Add the interaction term and use 3D surface plots for conditional effects.
4) **Interpretation**
   - Main-effect PE plots show unconditional shape.
   - Interaction plots show conditional shape (effect of X depends on Y).

### Precompute vs Post-Filter (Time-Saving Rule)
You can precompute most features before Cell 9 filtering.

Precompute before Cell 9:
- Raw metrics (tb ratio, pool mean, pool minus mean, pool diff, pool rank/pct)
- Quadratic terms (raw → square)
- Interaction terms (raw or z, depending on config)
- Optional z-scores (if enabled)

Compute after Cell 9:
- Model fitting
- PE plots and interaction surfaces
- Any statistics tied to the filtered sample

### Base Default (Raw-First) in the Pipeline
The current default behavior in `pipeline_config.py` is:
- **Models use raw variables** (ratios, pool minus-mean, rank/pct).
- **Z-scores are computed** (optional) but **not used for model inputs**.
- **Interactions are built from raw variables** unless explicitly overridden.
- **Plots use raw variables** and exclude z-columns by default.

Run overrides (`pip_config_file`) should only change these when you want a
z-score–first or cross-variable comparison run.

### Interaction Terms and Collinearity (Why, When, How)
**Why interactions:** they answer, “Does the effect of X depend on Y?”  
Example: the effect of `tb_ratio` may be stronger or weaker depending on
`pool_minus_mean` or `pool_rank_pct`.

**How interactions create collinearity:** an interaction term is a product of
two variables that are often correlated with the originals. This can make
coefficients unstable and cause the **main-effect PE curves** to flatten or flip.

**How to interpret PE plots with interactions:**
- Main-effect PE curves become **conditional** (effect of X when Y is held fixed).
- The 3D surface plot is the **joint effect**, which often carries the shape.

**Suggested modeling order:**
1) Fit and plot single-variable PE curves (no interactions).
2) Add quadratics if CIF/CR suggests curvature.
3) Add the interaction and inspect the 3D surface.
4) Expect main-effect curves to compress once the interaction is included.

### Precompute vs Post-Filter (What to Do Early)
You can safely precompute **all feature construction** before Cell 9:
- Raw metrics (tb ratios, pool means, pool minus mean, pool diff, ranks/pct)
- Quadratic terms (built from raw columns)
- Interaction terms (built from raw columns)
- Z-scores (if you want them available but not necessarily used)

What must happen **after Cell 9 filtering**:
- Model fitting (coefficients are sensitive to the filtered sample)
- PE plots and interaction surfaces (these are model-dependent)
- Any model diagnostics or significance tests

This keeps the pipeline fast and repeatable: heavy feature creation is done once,
and all modeling steps are re-run only on the filtered dataset.

