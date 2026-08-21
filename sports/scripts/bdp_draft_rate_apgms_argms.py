#!/usr/bin/env python3
"""BDP — draft rate vs APGMS / ARGMS (player + team-mean ventiles, side-by-side).

Left: mean Y_draft by ventile of player **APGMS_i** / **ARGMS_i**.
Right: mean Y_draft by ventile of team-mean **APGMS_j** / **ARGMS_j** (attached to each player-row).

Default: **+DFT** panel (draftee-team ecosystems), green player / blue team bars.

Run (repo root):
  python sports/scripts/bdp_draft_rate_apgms_argms.py
  python sports/scripts/bdp_draft_rate_apgms_argms.py --spec "mg10 min1 11_21"
  python sports/scripts/bdp_draft_rate_apgms_argms.py --all-teams  # full panel, no DFT filter

  python sports/scripts/bdp_draft_rate_apgms_argms.py --binning equal_width  # parallel ew16 files

Outputs (quantile, default):
  ``basic_data_plots/BDP_draft_rate_APGMS_mg10_min1_11_21.png`` (+ JSON + bin CSVs)

Outputs (equal width):
  ``basic_data_plots/BDP_draft_rate_APGMS_mg10_min1_11_21_ew16.png`` (+ JSON + bin CSVs)

Bin intervals: see JSON / ``*_bins.csv`` (`x_min`/`x_max`; equal-width also has `edge_lo`/`edge_hi`).
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SPORTS))

from bdp_ai_tj_distributions import parse_bdp_spec, subtitle_lines
from bdp_apgms_argms_distributions import (
    DEFAULT_SPEC,
    _attach_team_means,
    _prepare_panel,
)
from gallery_knobs import HERO_BINS
from gallery_mathtext import configure_matplotlib_mathtext
from hero_gallery_paths import BASIC_DATA_PLOTS, ensure_hero_dirs

N_BINS = HERO_BINS
FIGSIZE = (12.0, 6.8)
PLAYER_COLOR = "seagreen"
TEAM_COLOR = "steelblue"

METRICS = {
    "apgms": {
        "player_col": "apgms",
        "team_col": "T_apgms",
        "title_short": "APGMS",
        "player_xlabel": r"APGMS$_i$ ventile ($1$ = lowest avg min / played game)",
        "team_xlabel": r"APGMS$_j$ ventile ($1$ = lowest mean team APGMS)",
        "player_panel": r"Draft rate vs APGMS$_i$ ($n={n:,}$ PS)",
        "team_panel": r"Draft rate vs binned APGMS$_j$ ($n={n:,}$ PS)",
    },
    "argms": {
        "player_col": "argms",
        "team_col": "T_argms",
        "title_short": "ARGMS",
        "player_xlabel": r"ARGMS$_i$ ventile ($1$ = lowest avg min / rostered game)",
        "team_xlabel": r"ARGMS$_j$ ventile ($1$ = lowest mean team ARGMS)",
        "player_panel": r"Draft rate vs ARGMS$_i$ ($n={n:,}$ PS)",
        "team_panel": r"Draft rate vs binned ARGMS$_j$ ($n={n:,}$ PS)",
    },
}


BINNING_CHOICES = ("quantile", "equal_width")


def _binning_slug(binning: str) -> str:
    mode = str(binning).strip().lower()
    if mode == "equal_width":
        return f"ew{int(N_BINS)}"
    return ""


def _binning_label(binning: str) -> str:
    mode = str(binning).strip().lower()
    if mode == "equal_width":
        return f"{N_BINS} equal-width bins"
    return f"{N_BINS} quantile ventiles"


def _xlabels(metric_key: str, binning: str) -> tuple[str, str]:
    meta = METRICS[metric_key]
    unit = "bin" if str(binning).strip().lower() == "equal_width" else "ventile"
    player = meta["player_xlabel"].replace("ventile", unit)
    team = meta["team_xlabel"].replace("ventile", unit)
    return player, team


def _assign_ventiles(
    df: pd.DataFrame,
    value_col: str,
    n_bins: int,
    binning: str,
) -> pd.Series:
    from sports_pipeline.panel_build import assign_poolq_bin_labels

    return assign_poolq_bin_labels(df[value_col], n_bins, binning)


def _equal_width_edges(values: pd.Series, n_bins: int) -> np.ndarray:
    s = pd.to_numeric(values, errors="coerce").dropna()
    if s.empty:
        return np.linspace(0.0, 1.0, int(n_bins) + 1)
    lo = float(s.min())
    hi = float(s.max())
    if hi <= lo:
        hi = lo + 1.0
    return np.linspace(lo, hi, int(n_bins) + 1)


def _ventile_draft_table(
    df: pd.DataFrame,
    value_col: str,
    n_bins: int,
    binning: str,
) -> pd.DataFrame:
    work = df.dropna(subset=[value_col, "Y_draft"]).copy()
    work["vent"] = _assign_ventiles(work, value_col, n_bins, binning)
    tbl = (
        work.dropna(subset=["vent"])
        .groupby("vent", observed=True)
        .agg(
            n=("Y_draft", "size"),
            drafts=("Y_draft", "sum"),
            draft_rate=("Y_draft", "mean"),
            x_min=(value_col, "min"),
            x_max=(value_col, "max"),
            x_mean=(value_col, "mean"),
            x_median=(value_col, "median"),
        )
        .reset_index()
        .sort_values("vent")
    )
    if str(binning).strip().lower() == "equal_width":
        edges = _equal_width_edges(work[value_col], n_bins)
        tbl["edge_lo"] = tbl["vent"].astype(int).map(lambda v: float(edges[int(v)]))
        tbl["edge_hi"] = tbl["vent"].astype(int).map(lambda v: float(edges[int(v) + 1]))
    return tbl


def _table_to_records(tbl: pd.DataFrame, *, binning: str) -> list[dict]:
    rows = []
    use_edges = (
        str(binning).strip().lower() == "equal_width"
        and "edge_lo" in tbl.columns
        and "edge_hi" in tbl.columns
    )
    for _, r in tbl.iterrows():
        x_lo = float(r["x_min"])
        x_hi = float(r["x_max"])
        rec = {
            "vent": int(r["vent"]),
            "bin_display": int(r["vent"]) + 1,
            "n": int(r["n"]),
            "drafts": int(r["drafts"]),
            "draft_rate": float(r["draft_rate"]),
            "x_min": x_lo,
            "x_max": x_hi,
            "x_interval": f"[{x_lo:.4g}, {x_hi:.4g}]",
            "x_mean": float(r["x_mean"]),
            "x_median": float(r["x_median"]),
        }
        if use_edges:
            elo = float(r["edge_lo"])
            ehi = float(r["edge_hi"])
            rec["edge_lo"] = elo
            rec["edge_hi"] = ehi
            rec["edge_interval"] = f"[{elo:.4g}, {ehi:.4g})"
        rows.append(rec)
    return rows


def _write_bin_csv(tbl: pd.DataFrame, path: Path, *, value_label: str, binning: str) -> None:
    out = tbl.copy()
    out["bin_display"] = out["vent"].astype(int) + 1
    out["x_interval"] = out.apply(
        lambda r: f"[{float(r['x_min']):.4g}, {float(r['x_max']):.4g}]",
        axis=1,
    )
    cols = [
        "vent",
        "bin_display",
        "n",
        "drafts",
        "draft_rate",
        "x_min",
        "x_max",
        "x_interval",
        "x_median",
        "x_mean",
    ]
    if str(binning).strip().lower() == "equal_width" and "edge_lo" in out.columns:
        out["edge_interval"] = out.apply(
            lambda r: f"[{float(r['edge_lo']):.4g}, {float(r['edge_hi']):.4g})",
            axis=1,
        )
        cols.extend(["edge_lo", "edge_hi", "edge_interval"])
    out = out[cols].rename(columns={"x_min": f"{value_label}_min", "x_max": f"{value_label}_max"})
    out.to_csv(path, index=False, float_format="%.6g")
    print(f"Wrote {path.relative_to(REPO)}")


def _count_weighted_bar_colors(counts: np.ndarray, *, cmap_name: str) -> list:
    """Map bin row counts to bar face colors (light = sparse, dark = dense)."""
    n = np.asarray(counts, dtype=float)
    if n.size == 0:
        return []
    lo, hi = float(n.min()), float(n.max())
    cmap = plt.get_cmap(cmap_name)
    if hi <= lo:
        return [cmap(0.65) for _ in n]
    norm = plt.Normalize(vmin=lo, vmax=hi)
    # Keep pale bins visible; reserve top of colormap for largest n.
    levels = 0.28 + 0.67 * norm(n)
    return [cmap(float(v)) for v in levels]


def _label_color_for_bar(facecolor) -> str:
    rgba = facecolor if len(facecolor) >= 3 else (0.5, 0.5, 0.5, 1.0)
    r, g, b = float(rgba[0]), float(rgba[1]), float(rgba[2])
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    return "0.15" if lum > 0.62 else "white"


def _annotate_bin_n(
    ax,
    x: np.ndarray,
    y: np.ndarray,
    counts: np.ndarray,
    bar_colors: list | None = None,
    *,
    rotation: float = 90.0,
    y_frac: float = 0.10,
) -> None:
    """Label each bar with bin population on the bar face (lower third)."""
    for i, (xi, yi, n) in enumerate(zip(x, y, counts, strict=True)):
        ni = int(n)
        if ni <= 0 or float(yi) <= 0:
            continue
        y_pos = max(float(yi) * y_frac, 0.0015)
        txt_color = "white"
        if bar_colors is not None and i < len(bar_colors):
            txt_color = _label_color_for_bar(bar_colors[i])
        ax.text(
            xi,
            y_pos,
            f"{ni:,}",
            ha="center",
            va="bottom",
            fontsize=7,
            rotation=rotation,
            color=txt_color,
            fontweight="bold",
            clip_on=True,
        )


def build_figure(
    spec,
    metric_key: str,
    player_tbl: pd.DataFrame,
    team_tbl: pd.DataFrame,
    panel_n: int,
    total_drafts: int,
    png: Path,
    *,
    binning: str = "quantile",
    figsize: tuple[float, float] = FIGSIZE,
) -> None:
    meta = METRICS[metric_key]
    player_xlabel, team_xlabel = _xlabels(metric_key, binning)
    configure_matplotlib_mathtext()
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    equal_width = str(binning).strip().lower() == "equal_width"

    for ax, tbl, color, xlabel, title_tmpl, cmap_name in (
        (
            axes[0],
            player_tbl,
            PLAYER_COLOR,
            player_xlabel,
            meta["player_panel"],
            "Greens",
        ),
        (
            axes[1],
            team_tbl,
            TEAM_COLOR,
            team_xlabel,
            meta["team_panel"],
            "Blues",
        ),
    ):
        x = tbl["vent"].to_numpy(dtype=float) + 1
        y = tbl["draft_rate"].to_numpy(dtype=float)
        counts = tbl["n"].to_numpy(dtype=int)
        if equal_width:
            bar_colors = _count_weighted_bar_colors(counts, cmap_name=cmap_name)
            ax.bar(x, y, color=bar_colors, edgecolor="white", linewidth=0.6, alpha=0.95)
        else:
            bar_colors = None
            ax.bar(x, y, color=color, edgecolor="white", linewidth=0.6, alpha=0.9)
        ax.set_xlabel(xlabel, fontsize=10)
        ax.set_ylabel(r"Mean $Y_{\mathrm{draft}}$", fontsize=10)
        ax.set_title(title_tmpl.format(n=panel_n), fontsize=11, pad=6)
        ax.set_xticks(x)
        ax.grid(axis="y", alpha=0.25, linewidth=0.5)
        ymax = float(y.max()) if len(y) else 0.05
        ax.set_ylim(0, max(0.05, ymax * 1.15))
        if equal_width:
            _annotate_bin_n(ax, x, y, counts, bar_colors, rotation=90)

    fig.suptitle(
        rf"BDP — draft rate vs {meta['title_short']} (player + team mean bins)",
        fontsize=12,
        y=1.02,
    )
    sub1, sub2 = subtitle_lines(spec, has_overlay=False)
    sub2 = (
        f"{sub2} · {_binning_label(binning)} · n={panel_n:,} PS · drafts={total_drafts:,}"
    )
    if equal_width:
        sub2 += " · bar shade ∝ bin n (dark = more PS) · n on bar face"
    fig.text(0.5, 0.98, sub1, ha="center", va="top", fontsize=9, color="0.25")
    fig.text(0.5, 0.955, sub2, ha="center", va="top", fontsize=9, color="0.25")
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {png.relative_to(REPO)}")


def run_metric(
    spec_text: str,
    metric_key: str,
    *,
    dft_only: bool = True,
    binning: str = "quantile",
) -> Path:
    ensure_hero_dirs()
    spec = parse_bdp_spec(spec_text)
    build_spec = replace(spec, dft=True) if dft_only and not spec.dft else spec
    meta = METRICS[metric_key]
    mode = str(binning).strip().lower()
    if mode not in BINNING_CHOICES:
        raise ValueError(f"binning must be one of {BINNING_CHOICES}, got {binning!r}")

    panel = _attach_team_means(
        _prepare_panel(build_spec, need_cols=("minutes", "apgms", "argms"))
    )
    panel = panel.dropna(subset=["Y_draft"]).copy()
    panel_n = int(len(panel))
    total_drafts = int(pd.to_numeric(panel["Y_draft"], errors="coerce").fillna(0).sum())

    player_tbl = _ventile_draft_table(panel, meta["player_col"], N_BINS, mode)
    team_tbl = _ventile_draft_table(panel, meta["team_col"], N_BINS, mode)

    ew = _binning_slug(mode)
    stem = f"BDP_draft_rate_{meta['title_short']}_{spec.slug}" + (f"_{ew}" if ew else "")
    out_png = BASIC_DATA_PLOTS / f"{stem}.png"
    out_json = BASIC_DATA_PLOTS / f"{stem}.json"
    out_csv_player = BASIC_DATA_PLOTS / f"{stem}_{meta['player_col']}_bins.csv"
    out_csv_team = BASIC_DATA_PLOTS / f"{stem}_{meta['team_col']}_bins.csv"

    build_figure(
        build_spec,
        metric_key,
        player_tbl,
        team_tbl,
        panel_n,
        total_drafts,
        out_png,
        binning=mode,
    )

    _write_bin_csv(player_tbl, out_csv_player, value_label=meta["player_col"], binning=mode)
    _write_bin_csv(team_tbl, out_csv_team, value_label=meta["team_col"], binning=mode)

    if mode == "equal_width":
        interval_def = (
            "Equal-width bins on observed min–max (assign_poolq_bin_labels, mode=equal_width): "
            "edge_lo/edge_hi are fixed cutpoints; x_min/x_max are observed values within each bin."
        )
    else:
        interval_def = (
            "Rank-based quantile ventiles (assign_poolq_bin_labels, mode=quantile): "
            "each bin has ~equal row count; x_min/x_max are the observed range of the "
            "metric within assigned rows. Intervals can overlap at boundaries when values tie."
        )

    payload = {
        "diagnostic": "bdp_draft_rate_minutes_metric",
        "date": date.today().isoformat(),
        "metric": metric_key,
        "bdp_spec": build_spec.label,
        "seasons": f"{build_spec.season_min}-{build_spec.season_max}",
        "dft": bool(build_spec.dft),
        "n_bins": N_BINS,
        "binning": mode,
        "bin_interval_definition": interval_def,
        "panel_n": panel_n,
        "total_drafts": total_drafts,
        "player_col": meta["player_col"],
        "team_col": meta["team_col"],
        "player_ventiles": _table_to_records(player_tbl, binning=mode),
        "team_ventiles": _table_to_records(team_tbl, binning=mode),
        "bin_csv": {
            "player": out_csv_player.name,
            "team": out_csv_team.name,
        },
        "png": out_png.name,
    }
    out_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_json.relative_to(REPO)}")
    return out_png


def main() -> None:
    parser = argparse.ArgumentParser(description="Draft rate vs APGMS/ARGMS ventiles.")
    parser.add_argument("--spec", default=DEFAULT_SPEC)
    parser.add_argument(
        "--metric",
        choices=["apgms", "argms", "both"],
        default="both",
    )
    parser.add_argument(
        "--all-teams",
        action="store_true",
        help="Full panel (no DFT filter). Default is +DFT only.",
    )
    parser.add_argument(
        "--binning",
        choices=BINNING_CHOICES,
        default="quantile",
        help="quantile (equal n per bin) or equal_width (fixed minute ranges).",
    )
    args = parser.parse_args()
    keys = ["apgms", "argms"] if args.metric == "both" else [args.metric]
    for key in keys:
        print(f"\n=== draft rate · {key.upper()} · {args.spec} · {args.binning} ===")
        run_metric(
            args.spec,
            key,
            dft_only=not args.all_teams,
            binning=args.binning,
        )
    print("\nDone.")


if __name__ == "__main__":
    main()
