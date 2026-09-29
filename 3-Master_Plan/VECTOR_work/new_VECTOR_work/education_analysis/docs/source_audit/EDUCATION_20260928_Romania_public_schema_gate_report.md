# Romania public replication data: schema gate report

**Date:** 2026-09-28  
**Status:** **PASS for a bounded peer-environment analysis specification.**  
**Execution boundary:** Public files were inventoried and their grouping structure was checked. No assortativity measure, outcome relationship, regression, HERO curve, or other substantive result was calculated.

## 1. Why this gate mattered

The public-web audit established that the Romania replication archive contains prior transition scores, admission-cutoff information, and later Baccalaureate outcomes. It could not establish whether usable assigned-school or academic-track identifiers survived in the deposited files.

That was the decisive question. Without a common group identifier, the files could support the published regression-discontinuity design but could not support our descriptive peer-pool analysis.

The authenticated public archive has now been downloaded and inspected locally.

## 2. Source acquired

The complete public replication archive was downloaded from openICPSR project `112645`, version 1:

- Project: [Replication data for “Going to a Better School: Effects and Behavioral Responses”](https://www.openicpsr.org/openicpsr/project/112645/version/V1/view)
- Local archive: `datasets/romania/source_public_openicpsr_20260928/Romania_112645-V1.zip`
- Archive SHA-256: `00744e3b266f0d8a7ea3578dca733758f523fb62a5143a6216de523aa979b99b`
- ZIP integrity: passed

The archive contains eight Stata data files, three Stata programs, and README files in PDF and DOCX formats. The source directory is ignored by Git and included in the existing `education` rsync scope. No rsync transfer was executed during this audit.

## 3. The decisive files

`data-AER-4.dta`, `data-AER-5.dta`, and `data-AER-6.dta` provide the cleanest student-level structure for the 2001, 2002, and 2003 admission cohorts.

| File | Cohort | Student rows | Towns | Schools | School-track units |
|---|---:|---:|---:|---:|---:|
| `data-AER-4.dta` | 2001 | 107,812 | 134 | 797 | 1,722 |
| `data-AER-5.dta` | 2002 | 110,912 | 134 | 789 | 1,665 |
| `data-AER-6.dta` | 2003 | 115,413 | 135 | 801 | 1,615 |
| **Total** | 2001–2003 | **334,137** | — | — | **5,002 cohort × school-track cells** |

The relevant variables are:

- `grade` — the student's pre-assignment transition score;
- `year` — admission cohort;
- `ua` — town identifier used by the authors' code;
- `us` — school identifier used by the authors' code;
- `us2` — school-track identifier used by the authors' code;
- `bct` — indicator that the student took the Baccalaureate examination;
- `bcg` — Baccalaureate examination grade;
- `ct` — observation counter, equal to one on every row; and
- `survey` — indicator for the authors' survey subsample, not required for the administrative peer-pool analysis.

The public files do not attach informative labels to most administrative variables. Their meanings are established by the published paper and by how the authors' deposited Stata code uses them. In particular, the code counts students within `us2`, then school-track units within `us`, and schools within `ua`.

## 4. Peer-pool verification

The identifier nesting passed without exception in all three cohorts:

- every `us2` school-track identifier maps to exactly one `us` school;
- every `us2` school-track identifier maps to exactly one `ua` town; and
- every `us` school identifier maps to exactly one `ua` town.

There are no missing values in `year`, `grade`, `ua`, `us`, `us2`, `bct`, or `ct`.

The median school-track group contains:

- 50 students in 2001;
- 56 students in 2002; and
- 60 students in 2003.

Most school-track cells are therefore large enough for leave-one-out peer calculations. Of 5,002 cohort × school-track cells, 5 contain one student, 13 contain fewer than five students, and 28 contain fewer than ten students. A later analysis specification must state a minimum group-size rule before calculating peer measures. No such rule was chosen during this schema audit.

## 5. Student identity

Files 4–6 do not include a named stable student-ID variable. They are already organized as one administrative student record per row, with the prior score, assigned group, and later outcome on that same row. The authors' code treats `ct = 1` as the student counter when producing sample counts.

For the proposed descriptive peer-pool analysis, a reproducible row identifier can identify each anonymous student record. No cross-file person linkage is required because each file represents a different admission cohort and contains the necessary outcome on the same row.

This is sufficient for leave-one-out calculations. It would not be sufficient for an unplanned longitudinal merge to another person-level source.

## 6. Prior performance and later outcome

The pre-assignment transition score `grade` is present for all 334,137 student rows.

Baccalaureate participation `bct` is present and binary for every row: 275,719 students are coded as taking the examination and 58,418 as not taking it. No non-taker has a recorded grade. Among examination takers, 257,433 have a recorded Baccalaureate grade and 18,286 do not. The usable outcome must therefore remain two separate stages:

1. whether the student took the Baccalaureate examination; and
2. examination grade among takers with an observed grade, with the missing-grade incidence reported and investigated before modeling.

Do not collapse these stages into one invented success indicator merely to resemble a sports draft or Army selection outcome.

## 7. What the other files contain

`data-AER-1.dta` contains 3,621,905 cutoff-expanded rows and 19 variables. It preserves the published regression-discontinuity structure, including cutoff distance, treatment/better-school status, Baccalaureate outcomes, an encoded student identifier (`sid2`), and cutoff grouping variables. It is not the preferred input for constructing ordinary peer pools because students occur repeatedly around multiple cutoffs.

`data-AER-2.dta` and `data-AER-3.dta` are also expanded analytical files. Files 7 and 8 contain the authors' smaller survey samples and classroom/behavioral variables.

The clean student-level peer-pool analysis and the published cutoff-based identification analysis should remain separate. They answer related but different questions.

## 8. Selection intensity and congestion

Romania contains genuine scarcity in admission to school-track combinations. The public deposit preserves cutoff information in the expanded analytical files.

The clean student files do not provide the complete ranked applicant-choice set required to define one unambiguous applicant denominator \(N\) for each track. Therefore:

- use admission cutoff or cutoff percentile as the principal empirical measure of selectivity;
- treat realized school-track enrollment as filled capacity, not automatically as an official capacity field; and
- do not report a simple \(K/N\) unless a later provenance check establishes a defensible risk set.

Scarcity governs entry into the environment. The Baccalaureate examination is a later performance and attainment outcome, not a fixed-\(K\) award among the students after entry.

## 9. Gate decision

Romania **passes** the public peer-pool gate because the deposit supports a unique anonymous student-row table containing:

- admission cohort;
- prior transition score;
- assigned school;
- assigned academic track;
- Baccalaureate participation; and
- Baccalaureate grade.

The external dataset search should stop. Do not move to Chicago, Kenya, or a restricted-data application for the immediate education investigation.

Passing this gate authorizes preparation of a bounded analysis specification only after Charles reviews this report. It does not authorize calculation of assortativity, outcome curves, regressions, or figures.

## 10. What a later specification could ask

The narrow descriptive question would be:

> Among students with similar pre-assignment transition scores, how are assigned school-track peer performance and the student's relative position associated with later Baccalaureate participation and performance?

A separate identification question could use the published admission cutoffs:

> Among students close to an admission cutoff, what is the effect of gaining access to the stronger school environment on later outcomes?

The first describes peer composition and relative standing. The second estimates the effect of access to a bundle of school features. Neither should be presented as a pure causal estimate of peer quality or as direct proof of downstream congestion.

## 11. Reproducibility artifacts

- Header and provenance audit: `education_analysis/code/EDUCATION_20260928_romania_public_schema_audit.py`
- Pool-structure gate: `education_analysis/code/EDUCATION_20260928_romania_pool_structure_gate.py`
- File inventory: `education_analysis/outputs/romania_schema_audit_20260928/file_inventory.json`
- Variable inventory: `education_analysis/outputs/romania_schema_audit_20260928/variable_inventory.csv`
- Pool-structure results: `education_analysis/outputs/romania_schema_audit_20260928/pool_structure_gate.json`
