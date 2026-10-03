"""Freeze a source-only gymnasium sample for the four-county Romania pilot.

Alba already has every origin-school report. For CS, GL, and TL, preselect
school-specific applicant reports using only counts in the saved county lists.
No network requests, student names, examination scores, or placements are used.
"""

import argparse
import csv
import json
import random
import re
from collections import Counter

from EDUCATION_20261001_romania_offline_county_source_readiness import CACHE, ROOT, family_status
from EDUCATION_20261001_romania_origin_school_name_audit import OUT as FIRST_OUT, save_csv

COUNTIES = ("CS", "GL", "TL")
SEED = 20261001
OUT = ROOT / "outputs/romania_2001_four_county_source_pilot"
FIELDS = ["county", "source_school_code", "school_name", "sample_stratum",
          "applicants_listed_in_county_report", "school_report_relative_url"]


def school_directory(county):
    manifest = json.loads((CACHE / "county_manifests" / f"{county}.json").read_text())
    complete, unresolved = family_status(manifest, "origin_school_directory")
    if not complete or unresolved:
        raise ValueError(f"{county}: school directory is incomplete")
    rows = []
    links = {}
    for page in manifest["families"]["origin_school_directory"]["pages"]:
        saved = json.loads((CACHE / page["file"]).read_text())
        rows.extend(saved["rows"])
        for relative in saved["discovered_links"]:
            if "raport_candidati_per_scoala" not in relative:
                continue
            match = re.search(r"(?:[?&-])cs=(\d+)(?:[&.]|$)", relative, re.I)
            if match:
                code = match.group(1)
                if code in links and links[code] != relative:
                    raise ValueError(f"{county}: multiple source links for school {code}")
                links[code] = relative
    schools = {}
    for row in rows:
        code = row["Cod şcoală"].strip()
        if code in schools or code not in links:
            raise ValueError(f"{county}: duplicate code or missing school-specific link {code}")
        schools[code] = (row["Nume şcoală"].strip(), links[code])
    return schools


def listed_applicants():
    path = FIRST_OUT / "school_label_review.csv"
    counts = Counter()
    with path.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            if row["county"] not in COUNTIES or row["classification"] != "direct_whole_name_match":
                continue
            code = row["directory_code_candidates"].strip()
            if not code.isdigit():
                raise ValueError("Direct school-name match did not provide exactly one code")
            counts[(row["county"], code)] += int(row["applicants_with_label"])
    return counts


def select_county(county, schools, counts):
    rng = random.Random(SEED + sum(ord(char) for char in county))
    # Some directory entries are clubs, special schools, or other institutions.
    # The zero-list probe must sample plausible ordinary gymnasiums instead.
    zero = sorted(code for code, (name, _) in schools.items()
                  if counts[(county, code)] == 0
                  and name.upper().startswith("SCOALA")
                  and not any(word in name.upper() for word in
                              ("SPECIAL", "CLUB", "SPORTIV", "MUZICA", "ARTE", "CAMIN")))
    positive = sorted((code for code in schools if counts[(county, code)] > 0),
                      key=lambda code: (counts[(county, code)], int(code)))
    if len(zero) < 2 or len(positive) < 10:
        raise ValueError(f"{county}: not enough schools for frozen size-stratified sample")
    thirds = [positive[:len(positive)//3],
              positive[len(positive)//3:2*len(positive)//3],
              positive[2*len(positive)//3:]]
    result = []
    for label, population, n in [
        ("zero_in_county_list", zero, 2),
        ("small_listed_group", thirds[0], 3),
        ("middle_listed_group", thirds[1], 4),
        ("large_listed_group", thirds[2], 3),
    ]:
        for code in sorted(rng.sample(population, n), key=int):
            name, relative = schools[code]
            result.append({
                "county": county, "source_school_code": code, "school_name": name,
                "sample_stratum": label,
                "applicants_listed_in_county_report": counts[(county, code)],
                "school_report_relative_url": relative,
            })
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="write the frozen offline sample")
    args = parser.parse_args(argv)
    print("Four-county source pilot: AB already complete; planning 12 schools each in CS, GL, TL.", flush=True)
    if not args.run:
        print("Preview only. No archive pages requested. Use --run to freeze the sample.", flush=True)
        return
    counts = listed_applicants()
    selected = []
    for county in COUNTIES:
        schools = school_directory(county)
        rows = select_county(county, schools, counts)
        selected.extend(rows)
        print(f"{county}: {len(schools)} directory schools; {len(rows)} selected by size stratum.", flush=True)
    path = OUT / "frozen_school_report_sample.csv"
    save_csv(path, FIELDS, selected)
    narrative = [
        "# Romania 2001 four-county source pilot: frozen school sample", "",
        "The four counties were chosen before this source check: Alba (AB), Caraș-Severin (CS), Galați (GL), and Tulcea (TL). This is a source-completeness exercise, not an outcome analysis.", "",
        "Alba's 168 school-specific applicant reports were already recovered. Their prior audit found 78 applicant-name occurrences across 44 schools beyond the matching Alba county-list labels; those occurrences are not assumed to be 78 distinct students.", "",
        "For each of CS, GL, and TL, the attached CSV freezes 12 source school codes: two plausible ordinary schools with no applicant in that county list, three from the smaller positive groups, four from the middle groups, and three from the larger groups. Clubs and special schools are excluded from the zero-list stratum. Sampling is deterministic (seed 20261001) and uses only county-list applicant counts. It does not use examination scores, placements, or later success.", "",
        "The next step, after the ongoing background acquisition is out of the way, is a **source-only retrieval** of these 36 school-specific applicant reports. Compare each report's names and admission scores with the saved county applicant lists in memory, export only aggregate discrepancies, and keep failed requests unresolved. A sample checks whether county lists miss origin-school applicants; it cannot certify all schools in a county.", "",
        "No Wayback request was made in freezing this sample. No student names, scores, or identifiers are exported here.", "",
    ]
    report = OUT / "frozen_sample_reasoning.md"
    # This initial scaffold was later expanded with the completed source audit.
    # Re-running selection must not erase that manually maintained provenance.
    report_already_exists = report.exists()
    if not report_already_exists:
        report.write_text("\n".join(narrative), encoding="utf-8")
    print("Saved sample:", path, flush=True)
    print("Preserved reasoning:" if report_already_exists else "Saved reasoning:", report, flush=True)


if __name__ == "__main__":
    main()
