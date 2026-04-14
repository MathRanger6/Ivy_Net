"""
Yearly coverage counts across BOX, NBA draft register, and SR BPM match files.

Used to choose collegiate / draft analysis windows: grouped bars per year, one color
per dataset. BOX and SR use collegiate ``season``; DRAFT uses NBA draft ``year`` from
``nbaplayersdraft.csv`` (same integer x-axis; interpret overlap when picking windows).

Also builds a **detail table** and **dashboard** plots: ESPN box vs positive-minutes
player-seasons (PPM/minutes ``perf`` base) vs SR advanced (BPM/OBPM/DBPM share one
matched row), plus BOX∩SR overlap and match rates.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from sports_pipeline import paths
from sports_pipeline.perf_metric import export_plot_slug


def _box_unique_athletes_by_season() -> pd.Series:
    p = paths.player_box_csv()
    if not p.is_file():
        return pd.Series(dtype=int)
    df = pd.read_csv(p, usecols=["athlete_id", "season"], low_memory=False)
    df = df.dropna(subset=["athlete_id", "season"])
    df["season"] = df["season"].astype(int)
    return df.groupby("season")["athlete_id"].nunique()


def _sr_unique_athletes_by_season() -> pd.Series:
    p = paths.bpm_matched_csv()
    if not p.is_file():
        return pd.Series(dtype=int)
    cols = pd.read_csv(p, nrows=0).columns.tolist()
    use = [c for c in ("athlete_id", "season", "has_bpm") if c in cols]
    df = pd.read_csv(p, usecols=use, low_memory=False)
    if "has_bpm" in df.columns:
        df = df.loc[df["has_bpm"].fillna(0).astype(int) == 1]
    df = df.dropna(subset=["athlete_id", "season"])
    df["season"] = df["season"].astype(int)
    return df.groupby("season")["athlete_id"].nunique()


def _draft_register_rows_by_year() -> pd.Series:
    p = paths.nbaplayersdraft_csv()
    if not p.is_file():
        return pd.Series(dtype=int)
    df = pd.read_csv(p, low_memory=False)
    if "year" not in df.columns:
        return pd.Series(dtype=int)
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)
    return df.groupby("year").size()


def _box_minutes_positive_by_season() -> pd.Series:
    """Unique ``athlete_id`` per collegiate ``season`` with total game minutes ``> 0`` (PPM/minutes base)."""
    p = paths.player_box_csv()
    if not p.is_file():
        return pd.Series(dtype=int)
    df = pd.read_csv(p, usecols=["athlete_id", "season", "minutes"], low_memory=False)
    df = df.dropna(subset=["athlete_id", "season"])
    df["season"] = df["season"].astype(int)
    df["athlete_id"] = pd.to_numeric(df["athlete_id"], errors="coerce")
    df = df.dropna(subset=["athlete_id"])
    df["athlete_id"] = df["athlete_id"].astype(int)
    df["minutes"] = pd.to_numeric(df["minutes"], errors="coerce").fillna(0.0)
    ag = df.groupby(["athlete_id", "season"], as_index=False)["minutes"].sum()
    ag = ag.loc[ag["minutes"] > 0]
    return ag.groupby("season")["athlete_id"].nunique()


def _sr_metric_counts_by_season() -> tuple[pd.Series, pd.Series, pd.Series]:
    """
    Unique athletes per season with non-null BPM / OBPM / DBPM in the matched file.

    Typically identical counts (same SR table row); still reported separately for QA.
    """
    p = paths.bpm_matched_csv()
    if not p.is_file():
        z = pd.Series(dtype=int)
        return z, z, z
    cols = pd.read_csv(p, nrows=0).columns.tolist()
    use = ["athlete_id", "season", "has_bpm"]
    for c in ("BPM", "OBPM", "DBPM"):
        if c in cols:
            use.append(c)
    df = pd.read_csv(p, usecols=[c for c in use if c in cols], low_memory=False)
    if "has_bpm" in df.columns:
        df = df.loc[df["has_bpm"].fillna(0).astype(int) == 1]
    df = df.dropna(subset=["athlete_id", "season"])
    df["season"] = df["season"].astype(int)
    df["athlete_id"] = pd.to_numeric(df["athlete_id"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["athlete_id"])
    df["athlete_id"] = df["athlete_id"].astype(int)

    def _uniq_by_season(col: str | None) -> pd.Series:
        if col is None or col not in df.columns:
            return df.groupby("season")["athlete_id"].nunique()
        return df.loc[df[col].notna()].groupby("season")["athlete_id"].nunique()

    bpm_s = _uniq_by_season("BPM")
    obpm_s = _uniq_by_season("OBPM") if "OBPM" in df.columns else bpm_s
    dbpm_s = _uniq_by_season("DBPM") if "DBPM" in df.columns else bpm_s
    return bpm_s, obpm_s, dbpm_s


def _box_sr_intersection_by_season() -> pd.Series:
    """Unique ``(athlete_id, season)`` in box with minutes ``> 0`` that also appear in SR matched (has_bpm)."""
    p_box = paths.player_box_csv()
    p_sr = paths.bpm_matched_csv()
    if not p_box.is_file() or not p_sr.is_file():
        return pd.Series(dtype=int)
    df = pd.read_csv(p_box, usecols=["athlete_id", "season", "minutes"], low_memory=False)
    df = df.dropna(subset=["athlete_id", "season"])
    df["season"] = df["season"].astype(int)
    df["athlete_id"] = pd.to_numeric(df["athlete_id"], errors="coerce")
    df = df.dropna(subset=["athlete_id"])
    df["athlete_id"] = df["athlete_id"].astype(int)
    df["minutes"] = pd.to_numeric(df["minutes"], errors="coerce").fillna(0.0)
    ag = df.groupby(["athlete_id", "season"], as_index=False)["minutes"].sum()
    ag = ag.loc[ag["minutes"] > 0, ["athlete_id", "season"]]

    cols = pd.read_csv(p_sr, nrows=0).columns.tolist()
    use = ["athlete_id", "season", "has_bpm"]
    sr = pd.read_csv(p_sr, usecols=[c for c in use if c in cols], low_memory=False)
    if "has_bpm" in sr.columns:
        sr = sr.loc[sr["has_bpm"].fillna(0).astype(int) == 1]
    sr = sr.dropna(subset=["athlete_id", "season"])
    sr["season"] = sr["season"].astype(int)
    sr["athlete_id"] = pd.to_numeric(sr["athlete_id"], errors="coerce")
    sr = sr.dropna(subset=["athlete_id"])
    sr["athlete_id"] = sr["athlete_id"].astype(int)
    sr = sr[["athlete_id", "season"]].drop_duplicates()

    merged = ag.merge(sr, on=["athlete_id", "season"], how="inner")
    return merged.groupby("season")["athlete_id"].nunique()


def yearly_coverage_detail_table() -> pd.DataFrame:
    """
    Per calendar year on the x-axis: BOX presence, minute-positive player-seasons, SR splits,
    BOX∩SR overlap, draft register size, and match rates.

    **Note:** ``year`` matches ``yearly_coverage_table``: collegiate season for BOX/SR columns;
    ``draft_picks`` is still **NBA draft** ``year`` (June), not collegiate season.
    """
    box_any = _box_unique_athletes_by_season()
    box_minpos = _box_minutes_positive_by_season()
    sr_bpm, sr_obpm, sr_dbpm = _sr_metric_counts_by_season()
    inter = _box_sr_intersection_by_season()
    dr = _draft_register_rows_by_year()

    all_years = sorted(
        set(box_any.index.astype(int))
        | set(box_minpos.index.astype(int))
        | set(sr_bpm.index.astype(int))
        | set(inter.index.astype(int))
        | set(dr.index.astype(int))
    )
    out = pd.DataFrame({"year": all_years})
    y = out["year"]

    out["box_any_game_athletes"] = y.map(box_any).fillna(0).astype(int)
    out["box_minutes_gt0_athletes"] = y.map(box_minpos).fillna(0).astype(int)
    out["sr_bpm_athletes"] = y.map(sr_bpm).fillna(0).astype(int)
    out["sr_obpm_athletes"] = y.map(sr_obpm).fillna(0).astype(int)
    out["sr_dbpm_athletes"] = y.map(sr_dbpm).fillna(0).astype(int)
    out["box_sr_overlap_athletes"] = y.map(inter).fillna(0).astype(int)
    out["draft_picks"] = y.map(dr).fillna(0).astype(int)

    bx = out["box_any_game_athletes"].replace(0, np.nan)
    bm = out["box_minutes_gt0_athletes"].replace(0, np.nan)
    out["pct_sr_bpm_of_box_any"] = (100.0 * out["sr_bpm_athletes"] / bx).fillna(0.0)
    out["pct_sr_bpm_of_box_minpos"] = (100.0 * out["sr_bpm_athletes"] / bm).fillna(0.0)
    out["pct_overlap_of_box_any"] = (100.0 * out["box_sr_overlap_athletes"] / bx).fillna(0.0)
    out["pct_overlap_of_box_minpos"] = (100.0 * out["box_sr_overlap_athletes"] / bm).fillna(0.0)

    return out


def yearly_coverage_table() -> pd.DataFrame:
    """
    One row per year in the union of BOX seasons, SR seasons, and draft years.

    Columns: ``year``, ``box_players``, ``draft_picks``, ``sr_players`` (zeros if no data).
    """
    box = _box_unique_athletes_by_season()
    sr = _sr_unique_athletes_by_season()
    dr = _draft_register_rows_by_year()
    all_years = sorted(set(box.index.astype(int)) | set(sr.index.astype(int)) | set(dr.index.astype(int)))
    out = pd.DataFrame({"year": all_years})
    out["box_players"] = out["year"].map(box).fillna(0).astype(int)
    out["draft_picks"] = out["year"].map(dr).fillna(0).astype(int)
    out["sr_players"] = out["year"].map(sr).fillna(0).astype(int)
    return out


def plot_yearly_coverage_grouped(
    tab: pd.DataFrame,
    cfg: Any,
    *,
    show: bool = True,
    stamp: str | None = None,
    plot_slug: str | None = None,
) -> Path:
    """
    Grouped bar chart: three bars per year (BOX, DRAFT, SR). Saves PNG under ``cfg.exports_dir``.

    If ``cfg.analysis_season_min`` and ``cfg.analysis_season_max`` are both set, shades
    that year band (by **season** index on the x-axis).
    """
    import matplotlib.pyplot as plt

    years = tab["year"].to_numpy()
    x = np.arange(len(years), dtype=float)
    w = 0.25
    out_dir = Path(getattr(cfg, "exports_dir", paths.mbb_dir() / "exports_inverted_u_v0"))
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = stamp or date.today().isoformat()
    slug = plot_slug if plot_slug is not None else export_plot_slug(cfg)
    png = out_dir / f"dataset_coverage_by_year_{slug}_{stamp}.png"

    fig, ax = plt.subplots(figsize=(max(11.0, len(years) * 0.22), 5.8))
    ax.bar(
        x - w,
        tab["box_players"],
        width=w,
        label="BOX — unique athletes per collegiate season",
        color="#2980b9",
        edgecolor="white",
        linewidth=0.4,
    )
    ax.bar(
        x,
        tab["draft_picks"],
        width=w,
        label="DRAFT — register rows per NBA draft year",
        color="#c0392b",
        edgecolor="white",
        linewidth=0.4,
    )
    ax.bar(
        x + w,
        tab["sr_players"],
        width=w,
        label="SR — unique athletes per season (BPM matched)",
        color="#16a085",
        edgecolor="white",
        linewidth=0.4,
    )

    lo = getattr(cfg, "analysis_season_min", None)
    hi = getattr(cfg, "analysis_season_max", None)
    if lo is not None and hi is not None:
        in_win = (years >= int(lo)) & (years <= int(hi))
        idx = np.flatnonzero(in_win)
        if len(idx):
            ax.axvspan(
                float(idx[0]) - 0.5,
                float(idx[-1]) + 0.5,
                facecolor="#9b59b6",
                alpha=0.12,
                zorder=0,
                label=f"Highlighted window (seasons {int(lo)}–{int(hi)})",
            )

    step = 1 if len(years) <= 28 else max(1, len(years) // 20)
    tick_idx = np.arange(0, len(years), step, dtype=int)
    ax.set_xticks(x[tick_idx])
    ax.set_xticklabels([str(int(y)) for y in years[tick_idx]], rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Count")
    ax.set_xlabel("Year (see subtitle — BOX/SR = season, DRAFT = draft year)")
    ax.set_title(
        "Player / pick coverage by year — BOX vs DRAFT vs SR",
        fontsize=12,
    )
    fig.text(
        0.5,
        0.02,
        "BOX & SR: ESPN/SR collegiate season. DRAFT: nbaplayersdraft `year` (June draft). "
        "Use relative heights to choose overlapping analysis windows.",
        ha="center",
        fontsize=8,
        style="italic",
    )
    ax.legend(loc="upper left", fontsize=8, framealpha=0.92)
    ax.grid(True, axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    fig.subplots_adjust(bottom=0.18, top=0.92)
    fig.savefig(png, dpi=150)
    if show:
        plt.show()
    plt.close(fig)
    return png


def _apply_analysis_window_shade(ax: Any, years: np.ndarray, x: np.ndarray, cfg: Any) -> None:
    lo = getattr(cfg, "analysis_season_min", None)
    hi = getattr(cfg, "analysis_season_max", None)
    if lo is None or hi is None:
        return
    in_win = (years >= int(lo)) & (years <= int(hi))
    idx = np.flatnonzero(in_win)
    if len(idx):
        ax.axvspan(
            float(idx[0]) - 0.5,
            float(idx[-1]) + 0.5,
            facecolor="#9b59b6",
            alpha=0.08,
            zorder=0,
        )


def plot_metric_coverage_dashboard(
    detail: pd.DataFrame,
    cfg: Any,
    *,
    show: bool = True,
    stamp: str | None = None,
    plot_slug: str | None = None,
) -> Path:
    """
    Two-panel figure: (1) counts — BOX vs minute-positive base vs SR advanced vs overlap, plus
    draft register on a secondary axis; (2) SR/BPM as a share of the BOX minute-positive base.
    """
    import matplotlib.pyplot as plt

    years = detail["year"].to_numpy(dtype=int)
    x = np.arange(len(years), dtype=float)
    out_dir = Path(getattr(cfg, "exports_dir", paths.mbb_dir() / "exports_inverted_u_v0"))
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = stamp or date.today().isoformat()
    slug = plot_slug if plot_slug is not None else export_plot_slug(cfg)
    png = out_dir / f"dataset_coverage_dashboard_{slug}_{stamp}.png"

    fig, (ax0, ax1) = plt.subplots(
        2,
        1,
        figsize=(max(11.5, len(years) * 0.22), 8.4),
        gridspec_kw={"height_ratios": [2.15, 1.05], "hspace": 0.28},
    )

    _apply_analysis_window_shade(ax0, years, x, cfg)
    ax0.plot(
        x,
        detail["box_any_game_athletes"],
        label="BOX — unique athletes (any game row)",
        color="#2980b9",
        lw=2.2,
    )
    ax0.plot(
        x,
        detail["box_minutes_gt0_athletes"],
        label="BOX — unique athletes, Σminutes>0 (PPM / `minutes` perf)",
        color="#1abc9c",
        lw=2.0,
        ls="--",
    )
    ax0.plot(
        x,
        detail["sr_bpm_athletes"],
        label="SR matched — BPM (OBPM/DBPM use same rows)",
        color="#16a085",
        lw=2.2,
    )
    ax0.plot(
        x,
        detail["box_sr_overlap_athletes"],
        label="BOX∩SR — minute-positive & in matched file",
        color="#8e44ad",
        lw=1.9,
        ls=":",
    )

    ax0b = ax0.twinx()
    ax0b.bar(
        x,
        detail["draft_picks"],
        width=0.55,
        alpha=0.38,
        color="#c0392b",
        label="DRAFT — register rows (June `year`; not season)",
    )
    ax0b.set_ylabel("Draft register rows", color="#a93226", fontsize=9)
    ax0b.tick_params(axis="y", labelcolor="#a93226", labelsize=8)

    ax0.set_ylabel("Unique athletes (collegiate season)", fontsize=10)
    ax0.set_title(
        "Coverage by year — ESPN box vs SR match vs overlap; draft on right axis",
        fontsize=12,
    )
    ax0.grid(True, axis="y", alpha=0.25)
    ax0.set_axisbelow(True)

    h0, l0 = ax0.get_legend_handles_labels()
    h1, l1 = ax0b.get_legend_handles_labels()
    ax0.legend(h0 + h1, l0 + l1, loc="upper left", fontsize=7.5, framealpha=0.94, ncol=1)

    _apply_analysis_window_shade(ax1, years, x, cfg)
    ax1.fill_between(
        x,
        detail["pct_overlap_of_box_minpos"],
        alpha=0.25,
        color="#16a085",
        step="mid",
    )
    ax1.plot(
        x,
        detail["pct_overlap_of_box_minpos"],
        label="SR match rate: BOX∩SR / BOX (min>0)  [%]",
        color="#0d6e5c",
        lw=2.0,
    )
    ax1.plot(
        x,
        detail["pct_sr_bpm_of_box_any"],
        label="SR athletes / BOX any game  [%]",
        color="#2980b9",
        lw=1.3,
        ls="--",
        alpha=0.85,
    )
    ax1.set_ylabel("Percent")
    _mx = float(np.nanmax(detail["pct_overlap_of_box_minpos"].to_numpy(dtype=float)))
    if not np.isfinite(_mx):
        _mx = 0.0
    ax1.set_ylim(0, min(100.0, max(15.0, _mx * 1.15)))
    ax1.grid(True, axis="y", alpha=0.25)
    ax1.set_axisbelow(True)
    ax1.legend(loc="upper left", fontsize=8, framealpha=0.92)

    step = 1 if len(years) <= 28 else max(1, len(years) // 20)
    tick_idx = np.arange(0, len(years), step, dtype=int)
    for ax in (ax0, ax1):
        ax.set_xticks(x[tick_idx])
        ax.set_xticklabels([str(int(y)) for y in years[tick_idx]], rotation=45, ha="right", fontsize=8)
    ax1.set_xlabel("Year — BOX & SR = collegiate season; draft axis = June draft year")

    fig.text(
        0.5,
        0.01,
        "Lower panel — solid: share of minute-positive BOX athletes (Σminutes>0) who also appear in SR matched; "
        "dashed: SR matched athlete count as % of unique BOX athletes with any game row (denominator is larger after "
        "~2014, so dashed can sit below solid). OBPM/DBPM use the same SR rows as BPM.",
        ha="center",
        fontsize=7.5,
        style="italic",
    )
    fig.subplots_adjust(bottom=0.14, top=0.94)
    fig.savefig(png, dpi=150)
    if show:
        plt.show()
    plt.close(fig)
    return png


def plot_coverage_metric_heatmap(
    detail: pd.DataFrame,
    cfg: Any,
    *,
    show: bool = False,
    stamp: str | None = None,
    plot_slug: str | None = None,
) -> Path:
    """Rows = datasets/metrics, columns = year; color = row-normalized intensity (shape comparison)."""
    import matplotlib.pyplot as plt

    years = detail["year"].to_numpy(dtype=int)
    row_labels = [
        "BOX any game",
        "BOX min>0\n(PPM/min perf)",
        "SR BPM\n(OBPM/DBPM)",
        "BOX∩SR",
        "Draft register",
    ]
    mat = np.vstack(
        [
            detail["box_any_game_athletes"].to_numpy(dtype=float),
            detail["box_minutes_gt0_athletes"].to_numpy(dtype=float),
            detail["sr_bpm_athletes"].to_numpy(dtype=float),
            detail["box_sr_overlap_athletes"].to_numpy(dtype=float),
            detail["draft_picks"].to_numpy(dtype=float),
        ]
    )
    row_max = mat.max(axis=1, keepdims=True)
    row_max = np.where(row_max <= 0, 1.0, row_max)
    norm = mat / row_max

    out_dir = Path(getattr(cfg, "exports_dir", paths.mbb_dir() / "exports_inverted_u_v0"))
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = stamp or date.today().isoformat()
    slug = plot_slug if plot_slug is not None else export_plot_slug(cfg)
    png = out_dir / f"dataset_coverage_heatmap_{slug}_{stamp}.png"

    fig_w = max(12.0, len(years) * 0.18)
    fig, ax = plt.subplots(figsize=(fig_w, 4.2))
    im = ax.imshow(norm, aspect="auto", cmap="YlGnBu", vmin=0, vmax=1, interpolation="nearest")
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_yticklabels(row_labels, fontsize=9)
    step = 1 if len(years) <= 30 else max(1, len(years) // 24)
    xt = np.arange(0, len(years), step)
    ax.set_xticks(xt)
    ax.set_xticklabels([str(int(years[i])) for i in xt], rotation=45, ha="right", fontsize=7)
    ax.set_xlabel("Year (BOX/SR = season; bottom row = June draft year)")
    ax.set_title("Relative coverage shape by year (each row scaled to its own max = 1)")
    plt.colorbar(im, ax=ax, fraction=0.02, pad=0.02, label="Row-normalized")
    fig.tight_layout()
    fig.savefig(png, dpi=150)
    if show:
        plt.show()
    plt.close(fig)
    return png


def export_yearly_coverage_chart(cfg: Any, *, show: bool = True) -> tuple[pd.DataFrame, Path]:
    """
    Write legacy summary CSV, **detail** CSV (metrics + overlap rates), dashboard PNG, heatmap PNG,
    and the original three-bar chart (saved only, not shown, to avoid extra figure windows).

    The underlying counts come from on-disk BOX / SR matched / draft files only — not from the
    in-memory panel's ``perf`` column. ``export_plot_slug(cfg)`` affects filenames only; when
    sweeping ``perf_metric``, calling this once is enough.

    Returns ``(yearly_coverage_table(), path_to_dashboard_png)`` for backward compatibility.
    """
    out_dir = Path(getattr(cfg, "exports_dir", paths.mbb_dir() / "exports_inverted_u_v0"))
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = date.today().isoformat()
    plot_slug = export_plot_slug(cfg)

    tab = yearly_coverage_table()
    tab.to_csv(out_dir / f"dataset_coverage_by_year_{plot_slug}_{stamp}.csv", index=False)

    detail = yearly_coverage_detail_table()
    detail.to_csv(out_dir / f"dataset_coverage_detail_{plot_slug}_{stamp}.csv", index=False)

    plot_yearly_coverage_grouped(tab, cfg, show=False, stamp=stamp, plot_slug=plot_slug)
    heatmap_path = plot_coverage_metric_heatmap(
        detail, cfg, show=False, stamp=stamp, plot_slug=plot_slug
    )
    dashboard_png = plot_metric_coverage_dashboard(
        detail, cfg, show=show, stamp=stamp, plot_slug=plot_slug
    )
    legacy_name = f"dataset_coverage_by_year_{plot_slug}_{stamp}.png"
    print("--- Yearly coverage exports ---")
    print(f"  shown in notebook: {dashboard_png.name} (line chart + match-rate panel)")
    print(f"  detail metrics CSV: dataset_coverage_detail_{plot_slug}_{stamp}.csv")
    print(f"  heatmap (saved): {heatmap_path.name}")
    print(f"  legacy 3-bar chart (saved only): {legacy_name}")
    return tab, dashboard_png
