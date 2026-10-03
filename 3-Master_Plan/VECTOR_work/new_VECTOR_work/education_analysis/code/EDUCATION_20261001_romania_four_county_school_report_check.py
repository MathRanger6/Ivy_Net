"""Resumable, source-only check of the frozen CS/GL/TL school-report sample.

Run from a notebook after the ongoing national acquisition is stopped. All
raw pages and identifiable rows stay in ~/Desktop/VECTOR_temp; only name-free
counts go to the research workspace. A failed request remains unresolved.
This script does not calculate peer metrics, outcomes, or HERO curves.
"""

import argparse
import base64
import csv
import hashlib
import json
import os
import re
import time
import urllib.parse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from romania_archive_retrieval import ArchiveClient, RetrievalStopped
from EDUCATION_20260930_romania_2001_national_acquisition import (
    CACHE as NATIONAL_CACHE, _payload, archive_url, atomic_json,
)
from EDUCATION_20261001_romania_offline_county_source_readiness import saved_rows, signature
from EDUCATION_20261001_romania_four_county_school_sample import OUT, FIELDS
from EDUCATION_20261001_romania_origin_school_name_audit import OUT as FIRST_OUT, save_csv

PRIVATE = Path.home() / "Desktop/VECTOR_temp/romania_2001_four_county_school_source_pilot"
PAGES = PRIVATE / "school_reports"
SAMPLE = OUT / "frozen_school_report_sample.csv"
LABEL_REVIEW = FIRST_OUT / "school_label_review.csv"
COUNT_FIELDS = [
    "county", "school_code", "sample_stratum", "county_listed_applicants",
    "school_report_applicants", "shared_name_score_occurrences",
    "school_report_extra_to_county_list", "county_list_missing_from_school_report",
    "source_status",
]


def say(message):
    print(f"{datetime.now().astimezone():%Y-%m-%d %H:%M:%S %Z} | {message}", flush=True)


def event(record):
    kind = record.get("kind")
    if kind == "retrieval_wait":
        say(f"WAIT {record['seconds']}s before next archive request; {record.get('reason', 'pacing')}; "
            f"resume expected {record.get('expected_resume_at', 'unknown')}")
    elif kind == "retrieval_wait_remaining" and int(round(record["seconds"])) % 60 == 0:
        say(f"COOLDOWN: {record['seconds']}s remaining; "
            f"resume expected {record.get('expected_resume_at', 'unknown')}")
    elif kind == "http_attempt":
        say(f"ARCHIVE RESPONSE {record.get('status') or record.get('error')} for "
            f"{record.get('request_label', 'school report')}")
    elif kind == "adaptive_pace":
        say(f"PACE {record.get('direction')}: {record.get('new_seconds', '?')}s; "
            f"{record.get('reason', 'archive feedback')}")


def show_429_response(client, label):
    """Print the complete returned headers and text body without truncation."""
    say(f"FULL HTTP 429 RESPONSE for {label}; requested URL: {client.last_url}")
    print("HTTP status: 429\nResponse headers:", flush=True)
    for name, value in client.last_response_headers.items():
        print(f"{name}: {value}", flush=True)
    content_type = next((value for name, value in client.last_response_headers.items()
                         if name.lower() == "content-type"), "")
    match = re.search(r"charset\s*=\s*['\"]?([^;\s'\"]+)", content_type, re.I)
    encoding = match.group(1) if match else "utf-8"
    try:
        body = client.last_response_body.decode(encoding, errors="replace")
    except LookupError:
        body = client.last_response_body.decode("utf-8", errors="replace")
    print(f"Response body ({len(client.last_response_body)} bytes):\n"
          f"{body if body else '[empty body]'}\nEND HTTP 429 RESPONSE", flush=True)


def persist_429_cooldown(client, *, seconds=600, previous_state=False):
    """Keep a 429 no-request deadline across notebook restarts."""
    deadline = time.time() + seconds
    if previous_state and client.state_path.exists():
        state = json.loads(client.state_path.read_text())
        if state.get("reason") == "HTTP 429" and state.get("saved_utc"):
            saved = datetime.fromisoformat(state["saved_utc"])
            deadline = saved.timestamp() + seconds
        else:
            return
    client.not_before = max(client.not_before, deadline)
    client._save_state(f"pilot HTTP 429: {seconds}-second cooldown")
    resume = datetime.fromtimestamp(client.not_before, timezone.utc).astimezone()
    say(f"HTTP 429 COOLDOWN ({seconds}s): no new request before "
        f"{resume:%Y-%m-%d %H:%M:%S %Z}")


def verified_private_page(row):
    path = PAGES / f"{row['county']}_{row['source_school_code']}.json"
    if not path.exists():
        return None
    payload = json.loads(path.read_text())
    if payload.get("relative_source") != row["school_report_relative_url"]:
        raise ValueError(f"{path.name}: source URL changed")
    rows = payload.get("rows")
    if not isinstance(rows, list) or payload.get("row_count") != len(rows):
        raise ValueError(f"{path.name}: saved row count changed")
    expected = hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()
    if expected != payload.get("rows_sha256"):
        raise ValueError(f"{path.name}: saved source row hash changed")
    raw = base64.b64decode(payload.get("raw_html_base64", ""), validate=True)
    if hashlib.sha256(raw).hexdigest() != payload.get("raw_html_sha256"):
        raise ValueError(f"{path.name}: saved raw-page hash changed")
    return payload


def county_school_keys():
    """Use only unambiguous school-code links from the prior name audit."""
    names_to_codes = {}
    with LABEL_REVIEW.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            if row["classification"] == "direct_whole_name_match":
                names_to_codes[(row["county"], row["printed_school_label"])] = row["directory_code_candidates"]
    all_keys = defaultdict(Counter)
    for county in ("CS", "GL", "TL"):
        manifest = json.loads((NATIONAL_CACHE / "county_manifests" / f"{county}.json").read_text())
        for row in saved_rows(manifest, "candidate_roster"):
            code = names_to_codes.get((county, row.get("Şcoală", "").strip()))
            key = signature(row)
            if code and key:
                all_keys[(county, code)][key] += 1
    return all_keys


def compare(row, payload, county_keys):
    school_keys = Counter(key for source_row in payload["rows"]
                          if (key := signature(source_row)))
    if sum(school_keys.values()) != len(payload["rows"]):
        raise ValueError(f"{row['county']} school {row['source_school_code']}: missing name or score")
    local = county_keys[(row["county"], row["source_school_code"])]
    shared = sum((school_keys & local).values())
    return {
        "county": row["county"], "school_code": row["source_school_code"],
        "sample_stratum": row["sample_stratum"],
        "county_listed_applicants": sum(local.values()),
        "school_report_applicants": len(payload["rows"]),
        "shared_name_score_occurrences": shared,
        "school_report_extra_to_county_list": sum((school_keys - local).values()),
        "county_list_missing_from_school_report": sum((local - school_keys).values()),
        "source_status": "verified_saved_source",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="request missing frozen school reports")
    parser.add_argument("--max-new-pages", type=int, default=36,
                        help="new source pages allowed in this run; saved pages are reused")
    parser.add_argument("--max-hours", type=float, default=3.0)
    args = parser.parse_args(argv)
    with SAMPLE.open(newline="", encoding="utf-8") as stream:
        sample = list(csv.DictReader(stream))
    if len(sample) != 36 or any(set(row) != set(FIELDS) for row in sample):
        raise ValueError("Frozen sample is missing or changed; stop before requesting pages")
    say(f"SOURCE-ONLY school check: {len(sample)} reports; {args.max_new_pages} new-page cap")
    if not args.run:
        say("PREVIEW ONLY: no archive requests. Use --run after national acquisition stops.")
        return
    if args.max_new_pages < 1:
        parser.error("--max-new-pages must be positive")
    PRIVATE.mkdir(parents=True, exist_ok=True)
    PAGES.mkdir(parents=True, exist_ok=True)
    os.chmod(PRIVATE, 0o700)
    os.chmod(PAGES, 0o700)
    client = ArchiveClient(
        PRIVATE, event, archive_use_acknowledged=True,
        initial_interval_seconds=22.0, minimum_interval_seconds=22.0,
        maximum_interval_seconds=50.0, max_runtime_hours=args.max_hours,
        reuse_recorded_robots_absence=True,
        random_adaptive_fraction=0.10, pace_redirects=True, jitter_fraction=0.0,
    )
    # A 429 from the previous version saved only a five-minute floor. Raise
    # that original event's deadline to ten minutes without restarting its clock.
    persist_429_cooldown(client, previous_state=True)
    county_keys = county_school_keys()
    output_rows = []
    new_pages = 0
    for position, row in enumerate(sample, 1):
        label = f"{row['county']} school {row['source_school_code']} ({position}/{len(sample)})"
        payload = verified_private_page(row)
        stop_after_429 = False
        if payload is None and new_pages < args.max_new_pages:
            say(f"REQUEST {label}: school-specific applicant source page")
            try:
                result = client.get(archive_url(row["school_report_relative_url"]), request_label=label)
                if result is None and client.last_status == 429:
                    show_429_response(client, label)
                    for retry_number, cooldown_seconds in enumerate((600, 1500), 1):
                        persist_429_cooldown(client, seconds=cooldown_seconds)
                        say(f"RETRY {retry_number}/2 for {label} after the "
                            f"{cooldown_seconds}-second cooldown")
                        result = client.get(archive_url(row["school_report_relative_url"]),
                                            request_label=f"{label} retry {retry_number} after 429")
                        if result is None and client.last_status == 429:
                            show_429_response(client, label)
                            if retry_number == 2:
                                # Leave a safe deadline in place if the notebook is restarted.
                                persist_429_cooldown(client, seconds=1500)
                                stop_after_429 = True
                        else:
                            break
            except RetrievalStopped as exc:
                say(f"STOPPED by archive client: {exc}; saved pages remain available")
                result = None
                output_rows.append({"county": row["county"], "school_code": row["source_school_code"],
                                    "sample_stratum": row["sample_stratum"],
                                    "county_listed_applicants": row["applicants_listed_in_county_report"],
                                    "school_report_applicants": "", "shared_name_score_occurrences": "",
                                    "school_report_extra_to_county_list": "",
                                    "county_list_missing_from_school_report": "",
                                    "source_status": "unresolved_client_stop"})
                save_csv(OUT / "sample_source_comparison_counts.csv", COUNT_FIELDS, output_rows)
                break
            if result is not None:
                raw, effective = result
                effective_source = urllib.parse.unquote(effective)
                if not re.search(rf"(?:[?&-])cs={re.escape(row['source_school_code'])}(?:[&.]|$)",
                                 effective_source, re.I):
                    raise ValueError(f"{label}: archive redirected to a different school code")
                parsed = _payload(row["school_report_relative_url"], raw, effective,
                                  kind="sampled_origin_school_candidates")
                if not {"Nume", "Medie Admitere"}.issubset(parsed["headers"]):
                    raise ValueError(f"{label}: unexpected source table; page not accepted")
                target = PAGES / f"{row['county']}_{row['source_school_code']}.json"
                atomic_json(target, parsed)
                payload = verified_private_page(row)
                new_pages += 1
                say(f"NEW SOURCE SAVED {label}: {payload['row_count']} applicant rows")
            else:
                say(f"UNRESOLVED {label}: {client.last_status or client.last_error}; no absence inferred")
                if client.last_status in (500, 503):
                    say(f"WAIT 10s after HTTP {client.last_status} for server recovery")
                    time.sleep(10)
        if payload is not None:
            checked = compare(row, payload, county_keys)
            output_rows.append(checked)
            say(f"CHECKED {label}: {checked['school_report_applicants']} school-report applicants; "
                f"{checked['school_report_extra_to_county_list']} absent from same-county list")
        elif len(output_rows) < position:
            output_rows.append({
                "county": row["county"], "school_code": row["source_school_code"],
                "sample_stratum": row["sample_stratum"],
                "county_listed_applicants": row["applicants_listed_in_county_report"],
                "school_report_applicants": "", "shared_name_score_occurrences": "",
                "school_report_extra_to_county_list": "",
                "county_list_missing_from_school_report": "",
                "source_status": "unresolved_source_page",
            })
        save_csv(OUT / "sample_source_comparison_counts.csv", COUNT_FIELDS, output_rows)
        if stop_after_429:
            say("STOPPING THIS PASS after a third consecutive HTTP 429; "
                "leave remaining schools unresolved")
            break
    complete = sum(row["source_status"] == "verified_saved_source" for row in output_rows)
    say(f"PASS ENDED: {complete}/{len(sample)} sampled school reports verified; "
        f"{new_pages} newly saved this run. Unchecked reports remain unresolved.")


if __name__ == "__main__":
    main()
