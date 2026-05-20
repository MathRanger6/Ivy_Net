"""
Stage 2 — draft ↔ spine matching (NBA draft strings → `athlete_id` on ESPN box spine).

Placeholder: matcher logic still lives in `obsolete_files/sports_gameplan_old/sdv_second_bkup.ipynb`
(or successor). Outputs on disk today: `athlete_id_draft_lookup.csv`, `draft_athlete_match.csv`, etc.

After draft lookup exists, run ``combine_bridge.run(cfg)`` to link combine ``player_id`` →
``athlete_id`` (writes ``combine_player_id_bridge.csv``, ``athlete_id_combine_lookup.csv``).
"""

from __future__ import annotations

from typing import Any

from sports_pipeline import paths


def run(cfg: Any) -> dict[str, Any]:
    p = paths.draft_lookup_csv()
    if not p.is_file():
        return {
            "stage": "draft_match",
            "status": "todo",
            "note": "run matcher to write athlete_id_draft_lookup.csv",
        }
    out: dict[str, Any] = {
        "stage": "draft_match",
        "status": "skip",
        "path": str(p),
        "note": "lookup present",
    }
    if paths.draft_combine_stats_csv().is_file():
        from sports_pipeline import combine_bridge

        out["combine_bridge"] = combine_bridge.run(cfg)
    return out
