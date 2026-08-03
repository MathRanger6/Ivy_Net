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

# Pass C only (optional overrides)
RHO_LOW = _env_float("GALLERY_RHO_LOW", 0.1)
RHO_MODERATE = _env_float("GALLERY_RHO_MODERATE", 1.0)
RHO_HIGH = _env_float("GALLERY_RHO_HIGH", 8.0)
RHO_VERY_HIGH = _env_float("GALLERY_RHO_VERY_HIGH", 32.0)
