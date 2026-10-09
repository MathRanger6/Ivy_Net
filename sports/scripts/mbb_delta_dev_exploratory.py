#!/usr/bin/env python3
"""Exploratory Δ development (first PS → last PS) vs team / LOO / congestion.

Spec: sports/documents/MBB_DELTA_PPM_DEVELOPMENT_EXPLORATORY_SPEC.md

Run (repo root):
  PYTHONPATH=sports python sports/scripts/mbb_delta_dev_exploratory.py
  PYTHONPATH=sports python sports/scripts/mbb_delta_dev_exploratory.py --preset reigning --out-dir sports/exports/delta_ppm_dev/smoke
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SPORTS = REPO / "sports"
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SPORTS))
sys.path.insert(0, str(SCRIPTS))

DEFAULT_OUT = (
    REPO
    / "3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/_DISPOSABLE_delta_dev"
)

THETA_SPECS = {
    "drafted_median": "congestion_viable_drafted_med",
    "global_median": "congestion_viable_global_med",
    "fixed_zero": "congestion_viable_z0",
}

ENDPOINT_MINUTES_BOTH = "both"
ENDPOINT_MINUTES_LAST_ONLY = "last-only"
ENDPOINT_MINUTES_MODES = frozenset({ENDPOINT_MINUTES_BOTH, ENDPOINT_MINUTES_LAST_ONLY})

FIT_CURVES_OFF = "off"
FIT_CURVES_POOLED_QUADRATIC = "pooled-quadratic"
FIT_CURVES_SPLIT_QUADRATIC = "split-quadratic"
FIT_CURVES_MODES = frozenset(
    {FIT_CURVES_OFF, FIT_CURVES_POOLED_QUADRATIC, FIT_CURVES_SPLIT_QUADRATIC}
)
_QUADRATIC_MIN_N = 30

# Box-only metrics suitable for Δ dev without SR merge (extend via perf_metric.PERF_METRIC_BOX_ONLY).
from sports_pipeline.perf_metric import PERF_METRIC_BOX_ONLY  # noqa: E402


@dataclass
class DeltaDevSpec:
    season_min: int = 2009
    season_max: int = 2021
    use_prebuilt_panel_csv: bool = False
    drop_dash_placeholder_names: bool = True
    min_minutes: float = 20.0
    endpoint_minutes: str = ENDPOINT_MINUTES_BOTH
    min_minutes_first: float | None = None
    min_minutes_last: float | None = None
    min_team_season_games: int = 10
    ppm_zero_below_minutes: float | None = None
    winsor_lo: float = 0.01
    winsor_hi: float = 0.99
    no_poolq_winsor: bool = False
    y_draft_mode: str = "ever"
    dft: bool = False
    restrict_teams_by_draftees: bool = False
    require_two_seasons: bool = True
    exclude_transfer_spells: bool = False
    perf_metric: str = "ppm"
    perf_zscore_within_season: bool = True
    congestion_theta: str = "all"
    fit_curves: str = FIT_CURVES_POOLED_QUADRATIC
    out_dir: Path = field(default_factory=lambda: DEFAULT_OUT)


def _survival(step: str, n: int, notes: str = "") -> dict:
    return {"step": step, "n_rows_or_athletes": int(n), "notes": notes}


def _drafted_team_ids(panel: pd.DataFrame) -> set:
    y = pd.to_numeric(panel["Y_draft"], errors="coerce").fillna(0).astype(int)
    return set(panel.loc[y == 1, "team_id"].dropna().unique())


def _apply_dft(panel: pd.DataFrame, drafted_teams: set) -> pd.DataFrame:
    return panel.loc[panel["team_id"].isin(drafted_teams)].copy()


def _endpoint_row(g: pd.DataFrame, which: str) -> pd.Series:
    g = g.sort_values(["season", "team_id"])
    s = int(g["season"].min()) if which == "first" else int(g["season"].max())
    sub = g.loc[g["season"] == s]
    return sub.iloc[0]


def _attach_congestion_columns(panel: pd.DataFrame, thetas: dict[str, float]) -> pd.DataFrame:
    from sports_pipeline.tier1_mechanism_vars import (
        TIER1_CROWDING_COL,
        add_tier1_mechanism_variables,
    )

    out = panel.copy()
    for key, theta in thetas.items():
        col = THETA_SPECS[key]
        tmp = add_tier1_mechanism_variables(
            out,
            viability_theta=float(theta),
            crowding_mode="share",
            compute_weighted_crowding=False,
        )
        out[col] = tmp[TIER1_CROWDING_COL]
    return out


def _normalize_endpoint_minutes(mode: str) -> str:
    m = str(mode).strip().lower().replace("_", "-")
    aliases = {"last": ENDPOINT_MINUTES_LAST_ONLY, "lastonly": ENDPOINT_MINUTES_LAST_ONLY}
    m = aliases.get(m, m)
    if m not in ENDPOINT_MINUTES_MODES:
        raise ValueError(
            f"endpoint_minutes must be one of {sorted(ENDPOINT_MINUTES_MODES)!r}, got {mode!r}"
        )
    return m


def _resolve_endpoint_minute_floors(spec: DeltaDevSpec) -> tuple[float, float]:
    """Minutes floors on chronological first / last PS rows (not the full-panel row drop)."""
    mode = _normalize_endpoint_minutes(spec.endpoint_minutes)
    base = float(spec.min_minutes)
    if spec.min_minutes_last is not None:
        mm_last = float(spec.min_minutes_last)
    else:
        mm_last = base
    if spec.min_minutes_first is not None:
        mm_first = float(spec.min_minutes_first)
    elif mode == ENDPOINT_MINUTES_LAST_ONLY:
        mm_first = 0.0
    else:
        mm_first = base
    return mm_first, mm_last


def _team_tj_map(panel: pd.DataFrame) -> pd.DataFrame:
    return (
        panel.groupby(["team_id", "season"], observed=True)["perf"]
        .mean()
        .reset_index()
        .rename(columns={"perf": "T_j_hat"})
    )


def build_panel(spec: DeltaDevSpec) -> tuple[pd.DataFrame, list[dict], dict]:
    from sports_pipeline import conductor, panel_build
    from sports_pipeline.config import PipelineConfig
    from sports_pipeline.perf_metric import perf_metric_active
    from sports_pipeline.y_draft_mode import (
        apply_y_draft_last_season,
        filter_team_seasons_min_games,
        normalize_y_draft_mode,
    )

    survival: list[dict] = []
    y_mode = normalize_y_draft_mode(spec.y_draft_mode)

    metric_key = str(spec.perf_metric).strip().lower()
    if spec.ppm_zero_below_minutes is not None:
        if metric_key != "ppm":
            raise SystemExit("--ppm-zero-below-minutes only applies when --perf-metric ppm")
        if float(spec.min_minutes) > 0:
            raise SystemExit(
                "Use either --min-minutes (row drop) or --ppm-zero-below-minutes, not both."
            )

    filter_mm = 0.0 if spec.ppm_zero_below_minutes is not None else float(spec.min_minutes)
    winsor = None if spec.no_poolq_winsor else (float(spec.winsor_lo), float(spec.winsor_hi))

    pipe_cfg = PipelineConfig(
        perf_metric=[str(spec.perf_metric).strip().lower()],
        perf_zscore_within_season=False,
        min_minutes=0.0,
        min_team_season_games=0,
        drop_dash_placeholder_names=bool(spec.drop_dash_placeholder_names),
        restrict_teams_by_draftees=bool(spec.restrict_teams_by_draftees),
        use_prebuilt_panel_csv=bool(spec.use_prebuilt_panel_csv),
        panel_season_min=int(spec.season_min),
        panel_season_max=int(spec.season_max),
        analysis_season_min=int(spec.season_min),
        analysis_season_max=int(spec.season_max),
    )

    panel = conductor.prepare_panel(pipe_cfg)
    survival.append(_survival("raw_panel", len(panel)))

    if y_mode == "season":
        panel, _ = apply_y_draft_last_season(panel)
        survival.append(_survival("y_draft_season_label", len(panel)))

    panel = panel.loc[
        (pd.to_numeric(panel["season"], errors="coerce") >= spec.season_min)
        & (pd.to_numeric(panel["season"], errors="coerce") <= spec.season_max)
    ].copy()
    survival.append(_survival("season_window", len(panel)))

    if int(spec.min_team_season_games) > 0:
        panel = filter_team_seasons_min_games(panel, int(spec.min_team_season_games))
        survival.append(_survival("min_team_season_games", len(panel)))

    if spec.ppm_zero_below_minutes is not None:
        thr = float(spec.ppm_zero_below_minutes)
        if "minutes" not in panel.columns or "ppm" not in panel.columns:
            raise KeyError("Panel missing minutes/ppm for ppm-zero-below-minutes mode")
        panel = panel.copy()
        mins = pd.to_numeric(panel["minutes"], errors="coerce")
        low = mins.notna() & (mins < thr)
        panel.loc[low, "ppm"] = 0.0
        survival.append(
            _survival(
                "ppm_zero_below_minutes",
                len(panel),
                f"zeroed_ppm_rows={int(low.sum())} thr={thr}",
            )
        )

    drafted_teams: set | None = None
    if spec.dft:
        drafted_teams = _drafted_team_ids(panel.dropna(subset=["team_id", "season"]))
        panel = _apply_dft(panel, drafted_teams)
        survival.append(_survival("dft_filter", len(panel)))

    panel = panel_build.apply_perf_metric_for_analysis(
        panel,
        perf_metric_active(pipe_cfg),
        poolq_winsor_quantiles=winsor,
        zscore_perf_within_season=bool(spec.perf_zscore_within_season),
    )
    survival.append(_survival("perf_and_loo", len(panel)))

    if filter_mm > 0 and "minutes" in panel.columns:
        panel = panel.loc[pd.to_numeric(panel["minutes"], errors="coerce") >= filter_mm].copy()
        survival.append(_survival("min_minutes_panel", len(panel)))

    panel = panel.dropna(subset=["perf", "team_id", "season", "athlete_id"]).copy()
    survival.append(_survival("valid_perf_rows", len(panel)))

    theta_meta: dict[str, float] = {}
    theta_meta["drafted_median"] = panel_build.viability_theta_drafted_perf(
        panel, stat="median"
    )
    theta_meta["global_median"] = float(
        pd.to_numeric(panel["perf"], errors="coerce").median()
    )
    theta_meta["fixed_zero"] = 0.0

    keys = list(THETA_SPECS.keys())
    if spec.congestion_theta != "all":
        if spec.congestion_theta not in THETA_SPECS:
            raise SystemExit(f"Unknown congestion-theta {spec.congestion_theta!r}")
        keys = [spec.congestion_theta]

    panel = _attach_congestion_columns(panel, {k: theta_meta[k] for k in keys})

    tj = _team_tj_map(panel)
    panel = panel.merge(tj, on=["team_id", "season"], how="left")

    mm_first, mm_last = _resolve_endpoint_minute_floors(spec)
    survival.append(
        _survival(
            "endpoint_minute_floors",
            len(panel),
            f"mode={_normalize_endpoint_minutes(spec.endpoint_minutes)} "
            f"first>={mm_first} last>={mm_last}",
        )
    )

    rows: list[dict] = []
    for aid, g in panel.groupby("athlete_id", observed=True):
        if spec.require_two_seasons and g["season"].nunique() < 2:
            continue
        if spec.exclude_transfer_spells and g["team_id"].nunique() > 1:
            continue
        first = _endpoint_row(g, "first")
        last = _endpoint_row(g, "last")
        if mm_first > 0 and pd.to_numeric(first.get("minutes"), errors="coerce") < mm_first:
            continue
        if mm_last > 0 and pd.to_numeric(last.get("minutes"), errors="coerce") < mm_last:
            continue
        delta_dev = float(last["perf"]) - float(first["perf"])
        rec = {
            "athlete_id": int(aid),
            "season_first": int(first["season"]),
            "season_last": int(last["season"]),
            "team_id_first": first["team_id"],
            "team_id_last": last["team_id"],
            "minutes_first": first.get("minutes"),
            "minutes_last": last.get("minutes"),
            "delta_minutes": pd.to_numeric(last.get("minutes"), errors="coerce")
            - pd.to_numeric(first.get("minutes"), errors="coerce"),
            "perf_first_z": first["perf"],
            "perf_last_z": last["perf"],
            "delta_dev": delta_dev,
            "poolq_loo": last.get("poolq_loo"),
            "T_j_hat": last.get("T_j_hat"),
            "Y_draft": last.get("Y_draft"),
            "n_teams_career": int(g["team_id"].nunique()),
        }
        for key in keys:
            rec[THETA_SPECS[key]] = last.get(THETA_SPECS[key])
        rows.append(rec)

    dev = pd.DataFrame(rows)
    survival.append(_survival("athletes_delta_dev", len(dev)))

    meta = {
        "thetas": {k: theta_meta[k] for k in keys},
        "congestion_theta_mode": spec.congestion_theta,
        "endpoint_minutes_mode": _normalize_endpoint_minutes(spec.endpoint_minutes),
        "endpoint_minute_floors": {"first_ps": mm_first, "last_ps": mm_last},
        "delta_dev_summary": summarize_delta_dev(dev),
    }
    return dev, survival, meta


def _normalize_fit_curves(mode: str) -> str:
    m = str(mode).strip().lower().replace("_", "-")
    aliases = {
        "none": FIT_CURVES_OFF,
        "pooled": FIT_CURVES_POOLED_QUADRATIC,
        "quadratic": FIT_CURVES_POOLED_QUADRATIC,
        "pooled-quadratic": FIT_CURVES_POOLED_QUADRATIC,
        "split": FIT_CURVES_SPLIT_QUADRATIC,
        "split-quadratic": FIT_CURVES_SPLIT_QUADRATIC,
    }
    m = aliases.get(m, m)
    if m not in FIT_CURVES_MODES:
        raise ValueError(f"fit_curves must be one of {sorted(FIT_CURVES_MODES)!r}, got {mode!r}")
    return m


def _plot_quadratic_fit_on_ax(
    ax: plt.Axes,
    x: pd.Series,
    dy: pd.Series,
    *,
    color: str,
    label_prefix: str,
    fit_meta: dict[str, dict[str, float] | None],
    meta_key: str,
    beta_text_xy: tuple[float, float],
    beta_text_ha: str = "left",
) -> None:
    m = x.notna() & dy.notna()
    coef = _fit_quadratic_ols(x[m].to_numpy(), dy[m].to_numpy())
    fit_meta[meta_key] = coef
    if coef is None:
        return
    x_lo = float(np.nanpercentile(x[m], 1))
    x_hi = float(np.nanpercentile(x[m], 99))
    if not np.isfinite(x_lo) or not np.isfinite(x_hi) or x_hi <= x_lo:
        x_lo, x_hi = float(x[m].min()), float(x[m].max())
    x_grid = np.linspace(x_lo, x_hi, 200)
    y_hat = _eval_quadratic(coef, x_grid)
    ax.plot(
        x_grid,
        y_hat,
        color=color,
        lw=2.0,
        ls="-",
        alpha=0.95,
        label=rf"{label_prefix} ($n={coef['n']:,}$)",
        zorder=3,
    )
    ax.text(
        beta_text_xy[0],
        beta_text_xy[1],
        rf"$\beta_2={coef['x_sq']:+.3g}$ ({label_prefix})",
        transform=ax.transAxes,
        fontsize=7,
        va="top",
        ha=beta_text_ha,
        color=color,
    )


def _fit_quadratic_ols(x: np.ndarray, y: np.ndarray) -> dict[str, float] | None:
    mask = np.isfinite(x) & np.isfinite(y)
    if int(mask.sum()) < _QUADRATIC_MIN_N:
        return None
    xv = x[mask].astype(float)
    yv = y[mask].astype(float)
    x_mat = np.column_stack([np.ones(len(xv)), xv, xv**2])
    beta, *_ = np.linalg.lstsq(x_mat, yv, rcond=None)
    return {"const": float(beta[0]), "x": float(beta[1]), "x_sq": float(beta[2]), "n": int(len(xv))}


def _eval_quadratic(coef: dict[str, float], x_grid: np.ndarray) -> np.ndarray:
    return coef["const"] + coef["x"] * x_grid + coef["x_sq"] * (x_grid**2)


def _delta_dev_axis_labels(spec: DeltaDevSpec) -> tuple[str, str]:
    """Return (y-axis label, short token for summary text)."""
    m = str(spec.perf_metric).strip().lower()
    if spec.perf_zscore_within_season:
        return (
            r"$\Delta z$ (last PS $-$ first PS, within-season $z$)",
            r"$\Delta z$",
        )
    if m == "points":
        return r"$\Delta$ points (last PS $-$ first PS)", "Δ points"
    if m == "ppm":
        return r"$\Delta$ PPM (last PS $-$ first PS)", "Δ PPM"
    return rf"$\Delta$ {m} (last PS $-$ first PS)", f"Δ {m}"


def summarize_delta_dev(df: pd.DataFrame) -> dict:
    dy = pd.to_numeric(df["delta_dev"], errors="coerce")
    y = pd.to_numeric(df["Y_draft"], errors="coerce").fillna(0).astype(int)
    valid = dy.notna()
    dy = dy.loc[valid]
    y = y.loc[valid]
    if dy.empty:
        return {"n": 0}
    out: dict = {
        "n": int(len(dy)),
        "mean": float(dy.mean()),
        "median": float(dy.median()),
        "std": float(dy.std()),
        "share_positive": float((dy > 0).mean()),
        "share_negative": float((dy < 0).mean()),
    }
    for label in (0, 1):
        sub = dy[y == label]
        if sub.empty:
            continue
        out[f"Y_draft_{label}"] = {
            "n": int(len(sub)),
            "mean": float(sub.mean()),
            "share_positive": float((sub > 0).mean()),
        }
    return out


def _format_delta_summary_box(summary: dict, short_delta: str) -> str:
    if not summary.get("n"):
        return ""
    sd = short_delta.replace("$", "")
    lines = [
        f"N={summary['n']:,}",
        f"mean {sd}={summary['mean']:+.2f}",
        f"P({sd}>0)={100 * summary['share_positive']:.1f}%",
    ]
    for label in (0, 1):
        key = f"Y_draft_{label}"
        if key not in summary:
            continue
        s = summary[key]
        lines.append(f"Y={label}: P(>0)={100 * s['share_positive']:.1f}% (n={s['n']:,})")
    return "\n".join(lines)


def _plot_delta_dev_marginal_histogram(
    df: pd.DataFrame,
    out_path: Path,
    spec: DeltaDevSpec,
    summary: dict,
) -> None:
    ylab, short_delta = _delta_dev_axis_labels(spec)
    sub = df.dropna(subset=["delta_dev"]).copy()
    if sub.empty:
        return
    y_draft = pd.to_numeric(sub["Y_draft"], errors="coerce").fillna(0).astype(int)
    dy = pd.to_numeric(sub["delta_dev"], errors="coerce")
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    bins = np.linspace(float(dy.quantile(0.01)), float(dy.quantile(0.99)), 45)
    for label, color in [(0, "#4a90d9"), (1, "#c0392b")]:
        vals = dy[y_draft == label].dropna()
        if vals.empty:
            continue
        ax.hist(
            vals,
            bins=bins,
            alpha=0.55,
            color=color,
            label=f"Y_draft={label} (n={len(vals):,})",
            edgecolor="white",
            linewidth=0.3,
        )
    ax.axvline(float(dy.mean()), color="0.2", ls="--", lw=1.2, label=f"mean={dy.mean():+.2f}")
    ax.axvline(0, color="0.5", ls=":", lw=1.0)
    ax.set_xlabel(ylab.split("(")[0].strip())
    ax.set_ylabel("Athletes")
    metric = str(spec.perf_metric).strip().lower()
    ax.set_title(f"Marginal {short_delta} distribution ({metric})")
    box = _format_delta_summary_box(summary, short_delta)
    if box:
        ax.text(
            0.98,
            0.97,
            box,
            transform=ax.transAxes,
            fontsize=8,
            va="top",
            ha="right",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.85, edgecolor="0.8"),
        )
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def _scatter(
    df: pd.DataFrame,
    x_col: str,
    out_path: Path,
    *,
    title: str,
    xlabel: str,
    fit_curves: str = FIT_CURVES_POOLED_QUADRATIC,
    delta_ylabel: str,
    delta_summary: dict,
    delta_short: str,
) -> dict[str, dict[str, float] | None]:
    """Scatter Δ vs x; marginal y-histogram; optional quadratic OLS (pooled or by Y_draft)."""
    sub = df.dropna(subset=[x_col, "delta_dev"]).copy()
    fit_meta: dict[str, dict[str, float] | None] = {}
    if sub.empty:
        return fit_meta
    y_draft = pd.to_numeric(sub["Y_draft"], errors="coerce").fillna(0).astype(int)
    x = pd.to_numeric(sub[x_col], errors="coerce")
    dy = pd.to_numeric(sub["delta_dev"], errors="coerce")
    fig = plt.figure(figsize=(8.5, 5))
    gs = fig.add_gridspec(1, 2, width_ratios=[5.0, 1.15], wspace=0.08)
    ax = fig.add_subplot(gs[0, 0])
    ax_hist = fig.add_subplot(gs[0, 1], sharey=ax)
    strata = [
        (0, y_draft == 0, "#4a90d9"),
        (1, y_draft == 1, "#c0392b"),
    ]
    fit_mode = _normalize_fit_curves(fit_curves)
    do_split = fit_mode == FIT_CURVES_SPLIT_QUADRATIC
    do_pooled = fit_mode == FIT_CURVES_POOLED_QUADRATIC
    hist_bins = np.linspace(
        float(dy.quantile(0.01)),
        float(dy.quantile(0.99)),
        35,
    )
    for label, mask, color in strata:
        m = mask & x.notna() & dy.notna()
        ax.scatter(
            x[m],
            dy[m],
            s=12,
            alpha=0.25,
            c=color,
            label=f"Y_draft={label}",
            edgecolors="none",
            zorder=1,
        )
        vals = dy[m].dropna()
        if not vals.empty:
            ax_hist.hist(
                vals,
                bins=hist_bins,
                orientation="horizontal",
                alpha=0.45,
                color=color,
                edgecolor="none",
            )
        if not do_split:
            continue
        _plot_quadratic_fit_on_ax(
            ax,
            x[m],
            dy[m],
            color=color,
            label_prefix=rf"quad. fit $Y={label}$",
            fit_meta=fit_meta,
            meta_key=f"Y_draft_{label}",
            beta_text_xy=(0.98 if label else 0.02, 0.88 - 0.08 * label),
            beta_text_ha="right" if label else "left",
        )
    if do_pooled:
        _plot_quadratic_fit_on_ax(
            ax,
            x,
            dy,
            color="#1a1a1a",
            label_prefix="quad. fit (all)",
            fit_meta=fit_meta,
            meta_key="all",
            beta_text_xy=(0.5, 0.88),
            beta_text_ha="center",
        )
    ax.axhline(0, color="0.5", lw=0.8, ls="--", zorder=0)
    if delta_summary.get("n"):
        ax.axhline(
            float(delta_summary["mean"]),
            color="0.25",
            lw=1.0,
            ls="-.",
            alpha=0.7,
            zorder=0,
            label=rf"mean {delta_short}={delta_summary['mean']:+.2f}",
        )
    ax.set_xlabel(xlabel)
    ax.set_ylabel(delta_ylabel)
    ax.set_title(title)
    box = _format_delta_summary_box(delta_summary, delta_short)
    if box:
        ax.text(
            0.02,
            0.98,
            box,
            transform=ax.transAxes,
            fontsize=7.5,
            va="top",
            ha="left",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.88, edgecolor="0.75"),
            zorder=5,
        )
    if do_pooled or do_split:
        foot = (
            rf"Quadratic OLS {delta_short} $\sim x + x^2$ (all athletes; associational)"
            if do_pooled
            else rf"Quadratic OLS {delta_short} $\sim x + x^2$ by $Y_{{\mathrm{{draft}}}}$ (associational)"
        )
        fig.text(0.42, 0.01, foot, fontsize=7, ha="center", color="0.4")
    ax_hist.set_xlabel("count")
    plt.setp(ax_hist.get_yticklabels(), visible=False)
    ax.legend(loc="lower right", framealpha=0.9, fontsize=7)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return fit_meta


def run(spec: DeltaDevSpec) -> Path:
    dev, survival, meta = build_panel(spec)
    out_dir = Path(spec.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    tag = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = out_dir / f"run_{tag}"
    run_dir.mkdir(parents=True, exist_ok=True)

    csv_path = run_dir / "delta_dev_panel.csv"
    dev.to_csv(csv_path, index=False)
    pd.DataFrame(survival).to_csv(run_dir / "survival.csv", index=False)

    prov = {
        "spec": {k: str(v) if isinstance(v, Path) else v for k, v in asdict(spec).items()},
        "survival": survival,
        "meta": meta,
        "n_athletes": int(len(dev)),
        "spec_doc": "sports/documents/MBB_DELTA_PPM_DEVELOPMENT_EXPLORATORY_SPEC.md",
    }

    metric = str(spec.perf_metric).strip().lower()
    fit_mode = _normalize_fit_curves(spec.fit_curves)
    delta_ylabel, delta_short = _delta_dev_axis_labels(spec)
    delta_summary = meta.get("delta_dev_summary") or summarize_delta_dev(dev)
    quadratic_fits: dict[str, dict[str, dict[str, float] | None]] = {}

    _plot_delta_dev_marginal_histogram(
        dev,
        run_dir / f"delta_dev_marginal_{metric}.png",
        spec,
        delta_summary,
    )

    def _scatter_and_record(x_col: str, path: Path, *, title: str, xlabel: str) -> None:
        quadratic_fits[x_col] = _scatter(
            dev,
            x_col,
            path,
            title=title,
            xlabel=xlabel,
            fit_curves=fit_mode,
            delta_ylabel=delta_ylabel,
            delta_summary=delta_summary,
            delta_short=delta_short,
        )

    perf_z_note = "within-season z" if spec.perf_zscore_within_season else "levels"
    _scatter_and_record(
        "T_j_hat",
        run_dir / f"delta_dev_vs_Tj_{metric}.png",
        title=f"{delta_short} vs $\\hat{{T}}_j$ ({metric}, {perf_z_note}, exit season)",
        xlabel=r"$\hat{T}_j$ (mean perf on analysis scale, includes self)",
    )
    _scatter_and_record(
        "poolq_loo",
        run_dir / f"delta_dev_vs_poolq_loo_{metric}.png",
        title=f"{delta_short} vs poolq LOO ({metric}, {perf_z_note}, exit season)",
        xlabel="poolq_loo (LOO teammate mean on analysis scale)",
    )
    for key, col in THETA_SPECS.items():
        if col not in dev.columns:
            continue
        th = meta["thetas"].get(key, float("nan"))
        _scatter_and_record(
            col,
            run_dir / f"delta_dev_vs_{col}_{metric}.png",
            title=f"{delta_short} vs viable-peer share (θ={key}, {metric})",
            xlabel=f"LOO share teammates with perf > θ ({key}, θ={th:.4f})",
        )

    prov["meta"]["quadratic_fits_delta_dev"] = quadratic_fits
    prov["meta"]["fit_curves"] = fit_mode
    (run_dir / "provenance.json").write_text(json.dumps(prov, indent=2) + "\n", encoding="utf-8")

    for x_col, slug, xlab in [
        ("T_j_hat", "Tj", r"$\hat{T}_j$"),
        ("poolq_loo", "poolq_loo", "poolq_loo"),
    ]:
        sub = dev.dropna(subset=[x_col, "delta_minutes"]).copy()
        if sub.empty:
            continue
        x = pd.to_numeric(sub[x_col], errors="coerce")
        dm = pd.to_numeric(sub["delta_minutes"], errors="coerce")
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.scatter(x, dm, s=10, alpha=0.2, c="#555", edgecolors="none")
        ax.axhline(0, color="0.5", lw=0.8, ls="--")
        ax.set_xlabel(xlab)
        ax.set_ylabel("Δ minutes (last PS − first PS)")
        ax.set_title(f"Δ minutes vs {slug} (exit season)")
        fig.tight_layout()
        fig.savefig(run_dir / f"delta_minutes_vs_{slug}_{metric}.png", dpi=150)
        plt.close(fig)

    print(f"Wrote {len(dev):,} athletes → {run_dir}")
    return run_dir


def _parse_args(argv: list[str] | None = None) -> DeltaDevSpec:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--preset", choices=("reigning",), default=None)
    p.add_argument("--season-min", type=int, default=2009)
    p.add_argument("--season-max", type=int, default=2021)
    p.add_argument("--use-prebuilt-panel-csv", action="store_true")
    p.add_argument("--no-drop-dash", action="store_true")
    p.add_argument(
        "--min-minutes",
        type=float,
        default=20.0,
        help="Panel row drop before LOO (unless --ppm-zero-below-minutes). Also default "
        "floor for endpoint PS rows per --endpoint-minutes.",
    )
    p.add_argument(
        "--endpoint-minutes",
        choices=sorted(ENDPOINT_MINUTES_MODES),
        default=ENDPOINT_MINUTES_BOTH,
        help="'both': require min minutes on first and last PS; 'last-only': gate last PS "
        "only (first PS may be low minutes). Overrides default for first unless "
        "--min-minutes-first is set.",
    )
    p.add_argument(
        "--min-minutes-first",
        type=float,
        default=None,
        help="Override minutes floor on chronological first PS (default from --endpoint-minutes).",
    )
    p.add_argument(
        "--min-minutes-last",
        type=float,
        default=None,
        help="Override minutes floor on chronological last PS (default: --min-minutes).",
    )
    p.add_argument("--min-team-season-games", type=int, default=10)
    p.add_argument("--ppm-zero-below-minutes", type=float, default=None)
    p.add_argument("--winsor-lo", type=float, default=0.01)
    p.add_argument("--winsor-hi", type=float, default=0.99)
    p.add_argument("--no-poolq-winsor", action="store_true")
    p.add_argument("--y-draft-mode", choices=("ever", "season"), default="ever")
    p.add_argument("--dft", action="store_true")
    p.add_argument("--restrict-teams-by-draftees", action="store_true")
    p.add_argument("--no-require-two-seasons", action="store_true")
    p.add_argument("--exclude-transfer-spells", action="store_true")
    _perf_choices = tuple(
        sorted(
            set(PERF_METRIC_BOX_ONLY)
            | {"bpm", "obpm", "opm", "dbpm", "dpm", "per", "ws40", "ws", "tspct", "ts_pct"}
        )
    )
    p.add_argument(
        "--perf-metric",
        default="ppm",
        choices=_perf_choices,
        help="Outcome for Δ and LOO (ppm, points, minutes, BPM, …).",
    )
    p.add_argument("--no-perf-zscore-within-season", action="store_true")
    p.add_argument(
        "--congestion-theta",
        default="all",
        choices=("all", "drafted_median", "global_median", "fixed_zero"),
    )
    p.add_argument(
        "--fit-curves",
        default=FIT_CURVES_POOLED_QUADRATIC,
        choices=sorted(FIT_CURVES_MODES),
        help="pooled-quadratic (default): one Δ~x+x² curve on all athletes; "
        "split-quadratic: separate curves by Y_draft.",
    )
    p.add_argument(
        "--no-fit-curves",
        action="store_const",
        const=FIT_CURVES_OFF,
        dest="fit_curves",
        help="Scatter only (same as --fit-curves off).",
    )
    p.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = p.parse_args(argv)

    if args.preset == "reigning":
        pass  # defaults already match reigning-style preset

    return DeltaDevSpec(
        season_min=int(args.season_min),
        season_max=int(args.season_max),
        use_prebuilt_panel_csv=bool(args.use_prebuilt_panel_csv),
        drop_dash_placeholder_names=not bool(args.no_drop_dash),
        min_minutes=float(args.min_minutes),
        endpoint_minutes=str(args.endpoint_minutes),
        min_minutes_first=args.min_minutes_first,
        min_minutes_last=args.min_minutes_last,
        min_team_season_games=int(args.min_team_season_games),
        ppm_zero_below_minutes=args.ppm_zero_below_minutes,
        winsor_lo=float(args.winsor_lo),
        winsor_hi=float(args.winsor_hi),
        no_poolq_winsor=bool(args.no_poolq_winsor),
        y_draft_mode=str(args.y_draft_mode),
        dft=bool(args.dft),
        restrict_teams_by_draftees=bool(args.restrict_teams_by_draftees),
        require_two_seasons=not bool(args.no_require_two_seasons),
        exclude_transfer_spells=bool(args.exclude_transfer_spells),
        perf_metric=str(args.perf_metric),
        perf_zscore_within_season=not bool(args.no_perf_zscore_within_season),
        congestion_theta=str(args.congestion_theta),
        fit_curves=str(args.fit_curves),
        out_dir=Path(args.out_dir),
    )


def main(argv: list[str] | None = None) -> None:
    spec = _parse_args(argv)
    run(spec)


if __name__ == "__main__":
    main()
