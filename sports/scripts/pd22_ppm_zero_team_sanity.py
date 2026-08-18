#!/usr/bin/env python3
"""PD22 item 7 — no all-zero teams under PPM-zero policy.

Under ``--ppm-zero-below-minutes 20``, verify no team-season has every player
zeroed (sub-floor minutes → PPM forced to 0 before within-season z-score).
Emit per-team counts and headline sanity stats for Alex.

Run (repo root):
  python sports/scripts/pd22_ppm_zero_team_sanity.py
  python sports/scripts/pd22_ppm_zero_team_sanity.py --ppm-zero-below-minutes 20
  python sports/scripts/pd22_ppm_zero_team_sanity.py --plot-only

Outputs (HEROs_and_PASSes/pd22_minutes/):
  PD22_ppm_zero_team_sanity_2011_2021.csv
  PD22_ppm_zero_team_sanity_2011_2021.json
  PD22_ppm_zero_team_sanity_2011_2021.png
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
from pd21_rho_hsort_calibrate import PanelPrepConfig, prepare_calibration_panel

OUT = PD22_MINUTES
SEASON_MIN = 2011
SEASON_MAX = 2021
DEFAULT_PPM_ZERO = 20.0
ZERO_COUNT_LADDER = (1, 2, 5, 8, 10, 12, 15, 18, 20, 25, 30)
STEM = f"PD22_ppm_zero_team_sanity_{SEASON_MIN}_{SEASON_MAX}"


def _artifact_paths() -> dict[str, Path]:
    return {
        "csv": OUT / f"{STEM}.csv",
        "json": OUT / f"{STEM}.json",
        "png": OUT / f"{STEM}.png",
    }


def _load_ppm_zero_panel(*, ppm_zero_below_minutes: float) -> pd.DataFrame:
    cfg = PanelPrepConfig.from_args(min_minutes=0.0, ppm_zero_below_minutes=ppm_zero_below_minutes)
    print(f"Building PPM-zero panel (threshold={ppm_zero_below_minutes:g} min) ...", flush=True)
    panel = prepare_calibration_panel(cfg)
    for col in ("team_id", "season", "minutes", "ppm", "perf"):
        if col not in panel.columns:
            raise KeyError(f"Panel missing required column {col!r}")
    return panel


def _team_season_table(panel: pd.DataFrame, *, ppm_zero_below_minutes: float) -> pd.DataFrame:
    thr = float(ppm_zero_below_minutes)
    df = panel.copy()
    df["minutes"] = pd.to_numeric(df["minutes"], errors="coerce")
    df["ppm"] = pd.to_numeric(df["ppm"], errors="coerce")
    df["perf"] = pd.to_numeric(df["perf"], errors="coerce")
    df["zeroed_by_policy"] = df["minutes"].notna() & (df["minutes"] < thr)

    team_col = "team_short_display_name" if "team_short_display_name" in df.columns else None
    group_cols = ["team_id", "season"]

    rows = []
    for (team_id, season), g in df.groupby(group_cols, sort=True):
        n = int(len(g))
        n_zero = int(g["zeroed_by_policy"].sum())
        n_ge_thr = n - n_zero
        mins = g["minutes"].dropna()
        ppm = g["ppm"].dropna()
        perf = g["perf"].dropna()
        perf_span = float(perf.max() - perf.min()) if len(perf) >= 2 else 0.0
        row = {
            "team_id": team_id,
            "season": int(season),
            "n_roster": n,
            "n_zeroed_by_policy": n_zero,
            "n_minutes_ge_threshold": n_ge_thr,
            "zero_fraction": n_zero / n if n else float("nan"),
            "all_zeroed_by_policy": n_zero == n and n > 0,
            "all_raw_ppm_zero": bool(len(ppm) == n and n > 0 and (ppm == 0).all()),
            "all_identical_perf": bool(len(perf) == n and n > 0 and perf_span < 1e-12),
            "min_minutes": float(mins.min()) if len(mins) else float("nan"),
            "max_minutes": float(mins.max()) if len(mins) else float("nan"),
            "max_minutes_below_threshold": float(mins.max()) if n_zero == n and len(mins) else float("nan"),
        }
        if team_col:
            row[team_col] = g[team_col].iloc[0]
        rows.append(row)

    out = pd.DataFrame(rows).sort_values(
        ["all_zeroed_by_policy", "zero_fraction", "season", "team_id"],
        ascending=[False, False, True, True],
    )
    return out.reset_index(drop=True)


def _summary(team_df: pd.DataFrame, *, ppm_zero_below_minutes: float) -> dict:
    n_ts = int(len(team_df))
    frac = team_df["zero_fraction"].to_numpy(dtype=float)
    n_all_zero = int(team_df["all_zeroed_by_policy"].sum())
    n_all_ppm0 = int(team_df["all_raw_ppm_zero"].sum())
    n_all_ident = int(team_df["all_identical_perf"].sum())

    ladder = {}
    for k in ZERO_COUNT_LADDER:
        ladder[str(k)] = int((team_df["n_zeroed_by_policy"] >= k).sum())

    worst = team_df.loc[team_df["zero_fraction"].idxmax()] if n_ts else None
    return {
        "n_team_seasons": n_ts,
        "ppm_zero_below_minutes": float(ppm_zero_below_minutes),
        "n_all_zeroed_by_policy": n_all_zero,
        "n_all_raw_ppm_zero": n_all_ppm0,
        "n_all_identical_perf": n_all_ident,
        "sanity_pass": n_all_zero == 0,
        "zero_fraction_median": float(np.nanmedian(frac)) if n_ts else float("nan"),
        "zero_fraction_p90": float(np.nanpercentile(frac, 90)) if n_ts else float("nan"),
        "zero_fraction_p99": float(np.nanpercentile(frac, 99)) if n_ts else float("nan"),
        "zero_fraction_max": float(np.nanmax(frac)) if n_ts else float("nan"),
        "n_zeroed_ge_half_roster": int((team_df["zero_fraction"] >= 0.5).sum()),
        "teams_with_ge_k_zeros": ladder,
        "worst_team_season": (
            {
                "team_id": int(worst["team_id"]),
                "season": int(worst["season"]),
                "n_roster": int(worst["n_roster"]),
                "n_zeroed_by_policy": int(worst["n_zeroed_by_policy"]),
                "zero_fraction": float(worst["zero_fraction"]),
                "max_minutes": float(worst["max_minutes"]),
            }
            if worst is not None
            else None
        ),
        "all_zeroed_team_seasons": team_df.loc[team_df["all_zeroed_by_policy"]][
            ["team_id", "season", "n_roster", "max_minutes"]
        ].to_dict(orient="records"),
    }


def _plot(team_df: pd.DataFrame, summary: dict, png_path: Path, *, ppm_zero_below_minutes: float) -> None:
    configure_matplotlib_mathtext()
    seasons = seasons_label(SEASON_MIN, SEASON_MAX)
    thr = float(ppm_zero_below_minutes)
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.5))

    ax = axes[0]
    frac = team_df["zero_fraction"].dropna().to_numpy(dtype=float)
    if len(frac):
        ax.hist(frac, bins=30, color="steelblue", edgecolor="white", alpha=0.9)
    ax.axvline(1.0, color="crimson", ls="--", lw=1.5, label="all zeroed (fraction = 1)")
    ax.set_xlabel(rf"Zeroed fraction per team-season (minutes $<$ {thr:g})")
    ax.set_ylabel(r"$n$ team-seasons")
    ax.set_title(rf"Distribution of bench-zero share · max = {summary['zero_fraction_max']:.2f}")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.25, linewidth=0.5)

    ax = axes[1]
    ks = [int(k) for k in ZERO_COUNT_LADDER if int(k) <= int(team_df["n_zeroed_by_policy"].max())]
    if not ks:
        ks = list(ZERO_COUNT_LADDER[:3])
    counts = [summary["teams_with_ge_k_zeros"][str(k)] for k in ks]
    ax.bar([str(k) for k in ks], counts, color="teal", alpha=0.85, edgecolor="white")
    ax.set_xlabel(rf"$k$ — team-seasons with $\geq k$ zeroed players")
    ax.set_ylabel(r"$n$ team-seasons")
    ax.set_title("Teams with many policy-zeroed players")
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)

    verdict = "PASS" if summary["sanity_pass"] else "FAIL"
    fig.suptitle(
        rf"PD22 item 7 — PPM-zero team sanity ({seasons}) · "
        rf"all-zero teams = {summary['n_all_zeroed_by_policy']} [{verdict}]",
        fontsize=11,
        y=1.02,
    )
    fig.tight_layout()
    fig.savefig(png_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def run_sanity(*, ppm_zero_below_minutes: float) -> dict:
    ensure_hero_dirs()
    paths = _artifact_paths()

    panel = _load_ppm_zero_panel(ppm_zero_below_minutes=ppm_zero_below_minutes)
    team_df = _team_season_table(panel, ppm_zero_below_minutes=ppm_zero_below_minutes)
    summary = _summary(team_df, ppm_zero_below_minutes=ppm_zero_below_minutes)

    team_df.to_csv(paths["csv"], index=False, float_format="%.12g")
    _plot(team_df, summary, paths["png"], ppm_zero_below_minutes=ppm_zero_below_minutes)

    meta = {
        "diagnostic": "pd22_ppm_zero_team_sanity",
        "date": date.today().isoformat(),
        "season_min": SEASON_MIN,
        "season_max": SEASON_MAX,
        "seasons": seasons_label(SEASON_MIN, SEASON_MAX),
        "panel_spec": (
            f"rebuild min_minutes=0 + ppm_zero_below={ppm_zero_below_minutes:g}; "
            "perf z-scored within season (PD21 calibration path)"
        ),
        "summary": summary,
        "outputs": {k: str(v.relative_to(REPO)) for k, v in paths.items()},
    }
    paths["json"].write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(f"\nTeam-seasons: {summary['n_team_seasons']:,}", flush=True)
    print(f"All-zeroed teams (every player minutes < {ppm_zero_below_minutes:g}): {summary['n_all_zeroed_by_policy']}", flush=True)
    print(f"Sanity check: {'PASS' if summary['sanity_pass'] else 'FAIL'}", flush=True)
    print(f"Max zero fraction: {summary['zero_fraction_max']:.4f}", flush=True)
    if summary["worst_team_season"]:
        w = summary["worst_team_season"]
        print(
            f"Worst: team_id={w['team_id']} season={w['season']} "
            f"{w['n_zeroed_by_policy']}/{w['n_roster']} zeroed "
            f"(max minutes={w['max_minutes']:.1f})",
            flush=True,
        )
    print(f"\nWrote {paths['csv']}", flush=True)
    print(f"Wrote {paths['png']}", flush=True)
    print(f"Wrote {paths['json']}", flush=True)
    return meta


def plot_only() -> None:
    paths = _artifact_paths()
    if not paths["csv"].is_file():
        raise SystemExit(f"Missing CSV — run full sanity check first: {paths['csv']}")
    team_df = pd.read_csv(paths["csv"])
    meta = json.loads(paths["json"].read_text(encoding="utf-8")) if paths["json"].is_file() else {}
    thr = float(meta.get("summary", {}).get("ppm_zero_below_minutes", DEFAULT_PPM_ZERO))
    summary = _summary(team_df, ppm_zero_below_minutes=thr)
    _plot(team_df, summary, paths["png"], ppm_zero_below_minutes=thr)
    print(f"Wrote {paths['png']}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ppm-zero-below-minutes",
        type=float,
        default=DEFAULT_PPM_ZERO,
        help=f"Minutes floor for PPM-zero policy (default: {DEFAULT_PPM_ZERO:g})",
    )
    parser.add_argument(
        "--plot-only",
        action="store_true",
        help="Regenerate PNG from existing CSV (no panel rebuild)",
    )
    args = parser.parse_args()
    if args.plot_only:
        plot_only()
    else:
        run_sanity(ppm_zero_below_minutes=float(args.ppm_zero_below_minutes))


if __name__ == "__main__":
    main()
