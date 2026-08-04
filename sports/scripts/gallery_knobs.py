"""Shared gallery knobs — override via environment (see rebuild_hero_gallery.sh).

Example:
  export GALLERY_PRESET=540
  export GALLERY_HERO_BINS=20
  ./scripts/rebuild_hero_gallery.sh
"""

from __future__ import annotations

import os


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
PASS_B_PNG_SUFFIX = _env_str("GALLERY_PASS_B_PNG_SUFFIX", "")

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

# Optional suffix before .png (e.g. _with_sortchop) for characterization variants
PASS_C_PNG_SUFFIX = _env_str("GALLERY_PASS_C_PNG_SUFFIX", "")

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
