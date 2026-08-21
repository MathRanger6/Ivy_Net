#!/usr/bin/env python3
"""BDP — Empirical $\\hat{A}_i$ / $\\hat{T}_j$ side-by-side (PD17 slide 3 layout).

Basic Data Plots: configurable BDP filter chains (QC baseline + optional mg / min).

QC baseline (always): drop ESPN dash placeholder names (`drop_dash_placeholder_names=True`).
Does **not** imply mg10 unless the spec includes it.

Run (repo root):
  python sports/scripts/bdp_ai_tj_distributions.py
  python sports/scripts/bdp_ai_tj_distributions.py --perf-metric bpm
  python sports/scripts/bdp_ai_tj_distributions.py --spec "mg10 min20 11_21"

Outputs: ``HEROs_and_PASSes/basic_data_plots/BDP_Ai_Tj_<spec>.png`` (+ meta JSON).
With ``--perf-metric bpm`` / ``obpm``: ``BDP_Ai_Tj_<spec>_bpm.png`` / ``_obpm.png``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import BASIC_DATA_PLOTS, ensure_hero_dirs

DEFAULT_SPECS = [
    "FP 11_21",
    "mg10 min0 11_21",
    "mg10 min10 11_21",
    "mg10 min20 11_21",
]

N_BINS = 48
BAR_COLORS: dict[str, str] = {
    "ppm": "steelblue",
    "bpm": "#B39DDB",
    "obpm": "#E8B923",
    "dbpm": "#7E57C2",
}
BAR_ALPHA = 0.85
DFT_OVERLAY_COLOR = "darkorange"
Y_HEADROOM = 1.12  # modest y-axis pad above tallest bar for stats box
STATS_LABEL_W = 13


def format_stats_box(
    stats: dict,
    stats_dft: dict | None = None,
    *,
    decimals: int = 3,
    include_max: bool = False,
) -> str:
    """Monospace stats block; right edge of numeric columns aligns across rows."""

    def metrics(s: dict) -> str:
        if include_max:
            return (
                f"mean={s['mean']:5.{decimals}f}  "
                f"sd={s['std']:4.{decimals}f}  "
                f"max={int(s['max']):2d}"
            )
        return f"mean={s['mean']:7.{decimals}f}  sd={s['std']:6.{decimals}f}"

    lines = [f"{'without DFT:':<{STATS_LABEL_W}}{metrics(stats)}"]
    if stats_dft is not None:
        lines.append(f"{'+ DFT:':<{STATS_LABEL_W}}{metrics(stats_dft)}")
    return "\n".join(lines)


def draw_stats_box(
    ax,
    stats: dict,
    stats_dft: dict | None = None,
    *,
    decimals: int = 3,
    include_max: bool = False,
) -> None:
    ax.text(
        0.97,
        0.98,
        format_stats_box(stats, stats_dft, decimals=decimals, include_max=include_max),
        transform=ax.transAxes,
        va="top",
        ha="right",
        fontsize=7.5,
        linespacing=1.2,
        family="monospace",
        bbox=dict(
            boxstyle="round,pad=0.35",
            facecolor="white",
            alpha=0.92,
            edgecolor="0.8",
        ),
    )


def subtitle_lines(spec: BdpSpec, *, has_overlay: bool, perf_metric: str = "") -> tuple[str, str]:
    """Two-line figure subtitle — width stays near the plot panel."""
    prefix = f"{perf_metric.upper()} z · " if perf_metric else ""
    line1 = f"{prefix}MBB {spec.season_min}–{spec.season_max} · QC (dash names removed)"
    if spec.is_fp:
        line1 += " · FP (no mg filter)"
    else:
        line1 += f" · mg{spec.min_team_season_games}"
    if spec.min_minutes > 0:
        line2 = f"min {spec.min_minutes:g} min"
    else:
        line2 = "min 0 (no playing-time floor)"
    if spec.dft:
        line2 += " · DFT (draft-only teams)"
    if has_overlay:
        line2 += " · orange line = +DFT"
    return line1, line2


def _bar_color(perf_metric: str) -> str:
    return BAR_COLORS.get(perf_metric.strip().lower(), "steelblue")

MG_RE = re.compile(r"^mg(\d+)$", re.I)
MIN_RE = re.compile(r"^min(\d+)$", re.I)
YEAR_RE = re.compile(r"^(\d{2})_(\d{2})$")


@dataclass(frozen=True)
class BdpSpec:
    label: str
    season_min: int
    season_max: int
    min_team_season_games: int
    min_minutes: float
    is_fp: bool
    dft: bool = False

    @property
    def slug(self) -> str:
        return self.label.replace(" ", "_")

    @property
    def subtitle(self) -> str:
        parts = [
            f"MBB {self.season_min}–{self.season_max}",
            "QC (dash names removed)",
        ]
        if self.is_fp:
            parts.append("FP (no mg filter)")
        else:
            parts.append(f"mg{self.min_team_season_games}")
        if self.min_minutes > 0:
            parts.append(f"min {self.min_minutes:g} min")
        else:
            parts.append("min 0 (no playing-time floor)")
        if self.dft:
            parts.append("DFT (draft-only teams)")
        return " · ".join(parts)


def parse_bdp_spec(text: str) -> BdpSpec:
    tokens = text.strip().split()
    if not tokens:
        raise ValueError("empty spec")

    season_min: int | None = None
    season_max: int | None = None
    min_team_season_games = 0
    min_minutes = 0.0
    is_fp = False
    dft = False
    filters: list[str] = []

    for tok in tokens:
        low = tok.lower()
        if low == "fp":
            is_fp = True
            filters.append("FP")
            continue
        if low == "dft":
            dft = True
            filters.append("DFT")
            continue
        ym = YEAR_RE.match(tok)
        if ym:
            season_min = 2000 + int(ym.group(1))
            season_max = 2000 + int(ym.group(2))
            filters.append(tok)
            continue
        mg = MG_RE.match(low)
        if mg:
            min_team_season_games = int(mg.group(1))
            filters.append(f"mg{min_team_season_games}")
            continue
        mn = MIN_RE.match(low)
        if mn:
            min_minutes = float(mn.group(1))
            filters.append(f"min{int(min_minutes)}")
            continue
        raise ValueError(f"unknown token {tok!r} in spec {text!r}")

    if season_min is None or season_max is None:
        raise ValueError(f"spec must include YY_YY year range: {text!r}")
    if is_fp and min_team_season_games > 0:
        raise ValueError(f"FP cannot combine with mg filter: {text!r}")

    label = " ".join(filters)
    return BdpSpec(
        label=label,
        season_min=season_min,
        season_max=season_max,
        min_team_season_games=0 if is_fp else min_team_season_games,
        min_minutes=min_minutes,
        is_fp=is_fp,
        dft=dft,
    )


def _drafted_team_ids(panel: pd.DataFrame) -> set:
    y = pd.to_numeric(panel["Y_draft"], errors="coerce").fillna(0).astype(int)
    return set(panel.loc[y == 1, "team_id"].dropna().unique())


def _apply_dft(panel: pd.DataFrame, drafted_teams: set) -> pd.DataFrame:
    """DFT — keep rows only for teams with ≥1 draftee in the panel window."""
    return panel.loc[panel["team_id"].isin(drafted_teams)].copy()


def _pipeline_config(spec: BdpSpec, perf_metric: str, *, min_minutes: float | None = None):
    sys.path.insert(0, str(SPORTS))
    from sports_pipeline.config import PipelineConfig

    mm = spec.min_minutes if min_minutes is None else min_minutes
    return PipelineConfig(
        perf_metric=[perf_metric],
        perf_zscore_within_season=True,
        min_minutes=mm,
        drop_dash_placeholder_names=True,
        min_team_season_games=spec.min_team_season_games,
        panel_season_min=spec.season_min,
        panel_season_max=spec.season_max,
        analysis_season_min=spec.season_min,
        analysis_season_max=spec.season_max,
        poolq_winsor_quantiles=None,
        restrict_teams_by_draftees=spec.dft,
        draftee_restriction="all_time",
        use_prebuilt_panel_csv=False,
    )


def _prepare(spec: BdpSpec, perf_metric: str) -> pd.DataFrame:
    sys.path.insert(0, str(SPORTS))
    from sports_pipeline import conductor, panel_build
    from sports_pipeline.perf_metric import perf_metric_active

    drafted_teams: set | None = None
    if spec.dft:
        cfg0 = _pipeline_config(spec, perf_metric, min_minutes=0.0)
        raw = conductor.prepare_panel(cfg0)
        drafted_teams = _drafted_team_ids(raw.dropna(subset=["team_id", "season"]))

    build_min = 0.0 if spec.dft else None
    cfg = _pipeline_config(spec, perf_metric, min_minutes=build_min)
    panel = conductor.prepare_panel(cfg)
    if spec.dft and drafted_teams is not None:
        panel = _apply_dft(panel, drafted_teams)
    panel = panel_build.apply_perf_metric_for_analysis(
        panel,
        perf_metric_active(cfg),
        poolq_winsor_quantiles=None,
        zscore_perf_within_season=True,
    )
    use = panel.dropna(subset=["perf", "team_id", "season"]).copy()
    mm = float(spec.min_minutes)
    if mm > 0 and "minutes" in use.columns:
        use = use.loc[pd.to_numeric(use["minutes"], errors="coerce") >= mm]
    return use


def _summary(values: np.ndarray) -> dict:
    v = np.asarray(values, dtype=float)
    v = v[np.isfinite(v)]
    return {
        "n": int(v.size),
        "mean": float(v.mean()),
        "std": float(v.std()),
        "min": float(v.min()),
        "max": float(v.max()),
    }


def _histogram_edges(*arrays: np.ndarray, n_bins: int = N_BINS) -> np.ndarray:
    pooled = np.concatenate([np.asarray(a, dtype=float) for a in arrays])
    pooled = pooled[np.isfinite(pooled)]
    lo = float(np.quantile(pooled, 0.005))
    hi = float(np.quantile(pooled, 0.995))
    if hi <= lo:
        lo, hi = float(pooled.min()), float(pooled.max())
    pad = 0.05 * (hi - lo) if hi > lo else 0.5
    return np.linspace(lo - pad, hi + pad, n_bins + 1)


def _team_talent(use: pd.DataFrame) -> np.ndarray:
    team_df = (
        use.groupby(["team_id", "season"], observed=True)
        .agg(T_j_hat=("perf", "mean"))
        .reset_index()
    )
    return team_df["T_j_hat"].to_numpy(dtype=float)


def build_figure(
    spec: BdpSpec,
    ability: np.ndarray,
    team_talent: np.ndarray,
    png: Path,
    perf_metric: str,
    perf_axis_label: str,
    *,
    ability_dft: np.ndarray | None = None,
    team_talent_dft: np.ndarray | None = None,
    figsize: tuple[float, float] = (10.5, 4.2),
) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    bar_color = _bar_color(perf_metric)
    pool = [ability, team_talent]
    if ability_dft is not None and team_talent_dft is not None:
        pool.extend([ability_dft, team_talent_dft])
    edges = _histogram_edges(*pool)
    centers = 0.5 * (edges[:-1] + edges[1:])
    bin_width = edges[1] - edges[0]

    fig, axes = plt.subplots(1, 2, figsize=figsize, sharex=True)
    panels: list[tuple] = [
        (
            axes[0],
            ability,
            ability_dft,
            rf"$\hat{{A}}_i$ — player ability ($n={ability.size:,}$)",
        ),
        (
            axes[1],
            team_talent,
            team_talent_dft,
            rf"$\hat{{T}}_j$ — realized team talent ($n={team_talent.size:,}$ team-seasons)",
        ),
    ]

    legend_handles: list | None = None
    legend_labels: list | None = None

    for ax, values, values_dft, title in panels:
        counts, _ = np.histogram(values, bins=edges)
        ax.bar(
            centers,
            counts,
            width=bin_width * 0.98,
            align="center",
            color=bar_color,
            alpha=BAR_ALPHA,
            edgecolor=bar_color,
            linewidth=0.3,
            label="without DFT",
        )
        if values_dft is not None:
            counts_dft, _ = np.histogram(values_dft, bins=edges)
            ax.plot(
                centers,
                counts_dft,
                color=DFT_OVERLAY_COLOR,
                linewidth=2.0,
                marker="o",
                markersize=3,
                label=rf"+ DFT ($n={values_dft.size:,}$)",
            )
        else:
            counts_dft = None

        peak = int(counts.max())
        if counts_dft is not None:
            peak = max(peak, int(counts_dft.max()))
        ax.set_ylim(0, peak * Y_HEADROOM)

        ax.set_xlabel(perf_axis_label, fontsize=10)
        ax.set_ylabel("Count", fontsize=10)
        ax.set_title(title, fontsize=11, pad=6)
        ax.grid(axis="y", alpha=0.25, linewidth=0.5)
        if legend_handles is None:
            legend_handles, legend_labels = ax.get_legend_handles_labels()
        stats = _summary(values)
        sd = _summary(values_dft) if values_dft is not None else None
        draw_stats_box(ax, stats, sd, decimals=3)

    has_overlay = ability_dft is not None
    if legend_handles and has_overlay:
        fig.legend(
            legend_handles,
            legend_labels,
            loc="lower center",
            bbox_to_anchor=(0.5, 0.02),
            ncol=2,
            fontsize=8,
            framealpha=0.95,
        )
        bottom = 0.10
    else:
        axes[0].legend(loc="lower right", fontsize=8, framealpha=0.92)
        bottom = 0.06

    fig.suptitle(
        rf"BDP — Empirical $\hat{{A}}_i$ and $\hat{{T}}_j$",
        fontsize=12,
        y=0.995,
    )
    sub1, sub2 = subtitle_lines(spec, has_overlay=has_overlay, perf_metric=perf_metric)
    fig.text(0.5, 0.962, sub1, ha="center", va="top", fontsize=9, color="0.25")
    fig.text(0.5, 0.947, sub2, ha="center", va="top", fontsize=9, color="0.25")

    fig.tight_layout(rect=(0, bottom, 1, 0.925))
    fig.savefig(png, dpi=150)
    plt.close(fig)
    print(f"Wrote {png.relative_to(REPO)}")


def _output_stem(spec: BdpSpec, perf_metric: str) -> str:
    base = f"BDP_Ai_Tj_{spec.slug}"
    if perf_metric.strip().lower() != "ppm":
        return f"{base}_{perf_metric.strip().lower()}"
    return base


def run_spec(
    spec: BdpSpec,
    perf_metric: str,
    *,
    overlay_dft: bool = False,
    out_png: Path | None = None,
    figsize: tuple[float, float] = (10.5, 4.2),
) -> Path:
    sys.path.insert(0, str(SPORTS))
    from sports_pipeline.perf_metric import plot_label_for_metric

    ensure_hero_dirs()
    stem = _output_stem(spec, perf_metric)
    out_png = out_png or (BASIC_DATA_PLOTS / f"{stem}.png")
    out_meta = BASIC_DATA_PLOTS / f"{stem}.json"
    perf_label = plot_label_for_metric(perf_metric)
    perf_axis = rf"{perf_metric.upper()} $z$ within season"

    use = _prepare(spec, perf_metric)
    ability = use["perf"].to_numpy(dtype=float)
    team_talent = _team_talent(use)

    ability_dft: np.ndarray | None = None
    team_talent_dft: np.ndarray | None = None
    dft_meta: dict | None = None
    if overlay_dft and not spec.dft:
        spec_dft = replace(spec, dft=True)
        use_dft = _prepare(spec_dft, perf_metric)
        ability_dft = use_dft["perf"].to_numpy(dtype=float)
        team_talent_dft = _team_talent(use_dft)
        dft_meta = {
            "A_i_hat": _summary(ability_dft),
            "T_j_hat": _summary(team_talent_dft),
            "n_player_seasons": int(len(use_dft)),
            "n_team_seasons": int(
                use_dft.groupby(["team_id", "season"], observed=True).ngroups
            ),
        }

    build_figure(
        spec,
        ability,
        team_talent,
        out_png,
        perf_metric,
        perf_axis,
        ability_dft=ability_dft,
        team_talent_dft=team_talent_dft,
        figsize=figsize,
    )

    n_drafted = int(pd.to_numeric(use["Y_draft"], errors="coerce").fillna(0).sum())
    meta = {
        "diagnostic": "bdp_ai_tj_distributions",
        "date": date.today().isoformat(),
        "bdp_spec": spec.label,
        "perf_metric": perf_metric,
        "seasons": f"{spec.season_min}-{spec.season_max}",
        "qc": "drop_dash_placeholder_names=True",
        "min_team_season_games": spec.min_team_season_games,
        "min_minutes": spec.min_minutes,
        "dft": spec.dft,
        "overlay_dft": overlay_dft and not spec.dft,
        "perf": f"{perf_label} z within season (no poolq winsor)",
        "png": out_png.name,
        "A_i_hat": _summary(ability),
        "T_j_hat": _summary(team_talent),
        "n_team_seasons": int(use.groupby(["team_id", "season"], observed=True).ngroups),
        "theta_K_over_N": {
            "n_accepted": n_drafted,
            "n_total": int(len(use)),
            "K_over_N": n_drafted / len(use) if len(use) else float("nan"),
        },
    }
    if dft_meta:
        meta["dft_overlay"] = dft_meta
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_meta.relative_to(REPO)}")
    msg = (
        f"  {spec.label}: n_ps={len(use):,} team_seasons={meta['n_team_seasons']:,} "
        f"K/N={meta['theta_K_over_N']['K_over_N']:.5f}"
    )
    if dft_meta:
        msg += f"  |  +DFT n_ps={dft_meta['n_player_seasons']:,}"
    print(msg)
    return out_png


def main() -> None:
    parser = argparse.ArgumentParser(description="BDP A_i / T_j distribution pairs.")
    parser.add_argument(
        "--perf-metric",
        default="ppm",
        choices=("ppm", "bpm", "obpm", "dbpm"),
        help="Ability measure for A_i / T_j (default: ppm).",
    )
    parser.add_argument(
        "--overlay-dft",
        action="store_true",
        default=True,
        help="Overlay orange +DFT line on blue bars (default: on).",
    )
    parser.add_argument(
        "--no-overlay-dft",
        action="store_false",
        dest="overlay_dft",
        help="Disable +DFT orange overlay.",
    )
    parser.add_argument(
        "--spec",
        action="append",
        dest="specs",
        help=f"BDP filter chain (default: {DEFAULT_SPECS}).",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Output PNG filename under basic_data_plots/ (e.g. test.png).",
    )
    parser.add_argument(
        "--fig-height",
        type=float,
        default=6.5,
        help="Figure height in inches (default: 6.5).",
    )
    args = parser.parse_args()
    specs = [parse_bdp_spec(s) for s in (args.specs or DEFAULT_SPECS)]
    figsize = (10.5, args.fig_height)
    out_png = (BASIC_DATA_PLOTS / args.out) if args.out else None
    for i, spec in enumerate(specs):
        print(f"\n=== {args.perf_metric} · {spec.label} ===")
        run_spec(
            spec,
            args.perf_metric,
            overlay_dft=args.overlay_dft,
            out_png=out_png if (out_png and len(specs) == 1) else None,
            figsize=figsize,
        )
    print("\nDone.")


if __name__ == "__main__":
    main()
