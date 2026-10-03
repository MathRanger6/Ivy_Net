"""Read-only count of sampled school-view rows unmatched to county school codes.

This temporary diagnostic prints aggregates only. It does not save student data,
make web requests, or infer that equal printed names and scores prove identity.
"""

import csv
import json
from collections import Counter, defaultdict

from EDUCATION_20261001_romania_four_county_school_report_check import (
    SAMPLE, county_school_keys, verified_private_page,
)
from EDUCATION_20261001_romania_offline_county_source_readiness import (
    CACHE, saved_rows, signature, placement_status, verified_program_rows,
)
from EDUCATION_20261001_romania_origin_school_name_audit import OUT as NAME_OUT


with SAMPLE.open(newline="", encoding="utf-8") as stream:
    sample = list(csv.DictReader(stream))

direct_school_keys = county_school_keys()
all_county_keys = {}
for county in ("CS", "GL", "TL"):
    manifest = json.loads((CACHE / "county_manifests" / f"{county}.json").read_text())
    by_key = defaultdict(list)
    for candidate in saved_rows(manifest, "candidate_roster"):
        key = signature(candidate)
        if key:
            by_key[key].append(candidate.get("Şcoală", "").strip())
    all_county_keys[county] = by_key

label_class = {}
with (NAME_OUT / "school_label_review.csv").open(newline="", encoding="utf-8") as stream:
    for label in csv.DictReader(stream):
        label_class[(label["county"], label["printed_school_label"])] = label["classification"]

summary = defaultdict(Counter)
extra_records = []
for school in sample:
    county, code = school["county"], school["source_school_code"]
    payload = verified_private_page(school)
    if payload is None:
        raise ValueError(f"Saved school page missing for {county}/{code}; stop")
    school_keys = Counter(signature(row) for row in payload["rows"])
    extras = school_keys - direct_school_keys[(county, code)]
    for key, count in extras.items():
        extra_records.append((county, code, key, count))
        labels = all_county_keys[county].get(key, [])
        if not labels:
            summary[county]["not_found_by_name_and_score_in_county_view"] += count
            continue
        summary[county]["found_by_name_and_score_somewhere_in_county_view"] += count
        if len(labels) > 1:
            summary[county]["multiple_county_rows_share_name_and_score"] += count
        classes = {label_class.get((county, label), "unclassified_label") for label in labels}
        for category in classes:
            summary[county][f"printed_school_label_{category}"] += count

for county in ("CS", "GL", "TL"):
    print(county, dict(sorted(summary[county].items())), flush=True)
print("TOTAL", dict(sorted(sum((summary[c] for c in ("CS", "GL", "TL")), Counter()).items())), flush=True)

# Broaden only the lookup, not the data: search already saved candidate pages
# in other counties. Do not write names/scores or treat an equal signature as
# proof of a unique person.
other_candidate_keys = {}
for path in sorted((CACHE / "county_manifests").glob("*.json")):
    county = path.stem
    manifest = json.loads(path.read_text())
    other_candidate_keys[county] = Counter(
        signature(row) for row in saved_rows(manifest, "candidate_roster")
        if signature(row)
    )

cross_county = defaultdict(Counter)
for home, code, key, count in extra_records:
    located = [county for county, keys in other_candidate_keys.items()
               if county != home and keys[key]]
    if located:
        cross_county[home]["name_and_score_found_in_another_county_view"] += count
        if len(located) > 1:
            cross_county[home]["matching_rows_in_multiple_other_counties"] += count
    else:
        cross_county[home]["name_and_score_not_found_in_saved_county_views"] += count

for county in ("CS", "GL", "TL"):
    print("OTHER_COUNTIES", county, dict(sorted(cross_county[county].items())), flush=True)
print("OTHER_COUNTIES_TOTAL", dict(sorted(sum((cross_county[c] for c in ("CS", "GL", "TL")), Counter()).items())), flush=True)

unlocated = [(home, code, key, count) for home, code, key, count in extra_records
             if not any(keys[key] for county, keys in other_candidate_keys.items()
                        if county != home)]
target_keys = {key for _, _, key, _ in unlocated}
outcome_locations = defaultdict(set)
manifests = list(sorted((CACHE / "county_manifests").glob("*.json")))
for path in manifests:
    county = path.stem
    manifest = json.loads(path.read_text())
    for family, score_field in (("admitted_placements", "Medie Admitere"),
                                ("unassigned_applicants", "Media admitere")):
        for row in saved_rows(manifest, family):
            key = signature(row, score_field)
            if key in target_keys:
                outcome_locations[key].add((county, family))

progress = placement_status()
for path in manifests:
    county = path.stem
    info = progress.get(county, {})
    if info.get("state") != "placement_views_reconciled":
        continue
    for row in verified_program_rows(county, int(info["verified_programs"])):
        key = signature(row)
        if key in target_keys:
            outcome_locations[key].add((county, "recovered_program_placement"))

outcome_counts = defaultdict(Counter)
for home, code, key, count in unlocated:
    locations = outcome_locations[key]
    if not locations:
        outcome_counts[home]["not_found_in_saved_placement_or_unassigned_views"] += count
    else:
        outcome_counts[home]["found_in_saved_placement_or_unassigned_views"] += count
        for family in {family for _, family in locations}:
            outcome_counts[home][f"found_in_{family}"] += count

for county in ("CS", "GL", "TL"):
    print("OUTCOME_VIEWS", county, dict(sorted(outcome_counts[county].items())), flush=True)
print("OUTCOME_VIEWS_TOTAL", dict(sorted(sum((outcome_counts[c] for c in ("CS", "GL", "TL")), Counter()).items())), flush=True)

patterns = defaultdict(Counter)
for home, code, key, count in unlocated:
    kinds = tuple(sorted({family for _, family in outcome_locations[key]}))
    counties = {county for county, _ in outcome_locations[key]}
    geography = ("multiple_counties" if len(counties) > 1 else
                 "home_county" if counties == {home} else "another_county")
    patterns[home][(kinds, geography)] += count
for county in ("CS", "GL", "TL"):
    for (kinds, geography), count in sorted(patterns[county].items()):
        print("OUTCOME_PATTERN", county, kinds, geography, count, flush=True)
print("SIGNATURES", "appearances", sum(count for _, _, _, count in extra_records),
      "distinct_name_score_pairs", len({key for _, _, key, _ in extra_records}), flush=True)
