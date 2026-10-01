"""Recover five low-cutoff Vaslui program reports for source coverage only.

Raw student records stay in the private Desktop cache. Each completed page is
checkpointed, and reruns skip it. Console output contains aggregate counts only.
"""

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

INDEX = Path("/private/tmp/romania_vs_specializari_adm_20261001.html")
OUT = CACHE / "alternate_report_pilot" / "VS"
TARGET_CODES = (32, 38, 4, 65, 6)


def signature(row):
    return (" ".join(str(row.get("Nume", "")).split()),
            str(row.get("Medie Admitere", "")).replace(",", ".").strip())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    soup = BeautifulSoup(INDEX.read_bytes(), "html.parser")
    links = [a.get("href", "") for a in soup.find_all("a", href=True)
             if "raport_admisi_per_liceu.asp" in a.get("href", "")]
    manifest = json.loads((CACHE / "county_manifests" / "VS.json").read_text())
    saved = Counter(signature(row)
                    for page in manifest["families"]["admitted_placements"]["pages"]
                    for row in json.loads((CACHE / page["file"]).read_text())["rows"])
    prior_request = False
    for code in TARGET_CODES:
        matching = [link for link in links
                    if re.search(r"(?:^|&)cs=" + str(code) + r"(?:&|\.)", link)]
        if len(matching) != 1:
            raise ValueError(f"Expected one destination-program link for code {code}")
        relative = matching[0]
        raw_path = OUT / f"destination_program_{code}.html"
        meta_path = OUT / f"destination_program_{code}.json"
        if raw_path.exists() and meta_path.exists():
            metadata = json.loads(meta_path.read_text())
            raw = raw_path.read_bytes()
            if metadata["relative_source"] != relative or hashlib.sha256(raw).hexdigest() != metadata["sha256"]:
                raise ValueError(f"Checkpoint mismatch for program {code}")
            print(f"Program {code}: verified saved checkpoint", flush=True)
        else:
            if prior_request:
                pause = random.uniform(10.0, 12.0)
                print(f"Waiting {pause:.1f}s before program {code} request", flush=True)
                time.sleep(pause)
            request = urllib.request.Request(
                archive_url(relative),
                headers={"User-Agent": "RomaniaEducationResearch/1.0 (academic research; contact: charles.levine@virginia.edu)",
                         "From": "charles.levine@virginia.edu"},
            )
            print(f"Requesting Vaslui destination program {code}", flush=True)
            try:
                with urllib.request.urlopen(request, timeout=35) as response:
                    raw, effective = response.read(), response.geturl()
            except urllib.error.HTTPError as exc:
                print(f"Program {code}: HTTP {exc.code}; stopping with checkpoints intact", flush=True)
                break
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                print(f"Program {code}: network error {type(exc).__name__}; stopping", flush=True)
                break
            headers, rows = _extract_rows(raw)
            if "Nume" not in headers or "Medie Admitere" not in headers:
                print(f"Program {code}: unexpected table columns; stopping without saving", flush=True)
                break
            digest = hashlib.sha256(raw).hexdigest()
            temporary = raw_path.with_suffix(".part")
            temporary.write_bytes(raw)
            temporary.replace(raw_path)
            meta_path.write_text(json.dumps({"relative_source": relative,
                                             "effective_url": effective,
                                             "sha256": digest, "row_count": len(rows)},
                                            ensure_ascii=False, indent=2) + "\n")
            print(f"NEW SOURCE SAVED: program {code}, {len(rows)} rows", flush=True)
            prior_request = True
        headers, rows = _extract_rows(raw)
        program = Counter(signature(row) for row in rows)
        print(f"Program {code}: {len(rows)} source rows, "
              f"{sum((program & saved).values())} in saved county report, "
              f"{sum((program - saved).values())} absent from saved county report", flush=True)


if __name__ == "__main__":
    main()
