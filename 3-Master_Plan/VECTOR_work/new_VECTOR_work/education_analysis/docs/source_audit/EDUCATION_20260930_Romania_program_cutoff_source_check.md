# Alba 2001: program admission cutoffs are available

**Date:** September 30, 2026.  
**Result:** The archived Ministry main-allocation reports provide program-level last-admitted scores directly. We do not need to estimate them from the examination-score sample or retrieve every admitted-student roster merely to construct this ranking measure.

## What we did and why

Charles approved admission cutoff as the first program-ranking measure. We followed the archived Ministry home page to the main allocation map, Alba report index, specialization directory, and occupancy/results table. The home page links the main allocation and second allocation separately; these tables came from the main family, not `rep2/`. The archival capture dates are in 2002, but the source is the 2001 admissions site. We do not interpret the capture date as the admission cohort or claim these are final results after every later allocation round.

Only a handful of archive pages were requested using the existing identified, sequential, adaptive retriever. A local source parser then joined and checked the two aggregate program tables. No individual placement matching, success labels, or HERO calculation ran.

## Fields and completeness within this report family

The specialization directory contains 85 distinct literal program codes. It supplies school name, profile, specialization, level, attendance form, teaching language, and offered places. The results table has the same 85 codes embedded at the beginning of its program descriptions. It supplies offered places, free places, admitted count, `Prima notă` (first/highest listed score), and `Ultima notă` (last/lowest listed score).

All 85 code joins are exact. The school-name prefixes, profiles, specializations, and seat counts agree between the tables. Every row satisfies places = admitted + vacancies. The totals are:

- 4,325 offered places;
- 2,977 admitted students, agreeing with the earlier main-allocation county report count;
- 1,348 vacant places;
- 55 fully occupied programs;
- 28 partly occupied programs; and
- two programs with no admitted students.

Both empty programs print 0.00 as their first and last score. In the parsed data, their observed cutoff is **missing**, not zero. The original printed value is retained separately. The 28 partly occupied programs have observed last-admitted scores, but these are not automatically binding capacity thresholds.

## Program types that must remain distinguishable

The directory contains 15 Mathematics–Informatics programs, 12 Natural Sciences programs, seven Social Sciences programs, 11 Philology programs, 23 entries in the broad technological specialization, and 17 vocational entries. The broad technological and vocational labels do not establish that all their subfields are interchangeable.

There are 68 high-school-level and 17 vocational-level entries. Eighty-two use Romanian and three use Hungarian. Eighty-three are daytime programs, one evening, and one distance. The parsed file preserves every distinction. No eligibility exclusion or collapse of language/attendance categories was applied.

## Concrete examples supporting program-level ranking

Among the listed Mathematics–Informatics entries, the highest reported cutoff is **9.06**, at Colegiul Național “Horea, Cloșca și Crișan,” Alba Iulia (literal source code `xx8`). Its 100 places are all filled. The next listed mathematics cutoff is **8.79**, at Grup Școlar de Industrie Ușoară, Alba Iulia (`x47`), with 25 of 25 places filled.

Among the listed Philology entries, the highest reported cutoff is **8.03**, at Colegiul Național “David Prodan,” Cugir (`x22`), with 25 of 25 places filled. The next is **8.02**, at Grup Școlar de Industrie Ușoară, Alba Iulia (`x48`), also with 25 of 25 filled.

Thus the highest-cutoff mathematics and philology programs belong to different schools, as Charles anticipated. These examples describe entrance selectivity in the source, not teaching quality or preferred-choice attainment.

The program cutoffs are on the **admission-score scale**. Our gymnasium intervals use the separate **national-examination-score scale**. Those variables must not be conflated. Previous source checks support the admission composite's truncated 75% examination / 25% school-grade formula; the published paper's equal-weight description remains an unresolved documentary discrepancy.

## What this resolves and what remains

The ranking-field availability gate is passed for the 85 Alba entries in this report family. Source rows are ordered by specialization and descending observed cutoff in the saved JSON; this ordering creates no binary success definition.

Before producing a HERO, we still need the student placement merge and Charles's choice of the success boundary and comparison scope. We have not designated a top program or top tier as the successful set, determined all competitive preference sets, ranked outside-Alba destinations, or imposed transfer exclusions. Public cutoffs summarize realized allocation and do not reveal unobserved preferences, tie-breaks, or a guaranteed admission rule for every individual.

## Reproducible source trail

- [Main allocation map](https://web.archive.org/web/20020803161508id_/http://www.edu.ro/adm2001/harta.asp.htm).
- [Alba report index](https://web.archive.org/web/20020622154846id_/http://www.edu.ro/adm2001/rapoarte.asp-cj=AB&nj=ALBA.htm).
- [Program directory](https://web.archive.org/web/20020624015645id_/http://www.edu.ro/adm2001/raport_specializari.asp-cj=AB&nj=ALBA&idx=0.htm).
- [Program occupancy and first/last scores](https://web.archive.org/web/20020816152305id_/http://www.edu.ro/adm2001/raport_situatie_licee_per_judet.asp-cj=AB&nj=ALBA&idx=0.htm).
- Saved aggregate HTML, [parsed program records](../../outputs/romania_alba_2001_program_cutoffs_20260930/program_cutoffs.json), and [source checks with URLs and hashes](../../outputs/romania_alba_2001_program_cutoffs_20260930/source_audit_summary.json).
- [Local parser](../../code/EDUCATION_20260930_program_cutoff_source_audit.py). It performs no network requests and accepts `--source-dir` containing `programs.html` and `occupancy.html`. It can be rerun on the preserved source directory.
- [Ranking and HERO decision record](../decisions/EDUCATION_20260930_Romania_program_ranking_and_HERO_decisions.md).
