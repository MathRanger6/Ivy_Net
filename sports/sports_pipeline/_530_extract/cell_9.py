# =============================================================================
# CELL 9: Leave-one-out (LOO) teammate pool quality + quadratic term
# =============================================================================
# For each (team_id, season), pool quality for player i is the mean `perf` among
# teammates excluding i — i.e. sum(perf_team) - perf_i divided by (n_roster - 1).
#
# poolq_sq is the square of poolq_loo for the quadratic-in-pool-quality LPM spec.
# Rows with missing perf or singleton teams (cnt-1 == 0) drop out after LOO.


def _winsorize_series(s: pd.Series, pcts: tuple | None) -> pd.Series:
    """Clip to [q_lo, q_hi] from non-null values; no-op if pcts is None or too few rows."""
    if pcts is None:
        return s
    lo_p, hi_p = float(pcts[0]), float(pcts[1])
    if not (0.0 <= lo_p < hi_p <= 1.0):
        raise ValueError("Winsor pcts must be (lo, hi) with 0 <= lo < hi <= 1")
    v = s.dropna()
    if len(v) < 10:
        return s
    lo, hi = float(v.quantile(lo_p)), float(v.quantile(hi_p))
    if lo >= hi:
        return s
    return s.clip(lower=lo, upper=hi)


g = agg.dropna(subset=["perf", "team_id"]).copy()
_n_before = len(g)
g["perf"] = _winsorize_series(g["perf"], PERF_WINSOR_PCTS)
if PERF_WINSOR_PCTS is not None:
    print(
        f"Winsorized perf at quantiles {PERF_WINSOR_PCTS[0]:.3f}–{PERF_WINSOR_PCTS[1]:.3f} "
        f"(rows {_n_before:,}, before LOO)"
    )

# Optional: dense integer index per team-season (not used below; handy for manual checks).
idx = g.groupby(["team_id", "season"]).ngroup()

# Team-season sum of perf and roster count (same value for every row on that team-season).
sum_perf = g.groupby(["team_id", "season"])["perf"].transform("sum")
cnt = g.groupby(["team_id", "season"])["athlete_id"].transform("count")

# LOO mean teammate perf: (total - self) / (n - 1). replace(0, nan) avoids div-by-zero.
g["poolq_loo"] = (sum_perf - g["perf"]) / (cnt - 1).replace(0, np.nan)
g = g.dropna(subset=["poolq_loo"])
if POOLQ_WINSOR_PCTS is not None:
    g["poolq_loo"] = _winsorize_series(g["poolq_loo"], POOLQ_WINSOR_PCTS)
    print(
        f"Winsorized poolq_loo at quantiles {POOLQ_WINSOR_PCTS[0]:.3f}–{POOLQ_WINSOR_PCTS[1]:.3f}"
    )
g["poolq_sq"] = g["poolq_loo"] ** 2
print("After LOO:", len(g), "rows")
g[["athlete_id", "season", "team_id", "perf", "ppm", "poolq_loo", "Y_draft"]].describe()