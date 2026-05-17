"""
Tier 1 mechanism columns for VECTOR / SCOUT (pool quality Q vs crowding C).

``congestion_quality`` is the LOO *mean* teammate ``perf`` (only rows with non-null
``perf`` in the ``(team_id, season)`` group). This is \(Q_{jt}^{(-i)}\), not a
congestion measure — the name pairs with ``congestion_crowding`` for modeling toggles.

``congestion_crowding`` is the LOO *sum* of teammate ``perf`` (same validity rule).

Legacy ``poolq_loo`` from ``recompute_teammate_loo_pool_quality`` may differ slightly
when some roster rows have missing ``perf``, because that helper uses teammate
*count* = all roster rows, not count of non-null ``perf``.

``peer_perf_sd_loo`` is the LOO *sample standard deviation* (ddof=1) of teammate
``perf`` over teammates with valid ``perf``, excluding self. NaN when the
team-season has fewer than three valid ``perf`` rows or fewer than two LOO peers.
"""

from __future__ import annotations

from typing import Literal

import numpy as np
import pandas as pd

# Notebook / modeling: toggle which regressor represents "pool" vs "crowding"
TIER1_QUALITY_COL = "congestion_quality"
TIER1_CROWDING_COL = "congestion_crowding"
TIER1_CROWDING_WEIGHTED_COL = "congestion_crowding_weighted"
TIER1_PEER_PERF_SD_LOO_COL = "peer_perf_sd_loo"

GROUP_COLS = ("team_id", "season")
REQUIRED_FOR_LOO = frozenset({"athlete_id", "team_id", "season", "perf"})


def add_tier1_mechanism_variables(
    df: pd.DataFrame,
    *,
    min_minutes: float | None = None,
    minutes_col: str = "minutes",
    perf_col: str = "perf",
    compute_weighted_crowding: bool = True,
) -> pd.DataFrame:
    """
    Add Tier 1 LOO columns using **only** teammate rows with non-null ``perf``.

    Parameters
    ----------
    min_minutes
        If set and ``> 0``, drop player-season rows below this threshold **before**
        any group stats (optional filter for future tight samples).
    minutes_col
        Column used for the weighted crowding variant (and for ``min_minutes``).
    perf_col
        Own-performance proxy (e.g. ``perf`` after ``assign_perf_from_metric(..., "ppm")``).
    compute_weighted_crowding
        If True, also compute ``congestion_crowding_weighted``:
        LOO sum of ``perf_l * minutes_l`` over teammates with valid ``perf`` and ``minutes``.
        Not the default Tier 1 estimand yet — retained for quick experiments.

    Returns
    -------
    Copy of ``df`` with:

    - ``congestion_quality`` — LOO mean teammate ``perf`` (VALID ``perf`` only).
    - ``congestion_crowding`` — LOO sum teammate ``perf`` (VALID ``perf`` only).
    - ``peer_perf_sd_loo`` — LOO std (ddof=1) of teammate ``perf`` among valid teammates.
    - ``congestion_crowding_weighted`` — optional; NaN when disabled or invalid inputs.
    """
    miss = REQUIRED_FOR_LOO - set(df.columns)
    if miss:
        raise KeyError(f"add_tier1_mechanism_variables missing columns: {sorted(miss)}")

    out = df.copy()

    if min_minutes is not None and float(min_minutes) > 0 and minutes_col in out.columns:
        out = out.loc[pd.to_numeric(out[minutes_col], errors="coerce") >= float(min_minutes)]

    g = out.groupby(list(GROUP_COLS), observed=True)
    sum_perf = g[perf_col].transform("sum")
    cnt_perf = g[perf_col].transform("count")

    own = pd.to_numeric(out[perf_col], errors="coerce")
    crowding_sum = sum_perf - own
    crowding_sum = crowding_sum.where(own.notna(), np.nan)

    denom = (cnt_perf - 1).replace(0, np.nan)
    quality_loo = crowding_sum / denom

    out[TIER1_CROWDING_COL] = crowding_sum
    out[TIER1_QUALITY_COL] = quality_loo

    sd_series = pd.Series(np.nan, index=out.index, dtype=float)
    for _, sub in out.groupby(list(GROUP_COLS), observed=True):
        p = pd.to_numeric(sub[perf_col], errors="coerce")
        arr = p.to_numpy(dtype=float)
        st = np.full(len(sub), np.nan, dtype=float)
        valid = np.isfinite(arr)
        iv = np.flatnonzero(valid)
        if iv.size >= 3:
            vals = arr[iv]
            for k in range(iv.size):
                peers = np.delete(vals, k)
                if peers.size >= 2:
                    st[iv[k]] = float(np.std(peers, ddof=1))
        sd_series.loc[sub.index] = st
    out[TIER1_PEER_PERF_SD_LOO_COL] = sd_series

    if compute_weighted_crowding:
        if minutes_col not in out.columns:
            out[TIER1_CROWDING_WEIGHTED_COL] = np.nan
        else:
            minutes = pd.to_numeric(out[minutes_col], errors="coerce")
            wm = own * minutes
            valid_w = own.notna() & minutes.notna() & (minutes > 0)
            wm_masked = wm.where(valid_w, np.nan)
            out["_wm_tier1"] = wm_masked
            sum_wm = out.groupby(list(GROUP_COLS), observed=True)["_wm_tier1"].transform("sum")
            cnt_wm = out.groupby(list(GROUP_COLS), observed=True)["_wm_tier1"].transform("count")
            own_wm = out["_wm_tier1"].where(own.notna(), np.nan)
            cw = sum_wm - own_wm
            cw = cw.where(own.notna(), np.nan)
            cw = cw.where(cnt_wm >= 2, np.nan)
            out[TIER1_CROWDING_WEIGHTED_COL] = cw
            out = out.drop(columns=["_wm_tier1"])
    else:
        out[TIER1_CROWDING_WEIGHTED_COL] = np.nan

    return out


def tier1_primary_pool_column(mode: Literal["quality", "crowding"]) -> str:
    """Return the canonical Tier 1 column name for Q-style vs C-style regressors."""
    if mode == "quality":
        return TIER1_QUALITY_COL
    if mode == "crowding":
        return TIER1_CROWDING_COL
    raise ValueError(f"mode must be 'quality' or 'crowding', got {mode!r}")
