#!/usr/bin/env python3
"""Build PD22 PPM full-panel vs sub-20 overlay AUTO slide.

Run (repo root):
  python sports/scripts/build_pd22_ppm_full_vs_filtered_slide.py --slides-only
  python sports/scripts/build_pd22_ppm_full_vs_filtered_slide.py --plot-only
  python sports/scripts/build_pd22_ppm_full_vs_filtered_slide.py

Output:
  slides/auto/CHAR_PD22_ppm_full_vs_filtered_AUTO.pptx

Copy into HAND: Change Picture + bullets from AUTO deck.
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
    AUTO_PD22_PPM_OVERLAY_DECK,
    GRANDCHILD_ASSIGN,
    PD22_MINUTES,
    ensure_hero_dirs,
)
from pd17_interval_overlap_slide import build_figure_focus_slide, load_meta
from pd22_slide_common import BOX_QC_PANEL_NOTE, m, mapprox, mn, mn_approx, mgeq, mgt, mpct

PPM_SCRIPT = SCRIPTS / "pd22_ppm_distribution.py"
SEASON_MIN = 2011
SEASON_MAX = 2021
OVERLAY_STEM = f"PD22_ppm_full_vs_filtered_{SEASON_MIN}_{SEASON_MAX}"
HERO_LOCK = 20.0

ROSTER_META = GRANDCHILD_ASSIGN / "GRANDCHILD_ncaa_roster_size_distribution_2011_2021_meta.json"
MINUTES_META = PD22_MINUTES / f"PD22_raw_minutes_distribution_{SEASON_MIN}_{SEASON_MAX}.json"
PPM_META = PD22_MINUTES / f"PD22_ppm_distribution_{SEASON_MIN}_{SEASON_MAX}.json"

def _claim(ps: dict) -> str:
    n_gt1 = int(ps.get("n_filtered_out_ppm_gt_1", 0))
    ppm_max = float(ps.get("filtered_out_ppm_max", 6))
    return (
        rf"Claim (PD22): Sub-{HERO_LOCK:g}-min rows add PPM noise ({m(n_gt1)} with PPM {mgt(1)}, "
        rf"max {m(ppm_max, decimals=2 if ppm_max < 10 else 0)}) on top of a "
        r"rotation-player cloud — minutes floor cleans ability before hero / ASSIGN; "
        rf"empirical roster caps count season contributors, not NCAA dress-out {m(15)}."
    )

def _artifact_paths() -> tuple[Path, Path]:
    fig = PD22_MINUTES / f"{OVERLAY_STEM}.png"
    return fig, AUTO_PD22_PPM_OVERLAY_DECK


def _refresh_overlay(*, plot_only: bool) -> None:
    cmd = [sys.executable, str(PPM_SCRIPT)]
    if plot_only:
        cmd.append("--plot-only")
    print("Refreshing overlay PNG ..." if plot_only else "Running PPM diagnostic ...")
    subprocess.run(cmd, cwd=str(REPO), check=True)


def _roster_bullet() -> str:
    rm = load_meta(ROSTER_META)
    ts = (rm.get("team_season_summary") or {}) if rm else {}
    if not ts:
        return (
            r"Empirical roster caps: players per team-season on min-20 hero panel "
            r"(not NCAA game-day dress list)."
        )
    mean = float(ts.get("mean", 0))
    med = float(ts.get("median", 0))
    p25 = float(ts.get("p25", 0))
    p75 = float(ts.get("p75", 0))
    share15 = 100.0 * float(ts.get("share_eq_15", 0))
    return (
        rf"Empirical caps (min {mgeq(HERO_LOCK)} panel): mean {m(mean, decimals=1)} / median {m(med, decimals=0)} "
        rf"players per team-season (p25={m(p25, decimals=0)}, p75={m(p75, decimals=0)}); only {mpct(share15)} "
        rf"exactly {m(15)} — rotation-minute count, not who dressed for a game."
    )


def _readout_bullets(ppm: dict, minutes: dict) -> list[str]:
    ps = ppm.get("summary") or {}
    ms = minutes.get("summary") or {}
    seasons = ppm.get("seasons") or minutes.get("seasons") or f"{SEASON_MIN}–{SEASON_MAX}"
    n_full = int(ps.get("n_hero_panel", 0)) + int(ps.get("n_filtered_out_positive_minutes", 0))
    n_sub = int(ps.get("n_filtered_out_positive_minutes", 0))

    bullets = [
        r"PD22 overlay: gray = box-QC panel raw PPM (minutes $> 0$); blue = sub-20-min tail removed by drop policy.",
        BOX_QC_PANEL_NOTE,
        rf"Panel: {seasons} MBB · gray {mn_approx(n_full)} · blue {mn(n_sub)} · "
        rf"{m(int(ps.get('n_filtered_out_zero_minutes', 0)))} zero-min rows excluded (PPM undefined).",
        rf"Sub-{HERO_LOCK:g} PPM {mgt(1.0)}: {m(int(ps.get('n_filtered_out_ppm_gt_1', 0)))}; "
        rf"max {m(float(ps.get('filtered_out_ppm_max', 0)), decimals=2)}; "
        rf"sub-{HERO_LOCK:g} median PPM (positive min) = "
        rf"{m(float(ps.get('filtered_out_ppm_median_positive_min', 0)), decimals=3)}.",
        rf"After min-{HERO_LOCK:g} drop: hero panel {mn(int(ps.get('n_hero_panel', 0)))}; "
        rf"raw PPM median = {m(float(ps.get('hero_raw_ppm_median', 0)), decimals=3)} "
        rf"(p99 = {m(float(ps.get('hero_raw_ppm_p99', 0)), decimals=2)}).",
        rf"Minutes context (box-QC panel): {mpct(float(ms.get('pct_below_20', 0)))} below {m(HERO_LOCK, decimals=0)} min; "
        rf"median = {m(float(ms.get('minutes_median', 0)), decimals=0)} min (all) vs "
        rf"{m(float(ms.get('drafted_minutes_median', 0)), decimals=0)} min (ever-draft).",
        _roster_bullet(),
        rf"NCAA dress cap {mapprox(15)} per game $\neq$ our cap multiset — box panel counts season rows passing the minutes rule.",
    ]
    return [b for b in bullets if b]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build PD22 PPM overlay AUTO slide.")
    parser.add_argument("--slides-only", action="store_true", help="Use existing PNG + JSON")
    parser.add_argument("--plot-only", action="store_true", help="Regenerate overlay PNG only")
    args = parser.parse_args()

    fig, out_pptx = _artifact_paths()
    ensure_hero_dirs()

    if not args.slides_only:
        _refresh_overlay(plot_only=args.plot_only)

    if not fig.is_file():
        raise SystemExit(f"Missing figure: {fig}")

    ppm_meta = load_meta(PPM_META)
    minutes_meta = load_meta(MINUTES_META)
    if not ppm_meta:
        raise SystemExit(f"Missing PPM JSON: {PPM_META}")

    ps = ppm_meta.get("summary") or {}
    seasons = ppm_meta.get("seasons", f"{SEASON_MIN}–{SEASON_MAX}")
    subtitle = (
        rf"PD22 · PPM overlay · {seasons} · "
        rf"{m(int(ps.get('n_filtered_out_ppm_gt_1', 0)))} sub-{HERO_LOCK:g}-min rows with PPM {mgt(1)}"
    )

    build_figure_focus_slide(
        fig_path=fig,
        out_pptx=out_pptx,
        title=r"PD22 — Raw PPM: full panel vs sub-20-min filtered tail",
        subtitle=subtitle,
        bullets=_readout_bullets(ppm_meta, minutes_meta or {}),
        claim=_claim(ps),
    )
    print(f"Wrote {out_pptx}")


if __name__ == "__main__":
    main()
