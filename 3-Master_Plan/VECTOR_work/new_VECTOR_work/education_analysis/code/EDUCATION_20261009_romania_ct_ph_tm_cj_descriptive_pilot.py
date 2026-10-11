"""Researcher-run descriptive plots for the eleven source-checked counties.

This module makes no web requests. Student-level source rows stay in memory;
only aggregate tables, figures, and a name-free report enter the repository.
The corresponding notebook exposes every research setting and controls the run.
"""

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, replace
from datetime import datetime
from pathlib import Path
import hashlib
import json

import numpy as np
import pandas as pd

import EDUCATION_20261004_romania_four_county_pilot as base
import EDUCATION_20261006_romania_school_results_incoming_acquisition as views
from EDUCATION_20261001_romania_four_county_school_sample import school_directory
from EDUCATION_20261002_romania_three_county_gymnasium_acquisition import saved_school
from EDUCATION_20261002_romania_full_gymnasium_offline_reconciliation import components, name_score
from EDUCATION_20261003_romania_four_county_program_identity_gate import local_placement_rows, clean
from EDUCATION_20261001_romania_offline_county_source_readiness import placement_status
from EDUCATION_20261007_romania_seven_county_new_views_offline_audit import (
    county_suffix, marked_unassigned, rows, school_code,
)

NEW_COUNTIES = ("CT", "PH", "TM", "CJ")
COUNTIES = (*base.COUNTY_NAMES, *NEW_COUNTIES)
COUNTY_NAMES = {**base.COUNTY_NAMES,
                "CT": "Constanța", "PH": "Prahova", "TM": "Timiș", "CJ": "Cluj"}
ROOT = Path(__file__).resolve().parents[1]
SOURCE_GATE = ROOT / "outputs/romania_2001_four_new_county_source_reconciliation_20261008/plot_source_gate_counts.csv"
OUTPUTS = ROOT / "outputs/romania_2001_CT_PH_TM_CJ_descriptive_pilot"
ALL_OUTPUTS = ROOT / "outputs/romania_2001_all_scraped_counties_descriptive_pilot"


@dataclass(frozen=True)
class Settings(base.Settings):
    """Same frozen definitions as the earlier county notebook, selectable scope."""

    counties: tuple[str, ...] = COUNTIES

    @property
    def county_names(self):
        return COUNTY_NAMES

    def validate(self):
        if not self.counties or len(set(self.counties)) != len(self.counties):
            raise ValueError("Choose one or more distinct county codes")
        if not set(self.counties).issubset(COUNTIES):
            raise ValueError(f"Supported county codes: {', '.join(COUNTIES)}")
        if (not self.top_tiers or len(set(self.top_tiers)) != len(self.top_tiers)
                or any(type(t) is not int or t < 1 for t in self.top_tiers)):
            raise ValueError("TOP_TIERS must contain distinct positive integers")
        if self.peer_strength_bins < 3 or self.hero_bins < 3:
            raise ValueError("Plot bin counts must be at least three")
        if (len(self.ai_percentile_cuts) != 3
                or any(type(x) is not int for x in self.ai_percentile_cuts)
                or not 0 < self.ai_percentile_cuts[2] < self.ai_percentile_cuts[1]
                < self.ai_percentile_cuts[0] < 100):
            raise ValueError("AI_PERCENTILE_CUTS must be three descending percentiles")


def _gate(settings):
    if not SOURCE_GATE.exists():
        raise ValueError("Run the four-county offline plot-source gate first")
    gate = pd.read_csv(SOURCE_GATE).set_index("county")
    for county in settings.counties:
        if county not in NEW_COUNTIES:
            continue
        if county not in gate.index:
            raise ValueError(f"{county}: absent from source gate")
        row = gate.loc[county]
        if (row["applicant_rows"] != row["matched_result_rows"]
                or row["ambiguous_or_missing_result_rows"] != 0
                or row["top1_label_unresolved"] != 0
                or row["top2_label_unresolved"] != 0
                or row["occupancy_difference"] != 0):
            raise ValueError(f"{county}: source gate has an unresolved item")
    return gate


def _new_source_frames(settings):
    """Match each new-county applicant within its gymnasium; fail closed."""
    settings.validate()
    gate = _gate(settings)
    state = views.load_status()["counties"]
    progress = placement_status()
    frames, chosen, overview = [], [], []
    for county in settings.counties:
        if county not in NEW_COUNTIES:
            continue
        print(f"Source check {county}: gymnasium, result, and program pages...", flush=True)
        schools = school_directory(county)
        result_state = state[county]["school_results"]
        saved, missing = rows(county, "school_results", result_state)
        if missing or result_state["unresolved"] or len(saved) != result_state["saved_pages"]:
            raise ValueError(f"{county}: school-result pages are incomplete")
        results_by_school = {}
        for relative, page in saved:
            if relative.lower().startswith("raport_scoli_din_judet_tot.asp"):
                continue
            code = school_code(relative)
            if code is None or code in results_by_school:
                raise ValueError(f"{county}: duplicate or unidentified result school")
            results_by_school[code] = page["rows"]
        if set(results_by_school) != set(schools):
            raise ValueError(f"{county}: result pages differ from the school directory")

        manifest, programs, catalog = base._program_catalog(county)
        placements = local_placement_rows(manifest, county, progress, programs)
        if len(placements) != sum(p["admitted"] for p in catalog.values()):
            raise ValueError(f"{county}: destination placements differ from program occupancy")
        exact_codes = {}
        for row in placements:
            code = row.get("__source_program_code")
            if code is not None:
                key = name_score(row)
                if key is None or key in exact_codes:
                    raise ValueError(f"{county}: duplicate exact-code source key")
                exact_codes[key] = code
        by_identity = defaultdict(list)
        for code, program, *_ in programs:
            by_identity[tuple(clean(program[field]) for field in
                              ("Liceu", "Profil", "Specializare"))].append(code)
        winners = {tier: base._winner_codes(catalog, tier, settings)
                   for tier in settings.top_tiers}
        for tier, codes in winners.items():
            for code in sorted(codes):
                p = catalog[code]
                chosen.append({"county": county, "tier": tier, "program_code": code,
                               "category": p["category"], "school": p["school"],
                               "cutoff": p["cutoff"], "places": p["places"],
                               "admitted": p["admitted"]})

        school_pages, gym_sizes, gym_sums = {}, Counter(), defaultdict(float)
        for code, (_name, relative) in schools.items():
            page = saved_school(county, code, relative)
            if page is None:
                raise ValueError(f"{county} gymnasium {code}: score report absent")
            school_pages[code] = page
            gym_sizes[code] = page["row_count"]
            for student in page["rows"]:
                score = components(student)
                if score is None:
                    raise ValueError(f"{county} gymnasium {code}: exam score absent")
                gym_sums[code] += float(score[0])
        if sum(gym_sizes.values()) != gate.loc[county, "applicant_rows"]:
            raise ValueError(f"{county}: applicant total differs from saved source gate")

        tally = Counter()
        for code, page in school_pages.items():
            result_keys = defaultdict(list)
            for row in results_by_school[code]:
                result_keys[name_score(row)].append(row)
            for student in page["rows"]:
                key = name_score(student)
                matches = result_keys.get(key, [])
                if key is None or len(matches) != 1:
                    raise ValueError(f"{county} gymnasium {code}: result match is not unique")
                result = matches[0]
                exam = float(components(student)[0])
                n_peers = gym_sizes[code] - 1
                peer_mean = (gym_sums[code] - exam) / n_peers if n_peers else np.nan
                if marked_unassigned(result):
                    status, options = "confirmed_unassigned", []
                    tally["unassigned"] += 1
                elif (county_suffix(result.get("Liceu")) or county) != county:
                    status, options = "placed_other_county", []
                    tally["away"] += 1
                else:
                    options = base._destination_options(result, county, catalog, by_identity)
                    exact = exact_codes.get(key)
                    if exact is not None:
                        if exact not in options:
                            raise ValueError(f"{county}: exact code contradicts school-result label")
                        options = [exact]
                    if not options:
                        raise ValueError(f"{county}: home placement has no program")
                    status = ("local_unique_program" if len(options) == 1
                              else "local_ambiguous_program")
                    tally["home"] += 1
                vocational = bool(options) and all(
                    catalog[c]["level"] == "Profesional"
                    or catalog[c]["category"] == "Profesional" for c in options)
                for tier, winning_codes in winners.items():
                    possible = {c in winning_codes for c in options}
                    if len(possible) > 1:
                        raise ValueError(f"{county}: top-{tier} program label still mixed")
                    success = (np.nan if status == "placed_other_county" else
                               0 if status == "confirmed_unassigned" else int(possible.pop()))
                    frames.append({"county": county, "gymnasium": code, "tier": tier,
                                   "exam": exam, "peer_mean_exam": peer_mean,
                                   "peer_count": n_peers, "status": status,
                                   "success": success, "vocational_destination": vocational,
                                   "ambiguous_exact_program": len(options) > 1})
        expected = gate.loc[county]
        if (tally["home"] != expected["home_placements"]
                or tally["away"] != expected["away_placements"]
                or tally["unassigned"] != expected["unassigned"]):
            raise ValueError(f"{county}: outcome counts differ from saved source gate")
        applicant_n = sum(gym_sizes.values())
        incoming = len(placements) - tally["home"]
        overview.append({"county": county, "county_name": COUNTY_NAMES[county],
                         "directory_gymnasiums": len(schools),
                         "participating_gymnasiums": sum(n > 0 for n in gym_sizes.values()),
                         "gymnasiums_with_two_or_more_applicants": sum(n > 1 for n in gym_sizes.values()),
                         "origin_applicants": applicant_n,
                         "destination_placements": len(placements),
                         "origin_placed_locally": tally["home"],
                         "outgoing_students": tally["away"],
                         "origin_unassigned": tally["unassigned"],
                         "origin_outcome_unresolved": 0,
                         "incoming_students": incoming,
                         "destination_from_own_county": tally["home"],
                         "destination_origin_unresolved": 0,
                         "outgoing_pct_of_origin_applicants": 100 * tally["away"] / applicant_n,
                         "incoming_pct_of_destination_placements": 100 * incoming / len(placements)})
        print(f"  {county}: {applicant_n:,} applicants; {tally['home']:,} home placements; "
              f"{tally['away']:,} away; {tally['unassigned']:,} unassigned", flush=True)
    return pd.DataFrame(frames), pd.DataFrame(chosen), pd.DataFrame(overview)


def _source_frames(settings):
    """Join the two source-verified county pipelines without duplicating people."""
    settings.validate()
    earlier = tuple(c for c in settings.counties if c in base.COUNTY_NAMES)
    newer = tuple(c for c in settings.counties if c in NEW_COUNTIES)
    pieces = []
    if earlier:
        print(f"Checking the earlier {len(earlier)} counties: {', '.join(earlier)}", flush=True)
        pieces.append(base._load_rows(replace(settings, counties=earlier)))
    if newer:
        print(f"Checking the newer {len(newer)} counties: {', '.join(newer)}", flush=True)
        pieces.append(_new_source_frames(replace(settings, counties=newer)))
    frame = pd.concat([p[0] for p in pieces], ignore_index=True)
    chosen = pd.concat([p[1] for p in pieces], ignore_index=True)
    overview = pd.concat([p[2] for p in pieces], ignore_index=True)
    order = {county: i for i, county in enumerate(settings.counties)}
    for table in (frame, chosen, overview):
        table.sort_values("county", key=lambda s: s.map(order), inplace=True,
                          kind="stable", ignore_index=True)
    if overview["county"].tolist() != list(settings.counties):
        raise ValueError("A requested county is missing or repeated in the source overview")
    return frame, chosen, overview


def source_preview(settings):
    """Recheck requested sources and return name-free county counts only."""
    _frame, _chosen, overview = _source_frames(settings)
    return overview


def _equal_county_bins(frame, band_column, n_bins, *, hero=False):
    """Within each COMMON peer bin, average the represented county rates.

    Every county with eligible applicants in a cell contributes one rate, no
    matter how many applicants it contributes. A county with no applicants in
    that cell has no estimable rate and is absent, never treated as zero.
    """
    records = []
    for tier, group in frame.groupby("tier", sort=False):
        eligible = group.loc[group["exclusion"] == "included"].copy()
        if eligible.empty:
            continue
        kinds = ("equal_width", "quantile") if hero else ("quantile",)
        for kind in kinds:
            eligible["peer_bin"] = (
                pd.cut(eligible["peer_mean_exam"], bins=n_bins, labels=False,
                       include_lowest=True) if kind == "equal_width" else
                pd.qcut(eligible["peer_mean_exam"], q=n_bins, labels=False,
                        duplicates="drop"))
            groups = (["peer_bin"] if hero else [band_column, "peer_bin"])
            for key, cell in eligible.groupby(groups, sort=False):
                values = key if isinstance(key, tuple) else (key,)
                peer_bin = values[-1]
                if pd.isna(peer_bin):
                    continue
                by_county = cell.groupby("county", sort=False)
                county_rates = by_county["success"].mean()
                county_peer_means = by_county["peer_mean_exam"].mean()
                record = {"county": "ALL", "tier": tier,
                          "peer_mean_exam": county_peer_means.mean(),
                          "applicants": len(cell),
                          "gymnasiums": len(cell[["county", "gymnasium"]].drop_duplicates()),
                          "counties": len(county_rates),
                          "successes": int(cell["success"].sum()),
                          "success_rate": county_rates.mean(),
                          "pooling_method": "equal_county_within_cell"}
                if hero:
                    record.update(bin_type=kind, bin=int(peer_bin) + 1)
                else:
                    record.update(band=values[0], peer_bin=int(peer_bin) + 1)
                records.append(record)
    return pd.DataFrame(records)


def _pooled_gymnasium_mean_bins(frame, primary, settings, *, bin_method="quantile"):
    """One shared selected-county peer bin per gymnasium, not per student.

    Quantile or equal-width cutpoints use gymnasium means before looking at
    outcomes. Only groups with two or more applicants enter this peer plot.
    Every eligible applicant then inherits that gymnasium's bin; own-score
    bands are the pooled (all selected counties) applicant percentiles.
    """
    first_tier = settings.top_tiers[0]
    gyms = (frame.loc[frame["tier"] == first_tier]
            .groupby(["county", "gymnasium"], as_index=False)
            .agg(gym_mean_exam=("exam", "mean"),
                 observed_applicants=("exam", "size")))
    gyms = gyms.loc[gyms["observed_applicants"] >= 2].copy()
    if gyms.empty:
        raise ValueError("No gymnasiums have two observed applicants")
    if bin_method == "quantile":
        cut = pd.qcut(gyms["gym_mean_exam"], q=settings.peer_strength_bins,
                      duplicates="drop")
    elif bin_method == "equal_width":
        cut = pd.cut(gyms["gym_mean_exam"], bins=settings.peer_strength_bins,
                     include_lowest=True)
    else:
        raise ValueError("bin_method must be 'quantile' or 'equal_width'")
    if (cut.cat.codes < 0).any():
        raise ValueError("Gymnasium means cannot define shared peer bins")
    gyms["gym_bin"] = cut.cat.codes + 1
    intervals = pd.DataFrame({
        "gym_bin": range(1, len(cut.cat.categories) + 1),
        "bin_left": [interval.left for interval in cut.cat.categories],
        "bin_right": [interval.right for interval in cut.cat.categories],
    })
    observed = (gyms.groupby("gym_bin", as_index=False)
                .agg(gym_mean_min=("gym_mean_exam", "min"),
                     gym_mean_max=("gym_mean_exam", "max"),
                     gym_mean_center=("gym_mean_exam", "mean"),
                     gymnasiums=("gymnasium", "size"),
                     counties=("county", "nunique")))
    boundaries = intervals.merge(observed, on="gym_bin", how="left",
                                 validate="one_to_one")
    boundaries["gym_mean_center"] = boundaries["gym_mean_center"].fillna(
        (boundaries["bin_left"] + boundaries["bin_right"]) / 2)
    boundaries[["gymnasiums", "counties"]] = boundaries[["gymnasiums", "counties"]].fillna(0).astype(int)
    boundaries["bin_method"] = bin_method
    eligible = primary.loc[primary["exclusion"] == "included"].merge(
        gyms[["county", "gymnasium", "gym_bin"]],
        on=["county", "gymnasium"], how="left", validate="many_to_one")
    if eligible["gym_bin"].isna().any():
        raise ValueError("An eligible applicant has no gymnasium peer bin")
    records = []
    centers = boundaries.set_index("gym_bin")["gym_mean_center"]
    for (tier, band, gym_bin), cell in eligible.groupby(
            ["tier", "pooled_band", "gym_bin"], sort=False):
        records.append({"tier": tier, "band": band, "gym_bin": int(gym_bin),
                        "gym_mean_exam": float(centers.loc[gym_bin]),
                        "applicants": len(cell),
                        "gymnasiums": len(cell[["county", "gymnasium"]].drop_duplicates()),
                        "counties": cell["county"].nunique(),
                        "successes": int(cell["success"].sum()),
                        "success_rate": float(cell["success"].mean())})
    return pd.DataFrame(records), boundaries


def _plot_pooled_gymnasium_mean(bins, boundaries, tier, path, settings, *, bin_method="quantile"):
    """Standalone combined plot with literal full-gymnasium mean on x."""
    fig, axis = base.plt.subplots(figsize=(15, 7))
    for band, color in zip(base._band_labels(settings), base.BAND_COLORS):
        data = bins.loc[(bins["tier"] == tier) & (bins["band"] == band)]
        data = data.sort_values("gym_bin")
        if data.empty:
            continue
        # Missing equal-width bins remain visible as gaps rather than a line
        # implying an unobserved success rate between distant bins.
        plotted = boundaries[["gym_bin", "gym_mean_center"]].merge(
            data[["gym_bin", "success_rate"]], on="gym_bin", how="left",
            validate="one_to_one")
        axis.plot(plotted["gym_mean_center"], 100 * plotted["success_rate"],
                  marker="o", linewidth=2, color=color, label=band)
        if band in base._band_labels(settings)[2:]:
            for row in data.itertuples():
                axis.annotate(f"{row.successes}/{row.applicants}\n{row.gymnasiums} gyms",
                              (row.gym_mean_exam, 100 * row.success_rate),
                              xytext=(0, 8), textcoords="offset points",
                              ha="center", fontsize=7, color=color)
    axis.set_xticks(boundaries["gym_mean_center"],
                    [f"{row.gym_mean_center:.2f}\n{row.gymnasiums} gyms"
                     for row in boundaries.itertuples()])
    axis.set_xlabel("Mean national-exam score of all observed applicants in a gymnasium\n"
                    "(one shared bin per gymnasium; tick labels show gymnasiums per bin)")
    axis.set_ylabel("Placed in designated top-tier program (%)")
    method_label = "Equal-width" if bin_method == "equal_width" else "Quantile"
    axis.set_title(f"Romania 2001: {len(settings.counties)} counties pooled, {method_label.lower()} gymnasium-mean bins\n"
                   f"Top {tier} cutoff tier(s); shared own-score percentile bands; "
                   "applicant-weighted outcomes")
    axis.grid(alpha=.2)
    axis.legend(title="Own examination score", fontsize=9)
    fig.text(.5, .01, "Each gymnasium enters one peer-score bin. Labels on stronger "
             "student-score bands are successful placements / eligible applicants and "
             "distinct gymnasiums. Descriptive association only.",
             ha="center", fontsize=9)
    fig.tight_layout(rect=[0, .04, 1, 1])
    fig.savefig(path, dpi=170)
    base.plt.close(fig)


def run_pilot(settings: Settings = Settings(), *, run: bool = False):
    """Save descriptive outputs only after the notebook's RUN_ANALYSIS switch."""
    settings.validate()
    if not run:
        print("Analysis is off. Set RUN_ANALYSIS = True in the notebook.", flush=True)
        return None
    frame, chosen, overview = _source_frames(settings)
    frame, boundaries = base._add_bands(frame, settings)
    print("Calculating source-backed denominators and display bins...", flush=True)
    primary = base._eligible(frame, settings,
                             exclude_vocational=not settings.include_vocational_in_primary)
    summary = base._summary(frame, chosen, settings)
    hero = base._hero_bins(primary, settings.hero_bins)
    bands = pd.concat([base._binned(primary, "county_band", settings.peer_strength_bins),
                       base._pooled_binned(primary, "county_band", settings.peer_strength_bins)],
                      ignore_index=True)
    equal_county_bands = _equal_county_bins(primary, "county_band",
                                            settings.peer_strength_bins)
    equal_county_hero = _equal_county_bins(primary, "county_band",
                                           settings.hero_bins, hero=True)
    gym_mean_bins, gym_mean_boundaries = _pooled_gymnasium_mean_bins(
        frame, primary, settings, bin_method="quantile")
    gym_mean_ew_bins, gym_mean_ew_boundaries = _pooled_gymnasium_mean_bins(
        frame, primary, settings, bin_method="equal_width")
    pooled = (pd.concat([base._binned(primary, "pooled_band", settings.peer_strength_bins),
                         base._pooled_binned(primary, "pooled_band", settings.peer_strength_bins)],
                        ignore_index=True) if settings.compare_pooled_score_bands else pd.DataFrame())
    if (hero.empty or bands.empty or equal_county_bands.empty
            or equal_county_hero.empty or gym_mean_bins.empty or gym_mean_ew_bins.empty):
        raise ValueError("No supported cells for these plot settings")
    stamp = datetime.now().astimezone().strftime("run_%Y%m%dT%H%M%S%z")
    folder = (OUTPUTS if settings.counties == NEW_COUNTIES else ALL_OUTPUTS) / stamp
    folder.mkdir(parents=True, exist_ok=False)
    print("Saving aggregate CSVs and figures...", flush=True)
    for name, table in (("summary", summary), ("county_size_and_movement", overview),
                        ("score_band_boundaries", boundaries), ("qualifying_programs", chosen),
                        ("hero_bins", hero), ("conditional_bins_county_bands", bands),
                        ("hero_bins_equal_county", equal_county_hero),
                        ("conditional_bins_equal_county", equal_county_bands),
                        ("combined_gymnasium_mean_bins", gym_mean_bins),
                        ("gymnasium_mean_bin_boundaries", gym_mean_boundaries),
                        ("combined_gymnasium_mean_equal_width_bins", gym_mean_ew_bins),
                        ("gymnasium_mean_equal_width_bin_boundaries", gym_mean_ew_boundaries)):
        table.to_csv(folder / f"{name}.csv", index=False)
    if not pooled.empty:
        pooled.to_csv(folder / "conditional_bins_pooled_bands.csv", index=False)
    for tier in settings.top_tiers:
        base._plot_hero(hero, tier, folder / f"hero_top{tier}.png", settings)
        base._plot_hero(hero, tier, folder / f"hero_combined_top{tier}.png",
                        settings, counties=("ALL",))
        base._plot_hero(equal_county_hero, tier,
                        folder / f"hero_combined_equal_county_top{tier}.png",
                        settings, counties=("ALL",))
        base._plot_bands(bands, tier, folder / f"conditional_county_bands_top{tier}.png",
                         "within-county own-exam bands", settings)
        base._plot_bands(bands, tier, folder / f"conditional_county_only_bands_top{tier}.png",
                         "within-county own-exam bands", settings,
                         counties=settings.counties)
        base._plot_bands(bands, tier, folder / f"conditional_combined_bands_top{tier}.png",
                         "within-county own-exam bands", settings, counties=("ALL",))
        base._plot_bands(equal_county_bands, tier,
                         folder / f"conditional_combined_equal_county_bands_top{tier}.png",
                         "within-county own-exam bands", settings, counties=("ALL",))
        _plot_pooled_gymnasium_mean(
            gym_mean_bins, gym_mean_boundaries, tier,
            folder / f"combined_gymnasium_mean_top{tier}.png", settings)
        _plot_pooled_gymnasium_mean(
            gym_mean_ew_bins, gym_mean_ew_boundaries, tier,
            folder / f"combined_gymnasium_mean_equal_width_top{tier}.png",
            settings, bin_method="equal_width")
        if not pooled.empty:
            base._plot_bands(pooled, tier,
                             folder / f"conditional_pooled_bands_top{tier}.png",
                             "pooled own-exam bands", settings)
        print(f"  Saved top-{tier} county, applicant-weighted, and equal-county plots",
              flush=True)
    gate_files = ([SOURCE_GATE] if any(c in NEW_COUNTIES for c in settings.counties) else [])
    if any(c in base.COUNTY_NAMES for c in settings.counties):
        gate_files.append(base.SOURCE_GATE)
    if any(c in ("AR", "SB") for c in settings.counties):
        gate_files.append(base.EXPANSION_GATE)
    if "B" in settings.counties:
        gate_files.append(base.BUCHAREST_GATE)
    manifest = {"run_at_local": stamp, "settings": asdict(settings),
                "source_gate_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                       for p in gate_files},
                "privacy": "aggregate output only; private source pages remain on Desktop",
                "scope": f"{len(settings.counties)} origin counties, 2001 main admissions round; descriptive"}
    (folder / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    lines = [f"# Romania 2001: {len(settings.counties)}-county descriptive pilot", "",
             "This run combines the previously verified county-wide placement pipeline "
             "with the newer school-specific admitted/rejected-result pipeline. Printed name and admission "
             "score are provisional linkage keys because the archival ID is masked. "
             "The observed peer pool includes admission-round applicants, not all eighth graders.", "",
             "Program rankings and outcome settings are recorded in `run_manifest.json`. "
             "Top one and top two are separate cumulative cutoff tiers. An admitted student "
             "is successful only when their actual local program belongs to the designated tier. "
             "Outside-county placements are excluded from the outcome denominator but retained "
             "as gymnasium peers; confirmed unassigned applicants remain in the denominator.", "",
             "## County results", "",
             "| County | Top tiers | Applicants | Outcome denominator | Selected | Observed % | Winning programs | Program places |",
             "|---|---:|---:|---:|---:|---:|---:|---:|",]
    for row in summary.itertuples():
        lines.append(f"| {row.county} | {row.tier} | {row.source_applicants:,} | "
                     f"{row.primary_denominator:,} | {row.primary_successes:,} | "
                     f"{100 * row.primary_observed_success_fraction:.2f} | "
                     f"{row.qualifying_programs:,} | {row.qualifying_program_places:,} |")
    lines += ["", "Each plot point or bar has its applicant and gymnasium support recorded "
              "in the corresponding aggregate bin CSV. The applicant-weighted pooled plots "
              "compute a single rate over all applicants in each common peer-score bin. "
              "The equal-county pooled plots first compute one rate per represented county "
              "within each peer-score bin (and own-score band), then average those county "
              "rates equally. A county with no eligible applicants in a cell is absent, not "
              "assigned zero; the number of contributing counties is printed on the plot. "
              "Thus even equal-county curves can change composition across bins. "
              "The separate gymnasium-mean plot uses each observed gymnasium with at "
              "least two applicants once to set common peer-score quantile bins. All "
              "eligible students in that gymnasium inherit its bin; the colored "
              "own-score bands use pooled percentiles across the selected counties. "
              "Success rates within those cells weight eligible applicants equally. "
              "The matching equal-width plot changes only how the common gymnasium-mean "
              "bins are cut: equal score intervals replace equal-count gymnasium quantiles. "
              "Empty equal-width intervals remain visible as gaps. "
              "These are descriptive associations, "
              "not estimates of a causal peer or congestion effect. No applicant preferences "
              "are observed; the success fraction is not institutional K/N.", "",
              "The new-county source gate had zero unresolved top-one/top-two labels. "
              "Galați retains its documented one-applicant outcome uncertainty. This is a "
              "selected-county descriptive comparison, not a 41-county national analysis. "
              "No individual-level output was exported.", ""]
    (folder / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print("Completed. Read:", folder / "report.md", flush=True)
    return folder, summary


if __name__ == "__main__":
    raise SystemExit("Run from the researcher-controlled notebook; importing does nothing.")
