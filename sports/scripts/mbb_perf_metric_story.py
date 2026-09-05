#!/usr/bin/env python3
"""MBB perf metric story — reigning last-ps HERO by perf key (Q16 + EW16).

Each row: P(drafted) vs teammate poolq_LOO on that perf metric (excl. self).

Run (repo root):
  python sports/scripts/mbb_perf_metric_story.py
  python sports/scripts/mbb_perf_metric_story.py --no-footer --page-size letter
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "sports"))

from bdp_ai_tj_distributions import parse_bdp_spec  # noqa: E402
from bdp_reigning_loo_plots import _prepare_last_ps  # noqa: E402
from big_fish_data_story import DomainSpec, run_hero_porch  # noqa: E402
from build_perf_metric_mosaic import build_perf_metric_story_pages  # noqa: E402
from sports_pipeline.perf_metric import resolve_perf_metric  # noqa: E402
from sports_pipeline.y_draft_mode import PANEL_ROWS_LAST  # noqa: E402
from story_page_layout import PERF_PAGE_SIZE_CHOICES  # noqa: E402

SANDBOX = REPO / "3-Master_Plan" / "re_entry" / "HEROs_and_PASSes" / "sports_sandbox"
STORY_DIR = SANDBOX / "data_story"
PANEL_DIR = SANDBOX / "perf_story" / "panels"

BDP_SPEC_LABEL = "mg10 min20 09_21"
STORY_TITLE = "MBB — HERO by metric · P(drafted) vs teammate LOO"

MBB_METRIC_KEYS: tuple[str, ...] = (
    "ppm",
    "per",
    "bpm",
    "tspct",
    "ws",
    "minutes",
    "ws40",
    "obpm",
    "dbpm",
)
MBB_ROWS_PER_PAGE = 5

MBB_SHORT: dict[str, str] = {
    "ppm": "PPM",
    "per": "PER",
    "bpm": "BPM",
    "tspct": "TS%",
    "ws": "WS",
    "minutes": "minutes",
    "ws40": "WS/40",
    "obpm": "OBPM",
    "dbpm": "DBPM",
}

MBB_SPEC = DomainSpec(
    key="mbb",
    prefix="MBB",
    csv=REPO / "datasets/placeholder.csv",
    sandbox="sports_sandbox",
    title="MBB data story — reigning hero",
    subtitle="",
    reigning_tag="perm_loo_ever_lastps_ew16",
    ai_col="perf",
    loo_col="poolq_loo",
    y_col="Y_draft",
    pool_col="team_size",
    team_keys=("team_id", "season"),
    season_key="season",
    grain="NCAA MBB · last-ps · mg10 min20 09_21 · ALLT",
    y_pos_label="Drafted",
    y_neg_label="Not drafted",
    overlap_xlab=r"PPM $z$ within season",
    cohort_lines=(),
    panel_rows=PANEL_ROWS_LAST,
    athlete_id_col="athlete_id",
    tie_break_col="minutes",
)


def _paths() -> dict[str, Path]:
    return {
        "root": SANDBOX,
        "bdp": SANDBOX / "reigning_hero" / "basic_data_plots",
        "hero": SANDBOX / "hero",
        "act2": SANDBOX / "act2",
        "story": STORY_DIR,
        "perf": SANDBOX / "perf_story",
    }


def _load_metric_panel(metric_key: str) -> pd.DataFrame:
    resolve_perf_metric(metric_key)
    bdp = parse_bdp_spec(BDP_SPEC_LABEL)
    panel = _prepare_last_ps(bdp, metric_key)
    return panel.dropna(subset=["poolq_loo", "Y_draft"]).copy()


def _run_metric_panels(metric_key: str, paths: dict[str, Path]) -> dict[str, Any]:
    work = _load_metric_panel(metric_key)
    short = MBB_SHORT.get(metric_key, metric_key)
    panel_dir = PANEL_DIR
    panel_dir.mkdir(parents=True, exist_ok=True)
    compact = (6.4, 3.6)
    metric_rows: dict[str, Any] = {
        "metric_key": metric_key,
        "col": metric_key,
        "short": short,
        "n": len(work),
    }
    for mode in ("quantile", "equal_width"):
        is_ew = mode == "equal_width"
        tag = "ew16" if is_ew else "q16"
        bin_tag = "EW16" if is_ew else "Q16"
        x_label = f"Teammate LOO · {short} ({bin_tag})"
        out = run_hero_porch(
            work,
            MBB_SPEC,
            paths,
            x_col="poolq_loo",
            x_label=x_label,
            slug=f"perf_{tag}_loo_{metric_key}",
            binning=mode,
            out_dir=panel_dir,
            figsize=compact,
        )
        metric_rows[f"{tag}_png"] = str(out.relative_to(REPO))
    return metric_rows


def main() -> None:
    parser = argparse.ArgumentParser(description="MBB perf metric story mosaic")
    parser.add_argument(
        "--no-footer",
        action="store_true",
        help="Omit bottom-left footer (better for Preview/print on letter paper)",
    )
    parser.add_argument(
        "--page-size",
        choices=PERF_PAGE_SIZE_CHOICES,
        default="screen",
        help="STORY layout: letter (8.5×11), tabloid (11×17), or screen (default deck)",
    )
    args = parser.parse_args()
    show_footer = not args.no_footer
    page_size = args.page_size

    STORY_DIR.mkdir(parents=True, exist_ok=True)
    PANEL_DIR.mkdir(parents=True, exist_ok=True)
    paths = _paths()

    rows: list[dict[str, Any]] = []
    for metric_key in MBB_METRIC_KEYS:
        print(json.dumps({"metric": metric_key}))
        rows.append(_run_metric_panels(metric_key, paths))

    panel0 = _load_metric_panel("ppm")
    n_rows = len(panel0)
    y_rate = float(panel0["Y_draft"].mean()) if n_rows else 0.0

    built_pages = build_perf_metric_story_pages(
        rows,
        STORY_DIR,
        "MBB_PERF_METRIC_STORY",
        suptitle=STORY_TITLE,
        repo=REPO,
        show_footer=show_footer,
        page_size=page_size,
        footer_tag="MBB perf metric story · mbb_perf_metric_story.py",
        rows_per_page=MBB_ROWS_PER_PAGE,
    )

    manifest = {
        "domain": "mbb",
        "deck": "perf_metric_story",
        "bdp_spec": BDP_SPEC_LABEL,
        "title": STORY_TITLE,
        "show_footer": show_footer,
        "page_size": page_size,
        "rows_per_page": MBB_ROWS_PER_PAGE,
        "n": n_rows,
        "draft_rate": y_rate,
        "output_png": str(built_pages[0].relative_to(REPO)),
        "output_pages": [str(p.relative_to(REPO)) for p in built_pages],
        "panels_dir": str(PANEL_DIR.relative_to(REPO)),
        "metrics": rows,
    }
    manifest_path = STORY_DIR / "mbb_perf_metric_story_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {manifest_path.relative_to(REPO)}")
    for p in built_pages:
        print(f"Wrote {p.relative_to(REPO)}")


if __name__ == "__main__":
    main()
