# Romania 2001 national archive: gap and recovery audit

**Date:** October 1, 2026  
**Scope:** Source acquisition and completeness only. No national sorting index, placement outcome, or congestion result was calculated.  
**Private source cache:** `~/Desktop/VECTOR_temp/romania_2001_national_main_allocation_v1/`. It contains identifiable archived records and remains outside Dropbox and Git.

## What we learned

1. **The interrupted national run is incomplete, but its saved work is intact.** The official directory lists 41 county units. At the stopped checkpoint, 30 had county manifests, 10 of those were complete, and 11 had no manifest yet. The 30 manifests recorded 20 page addresses returning HTTP 404 and 10 returning HTTP 429. These numbers describe archive retrieval, not a research sample.
2. **A 404 is not simply evidence that we requested an invented page.** All 20 original 404 addresses were linked from saved, verified report pages. A paced lookup through the Internet Archive's Availability API reported no alternative capture for those exact addresses. This is evidence of a source-archive gap, though an empty API answer does not prove that every possible recovery route is exhausted.
3. **A 429 is a different problem.** It means the request was throttled. One targeted retry of a previously throttled Bistrița-Năsăud admitted-placement page returned 404 instead; its manifest now records that fixed gap. At that point, the manifests contained 21 HTTP 404 and nine HTTP 429 entries.
4. **Five of those nine throttled addresses had reported captures.** We retried only those five, using the existing archive client with 60-second request spacing. All five returned source pages, passed source-path, table-column, and checkpoint-integrity checks, and were saved in the private cache. Their report-view row counts were 500 (Gorj candidate roster), 194 (Galați unassigned applicants), 500 (Iași admitted placements), 500 (Maramureș admitted placements), and 500 (Neamț admitted placements): **2,194 rows across report views**, not 2,194 newly identified students. The remaining four 429 addresses had no capture reported by the Availability API; they have not been declared irrecoverable.
5. **Recovered pages do not make their counties complete.** Four of the five recovered pages link onward to another page not yet saved: Gorj candidate page index 3001, Iași and Maramureș admitted page index 1500, and Neamț admitted page index 2500. Galați's recovered unassigned report has no further page in that family, but its admitted-placement family still has a 404 gap. The saved county manifests are not yet refreshed to incorporate these five new page checkpoints; the normal acquisition notebook will rebuild them on resume.
6. **Redundant school-specific reports look promising as a bounded repair route.** The official origin-school directories list 248 schools in Bihor and 119 in Brăila. A two-page source pilot recovered one Bihor school candidate report with 47 rows, all 47 matching records already present in the saved Bihor county candidate report on name and admission average. A Brăila school placement report had 74 rows, 42 matching its saved county placement report; the other 32 are *unpaired with the currently saved county report*, not yet proven missing from the source universe. This establishes an overlapping report view, not completeness or a validated national reconstruction. The 17 counties with original 404 gaps list 3,249 origin-school codes in total, so a blanket school-report crawl would be a substantial new acquisition, not a small retry.

## Why this matters for the scientific question

An apparent change in placement rates could be caused by missing county pages or an incomplete originating-gymnasium applicant pool. We therefore cannot treat the presently saved national files as a national research cohort. The previously completed **Alba 2001** analyses have their own documented aperture and are not invalidated by this national acquisition gap. No new national curve, sorting estimate, or selection comparison follows from this audit.

We should also avoid assuming that a county candidate count must equal that county's admitted-plus-unassigned count: students can cross county boundaries. The identity-level reconciliation must use the saved source records, rather than count equality alone, and must remain within the private cache.

## Code and audit trail

- Acquisition and manifest logic: `education_analysis/code/EDUCATION_20260930_romania_2001_national_acquisition.py`.
- Archive pacing and HTTP log: `education_analysis/code/romania_archive_retrieval.py`; runtime events in the private cache.
- Read-only Availability API lookup: `education_analysis/code/EDUCATION_20261001_romania_archive_availability_probe.py`. It queries the saved 404 addresses by default or a supplied status such as `429`, one query every five seconds, and writes no source records.
- Two-page school-report overlap pilot: `education_analysis/code/EDUCATION_20261001_romania_school_view_overlap_pilot.py`. It keeps identifiable school pages in memory and prints aggregate overlap counts only.
- Exact five-address, source-only retry: `education_analysis/code/EDUCATION_20261001_romania_targeted_429_recovery.py`. This is a one-time audit script; the ordinary notebook remains the supported resume path.
- Researcher-run acquisition notebook: `education_analysis/notebooks/EDUCATION_20260930_Romania_2001_national_acquisition.ipynb`.

The acquisition companion was adjusted so a resumed run **retains known 404/410 addresses as unresolved without requesting them again**. It still retries transient failures. An offline, no-network check verified that a 404-only county is skipped, a county with both 404 and 429 is eligible for retry, and a saved page is read from its verified checkpoint. The notebook file was not edited; its import cell reloads the companion code.

## Next bounded gate

Resume the acquisition notebook only when Charles wants the background source gathering to continue. Rerun its import/reload cell before its acquisition cell so the 404-skipping change is loaded. The saved five-page recovery should be incorporated as the relevant county report families are revisited. After the remaining first-pass counties are attempted, audit which report families are complete, which links are unavailable, and whether school-specific views can fill a *small, specified* set of gaps. Stop before any national outcome analysis. PD44 places dissertation model-chapter drafting in the foreground while this source work continues in the background.
