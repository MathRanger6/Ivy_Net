#!/usr/bin/env python3
"""Pass B — ρ assignment ablation with selection held fixed.

Same synthetic A_i draw across arms; vary assignment only (ρ low, ρ high, sort-and-chop).
Selection fixed: S_i = A_i − w·L_C (crowding_smooth, w=0.5).

Writes to sports/datasets/mbb/exports_inverted_u_v0/alex_rho_ablation_v0/
Run from repo root: python sports/scripts/540_rho_ablation_bundle.py
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
OUT = SPORTS / "datasets/mbb/exports_inverted_u_v0/alex_rho_ablation_v0"
HERO_BINS = 16
HERO_SEED = 42
RHO_LOW = 0.1
RHO_HIGH = 8.0
RHO_MODERATE = 1.0

ARMS: list[tuple[str, str, float | None]] = [
    ("rho_low", "soft", RHO_LOW),
    ("rho_moderate", "soft", RHO_MODERATE),
    ("rho_high", "soft", RHO_HIGH),
    ("sort_chop", "sort_chop", None),
]


def _load_modules():
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
    (out_dir / "rho_ablation_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_figure(out_dir: Path, frames: dict[str, pd.DataFrame]) -> None:
    fig, ax = plt.subplots(figsize=(9, 4.5))
    colors = {
        "rho_low": "steelblue",
        "rho_moderate": "seagreen",
        "rho_high": "darkorange",
        "sort_chop": "crimson",
    }
    labels = {
        "rho_low": f"ρ={RHO_LOW} (mixing)",
        "rho_moderate": f"ρ={RHO_MODERATE} (moderate)",
        "rho_high": f"ρ={RHO_HIGH} (assortative)",
        "sort_chop": "sort-and-chop (benchmark)",
    }
    for key, df in frames.items():
        x = df["bin"].to_numpy(dtype=float) + 1
        y = df["selection_rate"].to_numpy(dtype=float)
        ax.plot(x, y, "o-", lw=2, ms=5, color=colors[key], label=labels[key])
    ax.set_xlabel("Bin (1 = lowest poolq_loo in sim)")
    ax.set_ylabel("Mean Y_selected")
    ax.set_title(
        "Pass B — assignment ablation (selection fixed)\n"
        "S_i = A_i − 0.5·L_C | 16 quantile on poolq_loo"
    )
    ax.legend(loc="best", fontsize=8)
    ax.set_ylim(bottom=0)
    fig.tight_layout()
    png = out_dir / "rho_ablation_selection_by_poolq_loo.png"
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {png}")


def main() -> None:
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
    meta_path = out_dir / "rho_ablation_meta.json"

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
        csv_name = f"generative_{label}_16quantile.csv"
        df.to_csv(out_dir / csv_name, index=False)
        print(f"  wrote {csv_name}")

    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    write_summary(out_dir, frames)
    build_figure(out_dir, frames)

    caption = out_dir / "rho_ablation_caption.txt"
    caption.write_text(
        "\n".join(
            [
                "Alex Pass B caption (ρ assignment ablation)",
                "",
                "Same synthetic player abilities across arms; selection rule fixed",
                "(S_i = A_i − 0.5·L_C, smooth viable-peer congestion). Only assignment differs:",
                f"low ρ={RHO_LOW}, moderate ρ={RHO_MODERATE}, high ρ={RHO_HIGH}, and",
                "sort-and-chop benchmark (537-style max partition assortativity).",
                "",
                "Y-axis: mean selection rate by 16 quantile bins on simulated poolq_loo.",
                "",
                "Limitation: we show whether roster-formation sorting moves the readout when",
                "congestion-in-selection is held fixed; we do not claim bin-for-bin hero match.",
                "",
                "Pass A (λ knockout) is in ../alex_side_by_side_v0/.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    readme = out_dir / "README.txt"
    readme.write_text(
        "\n".join(
            [
                "alex_rho_ablation_v0 — Pass B (ρ assignment ablation)",
                "",
                "Generated by: sports/scripts/540_rho_ablation_bundle.py",
                "Spec: sports/540_READ_ME_SIM.md",
                "",
                "Related: ../alex_side_by_side_v0/ (Pass A — λ knockout)",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"\nDone. Outputs in {out_dir}")


if __name__ == "__main__":
    main()
