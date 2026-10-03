"""Offline follow-up for unresolved Romania 2001 origin-school labels.

Reads the previously saved school-label review and archived source checkpoints.
No network access, outcomes, peer metrics, student names, scores, or national
identifiers are written to the workspace. Direct name matches use only the
printed origin-county directory; shortened or repeated names remain unresolved.
Alba's existing school-specific reports can provide separate source support.
"""

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from EDUCATION_20261001_romania_offline_county_source_readiness import (
    CACHE, ROOT, family_status, saved_rows, signature,
)
from EDUCATION_20261001_romania_origin_school_name_audit import (
    OUT as FIRST_OUT, normalized_school_name, split_school_label, save_csv,
)

OUT = ROOT / "outputs/romania_2001_origin_school_followup"
ALBA_SCHOOL_CACHE = Path.home() / "Desktop/VECTOR_temp/romania_alba_2001_differentiation_v1/school_reports"
DETAIL_FIELDS = [
    "destination_county", "printed_school_label", "applicants_with_label",
    "original_category", "followup_category", "origin_county",
    "possible_school_codes", "possible_school_names",
]
COUNT_FIELDS = [
    "destination_county", "outside_applicants", "outside_direct_school_name_match",
    "outside_ambiguous_or_possible", "outside_no_name_match", "outside_directory_unavailable",
    "local_ambiguous_applicants", "local_supported_by_alba_school_report",
    "local_still_unresolved",
]


def directory_for(county):
    path = CACHE / "county_manifests" / f"{county}.json"
    if not path.exists():
        return None
    manifest = json.loads(path.read_text())
    complete, unresolved = family_status(manifest, "origin_school_directory")
    if not complete or unresolved:
        return None
    by_name = defaultdict(list)
    for row in saved_rows(manifest, "origin_school_directory"):
        code = row.get("Cod şcoală", "").strip()
        name = row.get("Nume şcoală", "").strip()
        if not code or not name:
            raise ValueError(f"{county}: school-directory entry lacks a code or name")
        by_name[normalized_school_name(name)].append((code, name))
    return by_name


def name_candidates(by_name, printed_name):
    key = normalized_school_name(printed_name)
    exact = by_name.get(key, [])
    if exact:
        return ("direct_whole_name_match" if len(exact) == 1 else "ambiguous_same_name"), exact
    possible = [school for directory_key, schools in by_name.items()
                if len(key) >= 15 and len(directory_key) >= 15
                and (directory_key.startswith(key) or key.startswith(directory_key))
                for school in schools]
    if possible:
        return "possible_name_needs_review", possible
    return "no_name_candidate", []


def alba_school_signatures(code):
    """Return only comparison keys; never export source student rows."""
    if not re.fullmatch(r"\d+", code):
        raise ValueError("Unexpected Alba school code")
    path = ALBA_SCHOOL_CACHE / f"school_{int(code):03d}.json"
    if not path.exists():
        return None
    payload = json.loads(path.read_text())
    rows = payload.get("rows", [])
    if payload.get("source_code") != code or payload.get("row_count") != len(rows):
        raise ValueError(f"Alba school-report identity/count mismatch for code {code}")
    digest = hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()
    if digest != payload.get("rows_sha256"):
        raise ValueError(f"Alba school-report row digest mismatch for code {code}")
    return Counter(key for row in rows if (key := signature(row)))


def alba_supported_count(label, codes):
    """Count provisional candidate matches uniquely corroborated by a school report."""
    manifest = json.loads((CACHE / "county_manifests/AB.json").read_text())
    candidate_rows = [row for row in saved_rows(manifest, "candidate_roster")
                      if row.get("Şcoală", "").strip() == label]
    school_keys = {code: alba_school_signatures(code) for code in codes}
    if any(keys is None for keys in school_keys.values()):
        return 0
    candidate_keys = Counter(key for row in candidate_rows if (key := signature(row)))
    supported = 0
    for key, count in candidate_keys.items():
        matches = [code for code, keys in school_keys.items() if keys[key] == 1]
        if count == 1 and len(matches) == 1:
            supported += 1
    return supported


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="perform the offline source check")
    args = parser.parse_args(argv)
    first_path = FIRST_OUT / "school_label_review.csv"
    if not first_path.exists():
        parser.error("Run the first school-name audit before this follow-up")
    with first_path.open(newline="", encoding="utf-8") as stream:
        pending = [row for row in csv.DictReader(stream)
                   if row["classification"] in {"outside_county_origin",
                                                "ambiguous_same_directory_name",
                                                "ambiguous_possible_names"}]
    print(f"Offline follow-up: {len(pending)} school-label groups; no web requests.", flush=True)
    if not args.run:
        print("Preview only; pass --run to read saved directories/reports.", flush=True)
        return

    directory_cache = {}
    counts = defaultdict(Counter)
    details = []
    for row in pending:
        county, label = row["county"], row["printed_school_label"]
        n = int(row["applicants_with_label"])
        printed_name, origin = split_school_label(label)
        category = row["classification"]
        options = []
        if category == "outside_county_origin":
            counts[county]["outside_applicants"] += n
            if origin not in directory_cache:
                directory_cache[origin] = directory_for(origin)
            directory = directory_cache[origin]
            if directory is None:
                followup = "origin_directory_unavailable"
                counts[county]["outside_directory_unavailable"] += n
            else:
                followup, options = name_candidates(directory, printed_name)
                field = {
                    "direct_whole_name_match": "outside_direct_school_name_match",
                    "ambiguous_same_name": "outside_ambiguous_or_possible",
                    "possible_name_needs_review": "outside_ambiguous_or_possible",
                    "no_name_candidate": "outside_no_name_match",
                }[followup]
                counts[county][field] += n
        else:
            counts[county]["local_ambiguous_applicants"] += n
            codes = [code.strip() for code in row["directory_code_candidates"].split("|") if code.strip()]
            if county == "AB" and len(codes) > 1:
                supported = alba_supported_count(label, codes)
                counts[county]["local_supported_by_alba_school_report"] += supported
                counts[county]["local_still_unresolved"] += n - supported
                followup = (f"alba_school_report_supports_{supported}_of_{n}"
                            if supported else "no_unique_school_report_support")
            else:
                counts[county]["local_still_unresolved"] += n
                followup = "needs_school_specific_source_review"
            options = list(zip(codes, [s.strip() for s in row["directory_name_candidates"].split("|")]))
        details.append({
            "destination_county": county, "printed_school_label": label,
            "applicants_with_label": n, "original_category": category,
            "followup_category": followup, "origin_county": origin or "",
            "possible_school_codes": " | ".join(code for code, _ in options),
            "possible_school_names": " | ".join(name for _, name in options),
        })

    counties = sorted(counts)
    county_rows = [dict(destination_county=county,
                        **{field: counts[county][field] for field in COUNT_FIELDS[1:]})
                   for county in counties]
    save_csv(OUT / "county_followup_counts.csv", COUNT_FIELDS, county_rows)
    save_csv(OUT / "school_label_followup_review.csv", DETAIL_FIELDS, details)
    totals = {field: sum(row[field] for row in county_rows) for field in COUNT_FIELDS[1:]}
    if totals["outside_applicants"] != sum(totals[f] for f in COUNT_FIELDS[2:6]):
        raise ValueError("Out-of-county follow-up counts do not balance")
    if totals["local_ambiguous_applicants"] != (totals["local_supported_by_alba_school_report"]
                                                + totals["local_still_unresolved"]):
        raise ValueError("Local ambiguity counts do not balance")
    summary = [
        "# Romania 2001: second school-source check", "",
        "This is an offline source check, not an outcome analysis. It reads the saved directories for the counties printed beside applicants' school names. No student names, scores, or national identifiers are exported.", "",
        f"**Plain-English result:** {totals['outside_direct_school_name_match']:,} of {totals['outside_applicants']:,} out-of-county applicants have a direct school-directory match. The saved Alba school reports support {totals['local_supported_by_alba_school_report']:,} more applicants whose local school names were ambiguous. {totals['outside_ambiguous_or_possible'] + totals['outside_no_name_match'] + totals['outside_directory_unavailable'] + totals['local_still_unresolved']:,} school links remain unresolved across the audited counties.", "",
        f"**Applicants from a different county:** {totals['outside_applicants']:,}.",
        f"- Printed school name directly identifies one entry in its own county directory: {totals['outside_direct_school_name_match']:,}.",
        f"- Printed school name is ambiguous or only a possible shortened-name match: {totals['outside_ambiguous_or_possible']:,}.",
        f"- No school-name candidate found in that directory: {totals['outside_no_name_match']:,}.",
        f"- Origin-county directory unavailable: {totals['outside_directory_unavailable']:,}.", "",
        f"**Applicants with ambiguous local school names:** {totals['local_ambiguous_applicants']:,}.",
        f"- Provisional name-and-score match uniquely supported by an already saved Alba school-specific applicant report: {totals['local_supported_by_alba_school_report']:,}.",
        f"- Still unresolved: {totals['local_still_unresolved']:,}.", "",
        "A direct school-name match uses only case, accent, punctuation and spacing normalization. Alba's school-report support is a second source comparison, not proof of a unique national person identifier. Ambiguous or unmatched labels remain open, and no applicant is silently removed.", "",
        "The next bounded source gate is to verify whether the county applicant lists cover the whole *participating applicant group* for each originating gymnasium, including students who applied to another county. School-specific applicant reports are an independent check where saved. The remaining ambiguous names may also need those reports. This check does not establish complete gymnasium cohorts or authorize a HERO curve.", "",
    ]
    path = OUT / "school_source_followup_summary.md"
    path.write_text("\n".join(summary), encoding="utf-8")
    print("Direct home-county school-name matches:",
          f"{totals['outside_direct_school_name_match']:,}/{totals['outside_applicants']:,}", flush=True)
    print("Ambiguous local applicants still unresolved:",
          f"{totals['local_still_unresolved']:,}/{totals['local_ambiguous_applicants']:,}", flush=True)
    print("Saved plain-English summary:", path, flush=True)


if __name__ == "__main__":
    main()
