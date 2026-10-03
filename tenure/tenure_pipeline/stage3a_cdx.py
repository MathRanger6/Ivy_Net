"""
Stage 3A — Wayback CDX discovery (extracted from 540 Cell 3A).
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import pandas as pd

from wayback.cdx_client import make_cdx_session, query_cdx_html_snapshots
from wayback.paths import faculty_source_id, make_slug, normalize_wayback_slug_filter


def evenly_spaced_chron_pick(chron_snaps, k):
    n = len(chron_snaps)
    if n <= k:
        return list(chron_snaps)
    idxs = [int(round(i * (n - 1) / (k - 1))) for i in range(k)]
    out, seen_ts = [], set()
    for ix in idxs:
        s = chron_snaps[ix]
        ts = s["timestamp"]
        if ts in seen_ts:
            continue
        seen_ts.add(ts)
        out.append(s)
    if len(out) < k:
        for s in chron_snaps:
            ts = s["timestamp"]
            if ts not in seen_ts and len(out) < k:
                seen_ts.add(ts)
                out.append(s)
    out.sort(key=lambda s: int(s["timestamp"]))
    return out[:k]


def select_seasons(
    snapshots,
    year_min,
    year_max,
    seasons,
    max_per_season=12,
    spacing_pool_mult=2,
):
    by_year = {}
    for snap in snapshots:
        yr = snap["timestamp"][:4]
        by_year.setdefault(yr, []).append(snap)

    selected = []
    for year in range(year_min, year_max + 1):
        yr_snaps = by_year.get(str(year), [])
        if not yr_snaps:
            continue
        for season, mmdd in seasons.items():
            target = int(f"{year}{mmdd}000000")
            by_ts = {}
            for s in yr_snaps:
                ts = s["timestamp"]
                if ts not in by_ts:
                    by_ts[ts] = s
            uniq = list(by_ts.values())
            ranked = sorted(uniq, key=lambda s: abs(int(s["timestamp"]) - target))
            if len(ranked) <= max_per_season:
                pool = ranked
            else:
                inner_n = min(len(ranked), max_per_season * spacing_pool_mult)
                inner = sorted(ranked[:inner_n], key=lambda s: int(s["timestamp"]))
                pool = evenly_spaced_chron_pick(inner, max_per_season)
            for snap in pool:
                selected.append(
                    {
                        "year": year,
                        "season": season,
                        "timestamp": snap["timestamp"],
                        "original": snap["original"],
                    }
                )
    return selected


def run_stage3a_cdx(
    *,
    stage2_csv: Path,
    stage3_plan: Path,
    stage3_retry: Path,
    stage3_html_dir: Path,
    snapshot_local_prefix: str,
    cdx_headers: dict,
    cdx_year_min: int,
    cdx_year_max: int,
    cdx_seasons: dict,
    cdx_snaps_per_season: int,
    cdx_spacing_pool_mult: int,
    cdx_timeout: float,
    cdx_delay: float,
    wayback_slugs: set[str] | None = None,
    tymeout_fn=None,
) -> list[dict]:
    """Run CDX discovery; append to plan JSONL. Returns in-memory plan_records (all loaded + new)."""
    tymeout_fn = tymeout_fn or (lambda: "")

    session = make_cdx_session(cdx_headers)
    df_schools = pd.read_csv(stage2_csv)

    plan_records: list[dict] = []
    tried_urls: set[str] = set()
    if stage3_plan.exists():
        with open(stage3_plan, encoding="utf-8") as f:
            plan_records = [json.loads(l) for l in f if l.strip()]
        for r in plan_records:
            for key in ("source_url", "tried_primary_url"):
                u = r.get(key)
                if u:
                    tried_urls.add(u)
                    tried_urls.add(u.rstrip("/"))
            for u in r.get("tried_urls", []):
                tried_urls.add(u)
                tried_urls.add(u.rstrip("/"))
        print(f"  Loaded {len(plan_records)} existing plan records")
        print(f"  {len(tried_urls)} URL(s) already tried → will skip")

    slug_filter = normalize_wayback_slug_filter(wayback_slugs)
    if slug_filter:
        print(f"  WAYBACK_SLUGS filter : {len(slug_filter)} slug(s) — {', '.join(sorted(slug_filter)[:8])}"
              + (f" (+{len(slug_filter)-8} more)" if len(slug_filter) > 8 else ""))

    schools_to_query = []
    for _, row in df_schools.iterrows():
        uni_slug = make_slug(row["university"])
        if slug_filter and uni_slug not in slug_filter:
            continue
        urls = json.loads(row["urls"]) if pd.notna(row.get("urls", None)) else []
        untried = [u for u in urls if u.rstrip("/") not in tried_urls]
        if untried:
            schools_to_query.append((row, untried))

    print(
        f"  {len(df_schools) - len(schools_to_query)} school(s) fully covered or filtered — "
        f"{len(schools_to_query)} with untried URL(s) to query"
    )

    stage3_plan.parent.mkdir(parents=True, exist_ok=True)
    plan_f = open(stage3_plan, "a", encoding="utf-8")

    try:
        for cdx_i, (school, untried) in enumerate(schools_to_query, start=1):
            uni_name = school["university"]
            uni_slug = make_slug(uni_name)
            all_urls = json.loads(school["urls"]) if pd.notna(school.get("urls", None)) else []

            pos = df_schools.index[df_schools["university"] == uni_name]
            pos = (pos[0] + 1) if len(pos) else cdx_i
            print(
                f"\n  ── Now scraping: {uni_name}  ({pos}/{len(df_schools)}),  "
                f"({cdx_i} of {len(schools_to_query)} being scraped)",
                flush=True,
            )
            print(f"     {len(untried)} untried URL(s) of {len(all_urls)} total", flush=True)

            url_snaps = {}
            for url_i, url in enumerate(untried, start=1):
                print(f"     querying ({url_i}/{len(untried)}): {url}, at time: {tymeout_fn()}", flush=True)
                snaps = query_cdx_html_snapshots(
                    url,
                    cdx_year_min,
                    cdx_year_max,
                    session,
                    timeout=cdx_timeout,
                )
                url_snaps[url] = snaps
                time.sleep(cdx_delay)

            total_raw = sum(len(v) for v in url_snaps.values() if v is not None)
            print(f"\n  {uni_name}  ({pos}/{len(df_schools)}),  ({cdx_i} of {len(schools_to_query)} being scraped)")
            print(f"    CDX raw rows (all URLs) : {total_raw} snaps across {len(untried)} URL(s)")

            for url, snaps in url_snaps.items():
                if snaps is None:
                    continue
                src_id = faculty_source_id(url)
                selected = select_seasons(
                    snaps,
                    cdx_year_min,
                    cdx_year_max,
                    cdx_seasons,
                    cdx_snaps_per_season,
                    cdx_spacing_pool_mult,
                )
                n = len(snaps)
                print(
                    f"    url → seasons : {n!r:>6} snaps → {len(selected)} season rows  |  "
                    f"src_id={src_id}  {url[:65]}"
                )
                for sel in selected:
                    wayback_url = f"https://web.archive.org/web/{sel['timestamp']}/{sel['original']}"
                    out_filename = f"{sel['year']}_{sel['season']}_{sel['timestamp']}.html"
                    rec = {
                        "university": uni_name,
                        "uni_slug": uni_slug,
                        "year": sel["year"],
                        "season": sel["season"],
                        "timestamp": sel["timestamp"],
                        "source_url": url,
                        "source_id": src_id,
                        "wayback_url": wayback_url,
                        "local_path": f"{snapshot_local_prefix}/{uni_slug}/{src_id}/{out_filename}",
                        "total_snaps_union": len(snaps),
                    }
                    plan_records.append(rec)
                    plan_f.write(json.dumps(rec) + "\n")

            n_timeout = sum(1 for s in url_snaps.values() if s is None)
            n_empty = sum(1 for s in url_snaps.values() if s is not None and len(s) == 0)
            n_found = sum(1 for s in url_snaps.values() if s)
            for url, snaps in url_snaps.items():
                if snaps is None:
                    print(f"    ⏱  {url[:70]} → timed out — will retry next run")
                elif len(snaps) == 0:
                    sentinel = {
                        "university": uni_name,
                        "uni_slug": uni_slug,
                        "n_snaps": 0,
                        "source_url": url,
                        "queried_at": time.strftime("%Y-%m-%d"),
                    }
                    plan_records.append(sentinel)
                    plan_f.write(json.dumps(sentinel) + "\n")
                    print(f"    ⚠  {url[:70]} → 0 snapshots (sentinel written)")
                else:
                    bookmark = {
                        "plan_row_type": "cdx_bookmark",
                        "university": uni_name,
                        "uni_slug": uni_slug,
                        "source_url": url,
                        "queried_at": time.strftime("%Y-%m-%d"),
                    }
                    plan_records.append(bookmark)
                    plan_f.write(json.dumps(bookmark) + "\n")

            if n_timeout > 0 and n_found == 0:
                print(f"    ⏱  All {len(untried)} URL(s) timed out — will retry next run")
            elif n_empty > 0 and n_found == 0 and n_timeout == 0:
                print(f"    ⚠  All {len(untried)} URL(s) returned 0 snapshots")

            if n_timeout > 0:
                with open(stage3_retry, "a", encoding="utf-8") as rf:
                    for url, snaps in url_snaps.items():
                        if snaps is None:
                            rf.write(
                                json.dumps(
                                    {
                                        "university": uni_name,
                                        "uni_slug": uni_slug,
                                        "url": url,
                                        "added_at": time.strftime("%Y-%m-%d"),
                                    }
                                )
                                + "\n"
                            )

            plan_f.flush()
    finally:
        plan_f.close()

    n_schools_covered = len(
        {r["university"] for r in plan_records if r.get("local_path") and r.get("year") is not None}
    )
    print(f"\n\n  Plan written       : {len(plan_records):,} records")
    print(f"  Schools covered    : {n_schools_covered} / {len(df_schools)}")
    print(f"  Output             : {stage3_plan.resolve()}")
    return plan_records


def run_stage3a_from_globals(g: dict) -> list[dict] | None:
    if not g.get("RUN_CELL3_CDX"):
        return None
    clk = g["time_start"]("Stage 3A — CDX Discovery")
    records = run_stage3a_cdx(
        stage2_csv=Path(g["STAGE2_OUT"]),
        stage3_plan=Path(g["STAGE3_PLAN"]),
        stage3_retry=Path(g["STAGE3_RETRY"]),
        stage3_html_dir=Path(g["STAGE3_HTML_DIR"]),
        snapshot_local_prefix=g.get("SNAPSHOT_LOCAL_PREFIX", "tenure/tenure_pipeline/faculty_snapshots"),
        cdx_headers=g["CDX_HEADERS"],
        cdx_year_min=g["CDX_YEAR_MIN"],
        cdx_year_max=g["CDX_YEAR_MAX"],
        cdx_seasons=g["CDX_SEASONS"],
        cdx_snaps_per_season=g["CDX_SNAPS_PER_SEASON"],
        cdx_spacing_pool_mult=g["CDX_SPACING_POOL_MULT"],
        cdx_timeout=g["CDX_TIMEOUT"],
        cdx_delay=g["CDX_DELAY"],
        wayback_slugs=g.get("WAYBACK_SLUGS"),
        tymeout_fn=g.get("tymeout"),
    )
    g["time_stop"](clk)
    g["plan_records"] = records
    return records
