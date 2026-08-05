"""Generative pool assignment + score/select helpers for Tier 1 / **540 re-entry**.

==============================================================================
FOR LATER CHARLES — read this like a notebook CELL map
==============================================================================
Daily path: 540_READ_ME_SIM.md + hero_model_reset_bundle / 540_rho_ablation_bundle.
Plain English: 3-Master_Plan/re_entry/04_Pass_A_and_Pass_B_in_Plain_English.md

------------------------------------------------------------------------------
READ-FIRST GLOSSARY — every symbol below is defined HERE before it is used.
Do not skip this block. Later sections assume you already know these words.
------------------------------------------------------------------------------

WHAT THIS FILE BUILDS
  A *synthetic* (made-up) basketball-like league: fake players, fake teams,
  fake “who gets selected.” It is NOT the empirical hero plot. The hero uses
  real college data; this engine invents data so we can turn knobs (Pass A/B).

THREE STEPS (always in this order)
  (1) ASSIGN  — put each fake player on exactly one team.
  (2) SCORE   — give each player a ranking number S_i (higher = better for selection).
  (3) SELECT  — pick the winners from those scores (usually the top K).

  Important: SCORE ≠ SELECT. Ranking first, then a winner rule.

CORE LETTERS (people / teams / score)
  A_i   — ability of player i. A made-up talent number we draw from a distribution.
  T_j   — team target for team j. One number per team; soft assignment tries to
          seat players whose A is near that team’s T.
  pool  — same idea as “team” / roster group. pool_id = which team a player sits on.
  S_i   — selection *score* (ranking weight) for player i. Used only to rank people.
  K     — how many people get selected (N_SELECTED in config). “Top K” = the K
          highest S_i values under the default winner rule.
  Y_selected — 0/1 outcome after SELECT (1 = got the slot).

POOL STATISTIC L (what enters the SCORE beside ability)
  L     — a leave-one-out *pool* number for each player: something about their
          teammates, not about the whole league.
  LOO   — leave-one-out: when computing L for player i, exclude i themselves so
          their own ability does not inflate their pool measure.
  L_Q   — “quality” L = mean teammate ability (column poolq_loo). Same units as A.
          This is the sim analog of the hero plot’s X-axis idea (pool quality).
  L_C   — “crowding” L = how packed the roster is with high-ability / “viable”
          teammates. Lives on [0, 1]. Two flavors:
            hard   — share of teammates with A > θ          (column pool_c_loo)
            smooth — mean of soft viability σ(γ(A−θ))       (column pool_c_smooth_loo)
  θ (theta) — viability cutline: ability above θ counts as a “viable peer.”
  γ (gamma) — sharpness of the soft viability curve (large γ ≈ hard step at θ).

SCORE FORMULA (Pass A lives here)
  Talent-only:     S_i = A_i
  With pool L:     S_i = A_i − w · L_i
  w               — weight on the L piece (code name: loo_gap_weight).
  λ (lambda)      — Alex’s name for that same weight in the nesting
                    S = A − λ·L_C. In this file, w ≈ λ.
  l_term_scale    — NAME DECODE (do not wait for §6):
                      l     = pool L (the L above)
                      term  = the L-*term* in S = A − w·L  (the piece that involves L)
                      scale = multiplier so that L-term is in the same units as A
                    Why needed: L_C is on [0,1]; z-scored A is ~−2.5…3.5. Without
                    a scale, w·L_C is tiny and congestion barely moves rankings.
                    Config twin name: CROWDING_L_Z_SCALE (same idea).

ASSIGNMENT KNOBS (Pass B lives here)
  soft assignment — probabilistic seating: prefer teams with T_j near A_i, but
                    allow overlap (real college talent windows overlap).
  ρ (rho)         — assortativity strength in soft assignment. 0 ≈ random among
                    open seats; larger ρ ≈ sharper “sit near your T.”
                    NOT the same as λ/w (those are SCORE weights).
  σ (sigma)       — length-scale in the soft kernel (ability units; default ~0.65).
  τ (tau)         — *legacy* temperature knob (old code). Small τ ≈ assortative.
                    Prefer ρ in 540 work; τ is kept so old notebooks still run.
  sort-and-chop   — sort everyone by ability, cut into equal team slices.
                    Almost no overlap (diagnostic / extreme arm). NOT “ρ → ∞.”
  preferential attachment — optional rich-get-richer on seats already filling
                    (off for 540 unless you turn the flag on).

SELECT / WINNER RULE
  choice "C" — deterministic top K by S_i  ← default for Pass A and Pass B.
  choice "A"/"B" — older stochastic rules (kept for 537-era experiments).

PASS A vs PASS B (what each experiment toggles)
  Pass A — same assignment; change the SCORE (talent-only vs A − w·L_C).
  Pass B — same score rule; change ASSIGN only (ρ / soft vs sort-and-chop).

OTHER SHORT WORDS YOU WILL SEE
  z-scored / z-ish — A drawn on a roughly Normal/clipped scale (530-style), not [0,1].
  unit interval    — A drawn on [0,1] (539 beta/uniform). Then L_C needs no scale.
  coverage / overlap — how much team ability ranges overlap (smoke test: soft ≫ chop).
  kernel           — the soft-match weight formula (gaussian or cauchy) from A to each T.

SECTION MAP (scroll by banner — terms above already defined)
  0. Types & column names
  1. LOO mode helpers (which L column: quality vs crowding)
  2. AssignmentParams — knobs loaded from tier1_sim_config.py
  3. Draw abilities A_i and team targets T_j
  4. ASSIGN — soft_assign / sort-and-chop / build roster table
  5. LOO pool stats — build L_Q and L_C columns on the roster table
  6. SCORE — selection_weights (talent-only vs A − w·L); applies l_term_scale
  7. SELECT — choose_selected / assign_selection
  8. One-shot league — simulate_generative_rosters (ASSIGN only)
  9. Smoke test (soft overlap vs sort-and-chop)

Both Pass A and Pass B call into this file via tier1_generative_eda.run_inverted_u_pipeline.

Legacy UI: tier1_cell10_playground_run.py (do not use for daily re-entry).
Design / overlap forensics: documents/Tier1_Presorting_Design_Note.md
Defaults: tier1_sim_config.py
==============================================================================
"""

from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import numpy as np
import pandas as pd

# =============================================================================
# 0. TYPES & COLUMN NAMES
# =============================================================================
# These Literals document the allowed strings in config / Pass A–B knobs.
# Column constants are the names written onto the players DataFrame after LOO.
#
# Think of this like 530 CELL 2: every name below is a *setting label*, not math
# you have to re-derive. If a string shows up in tier1_sim_config.py or a Pass A/B
# arm, it must be one of these allowed values.
#
# Symbols A_i, T_j, L, LOO, ρ, λ/w, θ, γ, l_term_scale are defined in the
# module docstring READ-FIRST GLOSSARY above — read that before this section.

# AssignmentKernel: shape of soft-match preference for team target T_j near A_i.
#   "gaussian" — default; smooth falloff  exp(−ρ (A−T)² / (2σ²))
#   "cauchy"   — heavier tails (player still has weight far from T_j)
AssignmentKernel = Literal["gaussian", "cauchy"]

# TargetMeanDist: how we draw each team's fixed target mean T_j (one number per team).
#   Soft assignment seats players near T_j ≈ A_i; T_j is NOT real college means unless
#   you choose empirical_530.
TargetMeanDist = Literal["uniform", "normal_clipped", "empirical_530"]

# AbilityDraw: how we invent latent talent A_i for each synthetic player.
#   If A is z-ish and SCORE later subtracts crowding L (on [0,1]), the score step
#   multiplies L by l_term_scale (defined in the READ-FIRST GLOSSARY above).
AbilityDraw = Literal[
    "uniform_01",              # A ~ U(0,1) — 539-style unit interval
    "beta_2_2",                # A ~ Beta(2,2) on [0,1] — unimodal around 0.5
    "normal_clipped",          # A ~ Normal, clipped — 530-style z-ish (default for 540)
    "normal_plus_student_t",   # normal + Student-t noise — occasional stars/busts
    "empirical_530",           # resample from fitted empirical college perf
]

# AssignmentMethod: how players land on teams (Pass B toggles this / ρ).
#   "soft"      — probabilistic match to T_j (overlapping talent windows)
#   "sort_chop" — sort by ability, chop into equal slices (disjoint; diagnostic)
AssignmentMethod = Literal["soft", "sort_chop"]

# LooPoolLMode: which leave-one-out pool statistic enters the SCORE as "L".
#   "quality"         — L_Q = mean teammate ability (hero X-axis analog)
#   "crowding"        — L_C hard = share of teammates with A > θ
#   "crowding_smooth" — L_C soft = mean teammate σ(γ(A−θ)); Pass A congestion arm
LooPoolLMode = Literal["quality", "crowding", "crowding_smooth"]

# --- Column names written onto the players DataFrame after LOO -----------------
# L_Q — leave-one-out mean teammate ability (hero X-axis analog in sim)
POOL_L_QUALITY_COL = "poolq_loo"
# L_C hard — LOO share of teammates with ability > θ  (lives on [0, 1])
POOL_L_CROWDING_COL = "pool_c_loo"
# L_C smooth — LOO mean of σ(γ(A−θ)); Pass A congestion arm uses this ([0, 1])
POOL_L_CROWDING_SMOOTH_COL = "pool_c_smooth_loo"
# L_C smooth — team-level (PD16): mean σ(γ(A−θ)) over full roster, broadcast to all players
POOL_L_CROWDING_SMOOTH_TEAM_COL = "pool_c_smooth_team"
# Legacy diagnostic — LOO *sum* of teammate ability (not the default score input)
POOL_L_CROWDING_SUM_COL = "pool_c_loo_sum"


# =============================================================================
# 1. LOO MODE HELPERS
# =============================================================================
# Map human / config strings ("quality", "crowding_smooth", …) → DataFrame columns
# and plot labels. Used when building the SCORE (which L enters S_i).


def is_crowding_l_mode(mode: str) -> bool:
    """True if mode refers to an L_C crowding measure (needs unit scaling vs z-scored A)."""
    m = str(mode).strip().lower()
    return m in (
        "crowding",
        "l_c",
        POOL_L_CROWDING_COL,
        "crowding_smooth",
        "smooth_crowding",
        "smooth",
        POOL_L_CROWDING_SMOOTH_COL,
        "crowding_smooth_team",
        "team_smooth",
        POOL_L_CROWDING_SMOOTH_TEAM_COL,
    )


def pool_l_column(mode: str) -> str:
    """Return the players DataFrame column name for the chosen LOO pool L.

    quality         → poolq_loo
    crowding        → pool_c_loo          (hard viable share)
    crowding_smooth → pool_c_smooth_loo   (Pass A / Alex smooth L_C, LOO)
    crowding_smooth_team → pool_c_smooth_team (PD16 team L_C — same for whole roster)
    """
    m = str(mode).strip().lower()
    if m in ("quality", "l_q", POOL_L_QUALITY_COL):
        return POOL_L_QUALITY_COL
    if m in (
        "crowding_smooth_team",
        "team_smooth",
        "team_crowding_smooth",
        POOL_L_CROWDING_SMOOTH_TEAM_COL,
    ):
        return POOL_L_CROWDING_SMOOTH_TEAM_COL
    if m in ("crowding_smooth", "smooth_crowding", "smooth", POOL_L_CROWDING_SMOOTH_COL):
        return POOL_L_CROWDING_SMOOTH_COL
    if m in ("crowding", "l_c", POOL_L_CROWDING_COL):
        return POOL_L_CROWDING_COL
    raise ValueError(
        f"loo_pool_l_mode must be 'quality', 'crowding', 'crowding_smooth', "
        f"or 'crowding_smooth_team', got {mode!r}"
    )


def pool_l_short_label(mode: str) -> str:
    """Plain-text label for matplotlib axes / sweep logs."""
    m = str(mode).strip().lower()
    if m in ("crowding_smooth", "smooth_crowding", "smooth", POOL_L_CROWDING_SMOOTH_COL):
        return "L_C (smooth viability, LOO)"
    if m in (
        "crowding_smooth_team",
        "team_smooth",
        POOL_L_CROWDING_SMOOTH_TEAM_COL,
    ):
        return "L_C (smooth viability, team)"
    if m in ("crowding", "l_c", POOL_L_CROWDING_COL):
        return "L_C (viable share)"
    return "L_Q (LOO mean)"


def pool_l_html_label(mode: str) -> str:
    """HTML for widgets.HTML — real subscripts via <sub> (legacy CELL 10 UI)."""
    m = str(mode).strip().lower()
    if m in ("crowding_smooth", "smooth_crowding", "smooth", POOL_L_CROWDING_SMOOTH_COL):
        return "L<sub>c</sub><sup>smooth</sup>"
    if m in ("crowding", "l_c", POOL_L_CROWDING_COL):
        return "L<sub>c</sub>"
    return "L<sub>q</sub>"


def pool_l_dropdown_options() -> list[tuple[str, str]]:
    """(display label, value) for legacy widget dropdowns."""
    return [
        ("Quality — LOO mean", "quality"),
        ("Crowding — viable share (A > θ)", "crowding"),
        ("Crowding — smooth viability (539)", "crowding_smooth"),
    ]


# =============================================================================
# 2. AssignmentParams — ONE BUNDLE OF KNOBS FOR A LEAGUE DRAW
# =============================================================================
# Mirrors sports/tier1_sim_config.py. Pass A/B bundles load this, then replace()
# individual fields (e.g. assignment_rho for Pass B arms).


@dataclass(frozen=True)
class AssignmentParams:
    """Knobs for one generative roster draw (mirror tier1_sim_config.py).

    ASSIGN knobs: n_teams, roster_size, target means, kernel, ρ, σ, preferential.
    Ability knobs: which distribution for A_i.
    Viability knobs: θ, γ for smooth L_C (used later in SCORE, stored here for convenience).

    Field-by-field (530 CELL 2 style) — what each knob *is*:
      n_teams / roster_size — league size; total players = product (equal rosters).
      target_mean_*         — distribution + range for team targets T_j.
      assignment_kernel     — gaussian vs cauchy soft-match shape.
      assignment_temperature— legacy τ (small = assortative). Prefer ρ below.
      assignment_rho        — 540 assortativity ρ (Pass B knob). 0 = uniform among open.
      assignment_sigma      — fixed length-scale σ in the soft kernel (default ~0.65).
      use_preferential_*    — optional rich-get-richer on open seats (off for 540).
      ability_*             — how A_i is drawn and clipped.
      sorting_noise_sd      — only for sort_chop: noise added before the sort.
      viability_theta       — θ cutline for “viable peer” (L_C); 530 median drafted z.
      viability_sharpness   — γ in soft viability σ(γ(A−θ)); larger = sharper step.
    """

    # --- League geometry -------------------------------------------------------
    n_teams: int
    # n_teams: how many synthetic teams (pools) in this fake league.
    roster_size: int
    # roster_size: how many players sit on every team (fixed equal rosters).

    # --- Team targets T_j (what soft assignment aims at) -----------------------
    target_mean_dist: TargetMeanDist
    # target_mean_dist: which family draws T_j (uniform / normal_clipped / empirical).
    target_mean_low: float
    # target_mean_low: lower clip / uniform low for T_j.
    target_mean_high: float
    # target_mean_high: upper clip / uniform high for T_j.
    target_mean_mu: float
    # target_mean_mu: mean of T_j when target_mean_dist == "normal_clipped".
    target_mean_sigma: float
    # target_mean_sigma: SD of T_j when target_mean_dist == "normal_clipped".

    # --- Soft assignment kernel (Pass B lives here via ρ) ----------------------
    assignment_kernel: AssignmentKernel
    # assignment_kernel: "gaussian" (default) or "cauchy".
    assignment_temperature: float
    # assignment_temperature: legacy τ. Small τ = strong assortativity.
    #   Prefer assignment_rho + assignment_sigma in new / 540 code.
    assignment_rho: float
    # assignment_rho: 540 user-facing assortativity ρ (Pass B). 0 → flat among open seats;
    #   larger ρ → sharper preference for T_j near A_i. NOT the same as λ / w in SCORE.
    assignment_sigma: float
    # assignment_sigma: fixed scale σ in soft kernel (default ~0.65 on ability units).
    use_preferential_attachment: bool
    # use_preferential_attachment: if True, multiply kernel by (n_j+k)^α (rich-get-richer).
    preferential_alpha: float
    # preferential_alpha: α in preferential attachment (ignored when flag is False).
    preferential_k: float
    # preferential_k: k in (n_j + k)^α — keeps empty teams from going to weight 0.

    # --- Latent ability A_i ----------------------------------------------------
    ability_draw: AbilityDraw
    # ability_draw: which distribution invents A_i (see AbilityDraw comments above).
    ability_mean: float
    # ability_mean: location for normal_* draws.
    ability_sd: float
    # ability_sd: scale for normal_* draws.
    ability_clip_low: float
    # ability_clip_low: hard floor after draw (normal_* paths).
    ability_clip_high: float
    # ability_clip_high: hard ceiling after draw (normal_* paths).
    ability_student_t_df: float
    # ability_student_t_df: degrees of freedom for Student-t add-on noise.
    ability_student_t_scale: float
    # ability_student_t_scale: multiplier on Student-t noise (0 = off).

    # --- Sort-and-chop + viability (L_C) ---------------------------------------
    sorting_noise_sd: float = 0.0
    # sorting_noise_sd: ONLY for sort_chop — SD of noise added to ability before sorting.
    #   0 = pure ability order (537-style hard slices).
    viability_theta: float = 0.7546158731868137
    # viability_theta (θ): ability cutline for “viable peer.” Used when building L_C.
    #   Default ≈ 530 median drafted performance on z scale.
    viability_sharpness: float = 18.0
    # viability_sharpness (γ): logistic sharpness in soft viability σ(γ(A−θ)).
    #   Large γ ≈ hard step at θ; small γ = gradual. Used for crowding_smooth.

    @property
    def n_individuals(self) -> int:
        """Total synthetic players = teams × roster size (fixed equal rosters)."""
        return int(self.n_teams) * int(self.roster_size)

    @classmethod
    def from_module(cls, mod: Any) -> AssignmentParams:
        """Build params from an already-imported config module object."""
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
        """Load sports/tier1_sim_config.py from disk and build AssignmentParams."""
        cfg_path = path or Path(__file__).resolve().parent / "tier1_sim_config.py"
        spec = importlib.util.spec_from_file_location("tier1_sim_config", cfg_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"cannot load tier1_sim_config from {cfg_path}")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return cls.from_module(mod)


def load_tier1_sim_config(path: Path | None = None) -> Any:
    """Load sports/tier1_sim_config.py as a module (same pattern as 537 + sim_config).

    Returns the module object so callers can also read selection knobs
    (N_SELECTED, SELECTION_SCORE_MODE, …) that live beside AssignmentParams.
    """
    cfg_path = path or Path(__file__).resolve().parent / "tier1_sim_config.py"
    spec = importlib.util.spec_from_file_location("tier1_sim_config", cfg_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load tier1_sim_config from {cfg_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# =============================================================================
# 3. DRAW ABILITIES A_i AND TEAM TARGETS T_j
# =============================================================================
# Step 0 of assignment: create the talent deck and the team "targets."
# Pass B reuses the SAME A_i / T_j across arms; only placement changes.


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
    """Draw latent ability A_i for n synthetic players.

    What A_i *is*: a made-up talent number for each fake player. It is NOT taken
    from the empirical hero panel unless ability_draw == "empirical_530".

    Args (CELL 2 style)
      rng                 — NumPy Generator (caller owns the seed).
      n                   — how many players to invent (= n_teams × roster_size).
      ability_draw        — which distribution (see AbilityDraw comments in §0).
      ability_mean / sd   — location/scale for normal_* draws.
      ability_clip_*      — hard floor/ceiling after normal_* draws.
      ability_student_t_* — df + scale for optional heavy-tail add-on.

    Common choices
      normal_clipped        — z-ish scale (530-style); needs l_term_scale with L_C
      beta_2_2 / uniform_01 — [0,1] (539-style); L_C needs no extra scale
      normal_plus_student_t — heavier tails (occasional stars / busts)
      empirical_530         — resample from fitted empirical perf (optional)
    """
    if ability_draw == "uniform_01":
        return rng.uniform(0.0, 1.0, size=n)
    if ability_draw == "beta_2_2":
        # 539 Alex sim: Beta(2,2) on [0,1], unimodal, mean 0.5
        return rng.beta(2.0, 2.0, size=n)
    if ability_draw == "normal_clipped":
        # Clip keeps extreme z draws from blowing up soft kernels / plots.
        return np.clip(
            rng.normal(loc=ability_mean, scale=ability_sd, size=n),
            ability_clip_low,
            ability_clip_high,
        )
    if ability_draw == "normal_plus_student_t":
        # Base normal, then optional Student-t bumps for fat tails.
        base = rng.normal(loc=ability_mean, scale=ability_sd, size=n)
        if ability_student_t_scale > 0 and ability_student_t_df > 0:
            noise = rng.standard_t(df=ability_student_t_df, size=n)
            base = base + ability_student_t_scale * noise
        return np.clip(base, ability_clip_low, ability_clip_high)
    if ability_draw == "empirical_530":
        # Optional: pull A_i from the fitted empirical college-perf distribution.
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
    """Draw fixed team target means T_j (length n_teams).

    What T_j *is*: one number per team — the “ideal seat” soft assignment aims at.
    Soft assignment tries to put player i on teams whose T_j ≈ A_i.

    We do NOT copy real college means into T_j for the minimal cross-domain story
    (Alex); ranges are calibrated so overlap / SD look plausible vs 530 forensics.

    Args
      n_teams           — length of the returned T vector.
      target_mean_dist  — uniform / normal_clipped / empirical_530.
      target_mean_low/high — bounds (uniform range, or clip for normal).
      target_mean_mu/sigma — normal_clipped location/scale.
    """
    if target_mean_dist == "uniform":
        return rng.uniform(target_mean_low, target_mean_high, size=n_teams)
    if target_mean_dist == "normal_clipped":
        raw = rng.normal(loc=target_mean_mu, scale=target_mean_sigma, size=n_teams)
        return np.clip(raw, target_mean_low, target_mean_high)
    if target_mean_dist == "empirical_530":
        from sports_pipeline.empirical_perf_fit import draw_empirical_abilities

        return draw_empirical_abilities(rng, n_teams)
    raise ValueError(f"unknown target_mean_dist {target_mean_dist!r}")


# =============================================================================
# 4. ASSIGN — SOFT MATCH (ρ) OR SORT-AND-CHOP BENCHMARK
# =============================================================================
# This is generative step (1). Pass B varies ρ / method here.
# Soft assignment creates overlapping talent windows (like real 530 CELL 8).
# Sort-and-chop creates nearly disjoint slices (coverage ≈ 1) — diagnostic only.


def _kernel_weights(
    ability_i: float,
    team_targets: np.ndarray,
    *,
    assignment_kernel: AssignmentKernel,
    assignment_rho: float = 1.0,
    assignment_sigma: float = 0.65,
    assignment_temperature: float | None = None,
) -> np.ndarray:
    """Unnormalized soft-match weights for one player across all teams.

    What these weights *are*: how strongly player i “likes” each team j before
    we zero out full rosters and turn the vector into probabilities.

    540 default (ρ parameterization)
      w_j ∝ exp(−ρ · (A_i − T_j)² / (2σ²))   [gaussian]
      ρ = 0 → all ones (uniform among open rosters)
      ρ ↑   → sharper preference for T_j near A_i

    Args
      ability_i            — this player's A_i (a scalar).
      team_targets         — T_j for every team (length n_teams).
      assignment_rho       — ρ assortativity (Pass B).
      assignment_sigma     — σ length-scale in ability units.
      assignment_temperature — if not None, use legacy τ path instead of ρ
                               (opposite intuition: small τ = assortative).
                               Prefer ρ in new / 540 code.
    """
    # delta[j] = A_i − T_j  (how far this player is from each team's target)
    delta = float(ability_i) - np.asarray(team_targets, dtype=float)
    if assignment_temperature is not None:
        # Legacy τ path (537-era). Keep for old notebooks; new code should pass ρ.
        tau = max(float(assignment_temperature), 1e-12)
        if assignment_kernel == "gaussian":
            return np.exp(-0.5 * (delta / tau) ** 2)
        if assignment_kernel == "cauchy":
            return 1.0 / (1.0 + (delta / tau) ** 2)
        raise ValueError(f"unknown assignment_kernel {assignment_kernel!r}")

    rho = float(assignment_rho)
    if rho <= 0.0:
        # Flat weights → after open-roster masking, uniform among open seats.
        return np.ones(len(team_targets), dtype=float)
    sigma = max(float(assignment_sigma), 1e-12)
    z = delta / sigma  # distance in units of σ
    if assignment_kernel == "gaussian":
        return np.exp(-0.5 * rho * z**2)
    if assignment_kernel == "cauchy":
        return 1.0 / (1.0 + rho * z**2)
    raise ValueError(f"unknown assignment_kernel {assignment_kernel!r}")


def _normalize_probs(weights: np.ndarray) -> np.ndarray:
    """Turn non-negative weights into a probability vector (sums to 1)."""
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
    """Place each player on exactly one team with equal roster sizes (soft π_ij).

    What this returns
      pool_id[i] = integer team index for player i  (length = n_players)

    Algorithm (sequential fill — like dealing into piles with capacity)
      1. Shuffle player order (so seat-filling order is random, not ability-sorted).
      2. For each player i, compute kernel weights toward each team target T_j.
      3. Optional preferential attachment: multiply by (n_j + k)^α
         (default α=0 / off for 540 — leave this alone unless you turn the flag on).
      4. Zero out teams already at roster_size (full = cannot sit there).
      5. Sample one team from the remaining probabilities; increment that team's count.

    Args (CELL 2 style)
      ability              — A_i vector already drawn.
      team_targets         — T_j vector already drawn (length n_teams).
      roster_size          — seats per team; len(ability) must equal n_teams × roster_size.
      assignment_rho       — ρ assortativity (Pass B). 0 = uniform among open seats.
      assignment_sigma     — σ length-scale in the kernel (ability units).
      assignment_temperature — if set, use legacy τ path instead of ρ (prefer ρ).
      preferential_alpha/k — rich-get-richer; α=0 means off.

    Default kernel (540): exp(−ρ (A_i − T_j)² / (2σ²)).
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

    # pool_id: which team each player lands on (−1 until assigned).
    pool_id = np.full(n_players, -1, dtype=np.int64)
    # counts[j]: how many players already seated on team j (must end = roster_size).
    counts = np.zeros(n_teams, dtype=np.int64)
    alpha = float(preferential_alpha)
    k_pref = max(float(preferential_k), 1e-12)

    for i in rng.permutation(n_players):
        # Unnormalized soft-match weights for player i across all teams.
        w = _kernel_weights(
            ability[i],
            team_targets,
            assignment_kernel=assignment_kernel,
            assignment_rho=assignment_rho,
            assignment_sigma=assignment_sigma,
            assignment_temperature=assignment_temperature,
        )
        if alpha != 0.0:
            # Preferential attachment: teams that already have more players get
            # extra weight (optional; off when α=0).
            w = w * np.power(counts.astype(float) + k_pref, alpha)
        # open_mask: True where the team still has an empty seat.
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
    """537-style hard assortative assignment: sort by ability, equal-count slices.

    What this *is*: Pass B "sort_chop" arm / 530 CELL 8 red-line benchmark.
    Sort everyone by ability (optionally + noise), then chop into n_teams contiguous
    blocks of equal size. Talent windows barely overlap (coverage ≈ 1).

    Important: this is NOT "ρ → ∞". Soft ρ and sort-chop are different mechanisms.
    """
    ability = np.asarray(ability, dtype=float)
    n = len(ability)
    noise_sd = max(float(sorting_noise_sd), 0.0)
    # signal: what we sort on. Pure ability when noise_sd=0; else ability + noise.
    signal = (
        ability
        if noise_sd == 0.0
        else ability + rng.normal(0.0, noise_sd, size=n)
    )
    order = np.argsort(signal, kind="mergesort")
    # base: team labels in ability order — team 0 gets the lowest block, etc.
    base = np.repeat(np.arange(n_teams), int(np.ceil(n / n_teams)))[:n]
    pool_id = np.empty(n, dtype=np.int64)
    pool_id[order] = base
    return pool_id


def build_roster_dataframe(
    ability: np.ndarray,
    pool_id: np.ndarray,
    team_targets: np.ndarray,
) -> pd.DataFrame:
    """One row per player after assignment — the table SCORE/SELECT will enrich.

    Columns written here (before LOO / selection)
      player_id   — 0 … n−1
      ability     — A_i (latent talent)
      pool_id     — which team this player sits on
      team_target — T_j for that player's team (looked up from team_targets[pool_id])

    Later steps add: poolq_loo / pool_c_* (LOO), selection_weight, Y_selected.
    """
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


# =============================================================================
# 5. LOO POOL STATS — L_Q AND L_C ON EACH FAKE ROSTER
# =============================================================================
# After assignment, each player sees teammates. Leave-one-out (exclude self):
#   L_Q  = mean teammate ability
#   L_C  = congestion among viable peers (hard share or smooth viability)
# Pass A congestion arm uses crowding_smooth (pool_c_smooth_loo).


def _default_viability_theta() -> float:
    """Fallback θ if not passed — usually 530 median drafted perf on z scale."""
    try:
        return float(
            AssignmentParams.from_tier1_sim_config().viability_theta
        )
    except Exception:
        return 0.7546158731868137


def _viability_logistic(ability: pd.Series, *, theta: float, gamma: float) -> pd.Series:
    """Soft viability σ(γ(A−θ)) elementwise; NaN where ability is NaN.

    θ = cutline, γ = sharpness. This is crowding softness — NOT assignment ρ
    and NOT selection noise.
    """
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
    """Add L_Q (poolq_loo) and L_C leave-one-out teammate stats to ``players``.

    Leave-one-out (LOO) means: for player i on a team, compute the pool statistic
    from *everyone else on that team* — exclude i — so your own ability does not
    inflate your pool quality / crowding.

    Requires columns already present: ability, pool_id.

    Writes (what each column *is*)
      poolq_loo           — L_Q: mean teammate ability (hero X-axis analog)
      pool_c_loo          — L_C hard: share of teammates with ability > θ  ∈ [0,1]
      pool_c_smooth_loo   — L_C soft: mean teammate σ(γ(A−θ))              ∈ [0,1]
      pool_c_loo_sum      — legacy: sum of teammate ability (diagnostic only)

    Args
      viability_theta (θ)     — cutline for “viable peer”; None → config default.
      viability_sharpness (γ) — logistic sharpness for smooth L_C.
    """
    theta = (
        float(viability_theta)
        if viability_theta is not None
        else _default_viability_theta()
    )
    gamma = float(viability_sharpness)
    out = players.copy()

    # --- Team totals (include self); we subtract self next for LOO -------------
    g = out.groupby("pool_id", observed=True)["ability"]
    ssum = g.transform("sum")          # sum of ability on i's team (incl. i)
    cnt = g.transform("count").astype(float)  # roster size on i's team
    den = (cnt - 1.0).replace(0.0, np.nan)    # LOO denominator = teammates only
    own = pd.to_numeric(out["ability"], errors="coerce")  # A_i for this row
    loo_sum = ssum - own               # sum of teammate ability (exclude self)
    out[POOL_L_CROWDING_SUM_COL] = loo_sum
    # L_Q = mean of teammates' ability (exclude self)
    out[POOL_L_QUALITY_COL] = loo_sum / den

    # --- Hard crowding L_C: LOO share of teammates above θ ---------------------
    # above: 1.0 if this player's A > θ, else 0.0 (then we LOO that indicator).
    above = (own > theta).astype(float)
    out["_above_theta"] = above
    sum_above = out.groupby("pool_id", observed=True)["_above_theta"].transform("sum")
    own_above = out["_above_theta"].where(own.notna(), np.nan)
    # loo_count: how many *other* teammates sit above θ
    loo_count = sum_above - own_above.fillna(0.0)
    loo_count = loo_count.where(own.notna(), np.nan)
    # LOO pool size = roster count − 1 (exclude self), same denominator as L_Q
    loo_pool_n = (cnt - 1.0).replace(0.0, np.nan)
    loo_share = loo_count / loo_pool_n   # ∈ [0,1] when defined
    loo_share = loo_share.where(own.notna(), np.nan)
    loo_share = loo_share.where(cnt >= 2.0, np.nan)  # need ≥1 teammate
    out[POOL_L_CROWDING_COL] = loo_share

    # --- Smooth crowding L_C: LOO mean of soft viability σ(γ(A−θ)) -------------
    viability = _viability_logistic(out["ability"], theta=theta, gamma=gamma)
    out["_viability"] = viability
    sum_v = out.groupby("pool_id", observed=True)["_viability"].transform("sum")
    own_v = viability
    loo_smooth = (sum_v - own_v) / den   # mean teammate soft-viability ∈ [0,1]
    loo_smooth = loo_smooth.where(own.notna(), np.nan)
    loo_smooth = loo_smooth.where(cnt >= 2.0, np.nan)
    out[POOL_L_CROWDING_SMOOTH_COL] = loo_smooth
    out = out.drop(columns=["_above_theta", "_viability"])
    return out


# =============================================================================
# 5b. TEAM-LEVEL L_C (PD16) — congestion is a property of team j
# =============================================================================
# Alex PD16 (Aug 2026): "Congestion should be how many good players are on the team."
# Same soft viability σ(γ(A−θ)) as LOO smooth L_C, but computed over the FULL roster
# (include self) and broadcast — every player on team j shares one L_C value.
#
# LOO L_C (§5 above) excludes player i when measuring peers — fine for hero-axis
# readouts; PD16 score story uses team-level congestion instead.
#
# Column written: pool_c_smooth_team ∈ [0,1]
# L_Q (poolq_loo) is still LOO mean teammate ability for visualization compatibility.


def add_team_pool_columns(
    players: pd.DataFrame,
    *,
    viability_theta: float | None = None,
    viability_sharpness: float = 18.0,
) -> pd.DataFrame:
    """Attach L_Q (LOO) + team smooth L_C (PD16) to ``players``.

    Requires: ability, pool_id.

    Writes
      poolq_loo           — L_Q: LOO mean teammate ability (unchanged from §5)
      pool_c_smooth_team  — L_C: team mean σ(γ(A−θ)) over ALL roster members
    """
    theta = (
        float(viability_theta)
        if viability_theta is not None
        else _default_viability_theta()
    )
    gamma = float(viability_sharpness)
    out = players.copy()

    # --- L_Q: keep LOO mean teammate ability (hero / pool-mean bin axis) ---------
    g = out.groupby("pool_id", observed=True)["ability"]
    ssum = g.transform("sum")
    cnt = g.transform("count").astype(float)
    den = (cnt - 1.0).replace(0.0, np.nan)
    own = pd.to_numeric(out["ability"], errors="coerce")
    loo_sum = ssum - own
    out[POOL_L_QUALITY_COL] = loo_sum / den

    # --- Team smooth L_C: mean_j σ(γ(A_k − θ)) — include every roster member ----
    viability = _viability_logistic(out["ability"], theta=theta, gamma=gamma)
    out["_viability"] = viability
    out[POOL_L_CROWDING_SMOOTH_TEAM_COL] = out.groupby("pool_id", observed=True)[
        "_viability"
    ].transform("mean")
    out[POOL_L_CROWDING_SMOOTH_TEAM_COL] = out[POOL_L_CROWDING_SMOOTH_TEAM_COL].where(
        own.notna(), np.nan
    )
    out[POOL_L_CROWDING_SMOOTH_TEAM_COL] = out[POOL_L_CROWDING_SMOOTH_TEAM_COL].where(
        cnt >= 1.0, np.nan
    )
    out = out.drop(columns=["_viability"])
    return out


def _attach_pool_l_columns(
    players: pd.DataFrame,
    *,
    pool_l_mode: str,
    viability_theta: float | None,
    viability_sharpness: float,
) -> pd.DataFrame:
    """Dispatch LOO vs team L_C attachment based on pool_l_mode."""
    m = str(pool_l_mode).strip().lower()
    if m in (
        "crowding_smooth_team",
        "team_smooth",
        "team_crowding_smooth",
        POOL_L_CROWDING_SMOOTH_TEAM_COL,
    ):
        return add_team_pool_columns(
            players,
            viability_theta=viability_theta,
            viability_sharpness=viability_sharpness,
        )
    return add_loo_pool_columns(
        players,
        viability_theta=viability_theta,
        viability_sharpness=viability_sharpness,
    )


def add_poolq_loo(players: pd.DataFrame) -> pd.DataFrame:
    """Backward-compatible alias: adds both L_Q and L_C columns."""
    return add_loo_pool_columns(players)


# =============================================================================
# 6. SCORE — TURN (A, L) INTO A RANKING WEIGHT S_i
# =============================================================================
# Generative step (2). Pass A toggles here:
#   ability              → S = A          (talent-only / λ = 0)
#   loo_gap_plus_ability → S = (1−w)A + w(A−L) = A − w·L
#     with L = crowding_smooth ⇒ congestion-in-score story
#
# NAME DECODE + UNIT MATCHING — parameter l_term_scale
# ----------------------------------------------------------------
# Full decode is in the module docstring READ-FIRST GLOSSARY (top of file).
# Short reminder only here (you should already know this before §6):
#
#   l = pool L;  term = L-piece of S = A − w·L;  scale = unit-matching multiplier.
#   L_used_in_score = L_C × l_term_scale
#   None → auto ≈ (p90 of A − p10 of A). Skip scaling if A already on [0,1].
#   Config twin: CROWDING_L_Z_SCALE.


def ability_on_unit_interval(ability: np.ndarray) -> bool:
    """True when synthetic A_i looks drawn on [0, 1] (539 beta/uniform), not z-scored.

    Used only to decide whether crowding L needs l_term_scale.
    Heuristic: min ≳ −0.05 and max ≲ 1.05 after dropping non-finite values.
    """
    finite = np.asarray(ability, dtype=float)
    finite = finite[np.isfinite(finite)]
    if finite.size == 0:
        return False
    return float(finite.min()) >= -0.05 and float(finite.max()) <= 1.05


def default_crowding_l_z_scale(ability: np.ndarray) -> float:
    """Auto value for l_term_scale when A is z-scored and L is crowding on [0,1].

    What it *is*: p90(A) − p10(A) — a robust “typical spread” of ability.
    Fallback 4.0 if too few finite values or a near-zero spread.

    Why: map L_C ∈ [0,1] into ability units so w·L_C can actually move S_i.
    Otherwise congestion is numerically invisible next to z-scored A.
    """
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
    """Return L in the same units as ability for subtractive scores.

    Args
      l_values     — raw LOO L from the players table (L_Q or L_C column).
      ability      — A_i vector (used only to decide / auto-pick the scale).
      pool_l_mode  — "quality" / "crowding" / "crowding_smooth".
      l_term_scale — OPTIONAL. Name decode: l = pool L; term = the L-piece of
                     S = A − w·L; scale = unit-matching multiplier.
                     What the *number* is: converts L_C ∈ [0,1] into ability
                     units: L_used = L_C × l_term_scale. Full story: §6 banner.
                     None → auto = default_crowding_l_z_scale(ability)
                     (≈ p90(A)−p10(A)). Ignored for quality mode and for
                     unit-interval ability draws.

    Behavior
      L_Q (quality)              → pass through (already ability units).
      L_C + A on [0,1]           → pass through (already comparable).
      L_C + A z-scored           → multiply by l_term_scale (or auto).
    """
    l = np.asarray(l_values, dtype=float)
    # Quality L is already in ability units — no scaling.
    if not is_crowding_l_mode(pool_l_mode):
        return l
    # Unit-interval A (beta/uniform): L_C ∈ [0,1] is already comparable — no scale.
    if ability_on_unit_interval(ability):
        return l
    # Z-scored A + crowding L: pick / apply l_term_scale.
    scale = (
        float(l_term_scale)
        if l_term_scale is not None and np.isfinite(l_term_scale) and l_term_scale > 0
        else default_crowding_l_z_scale(ability)
    )
    # L_used_in_score = L_C × scale  (now in ability units)
    return l * scale


def selection_weights(
    players: pd.DataFrame,
    *,
    score_mode: str,
    loo_gap_weight: float,
    pool_l_mode: str = "quality",
    l_term_scale: float | None = None,
) -> np.ndarray:
    """Compute score / ranking weight for each player (the S_i vector).

    What S_i *is*: a number used only to *rank* players for selection. Higher
    weight → more likely (or certain, under choice C) to get Y_selected=1.
    This is the SCORE step; SELECT happens in choose_selected.

    score_mode
      "ability"
          S_i = A_i                          ← Pass A talent-only arm (λ = 0)
      "loo_gap_plus_ability"
          S_i = w·(A_i − L_i) + (1−w)·A_i
              = A_i − w·L_i                 ← Pass A congestion arm when L = L_C
          loo_gap_weight is w (Alex λ story in code).

    Args (CELL 2 style)
      score_mode      — "ability" or "loo_gap_plus_ability" (see above).
      loo_gap_weight  — w in A − w·L. 0 ≈ talent-only; 1 ≈ full gap A−L.
                        Same role as Alex λ in the nesting S = A − λ·L_C.
      pool_l_mode     — which L column: quality / crowding / crowding_smooth.
      l_term_scale    — name: l = pool L; term = L-piece of S=A−w·L; scale =
                        unit matcher. Number: L_used = L_C × this. See §6.
                        None = auto. Only when crowding mode AND A not on [0,1].
    """
    # a: raw ability A_i
    a = players["ability"].to_numpy(dtype=float)
    # lcol: which DataFrame column holds the chosen L (poolq_loo / pool_c_*)
    lcol = pool_l_column(pool_l_mode)
    # q_raw: L as stored on the table (L_C still on [0,1] here if crowding)
    q_raw = players[lcol].to_numpy(dtype=float)
    # q: L after unit matching (may be L_C × l_term_scale)
    q = effective_l_for_selection(
        q_raw, a, pool_l_mode=pool_l_mode, l_term_scale=l_term_scale
    )
    mode = str(score_mode).strip().lower()
    if mode == "ability":
        # Talent-only: ignore L entirely.
        w = a.copy()
    elif mode == "loo_gap_plus_ability":
        # Congestion-in-score: S = A − w·L  (algebraically same as the mix form).
        wgt = float(loo_gap_weight)  # w / λ in the nesting
        w = wgt * (a - q) + (1.0 - wgt) * a
        # If L was missing for a row, fall back to talent-only for that row.
        w = np.where(np.isfinite(q_raw), w, a)
    else:
        raise ValueError(f"unknown selection score_mode {score_mode!r}")
    w = np.where(np.isfinite(w), w, 0.0)
    # Clip at 0: ranking weights are non-negative for stochastic choices A/B too.
    return np.clip(w, 0.0, None)


# =============================================================================
# 7. SELECT — WINNER RULE GIVEN SCORES
# =============================================================================
# Generative step (3). v1 / Pass A–B default: choice "C" = top K by score.
# Choices A/B are stochastic draws (kept for older 537 experiments).


def choose_selected(
    rng: np.random.Generator,
    weights: np.ndarray,
    k: int,
    choice: str,
) -> np.ndarray:
    """Boolean mask of length n: True = selected (drafted / advanced).

    What this *is*: the SELECT step. Takes the score vector S_i (= weights) and
    picks exactly who gets the slot. Score ≠ select — ranking first, then this.

    choice (winner rule)
      "A" — sample K players without replacement ∝ weights (stochastic)
      "B" — independent Bernoulli with p ∝ weight (stochastic; expected ~K)
      "C" — deterministic top K by weight  ← Pass A/B default (winner rule)

    Args
      weights — S_i from selection_weights (non-negative ranking scores).
      k       — how many players get selected (N_SELECTED in config).
      choice  — "A" / "B" / "C" as above.
    """
    n = len(weights)
    w = np.asarray(weights, dtype=float)
    w = np.where(np.isfinite(w), w, 0.0)
    w = np.clip(w, 0.0, None)
    # n_positive: how many players have a usable positive score (can be picked).
    n_positive = int(np.count_nonzero(w > 0))
    if n_positive == 0:
        return np.zeros(n, dtype=bool)
    # k_eff: cannot select more people than have positive weight.
    k_eff = min(int(k), n_positive)
    if choice == "A":
        # Stochastic proportional sample without replacement.
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
        # Independent coin flips; expected number selected ≈ k_eff.
        total = float(w.sum())
        p = w / total if total > 0 else np.full(n, 1.0 / n)
        return rng.uniform(size=n) < np.minimum(p * k_eff, 1.0)
    if choice == "C":
        # Deterministic: the K highest scores win (ties broken by mergesort stability).
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
    """Decide the l_term_scale value that selection_weights should use.

    What this returns
      A positive float  → use that as l_term_scale (multiply L_C by it).
      None              → tell effective_l_for_selection to AUTO-pick
                          (p90(A)−p10(A)), or skip scaling if not needed.

    Priority
      1. Explicit crowding_l_z_scale argument if it is a finite positive number.
      2. Else, if pool_l_mode is a crowding mode, read CROWDING_L_Z_SCALE from
         tier1_sim_config.py when that constant is set and positive.
      3. Else None (auto inside effective_l_for_selection, or no-op for quality).

    Only relevant for crowding L modes. Quality mode always gets None here.
    Same idea as l_term_scale — two names for one knob (API vs config).
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
        # CROWDING_L_Z_SCALE in config = same concept as l_term_scale in the API.
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
    """SCORE then SELECT on an already-assigned roster table.

    Pipeline inside this function (after ASSIGN already happened)
      1. _attach_pool_l_columns → attach L_Q / L_C (LOO or team per pool_l_mode)
      2. selection_weights     → S_i (ranking score)
      3. choose_selected       → Y_selected ∈ {0,1}

    Domain-agnostic name: "selected" can mean draft / tenure / promotion.

    Args (CELL 2 style)
      players              — roster table with ability + pool_id (from ASSIGN).
      n_selected           — K: how many get Y_selected=1 (top-K under choice C).
      score_mode           — "ability" or "loo_gap_plus_ability" (Pass A toggle).
      loo_gap_weight       — w / λ in S = A − w·L (Pass A congestion strength).
      winner_selection     — "A"/"B"/"C"; Pass A/B default "C" = top K by score.
      pool_l_mode          — which L enters the score (quality / crowding_smooth /
                             crowding_smooth_team for PD16 team L_C).
      viability_theta      — θ for L_C; None → config default.
      viability_sharpness  — γ for smooth L_C; None → config default.
      crowding_l_z_scale   — explicit l_term_scale for crowding L (None → config/auto).
                             See §6 banner: converts L_C ∈ [0,1] into ability units.

    Writes onto the returned copy
      poolq_loo / pool_c_*   — LOO pool stats
      selection_weight       — S_i for each player
      Y_selected             — 1 if selected, else 0
    """
    gamma = (
        float(viability_sharpness)
        if viability_sharpness is not None
        else float(AssignmentParams.from_tier1_sim_config().viability_sharpness)
    )
    # Step 1 — attach L columns (LOO or team L_C per pool_l_mode).
    out = _attach_pool_l_columns(
        players,
        pool_l_mode=pool_l_mode,
        viability_theta=viability_theta,
        viability_sharpness=gamma,
    )
    # l_scale: resolved l_term_scale (explicit arg → config → None=auto).
    l_scale = resolve_crowding_l_z_scale(
        crowding_l_z_scale, pool_l_mode=pool_l_mode
    )
    # Step 2 — SCORE: S_i for every player (may use L_C × l_scale).
    w = selection_weights(
        out,
        score_mode=score_mode,
        loo_gap_weight=loo_gap_weight,
        pool_l_mode=pool_l_mode,
        l_term_scale=l_scale,
    )
    # Step 3 — SELECT: winner rule turns scores into 0/1 outcomes.
    out["Y_selected"] = choose_selected(
        rng, w, int(n_selected), str(winner_selection)
    ).astype(int)
    out["selection_weight"] = w
    return out


# Legacy names (early 538 drafts used "promotion" instead of "selection")
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
    """Legacy wrapper: same as assign_selection, also writes Y_promoted."""
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
    """Per-pool realized mean, SD, min, max of ability (530 CELL 5–8 style).

    Used for Plot A overlap diagnostics: soft should have high coverage_peak;
    sort-and-chop should sit near coverage = 1.
    """
    g = df.groupby("pool_id", sort=True)["ability"]
    out = g.agg(["mean", "std", "min", "max", "count"]).rename(
        columns={"mean": "pool_mean", "std": "pool_sd", "count": "roster_n"}
    )
    out["team_target"] = df.groupby("pool_id", sort=True)["team_target"].first()
    return out.reset_index()


# =============================================================================
# 8. ONE-SHOT LEAGUE DRAW — ASSIGN ONLY (score/select happen upstream)
# =============================================================================
# simulate_generative_rosters = draw A, draw T, assign → players + team summary.
# Pass A/B then call assign_selection (via tier1_generative_eda) on that table.


def simulate_generative_rosters(
    params: AssignmentParams | None = None,
    *,
    rng: np.random.Generator | None = None,
    seed: int | None = 42,
    method: AssignmentMethod = "soft",
    ability: np.ndarray | None = None,
    team_targets: np.ndarray | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, np.ndarray]:
    """One full synthetic league **assignment** draw (ASSIGN only).

    What this does NOT do: score or select. Pass A/B call assign_selection
    (via tier1_generative_eda) afterward on the players table returned here.

    Optional ability / team_targets: Pass B passes the SAME draws into every arm
    so only the assignment method / ρ changes (fair comparison across ρ).

    Args (CELL 2 style)
      params        — AssignmentParams bundle; None → load tier1_sim_config.py.
      rng / seed    — RNG; if rng is None, build one from seed (default 42).
      method        — "soft" (ρ kernel) or "sort_chop" (hard slices).
      ability       — optional pre-drawn A_i (Pass B reuse). None → draw now.
      team_targets  — optional pre-drawn T_j (Pass B reuse). None → draw now.

    Returns
    -------
    players : DataFrame
        player_id, ability, pool_id, team_target  (no Y_selected yet)
    teams : DataFrame
        per-pool summary (pool_mean, pool_sd, min, max, team_target, ...)
    team_targets : ndarray
        length n_teams — the T_j used (returned so Pass B can reuse them)
    """
    if params is None:
        params = AssignmentParams.from_tier1_sim_config()
    if rng is None:
        rng = np.random.default_rng(seed)

    n = params.n_individuals  # n_teams × roster_size
    if ability is None:
        # Invent latent talent A_i for every synthetic player.
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
        # Invent one target mean T_j per team (soft-match aims here).
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

    # Preferential attachment off unless config boolean is True (α=0 → no effect).
    pref_alpha = (
        float(params.preferential_alpha)
        if params.use_preferential_attachment
        else 0.0
    )

    if method == "soft":
        # Probabilistic seating near T_j; ρ from params.assignment_rho (Pass B).
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
        # Hard sorted slices — diagnostic / Pass B extreme arm (not ρ→∞).
        pool_id = assign_sort_chop_benchmark(
            rng,
            ability,
            params.n_teams,
            sorting_noise_sd=params.sorting_noise_sd,
        )
    else:
        raise ValueError(f"unknown method {method!r}")

    # players: one row per person; teams: one row per pool for overlap diagnostics.
    players = build_roster_dataframe(ability, pool_id, team_targets)
    teams = roster_team_stats(players)
    return players, teams, team_targets


# =============================================================================
# 9. SMOKE TEST — soft overlap should beat sort-and-chop
# =============================================================================


def _smoke_compare_overlap() -> None:
    """Quick stdout check: soft assignment should raise interval overlap vs sort-chop.

    Run: python sports/tier1_pool_assignment.py
    Expect: soft coverage_peak ≫ 1; sort_chop coverage_peak near 1;
            soft median_pool_sd closer to ~0.8 z than chop.
    """
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
