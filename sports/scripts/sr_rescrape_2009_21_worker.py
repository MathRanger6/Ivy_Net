#!/usr/bin/env python3
"""Background worker: SR re-scrape 2009–2021 + re-match. Log to datasets/mbb/sr_rescrape_2009_21.log"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "sports"))

from sports_pipeline.config import PipelineConfig
from sports_pipeline import panel_rebuild, bpm_merge, scrape_bpm


def main() -> None:
    print("=== SR rescrape worker started ===", flush=True)
    cfg = PipelineConfig(
        panel_season_min=2009,
        panel_season_max=2021,
        min_team_season_games=10,
        min_minutes=0,
        drop_dash_placeholder_names=True,
        sr_scrape_contact="dissertation-research",
    )
    panel = panel_rebuild.build_from_box(cfg)
    print(f"Panel {len(panel):,}", flush=True)
    bpm_merge.ensure_crosswalk(cfg)
    bpm_merge.write_scrape_jobs(panel, cfg)
    print("Scrape starting (no fetch cap)...", flush=True)
    scrape_out = scrape_bpm.run_batch(pipeline_cfg=cfg)
    print("Scrape done:", scrape_out, flush=True)
    match_out = bpm_merge.run_match(cfg, panel=panel)
    print("Match done:", match_out, flush=True)
    print("=== SR rescrape worker finished ===", flush=True)


if __name__ == "__main__":
    main()
