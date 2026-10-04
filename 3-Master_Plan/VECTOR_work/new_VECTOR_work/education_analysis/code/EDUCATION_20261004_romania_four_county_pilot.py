"""Researcher-run four-county Romania 2001 descriptive placement pilot.

This module makes no network requests and performs no analysis on import.
``run_pilot`` reads verified private source checkpoints, then writes only
name-free aggregate tables, figures, and a plain-English report. The plots
are descriptive associations, not causal estimates or institutional K/N.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from EDUCATION_20260930_romania_2001_national_acquisition import CACHE
from EDUCATION_20260930_romania_placements_and_hero import COMBINED_CATEGORIES
from EDUCATION_20261001_romania_offline_county_source_readiness import placement_status
from EDUCATION_20261002_romania_full_gymnasium_offline_reconciliation import (
    COUNTIES, all_gymnasium_rows, name_score, saved_national_indexes,
)
from EDUCATION_20261003_romania_four_county_program_identity_gate import (
    clean, local_placement_rows, source_programs,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs/romania_2001_four_county_descriptive_pilot"
DECISIONS = ROOT / "docs/decisions/EDUCATION_20261002_Romania_four_county_pilot_design_decisions.md"
SOURCE_GATE = ROOT / "outputs/romania_2001_four_county_source_pilot/program_identity_source_gate.csv"
BAND_LABELS = ("Lower 50%", "50th–75th", "75th–90th", "Top 10%")
BAND_COLORS = ("#73afd2", "#999999", "#e58b25", "#a43d4c")


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
    peer_strength_bins: int = 8
    hero_bins: int = 16

    def validate(self):
        if not self.top_tiers or any(t < 1 or type(t) is not int for t in self.top_tiers):
            raise ValueError("top_tiers must contain positive integers")
        if len(set(self.top_tiers)) != len(self.top_tiers):
            raise ValueError("top_tiers contains a repeated tier")
        if self.peer_strength_bins < 3 or self.hero_bins < 3:
            raise ValueError("Plot bin counts must be at least three")


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


def _load_rows(settings):
    """Recheck saved sources, then hold personal fields only in local memory."""
    print("Step 1/4 — verifying gymnasium and county source checkpoints...", flush=True)
    gymnasiums, _ = all_gymnasium_rows()
    _, national_placements, national_unassigned, _ = saved_national_indexes()
    progress = placement_status()
    all_keys = Counter(key for group in gymnasiums.values() for _code, key, _comp in group)
    if None in all_keys or max(all_keys.values()) != 1:
        raise ValueError("Gymnasium printed name-score signatures are incomplete or repeated")
    frames = []
    selected_programs = []
    for county in COUNTIES:
        manifest, source_program_rows, catalog = _program_catalog(county)
        reports = local_placement_rows(manifest, county, progress, source_program_rows)
        if len(reports) != sum(p["admitted"] for p in catalog.values()):
            raise ValueError(f"{county}: placement count disagrees with program occupancy")
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
    frame = pd.DataFrame(frames)
    chosen = pd.DataFrame(selected_programs)
    if frame.empty or chosen.empty:
        raise ValueError("No source-backed analysis rows or qualifying programs")
    return frame, chosen


def _add_bands(frame, settings):
    """Freeze score bands from every participating applicant, not outcome rows."""
    print("Step 2/4 — defining county and pooled examination-score bands...", flush=True)
    first = frame.loc[frame["tier"] == settings.top_tiers[0], ["county", "exam"]]
    pooled = first["exam"].quantile([0.50, 0.75, 0.90]).to_dict()
    boundaries = []
    county_edges = {}
    for county in COUNTIES:
        scores = first.loc[first["county"] == county, "exam"]
        edges = scores.quantile([0.50, 0.75, 0.90]).to_dict()
        county_edges[county] = edges
        boundaries.append({"county": county, "n_applicants": len(scores),
                           "score_p50": edges[0.50], "score_p75": edges[0.75],
                           "score_p90": edges[0.90],
                           "pooled_score_p50": pooled[0.50],
                           "pooled_score_p75": pooled[0.75],
                           "pooled_score_p90": pooled[0.90]})
    def assign(scores, edges):
        return np.select([scores >= edges[0.90], scores >= edges[0.75],
                          scores >= edges[0.50]],
                         [BAND_LABELS[3], BAND_LABELS[2], BAND_LABELS[1]],
                         default=BAND_LABELS[0])
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


def _hero_bins(frame, n_bins):
    records = []
    for (county, tier), group in frame.groupby(["county", "tier"], sort=False):
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
                                "gymnasiums": cell["gymnasium"].nunique(),
                                "successes": int(cell["success"].sum()),
                                "success_rate": cell["success"].mean()})
    return pd.DataFrame(records)


def _plot_hero(bins, tier, path, settings):
    fig, axes = plt.subplots(4, 2, figsize=(20, 21), sharey=True)
    for row_number, county in enumerate(COUNTIES):
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
                axis.annotate(f"{item.successes}/{item.applicants}\n{item.gymnasiums} gyms",
                              (position, heights[position]), fontsize=6,
                              xytext=(0, 3), textcoords="offset points", ha="center")
            axis.set_title(f"{county} · {'equal-width' if kind == 'equal_width' else 'quantile'} bins")
            axis.grid(axis="y", alpha=.2)
            axis.set_axisbelow(True)
            axis.set_xlabel("Mean peer exam score in bin")
            if column_number == 0:
                axis.set_ylabel("Placed in designated program (%)")
    program_rule = "full programs" if settings.require_full_programs else "nonempty programs"
    group_rule = "three combined groups" if settings.combine_program_categories else "six subjects"
    fig.suptitle(f"Romania 2001: selective placement vs gymnasium applicant peer score\n"
                 f"Top {tier} cutoff tier(s); {program_rule}; {group_rule} — descriptive")
    fig.text(.5, .01, "Labels: successful placements / applicants; number of distinct gymnasiums. "
             "Same gymnasium may contribute to more than one bin.", ha="center", fontsize=9)
    fig.tight_layout(rect=[0.02, .03, 1, .96])
    fig.savefig(path, dpi=170)
    plt.close(fig)


def _plot_bands(bins, tier, path, band_name, settings):
    fig, axes = plt.subplots(2, 2, figsize=(17, 11), sharex=True, sharey=True)
    for axis, county in zip(axes.flat, COUNTIES):
        county_data = bins.loc[(bins["county"] == county) & (bins["tier"] == tier)]
        for band, color in zip(BAND_LABELS, BAND_COLORS):
            data = county_data.loc[county_data["band"] == band].sort_values("peer_mean_exam")
            if data.empty:
                continue
            axis.plot(data["peer_mean_exam"], 100 * data["success_rate"],
                      marker="o", color=color, label=band)
            if band in BAND_LABELS[2:]:
                for _, row in data.iterrows():
                    axis.annotate(f"{row.successes}/{row.applicants}\n{row.gymnasiums} gyms",
                                  (row.peer_mean_exam, 100 * row.success_rate), fontsize=6,
                                  xytext=(0, 7), textcoords="offset points", ha="center",
                                  color=color)
        axis.set_title(county)
        axis.grid(alpha=.2)
        axis.legend(fontsize=8)
    program_rule = "full programs" if settings.require_full_programs else "nonempty programs"
    group_rule = "three combined groups" if settings.combine_program_categories else "six subjects"
    fig.suptitle(f"Romania 2001: placement at fixed own-exam bands across peer strength\n"
                 f"Top {tier} tier(s); {program_rule}; {group_rule}; {band_name} — descriptive")
    fig.supxlabel("Mean national exam score of other observed gymnasium applicants")
    fig.supylabel("Placed in a designated program (%)")
    fig.text(.5, .01, "Labels on stronger focal bands: successes / applicants; distinct gymnasiums. "
             "Cells with one gymnasium are descriptive, not replication.", ha="center", fontsize=9)
    fig.tight_layout(rect=[0.03, .045, 1, .93])
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


def _write_report(folder, summary, boundaries, settings):
    lines = ["# Romania 2001 four county descriptive placement pilot", "",
             "This researcher-run analysis uses saved 2001 Romanian Ministry admission webpages for Alba, Caraș-Severin, Galați, and Tulcea. It asks whether actual placement in a designated selective program varies with the examination performance of *other observed admission-round applicants from the same originating gymnasium*. It is descriptive. It does not establish that peers caused placement differences or that all eighth graders are represented.", "",
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
              "The 75th–90th percentile and top 10 percent are defined within each originating county from **all recovered admission-round applicants**, before outcome exclusions. A separately saved plot applies pooled four-county boundaries. Ties at a boundary enter the higher band, so actual band sizes may differ slightly from the named percentages. The horizontal axis is the mean national exam score of other observed gymnasium applicants on its original score scale. Figures and bin CSV files show applicant counts and distinct gymnasium counts; one large gymnasium is not many independent environments.", "",
              "County exam-score boundaries (50th, 75th, and 90th percentiles):", ""]
    for row in boundaries.itertuples():
        lines.append(f"- **{row.county}:** {row.score_p50:.2f}, {row.score_p75:.2f}, {row.score_p90:.2f} "
                     f"from {row.n_applicants:,} recovered applicants.")
    lines += ["", "## Limits and sensitivity", "",
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
    frame, chosen = _load_rows(settings)
    frame, boundaries = _add_bands(frame, settings)
    if (not settings.combine_program_categories and settings.require_full_programs
            and set(settings.top_tiers).issubset({1, 2})):
        known = frame.loc[frame["status"] == "local_ambiguous_program"]
        if (known["success"] != 0).any() or known.groupby("tier").size().min() != 558:
            raise ValueError("Frozen 558-case source-gate finding did not replicate")
    print("Step 3/4 — calculating source-backed denominators and display bins...", flush=True)
    primary = _eligible(frame, settings,
                        exclude_vocational=not settings.include_vocational_in_primary)
    summary = _summary(frame, chosen, settings)
    hero = _hero_bins(primary, settings.hero_bins)
    bands = _binned(primary, "county_band", settings.peer_strength_bins)
    pooled_bands = (_binned(primary, "pooled_band", settings.peer_strength_bins)
                    if settings.compare_pooled_score_bands else pd.DataFrame())
    if hero.empty or bands.empty:
        raise ValueError("No supported bins for four-county display")
    stamp = datetime.now().astimezone().strftime("run_%Y%m%dT%H%M%S%z")
    folder = OUTPUTS / stamp
    folder.mkdir(parents=True, exist_ok=False)
    print("Step 4/4 — saving name-free tables, report, and plots...", flush=True)
    summary.to_csv(folder / "summary.csv", index=False)
    boundaries.to_csv(folder / "score_band_boundaries.csv", index=False)
    chosen.to_csv(folder / "qualifying_programs.csv", index=False)
    hero.to_csv(folder / "hero_bins.csv", index=False)
    bands.to_csv(folder / "conditional_bins_county_bands.csv", index=False)
    if not pooled_bands.empty:
        pooled_bands.to_csv(folder / "conditional_bins_pooled_bands.csv", index=False)
    for tier in settings.top_tiers:
        _plot_hero(hero, tier, folder / f"hero_top{tier}.png", settings)
        _plot_bands(bands, tier, folder / f"conditional_county_bands_top{tier}.png",
                    "within-county own-exam bands", settings)
        if not pooled_bands.empty:
            _plot_bands(pooled_bands, tier, folder / f"conditional_pooled_bands_top{tier}.png",
                        "pooled four-county own-exam bands", settings)
        print(f"  Saved top-{tier} HERO and conditional figures", flush=True)
    manifest = {"run_at_local": stamp, "settings": asdict(settings),
                "decision_log_sha256": hashlib.sha256(DECISIONS.read_bytes()).hexdigest(),
                "source_gate_sha256": hashlib.sha256(SOURCE_GATE.read_bytes()).hexdigest(),
                "privacy": "aggregate outputs only; individual records retained in private cache",
                "scope": "four origin counties; 2001 main admissions round; descriptive"}
    (folder / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    _write_report(folder, summary, boundaries, settings)
    print("Completed. Read:", folder / "report.md", flush=True)
    return folder, summary


if __name__ == "__main__":
    raise SystemExit("Run from the researcher-controlled notebook; importing this file does nothing.")
