#!/usr/bin/env python3
"""PD22 item 8 — bench-zero clustering vs empirical H_sort under PPM-zero.

Per team-season on the PPM-zero panel: count policy-zeroed players and within-team
perf dispersion. Compare season-level empirical H_sort under drop vs PPM-zero.

Run (repo root):
  python sports/scripts/pd22_ppm_zero_hsort_mechanism.py
  python sports/scripts/pd22_ppm_zero_hsort_mechanism.py --plot-only

Outputs (HEROs_and_PASSes/pd22_minutes/):
  PD22_ppm_zero_hsort_mechanism_2011_2021.csv
  PD22_ppm_zero_hsort_mechanism_season_2011_2021.csv
  PD22_ppm_zero_hsort_mechanism_2011_2021.json
  PD22_ppm_zero_hsort_mechanism_2011_2021.png
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SPORTS))
sys.path.insert(0, str(SCRIPTS))

from gallery_mathtext import configure_matplotlib_mathtext
from hero_gallery_paths import PD22_MINUTES, ensure_hero_dirs
from interval_overlap_paths import seasons_label

from pd20_22_campaign_window import (
    activate_from_args,
    add_window_args,
    current_window,
)


def _w():
    return current_window()


STEM_PREFIX = "PD22_ppm_zero_hsort_mechanism"


def _stem() -> str:
    return f"{STEM_PREFIX}_{_w().tag}"
from pd21_rho_hsort_calibrate import PanelPrepConfig, empirical_h_sort, prepare_calibration_panel

OUT = PD22_MINUTES
DEFAULT_PPM_ZERO = 20.0
SEASON_STEM = f"{_stem().replace('_mechanism_', '_mechanism_season_')}"


def _pipeline_config(*, min_minutes: float) -> object:
    from sports_pipeline.config import PipelineConfig

    return PipelineConfig(
        perf_metric=["ppm"],
        perf_zscore_within_season=True,
        ventiles=16,
        poolq_binning="quantile",
        poolq_winsor_quantiles=(0.01, 0.99),
        min_minutes=float(min_minutes),
        restrict_teams_by_draftees=False,
        use_prebuilt_panel_csv=False,
        panel_season_min=_w().season_min,
        panel_season_max=_w().season_max,
        analysis_season_min=_w().season_min,
        analysis_season_max=_w().season_max,
    )


def _load_drop_panel() -> pd.DataFrame:
    from sports_pipeline import conductor, panel_build
    from sports_pipeline.perf_metric import perf_metric_active

    cfg = _pipeline_config(min_minutes=DEFAULT_PPM_ZERO)
    print(f"Rebuilding drop panel (min_minutes={DEFAULT_PPM_ZERO:g}) ...", flush=True)
    raw = conductor.prepare_panel(cfg)
    panel = panel_build.apply_perf_metric_for_analysis(
        raw,
        perf_metric_active(cfg),
        poolq_winsor_quantiles=cfg.poolq_winsor_quantiles,
        zscore_perf_within_season=True,
    )
    return panel_build.filter_panel(panel, cfg)


def _load_ppm_zero_panel(*, ppm_zero_below_minutes: float) -> pd.DataFrame:
    cfg = PanelPrepConfig.from_args(min_minutes=0.0, ppm_zero_below_minutes=ppm_zero_below_minutes)
    print(f"Rebuilding PPM-zero panel (threshold={ppm_zero_below_minutes:g} min) ...", flush=True)
    return prepare_calibration_panel(cfg)


def _team_season_table(panel: pd.DataFrame, *, ppm_zero_below_minutes: float) -> pd.DataFrame:
    thr = float(ppm_zero_below_minutes)
    df = panel.copy()
    df["minutes"] = pd.to_numeric(df["minutes"], errors="coerce")
    df["perf"] = pd.to_numeric(df["perf"], errors="coerce")
    df["zeroed_by_policy"] = df["minutes"].notna() & (df["minutes"] < thr)

    rows = []
    for (team_id, season), g in df.groupby(["team_id", "season"], sort=True):
        perf = g["perf"].dropna()
        n = int(len(g))
        n_zero = int(g["zeroed_by_policy"].sum())
        row = {
            "team_id": int(team_id),
            "season": int(season),
            "n_roster": n,
            "n_zeroed_by_policy": n_zero,
            "zero_fraction": n_zero / n if n else float("nan"),
            "perf_std": float(perf.std(ddof=0)) if len(perf) >= 2 else float("nan"),
            "perf_var": float(perf.var(ddof=0)) if len(perf) >= 2 else float("nan"),
            "perf_range": float(perf.max() - perf.min()) if len(perf) >= 2 else float("nan"),
        }
        if "team_short_display_name" in g.columns:
            row["team_short_display_name"] = g["team_short_display_name"].iloc[0]
        rows.append(row)
    return pd.DataFrame(rows)


def _season_hsort_table(
    drop_panel: pd.DataFrame,
    ppm_zero_panel: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    for season in range(_w().season_min, _w().season_max + 1):
        sub_drop = drop_panel.loc[drop_panel["season"] == season]
        sub_pz = ppm_zero_panel.loc[ppm_zero_panel["season"] == season]
        h_drop = empirical_h_sort(sub_drop)
        h_pz = empirical_h_sort(sub_pz)
        ts = _team_season_table(sub_pz, ppm_zero_below_minutes=DEFAULT_PPM_ZERO)
        ts_season = ts.loc[ts["season"] == season]
        rows.append(
            {
                "season": int(season),
                "h_sort_drop": h_drop,
                "h_sort_ppm_zero": h_pz,
                "h_sort_delta_ppm_zero_minus_drop": h_pz - h_drop,
                "n_players_drop": int(sub_drop["perf"].notna().sum()),
                "n_players_ppm_zero": int(sub_pz["perf"].notna().sum()),
                "mean_zero_fraction": float(ts_season["zero_fraction"].mean()) if len(ts_season) else float("nan"),
                "median_zero_fraction": float(ts_season["zero_fraction"].median()) if len(ts_season) else float("nan"),
            }
        )
    return pd.DataFrame(rows)


def _corr(x: pd.Series, y: pd.Series) -> float:
    frame = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(frame) < 3:
        return float("nan")
    return float(frame["x"].corr(frame["y"]))


def _summary(team_df: pd.DataFrame, season_df: pd.DataFrame, *, ppm_zero_below_minutes: float) -> dict:
    valid = team_df.dropna(subset=["zero_fraction", "perf_std"])
    r_zero_std = _corr(valid["zero_fraction"], valid["perf_std"])
    r_zero_var = _corr(valid["zero_fraction"], valid["perf_var"])
    r_season_zero_h = _corr(season_df["mean_zero_fraction"], season_df["h_sort_ppm_zero"])
    r_season_zero_delta = _corr(season_df["mean_zero_fraction"], season_df["h_sort_delta_ppm_zero_minus_drop"])

    return {
        "ppm_zero_below_minutes": float(ppm_zero_below_minutes),
        "n_team_seasons": int(len(team_df)),
        "corr_zero_fraction_vs_perf_std": r_zero_std,
        "corr_zero_fraction_vs_perf_var": r_zero_var,
        "corr_season_mean_zero_fraction_vs_h_sort_ppm_zero": r_season_zero_h,
        "corr_season_mean_zero_fraction_vs_h_sort_delta": r_season_zero_delta,
        "h_sort_drop_mean": float(season_df["h_sort_drop"].mean()),
        "h_sort_ppm_zero_mean": float(season_df["h_sort_ppm_zero"].mean()),
        "h_sort_delta_mean": float(season_df["h_sort_delta_ppm_zero_minus_drop"].mean()),
        "h_sort_delta_min": float(season_df["h_sort_delta_ppm_zero_minus_drop"].min()),
        "h_sort_delta_max": float(season_df["h_sort_delta_ppm_zero_minus_drop"].max()),
        "n_team_seasons_ge_half_zeroed": int((team_df["zero_fraction"] >= 0.5).sum()),
    }


def _plot(team_df: pd.DataFrame, season_df: pd.DataFrame, summary: dict, png_path: Path) -> None:
    configure_matplotlib_mathtext()
    seasons = seasons_label(_w().season_min, _w().season_max)
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.8))

    ax = axes[0]
    valid = team_df.dropna(subset=["zero_fraction", "perf_std"])
    if len(valid):
        ax.scatter(
            valid["zero_fraction"],
            valid["perf_std"],
            s=12,
            alpha=0.35,
            color="steelblue",
            edgecolors="none",
        )
    r = summary["corr_zero_fraction_vs_perf_std"]
    ax.set_xlabel(rf"Zeroed fraction per team-season (min $<$ {DEFAULT_PPM_ZERO:g})")
    ax.set_ylabel(r"Within-team perf std (PPM $z$)")
    ax.set_title(rf"Bench-zero share vs dispersion · $r = {r:.3f}$")
    ax.grid(alpha=0.25, linewidth=0.5)

    ax = axes[1]
    xs = season_df["season"].to_numpy(dtype=int)
    ax.plot(xs, season_df["h_sort_drop"], "o-", color="darkorange", lw=2, ms=5, label="Drop (min 20)")
    ax.plot(xs, season_df["h_sort_ppm_zero"], "s-", color="steelblue", lw=2, ms=5, label="PPM-zero")
    ax.set_xlabel("Season")
    ax.set_ylabel(r"Empirical $H_{\mathrm{sort}}$")
    delta_mean = summary["h_sort_delta_mean"]
    ax.set_title(rf"Season $H_{{\mathrm{{sort}}}}$ · $\Delta$ mean = {delta_mean:+.4f}")
    ax.legend(fontsize=8, loc="best")
    ax.grid(alpha=0.25, linewidth=0.5)

    fig.suptitle(
        rf"PD22 item 8 — bench zeros vs sorting · {seasons} · "
        rf"$H_{{\mathrm{{sort}}}}$ ppm-zero mean = {summary['h_sort_ppm_zero_mean']:.4f} "
        rf"(drop {summary['h_sort_drop_mean']:.4f})",
        fontsize=11,
        y=1.02,
    )
    fig.tight_layout()
    fig.savefig(png_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _artifact_paths() -> dict[str, Path]:
    return {
        "csv": OUT / f"{_stem()}.csv",
        "season_csv": OUT / f"{SEASON_STEM}.csv",
        "json": OUT / f"{_stem()}.json",
        "png": OUT / f"{_stem()}.png",
    }


def run(*, ppm_zero_below_minutes: float) -> dict:
    ensure_hero_dirs()
    paths = _artifact_paths()

    drop_panel = _load_drop_panel()
    ppm_zero_panel = _load_ppm_zero_panel(ppm_zero_below_minutes=ppm_zero_below_minutes)
    team_df = _team_season_table(ppm_zero_panel, ppm_zero_below_minutes=ppm_zero_below_minutes)
    season_df = _season_hsort_table(drop_panel, ppm_zero_panel)
    summary = _summary(team_df, season_df, ppm_zero_below_minutes=ppm_zero_below_minutes)
    _plot(team_df, season_df, summary, paths["png"])

    team_df.to_csv(paths["csv"], index=False, float_format="%.12g")
    season_df.to_csv(paths["season_csv"], index=False, float_format="%.12g")

    meta = {
        "diagnostic": "pd22_ppm_zero_hsort_mechanism",
        "date": date.today().isoformat(),
        "season_min": _w().season_min,
        "season_max": _w().season_max,
        "seasons": seasons_label(_w().season_min, _w().season_max),
        "panel_spec": (
            f"PPM-zero min=0 + ppm_zero_below={ppm_zero_below_minutes:g}; "
            f"drop min={DEFAULT_PPM_ZERO:g}; H_sort from realized partition on perf"
        ),
        "summary": summary,
        "outputs": {k: str(v.relative_to(REPO)) for k, v in paths.items()},
    }
    paths["json"].write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(f"\nTeam-seasons: {summary['n_team_seasons']:,}", flush=True)
    print(f"corr(zero_fraction, perf_std) = {summary['corr_zero_fraction_vs_perf_std']:.4f}", flush=True)
    print(
        f"H_sort mean: drop={summary['h_sort_drop_mean']:.4f}, "
        f"ppm-zero={summary['h_sort_ppm_zero_mean']:.4f}, "
        f"delta={summary['h_sort_delta_mean']:+.4f}",
        flush=True,
    )
    print(f"\nWrote {paths['png']}", flush=True)
    print(f"Wrote {paths['csv']}", flush=True)
    print(f"Wrote {paths['season_csv']}", flush=True)
    print(f"Wrote {paths['json']}", flush=True)
    return meta


def plot_only() -> None:
    paths = _artifact_paths()
    if not paths["csv"].is_file() or not paths["season_csv"].is_file():
        raise SystemExit(f"Missing CSV — run full diagnostic first: {paths['csv']}")
    team_df = pd.read_csv(paths["csv"])
    season_df = pd.read_csv(paths["season_csv"])
    meta = json.loads(paths["json"].read_text(encoding="utf-8")) if paths["json"].is_file() else {}
    thr = float(meta.get("summary", {}).get("ppm_zero_below_minutes", DEFAULT_PPM_ZERO))
    summary = _summary(team_df, season_df, ppm_zero_below_minutes=thr)
    _plot(team_df, season_df, summary, paths["png"])
    print(f"Wrote {paths['png']}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ppm-zero-below-minutes",
        type=float,
        default=DEFAULT_PPM_ZERO,
        help=f"Minutes threshold for PPM-zero policy (default: {DEFAULT_PPM_ZERO:g})",
    )
    parser.add_argument(
        "--plot-only",
        action="store_true",
        help="Regenerate PNG from existing CSV (no panel rebuild)",
    )
    add_window_args(parser)
    args = parser.parse_args()
    activate_from_args(args)
    if args.plot_only:
        plot_only()
    else:
        run(ppm_zero_below_minutes=float(args.ppm_zero_below_minutes))


if __name__ == "__main__":
    main()
