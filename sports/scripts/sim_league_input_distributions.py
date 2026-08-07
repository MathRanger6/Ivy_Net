#!/usr/bin/env python3
"""One-shot draw of simulated league inputs — $A_i$ and $T_{j^*}$ (gallery seed).

Uses the same 539 preset + draw functions as Pass B/C characterization scripts.
No assignment, score, or select — inputs only.

Outputs (under HEROs_and_PASSes/sim_inputs/):
  SIM_league_Ai_Tj_distributions.png  — side-by-side histograms
  SIM_league_Ai_Tj_draws.csv          — one row per player (A_i) + T_j_star column
  SIM_league_Ai_Tj_meta.json          — summary stats

Run (repo root):
  python sports/scripts/sim_league_input_distributions.py
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SCRIPTS))

from gallery_knobs import HERO_N_TEAMS, HERO_ROSTER_SIZE, HERO_SEED, PRESET, hero_league_n
from hero_gallery_paths import SIM_INPUTS, ensure_hero_dirs

OUT = SIM_INPUTS
PNG = OUT / "SIM_league_Ai_Tj_distributions.png"
CSV = OUT / "SIM_league_Ai_Tj_draws.csv"
META_JSON = OUT / "SIM_league_Ai_Tj_meta.json"

N_BINS = 48
BAR_COLOR = "steelblue"
BAR_ALPHA = 0.85


def _load_modules():
    for mod_name in list(sys.modules):
        if mod_name.startswith("tier1_"):
            del sys.modules[mod_name]
    sys.path.insert(0, str(SPORTS))
    sys.path.insert(0, str(REPO))
    import tier1_generative_eda as tge
    import tier1_pool_assignment as tpa

    return tge, tpa


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
        "n_bins": 16,
        "n_teams": HERO_N_TEAMS,
        "roster_size": HERO_ROSTER_SIZE,
        "winner_selection": str(getattr(mod, "SELECTION_539_WINNER_SELECTION", "C")),
    }


def _beta22_pdf(x: np.ndarray) -> np.ndarray:
    """Beta(2,2) on [0,1] — no scipy."""
    x = np.clip(x, 0.0, 1.0)
    return 6.0 * x * (1.0 - x)


def _draw_league(*, tge, tpa, params) -> tuple[np.ndarray, np.ndarray]:
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
    return ability, team_targets


def _summary(name: str, values: np.ndarray) -> dict:
    v = np.asarray(values, dtype=float)
    return {
        "label": name,
        "n": int(v.size),
        "mean": float(v.mean()),
        "std": float(v.std()),
        "min": float(v.min()),
        "max": float(v.max()),
    }


def build_figure(
    ability: np.ndarray,
    team_targets: np.ndarray,
    *,
    ability_draw: str,
    target_dist: str,
) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    edges = np.linspace(0.0, 1.0, N_BINS + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])
    bin_width = edges[1] - edges[0]

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), sharex=True)

    panels = [
        (
            axes[0],
            ability,
            rf"$A_i$ — player ability ($n={ability.size:,}$)",
            rf"Beta(2,2) pdf ({ability_draw})",
            _beta22_pdf if ability_draw in ("beta_2_2", "beta", "beta22") else None,
        ),
        (
            axes[1],
            team_targets,
            rf"$T_{{j^*}}$ — sim team target ($n={team_targets.size:,}$ teams)",
            rf"Uniform[0,1] pdf ({target_dist})",
            (lambda x: np.ones_like(x)) if target_dist == "uniform" else None,
        ),
    ]

    for ax, values, title, theory_label, theory_fn in panels:
        counts, _ = np.histogram(values, bins=edges)
        ax.bar(
            centers,
            counts,
            width=bin_width * 0.98,
            align="center",
            color=BAR_COLOR,
            alpha=BAR_ALPHA,
            edgecolor=BAR_COLOR,
            linewidth=0.3,
            label=rf"Sim draw (seed {HERO_SEED})",
        )
        if theory_fn is not None:
            x_line = np.linspace(0.0, 1.0, 200)
            pdf = theory_fn(x_line)
            scale = values.size * bin_width
            ax.plot(
                x_line,
                pdf * scale,
                color="darkorange",
                lw=2.0,
                label=theory_label,
            )
        ax.set_xlim(0.0, 1.0)
        ax.set_xlabel(r"Value on [0, 1]", fontsize=10)
        ax.set_ylabel("Count", fontsize=10)
        ax.set_title(title, fontsize=11, pad=8)
        ax.grid(axis="y", alpha=0.25, linewidth=0.5)
        ax.legend(loc="upper right", fontsize=8, framealpha=0.92)
        stats = _summary("", values)
        ax.text(
            0.03,
            0.97,
            rf"mean={stats['mean']:.3f}, sd={stats['std']:.3f}",
            transform=ax.transAxes,
            va="top",
            ha="left",
            fontsize=8,
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white", alpha=0.85, edgecolor="0.8"),
        )

    fig.suptitle(
        rf"Simulated league inputs — {PRESET} preset, seed {HERO_SEED}, "
        rf"$N={hero_league_n():,}$ players",
        fontsize=12,
        y=1.02,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(PNG, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {PNG}")


def main() -> None:
    ensure_hero_dirs()
    import importlib.util

    mod_path = SPORTS / "tier1_sim_config.py"
    spec = importlib.util.spec_from_file_location("tier1_sim_config", mod_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)

    tge, tpa = _load_modules()
    state = _539_state(mod)
    params = tge.assignment_params_from_state(SPORTS, state, tpa=tpa)
    ability, team_targets = _draw_league(tge=tge, tpa=tpa, params=params)

    # CSV: one row per player; repeat T_j_star on each roster slot for inspection
    team_id = np.repeat(np.arange(params.n_teams), params.roster_size)
    df = pd.DataFrame(
        {
            "player_idx": np.arange(params.n_individuals),
            "team_id": team_id,
            "A_i": ability,
            "T_j_star": team_targets[team_id],
        }
    )
    df.to_csv(CSV, index=False)
    print(f"Wrote {CSV}")

    build_figure(
        ability,
        team_targets,
        ability_draw=str(params.ability_draw),
        target_dist=str(params.target_mean_dist),
    )

    meta = {
        "diagnostic": "sim_league_input_distributions",
        "date": date.today().isoformat(),
        "preset": PRESET,
        "seed": HERO_SEED,
        "ability_draw": str(params.ability_draw),
        "target_mean_dist": str(params.target_mean_dist),
        "n_players": int(params.n_individuals),
        "n_teams": int(params.n_teams),
        "outputs": {
            "png": PNG.name,
            "csv": CSV.name,
        },
        "A_i": _summary("A_i", ability),
        "T_j_star": _summary("T_{j*}", team_targets),
    }
    META_JSON.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {META_JSON}")
    print("Done.")


if __name__ == "__main__":
    main()
