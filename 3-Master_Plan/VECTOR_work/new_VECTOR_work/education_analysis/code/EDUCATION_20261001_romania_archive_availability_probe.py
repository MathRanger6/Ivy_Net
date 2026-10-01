"""Read-only availability probe for unresolved Romania 2001 county pages.

Queries only the Internet Archive's availability endpoint. Does not request
archived student tables, alter the acquisition cache, or write output files.
"""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CACHE = Path.home() / "Desktop/VECTOR_temp/romania_2001_national_main_allocation_v1"
SLEEP_SECONDS = 5.0
TARGET_STATUS = int(sys.argv[1]) if len(sys.argv) > 1 else 404

jobs = []
for manifest_path in sorted((CACHE / "county_manifests").glob("*.json")):
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    code = manifest["county"]["county_code"]
    for family, record in manifest["families"].items():
        for detail in record.get("unresolved_details", []):
            if detail.get("status") == TARGET_STATUS:
                jobs.append((code, family, detail["relative_source"]))

print(f"Checking {len(jobs)} saved HTTP {TARGET_STATUS} addresses. One query every {SLEEP_SECONDS:.0f} seconds.", flush=True)
for position, (code, family, relative) in enumerate(jobs, 1):
    original = "http://www.edu.ro/adm2001/" + relative
    query = urllib.parse.urlencode({"url": original})
    request = urllib.request.Request(
        "https://archive.org/wayback/available?" + query,
        headers={
            "User-Agent": "RomaniaEducationResearch/1.0 (academic research; contact: charles.levine@virginia.edu)",
            "From": "charles.levine@virginia.edu",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            payload = json.load(response)
        closest = payload.get("archived_snapshots", {}).get("closest")
        if closest and closest.get("available") and closest.get("status") == "200":
            print(
                f"{position:02}/{len(jobs)} {code} {family}: ALTERNATE "
                f"{closest.get('timestamp')} {closest.get('url')}",
                flush=True,
            )
        else:
            print(f"{position:02}/{len(jobs)} {code} {family}: no available capture reported", flush=True)
    except urllib.error.HTTPError as exc:
        print(f"{position:02}/{len(jobs)} {code} {family}: HTTP {exc.code}; stopping", flush=True)
        break
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        print(f"{position:02}/{len(jobs)} {code} {family}: lookup error {type(exc).__name__}; stopping", flush=True)
        break
    if position < len(jobs):
        time.sleep(SLEEP_SECONDS)
