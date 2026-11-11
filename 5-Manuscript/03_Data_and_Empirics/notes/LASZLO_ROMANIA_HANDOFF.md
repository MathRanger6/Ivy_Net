# Romania acquisition and reconciliation handoff to LASZLO

**From:** NVector, working with Charles Levine  
**To:** LASZLO, the Cursor agent taking over Romania  
**Prepared:** October 14, 2026  
**Inventory refreshed:** October 14, 2026, 18:45:59 EDT

## Your immediate job

Charles reports that the download pass has finished. The next useful background task is **offline reconciliation of all saved county sources**: establish which applicant, school-result, placement, and cross-county records agree, and identify exactly what remains unresolved. Charles and NVector are focusing on the dissertation and basketball work while you take responsibility for Romania.

You have access to the entire workspace. Work in the existing project and reuse its verified parsers, checkpoint readers, and matching methods. There is no isolated handoff code copy to maintain. Prepare a researcher-controlled notebook so Charles can run the reconciliation and watch clear progress messages. Do not interpret this handoff as permission to launch a new national outcome analysis, silently change research definitions, or start another broad download campaign.

## Start here and establish the current state

This handoff is in `3-Master_Plan/VECTOR_work/new_VECTOR_work/`. All links below are relative to that folder. The main Romania folder is [education_analysis](education_analysis/).

1. Read the repository-root `AGENTS.md` and relevant local instructions. Charles has explicitly waived the notebook editing rule until further notice: it was intended for work he must hand-transcribe onto an Army system. Direct notebook editing is authorized; do not repeatedly ask him to waive it again.
2. Refresh the [county progress notebook](education_analysis/notebooks/EDUCATION_20261013_Romania_2001_county_progress.ipynb), or call `collect_progress()` from its [Python companion](education_analysis/code/EDUCATION_20261013_romania_county_progress.py). This is a read-only inventory, not a fresh integrity or person-linkage audit.
3. Read the existing seven-county and four-new-county reconciliation code identified below. Their names and hard-coded county lists reflect previous stages. Do not simply rerun them and label the output national.
4. Prepare an all-county offline reconciliation notebook, using the acquisition inventory to enumerate county units. Leave Charles in control of running it. Refresh the inventory again when work starts because downloads or audits may have changed since this snapshot.

Python on this Mac is `/opt/anaconda3/envs/sports_net/bin/python`. Use the `sports_net` notebook kernel. Do not assume that repository access on another computer includes the private source files on this Mac's Desktop.

## What is actually saved now

The [handoff inventory snapshot](education_analysis/outputs/laszlo_handoff/progress_at_handoff.json) contains the county-by-county details and the following totals. These are checkpoint/status counts, not a new verification of every downloaded page.

- The acquisition inventory has **41 county units**. Its `B` unit is labelled **BUCURESTI si ILFOV**. Preserve that source geography; do not equate this inventory mechanically with modern administrative units.
- **School applicant pages:** 2,000 saved out of 7,553 listed schools, complete for **11 county units**.
- **School result pages:** 7,592 saved out of 7,594 targets, complete for **39 county units**. These counts include directory pages. **BN and SV each have one unresolved school-result URL.** Keep both open.
- **Incoming lists:** all three tracked incoming families have all known pages saved in **all 41 units**. The families are incoming candidates, incoming admitted, and incoming rejected.
- **Resident applicant lists:** 299 pages saved out of 385 projected, complete for **27 units**. Other views may corroborate or recover people absent from incomplete resident lists; a short resident list is not automatically a reason to discard the county.
- **Later school/result audit records:** present for **11 units**, absent for **30**. “Saved checks available” is not equivalent to “all source gates passed.” Inspect their findings and dates.

The 11 previously developed origin-county datasets are **AB, CS, GL, TL, AR, SB, B, CT, PH, TM, CJ**. Existing plots and reconciliation work cover different subsets and dates; preserve those distinctions.

Charles's statement that downloading is complete means the acquisition pass has finished. It does not establish that every source family is complete. In particular, the newly downloaded **school results** are not the same webpage family as the separately downloaded **school applicants**.

## The source webpages in ordinary language

These are different views of the Romanian Ministry's 2001 admissions records, recovered through the Wayback Machine. A webpage organized by school is still a Ministry report, not an independently maintained school website.

**School Applicant View:** A list of applicants associated with an originating gymnasium, with examination and admission-score information. This is the established source for constructing the observed gymnasium peer population. It does not prove that every eighth grader at the school applied.

**School Result View:** A school-organized list showing admitted and unassigned applicants and destination labels where provided. This helps establish outcomes and movements. Do not assume its rows and the School Applicant View are identical or silently add result-only rows to the score-bearing population.

**County Applicant Views:** County-wide lists, including resident and general applicant lists. Their populations and completeness can differ. Identify the actual report family rather than calling every one “the county list.”

**County Placement and Unassigned Views:** Lists of admitted applicants and applicants not allocated a place in the main round. The label translated as “rejected” or `NEREPARTIZAT` does not establish rejection from a specific desired program or failure in every later admissions round.

**Incoming Applicant and Outcome Views:** Lists of applicants from other counties and their admitted/unassigned outcomes in the receiving county. They allow comparisons against outgoing destinations in origin-school reports. Movement means an observed admissions route, not necessarily a residential move.

**Program Views:** Program directories, capacity/occupancy tables, and admitted-student lists per specialization. These identify programs and help reconcile placement totals and destination labels. Program places are offered seats, not a count of applicants expressing that preference.

## Where the private source files live

Read the path constants in code before using a directory. The following are the established locations on Charles's Mac:

- `~/Desktop/VECTOR_temp/romania_2001_national_main_allocation_v1/`: national county directory, original report checkpoints, county manifests, and related source files. Program recovery uses its `alternate_report_pilot/` subfolder.
- `~/Desktop/VECTOR_temp/romania_2001_school_results_incoming_v1/`: new school-result and incoming report families, with `pages/`, `status.json`, and retrieval events.
- `~/Desktop/VECTOR_temp/romania_2001_four_county_school_source_pilot/school_reports/`: the shared non-Alba school-applicant checkpoint store, whose historical folder name does not limit it to four counties.
- `~/Desktop/VECTOR_temp/romania_alba_2001_differentiation_v1/school_reports/`: Alba's earlier school-applicant format. Reuse the special reader that verifies its schema and hashes.

Keep raw student records and identifying linkage ledgers in the private source area. Repository outputs should contain name-free aggregates, metadata, decisions, and figures. Preserve source URL addresses, capture timestamps where available, hashes, and provenance. Do not overwrite or repair raw historical evidence merely to make reconciliation pass.

## The existing code to reuse

### Acquisition and progress

- [All-county progress](education_analysis/code/EDUCATION_20261013_romania_county_progress.py): checkpoint counts and recorded audit status. Its notebook supports sorting by saved School Applicant View pages.
- [School results and incoming notebook](education_analysis/notebooks/EDUCATION_20261006_Romania_2001_school_results_and_incoming.ipynb) and [worker](education_analysis/code/EDUCATION_20261006_romania_school_results_incoming_acquisition.py): the latest nationwide acquisition families.
- [National gymnasium applicants notebook](education_analysis/notebooks/EDUCATION_20261006_Romania_2001_national_gymnasium_applicants.ipynb): additional School Applicant View acquisition, using the [shared school acquisition module](education_analysis/code/EDUCATION_20261002_romania_three_county_gymnasium_acquisition.py). Do not start these remaining downloads until the audit identifies what is needed and Charles chooses the next acquisition step.
- [National acquisition module](education_analysis/code/EDUCATION_20260930_romania_2001_national_acquisition.py): source identities, checkpoint verification, and original county reports.
- [Background placement recovery worker](education_analysis/code/EDUCATION_20261001_romania_background_placement_worker.py): reconstructs missing county placements from program-specific views. `placement_views_reconciled` does not certify applicant completeness.

### Offline reconciliation

- [Original full gymnasium reconciliation](education_analysis/code/EDUCATION_20261002_romania_full_gymnasium_offline_reconciliation.py): verified school-page readers, normalized score comparisons, name/score linkage, and ambiguity handling. Some routines retain four-county globals.
- [Seven-county new-view audit](education_analysis/code/EDUCATION_20261007_romania_seven_county_new_views_offline_audit.py): compares applicant and school-result views and incoming/outgoing flows for the original seven counties.
- [Four-new-county audit](education_analysis/code/EDUCATION_20261008_romania_four_new_county_offline_audit.py): extends source comparisons to CT, PH, TM, CJ and checks flows against the original eleven-county collection.
- [Gymnasium result audit](education_analysis/code/EDUCATION_20261009_romania_four_county_gymnasium_result_audit.py) and [plot-source gate](education_analysis/code/EDUCATION_20261009_romania_four_county_plot_source_gate.py): help establish whether destination labels support the designated program-success classifications.
- [Cross-county outcome ledger](education_analysis/code/EDUCATION_20261007_romania_cross_county_outcome_ledger.py): existing source-backed home-versus-anywhere logic. Inspect its scope and unresolved cases before extending it.

### Existing research outputs

The [all-scraped-counties descriptive notebook](education_analysis/notebooks/EDUCATION_20261009_Romania_2001_all_scraped_counties_descriptive_pilot.ipynb) is the established plotting entry point for the developed county datasets. “All scraped” in its filename is not permission to bypass source checks for every newly downloaded county. Read its saved settings and supported populations before changing it. Preserve the original eleven-county results and run manifests.

## The next notebook should do these jobs

1. **Inventory each source family separately.** Report expected, saved, verified, and unresolved pages. Identify malformed checkpoints, missing metadata partners, conflicting snapshots, and directory coverage discrepancies. One failed county must not prevent independent checks in the others.
2. **Reconcile people conservatively.** Compare School Applicant Views, School Result Views, and county reports. The source masks personal identifiers. Printed name plus admission score, even with origin-school information, is a provisional match. Keep duplicate keys, score-component disagreements, conflicting outcomes, and unmatched records explicit. Do not merge people solely to force counts to agree.
3. **Check cross-county routes from both ends.** Compare school-reported outgoing placements with receiving-county incoming admissions. First compare aggregate origin/destination counts; then report whether individual matches are uniquely supported. Aggregate agreement alone does not prove person-level linkage.
4. **Check program identities and totals.** Preserve county-scoped program codes and specialization details. Compare placements with occupancy counts and program-specific admitted lists. Keep exact-program uncertainty separate from binary outcome uncertainty.
5. **Produce actionable county summaries.** Report observed gymnasium counts, applicants, known placements, explicitly unassigned people, ambiguous/unmatched cases, incoming/outgoing counts with explicit denominators, and precise next-source questions. Say “17 applicants have no uniquely matched result” rather than an unexplained status code.
6. **Save and resume.** Write timestamped aggregate outputs after each county, retain settings and source fingerprints, and skip unchanged verified work when appropriate. Resume logic must notice changed source files; a previous success is not permanent if its inputs changed. Print county name/code, current check, counts, and completion status.

The output should answer: **Which counties can support which analyses, and exactly what evidence is still missing?** It should not declare counties scientifically ready solely because every URL in a queue was attempted.

## Scientific choices to preserve

Read these decision records before extending a research population or outcome:

- [Original program-ranking decisions](education_analysis/docs/decisions/EDUCATION_20260930_Romania_program_ranking_and_HERO_decisions.md).
- [Pilot decisions and six-county extension](education_analysis/docs/decisions/EDUCATION_20261002_Romania_four_county_pilot_design_decisions.md).
- [Home-versus-anywhere outcome extension](education_analysis/docs/decisions/EDUCATION_20261007_cross_county_outcome_design.md).

They describe successive stages, not interchangeable current defaults. Some contain historical “not yet run” statements. Use current notebook settings and saved run manifests to establish what was actually executed.

The core distinctions are:

- Actual placement in a designated high-cutoff program is the outcome. It is not “received first choice”; preference lists are not observed. A score above a cutoff is not itself a successful placement.
- Original rankings use cutoff tiers within county and subject, with ties retained. Top-two is cumulative. Full-occupancy eligibility and six-category versus broader grouping are explicit settings, not interchangeable labels.
- Peer strength uses the other observed applicants from the originating gymnasium. Do not redefine peers using only selected students or only the outcome-analysis denominator.
- Original within-county analyses exclude confirmed outward placements from their outcome denominator while retaining them as peers. The later paired home-versus-anywhere analysis uses a different, explicitly documented denominator and codes outward placement as zero for the home indicator. Do not silently replace one design with the other.
- A destination can have an unresolved exact program code but a known binary classification if every source-supported possible code implies the same success status under the chosen settings. Recheck this when settings change. If possible codes imply different classifications, retain uncertainty.
- A placement gap between an old county list and occupancy totals can be filled by program-specific reports. The original gap column need not become zero; distinguish the original shortfall from the remaining unreconciled shortfall.
- No applicant becomes unsuccessful merely because a match is missing. Confirmed unassigned is different from unresolved.
- County pooling is applicant-based unless explicitly labelled otherwise. Charles also requested pooled absolute peer-score plots with common bins, configurable own-score bands, and both quantile and equal-width versions. Keep axis, band population, denominator, and weighting explicit.

Alex asked us to track gymnasium counts and incoming/outgoing routes when considering counties. Those are source/population diagnostics, not permission to choose only counties with the desired downturn. His priority has been dissertation writing while bounded Romania acquisition proceeds. **National outcome analysis requires the source gates to pass and Charles's explicit authorization.** Existing authorization for particular descriptive county extensions does not automatically authorize a new nationwide run.

## How Charles wants you to work

Charles wants notebooks with visible settings and real-time, conversational progress. Explain the population and question before parameters or abbreviations. Define each source view before referring to it. Say “URL address” when you mean a URL address. Avoid unexplained labels such as “zero-list stratum.” Do not use em dashes.

He values speed. Make focused checks appropriate to the change, and leave expensive or substantive notebook runs under his control. Do not create an elaborate test campaign for a small edit. He likes short progress updates and concrete next steps.

If later downloads are authorized, preserve checkpointing, request identification and contact headers, explicit requested URL addresses, download-versus-cache messages, and pause reasons with start/resume datetimes. Preserve the ability to defer retries of previously unresolved 404s. Charles requested full 429 response diagnostics and substantial recovery waits, plus at least 10 seconds after 500/503 errors. Actual retry policies vary across workers; inspect their current settings rather than overwriting them from remembered numbers. A 404 or exhausted automatic search stays unresolved unless Charles decides otherwise.

Do not alter the manuscript, basketball statistics, or LG exploration project as part of this handoff. Do not send messages to Alex or other agents on Charles's behalf without explicit authorization.

## Your first response to Charles

Confirm that you have read this handoff, refreshed the inventory, and identified the scope of the all-county offline notebook. State any difference from this dated snapshot. Then prepare the notebook and tell Charles exactly which cells to run. If a particular missing source blocks a check, explain that source in ordinary language while allowing other checks and counties to continue.
