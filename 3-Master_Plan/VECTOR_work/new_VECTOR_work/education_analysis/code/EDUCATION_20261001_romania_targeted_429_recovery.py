"""Retry only five previously throttled pages with reported surviving captures.

Uses the existing archive client, checks source identity and table structure,
and checkpoints raw pages only inside the private Desktop acquisition cache.
County manifests are refreshed by the normal notebook resume after this pass.
"""
import json
import urllib.parse

import EDUCATION_20260930_romania_2001_national_acquisition as source
from romania_archive_retrieval import ArchiveClient, RetrievalStopped

TARGETS = [
    ("GJ", "candidate_roster"),
    ("GL", "unassigned_applicants"),
    ("IS", "admitted_placements"),
    ("MM", "admitted_placements"),
    ("NT", "admitted_placements"),
]

client = ArchiveClient(
    source.CACHE,
    source._write_event,
    archive_use_acknowledged=True,
    initial_interval_seconds=60.0,
    minimum_interval_seconds=60.0,
    maximum_interval_seconds=60.0,
    max_runtime_hours=1.0,
)
print("Source-only retry: at most five page addresses; 60 seconds between requests.", flush=True)
for position, (code, family) in enumerate(TARGETS, 1):
    manifest = json.loads(
        (source.CACHE / "county_manifests" / f"{code}.json").read_text()
    )
    record = manifest["families"][family]
    details = [d for d in record["unresolved_details"] if d.get("status") == 429]
    if len(details) != 1:
        raise ValueError(f"Expected one saved 429 address in {code} {family}")
    relative = details[0]["relative_source"]
    path = source.page_file(code, family, relative)
    existing = source.verified_page(path, relative=relative, kind=family)
    if existing is not None:
        print(position, code, family, "already checkpointed", flush=True)
        continue
    print(position, code, family, "requesting one archived page", flush=True)
    try:
        result = client.get(source.archive_url(relative))
    except RetrievalStopped as error:
        print("Stopped safely:", error, flush=True)
        break
    if result is None:
        print(position, code, family, "unresolved HTTP", client.last_status, flush=True)
        if client.last_status == 429:
            print("Stopping after renewed throttling; saved checkpoints remain.", flush=True)
            break
        continue
    raw, effective = result
    if relative not in urllib.parse.unquote(effective):
        raise ValueError(f"Archive redirected {code} {family} to another source path")
    payload = source._payload(relative, raw, effective, kind=family)
    # Some county/family combinations have no earlier saved page. In that
    # case compare against all already verified pages of the same report type.
    baseline_paths = ([source.CACHE / record["pages"][0]["file"]]
                      if record["pages"] else
                      sorted((source.PAGES).glob(f"*/{family}/*.json")))
    if not baseline_paths:
        raise ValueError(f"No saved {family} page to verify table columns")
    header_sets = {
        tuple(json.loads(path.read_text())["headers"])
        for path in baseline_paths
    }
    if header_sets != {tuple(payload["headers"])}:
        raise ValueError(f"Source columns changed for {code} {family}")
    source.atomic_json(path, payload)
    source.verified_page(path, relative=relative, kind=family)
    print(position, code, family, "checkpointed", payload["row_count"], "rows", flush=True)
