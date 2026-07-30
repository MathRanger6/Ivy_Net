#!/usr/bin/env python3
"""Pass B — ρ assignment ablation (score + winner rule held fixed).

==============================================================================
FOR LATER CHARLES — read this block first
==============================================================================
What this file is
  One-shot script that draws ONE synthetic ability / team-target league, then
  re-assigns that same talent under different assignment rules (ρ low / mid /
  high / very-high soft match, plus sort-and-chop). Score and top-K stay FIXED:
      S_i = A_i − 0.5·L_C  (crowding_smooth), then select top K.

What this file is NOT
  - Not Pass A (λ knockout) — see hero_model_reset_bundle.py.
  - Not proof that NBA uses ρ; not bin-for-bin hero match.
  - Not the 538 CELL 10 widget — tier1_cell10_playground_run.py is LEGACY.

Why Pass B exists
  Pass A asks: does congestion in the SCORE matter?
  Pass B asks: does ASSIGNMENT assortativity move the readout when score+K fixed?

ρ (assortativity)
  Soft kernel: π_ij ∝ exp(−ρ · (A_i−T_j)² / (2σ²)); σ fixed (~0.65).
  ρ=0 → max mixing; ρ↑ → sharper match to T_j.
  sort-and-chop = separate hard benchmark (NOT ρ→∞).
  Plot tip: set SHOW_SORT_CHOP_ON_FIGURE = False to hide the red spike so soft-ρ
  curves fill the y-axis (CSV for sort_chop is still written).

Run (repo root)
  python sports/scripts/540_rho_ablation_bundle.py

Outputs (only)
  3-Master_Plan/re_entry/HEROs_and_PASSes/PASS_B_*

Spec
  sports/540_READ_ME_SIM.md
  3-Master_Plan/re_entry/CHARLES_CHECKLIST.md  (§4)
==============================================================================
"""

from __future__ import annotations

import json
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SPORTS = REPO / "sports"
# Single home for Pass A / Pass B / hero gallery artifacts (no duplicate export folder).
OUT = REPO / "3-Master_Plan" / "re_entry" / "HEROs_and_PASSes"
PASS_B_PNG_NAME = "PASS_B_rho_ablation_selection_by_poolq_loo.png"
HERO_BINS = 16
HERO_SEED = 42
# Soft-assignment assortativity ladder (σ fixed ~0.65 in config).
# Larger ρ → sharper match of A_i to team target T_j. Still soft — not sort-and-chop.
RHO_LOW = 0.1
RHO_MODERATE = 1.0
RHO_HIGH = 8.0
RHO_VERY_HIGH = 32.0  # near-hard soft assortativity; still ≠ sort_chop

# Plot knob: sort-and-chop spikes (~0.9) squash the soft-ρ curves (often <0.3).
# False → omit that line from the PNG so the y-axis can rescale to the ρ arms.
# The sort_chop arm is still RUN and written to CSV either way (science artifact).
# Set True when you want the crimson benchmark on the same axes again.
SHOW_SORT_CHOP_ON_FIGURE = False

# (export_label, assignment_method, rho_or_None)
# soft → soft_assign with assignment_rho; sort_chop → disjoint slices benchmark
ARMS: list[tuple[str, str, float | None]] = [
    ("rho_low", "soft", RHO_LOW),
    ("rho_moderate", "soft", RHO_MODERATE),
    ("rho_high", "soft", RHO_HIGH),
    ("rho_very_high", "soft", RHO_VERY_HIGH),
    ("sort_chop", "sort_chop", None),
]


def _load_modules():
    """Import engines fresh (avoids stale tier1_* if config was edited mid-session)."""
    for mod_name in list(sys.modules):
        if mod_name.startswith("tier1_"):
            del sys.modules[mod_name]
    sys.path.insert(0, str(SPORTS))
    sys.path.insert(0, str(REPO))
    import tier1_generative_eda as tge
    import tier1_pool_assignment as tpa
    from sports_pipeline.panel_build import assign_poolq_bin_labels

    return tge, tpa, assign_poolq_bin_labels


def _draw_league_once(tpa, params, rng):
    """Shared A_i and T_j across all arms — only assignment method/ρ changes later."""
    ability = tpa.draw_abilities(
        rng,
        params.n_individuals,
        ability_draw=params.ability_draw,
        ability_mean=params.ability_mean,
        ability_sd=params.ability_sd,
        ability_clip_low=params.ability_clip_low,
        ability_clip_high=params.ability_clip_high,
        ability_student_t_df=params.ability_student_t_df,
        ability_student_t_scale=params.ability_student_t_scale,
    )
    team_targets = tpa.draw_target_means(
        rng,
        params.n_teams,
        target_mean_dist=params.target_mean_dist,
        target_mean_low=params.target_mean_low,
        target_mean_high=params.target_mean_high,
        target_mean_mu=params.target_mean_mu,
        target_mean_sigma=params.target_mean_sigma,
    )
    return ability, team_targets


def run_one_arm(
    label: str,
    method: str,
    rho: float | None,
    *,
    params,
    sel,
    ability,
    team_targets,
    rng,
    tge,
    tpa,
    assign_poolq_bin_labels,
) -> pd.DataFrame:
    """Assign (this arm) → score/select (fixed sel) → 16-bin table on poolq_loo."""
    if method == "soft":
        arm_params = replace(params, assignment_rho=float(rho))
    else:
        arm_params = params
    _, summ, _ = tge.run_inverted_u_pipeline(
        arm_params,
        sel,
        rng,
        tpa=tpa,
        assign_poolq_bin_labels=assign_poolq_bin_labels,
        method=method,
        ability=ability,
        team_targets=team_targets,
    )
    out = summ.copy()
    out["arm"] = label
    out["method"] = method
    out["rho"] = np.nan if rho is None else float(rho)
    return out


def write_summary(out_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    """Plain-text arm comparison for Alex / checklist proof."""
    lines = [
        f"# ρ assignment ablation ({date.today().isoformat()})",
        "",
        "Pass B: assignment varies; selection fixed (S_i = A_i − 0.5·L_C, crowding_smooth).",
        f"Same A_i / T_j draw, seed={HERO_SEED}. Bins: {HERO_BINS} quantile on poolq_loo.",
        "",
        "## Arms",
        "",
    ]
    for label, df in frames.items():
        top = float(df.loc[df["bin"] == df["bin"].max(), "selection_rate"].iloc[0])
        bot = float(df.loc[df["bin"] == df["bin"].min(), "selection_rate"].iloc[0])
        rho = df["rho"].iloc[0]
        method = df["method"].iloc[0]
        rho_s = "—" if np.isnan(rho) else f"{rho:g}"
        lines.append(
            f"- **{label}** ({method}, ρ={rho_s}): bin 1→{HERO_BINS} rate {bot:.4f}→{top:.4f}"
        )
    lines.extend(
        [
            "",
            "## Limitation",
            "",
            "- Does not claim bin-for-bin hero match.",
            "- sort-and-chop is a separate benchmark (537-style max partition assortativity).",
            "- ρ=0 would be uniform mixing; not run here (see 540_READ_ME_SIM.md).",
        ]
    )
    (out_dir / "PASS_B_rho_ablation_summary.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def build_figure(
    out_dir: Path,
    frames: dict[str, pd.DataFrame],
    *,
    assignment_sigma: float,
) -> None:
    """Overlay selection-rate curves for each assignment arm.

    Honors SHOW_SORT_CHOP_ON_FIGURE: when False, drop the sort_chop series so the
    soft-ρ curves are not crushed against the bottom of a 0–1 y-axis.

    assignment_sigma: σ in the soft kernel (fixed across arms; ρ is what varies).
    """
    fig, ax = plt.subplots(figsize=(9, 4.8))
    colors = {
        "rho_low": "steelblue",
        "rho_moderate": "seagreen",
        "rho_high": "darkorange",
        "rho_very_high": "purple",
        "sort_chop": "crimson",
    }
    labels = {
        "rho_low": f"ρ={RHO_LOW} (mixing)",
        "rho_moderate": f"ρ={RHO_MODERATE} (moderate)",
        "rho_high": f"ρ={RHO_HIGH} (assortative)",
        "rho_very_high": f"ρ={RHO_VERY_HIGH} (very high)",
        "sort_chop": "sort-and-chop (benchmark)",
    }
    plot_frames = {
        k: v
        for k, v in frames.items()
        if SHOW_SORT_CHOP_ON_FIGURE or k != "sort_chop"
    }
    for key, df in plot_frames.items():
        x = df["bin"].to_numpy(dtype=float) + 1
        y = df["selection_rate"].to_numpy(dtype=float)
        ax.plot(x, y, "o-", lw=2, ms=5, color=colors[key], label=labels[key])
    ax.set_xlabel("Bin (1 = lowest poolq_loo in sim)")
    ax.set_ylabel("Mean Y_selected")
    title_extra = ""
    if not SHOW_SORT_CHOP_ON_FIGURE and "sort_chop" in frames:
        title_extra = "\n(sort-and-chop hidden on plot — CSV still saved)"
    ax.set_title(
        "Pass B — assignment ablation (score + top-K fixed)\n"
        "S_i = A_i − 0.5·L_C | 16 quantile on poolq_loo"
        + title_extra
    )
    ax.legend(loc="best", fontsize=8)
    ax.set_ylim(bottom=0)

    # Soft-assignment kernel: ρ is the Pass B knob; σ is held fixed.
    sigma = float(assignment_sigma)
    formula = (
        r"Soft assign (Pass B knob $=\rho$):"
        "\n"
        r"$\pi_{ij}\propto\exp\!\left(-\rho\cdot"
        r"\dfrac{(A_i-T_j)^2}{2\sigma^2}\right)$"
        "\n"
        rf"$\rho\uparrow$ $\Rightarrow$ sharper match to $T_j$;  "
        rf"$\rho=0$ $\Rightarrow$ flat among open seats"
        "\n"
        rf"$\sigma$ fixed $={sigma:g}$ (ability units);  "
        r"score $S_i=A_i-0.5\,L_C$ held fixed"
    )
    ax.text(
        0.02,
        0.98,
        formula,
        transform=ax.transAxes,
        fontsize=8,
        va="top",
        ha="left",
        family="sans-serif",
        bbox={
            "boxstyle": "round,pad=0.35",
            "facecolor": "white",
            "edgecolor": "0.6",
            "alpha": 0.92,
        },
    )

    fig.tight_layout()
    # Prefixed name so Pass B figures are obvious next to HERO_ / PASS_A_ PNGs.
    png = out_dir / PASS_B_PNG_NAME
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {png} (SHOW_SORT_CHOP_ON_FIGURE={SHOW_SORT_CHOP_ON_FIGURE})")


def main() -> None:
    """Shared A/T draw → five assignment arms → CSVs, summary, PNG, captions."""
    out_dir = OUT
    out_dir.mkdir(parents=True, exist_ok=True)
    tge, tpa, assign_poolq_bin_labels = _load_modules()

    import importlib.util

    cfg_path = SPORTS / "tier1_sim_config.py"
    spec = importlib.util.spec_from_file_location("tier1_sim_config", cfg_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)

    base_params = tpa.AssignmentParams.from_tier1_sim_config(cfg_path)
    base_sel = tge.SelectionConfig.from_module(mod)
    # FIXED across arms: congestion-in-score + weight + binning (Pass A–style score)
    sel = replace(
        base_sel,
        n_bins=HERO_BINS,
        bin_mode="quantile",
        score_mode="loo_gap_plus_ability",
        loo_pool_l_mode="crowding_smooth",
        loo_gap_weight=0.5,
    )

    rng = np.random.default_rng(HERO_SEED)
    ability, team_targets = _draw_league_once(tpa, base_params, rng)

    meta = {
        "pass": "B",
        "hero_bins": HERO_BINS,
        "seed": HERO_SEED,
        "selection": {
            "score_mode": "loo_gap_plus_ability",
            "loo_pool_l_mode": "crowding_smooth",
            "w": 0.5,
        },
        "arms": [
            {"label": a, "method": m, "rho": r} for a, m, r in ARMS
        ],
        "assignment_sigma": base_params.assignment_sigma,
    }
    meta_path = out_dir / "PASS_B_rho_ablation_meta.json"

    frames: dict[str, pd.DataFrame] = {}
    for label, method, rho in ARMS:
        print(f"Running arm: {label} ...")
        df = run_one_arm(
            label,
            method,
            rho,
            params=base_params,
            sel=sel,
            ability=ability,
            team_targets=team_targets,
            rng=np.random.default_rng(HERO_SEED + len(label) + int((rho or 0) * 100)),
            tge=tge,
            tpa=tpa,
            assign_poolq_bin_labels=assign_poolq_bin_labels,
        )
        frames[label] = df
        csv_name = f"PASS_B_generative_{label}_16quantile.csv"
        df.to_csv(out_dir / csv_name, index=False)
        print(f"  wrote {csv_name}")

    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    write_summary(out_dir, frames)
    build_figure(
        out_dir,
        frames,
        assignment_sigma=float(base_params.assignment_sigma),
    )

    caption = out_dir / "PASS_B_rho_ablation_caption.txt"
    caption.write_text(
        "\n".join(
            [
                "Alex Pass B caption (ρ assignment ablation)",
                "",
                "Same synthetic player abilities across arms; score + winner rule fixed",
                "(S_i = A_i − 0.5·L_C, smooth viable-peer congestion, then top K).",
                "Only assignment differs:",
                f"low ρ={RHO_LOW}, moderate ρ={RHO_MODERATE}, high ρ={RHO_HIGH},",
                f"very high ρ={RHO_VERY_HIGH}, and",
                "sort-and-chop benchmark (537-style max partition assortativity).",
                "",
                "Y-axis: mean selection rate by 16 quantile bins on simulated poolq_loo.",
                "",
                "Limitation: we show whether roster-formation sorting moves the readout when",
                "congestion-in-score is held fixed; we do not claim bin-for-bin hero match.",
                "",
                "Pass A (λ knockout): PASS_A_* files in this same HEROs_and_PASSes folder.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    readme = out_dir / "PASS_B_README.txt"
    readme.write_text(
        "\n".join(
            [
                "Pass B — ρ assignment ablation",
                "",
                "Generated by: sports/scripts/540_rho_ablation_bundle.py",
                "Home: 3-Master_Plan/re_entry/HEROs_and_PASSes/",
                "Spec: sports/540_READ_ME_SIM.md",
                "",
                "Related: PASS_A_* in this folder (λ knockout).",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"\nDone. Outputs in {out_dir}")


if __name__ == "__main__":
    main()
