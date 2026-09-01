"""HERO panel prep — last assistant year + cumulative pool perf.

Stage 8 ``poolq_loo_mean`` uses annual ``pubs_year``. For the MBB-style
last-ps cross-section on cumulative stock, recompute LOO from
``pubs_cumulative`` at the final assistant row.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def _mean(vals: list[float]) -> float | None:
    if not vals:
        return None
    return sum(vals) / len(vals)


def attach_loo_cumulative(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Add ``poolq_loo_cum_mean`` from OA peer cumulative pubs (uni×year pools)."""
    pools: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        if r.get("rank") != "assistant":
            continue
        key = (r["uni_slug"], int(r["year"]))
        cum = r.get("pubs_cumulative")
        cum_val = float(cum) if cum is not None else None
        pools[key].append(
            {
                "fid": r["faculty_id"],
                "cum": cum_val,
                "has_oa": bool(r.get("openalex_id")),
            }
        )

    loo_lookup: dict[tuple[tuple[str, int], str], float | None] = {}
    for key, members in pools.items():
        oa = [m for m in members if m["has_oa"] and m["cum"] is not None]
        for m in members:
            if not m["has_oa"] or m["cum"] is None:
                loo_lookup[(key, m["fid"])] = None
                continue
            peers = [x["cum"] for x in oa if x["fid"] != m["fid"]]
            loo_lookup[(key, m["fid"])] = _mean(peers)

    for r in rows:
        key = (r["uni_slug"], int(r["year"]))
        r["poolq_loo_cum_mean"] = loo_lookup.get((key, r["faculty_id"]))
    return rows


def filter_last_asst_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep assistant rows at ``year == last_asst_year`` (one row per spell exit)."""
    out: list[dict[str, Any]] = []
    for r in rows:
        if r.get("rank") != "assistant":
            continue
        la = r.get("last_asst_year")
        yr = r.get("year")
        if la is None or yr is None:
            continue
        if int(yr) == int(la):
            out.append(r)
    return out


def load_inference_rows(
    in_path: Path,
    *,
    tiers: frozenset[str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with in_path.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r.get("match_confidence") not in tiers:
                continue
            if r.get("rank") != "assistant":
                continue
            rows.append(r)
    return rows


def prepare_hero_panel(
    in_path: Path,
    *,
    tiers: frozenset[str],
    grain: str = "spell_mean",
    pool_perf: str = "annual",
    x_metric: str = "loo",
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """
    Return rows ready for stage9 + prep stats.

    grain: ``spell_mean`` | ``last_asst``
    pool_perf: ``annual`` (existing poolq_loo_mean collapse) | ``cumulative``
    x_metric: ``loo`` | ``poolq`` | ``own_cum`` (own pubs_cumulative at last_asst only)
    """
    if grain not in ("spell_mean", "last_asst"):
        raise ValueError(f"grain must be spell_mean or last_asst, got {grain!r}")
    if pool_perf not in ("annual", "cumulative"):
        raise ValueError(f"pool_perf must be annual or cumulative, got {pool_perf!r}")
    if x_metric == "own_cum" and grain != "last_asst":
        raise ValueError("x_metric=own_cum requires grain=last_asst")

    raw = load_inference_rows(in_path, tiers=tiers)
    stats: dict[str, Any] = {
        "n_inference_asst_rows": len(raw),
        "grain": grain,
        "pool_perf": pool_perf,
        "x_metric": x_metric,
    }

    if grain == "last_asst":
        work = filter_last_asst_rows(raw)
        stats["n_last_asst_rows"] = len(work)
    else:
        work = raw

    if x_metric == "own_cum":
        before = len(work)
        work = [r for r in work if r.get("pubs_cumulative") is not None]
        stats["n_with_x"] = len(work)
        stats["n_dropped_null_x"] = before - len(work)
        stats["x_field"] = "pubs_cumulative"
        return work, stats

    if pool_perf == "cumulative":
        work = attach_loo_cumulative(work)
        loo_key = "poolq_loo_cum_mean"
    else:
        loo_key = "poolq_loo_mean"

    before = len(work)
    work = [r for r in work if r.get(loo_key) is not None]
    stats["n_with_loo"] = len(work)
    stats["n_with_x"] = len(work)
    stats["n_dropped_null_loo"] = before - len(work)
    stats["loo_field"] = loo_key
    return work, stats


def write_jsonl(rows: list[dict[str, Any]], out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
