"""
Stage 3 — Sports Reference advanced stats (BPM / OBPM / DBPM) scrape + merge onto spine.

Durable artifacts: `DO_NOT_ERASE/bpm_player_season_raw.csv`, `bpm_player_season_matched.csv`,
`sr_school_slug_crosswalk.csv`, `sr_school_slug_aliases.csv`. Salvage notebooks under
`obsolete_files/sports_gameplan_old/` (`bpm_merge_to_530_bkup` for match).

If ``cfg.run_sr_scrape`` is True, calls ``scrape_bpm.run_batch`` (requires ``pip install -e .[scrape]``).
Otherwise ``run()`` only checks file presence and does not hit the network.
"""

from __future__ import annotations

from typing import Any

from sports_pipeline import paths


def run(cfg: Any) -> dict[str, Any]:
    raw = paths.bpm_raw_csv()
    matched = paths.bpm_matched_csv()
    xw = paths.sr_crosswalk_csv()
    jobs = paths.bpm_scrape_jobs_csv()
    skip = paths.bpm_scrape_skip_pairs_csv()
    out: dict[str, Any] = {"stage": "sr_bpm", "files": {}}
    for label, p in (
        ("bpm_raw", raw),
        ("bpm_matched", matched),
        ("sr_crosswalk", xw),
        ("bpm_scrape_jobs", jobs),
        ("bpm_scrape_skip_pairs", skip),
    ):
        out["files"][label] = {"path": str(p), "exists": p.is_file()}

    if bool(getattr(cfg, "run_sr_scrape", False)):
        from sports_pipeline import scrape_bpm

        out["scrape"] = scrape_bpm.run_batch(pipeline_cfg=cfg)
        out["status"] = "scraped"
        out["note"] = "Network scrape finished; re-run merge notebook to refresh bpm_player_season_matched.csv"
        return out

    out["status"] = "skip" if matched.is_file() else "todo"
    out["note"] = (
        "Set run_sr_scrape=True to fetch SR pages (scrape_bpm), or port merge from "
        "obsolete_files/sports_gameplan_old/bpm_merge_to_530_bkup.ipynb"
    )
    return out
