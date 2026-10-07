"""Recover the *distinct* 2001 school-result and cross-county Ministry views.

SOURCE ONLY: no matching, analysis, or outcome inference. Raw identifiable pages
are saved under ~/Desktop/VECTOR_temp, never in Dropbox. Every page is saved
immediately with source URL, raw HTML, rows, and verification hashes. Failed
URLs remain in a private unresolved queue and are retried on a later run.
Without --run, only the saved Ministry county menus are read.
"""

import argparse
import base64
import hashlib
import json
import math
import os
import re
import time
import urllib.parse
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from romania_archive_retrieval import ArchiveClient, RetrievalStopped
from EDUCATION_20260930_romania_2001_national_acquisition import (
    CACHE, _links, _payload, archive_url, atomic_json, verified_page,
)
from EDUCATION_20261001_romania_four_county_school_report_check import (
    event as archive_event, show_429_response,
)

PRIVATE = Path.home() / "Desktop/VECTOR_temp/romania_2001_school_results_incoming_v1"
PAGES = PRIVATE / "pages"
STATUS = PRIVATE / "status.json"
EVENTS = PRIVATE / "events.jsonl"
FAMILIES = {
    "school_results": ("raport_scoli_din_judet_tot.asp", "raport_total_per_scoala.asp"),
    "resident_candidates": ("raport_candidati.asp",),
    "incoming_candidates": ("raport_candidati_altejud_per_judet.asp",),
    "incoming_admitted": ("raport_admisi_altejud_per_judet.asp",),
    "incoming_rejected": ("raport_respinsi_altejud_per_judet.asp",),
}
COUNTIES = tuple(row["county_code"] for row in
                 json.loads((CACHE / "county_directory.json").read_text())["counties"])


def say(message):
    print(f"{datetime.now().astimezone():%Y-%m-%d %H:%M:%S %Z} | {message}", flush=True)


def emit(record):
    with EVENTS.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"utc": datetime.now(timezone.utc).isoformat(), **record}) + "\n")
        stream.flush()
    archive_event(record)


def menu_seeds(county, family):
    """Take report URLs from the Ministry's *saved* county menu, not guesses."""
    menu = json.loads((CACHE / "county_menus" / f"{county}.json").read_text())
    raw = base64.b64decode(menu["raw_html_base64"], validate=True)
    if hashlib.sha256(raw).hexdigest() != menu["raw_html_sha256"]:
        raise ValueError(f"{county}: saved county menu hash changed")
    stem = FAMILIES[family][0]
    links = [link for link in _links(raw) if link.lower().startswith(stem.lower())]
    if len(links) != 1:
        raise ValueError(f"{county}: expected exactly one {family} menu link; found {len(links)}")
    return links


def belongs(relative, county, family):
    """Allow only the selected county and exact report family."""
    allowed = FAMILIES[family]
    if not any(relative.lower().startswith(stem.lower()) for stem in allowed):
        return False
    return bool(re.search(rf"(?:[?&-])cj={re.escape(county)}(?:[&.]|$)",
                          urllib.parse.unquote(relative), re.I))


def page_path(county, family, relative):
    digest = hashlib.sha256(relative.encode()).hexdigest()[:20]
    return PAGES / county / family / f"{digest}.json"


def checked_page(county, family, relative):
    return verified_page(page_path(county, family, relative),
                         relative=relative, kind=family)


def load_status():
    return json.loads(STATUS.read_text()) if STATUS.exists() else {"counties": {}}


def save_status(status):
    atomic_json(STATUS, status)


def family_state(status, county, family):
    return status["counties"].setdefault(county, {}).setdefault(family, {
        "discovered": [], "unresolved": {}, "saved_pages": 0, "saved_rows": 0,
    })


def discover(state, links, county, family):
    known = set(state["discovered"])
    for relative in links:
        if belongs(relative, county, family) and relative not in known:
            state["discovered"].append(relative)
            known.add(relative)


def update_projection(state, family, relative, page):
    """Use the report's own range/total line, never a guessed page count.

    For a paginated candidate list, `de la 1 la 500 din 1317` tells us
    1,317 source rows and 500 per full page, hence three expected pages.
    For the school-results directory, every printed school has its own link;
    count the directory itself plus its linked school reports. A school with
    additional pagination may increase that lower bound when links appear.
    """
    raw = base64.b64decode(page["raw_html_base64"]).decode("cp1250", errors="replace")
    match = re.search(r"de\s+la\s+(\d+)\s+la\s+(\d+)\s+din\s+(\d+)", raw, re.I)
    if not match:
        return
    first, last, total = map(int, match.groups())
    if family == "school_results" and relative.lower().startswith("raport_scoli_din_judet_tot"):
        # The directory and one page per listed school are the minimum work.
        school_links = [link for link in page["discovered_links"]
                        if link.lower().startswith("raport_total_per_scoala.asp")]
        state["projected_pages"] = 1 + len(school_links)
        state["projected_schools"] = total
        state["projection_basis"] = "source school-directory links; minimum if a school report paginates"
    elif family != "school_results" and first == 1 and last >= first:
        page_size = last - first + 1
        state["projected_pages"] = max(1, math.ceil(total / page_size))
        state["projected_records"] = total
        state["projection_basis"] = f"source range 1–{last} of {total}"


def progress_text(county, family, state):
    """Explain both known links and projected total in every progress line."""
    saved = state["saved_pages"]
    known = len(state["discovered"])
    projected = state.get("projected_pages")
    if projected is None:
        scale = f"{saved} saved / {known} URLs known so far; total pages not known yet"
    else:
        projected = max(projected, known)
        scale = f"{saved}/{projected} projected pages saved"
    if family == "school_results":
        detail = (f"; {state['projected_schools']} school reports listed"
                  if "projected_schools" in state else "")
    else:
        detail = (f"; {state['saved_rows']}/{state['projected_records']} source rows saved"
                  if "projected_records" in state else f"; {state['saved_rows']} source rows saved")
    return (f"{county} {family}: {scale}{detail}; "
            f"{len(state['unresolved'])} unresolved URLs")


def recount_saved(state, county, family):
    """Recover counts and newly linked URLs after any interrupted notebook run."""
    index = 0
    pages = rows = 0
    while index < len(state["discovered"]):
        relative = state["discovered"][index]
        index += 1
        saved = checked_page(county, family, relative)
        if saved:
            pages += 1
            rows += saved["row_count"]
            discover(state, saved["discovered_links"], county, family)
            update_projection(state, family, relative, saved)
            state["unresolved"].pop(relative, None)
    state["saved_pages"] = pages
    state["saved_rows"] = rows


def verify_effective(effective, county, relative):
    """An HTTP 200 is insufficient if Wayback redirects to a different report."""
    decoded = urllib.parse.unquote(effective)
    stem = relative.split(".asp", 1)[0]
    if stem.lower() not in decoded.lower():
        return False
    requested_code = re.search(r"(?:[?&-])cs=([A-Za-z0-9]+)(?:[&.]|$)", relative, re.I)
    if requested_code and not re.search(rf"(?:[?&-])cs={re.escape(requested_code.group(1))}(?:[&.]|$)", decoded, re.I):
        return False
    return bool(re.search(rf"(?:[?&-])cj={re.escape(county)}(?:[&.]|$)", decoded, re.I))


def expected_columns(family, relative, headers):
    """Reject a Wayback error page or an unexpected Ministry report schema."""
    normalized = {
        "".join(c for c in unicodedata.normalize("NFKD", str(header).lower())
                if not unicodedata.combining(c)).replace("ş", "s").replace("ţ", "t")
        for header in headers
    }
    if family == "school_results" and relative.lower().startswith("raport_scoli_din_judet_tot"):
        required = {"cod scoala", "nume scoala"}
    elif family == "incoming_admitted":
        required = {"nume", "liceu", "medie admitere"}
    elif family == "incoming_rejected":
        required = {"nume", "medie admitere"}
    elif family == "school_results":
        required = {"nume", "liceu", "medie admitere"}
    else:
        required = {"nume", "medie admitere"}
    return required <= normalized


def wait_after_429(client, seconds):
    """Persist the no-request deadline across notebook restarts."""
    client.not_before = max(client.not_before, time.time() + seconds)
    client._save_state("HTTP 429")
    resume = datetime.fromtimestamp(client.not_before).astimezone()
    say(f"HTTP 429 cooldown: {seconds}s; no request before {resume:%Y-%m-%d %H:%M:%S %Z}")


def fetch(client, relative, label, args):
    """After 429: 600s, then 1500s, then stop; show full response."""
    for attempt in range(3):
        result = client.get(archive_url(relative), request_label=label)
        if result is not None or client.last_status != 429:
            return result, False
        show_429_response(client, label)
        if attempt == 2:
            wait_after_429(client, args.second_429_cooldown_seconds)
            return None, True
        seconds = (args.first_429_cooldown_seconds if attempt == 0
                   else args.second_429_cooldown_seconds)
        wait_after_429(client, seconds)
        say(f"RETRY {attempt + 1}/2 after HTTP 429: {label}")
    return None, True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="contact Wayback; preview otherwise")
    parser.add_argument("--counties", nargs="+", choices=COUNTIES, default=["B"])
    parser.add_argument("--families", nargs="+", choices=FAMILIES,
                        default=list(FAMILIES))
    parser.add_argument("--max-new-pages", type=int, default=300)
    parser.add_argument("--max-http-attempts", type=int, default=1000)
    parser.add_argument("--max-hours", type=float, default=12)
    parser.add_argument("--min-interval-seconds", type=float, default=22)
    parser.add_argument("--max-interval-seconds", type=float, default=50)
    parser.add_argument("--first-429-cooldown-seconds", type=int, default=600)
    parser.add_argument("--second-429-cooldown-seconds", type=int, default=1500)
    parser.add_argument("--server-error-wait-seconds", type=float, default=10)
    args = parser.parse_args(argv)
    if (args.max_new_pages < 1 or args.max_http_attempts < 1 or args.max_hours <= 0
            or args.min_interval_seconds <= 0
            or args.max_interval_seconds < args.min_interval_seconds
            or args.first_429_cooldown_seconds < 600
            or args.second_429_cooldown_seconds < 1500
            or args.server_error_wait_seconds < 10):
        parser.error("Invalid limits: 429 cooldowns must be at least 600/1500s; server wait at least 10s")
    counties = tuple(dict.fromkeys(args.counties))
    families = tuple(dict.fromkeys(args.families))
    status = load_status()
    for county in counties:
        for family in families:
            state = family_state(status, county, family)
            discover(state, menu_seeds(county, family), county, family)
            recount_saved(state, county, family)
            say(f"INVENTORY {progress_text(county, family, state)}")
    if not args.run:
        say("PREVIEW ONLY. No Wayback requests. Incoming series are best acquired first.")
        return
    PRIVATE.mkdir(parents=True, exist_ok=True)
    os.chmod(PRIVATE, 0o700)
    save_status(status)
    client = ArchiveClient(
        PRIVATE, emit, archive_use_acknowledged=True,
        initial_interval_seconds=args.min_interval_seconds,
        minimum_interval_seconds=args.min_interval_seconds,
        maximum_interval_seconds=args.max_interval_seconds,
        max_runtime_hours=args.max_hours,
        max_http_attempts=args.max_http_attempts,
        reuse_recorded_robots_absence=True,
        random_adaptive_fraction=0.10, pace_redirects=True, jitter_fraction=0.0,
    )
    new_pages = 0
    stopped = False
    for county in counties:
        for family in families:
            state = family_state(status, county, family)
            # We append newly discovered pagination/school links to this list.
            # Index traversal lets us reach them in the same run, then resume later.
            index = 0
            while index < len(state["discovered"]):
                relative = state["discovered"][index]
                index += 1
                if new_pages >= args.max_new_pages:
                    stopped = True
                    say("RUN LIMIT reached. Remaining URLs stay open for the next run.")
                    break
                saved = checked_page(county, family, relative)
                if saved:
                    discover(state, saved["discovered_links"], county, family)
                    continue
                label = f"{county}/{family}/{index}"
                say(f"REQUEST {label}: {archive_url(relative)}")
                try:
                    result, third_429 = fetch(client, relative, label, args)
                except RetrievalStopped as exc:
                    state["unresolved"][relative] = f"client stop: {exc}"
                    save_status(status)
                    say(f"SAFE STOP {label}: {exc}")
                    stopped = True
                    break
                if result is None:
                    state["unresolved"][relative] = f"HTTP {client.last_status or 'network error'}"
                    save_status(status)
                    say(f"UNRESOLVED {label}: {state['unresolved'][relative]}; preserved for retry")
                    if third_429 or client.last_status in (401, 403, 451):
                        stopped = True
                        break
                    if client.last_status in (500, 503):
                        say(f"WAIT at least {args.server_error_wait_seconds}s after HTTP "
                            f"{client.last_status} for {label}")
                        time.sleep(args.server_error_wait_seconds)
                    continue
                raw, effective = result
                if not verify_effective(effective, county, relative):
                    state["unresolved"][relative] = "archive redirected to different source URL"
                    save_status(status)
                    say(f"UNRESOLVED {label}: archive source URL mismatch")
                    continue
                try:
                    payload = _payload(relative, raw, effective, kind=family)
                except ValueError as exc:
                    state["unresolved"][relative] = f"page parse: {exc}"
                    save_status(status)
                    say(f"UNRESOLVED {label}: {exc}")
                    continue
                if not expected_columns(family, relative, payload["headers"]):
                    state["unresolved"][relative] = "unexpected report columns"
                    save_status(status)
                    say(f"UNRESOLVED {label}: unexpected report columns; page not accepted")
                    continue
                target = page_path(county, family, relative)
                target.parent.mkdir(parents=True, exist_ok=True)
                os.chmod(target.parent, 0o700)
                atomic_json(target, payload)
                verified = checked_page(county, family, relative)
                discover(state, verified["discovered_links"], county, family)
                update_projection(state, family, relative, verified)
                state["unresolved"].pop(relative, None)
                state["saved_pages"] += 1
                state["saved_rows"] += verified["row_count"]
                new_pages += 1
                save_status(status)
                say(f"DOWNLOADED AND VERIFIED {label}: {verified['row_count']} rows. "
                    f"PROGRESS {progress_text(county, family, state)}")
            say(f"PROGRESS {progress_text(county, family, state)}")
            if stopped:
                break
        if stopped:
            break
    say(f"SOURCE-ONLY run complete: {new_pages} newly verified pages. Private status: {STATUS}")


if __name__ == "__main__":
    main()
