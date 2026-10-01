"""Paced source-only pilot for two Romania per-school report views.

Keeps identifiable page bodies in memory. Prints aggregate coverage checks only.
"""
import json
from collections import Counter
from pathlib import Path

from EDUCATION_20260930_romania_2001_national_acquisition import (
    CACHE, _extract_rows, archive_url,
)
from romania_archive_retrieval import ArchiveClient


def emit(event):
    if event.get("kind") == "retrieval_wait" and event.get("seconds", 0) >= 10:
        print(
            f"Archive wait: {event['seconds']:.1f}s "
            f"({event['reason']}). {event.get('timing', '')}",
            flush=True,
        )
    elif event.get("kind") == "http_attempt":
        print(f"Archive HTTP response: {event.get('status')}", flush=True)


def rows_in_saved_county_report(manifest, family):
    rows = []
    for item in manifest["families"][family]["pages"]:
        page = json.loads((CACHE / item["file"]).read_text())
        rows.extend(page["rows"])
    return rows


def row_key(row):
    # Both the county and per-school views should have these literal source
    # columns. Never print the key: it contains identifying name text.
    if "Nume" not in row or "Medie Admitere" not in row:
        return None
    return (
        " ".join(str(row["Nume"]).casefold().split()),
        " ".join(str(row["Medie Admitere"]).casefold().split()),
    )


client = ArchiveClient(
    Path.home() / "Desktop/VECTOR_temp/romania_2001_school_view_pilot_20261001",
    emit,
    archive_use_acknowledged=True,
    initial_interval_seconds=60.0,
    minimum_interval_seconds=60.0,
    maximum_interval_seconds=60.0,
    max_runtime_hours=1.0,
)

for county, family in (("BH", "candidate_roster"), ("BR", "admitted_placements")):
    manifest = json.loads((CACHE / "county_manifests" / f"{county}.json").read_text())
    directory = manifest["families"]["origin_school_directory"]["pages"][0]
    directory_page = json.loads((CACHE / directory["file"]).read_text())
    links = [
        link for link in directory_page["discovered_links"]
        if "raport_candidati_per_scoala" in link
    ]
    relative = links[0]
    if family == "admitted_placements":
        relative = relative.replace(
            "raport_candidati_per_scoala", "raport_total_per_scoala", 1
        )
    result = client.get(archive_url(relative))
    if result is None:
        print(county, family, "school report unavailable in this pilot", flush=True)
        continue
    raw, _effective = result
    headers, school_rows = _extract_rows(raw)
    county_rows = rows_in_saved_county_report(manifest, family)
    school_keys = Counter(key for row in school_rows if (key := row_key(row)))
    county_keys = Counter(key for row in county_rows if (key := row_key(row)))
    overlap = sum((school_keys & county_keys).values())
    print(
        county, family,
        "school_rows=", len(school_rows),
        "matching_saved_county_rows=", overlap,
        "source_columns=", headers,
        flush=True,
    )
