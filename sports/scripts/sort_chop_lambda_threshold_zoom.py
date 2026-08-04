#!/usr/bin/env python3
"""Sort-and-chop — zoom on λ_crit ≈ 4/γ (λ ∈ [0, 1], seven below crit, three above).

Same rosters as the full λ sweep; only SCORE changes:
  7 λ below crit (linspace 0 → crit, excluding crit)
  crit (= 4/γ)  |  3 λ above crit (linspace crit → 1, excluding crit)

Run (repo root):
  python sports/scripts/sort_chop_lambda_threshold_zoom.py

Override scale:
  GALLERY_N_TEAMS GALLERY_ROSTER_SIZE GALLERY_N_SELECTED GALLERY_HERO_BINS
  GALLERY_THRESHOLD_N_BELOW=7 GALLERY_THRESHOLD_N_ABOVE=3

Output:
  3-Master_Plan/re_entry/HEROs_and_PASSes/sort_chop_lambda/PASS_C_sort_chop_lambda_threshold_zoom.png
"""

from __future__ import annotations

import json
import os
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
    league_scale_title_line,
    PRESET,
)
from hero_gallery_paths import SORT_CHOP_LAMBDA, ensure_hero_dirs

OUT = SORT_CHOP_LAMBDA
PNG = OUT / "PASS_C_sort_chop_lambda_threshold_zoom.png"

LAMBDA_MIN = float(os.environ.get("GALLERY_THRESHOLD_LAMBDA_MIN", "0"))
LAMBDA_MAX = float(os.environ.get("GALLERY_THRESHOLD_LAMBDA_MAX", "1"))
N_BELOW = int(os.environ.get("GALLERY_THRESHOLD_N_BELOW", "7"))
N_ABOVE = int(os.environ.get("GALLERY_THRESHOLD_N_ABOVE", "3"))
# Upper-tail zoom: default bin 10 for 16-bin plots; ~top 15% when bins ≥ 50.
_default_x_bin_lo = "10" if HERO_BINS < 50 else str(max(1, int(round(HERO_BINS * 0.85))))
X_BIN_LO = int(os.environ.get("GALLERY_THRESHOLD_ZOOM_BIN_LO", _default_x_bin_lo))


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
        "n_teams": HERO_N_TEAMS,
        "roster_size": HERO_ROSTER_SIZE,
        "n_selected": HERO_N_SELECTED,
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


def lambda_arms(gamma: float) -> list[tuple[str, float]]:
    crit = 4.0 / float(gamma)
    lo = min(LAMBDA_MIN, crit)
    hi = max(LAMBDA_MAX, crit)
    below = np.linspace(lo, crit, N_BELOW + 1)[:-1]
    above = np.linspace(crit, hi, N_ABOVE + 1)[1:]
    arms: list[tuple[str, float]] = []
    for i, lam in enumerate(below, start=1):
        arms.append((f"below_{i}", round(float(lam), 6)))
    arms.append(("crit", round(crit, 6)))
    for i, lam in enumerate(above, start=1):
        arms.append((f"above_{i}", round(float(lam), 6)))
    return arms


def _plot_order() -> list[str]:
    order = [f"below_{i}" for i in range(1, N_BELOW + 1)]
    order.extend(f"above_{i}" for i in range(N_ABOVE, 0, -1))
    order.append("crit")
    return order


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
    players = tpa.assign_selection(
        players_base.copy(),
        rng,
        n_selected=sel.n_selected,
        score_mode=score_mode,
        loo_gap_weight=w,
        winner_selection=sel.winner_selection,
        pool_l_mode=pool_l,
        viability_theta=params.viability_theta,
        viability_sharpness=params.viability_sharpness,
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
    out["arm"] = label
    out["lambda"] = float(lam)
    return out


def _arm_style(label: str, lam: float, *, crit: float) -> tuple[str, str, float, str]:
    """Style + legend from arm label."""
    if label == "crit":
        return "#023047", rf"$\lambda={lam:.3f}$ ($4/\gamma$, crit)", 3.0, "s"

    blues = plt.cm.Blues(np.linspace(0.35, 0.95, max(N_BELOW, 1)))
    oranges = plt.cm.OrRd(np.linspace(0.45, 0.95, max(N_ABOVE, 1)))

    if label.startswith("below_"):
        i = int(label.removeprefix("below_"))
        color = blues[i - 1]
        lw = 1.4 + 0.1 * i
        tag = "talent-only" if lam <= 0.0 else "below crit"
        leg = rf"$\lambda={lam:.3f}$ ({tag})"
        return color, leg, lw, "o"

    if label.startswith("above_"):
        i = int(label.removeprefix("above_"))
        color = oranges[i - 1]
        lw = 2.2 - 0.15 * i
        leg = rf"$\lambda={lam:.3f}$ (above crit)"
        return color, leg, lw, "o"

    raise KeyError(f"unknown arm label {label!r}")


def build_figure(
    frames: dict[str, pd.DataFrame],
    *,
    gamma: float,
    crit: float,
) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    fig, ax = plt.subplots(figsize=(11.5, 6.2))

    for key in _plot_order():
        if key not in frames:
            continue
        df = frames[key]
        lam = float(df["lambda"].iloc[0])
        color, leg, lw, marker = _arm_style(key, lam, crit=crit)
        x = df["bin"].to_numpy(dtype=float) + 1
        y = df["selection_rate"].to_numpy(dtype=float)
        ax.plot(
            x,
            y,
            marker=marker,
            linestyle="-",
            lw=lw,
            ms=6 if key == "crit" else 5,
            color=color,
            label=leg,
            zorder=8 if key == "crit" else 5,
        )

    ax.set_xlim(X_BIN_LO - 0.4, HERO_BINS + 0.4)
    ax.set_xlabel(r"Bin ($1$ = lowest pool mean in sim)")
    ax.set_ylabel(r"Mean $Y_{\mathrm{selected}}$")
    ax.set_title(
        rf"Sort-and-chop — $\lambda$ threshold zoom ({PRESET})"
        "\n"
        rf"$S_i = A_i - \lambda L_C$ | $\lambda_{{\mathrm{{crit}}}}=4/\gamma={crit:.3f}$ "
        rf"($\gamma={gamma:g}$) | $\lambda\in[{LAMBDA_MIN:g},{LAMBDA_MAX:g}]$ | "
        rf"{league_scale_title_line()}"
        "\n"
        rf"${HERO_BINS}$ bins on pool mean | seed={HERO_SEED} | x zoom: bins $\geq {X_BIN_LO}$",
        fontsize=10.5,
    )
    ax.legend(loc="upper left", fontsize=6, ncol=2, framealpha=0.92)
    ax.set_ylim(bottom=-0.02, top=1.05)
    ax.grid(True, alpha=0.25, lw=0.8)
    fig.tight_layout()
    fig.savefig(PNG, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {PNG}")


def main() -> None:
    ensure_hero_dirs()
    mod = _load_cfg_module()
    tge, tpa, assign_poolq_bin_labels = _load_modules()

    state = _539_playground_state(mod)
    gamma = float(state["viability_sharpness"])
    crit = 4.0 / gamma
    arms = lambda_arms(gamma)

    params = tge.assignment_params_from_state(SPORTS, state, tpa=tpa)
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
        method="sort_chop",
        ability=ability,
        team_targets=team_targets,
    )

    n_players = HERO_N_TEAMS * HERO_ROSTER_SIZE
    frames: dict[str, pd.DataFrame] = {}
    for label, lam in arms:
        print(f"Running threshold arm: {label} (λ={lam:g}, crit={crit:g}) ...")
        df = run_arm(
            label,
            lam,
            players_base=players_base,
            sel=sel,
            params=params,
            rng=np.random.default_rng(
                HERO_SEED + len(label) + int(abs(lam) * 1000)
            ),
            tge=tge,
            tpa=tpa,
            assign_poolq_bin_labels=assign_poolq_bin_labels,
        )
        frames[label] = df
        csv = OUT / (
            f"PASS_C_sort_chop_threshold_{label}_lam{lam:.3f}"
            f"_N{n_players}_K{HERO_N_SELECTED}.csv"
        )
        df.to_csv(csv, index=False)
        print(f"  wrote {csv.name}")

    meta = {
        "diagnostic": "sort_chop_lambda_threshold_zoom",
        "preset": PRESET,
        "seed": HERO_SEED,
        "assignment": "sort_chop",
        "gamma": gamma,
        "lambda_crit_4_over_gamma": crit,
        "lambda_min": LAMBDA_MIN,
        "lambda_max": LAMBDA_MAX,
        "n_below": N_BELOW,
        "n_above": N_ABOVE,
        "x_bin_zoom_lo": X_BIN_LO,
        "n_teams": HERO_N_TEAMS,
        "roster_size": HERO_ROSTER_SIZE,
        "n_individuals": n_players,
        "n_selected": HERO_N_SELECTED,
        "k_over_n": HERO_N_SELECTED / n_players,
        "arms": [{"label": a, "lambda": lam} for a, lam in arms],
        "hero_bins": HERO_BINS,
    }
    (OUT / "PASS_C_sort_chop_lambda_threshold_zoom_meta.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )

    summary_lines = [
        f"# Sort-and-chop λ threshold zoom ({date.today().isoformat()})",
        "",
        f"λ_crit = 4/γ = {crit:.4f} (γ={gamma:g}), λ ∈ [{LAMBDA_MIN:g}, {LAMBDA_MAX:g}], "
        f"{N_BELOW} below + crit + {N_ABOVE} above, seed {HERO_SEED}.",
        f"N={n_players}, K={HERO_N_SELECTED}, {HERO_BINS} bins, x zoom bins ≥ {X_BIN_LO}.",
        "",
    ]
    for label, df in frames.items():
        lam = float(df["lambda"].iloc[0])
        bot = float(df.loc[df["bin"] == df["bin"].min(), "selection_rate"].iloc[0])
        top = float(df.loc[df["bin"] == df["bin"].max(), "selection_rate"].iloc[0])
        peak = float(df["selection_rate"].max())
        peak_bin = int(df.loc[df["selection_rate"].idxmax(), "bin"]) + 1
        summary_lines.append(
            f"- **{label}** (λ={lam:g}): peak {peak:.4f} at bin {peak_bin}; "
            f"bin1→{HERO_BINS} {bot:.4f}→{top:.4f}"
        )
    (OUT / "PASS_C_sort_chop_lambda_threshold_zoom_summary.txt").write_text(
        "\n".join(summary_lines) + "\n", encoding="utf-8"
    )

    build_figure(frames, gamma=gamma, crit=crit)
    print(f"\nDone. λ arms: {[lam for _, lam in arms]}")
    print(f"Outputs in {OUT}")


if __name__ == "__main__":
    main()
