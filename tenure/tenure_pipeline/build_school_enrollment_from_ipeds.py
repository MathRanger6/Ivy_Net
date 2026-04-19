#!/usr/bin/env python3
"""
Build tenure_pipeline/school_enrollment_annual.csv from IPEDS fall enrollment (Part A).

Source: NCES IPEDS Data Center — ``ef{YY}a`` files (fall snapshot headcount).
Metric: ``EFTOTLT`` where ``EFALEVEL == 1`` (one grand-total row per institution).

Institution match: IPEDS ``hd{Y}`` directory (``INSTNM`` + ``IALIAS`` tokens) with a small
override table for names that do not appear verbatim in IPEDS (e.g. "UC Berkeley").

Usage (from workspace root):
  python tenure_pipeline/build_school_enrollment_from_ipeds.py
  python tenure_pipeline/build_school_enrollment_from_ipeds.py --year-min 2015 --year-max 2024

First run downloads one IPEDS zip per year (cached under ``_ipeds_cache``); a full 2004–2024
build is typically a few minutes on a normal connection—reruns are fast.

Years **2000–2003** are skipped (``ef*a`` files use a different layout without ``EFALEVEL``).

**HTTP:** Every NCES GET uses exponential backoff + jitter on 429 / 5xx / timeouts / connection errors
(``--max-retries``, ``--backoff-base``). **404 is not retried** (logged, then skip).

**Errors:** Events append to ``ipeds_download_errors.jsonl`` (JSONL: one JSON object per line) —
``http_404``, ``retry_exhausted``, ``stale_cache_removed``, ``bad_zipfile``, ``ef_year_skip``, ``hd_schema``, etc., with ``url`` where applicable.
**Reference:** ``tenure/documents/TENURE_PIPELINE_OVERVIEW.md`` section **7.5** (outcome meanings and ``HD_YEAR``).

Requires: pandas, requests (stdlib zipfile/io otherwise ok)
"""
from __future__ import annotations

import argparse
import io
import json
import random
import re
import sys
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

NCES_BASE = "https://nces.ed.gov/ipeds/datacenter/data"


def nces_data_file_url(table: str) -> str:
    """Canonical NCES Data Center URL for ``{table}.zip`` (e.g. ``ef2024a``, ``hd2023``)."""
    return f"{NCES_BASE}/{table}.zip"


# Retry these HTTP statuses (rate limit / server overload). 404 is never retried.
_TRANSIENT_HTTP = frozenset({429, 500, 502, 503, 504})


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _append_error_log(log_path: Path | None, record: dict) -> None:
    """Append one JSON object per line (JSONL) for manual follow-up."""
    if log_path is None:
        return
    record.setdefault("ts", _utc_iso())
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def _fetch_zip_bytes(
    url: str,
    *,
    error_log: Path | None,
    context: dict,
    max_retries: int,
    base_delay: float,
    timeout: float,
) -> bytes:
    """
    GET url; retry with exponential backoff + jitter on transient HTTP/network errors.
    Logs and raises on 404 or exhausted retries. Does not retry 404.
    """
    last_exc: BaseException | None = None
    for attempt in range(max_retries):
        try:
            r = requests.get(url, timeout=timeout)
            if r.status_code == 200:
                return r.content

            if r.status_code == 404:
                _append_error_log(
                    error_log,
                    {
                        **context,
                        "outcome": "http_404",
                        "status_code": 404,
                        "url": url,
                        "reason": r.reason,
                        "note": (
                            "NCES has no file at this URL yet (wrong year?), or table renamed. "
                            "Search https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx for the zip name."
                        ),
                    },
                )
                r.raise_for_status()

            if r.status_code in _TRANSIENT_HTTP:
                last_exc = f"HTTP {r.status_code} {r.reason}"
                if attempt < max_retries - 1:
                    delay = base_delay * (2**attempt) + random.uniform(0, 1.5)
                    time.sleep(delay)
                    continue
                _append_error_log(
                    error_log,
                    {
                        **context,
                        "outcome": "retry_exhausted",
                        "status_code": r.status_code,
                        "url": url,
                        "attempts": attempt + 1,
                        "error": last_exc,
                    },
                )
                r.raise_for_status()

            # Other 4xx/5xx: log once, no retry loop for e.g. 403
            _append_error_log(
                error_log,
                {
                    **context,
                    "outcome": "http_error",
                    "status_code": r.status_code,
                    "url": url,
                    "reason": r.reason,
                },
            )
            r.raise_for_status()

        except requests.HTTPError:
            raise
        except requests.Timeout as e:
            last_exc = e
            if attempt < max_retries - 1:
                time.sleep(base_delay * (2**attempt) + random.uniform(0, 1.5))
                continue
            _append_error_log(
                error_log,
                {
                    **context,
                    "outcome": "retry_exhausted",
                    "url": url,
                    "attempts": attempt + 1,
                    "error": repr(e),
                    "error_type": "Timeout",
                },
            )
            raise
        except requests.ConnectionError as e:
            last_exc = e
            if attempt < max_retries - 1:
                time.sleep(base_delay * (2**attempt) + random.uniform(0, 1.5))
                continue
            _append_error_log(
                error_log,
                {
                    **context,
                    "outcome": "retry_exhausted",
                    "url": url,
                    "attempts": attempt + 1,
                    "error": repr(e),
                    "error_type": "ConnectionError",
                },
            )
            raise

# Pipeline university string -> exact IPEDS Institution Name (INSTNM) as in HD file.
# Extend this if auto-match reports UNMATCHED for a school you care about.
INSTNM_OVERRIDES: dict[str, str] = {
    "UC Berkeley": "University of California-Berkeley",
    "UC Santa Barbara": "University of California-Santa Barbara",
    "UC Irvine": "University of California-Irvine",
    "UC Davis": "University of California-Davis",
    "UC Riverside": "University of California-Riverside",
    "UC Santa Cruz": "University of California-Santa Cruz",
    "University of California San Diego": "University of California-San Diego",
    "University of California Los Angeles": "University of California-Los Angeles",
    "University of Illinois Urbana-Champaign": "University of Illinois Urbana-Champaign",
    "University of North Carolina Chapel Hill": "University of North Carolina at Chapel Hill",
    "University of Massachusetts Amherst": "University of Massachusetts-Amherst",
    "University of Nevada Las Vegas": "University of Nevada-Las Vegas",
    "University of Nevada Reno": "University of Nevada-Reno",
    "University of Texas at Austin": "The University of Texas at Austin",
    "University of Texas at Dallas": "The University of Texas at Dallas",
    "University of Texas at Arlington": "The University of Texas at Arlington",
    "University of Texas at San Antonio": "The University of Texas at San Antonio",
    "University of Texas El Paso": "The University of Texas at El Paso",
    "Indiana University": "Indiana University-Bloomington",
    "University at Buffalo (SUNY)": "University at Buffalo",
    "Binghamton University (SUNY)": "Binghamton University",
    "University at Albany SUNY": "University at Albany",
    "College of William & Mary": "William & Mary",
    "Rutgers University": "Rutgers University-New Brunswick",
    "Ohio State University": "Ohio State University-Main Campus",
    "Penn State University": "Pennsylvania State University-Main Campus",
    "University of Pittsburgh": "University of Pittsburgh-Pittsburgh Campus",
    "North Carolina State University": "North Carolina State University at Raleigh",
    "Texas A&M University": "Texas A & M University-College Station",
    "University of Alabama Birmingham": "University of Alabama at Birmingham",
    "University of Colorado Boulder": "University of Colorado Boulder",
    "University of Colorado Denver": "University of Colorado Denver/Anschutz Medical Campus",
    "University of Wisconsin-Madison": "University of Wisconsin-Madison",
    "University of Wisconsin Milwaukee": "University of Wisconsin-Milwaukee",
    "Missouri University of Science and Technology": "Missouri University of Science and Technology",
    "Indiana University Indianapolis": "Indiana University-Indianapolis",
    "Purdue University": "Purdue University-Main Campus",
    "Georgia Institute of Technology": "Georgia Institute of Technology-Main Campus",
    "University of Maryland": "University of Maryland-College Park",
    "University of Minnesota": "University of Minnesota-Twin Cities",
    "University of Washington": "University of Washington-Seattle Campus",
    "University of Virginia": "University of Virginia-Main Campus",
    "University of Michigan": "University of Michigan-Ann Arbor",
    "Colorado State University": "Colorado State University-Fort Collins",
    "University of Missouri": "University of Missouri-Columbia",
    "Oklahoma State University": "Oklahoma State University-Main Campus",
    "University of Tennessee": "The University of Tennessee-Knoxville",
    "University of Alabama": "The University of Alabama",
    "University of South Carolina": "University of South Carolina-Columbia",
    "University of Maryland Baltimore County": "University of Maryland-Baltimore County",
    "New Mexico State University": "New Mexico State University-Main Campus",
    "University of Hawaii": "University of Hawaii at Manoa",
    "Arizona State University": "Arizona State University Campus Immersion",
    "University of New Mexico": "University of New Mexico-Main Campus",
    "University of Cincinnati": "University of Cincinnati-Main Campus",
    "University of Massachusetts Lowell": "University of Massachusetts-Lowell",
    "University of New Hampshire": "University of New Hampshire-Main Campus",
    "North Dakota State University": "North Dakota State University-Main Campus",
    "University of North Carolina Charlotte": "University of North Carolina at Charlotte",
    "Kent State University": "Kent State University at Kent",
    "Ohio University": "Ohio University-Main Campus",
    "University of Massachusetts Boston": "University of Massachusetts-Boston",
    "University of Missouri Kansas City": "University of Missouri-Kansas City",
    "Virginia Tech": "Virginia Polytechnic Institute and State University",
}


def _norm_key(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    s = s.replace("&", "and")
    s = re.sub(r"[^a-z0-9 ]+", "", s)
    return s


def _strip_bom(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={c: c.lstrip("\ufeff") for c in df.columns})
    return df


def download_zip_csv(
    table: str,
    cache_dir: Path,
    *,
    encoding: str = "utf-8-sig",
    error_log: Path | None = None,
    max_retries: int = 5,
    base_delay: float = 2.0,
    timeout: float = 120,
) -> pd.DataFrame:
    """table: e.g. ef2021a, hd2023 (without .zip). Uses backoff/retry on GET; logs failures to JSONL."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    zip_name = f"{table}.zip"
    url = f"{NCES_BASE}/{zip_name}"
    path = cache_dir / zip_name
    ctx: dict = {"kind": "ipeds_zip", "table": table, "zip_name": zip_name, "url": url}

    # Stale cache: a previous run may have saved HTML or a partial body as ``*.zip``.
    # Browser downloads work; we must not skip HTTP when the file on disk is not a real zip.
    if path.exists() and not zipfile.is_zipfile(path):
        _append_error_log(
            error_log,
            {
                **ctx,
                "outcome": "stale_cache_removed",
                "path": str(path),
                "note": (
                    "Cached file exists but is not a valid ZIP (often an NCES error page saved as .zip). "
                    "Removing and re-downloading."
                ),
            },
        )
        print(
            f"      replacing invalid cache (not a zip, deleting): {path}",
            file=sys.stderr,
            flush=True,
        )
        path.unlink(missing_ok=True)

    if not path.exists():
        try:
            data = _fetch_zip_bytes(
                url,
                error_log=error_log,
                context=ctx,
                max_retries=max_retries,
                base_delay=base_delay,
                timeout=timeout,
            )
            path.write_bytes(data)
        except requests.HTTPError:
            # Already logged in _fetch_zip_bytes (e.g. http_404, retry_exhausted + raise)
            raise
        except Exception as e:
            _append_error_log(
                error_log,
                {
                    **ctx,
                    "outcome": "download_failed",
                    "error": repr(e),
                },
            )
            raise

    try:
        with zipfile.ZipFile(path, "r") as zf:
            names = [n for n in zf.namelist() if n.lower().endswith(".csv") and "_rv" not in n.lower()]
            if not names:
                names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
            if not names:
                _append_error_log(
                    error_log,
                    {
                        **ctx,
                        "outcome": "zip_no_csv",
                        "path": str(path),
                        "members": zf.namelist()[:30],
                    },
                )
                raise ValueError(f"No CSV in zip: {path}")
            inner = sorted(names, key=len)[0]
            raw = zf.read(inner)
    except zipfile.BadZipFile as e:
        _append_error_log(
            error_log,
            {**ctx, "outcome": "bad_zipfile", "path": str(path), "error": repr(e)},
        )
        raise

    try:
        df = pd.read_csv(io.BytesIO(raw), encoding=encoding, low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(io.BytesIO(raw), encoding="latin-1", low_memory=False)
    return _strip_bom(df)


def load_hd_institution_table(
    hd_year: int,
    cache_dir: Path,
    *,
    error_log: Path | None = None,
    max_retries: int = 5,
    base_delay: float = 2.0,
    timeout: float = 120,
) -> pd.DataFrame:
    df = download_zip_csv(
        f"hd{hd_year}",
        cache_dir,
        encoding="utf-8-sig",
        error_log=error_log,
        max_retries=max_retries,
        base_delay=base_delay,
        timeout=timeout,
    )
    df = _strip_bom(df)
    need = {"UNITID", "INSTNM", "IALIAS"}
    if not need.issubset(df.columns):
        _append_error_log(
            error_log,
            {
                "kind": "hd_schema",
                "table": f"hd{hd_year}",
                "outcome": "missing_columns",
                "have": [c for c in df.columns][:40],
                "need": sorted(need),
            },
        )
        raise ValueError(f"HD file missing columns: {df.columns.tolist()[:20]}")
    return df


def build_lookup_strings(hd: pd.DataFrame) -> dict[str, int]:
    """Map normalized search string -> UNITID (first wins on collision)."""
    out: dict[str, int] = {}
    for _, row in hd.iterrows():
        uid = int(row["UNITID"])
        for part in [row["INSTNM"], str(row.get("IALIAS", "") or "")]:
            for token in re.split(r"[|;]", part):
                k = _norm_key(token)
                if len(k) < 6:
                    continue
                out.setdefault(k, uid)
    return out


def resolve_unitid(school: str, hd: pd.DataFrame, lookup: dict[str, int]) -> int | None:
    if school in INSTNM_OVERRIDES:
        target = INSTNM_OVERRIDES[school]
        row = hd[hd["INSTNM"].str.strip() == target]
        if len(row) == 1:
            return int(row["UNITID"].iloc[0])
        # try case-insensitive
        row = hd[hd["INSTNM"].str.lower() == target.lower()]
        if len(row) == 1:
            return int(row["UNITID"].iloc[0])
        return None

    # Exact INSTNM
    row = hd[hd["INSTNM"].str.strip() == school]
    if len(row) == 1:
        return int(row["UNITID"].iloc[0])

    nk = _norm_key(school)
    if nk in lookup:
        return lookup[nk]

    # Longest prefix / substring match on INSTNM (conservative)
    hits = hd[hd["INSTNM"].str.lower().str.startswith(nk[: min(12, len(nk))], na=False)]
    if len(hits) == 1:
        return int(hits["UNITID"].iloc[0])
    return None


_RACE_COL = re.compile(r"^EFRACE\d+$")


def fall_total_from_ef_part_a(ef: pd.DataFrame, unitid: int) -> int | None:
    """Fall headcount: ``EFTOTLT`` at ``EFALEVEL==1`` (newer files), else sum ``EFRACE*`` (legacy IPEDS)."""
    if "UNITID" not in ef.columns or "EFALEVEL" not in ef.columns:
        return None
    sub = ef[(ef["UNITID"] == unitid) & (ef["EFALEVEL"] == 1)]
    if len(sub) != 1:
        return None
    row = sub.iloc[0]
    if "EFTOTLT" in ef.columns:
        v = row["EFTOTLT"]
        if pd.notna(v):
            return int(v)
    race_cols = [c for c in ef.columns if _RACE_COL.match(str(c))]
    if race_cols:
        s = pd.to_numeric(row[race_cols], errors="coerce").fillna(0).sum()
        if s > 0:
            return int(s)
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Build school_enrollment_annual.csv from IPEDS fall EF Part A.")
    ap.add_argument(
        "--schools-csv",
        type=Path,
        default=None,
        help="Default: tenure_pipeline/r1_cs_departments.csv next to this file",
    )
    ap.add_argument(
        "--out-csv",
        type=Path,
        default=None,
        help="Default: tenure_pipeline/school_enrollment_annual.csv",
    )
    ap.add_argument(
        "--year-min",
        type=int,
        default=2004,
        help="Default 2004 (ef2000a–ef2003a lack EFALEVEL and are skipped).",
    )
    ap.add_argument("--year-max", type=int, default=2024)
    ap.add_argument("--hd-year", type=int, default=2023, help="Directory year for name matching (UNITIDs stable).")
    ap.add_argument(
        "--cache-dir",
        type=Path,
        default=None,
        help="Default: tenure_pipeline/_ipeds_cache",
    )
    ap.add_argument(
        "--error-log",
        type=Path,
        default=None,
        help="JSONL log of download/parse issues (default: tenure_pipeline/ipeds_download_errors.jsonl).",
    )
    ap.add_argument(
        "--append-error-log",
        action="store_true",
        help="Append to error log instead of truncating at run start.",
    )
    ap.add_argument("--max-retries", type=int, default=5, help="HTTP GET retries for transient errors (429/5xx/timeouts).")
    ap.add_argument("--backoff-base", type=float, default=2.0, help="Base seconds for exponential backoff (jitter added).")
    ap.add_argument("--http-timeout", type=float, default=120.0, help="Per-request timeout in seconds.")
    args = ap.parse_args()

    here = Path(__file__).resolve().parent
    schools_csv = args.schools_csv or (here / "r1_cs_departments.csv")
    out_csv = args.out_csv or (here / "school_enrollment_annual.csv")
    cache_dir = args.cache_dir or (here / "_ipeds_cache")
    error_log = args.error_log if args.error_log is not None else (here / "ipeds_download_errors.jsonl")

    if not args.append_error_log:
        error_log.parent.mkdir(parents=True, exist_ok=True)
        error_log.write_text("", encoding="utf-8")
    _append_error_log(
        error_log,
        {
            "kind": "run_start",
            "script": "build_school_enrollment_from_ipeds.py",
            "year_min": args.year_min,
            "year_max": args.year_max,
            "hd_year": args.hd_year,
            "max_retries": args.max_retries,
            "backoff_base_sec": args.backoff_base,
        },
    )

    sch = pd.read_csv(schools_csv)
    if "university" not in sch.columns:
        print("ERROR: schools csv must have 'university' column.", file=sys.stderr)
        return 1

    _hd_table = f"hd{args.hd_year}"
    _hd_url = nces_data_file_url(_hd_table)
    print(f"  Loading {_hd_table} for institution names …")
    print(f"      url: {_hd_url}", flush=True)
    try:
        hd = load_hd_institution_table(
            args.hd_year,
            cache_dir,
            error_log=error_log,
            max_retries=args.max_retries,
            base_delay=args.backoff_base,
            timeout=args.http_timeout,
        )
    except Exception as e:
        print(f"  ERROR: could not load institution directory\n      url: {_hd_url}\n      ({e})", file=sys.stderr)
        return 1
    lookup = build_lookup_strings(hd)

    rows: list[dict] = []
    unmatched: list[str] = []
    unitid_by_school: dict[str, int] = {}

    for school in sch["university"].tolist():
        uid = resolve_unitid(school, hd, lookup)
        if uid is None:
            unmatched.append(school)
            continue
        unitid_by_school[school] = uid

    if unmatched:
        print("  UNMATCHED (add INSTNM_OVERRIDES in build_school_enrollment_from_ipeds.py):", file=sys.stderr)
        for u in unmatched:
            print(f"    - {u}", file=sys.stderr)

    cross_path = here / "ipeds_unitid_crosswalk.json"
    cross_path.write_text(
        json.dumps({"hd_year": args.hd_year, "school_to_unitid": unitid_by_school}, indent=2),
        encoding="utf-8",
    )
    print(f"  Wrote {cross_path} ({len(unitid_by_school)} schools matched)")

    if args.year_min < 2004:
        print(
            "  Note: years before 2004 are skipped (IPEDS ef*a layout). "
            "Use --year-min 2004 to avoid wasted requests.",
            file=sys.stderr,
        )

    n_years = args.year_max - args.year_min + 1
    t0 = time.perf_counter()
    for i, year in enumerate(range(args.year_min, args.year_max + 1), start=1):
        tname = f"ef{year}a"
        zip_url = nces_data_file_url(tname)
        print(f"  Year {year} ({i}/{n_years})  loading {tname} …", flush=True)
        y0 = time.perf_counter()
        try:
            ef = download_zip_csv(
                tname,
                cache_dir,
                encoding="latin-1",
                error_log=error_log,
                max_retries=args.max_retries,
                base_delay=args.backoff_base,
                timeout=args.http_timeout,
            )
        except Exception as e:
            print(f"    skip: could not load\n      url: {zip_url}\n      ({e})", file=sys.stderr)
            continue
        ef = _strip_bom(ef)
        if "EFALEVEL" not in ef.columns:
            print(f"    skip: no EFALEVEL in {tname}\n      url: {zip_url}", file=sys.stderr)
            _append_error_log(
                error_log,
                {
                    "kind": "ef_year_skip",
                    "table": tname,
                    "year": year,
                    "url": zip_url,
                    "outcome": "no_efalevel",
                    "note": "IPEDS layout change or wrong file; try another release year on NCES Data Center.",
                },
            )
            continue
        if "EFTOTLT" not in ef.columns:
            race_cols = [c for c in ef.columns if _RACE_COL.match(str(c))]
            if not race_cols:
                print(f"    skip: no EFTOTLT or EFRACE* in {tname}\n      url: {zip_url}", file=sys.stderr)
                _append_error_log(
                    error_log,
                    {
                        "kind": "ef_year_skip",
                        "table": tname,
                        "year": year,
                        "url": zip_url,
                        "outcome": "no_enrollment_columns",
                        "note": "No EFTOTLT or EFRACE* columns; cannot compute total.",
                    },
                )
                continue
        n_ok = 0
        for school, uid in unitid_by_school.items():
            tot = fall_total_from_ef_part_a(ef, uid)
            if tot is None:
                continue
            rows.append({"university": school, "year": year, "total_enrollment": tot})
            n_ok += 1
        print(
            f"    done in {time.perf_counter() - y0:.1f}s — {n_ok}/{len(unitid_by_school)} schools",
            flush=True,
        )
    print(f"  All years finished in {time.perf_counter() - t0:.1f}s", flush=True)

    out = pd.DataFrame(rows).sort_values(["university", "year"])
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    # Brief header comment for humans (pandas will write after our prelude)
    prelude = (
        "# IPEDS Fall Enrollment Part A (ef{year}a), EFTOTLT where EFALEVEL=1 — total fall headcount.\n"
        f"# Generated by build_school_enrollment_from_ipeds.py — years {args.year_min}-{args.year_max}.\n"
        "# university must match r1_cs_departments.csv exactly.\n"
    )
    with open(out_csv, "w", encoding="utf-8") as f:
        f.write(prelude)
    out.to_csv(out_csv, mode="a", index=False)
    print(f"  Wrote {out_csv}  ({len(out)} rows)")

    if error_log.exists():
        nlines = sum(1 for _ in error_log.open(encoding="utf-8") if _.strip())
        print(f"  Error / event log (JSONL): {error_log}  ({nlines} lines — review non-run_start entries)")
    if unmatched:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
