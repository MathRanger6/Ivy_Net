#!/usr/bin/env python3
"""Build PD22 item 1 drafted-minutes audit AUTO slide.

Run (repo root):
  python sports/scripts/build_pd22_drafted_minutes_audit_slide.py --slides-only
  python sports/scripts/build_pd22_drafted_minutes_audit_slide.py

Output:
  slides/auto/CHAR_PD22_drafted_minutes_audit_AUTO.pptx

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

from hero_gallery_paths import AUTO_PD22_DRAFTED_MINUTES_DECK, PD22_MINUTES, ensure_hero_dirs
from pd17_interval_overlap_slide import build_figure_focus_slide, load_meta
from pd22_slide_common import BOX_QC_PANEL_NOTE, m, mapprox, mfrac

from pd20_22_campaign_window import (
    activate_from_args,
    add_window_args,
    auto_deck_path,
    current_window,
    window_cli_flags,
)


def _w():
    return current_window()


STEM_PREFIX = "PD22_drafted_minutes_audit"


def _stem() -> str:
    return f"{STEM_PREFIX}_{_w().tag}"

AUDIT_SCRIPT = SCRIPTS / "pd22_drafted_minutes_audit.py"

CLAIM = (
    r"Claim (PD22): Playing-time floor must be draft-safe — retain every "
    r"ever-draft ($Y_{\mathrm{draft}}=1$) player-season before we justify min 20 min "
    r"or PPM-zero bench policy for $\rho$ / $H_{\mathrm{sort}}$ calibration."
)


def _artifact_paths() -> tuple[Path, Path, Path]:
    fig = PD22_MINUTES / f"{_stem()}.png"
    meta = PD22_MINUTES / f"{_stem()}.json"
    return fig, meta, auto_deck_path(AUTO_PD22_DRAFTED_MINUTES_DECK)


def _refresh_audit(*, plot_only: bool) -> None:
    cmd = [sys.executable, str(AUDIT_SCRIPT)]
    if plot_only:
        cmd.append("--plot-only")
    cmd.extend(window_cli_flags())
    print("Running drafted-minutes audit ..." if not plot_only else "Refreshing audit PNG ...")
    subprocess.run(cmd, cwd=str(REPO), check=True)


def _format_lost_rows(meta: dict, limit: int = 3) -> str:
    lost = meta.get("summary", {}).get("n_lost_player_season_ids_at_20") or []
    if not lost:
        return r"At min 20 drop: zero drafted player-seasons lost."
    parts = []
    for row in lost[:limit]:
        parts.append(
            rf"id {row['athlete_id']} ({int(row['season'])}): {float(row['minutes']):.1f} min"
        )
    tail = "" if len(lost) <= limit else rf" (+{len(lost) - limit} more — see CSV)"
    return rf"Lost at min {m(20)} drop ({m(len(lost))}): " + "; ".join(parts) + tail


def _readout_bullets(meta: dict) -> list[str]:
    s = meta.get("summary") or {}
    n_all = int(s.get("n_drafted_player_seasons", 0))
    n_ret = int(s.get("n_retained_at_hero_lock_drop", n_all))
    n_lost = int(s.get("n_lost_at_hero_lock_drop", 0))
    n_unique_lost = int(s.get("n_unique_lost_at_hero_lock_drop", n_lost))
    n_zero = int(s.get("n_lost_zero_minutes_at_hero_lock_drop", 0))
    min_m = s.get("min_minutes_among_drafted")
    safe = s.get("draft_safe_max_floor_drop")
    min_line = m(float(min_m)) if min_m is not None else r"$?$"
    safe_line = mapprox(float(safe)) if safe is not None else r"$?$"
    seasons = meta.get("seasons", f"{_w().season_min}–{_w().season_max}")

    return [
        r"PD22 item 1: audit minutes floor before defending min 20 min "
        r"or PPM-zero bench policy.",
        rf"Panel: {seasons} MBB · rebuild min\_minutes=0 after box QC · "
        rf"$Y_{{\mathrm{{draft}}}}$ = ever-draft flag (not season-specific).",
        BOX_QC_PANEL_NOTE,
        rf"Drafted player-seasons: {m(n_all)} ({m(int(s.get('n_unique_drafted_athletes', 0)))} unique athletes).",
        rf"Minutes among drafted: min = {min_line}; draft-safe max floor (drop) {safe_line} min.",
        rf"Hero lock min = {m(20)}: retain {mfrac(n_ret, n_all)}; lose {m(n_lost)} player-seasons "
        rf"({m(n_unique_lost)} unique athletes; {m(n_zero)} at {m(0)} min).",
        r"Right panel: red labels = drafted player-seasons lost vs min\_minutes=0 floor at each threshold.",
        r"PPM-zero policy: all drafted rows retained; sub-floor players get raw PPM = 0 before z-score.",
        _format_lost_rows(meta),
        rf"Left: empirical cumulative distribution function (ECDF) of drafted minutes ({m(10)} min teal, {m(20)} min red). "
        r"Right: retained count vs floor.",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build PD22 drafted-minutes audit AUTO slide.")
    parser.add_argument(
        "--slides-only",
        action="store_true",
        help="Use existing PNG + JSON (no audit rerun)",
    )
    parser.add_argument(
        "--plot-only",
        action="store_true",
        help="Regenerate PNG from CSV only, then build slide",
    )
    add_window_args(parser)
    args = parser.parse_args()
    activate_from_args(args)

    fig, meta_path, out_pptx = _artifact_paths()
    ensure_hero_dirs()

    if not args.slides_only:
        _refresh_audit(plot_only=args.plot_only)

    meta = load_meta(meta_path)
    if not meta:
        raise SystemExit(f"Missing audit JSON: {meta_path}")
    if not fig.is_file():
        raise SystemExit(f"Missing figure: {fig}")

    s = meta.get("summary") or {}
    n_lost = int(s.get("n_lost_at_hero_lock_drop", 0))
    n_all = int(s.get("n_drafted_player_seasons", 0))
    seasons = meta.get("seasons", f"{_w().season_min}–{_w().season_max}")

    subtitle = (
        rf"PD22 · drafted retention audit · {seasons} · "
        rf"at min {m(20)} drop: {mfrac(n_all - n_lost, n_all)} drafted player-seasons kept"
    )

    build_figure_focus_slide(
        fig_path=fig,
        out_pptx=out_pptx,
        title=r"PD22 — Drafted-player retention vs playing-time floor",
        subtitle=subtitle,
        bullets=_readout_bullets(meta),
        claim=CLAIM,
    )
    print(f"Wrote {out_pptx}")


if __name__ == "__main__":
    main()
