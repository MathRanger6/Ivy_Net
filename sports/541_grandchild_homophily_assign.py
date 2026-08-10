"""541 — Grandchild ASSIGN: endogenous-centroid homophilic stub matching.

Experimental ASSIGN arm (PD18 / VECTOR Aug 2026). Parent and Child paths in
``tier1_pool_assignment.py`` are unchanged.

One-shot sequential assignment:
  - All teams start with mu_j = mu_0 = mean(A), R_j = C.
  - Each player i samples team j with weight R_j * exp(-rho * |A_i - mu_j|).
  - After seating, update that team's centroid from actual members only.
  - First player on an empty team: mu_j <- A_i (mu_0 is not a pseudo-player).

Lineage: Fosdick et al. stub capacity R_j; Quayle et al. exponential homophily;
combined rule is project synthesis (see VECTOR_work COMPASS_DETAILED_ASSIGN_*).

Call from ASSIGN via ``simulate_generative_rosters(..., method="grandchild")`` or
``grandchild_assign`` directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# --- Empirical MBB defaults (2015 season) ------------------------------------
EMPIRICAL_SEASON_DEFAULT = 2015
ROSTER_SIZE_DEFAULT = 15


@dataclass(frozen=True)
class GrandchildAssignResult:
    """One stochastic formation run."""

    pool_id: np.ndarray
    ability: np.ndarray
    roster_size: int
    rho: float
    mu_initial: float
    mu_final: np.ndarray
    n_teams: int
    seed: int | None
    within_team_mse: float
    sorting_index_h: float
    centroid_sd: float


def _normalize_probs(weights: np.ndarray) -> np.ndarray:
    w = np.asarray(weights, dtype=float)
    w = np.where(np.isfinite(w), w, 0.0)
    w = np.clip(w, 0.0, None)
    total = float(w.sum())
    if total <= 0.0:
        raise ValueError("non-positive total assignment weight")
    return w / total


def grandchild_homophily_weights(
    ability_i: float,
    mu: np.ndarray,
    remaining: np.ndarray,
    rho: float,
) -> np.ndarray:
    """Unnormalized stub weights w_ij = R_j * exp(-rho * |A_i - mu_j|) for open teams."""
    r = np.asarray(remaining, dtype=float)
    m = np.asarray(mu, dtype=float)
    dist = np.abs(float(ability_i) - m)
    w = r * np.exp(-float(rho) * dist)
    return np.where(r > 0.0, w, 0.0)


def grandchild_assign(
    rng: np.random.Generator,
    ability: np.ndarray,
    roster_size: int,
    *,
    rho: float = 1.0,
    n_teams: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Run one Grandchild formation pass.

    Returns
    -------
    pool_id : int64 array, shape (n_players,)
    mu_final : float array, shape (n_teams,) — final team centroids
    """
    ability = np.asarray(ability, dtype=float)
    n_players = len(ability)
    c = int(roster_size)
    if n_teams is None:
        if n_players % c != 0:
            raise ValueError(
                f"len(ability)={n_players} must be divisible by roster_size={c}"
            )
        n_teams = n_players // c
    else:
        expected = int(n_teams) * c
        if n_players != expected:
            raise ValueError(
                f"len(ability)={n_players} != n_teams*roster_size={expected}"
            )

    mu_0 = float(np.mean(ability))
    mu = np.full(int(n_teams), mu_0, dtype=float)
    remaining = np.full(int(n_teams), c, dtype=float)
    counts = np.zeros(int(n_teams), dtype=np.int64)
    pool_id = np.full(n_players, -1, dtype=np.int64)

    for i in rng.permutation(n_players):
        w = grandchild_homophily_weights(ability[i], mu, remaining, rho)
        if float(w.sum()) <= 0.0:
            open_idx = np.flatnonzero(remaining > 0.0)
            if open_idx.size == 0:
                raise RuntimeError("grandchild_assign: no open roster slots")
            w = np.zeros(int(n_teams), dtype=float)
            w[open_idx] = 1.0
        j = int(rng.choice(int(n_teams), p=_normalize_probs(w)))
        n_before = int(counts[j])
        pool_id[i] = j
        counts[j] += 1
        remaining[j] -= 1.0
        if n_before == 0:
            mu[j] = float(ability[i])
        else:
            mu[j] = (n_before * mu[j] + float(ability[i])) / (n_before + 1)

    validate_grandchild_assignment(
        ability,
        pool_id,
        mu,
        remaining,
        roster_size=c,
        rho=rho,
        mu_initial=mu_0,
    )
    return pool_id, mu.copy()


def validate_grandchild_assignment(
    ability: np.ndarray,
    pool_id: np.ndarray,
    mu_final: np.ndarray,
    remaining: np.ndarray,
    *,
    roster_size: int,
    rho: float,
    mu_initial: float,
) -> None:
    """Lightweight asserts from VECTOR §9 validation locks."""
    ability = np.asarray(ability, dtype=float)
    pool_id = np.asarray(pool_id, dtype=np.int64)
    mu_final = np.asarray(mu_final, dtype=float)
    remaining = np.asarray(remaining, dtype=float)
    n_players = len(ability)
    n_teams = len(mu_final)
    c = int(roster_size)

    if np.any(pool_id < 0):
        raise AssertionError("unassigned players remain")
    if pool_id.size != n_players:
        raise AssertionError("pool_id length mismatch")
    counts = np.bincount(pool_id, minlength=n_teams)
    if not np.all(counts == c):
        raise AssertionError(f"uneven rosters: {counts}")
    if float(remaining.sum()) != 0.0:
        raise AssertionError(f"remaining stubs not zero: {remaining.sum()}")
    if not np.all(remaining == 0.0):
        raise AssertionError("remaining capacity not zero on all teams")

    mu_0 = float(np.mean(ability))
    if abs(mu_0 - float(mu_initial)) > 1e-12:
        raise AssertionError("mu_initial != mean(ability)")

    if float(rho) == 0.0:
        # Spot-check: weights proportional to R_j only (uniform among open).
        rng = np.random.default_rng(0)
        test_mu = np.full(n_teams, mu_0)
        test_rem = np.full(n_teams, float(c), dtype=float)
        w = grandchild_homophily_weights(ability[0], test_mu, test_rem, 0.0)
        if not np.allclose(w, test_rem):
            raise AssertionError("rho=0 weights should equal remaining stubs")

    # Recompute centroids from rosters; match mu_final.
    for j in range(n_teams):
        members = ability[pool_id == j]
        if len(members) != c:
            raise AssertionError(f"team {j} roster size {len(members)} != {c}")
        expected_mu = float(members.mean())
        if abs(expected_mu - mu_final[j]) > 1e-9:
            raise AssertionError(
                f"team {j} centroid mismatch: stored={mu_final[j]}, mean={expected_mu}"
            )


def within_team_mse(ability: np.ndarray, pool_id: np.ndarray, mu_final: np.ndarray) -> float:
    """D — within-team MSE (not assortativity)."""
    mu_player = mu_final[np.asarray(pool_id, dtype=np.int64)]
    return float(np.mean((ability - mu_player) ** 2))


def sorting_index_h(ability: np.ndarray, pool_id: np.ndarray, mu_final: np.ndarray) -> float:
    """H — normalized sorting / explained-variance-style index."""
    mu_player = mu_final[np.asarray(pool_id, dtype=np.int64)]
    num = float(np.sum((ability - mu_player) ** 2))
    den = float(np.sum((ability - np.mean(ability)) ** 2))
    if den <= 0.0:
        return float("nan")
    return 1.0 - num / den


def centroid_dispersion_sd(mu_final: np.ndarray) -> float:
    return float(np.std(mu_final, ddof=0))


def run_one_realization(
    ability: np.ndarray,
    roster_size: int,
    rho: float,
    *,
    rng: np.random.Generator | None = None,
    seed: int | None = None,
) -> GrandchildAssignResult:
    if rng is None:
        rng = np.random.default_rng(seed)
    pool_id, mu_final = grandchild_assign(
        rng, ability, roster_size, rho=rho
    )
    d = within_team_mse(ability, pool_id, mu_final)
    h = sorting_index_h(ability, pool_id, mu_final)
    return GrandchildAssignResult(
        pool_id=pool_id,
        ability=np.asarray(ability, dtype=float),
        roster_size=int(roster_size),
        rho=float(rho),
        mu_initial=float(np.mean(ability)),
        mu_final=mu_final,
        n_teams=len(mu_final),
        seed=seed,
        within_team_mse=d,
        sorting_index_h=h,
        centroid_sd=centroid_dispersion_sd(mu_final),
    )


def load_empirical_abilities_season(
    season: int = EMPIRICAL_SEASON_DEFAULT,
    *,
    repo_root: Path | None = None,
) -> tuple[np.ndarray, dict[str, Any]]:
    """Load PPM z within-season abilities for one NCAA season (530/PD17 panel)."""
    repo = repo_root or Path(__file__).resolve().parents[1]
    scripts = repo / "scripts"
    import sys

    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    from empirical_team_interval_overlap import _prepare_panel

    panel = _prepare_panel()
    work = panel.loc[panel["season"] == int(season)].copy()
    work = work.dropna(subset=["perf"])
    work["perf"] = pd.to_numeric(work["perf"], errors="coerce")
    work = work.dropna(subset=["perf"])
    abilities = work["perf"].to_numpy(dtype=float)
    meta = {
        "season": int(season),
        "n_players": int(len(abilities)),
        "n_teams_empirical": int(work["team_id"].nunique()),
        "perf": "PPM z within season",
        "mean": float(abilities.mean()),
        "std": float(abilities.std()),
    }
    return abilities, meta


def assignment_params_for_abilities(
    ability: np.ndarray,
    roster_size: int = ROSTER_SIZE_DEFAULT,
):
    """Build AssignmentParams for full-capacity Grandchild run."""
    from dataclasses import replace

    import tier1_pool_assignment as tpa

    n_players = len(ability)
    c = int(roster_size)
    if n_players % c != 0:
        raise ValueError(
            f"N={n_players} not divisible by C={c}; trim or pad before assign"
        )
    n_teams = n_players // c
    base = tpa.AssignmentParams.from_tier1_sim_config()
    return replace(
        base,
        n_teams=n_teams,
        roster_size=c,
    )


def _self_test() -> None:
    """Quick validation on small synthetic league."""
    rng = np.random.default_rng(42)
    n_teams, c = 8, 5
    ability = rng.normal(size=n_teams * c)
    for rho in (0.0, 0.5, 4.0, 16.0):
        res = run_one_realization(ability, c, rho, rng=rng)
        assert res.within_team_mse >= 0.0
        assert np.isfinite(res.sorting_index_h)
    print("541_grandchild_homophily_assign: self_test OK")


if __name__ == "__main__":
    _self_test()
