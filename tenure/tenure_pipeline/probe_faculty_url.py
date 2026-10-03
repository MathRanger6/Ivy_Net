#!/usr/bin/env python3
"""
Quick-check one faculty URL: CDX capture count, one Wayback download, parse record count.

Usage (from repo root, tenure_net recommended):
  python3 tenure/tenure_pipeline/probe_faculty_url.py --url 'https://cidse.engineering.asu.edu/faculty/'
  python3 tenure/tenure_pipeline/probe_faculty_url.py --url '...' --slug arizona_state_university --season fall --year 2020

Replaces ad-hoc test_candidates.py / discover TEST_PARSE for a single URL decision.
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

import html_parser
import requests

from wayback.cdx_client import count_cdx_captures, make_cdx_session, query_cdx_html_snapshots
from wayback.paths import faculty_source_id, make_slug, normalize_faculty_url

DEFAULT_HEADERS = {
    "User-Agent": "TenurePipelineResearch/1.0 (academic research; UVA dissertation pipeline)",
}


def _pick_snapshot(snaps: list[dict], year: int | None, season: str | None) -> dict | None:
    if not snaps:
        return None
    if year is None:
        return snaps[len(snaps) // 2]
    season = (season or "spring").lower()
    anchor = "0315" if season == "spring" else "1015"
    target = int(f"{year}{anchor}000000")
    ranked = sorted(snaps, key=lambda s: abs(int(s["timestamp"]) - target))
    return ranked[0]


def probe_url(
    url: str,
    *,
    slug: str | None = None,
    year: int | None = None,
    season: str | None = None,
    year_min: int = 2000,
    year_max: int = 2024,
    cdx_timeout: float = 45,
    html_timeout: float = 45,
    headers: dict | None = None,
) -> dict:
    headers = headers or DEFAULT_HEADERS
    url = url.strip()
    nu = normalize_faculty_url(url)
    sid = faculty_source_id(url)
    if not slug:
        slug = "probe_school"

    session = make_cdx_session(headers)
    snaps = query_cdx_html_snapshots(url, year_min, year_max, session, timeout=cdx_timeout)
    cdx_count, yr_min, yr_max = count_cdx_captures(url, timeout=30, headers=headers)

    result = {
        "url": url,
        "normalized": nu,
        "source_id": sid,
        "uni_slug": slug,
        "cdx_html_snaps_in_range": 0 if snaps is None else len(snaps),
        "cdx_total_captures": cdx_count,
        "cdx_year_span": (yr_min, yr_max) if cdx_count else None,
        "wayback_url": None,
        "http_status": None,
        "n_records": 0,
        "parse_winner": None,
        "error": None,
    }

    if snaps is None:
        result["error"] = "CDX query failed (timeout/connection)"
        return result
    if not snaps:
        result["error"] = "CDX returned 0 HTML snapshots in year range"
        return result

    pick = _pick_snapshot(snaps, year, season)
    if not pick:
        result["error"] = "no snapshot to download"
        return result

    wayback_url = f"https://web.archive.org/web/{pick['timestamp']}/{pick['original']}"
    result["wayback_url"] = wayback_url

    try:
        r = session.get(wayback_url, timeout=html_timeout)
        result["http_status"] = r.status_code
        if r.status_code != 200 or len(r.content) < 500:
            result["error"] = f"download too small or HTTP {r.status_code}"
            return result
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tf:
            tf.write(r.content)
            tmp = Path(tf.name)
        try:
            recs, meta = html_parser.extract_faculty(tmp, slug, return_meta=True)
            result["n_records"] = len(recs)
            result["parse_winner"] = meta.get("winner")
        finally:
            tmp.unlink(missing_ok=True)
    except Exception as e:
        result["error"] = str(e)[:120]

    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="Probe one faculty URL via CDX + parse.")
    ap.add_argument("--url", required=True, help="Live faculty page URL (not Wayback wrapper)")
    ap.add_argument("--slug", default="", help="uni_slug for parser context (optional)")
    ap.add_argument("--year", type=int, default=None, help="Pick snapshot near this calendar year")
    ap.add_argument("--season", choices=("spring", "fall"), default=None)
    ap.add_argument("--year-min", type=int, default=2000)
    ap.add_argument("--year-max", type=int, default=2024)
    args = ap.parse_args()

    tp = Path(__file__).resolve().parent
    sys.path.insert(0, str(tp))
    os.chdir(tp.parent.parent)

    slug = args.slug.strip() or None
    res = probe_url(
        args.url,
        slug=slug or make_slug("probe"),
        year=args.year,
        season=args.season,
        year_min=args.year_min,
        year_max=args.year_max,
    )

    print(f"\n  URL            : {res['url']}")
    print(f"  Normalized     : {res['normalized']}")
    print(f"  source_id      : {res['source_id']}")
    print(f"  CDX HTML snaps : {res['cdx_html_snaps_in_range']}  (in {args.year_min}–{args.year_max})")
    print(f"  CDX all caps   : {res['cdx_total_captures']}  span {res['cdx_year_span']}")
    if res.get("wayback_url"):
        print(f"  Wayback        : {res['wayback_url']}")
    if res.get("http_status"):
        print(f"  HTTP           : {res['http_status']}")
    print(f"  Parse records  : {res['n_records']}  (strategy: {res.get('parse_winner')})")
    if res.get("error"):
        print(f"  Note           : {res['error']}")

    if res["n_records"] >= 10:
        verdict = "GOOD — reasonable faculty list"
    elif res["n_records"] >= 3:
        verdict = "MARGINAL — paste to worksheet only if no better URL"
    elif res["n_records"] > 0:
        verdict = "LOW — likely wrong page or weak archive capture"
    else:
        verdict = "FAIL — do not add without a different URL or timestamp"
    print(f"\n  Verdict        : {verdict}\n")
    return 0 if res["n_records"] >= 3 and not res.get("error") else 1


if __name__ == "__main__":
    sys.exit(main())
