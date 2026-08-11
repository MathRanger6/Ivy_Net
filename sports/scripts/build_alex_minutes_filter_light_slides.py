#!/usr/bin/env python3
"""Light AUTO slides for Alex — min_minutes filter & roster-size issue.

Slides-only (uses existing PNGs in grandchild_assign/). No diagnostic rerun.

Run (repo root):
  python sports/scripts/build_alex_minutes_filter_light_slides.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import GRANDCHILD_ASSIGN, SLIDES_AUTO, ensure_hero_dirs
from pd17_interval_overlap_slide import build_interval_overlap_slide, load_meta

ASSIGN = GRANDCHILD_ASSIGN
SENS_META = ASSIGN / "HERO_min_minutes_sensitivity_2011_2021_meta.json"
ROSTER_META = ASSIGN / "GRANDCHILD_ncaa_roster_size_distribution_2011_2021_meta.json"

FIG_COMPARE = ASSIGN / "HERO_min_minutes_sensitivity_compare_2011_2021.png"
FIG_OVERLAY = ASSIGN / "HERO_min_minutes_sensitivity_overlay_2011_2021.png"
FIG_ROSTER = ASSIGN / "GRANDCHILD_ncaa_roster_size_distribution_2011_2021.png"

OUT_COMPARE = SLIDES_AUTO / "CHAR_hero_min_minutes_sensitivity_compare_AUTO.pptx"
OUT_OVERLAY = SLIDES_AUTO / "CHAR_hero_min_minutes_sensitivity_overlay_AUTO.pptx"
OUT_ROSTER = SLIDES_AUTO / "CHAR_ncaa_roster_size_distribution_AUTO.pptx"


def _run_row(meta: dict, mm: float) -> dict | None:
    for row in meta.get("runs", []):
        if float(row.get("min_minutes", -1)) == float(mm):
            return row
    return None


def _sensitivity_bullets(meta: dict, *, overlay: bool) -> list[str]:
    seasons = meta.get("seasons", "2011-2021")
    bullets = [
        rf"Hero x-axis: draft rate vs poolq_loo ventiles · MBB {seasons} · 16 quantile.",
        r"min\_minutes defines who enters the panel and LOO peer pool — not neutral QC.",
    ]
    for mm in meta.get("floors_run", []):
        row = _run_row(meta, mm)
        if not row:
            continue
        curv = row.get("curvature", {})
        bullets.append(
            rf"min={mm:g}: $n={row['n_player_seasons']:,}$, drafted={row['n_drafted']:,}, "
            rf"bin16={100 * curv.get('bin16_rate', 0):.2f}\%, {curv.get('shape', '?')}."
        )
    if overlay:
        bullets.append(r"Overlay: same estimand, different playing-time floors.")
    else:
        bullets.append(r"Hero lock: min=20 — cleanest top-ventile cliff; min=10 robust appendix.")
    bullets.append(r"We are not simulating minutes in LG.")
    return bullets


def _roster_bullets(meta: dict) -> list[str]:
    s = meta.get("team_season_summary", {})
    c = meta.get("lg_roster_size_reference", 15)
    return [
        r"Qualifying players per real NCAA team-season (\geq 20 ESPN minutes).",
        rf"$n={s.get('n', 0):,}$ team-seasons · mean={s.get('mean', 0):.1f} · "
        rf"median={s.get('median', 0):.0f} · sd={s.get('std', 0):.1f}.",
        rf"Red dotted = NCAA mean; orange dashed = LG fixed $C={c:g}$.",
        rf"Only {100 * s.get('share_eq_15', 0):.1f}\% of teams have exactly {c:g} qualifying players.",
        r"Same ability pool ~62k; LG repacks into J=N/15 synthetic 15-man leagues.",
        r"Minutes floor shapes peer count — state explicitly in methods.",
    ]


def main() -> None:
    ensure_hero_dirs()
    sens = load_meta(SENS_META)
    roster = load_meta(ROSTER_META)
    seasons = sens.get("seasons", "2011-2021")

    build_interval_overlap_slide(
        fig_path=FIG_COMPARE,
        out_pptx=OUT_COMPARE,
        title=r"Hero sensitivity — min\_minutes ladder",
        subtitle=rf"MBB {seasons} · poolq\_loo ventiles · 0 / 10 / 20 min",
        bullets=_sensitivity_bullets(sens, overlay=False),
        claim=(
            "Talking point: inverted-U survives 10- and 20-minute floors; "
            "min=20 sharpens the elite ventile dip (+2 drafted vs min=0)."
        ),
    )
    print(f"Wrote {OUT_COMPARE}")

    build_interval_overlap_slide(
        fig_path=FIG_OVERLAY,
        out_pptx=OUT_OVERLAY,
        title=r"Hero sensitivity — min\_minutes overlay",
        subtitle=rf"MBB {seasons} · same bins, three floors",
        bullets=_sensitivity_bullets(sens, overlay=True),
        claim="Talking point: pattern is not an artifact of one arbitrary cutoff.",
    )
    print(f"Wrote {OUT_OVERLAY}")

    s = roster.get("team_season_summary", {})
    build_interval_overlap_slide(
        fig_path=FIG_ROSTER,
        out_pptx=OUT_ROSTER,
        title=r"NCAA roster sizes after the minutes filter",
        subtitle=rf"MBB {seasons} · min 20 min · mean={s.get('mean', 0):.1f} vs LG $C=15$",
        bullets=_roster_bullets(roster),
        claim=(
            "Talking point: empirical teams are ~10 rotation players; "
            "LG uses fixed 15 — comparability is distributional, not headcount."
        ),
    )
    print(f"Wrote {OUT_ROSTER}")


if __name__ == "__main__":
    main()
