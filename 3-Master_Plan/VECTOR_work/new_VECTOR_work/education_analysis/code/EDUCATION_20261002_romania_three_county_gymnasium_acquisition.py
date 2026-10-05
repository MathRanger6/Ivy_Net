"""Acquire 2001 Ministry Gymnasium Applicant Views for selected counties.

This is SOURCE ACQUISITION ONLY. Importing the module or running without --run
does not contact Wayback. Charles runs it from Cursor; every verified page is
saved at once under ~/Desktop/VECTOR_temp, outside Dropbox and Git. The 36
already saved pilot pages are verified and reused. A failed address remains
unresolved and can be retried on a later run; no absence is inferred.
"""

import argparse
import csv
import json
import os
import re
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

from romania_archive_retrieval import ArchiveClient, RetrievalStopped
from EDUCATION_20260930_romania_2001_national_acquisition import (
    _payload, archive_url, atomic_json, verified_page,
)
from EDUCATION_20261001_romania_four_county_school_report_check import (
    PRIVATE, PAGES, event, persist_429_cooldown, say, show_429_response,
)
from EDUCATION_20261001_romania_four_county_school_sample import school_directory
from EDUCATION_20261001_romania_origin_school_name_audit import save_csv

COUNTIES = ("CS", "GL", "TL", "AR", "SB")
OUT = Path(__file__).resolve().parents[1] / "outputs/romania_2001_four_county_source_pilot"
DEFAULT_STATUS = OUT / "full_school_view_acquisition_status.csv"
STATUS = DEFAULT_STATUS
EVENTS = PRIVATE / "full_school_view_retrieval_events.jsonl"
FIELDS = ("county", "gymnasium_code", "status", "applicant_rows", "last_http_status")
REQUIRED_HEADERS = {"Nume", "Medie Admitere", "Medie Capacitate", "Medie Absolvire"}
ACCEPTED_KINDS = {"sampled_origin_school_candidates", "origin_school_candidates"}


def emit(record):
    """Show live progress and retain request/wait history in the private folder."""
    line = {"utc": datetime.now(timezone.utc).isoformat(), **record}
    with EVENTS.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(line, ensure_ascii=False) + "\n")
        stream.flush()
    event(record)


def saved_school(county, code, relative):
    """Never reuse a page unless its source identity and both hashes verify."""
    path = PAGES / f"{county}_{code}.json"
    if not path.exists():
        return None
    kind = json.loads(path.read_text(encoding="utf-8")).get("kind")
    if kind not in ACCEPTED_KINDS:
        raise ValueError(f"Unexpected source kind in saved checkpoint: {county}/{code}")
    page = verified_page(path, relative=relative, kind=kind)
    if not REQUIRED_HEADERS.issubset(page["headers"]):
        raise ValueError(f"Missing score or name column in saved checkpoint: {county}/{code}")
    return page


def expected_schools(counties):
    """Enumerate only codes and links published in saved Ministry directories."""
    result = []
    for county in counties:
        schools = school_directory(county)
        for code, (_name, relative) in sorted(schools.items(), key=lambda item: int(item[0])):
            result.append((county, code, relative))
    return result


def prior_status():
    if not STATUS.exists():
        return {}
    with STATUS.open(newline="", encoding="utf-8") as stream:
        return {(row["county"], row["gymnasium_code"]): row
                for row in csv.DictReader(stream)}


def status_rows(schools, prior):
    """Build a full inventory; a previous error stays open until a page verifies."""
    rows = []
    for county, code, relative in schools:
        page = saved_school(county, code, relative)
        previous = prior.get((county, code), {})
        if previous.get("status") == "saved_verified" and page is None:
            raise ValueError(f"Previously verified checkpoint is missing: {county}/{code}")
        rows.append({
            "county": county,
            "gymnasium_code": code,
            "status": "saved_verified" if page else previous.get("status", "not_yet_attempted"),
            "applicant_rows": page["row_count"] if page else "",
            "last_http_status": "" if page else previous.get("last_http_status", ""),
        })
    return rows


def write_status(rows):
    """Atomic, name-free progress file for the Cursor notebook's status cell."""
    # A scoped AR/SB run must not erase CS/GL/TL progress in a shared file.
    merged = prior_status()
    merged.update({(row["county"], row["gymnasium_code"]): row for row in rows})
    save_csv(STATUS, FIELDS, [merged[key] for key in sorted(merged)])


def print_progress(rows, counties, new_pages, attempts):
    for county in counties:
        local = [row for row in rows if row["county"] == county]
        complete = sum(row["status"] == "saved_verified" for row in local)
        unresolved = sum(row["status"].startswith("unresolved") for row in local)
        say(f"PROGRESS {county}: {complete}/{len(local)} gymnasium views verified; "
            f"{unresolved} unresolved; {len(local) - complete - unresolved} not yet attempted")
    say(f"THIS RUN: {new_pages} newly saved pages; {attempts} school addresses attempted")


def source_url_is_correct(effective, county, code):
    """A successful HTTP response must still belong to the requested school."""
    url = urllib.parse.unquote(effective)
    return (bool(re.search(rf"(?:[?&-])cj={re.escape(county)}(?:[&.]|$)", url, re.I))
            and bool(re.search(rf"(?:[?&-])cs={re.escape(code)}(?:[&.]|$)", url, re.I)))


def fetch_with_429_cooldowns(client, requested, label, cooldowns):
    """Wait 600s, then 1500s on consecutive 429s; stop after a third."""
    result = client.get(requested, request_label=label)
    if result is not None or client.last_status != 429:
        return result, False
    show_429_response(client, label)
    for retry_number, seconds in enumerate(cooldowns, 1):
        persist_429_cooldown(client, seconds=seconds)
        say(f"RETRY {retry_number}/2 for {label} after at least {seconds} seconds")
        result = client.get(requested, request_label=f"{label} retry {retry_number} after 429")
        if result is not None or client.last_status != 429:
            return result, False
        show_429_response(client, label)
    # If restarted immediately, do not turn a three-429 stop into a rapid retry.
    persist_429_cooldown(client, seconds=cooldowns[-1])
    return None, True


def main(argv=None):
    global STATUS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="contact Wayback for missing pages")
    parser.add_argument("--counties", nargs="+", choices=COUNTIES, default=list(COUNTIES))
    parser.add_argument("--status-file", default=str(DEFAULT_STATUS),
                        help="name-free progress CSV; use a separate file for an expansion")
    parser.add_argument("--max-new-pages", type=int, default=500,
                        help="stop after this many newly saved pages")
    parser.add_argument("--max-http-attempts", type=int, default=1500,
                        help="bound HTTP requests, including redirects and failed attempts")
    parser.add_argument("--max-hours", type=float, default=12.0,
                        help="maximum running time including server cooldowns")
    parser.add_argument("--min-interval-seconds", type=float, default=22.0)
    parser.add_argument("--max-interval-seconds", type=float, default=50.0)
    parser.add_argument("--first-429-cooldown-seconds", type=int, default=600)
    parser.add_argument("--second-429-cooldown-seconds", type=int, default=1500)
    parser.add_argument("--server-error-wait-seconds", type=float, default=10.0)
    args = parser.parse_args(argv)
    STATUS = Path(args.status_file).expanduser().resolve()
    if args.max_new_pages < 1 or args.max_http_attempts < 1 or args.max_hours <= 0:
        parser.error("all run limits must be positive")
    if (args.min_interval_seconds <= 0 or args.max_interval_seconds < args.min_interval_seconds
            or args.first_429_cooldown_seconds <= 0 or args.second_429_cooldown_seconds <= 0
            or args.server_error_wait_seconds < 10):
        parser.error("Require positive pace/cooldowns, max interval >= min, and server wait >= 10s")
    counties = tuple(dict.fromkeys(args.counties))
    schools = expected_schools(counties)
    prior = prior_status()
    rows = status_rows(schools, prior)
    total_saved = sum(row["status"] == "saved_verified" for row in rows)
    say(f"SOURCE-ONLY VIEW INVENTORY: {total_saved}/{len(rows)} already verified "
        f"for {', '.join(counties)}; {len(rows) - total_saved} still to obtain or retry")
    print_progress(rows, counties, new_pages=0, attempts=0)
    if not args.run:
        say("PREVIEW ONLY: no Wayback request and no status file written")
        return

    PRIVATE.mkdir(parents=True, exist_ok=True)
    PAGES.mkdir(parents=True, exist_ok=True)
    os.chmod(PRIVATE, 0o700)
    os.chmod(PAGES, 0o700)
    write_status(rows)
    client = ArchiveClient(
        PRIVATE, emit, archive_use_acknowledged=True,
        initial_interval_seconds=args.min_interval_seconds,
        minimum_interval_seconds=args.min_interval_seconds,
        maximum_interval_seconds=args.max_interval_seconds, max_runtime_hours=args.max_hours,
        max_http_attempts=args.max_http_attempts,
        reuse_recorded_robots_absence=True, random_adaptive_fraction=0.10,
        pace_redirects=True, jitter_fraction=0.0,
    )
    # Honor an old generic 429 deadline already saved by the pilot client.
    persist_429_cooldown(client, previous_state=True)
    new_pages = attempts = 0
    for index, (county, code, relative) in enumerate(schools):
        row = rows[index]
        if row["status"] == "saved_verified":
            continue
        if new_pages >= args.max_new_pages:
            say("RUN LIMIT: new-page cap reached; remaining school codes stay unresolved/open")
            break
        label = f"{county} gymnasium {code}"
        requested = archive_url(relative)
        attempts += 1
        say(f"REQUEST {label}: {requested}")
        try:
            result, third_429 = fetch_with_429_cooldowns(
                client, requested, label,
                (args.first_429_cooldown_seconds, args.second_429_cooldown_seconds),
            )
        except RetrievalStopped as exc:
            row["status"] = "unresolved_client_stop"
            row["last_http_status"] = client.last_status or ""
            write_status(rows)
            say(f"SAFE STOP at {label}: {exc}; all saved pages remain available")
            break
        if result is not None:
            raw, effective = result
            if not source_url_is_correct(effective, county, code):
                raise ValueError(f"{label}: archive returned a different county or gymnasium")
            payload = _payload(relative, raw, effective, kind="origin_school_candidates")
            if not REQUIRED_HEADERS.issubset(payload["headers"]):
                raise ValueError(f"{label}: expected applicant/score columns are absent")
            target = PAGES / f"{county}_{code}.json"
            if target.exists():
                raise ValueError(f"{label}: existing checkpoint must not be overwritten")
            atomic_json(target, payload)
            saved = saved_school(county, code, relative)
            row.update(status="saved_verified", applicant_rows=saved["row_count"],
                       last_http_status="")
            new_pages += 1
            say(f"NEW SOURCE SAVED {label}: {saved['row_count']} applicant rows; "
                f"{total_saved + new_pages}/{len(rows)} verified")
        else:
            row["status"] = f"unresolved_http_{client.last_status}" if client.last_status else "unresolved_network"
            row["last_http_status"] = client.last_status or ""
            say(f"UNRESOLVED {label}: HTTP {client.last_status} or network error; "
                "no missing-student conclusion")
        write_status(rows)
        if third_429:
            say("SAFE STOP after three consecutive HTTP 429 responses; retry later")
            break
        if client.last_status in (401, 403, 451):
            say(f"SAFE STOP after HTTP {client.last_status}; no further requests this run")
            break
        if client.last_status in (500, 503):
            say(f"WAIT {args.server_error_wait_seconds:.1f}s after HTTP {client.last_status} "
                "before another request")
            time.sleep(args.server_error_wait_seconds)
        if attempts % 25 == 0:
            print_progress(rows, counties, new_pages, attempts)
    print_progress(rows, counties, new_pages, attempts)
    say(f"STATUS FILE: {STATUS}")
    say("Acquisition only. No student outcomes, peer measures, or HERO curves were calculated.")


if __name__ == "__main__":
    main()
