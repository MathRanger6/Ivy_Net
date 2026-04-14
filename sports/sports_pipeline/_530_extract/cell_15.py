# =============================================================================
# CELL 15: Visualize fitted quadratic in poolq_loo (marginal effect plot)
# =============================================================================
# Uses the same OLS coefficients as the LPM cell. Holds `perf` at its sample mean and
# each season dummy at its sample mean (so the curve is poolq_loo + poolq_sq with those
# offsets). Optional overlay: ventile bin means from the EDA cell if `binned` exists.
# Vertical line: interior turning point -b2/(2*b3) when it lies inside the data range.

if HAS_SM and "res" in dir():
    dplot = g.dropna(subset=["perf", "poolq_loo", "poolq_sq", "Y_draft"]).copy()
    season_d_plot = pd.get_dummies(dplot["season"].astype(int), prefix="s", drop_first=True).astype(float)
    p = res.params
    # Fix self-performance at mean when tracing the pool-quality curve.
    perf_bar = float(dplot["perf"].mean())
    # Contribution of season FE evaluated at mean dummy vector (same sample as dplot).
    season_part = 0.0
    for col in season_d_plot.columns:
        if col in p.index:
            season_part += float(p[col]) * float(season_d_plot[col].mean())

    c0 = float(p.get("const", 0.0))
    b1 = float(p.get("perf", 0.0))
    b2 = float(p.get("poolq_loo", 0.0))
    b3 = float(p.get("poolq_sq", 0.0))

    def pred_from_poolq(x):
        return c0 + b1 * perf_bar + b2 * x + b3 * x * x + season_part

    grid = np.linspace(float(dplot["poolq_loo"].min()), float(dplot["poolq_loo"].max()), 200)
    y_fit = np.array([pred_from_poolq(x) for x in grid])

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.plot(grid, y_fit, color="darkred", lw=2.2, label="LPM (perf & seasons @ means)")

    if "binned" in dir() and len(binned):
        ax.scatter(
            binned["poolq_loo_mid"],
            binned["mean_y_draft"],
            s=36,
            color="steelblue",
            edgecolors="white",
            linewidths=0.5,
            zorder=5,
            label="Ventile mean Y_draft (3b)",
        )

    if np.isfinite(b3) and b3 != 0:
        tp = -b2 / (2 * b3)
        lo, hi = float(dplot["poolq_loo"].min()), float(dplot["poolq_loo"].max())
        if lo <= tp <= hi:
            ax.axvline(tp, color="gray", ls="--", lw=1.1, label=f"Turning point ≈ {tp:.4f}")

    ax.set_xlabel("Leave-one-out teammate pool quality (poolq_loo)")
    ax.set_ylabel("Predicted / mean draft rate")
    ax.set_title("Quadratic fit: predicted P(Y_draft) vs pool quality")
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout(rect=[0, 0.08, 1, 1])
    fig.text(
        0.5,
        0.02,
        f"Performance metric (perf): {PERF_METRIC!r}",
        ha="center",
        fontsize=9,
        color="0.35",
        transform=fig.transFigure,
    )
    plt.show()
else:
    print("Run the LPM cell (statsmodels) first.")