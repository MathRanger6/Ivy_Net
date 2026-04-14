# =============================================================================
# CELL 13: Linear probability model (LPM) with quadratic pool quality + season FE
# =============================================================================
# Model: Y_draft ~ perf + poolq_loo + poolq_sq + season dummies (drop_first).
# - Y is binary draft indicator; LPM coefficients are marginal probability changes.
# - Cluster-robust SEs at team_id account for repeated team-seasons across years/players.
# - Turning point of quadratic in poolq_loo (holding linear terms fixed): -b2/(2*b3).

try:
    import statsmodels.api as sm

    HAS_SM = True
except ImportError:
    HAS_SM = False
    print("Install statsmodels for LPM + clustered SEs: pip install statsmodels")

if HAS_SM:
    # Complete-case for all regressors (SR perf can be NaN for unmatched rows).
    d = g.dropna(subset=["perf", "poolq_loo", "poolq_sq", "Y_draft"]).copy()
    # Season fixed effects: drop_first avoids perfect collinearity with constant.
    season_d = pd.get_dummies(d["season"].astype(int), prefix="s", drop_first=True).astype(float)
    X = pd.concat([d[["perf", "poolq_loo", "poolq_sq"]].astype(float), season_d], axis=1)
    X = sm.add_constant(X, has_constant="add")
    y = d["Y_draft"].astype(float)
    # cov_type="cluster" + groups=team_id: inference robust to within-team correlation.
    res = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": d["team_id"]})
    print(res.summary().tables[1])
    b2 = res.params.get("poolq_loo", float("nan"))
    b3 = res.params.get("poolq_sq", float("nan"))
    if np.isfinite(b2) and np.isfinite(b3) and b3 != 0:
        tp = -b2 / (2 * b3)
        print(f"\nTurning point (poolq): {tp:.4f}")
else:
    print("Skipping fit — add statsmodels")