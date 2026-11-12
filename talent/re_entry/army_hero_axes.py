"""B1/B2/B3 column names for Army HERO (peer-influence axes)."""

from __future__ import annotations

from typing import Literal

Axis = Literal["b1", "b2", "b3"]
Direction = Literal["fwd", "bwd"]
Scale = Literal["z", "raw"]
Band = Literal["full", "boe"]

_AXIS_RAW_BASE: dict[Axis, tuple[str, ...]] = {
  # B1 full-group mean T_j (incl. self)
    "b1": ("pool_mean_snr",),
    # B2 leave-one-out peer mean (canonical then legacy feather names)
    "b2": ("pool_loo_snr", "pool_tb_ratio_mean_snr"),
    # B3 own minus LOO peer mean
    "b3": ("pool_minus_loo_snr", "pool_minus_mean_snr"),
}


def resolve_hero_column(
    *,
    axis: Axis,
    direction: Direction,
    scale: Scale,
    available: set[str] | frozenset[str] | None = None,
) -> str:
    """Pick the first matching feather column for axis × direction × scale."""
    bases = _AXIS_RAW_BASE[axis]
    cols: list[str] = []
    for base in bases:
        raw = f"{base}_{direction}"
        if scale == "z":
            cols.append(f"z_{raw}")
        cols.append(raw)
    if available is not None:
        for c in cols:
            if c in available:
                return c
        raise KeyError(
            f"No column for axis={axis} direction={direction} scale={scale}; "
            f"tried {cols}"
        )
    # Config-time default (canonical raw; Cell 10.5 supplies z_)
    raw = f"{bases[0]}_{direction}"
    return f"z_{raw}" if scale == "z" else raw


def hero_output_stem(
    *,
    axis: Axis,
    direction: Direction,
    scale: Scale,
    bin_method: str,
    n_bins: int,
    band: Band,
    tag: str,
    prefix: str = "ARMY",
) -> str:
    """Filename stem, e.g. ARMY_HERO_b2_fwd_z_ew12_full_run1."""
    bm = "ew" if bin_method == "equal_width" else "q"
    return f"{prefix}_HERO_{axis}_{direction}_{scale}_{bm}{n_bins}_{band}_{tag}"
