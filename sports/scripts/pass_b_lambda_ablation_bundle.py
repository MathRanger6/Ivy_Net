#!/usr/bin/env python3
"""Pass B — λ score ablation (assignment + top-K held fixed).

One synthetic league draw + one soft assignment at fixed ρ; only SCORE changes:
  S_i = A_i − λ L_C  (λ = 0 → talent-only score S_i = A_i)
Step 4 VISUALIZE: 16 quantile bins on pool mean (539 preset, same as Pass C).

Run (repo root):
  python sports/scripts/pass_b_lambda_ablation_bundle.py

Outputs:
  3-Master_Plan/re_entry/HEROs_and_PASSes/PASS_B_lambda_ablation_*
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
    LAMBDA_FIXED_RHO,
    LAMBDA_HIGH,
    LAMBDA_LOW,
    LAMBDA_MODERATE,
    PASS_B_PNG_SUFFIX,
    PRESET,
)

OUT = REPO / "3-Master_Plan" / "re_entry" / "HEROs_and_PASSes"
PASS_B_PNG_NAME = f"PASS_B_lambda_ablation_selection_by_pool_mean{PASS_B_PNG_SUFFIX}.png"
BIN_AXIS = "pool_mean"

ARMS: list[tuple[str, float]] = [
    ("lambda_0", 0.0),
    ("lambda_low", LAMBDA_LOW),
    ("lambda_moderate", LAMBDA_MODERATE),
    ("lambda_high", LAMBDA_HIGH),
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


def _score_config(lam: float) -> tuple[str, str, float]:
    if lam <= 0.0:
        return "ability", "quality", 0.0
    return "loo_gap_plus_ability", "crowding_smooth", float(lam)


def run_one_arm(
    label: str,
    lam: float,
    *,
    players_base: pd.DataFrame,
    sel,
    params,
    rng,
    tge,
    tpa,
    assign_poolq_bin_labels,
) -> pd.DataFrame:
    score_mode, pool_l, w = _score_config(lam)
    sel_arm = replace(
        sel,
        score_mode=score_mode,
        loo_pool_l_mode=pool_l,
        loo_gap_weight=w,
    )
    players = tpa.assign_selection(
        players_base.copy(),
        rng,
        n_selected=sel_arm.n_selected,
        score_mode=sel_arm.score_mode,
        loo_gap_weight=sel_arm.loo_gap_weight,
        winner_selection=sel_arm.winner_selection,
        pool_l_mode=sel_arm.loo_pool_l_mode,
        viability_theta=params.viability_theta,
        viability_sharpness=params.viability_sharpness,
    )
    summ = tge.inverted_u_bin_table_team_mean(
        players, sel_arm, assign_poolq_bin_labels=assign_poolq_bin_labels
    )
    out = summ.copy()
    out["arm"] = label
    out["lambda"] = float(lam)
    return out


def write_summary(
    out_dir: Path,
    frames: dict[str, pd.DataFrame],
    *,
    fixed_rho: float,
) -> None:
    lines = [
        f"# Pass B — λ score ablation ({date.today().isoformat()})",
        "",
        f"Preset: {PRESET}. SCORE (λ) varies; ASSIGN + SELECT fixed.",
        rf"Fixed soft assign: $\rho={fixed_rho:g}$.",
        f"Same $A_i$ / $T_j$ draw + one roster, seed={HERO_SEED}.",
        f"VISUALIZE: {HERO_BINS} quantile bins on pool mean (not poolq_loo).",
        "",
        "## Arms",
        "",
    ]
    for label, df in frames.items():
        top = float(df.loc[df["bin"] == df["bin"].max(), "selection_rate"].iloc[0])
        bot = float(df.loc[df["bin"] == df["bin"].min(), "selection_rate"].iloc[0])
        peak = float(df["selection_rate"].max())
        lam = float(df["lambda"].iloc[0])
        lines.append(
            f"- **{label}** (λ={lam:g}): bin 1→{HERO_BINS} "
            f"rate {bot:.4f}→{top:.4f} (peak {peak:.4f})"
        )
    lines.extend(
        [
            "",
            "## Story",
            "",
            "- λ = 0: score is talent-only — curve stays roughly monotone on pool mean.",
            "- λ > 0: roster pressure in score bends the readout (congestion in SCORE).",
            "",
            "## Limitation",
            "",
            "- Qualitative POC; pool-mean axis (Pass B/C), not Pass A poolq_loo hero.",
        ]
    )
    (out_dir / "PASS_B_lambda_ablation_summary.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def build_figure(
    out_dir: Path,
    frames: dict[str, pd.DataFrame],
    *,
    fixed_rho: float,
    assignment_sigma: float,
) -> None:
    sys.path.insert(0, str(SCRIPTS))
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    fig = plt.figure(figsize=(9, 5.4))
    gs = fig.add_gridspec(2, 1, height_ratios=[4.2, 1], hspace=0.08)
    ax = fig.add_subplot(gs[0, 0])
    colors = {
        "lambda_0": "steelblue",
        "lambda_low": "seagreen",
        "lambda_moderate": "darkorange",
        "lambda_high": "purple",
    }
    labels = {
        "lambda_0": r"$\lambda=0$ (talent only)",
        "lambda_low": rf"$\lambda={LAMBDA_LOW:g}$",
        "lambda_moderate": rf"$\lambda={LAMBDA_MODERATE:g}$ (539 baseline)",
        "lambda_high": rf"$\lambda={LAMBDA_HIGH:g}$",
    }
    for key, df in frames.items():
        x = df["bin"].to_numpy(dtype=float) + 1
        y = df["selection_rate"].to_numpy(dtype=float)
        ax.plot(x, y, "o-", lw=2, ms=5, color=colors[key], label=labels[key])
    ax.set_xlabel(r"Bin ($1$ = lowest pool mean in sim)")
    ax.set_ylabel(r"Mean $Y_{\mathrm{selected}}$")
    ax.set_title(
        rf"Pass B — score ablation ({PRESET}, assign + top-$K$ fixed)"
        "\n"
        rf"$\rho={fixed_rho:g}$ fixed | ${HERO_BINS}$ quantile on pool mean"
    )
    ax.legend(loc="upper left", fontsize=8)
    ax.set_ylim(bottom=0)

    sigma = float(assignment_sigma)
    formula = (
        r"Score (knob $\lambda$): $S_i=A_i-\lambda\,L_C$ "
        rf"(fixed soft assign $\rho={fixed_rho:g}$, $\sigma={sigma:g}$). "
        r"VISUALIZE on pool mean."
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

    png = out_dir / PASS_B_PNG_NAME
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {png}")


def main() -> None:
    out_dir = OUT
    out_dir.mkdir(parents=True, exist_ok=True)
    mod = _load_cfg_module()
    tge, tpa, assign_poolq_bin_labels = _load_modules()

    state = _539_playground_state(mod)
    base_params = tge.assignment_params_from_state(SPORTS, state, tpa=tpa)
    params = replace(base_params, assignment_rho=float(LAMBDA_FIXED_RHO))
    base_sel = tge.SelectionConfig.from_module(mod)
    sel = replace(
        base_sel,
        n_bins=HERO_BINS,
        bin_mode="quantile",
        n_selected=int(state.get("n_selected", base_sel.n_selected)),
        winner_selection=str(state.get("winner_selection", base_sel.winner_selection)),
    )

    rng = np.random.default_rng(HERO_SEED)
    ability, team_targets = _draw_league_once(tpa, params, rng)
    players_base, _, _ = tpa.simulate_generative_rosters(
        params,
        rng=rng,
        method="soft",
        ability=ability,
        team_targets=team_targets,
    )

    meta = {
        "pass": "B_lambda_ablation",
        "preset": PRESET,
        "visualize_x_axis": BIN_AXIS,
        "hero_bins": HERO_BINS,
        "seed": HERO_SEED,
        "assignment": {
            "method": "soft",
            "rho_fixed": float(LAMBDA_FIXED_RHO),
            "assignment_sigma": float(params.assignment_sigma),
            "ability_draw": params.ability_draw,
            "viability_theta": params.viability_theta,
            "viability_sharpness": params.viability_sharpness,
        },
        "selection": {
            "winner_selection": sel.winner_selection,
            "n_selected": sel.n_selected,
        },
        "arms": [{"label": a, "lambda": lam} for a, lam in ARMS],
    }
    meta_path = out_dir / "PASS_B_lambda_ablation_meta.json"

    frames: dict[str, pd.DataFrame] = {}
    for label, lam in ARMS:
        print(f"Running arm: {label} (λ={lam:g}) ...")
        df = run_one_arm(
            label,
            lam,
            players_base=players_base,
            sel=sel,
            params=params,
            rng=np.random.default_rng(HERO_SEED + len(label) + int(lam * 100)),
            tge=tge,
            tpa=tpa,
            assign_poolq_bin_labels=assign_poolq_bin_labels,
        )
        frames[label] = df
        csv_name = f"PASS_B_generative_{label}_16quantile_poolmean.csv"
        df.to_csv(out_dir / csv_name, index=False)
        print(f"  wrote {csv_name}")

    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    write_summary(out_dir, frames, fixed_rho=float(LAMBDA_FIXED_RHO))
    build_figure(
        out_dir,
        frames,
        fixed_rho=float(LAMBDA_FIXED_RHO),
        assignment_sigma=float(params.assignment_sigma),
    )

    caption = out_dir / "PASS_B_lambda_ablation_caption.txt"
    caption.write_text(
        "\n".join(
            [
                "Pass B caption — λ score ablation (characterization)",
                "",
                f"Preset: {PRESET}. One roster draw; ASSIGN (ρ) + SELECT (top-K) fixed.",
                f"Fixed ρ = {LAMBDA_FIXED_RHO:g}. Only λ in S_i = A_i − λ L_C varies.",
                "",
                f"Arms: λ = 0, {LAMBDA_LOW:g}, {LAMBDA_MODERATE:g}, {LAMBDA_HIGH:g}.",
                "VISUALIZE: pool mean (16 quantile bins).",
                "",
                "Story: roster pressure in score bends the curve; λ = 0 is talent-only baseline.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"\nDone. Outputs in {out_dir}")


if __name__ == "__main__":
    main()
