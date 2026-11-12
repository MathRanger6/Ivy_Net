#!/usr/bin/env python3
"""Pool size probe: computed vs Army official.

Run from 520 root:
  python -u talent/re_entry/army_pool_size_probe.py

Reads POOL_GROUPING_MODE from pipeline_config when available (informational).
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

OFFICIAL = "snr_rater_rates_this_grd"  # rates not pools
COMPUTED = "pool_size_snr_fwd"


def _pool_config_labels() -> tuple[str, bool]:
    try:
        # Script lives in talent/re_entry/; pipeline_config.py is at 520 root.
        root = str(Path.cwd())
        if root not in sys.path:
            sys.path.insert(0, root)
        from pipeline_config import (  # noqa: WPS433
            POOL_EXCLUDE_PEER_TB_ZERO,
            POOL_GROUPING_MODE,
        )

        return str(POOL_GROUPING_MODE), bool(POOL_EXCLUDE_PEER_TB_ZERO)
    except Exception:
        return "unknown", False


def resolve_feather() -> Path:
    p = Path.cwd() / "big_dfs" / "df_pipeline_11_cox_analysis.feather"
    if not p.is_file():
        raise FileNotFoundError(f"Missing {p} — run 520 Cell 11 first.")
    return p


def summarize(label: str, series: pd.Series) -> None:
    x = pd.to_numeric(series, errors="coerce").dropna()
    if x.empty:
        print(f"{label}: no data", flush=True)
        return
    print(
        f"{label}: n={len(x):,} max={x.max():.0f} median={x.median():.0f} "
        f"p95={x.quantile(0.95):.0f} pct>50={(x > 50).mean():.1%}",
        flush=True,
    )


def _active_at_eval_thru_pool_size(
    snap: pd.DataFrame,
    *,
    exclude_peer_tb_zero: bool = False,
) -> pd.Series:
    """Simulate active_at_eval_thru LOO pool size (unique peers at eval_thru)."""
    cols = [
        "pid_pde",
        "snr_rater_bwd",
        "eval_strt_dt_bwd",
        "eval_thru_dt_bwd",
        "tb_ratio_fwd_snr",
    ]
    work = snap[cols].copy()
    for c in ("eval_strt_dt_bwd", "eval_thru_dt_bwd"):
        work[c] = pd.to_datetime(work[c], errors="coerce")
    out = pd.Series(np.nan, index=snap.index, dtype=float)
    valid = (
        work["snr_rater_bwd"].notna()
        & work["eval_thru_dt_bwd"].notna()
        & work["eval_strt_dt_bwd"].notna()
        & work["tb_ratio_fwd_snr"].notna()
    )
    peers = work.loc[valid].drop_duplicates(
        subset=["pid_pde", "snr_rater_bwd", "eval_strt_dt_bwd", "eval_thru_dt_bwd"],
        keep="last",
    )
    if exclude_peer_tb_zero:
        peer_tb = pd.to_numeric(peers["tb_ratio_fwd_snr"], errors="coerce")
        peers = peers.loc[peer_tb != 0].copy()
    left = work.loc[valid]
    if not left.empty and not peers.empty:
        peer_g = peers.rename(
            columns={
                "pid_pde": "_peer_pid",
                "eval_strt_dt_bwd": "_ps",
                "eval_thru_dt_bwd": "_pt",
            }
        )
        cross = left.merge(peer_g, on="snr_rater_bwd", how="inner")
        cross = cross[
            (cross["eval_thru_dt_bwd"] >= cross["_ps"])
            & (cross["eval_thru_dt_bwd"] <= cross["_pt"])
            & (cross["pid_pde"] != cross["_peer_pid"])
        ]
        if not cross.empty:
            counts = cross.groupby(cross.index, sort=False).size()
            out.loc[counts.index] = counts.astype(float)
    return out


def _probe_tb_zero_peer_share(snap: pd.DataFrame) -> None:
    """How many pool-eligible rows have tb_ratio == 0 (peer-exclusion sensitivity)."""
    ratio = pd.to_numeric(snap.get("tb_ratio_fwd_snr"), errors="coerce")
    valid = ratio.notna()
    if not valid.any():
        print("tb_zero peers: no finite tb_ratio_fwd_snr on Cell 5 panel", flush=True)
        return
    is_zero = valid & (ratio == 0)
    n_valid = int(valid.sum())
    n_zero = int(is_zero.sum())
    print(
        f"tb_ratio_fwd_snr==0 (Cell 5 rows): n={n_zero:,} / {n_valid:,} "
        f"({100.0 * n_zero / n_valid:.1f}%)",
        flush=True,
    )


def _probe_tb_zero_pool_impact(snap: pd.DataFrame, *, pool_min: int = 3) -> None:
    """Compare active_at_eval_thru LOO sizes with vs without zero-TB peers."""
    base = _active_at_eval_thru_pool_size(snap, exclude_peer_tb_zero=False)
    excl = _active_at_eval_thru_pool_size(snap, exclude_peer_tb_zero=True)
    ok_base = base.dropna()
    ok_excl = excl.dropna()
    if ok_base.empty:
        print("tb_zero pool impact: no simulated pools (check eval date columns)", flush=True)
        return
    lost = int((base.notna() & excl.isna()).sum())
    shrunk = ok_excl - base.reindex(excl.index)
    print(
        f"tb_zero pool impact (active_at_eval_thru sim): "
        f"median size {ok_base.median():.0f} -> {ok_excl.median() if not ok_excl.empty else float('nan'):.0f}; "
        f"pools lost (>= {pool_min} -> NaN)={lost:,}; "
        f"median shrink among survivors={(shrunk.dropna().median() if shrunk.notna().any() else 0):.0f}",
        flush=True,
    )


def main() -> None:
    mode, exclude_zero = _pool_config_labels()
    print(f"pipeline POOL_GROUPING_MODE={mode}", flush=True)
    print(f"pipeline POOL_EXCLUDE_PEER_TB_ZERO={exclude_zero}", flush=True)
    feather = resolve_feather()
    print(f"Reading {feather}", flush=True)
    df = pd.read_feather(feather)
    print(f"Cell 11: rows={len(df):,}", flush=True)

    last = df.sort_values(["pid_pde", "stop_time"]).groupby("pid_pde").tail(1)
    if COMPUTED in last.columns:
        summarize(f"computed {COMPUTED} (last snapshot)", last[COMPUTED])

    oer_path = Path.cwd() / "big_dfs" / "df_oer_enriched.feather"
    try:
        summarize(
            f"official {OFFICIAL} (OER rows)",
            pd.read_feather(oer_path, columns=[OFFICIAL])[OFFICIAL],
        )
    except Exception as exc:
        print(f"official {OFFICIAL}: skipped ({exc})", flush=True)

    p05 = Path.cwd() / "big_dfs" / "df_pipeline_05_pool_means.feather"
    try:
        p05_cols = [
            "pid_pde",
            "snr_rater_bwd",
            "eval_strt_dt_bwd",
            "eval_thru_dt_bwd",
            "tb_ratio_fwd_snr",
            COMPUTED,
        ]
        snap = pd.read_feather(p05, columns=p05_cols)
        if COMPUTED in snap.columns:
            summarize(f"Cell 5 {COMPUTED} (all rows, fresh)", snap[COMPUTED])
        cnt = snap.groupby(
            ["snr_rater_bwd", "eval_strt_dt_bwd", "eval_thru_dt_bwd"],
            observed=True,
        )["tb_ratio_fwd_snr"].transform("count")
        summarize("alt rating_window key (snr x eval window)", cnt)
        _probe_tb_zero_peer_share(snap)
        _probe_tb_zero_pool_impact(snap)
        active = _active_at_eval_thru_pool_size(snap, exclude_peer_tb_zero=exclude_zero)
        summarize("sim active_at_eval_thru (matches config zero-excl)", active.dropna())
        if not exclude_zero:
            active_ex = _active_at_eval_thru_pool_size(snap, exclude_peer_tb_zero=True)
            summarize("sim active_at_eval_thru (exclude tb_zero peers)", active_ex.dropna())
    except Exception as exc:
        print(f"alt pool: skipped ({exc})", flush=True)


if __name__ == "__main__":
    try:
        main()
        print("Done.", flush=True)
    except Exception as exc:
        print(f"FATAL: {exc}", file=sys.stderr, flush=True)
        sys.exit(1)
