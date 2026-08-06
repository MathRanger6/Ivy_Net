"""Shared gallery knobs — override via environment (see rebuild_hero_gallery.sh).

Example (baseline — reproduces Phase B deck PNGs):
  export GALLERY_PRESET=539
  ./scripts/build_characterization_slides.sh

Example (PD16 variant — team L_C + naive-draft θ, new *_pd16.png files):
  ./scripts/build_characterization_slides.sh --pd16

Manual equivalent:
  export GALLERY_LC_MODE=team_smooth
  export GALLERY_THETA_MODE=k_over_n
  export GALLERY_OUTPUT_SUFFIX=_pd16
  ./scripts/build_characterization_slides.sh

PD16 modes (Paper Directions 16, Aug 2026 — re_entry/08_PD16_Alex_meeting_takeaways.md)
---------------------------------------------------------------------------------------
GALLERY_LC_MODE:
  loo_smooth   — DEFAULT. L_C = LOO mean σ(γ(A−θ)); current Phase B deck.
  team_smooth  — PD16. L_C = team-level mean σ(γ(A−θ)); same value for whole roster.

GALLERY_THETA_MODE:
  preset       — DEFAULT. θ from tier1_539_reference_settings / SELECTION_539 (0.72).
  k_over_n     — PD16 naive draft: θ = F_A⁻¹(1 − K/N) on the ability draw (Beta(2,2) in sim).

GALLERY_OUTPUT_SUFFIX:
  ""           — DEFAULT. Overwrites baseline PNG names (same as today).
  _pd16        — Writes parallel figures; baseline PNGs untouched for side-by-side decks.
"""

from __future__ import annotations

import os

try:
    from scipy.stats import beta as _beta_dist
except ImportError:  # pragma: no cover — scipy expected in project env
    _beta_dist = None  # type: ignore[assignment]


def _env_str(name: str, default: str) -> str:
    val = os.environ.get(name)
    return default if val is None or val == "" else val


def _env_int(name: str, default: int) -> int:
    val = os.environ.get(name)
    if val is None or val == "":
        return default
    return int(val)


def _env_float(name: str, default: float) -> float:
    val = os.environ.get(name)
    if val is None or val == "":
        return default
    return float(val)


# Pass A/B/C PNG generation
PRESET = _env_str("GALLERY_PRESET", "539")  # "539" | "540"
HERO_BINS = _env_int("GALLERY_HERO_BINS", 16)
HERO_SEED = _env_int("GALLERY_HERO_SEED", 42)

# League scale — characterization default K/N = 10% (not MBB ~1%)
# Override: GALLERY_N_TEAMS, GALLERY_ROSTER_SIZE, GALLERY_N_SELECTED, or GALLERY_K_OVER_N
HERO_N_TEAMS = _env_int("GALLERY_N_TEAMS", 350)
HERO_ROSTER_SIZE = _env_int("GALLERY_ROSTER_SIZE", 16)
HERO_K_OVER_N = _env_float("GALLERY_K_OVER_N", 0.10)
_default_n = HERO_N_TEAMS * HERO_ROSTER_SIZE
HERO_N_SELECTED = _env_int(
    "GALLERY_N_SELECTED",
    max(1, int(round(_default_n * HERO_K_OVER_N))),
)


def hero_league_n() -> int:
    return HERO_N_TEAMS * HERO_ROSTER_SIZE


def hero_k_over_n() -> float:
    n = hero_league_n()
    return HERO_N_SELECTED / n if n else 0.0


def league_scale_title_line() -> str:
    n = hero_league_n()
    kn = hero_k_over_n()
    return rf"$N={n}$, $K={HERO_N_SELECTED}$, $K/N={kn:.2f}$"

# Pass B λ ablation — fixed ρ, vary λ in score (characterization deck)
LAMBDA_FIXED_RHO = _env_float("GALLERY_LAMBDA_FIXED_RHO", 8.0)
LAMBDA_LOW = _env_float("GALLERY_LAMBDA_LOW", 0.25)
LAMBDA_MODERATE = _env_float("GALLERY_LAMBDA_MODERATE", 0.55)
LAMBDA_HIGH = _env_float("GALLERY_LAMBDA_HIGH", 1.0)

# ---------------------------------------------------------------------------
# PD16 — team L_C, naive-draft θ, parallel output suffix (_pd16)
# ---------------------------------------------------------------------------
# Read once at import; unset env → baseline Phase B behavior unchanged.
LC_MODE = _env_str("GALLERY_LC_MODE", "loo_smooth").strip().lower()
THETA_MODE = _env_str("GALLERY_THETA_MODE", "preset").strip().lower()

# Master suffix for new PD16 figures. Per-pass overrides still win if set explicitly.
OUTPUT_SUFFIX = _env_str("GALLERY_OUTPUT_SUFFIX", "")

PASS_B_PNG_SUFFIX = _env_str("GALLERY_PASS_B_PNG_SUFFIX", OUTPUT_SUFFIX)
PASS_C_PNG_SUFFIX = _env_str("GALLERY_PASS_C_PNG_SUFFIX", OUTPUT_SUFFIX)
THETA_PNG_SUFFIX = _env_str("GALLERY_THETA_PNG_SUFFIX", OUTPUT_SUFFIX)

_VALID_LC_MODES = frozenset({"loo_smooth", "team_smooth"})
_VALID_THETA_MODES = frozenset({"preset", "k_over_n", "kover_n", "kn"})


def resolve_pool_l_mode() -> str:
    """Map GALLERY_LC_MODE → pool_l_mode string for assign_selection().

    loo_smooth  → crowding_smooth      (column pool_c_smooth_loo)
    team_smooth → crowding_smooth_team (column pool_c_smooth_team; PD16)
    """
    if LC_MODE not in _VALID_LC_MODES:
        raise ValueError(
            f"GALLERY_LC_MODE must be one of {sorted(_VALID_LC_MODES)!r}, got {LC_MODE!r}"
        )
    if LC_MODE == "team_smooth":
        return "crowding_smooth_team"
    return "crowding_smooth"


def resolve_viability_theta(
    *,
    preset: float = 0.72,
    k_over_n: float | None = None,
    ability_draw: str = "beta_2_2",
) -> float:
    """Return θ for L_C / sigmoid under current GALLERY_THETA_MODE.

    preset (default):
        Fixed 539 / Phase B value — does not move when K/N changes.

    k_over_n (PD16 naive draft):
        θ = F_A⁻¹(1 − K/N). Top K/N of the ability distribution advances in the
        thought experiment; that cutoff defines the viability center.
        Sim default draw Beta(2,2) on [0,1]: scipy.stats.beta.ppf(1 − K/N, 2, 2).
    """
    mode = THETA_MODE
    if mode in ("preset", "539", "fixed"):
        return float(preset)
    if mode not in _VALID_THETA_MODES:
        raise ValueError(
            f"GALLERY_THETA_MODE must be preset or k_over_n, got {THETA_MODE!r}"
        )
    kn = hero_k_over_n() if k_over_n is None else float(k_over_n)
    kn = min(max(kn, 1e-9), 1.0 - 1e-9)
    draw = str(ability_draw).strip().lower()
    if draw in ("beta_2_2", "beta", "beta22"):
        if _beta_dist is None:
            raise ImportError(
                "scipy required for GALLERY_THETA_MODE=k_over_n (beta.ppf)"
            )
        return float(_beta_dist.ppf(1.0 - kn, 2.0, 2.0))
    raise ValueError(
        f"k_over_n θ not implemented for ability_draw={ability_draw!r}; "
        "use beta_2_2 or preset mode"
    )


def gallery_mode_subtitle(*, theta_value: float | None = None) -> str:
    """Second-line PNG title fragment documenting active PD16 modes."""
    parts: list[str] = []
    if LC_MODE == "team_smooth":
        parts.append(r"team $L_C$")
    if THETA_MODE != "preset":
        th = f"{theta_value:.3f}" if theta_value is not None else "K/N quantile"
        parts.append(rf"$\theta$ = {th} (naive draft)")
    if OUTPUT_SUFFIX:
        parts.append(f"suffix={OUTPUT_SUFFIX}")
    if not parts:
        return "baseline: LOO L_C, preset θ"
    return "PD16: " + "; ".join(parts)


def gallery_mode_summary_lines(*, theta_value: float | None = None) -> list[str]:
    """Bullet lines for PASS_* summary.txt headers."""
    lines = [
        f"L_C mode: {LC_MODE} → pool_l_mode={resolve_pool_l_mode()}",
        f"θ mode: {THETA_MODE}"
        + (
            f" (θ={theta_value:.4f})"
            if theta_value is not None and THETA_MODE != "preset"
            else f" (θ={theta_value:.4f} preset)" if theta_value is not None else ""
        ),
    ]
    if OUTPUT_SUFFIX:
        lines.append(f"Output suffix: {OUTPUT_SUFFIX}")
    return lines

# Pass C only (optional overrides)
RHO_LOW = _env_float("GALLERY_RHO_LOW", 0.1)
RHO_MODERATE = _env_float("GALLERY_RHO_MODERATE", 1.0)
RHO_HIGH = _env_float("GALLERY_RHO_HIGH", 8.0)
RHO_VERY_HIGH = _env_float("GALLERY_RHO_VERY_HIGH", 32.0)

# Pass C: legacy env toggle (prefer two-PNG output from pass_c_rho_ablation_bundle.py)
SHOW_SORT_CHOP = _env_str("GALLERY_SHOW_SORT_CHOP", "0").lower() in (
    "1",
    "true",
    "yes",
)

# K/N presets (N = HERO_N_TEAMS × HERO_ROSTER_SIZE unless overridden)
# Use: GALLERY_K_OVER_N=0.01 | 0.10 | 0.40  or  GALLERY_KN_PRESET=mbb_draft|characterization|army_high
KN_PRESETS: dict[str, float] = {
    "mbb_draft": 0.01,          # ~60/5600 D1 draft rate (domain cal later)
    "characterization": 0.10,   # Phase B default
    "army_high": 0.40,         # high-selectivity explore
}
_kn_preset = _env_str("GALLERY_KN_PRESET", "").strip().lower()
if _kn_preset and _kn_preset in KN_PRESETS:
    HERO_K_OVER_N = KN_PRESETS[_kn_preset]
    HERO_N_SELECTED = max(1, int(round(_default_n * HERO_K_OVER_N)))
