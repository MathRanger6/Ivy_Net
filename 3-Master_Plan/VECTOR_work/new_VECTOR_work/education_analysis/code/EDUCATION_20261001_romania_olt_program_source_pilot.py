"""Bounded Olt 2001 placement-source recovery; never export student rows.

Raw Wayback pages remain in the private Desktop cache. Reruns verify and reuse
checkpoints. This script stops on a failed request rather than hammering it.
"""

import base64
import csv
import hashlib
import json
import random
import re
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup
from EDUCATION_20260930_romania_2001_national_acquisition import (
    CACHE, _extract_rows, archive_url,
)

COUNTY = "OT"
OUT = CACHE / "alternate_report_pilot" / COUNTY
RESULT = Path(__file__).resolve().parents[1] / "docs/source_audit/EDUCATION_20261001_Romania_Olt_destination_program_recovery.csv"
TARGETS = {34: 200, 1: 75, 33: 60, 45: 75, 63: 21, 41: 40, 29: 55,
           31: 12, 60: 22, 53: 60, 13: 30, 50: 47, 35: 40, 48: 59, 70: 107}
HEADERS = {"User-Agent": "RomaniaEducationResearch/1.0 (academic research; contact: charles.levine@virginia.edu)",
           "From": "charles.levine@virginia.edu"}


def signature(row):
    return (" ".join(str(row.get("Nume", "")).split()),
            str(row.get("Medie Admitere", "")).replace(",", ".").strip())


def retrieve(relative, stem, required):
    raw_path = OUT / f"{stem}.html"
    meta_path = OUT / f"{stem}.json"
    if raw_path.exists() and meta_path.exists():
        raw = raw_path.read_bytes()
        meta = json.loads(meta_path.read_text())
        if meta["relative_source"] != relative or meta["sha256"] != hashlib.sha256(raw).hexdigest():
            raise ValueError(f"Checkpoint mismatch: {stem}")
        print(f"{stem}: verified private checkpoint", flush=True)
        return raw, False
    print(f"REQUESTING: Olt {stem}", flush=True)
    request = urllib.request.Request(archive_url(relative), headers=HEADERS)
    with urllib.request.urlopen(request, timeout=45) as response:
        raw, effective = response.read(), response.geturl()
    headers, rows = _extract_rows(raw)
    if not required.issubset(headers):
        raise ValueError(f"Unexpected columns for {stem}: {headers}")
    temporary = raw_path.with_suffix(".part")
    temporary.write_bytes(raw)
    temporary.replace(raw_path)
    meta_path.write_text(json.dumps({"relative_source": relative, "effective_url": effective,
                                     "sha256": hashlib.sha256(raw).hexdigest(),
                                     "row_count": len(rows)}, ensure_ascii=False, indent=2) + "\n")
    print(f"NEW SOURCE SAVED: Olt {stem}, {len(rows)} rows", flush=True)
    return raw, True


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    menu = json.loads((CACHE / "county_menus/OT.json").read_text())
    soup = BeautifulSoup(base64.b64decode(menu["raw_html_base64"]), "html.parser")
    indices = [a.get("href", "") for a in soup.find_all("a", href=True)
               if "raport_specializari_adm.asp" in a.get("href", "")]
    if len(indices) != 1:
        raise ValueError(f"Expected one Olt program index, found {len(indices)}")
    last_request = False
    index_path = OUT / "specialization_index.html"
    if not index_path.exists():
        try:
            index, last_request = retrieve(indices[0], "specialization_index", set())
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError) as exc:
            print(f"INDEX REQUEST STOPPED: {exc}", flush=True)
            return
    else:
        index, _ = retrieve(indices[0], "specialization_index", set())
    soup = BeautifulSoup(index, "html.parser")
    links = [a.get("href", "") for a in soup.find_all("a", href=True)
             if "raport_admisi_per_liceu.asp" in a.get("href", "")]
    manifest = json.loads((CACHE / "county_manifests/OT.json").read_text())
    saved = Counter(signature(row)
                    for page in manifest["families"]["admitted_placements"]["pages"]
                    for row in json.loads((CACHE / page["file"]).read_text())["rows"])
    all_program = Counter()
    results = []
    for position, (code, expected) in enumerate(TARGETS.items(), 1):
        matching = [link for link in links if re.search(r"(?:^|&)cs=" + str(code) + r"(?:&|\.)", link)]
        if len(matching) != 1:
            raise ValueError(f"Expected one index link for code {code}, got {len(matching)}")
        if last_request and not (OUT / f"destination_program_{code}.html").exists():
            pause = random.uniform(10, 12)
            print(f"WAITING {pause:.1f}s after completed request, before program {code}", flush=True)
            time.sleep(pause)
        try:
            raw, last_request = retrieve(matching[0], f"destination_program_{code}",
                                         {"Nume", "Medie Admitere"})
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError) as exc:
            print(f"REQUEST STOPPED at program {code}: {exc}; checkpoints retained", flush=True)
            break
        _, rows = _extract_rows(raw)
        signatures = Counter(map(signature, rows))
        all_program += signatures
        in_county = sum((signatures & saved).values())
        absent = sum((signatures - saved).values())
        results.append({"program_code": code, "occupancy_admitted": expected,
                        "program_report_rows": len(rows), "rows_in_saved_county": in_county,
                        "rows_absent_from_saved_county": absent,
                        "row_count_matches_occupancy": len(rows) == expected})
        print(f"PROGRAM {position}/{len(TARGETS)}: {code}; report {len(rows)}/{expected}; "
              f"absent from county report {absent}", flush=True)
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    with RESULT.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(results[0]) if results else
                                ["program_code", "occupancy_admitted", "program_report_rows",
                                 "rows_in_saved_county", "rows_absent_from_saved_county",
                                 "row_count_matches_occupancy"])
        writer.writeheader()
        writer.writerows(results)
    print(f"REPORTS VERIFIED: {len(results)}/{len(TARGETS)}", flush=True)
    if len(results) == len(TARGETS):
        print(f"UNIQUE PROGRAM SIGNATURES: {len(all_program)}; "
              f"DUPLICATE SIGNATURE OCCURRENCES: {sum(all_program.values())-len(all_program)}", flush=True)
        print(f"DISTINCT SIGNATURES ABSENT FROM SAVED COUNTY: {len(all_program-saved)}; "
              f"OCCUPANCY GAP: 253", flush=True)
    print(f"Aggregate-only audit: {RESULT}", flush=True)


if __name__ == "__main__":
    main()
