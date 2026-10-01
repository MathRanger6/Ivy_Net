"""Check indexed successful Wayback captures for exact unresolved 2001 report URLs.

Source metadata only: no student pages are downloaded. Append and flush after
each address so a stopped run can resume without repeating completed checks.
"""

import argparse
import csv
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "docs" / "source_audit"
INVENTORY = ROOT / "EDUCATION_20261001_Romania_unresolved_page_inventory.csv"
RESULTS = ROOT / "EDUCATION_20261001_Romania_alternate_capture_index_results.csv"
FIELDS = ["checked_utc", "county", "report_family", "missing_relative_source",
          "result", "capture_count", "capture_timestamps", "error"]
DELAY_SECONDS = 5.0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=40,
                        help="Maximum new exact-address checks in this run")
    args = parser.parse_args()
    jobs = list(csv.DictReader(INVENTORY.open(encoding="utf-8")))
    completed = set()
    if RESULTS.exists():
        for row in csv.DictReader(RESULTS.open(encoding="utf-8")):
            if row["result"] in ("indexed_200", "no_indexed_200"):
                completed.add(row["missing_relative_source"])

    with RESULTS.open("a", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        if stream.tell() == 0:
            writer.writeheader()
            stream.flush()
        attempted = 0
        for job in jobs:
            relative = job["missing_relative_source"]
            if relative in completed:
                continue
            if attempted >= args.limit:
                break
            if attempted:
                time.sleep(DELAY_SECONDS)
            original = "http://www.edu.ro/adm2001/" + relative
            query = urllib.parse.urlencode({"url": original, "output": "json",
                                            "filter": "statuscode:200",
                                            "fl": "timestamp,statuscode,original"})
            request = urllib.request.Request(
                "https://web.archive.org/cdx/search/cdx?" + query,
                headers={"User-Agent": "RomaniaEducationResearch/1.0 (academic research; contact: charles.levine@virginia.edu)",
                         "From": "charles.levine@virginia.edu", "Accept": "application/json"},
            )
            result, timestamps, error = "", [], ""
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    records = json.load(response)
                timestamps = sorted({row[0] for row in records[1:]}) if records else []
                result = "indexed_200" if timestamps else "no_indexed_200"
            except urllib.error.HTTPError as exc:
                result, error = "http_error", str(exc.code)
            except (urllib.error.URLError, TimeoutError, ValueError, IndexError) as exc:
                result, error = "lookup_error", type(exc).__name__
            writer.writerow({"checked_utc": datetime.now(timezone.utc).isoformat(),
                             "county": job["county"], "report_family": job["report_family"],
                             "missing_relative_source": relative, "result": result,
                             "capture_count": len(timestamps),
                             "capture_timestamps": ";".join(timestamps), "error": error})
            stream.flush()
            attempted += 1
            print(f"{attempted}/{args.limit}: {job['county']} {job['report_family']} — "
                  f"{result}, {len(timestamps)} capture(s){'; '+error if error else ''}", flush=True)
            if result not in ("indexed_200", "no_indexed_200"):
                print("Stopping after archive/index error; saved results can resume.", flush=True)
                break


if __name__ == "__main__":
    main()
