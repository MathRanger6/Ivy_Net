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
PNG_KEY = OUT / "GAMMA_sweep_lambda_curves_key_arms.png"
CSV = OUT / "GAMMA_sweep_summary.csv"
KEY_LAMBDAS = frozenset({0.0, 0.55, 1.0})

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


def _plot_gamma_panels(
    all_frames: dict[float, dict[str, pd.DataFrame]],
    *,
    lambda_filter: frozenset[float] | None,
    out_path: Path,
    suptitle_extra: str,
) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    n_gamma = len(GAMMA_GRID)
    fig, axes = plt.subplots(n_gamma, 1, figsize=(8.8, 9.2), sharex=True, sharey=True)
    if n_gamma == 1:
        axes = [axes]

    legend_handles: list = []
    legend_labels: list[str] = []

    for ax, gamma in zip(axes, GAMMA_GRID):
        frames = all_frames[gamma]
        crit = 4.0 / gamma
        for label, lam in LAMBDA_ARMS:
            if lambda_filter is not None and lam not in lambda_filter:
                continue
            df = frames[label]
            x = df["bin"].to_numpy(dtype=float) + 1
            y = df["selection_rate"].to_numpy(dtype=float)
            is_key = lam in KEY_LAMBDAS
            (line,) = ax.plot(
                x,
                y,
                marker="o",
                lw=2.8 if is_key else 1.6,
                ms=5 if is_key else 3,
                alpha=1.0 if is_key else 0.55,
                ls="-" if is_key else "--",
                color=LAM_COLORS[lam],
                label=rf"$\lambda={lam:g}$",
                zorder=3 if is_key else 2,
            )
            if ax is axes[0]:
                legend_handles.append(line)
                legend_labels.append(rf"$\lambda={lam:g}$")
        ax.axhline(1.0 / HERO_BINS, color="#bbbbbb", lw=0.8, ls=":", zorder=0)
        ax.set_title(
            rf"$\gamma={gamma:g}$  —  $\lambda_{{\mathrm{{crit}}}}\approx {crit:.2f}$",
            fontsize=12,
            loc="left",
            pad=8,
        )
        ax.set_ylim(0, max(0.28, ax.get_ylim()[1]))
        ax.grid(True, axis="y", alpha=0.25, lw=0.6)
        ax.tick_params(labelsize=10)

    axes[-1].set_xlabel("Pool-mean bin (1 = weakest teams)", fontsize=11)
    axes[0].set_ylabel("Selection rate", fontsize=11)

    subtitle = (
        rf"Sort-and-chop assign | {league_scale_title_line()} | {HERO_BINS} bins | seed={HERO_SEED}"
    )
    if lambda_filter is not None:
        arms = ", ".join(rf"$\lambda={v:g}$" for _, v in LAMBDA_ARMS if v in lambda_filter)
        subtitle += rf"\nKey arms only: {arms}"
    else:
        subtitle += r"\nSolid = $\lambda \in \{0, 0.55, 1.0\}$; dashed = intermediate $\lambda$"

    fig.suptitle(
        rf"$\gamma$ sweep — congestion weight in score ({PRESET}){suptitle_extra}",
        fontsize=13,
        y=0.995,
    )
    fig.text(0.5, 0.02, subtitle, ha="center", va="bottom", fontsize=9, color="#333333")
    fig.legend(
        legend_handles,
        legend_labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.06),
        ncol=min(5, len(legend_labels)),
        fontsize=10,
        frameon=False,
    )
    fig.subplots_adjust(left=0.1, right=0.98, top=0.93, bottom=0.11, hspace=0.32)
    fig.savefig(out_path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_path}")


def build_figure(all_frames: dict[float, dict[str, pd.DataFrame]]) -> None:
    _plot_gamma_panels(all_frames, lambda_filter=None, out_path=PNG, suptitle_extra="")
    _plot_gamma_panels(
        all_frames,
        lambda_filter=KEY_LAMBDAS,
        out_path=PNG_KEY,
        suptitle_extra=" (readable key arms)",
    )


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
