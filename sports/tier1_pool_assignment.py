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
TargetMeanDist = Literal["uniform", "normal_clipped", "empirical_530"]
AbilityDraw = Literal[
    "uniform_01",
    "beta_2_2",
    "normal_clipped",
    "normal_plus_student_t",
    "empirical_530",
]
AssignmentMethod = Literal["soft", "sort_chop"]
LooPoolLMode = Literal["quality", "crowding", "crowding_smooth"]

POOL_L_QUALITY_COL = "poolq_loo"  # L_Q — LOO mean teammate ability
POOL_L_CROWDING_COL = "pool_c_loo"  # L_C — LOO viable-peer share (count above θ / pool size)
POOL_L_CROWDING_SMOOTH_COL = "pool_c_smooth_loo"  # L_C smooth — LOO mean σ(γ(A−θ)) (539-style)
POOL_L_CROWDING_SUM_COL = "pool_c_loo_sum"  # legacy LOO sum (diagnostic)


def is_crowding_l_mode(mode: str) -> bool:
    m = str(mode).strip().lower()
    return m in (
        "crowding",
        "l_c",
        POOL_L_CROWDING_COL,
        "crowding_smooth",
        "smooth_crowding",
        "smooth",
        POOL_L_CROWDING_SMOOTH_COL,
    )


def pool_l_column(mode: str) -> str:
    """Column name for generative LOO pool regressor L (quality vs crowding)."""
    m = str(mode).strip().lower()
    if m in ("quality", "l_q", POOL_L_QUALITY_COL):
        return POOL_L_QUALITY_COL
    if m in ("crowding_smooth", "smooth_crowding", "smooth", POOL_L_CROWDING_SMOOTH_COL):
        return POOL_L_CROWDING_SMOOTH_COL
    if m in ("crowding", "l_c", POOL_L_CROWDING_COL):
        return POOL_L_CROWDING_COL
    raise ValueError(
        f"loo_pool_l_mode must be 'quality', 'crowding', or 'crowding_smooth', got {mode!r}"
    )


def pool_l_short_label(mode: str) -> str:
    """Plain-text label (matplotlib axes, sweep logs)."""
    m = str(mode).strip().lower()
    if m in ("crowding_smooth", "smooth_crowding", "smooth", POOL_L_CROWDING_SMOOTH_COL):
        return "L_C (smooth viability)"
    if m in ("crowding", "l_c", POOL_L_CROWDING_COL):
        return "L_C (viable share)"
    return "L_Q (LOO mean)"


def pool_l_html_label(mode: str) -> str:
    """HTML for widgets.HTML — real subscripts via <sub> (not Unicode modifier letters)."""
    m = str(mode).strip().lower()
    if m in ("crowding_smooth", "smooth_crowding", "smooth", POOL_L_CROWDING_SMOOTH_COL):
        return "L<sub>c</sub><sup>smooth</sup>"
    if m in ("crowding", "l_c", POOL_L_CROWDING_COL):
        return "L<sub>c</sub>"
    return "L<sub>q</sub>"


def pool_l_dropdown_options() -> list[tuple[str, str]]:
    """(display label, value) — mode name only; symbol shown in loo_l_hint_html."""
    return [
        ("Quality — LOO mean", "quality"),
        ("Crowding — viable share (A > θ)", "crowding"),
        ("Crowding — smooth viability (539)", "crowding_smooth"),
    ]


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
    assignment_rho: float
    assignment_sigma: float
    use_preferential_attachment: bool
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
    viability_theta: float = 0.7546158731868137
    """Viable-peer cutoff on synthetic ability (530 median drafted z)."""
    viability_sharpness: float = 18.0
    """Logistic sharpness γ for smooth viability σ(γ(A−θ)) (539 Alex sim)."""

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
            assignment_rho=float(getattr(mod, "ASSIGNMENT_RHO", 1.0)),
            assignment_sigma=float(
                getattr(mod, "ASSIGNMENT_SIGMA", mod.ASSIGNMENT_TEMPERATURE)
            ),
            use_preferential_attachment=bool(
                getattr(mod, "USE_PREFERENTIAL_ATTACHMENT", False)
            ),
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
            viability_theta=float(getattr(mod, "VIABILITY_THETA", 0.7546158731868137)),
            viability_sharpness=float(getattr(mod, "VIABILITY_SHARPNESS", 18.0)),
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
    if ability_draw == "beta_2_2":
        # 539 Alex sim: Beta(2,2) on [0,1], unimodal, mean 0.5
        return rng.beta(2.0, 2.0, size=n)
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
    if ability_draw == "empirical_530":
        from sports_pipeline.empirical_perf_fit import draw_empirical_abilities

        return draw_empirical_abilities(rng, n)
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
    if target_mean_dist == "empirical_530":
        from sports_pipeline.empirical_perf_fit import draw_empirical_abilities

        return draw_empirical_abilities(rng, n_teams)
    raise ValueError(f"unknown target_mean_dist {target_mean_dist!r}")


def _kernel_weights(
    ability_i: float,
    team_targets: np.ndarray,
    *,
    assignment_kernel: AssignmentKernel,
    assignment_rho: float = 1.0,
    assignment_sigma: float = 0.65,
    assignment_temperature: float | None = None,
) -> np.ndarray:
    """Soft-match weights. ρ=0 → uniform; ρ↑ → sharper match (540 assortativity).

    Legacy: pass ``assignment_temperature`` only (old τ parameterization).
    """
    delta = float(ability_i) - np.asarray(team_targets, dtype=float)
    if assignment_temperature is not None:
        tau = max(float(assignment_temperature), 1e-12)
        if assignment_kernel == "gaussian":
            return np.exp(-0.5 * (delta / tau) ** 2)
        if assignment_kernel == "cauchy":
            return 1.0 / (1.0 + (delta / tau) ** 2)
        raise ValueError(f"unknown assignment_kernel {assignment_kernel!r}")

    rho = float(assignment_rho)
    if rho <= 0.0:
        return np.ones(len(team_targets), dtype=float)
    sigma = max(float(assignment_sigma), 1e-12)
    z = delta / sigma
    if assignment_kernel == "gaussian":
        return np.exp(-0.5 * rho * z**2)
    if assignment_kernel == "cauchy":
        return 1.0 / (1.0 + rho * z**2)
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
    assignment_rho: float = 1.0,
    assignment_sigma: float = 0.65,
    assignment_temperature: float | None = None,
    preferential_alpha: float = 0.0,
    preferential_k: float = 1.0,
) -> np.ndarray:
    """Place each player on exactly one team with equal roster sizes.

    Sequential assignment on a random player order. For player i,
    pi_ij ∝ f(A_i - T_j) * (n_j + k)^alpha, zeroed for teams already at roster_size.

    Default kernel (540): exp(-ρ (A_i - T_j)² / (2σ²)); ρ=0 → uniform among open teams.
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
            assignment_rho=assignment_rho,
            assignment_sigma=assignment_sigma,
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


def _default_viability_theta() -> float:
    try:
        return float(
            AssignmentParams.from_tier1_sim_config().viability_theta
        )
    except Exception:
        return 0.7546158731868137


def _viability_logistic(ability: pd.Series, *, theta: float, gamma: float) -> pd.Series:
    """σ(γ(A−θ)) elementwise; NaN where ability is NaN."""
    a = pd.to_numeric(ability, errors="coerce")
    z = gamma * (a - theta)
    z = z.clip(-500.0, 500.0)
    return (1.0 / (1.0 + np.exp(-z))).where(a.notna(), np.nan)


def add_loo_pool_columns(
    players: pd.DataFrame,
    *,
    viability_theta: float | None = None,
    viability_sharpness: float = 18.0,
) -> pd.DataFrame:
    """Add L_Q (``poolq_loo``) and L_C leave-one-out teammate stats.

    ``pool_c_loo`` is the LOO *share* of teammates with ``ability > viability_theta``
    (viable-peer count / LOO pool size; same rule as empirical ``congestion_crowding``).
    ``pool_c_smooth_loo`` is LOO mean teammate viability σ(γ(A−θ)) (539 Option B).
    ``pool_c_loo_sum`` keeps the legacy LOO sum of teammate ability for diagnostics.
    """
    theta = (
        float(viability_theta)
        if viability_theta is not None
        else _default_viability_theta()
    )
    gamma = float(viability_sharpness)
    out = players.copy()
    g = out.groupby("pool_id", observed=True)["ability"]
    ssum = g.transform("sum")
    cnt = g.transform("count").astype(float)
    den = (cnt - 1.0).replace(0.0, np.nan)
    own = pd.to_numeric(out["ability"], errors="coerce")
    loo_sum = ssum - own
    out[POOL_L_CROWDING_SUM_COL] = loo_sum
    out[POOL_L_QUALITY_COL] = loo_sum / den

    above = (own > theta).astype(float)
    out["_above_theta"] = above
    sum_above = out.groupby("pool_id", observed=True)["_above_theta"].transform("sum")
    own_above = out["_above_theta"].where(own.notna(), np.nan)
    loo_count = sum_above - own_above.fillna(0.0)
    loo_count = loo_count.where(own.notna(), np.nan)
    # LOO pool size = roster count − 1 (exclude self), same denominator as L_Q
    loo_pool_n = (cnt - 1.0).replace(0.0, np.nan)
    loo_share = loo_count / loo_pool_n
    loo_share = loo_share.where(own.notna(), np.nan)
    loo_share = loo_share.where(cnt >= 2.0, np.nan)
    out[POOL_L_CROWDING_COL] = loo_share

    viability = _viability_logistic(out["ability"], theta=theta, gamma=gamma)
    out["_viability"] = viability
    sum_v = out.groupby("pool_id", observed=True)["_viability"].transform("sum")
    own_v = viability
    loo_smooth = (sum_v - own_v) / den
    loo_smooth = loo_smooth.where(own.notna(), np.nan)
    loo_smooth = loo_smooth.where(cnt >= 2.0, np.nan)
    out[POOL_L_CROWDING_SMOOTH_COL] = loo_smooth
    out = out.drop(columns=["_above_theta", "_viability"])
    return out


def add_poolq_loo(players: pd.DataFrame) -> pd.DataFrame:
    """Backward-compatible alias: adds both L_Q and L_C columns."""
    return add_loo_pool_columns(players)


def ability_on_unit_interval(ability: np.ndarray) -> bool:
    """True when synthetic A_i looks drawn on [0, 1] (539 beta/uniform), not z-scored."""
    finite = np.asarray(ability, dtype=float)
    finite = finite[np.isfinite(finite)]
    if finite.size == 0:
        return False
    return float(finite.min()) >= -0.05 and float(finite.max()) <= 1.05


def default_crowding_l_z_scale(ability: np.ndarray) -> float:
    """Map L_C ∈ [0, 1] to ability units when A_i is z-scored (530-style draws)."""
    finite = np.asarray(ability, dtype=float)
    finite = finite[np.isfinite(finite)]
    if finite.size < 10:
        return 4.0
    spread = float(np.nanpercentile(finite, 90) - np.nanpercentile(finite, 10))
    return spread if spread > 1e-6 else 4.0


def effective_l_for_selection(
    l_values: np.ndarray,
    ability: np.ndarray,
    *,
    pool_l_mode: str,
    l_term_scale: float | None = None,
) -> np.ndarray:
    """L term in the same units as ability for subtractive selection scores.

    L_Q (quality) is already in ability units. L_C crowding terms live on [0, 1];
    when ability is z-scored, multiply L_C by a spread factor so w·L is commensurate
    with A_i (539 uses both on [0, 1] and needs no scaling).
    """
    l = np.asarray(l_values, dtype=float)
    if not is_crowding_l_mode(pool_l_mode):
        return l
    if ability_on_unit_interval(ability):
        return l
    scale = (
        float(l_term_scale)
        if l_term_scale is not None and np.isfinite(l_term_scale) and l_term_scale > 0
        else default_crowding_l_z_scale(ability)
    )
    return l * scale


def selection_weights(
    players: pd.DataFrame,
    *,
    score_mode: str,
    loo_gap_weight: float,
    pool_l_mode: str = "quality",
    l_term_scale: float | None = None,
) -> np.ndarray:
    a = players["ability"].to_numpy(dtype=float)
    lcol = pool_l_column(pool_l_mode)
    q_raw = players[lcol].to_numpy(dtype=float)
    q = effective_l_for_selection(
        q_raw, a, pool_l_mode=pool_l_mode, l_term_scale=l_term_scale
    )
    mode = str(score_mode).strip().lower()
    if mode == "ability":
        w = a.copy()
    elif mode == "loo_gap_plus_ability":
        wgt = float(loo_gap_weight)
        w = wgt * (a - q) + (1.0 - wgt) * a
        w = np.where(np.isfinite(q_raw), w, a)
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


def resolve_crowding_l_z_scale(
    crowding_l_z_scale: float | None,
    *,
    pool_l_mode: str,
) -> float | None:
    """``l_term_scale`` for ``selection_weights`` (None → auto p90−p10 of A_i).

    Explicit positive ``crowding_l_z_scale`` wins. Otherwise reads
    ``CROWDING_L_Z_SCALE`` from ``tier1_sim_config.py`` when set and finite.
    """
    if crowding_l_z_scale is not None:
        val = float(crowding_l_z_scale)
        if np.isfinite(val) and val > 0:
            return val
        return None
    if not is_crowding_l_mode(pool_l_mode):
        return None
    try:
        mod = load_tier1_sim_config()
        raw = getattr(mod, "CROWDING_L_Z_SCALE", None)
        if raw is not None:
            val = float(raw)
            if np.isfinite(val) and val > 0:
                return val
    except (ImportError, OSError, TypeError, ValueError):
        pass
    return None


def assign_selection(
    players: pd.DataFrame,
    rng: np.random.Generator,
    *,
    n_selected: int,
    score_mode: str,
    loo_gap_weight: float,
    winner_selection: str,
    pool_l_mode: str = "quality",
    viability_theta: float | None = None,
    viability_sharpness: float | None = None,
    crowding_l_z_scale: float | None = None,
) -> pd.DataFrame:
    """Mark K selected players (draft / tenure / promotion — domain-agnostic).

    ``crowding_l_z_scale``: multiply L_C by this when ability is z-scored so w·L
    matches A_i units. ``None`` uses ``CROWDING_L_Z_SCALE`` from config, else auto
    p90−p10 spread of A_i. Ignored for [0,1] ability draws and quality (L_Q) mode.
    """
    gamma = (
        float(viability_sharpness)
        if viability_sharpness is not None
        else float(AssignmentParams.from_tier1_sim_config().viability_sharpness)
    )
    out = add_loo_pool_columns(
        players,
        viability_theta=viability_theta,
        viability_sharpness=gamma,
    )
    l_scale = resolve_crowding_l_z_scale(
        crowding_l_z_scale, pool_l_mode=pool_l_mode
    )
    w = selection_weights(
        out,
        score_mode=score_mode,
        loo_gap_weight=loo_gap_weight,
        pool_l_mode=pool_l_mode,
        l_term_scale=l_scale,
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
    pool_l_mode: str = "quality",
    viability_theta: float | None = None,
    viability_sharpness: float | None = None,
    crowding_l_z_scale: float | None = None,
) -> pd.DataFrame:
    out = assign_selection(
        players,
        rng,
        n_selected=n_promoted,
        score_mode=score_mode,
        loo_gap_weight=loo_gap_weight,
        winner_selection=winner_selection,
        pool_l_mode=pool_l_mode,
        viability_theta=viability_theta,
        viability_sharpness=viability_sharpness,
        crowding_l_z_scale=crowding_l_z_scale,
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
    ability: np.ndarray | None = None,
    team_targets: np.ndarray | None = None,
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
    if ability is None:
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
    else:
        ability = np.asarray(ability, dtype=float)
        if len(ability) != n:
            raise ValueError(f"len(ability)={len(ability)} != n_individuals={n}")
    if team_targets is None:
        team_targets = draw_target_means(
            rng,
            params.n_teams,
            target_mean_dist=params.target_mean_dist,
            target_mean_low=params.target_mean_low,
            target_mean_high=params.target_mean_high,
            target_mean_mu=params.target_mean_mu,
            target_mean_sigma=params.target_mean_sigma,
        )
    else:
        team_targets = np.asarray(team_targets, dtype=float)
        if len(team_targets) != params.n_teams:
            raise ValueError(
                f"len(team_targets)={len(team_targets)} != n_teams={params.n_teams}"
            )

    pref_alpha = (
        float(params.preferential_alpha)
        if params.use_preferential_attachment
        else 0.0
    )

    if method == "soft":
        pool_id = soft_assign(
            rng,
            ability,
            team_targets,
            params.roster_size,
            assignment_kernel=params.assignment_kernel,
            assignment_rho=params.assignment_rho,
            assignment_sigma=params.assignment_sigma,
            preferential_alpha=pref_alpha,
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
