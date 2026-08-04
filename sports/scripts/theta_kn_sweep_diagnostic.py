#!/usr/bin/env python3
"""Diagnostic: θ × K/N panel — does peak shape co-vary with both knobs?

PD15 open question: set θ only after seeing whether viability cutline moves with
selectivity (K/N). Fixed soft assign (ρ=8), fixed λ weight (0.55), γ=10.

Grid default:
  θ ∈ {0.50, 0.72, 0.90}
  K/N ∈ {0.01, 0.10, 0.40}  on N = 5600

Run (repo root):
  python sports/scripts/theta_kn_sweep_diagnostic.py

Outputs:
  3-Master_Plan/re_entry/HEROs_and_PASSes/theta/THETA_KN_sweep_summary.csv
  3-Master_Plan/re_entry/HEROs_and_PASSes/theta/THETA_KN_sweep_peak_bin.png
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
    HERO_N_TEAMS,
    HERO_ROSTER_SIZE,
    HERO_SEED,
    KN_PRESETS,
    LAMBDA_FIXED_RHO,
    LAMBDA_MODERATE,
    PRESET,
    hero_league_n,
)
from hero_gallery_paths import THETA, ensure_hero_dirs

OUT = THETA
SUMMARY_CSV = OUT / "THETA_KN_sweep_summary.csv"
PEAK_PNG = OUT / "THETA_KN_sweep_peak_bin.png"

THETA_GRID = (0.50, 0.72, 0.90)
KN_GRID = (
    ("mbb_draft", KN_PRESETS["mbb_draft"]),
    ("characterization", KN_PRESETS["characterization"]),
    ("army_high", KN_PRESETS["army_high"]),
)
FIXED_LAMBDA = LAMBDA_MODERATE
FIXED_RHO = LAMBDA_FIXED_RHO


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


def _playground_state(mod, *, n_selected: int, theta: float) -> dict:
    return {
        "ability_draw": str(getattr(mod, "SELECTION_539_ABILITY_DRAW", "beta_2_2")),
        "target_dist": "uniform",
        "t_low": float(getattr(mod, "SELECTION_539_TARGET_MEAN_LOW", 0.0)),
        "t_high": float(getattr(mod, "SELECTION_539_TARGET_MEAN_HIGH", 1.0)),
        "viability_theta": float(theta),
        "viability_sharpness": float(
            getattr(mod, "SELECTION_539_VIABILITY_SHARPNESS", 10.0)
        ),
        "n_bins": HERO_BINS,
        "n_teams": HERO_N_TEAMS,
        "roster_size": HERO_ROSTER_SIZE,
        "rho": FIXED_RHO,
        "n_selected": n_selected,
        "winner_selection": str(getattr(mod, "SELECTION_539_WINNER_SELECTION", "C")),
    }


def _summarize_selection(
    players: pd.DataFrame,
    sel,
    tge,
    assign_poolq_bin_labels,
) -> dict[str, float | int]:
    summ = tge.inverted_u_bin_table_team_mean(
        players, sel, assign_poolq_bin_labels=assign_poolq_bin_labels
    )
    peak_idx = int(summ["selection_rate"].idxmax())
    peak_bin = int(summ.loc[peak_idx, "bin"]) + 1
    top_rate = float(summ.loc[summ["bin"] == summ["bin"].max(), "selection_rate"].iloc[0])
    bot_rate = float(summ.loc[summ["bin"] == summ["bin"].min(), "selection_rate"].iloc[0])
    rates = summ.set_index("bin")["selection_rate"].sort_index().to_numpy()
    monotone = bool(np.all(rates[:-1] <= rates[1:] + 1e-9))
    return {
        "peak_bin": peak_bin,
        "peak_rate": float(summ["selection_rate"].max()),
        "top_bin_rate": top_rate,
        "bottom_bin_rate": bot_rate,
        "monotone_increasing": int(monotone),
    }


def _draw_roster_once(
    *,
    k: int,
    theta_ref: float,
    mod,
    tge,
    tpa,
) -> tuple[pd.DataFrame, object, dict]:
    """One soft-assign roster per K/N; θ varies only at SCORE."""
    state = _playground_state(mod, n_selected=k, theta=theta_ref)
    params = tge.assignment_params_from_state(SPORTS, state, tpa=tpa)
    params = replace(params, assignment_rho=FIXED_RHO)

    base_sel = tge.SelectionConfig.from_module(mod)
    sel = replace(
        base_sel,
        n_bins=HERO_BINS,
        bin_mode="quantile",
        n_selected=k,
        score_mode="loo_gap_plus_ability",
        loo_pool_l_mode="crowding_smooth",
        loo_gap_weight=FIXED_LAMBDA,
        winner_selection=str(state["winner_selection"]),
    )

    rng = np.random.default_rng(HERO_SEED)
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
    players, _, _ = tpa.simulate_generative_rosters(
        params,
        rng=rng,
        method="soft",
        ability=ability,
        team_targets=team_targets,
    )
    meta = {"params": params, "gamma": params.viability_sharpness}
    return players, sel, meta


def run_cell(
    *,
    theta: float,
    kn_label: str,
    k_over_n: float,
    players_base: pd.DataFrame,
    sel,
    params,
    tge,
    tpa,
    assign_poolq_bin_labels,
) -> dict:
    players = tpa.assign_selection(
        players_base.copy(),
        np.random.default_rng(HERO_SEED + int(theta * 1000)),
        n_selected=sel.n_selected,
        score_mode=sel.score_mode,
        loo_gap_weight=sel.loo_gap_weight,
        winner_selection=sel.winner_selection,
        pool_l_mode=sel.loo_pool_l_mode,
        viability_theta=theta,
        viability_sharpness=params.viability_sharpness,
    )
    stats = _summarize_selection(players, sel, tge, assign_poolq_bin_labels)
    n = hero_league_n()
    return {
        "theta": theta,
        "kn_preset": kn_label,
        "k_over_n": k_over_n,
        "n_individuals": n,
        "n_selected": sel.n_selected,
        "rho": FIXED_RHO,
        "lambda_weight": FIXED_LAMBDA,
        "gamma": params.viability_sharpness,
        **stats,
    }


def build_peak_heatmap(df: pd.DataFrame) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    thetas = sorted(df["theta"].unique())
    kn_labels = [label for label, _ in KN_GRID]
    pivot = df.pivot(index="kn_preset", columns="theta", values="peak_bin")
    pivot = pivot.reindex(index=kn_labels, columns=thetas)

    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    im = ax.imshow(pivot.to_numpy(), aspect="auto", cmap="viridis", vmin=1, vmax=HERO_BINS)
    ax.set_xticks(range(len(thetas)), [f"{t:g}" for t in thetas])
    ax.set_yticks(range(len(kn_labels)), [f"{l}\n(K/N={KN_PRESETS[l]:g})" for l in kn_labels])
    ax.set_xlabel(r"Viability cutline $\theta$")
    ax.set_ylabel(r"Selectivity preset")
    ax.set_title(
        rf"Peak pool-mean bin vs $\theta$ and $K/N$ ({PRESET})"
        "\n"
        rf"soft $\rho={FIXED_RHO:g}$, $\lambda={FIXED_LAMBDA:g}$, $\gamma=10$, $N={hero_league_n()}$"
    )
    for i, kn in enumerate(kn_labels):
        for j, th in enumerate(thetas):
            val = pivot.iloc[i, j]
            if np.isfinite(val):
                ax.text(j, i, f"{int(val)}", ha="center", va="center", color="white", fontsize=11)
    fig.colorbar(im, ax=ax, label="Peak bin (1 = lowest pool mean)")
    fig.tight_layout()
    fig.savefig(PEAK_PNG, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {PEAK_PNG}")


def main() -> None:
    ensure_hero_dirs()
    mod = _load_cfg_module()
    tge, tpa, assign_poolq_bin_labels = _load_modules()

    rows: list[dict] = []
    for kn_label, kn in KN_GRID:
        n = hero_league_n()
        k = max(1, int(round(n * kn)))
        print(f"Drawing roster once for {kn_label} (K/N={kn:g}, K={k}) ...")
        players_base, sel, roster_meta = _draw_roster_once(
            k=k,
            theta_ref=0.72,
            mod=mod,
            tge=tge,
            tpa=tpa,
        )
        params = roster_meta["params"]
        for theta in THETA_GRID:
            print(f"  θ={theta:g} ...")
            rows.append(
                run_cell(
                    theta=theta,
                    kn_label=kn_label,
                    k_over_n=kn,
                    players_base=players_base,
                    sel=sel,
                    params=params,
                    tge=tge,
                    tpa=tpa,
                    assign_poolq_bin_labels=assign_poolq_bin_labels,
                )
            )

    df = pd.DataFrame(rows)
    df.to_csv(SUMMARY_CSV, index=False)
    print(f"Wrote {SUMMARY_CSV}")

    meta = {
        "diagnostic": "theta_kn_sweep",
        "date": date.today().isoformat(),
        "preset": PRESET,
        "seed": HERO_SEED,
        "theta_grid": list(THETA_GRID),
        "kn_grid": {k: v for k, v in KN_GRID},
        "fixed": {
            "rho": FIXED_RHO,
            "lambda_weight": FIXED_LAMBDA,
            "gamma": 10.0,
            "assignment": "soft",
        },
        "n_teams": HERO_N_TEAMS,
        "roster_size": HERO_ROSTER_SIZE,
        "hero_bins": HERO_BINS,
    }
    (OUT / "THETA_KN_sweep_meta.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )

    build_peak_heatmap(df)
    print("\nPeak bin table:")
    print(df.pivot(index="kn_preset", columns="theta", values="peak_bin").to_string())
    print("\nDone.")


if __name__ == "__main__":
    main()
