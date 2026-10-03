"""Offline check of applicant gymnasium labels against the county school directory.

This is a SOURCE audit, not a student-outcome analysis. It makes no network
requests and does not export student names or scores. Only an unambiguous,
normalized *whole-name* match is counted as a direct school-code link. A
truncated name can suggest a school for human review but never assigns a code.

Run with --run from the notebook or command line. Without --run, preview only.
"""

import argparse
import csv
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

from EDUCATION_20261001_romania_offline_county_source_readiness import (
    CACHE, OUT as READINESS_OUT, ROOT, family_status, saved_rows,
)

OUT = ROOT / "outputs/romania_2001_origin_school_name_audit"
READINESS_CSV = READINESS_OUT / "EDUCATION_20261001_county_source_readiness.csv"
COUNT_FIELDS = [
    "county", "applicants", "directory_schools", "distinct_printed_school_labels",
    "direct_school_code_link_applicants", "possible_unique_name_applicants",
    "ambiguous_name_applicants", "no_directory_name_candidate_applicants",
    "outside_county_applicants", "missing_or_unreadable_school_label_applicants",
]
REVIEW_FIELDS = [
    "county", "printed_school_label", "applicants_with_label", "classification",
    "directory_code_candidates", "directory_name_candidates",
]


def normalized_school_name(value):
    """For comparison only: ignore accents, punctuation, spacing and case.

    This does not insert missing words, expand abbreviations, or make fuzzy
    matches. The full resulting string must agree for a direct link.
    """
    plain = unicodedata.normalize("NFKD", value.upper())
    plain = "".join(c for c in plain if not unicodedata.combining(c))
    return " ".join(re.findall(r"[A-Z0-9]+", plain))


def split_school_label(label):
    """Source labels normally end in '/ AB', '/ B', etc."""
    match = re.fullmatch(r"\s*(.*?)\s*/\s*([A-Z]{1,2})\s*", label)
    if match:
        return match.group(1), match.group(2)
    return label.strip(), None


def audit_county(county):
    manifest = json.loads((CACHE / "county_manifests" / f"{county}.json").read_text())
    for family in ("candidate_roster", "origin_school_directory"):
        complete, unresolved = family_status(manifest, family)
        if not complete or unresolved:
            raise ValueError(f"{county}: {family} is incomplete; source audit stops")

    applicants = saved_rows(manifest, "candidate_roster")
    directory = saved_rows(manifest, "origin_school_directory")
    by_name = defaultdict(list)
    for school in directory:
        code = school.get("Cod şcoală", "").strip()
        name = school.get("Nume şcoală", "").strip()
        if not code or not name:
            raise ValueError(f"{county}: directory has a missing school code or name")
        by_name[normalized_school_name(name)].append((code, name))

    labels = Counter(row.get("Şcoală", "").strip() for row in applicants)
    counts = Counter()
    review = []
    for label, n in sorted(labels.items()):
        school_name, printed_county = split_school_label(label)
        key = normalized_school_name(school_name)
        options = []
        if not key or printed_county is None:
            classification = "missing_or_unreadable_school_label"
        elif printed_county != county:
            classification = "outside_county_origin"
        else:
            exact = by_name.get(key, [])
            if len(exact) == 1:
                classification, options = "direct_whole_name_match", exact
            elif len(exact) > 1:
                classification, options = "ambiguous_same_directory_name", exact
            else:
                # One name may be a truncated prefix of the other. List such
                # candidates for review, but do not treat them as linked.
                possible = [school for directory_key, schools in by_name.items()
                            if len(key) >= 15 and len(directory_key) >= 15
                            and (directory_key.startswith(key) or key.startswith(directory_key))
                            for school in schools]
                options = possible
                if len(possible) == 1:
                    classification = "one_possible_name_needs_review"
                elif len(possible) > 1:
                    classification = "ambiguous_possible_names"
                else:
                    classification = "no_directory_name_candidate"
        counts[classification] += n
        review.append({
            "county": county,
            "printed_school_label": label,
            "applicants_with_label": n,
            "classification": classification,
            "directory_code_candidates": " | ".join(code for code, _ in options),
            "directory_name_candidates": " | ".join(name for _, name in options),
        })

    result = {
        "county": county, "applicants": len(applicants),
        "directory_schools": len(directory),
        "distinct_printed_school_labels": len(labels),
        "direct_school_code_link_applicants": counts["direct_whole_name_match"],
        "possible_unique_name_applicants": counts["one_possible_name_needs_review"],
        "ambiguous_name_applicants": (counts["ambiguous_same_directory_name"]
                                      + counts["ambiguous_possible_names"]),
        "no_directory_name_candidate_applicants": counts["no_directory_name_candidate"],
        "outside_county_applicants": counts["outside_county_origin"],
        "missing_or_unreadable_school_label_applicants": counts["missing_or_unreadable_school_label"],
    }
    if sum(result[field] for field in COUNT_FIELDS[4:]) != len(applicants):
        raise ValueError(f"{county}: school-label categories do not sum to applicants")
    return result, review


def complete_counties():
    with READINESS_CSV.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    return [row["county"] for row in rows
            if row["candidate_pages_complete"] == "True"
            and row["unassigned_pages_complete"] == "True"
            and row["placement_source_status"] != "placement_pages_unresolved"]


def save_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".part")
    with temporary.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="read saved pages and write aggregate outputs")
    parser.add_argument("--counties", nargs="*", help="county abbreviations; default all source-complete counties")
    args = parser.parse_args(argv)
    eligible = complete_counties()
    selected = args.counties or eligible
    unknown = set(selected) - set(eligible)
    if unknown:
        parser.error(f"These counties are not in the source-complete set: {sorted(unknown)}")
    print(f"Offline school-name check: {len(selected)} counties; no web requests or outcome analysis.", flush=True)
    if not args.run:
        print("Preview only. Pass --run after reviewing the county list:", ", ".join(selected), flush=True)
        return

    results, review = [], []
    for index, county in enumerate(selected, 1):
        counts, labels = audit_county(county)
        results.append(counts)
        review.extend(labels)
        print(f"{index}/{len(selected)} {county}: {counts['applicants']:,} applicants; "
              f"{counts['direct_school_code_link_applicants']:,} direct school-name matches; "
              f"{counts['possible_unique_name_applicants']:,} possible names need review; "
              f"{counts['ambiguous_name_applicants']:,} ambiguous; "
              f"{counts['outside_county_applicants']:,} from another county.", flush=True)

    counts_path = OUT / "county_school_name_match_counts.csv"
    review_path = OUT / "school_label_review.csv"
    save_csv(counts_path, COUNT_FIELDS, results)
    save_csv(review_path, REVIEW_FIELDS, review)
    totals = {field: sum(row[field] for row in results) for field in COUNT_FIELDS[1:]}
    ambiguous_labels = sum(row["classification"].startswith("ambiguous") for row in review)
    share = lambda count: f"{100 * count / totals['applicants']:.1f}%"
    report = [
        "# Romania 2001: originating-school name check", "",
        "This check reads saved applicant lists and school directories only. It does not fetch pages, calculate peer strength, or analyze placement outcomes.", "",
        f"**Counties checked:** {len(results)} ({', '.join(selected)}).",
        f"**Applicants in those saved lists:** {totals['applicants']:,}.",
        f"**Applicants whose printed school name directly identifies one directory school:** {totals['direct_school_code_link_applicants']:,} ({share(totals['direct_school_code_link_applicants'])}).",
        f"**Applicants with one possible but unverified directory name:** {totals['possible_unique_name_applicants']:,}.",
        f"**Applicants whose school name could identify more than one directory entry:** {totals['ambiguous_name_applicants']:,} ({share(totals['ambiguous_name_applicants'])}). These come from {ambiguous_labels} distinct printed school labels.",
        f"**Applicants with no directory-name candidate:** {totals['no_directory_name_candidate_applicants']:,}.",
        f"**Applicants whose printed school belongs to another county:** {totals['outside_county_applicants']:,} ({share(totals['outside_county_applicants'])}).",
        f"**Applicants with a missing or unreadable school label:** {totals['missing_or_unreadable_school_label_applicants']:,}.", "",
        "A direct match ignores only case, accent marks, punctuation, and spacing. Shortened names are never automatically accepted. The label review CSV lists school names and possible directory entries for human review; it contains no student names or scores.", "",
        "Next source check: review the small set of ambiguous local school labels and compare out-of-county labels with their own counties' saved school directories. Keep all unresolved labels open; do not guess a school code or drop these students silently.", "",
        "This is a name-link check, not proof that every eighth grader at a gymnasium participated. No county is authorized for a HERO curve by this report.", "",
    ]
    summary_path = OUT / "school_name_match_summary.md"
    summary_path.write_text("\n".join(report), encoding="utf-8")
    print("Saved counts:", counts_path, flush=True)
    print("Saved school-label review:", review_path, flush=True)
    print("Saved plain-English summary:", summary_path, flush=True)


if __name__ == "__main__":
    main()
