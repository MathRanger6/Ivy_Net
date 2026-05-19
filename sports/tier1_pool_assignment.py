"""Generative pool assignment for Tier 1 Thread A (**538**, not **537**).

Soft assignment: draw team target means T_j, draw abilities A_i, place players on
rosters with pi_ij ∝ f(A_i - T_j) (optional preferential attachment on fixed T_j).

Benchmark: sort-and-chop (537 assortative choice B) for overlap comparisons vs 530.

Design: sports/documents/Tier1_Presorting_Design_Note.md
Defaults: sports/tier1_sim_config.py
"""

from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import numpy as np
import pandas as pd

AssignmentKernel = Literal["gaussian", "cauchy"]
TargetMeanDist = Literal["uniform", "normal_clipped"]
AbilityDraw = Literal["uniform_01", "normal_clipped", "normal_plus_student_t"]
AssignmentMethod = Literal["soft", "sort_chop"]


@dataclass(frozen=True)
class AssignmentParams:
    """Knobs for one generative roster draw (mirror tier1_sim_config.py)."""

    n_teams: int
    roster_size: int
    target_mean_dist: TargetMeanDist
    target_mean_low: float
    target_mean_high: float
    target_mean_mu: float
    target_mean_sigma: float
    assignment_kernel: AssignmentKernel
    assignment_temperature: float
    preferential_alpha: float
    preferential_k: float
    ability_draw: AbilityDraw
    ability_mean: float
    ability_sd: float
    ability_clip_low: float
    ability_clip_high: float
    ability_student_t_df: float
    ability_student_t_scale: float
    sorting_noise_sd: float = 0.0
    """Only used for sort_chop benchmark (537-style noise on sort signal)."""

    @property
    def n_individuals(self) -> int:
        return int(self.n_teams) * int(self.roster_size)

    @classmethod
    def from_module(cls, mod: Any) -> AssignmentParams:
        return cls(
            n_teams=int(mod.N_TEAMS),
            roster_size=int(mod.ROSTER_SIZE),
            target_mean_dist=mod.TARGET_MEAN_DIST,
            target_mean_low=float(mod.TARGET_MEAN_LOW),
            target_mean_high=float(mod.TARGET_MEAN_HIGH),
            target_mean_mu=float(mod.TARGET_MEAN_MU),
            target_mean_sigma=float(mod.TARGET_MEAN_SIGMA),
            assignment_kernel=mod.ASSIGNMENT_KERNEL,
            assignment_temperature=float(mod.ASSIGNMENT_TEMPERATURE),
            preferential_alpha=float(mod.PREFERENTIAL_ALPHA),
            preferential_k=float(mod.PREFERENTIAL_K),
            ability_draw=mod.ABILITY_DRAW,
            ability_mean=float(mod.ABILITY_MEAN),
            ability_sd=float(mod.ABILITY_SD),
            ability_clip_low=float(mod.ABILITY_CLIP_LOW),
            ability_clip_high=float(mod.ABILITY_CLIP_HIGH),
            ability_student_t_df=float(mod.ABILITY_STUDENT_T_DF),
            ability_student_t_scale=float(mod.ABILITY_STUDENT_T_SCALE),
            sorting_noise_sd=float(getattr(mod, "SORTING_NOISE_SD", 0.0)),
        )

    @classmethod
    def from_tier1_sim_config(cls, path: Path | None = None) -> AssignmentParams:
        cfg_path = path or Path(__file__).resolve().parent / "tier1_sim_config.py"
        spec = importlib.util.spec_from_file_location("tier1_sim_config", cfg_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"cannot load tier1_sim_config from {cfg_path}")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return cls.from_module(mod)


def load_tier1_sim_config(path: Path | None = None) -> Any:
    """Load sports/tier1_sim_config.py as a module (same pattern as 537 + sim_config)."""
    cfg_path = path or Path(__file__).resolve().parent / "tier1_sim_config.py"
    spec = importlib.util.spec_from_file_location("tier1_sim_config", cfg_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load tier1_sim_config from {cfg_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def draw_abilities(
    rng: np.random.Generator,
    n: int,
    *,
    ability_draw: AbilityDraw,
    ability_mean: float = 0.0,
    ability_sd: float = 1.0,
    ability_clip_low: float = -2.5,
    ability_clip_high: float = 3.5,
    ability_student_t_df: float = 4.0,
    ability_student_t_scale: float = 0.25,
) -> np.ndarray:
    """Draw A_i for n synthetic players."""
    if ability_draw == "uniform_01":
        return rng.uniform(0.0, 1.0, size=n)
    if ability_draw == "normal_clipped":
        return np.clip(
            rng.normal(loc=ability_mean, scale=ability_sd, size=n),
            ability_clip_low,
            ability_clip_high,
        )
    if ability_draw == "normal_plus_student_t":
        base = rng.normal(loc=ability_mean, scale=ability_sd, size=n)
        if ability_student_t_scale > 0 and ability_student_t_df > 0:
            noise = rng.standard_t(df=ability_student_t_df, size=n)
            base = base + ability_student_t_scale * noise
        return np.clip(base, ability_clip_low, ability_clip_high)
    raise ValueError(f"unknown ability_draw {ability_draw!r}")


def draw_target_means(
    rng: np.random.Generator,
    n_teams: int,
    *,
    target_mean_dist: TargetMeanDist,
    target_mean_low: float,
    target_mean_high: float,
    target_mean_mu: float,
    target_mean_sigma: float,
) -> np.ndarray:
    """Draw fixed team targets T_j (length n_teams)."""
    if target_mean_dist == "uniform":
        return rng.uniform(target_mean_low, target_mean_high, size=n_teams)
    if target_mean_dist == "normal_clipped":
        raw = rng.normal(loc=target_mean_mu, scale=target_mean_sigma, size=n_teams)
        return np.clip(raw, target_mean_low, target_mean_high)
    raise ValueError(f"unknown target_mean_dist {target_mean_dist!r}")


def _kernel_weights(
    ability_i: float,
    team_targets: np.ndarray,
    *,
    assignment_kernel: AssignmentKernel,
    assignment_temperature: float,
) -> np.ndarray:
    tau = max(float(assignment_temperature), 1e-12)
    delta = float(ability_i) - np.asarray(team_targets, dtype=float)
    if assignment_kernel == "gaussian":
        return np.exp(-0.5 * (delta / tau) ** 2)
    if assignment_kernel == "cauchy":
        return 1.0 / (1.0 + (delta / tau) ** 2)
    raise ValueError(f"unknown assignment_kernel {assignment_kernel!r}")


def _normalize_probs(weights: np.ndarray) -> np.ndarray:
    w = np.asarray(weights, dtype=float)
    w = np.where(np.isfinite(w), w, 0.0)
    w = np.clip(w, 0.0, None)
    total = float(w.sum())
    if total <= 0:
        raise ValueError("non-positive total assignment weight")
    return w / total


def soft_assign(
    rng: np.random.Generator,
    ability: np.ndarray,
    team_targets: np.ndarray,
    roster_size: int,
    *,
    assignment_kernel: AssignmentKernel = "gaussian",
    assignment_temperature: float = 0.45,
    preferential_alpha: float = 0.0,
    preferential_k: float = 1.0,
) -> np.ndarray:
    """Place each player on exactly one team with equal roster sizes.

    Sequential assignment on a random player order. For player i,
    pi_ij ∝ f(A_i - T_j) * (n_j + k)^alpha, zeroed for teams already at roster_size.
    """
    ability = np.asarray(ability, dtype=float)
    team_targets = np.asarray(team_targets, dtype=float)
    n_players = len(ability)
    n_teams = len(team_targets)
    expected = n_teams * int(roster_size)
    if n_players != expected:
        raise ValueError(
            f"len(ability)={n_players} must equal n_teams*roster_size={expected}"
        )

    pool_id = np.full(n_players, -1, dtype=np.int64)
    counts = np.zeros(n_teams, dtype=np.int64)
    alpha = float(preferential_alpha)
    k_pref = max(float(preferential_k), 1e-12)

    for i in rng.permutation(n_players):
        w = _kernel_weights(
            ability[i],
            team_targets,
            assignment_kernel=assignment_kernel,
            assignment_temperature=assignment_temperature,
        )
        if alpha != 0.0:
            w = w * np.power(counts.astype(float) + k_pref, alpha)
        open_mask = counts < int(roster_size)
        w = np.where(open_mask, w, 0.0)
        if float(w.sum()) <= 0.0:
            # Tiny τ or extreme A_i vs T_j can zero out the kernel; place uniformly
            # among teams that still have roster room.
            open_idx = np.flatnonzero(open_mask)
            if open_idx.size == 0:
                raise RuntimeError(
                    "soft_assign: no open roster slots "
                    f"(counts={counts}, roster_size={roster_size})"
                )
            w = np.zeros(n_teams, dtype=float)
            w[open_idx] = 1.0
        pool_id[i] = int(rng.choice(n_teams, p=_normalize_probs(w)))
        counts[pool_id[i]] += 1

    if np.any(counts != int(roster_size)):
        raise RuntimeError(f"uneven rosters after soft_assign: {counts}")
    return pool_id


def assign_sort_chop_benchmark(
    rng: np.random.Generator,
    ability: np.ndarray,
    n_teams: int,
    *,
    sorting_noise_sd: float = 0.0,
) -> np.ndarray:
    """537-style assortative assignment: sort by (noisy) ability, equal-count slices."""
    ability = np.asarray(ability, dtype=float)
    n = len(ability)
    noise_sd = max(float(sorting_noise_sd), 0.0)
    signal = (
        ability
        if noise_sd == 0.0
        else ability + rng.normal(0.0, noise_sd, size=n)
    )
    order = np.argsort(signal, kind="mergesort")
    base = np.repeat(np.arange(n_teams), int(np.ceil(n / n_teams)))[:n]
    pool_id = np.empty(n, dtype=np.int64)
    pool_id[order] = base
    return pool_id


def build_roster_dataframe(
    ability: np.ndarray,
    pool_id: np.ndarray,
    team_targets: np.ndarray,
) -> pd.DataFrame:
    """One row per player with assigned pool and that pool's target mean T_j."""
    ability = np.asarray(ability, dtype=float)
    pool_id = np.asarray(pool_id, dtype=np.int64)
    team_targets = np.asarray(team_targets, dtype=float)
    return pd.DataFrame(
        {
            "player_id": np.arange(len(ability), dtype=np.int64),
            "ability": ability,
            "pool_id": pool_id,
            "team_target": team_targets[pool_id],
        }
    )


def add_poolq_loo(players: pd.DataFrame) -> pd.DataFrame:
    """Leave-one-out mean teammate ability (LOO pool quality L / poolq_loo)."""
    out = players.copy()
    g = out.groupby("pool_id", observed=True)["ability"]
    ssum = g.transform("sum")
    cnt = g.transform("count").astype(float)
    den = (cnt - 1.0).replace(0.0, np.nan)
    out["poolq_loo"] = (ssum - out["ability"]) / den
    return out


def selection_weights(
    players: pd.DataFrame,
    *,
    score_mode: str,
    loo_gap_weight: float,
) -> np.ndarray:
    a = players["ability"].to_numpy(dtype=float)
    q = players["poolq_loo"].to_numpy(dtype=float)
    mode = str(score_mode).strip().lower()
    if mode == "ability":
        w = a.copy()
    elif mode == "loo_gap_plus_ability":
        wgt = float(loo_gap_weight)
        w = wgt * (a - q) + (1.0 - wgt) * a
        w = np.where(np.isfinite(q), w, a)
    else:
        raise ValueError(f"unknown selection score_mode {score_mode!r}")
    w = np.where(np.isfinite(w), w, 0.0)
    return np.clip(w, 0.0, None)


def choose_selected(
    rng: np.random.Generator,
    weights: np.ndarray,
    k: int,
    choice: str,
) -> np.ndarray:
    """Boolean selected mask (537 winner draw A/B/C)."""
    n = len(weights)
    w = np.asarray(weights, dtype=float)
    w = np.where(np.isfinite(w), w, 0.0)
    w = np.clip(w, 0.0, None)
    n_positive = int(np.count_nonzero(w > 0))
    if n_positive == 0:
        return np.zeros(n, dtype=bool)
    k_eff = min(int(k), n_positive)
    if choice == "A":
        total = float(w.sum())
        if total <= 0:
            p = np.full(n, 1.0 / n)
        else:
            p = w / total
        idx = rng.choice(n, size=k_eff, replace=False, p=p)
        out = np.zeros(n, dtype=bool)
        out[idx] = True
        return out
    if choice == "B":
        total = float(w.sum())
        p = w / total if total > 0 else np.full(n, 1.0 / n)
        return rng.uniform(size=n) < np.minimum(p * k_eff, 1.0)
    if choice == "C":
        idx = np.argsort(w, kind="mergesort")[-k_eff:]
        out = np.zeros(n, dtype=bool)
        out[idx] = True
        return out
    raise ValueError(f"unknown winner_selection {choice!r}")


def assign_selection(
    players: pd.DataFrame,
    rng: np.random.Generator,
    *,
    n_selected: int,
    score_mode: str,
    loo_gap_weight: float,
    winner_selection: str,
) -> pd.DataFrame:
    """Mark K selected players (draft / tenure / promotion — domain-agnostic)."""
    out = add_poolq_loo(players)
    w = selection_weights(
        out, score_mode=score_mode, loo_gap_weight=loo_gap_weight
    )
    out["Y_selected"] = choose_selected(
        rng, w, int(n_selected), str(winner_selection)
    ).astype(int)
    out["selection_weight"] = w
    return out


# Legacy names (early 538 drafts)
promotion_weights = selection_weights
choose_promoted = choose_selected


def assign_promotion(
    players: pd.DataFrame,
    rng: np.random.Generator,
    *,
    n_promoted: int,
    score_mode: str,
    loo_gap_weight: float,
    winner_selection: str,
) -> pd.DataFrame:
    out = assign_selection(
        players,
        rng,
        n_selected=n_promoted,
        score_mode=score_mode,
        loo_gap_weight=loo_gap_weight,
        winner_selection=winner_selection,
    )
    out["Y_promoted"] = out["Y_selected"]
    out["promotion_weight"] = out["selection_weight"]
    return out


def roster_team_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Per-pool realized mean, SD, min, max of ability (530-style intervals)."""
    g = df.groupby("pool_id", sort=True)["ability"]
    out = g.agg(["mean", "std", "min", "max", "count"]).rename(
        columns={"mean": "pool_mean", "std": "pool_sd", "count": "roster_n"}
    )
    out["team_target"] = df.groupby("pool_id", sort=True)["team_target"].first()
    return out.reset_index()


def simulate_generative_rosters(
    params: AssignmentParams | None = None,
    *,
    rng: np.random.Generator | None = None,
    seed: int | None = 42,
    method: AssignmentMethod = "soft",
) -> tuple[pd.DataFrame, pd.DataFrame, np.ndarray]:
    """One full synthetic league draw.

    Returns
    -------
    players : DataFrame
        player_id, ability, pool_id, team_target
    teams : DataFrame
        per-pool summary (pool_mean, pool_sd, min, max, team_target, ...)
    team_targets : ndarray
        length n_teams — drawn T_j
    """
    if params is None:
        params = AssignmentParams.from_tier1_sim_config()
    if rng is None:
        rng = np.random.default_rng(seed)

    n = params.n_individuals
    ability = draw_abilities(
        rng,
        n,
        ability_draw=params.ability_draw,
        ability_mean=params.ability_mean,
        ability_sd=params.ability_sd,
        ability_clip_low=params.ability_clip_low,
        ability_clip_high=params.ability_clip_high,
        ability_student_t_df=params.ability_student_t_df,
        ability_student_t_scale=params.ability_student_t_scale,
    )
    team_targets = draw_target_means(
        rng,
        params.n_teams,
        target_mean_dist=params.target_mean_dist,
        target_mean_low=params.target_mean_low,
        target_mean_high=params.target_mean_high,
        target_mean_mu=params.target_mean_mu,
        target_mean_sigma=params.target_mean_sigma,
    )

    if method == "soft":
        pool_id = soft_assign(
            rng,
            ability,
            team_targets,
            params.roster_size,
            assignment_kernel=params.assignment_kernel,
            assignment_temperature=params.assignment_temperature,
            preferential_alpha=params.preferential_alpha,
            preferential_k=params.preferential_k,
        )
    elif method == "sort_chop":
        pool_id = assign_sort_chop_benchmark(
            rng,
            ability,
            params.n_teams,
            sorting_noise_sd=params.sorting_noise_sd,
        )
    else:
        raise ValueError(f"unknown method {method!r}")

    players = build_roster_dataframe(ability, pool_id, team_targets)
    teams = roster_team_stats(players)
    return players, teams, team_targets


def _smoke_compare_overlap() -> None:
    """Quick stdout check: soft assignment should raise interval overlap vs sort-chop."""
    params = AssignmentParams.from_tier1_sim_config()
    rng = np.random.default_rng(42)

    def coverage_peak(teams: pd.DataFrame, grid: np.ndarray) -> float:
        lo = teams["min"].to_numpy()
        hi = teams["max"].to_numpy()
        cov = np.zeros(len(grid), dtype=float)
        for a, b in zip(lo, hi):
            cov += (grid >= a) & (grid <= b)
        return float(cov.max())

    grid = np.linspace(-2.0, 2.0, 81)
    _, teams_soft, _ = simulate_generative_rosters(params, rng=rng, method="soft")
    _, teams_chop, _ = simulate_generative_rosters(params, rng=rng, method="sort_chop")
    peak_soft = coverage_peak(teams_soft, grid)
    peak_chop = coverage_peak(teams_chop, grid)
    med_sd_soft = float(teams_soft["pool_sd"].median())
    med_sd_chop = float(teams_chop["pool_sd"].median())
    print(
        f"soft: coverage_peak={peak_soft:.0f} median_pool_sd={med_sd_soft:.3f} | "
        f"sort_chop: coverage_peak={peak_chop:.0f} median_pool_sd={med_sd_chop:.3f}"
    )


if __name__ == "__main__":
    _smoke_compare_overlap()
