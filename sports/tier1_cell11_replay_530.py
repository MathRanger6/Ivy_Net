# Executed by 538 notebook CELL 11 via exec(..., globals()).
# 530 CELL 6 analog on simulated rosters: pool mean vs pool SD (+ span stats).

from __future__ import annotations

import json
import sys
from pathlib import Path

import importlib

import matplotlib.pyplot as plt
import numpy as np


def _sports_dir() -> Path:
    cwd = Path.cwd().resolve()
    for candidate in (cwd / "sports", cwd):
        if (candidate / "tier1_sim_config.py").is_file():
            return candidate
    raise FileNotFoundError(f"Cannot find sports/ from cwd={cwd}")


def _load_tpa():
    """Import/reload tier1_pool_assignment after sports/ is on sys.path."""
    sports = _sports_dir()
    if str(sports) not in sys.path:
        sys.path.insert(0, str(sports))
    import tier1_pool_assignment as tpa

    importlib.reload(tpa)
    return tpa, sports


def _params_from_playground_state(sports: Path, tpa) -> object:
    AssignmentParams = tpa.AssignmentParams
    base = AssignmentParams.from_tier1_sim_config(sports / "tier1_sim_config.py")
    state_path = sports / "tier1_cell10_playground_state.json"
    if not state_path.is_file():
        return base
    try:
        st = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return base
    return AssignmentParams(
        n_teams=int(st.get("n_teams", base.n_teams)),
        roster_size=int(st.get("roster_size", base.roster_size)),
        target_mean_dist=st.get("target_dist", base.target_mean_dist),
        target_mean_low=float(st.get("t_low", base.target_mean_low)),
        target_mean_high=float(st.get("t_high", base.target_mean_high)),
        target_mean_mu=base.target_mean_mu,
        target_mean_sigma=base.target_mean_sigma,
        assignment_kernel=st.get("kernel", base.assignment_kernel),
        assignment_temperature=float(st.get("tau", base.assignment_temperature)),
        assignment_rho=float(st.get("rho", base.assignment_rho)),
        assignment_sigma=float(st.get("sigma", base.assignment_sigma)),
        use_preferential_attachment=bool(
            st.get("use_preferential_attachment", base.use_preferential_attachment)
        ),
        preferential_alpha=float(st.get("pref_alpha", base.preferential_alpha)),
        preferential_k=base.preferential_k,
        ability_draw=st.get("ability_draw", base.ability_draw),
        ability_mean=base.ability_mean,
        ability_sd=base.ability_sd,
        ability_clip_low=base.ability_clip_low,
        ability_clip_high=base.ability_clip_high,
        ability_student_t_df=base.ability_student_t_df,
        ability_student_t_scale=base.ability_student_t_scale,
        sorting_noise_sd=base.sorting_noise_sd,
        viability_theta=float(st.get("viability_theta", base.viability_theta)),
    )


def run_cell11(*, seed: int | None = None) -> None:
    tpa, sports = _load_tpa()
    simulate_generative_rosters = tpa.simulate_generative_rosters

    params = _params_from_playground_state(sports, tpa)
    if seed is None:
        state_path = sports / "tier1_cell10_playground_state.json"
        if state_path.is_file():
            try:
                seed = int(json.loads(state_path.read_text(encoding="utf-8")).get("seed", 42))
            except (OSError, json.JSONDecodeError, TypeError, ValueError):
                seed = 42
        else:
            seed = 42

    print(
        f"CELL 11: sim rosters J={params.n_teams} roster={params.roster_size} "
        f"N={params.n_individuals} seed={seed}"
    )
    if params.n_teams > 500:
        print("  (large J — assignment may take a while)")

    _, teams, _ = simulate_generative_rosters(
        params, seed=seed, method="soft"
    )
    teams = teams.dropna(subset=["pool_mean", "pool_sd"])
    span = teams["max"] - teams["min"]
    med_sd = float(teams["pool_sd"].median())
    med_span = float(span.median())
    r_mean_sd = float(teams["pool_mean"].corr(teams["pool_sd"]))

    print(f"  median pool_sd={med_sd:.3f}  median span={med_span:.3f}  r(mean,sd)={r_mean_sd:.3f}")
    print("  530 targets: median roster SD ~ 0.8; weak positive mean–SD link OK")

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.5))
    ax0, ax1 = axes

    ax0.scatter(
        teams["pool_mean"],
        teams["pool_sd"],
        s=12,
        alpha=0.35,
        c="C0",
        edgecolors="none",
    )
    ax0.set_xlabel("Pool mean ability (realized)")
    ax0.set_ylabel("Pool SD (within roster)")
    ax0.set_title("538 CELL 11 — mean vs SD (530 CELL 6 analog)")

    ax1.hist(span, bins=40, color="C1", alpha=0.85, edgecolor="white")
    ax1.axvline(med_span, color="k", ls="--", lw=1.2, label=f"median span={med_span:.2f}")
    ax1.set_xlabel("Roster span (max − min ability)")
    ax1.set_ylabel("Number of teams")
    ax1.set_title("Roster span histogram")
    ax1.legend(loc="upper right")

    fig.suptitle(
        f"Soft assign · J={params.n_teams} · τ={params.assignment_temperature:.2f}",
        fontsize=11,
        y=1.02,
    )
    fig.tight_layout()
    plt.show()
    plt.close(fig)


if __name__ == "__main__":
    run_cell11()
