"""Resumable acquisition of the Romania 2001 main-allocation national core.

Importing this module makes no network requests. Identifiable archived pages
are checkpointed only beneath ~/Desktop/VECTOR_temp. Repository outputs are
limited to later name-free analysis products.

The six source families retained for every county are:
  * origin-school directory;
  * candidate roster with examination and grades 5-8 components;
  * admitted placements;
  * unassigned applicants;
  * destination-program directory;
  * destination-program occupancy and observed cutoffs.

The second allocation and redundant per-school/per-specialization views are
deliberately outside this first national acquisition.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import time
import urllib.parse
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup

from romania_archive_retrieval import ArchiveClient, RetrievalStopped


SOURCE = "http://www.edu.ro/adm2001/"
STAMP = "20020816151117"
CACHE = (
    Path.home() / "Desktop" / "VECTOR_temp" / "romania_2001_national_main_allocation_v1"
)
PAGES = CACHE / "pages"
SCHEMA_VERSION = 1
MAX_CONSECUTIVE_NETWORK_FAILURES = 4

FAMILIES = {
    "origin_school_directory": "raport_scoli_din_judet",
    "candidate_roster": "raport_candidati_total",
    "admitted_placements": "raport_admisi_per_judet",
    "unassigned_applicants": "raport_respinsi_per_judet",
    "program_directory": "raport_specializari",
    "program_occupancy": "raport_situatie_licee_per_judet",
}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_bytes(value) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def atomic_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".part-{os.getpid()}")
    try:
        with temporary.open("x", encoding="utf-8") as stream:
            os.chmod(temporary, 0o600)
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def prepare_cache() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    PAGES.mkdir(parents=True, exist_ok=True)
    os.chmod(CACHE, 0o700)
    os.chmod(PAGES, 0o700)


def original_url(relative: str) -> str:
    cleaned = relative.lstrip("./")
    return SOURCE + cleaned


def replay_url(relative: str, timestamp: str = STAMP, original: str | None = None) -> str:
    original = original or original_url(relative)
    safe_original = urllib.parse.quote(original, safe=":/?&=%-._~+")
    return f"https://web.archive.org/web/{timestamp}id_/{safe_original}"


def archive_url(relative: str) -> str:
    return replay_url(relative, STAMP)


def normalize_relative(href: str) -> str | None:
    if not href:
        return None
    href = urllib.parse.unquote(href).strip()
    if href.lower().startswith(("javascript:", "mailto:", "#")):
        return None
    # Wayback sometimes leaves the historical link as a normal edu.ro URL and
    # sometimes rewrites it as an absolute web.archive.org URL containing the
    # original URL. Recover the original address without changing its case.
    lowered_href = href.lower()
    embedded_source = lowered_href.find("http://www.edu.ro/adm2001/")
    if embedded_source < 0:
        embedded_source = lowered_href.find("https://www.edu.ro/adm2001/")
    if embedded_source >= 0:
        href = href[embedded_source:]

    parsed = urllib.parse.urlsplit(href)
    if parsed.scheme or parsed.netloc:
        # Accept links back to this exact historical source only.
        if parsed.netloc.lower() not in {"www.edu.ro", "edu.ro"}:
            return None
        path = parsed.path
        marker = "/adm2001/"
        marker_position = path.lower().find(marker)
        if marker_position < 0:
            return None
        relative = path[marker_position + len(marker):]
        if parsed.query:
            relative += "?" + parsed.query
        return relative
    return href.lstrip("./")


def page_file(county_code: str, family: str, relative: str) -> Path:
    token = hashlib.sha256(relative.encode("utf-8")).hexdigest()[:16]
    match = re.search(r"idx=(\d+)", relative, flags=re.I)
    index = f"idx_{int(match.group(1)):07d}" if match else "single"
    return PAGES / county_code / family / f"{index}_{token}.json"


def special_file(label: str) -> Path:
    return CACHE / f"{label}.json"


def _extract_rows(raw: bytes) -> tuple[list[str], list[dict]]:
    body = raw.decode("cp1250", errors="replace")
    soup = BeautifulSoup(body, "html.parser")
    candidates = []
    for table in soup.find_all("table"):
        headers = [h.get_text(" ", strip=True) for h in table.find_all("th")]
        if not headers:
            continue
        rows = []
        for tr in table.find_all("tr"):
            cells = [
                td.get_text(" ", strip=True)
                for td in tr.find_all("td", recursive=False)
            ]
            if len(cells) == len(headers) and cells:
                rows.append(dict(zip(headers, cells)))
        numeric = sum(
            bool(re.fullmatch(r"\d+", next(iter(row.values()), ""))) for row in rows
        )
        candidates.append((numeric, len(rows), headers, rows))
    if not candidates:
        raise ValueError("No source table with headings was found")
    _, _, headers, rows = max(candidates, key=lambda item: (item[0], item[1]))
    return headers, rows


def _links(raw: bytes) -> list[str]:
    soup = BeautifulSoup(raw.decode("cp1250", errors="replace"), "html.parser")
    found = []
    for anchor in soup.find_all("a", href=True):
        relative = normalize_relative(anchor.get("href"))
        if relative:
            found.append(relative)
    for area in soup.find_all("area", href=True):
        relative = normalize_relative(area.get("href"))
        if relative:
            found.append(relative)
    return list(dict.fromkeys(found))


def _payload(relative: str, raw: bytes, effective_url: str, *, kind: str) -> dict:
    headers, rows = _extract_rows(raw)
    return {
        "schema_version": SCHEMA_VERSION,
        "kind": kind,
        "relative_source": relative,
        "requested_url": archive_url(relative),
        "effective_url": effective_url,
        "saved_utc": now_utc(),
        "headers": headers,
        "row_count": len(rows),
        "rows_sha256": hashlib.sha256(canonical_bytes(rows)).hexdigest(),
        "raw_html_sha256": hashlib.sha256(raw).hexdigest(),
        "raw_html_base64": base64.b64encode(raw).decode("ascii"),
        "rows": rows,
        "discovered_links": _links(raw),
    }


def verified_page(path: Path, *, relative: str, kind: str) -> dict | None:
    if not path.exists():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "schema_version", "kind", "relative_source", "row_count", "rows",
        "rows_sha256", "raw_html_sha256", "raw_html_base64", "discovered_links",
    }
    if not isinstance(value, dict) or not required.issubset(value):
        raise ValueError(f"Incomplete checkpoint: {path}")
    if (
        value["schema_version"] != SCHEMA_VERSION
        or value["kind"] != kind
        or value["relative_source"] != relative
    ):
        raise ValueError(f"Checkpoint identity mismatch: {path}")
    rows = value["rows"]
    if value["row_count"] != len(rows):
        raise ValueError(f"Checkpoint row-count mismatch: {path}")
    if hashlib.sha256(canonical_bytes(rows)).hexdigest() != value["rows_sha256"]:
        raise ValueError(f"Checkpoint row digest mismatch: {path}")
    raw = base64.b64decode(value["raw_html_base64"], validate=True)
    if hashlib.sha256(raw).hexdigest() != value["raw_html_sha256"]:
        raise ValueError(f"Checkpoint HTML digest mismatch: {path}")
    return value


def _write_event(event: dict) -> None:
    record = {"utc": now_utc(), **event}
    with (CACHE / "retrieval_events.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        stream.flush()
    kind = event.get("kind")
    if kind == "adaptive_pace" and event.get("direction") == "slower":
        print(
            f"  Archive slowed to {event['new_seconds']:.1f}s between requests.",
            flush=True,
        )
    elif kind == "retrieval_wait" and event.get("seconds", 0) >= 10:
        print(
            f"  Archive wait: {event['seconds']:.1f}s "
            f"({event.get('reason', 'backoff')}). "
            f"{event.get('timing', '')}",
            flush=True,
        )
    elif kind == "http_attempt" and event.get("status") not in (200, 302):
        print(
            f"  Unresolved HTTP attempt: {event.get('status')} "
            f"{event.get('error') or ''}",
            flush=True,
        )
def _fetch_raw(client: ArchiveClient, relative: str) -> tuple[bytes, str] | None:
    """Fetch the nearest replay selected by Wayback for this archived URL.

    Wayback already redirects the nominal timestamp to another surviving
    capture when one exists. A 404 is retained as a source-coverage gap for
    later recovery from the Ministry's redundant report views.
    """
    return client.get(archive_url(relative))


def _save_special(
    client: ArchiveClient, label: str, relative: str, parser
) -> dict | None:
    path = special_file(label)
    if path.exists():
        value = json.loads(path.read_text(encoding="utf-8"))
        if value.get("schema_version") != SCHEMA_VERSION:
            raise ValueError(f"Special checkpoint schema mismatch: {path}")
        return value
    result = _fetch_raw(client, relative)
    if result is None:
        return None
    raw, effective = result
    value = parser(raw)
    value.update({
        "schema_version": SCHEMA_VERSION,
        "relative_source": relative,
        "requested_url": archive_url(relative),
        "effective_url": effective,
        "saved_utc": now_utc(),
        "raw_html_sha256": hashlib.sha256(raw).hexdigest(),
        "raw_html_base64": base64.b64encode(raw).decode("ascii"),
    })
    atomic_json(path, value)
    return value


def parse_county_map(raw: bytes) -> dict:
    soup = BeautifulSoup(raw.decode("cp1250", errors="replace"), "html.parser")
    counties = []
    for area in soup.find_all("area", href=True):
        relative = normalize_relative(area.get("href"))
        if not relative or "rapoarte.asp-cj=" not in relative.lower():
            continue
        code = re.search(r"cj=([^&.]+)", relative, flags=re.I)
        name = re.search(r"nj=(.*?)(?:\.htm|&|$)", relative, flags=re.I)
        if not code or not name:
            continue
        counties.append({
            "county_code": urllib.parse.unquote_plus(code.group(1)),
            "county_name": urllib.parse.unquote_plus(name.group(1)),
            "menu_relative": relative,
        })
    unique = {item["county_code"]: item for item in counties}
    if len(unique) != 41:
        raise ValueError(f"Expected 41 county units from the official map; found {len(unique)}")
    return {"counties": list(unique.values()), "county_units": len(unique)}


def parse_county_menu(raw: bytes) -> dict:
    links = _links(raw)
    seeds = {}
    for family, stem in FAMILIES.items():
        matches = [link for link in links if _exact_report_name(link, stem)]
        if len(matches) != 1:
            raise ValueError(
                f"Expected one menu link for {family}; found {len(matches)}"
            )
        seeds[family] = matches[0]
    return {"family_seeds": seeds}


def _exact_report_name(relative: str, stem: str) -> bool:
    """Match one report without also matching a longer, similarly named report.

    Archived filenames look like ``report.asp-cj=AB...``. Requiring the exact
    ``<stem>.asp`` prefix keeps, for example, ``raport_specializari`` separate
    from ``raport_specializari_adm``.
    """
    basename = relative.rsplit("/", 1)[-1].lower()
    return basename.startswith(stem.lower() + ".asp")


def _family_link(relative: str, stem: str, county_code: str) -> bool:
    low = relative.lower()
    return (
        _exact_report_name(relative, stem)
        and f"cj={county_code.lower()}" in low
        and "rep2/" not in low
    )


def crawl_family(
    client: ArchiveClient,
    county: dict,
    family: str,
    seed: str,
    known_missing: dict[str, dict] | None = None,
) -> dict:
    code = county["county_code"]
    stem = FAMILIES[family]
    queue = deque([seed])
    seen = set()
    pages = []
    unresolved = []
    unresolved_details = []
    known_missing = known_missing or {}
    while queue:
        relative = queue.popleft()
        if relative in seen:
            continue
        seen.add(relative)
        path = page_file(code, family, relative)
        value = verified_page(path, relative=relative, kind=family)
        if value is None:
            # A prior HTTP 404/410 is an archived-capture gap, not transient
            # server pressure. Keep it in the manifest without asking Wayback
            # for the same unavailable address on every resumed pass.
            if relative in known_missing:
                unresolved.append(relative)
                unresolved_details.append(known_missing[relative])
                continue
            result = _fetch_raw(client, relative)
            if result is None:
                unresolved.append(relative)
                unresolved_details.append({
                    "relative_source": relative,
                    "status": client.last_status,
                    "error": client.last_error,
                })
                continue
            raw, effective = result
            try:
                value = _payload(relative, raw, effective, kind=family)
            except ValueError as error:
                _write_event({
                    "kind": "parse_error", "county": code, "family": family,
                    "relative": relative, "error": str(error),
                })
                unresolved.append(relative)
                unresolved_details.append({
                    "relative_source": relative,
                    "status": 200,
                    "error": f"parse error: {error}",
                })
                continue
            atomic_json(path, value)
            verified_page(path, relative=relative, kind=family)
        pages.append({
            "relative_source": relative,
            "file": str(path.relative_to(CACHE)),
            "sha256": sha256(path),
            "rows": value["row_count"],
        })
        if len(pages) == 1 or len(pages) % 5 == 0:
            print(
                f"    {code} {family}: {len(pages)} pages checkpointed, "
                f"{sum(page['rows'] for page in pages):,} rows so far; "
                f"{len(queue)} discovered pages waiting.",
                flush=True,
            )
        for link in value["discovered_links"]:
            if _family_link(link, stem, code) and link not in seen:
                queue.append(link)
    return {
        "family": family,
        "pages": pages,
        "page_count": len(pages),
        "row_count": sum(page["rows"] for page in pages),
        "unresolved": unresolved,
        "unresolved_details": unresolved_details,
        "complete": not unresolved,
    }


def _menu_path(county_code: str) -> Path:
    return CACHE / "county_menus" / f"{county_code}.json"


def _county_needs_another_network_pass(county_code: str) -> bool:
    """Retry transient failures, while leaving fixed 404 gaps for recovery work."""
    manifest_path = CACHE / "county_manifests" / f"{county_code}.json"
    if not manifest_path.exists():
        return True
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("complete"):
        return False
    details = [
        detail
        for family in manifest.get("families", {}).values()
        for detail in family.get("unresolved_details", [])
    ]
    # Manifests written by the first code version did not record the status;
    # inspect them once under the corrected logic.
    if not details:
        return True
    return any(detail.get("status") not in (404, 410) for detail in details)


def county_status() -> dict:
    directory_path = special_file("county_directory")
    if not directory_path.exists():
        return {
            "county_directory_ready": False,
            "county_units": 0,
            "complete_counties": 0,
            "remaining_counties": None,
            "cache_folder": str(CACHE),
        }
    directory = json.loads(directory_path.read_text())
    counties = directory["counties"]
    complete = []
    for county in counties:
        manifest = CACHE / "county_manifests" / f"{county['county_code']}.json"
        if manifest.exists():
            value = json.loads(manifest.read_text())
            if value.get("complete"):
                complete.append(county["county_code"])
    return {
        "county_directory_ready": True,
        "county_units": len(counties),
        "complete_counties": len(complete),
        "remaining_counties": len(counties) - len(complete),
        "complete_county_codes": complete,
        "cache_folder": str(CACHE),
    }


def acquire(
    *,
    live: bool = False,
    initial_interval_seconds: float = 2.0,
    minimum_interval_seconds: float = 1.2,
    maximum_interval_seconds: float = 60.0,
    max_runtime_hours: float = 10.0,
    retry_passes: int = 3,
    retry_cooldown_seconds: float = 180.0,
) -> dict:
    """Run or resume the national acquisition, checkpointing every page."""
    if not live:
        print("Preview only: no archive requests.", flush=True)
        return county_status()
    if retry_passes < 1 or retry_cooldown_seconds < 0:
        raise ValueError("Retry passes must be positive and cooldown nonnegative")
    prepare_cache()
    client = ArchiveClient(
        CACHE,
        _write_event,
        archive_use_acknowledged=True,
        initial_interval_seconds=initial_interval_seconds,
        minimum_interval_seconds=minimum_interval_seconds,
        maximum_interval_seconds=maximum_interval_seconds,
        max_runtime_hours=max_runtime_hours,
    )

    print("National acquisition 1/3 — recovering the official county directory.", flush=True)
    directory = _save_special(
        client, "county_directory", "harta.asp.htm", parse_county_map
    )
    if directory is None:
        raise RetrievalStopped("The national county map remains unresolved.")
    counties = directory["counties"]
    print(f"  Official map recovered: {len(counties)} county units.", flush=True)

    started = time.monotonic()
    for pass_number in range(1, retry_passes + 1):
        remaining = [
            county for county in counties
            if _county_needs_another_network_pass(county["county_code"])
        ]
        if not remaining:
            break
        if pass_number > 1:
            client.wait_between_passes(retry_cooldown_seconds, pass_number)
        print(
            f"National acquisition 2/3 — pass {pass_number}/{retry_passes}; "
            f"{len(remaining)} counties remain.",
            flush=True,
        )
        try:
            from tqdm.auto import tqdm
            iterator = tqdm(
                remaining, desc=f"National pass {pass_number}",
                unit="county", dynamic_ncols=True
            )
        except ImportError:
            iterator = remaining
        for position, county in enumerate(iterator, 1):
            code = county["county_code"]
            name = county["county_name"]
            print(
                f"\nCounty {position}/{len(remaining)} this pass: {code} — {name}",
                flush=True,
            )
            menu_path = _menu_path(code)
            if menu_path.exists():
                menu = json.loads(menu_path.read_text())
            else:
                result = _fetch_raw(client, county["menu_relative"])
                if result is None:
                    print("  County menu unresolved; queued for the next pass.", flush=True)
                    continue
                raw, effective = result
                try:
                    menu = parse_county_menu(raw)
                except ValueError as error:
                    _write_event({
                        "kind": "menu_parse_error", "county": code,
                        "error": str(error),
                    })
                    continue
                menu.update({
                    "schema_version": SCHEMA_VERSION,
                    "county": county,
                    "effective_url": effective,
                    "raw_html_sha256": hashlib.sha256(raw).hexdigest(),
                    "raw_html_base64": base64.b64encode(raw).decode("ascii"),
                })
                atomic_json(menu_path, menu)

            family_results = {}
            prior_manifest_path = CACHE / "county_manifests" / f"{code}.json"
            prior_families = (
                json.loads(prior_manifest_path.read_text()).get("families", {})
                if prior_manifest_path.exists() else {}
            )
            for family in FAMILIES:
                known_missing = {
                    detail["relative_source"]: detail
                    for detail in prior_families.get(family, {}).get("unresolved_details", [])
                    if detail.get("status") in (404, 410)
                }
                result = crawl_family(
                    client, county, family, menu["family_seeds"][family],
                    known_missing=known_missing,
                )
                family_results[family] = result
                print(
                    f"  {family}: {result['page_count']} pages, "
                    f"{result['row_count']:,} rows"
                    + (
                        f", {len(result['unresolved'])} unresolved"
                        if result["unresolved"] else ""
                    ),
                    flush=True,
                )
            complete = all(item["complete"] for item in family_results.values())
            manifest = {
                "schema_version": SCHEMA_VERSION,
                "county": county,
                "saved_utc": now_utc(),
                "families": family_results,
                "complete": complete,
                "total_pages": sum(x["page_count"] for x in family_results.values()),
                "total_rows_across_report_views": sum(
                    x["row_count"] for x in family_results.values()
                ),
            }
            atomic_json(
                CACHE / "county_manifests" / f"{code}.json", manifest
            )
            completed = county_status()["complete_counties"]
            print(
                f"  County {'complete' if complete else 'paused'}; "
                f"national progress {completed}/{len(counties)} counties.",
                flush=True,
            )

    print("National acquisition 3/3 — auditing completed checkpoints.", flush=True)
    status = county_status()
    status["elapsed_minutes_this_invocation"] = round(
        (time.monotonic() - started) / 60, 2
    )
    manifests = []
    if status["remaining_counties"] == 0:
        for county in counties:
            path = CACHE / "county_manifests" / f"{county['county_code']}.json"
            manifests.append({
                "county_code": county["county_code"],
                "file": str(path.relative_to(CACHE)),
                "sha256": sha256(path),
            })
        atomic_json(
            CACHE / "completed_national_manifest.json",
            {
                "schema_version": SCHEMA_VERSION,
                "completed_utc": now_utc(),
                "scope": "Romania 2001 main-allocation national analytical core",
                "county_units": len(counties),
                "county_manifests": manifests,
                "second_allocation_included": False,
                "redundant_per_school_views_included": False,
            },
        )
        print("All national core county report families are saved and verified.", flush=True)
    else:
        retryable = [
            county["county_code"] for county in counties
            if _county_needs_another_network_pass(county["county_code"])
        ]
        print(
            f"Acquisition paused with {status['remaining_counties']} counties remaining. "
            + (
                "Transient or parse failures remain; run the same cell again to resume."
                if retryable
                else "Their unresolved pages are fixed archive-coverage gaps reserved "
                     "for redundant-report recovery."
            ),
            flush=True,
        )
    return status


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--initial-interval-seconds", type=float, default=2.0)
    parser.add_argument("--minimum-interval-seconds", type=float, default=1.2)
    parser.add_argument("--maximum-interval-seconds", type=float, default=60.0)
    parser.add_argument("--max-runtime-hours", type=float, default=10.0)
    parser.add_argument("--retry-passes", type=int, default=3)
    parser.add_argument("--retry-cooldown-seconds", type=float, default=180.0)
    args = parser.parse_args()
    try:
        result = acquire(
            live=args.run,
            initial_interval_seconds=args.initial_interval_seconds,
            minimum_interval_seconds=args.minimum_interval_seconds,
            maximum_interval_seconds=args.maximum_interval_seconds,
            max_runtime_hours=args.max_runtime_hours,
            retry_passes=args.retry_passes,
            retry_cooldown_seconds=args.retry_cooldown_seconds,
        )
        print(json.dumps(result, indent=2))
    except (RetrievalStopped, KeyboardInterrupt) as error:
        print(f"Stopped safely: {error or 'Interrupted by user'}", flush=True)
        raise SystemExit(2)
