"""
Stage 6A pilot ordering: rank schools by panel coverage, optionally filter by
Stage 4 strategy audit (high `winner == 'none'` rate ⇒ weak / failed parses).
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def _audit_stats_by_school(strat_path: Path) -> dict[str, dict[str, Any]]:
    """Per uni_slug: n_audit_rows, n_none, frac_none (winner == 'none' per audit row)."""
    winners_by: dict[str, list[str]] = defaultdict(list)
    if not strat_path.is_file():
        return {}
    with open(strat_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            slug = (rec.get("uni_slug") or "").strip()
            if not slug:
                continue
            w = rec.get("winner")
            winners_by[slug].append(w if isinstance(w, str) else "")
    out: dict[str, dict[str, Any]] = {}
    for slug, winners in winners_by.items():
        n = len(winners)
        n_none = sum(1 for w in winners if w == "none")
        out[slug] = {
            "n_audit_rows": n,
            "n_none": n_none,
            "frac_none": (n_none / n) if n else 0.0,
        }
    return out


def prepare_stage6_panel(
    panel_records: list[dict],
    strat_audit_path: Path,
    *,
    pilot_mode: bool = True,
    pilot_top_n: int | None = None,
    sanity_filter: bool = True,
    sanity_max_none_frac: float = 0.35,
    sanity_min_audit_rows: int = 3,
) -> tuple[list[dict], list[str], dict[str, Any]]:
    """
    Reorder and optionally subset panel rows for OpenAlex Stage 6A.

    Ranking: descending unique faculty per school, then descending panel row count,
    then ``uni_slug`` for stability.

    Returns
    -------
    panel_out
        Rows filtered to kept schools, sorted so higher-priority schools are
        processed first by ``openalex_resolver.resolve_authors`` (insertion order).
    uni_slugs_ordered
        School slugs in the same priority order (for ``resolve_institutions``).
    report
        Diagnostics (drops, preview table, paths).
    """
    report: dict[str, Any] = {
        "pilot_mode": pilot_mode,
        "strat_path": str(strat_audit_path),
        "strat_found": strat_audit_path.is_file(),
    }

    if not pilot_mode:
        slugs = sorted({r["uni_slug"] for r in panel_records if r.get("uni_slug")})
        report["uni_slugs_ordered"] = slugs
        report["n_schools"] = len(slugs)
        return panel_records, slugs, report

    all_slugs = {r["uni_slug"] for r in panel_records if r.get("uni_slug")}
    fac_per: dict[str, set] = defaultdict(set)
    rows_per: Counter[str] = Counter()
    for r in panel_records:
        slug = r.get("uni_slug")
        fid = r.get("faculty_id")
        if not slug or fid is None:
            continue
        fac_per[slug].add(fid)
        rows_per[slug] += 1

    n_faculty = {s: len(fac_per[s]) for s in all_slugs}
    audit = _audit_stats_by_school(strat_audit_path) if sanity_filter else {}

    dropped_sanity: list[str] = []
    if sanity_filter and audit:
        for slug in list(all_slugs):
            st = audit.get(slug)
            if not st:
                continue
            if st["n_audit_rows"] >= sanity_min_audit_rows and st["frac_none"] > sanity_max_none_frac:
                dropped_sanity.append(slug)

    eligible = all_slugs - set(dropped_sanity)
    ranked = sorted(
        eligible,
        key=lambda s: (-n_faculty.get(s, 0), -rows_per[s], s),
    )

    if pilot_top_n is not None and pilot_top_n > 0:
        ranked = ranked[:pilot_top_n]

    keep_slugs = set(ranked)
    rank_idx = {s: i for i, s in enumerate(ranked)}

    panel_work = [r for r in panel_records if r.get("uni_slug") in keep_slugs]
    panel_out = sorted(
        panel_work,
        key=lambda r: (
            rank_idx.get(r.get("uni_slug"), 10**9),
            str(r.get("faculty_id", "")),
            int(r.get("year") or 0),
            str(r.get("season") or ""),
        ),
    )

    report["dropped_sanity"] = sorted(dropped_sanity)
    report["n_dropped_sanity"] = len(dropped_sanity)
    report["pilot_top_n"] = pilot_top_n
    report["uni_slugs_ordered"] = ranked
    report["n_schools"] = len(ranked)
    report["n_panel_rows"] = len(panel_out)
    report["top_schools_preview"] = [
        {
            "uni_slug": s,
            "n_faculty": n_faculty.get(s, 0),
            "n_rows": rows_per[s],
            **(audit.get(s, {})),
        }
        for s in ranked[: min(15, len(ranked))]
    ]
    return panel_out, ranked, report
