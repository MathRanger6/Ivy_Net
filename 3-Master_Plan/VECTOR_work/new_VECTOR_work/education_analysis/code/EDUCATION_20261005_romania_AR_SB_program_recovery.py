"""Recover the five AR/SB program lists needed to resolve placement labels.

Charles starts acquisition from the existing notebook. Importing, previewing,
and reconciling are offline. Raw student records stay in the Desktop cache;
only progress counts are written to the repository. Failed sources stay open.
"""

import base64
import json
import re
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import unquote

from EDUCATION_20260930_romania_2001_national_acquisition import (
    CACHE, _links, _payload, archive_url, atomic_json, verified_page,
)
from EDUCATION_20261001_romania_four_county_school_report_check import (
    PRIVATE, persist_429_cooldown, say,
)
from EDUCATION_20261002_romania_three_county_gymnasium_acquisition import (
    emit, fetch_with_429_cooldowns,
)
from romania_archive_retrieval import ArchiveClient, RetrievalStopped

TARGETS = {"AR": ("x69", "x70"), "SB": ("x93", "x94", "x95")}
PAGES = PRIVATE / "program_identity_reports"
OUT = Path(__file__).resolve().parents[1] / "outputs/romania_2001_county_expansion_20261004"
STATUS = OUT / "targeted_program_recovery_status.json"


def code_in_url(url, county, code=None):
    """Check printed source parameters, including after a Wayback redirect."""
    url = unquote(url)
    county_ok = re.search(rf"(?:[?&-])cj={county}(?:[&.]|$)", url, re.I)
    code_ok = code is None or re.search(
        rf"(?:[?&-])cs={code.lstrip('x')}(?:[&.]|$)", url, re.I)
    return bool(county_ok and code_ok)


def index_relative(county):
    """Read the exact program-menu link already saved from the Ministry site."""
    menu = json.loads((CACHE / "county_menus" / f"{county}.json").read_text())
    links = [link for link in _links(base64.b64decode(menu["raw_html_base64"]))
             if "raport_specializari_adm.asp" in link and code_in_url(link, county)]
    if len(links) != 1:
        raise ValueError(f"{county}: expected one published program-menu URL")
    return links[0]


def checkpoint(county, code=None):
    return PAGES / f"{county}_{code or 'program_menu'}.json"


def program_relative(index, county, code):
    links = [link for link in index["discovered_links"]
             if "raport_admisi_per_liceu.asp" in link and code_in_url(link, county, code)]
    if len(links) != 1:
        raise ValueError(f"{county} {code}: expected one exact program link; found {len(links)}")
    return links[0]


def check_payload(payload, county, code=None, admitted=None):
    if not code_in_url(payload["effective_url"], county, code):
        raise ValueError(f"{county} {code}: returned URL belongs to a different source")
    endpoint = "raport_admisi_per_liceu.asp" if code else "raport_specializari_adm.asp"
    if endpoint not in unquote(payload["effective_url"]):
        raise ValueError(f"{county} {code}: archive returned the wrong kind of webpage")
    if code:
        if not {"Nume", "Medie Admitere"}.issubset(payload["headers"]):
            raise ValueError(f"{county} {code}: student-name/admission-score columns absent")
        if payload["row_count"] != admitted:
            raise ValueError(f"{county} {code}: {payload['row_count']} rows; occupancy expects {admitted}")
    return payload


def saved(county, relative, code=None, admitted=None):
    payload = verified_page(checkpoint(county, code), relative=relative,
                            kind="destination_program_students" if code else "destination_program_menu")
    return check_payload(payload, county, code, admitted) if payload else None


def program_counts(county):
    # Local import avoids making the shared reconciliation module depend on
    # acquisition at import time. No network request occurs here.
    from EDUCATION_20261003_romania_four_county_program_identity_gate import source_programs
    manifest = json.loads((CACHE / "county_manifests" / f"{county}.json").read_text())
    programs = source_programs(manifest, county)
    counts = {code: admitted for code, _, _, admitted, _, _ in programs}
    return {code: counts[code] for code in TARGETS[county]}


def preview():
    """Show the seven-source job without sending requests or writing files."""
    result = []
    for county in TARGETS:
        index = saved(county, index_relative(county))
        say(f"{county}: program menu {'saved' if index else 'still needed'}")
        for code, admitted in program_counts(county).items():
            page = saved(county, program_relative(index, county, code), code, admitted) if index else None
            row = dict(county=county, program=code, expected_students=admitted,
                       state="saved_verified" if page else "unresolved_source_needed")
            result.append(row)
            say(f"{county} {code}: {admitted} expected students; {row['state']}")
    say("PREVIEW ONLY: no archive requests. Up to two menus plus five program lists are needed.")
    return result


def run(*, min_interval=22.0, max_interval=50.0, first_429=600,
        second_429=1500, server_error_wait=10.0, max_hours=2.0, max_http_attempts=80):
    """One bounded pass; rerunning skips every verified saved page."""
    if not (0 < min_interval <= max_interval and first_429 > 0 and second_429 > 0
            and server_error_wait >= 10 and max_hours > 0 and max_http_attempts > 0):
        raise ValueError("Invalid pacing settings; server-error wait must be at least 10 seconds")
    PAGES.mkdir(parents=True, exist_ok=True, mode=0o700)
    # Reuse the school downloader's pacing state, so restarting does not erase
    # a server cooldown. Run only one Wayback notebook at a time.
    client = ArchiveClient(
        PRIVATE, emit, archive_use_acknowledged=True,
        initial_interval_seconds=min_interval, minimum_interval_seconds=min_interval,
        maximum_interval_seconds=max_interval, max_runtime_hours=max_hours,
        max_http_attempts=max_http_attempts, reuse_recorded_robots_absence=True,
        random_adaptive_fraction=0.10, pace_redirects=True, jitter_fraction=0.0,
    )
    persist_429_cooldown(client, previous_state=True)
    status = json.loads(STATUS.read_text()) if STATUS.exists() else {}

    def record(label, state, **details):
        status[label] = dict(state=state, updated=datetime.now().astimezone().isoformat(), **details)
        atomic_json(STATUS, status)

    def obtain(county, relative, code=None, admitted=None):
        label = f"{county}/{code or 'program_menu'}"
        page = saved(county, relative, code, admitted)
        if page:
            say(f"VERIFIED SAVED {label}: {page['row_count']} rows; no download")
            record(label, "saved_verified", rows=page["row_count"])
            return page
        requested = archive_url(relative)
        say(f"REQUEST {label}: {requested}")
        record(label, "unresolved_request_started", url=requested)
        result, third_429 = fetch_with_429_cooldowns(client, requested, label, (first_429, second_429))
        if result is None:
            record(label, "unresolved", url=requested, http_status=client.last_status)
            say(f"UNRESOLVED {label}: HTTP {client.last_status}; retained for a later retry")
            if third_429 or client.last_status in (401, 403, 451):
                raise RetrievalStopped(f"Access/server pause at {label}; retry later")
            if client.last_status in (500, 503):
                resume = datetime.now().astimezone() + timedelta(seconds=server_error_wait)
                say(f"WAIT {server_error_wait:.1f}s: HTTP {client.last_status} recovery after {label}; "
                    f"resume expected {resume:%Y-%m-%d %H:%M:%S %Z}")
                client._sleep(server_error_wait, reason=f"HTTP {client.last_status} recovery after {label}")
            return None
        raw, effective = result
        try:
            page = _payload(relative, raw, effective,
                            kind="destination_program_students" if code else "destination_program_menu")
            check_payload(page, county, code, admitted)
        except ValueError as exc:
            record(label, "unresolved_source_check", url=requested, reason=str(exc))
            say(f"UNRESOLVED {label}: {exc}; no student labels assigned")
            return None
        atomic_json(checkpoint(county, code), page)
        record(label, "saved_verified", rows=page["row_count"])
        say(f"NEW DOWNLOAD SAVED {label}: {page['row_count']} rows; checkpoint complete")
        return page

    try:
        for county in TARGETS:
            index = obtain(county, index_relative(county))
            if index is None:
                continue
            for code, admitted in program_counts(county).items():
                try:
                    relative = program_relative(index, county, code)
                except ValueError as exc:
                    record(f"{county}/{code}", "unresolved_source_link", reason=str(exc))
                    say(str(exc))
                    continue
                obtain(county, relative, code, admitted)
    except (RetrievalStopped, KeyboardInterrupt) as exc:
        say(f"RUN STOPPED: {type(exc).__name__}: {exc}; saved pages retained")
    say(f"Acquisition pass finished. Progress: {STATUS}")
    return preview()


def attach_verified_program_codes(county, reports, programs):
    """Resolve codes only when the complete ambiguous group reconciles exactly.

    Count agreement alone is insufficient: every program-list student must
    match one county-placement row, and the union must equal the entire group.
    Missing pages leave all original rows unchanged. Names never leave memory.
    """
    if county not in TARGETS:
        return reports
    from EDUCATION_20261002_romania_full_gymnasium_offline_reconciliation import name_score
    from EDUCATION_20261003_romania_four_county_program_identity_gate import clean
    index = saved(county, index_relative(county))
    if index is None:
        return reports
    directory = {code: (program, admitted) for code, program, _, admitted, _, _ in programs}
    identities = {tuple(clean(directory[code][0][field]) for field in ("Liceu", "Profil", "Specializare"))
                  for code in TARGETS[county]}
    if len(identities) != 1:
        raise ValueError(f"{county}: targeted program group changed; review before reconciling")
    identity = next(iter(identities))
    all_codes = {code for code, (program, _) in directory.items()
                 if tuple(clean(program[field]) for field in ("Liceu", "Profil", "Specializare")) == identity}
    if all_codes != set(TARGETS[county]):
        raise ValueError(f"{county}: target list does not cover the full ambiguous program group")
    code_by_person = {}
    for code in TARGETS[county]:
        page = saved(county, program_relative(index, county, code), code, directory[code][1])
        if page is None:
            say(f"{county}: program identities remain unresolved until all targeted pages are saved")
            return reports
        for row in page["rows"]:
            key = name_score(row)
            if key is None or key in code_by_person:
                raise ValueError(f"{county}: blank/duplicate student match in program lists")
            code_by_person[key] = code
    expected = []
    for row in reports:
        school = clean(row.get("Liceu"))
        suffix = f" / {county}"
        if school.endswith(suffix):
            school = school[:-len(suffix)]
        if (school, clean(row.get("Profil")), clean(row.get("Specializare"))) == identity:
            expected.append(name_score(row))
    keys = [name_score(row) for row in reports]
    if None in expected or Counter(expected) != Counter(code_by_person.keys()):
        raise ValueError(f"{county}: program lists do not exactly partition the county placement group")
    if any(Counter(keys)[key] != 1 for key in code_by_person):
        raise ValueError(f"{county}: program student does not match exactly one county placement")
    say(f"{county}: RESOLVED {len(code_by_person)} exact program identities; enrollment and student lists agree")
    return [{**row, "__source_program_code": code_by_person[key]} if key in code_by_person else row
            for row, key in zip(reports, keys)]
