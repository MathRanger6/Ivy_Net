# =============================================================================
# CELL 11: Nonparametric EDA — draft rate by ventile of LOO pool quality
# =============================================================================
# Splits the sample into ~20 equal-count bins on poolq_loo (ventiles when unique values allow).
# Left panel: mean Y_draft vs bin index (1 = lowest teammate pool quality).
# Right panel: same means vs median poolq_loo inside each bin (actual x-scale).

dfp = g.dropna(subset=["poolq_loo", "Y_draft"]).copy()
# qcut with duplicates="drop" handles ties at bin edges (can yield <20 bins).
dfp["poolq_bin"] = pd.qcut(dfp["poolq_loo"], q=20, duplicates="drop")

binned = (
    dfp.groupby("poolq_bin", observed=True)
    .agg(
        mean_y_draft=("Y_draft", "mean"),
        n=("Y_draft", "size"),
        poolq_loo_mid=("poolq_loo", "median"),
        poolq_loo_lo=("poolq_loo", "min"),
        poolq_loo_hi=("poolq_loo", "max"),
    )
    .reset_index()
)
binned["bin_i"] = range(1, len(binned) + 1)

print(binned[["bin_i", "poolq_loo_lo", "poolq_loo_hi", "n", "mean_y_draft"]].to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(11, 4))

ax = axes[0]
ax.bar(binned["bin_i"], binned["mean_y_draft"], color="steelblue", edgecolor="white", linewidth=0.4)
ax.set_xlabel("Ventile bin (1 = lowest poolq_loo)")
ax.set_ylabel("Mean Y_draft")
ax.set_title("Mean draft rate by ventile of poolq_loo (LOO teammate perf)")

ax = axes[1]
ax.plot(binned["poolq_loo_mid"], binned["mean_y_draft"], marker="o", ms=4, color="steelblue")
ax.set_xlabel("Median poolq_loo in bin")
ax.set_ylabel("Mean Y_draft")
ax.set_title("Same pattern vs pool quality level")

# Leave footroom for the PERF_METRIC caption (figure coordinates, not axes).
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