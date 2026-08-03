#!/usr/bin/env python3
"""Pass C — ρ assignment ablation (score + winner rule held fixed).

==============================================================================
FOR LATER CHARLES — read this block first
==============================================================================
What this file is
  One-shot script that draws ONE synthetic ability / team-target league, then
  re-assigns that same talent under different assignment rules (ρ low / mid /
  high / very-high soft match, plus sort-and-chop). Score and top-K stay FIXED:
      S_i = A_i − w·L_C  (crowding_smooth, w=0.55 @ 539 preset), then top K.
  Step 4 VISUALIZE: 16 quantile bins on **pool mean** (539 preset, same as Pass B).

Four steps
  (1) ASSIGN (varies by ρ arm)  (2) SCORE  (3) SELECT  (4) VISUALIZE

Story
  Pass B: congestion in SCORE bends the curve.
  Pass C: assortativity in ASSIGNMENT changes that curve once score is fixed —
  sorting shapes the roster environments we visualize.

Run (repo root)
  python sports/scripts/pass_c_rho_ablation_bundle.py

Outputs (only)
  3-Master_Plan/re_entry/HEROs_and_PASSes/PASS_C_*

Spec
  sports/540_READ_ME_SIM.md
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
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SCRIPTS))
from gallery_knobs import (
    HERO_BINS,
    HERO_SEED,
    PRESET,
    RHO_HIGH,
    RHO_LOW,
    RHO_MODERATE,
    RHO_VERY_HIGH,
)
OUT = REPO / "3-Master_Plan" / "re_entry" / "HEROs_and_PASSes"
PASS_C_PNG_NAME = "PASS_C_rho_ablation_selection_by_pool_mean.png"
BIN_AXIS = "pool_mean"
SHOW_SORT_CHOP_ON_FIGURE = False

ARMS: list[tuple[str, str, float | None]] = [
    ("rho_low", "soft", RHO_LOW),
    ("rho_moderate", "soft", RHO_MODERATE),
    ("rho_high", "soft", RHO_HIGH),
    ("rho_very_high", "soft", RHO_VERY_HIGH),
    ("sort_chop", "sort_chop", None),
]


def _load_cfg_module():
    import importlib.util

    cfg_path = SPORTS / "tier1_sim_config.py"
    spec = importlib.util.spec_from_file_location("tier1_sim_config", cfg_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _539_playground_state(mod) -> dict:
    return {
        "ability_draw": str(getattr(mod, "SELECTION_539_ABILITY_DRAW", "beta_2_2")),
        "target_dist": "uniform",
        "t_low": float(getattr(mod, "SELECTION_539_TARGET_MEAN_LOW", 0.0)),
        "t_high": float(getattr(mod, "SELECTION_539_TARGET_MEAN_HIGH", 1.0)),
        "viability_theta": float(getattr(mod, "SELECTION_539_VIABILITY_THETA", 0.72)),
        "viability_sharpness": float(
            getattr(mod, "SELECTION_539_VIABILITY_SHARPNESS", 10.0)
        ),
        "n_bins": HERO_BINS,
        "n_selected": int(getattr(mod, "N_SELECTED", 1500)),
        "winner_selection": str(getattr(mod, "SELECTION_539_WINNER_SELECTION", "C")),
    }


def _congestion_w(mod) -> float:
    return float(getattr(mod, "SELECTION_539_LOO_GAP_WEIGHT", 0.55))


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
    players, _, _ = tpa.simulate_generative_rosters(
        arm_params,
        rng=rng,
        method=method,
        ability=ability,
        team_targets=team_targets,
    )
    players = tpa.assign_selection(
        players,
        rng,
        n_selected=sel.n_selected,
        score_mode=sel.score_mode,
        loo_gap_weight=sel.loo_gap_weight,
        winner_selection=sel.winner_selection,
        pool_l_mode=sel.loo_pool_l_mode,
        viability_theta=arm_params.viability_theta,
        viability_sharpness=arm_params.viability_sharpness,
    )
    summ = tge.inverted_u_bin_table_team_mean(
        players, sel, assign_poolq_bin_labels=assign_poolq_bin_labels
    )
    out = summ.copy()
    out["arm"] = label
    out["method"] = method
    out["rho"] = np.nan if rho is None else float(rho)
    return out


def write_summary(out_dir: Path, frames: dict[str, pd.DataFrame], w: float) -> None:
    lines = [
        f"# Pass C — ρ assignment ablation ({date.today().isoformat()})",
        "",
        f"Preset: {PRESET}. ASSIGN (ρ) varies; SCORE + SELECT fixed.",
        f"$S_i = A_i − {w:g}·L_C$ (crowding_smooth).",
        f"Same $A_i$ / $T_j$ draw, seed={HERO_SEED}.",
        f"VISUALIZE: {HERO_BINS} quantile bins on pool mean (not poolq_loo).",
        "",
        "## Arms",
        "",
    ]
    for label, df in frames.items():
        top = float(df.loc[df["bin"] == df["bin"].max(), "selection_rate"].iloc[0])
        bot = float(df.loc[df["bin"] == df["bin"].min(), "selection_rate"].iloc[0])
        peak = float(df["selection_rate"].max())
        rho = df["rho"].iloc[0]
        method = df["method"].iloc[0]
        rho_s = "—" if np.isnan(rho) else f"{rho:g}"
        lines.append(
            f"- **{label}** ({method}, ρ={rho_s}): bin 1→{HERO_BINS} "
            f"rate {bot:.4f}→{top:.4f} (peak {peak:.4f})"
        )
    lines.extend(
        [
            "",
            "## Story",
            "",
            "- Pass B: congestion in SCORE bends the curve.",
            "- Pass C: assortativity changes that curve once score is fixed.",
            "",
            "## Limitation",
            "",
            "- Qualitative POC; not bin-for-bin match to Pass A (poolq_loo hero).",
            "- sort-and-chop is a separate hard-assortativity benchmark.",
        ]
    )
    (out_dir / "PASS_C_rho_ablation_summary.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def build_figure(
    out_dir: Path,
    frames: dict[str, pd.DataFrame],
    *,
    assignment_sigma: float,
    w: float,
) -> None:
    sys.path.insert(0, str(SCRIPTS))
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    fig = plt.figure(figsize=(9, 5.4))
    gs = fig.add_gridspec(2, 1, height_ratios=[4.2, 1], hspace=0.08)
    ax = fig.add_subplot(gs[0, 0])
    colors = {
        "rho_low": "steelblue",
        "rho_moderate": "seagreen",
        "rho_high": "darkorange",
        "rho_very_high": "purple",
        "sort_chop": "crimson",
    }
    labels = {
        "rho_low": rf"$\rho={RHO_LOW}$ (mixing)",
        "rho_moderate": rf"$\rho={RHO_MODERATE}$ (moderate)",
        "rho_high": rf"$\rho={RHO_HIGH}$ (assortative)",
        "rho_very_high": rf"$\rho={RHO_VERY_HIGH}$ (very high)",
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
    ax.set_xlabel(r"Bin ($1$ = lowest pool mean in sim)")
    ax.set_ylabel(r"Mean $Y_{\mathrm{selected}}$")
    title_extra = ""
    if not SHOW_SORT_CHOP_ON_FIGURE and "sort_chop" in frames:
        title_extra = "\n(sort-and-chop hidden on plot — CSV still saved)"
    ax.set_title(
        rf"Pass C — assignment ablation ({PRESET}, score + top-$K$ fixed)"
        "\n"
        rf"$S_i = A_i - {w:g}\,L_C$ | ${HERO_BINS}$ quantile on pool mean"
        + title_extra
    )
    ax.legend(loc="upper left", fontsize=8)
    ax.set_ylim(bottom=0)

    sigma = float(assignment_sigma)
    formula = (
        r"Soft assign (knob $\rho$): "
        r"$\pi_{ij}\propto\exp\!\left(-\rho\,(A_i-T_j)^2/(2\sigma^2)\right)$ "
        rf"with $\sigma={sigma:g}$ fixed. "
        rf"Score $S_i=A_i-{w:g}\,L_C$ held fixed; VISUALIZE on pool mean."
    )
    cap_ax = fig.add_subplot(gs[1, 0])
    cap_ax.axis("off")
    cap_ax.text(
        0.5,
        0.55,
        formula,
        ha="center",
        va="center",
        fontsize=8,
        transform=cap_ax.transAxes,
    )

    png = out_dir / PASS_C_PNG_NAME
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {png} (SHOW_SORT_CHOP_ON_FIGURE={SHOW_SORT_CHOP_ON_FIGURE})")


def main() -> None:
    out_dir = OUT
    out_dir.mkdir(parents=True, exist_ok=True)
    mod = _load_cfg_module()
    tge, tpa, assign_poolq_bin_labels = _load_modules()
    w = _congestion_w(mod)

    state = _539_playground_state(mod)
    base_params = tge.assignment_params_from_state(SPORTS, state, tpa=tpa)
    base_sel = tge.SelectionConfig.from_module(mod)
    sel = replace(
        base_sel,
        n_bins=HERO_BINS,
        bin_mode="quantile",
        n_selected=int(state.get("n_selected", base_sel.n_selected)),
        score_mode="loo_gap_plus_ability",
        loo_pool_l_mode="crowding_smooth",
        loo_gap_weight=w,
        winner_selection=str(state.get("winner_selection", base_sel.winner_selection)),
    )

    rng = np.random.default_rng(HERO_SEED)
    ability, team_targets = _draw_league_once(tpa, base_params, rng)

    meta = {
        "pass": "C",
        "preset": PRESET,
        "visualize_x_axis": BIN_AXIS,
        "hero_bins": HERO_BINS,
        "seed": HERO_SEED,
        "selection": {
            "score_mode": "loo_gap_plus_ability",
            "loo_pool_l_mode": "crowding_smooth",
            "w": w,
        },
        "assignment": {
            "ability_draw": base_params.ability_draw,
            "viability_theta": base_params.viability_theta,
            "viability_sharpness": base_params.viability_sharpness,
        },
        "arms": [{"label": a, "method": m, "rho": r} for a, m, r in ARMS],
        "assignment_sigma": base_params.assignment_sigma,
    }
    meta_path = out_dir / "PASS_C_rho_ablation_meta.json"

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
        csv_name = f"PASS_C_generative_{label}_16quantile_poolmean.csv"
        df.to_csv(out_dir / csv_name, index=False)
        print(f"  wrote {csv_name}")

    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    write_summary(out_dir, frames, w)
    build_figure(
        out_dir,
        frames,
        assignment_sigma=float(base_params.assignment_sigma),
        w=w,
    )

    caption = out_dir / "PASS_C_rho_ablation_caption.txt"
    caption.write_text(
        "\n".join(
            [
                "Pass C caption — ρ assignment ablation",
                "",
                f"Preset: {PRESET} (aligned with Pass B).",
                "Four steps: ASSIGN (ρ varies) → SCORE → SELECT → VISUALIZE (pool mean).",
                "",
                f"Score + winner rule fixed: S_i = A_i − {w:g}·L_C (crowding_smooth), top K.",
                "Only assignment differs across arms:",
                f"ρ = {RHO_LOW}, {RHO_MODERATE}, {RHO_HIGH}, {RHO_VERY_HIGH}, plus sort-and-chop.",
                "",
                "Story: assortativity in assignment changes the curve once score is fixed —",
                "sorting shapes the roster environments we visualize.",
                "",
                "Related: Pass A (empirical poolq_loo hero), Pass B (λ knockout).",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    readme = out_dir / "PASS_C_README.txt"
    readme.write_text(
        "\n".join(
            [
                "Pass C — ρ assignment ablation",
                "",
                "Generated by: sports/scripts/pass_c_rho_ablation_bundle.py",
                f"Preset: {PRESET}; VISUALIZE on pool mean.",
                "Home: 3-Master_Plan/re_entry/HEROs_and_PASSes/",
                "",
                "Related: PASS_A_* (empirical), PASS_B_* (λ knockout).",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"\nDone. Outputs in {out_dir}")


if __name__ == "__main__":
    main()
