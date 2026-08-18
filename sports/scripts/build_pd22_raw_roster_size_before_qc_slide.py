#!/usr/bin/env python3
"""Build PD22 roster-size BEFORE box QC AUTO slide (motivation / tail diagnostic).

Run (repo root):
  python sports/scripts/build_pd22_raw_roster_size_before_qc_slide.py --slides-only
  python sports/scripts/build_pd22_raw_roster_size_before_qc_slide.py

Output:
  slides/auto/CHAR_PD22_raw_roster_size_distribution_before_qc_AUTO.pptx

Copy into HAND before the after-QC roster slide and games-count pair.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import (
    AUTO_PD22_RAW_ROSTER_SIZE_BEFORE_QC_DECK,
    PD22_MINUTES,
    ensure_hero_dirs,
)
from pd17_interval_overlap_slide import build_figure_focus_slide, load_meta
from pd22_slide_common import m, mgeq, mgt, mpct

DIST_SCRIPT = SCRIPTS / "pd22_raw_roster_size_distribution.py"
SEASON_MIN = 2011
SEASON_MAX = 2021
STEM = f"PD22_raw_roster_size_distribution_{SEASON_MIN}_{SEASON_MAX}_before_qc"
HERO_LOCK = 20.0
NCAA_DRESS = 15

CLAIM = (
    r"Claim (PD22 backup): Raw ESPN box rows inflate team-season roster counts — "
    r"dash placeholders and sparse junk games before panel QC at build."
)


def _artifact_paths() -> tuple[Path, Path, Path]:
    fig = PD22_MINUTES / f"{STEM}.png"
    meta = PD22_MINUTES / f"{STEM}.json"
    return fig, meta, AUTO_PD22_RAW_ROSTER_SIZE_BEFORE_QC_DECK


def _refresh_distribution(*, plot_only: bool) -> None:
    cmd = [sys.executable, str(DIST_SCRIPT), "--before-qc-only"]
    if plot_only:
        cmd.append("--plot-only")
    print(
        "Running before-QC roster size distribution ..."
        if not plot_only
        else "Refreshing before-QC roster size PNG ..."
    )
    subprocess.run(cmd, cwd=str(REPO), check=True)


def _max_outlier_bullet(meta: dict) -> str:
    csv_raw = PD22_MINUTES / (
        f"PD22_raw_roster_size_by_team_season_{SEASON_MIN}_{SEASON_MAX}_before_qc_raw.csv"
    )
    if not csv_raw.is_file():
        raw = meta.get("raw_team_season_summary") or {}
        return (
            rf"Tail: max = {m(int(raw.get('max', 0)))} player-seasons per team-season on legacy raw box "
            r"(ESPN dash placeholders still in panel)."
        )
    import pandas as pd

    top = pd.read_csv(csv_raw).nlargest(1, "roster_n").iloc[0]
    tid = int(top["team_id"])
    school = "BYU" if tid == 252 else rf"team\_id {tid}"
    return (
        rf"Tail: max = {m(int(top['roster_n']))} ({school} {m(int(top['season']))}); "
        rf"{m(115)} BYU spike from ESPN dash rows in one game (SCOUT Aug {m(2026)})."
    )


def _readout_bullets(meta: dict) -> list[str]:
    raw = meta.get("raw_team_season_summary") or {}
    filt = meta.get("filtered_team_season_summary") or {}
    seasons = meta.get("seasons", f"{SEASON_MIN}–{SEASON_MAX}")
    n_ts = int(raw.get("n", 0))
    share15 = 100.0 * float(raw.get("share_eq_15", 0))
    share_ge15 = 100.0 * float(raw.get("share_ge_15", 0))
    share_gt15 = 100.0 * float(raw.get("share_gt_15", 0))
    filt_share15 = 100.0 * float(filt.get("share_eq_15", 0))

    return [
        r"PD22 backup: players per team-season — legacy raw box (no QC) vs min-20 drop.",
        r"No box QC: dash-name placeholders and sparse team-seasons still in panel.",
        rf"Panel: {seasons} MBB · {m(n_ts)} team-seasons · {m(int(meta.get('player_seasons_raw', 0)))} player-season rows.",
        rf"Min={m(0)} raw box (blue): median = {m(float(raw.get('median', 0)), decimals=0)}, mean = {m(float(raw.get('mean', 0)), decimals=1)}; "
        rf"{mpct(share15)} exactly {m(NCAA_DRESS)}, {mpct(share_ge15)} {mgeq(NCAA_DRESS)}, "
        rf"{mpct(share_gt15)} {mgt(NCAA_DRESS)}.",
        rf"Min-{HERO_LOCK:g} drop (orange): median = {m(float(filt.get('median', 0)), decimals=0)}, "
        rf"mean = {m(float(filt.get('mean', 0)), decimals=1)}; only {mpct(filt_share15)} exactly {m(NCAA_DRESS)}.",
        _max_outlier_bullet(meta),
        r"Motivation for box QC at panel build — next slide shows after dash + min-games filters.",
        r"Left: team-season counts; right: normalized — long tail from junk box rows.",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build PD22 before-QC roster size AUTO slide.")
    parser.add_argument("--slides-only", action="store_true", help="Use existing PNG + JSON")
    parser.add_argument("--plot-only", action="store_true", help="Regenerate PNG from CSV/JSON")
    args = parser.parse_args()

    fig, meta_path, out_pptx = _artifact_paths()
    ensure_hero_dirs()

    if not args.slides_only:
        _refresh_distribution(plot_only=args.plot_only)

    meta = load_meta(meta_path)
    if not meta:
        raise SystemExit(f"Missing JSON: {meta_path}")
    if not fig.is_file():
        raise SystemExit(f"Missing figure: {fig}")

    raw = meta.get("raw_team_season_summary") or {}
    seasons = meta.get("seasons", f"{SEASON_MIN}–{SEASON_MAX}")
    subtitle = (
        rf"PD22 · roster size (before QC) · {seasons} · raw median = {m(float(raw.get('median', 0)), decimals=0)} · "
        rf"max = {m(int(raw.get('max', 0)))}"
    )

    build_figure_focus_slide(
        fig_path=fig,
        out_pptx=out_pptx,
        title=r"PD22 — Roster size: raw box (no QC) vs min-20 drop",
        subtitle=subtitle,
        bullets=_readout_bullets(meta),
        claim=CLAIM,
    )
    print(f"Wrote {out_pptx}")


if __name__ == "__main__":
    main()
