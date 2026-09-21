#!/usr/bin/env python3
"""Army porch basic data plots — uniform 3×3 deck (panels 2–4, 6).

Mirrors tenure/scripts/tenure_basic_plots.py panel semantics for cross-domain comparison.

Run (AWS 520 root, e.g. Network_1P_shell — no PYTHONPATH needed):
  ./talent/re_entry/army_basic_plots.py --all
  ./talent/re_entry/army_basic_plots.py --input ./big_dfs/df_pipeline_11_cox_analysis.feather

Prerequisite: 520 through Cell 11 → big_dfs/df_pipeline_11_cox_analysis.feather
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from army_gallery_paths import (  # noqa: E402 — bootstraps sys.path
    BASIC_DATA_PLOTS,
    PREFIX,
    REPO,
    TAG_RUN1,
    ensure_army_output_dirs,
    resolve_feather,
)
from hero_plot_style import PLOT_DPI  # noqa: E402

# Run 1 · forward senior-rater columns (match pipeline_config_17_1)
COL_PID = "pid_pde"
COL_STOP = "stop_time"
COL_EVENT = "event"
COL_AI = "tb_ratio_fwd_snr"
COL_TJ = "pool_tb_ratio_mean_snr_fwd"
COL_LOO = "pool_minus_mean_snr_fwd"
COL_POOL_SIZE = "pool_size_snr_fwd"
COL_SNAPSHOT = "snpsht_dt"
COL_SNR = "snr_rater_bwd"  # Cell 6 pool key (matches pipeline_config base_time_varying_cols)
SNR_COL_CANDIDATES = ("snr_rater_bwd", "snr_rater", "snr_rater_fwd")
COL_PERF_Z = "z_tb_ratio_fwd_snr"
POOL_MIN = 3

ARMY_OVERLAP_LABELS = {
    "coverage_ylabel": "Senior-rater pools covering this level",
    "span_ylabel": "Snapshot × SNR pools",
    "sample_ylabel": "Sample of {n} pools (sorted by $\\hat{{T}}_j$)",
    "all_ylabel": "All snapshot × SNR pools (sorted by $\\hat{{T}}_j$)",
    "coverage_grid_note": "{frac:.1%} of grid with $>$1 pool",
    "legend_actual": "Actual senior-rater pools",
    "overlap_title": "Interval overlap along performance spectrum",
    "span_xlabel": r"Pool span ($\max \hat{A}_i - \min \hat{A}_i$)",
    "span_title": "Width of each pool's performance window",
    "sample_title": r"Pool $[\min, \max]$ intervals (sample)",
}

ECDF_PROMOTED = "#2166AC"
ECDF_ATTRITION = "#B2182B"
ECDF_CENSORED = "#757575"
ECDF_LOO_HIST = "#4daf4a"

GRAIN_LABEL = "Last snapshot per officer (Cell 11 grain)"
SNAPSHOT_GRAIN_LABEL = "All snapshot rows · pool = snpsht_dt × snr_rater_bwd"


def _z_within_groups(series: pd.Series) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    mu = float(s.mean())
    sd = float(s.std())
    if not np.isfinite(sd) or sd <= 0:
        return pd.Series(0.0, index=series.index)
    return (s - mu) / sd


_INVALID_SNR_VALUES = frozenset({"", "0", "0.0", "unknown", "Unknown", "nan", "NaN", "None"})


def _is_valid_snr_id(value: object) -> bool:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return False
    if pd.isna(value):
        return False
    if isinstance(value, (int, np.integer)) and value == 0:
        return False
    if isinstance(value, (float, np.floating)) and value == 0.0:
        return False
    return str(value).strip() not in _INVALID_SNR_VALUES


def _resolve_snr_col(panel: pd.DataFrame) -> str:
    """Cell 6 pools use snr_rater_bwd; Cell 11 export often drops rater IDs."""
    for cand in SNR_COL_CANDIDATES:
        if cand in panel.columns:
            return cand
    snr_like = [c for c in panel.columns if "snr" in c.lower() and "rater" in c.lower()]
    raise SystemExit(
        "Overlap panel needs a senior-rater ID column "
        f"({', '.join(SNR_COL_CANDIDATES)}). "
        "Re-run Cell 11 after adding snr_rater_bwd to pipeline_config base_time_varying_cols. "
        f"SNR-like columns seen: {snr_like or '(none)'}"
    )


def _load_pool_grouping_config() -> tuple[str, str, str, str, bool]:
    """Read Cell 5 pool toggles from pipeline_config (520 root on AWS)."""
    for root in (str(Path.cwd().resolve()), str(REPO)):
        if root not in sys.path:
            sys.path.insert(0, root)
        try:
            from pipeline_config import (  # noqa: WPS433
                POOL_ANCHOR_COL,
                POOL_EVAL_STRT_COL,
                POOL_EVAL_THRU_COL,
                POOL_EXCLUDE_PEER_TB_ZERO,
                POOL_GROUPING_MODE,
            )

            return (
                str(POOL_GROUPING_MODE).strip().lower(),
                POOL_EVAL_STRT_COL,
                POOL_EVAL_THRU_COL,
                POOL_ANCHOR_COL,
                bool(POOL_EXCLUDE_PEER_TB_ZERO),
            )
        except Exception:
            continue
    return ("legacy", "eval_strt_dt_bwd", "eval_thru_dt_bwd", "eval_thru_dt_bwd", False)


def _pool_members_for_overlap(work: pd.DataFrame, *, exclude_peer_tb_zero: bool) -> pd.DataFrame:
    """Drop tb_ratio == 0 rows from pool interval membership (matches Cell 5 toggle)."""
    if not exclude_peer_tb_zero or COL_AI not in work.columns:
        return work
    tb = pd.to_numeric(work[COL_AI], errors="coerce")
    return work.loc[tb != 0].copy()


def _resolve_overlap_group_cols(
    mode: str,
    snapshot_col: str,
    snr_col: str,
    eval_strt_col: str,
    eval_thru_col: str,
) -> list[str] | None:
    """Match Cell 5 resolve_pool_group_cols — None => active-at-anchor merge."""
    if mode == "legacy":
        return [snapshot_col, snr_col]
    if mode == "rating_window":
        return [snapshot_col, snr_col, eval_strt_col, eval_thru_col]
    if mode in ("active_at_eval_thru", "active_at_snapshot"):
        return None
    raise ValueError(
        f"Unknown pool_grouping_mode={mode!r}. "
        "Expected legacy, rating_window, active_at_eval_thru, or active_at_snapshot."
    )


def _overlap_grain_label(
    mode: str,
    snr_col: str,
    *,
    anchor_col: str,
    exclude_peer_tb_zero: bool = False,
) -> str:
    prefix = "All snapshot rows · pool = "
    if mode == "legacy":
        grain = f"{prefix}{COL_SNAPSHOT} × {snr_col}"
    elif mode == "rating_window":
        grain = f"{prefix}{COL_SNAPSHOT} × {snr_col} × eval window"
    elif mode == "active_at_eval_thru":
        grain = f"{prefix}{snr_col} × peers active at {anchor_col}"
    elif mode == "active_at_snapshot":
        grain = f"{prefix}{snr_col} × peers active at {COL_SNAPSHOT}"
    else:
        grain = SNAPSHOT_GRAIN_LABEL.replace("snr_rater", snr_col)
    if exclude_peer_tb_zero:
        grain += " · exclude tb_ratio=0 peers"
    return grain


def _overlap_span_label(mode: str) -> str:
    if mode == "legacy":
        return "Snapshot × SNR pools"
    if mode == "rating_window":
        return "Snapshot × SNR × eval-window pools"
    if mode in ("active_at_eval_thru", "active_at_snapshot"):
        return "Active senior-rater pools"
    return "Senior-rater pools"


def _intervals_from_row_groupby(
    work: pd.DataFrame,
    group_cols: list[str],
    snr_col: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    iv = (
        work.groupby(group_cols, observed=True)["perf"]
        .agg(
            A_hat_min="min",
            A_hat_max="max",
            T_j_hat="mean",
            roster_n="count",
        )
        .reset_index()
    )
    iv = iv.loc[iv["roster_n"] >= POOL_MIN].copy()
    iv["perf_span"] = iv["A_hat_max"] - iv["A_hat_min"]

    members = work.copy()
    members["team_id"] = members[snr_col].astype(str)
    if COL_SNAPSHOT in group_cols:
        members["season"] = members[COL_SNAPSHOT].dt.strftime("%Y-%m-%d")
        iv["team_id"] = iv[snr_col].astype(str)
        iv["season"] = pd.to_datetime(iv[COL_SNAPSHOT]).dt.strftime("%Y-%m-%d")
    else:
        season_col = group_cols[-1]
        members["season"] = pd.to_datetime(members[season_col]).dt.strftime("%Y-%m-%d")
        iv["team_id"] = iv[snr_col].astype(str)
        iv["season"] = pd.to_datetime(iv[season_col]).dt.strftime("%Y-%m-%d")
    return iv, members


def _intervals_active_at_anchor(
    work: pd.DataFrame,
    *,
    snr_col: str,
    anchor_col: str,
    eval_strt_col: str,
    eval_thru_col: str,
    pid_col: str,
    tb_col: str | None = None,
    exclude_peer_tb_zero: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Pool intervals where peers = officers under same SNR with OER window covering anchor."""
    for col in (anchor_col, eval_strt_col, eval_thru_col):
        if col not in work.columns:
            raise SystemExit(
                f"Overlap active-at-anchor mode needs column {col!r} in feather — "
                "re-run Cell 11 with eval dates in base_time_varying_cols."
            )
        work[col] = pd.to_datetime(work[col], errors="coerce")

    peers = work.dropna(subset=[snr_col, eval_strt_col, eval_thru_col, "perf", pid_col])
    if exclude_peer_tb_zero and tb_col and tb_col in peers.columns:
        peer_tb = pd.to_numeric(peers[tb_col], errors="coerce")
        peers = peers.loc[peer_tb != 0].copy()
    peers = peers.drop_duplicates(
        subset=[pid_col, snr_col, eval_strt_col, eval_thru_col],
        keep="last",
    )
    anchors = work.dropna(subset=[snr_col, anchor_col]).drop_duplicates([snr_col, anchor_col])
    if anchors.empty or peers.empty:
        empty = pd.DataFrame(
            columns=[
                snr_col,
                anchor_col,
                "A_hat_min",
                "A_hat_max",
                "T_j_hat",
                "roster_n",
                "perf_span",
                "team_id",
                "season",
            ]
        )
        return empty, empty

    peer_g = peers.rename(
        columns={
            pid_col: "_peer_pid",
            eval_strt_col: "_peer_strt",
            eval_thru_col: "_peer_thru",
            "perf": "_peer_perf",
        }
    )
    cross = anchors.merge(peer_g, on=snr_col, how="inner")
    cross = cross[
        (cross[anchor_col] >= cross["_peer_strt"])
        & (cross[anchor_col] <= cross["_peer_thru"])
    ]
    if cross.empty:
        empty = pd.DataFrame(
            columns=[
                snr_col,
                anchor_col,
                "A_hat_min",
                "A_hat_max",
                "T_j_hat",
                "roster_n",
                "perf_span",
                "team_id",
                "season",
            ]
        )
        return empty, empty

    iv = (
        cross.groupby([snr_col, anchor_col], observed=True)
        .agg(
            A_hat_min=("_peer_perf", "min"),
            A_hat_max=("_peer_perf", "max"),
            T_j_hat=("_peer_perf", "mean"),
            roster_n=("_peer_perf", "count"),
        )
        .reset_index()
    )
    iv = iv.loc[iv["roster_n"] >= POOL_MIN].copy()
    iv["perf_span"] = iv["A_hat_max"] - iv["A_hat_min"]
    iv["team_id"] = iv[snr_col].astype(str)
    iv["season"] = pd.to_datetime(iv[anchor_col]).dt.strftime("%Y-%m-%d")

    members = cross.copy()
    members["perf"] = members["_peer_perf"]
    members["team_id"] = members[snr_col].astype(str)
    members["season"] = pd.to_datetime(members[anchor_col]).dt.strftime("%Y-%m-%d")
    return iv, members


def _prepare_army_overlap(panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, str, str]:
    """Build pool intervals — grain follows pipeline_config POOL_GROUPING_MODE (Cell 5)."""
    mode, eval_strt_col, eval_thru_col, pool_anchor_col, exclude_peer_tb_zero = (
        _load_pool_grouping_config()
    )
    snr_col = _resolve_snr_col(panel)
    if COL_SNAPSHOT not in panel.columns:
        raise SystemExit(f"Overlap panel missing column: {COL_SNAPSHOT}")
    if COL_POOL_SIZE not in panel.columns:
        raise SystemExit(f"Overlap panel missing column: {COL_POOL_SIZE}")

    work = panel.copy()
    if COL_PERF_Z in work.columns:
        work["perf"] = pd.to_numeric(work[COL_PERF_Z], errors="coerce")
        xlab = r"Own TB ratio SNR fwd ($z$ from pipeline)"
    elif COL_AI in work.columns:
        work["perf"] = work.groupby(COL_SNAPSHOT, observed=True)[COL_AI].transform(_z_within_groups)
        xlab = r"Own TB ratio SNR fwd ($z$ within snapshot)"
    else:
        raise SystemExit(f"Overlap panel needs {COL_PERF_Z} or {COL_AI} in feather.")

    work[COL_SNAPSHOT] = pd.to_datetime(work[COL_SNAPSHOT], errors="coerce")
    work = work.dropna(subset=[COL_SNAPSHOT, "perf"])
    valid_snr = work[snr_col].map(_is_valid_snr_id)
    n_bad_snr = int((~valid_snr).sum())
    if n_bad_snr:
        print(f"  Overlap: dropping {n_bad_snr:,} rows with missing/invalid {snr_col}")
    work = work.loc[valid_snr].copy()
    pool_size = pd.to_numeric(work[COL_POOL_SIZE], errors="coerce")
    work = work.loc[pool_size >= POOL_MIN].copy()

    group_cols = _resolve_overlap_group_cols(
        mode, COL_SNAPSHOT, snr_col, eval_strt_col, eval_thru_col
    )
    anchor_col = COL_SNAPSHOT if mode == "active_at_snapshot" else pool_anchor_col
    print(
        f"  Overlap pool grain: POOL_GROUPING_MODE={mode!r} "
        f"POOL_EXCLUDE_PEER_TB_ZERO={exclude_peer_tb_zero}"
    )

    pool_work = _pool_members_for_overlap(work, exclude_peer_tb_zero=exclude_peer_tb_zero)
    if group_cols is not None:
        for col in group_cols:
            if col in (eval_strt_col, eval_thru_col):
                pool_work[col] = pd.to_datetime(pool_work[col], errors="coerce")
        iv, work = _intervals_from_row_groupby(pool_work, group_cols, snr_col)
    else:
        iv, work = _intervals_active_at_anchor(
            pool_work,
            snr_col=snr_col,
            anchor_col=anchor_col,
            eval_strt_col=eval_strt_col,
            eval_thru_col=eval_thru_col,
            pid_col=_resolve_pid_col(pool_work),
            tb_col=COL_AI if COL_AI in pool_work.columns else None,
            exclude_peer_tb_zero=exclude_peer_tb_zero,
        )

    grain = _overlap_grain_label(
        mode,
        snr_col,
        anchor_col=anchor_col,
        exclude_peer_tb_zero=exclude_peer_tb_zero,
    )
    return iv, work, xlab, grain


def _compute_h_sort(work: pd.DataFrame) -> float | None:
    """Realized sorting index on overlap pools (optional if 541 module absent)."""
    try:
        import importlib

        sports_root = str(REPO / "sports")
        if sports_root not in sys.path:
            sys.path.insert(0, sports_root)
        gc = importlib.import_module("541_grandchild_homophily_assign")
        use = work.dropna(subset=["perf"]).copy()
        if "team_id" in use.columns and "season" in use.columns:
            use["pool_id"] = use.groupby(["team_id", "season"], observed=True).ngroup()
        else:
            snr_col = _resolve_snr_col(work)
            use["pool_id"] = use.groupby([COL_SNAPSHOT, snr_col], observed=True).ngroup()
        return float(
            gc.realized_sorting_index_H_sort(
                use["perf"].to_numpy(dtype=float),
                use["pool_id"].to_numpy(dtype=np.int64),
            )
        )
    except Exception as exc:
        print(f"  H_sort skipped: {exc}")
        return None


def _resolve_pid_col(panel: pd.DataFrame) -> str:
    for cand in (COL_PID, "pid", "officer_id"):
        if cand in panel.columns:
            return cand
    raise SystemExit(f"Overlap panel needs an officer ID column ({COL_PID}).")


def run_pool_interval_overlap(feather_path: Path, *, tag: str = TAG_RUN1) -> Path:
    """Panel 5 — senior-rater pool interval overlap (assortativity diagnostic)."""
    from empirical_team_interval_overlap import build_figure  # noqa: WPS433

    panel = pd.read_feather(feather_path)
    iv, work, xlab, grain = _prepare_army_overlap(panel)
    if iv.empty:
        raise SystemExit("No pools for overlap panel — check snapshot / SNR columns.")

    mode, _, _, pool_anchor_col, exclude_peer_tb_zero = _load_pool_grouping_config()
    span_lbl = _overlap_span_label(mode)
    overlap_labels = dict(ARMY_OVERLAP_LABELS)
    overlap_labels["span_ylabel"] = span_lbl
    overlap_labels["all_ylabel"] = f"All {span_lbl.lower()} (sorted by $\\hat{{T}}_j$)"

    date_col = COL_SNAPSHOT if COL_SNAPSHOT in work.columns else pool_anchor_col
    dates = pd.to_datetime(work[date_col], errors="coerce").dropna()
    seasons = f"{dates.min():%Y-%m-%d} to {dates.max():%Y-%m-%d}" if not dates.empty else "n/a"

    stem = f"{PREFIX}_BDP_pool_interval_overlap_{tag}"
    out_png = BASIC_DATA_PLOTS / f"{stem}.png"
    out_csv = BASIC_DATA_PLOTS / f"{stem}_pool_snapshot.csv"
    out_meta = BASIC_DATA_PLOTS / f"{stem}.json"

    iv.to_csv(out_csv, index=False)
    print(f"Wrote {out_csv.relative_to(REPO)}")

    h_sort = _compute_h_sort(work)
    h_line = f"\nRealized sorting $H_{{sort}}={h_sort:.3f}$" if h_sort is not None else ""
    stats = build_figure(
        iv,
        work,
        png_path=out_png,
        seasons=seasons,
        h_sort=h_sort,
        suptitle=(
            f"{PREFIX} — senior-rater pool interval overlap ({seasons})"
            + h_line
        ),
        xlab=xlab,
        labels=overlap_labels,
        grain_badge=grain,
    )

    meta = {
        "date": date.today().isoformat(),
        "panel": 5,
        "diagnostic": "army_pool_interval_overlap",
        "pool_grouping_mode": mode,
        "pool_exclude_peer_tb_zero": exclude_peer_tb_zero,
        "pool_unit": grain.split("pool = ")[-1] if "pool = " in grain else f"{COL_SNAPSHOT} × snr_rater_bwd",
        "pool_min": POOL_MIN,
        "seasons": seasons,
        "grain": grain,
        **stats,
        "n_pools": stats.get("n_team_seasons"),
        "n_snapshot_rows": stats.get("n_player_seasons"),
        "outputs": {"png": out_png.name, "pool_csv": out_csv.name},
    }
    _write_meta(out_meta, meta)
    print(f"Wrote {out_png.relative_to(REPO)}")
    return out_png


def _summary(name: str, values: np.ndarray) -> dict[str, float | int]:
    v = values[np.isfinite(values)]
    if v.size == 0:
        return {"name": name, "n": 0}
    return {
        "name": name,
        "n": int(v.size),
        "mean": float(np.mean(v)),
        "median": float(np.median(v)),
        "std": float(np.std(v)),
        "p05": float(np.percentile(v, 5)),
        "p95": float(np.percentile(v, 95)),
    }


def _write_meta(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _plot_ecdf(
    ax,
    values: np.ndarray,
    *,
    color: str,
    label: str,
    lw: float = 2.0,
    ls: str = "-",
    alpha: float = 1.0,
) -> None:
    v = np.sort(values[np.isfinite(values)])
    if v.size == 0:
        return
    ys = np.arange(1, v.size + 1) / v.size
    ax.step(v, ys, where="post", color=color, lw=lw, label=label, ls=ls, alpha=alpha)


def load_officer_last_snapshot(feather_path: Path) -> tuple[pd.DataFrame, dict[str, Any]]:
    """One row per officer — last interval by stop_time (Cell 11 collapse rule)."""
    raw = pd.read_feather(feather_path)
    need = [COL_PID, COL_STOP, COL_EVENT, COL_AI, COL_LOO, COL_TJ]
    missing = [c for c in need if c not in raw.columns]
    if missing:
        raise SystemExit(f"Missing columns in feather: {missing}")

    work = raw.copy()
    work[COL_STOP] = pd.to_numeric(work[COL_STOP], errors="coerce")
    work = work.sort_values([COL_PID, COL_STOP])
    last = work.groupby(COL_PID, as_index=False).tail(1).copy()

    # Ever-promoted / ever-attrited flags from full panel
    ever = work.groupby(COL_PID)[COL_EVENT].agg(
        ever_promoted=lambda s: bool((s == 1).any()),
        ever_attrition=lambda s: bool((s == 2).any()),
    )
    last = last.merge(ever, on=COL_PID, how="left")
    last["outcome"] = np.where(
        last["ever_promoted"],
        "promoted",
        np.where(last["ever_attrition"], "attrition", "censored"),
    )

    stats = {
        "n_officers": int(last[COL_PID].nunique()),
        "n_rows_raw": int(len(raw)),
        "n_promoted": int((last["outcome"] == "promoted").sum()),
        "n_attrition": int((last["outcome"] == "attrition").sum()),
        "n_censored": int((last["outcome"] == "censored").sum()),
        "feather": str(feather_path),
        "grain": GRAIN_LABEL,
    }
    if COL_POOL_SIZE in last.columns:
        ps = pd.to_numeric(last[COL_POOL_SIZE], errors="coerce")
        stats["median_pool_size"] = float(np.nanmedian(ps))
    return last, stats


def run_ai_tj(officers: pd.DataFrame, *, tag: str = TAG_RUN1) -> Path:
    """Panel 2 — own TB ratio vs pool mean (T̂_j includes self)."""
    ai = pd.to_numeric(officers[COL_AI], errors="coerce").to_numpy(dtype=float)
    tj = pd.to_numeric(officers[COL_TJ], errors="coerce").to_numpy(dtype=float)
    mask = np.isfinite(ai) & np.isfinite(tj)
    ai, tj = ai[mask], tj[mask]

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6))
    fig.subplots_adjust(wspace=0.28, top=0.84)

    ax = axes[0]
    ax.hist(ai, bins=48, color="steelblue", alpha=0.85, edgecolor="white", linewidth=0.35)
    s_ai = _summary(COL_AI, ai)
    ax.set_title(r"Own performance ($\hat{A}_i$ · TB ratio SNR fwd)", fontsize=10)
    ax.set_xlabel("tb_ratio_fwd_snr")
    ax.set_ylabel("Officers")
    ax.text(
        0.98, 0.98,
        f"n={s_ai['n']:,}\nmed={s_ai['median']:.3f}",
        transform=ax.transAxes, ha="right", va="top", fontsize=8,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
    )

    ax = axes[1]
    ax.hist(tj, bins=48, color="#E8B923", alpha=0.85, edgecolor="white", linewidth=0.35)
    s_tj = _summary(COL_TJ, tj)
    ax.set_title(r"Pool mean talent ($\hat{T}_j$ · incl. self)", fontsize=10)
    ax.set_xlabel("pool_tb_ratio_mean_snr_fwd")
    ax.set_ylabel("Officers")
    ax.text(
        0.98, 0.98,
        f"n={s_tj['n']:,}\nmed={s_tj['median']:.3f}",
        transform=ax.transAxes, ha="right", va="top", fontsize=8,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
    )

    fig.suptitle(f"{PREFIX} BDP · Â_i and T̂_j · {GRAIN_LABEL}", fontsize=11, fontweight="bold", y=0.98)
    stem = f"{PREFIX}_BDP_Ai_Tj_{tag}"
    out_png = BASIC_DATA_PLOTS / f"{stem}.png"
    out_meta = BASIC_DATA_PLOTS / f"{stem}.json"
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(out_png, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    _write_meta(out_meta, {"date": date.today().isoformat(), "panel": 2, "stats_ai": s_ai, "stats_tj": s_tj})
    print(f"Wrote {out_png.relative_to(REPO)}")
    return out_png


def run_pool_loo_distribution(officers: pd.DataFrame, *, tag: str = TAG_RUN1) -> Path:
    """Panel 3 — LOO pool minus mean (peer context support)."""
    loo = pd.to_numeric(officers[COL_LOO], errors="coerce").to_numpy(dtype=float)
    loo = loo[np.isfinite(loo)]
    if loo.size == 0:
        raise SystemExit(f"No finite values in {COL_LOO} — check pool LOO columns in feather.")
    stats = _summary(COL_LOO, loo)
    lo, hi = float(np.min(loo)), float(np.max(loo))
    if lo == hi:
        lo, hi = lo - 0.5, hi + 0.5
    bins = np.linspace(lo, hi, 36)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6))
    fig.subplots_adjust(wspace=0.28, top=0.84)

    ax = axes[0]
    ax.hist(loo, bins=bins, color=ECDF_LOO_HIST, alpha=0.85, edgecolor="white", linewidth=0.35)
    ax.axvline(stats["median"], color="0.35", linestyle=":", linewidth=1.4)
    ax.set_xlabel("pool_minus_mean_snr_fwd (LOO peer context)")
    ax.set_ylabel("Officers")
    ax.set_title("Peer pool quality (LOO minus mean)", fontsize=10)

    ax = axes[1]
    _plot_ecdf(ax, loo, color=ECDF_LOO_HIST, label=f"All ($n={stats['n']:,}$)", lw=1.8, ls="-")
    for key, color, ls in (
        ("promoted", ECDF_PROMOTED, "-"),
        ("attrition", ECDF_ATTRITION, "--"),
    ):
        sub = officers.loc[officers["outcome"] == key, COL_LOO].to_numpy(dtype=float)
        if sub.size:
            _plot_ecdf(ax, sub, color=color, label=f"{key} ($n={sub.size:,}$)", lw=2.2, ls=ls)
    ax.set_xlim(lo, hi)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("pool_minus_mean_snr_fwd")
    ax.set_ylabel(r"ECDF  $F(x)$")
    ax.set_title("ECDF by eventual outcome", fontsize=10)
    ax.legend(fontsize=7, loc="lower right", framealpha=0.95)
    ax.grid(alpha=0.2)

    fig.suptitle(f"{PREFIX} BDP · pool LOO distribution · {GRAIN_LABEL}", fontsize=11, fontweight="bold", y=0.98)
    stem = f"{PREFIX}_BDP_pool_minus_mean_loo_{tag}"
    out_png = BASIC_DATA_PLOTS / f"{stem}.png"
    out_meta = BASIC_DATA_PLOTS / f"{stem}.json"
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(out_png, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    _write_meta(out_meta, {"date": date.today().isoformat(), "panel": 3, "stats": stats})
    print(f"Wrote {out_png.relative_to(REPO)}")
    return out_png


def run_promotion_mass_ecdf(officers: pd.DataFrame, *, tag: str = TAG_RUN1) -> Path:
    """Panel 4 — cumulative share of promotions by own-TB (Â) tiers."""
    ai = pd.to_numeric(officers[COL_AI], errors="coerce")
    promoted = officers["outcome"] == "promoted"
    work = pd.DataFrame({"ai": ai, "promoted": promoted}).dropna()
    work = work.sort_values("ai")
    n_prom = int(work["promoted"].sum())
    if n_prom == 0:
        raise SystemExit("No promoted officers in panel — check event coding.")

    work["cum_prom_share"] = work["promoted"].cumsum() / n_prom

    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.step(work["ai"], work["cum_prom_share"], where="post", color=ECDF_PROMOTED, lw=2.2)
    ax.set_xlabel(r"Own TB ratio SNR fwd ($\hat{A}_i$)")
    ax.set_ylabel("Cumulative share of promotions")
    ax.set_title(
        f"{PREFIX} — promotion mass vs own performance\n{GRAIN_LABEL} · n_prom={n_prom:,}",
        fontsize=11,
        fontweight="bold",
    )
    ax.set_ylim(0, 1.02)
    ax.grid(alpha=0.25)

    stem = f"{PREFIX}_BDP_promotion_mass_ecdf_{tag}"
    out_png = BASIC_DATA_PLOTS / f"{stem}.png"
    out_meta = BASIC_DATA_PLOTS / f"{stem}.json"
    fig.tight_layout()
    fig.savefig(out_png, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    _write_meta(
        out_meta,
        {
            "date": date.today().isoformat(),
            "panel": 4,
            "n_promoted": n_prom,
            "n_officers": len(work),
        },
    )
    print(f"Wrote {out_png.relative_to(REPO)}")
    return out_png


def run_pool_size_distribution(officers: pd.DataFrame, *, tag: str = TAG_RUN1) -> Path:
    """Panel 6 — senior-rater pool size at last snapshot."""
    if COL_POOL_SIZE not in officers.columns:
        raise SystemExit(f"Column {COL_POOL_SIZE} not in feather — re-run 520 pool cells.")
    ps = pd.to_numeric(officers[COL_POOL_SIZE], errors="coerce").to_numpy(dtype=float)
    stats = _summary(COL_POOL_SIZE, ps)

    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.hist(ps, bins=40, color="steelblue", alpha=0.85, edgecolor="white")
    ax.set_xlabel("pool_size_snr_fwd (senior-rater pool count)")
    ax.set_ylabel("Officers")
    ax.set_title(f"{PREFIX} — pool size |T_j| · {GRAIN_LABEL}", fontsize=11, fontweight="bold")
    ax.text(
        0.98, 0.98,
        f"n={stats['n']:,}\nmed={stats['median']:.0f}",
        transform=ax.transAxes, ha="right", va="top", fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
    )
    stem = f"{PREFIX}_BDP_pool_size_{tag}"
    out_png = BASIC_DATA_PLOTS / f"{stem}.png"
    out_meta = BASIC_DATA_PLOTS / f"{stem}.json"
    fig.tight_layout()
    fig.savefig(out_png, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    _write_meta(out_meta, {"date": date.today().isoformat(), "panel": 6, "stats": stats})
    print(f"Wrote {out_png.relative_to(REPO)}")
    return out_png


PLOT_RUNNERS = {
    "ai_tj": lambda df, _s: run_ai_tj(df),
    "pool_loo": lambda df, _s: run_pool_loo_distribution(df),
    "promotion_mass": lambda df, _s: run_promotion_mass_ecdf(df),
    "pool_size": lambda df, _s: run_pool_size_distribution(df),
}
# overlap uses full snapshot panel — handled in main() via run_pool_interval_overlap(feather)


def main() -> None:
    parser = argparse.ArgumentParser(description="Army porch basic data plots (BDP)")
    parser.add_argument("--input", type=Path, default=None, help="df_pipeline_11 feather path")
    parser.add_argument(
        "--only",
        nargs="+",
        default=None,
        choices=sorted({*PLOT_RUNNERS, "overlap"}),
        help="Subset of panels to build",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Build all implemented BDP panels (default if --only omitted)",
    )
    args = parser.parse_args()

    ensure_army_output_dirs()
    feather = resolve_feather(args.input)
    officers, cohort_stats = load_officer_last_snapshot(feather)
    print(
        f"Loaded {cohort_stats['n_officers']:,} officers from {feather.name} "
        f"(promoted={cohort_stats['n_promoted']:,}, "
        f"attrition={cohort_stats['n_attrition']:,}, "
        f"censored={cohort_stats['n_censored']:,})"
    )

    default_keys = sorted({*PLOT_RUNNERS, "overlap"})
    keys = args.only if args.only else default_keys
    manifest: list[dict[str, str]] = []
    for key in keys:
        if key == "overlap":
            png = run_pool_interval_overlap(feather)
        else:
            png = PLOT_RUNNERS[key](officers, cohort_stats)
        manifest.append({"key": key, "png": png.name})

    manifest_path = BASIC_DATA_PLOTS / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "date": date.today().isoformat(),
                "cohort": cohort_stats,
                "plots": manifest,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {manifest_path.relative_to(REPO)}")
    print("Done.")


if __name__ == "__main__":
    main()
