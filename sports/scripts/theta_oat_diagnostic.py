#!/usr/bin/env python3
"""θ OAT at K/N=10% — full bin curves after θ×K/N panel.

Fixed: soft ρ=8, λ=0.55, γ=10, N=5600, K=560, seed=42.
Varies: θ ∈ {0.50, 0.72, 0.90} (viability cutline in L_C).

Run (repo root):
  python sports/scripts/theta_oat_diagnostic.py

Outputs:
  HEROs_and_PASSes/theta/THETA_OAT_selection_by_pool_mean.png
  HEROs_and_PASSes/theta/THETA_OAT_summary.csv
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
    HERO_N_SELECTED,
    HERO_N_TEAMS,
    HERO_ROSTER_SIZE,
    HERO_SEED,
    LAMBDA_FIXED_RHO,
    LAMBDA_MODERATE,
    PRESET,
    league_scale_title_line,
)
from hero_gallery_paths import THETA, ensure_hero_dirs

OUT = THETA
PNG = OUT / "THETA_OAT_selection_by_pool_mean.png"
CSV = OUT / "THETA_OAT_summary.csv"

THETA_ARMS: list[tuple[str, float]] = [
    ("theta_050", 0.50),
    ("theta_072", 0.72),
    ("theta_090", 0.90),
]
ARM_STYLES = {
    "theta_050": ("#2ca02c", r"$\theta=0.50$"),
    "theta_072": ("#1f77b4", r"$\theta=0.72$ (539 default)"),
    "theta_090": ("#d62728", r"$\theta=0.90$"),
}


def _load_cfg_module():
    import importlib.util

    cfg_path = SPORTS / "tier1_sim_config.py"
    spec = importlib.util.spec_from_file_location("tier1_sim_config", cfg_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


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


def _539_state(mod) -> dict:
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
        "n_teams": HERO_N_TEAMS,
        "roster_size": HERO_ROSTER_SIZE,
        "n_selected": HERO_N_SELECTED,
        "winner_selection": str(getattr(mod, "SELECTION_539_WINNER_SELECTION", "C")),
    }


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


def run_arm(
    label: str,
    theta: float,
    *,
    players_base: pd.DataFrame,
    sel,
    params,
    tge,
    tpa,
    assign_poolq_bin_labels,
) -> pd.DataFrame:
    players = tpa.assign_selection(
        players_base.copy(),
        np.random.default_rng(HERO_SEED + int(theta * 1000)),
        n_selected=sel.n_selected,
        score_mode="loo_gap_plus_ability",
        loo_gap_weight=LAMBDA_MODERATE,
        winner_selection=sel.winner_selection,
        pool_l_mode="crowding_smooth",
        viability_theta=theta,
        viability_sharpness=params.viability_sharpness,
    )
    sel_arm = replace(sel, loo_gap_weight=LAMBDA_MODERATE)
    summ = tge.inverted_u_bin_table_team_mean(
        players, sel_arm, assign_poolq_bin_labels=assign_poolq_bin_labels
    )
    out = summ.copy()
    out["arm"] = label
    out["theta"] = float(theta)
    return out


def build_figure(frames: dict[str, pd.DataFrame]) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    fig, ax = plt.subplots(figsize=(9, 5.2))
    for label, df in frames.items():
        color, leg = ARM_STYLES[label]
        x = df["bin"].to_numpy(dtype=float) + 1
        y = df["selection_rate"].to_numpy(dtype=float)
        ax.plot(x, y, "o-", lw=2.2, ms=6, color=color, label=leg)
    ax.set_xlabel("Pool-mean bin (1 = lowest)")
    ax.set_ylabel("Selection rate")
    ax.set_title(
        rf"$\theta$ OAT at $K/N=0.10$ ({PRESET}) — soft $\rho={LAMBDA_FIXED_RHO:g}$, "
        rf"$\lambda={LAMBDA_MODERATE:g}$, $\gamma=10$"
        "\n"
        rf"{league_scale_title_line()} | {HERO_BINS} bins | seed={HERO_SEED}"
    )
    ax.legend(loc="upper left", fontsize=9)
    ax.set_ylim(bottom=0)
    fig.tight_layout()
    fig.savefig(PNG, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {PNG}")


def main() -> None:
    ensure_hero_dirs()
    mod = _load_cfg_module()
    tge, tpa, assign_poolq_bin_labels = _load_modules()

    state = _539_state(mod)
    base_params = tge.assignment_params_from_state(SPORTS, state, tpa=tpa)
    params = replace(base_params, assignment_rho=float(LAMBDA_FIXED_RHO))
    base_sel = tge.SelectionConfig.from_module(mod)
    sel = replace(
        base_sel,
        n_bins=HERO_BINS,
        bin_mode="quantile",
        n_selected=HERO_N_SELECTED,
        score_mode="loo_gap_plus_ability",
        loo_pool_l_mode="crowding_smooth",
        loo_gap_weight=LAMBDA_MODERATE,
        winner_selection=str(state["winner_selection"]),
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

    frames: dict[str, pd.DataFrame] = {}
    summary_rows: list[dict] = []
    for label, theta in THETA_ARMS:
        print(f"Running θ={theta:g} ...")
        df = run_arm(
            label,
            theta,
            players_base=players_base,
            sel=sel,
            params=params,
            tge=tge,
            tpa=tpa,
            assign_poolq_bin_labels=assign_poolq_bin_labels,
        )
        frames[label] = df
        peak_idx = int(df["selection_rate"].idxmax())
        summary_rows.append(
            {
                "arm": label,
                "theta": theta,
                "peak_bin": int(df.loc[peak_idx, "bin"]) + 1,
                "peak_rate": float(df["selection_rate"].max()),
                "top_bin_rate": float(
                    df.loc[df["bin"] == df["bin"].max(), "selection_rate"].iloc[0]
                ),
                "bottom_bin_rate": float(
                    df.loc[df["bin"] == df["bin"].min(), "selection_rate"].iloc[0]
                ),
                "monotone_increasing": int(
                    np.all(
                        df.sort_values("bin")["selection_rate"].to_numpy()[:-1]
                        <= df.sort_values("bin")["selection_rate"].to_numpy()[1:] + 1e-9
                    )
                ),
            }
        )

    pd.DataFrame(summary_rows).to_csv(CSV, index=False)
    print(f"Wrote {CSV}")

    meta = {
        "diagnostic": "theta_oat",
        "date": date.today().isoformat(),
        "preset": PRESET,
        "seed": HERO_SEED,
        "k_over_n": HERO_N_SELECTED / (HERO_N_TEAMS * HERO_ROSTER_SIZE),
        "fixed": {
            "rho": LAMBDA_FIXED_RHO,
            "lambda_weight": LAMBDA_MODERATE,
            "gamma": params.viability_sharpness,
        },
        "theta_arms": [{"label": a, "theta": t} for a, t in THETA_ARMS],
    }
    (OUT / "THETA_OAT_meta.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )
    build_figure(frames)
    print("Done.")


if __name__ == "__main__":
    main()
