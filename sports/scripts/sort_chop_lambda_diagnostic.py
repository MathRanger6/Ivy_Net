#!/usr/bin/env python3
"""Diagnostic: sort-and-chop assignment only — λ sweep (same rosters).

Same A_i draw + one sort-and-chop assign; only SCORE changes:
  S_i = A_i − λ·L_C  (λ=0 → S_i = A_i)
VISUALIZE: quantile bins on pool mean (gallery knobs: N teams, roster, K, bins, seed).

Default λ grid: 0, 0.1, …, 1.0 plus λ_crit = 4/γ if not already on grid.
Legacy 5-arm grid: GALLERY_LAMBDA_SWEEP=legacy

League default: 350×16 = 5600 players, K=560 (K/N=10% characterization). Override:
  GALLERY_N_TEAMS GALLERY_ROSTER_SIZE GALLERY_N_SELECTED GALLERY_HERO_BINS
  GALLERY_LAMBDA_SWEEP=decile|legacy|0,0.25,0.55

Run (repo root):
  python sports/scripts/sort_chop_lambda_diagnostic.py

  GALLERY_HERO_BINS=100 python sports/scripts/sort_chop_lambda_diagnostic.py

Output:
  3-Master_Plan/re_entry/HEROs_and_PASSes/sort_chop_lambda/PASS_C_sort_chop_lambda_sweep.png
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
    resolve_pool_l_mode,
)
from hero_gallery_paths import SORT_CHOP_LAMBDA, ensure_hero_dirs

OUT = SORT_CHOP_LAMBDA
PNG = OUT / "PASS_C_sort_chop_lambda_sweep.png"

LEGACY_LAMBDA_ARMS: list[tuple[str, float]] = [
    ("lambda_0", 0.0),
    ("lambda_025", 0.25),
    ("lambda_055", 0.55),
    ("lambda_075", 0.75),
    ("lambda_1", 1.0),
]


def _lam_label(lam: float) -> str:
    if lam <= 0.0:
        return "lambda_0"
    txt = f"{lam:.3f}".rstrip("0").rstrip(".")
    return "lambda_" + txt.replace(".", "")


def build_lambda_arms(gamma: float) -> list[tuple[str, float]]:
    """λ arms from env or decile default; always includes λ_crit = 4/γ."""
    mode = os.environ.get("GALLERY_LAMBDA_SWEEP", "decile").strip().lower()
    if mode == "legacy":
        return list(LEGACY_LAMBDA_ARMS)

    if mode == "decile":
        values = [round(i * 0.1, 10) for i in range(11)]
    else:
        values = sorted({float(x.strip()) for x in mode.split(",") if x.strip()})

    crit = round(4.0 / float(gamma), 10)
    merged = sorted(set(values) | {crit})
    return [(_lam_label(lam), lam) for lam in merged]


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
    return "loo_gap_plus_ability", resolve_pool_l_mode(), float(lam)


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


def build_figure(
    frames: dict[str, pd.DataFrame],
    *,
    lambda_arms: list[tuple[str, float]],
    gamma: float,
) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    crit = 4.0 / float(gamma)
    n_arms = len(lambda_arms)
    fig_w = 10.5 if n_arms > 6 else 9.0
    fig, ax = plt.subplots(figsize=(fig_w, 5.8))

    lams = sorted({lam for _, lam in lambda_arms})
    lam_min, lam_max = min(lams), max(lams)
    cmap = plt.cm.viridis
    norm_lam = plt.Normalize(vmin=lam_min, vmax=lam_max if lam_max > lam_min else lam_min + 1.0)

    # High λ first; λ=0 and λ_crit drawn last on top.
    plot_items = sorted(lambda_arms, key=lambda t: t[1], reverse=True)
    crit_key = _lam_label(crit) if any(abs(lam - crit) < 1e-9 for _, lam in lambda_arms) else None
    zero_key = "lambda_0" if "lambda_0" in frames else None

    for label, lam in plot_items:
        if label not in frames:
            continue
        df = frames[label]
        x = df["bin"].to_numpy(dtype=float) + 1
        y = df["selection_rate"].to_numpy(dtype=float)
        is_zero = label == zero_key
        is_crit = crit_key is not None and abs(lam - crit) < 1e-9
        if is_zero:
            color, leg = "steelblue", r"$\lambda=0$ (talent-only)"
            ls, lw, ms, marker, zorder = "--", 2.5, 5, "s", 12
        elif is_crit:
            color, leg = "#023047", rf"$\lambda={lam:.2f}$ ($4/\gamma$, crit)"
            ls, lw, ms, marker, zorder = "-", 3.0, 5, "s", 11
        else:
            color = cmap(norm_lam(lam))
            leg = rf"$\lambda={lam:.1f}$" if lam == round(lam, 1) else rf"$\lambda={lam:g}$"
            ls, lw, ms, marker, zorder = "-", 1.6, 3, ".", 5
        ax.plot(
            x,
            y,
            linestyle=ls,
            marker=marker,
            lw=lw,
            ms=ms,
            color=color,
            label=leg,
            zorder=zorder,
            alpha=0.95 if is_zero or is_crit else 0.85,
        )

    ax.set_xlabel(r"Bin ($1$ = lowest pool mean in sim)")
    ax.set_ylabel(r"Mean $Y_{\mathrm{selected}}$")
    ax.set_title(
        rf"Sort-and-chop only ({PRESET}) — same assign, $\lambda$ in score varies"
        "\n"
        rf"$S_i = A_i - \lambda L_C$ | $\lambda_{{\mathrm{{crit}}}}=4/\gamma={crit:.2f}$ "
        rf"($\gamma={gamma:g}$) | {league_scale_title_line()}, "
        rf"${HERO_BINS}$ bins on pool mean | seed={HERO_SEED}",
        fontsize=10.5,
    )
    ncol = 2 if n_arms > 6 else 1
    ax.legend(loc="upper left", fontsize=7 if n_arms > 6 else 8, ncol=ncol, framealpha=0.92)
    ax.set_ylim(bottom=0)
    ax.set_xlim(1, HERO_BINS)
    ax.grid(True, alpha=0.2, lw=0.7)
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
    lambda_arms = build_lambda_arms(gamma)
    crit = 4.0 / gamma

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
    for label, lam in lambda_arms:
        print(f"Running sort-and-chop arm: {label} (λ={lam:g}) ...")
        df = run_arm(
            label,
            lam,
            players_base=players_base,
            sel=sel,
            params=params,
            rng=np.random.default_rng(HERO_SEED + len(label) + int(lam * 1000)),
            tge=tge,
            tpa=tpa,
            assign_poolq_bin_labels=assign_poolq_bin_labels,
        )
        frames[label] = df
        csv = OUT / (
            f"PASS_C_sort_chop_{label}_{HERO_BINS}quantile_poolmean"
            f"_N{n_players}_K{HERO_N_SELECTED}.csv"
        )
        df.to_csv(csv, index=False)
        print(f"  wrote {csv.name}")

    meta = {
        "diagnostic": "sort_chop_lambda_sweep",
        "preset": PRESET,
        "seed": HERO_SEED,
        "assignment": "sort_chop",
        "gamma": gamma,
        "lambda_crit_4_over_gamma": crit,
        "n_teams": HERO_N_TEAMS,
        "roster_size": HERO_ROSTER_SIZE,
        "n_individuals": n_players,
        "n_selected": HERO_N_SELECTED,
        "k_over_n": HERO_N_SELECTED / n_players,
        "arms": [{"label": a, "lambda": lam} for a, lam in lambda_arms],
        "visualize_x_axis": "pool_mean",
        "hero_bins": HERO_BINS,
        "lambda_sweep_mode": os.environ.get("GALLERY_LAMBDA_SWEEP", "decile"),
    }
    (OUT / "PASS_C_sort_chop_lambda_diagnostic_meta.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )

    summary_lines = [
        f"# Sort-and-chop λ diagnostic ({date.today().isoformat()})",
        "",
        "Same sort-and-chop rosters; only λ in score changes.",
        f"Preset {PRESET}, seed {HERO_SEED}, N={n_players} ({HERO_N_TEAMS}×{HERO_ROSTER_SIZE}), "
        f"K={HERO_N_SELECTED}, {HERO_BINS} bins on pool mean.",
        f"λ_crit = 4/γ = {crit:.4f} (γ={gamma:g}).",
        "",
    ]
    for label, df in frames.items():
        lam = float(df["lambda"].iloc[0])
        bot = float(df.loc[df["bin"] == df["bin"].min(), "selection_rate"].iloc[0])
        top = float(df.loc[df["bin"] == df["bin"].max(), "selection_rate"].iloc[0])
        peak = float(df["selection_rate"].max())
        peak_bin = int(df.loc[df["selection_rate"].idxmax(), "bin"]) + 1
        tag = " **crit**" if abs(lam - crit) < 1e-9 else ""
        summary_lines.append(
            f"- **{label}** (λ={lam:g}){tag}: bin1→{HERO_BINS} {bot:.4f}→{top:.4f}; "
            f"peak {peak:.4f} at bin {peak_bin}"
        )
    (OUT / "PASS_C_sort_chop_lambda_diagnostic_summary.txt").write_text(
        "\n".join(summary_lines) + "\n", encoding="utf-8"
    )

    build_figure(frames, lambda_arms=lambda_arms, gamma=gamma)
    print(f"\nDone. λ arms ({len(lambda_arms)}): {[lam for _, lam in lambda_arms]}")
    print(f"Outputs in {OUT}")


if __name__ == "__main__":
    main()
