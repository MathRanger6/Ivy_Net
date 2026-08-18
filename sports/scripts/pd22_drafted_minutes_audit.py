#!/usr/bin/env python3
"""PD22 item 1 — drafted-player retention vs min_minutes floor.

Build panel once at min_minutes=0; audit ever-draft (Y_draft=1) player-seasons against
candidate playing-time floors under drop policy. PPM-zero policy retains all rows.

Run (repo root):
  python sports/scripts/pd22_drafted_minutes_audit.py
  python sports/scripts/pd22_drafted_minutes_audit.py --thresholds 0 5 10 15 20
  python sports/scripts/pd22_drafted_minutes_audit.py --plot-only

Outputs (HEROs_and_PASSes/pd22_minutes/):
  PD22_drafted_minutes_audit_2011_2021.csv
  PD22_drafted_minutes_threshold_table_2011_2021.csv
  PD22_drafted_minutes_audit_2011_2021.json
  PD22_drafted_minutes_audit_2011_2021.png
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

OUT = PD22_MINUTES
SEASON_MIN = 2011
SEASON_MAX = 2021
DEFAULT_THRESHOLDS = (0, 1, 2, 5, 8, 10, 15, 20, 25, 30)
HERO_LOCK = 20.0
STEM = f"PD22_drafted_minutes_audit_{SEASON_MIN}_{SEASON_MAX}"


def _pipeline_config() -> object:
    from sports_pipeline.config import PipelineConfig

    return PipelineConfig(
        perf_metric=["ppm"],
        perf_zscore_within_season=True,
        ventiles=16,
        poolq_binning="quantile",
        poolq_winsor_quantiles=(0.01, 0.99),
        min_minutes=0.0,
        restrict_teams_by_draftees=False,
        use_prebuilt_panel_csv=False,
        panel_season_min=SEASON_MIN,
        panel_season_max=SEASON_MAX,
        analysis_season_min=SEASON_MIN,
        analysis_season_max=SEASON_MAX,
    )


def _load_raw_panel() -> pd.DataFrame:
    from sports_pipeline import conductor

    cfg = _pipeline_config()
    print("Rebuilding panel from box (min_minutes=0) ...", flush=True)
    panel = conductor.prepare_panel(cfg)
    if "Y_draft" not in panel.columns:
        raise KeyError("Panel missing Y_draft — check draft lookup merge in panel_rebuild.")
    if "minutes" not in panel.columns:
        raise KeyError("Panel missing minutes column.")
    return panel


def _drafted_table(panel: pd.DataFrame) -> pd.DataFrame:
    drafted = panel.loc[pd.to_numeric(panel["Y_draft"], errors="coerce").fillna(0).astype(int) == 1].copy()
    drafted["minutes"] = pd.to_numeric(drafted["minutes"], errors="coerce")
    if "ppm" in drafted.columns:
        drafted["ppm"] = pd.to_numeric(drafted["ppm"], errors="coerce")
    if "points" in drafted.columns:
        drafted["points"] = pd.to_numeric(drafted["points"], errors="coerce")

    name_col = "athlete_display_name" if "athlete_display_name" in drafted.columns else None
    team_col = "team_short_display_name" if "team_short_display_name" in drafted.columns else None

    cols = ["athlete_id", "season", "team_id", "minutes", "ppm", "points", "Y_draft"]
    if name_col:
        cols.insert(1, name_col)
    if team_col:
        cols.insert(-1, team_col)
    cols = [c for c in cols if c in drafted.columns]

    out = drafted[cols].sort_values(["minutes", "season", "athlete_id"], ascending=[True, True, True])
    out = out.reset_index(drop=True)
    out["lost_at_min20_drop"] = out["minutes"] < HERO_LOCK
    out["zeroed_at_min20_ppm0"] = out["minutes"] < HERO_LOCK
    return out


def _unique_lost(drafted: pd.DataFrame, threshold: float) -> int:
    sub = drafted.loc[pd.to_numeric(drafted["minutes"], errors="coerce") < float(threshold)]
    return int(sub["athlete_id"].nunique()) if len(sub) else 0


def _threshold_table(drafted: pd.DataFrame, thresholds: list[float]) -> pd.DataFrame:
    mins = drafted["minutes"].to_numpy(dtype=float)
    n_total = int(len(drafted))
    rows = []
    for thr in thresholds:
        t = float(thr)
        n_lost = int(np.sum(mins < t)) if n_total else 0
        rows.append(
            {
                "min_minutes_threshold": t,
                "n_drafted_retained_drop": n_total - n_lost,
                "n_drafted_lost_drop": n_lost,
                "n_unique_drafted_lost_drop": _unique_lost(drafted, t),
                "pct_drafted_retained_drop": (n_total - n_lost) / n_total if n_total else float("nan"),
                "n_drafted_retained_ppm_zero": n_total,
                "n_zeroed_ppm_zero": n_lost,
            }
        )
    return pd.DataFrame(rows)


def _summary(drafted: pd.DataFrame, threshold_df: pd.DataFrame) -> dict:
    mins = drafted["minutes"].dropna()
    min_m = float(mins.min()) if len(mins) else float("nan")
    max_m = float(mins.max()) if len(mins) else float("nan")
    row20 = threshold_df.loc[threshold_df["min_minutes_threshold"] == HERO_LOCK]
    if row20.empty:
        nearest = threshold_df.iloc[(threshold_df["min_minutes_threshold"] - HERO_LOCK).abs().argsort()[:1]]
        row20 = nearest
    n_lost_20 = int(row20["n_drafted_lost_drop"].iloc[0]) if len(row20) else 0
    n_retained_20 = int(row20["n_drafted_retained_drop"].iloc[0]) if len(row20) else 0

    lost_rows = drafted.loc[drafted["minutes"] < HERO_LOCK]
    lost_zero = drafted.loc[pd.to_numeric(drafted["minutes"], errors="coerce").fillna(-1) == 0]
    draft_safe_max_floor = min_m if np.isfinite(min_m) else float("nan")

    return {
        "n_drafted_player_seasons": int(len(drafted)),
        "n_unique_drafted_athletes": int(drafted["athlete_id"].nunique()) if len(drafted) else 0,
        "min_minutes_among_drafted": min_m,
        "max_minutes_among_drafted": max_m,
        "median_minutes_among_drafted": float(mins.median()) if len(mins) else float("nan"),
        "draft_safe_max_floor_drop": draft_safe_max_floor,
        "hero_lock_min_minutes": HERO_LOCK,
        "n_lost_at_hero_lock_drop": n_lost_20,
        "n_unique_lost_at_hero_lock_drop": _unique_lost(drafted, HERO_LOCK),
        "n_lost_zero_minutes_at_hero_lock_drop": int(len(lost_zero)),
        "n_retained_at_hero_lock_drop": n_retained_20,
        "n_lost_player_season_ids_at_20": lost_rows[["athlete_id", "season", "minutes"]].to_dict(orient="records")
        if len(lost_rows)
        else [],
    }


def _plot_audit(drafted: pd.DataFrame, threshold_df: pd.DataFrame, summary: dict, png_path: Path) -> None:
    configure_matplotlib_mathtext()
    seasons = seasons_label(SEASON_MIN, SEASON_MAX)
    mins = drafted["minutes"].dropna().to_numpy(dtype=float)
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6))

    ax = axes[0]
    if len(mins):
        xs = np.sort(mins)
        ys = np.arange(1, len(xs) + 1) / len(xs)
        ax.step(xs, ys, where="post", color="steelblue", lw=2)
    for thr, color, ls in [(10, "teal", "--"), (HERO_LOCK, "crimson", "-")]:
        ax.axvline(thr, color=color, ls=ls, lw=1.5, alpha=0.85, label=rf"min = {thr:g}")
    ax.set_xlabel("Season minutes (drafted player-seasons)")
    ax.set_ylabel("Cumulative fraction")
    ax.set_title(rf"Drafted minutes — empirical CDF (ECDF) · {seasons}")
    ax.grid(alpha=0.25, linewidth=0.5)
    ax.legend(fontsize=8, loc="lower right")

    ax = axes[1]
    x = threshold_df["min_minutes_threshold"].to_numpy(dtype=float)
    y = threshold_df["n_drafted_retained_drop"].to_numpy(dtype=int)
    n_lost_pts = threshold_df["n_drafted_lost_drop"].to_numpy(dtype=int)
    ax.plot(x, y, "o-", color="steelblue", lw=2, ms=6, label="Drop policy")
    for xi, yi, nl in zip(x, y, n_lost_pts):
        if nl <= 0:
            continue
        ax.annotate(
            str(int(nl)),
            (xi, yi),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            va="bottom",
            color="crimson",
            fontsize=9,
            fontweight="bold",
        )
    ax.axhline(summary["n_drafted_player_seasons"], color="gray", ls=":", lw=1, alpha=0.7)
    ax.axvline(HERO_LOCK, color="crimson", ls="-", lw=1.5, alpha=0.85)
    ax.set_xlabel(r"min_minutes floor (drop if minutes $<$ floor)")
    ax.set_ylabel(r"$n$ drafted player-seasons retained")
    n_lost = summary["n_lost_at_hero_lock_drop"]
    n_unique_lost = summary.get("n_unique_lost_at_hero_lock_drop", n_lost)
    n_all = summary["n_drafted_player_seasons"]
    ax.set_title(
        rf"Retention vs floor · at 20 min: {n_all - n_lost}/{n_all} kept "
        rf"({n_unique_lost} unique athletes lost)"
    )
    y_lo = int(y.min()) if len(y) else 0
    y_hi = int(y.max()) if len(y) else n_all
    span = max(y_hi - y_lo, 1)
    margin = max(4, int(round(span * 0.08)))
    label_headroom = max(10, int(round(span * 0.12)))
    ax.set_ylim(y_lo - margin, y_hi + margin + label_headroom)
    ax.grid(alpha=0.25, linewidth=0.5)
    ax.legend(fontsize=8, loc="lower left")

    safe = summary["draft_safe_max_floor_drop"]
    safe_s = f"{safe:.2g}" if np.isfinite(safe) else "?"
    fig.suptitle(
        rf"PD22 item 1 — draft-safe max floor (drop) $\approx {safe_s}$ min · "
        rf"{summary['n_lost_at_hero_lock_drop']} lost at {HERO_LOCK:g} min",
        fontsize=11,
        y=1.02,
    )
    fig.tight_layout()
    fig.savefig(png_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _artifact_paths() -> dict[str, Path]:
    return {
        "csv": OUT / f"{STEM}.csv",
        "threshold_csv": OUT / f"{STEM.replace('_audit_', '_threshold_table_')}.csv",
        "json": OUT / f"{STEM}.json",
        "png": OUT / f"{STEM}.png",
    }


def run_audit(*, thresholds: list[float]) -> dict:
    ensure_hero_dirs()
    paths = _artifact_paths()

    panel = _load_raw_panel()
    drafted = _drafted_table(panel)
    threshold_df = _threshold_table(drafted, thresholds)
    summary = _summary(drafted, threshold_df)

    drafted.to_csv(paths["csv"], index=False, float_format="%.12g")
    threshold_df.to_csv(paths["threshold_csv"], index=False, float_format="%.12g")
    _plot_audit(drafted, threshold_df, summary, paths["png"])

    meta = {
        "diagnostic": "pd22_drafted_minutes_audit",
        "date": date.today().isoformat(),
        "season_min": SEASON_MIN,
        "season_max": SEASON_MAX,
        "seasons": seasons_label(SEASON_MIN, SEASON_MAX),
        "panel_spec": "rebuild from box, min_minutes=0 at rebuild; Y_draft ever-draft flag",
        "thresholds": thresholds,
        "summary": summary,
        "outputs": {k: str(v.relative_to(REPO)) for k, v in paths.items()},
    }
    paths["json"].write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(f"\nDrafted player-seasons: {summary['n_drafted_player_seasons']:,}", flush=True)
    print(f"Unique drafted athletes: {summary['n_unique_drafted_athletes']:,}", flush=True)
    print(f"Min minutes among drafted: {summary['min_minutes_among_drafted']:.4g}", flush=True)
    print(
        f"At min={HERO_LOCK:g} drop: retain {summary['n_retained_at_hero_lock_drop']:,}, "
        f"lose {summary['n_lost_at_hero_lock_drop']:,} player-seasons "
        f"({summary['n_unique_lost_at_hero_lock_drop']:,} unique athletes; "
        f"{summary['n_lost_zero_minutes_at_hero_lock_drop']:,} at 0 min)",
        flush=True,
    )
    if summary["n_lost_player_season_ids_at_20"]:
        print("Lost at 20 min (drop policy):", flush=True)
        for row in summary["n_lost_player_season_ids_at_20"]:
            print(f"  athlete_id={row['athlete_id']} season={row['season']} minutes={row['minutes']}", flush=True)

    print(f"\nWrote {paths['csv']}", flush=True)
    print(f"Wrote {paths['threshold_csv']}", flush=True)
    print(f"Wrote {paths['png']}", flush=True)
    print(f"Wrote {paths['json']}", flush=True)
    return meta


def plot_only() -> None:
    paths = _artifact_paths()
    if not paths["csv"].is_file() or not paths["threshold_csv"].is_file():
        raise SystemExit(f"Missing CSV artifacts — run full audit first: {paths['csv']}")
    drafted = pd.read_csv(paths["csv"])
    threshold_df = pd.read_csv(paths["threshold_csv"])
    meta = json.loads(paths["json"].read_text(encoding="utf-8")) if paths["json"].is_file() else {}
    summary = _summary(drafted, threshold_df)
    _plot_audit(drafted, threshold_df, summary, paths["png"])
    print(f"Wrote {paths['png']}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--thresholds",
        type=float,
        nargs="+",
        default=list(DEFAULT_THRESHOLDS),
        help=f"Candidate min_minutes floors (default: {list(DEFAULT_THRESHOLDS)})",
    )
    parser.add_argument(
        "--plot-only",
        action="store_true",
        help="Regenerate PNG from existing CSV/JSON (no panel rebuild)",
    )
    args = parser.parse_args()

    if args.plot_only:
        plot_only()
        return

    thresholds = sorted(set(float(t) for t in args.thresholds))
    run_audit(thresholds=thresholds)


if __name__ == "__main__":
    main()
