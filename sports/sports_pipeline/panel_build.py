"""
Stage 4 — panel load, LOO diagnostics, ventile EDA, dirty LPM, export.

**Inputs:** Prefer an in-memory panel from ``panel_rebuild.build_from_box`` (then
``apply_perf_metric_for_analysis``). Alternatively load a pre-exported
``player_season_panel_530.csv`` via ``load_panel`` if it already has draft + SR columns.

**Performance / `perf`:** Ventiles and LPM read `poolq_loo` / `poolq_sq`. To switch
the measure **in this repo** without re-running the full legacy notebook:

1. ``assign_perf_from_metric(df, "bpm")`` (or ``"ppm"``, ``"minutes"``, …) — copies
   the mapped column into ``perf`` (see ``sports_pipeline.perf_metric``).
2. ``recompute_teammate_loo_pool_quality(df, ...)`` — rebuilds ``poolq_loo`` /
   ``poolq_sq`` as leave-one-out mean teammate ``perf`` within ``(team_id, season)``.

Plot titles use ``CFG.perf_measure_label``, derived from the **active** (first) entry in
``CFG.perf_metric`` via ``perf_metric.plot_label_for_metric``. Re-export from ``530_sports_pipeline_bkup.ipynb``
if you need winsorization / filters from the old Cells 5–9 verbatim.

**Outputs:** PNG + CSV under `CFG.exports_dir` (dated filenames).
"""

from __future__ import annotations

import textwrap
import warnings
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from sports_pipeline import paths
from sports_pipeline.perf_metric import export_plot_slug, perf_metric_active, resolve_perf_metric


def load_panel(cfg: Any) -> pd.DataFrame:
    """Read the canonical 530 modeling CSV (`paths.panel_530_csv()`)."""
    p = paths.panel_530_csv()
    if not p.is_file():
        raise FileNotFoundError(f"Missing panel: {p}")
    return pd.read_csv(p, low_memory=False)


def assign_perf_from_metric(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    """
    Copy the column for ``metric`` into ``perf`` (in-place on a **copy** of ``df``).

    ``metric`` is a PERF_METRIC string (``ppm``, ``minutes``, BPM family, ``per``,
    ``ws40``, ``ws``, ``tspct``/``ts_pct``, …) — see ``perf_metric.resolve_perf_metric``.

    Raises ``KeyError`` if the source column is missing (e.g. SR columns before merge).
    """
    _label, col = resolve_perf_metric(metric)
    out = df.copy()
    if col not in out.columns:
        raise KeyError(
            f"Panel has no column {col!r} — cannot set perf from metric {metric!r}. "
            f"For SR metrics, merge `bpm_player_season_matched` first."
        )
    out["perf"] = pd.to_numeric(out[col], errors="coerce")
    return out


def standardize_perf_zscore_by_season(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replace ``perf`` with `(perf - mean_season) / std_season`` per collegiate ``season``.

    Rows in seasons with zero or undefined std become NaN in ``perf``.
    """
    out = df.copy()
    g = out.groupby("season")["perf"]
    mu = g.transform("mean")
    sigma = g.transform("std")
    sigma = sigma.replace(0, np.nan)
    out["perf"] = (out["perf"] - mu) / sigma
    return out


def recompute_teammate_loo_pool_quality(
    df: pd.DataFrame,
    poolq_winsor_quantiles: tuple[float, float] | None = None,
) -> pd.DataFrame:
    """
    Recompute ``poolq_loo`` = mean teammate ``perf`` excluding self, by ``(team_id, season)``.

    Matches the algebra in ``530_sports_pipeline_bkup`` Cell 9:
    ``(sum_perf - own_perf) / (n_teammates - 1)``. Then ``poolq_sq = poolq_loo**2``.

    Optional ``poolq_winsor_quantiles`` e.g. ``(0.01, 0.99)`` clips ``poolq_loo``
    after computation (``None`` = no clip).
    """
    required = {"athlete_id", "team_id", "season", "perf"}
    miss = required - set(df.columns)
    if miss:
        raise KeyError(f"recompute_teammate_loo_pool_quality missing columns: {sorted(miss)}")

    out = df.copy()
    g = out
    sum_perf = g.groupby(["team_id", "season"])["perf"].transform("sum")
    cnt = g.groupby(["team_id", "season"])["athlete_id"].transform("count")
    denom = (cnt - 1).replace(0, np.nan)
    g["poolq_loo"] = (sum_perf - g["perf"]) / denom
    if poolq_winsor_quantiles is not None:
        lo_q, hi_q = poolq_winsor_quantiles
        lo = g["poolq_loo"].quantile(lo_q)
        hi = g["poolq_loo"].quantile(hi_q)
        g["poolq_loo"] = g["poolq_loo"].clip(lower=lo, upper=hi)
    g["poolq_sq"] = g["poolq_loo"] ** 2
    return g


def apply_perf_metric_for_analysis(
    df: pd.DataFrame,
    metric: str,
    poolq_winsor_quantiles: tuple[float, float] | None = None,
    *,
    zscore_perf_within_season: bool = False,
) -> pd.DataFrame:
    """
    ``assign_perf_from_metric`` → optional within-season z-score of ``perf`` →
    ``recompute_teammate_loo_pool_quality``.
    """
    out = assign_perf_from_metric(df, metric)
    if zscore_perf_within_season:
        out = standardize_perf_zscore_by_season(out)
    return recompute_teammate_loo_pool_quality(out, poolq_winsor_quantiles=poolq_winsor_quantiles)


def filter_panel(df: pd.DataFrame, cfg: Any) -> pd.DataFrame:
    """
    Rows for ventile / LPM / integrity: valid ``poolq_loo`` and ``Y_draft``, optional ``min_minutes``,
    and optional restriction to teams with at least one drafted player (see ``cfg``).
    """
    use = df.dropna(subset=["poolq_loo", "Y_draft"]).copy()
    mm = float(getattr(cfg, "min_minutes", 0.0))
    if mm > 0 and "minutes" in use.columns:
        use = use.loc[use["minutes"] >= mm]

    if not bool(getattr(cfg, "restrict_teams_by_draftees", True)):
        return use
    if "team_id" not in use.columns:
        return use

    mode = str(getattr(cfg, "draftee_restriction", "all_time")).strip().lower()
    y = pd.to_numeric(use["Y_draft"], errors="coerce").fillna(0).astype(int)
    tmp = use.assign(_y=y)
    if mode == "season":
        keep = tmp.groupby(["team_id", "season"], observed=True)["_y"].transform("max") == 1
    elif mode == "all_time":
        keep = tmp.groupby("team_id", observed=True)["_y"].transform("max") == 1
    else:
        warnings.warn(
            f"Unknown draftee_restriction {mode!r}; expected 'all_time' or 'season'. Skipping team filter.",
            UserWarning,
            stacklevel=2,
        )
        return use
    return tmp.loc[keep].drop(columns=["_y"])


def assign_poolq_bin_labels(poolq: pd.Series, n_bins: int, mode: str) -> pd.Series:
    """
    Integer bin labels 0.. on ``poolq`` (``poolq_loo``): ``quantile`` → ``pd.qcut``,
    ``equal_width`` → ``pd.cut`` on the observed range.
    """
    m = str(mode).strip().lower()
    s = pd.to_numeric(poolq, errors="coerce")
    if m == "equal_width":
        try:
            return pd.cut(s, bins=int(n_bins), labels=False, include_lowest=True)
        except (ValueError, TypeError) as e:
            warnings.warn(
                f"poolq_binning='equal_width' failed ({e!r}); falling back to quantile bins.",
                UserWarning,
                stacklevel=2,
            )
            return pd.qcut(s, q=int(n_bins), labels=False, duplicates="drop")
    return pd.qcut(s, q=int(n_bins), labels=False, duplicates="drop")


def ventile_table(df: pd.DataFrame, cfg: Any) -> pd.DataFrame:
    """
    Bin ``poolq_loo`` (quantile or equal-width per ``cfg.poolq_binning``); within each bin,
    mean ``Y_draft`` = empirical draft rate. Column ``vent`` is the bin index (0 = lowest poolq).
    """
    q = int(getattr(cfg, "ventiles", 20))
    mode = str(getattr(cfg, "poolq_binning", "quantile")).strip().lower()
    work = df.copy()
    work["vent"] = assign_poolq_bin_labels(work["poolq_loo"], q, mode)
    return (
        work.dropna(subset=["vent"])
        .groupby("vent", observed=True)
        .agg(
            n=("Y_draft", "size"),
            draft_rate=("Y_draft", "mean"),
            poolq_mean=("poolq_loo", "mean"),
            poolq_median=("poolq_loo", "median"),
        )
        .reset_index()
        .sort_values("vent")
    )


def draftee_filter_plot_title_line(cfg: Any) -> str:
    """Short note for the ventile figure title: team draftee filter flags from ``cfg``."""
    if not bool(getattr(cfg, "restrict_teams_by_draftees", True)):
        return "restrict_teams_by_draftees=False"
    dr = str(getattr(cfg, "draftee_restriction", "all_time")).strip().lower()
    return f"restrict_teams_by_draftees=True, draftee_restriction={dr!r}"


def poolq_winsor_short_note(cfg: Any) -> str:
    """One-line tag for figure foot / title when ``poolq_winsor_quantiles`` is set; else empty."""
    wq = getattr(cfg, "poolq_winsor_quantiles", None)
    if wq is None:
        return ""
    lo_q, hi_q = wq
    return f"poolq_winsor_quantiles=({float(lo_q)}, {float(hi_q)})"


def ventile_provenance_lines(
    use: pd.DataFrame,
    cfg: Any,
    bin_tab: pd.DataFrame,
) -> list[str]:
    """
    Human-readable lines: modeling sample scope, BOX/SR/draft year spans, and per-ventile n.

    Used under the ventile figure and in a sidecar ``.txt`` export.
    """
    lines: list[str] = []
    n = int(len(use))
    u_ath = int(use["athlete_id"].nunique())
    s = pd.to_numeric(use["season"], errors="coerce").dropna().astype(int)
    slo, shi = int(s.min()), int(s.max())
    lines.append(
        f"Modeling sample (after dropna poolq_loo, Y_draft; min_minutes; optional team draftee filter): "
        f"n={n:,} player-seasons; {u_ath:,} unique athletes; collegiate seasons {slo}–{shi}."
    )
    bin_mode = str(getattr(cfg, "poolq_binning", "quantile")).strip().lower()
    nv = int(getattr(cfg, "ventiles", 20))
    lines.append(
        f"poolq_loo EDA bins: poolq_binning={bin_mode!r}, ventiles={nv} (number of bins). "
        + (
            "quantile: ~equal counts per bin (pd.qcut); 20 bins = traditional ventiles."
            if bin_mode == "quantile"
            else "equal_width: equal intervals from min to max poolq_loo (pd.cut)."
        )
    )

    wq = getattr(cfg, "poolq_winsor_quantiles", None)
    if wq is not None:
        lo_q, hi_q = wq
        lines.append(
            f"poolq_loo winsorization: poolq_winsor_quantiles=({float(lo_q)}, {float(hi_q)}). "
            "After leave-one-out poolq_loo is computed on the panel, values are clipped to "
            "[q_lo, q_hi] where q_lo and q_hi are the empirical quantiles of poolq_loo on all "
            "rows with defined poolq_loo at that step (before min_minutes and team-draftee filters "
            "on the ventile/LPM subsample); then poolq_sq = poolq_loo²."
        )

    if bool(getattr(cfg, "restrict_teams_by_draftees", True)):
        dr = str(getattr(cfg, "draftee_restriction", "all_time")).strip().lower()
        lines.append(
            f"Team draftee filter: restrict_teams_by_draftees=True, draftee_restriction={dr!r} — "
            + (
                "only (team_id, season) with ≥1 roster member Y_draft=1."
                if dr == "season"
                else "only team_id with ≥1 Y_draft=1 anywhere in this filtered sample."
            )
        )
    else:
        lines.append("Team draftee filter: off (restrict_teams_by_draftees=False).")

    lo = getattr(cfg, "analysis_season_min", None)
    hi = getattr(cfg, "analysis_season_max", None)
    if lo is not None and hi is not None:
        lines.append(
            f"CFG analysis_season_min/max: {int(lo)}–{int(hi)} "
            f"(plot sample uses all seasons with valid rows unless you filter upstream)."
        )

    lines.append(
        f"ESPN box: panel built from game-level box; collegiate season span on sample rows: {slo}–{shi}."
    )

    reg_p = paths.nbaplayersdraft_csv()
    if reg_p.is_file():
        reg = pd.read_csv(reg_p, usecols=["year"], low_memory=False)
        reg = reg.dropna(subset=["year"])
        if len(reg):
            ry = reg["year"].astype(int)
            lines.append(
                f"NBA draft register (nbaplayersdraft.csv): draft `year` in file {int(ry.min())}–{int(ry.max())}."
            )

    lu_path = paths.draft_lookup_csv()
    if lu_path.is_file():
        lu = pd.read_csv(lu_path, usecols=["athlete_id", "draft_year"], low_memory=False)
        lu["athlete_id"] = pd.to_numeric(lu["athlete_id"], errors="coerce")
        lu = lu.dropna(subset=["athlete_id"])
        lu["athlete_id"] = lu["athlete_id"].astype(int)
        ids = set(use["athlete_id"].astype(int))
        hit = lu.loc[lu["athlete_id"].isin(ids)]
        hit = hit.dropna(subset=["draft_year"])
        if len(hit):
            dy = hit["draft_year"].astype(int)
            lines.append(
                f"Draft lookup (athlete_id_draft_lookup): NBA draft years {int(dy.min())}–{int(dy.max())} "
                f"among lookup rows whose athlete_id appears in this sample (n_lookup_rows={len(hit):,})."
            )
        n_d1 = int((use["Y_draft"] == 1).sum())
        lines.append(f"Draft outcome on sample: Y_draft=1 on {n_d1:,} player-seasons (ever-draft flag).")

    metric = perf_metric_active(cfg).strip().lower()
    try:
        _, col = resolve_perf_metric(metric)
    except ValueError:
        col = "minutes"
    if col in ("BPM", "OBPM", "DBPM"):
        if col in use.columns:
            m = use[col].notna()
            if m.any():
                ss = use.loc[m, "season"].astype(int)
                lines.append(
                    f"SR matched advanced (`perf` ← {col}): collegiate seasons with non-null {col} "
                    f"on sample rows {int(ss.min())}–{int(ss.max())} (n={int(m.sum()):,} player-seasons)."
                )
            else:
                lines.append(f"SR matched (`perf` ← {col}): no non-null values on sample rows.")
        else:
            lines.append(f"SR matched: column {col!r} missing on panel — check BPM merge.")
    else:
        lines.append(
            f"SR advanced: not used for `perf` (ESPN box column {col!r}; teammate LOO pool quality from that measure)."
        )

    lines.append("")
    lines.append("Per-bin n (player-seasons; bin index 0 = lowest poolq_loo on the x-axis):")
    bt = bin_tab.sort_values("vent", kind="stable")
    chunks: list[str] = []
    for _, row in bt.iterrows():
        chunks.append(f"v{int(row['vent'])}={int(row['n']):,}")
    per_line = 5
    for i in range(0, len(chunks), per_line):
        lines.append("  " + "  |  ".join(chunks[i : i + per_line]))

    return lines


def draft_poolq_quadratic_coeffs(use: pd.DataFrame) -> pd.Series:
    """numpy OLS: Y_draft ~ 1 + poolq_loo + poolq_sq (same linear spec as LPM cell)."""
    y = use["Y_draft"].astype(float).to_numpy()
    p = use["poolq_loo"].astype(float).to_numpy()
    q = use["poolq_sq"].astype(float).to_numpy()
    mask = np.isfinite(y) & np.isfinite(p) & np.isfinite(q)
    X = np.column_stack([np.ones(mask.sum()), p[mask], q[mask]])
    beta, *_ = np.linalg.lstsq(X, y[mask], rcond=None)
    return pd.Series(beta, index=["const", "poolq_loo", "poolq_sq"])


def _add_lpm_curve_poolq_space(
    ax: Any,
    bin_tab: pd.DataFrame,
    use: pd.DataFrame,
    cfg: Any,
    poolq_col: str,
) -> bool:
    """Draw quadratic LPM in ``poolq_loo`` space on ``ax``; x-range from bin column ``poolq_col``."""
    if not bool(getattr(cfg, "show_quadratic_lpm_on_eda_plot", True)):
        return False
    if len(use) <= 50:
        return False
    b = draft_poolq_quadratic_coeffs(use)
    if b is None or len(b) != 3:
        return False
    pq_m = bin_tab[poolq_col].astype(float)
    lo = float(pq_m.min())
    hi = float(pq_m.max())
    span = hi - lo if hi > lo else 1.0
    pad = max(span * 0.04, 0.05)
    xs = np.linspace(lo - pad, hi + pad, 200)
    yhat = (
        float(b["const"])
        + float(b["poolq_loo"]) * xs
        + float(b["poolq_sq"]) * (xs**2)
    )
    ax.plot(
        xs,
        np.clip(yhat, 0.0, 1.0),
        color="C1",
        linestyle="--",
        linewidth=2,
        alpha=0.9,
        label="LPM (OLS) — E[draft|poolq] ≈ β₀+β₁·poolq+β₂·poolq²",
    )
    ax.set_xlim(lo - pad, hi + pad)
    return True


def ventile_plot(
    bin_tab: pd.DataFrame,
    cfg: Any,
    n_rows: int,
    use: pd.DataFrame | None = None,
    *,
    provenance_lines: list[str] | None = None,
    show: bool = True,
) -> Path:
    """
    Ventile draft-rate figure controlled by ``cfg.ventile_eda_plot_style``:

    - ``poolq_line`` (default): one axes, draft rate vs mean ``poolq_loo`` per bin + optional LPM.
    - ``bins_bars_520``: **bar chart only** vs bin index (1 = lowest poolq), ``steelblue`` / white edges
      (legacy Cell 11 left panel); no second scatter panel. Y-axis pinned at 0.

    Pass ``provenance_lines`` (from ``ventile_provenance_lines``) to add a caption panel;
    if omitted and ``use`` is set, provenance is computed once here (unless
    ``cfg.ventile_plot_show_metadata`` is False — chart only, tighter PNG).
    """
    import matplotlib.pyplot as plt

    out_dir = Path(getattr(cfg, "exports_dir", paths.mbb_dir() / "exports_inverted_u_v0"))
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = date.today().isoformat()
    perf_lbl = getattr(cfg, "perf_measure_label", "perf")
    v = int(getattr(cfg, "ventiles", 20))
    bin_mode = str(getattr(cfg, "poolq_binning", "quantile")).strip().lower()
    if bin_mode == "equal_width":
        bin_title = f"{v} equal-width bins on poolq_loo"
    elif v == 20:
        bin_title = "20 ventiles (quantile bins, ~equal n per bin)"
    else:
        bin_title = f"{v} quantile bins (~equal n per bin)"
    show_meta = bool(getattr(cfg, "ventile_plot_show_metadata", True))
    plot_style = str(getattr(cfg, "ventile_eda_plot_style", "poolq_line")).strip().lower()
    z_sc = bool(getattr(cfg, "perf_zscore_within_season", False))
    draftee_line = draftee_filter_plot_title_line(cfg)

    provenance: list[str] = []
    if show_meta:
        provenance = list(provenance_lines) if provenance_lines is not None else []
        if not provenance and use is not None and len(use):
            provenance = ventile_provenance_lines(use, cfg, bin_tab)

    cap = ""
    if provenance:
        wrapped_blocks: list[str] = []
        for ln in provenance:
            if ln.strip() == "":
                wrapped_blocks.append("")
            elif ln.startswith("  "):
                wrapped_blocks.append(ln)
            else:
                wrapped_blocks.append(
                    textwrap.fill(ln, width=104, break_long_words=False, break_on_hyphens=False)
                )
        cap = "\n".join(wrapped_blocks)

    if plot_style == "bins_bars_520":
        bin_1 = bin_tab["vent"].astype(int) + 1

        if provenance:
            fig = plt.figure(figsize=(8.2, 6.0), constrained_layout=True)
            gs = fig.add_gridspec(2, 1, height_ratios=[3.15, 1.0])
            ax0 = fig.add_subplot(gs[0, 0])
            ax_cap = fig.add_subplot(gs[1, 0])
            ax_cap.axis("off")
            ax_cap.text(
                0.0,
                1.0,
                cap,
                transform=ax_cap.transAxes,
                va="top",
                ha="left",
                fontsize=6.65,
                linespacing=1.12,
                family="sans-serif",
            )
        else:
            fig, ax0 = plt.subplots(figsize=(8.2, 5.5))

        ax0.bar(
            bin_1,
            bin_tab["draft_rate"],
            color="steelblue",
            edgecolor="white",
            linewidth=0.4,
        )
        ax0.set_xlabel("Ventile bin (1 = lowest poolq_loo)")
        ax0.set_ylabel("Mean Y_draft")
        ax0.set_title("Mean draft rate by ventile of poolq_loo (LOO teammate perf)")
        ax0.set_xticks(bin_1)
        ax0.set_ylim(bottom=0)
        ax0.grid(True, axis="y", alpha=0.3)

        if not provenance:
            wn = poolq_winsor_short_note(cfg)
            foot = (
                f"Performance measure: {perf_lbl}"
                + (" · perf z-scored within season before LOO" if z_sc else "")
                + f" · {draftee_line} · {bin_title} · n={n_rows:,} player-seasons"
                + (f" · {wn}" if wn else "")
            )
            fig.text(0.5, 0.02, foot, ha="center", fontsize=8.5, color="0.35")
            fig.tight_layout(rect=[0, 0.10, 1, 1])

    else:
        if provenance:
            fig = plt.figure(figsize=(8.2, 6.0), constrained_layout=True)
            gs = fig.add_gridspec(2, 1, height_ratios=[3.15, 1.0])
            ax = fig.add_subplot(gs[0, 0])
            ax_cap = fig.add_subplot(gs[1, 0])
            ax_cap.axis("off")
            ax_cap.text(
                0.0,
                1.0,
                cap,
                transform=ax_cap.transAxes,
                va="top",
                ha="left",
                fontsize=6.65,
                linespacing=1.12,
                family="sans-serif",
            )
        else:
            fig, ax = plt.subplots(figsize=(8.2, 5.5))

        ax.plot(
            bin_tab["poolq_mean"],
            bin_tab["draft_rate"],
            marker="o",
            ms=4,
            label="Ventile means",
        )
        poolq_x = (
            "Mean teammate pool quality within ventile (poolq_loo, leave-one-out on perf)"
            + (" — SD units within season" if z_sc else "")
        )
        ax.set_xlabel(poolq_x)
        ax.set_ylabel("Draft rate (mean Y_draft)")
        z_line = "\nperf z-scored within collegiate season before LOO" if z_sc else ""
        wn = poolq_winsor_short_note(cfg)
        winsor_line = (
            f"\n{wn} (clip poolq_loo after LOO)" if wn and not provenance else ""
        )
        ax.set_title(
            f"Draft rate vs pool quality — {bin_title} (n={n_rows:,} player-seasons)\n"
            f"Performance measure: {perf_lbl}{z_line}\n"
            f"{draftee_line}{winsor_line}",
            fontsize=11,
        )
        if use is not None and len(use) > 50:
            _add_lpm_curve_poolq_space(ax, bin_tab, use, cfg, "poolq_mean")
        ax.legend(loc="best", fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(bottom=0)

        if not provenance:
            fig.tight_layout()

    plot_slug = export_plot_slug(cfg)
    png = out_dir / f"inverted_u_ventiles_{plot_slug}_{stamp}.png"
    fig.savefig(png, dpi=150, bbox_inches="tight", pad_inches=0.14)
    if show:
        plt.show()
    plt.close(fig)
    return png


def run_ventile_eda(df: pd.DataFrame, cfg: Any) -> tuple[pd.DataFrame, Path]:
    """Filter → binned table CSV → ventile PNG (with optional quadratic overlay)."""
    use = filter_panel(df, cfg)
    bin_tab = ventile_table(use, cfg)
    out_dir = Path(getattr(cfg, "exports_dir", paths.mbb_dir() / "exports_inverted_u_v0"))
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = date.today().isoformat()
    plot_slug = export_plot_slug(cfg)
    csv_path = out_dir / f"binned_draft_rate_ventiles_{plot_slug}_{stamp}.csv"
    bin_tab.to_csv(csv_path, index=False)

    prov_lines = ventile_provenance_lines(use, cfg, bin_tab) if len(use) else []
    prov_path = out_dir / f"ventile_eda_provenance_{plot_slug}_{stamp}.txt"
    prov_path.write_text("\n".join(prov_lines) + "\n", encoding="utf-8")
    print("--- Ventile EDA — sample / datasets / per-ventile n ---")
    print("\n".join(prov_lines))
    print(f"(Also wrote {prov_path.name})")
    print()

    png_path = ventile_plot(
        bin_tab, cfg, len(use), use=use, provenance_lines=prov_lines if prov_lines else None
    )
    return bin_tab, png_path


def run_dirty_lpm(df: pd.DataFrame, cfg: Any) -> Any | pd.Series:
    """statsmodels summary if installed; otherwise return coefficient Series (numpy OLS)."""
    use = filter_panel(df, cfg)
    try:
        import statsmodels.api as sm
    except ImportError:
        return draft_poolq_quadratic_coeffs(use)
    y = use["Y_draft"].astype(float)
    X = use[["poolq_loo", "poolq_sq"]].astype(float)
    X = sm.add_constant(X)
    return sm.OLS(y, X, missing="drop").fit()


def export_panel(df: pd.DataFrame, cfg: Any, dest: Path | None = None) -> Path:
    """Write panel CSV (default: overwrite canonical path)."""
    target = dest or paths.panel_530_csv()
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(target, index=False)
    return target
