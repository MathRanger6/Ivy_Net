#!/usr/bin/env python3
"""Rebuild Stage 7 (enriched panel) and Stage 8 (pool metrics) from local pipeline files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from tenure.tenure_pipeline import panel_builder as pb
from tenure.tenure_pipeline import pool_metrics as pm

_HERE = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Rebuild faculty_panel_enriched + with_pools")
    parser.add_argument("--panel", type=Path, default=_HERE / "faculty_panel.jsonl")
    parser.add_argument("--works", type=Path, default=_HERE / "openalex_works_by_year.jsonl")
    parser.add_argument("--authors", type=Path, default=_HERE / "openalex_author_ids.jsonl")
    parser.add_argument("--enriched-out", type=Path, default=_HERE / "faculty_panel_enriched.jsonl")
    parser.add_argument("--pools-out", type=Path, default=_HERE / "faculty_panel_with_pools.jsonl")
    parser.add_argument("--transfers-audit", type=Path, default=_HERE / "transfers_audit.jsonl")
    parser.add_argument("--gap-tolerance", type=int, default=0)
    parser.add_argument("--min-year", type=int, default=2000)
    parser.add_argument("--max-year", type=int, default=2024)
    args = parser.parse_args()

    loss = pb.build_annual_panel(
        panel_path=args.panel,
        works_path=args.works,
        author_path=args.authors,
        out_path=args.enriched_out,
        min_year=args.min_year,
        max_year=args.max_year,
        gap_tolerance=args.gap_tolerance,
        transfers_audit_path=args.transfers_audit,
    )

    summary = pm.build_pool_metrics(
        in_path=args.enriched_out,
        out_path=args.pools_out,
    )

    meta_path = args.pools_out.with_name("panel_rebuild_meta.json")
    meta_path.write_text(json.dumps({"stage7": loss, "stage8": summary}, indent=2) + "\n")
    print(f"Wrote meta → {meta_path}")


if __name__ == "__main__":
    main()
