#!/usr/bin/env python3
"""Tenure perf metric story — decision cohort HERO by pub-metric LOO.

Page 1: Q16 + EW16 (16 bins) · Page 2: Q10 + EW10 (10 bins).

Run (repo root):
  python tenure/scripts/tenure_perf_metric_story.py
  python tenure/scripts/tenure_perf_metric_story.py --no-footer --page-size letter
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
TENURE_PIPELINE = REPO / "tenure" / "tenure_pipeline"
DEFAULT_IN = TENURE_PIPELINE / "faculty_panel_with_pools.jsonl"
DEFAULT_CAREER = TENURE_PIPELINE / "author_year_career_master.jsonl"
SANDBOX = REPO / "3-Master_Plan" / "re_entry" / "HEROs_and_PASSes" / "tenure_sandbox"
STORY_DIR = SANDBOX / "data_story"
PERF_DIR = SANDBOX / "perf_story"
PANEL_DIR = PERF_DIR / "panels"

sys.path.insert(0, str(TENURE_PIPELINE))
sys.path.insert(0, str(REPO / "sports" / "scripts"))
from build_perf_metric_mosaic import (  # noqa: E402
    build_perf_metric_mosaic,
    build_perf_metric_story_pages,
)
from story_page_layout import PERF_PAGE_SIZE_CHOICES  # noqa: E402
from decision_hero_prep import DECISION_LOO_METRICS, prepare_decision_loo_persons  # noqa: E402
from stage9_analysis import build_inverted_u  # noqa: E402

SCRIPTS_DIR = REPO / "tenure" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
from tenure_grain_labels import DECISION  # noqa: E402
from tenure_hero_slide_plot import build_hero_slide_panel  # noqa: E402

STORY_TITLE = "Tenure — HERO by metric · P(tenure) vs dept LOO"

# (bin_method, file tag, n_bins)
BIN_PAGE_16: tuple[tuple[str, str, int], ...] = (
    ("quantile", "q16", 16),
    ("equal_width", "ew16", 16),
)
BIN_PAGE_10: tuple[tuple[str, str, int], ...] = (
    ("quantile", "q10", 10),
    ("equal_width", "ew10", 10),
)


def _x_label(short: str, bin_tag: str) -> str:
    return f"Dept LOO · {short} ({bin_tag})"


def _mosaic_rows(
    metric_rows: list[dict[str, Any]],
    *,
    q_tag: str = "q16",
    ew_tag: str = "ew16",
) -> list[dict[str, str]]:
    """Map metric panel paths to compositor keys (q16_png / ew16_png)."""
    return [
        {"q16_png": row[f"{q_tag}_png"], "ew16_png": row[f"{ew_tag}_png"]}
        for row in metric_rows
    ]


def _run_metric_panels(
    panel_path: Path,
    career_path: Path,
    metric_key: str,
    short: str,
    persons: list[dict[str, Any]],
    prep_stats: dict[str, Any],
    bin_configs: tuple[tuple[str, str, int], ...],
) -> dict[str, Any]:
    work_dir = PANEL_DIR / f"_scratch_{metric_key}"
    work_dir.mkdir(parents=True, exist_ok=True)
    metric_rows: dict[str, Any] = {
        "metric_key": metric_key,
        "short": short,
        "n": len(persons),
        "prep_stats": prep_stats,
    }

    for bin_method, tag, n_bins in bin_configs:
        bin_tag = tag.upper()
        result = build_inverted_u(
            panel_path,
            work_dir,
            n_bins=n_bins,
            exclude_censored=True,
            bin_method=bin_method,
            x_metric="decision_loo",
            window=DECISION,
            stat="mean",
            persons=persons,
        )
        base = f"HERO_tenure_perf_{tag}_loo_{metric_key}"
        csv_src = work_dir / "stage9_binned_table.csv"
        slide_path = PANEL_DIR / f"{base}_slide.png"
        csv_path = PANEL_DIR / f"{base}_binned.csv"
        shutil.copy2(csv_src, csv_path)
        build_hero_slide_panel(
            csv_path,
            slide_path,
            persons=persons,
            n_bins=n_bins,
            bin_method=bin_method,
            x_metric="decision_loo",
            window=DECISION,
            stat="mean",
            stage9_summary=result,
            x_axis_label=_x_label(short, bin_tag),
            metric_key=metric_key,
            metric_short=short,
        )
        metric_rows[f"{tag}_png"] = str(slide_path.relative_to(REPO))
        metric_rows[f"{tag}_csv"] = str(csv_path.relative_to(REPO))
        print(f"Wrote {slide_path.relative_to(REPO)}")

    return metric_rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Tenure perf metric story mosaic")
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

    if not DEFAULT_IN.is_file():
        raise SystemExit(f"Missing panel: {DEFAULT_IN}")
    if not DEFAULT_CAREER.is_file():
        raise SystemExit(f"Missing career master: {DEFAULT_CAREER}")

    STORY_DIR.mkdir(parents=True, exist_ok=True)
    PANEL_DIR.mkdir(parents=True, exist_ok=True)

    rows_16: list[dict[str, Any]] = []
    rows_10: list[dict[str, Any]] = []
    for metric_key, short, _field in DECISION_LOO_METRICS:
        print(json.dumps({"metric": metric_key, "short": short}))
        persons, prep_stats = prepare_decision_loo_persons(
            DEFAULT_IN, DEFAULT_CAREER, metric_key
        )
        if not persons:
            raise SystemExit(f"No persons for metric {metric_key!r}")
        rows_16.append(
            _run_metric_panels(
                DEFAULT_IN,
                DEFAULT_CAREER,
                metric_key,
                short,
                persons,
                prep_stats,
                BIN_PAGE_16,
            )
        )
        rows_10.append(
            _run_metric_panels(
                DEFAULT_IN,
                DEFAULT_CAREER,
                metric_key,
                short,
                persons,
                prep_stats,
                BIN_PAGE_10,
            )
        )

    persons0, stats0 = prepare_decision_loo_persons(DEFAULT_IN, DEFAULT_CAREER, "career_rate")
    n_cohort = len(persons0)
    y_rate = sum(p["tenure"] for p in persons0) / n_cohort if n_cohort else 0.0

    footer_tag = "TENURE perf metric story · tenure_perf_metric_story.py"

    built_p1 = build_perf_metric_story_pages(
        _mosaic_rows(rows_16),
        STORY_DIR,
        "TENURE_PERF_METRIC_STORY",
        suptitle=f"{STORY_TITLE} · 16-bin",
        repo=REPO,
        show_footer=show_footer,
        page_size=page_size,
        footer_tag=footer_tag,
    )

    built_p2 = build_perf_metric_mosaic(
        _mosaic_rows(rows_10, q_tag="q10", ew_tag="ew10"),
        STORY_DIR / "TENURE_PERF_METRIC_STORY_p2.png",
        suptitle=f"{STORY_TITLE} · 10-bin",
        repo=REPO,
        show_footer=show_footer,
        page_size=page_size,
        footer_tag=footer_tag,
    )

    built_pages = [*built_p1, built_p2]

    manifest = {
        "domain": "tenure",
        "deck": "perf_metric_story",
        "cohort": "decision_pd29",
        "title": STORY_TITLE,
        "show_footer": show_footer,
        "page_size": page_size,
        "n": n_cohort,
        "tenure_rate": y_rate,
        "output_png": str(built_pages[0].relative_to(REPO)),
        "output_pages": [str(p.relative_to(REPO)) for p in built_pages],
        "panels_dir": str(PANEL_DIR.relative_to(REPO)),
        "metrics_16bin": rows_16,
        "metrics_10bin": rows_10,
        "metrics": rows_16,
        "prep_stats_career_rate": stats0,
    }
    manifest_path = STORY_DIR / "tenure_perf_metric_story_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {manifest_path.relative_to(REPO)}")
    for p in built_pages:
        print(f"Wrote {p.relative_to(REPO)}")


if __name__ == "__main__":
    main()
