#!/usr/bin/env python3
"""Build PD22 roster-size AFTER box QC AUTO slide (backup).

Run (repo root):
  python sports/scripts/build_pd22_raw_roster_size_after_qc_slide.py --slides-only
  python sports/scripts/build_pd22_raw_roster_size_after_qc_slide.py

Output:
  slides/auto/CHAR_PD22_raw_roster_size_distribution_after_qc_AUTO.pptx

Copy into HAND after the before-QC roster slide: Change Picture + bullets from AUTO deck.
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
    AUTO_PD22_RAW_ROSTER_SIZE_AFTER_QC_DECK,
    PD22_MINUTES,
    ensure_hero_dirs,
)
from pd17_interval_overlap_slide import build_figure_focus_slide, load_meta
from pd22_slide_common import BOX_QC_PANEL_NOTE, m, mgeq, mgt, mpct

from pd20_22_campaign_window import (
    activate_from_args,
    add_window_args,
    auto_deck_path,
    current_window,
    window_cli_flags,
)


def _w():
    return current_window()

DIST_SCRIPT = SCRIPTS / "pd22_raw_roster_size_distribution.py"
HERO_LOCK = 20.0
NCAA_DRESS = 15


def _stem() -> str:
    return f"PD22_raw_roster_size_distribution_{_w().tag}_after_qc"

CLAIM = (
    rf"Claim (PD22 backup): After box QC, team-season roster counts cluster near NCAA dress cap {m(NCAA_DRESS)}; "
    rf"empirical hero caps (min {mgeq(HERO_LOCK)}) count rotation-minute contributors — not game-day dress lists."
)


def _artifact_paths() -> tuple[Path, Path, Path]:
    fig = PD22_MINUTES / f"{_stem()}.png"
    meta = PD22_MINUTES / f"{_stem()}.json"
    return fig, meta, auto_deck_path(AUTO_PD22_RAW_ROSTER_SIZE_AFTER_QC_DECK)


def _refresh_distribution(*, plot_only: bool) -> None:
    cmd = [sys.executable, str(DIST_SCRIPT), "--after-qc-only"]
    if plot_only:
        cmd.append("--plot-only")
    cmd.extend(window_cli_flags())
    print(
        "Running after-QC roster size distribution ..."
        if not plot_only
        else "Refreshing after-QC roster size PNG ..."
    )
    subprocess.run(cmd, cwd=str(REPO), check=True)


def _max_outlier_bullet(meta: dict) -> str:
    csv_raw = PD22_MINUTES / (
        f"PD22_raw_roster_size_by_team_season_{_w().tag}_after_qc_raw.csv"
    )
    if not csv_raw.is_file():
        raw = meta.get("raw_team_season_summary") or {}
        return (
            rf"Tail: max = {m(int(raw.get('max', 0)))} player-seasons per team-season after box QC "
            r"(ESPN dash placeholders removed at panel build)."
        )
    import pandas as pd

    top = pd.read_csv(csv_raw).nlargest(1, "roster_n").iloc[0]
    tid = int(top["team_id"])
    school = "BYU" if tid == 252 else rf"team\_id {tid}"
    return (
        rf"Tail: max = {m(int(top['roster_n']))} ({school} {m(int(top['season']))}); "
        rf"{m(115)} BYU spike gone — dash rows dropped at panel build (SCOUT Aug {m(2026)})."
    )


def _readout_bullets(meta: dict) -> list[str]:
    raw = meta.get("raw_team_season_summary") or {}
    filt = meta.get("filtered_team_season_summary") or {}
    seasons = meta.get("seasons", f"{_w().season_min}–{_w().season_max}")
    n_ts = int(raw.get("n", 0))
    share15 = 100.0 * float(raw.get("share_eq_15", 0))
    share_ge15 = 100.0 * float(raw.get("share_ge_15", 0))
    share_gt15 = 100.0 * float(raw.get("share_gt_15", 0))
    filt_share15 = 100.0 * float(filt.get("share_eq_15", 0))

    return [
        r"PD22 backup: players per team-season — box-QC panel (min\_minutes=0) vs min-20 drop.",
        BOX_QC_PANEL_NOTE,
        rf"Panel: {seasons} MBB · {m(n_ts)} team-seasons · {m(int(meta.get('player_seasons_raw', 0)))} player-season rows.",
        rf"Min={m(0)} after QC (blue): median = {m(float(raw.get('median', 0)), decimals=0)}, mean = {m(float(raw.get('mean', 0)), decimals=1)}; "
        rf"{mpct(share15)} exactly {m(NCAA_DRESS)}, {mpct(share_ge15)} {mgeq(NCAA_DRESS)}, "
        rf"{mpct(share_gt15)} {mgt(NCAA_DRESS)}.",
        rf"Min-{HERO_LOCK:g} drop (orange): median = {m(float(filt.get('median', 0)), decimals=0)}, "
        rf"mean = {m(float(filt.get('mean', 0)), decimals=1)}; only {mpct(filt_share15)} exactly {m(NCAA_DRESS)} — "
        r"rotation-minute survivors, not dress cap.",
        _max_outlier_bullet(meta),
        rf"Red dashed = NCAA dress cap {m(NCAA_DRESS)}; empirical caps in PD21 use min-{HERO_LOCK:g} multiset.",
        rf"Left: team-season counts; right: normalized — bulk mass sits {m(14)}–{m(17)} after box QC.",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build PD22 after-QC roster size AUTO slide.")
    parser.add_argument("--slides-only", action="store_true", help="Use existing PNG + JSON")
    parser.add_argument("--plot-only", action="store_true", help="Regenerate PNG from CSV/JSON")
    add_window_args(parser)
    args = parser.parse_args()
    activate_from_args(args)

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
    seasons = meta.get("seasons", f"{_w().season_min}–{_w().season_max}")
    subtitle = (
        rf"PD22 · roster size (after QC) · {seasons} · raw median = {m(float(raw.get('median', 0)), decimals=0)} · "
        rf"{mpct(100 * float(raw.get('share_eq_15', 0)))} exactly {m(NCAA_DRESS)}"
    )

    build_figure_focus_slide(
        fig_path=fig,
        out_pptx=out_pptx,
        title=r"PD22 — Roster size: box-QC panel (min=0) vs min-20 drop",
        subtitle=subtitle,
        bullets=_readout_bullets(meta),
        claim=CLAIM,
    )
    print(f"Wrote {out_pptx}")


if __name__ == "__main__":
    main()
