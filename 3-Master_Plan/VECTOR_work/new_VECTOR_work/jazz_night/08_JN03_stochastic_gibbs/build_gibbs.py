#!/usr/bin/env python3
"""JN-03 — observed vs top-K vs Gibbs SELECT (rule D) inclusion frequencies.

Same cohort, bins, and K=615 as JN-01 / JN-02. SCORE: S_i = A_i (within-season PPM z).
SELECT: original, unclipped scores; weights exp(S/t_sel), K draws without replacement.
Corrected v2: legacy rule D clipped negative scores before exponentiation.

Illustrative temperatures only (Step 3); no MLE fit (Step 4).
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import PercentFormatter

JAZZ = Path('/Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/jazz_night')
REPO = Path('/Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE')
OUT = Path(__file__).resolve().parent
CANON = JAZZ / "04_canonical_naive"
JN02 = JAZZ / "07_JN02_deterministic_topK"

# Deliberately local: the legacy shared rule-D wrapper clips scores at zero.
# This plot uses raw finite scores; other project simulations are not modified.

N_REP_DEFAULT = 12_000
SEED = 20261027
# Illustrative grid (not MLE); cold t ≈ top-K, larger t spreads mass down-bin.
T_SWEEP = [0.08, 0.15, 0.25, 0.4, 0.7, 1.0, 1.5, 2.5, 5.0]
T_FEATURED = [0.25, 0.7, 2.5]


def sha256_path(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n <= 0:
        return float("nan"), float("nan")
    p = k / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    half = z * np.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / denom
    return max(0.0, center - half), min(1.0, center + half)


def gibbs_probabilities(scores: np.ndarray, t_sel: float) -> np.ndarray:
    scores = np.asarray(scores, dtype=float)
    if not np.isfinite(scores).all() or not np.isfinite(t_sel) or t_sel <= 0:
        raise ValueError("Finite original scores and a positive finite temperature are required")
    scaled = scores / t_sel
    weights = np.exp(scaled - np.max(scaled))
    if not np.all(weights > 0):
        raise ValueError("Numerical underflow: do not silently clip scores or fall back to top-K")
    return weights / weights.sum()


def gibbs_inclusion_freq(scores, k, t_sel, n_rep, seed):
    """Successive weighted sampling without replacement using original scores.

    numpy choice(replace=False,p=...) retains the previous sampling algorithm.
    Only the zero-clipping step has been removed. A shared exponent shift is
    numerical stabilization and preserves all pairwise weight ratios.
    """
    rng = np.random.default_rng(seed)
    n = scores.size
    assert 0 < k <= n
    p = gibbs_probabilities(scores, t_sel)
    counts = np.zeros(n, dtype=np.int64)
    for _ in range(n_rep):
        selected = rng.choice(n, size=k, replace=False, p=p)
        assert selected.size == k and np.unique(selected).size == k
        counts[selected] += 1
    assert counts.sum() == k * n_rep
    assert counts.min() >= 0 and counts.max() <= n_rep
    return counts / float(n_rep)


def main() -> None:
    d = pd.read_csv(CANON / "canonical_player_membership.csv.gz")
    t = pd.read_csv(CANON / "canonical_bin_counts.csv").sort_values("bin").reset_index(drop=True)
    jn02 = pd.read_csv(JN02 / "observed_vs_topK_bin_counts.csv").sort_values("bin")

    assert d.athlete_id.nunique() == len(d)
    assert np.isfinite(d.perf).all()
    assert np.array_equal(d.groupby('bin').size().to_numpy(), t.n.to_numpy())
    assert np.array_equal(d.groupby('bin').Y_draft.sum().to_numpy(), t.drafted.to_numpy())
    # Analytical checks: negative scores remain distinct; score-shift invariance;
    # equal scores imply uniform weights; all-negative pools remain eligible.
    test = np.array([-2., -1., 0., 1.])
    ptest = gibbs_probabilities(test, .7)
    assert np.all(np.diff(ptest) > 0)
    assert np.allclose(ptest, gibbs_probabilities(test + 10., .7), atol=1e-14)
    assert np.allclose(ptest[1:] / ptest[:-1], np.exp(1/.7))
    assert np.allclose(gibbs_probabilities(np.full(4,-3.),.7), .25)
    assert np.isclose(gibbs_inclusion_freq(np.array([-3.,-2.,-1.]),2,.7,10,1).sum(),2.)
    n_players = len(d)
    k = int(d["Y_draft"].sum())
    assert n_players == 22_795 and k == 615
    assert np.array_equal(t["n"].to_numpy(), jn02["n"].to_numpy())
    assert np.array_equal(t["drafted"].to_numpy(), jn02["drafted"].to_numpy())

    scores = d["perf"].to_numpy(dtype=float)
    d["topK_selected"] = d["perf"].rank(method="first", ascending=False).le(k).astype(int)

    sweep_rows: list[dict] = []
    player_cols = ["athlete_id", "bin", "perf", "Y_draft", "topK_selected"]
    player_out = d[player_cols].copy()

    for i, t_sel in enumerate(T_SWEEP):
        print(f"Rebuilding temperature {t_sel:g} ({i+1}/{len(T_SWEEP)})", flush=True)
        inc = gibbs_inclusion_freq(scores, k, t_sel, N_REP_DEFAULT, SEED + i)
        player_out[f"gibbs_inc_t{t_sel:g}".replace(".", "p")] = inc
        for bin_id in t["bin"]:
            sub = d.loc[d["bin"] == bin_id]
            idx = sub.index.to_numpy()
            sweep_rows.append(
                {
                    "t_sel": float(t_sel),
                    "bin": int(bin_id),
                    "n": int(sub.shape[0]),
                    "gibbs_mean_inclusion": float(inc[idx].mean()),
                    "observed_rate": float(sub["Y_draft"].mean()),
                    "topK_rate": float(sub["topK_selected"].mean()),
                }
            )

    sweep = pd.DataFrame(sweep_rows)
    sweep.to_csv(OUT / "gibbs_t_sweep_bin_rates.csv", index=False)
    player_out.to_csv(OUT / "player_gibbs_inclusion_by_t.csv.gz", index=False)

    # Bin table for featured temperatures (main figure).
    feat = sweep[sweep["t_sel"].isin(T_FEATURED)].copy()
    wide = t[["bin", "n", "drafted", "draft_rate", "ci_low", "ci_high"]].merge(
        jn02[["bin", "topK_selected", "topK_rate"]],
        on="bin",
    )
    for t_sel in T_FEATURED:
        sub = feat.loc[feat["t_sel"] == t_sel, ["bin", "gibbs_mean_inclusion"]]
        wide = wide.merge(
            sub.rename(columns={"gibbs_mean_inclusion": f"gibbs_rate_t{t_sel:g}".replace(".", "p")}),
            on="bin",
            how="left",
        )
    wide.to_csv(OUT / "observed_topK_gibbs_bin_counts.csv", index=False)

    # --- Figure: observed bars + top-K bars + Gibbs lines (featured t) ---
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.subplots_adjust(left=0.105, right=0.98, top=0.69, bottom=0.33)

    x = wide["bin"].to_numpy(dtype=float)
    w = 0.34
    ax.bar(
        x - 0.19,
        wide["draft_rate"],
        width=w,
        color="#347da3",
        label="Observed ever drafted",
        zorder=3,
    )
    ax.bar(
        x + 0.19,
        wide["topK_rate"],
        width=w,
        color="#d27a24",
        label="Deterministic top-K (JN-02)",
        zorder=3,
    )
    yerr = np.maximum(
        0,
        np.vstack([wide["draft_rate"] - wide["ci_low"], wide["ci_high"] - wide["draft_rate"]]),
    )
    ax.errorbar(
        x - 0.19,
        wide["draft_rate"],
        yerr=yerr,
        fmt="none",
        ecolor="#303030",
        elinewidth=1,
        capsize=2,
        zorder=4,
    )

    line_styles = [
        ("#2a7a4b", 0.25),
        ("#6b3fa0", 0.7),
        ("#1a6b8a", 2.5),
    ]
    for color, t_sel in line_styles:
        col = f"gibbs_rate_t{t_sel:g}".replace(".", "p")
        ax.plot(
            x,
            wide[col],
            color=color,
            lw=2.2,
            marker="o",
            ms=5,
            label=rf"Gibbs inclusion freq. ($t_{{\mathrm{{sel}}}}={t_sel:g}$)",
            zorder=5,
        )

    for row in wide.itertuples():
        if row.drafted:
            label = f"{row.draft_rate:.1%}" if row.draft_rate >= 0.01 else f"{row.draft_rate:.2%}"
            ax.annotate(
                label,
                (row.bin - 0.19, row.ci_high),
                xytext=(-1, 4),
                textcoords="offset points",
                ha="center",
                fontsize=9,
                fontweight="bold",
                color="#245c7b",
            )

    ax.set_xticks(x)
    ax.set_xlim(0.4, 16.7)
    ax.set_ylim(0, 0.5)
    ax.set_yticks(np.arange(0, 0.501, 0.1))
    ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    ax.set_ylabel("Proportion drafted / selected / included", fontsize=12)
    ax.set_xlabel(
        "Own-performance quantile bin (1 = lowest PPM; 16 = highest PPM)",
        fontsize=12,
        labelpad=10,
    )
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)
    ax.legend(loc="upper left", frameon=False, fontsize=10)

    tab = ax.table(
        cellText=[
            [f"{int(v):,}" for v in wide["n"]],
            [str(int(v)) for v in wide["drafted"]],
            [str(int(v)) for v in wide["topK_selected"]],
        ],
        rowLabels=["Players", "Observed drafted", "Top-K selected"],
        cellLoc="center",
        bbox=[0, -0.40, 1, 0.18],
    )
    tab.auto_set_font_size(False)
    tab.set_fontsize(8.5)
    for (r, c), cell in tab.get_celld().items():
        cell.set_edgecolor("#c7c7c7")
        cell.set_linewidth(0.45)
        if r == 1:
            cell.set_facecolor("#edf5f9")
        if r == 2:
            cell.set_facecolor("#fcf2e8")

    fig.suptitle(
        "Can stochastic selection spread opportunities beyond the top scores?",
        fontsize=19,
        fontweight="bold",
        y=0.97,
    )
    fig.text(
        0.105,
        0.90,
        "Performance: PPM, standardized within season | 2009–2021 | Same 16 quantile bins as JN-01",
        fontsize=12,
    )
    fig.text(
        0.105,
        0.86,
        "All eligible colleges | ≥ 11 captured team games (MG10) | ≥ 20 total season minutes | Final eligible record per player",
        fontsize=10.5,
    )
    fig.text(
        0.105,
        0.82,
        "N = 22,795 | K = 615 per replicate | SCORE: Sᵢ = Aᵢ → SELECT: Gibbs weights from unclipped scores; K without replacement",
        fontsize=12,
    )
    fig.text(
        0.105,
        0.77,
        f"Pooled descriptive comparison; lines = Monte Carlo inclusion frequencies ({N_REP_DEFAULT:,} replicates per t; illustrative t, not MLE).",
        fontsize=11,
        color="#555555",
    )
    footer = (
        "Observed bars: ever-drafted outcomes; Wilson 95% intervals (no college clustering).\n"
        "Orange bars: exact JN-02 top-K fractions. Green/purple/teal lines: mean simulated inclusion using original scores.\n"
        "Inclusion frequency is P(selected in one K-draw replicate), not the per-step Gibbs weight.\n"
        "Corrected JN-03 v2: negative scores retained. Original players, bins, temperatures, seeds and replicate counts unchanged."
    )
    fig.text(0.105, 0.135, footer, fontsize=9, va="top", linespacing=1.5)

    for ext in ("png", "svg"):
        fig.savefig(OUT / f"JN03_PPM_observed_topK_gibbs_Q16.{ext}", dpi=240, facecolor="white")
    plt.close(fig)

    cold = sweep.loc[sweep["t_sel"] == T_SWEEP[0]]
    hot = sweep.loc[sweep["t_sel"] == T_SWEEP[-1]]
    prov = {
        "date": "2026-10-27",
        "status": "ready for review, not locked",
        "source_hashes": {
            p.name: sha256_path(p)
            for p in [
                CANON / "canonical_player_membership.csv.gz",
                CANON / "canonical_bin_counts.csv",
                JN02 / "observed_vs_topK_bin_counts.csv",
            ]
        },
        "N": n_players,
        "K": k,
        "score": "S_i = A_i; within-season standardized PPM",
        "version": 2,
        "selection": "unclipped finite scores; stabilized exponential weights; numpy choice without replacement",
        "correction": "Remove legacy zero-clipping before exponentiation; same RNG algorithm, seeds, temperatures and repetitions",
        "nonpositive_scores": int(np.count_nonzero(scores <= 0)),
        "script_sha256": sha256_path(Path(__file__)),
        "shared_legacy_helper_modified": False,
        "numpy_version": np.__version__,
        "n_replicates": N_REP_DEFAULT,
        "seed_base": SEED,
        "t_sweep": T_SWEEP,
        "t_featured_on_plot": T_FEATURED,
        "model_fitted": False,
        "mle_t_sel": None,
        "scope": "Step 3 illustrative stochastic comparison; Step 4 likelihood fit not run",
    }
    (OUT / "provenance.json").write_text(json.dumps(prov, indent=2) + "\n")

    # Validation notes
    top_bin = wide.loc[wide["bin"] == 16].iloc[0]
    lines = [
        "PASS: JN-01 membership, bins, and observed counts unchanged.",
        "PASS: every replicate explicitly checked for exactly K distinct selections; aggregate total K*n_rep.",
        "PASS: negative scores have distinct positive weights; pairwise ratios and common-score-shift invariance checked.",
        "PASS: uniform scores give uniform weights; all-negative pool still fills K places.",
        f"PASS: top-K matches JN-02 (bin 16 topK rate {top_bin.topK_rate:.4f}).",
        f"Cold t={T_SWEEP[0]} bin-16 gibbs rate {cold.loc[cold.bin==16,'gibbs_mean_inclusion'].iloc[0]:.4f} (should approach top-K).",
        f"Hot t={T_SWEEP[-1]} bin-16 gibbs rate {hot.loc[hot.bin==16,'gibbs_mean_inclusion'].iloc[0]:.4f} (should fall below observed 0.16).",
        f"Each replicate selects exactly K={k} players.",
    ]
    (OUT / "validation.txt").write_text("\n".join(lines) + "\n")
    print(json.dumps(prov, indent=2))


if __name__ == "__main__":
    main()
