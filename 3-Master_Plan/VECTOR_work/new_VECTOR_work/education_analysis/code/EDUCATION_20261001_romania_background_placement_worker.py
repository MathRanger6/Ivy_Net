"""Resume 2001 placement-source recovery, county by county.

Only archived source reports are fetched. Raw student rows stay in the private
Desktop cache. This never calculates a research outcome or declares missing
material permanently unavailable. Each county is reconciled independently.

Example, small first run:
  python -u EDUCATION_20261001_romania_background_placement_worker.py --run --counties NT --max-new-pages 3
Later resume without --counties; verified pages are reused.
"""

import argparse
import base64
import csv
import hashlib
import json
import random
import re
import signal
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from bs4 import BeautifulSoup
from EDUCATION_20260930_romania_2001_national_acquisition import (
    CACHE, _extract_rows, archive_url,
)

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "docs/source_audit/EDUCATION_20261001_Romania_placement_recovery_scope_by_county.csv"
OUT = ROOT / "outputs/romania_2001_national_source_recovery"
STATUS = OUT / "placement_county_status.csv"
PRIVATE = CACHE / "alternate_report_pilot"
FAILED = PRIVATE / "unresolved_requests.json"
HEADERS = {"User-Agent": "RomaniaEducationResearch/1.0 (academic research; contact: charles.levine@virginia.edu)",
           "From": "charles.levine@virginia.edu"}
FIELDS = ["county", "state", "target_programs", "verified_programs", "unresolved_programs",
          "saved_county_placements", "occupancy_admitted", "placement_gap",
          "recovered_distinct_absent", "duplicate_program_signatures", "detail"]


def say(message):
    print(f"{datetime.now().astimezone():%Y-%m-%d %H:%M:%S %Z} | {message}", flush=True)


def signature(row):
    return (" ".join(str(row.get("Nume", "")).split()),
            str(row.get("Medie Admitere", "")).replace(",", ".").strip())


def number(value):
    return int(str(value).replace(".", "").replace(" ", ""))


def saved_rows(manifest, family):
    for page in manifest["families"][family]["pages"]:
        payload = json.loads((CACHE / page["file"]).read_text())
        for row in payload["rows"]:
            yield row


def targets(manifest, cutoff):
    result = {}
    for row in saved_rows(manifest, "program_occupancy"):
        admitted = number(row["Candidaţi admişi"])
        if not admitted or not row["Ultima notă"].strip():
            continue
        if Decimal(row["Ultima notă"].replace(",", ".")) > cutoff:
            continue
        # The same archived column uses both "x55 ..." and "103 ...".
        # In either form its leading number is the destination-program code.
        match = re.match(r"(?:x+)?(\d+)\b", row["Liceu"].strip(), re.I)
        if not match:
            raise ValueError("Cannot identify a source program code")
        code = int(match.group(1))
        if code in result:
            raise ValueError(f"Duplicate source program code {code}")
        result[code] = admitted
    return result


class Worker:
    def __init__(self, args):
        self.args = args
        self.started = time.monotonic()
        self.last_request = None
        self.new_pages = 0
        self.stop = False
        self.failed = json.loads(FAILED.read_text()) if FAILED.exists() else {}

    def remember_unresolved(self, county, stem, relative, reason):
        key = f"{county}/{stem}"
        self.failed[key] = {"relative_source": relative, "reason": reason,
                            "last_attempt_local": datetime.now().astimezone().isoformat(),
                            "state": "unresolved; researcher review required"}
        PRIVATE.mkdir(parents=True, exist_ok=True)
        temporary = FAILED.with_suffix(".part")
        temporary.write_text(json.dumps(self.failed, ensure_ascii=False, indent=2) + "\n")
        temporary.replace(FAILED)

    def limit_reached(self):
        return (self.new_pages >= self.args.max_new_pages or
                time.monotonic() - self.started >= self.args.max_hours * 3600)

    def retrieve(self, county, relative, stem, required):
        folder = PRIVATE / county
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{stem}.html"
        meta_path = folder / f"{stem}.json"
        if path.exists() or meta_path.exists():
            if not path.exists() or not meta_path.exists():
                raise ValueError(f"Incomplete private checkpoint: {county}/{stem}")
            raw = path.read_bytes()
            meta = json.loads(meta_path.read_text())
            if meta["relative_source"] != relative or meta["sha256"] != hashlib.sha256(raw).hexdigest():
                raise ValueError(f"Checkpoint identity or hash mismatch: {county}/{stem}")
            headings, rows = _extract_rows(raw)
            if not required.issubset(headings) or len(rows) != meta["row_count"]:
                raise ValueError(f"Checkpoint content mismatch: {county}/{stem}")
            return raw, "saved"
        prior = self.failed.get(f"{county}/{stem}")
        if prior and prior["relative_source"] == relative and prior["reason"] == "http_404" and not self.args.retry_unresolved:
            say(f"STILL UNRESOLVED {county}/{stem}: prior HTTP 404; no repeat request")
            return None, "prior_http_404"
        if self.limit_reached():
            return None, "run_limit"
        if self.last_request is not None:
            elapsed = time.monotonic() - self.last_request
            target = random.uniform(self.args.min_interval, self.args.max_interval)
            delay = max(0, target - elapsed)
            if delay:
                say(f"WAIT {delay:.1f}s before requesting {county}/{stem}; archive request spacing")
                time.sleep(delay)
        if self.stop:
            return None, "researcher_stop"
        say(f"REQUEST {county}/{stem}: archived source page")
        self.last_request = time.monotonic()
        try:
            request = urllib.request.Request(archive_url(relative), headers=HEADERS)
            with urllib.request.urlopen(request, timeout=45) as response:
                raw, effective = response.read(), response.geturl()
        except urllib.error.HTTPError as exc:
            if exc.code == 429:
                self.stop = True
                say(f"ARCHIVE THROTTLED (HTTP 429) at {county}/{stem}; stopping; all unresolved items retained")
            else:
                say(f"UNRESOLVED HTTP {exc.code} at {county}/{stem}; moving to next item")
                if exc.code == 404:
                    self.remember_unresolved(county, stem, relative, "http_404")
            return None, f"http_{exc.code}"
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            say(f"UNRESOLVED network error at {county}/{stem}: {type(exc).__name__}; moving on")
            return None, "network_error"
        headings, rows = _extract_rows(raw)
        if not required.issubset(headings):
            say(f"UNRESOLVED unexpected table at {county}/{stem}; source not accepted")
            return None, "unexpected_table"
        temporary = path.with_suffix(".part")
        temporary.write_bytes(raw)
        temporary.replace(path)
        meta_path.write_text(json.dumps({"relative_source": relative, "effective_url": effective,
                                         "sha256": hashlib.sha256(raw).hexdigest(),
                                         "row_count": len(rows)}, ensure_ascii=False, indent=2) + "\n")
        self.new_pages += 1
        say(f"NEW SOURCE SAVED {county}/{stem}: {len(rows)} rows; new pages this run {self.new_pages}")
        return raw, "new"


def load_status():
    if not STATUS.exists():
        return {}
    with STATUS.open(newline="") as stream:
        return {row["county"]: row for row in csv.DictReader(stream)}


def write_status(status):
    OUT.mkdir(parents=True, exist_ok=True)
    temporary = STATUS.with_suffix(".part")
    with temporary.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(status[key] for key in sorted(status))
    temporary.replace(STATUS)


def inspect_county(worker, scope, status):
    # import pandas as pd
    # from IPython.display import display
    # # Display the results os all counties so far in a dataframe
    # county_status = pd.read_csv(STATUS)
    # display(county_status.sort_values("county").reset_index(drop=True))
    
    county = scope["county"]
    manifest = json.loads((CACHE / "county_manifests" / f"{county}.json").read_text())
    cutoff = Decimal(scope["last_saved_score"])
    expected = targets(manifest, cutoff)
    if len(expected) != int(scope["candidate_program_reports"]):
        raise ValueError(f"{county}: target count differs from frozen scope inventory")
    saved = Counter(map(signature, saved_rows(manifest, "admitted_placements")))
    admitted_total = int(scope["occupancy_admitted_total"])
    gap = admitted_total - sum(saved.values())
    if gap != int(scope["placement_shortfall"]):
        raise ValueError(f"{county}: county placement gap changed")
    menu = json.loads((CACHE / "county_menus" / f"{county}.json").read_text())
    soup = BeautifulSoup(base64.b64decode(menu["raw_html_base64"]), "html.parser")
    indices = [a.get("href", "") for a in soup.find_all("a", href=True)
               if "raport_specializari_adm.asp" in a.get("href", "")]
    if len(indices) != 1:
        raise ValueError(f"{county}: expected one destination-program index")
    raw_index, index_state = worker.retrieve(county, indices[0], "specialization_index", set())
    problems = []
    found = Counter()
    verified = 0
    if raw_index is None:
        problems.append(f"index:{index_state}")
    else:
        soup = BeautifulSoup(raw_index, "html.parser")
        links = [a.get("href", "") for a in soup.find_all("a", href=True)
                 if "raport_admisi_per_liceu.asp" in a.get("href", "")]
        for code, count in expected.items():
            if worker.stop or worker.limit_reached():
                break
            matches = [link for link in links
                       if re.search(r"(?:^|&)cs=" + str(code) + r"(?:&|\.)", link)]
            if len(matches) != 1:
                problems.append(f"program_{code}:index_link_count_{len(matches)}")
                continue
            raw, source_state = worker.retrieve(county, matches[0], f"destination_program_{code}",
                                                {"Nume", "Medie Admitere"})
            if raw is None:
                problems.append(f"program_{code}:{source_state}")
                continue
            _, rows = _extract_rows(raw)
            if len(rows) != count:
                problems.append(f"program_{code}:occupancy_mismatch_{len(rows)}_vs_{count}")
                continue
            verified += 1
            found.update(map(signature, rows))
            say(f"VERIFIED {county} program {code}: {len(rows)}/{count} occupancy rows")
    duplicates = sum(found.values()) - len(found)
    absent = sum((found - saved).values())
    if verified == len(expected) and not problems and not duplicates and absent == gap:
        state = "placement_views_reconciled"
    else:
        state = "unresolved"
        if verified == len(expected) and absent != gap:
            problems.append(f"gap_mismatch:{absent}_vs_{gap}")
        if duplicates:
            problems.append(f"duplicate_signatures:{duplicates}")
    if state == "placement_views_reconciled":
        detail = "placement source views reconcile; applicant completeness still unverified"
    else:
        if verified < len(expected) and not worker.stop and worker.limit_reached():
            problems.append("run_limit_reached; resume later")
        detail = "; ".join(problems) if problems else "source reports pending; resume later"
    result = {"county": county, "state": state, "target_programs": len(expected),
              "verified_programs": verified, "unresolved_programs": len(expected)-verified,
              "saved_county_placements": sum(saved.values()), "occupancy_admitted": admitted_total,
              "placement_gap": gap, "recovered_distinct_absent": absent,
              "duplicate_program_signatures": duplicates,
              "detail": detail}
    status[county] = result
    write_status(status)
    say(f"COUNTY {county}: {state}; verified {verified}/{len(expected)} reports; "
        f"absent signatures {absent}/{gap} gap; details: {result['detail']}")



def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="fetch source pages; omission previews queue only")
    parser.add_argument("--counties", nargs="*", help="specific county codes; default all remaining gap counties")
    parser.add_argument("--max-new-pages", type=int, default=40)
    parser.add_argument("--max-hours", type=float, default=2)
    parser.add_argument("--min-interval", type=float, default=10)
    parser.add_argument("--max-interval", type=float, default=12)
    parser.add_argument("--retry-unresolved", action="store_true",
                        help="explicitly retry previously recorded HTTP 404 source links")
    args = parser.parse_args(argv)
    if args.max_new_pages < 1 or args.max_hours <= 0 or args.min_interval < 1 or args.max_interval < args.min_interval:
        parser.error("Use positive bounds and max interval at least min interval")
    with SCOPE.open(newline="") as stream:
        scope = list(csv.DictReader(stream))
    scope.sort(key=lambda row: int(row["candidate_program_reports"]))
    wanted = set(args.counties or [])
    if wanted:
        unknown = wanted - {row["county"] for row in scope}
        if unknown:
            parser.error(f"Unknown county code(s): {sorted(unknown)}")
        scope = [row for row in scope if row["county"] in wanted]
    else:
        scope = [row for row in scope if row["county"] not in {"OT", "VS"}]
    say("QUEUE: " + ", ".join(f"{row['county']}({row['candidate_program_reports']})" for row in scope))
    if not args.run:
        say("PREVIEW ONLY. Add --run to request archived source pages.")
        return
    worker = Worker(args)
    def researcher_stop(_signum, _frame):
        worker.stop = True
        say("STOP REQUESTED: finishing the current page or wait, then recording unresolved county status")
    previous_handlers = None
    try:
        previous_handlers = (signal.getsignal(signal.SIGINT), signal.getsignal(signal.SIGTERM))
        signal.signal(signal.SIGINT, researcher_stop)
        signal.signal(signal.SIGTERM, researcher_stop)
    except ValueError:
        # Some notebook kernels execute cells outside Python's main thread.
        # Kernel interruption still preserves each completed page checkpoint.
        previous_handlers = None
    status = load_status()
    try:
        for row in scope:
            if worker.stop or worker.limit_reached():
                break
            inspect_county(worker, row, status)
        say(f"WORKER STOPPED: {worker.new_pages} new source pages this run; "
            f"aggregate status: {STATUS}; unresolved entries remain open")
    finally:
        if previous_handlers is not None:
            signal.signal(signal.SIGINT, previous_handlers[0])
            signal.signal(signal.SIGTERM, previous_handlers[1])


if __name__ == "__main__":
    main()
