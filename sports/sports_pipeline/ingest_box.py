"""
Stage 1 — spine from BOX (sportsdataverse / ESPN college MBB).

Placeholder: real implementation should refresh `mbb_df_player_box.csv` (and related
schedule/team tables) from the API. Until then, `run()` only checks that the CSV exists.
"""

from __future__ import annotations

from typing import Any

from sports_pipeline import paths


def run(cfg: Any) -> dict[str, Any]:
    """
    If `mbb_df_player_box.csv` exists, report skip; else return a todo dict.

    `cfg` reserved for future season lists / force-refresh flags.
    """
    p = paths.player_box_csv()
    if p.is_file():
        return {"stage": "ingest_box", "status": "skip", "path": str(p), "note": "file present"}
    return {
        "stage": "ingest_box",
        "status": "todo",
        "note": "implement SDV ingest or restore data under datasets/mbb/",
    }
