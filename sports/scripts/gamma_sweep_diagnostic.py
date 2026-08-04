#!/usr/bin/env python3
"""γ sweep on sort-and-chop — λ_crit ≈ 4/γ threshold shifts with sigmoid slope.

Same sort-and-chop rosters per γ; only viability_sharpness (γ) and λ vary.
Grid: γ ∈ {5, 10, 20}; λ ∈ {0, 0.25, 0.55, 0.75, 1.0}.

Run (repo root):
  python sports/scripts/gamma_sweep_diagnostic.py

Outputs:
  HEROs_and_PASSes/sort_chop_lambda/GAMMA_sweep_lambda_curves.png
  HEROs_and_PASSes/sort_chop_lambda/GAMMA_sweep_summary.csv
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
    PRESET,
    league_scale_title_line,
)
from hero_gallery_paths import SORT_CHOP_LAMBDA, ensure_hero_dirs

OUT = SORT_CHOP_LAMBDA
PNG = OUT / "GAMMA_sweep_lambda_curves.png"
CSV = OUT / "GAMMA_sweep_summary.csv"

GAMMA_GRID = (5.0, 10.0, 20.0)
LAMBDA_ARMS = [
    ("lambda_0", 0.0),
    ("lambda_025", 0.25),
    ("lambda_055", 0.55),
    ("lambda_075", 0.75),
    ("lambda_1", 1.0),
]
LAM_COLORS = {
    0.0: "#1f77b4",
    0.25: "#2ca02c",
    0.55: "#ff7f0e",
    0.75: "#d62728",
    1.0: "#9467bd",
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


def _score_config(lam: float) -> tuple[str, str, float]:
    if lam <= 0.0:
        return "ability", "quality", 0.0
    return "loo_gap_plus_ability", "crowding_smooth", float(lam)


def run_arm(
    lam: float,
    *,
    players_base: pd.DataFrame,
    sel,
    params,
    gamma: float,
    tge,
    tpa,
    assign_poolq_bin_labels,
) -> pd.DataFrame:
    score_mode, pool_l, w = _score_config(lam)
    players = tpa.assign_selection(
        players_base.copy(),
        np.random.default_rng(HERO_SEED + int(gamma * 10) + int(lam * 100)),
        n_selected=sel.n_selected,
        score_mode=score_mode,
        loo_gap_weight=w,
        winner_selection=sel.winner_selection,
        pool_l_mode=pool_l,
        viability_theta=params.viability_theta,
        viability_sharpness=gamma,
    )
    sel_arm = replace(
        sel,
        score_mode=score_mode,
        loo_pool_l_mode=pool_l,
        loo_gap_weight=w,
    )
    summ = tge.inverted_u_bin_table_team_mean(
        players, sel_arm, assign_poolq_bin_labels=assign_poolq_bin_labels
    )
    out = summ.copy()
    out["lambda"] = float(lam)
    out["gamma"] = float(gamma)
    return out


def build_figure(all_frames: dict[float, dict[str, pd.DataFrame]]) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.8), sharey=True)
    for ax, gamma in zip(axes, GAMMA_GRID):
        frames = all_frames[gamma]
        for label, lam in LAMBDA_ARMS:
            df = frames[label]
            x = df["bin"].to_numpy(dtype=float) + 1
            y = df["selection_rate"].to_numpy(dtype=float)
            ax.plot(
                x,
                y,
                "o-",
                lw=1.8,
                ms=4,
                color=LAM_COLORS[lam],
                label=rf"$\lambda={lam:g}$",
            )
        crit = 4.0 / gamma
        ax.axvline(x=0, color="none")  # spacer
        ax.set_title(rf"$\gamma={gamma:g}$  ($\lambda_{{\mathrm{{crit}}}}\approx{crit:.2f}$)")
        ax.set_xlabel("Pool-mean bin")
        ax.set_ylim(bottom=0)
    axes[0].set_ylabel("Selection rate")
    fig.suptitle(
        rf"Sort-and-chop: λ sweep at three $\gamma$ ({PRESET})"
        "\n"
        rf"{league_scale_title_line()} | {HERO_BINS} bins | seed={HERO_SEED}",
        fontsize=11,
    )
    axes[-1].legend(loc="upper left", fontsize=7)
    fig.tight_layout()
    fig.savefig(PNG, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {PNG}")


def main() -> None:
    ensure_hero_dirs()
    mod = _load_cfg_module()
    tge, tpa, assign_poolq_bin_labels = _load_modules()

    state = _539_state(mod)
    params = tge.assignment_params_from_state(SPORTS, state, tpa=tpa)
    base_sel = tge.SelectionConfig.from_module(mod)
    sel = replace(
        base_sel,
        n_bins=HERO_BINS,
        bin_mode="quantile",
        n_selected=HERO_N_SELECTED,
        winner_selection=str(state["winner_selection"]),
    )

    all_frames: dict[float, dict[str, pd.DataFrame]] = {}
    summary_rows: list[dict] = []

    for gamma in GAMMA_GRID:
        print(f"γ={gamma:g} (λ_crit≈{4/gamma:.2f}) — drawing sort-and-chop roster ...")
        rng = np.random.default_rng(HERO_SEED + int(gamma))
        ability, team_targets = _draw_league_once(tpa, params, rng)
        players_base, _, _ = tpa.simulate_generative_rosters(
            params,
            rng=rng,
            method="sort_chop",
            ability=ability,
            team_targets=team_targets,
        )
        frames: dict[str, pd.DataFrame] = {}
        for label, lam in LAMBDA_ARMS:
            print(f"  λ={lam:g} ...")
            df = run_arm(
                lam,
                players_base=players_base,
                sel=sel,
                params=params,
                gamma=gamma,
                tge=tge,
                tpa=tpa,
                assign_poolq_bin_labels=assign_poolq_bin_labels,
            )
            frames[label] = df
            peak_idx = int(df["selection_rate"].idxmax())
            summary_rows.append(
                {
                    "gamma": gamma,
                    "lambda_crit_approx": 4.0 / gamma,
                    "lambda": lam,
                    "peak_bin": int(df.loc[peak_idx, "bin"]) + 1,
                    "peak_rate": float(df["selection_rate"].max()),
                }
            )
        all_frames[gamma] = frames

    pd.DataFrame(summary_rows).to_csv(CSV, index=False)
    print(f"Wrote {CSV}")

    meta = {
        "diagnostic": "gamma_sweep_sort_chop",
        "date": date.today().isoformat(),
        "preset": PRESET,
        "seed": HERO_SEED,
        "gamma_grid": list(GAMMA_GRID),
        "lambda_arms": [{"label": a, "lambda": l} for a, l in LAMBDA_ARMS],
        "assignment": "sort_chop",
        "theta": params.viability_theta,
    }
    (OUT / "GAMMA_sweep_meta.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )
    build_figure(all_frames)
    print("Done.")


if __name__ == "__main__":
    main()
