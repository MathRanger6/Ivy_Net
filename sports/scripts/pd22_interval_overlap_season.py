#!/usr/bin/env python3
"""PD22 items 10–11 — single-season PD17-style interval overlap.

Reproduce empirical team talent-window overlap for one season (not pooled).
Default season 2012 (rho* ≈ 0 under drop-at-20 bracket).

Run (repo root):
  python sports/scripts/pd22_interval_overlap_season.py --season 2012
  python sports/scripts/pd22_interval_overlap_season.py --season 2013
  python sports/scripts/pd22_interval_overlap_season.py --plot-only --season 2012

Outputs (HEROs_and_PASSes/pd22_minutes/):
  PD22_interval_overlap_season_{season}.png
  PD22_interval_overlap_season_{season}.csv
  PD22_interval_overlap_season_{season}.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from empirical_team_interval_overlap import (
    _compute_H_sort,
    _prepare_panel,
    _team_intervals,
    build_figure,
)
from hero_gallery_paths import PD21_RHO, PD22_MINUTES, ensure_hero_dirs

from pd20_22_campaign_window import (
    activate_from_args,
    add_window_args,
    current_window,
)

OUT = PD22_MINUTES
DEFAULT_SEASON = 2012


def _w():
    return current_window()


def _drop_json() -> Path:
    return PD21_RHO / f"PD21_rho_hsort_calibrate_{_w().tag}_fit_bracket.json"


def _stem(season: int) -> str:
    return f"PD22_interval_overlap_season_{season}"


def _artifact_paths(season: int) -> dict[str, Path]:
    stem = _stem(season)
    return {
        "png": OUT / f"{stem}.png",
        "csv": OUT / f"{stem}.csv",
        "json": OUT / f"{stem}.json",
    }


def _rho_star_drop(season: int) -> float | None:
    drop_json = _drop_json()
    if not drop_json.is_file():
        return None
    meta = json.loads(drop_json.read_text(encoding="utf-8"))
    for row in meta.get("per_season", []):
        if int(row["season"]) == int(season):
            return float(row["rho_star"])
    return None


def run(*, season: int) -> dict:
    ensure_hero_dirs()
    paths = _artifact_paths(season)

    panel = _prepare_panel()
    panel = panel.loc[panel["season"] == int(season)].copy()
    if panel.empty:
        raise ValueError(f"No panel rows for season {season}")

    iv, work = _team_intervals(panel)
    h_sort = _compute_H_sort(work)
    rho_star = _rho_star_drop(season)

    stats = build_figure(
        iv,
        work,
        png_path=paths["png"],
        seasons=str(season),
        h_sort=h_sort,
    )

    iv.to_csv(paths["csv"], index=False, float_format="%.12g")

    meta = {
        "diagnostic": "pd22_interval_overlap_season",
        "pd22_item": 10 if int(season) == 2012 else (11 if int(season) == 2013 else None),
        "date": date.today().isoformat(),
        "season": int(season),
        "panel_spec": "drop-at-20 hero panel; PPM z within season; single season only",
        "rho_star_drop_bracket": rho_star,
        "question": (
            "Does PD17-style interval overlap structure persist when bracket rho* ≈ 0?"
            if rho_star is not None and abs(rho_star) < 0.01
            else "Single-season overlap vs bracket rho*."
        ),
        **stats,
        "outputs": {k: str(v.relative_to(REPO)) for k, v in paths.items()},
    }
    paths["json"].write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(f"\nSeason {season}: team-seasons={stats['n_team_seasons']:,}, "
          f"H_sort={h_sort:.4f}, rho*={rho_star}", flush=True)
    print(f"Max coverage={stats['coverage_max']:,}, "
          f"grid frac >1 team={stats['coverage_frac_gt_1']:.1%}", flush=True)
    print(f"\nWrote {paths['png']}", flush=True)
    print(f"Wrote {paths['csv']}", flush=True)
    print(f"Wrote {paths['json']}", flush=True)
    return meta


def plot_only(*, season: int) -> None:
    paths = _artifact_paths(season)
    if not paths["csv"].is_file():
        raise SystemExit(f"Missing CSV — run full diagnostic first: {paths['csv']}")
    iv = pd.read_csv(paths["csv"])
    panel = _prepare_panel()
    work = panel.loc[panel["season"] == int(season)].dropna(subset=["perf", "team_id", "season"])
    h_sort = _compute_H_sort(work)
    meta = json.loads(paths["json"].read_text(encoding="utf-8")) if paths["json"].is_file() else {}
    stats = build_figure(
        iv,
        work,
        png_path=paths["png"],
        seasons=str(season),
        h_sort=h_sort,
    )
    print(f"Wrote {paths['png']}", flush=True)
    _ = stats, meta


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--season", type=int, default=DEFAULT_SEASON, help=f"Season (default: {DEFAULT_SEASON})")
    parser.add_argument("--plot-only", action="store_true")
    add_window_args(parser)
    args = parser.parse_args()
    activate_from_args(args)
    if args.plot_only:
        plot_only(season=int(args.season))
    else:
        run(season=int(args.season))


if __name__ == "__main__":
    main()
