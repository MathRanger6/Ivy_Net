"""
Internet Archive CDX API helpers (Cell 3A and future discover integration).
"""
from __future__ import annotations

import time

import requests

CDX_API = "https://web.archive.org/cdx/search/cdx"


def query_cdx_html_snapshots(
    url: str,
    year_min: int,
    year_max: int,
    session: requests.Session,
    *,
    timeout: float,
    limit: int = 600,
) -> list[dict] | None:
    """
    Query CDX for 200 OK HTML snapshots of ``url``.

    Returns list of {timestamp, original, statuscode}, [] if empty, None on connection/timeout.
    """
    params = {
        "url": url,
        "output": "json",
        "fl": "timestamp,original,statuscode",
        "from": f"{year_min}0101",
        "to": f"{year_max}1231",
        "filter": ["statuscode:200", "mimetype:text/html"],
        "collapse": "timestamp:6",
        "limit": str(limit),
    }
    try:
        r = session.get(CDX_API, params=params, timeout=timeout)
        if r.status_code == 429:
            print("  WARNING: 429 rate limit — sleeping 60s then retrying")
            time.sleep(60)
            r = session.get(CDX_API, params=params, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        if len(data) <= 1:
            return []
        hdr = data[0]
        return [dict(zip(hdr, row)) for row in data[1:]]
    except requests.exceptions.ConnectionError as e:
        print(f"  CDX connection error for {url}: {e}")
        print("  ⏸  Connection refused — pausing 10s before next request")
        time.sleep(10)
        return None
    except Exception as e:
        print(f"  CDX error for {url}: {e}")
        return None


def query_cdx_collapsed(
    url_pattern: str,
    *,
    match_type: str = "prefix",
    limit: int = 200_000,
    timeout: float = 45,
    headers: dict | None = None,
) -> list[dict]:
    """
    CDX query with collapse=urlkey (one row per unique URL). Used by URL discovery.

    Returns list of {url, count, year_min, year_max, sample_ts}.
    """
    params = {
        "url": url_pattern,
        "output": "json",
        "fl": "original,timestamp,statuscode",
        "collapse": "urlkey",
        "limit": str(limit),
        "matchType": match_type,
    }
    hdrs = headers or {"User-Agent": "TenurePipelineResearch/1.0"}
    try:
        r = requests.get(CDX_API, params=params, headers=hdrs, timeout=timeout)
        r.raise_for_status()
        raw = r.json()
    except Exception as exc:
        print(f"    CDX error [{match_type}] {url_pattern}: {exc}", flush=True)
        return []

    if not raw or len(raw) < 2:
        return []

    header = raw[0]
    rows = raw[1:]
    try:
        i_url = header.index("original")
        i_ts = header.index("timestamp")
        i_status = header.index("statuscode")
    except ValueError:
        return []

    results = []
    for row in rows:
        try:
            url = row[i_url]
            ts = row[i_ts]
            status = row[i_status]
        except IndexError:
            continue
        if status in ("404", "403", "301", "302"):
            continue
        if not str(url).startswith("http"):
            continue
        year = int(ts[:4]) if ts and len(ts) >= 4 else 0
        results.append(
            {
                "url": url,
                "count": 1,
                "year_min": year,
                "year_max": year,
                "sample_ts": ts,
            }
        )
    return results


def count_cdx_captures(
    url: str,
    *,
    timeout: float = 30,
    limit: int = 10_000,
    headers: dict | None = None,
) -> tuple[int, int, int]:
    """Return (capture_count, year_min, year_max) for a exact URL."""
    params = {
        "url": url,
        "output": "json",
        "fl": "timestamp",
        "limit": str(limit),
    }
    hdrs = headers or {"User-Agent": "TenurePipelineResearch/1.0"}
    try:
        r = requests.get(CDX_API, params=params, headers=hdrs, timeout=timeout)
        r.raise_for_status()
        raw = r.json()
    except Exception:
        return 0, 0, 0
    if not raw or len(raw) < 2:
        return 0, 0, 0
    years = []
    for row in raw[1:]:
        if row and row[0]:
            years.append(int(str(row[0])[:4]))
    if not years:
        return 0, 0, 0
    return len(years), min(years), max(years)


def make_cdx_session(headers: dict) -> requests.Session:
    """Session with no urllib3 retries (avoid burst on connection refused)."""
    from requests.adapters import HTTPAdapter

    session = requests.Session()
    session.headers.update(headers)
    no_retry = HTTPAdapter(max_retries=0)
    session.mount("https://", no_retry)
    session.mount("http://", no_retry)
    return session
