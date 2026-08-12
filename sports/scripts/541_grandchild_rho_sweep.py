#!/usr/bin/env python3
"""541 — Grandchild ASSIGN ρ sweep on empirical 2015 MBB abilities.

Uses N = all filtered player-seasons in 2015, C = 15, J = N/15 (402 teams).

Run (repo root):
  python sports/scripts/541_grandchild_rho_sweep.py
  python sports/scripts/541_grandchild_rho_sweep.py --realizations 20 --quick
  python sports/scripts/541_grandchild_rho_sweep.py --progress-every 10

Outputs (HEROs_and_PASSes/grandchild_assign/):
  GRANDCHILD_rho_sweep_D_H.png
  GRANDCHILD_rho_sweep_centroid_sd.png
  GRANDCHILD_rho_sweep_example_centroids.png
  GRANDCHILD_rho_sweep_summary.csv
  GRANDCHILD_rho_sweep_meta.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SPORTS = REPO / "sports"
sys.path.insert(0, str(SPORTS))
sys.path.insert(0, str(REPO))

from hero_gallery_paths import GRANDCHILD_ASSIGN, ensure_hero_dirs

OUT = GRANDCHILD_ASSIGN
PNG_DH = OUT / "GRANDCHILD_rho_sweep_D_H.png"
PNG_RHO_H = OUT / "GRANDCHILD_rho_vs_assortativity.png"
PNG_RHO_WSS = OUT / "GRANDCHILD_rho_vs_global_wss.png"
PNG_SD = OUT / "GRANDCHILD_rho_sweep_centroid_sd.png"
PNG_EX = OUT / "GRANDCHILD_rho_sweep_example_centroids.png"
CSV_SUM = OUT / "GRANDCHILD_rho_sweep_summary.csv"
META_JSON = OUT / "GRANDCHILD_rho_sweep_meta.json"

DEFAULT_RHO = [float(x) for x in np.linspace(0.0, 1.0, 21)]  # calibration band 0–1


def _load_modules():
    import importlib

    gc = importlib.import_module("541_grandchild_homophily_assign")
    tpa = importlib.import_module("tier1_pool_assignment")
    return gc, tpa


def _run_sweep(
    ability: np.ndarray,
    roster_size: int,
    rho_values: list[float],
    n_realizations: int,
    base_seed: int,
    *,
    progress_every: int = 5,
) -> tuple[pd.DataFrame, pd.DataFrame, list[dict]]:
    gc, _ = _load_modules()
    rows: list[dict] = []
    examples: list[dict] = []
    total_runs = len(rho_values) * n_realizations
    done = 0
    t0 = time.perf_counter()

    print(
        f"Sweep: {len(rho_values)} rho arms × {n_realizations} reps = {total_runs} runs",
        flush=True,
    )

    for rho_idx, rho in enumerate(rho_values):
        print(
            f"\n=== rho={rho:g} ({rho_idx + 1}/{len(rho_values)}) ===",
            flush=True,
        )
        d_vals: list[float] = []
        h_vals: list[float] = []
        wss_vals: list[float] = []
        sd_vals: list[float] = []
        for rep in range(n_realizations):
            seed = int(base_seed + rep + 1000 * int(rho * 100))
            rng = np.random.default_rng(seed)
            res = gc.run_one_realization(
                ability, roster_size, float(rho), rng=rng, seed=seed
            )
            rows.append(
                {
                    "rho": float(rho),
                    "rep": int(rep),
                    "seed": seed,
                    "D_within_team_mse": res.within_team_mse,
                    "H_sorting_index": res.sorting_index_h,
                    "global_wss": res.global_wss,
                    "centroid_sd": res.centroid_sd,
                    "n_teams": res.n_teams,
                }
            )
            d_vals.append(res.within_team_mse)
            h_vals.append(res.sorting_index_h)
            wss_vals.append(res.global_wss)
            sd_vals.append(res.centroid_sd)
            done += 1
            if progress_every > 0 and (
                (rep + 1) % progress_every == 0 or rep + 1 == n_realizations
            ):
                elapsed = time.perf_counter() - t0
                rate = done / elapsed if elapsed > 0 else float("nan")
                eta = (total_runs - done) / rate if rate > 0 else float("nan")
                print(
                    f"  rep {rep + 1}/{n_realizations} | "
                    f"overall {done}/{total_runs} ({100 * done / total_runs:.0f}%) | "
                    f"H_sort={res.sorting_index_h:.3f} global_wss={res.global_wss:,.0f} | "
                    f"{elapsed:.0f}s elapsed"
                    + (f", ~{eta:.0f}s left" if eta == eta else ""),
                    flush=True,
                )
            if rep == 0 and rho in (rho_values[0], rho_values[len(rho_values) // 2], rho_values[-1]):
                examples.append(
                    {
                        "rho": float(rho),
                        "mu_final": res.mu_final.tolist(),
                        "seed": seed,
                    }
                )
        print(
            f"  rho={rho:g} summary: "
            f"H_sort={np.mean(h_vals):.3f}±{np.std(h_vals):.3f}  "
            f"global_wss={np.mean(wss_vals):,.0f}±{np.std(wss_vals):,.0f}  "
            f"D={np.mean(d_vals):.3f}",
            flush=True,
        )

    elapsed = time.perf_counter() - t0
    print(f"\nSweep finished in {elapsed:.1f}s ({total_runs} runs).", flush=True)

    detail = pd.DataFrame(rows)
    summary = (
        detail.groupby("rho", as_index=False)
        .agg(
            n_realizations=("rep", "count"),
            D_mean=("D_within_team_mse", "mean"),
            D_std=("D_within_team_mse", "std"),
            H_mean=("H_sorting_index", "mean"),
            H_std=("H_sorting_index", "std"),
            global_wss_mean=("global_wss", "mean"),
            global_wss_std=("global_wss", "std"),
            centroid_sd_mean=("centroid_sd", "mean"),
            centroid_sd_std=("centroid_sd", "std"),
        )
        .sort_values("rho")
    )
    return detail, summary, examples


def _plot_rho_vs_assortativity(summary: pd.DataFrame, out_path: Path) -> None:
    """Single-panel Alex brief: homophily ρ (ASSIGN knob) vs realized assortativity H_sort."""
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()

    n_rep = int(summary["n_realizations"].iloc[0]) if "n_realizations" in summary.columns else 30
    fig, ax = plt.subplots(figsize=(7.5, 5))
    x = summary["rho"].to_numpy()
    y = summary["H_mean"].to_numpy()
    yerr = summary["H_std"].fillna(0.0).to_numpy()
    ax.errorbar(
        x,
        y,
        yerr=yerr,
        fmt="o-",
        capsize=4,
        color="#1a5490",
        ecolor="#6a8caf",
        markersize=6,
        linewidth=1.5,
        label=rf"Mean $H_{{sort}}$ ± 1 SD ({n_rep} reps)",
    )
    if len(x) >= 2:
        coef = np.polyfit(x, y, 1)
        x_line = np.linspace(float(x.min()), float(x.max()), 100)
        ax.plot(x_line, np.polyval(coef, x_line), "--", color="#b03030", lw=1.2, alpha=0.85, label="OLS trend")
    ax.set_xlabel(r"Homophily knob $\rho$ (LG ASSIGN)", fontsize=11)
    ax.set_ylabel(r"Realized assortativity $H_{sort}$", fontsize=11)
    ax.set_title(
        r"Increase homophily $\rho$ $\Rightarrow$ increase realized assortativity $H_{sort}$",
        fontsize=12,
        pad=10,
    )
    ax.set_xlim(-0.02, 1.02)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9, loc="lower right")
    rho0 = summary.loc[summary["rho"] == summary["rho"].min(), "H_mean"]
    rho1 = summary.loc[summary["rho"] == summary["rho"].max(), "H_mean"]
    if len(rho0) and len(rho1):
        ax.text(
            0.03,
            0.97,
            rf"$H_{{sort}}({summary['rho'].min():g}) \approx {float(rho0.iloc[0]):.3f}$"
            rf" $\to$ $H_{{sort}}({summary['rho'].max():g}) \approx {float(rho1.iloc[0]):.3f}$",
            transform=ax.transAxes,
            va="top",
            ha="left",
            fontsize=9,
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
        )
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _plot_rho_vs_global_wss(summary: pd.DataFrame, out_path: Path) -> None:
    """Homophily ρ vs global within-team sum of squares."""
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()

    n_rep = int(summary["n_realizations"].iloc[0]) if "n_realizations" in summary.columns else 30
    fig, ax = plt.subplots(figsize=(7.5, 5))
    x = summary["rho"].to_numpy()
    y = summary["global_wss_mean"].to_numpy()
    yerr = summary["global_wss_std"].fillna(0.0).to_numpy()
    ax.errorbar(
        x,
        y,
        yerr=yerr,
        fmt="o-",
        capsize=4,
        color="#2d6a4f",
        ecolor="#95b8a3",
        markersize=6,
        linewidth=1.5,
        label=rf"Mean $\mathrm{{global\_wss}}$ ± 1 SD ({n_rep} reps)",
    )
    if len(x) >= 2:
        coef = np.polyfit(x, y, 1)
        x_line = np.linspace(float(x.min()), float(x.max()), 100)
        ax.plot(x_line, np.polyval(coef, x_line), "--", color="#b03030", lw=1.2, alpha=0.85, label="OLS trend")
    ax.set_xlabel(r"Homophily knob $\rho$ (LG ASSIGN)", fontsize=11)
    ax.set_ylabel(r"Global within-team SS ($\mathrm{global\_wss}$)", fontsize=11)
    ax.set_title(
        r"Increase homophily $\rho$ $\Rightarrow$ decrease $\mathrm{global\_wss}$ (more sorting)",
        fontsize=12,
        pad=10,
    )
    ax.set_xlim(-0.02, 1.02)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9, loc="upper right")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _plot_dh(summary: pd.DataFrame, out_path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    x = summary["rho"].to_numpy()
    specs = (
        (axes[0], "D_mean", "D_std", r"Within-team MSE $D$"),
        (axes[1], "H_mean", "H_std", r"Sorting index $H$"),
    )
    for ax, col, ylab, title in specs:
        y = summary[col].to_numpy()
        yerr = summary[ylab].fillna(0.0).to_numpy()
        ax.errorbar(x, y, yerr=yerr, fmt="o-", capsize=3, color="#1a5490")
        ax.set_xlabel(r"Homophily $\rho$")
        ax.set_ylabel(title)
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
    fig.suptitle("LG ASSIGN — 2015 empirical PPM z · C=15 · ρ ∈ [0, 1]", fontsize=11)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _plot_centroid_sd(summary: pd.DataFrame, out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4))
    x = summary["rho"].to_numpy()
    y = summary["centroid_sd_mean"].to_numpy()
    yerr = summary["centroid_sd_std"].fillna(0.0).to_numpy()
    ax.errorbar(x, y, yerr=yerr, fmt="o-", capsize=3, color="#b03030")
    ax.set_xlabel(r"Homophily $\rho$")
    ax.set_ylabel(r"SD of final team centroids $\mu_j$")
    ax.set_title("Between-team centroid dispersion vs ρ")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _plot_examples(examples: list[dict], out_path: Path) -> None:
    if not examples:
        return
    fig, axes = plt.subplots(1, len(examples), figsize=(4 * len(examples), 3.5), sharey=True)
    if len(examples) == 1:
        axes = [axes]
    for ax, ex in zip(axes, examples):
        mu = np.asarray(ex["mu_final"], dtype=float)
        ax.hist(mu, bins=30, color="steelblue", edgecolor="white")
        ax.set_title(rf"$\rho={ex['rho']:g}$")
        ax.set_xlabel(r"Final $\mu_j$")
    axes[0].set_ylabel("Team count")
    fig.suptitle("Final team centroid distributions (rep 0)", fontsize=11)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="541 Grandchild ρ sweep")
    parser.add_argument("--season", type=int, default=2015)
    parser.add_argument("--realizations", type=int, default=30)
    parser.add_argument("--seed", type=int, default=5412015)
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Fewer ρ points and 8 realizations (smoke)",
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=5,
        metavar="N",
        help="Print progress every N reps per rho arm (0 = rho-arm summaries only)",
    )
    args = parser.parse_args()

    ensure_hero_dirs()
    OUT.mkdir(parents=True, exist_ok=True)

    gc, tpa = _load_modules()
    c = gc.ROSTER_SIZE_DEFAULT
    ability, emp_meta = gc.load_empirical_abilities_season(args.season, roster_size=c)
    n = len(ability)
    if n % c != 0:
        raise SystemExit(f"N={n} not divisible by C={c}")
    n_teams = n // c

    rho_values = [0.0, 0.5, 1.0] if args.quick else DEFAULT_RHO
    n_rep = 8 if args.quick else args.realizations

    print(f"541 sweep: season={args.season} N={n} J={n_teams} C={c} reps={n_rep}", flush=True)

    detail, summary, examples = _run_sweep(
        ability,
        c,
        rho_values,
        n_rep,
        args.seed,
        progress_every=max(0, int(args.progress_every)),
    )
    detail.to_csv(OUT / "GRANDCHILD_rho_sweep_detail.csv", index=False)
    summary.to_csv(CSV_SUM, index=False)

    print("\nWriting figures ...", flush=True)

    _plot_dh(summary, PNG_DH)
    _plot_rho_vs_assortativity(summary, PNG_RHO_H)
    _plot_rho_vs_global_wss(summary, PNG_RHO_WSS)
    _plot_centroid_sd(summary, PNG_SD)
    _plot_examples(examples, PNG_EX)

    meta = {
        "last_synced": date.today().isoformat(),
        "module": "541_grandchild_homophily_assign",
        "season": args.season,
        "empirical": emp_meta,
        "n_teams": n_teams,
        "roster_size": c,
        "n_realizations": n_rep,
        "rho_calibration_band": [0.0, 1.0],
        "rho_values": rho_values,
        "base_seed": args.seed,
        "outputs": {
            "summary_csv": str(CSV_SUM.relative_to(REPO)),
            "png_d_h": str(PNG_DH.relative_to(REPO)),
            "png_rho_vs_assortativity": str(PNG_RHO_H.relative_to(REPO)),
            "png_rho_vs_global_wss": str(PNG_RHO_WSS.relative_to(REPO)),
            "png_centroid_sd": str(PNG_SD.relative_to(REPO)),
            "png_examples": str(PNG_EX.relative_to(REPO)),
        },
        "interpretation_stub": (
            "D = within-team MSE (not assortativity). H = normalized sorting. "
            "Inspect curves for nonlinear saturation; do not assume monotonicity per realization."
        ),
    }
    META_JSON.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"Wrote {CSV_SUM}")
    print(f"Wrote {PNG_DH}")
    print(f"Wrote {PNG_RHO_H}")
    print(f"Wrote {PNG_RHO_WSS}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
