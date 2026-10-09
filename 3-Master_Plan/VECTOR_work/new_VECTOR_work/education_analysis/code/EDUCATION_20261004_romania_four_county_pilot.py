"""Researcher-run, county-configurable Romania 2001 descriptive placement pilot.

This module makes no network requests and performs no analysis on import.
``run_pilot`` reads verified private source checkpoints, then writes only
name-free aggregate tables, figures, and a plain-English report. The plots
are descriptive associations, not causal estimates or institutional K/N.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from EDUCATION_20260930_romania_2001_national_acquisition import CACHE
from EDUCATION_20260930_romania_placements_and_hero import COMBINED_CATEGORIES
from EDUCATION_20261001_romania_offline_county_source_readiness import placement_status, saved_rows
from EDUCATION_20261002_romania_full_gymnasium_offline_reconciliation import (
    all_gymnasium_rows, name_score, saved_national_indexes,
)
from EDUCATION_20261003_romania_four_county_program_identity_gate import (
    clean, local_placement_rows, source_programs,
)
from EDUCATION_20261007_romania_bucharest_plot_source_gate import (
    GATE as BUCHAREST_GATE, verify_bucharest,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs/romania_2001_four_county_descriptive_pilot"
DECISIONS = ROOT / "docs/decisions/EDUCATION_20261002_Romania_four_county_pilot_design_decisions.md"
SOURCE_GATE = ROOT / "outputs/romania_2001_four_county_source_pilot/program_identity_source_gate.csv"
BAND_COLORS = ("#73afd2", "#999999", "#e58b25", "#a43d4c")
ORIGINAL_COUNTIES = ("AB", "CS", "GL", "TL")
COUNTY_NAMES = {"AB": "Alba", "CS": "Caraș-Severin", "GL": "Galați", "TL": "Tulcea",
                "AR": "Arad", "SB": "Sibiu", "B": "Bucharest–Ilfov"}
EXPANSION_GATE = ROOT / "outputs/romania_2001_county_expansion_20261004/AR_SB_program_outcome_gate.csv"


@dataclass(frozen=True)
class Settings:
    """All choices exposed in the notebook's first code cell."""

    top_tiers: tuple[int, ...] = (1, 2)
    require_full_programs: bool = True
    combine_program_categories: bool = False
    include_vocational_in_primary: bool = True
    compare_excluding_ambiguous: bool = True
    compare_excluding_vocational: bool = True
    compare_pooled_score_bands: bool = True
    ai_percentile_cuts: tuple[int, int, int] = (90, 75, 50)
    peer_strength_bins: int = 8
    hero_bins: int = 16
    # Explicit scope avoids modifying a shared module's global county list.
    counties: tuple[str, ...] = ORIGINAL_COUNTIES

    def validate(self):
        if (not self.counties or len(set(self.counties)) != len(self.counties)
                or not set(self.counties).issubset(COUNTY_NAMES)):
            raise ValueError("counties must be distinct supported county codes: AB, CS, GL, TL, AR, SB, B")
        if not self.top_tiers or any(t < 1 or type(t) is not int for t in self.top_tiers):
            raise ValueError("top_tiers must contain positive integers")
        if len(set(self.top_tiers)) != len(self.top_tiers):
            raise ValueError("top_tiers contains a repeated tier")
        if self.peer_strength_bins < 3 or self.hero_bins < 3:
            raise ValueError("Plot bin counts must be at least three")
        cuts = self.ai_percentile_cuts
        if (len(cuts) != 3 or any(type(value) is not int for value in cuts)
                or not 0 < cuts[2] < cuts[1] < cuts[0] < 100):
            raise ValueError(
                "ai_percentile_cuts must be three descending whole-number percentiles, "
                "for example (90, 75, 50)"
            )


def _band_labels(settings):
    top, excellence, middle = settings.ai_percentile_cuts
    return (f"Below {middle}th", f"{middle}th–{excellence}th",
            f"{excellence}th–{top}th (excellence)", f"Top {100-top}%")


def _program_catalog(county):
    manifest = json.loads((CACHE / "county_manifests" / f"{county}.json").read_text())
    programs = source_programs(manifest, county)
    catalog = {}
    for code, source, places, admitted, vacancies, cutoff in programs:
        catalog[code] = {
            "code": code, "school": clean(source["Liceu"]),
            "category": clean(source["Specializare"]), "level": clean(source["Nivel"]),
            "places": places, "admitted": admitted, "vacancies": vacancies,
            "cutoff": float(cutoff) if cutoff is not None else None,
        }
    return manifest, programs, catalog


def _winner_codes(catalog, tier, settings):
    by_category = defaultdict(set)
    for program in catalog.values():
        if (program["places"] <= 0 or program["admitted"] <= 0
                or program["cutoff"] is None
                or (settings.require_full_programs and program["vacancies"] != 0)):
            continue
        category = (COMBINED_CATEGORIES[program["category"]]
                    if settings.combine_program_categories else program["category"])
        by_category[category].add(program["cutoff"])
    thresholds = {category: sorted(scores, reverse=True)[:tier]
                  for category, scores in by_category.items()}
    winners = set()
    for code, program in catalog.items():
        category = (COMBINED_CATEGORIES[program["category"]]
                    if settings.combine_program_categories else program["category"])
        if (program["places"] > 0 and program["admitted"] > 0
                and (not settings.require_full_programs or program["vacancies"] == 0)
                and program["cutoff"] in thresholds.get(category, [])):
            winners.add(code)
    return winners


def _destination_options(report, county, catalog, by_identity):
    """Return every exact directory program consistent with one source row."""
    if "__source_program_code" in report:
        code = report["__source_program_code"]
        if code not in catalog:
            raise ValueError(f"{county}: verified source program absent from directory")
        return [code]
    destination = clean(report.get("Liceu"))
    if destination.endswith(f" / {county}"):
        destination = destination[:-(len(county) + 3)]
    identity = (destination, clean(report.get("Profil")),
                clean(report.get("Specializare")))
    return by_identity[identity]


def _classify(key, county, local, national_placements, national_unassigned,
              catalog, by_identity, winners):
    """Keep exact program uncertainty distinct from binary outcome certainty."""
    reports = local[key]
    if len(reports) == 1:
        options = _destination_options(reports[0], county, catalog, by_identity)
        if not options:
            return "unmatched_program", np.nan, False, False
        possible = {code in winners for code in options}
        if len(possible) != 1:
            return "mixed_program_success", np.nan, False, len(options) > 1
        vocational = all(catalog[code]["level"] == "Profesional"
                         or catalog[code]["category"] == "Profesional" for code in options)
        return ("local_unique_program" if len(options) == 1 else "local_ambiguous_program",
                int(next(iter(possible))), vocational, len(options) > 1)
    if len(reports) > 1:
        return "ambiguous_person", np.nan, False, False
    if len(national_unassigned[key]) == 1 and not national_placements[key]:
        return "confirmed_unassigned", 0, False, False
    if len(national_placements[key]) == 1 and national_placements[key][0] != county:
        return "placed_other_county", np.nan, False, False
    return "unresolved_outcome", np.nan, False, False


def _county_movement(county, gymnasiums, directories, manifest, reports,
                     national_placements, national_unassigned, origin_by_person):
    """Describe origin/destination counties before any outcome exclusions.

    Incoming share uses all placements IN the county. Outgoing share uses all
    observed applicants FROM its gymnasiums. Unknowns are separate, never zero.
    This observes school locations, not family relocation or student intent.
    """
    rows = gymnasiums[county]
    sizes = Counter(code for code, _key, _comp in rows)
    outcomes = Counter()
    for _code, key, _comp in rows:
        placed, unassigned = national_placements[key], national_unassigned[key]
        if len(placed) + len(unassigned) != 1:
            outcomes["origin_outcome_unresolved"] += 1
        elif unassigned:
            outcomes["origin_unassigned"] += 1
        elif placed[0] == county:
            outcomes["origin_placed_locally"] += 1
        else:
            outcomes["outgoing_students"] += 1

    # The county applicant list prints originating-school county suffixes.
    # Use that evidence for students whose gymnasiums lie beyond our six,
    # rather than misclassifying every unmatched local signature as incoming.
    applicant_origins = defaultdict(list)
    for row in saved_rows(manifest, "candidate_roster"):
        match = re.search(r"/\s*([A-Z]{1,2})\s*$", clean(row.get("Şcoală")))
        applicant_origins[name_score(row)].append(match.group(1) if match else None)
    available_counties = {path.stem for path in (CACHE / "county_manifests").glob("*.json")}
    destination_counts = Counter()
    for row in reports:
        key = name_score(row)
        printed = applicant_origins.get(key, [])
        origin = origin_by_person.get(key)
        if len(printed) > 1:
            origin = None
        elif len(printed) == 1 and printed[0] in available_counties:
            origin = printed[0] if origin is None or origin == printed[0] else None
        unique_destination = national_placements[key] == [county] and not national_unassigned[key]
        if origin is None or not unique_destination:
            destination_counts["destination_origin_unresolved"] += 1
        elif origin == county:
            destination_counts["destination_from_own_county"] += 1
        else:
            destination_counts["incoming_students"] += 1
    if sum(outcomes.values()) != len(rows) or sum(destination_counts.values()) != len(reports):
        raise ValueError(f"{county}: movement categories do not add to their source totals")
    return {
        "county": county, "county_name": COUNTY_NAMES[county],
        "directory_gymnasiums": directories[county], "participating_gymnasiums": len(sizes),
        "gymnasiums_with_two_or_more_applicants": sum(n >= 2 for n in sizes.values()),
        "origin_applicants": len(rows), "destination_placements": len(reports),
        **{key: outcomes[key] for key in ("origin_placed_locally", "outgoing_students",
                                        "origin_unassigned", "origin_outcome_unresolved")},
        **{key: destination_counts[key] for key in ("incoming_students", "destination_from_own_county",
                                                  "destination_origin_unresolved")},
        "outgoing_pct_of_origin_applicants": 100 * outcomes["outgoing_students"] / len(rows),
        "incoming_pct_of_destination_placements": (
            100 * destination_counts["incoming_students"] / len(reports) if reports else np.nan),
    }


def _load_rows(settings, *, source_only=False):
    """Recheck saved sources, then hold personal fields only in local memory."""
    print("Step 1/4 — verifying gymnasium and county source checkpoints...", flush=True)
    gymnasiums, directories = all_gymnasium_rows(settings.counties)
    # B's older county applicant/unassigned series is incomplete. Its verified
    # originating-school result pages provide the outcome source instead.
    index_counties = tuple(county for county in settings.counties if county != "B")
    _, national_placements, national_unassigned, _ = saved_national_indexes(index_counties)
    progress = placement_status()
    all_keys = Counter(key for group in gymnasiums.values() for _code, key, _comp in group)
    if None in all_keys or max(all_keys.values()) != 1:
        raise ValueError("Gymnasium printed name-score signatures are incomplete or repeated")
    frames = []
    selected_programs = []
    overview = []
    origin_by_person = {key: county for county, rows in gymnasiums.items() for _code, key, _comp in rows}
    for county in settings.counties:
        manifest, source_program_rows, catalog = _program_catalog(county)
        reports = local_placement_rows(manifest, county, progress, source_program_rows)
        if len(reports) != sum(p["admitted"] for p in catalog.values()):
            raise ValueError(f"{county}: placement count disagrees with program occupancy")
        if county == "B":
            b_outcomes, audit = verify_bucharest(gymnasiums[county], reports,
                                                 national_placements)
            if not BUCHAREST_GATE.exists() or json.loads(BUCHAREST_GATE.read_text()) != audit:
                raise ValueError("B school-result source gate is absent or differs from saved sources")
            for key, outcome in b_outcomes.items():
                if outcome == "unassigned":
                    national_unassigned[key] = ["B"]
            sizes = Counter(code for code, _key, _comp in gymnasiums[county])
            overview.append({
                "county": county, "county_name": COUNTY_NAMES[county],
                "directory_gymnasiums": directories[county],
                "participating_gymnasiums": len(sizes),
                "gymnasiums_with_two_or_more_applicants": sum(n >= 2 for n in sizes.values()),
                "origin_applicants": audit["origin_applicants"],
                "destination_placements": audit["local_placement_reports"],
                "origin_placed_locally": audit["local"],
                "outgoing_students": audit["external"],
                "origin_unassigned": audit["unassigned"],
                "origin_outcome_unresolved": 0,
                "incoming_students": audit["incoming_admitted"],
                "destination_from_own_county": audit["local"],
                "destination_origin_unresolved": 0,
                "outgoing_pct_of_origin_applicants": 100 * audit["external"] / audit["origin_applicants"],
                "incoming_pct_of_destination_placements": 100 * audit["incoming_admitted"] / len(reports),
            })
        else:
            overview.append(_county_movement(county, gymnasiums, directories, manifest, reports,
                                            national_placements, national_unassigned, origin_by_person))
        if source_only:
            continue
        local = defaultdict(list)
        for report in reports:
            key = name_score(report)
            if key is None:
                raise ValueError(f"{county}: blank printed name or score in placement report")
            local[key].append(report)
        by_identity = defaultdict(list)
        for code, source, *_rest in source_program_rows:
            identity = tuple(clean(source[field]) for field in ("Liceu", "Profil", "Specializare"))
            by_identity[identity].append(code)
        group_sizes = Counter(code for code, _key, _comp in gymnasiums[county])
        group_sums = defaultdict(float)
        for code, _key, components in gymnasiums[county]:
            if components is None:
                raise ValueError(f"{county}: missing national examination component")
            group_sums[code] += float(components[0])
        winners_by_tier = {tier: _winner_codes(catalog, tier, settings)
                           for tier in settings.top_tiers}
        for tier, winners in winners_by_tier.items():
            for code in sorted(winners):
                p = catalog[code]
                selected_programs.append({"county": county, "tier": tier,
                                          "program_code": code, "category": p["category"],
                                          "school": p["school"], "cutoff": p["cutoff"],
                                          "places": p["places"], "admitted": p["admitted"]})
        for code, key, components in gymnasiums[county]:
            own_exam = float(components[0])
            n_peers = group_sizes[code] - 1
            peer_mean = (group_sums[code] - own_exam) / n_peers if n_peers else np.nan
            for tier, winners in winners_by_tier.items():
                status, success, vocational, ambiguous = _classify(
                    key, county, local, national_placements, national_unassigned,
                    catalog, by_identity, winners)
                frames.append({"county": county, "gymnasium": code, "tier": tier,
                               "exam": own_exam, "peer_mean_exam": peer_mean,
                               "peer_count": n_peers, "status": status,
                               "success": success, "vocational_destination": vocational,
                               "ambiguous_exact_program": ambiguous})
        print(f"  {county}: {len(gymnasiums[county]):,} applicant rows; "
              f"{len(catalog)} programs; source counts agree", flush=True)
    if source_only:
        return pd.DataFrame(overview)
    frame = pd.DataFrame(frames)
    chosen = pd.DataFrame(selected_programs)
    if frame.empty or chosen.empty:
        raise ValueError("No source-backed analysis rows or qualifying programs")
    return frame, chosen, pd.DataFrame(overview)


def source_preview(settings):
    """Read-only county size/movement summary; no scientific outcome plots."""
    settings.validate()
    return _load_rows(settings, source_only=True)


def _add_bands(frame, settings):
    """Freeze score bands from every participating applicant, not outcome rows."""
    print("Step 2/4 — defining county and pooled examination-score bands...", flush=True)
    top, excellence, middle = settings.ai_percentile_cuts
    top_q, excellence_q, middle_q = (value / 100 for value in (top, excellence, middle))
    labels = _band_labels(settings)
    first = frame.loc[frame["tier"] == settings.top_tiers[0], ["county", "exam"]]
    pooled = first["exam"].quantile([middle_q, excellence_q, top_q]).to_dict()
    boundaries = []
    county_edges = {}
    for county in settings.counties:
        scores = first.loc[first["county"] == county, "exam"]
        edges = scores.quantile([middle_q, excellence_q, top_q]).to_dict()
        county_edges[county] = edges
        boundaries.append({"county": county, "n_applicants": len(scores),
                           "middle_percentile": middle,
                           "excellence_start_percentile": excellence,
                           "top_start_percentile": top,
                           "middle_exam_boundary": edges[middle_q],
                           "excellence_start_exam_boundary": edges[excellence_q],
                           "top_start_exam_boundary": edges[top_q],
                           "pooled_middle_exam_boundary": pooled[middle_q],
                           "pooled_excellence_start_exam_boundary": pooled[excellence_q],
                           "pooled_top_start_exam_boundary": pooled[top_q]})
    def assign(scores, edges):
        return np.select([scores >= edges[top_q], scores >= edges[excellence_q],
                          scores >= edges[middle_q]],
                         [labels[3], labels[2], labels[1]],
                         default=labels[0])
    frame = frame.copy()
    frame["county_band"] = ""
    for county, edges in county_edges.items():
        mask = frame["county"] == county
        frame.loc[mask, "county_band"] = assign(frame.loc[mask, "exam"], edges)
    frame["pooled_band"] = assign(frame["exam"], pooled)
    return frame, pd.DataFrame(boundaries)


def _eligible(frame, settings, *, exclude_ambiguous=False,
              exclude_vocational=False):
    result = frame.copy()
    result["exclusion"] = "included"
    result.loc[result["success"].isna(), "exclusion"] = "outcome_unknown_or_outside"
    result.loc[result["status"] == "placed_other_county", "exclusion"] = "outside_origin_county"
    result.loc[result["status"] == "unresolved_outcome", "exclusion"] = "unresolved_outcome"
    result.loc[result["peer_count"] == 0, "exclusion"] = "no_observed_peer"
    if exclude_ambiguous:
        result.loc[result["ambiguous_exact_program"] & result["exclusion"].eq("included"),
                   "exclusion"] = "ambiguous_program_comparison"
    if exclude_vocational:
        result.loc[result["vocational_destination"] & result["exclusion"].eq("included"),
                   "exclusion"] = "vocational_destination_comparison"
    return result


def _binned(frame, band_column, n_bins):
    """Build display cells with both people and independent gymnasium counts."""
    records = []
    for (county, tier), group in frame.groupby(["county", "tier"], sort=False):
        eligible = group.loc[group["exclusion"] == "included"].copy()
        if eligible.empty:
            continue
        eligible["peer_bin"] = pd.qcut(eligible["peer_mean_exam"], q=n_bins,
                                       labels=False, duplicates="drop")
        for (band, peer_bin), cell in eligible.groupby([band_column, "peer_bin"], sort=False):
            if pd.isna(peer_bin):
                continue
            records.append({"county": county, "tier": tier, "band": band,
                            "peer_bin": int(peer_bin) + 1,
                            "peer_mean_exam": cell["peer_mean_exam"].mean(),
                            "applicants": len(cell), "gymnasiums": cell["gymnasium"].nunique(),
                            "successes": int(cell["success"].sum()),
                            "success_rate": cell["success"].mean()})
    return pd.DataFrame(records)


def _pooled_binned(frame, band_column, n_bins):
    """One applicant-weighted panel across counties, with a common peer-score axis."""
    records = []
    for tier, group in frame.groupby("tier", sort=False):
        eligible = group.loc[group["exclusion"] == "included"].copy()
        if eligible.empty:
            continue
        # Unlike the individual county panels, these bin edges use all selected counties
        # together. The county count on each point reveals incomplete coverage.
        eligible["peer_bin"] = pd.qcut(eligible["peer_mean_exam"], q=n_bins,
                                       labels=False, duplicates="drop")
        for (band, peer_bin), cell in eligible.groupby([band_column, "peer_bin"], sort=False):
            if pd.isna(peer_bin):
                continue
            records.append({"county": "ALL", "tier": tier, "band": band,
                            "peer_bin": int(peer_bin) + 1,
                            "peer_mean_exam": cell["peer_mean_exam"].mean(),
                            "applicants": len(cell),
                            "gymnasiums": len(cell[["county", "gymnasium"]].drop_duplicates()),
                            "counties": cell["county"].nunique(),
                            "successes": int(cell["success"].sum()),
                            "success_rate": cell["success"].mean()})
    return pd.DataFrame(records)


def _hero_bins(frame, n_bins):
    records = []
    county_groups = list(frame.groupby(["county", "tier"], sort=False))
    pooled_groups = [(("ALL", tier), group)
                     for tier, group in frame.groupby("tier", sort=False)]
    for (county, tier), group in county_groups + pooled_groups:
        eligible = group.loc[group["exclusion"] == "included"].copy()
        if eligible.empty:
            continue
        for kind in ("equal_width", "quantile"):
            if kind == "equal_width":
                eligible["bin"] = pd.cut(eligible["peer_mean_exam"], bins=n_bins,
                                         labels=False, include_lowest=True)
            else:
                eligible["bin"] = pd.qcut(eligible["peer_mean_exam"], q=n_bins,
                                          labels=False, duplicates="drop")
            for number, cell in eligible.groupby("bin"):
                if pd.isna(number):
                    continue
                records.append({"county": county, "tier": tier, "bin_type": kind,
                                "bin": int(number) + 1,
                                "peer_mean_exam": cell["peer_mean_exam"].mean(),
                                "applicants": len(cell),
                                "gymnasiums": (len(cell[["county", "gymnasium"]].drop_duplicates())
                                               if county == "ALL" else cell["gymnasium"].nunique()),
                                "counties": cell["county"].nunique(),
                                "successes": int(cell["success"].sum()),
                                "success_rate": cell["success"].mean()})
    return pd.DataFrame(records)


def _plot_hero(bins, tier, path, settings, counties=None):
    counties = (*settings.counties, "ALL") if counties is None else counties
    fig, axes = plt.subplots(len(counties), 2, figsize=(20, 5 * len(counties)),
                             sharey=True, squeeze=False)
    for row_number, county in enumerate(counties):
        for column_number, (kind, color) in enumerate((
                ("equal_width", "#a43d4c"), ("quantile", "#356c9b"))):
            axis = axes[row_number, column_number]
            data = bins.loc[(bins["county"] == county) & (bins["tier"] == tier)
                            & (bins["bin_type"] == kind)].sort_values("peer_mean_exam")
            positions = np.arange(len(data))
            heights = 100 * data["success_rate"].to_numpy()
            axis.bar(positions, heights, color=color, alpha=.9)
            axis.set_xticks(positions, [f"{value:.2f}" for value in data["peer_mean_exam"]],
                            rotation=60, fontsize=7)
            for position, (_, item) in enumerate(data.iterrows()):
                support = f"{item.gymnasiums} gyms"
                if county == "ALL":
                    support += f", {item.counties} counties"
                axis.annotate(f"{item.successes}/{item.applicants}\n{support}",
                              (position, heights[position]), fontsize=6,
                              xytext=(0, 3), textcoords="offset points", ha="center")
            location = (f"All {len(settings.counties)} counties pooled (applicant-weighted)"
                        if county == "ALL" else f"{COUNTY_NAMES[county]} ({county})")
            axis.set_title(f"{location} · {'equal-width' if kind == 'equal_width' else 'quantile'} bins")
            axis.grid(axis="y", alpha=.2)
            axis.set_axisbelow(True)
            axis.set_xlabel("Mean peer exam score in bin")
            if column_number == 0:
                axis.set_ylabel("Placed in designated program (%)")
    program_rule = "full programs" if settings.require_full_programs else "nonempty programs"
    group_rule = "three combined groups" if settings.combine_program_categories else "six subjects"
    scope = (f"all {len(settings.counties)} counties combined" if counties == ("ALL",)
             else f"{len(settings.counties)} counties and applicant-weighted combination")
    fig.suptitle(f"Romania 2001: selective placement vs gymnasium applicant peer score\n"
                 f"Top {tier} cutoff tier(s); {program_rule}; {group_rule}; {scope} — descriptive")
    fig.text(.5, .01, "Labels: successful placements / applicants; distinct gymnasiums. "
             "Pooled bars also show counties represented; county mix may change across bars.",
             ha="center", fontsize=9)
    fig.tight_layout(rect=[0.02, .03, 1, .96])
    fig.savefig(path, dpi=170)
    plt.close(fig)


def _plot_bands(bins, tier, path, band_name, settings):
    # One panel per county, a combined panel, and a reading guide. Growing the
    # county list must not silently drop the combined panel from a fixed grid.
    locations = (*settings.counties, "ALL")
    n_rows = (len(locations) + 2) // 2
    fig, axes = plt.subplots(n_rows, 2, figsize=(17, 5 * n_rows), sharex=True, sharey=True,
                             squeeze=False)
    labels = _band_labels(settings)
    for axis, county in zip(axes.flat, locations):
        county_data = bins.loc[(bins["county"] == county) & (bins["tier"] == tier)]
        for band, color in zip(labels, BAND_COLORS):
            data = county_data.loc[county_data["band"] == band].sort_values("peer_mean_exam")
            if data.empty:
                continue
            axis.plot(data["peer_mean_exam"], 100 * data["success_rate"],
                      marker="o", color=color, label=band)
            if band in labels[2:]:
                for _, row in data.iterrows():
                    support = f"{row.gymnasiums} gyms"
                    if county == "ALL":
                        support += f", {row.counties} counties"
                    axis.annotate(f"{row.successes}/{row.applicants}\n{support}",
                                  (row.peer_mean_exam, 100 * row.success_rate), fontsize=6,
                                  xytext=(0, 7), textcoords="offset points", ha="center",
                                  color=color)
        axis.set_title(f"All {len(settings.counties)} counties pooled (applicant-weighted)"
                       if county == "ALL" else f"{COUNTY_NAMES[county]} ({county})")
        axis.grid(alpha=.2)
        axis.legend(fontsize=8)
    for axis in list(axes.flat)[len(locations):]:
        axis.axis("off")
    guide = axes.flat[len(locations)]
    guide.text(.05, .82, "How to read the combined panel",
                       fontsize=13, fontweight="bold", transform=guide.transAxes)
    guide.text(
        .05, .62,
        f"Applicants from all {len(settings.counties)} counties are combined within\n"
        "common peer-score bins. Larger counties contribute more.\n"
        "County success rates and county mix differ, so this pooled\n"
        "line is descriptive, not a county-adjusted peer effect.",
        fontsize=10, va="top", transform=guide.transAxes,
    )
    program_rule = "full programs" if settings.require_full_programs else "nonempty programs"
    group_rule = "three combined groups" if settings.combine_program_categories else "six subjects"
    fig.suptitle(f"Romania 2001: placement at fixed own-exam bands across peer strength\n"
                 f"Top {tier} tier(s); {program_rule}; {group_rule}; {band_name} — descriptive")
    fig.supxlabel("Mean national exam score of other observed gymnasium applicants")
    fig.supylabel("Placed in a designated program (%)")
    fig.text(.5, .01, "Labels on stronger focal bands: successes / applicants; distinct gymnasiums. "
             "The pooled panel also shows counties represented.", ha="center", fontsize=9)
    fig.tight_layout(rect=[0.03, .04, 1, .94])
    fig.savefig(path, dpi=170)
    plt.close(fig)


def _summary(frame, chosen, settings):
    records = []
    for (county, tier), group in frame.groupby(["county", "tier"], sort=False):
        base = _eligible(group, settings,
                         exclude_vocational=not settings.include_vocational_in_primary)
        included = base.loc[base["exclusion"] == "included"]
        ambiguous_comparison = _eligible(group, settings, exclude_ambiguous=True,
            exclude_vocational=not settings.include_vocational_in_primary)
        ambiguity_included = ambiguous_comparison.loc[ambiguous_comparison["exclusion"] == "included"]
        vocational_comparison = _eligible(group, settings, exclude_vocational=True)
        vocational_included = vocational_comparison.loc[vocational_comparison["exclusion"] == "included"]
        selected = chosen.loc[(chosen["county"] == county) & (chosen["tier"] == tier)]
        counts = base["exclusion"].value_counts().to_dict()
        successes = int(included["success"].sum())
        n = len(included)
        one_case_low = successes / (n + 1) if county == "GL" else np.nan
        one_case_high = (successes + 1) / (n + 1) if county == "GL" else np.nan
        records.append({"county": county, "tier": tier,
                        "source_applicants": len(group), "primary_denominator": n,
                        "primary_successes": successes,
                        "primary_observed_success_fraction": successes / n if n else np.nan,
                        "qualifying_programs": len(selected),
                        "qualifying_program_places": int(selected["places"].sum()),
                        "ambiguous_exact_program_known_nonsuccess": int(
                            (group["status"] == "local_ambiguous_program").sum()),
                        "confirmed_unassigned": int((group["status"] == "confirmed_unassigned").sum()),
                        "outside_origin_county": int((group["status"] == "placed_other_county").sum()),
                        "unresolved_outcome": int((group["status"] == "unresolved_outcome").sum()),
                        "no_observed_peer": int((group["peer_count"] == 0).sum()),
                        "other_unknown": counts.get("outcome_unknown_or_outside", 0),
                        "ambiguous_excluded_denominator": (len(ambiguity_included)
                            if settings.compare_excluding_ambiguous else np.nan),
                        "ambiguous_excluded_success_fraction": (
                            ambiguity_included["success"].mean()
                            if settings.compare_excluding_ambiguous and len(ambiguity_included)
                            else np.nan),
                        "vocational_excluded_denominator": (len(vocational_included)
                            if settings.compare_excluding_vocational else np.nan),
                        "vocational_excluded_success_fraction": (
                            vocational_included["success"].mean()
                            if settings.compare_excluding_vocational and len(vocational_included)
                            else np.nan),
                        "unresolved_one_case_fraction_low": one_case_low,
                        "unresolved_one_case_fraction_high": one_case_high})
    return pd.DataFrame(records)


def _write_report(folder, summary, boundaries, settings, overview):
    top, excellence, middle = settings.ai_percentile_cuts
    lines = [f"# Romania 2001: {len(settings.counties)}-county descriptive placement pilot", "",
             f"This researcher-run analysis uses saved 2001 Romanian Ministry admission webpages for {', '.join(COUNTY_NAMES[c] for c in settings.counties)}. It asks whether actual placement in a designated selective program varies with the examination performance of *other observed admission-round applicants from the same originating gymnasium*. It is descriptive. It does not establish that peers caused placement differences or that all eighth graders are represented.", "",
             "## What counts", "",
             f"This run designates the top {', '.join(map(str, settings.top_tiers))} cumulative cutoff tier(s), separately, in each of the {'three combined groups' if settings.combine_program_categories else 'six original program categories'}, among {'fully occupied' if settings.require_full_programs else 'nonempty'} programs. Under the agreed primary specification, top one is primary and top two is a planned comparison. Actual placement is required. Vacancies, ties, number of winning programs, and the sum of their places are reported separately from the observed success fraction. No applicant preference list is available; the observed fraction is **not institutional K/N**.", "",
             "Primary outcome participants have a confirmed placement in their originating county or are confirmed unassigned, and have at least one observed gymnasium peer. Confirmed placements outside the originating county and the one unresolved outcome are excluded from the outcome denominator but retained as peers. Applicants with more than one possible exact local program are included only when every possible program has the same top-program success label under this run's settings. A comparison omitting those applicants is saved when requested. " + ("Vocationally placed applicants remain in the primary denominator." if settings.include_vocational_in_primary else "This run excludes vocationally placed applicants from the primary denominator; it is not the agreed primary specification."), "",
             "## County counts", "",
             "| County | Top tiers | Applicants | Outcome denominator | Selected | Observed % | Winning programs | Places in winning programs | Ambiguous exact program, binary known | Outside county | No observed peer |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
            ]
    for row in summary.itertuples():
        lines.append(f"| {row.county} | {row.tier} | {row.source_applicants:,} | "
                     f"{row.primary_denominator:,} | {row.primary_successes:,} | "
                     f"{100*row.primary_observed_success_fraction:.2f} | "
                     f"{row.qualifying_programs:,} | {row.qualifying_program_places:,} | "
                     f"{row.ambiguous_exact_program_known_nonsuccess:,} | "
                     f"{row.outside_origin_county:,} | {row.no_observed_peer:,} |")
    movement_lines = ["## County size and cross-county placements", "",
        "These counts use all recovered applicants and all saved county placements, before vocational, peer-count, or outcome exclusions. Participating gymnasiums have at least one observed applicant; the directory can also list schools with none. Outgoing means a student from this county's gymnasium was placed in another county. Incoming means a placement here belongs to an applicant from another county's gymnasium. These are school-location changes, not evidence that families moved.", "",
        "**Outgoing percentages divide by all applicants from the county's gymnasiums. Incoming percentages divide by all placements in the destination county.** They have different denominators and should not be subtracted. Incoming origins are identified from recovered gymnasium pages or the printed originating-school county in the County Applicant View, linked to the placement by name and admission score. For Bucharest, the complete incoming-admitted webpages and per-school results replace its incomplete county-wide applicant and unassigned webpages. Unknown origins/outcomes are reported separately, not counted as stayers.", ""]
    for row in overview.itertuples():
        movement_lines.append(
            f"- **{row.county_name} ({row.county}):** {row.participating_gymnasiums:,} participating gymnasiums "
            f"({row.gymnasiums_with_two_or_more_applicants:,} with at least two applicants; "
            f"{row.directory_gymnasiums:,} listed in the directory), {row.origin_applicants:,} applicants. "
            f"Outgoing: {row.outgoing_students:,} ({row.outgoing_pct_of_origin_applicants:.2f}% of origin applicants). "
            f"Incoming: {row.incoming_students:,} ({row.incoming_pct_of_destination_placements:.2f}% of "
            f"{row.destination_placements:,} placements here). "
            f"Unresolved origin-applicant outcomes: {row.origin_outcome_unresolved:,}; "
            f"destination placements with unresolved origin/matching: {row.destination_origin_unresolved:,}.")
    movement_lines += ["", "The full counts, including unassigned applicants and local placements, are saved in `county_size_and_movement.csv`. Lower movement may make the county a more complete view of its selection market; it does not establish causal identification. The county list is not automatically changed in response to these counts or the curves.", ""]
    lines[4:4] = movement_lines
    if settings.compare_excluding_ambiguous or settings.compare_excluding_vocational:
        lines += ["", "## What changes when we alter the denominator", "",
                  "Each line below uses the **same designated programs** as the primary row. Removing a group changes the people described by the rate; it does not recover anyone's unobserved program preferences.", ""]
        for row in summary.itertuples():
            comparison = [f"**{row.county}, top {row.tier}:** primary "
                          f"{row.primary_successes:,}/{row.primary_denominator:,} "
                          f"({100*row.primary_observed_success_fraction:.2f}%)."]
            if settings.compare_excluding_ambiguous and pd.notna(row.ambiguous_excluded_denominator):
                comparison.append("Exclude uncertain exact-program identities: "
                    f"{row.ambiguous_excluded_denominator:,.0f} applicants, "
                    f"{100*row.ambiguous_excluded_success_fraction:.2f}% selected.")
            if settings.compare_excluding_vocational and pd.notna(row.vocational_excluded_denominator):
                comparison.append("Exclude vocational destinations: "
                    f"{row.vocational_excluded_denominator:,.0f} applicants, "
                    f"{100*row.vocational_excluded_success_fraction:.2f}% selected.")
            lines.append("- " + " ".join(comparison))
        lines.append("")
    gala = summary.loc[summary["county"] == "GL"]
    if not gala.empty:
        lines += ["The single unresolved Galați applicant remains outside the primary denominator. "
                  "If that student later proves eligible for this outcome, the report's one-case "
                  "low/high bounds treat the student as a nonsuccess or success, respectively; "
                  "neither status is asserted now.", ""]
    lines += ["", "## Score bands and plots", "",
              f"The {excellence}th–{top}th percentile band of excellence and top {100-top} percent are defined within each originating county from **all recovered admission-round applicants**, before outcome exclusions. The lower boundary is the {middle}th percentile. A separately saved plot applies pooled {len(settings.counties)}-county boundaries. Ties at a boundary enter the higher band, so actual band sizes may differ slightly from the named percentages. The horizontal axis is the mean national exam score of other observed gymnasium applicants on its original score scale. Figures and bin CSV files show applicant counts and distinct gymnasium counts; one large gymnasium is not many independent environments.", "",
              f"County exam-score boundaries ({middle}th, {excellence}th, and {top}th percentiles):", ""]
    for row in boundaries.itertuples():
        lines.append(f"- **{row.county}:** {row.middle_exam_boundary:.2f}, {row.excellence_start_exam_boundary:.2f}, {row.top_start_exam_boundary:.2f} "
                     f"from {row.n_applicants:,} recovered applicants.")
    lines += ["", "## Limits and sensitivity", "",
              f"Each conditional score-band figure has {len(settings.counties)} county panels and one additional combined panel. Each HERO figure likewise has one row per county plus a combined row, with equal-width and equal-number bars. Pooled panels use common peer-score bins and weight each applicant equally, so large counties contribute more. Pooled labels report the number of counties represented. A pooled slope can change because the county mix changes across bins; it is not a county-adjusted peer effect.", "",
              "The ambiguous-program exclusion comparison changes the denominator, not the observed top-program numerator under the frozen six-category/full-program rule. The vocational exclusion comparison changes the described population and cannot reveal who actually applied to selective academic programs. One Galați applicant has no saved outcome; the summary CSV supplies a simple one-case low/high bound. Neither endpoint is asserted as the student's actual result. Source-status counts in the summary can overlap with 'no observed peer'; they are not meant to be added as mutually exclusive exclusions.", "",
              "All source matches rely on printed name plus admission score because the archived personal identifier is masked. Examination scores were measured after time in the gymnasium. Geography, preferences, prior preparation, and other unobserved differences may explain descriptive patterns. Do not interpret a downturn or an upward slope as a causal congestion effect.", "",
              "Every CSV here is free of applicant names and individual applicant rows. The program table includes public program names; the other CSVs contain aggregate counts or score boundaries. The private source pages remain in the Desktop cache. See the four-county design decision log and source-gate report for the exact prior choices and unresolved source item.", ""]
    (folder / "report.md").write_text("\n".join(lines), encoding="utf-8")


def run_pilot(settings: Settings = Settings(), *, run: bool = False):
    """Called explicitly from Cursor notebook; ``run=False`` prevents accidents."""
    settings.validate()
    if not run:
        print("Analysis is off. Set RUN_ANALYSIS = True in the notebook run cell.", flush=True)
        return None
    frame, chosen, overview = _load_rows(settings)
    frame, boundaries = _add_bands(frame, settings)
    if (not settings.combine_program_categories and settings.require_full_programs
            and set(settings.top_tiers).issubset({1, 2})):
        # The old 558 total applied only to the original four counties. Compare
        # each county with its own saved audit, including the new program links.
        old_gate = pd.read_csv(SOURCE_GATE).set_index("county")
        expansion = (pd.read_csv(EXPANSION_GATE).set_index(["county", "top_cutoff_tiers"])
                     if set(settings.counties) - set(ORIGINAL_COUNTIES) else None)
        for (county, tier), group in frame.groupby(["county", "tier"]):
            expected = (0 if county == "B" else
                        int(old_gate.loc[county, "local_program_ambiguous"])
                        if county in ORIGINAL_COUNTIES else
                        int(expansion.loc[(county, tier), "multiple_possible_programs"]))
            known = group.loc[group["status"] == "local_ambiguous_program"]
            if (len(known) != expected or (known["success"] != 0).any()
                    or group["status"].isin(["mixed_program_success", "unmatched_program"]).any()):
                raise ValueError(f"{county} top {tier}: current program labels disagree with the saved audit")
    print("Step 3/4 — calculating source-backed denominators and display bins...", flush=True)
    primary = _eligible(frame, settings,
                        exclude_vocational=not settings.include_vocational_in_primary)
    summary = _summary(frame, chosen, settings)
    hero = _hero_bins(primary, settings.hero_bins)
    bands = pd.concat([
        _binned(primary, "county_band", settings.peer_strength_bins),
        _pooled_binned(primary, "county_band", settings.peer_strength_bins),
    ], ignore_index=True)
    pooled_bands = (pd.concat([
        _binned(primary, "pooled_band", settings.peer_strength_bins),
        _pooled_binned(primary, "pooled_band", settings.peer_strength_bins),
    ], ignore_index=True) if settings.compare_pooled_score_bands else pd.DataFrame())
    if hero.empty or bands.empty:
        raise ValueError("No supported bins for the selected counties")
    stamp = datetime.now().astimezone().strftime("run_%Y%m%dT%H%M%S%z")
    output_root = (OUTPUTS if settings.counties == ORIGINAL_COUNTIES else
                   ROOT / f"outputs/romania_2001_{len(settings.counties)}_county_descriptive_pilot")
    folder = output_root / stamp
    folder.mkdir(parents=True, exist_ok=False)
    print("Step 4/4 — saving name-free tables, report, and plots...", flush=True)
    summary.to_csv(folder / "summary.csv", index=False)
    overview.to_csv(folder / "county_size_and_movement.csv", index=False)
    boundaries.to_csv(folder / "score_band_boundaries.csv", index=False)
    chosen.to_csv(folder / "qualifying_programs.csv", index=False)
    hero.to_csv(folder / "hero_bins.csv", index=False)
    bands.to_csv(folder / "conditional_bins_county_bands.csv", index=False)
    if not pooled_bands.empty:
        pooled_bands.to_csv(folder / "conditional_bins_pooled_bands.csv", index=False)
    for tier in settings.top_tiers:
        _plot_hero(hero, tier, folder / f"hero_top{tier}.png", settings)
        _plot_hero(hero, tier, folder / f"hero_combined_top{tier}.png",
                   settings, counties=("ALL",))
        _plot_bands(bands, tier, folder / f"conditional_county_bands_top{tier}.png",
                    "within-county own-exam bands", settings)
        if not pooled_bands.empty:
            _plot_bands(pooled_bands, tier, folder / f"conditional_pooled_bands_top{tier}.png",
                        f"pooled {len(settings.counties)}-county own-exam bands", settings)
        print(f"  Saved top-{tier} HERO and conditional figures", flush=True)
    manifest = {"run_at_local": stamp, "settings": asdict(settings),
                "decision_log_sha256": hashlib.sha256(DECISIONS.read_bytes()).hexdigest(),
                "source_gate_sha256": hashlib.sha256(SOURCE_GATE.read_bytes()).hexdigest(),
                "privacy": "aggregate outputs only; individual records retained in private cache",
                "scope": f"{len(settings.counties)} origin counties; 2001 main admissions round; descriptive"}
    if set(settings.counties) - set(ORIGINAL_COUNTIES):
        manifest["expansion_source_gate_sha256"] = hashlib.sha256(EXPANSION_GATE.read_bytes()).hexdigest()
    if "B" in settings.counties:
        manifest["bucharest_source_gate_sha256"] = hashlib.sha256(BUCHAREST_GATE.read_bytes()).hexdigest()
    (folder / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    _write_report(folder, summary, boundaries, settings, overview)
    print("Completed. Read:", folder / "report.md", flush=True)
    return folder, summary


if __name__ == "__main__":
    raise SystemExit("Run from the researcher-controlled notebook; importing this file does nothing.")
