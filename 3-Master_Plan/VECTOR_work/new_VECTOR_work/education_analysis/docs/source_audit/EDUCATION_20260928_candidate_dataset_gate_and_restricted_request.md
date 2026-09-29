# Education candidate-dataset gate and minimum restricted-data request

**Date:** 2026-09-28  
**Status:** Public-source acquisition and feasibility gate completed. No substantive model was fitted.  
**Decision:** Retain National Education Longitudinal Study of 1988 (NELS:88) and High School and Beyond 1980 (HS&B:80) for immediate public-data work. Preserve Education Longitudinal Study of 2002 (ELS:2002) and High School Longitudinal Study of 2009 (HSLS:09) as high-priority restricted-use candidates.

## 1. Why we paused before rebuilding the older panels

We asked a prior question before spending more time reproducing the older supplied panels: is there a newer education dataset that fits the scientific problem better?

The required structure is unusually demanding. A viable dataset must contain all of the following:

1. A common peer-group identifier shared by multiple students.
2. A performance or preparation measure observed before the outcome.
3. Enough sampled students in each peer group to calculate a leave-one-out peer measure and relative standing.
4. A later outcome that represents a meaningful transition or selection, such as application, acceptance, selective-college attendance, or degree completion.
5. Documentation and weights sufficient to state the population and uncertainty honestly.

This is the **candidate gate**. A dataset that lacks any indispensable item does not proceed to the nine-panel data-story mosaic.

## 2. Sources downloaded and preserved

Official National Center for Education Statistics (NCES) public-use packages were downloaded from the DataLab Online Codebook and preserved in dated, Git-ignored source directories.

### ELS:2002

Repository source directory: `datasets/els2002/source_public_nces_20260928/`

- Student Stata archive SHA-256: `ebc4b3a64e4314d71911fd976332b151e36cbd2f9c917946084848b2adab6c5c`
- Balanced repeated replication weight archive SHA-256: `062a369807da47d80296a01b85fafba50873e56061a52c0603421b4509adf16d`
- Other-files archive SHA-256: `4f8721d3141905c6c415019f250b809b7828583bfce1cc3f673f4fb8983cb64d`
- Codebook archive SHA-256: `174b7802a96d35b5c3af692433ae0d86da619be2260a996ba3a92aaeeb3d0e8b`

The extracted public files contain 16,197 student records, 1,954 school records, and separate postsecondary institution files.

### HSLS:09

Repository source directory: `datasets/hsls09/source_public_nces_20260928/`

- Student and school Stata archive SHA-256: `9a4196b7df76f1fca620d6ac2116a52a5714fa51ea4d5473a992e41ff27ab832`
- Codebook archive SHA-256: `402dda1d83595a3b6009b52b8e5463506b97ea9277d32a4087b4c494a7389e92`

The extracted public files contain 23,503 student records and 944 school records.

All six archives passed ZIP integrity checks before extraction.

## 3. What the fast public-data gate found

### ELS:2002 contains the desired transitions

Directly inspected public fields include:

- base-year standardized mathematics score (`BYTXMSTD`);
- base-year standardized mathematics/reading composite (`BYTXCSTD`);
- number of applications (`F2NAPP1P`);
- number of acceptances (`F2NACC1P`);
- postsecondary-transcript selectivity of the first known institution (`F3TZPS1SLC`);
- highest known degree by 2013 (`F3TZHIGHDEG`);
- base-year student weight (`BYSTUWT`).

The especially useful selectivity-of-applications, selectivity-of-acceptances, and first-attended-selectivity variables (`F2PSAPSL`, `F2PSACSL`, and `F2PS1SLC`) are present in the file layout but completely suppressed in the public records inspected.

### HSLS:09 contains newer transitions and longer follow-up

Directly inspected public fields include:

- ninth-grade standardized mathematics score (`X1TXMTSCOR`);
- number of colleges applied to (`X4CLGAPPNUM`);
- first postsecondary institution selectivity as of 2016 (`X4PS1SELECT`);
- first known postsecondary institution selectivity as of 2021 (`X6PS1SLC`);
- highest known degree by 2021 (`X6HIGHDEG`).

The bachelor's-degree count variable (`X6BACCRED`) is present in the file layout but completely suppressed in the public records inspected. Its information may still be recoverable from a documented recode of the public highest-degree field; that recode was not performed in this gate.

### Both public files fail the indispensable peer-group test

In both student files, every `SCH_ID` value is the NCES suppression code `-5`:

- ELS:2002: 0 usable common school identifiers among 16,197 students.
- HSLS:09: 0 usable common school identifiers among 23,503 students.

Consequently, the public files cannot identify which sampled students attended the same high school. We cannot calculate a school mean, leave-one-out peer performance, within-school standing, school interval overlap, or assortativity without that link.

The existing mosaic pipeline correctly stopped at this gate. Generating a mosaic by treating sampling strata, geography, or a collection of school characteristics as if they were school identifiers would misstate the scientific unit and defeat the disclosure protection.

The detailed machine-readable evidence is in:

- `education_analysis/outputs/candidate_schema_audit_20260928/`
- `education_analysis/outputs/candidate_feasibility_gate_20260928/`
- `education_analysis/code/EDUCATION_20260928_candidate_schema_audit.py`
- `education_analysis/code/EDUCATION_20260928_candidate_feasibility_gate.py`

## 4. What the other candidate screen told us

### NELS:88 and HS&B:80 remain immediately useful

Their public source files retain a common student-to-school identifier, prior test performance, and later attainment. That makes them unusually useful for a public-data peer-pool investigation despite their age. The recovered source mapping also corrected an earlier repository description: the supplied NELS performance field is the official standardized mathematics score `BY2XMSTD`, rather than a locally created reading/history composite.

### National Longitudinal Survey of Youth 1997

The public identifier can link one respondent's school history across survey rounds, but it cannot identify different respondents who attended the same school. Cross-student school linkage and the School Survey require restricted access. It therefore does not improve the immediate public-data design.

### Project Talent

Project Talent is scientifically attractive: approximately 377,000 students from 1,226 schools, extensive aptitude measurement, and follow-ups after high-school graduation. The readily public linked 1960–1976 file is a 4,000-person subsample of respondents to the eleven-year follow-up, while the full linked student and school data require a request to the American Institutes for Research. It remains a secondary restricted/request candidate, not an immediate download-and-mosaic candidate.

## 5. Minimum restricted-use request

The first question for a licensed faculty collaborator is not “Can you send us the files?” It is:

> Does your approved restricted-use arrangement cover ELS:2002 and/or HSLS:09, and can Charles be added to the approved project or can the following extraction and analysis be run within the approved environment?

Restricted data should remain inside the licensed environment unless the governing agreement expressly permits another arrangement.

### Minimum common fields

For either study, request:

1. A stable anonymous student identifier.
2. A stable common high-school identifier shared by sampled students.
3. Survey stratum, primary sampling unit, final student weight, and replicate weights required for uncertainty.
4. Baseline socioeconomic and demographic variables already available publicly, so the restricted extract can be joined or reproduced without changing definitions.

The common high-school identifier is the decisive addition. It enables school peer groups, relative standing, leave-one-out peer performance, interval overlap, and measured sorting.

### ELS:2002 additions

Request or confirm access to:

- `BYTXMSTD` and/or `BYTXCSTD` — prior measured performance;
- `F2NAPP1P` and `F2NACC1P` — application and acceptance counts;
- `F2PSAPSL` — greatest selectivity among applied-to institutions;
- `F2PSACSL` — greatest selectivity among accepting institutions;
- `F2PS1SLC` — selectivity of first attended institution;
- `F3TZPS1SLC` — transcript-based selectivity of first known institution;
- `F3TZHIGHDEG` and documented degree recodes — later completion;
- application, acceptance, and attended-institution identifiers only if the approved design permits them and they add information beyond the selectivity categories.

These fields distinguish applying, being accepted, attending, and completing. They do not reconstruct the complete peer population inside the attended college.

### HSLS:09 additions

Request or confirm access to:

- `X1TXMTSCOR` — ninth-grade measured mathematics preparation;
- `X4CLGAPPNUM` and the documented application/acceptance measures;
- `X4PS1SELECT` and `X6PS1SLC` — first-institution selectivity at two follow-up horizons;
- `X6HIGHDEG` and/or `X6BACCRED` — completion through 2021;
- application, acceptance, and attendance identifiers or selectivity classifications when permitted.

HSLS is newer and has a longer modern follow-up. ELS currently provides the cleaner documented application-to-acceptance sequence. If access burden is equal, both should receive the same short candidate gate before choosing one.

## 6. What restricted access would and would not buy us

Restricted student-to-school linkage would permit the central high-school transition question:

> Among students with comparable prior measured preparation, how do high-school peer quality and the student's standing within that school relate to application, acceptance, selective-college attendance, and later completion?

It would not by itself permit a claim about congestion **inside the college**. ELS and HSLS sample students through high schools; they do not observe complete entering classes at each college. A college identifier may show destination, but a few sampled students at the same college are not the college's full competition pool.

## 7. Current decision

1. Keep the recovered NELS and HS&B public sources and finish their provenance-safe reconstruction only when needed for the immediate existing-data analysis.
2. Do not replace those usable peer-pool panels with ELS or HSLS public files.
3. Preserve ELS and HSLS locally and synchronize them through the existing `education` rsync scope.
4. Ask the licensed colleague the access question above before requesting or transferring any restricted records.
5. If restricted access is feasible, run the same qualification gate first and generate the mosaic only after the common school identifier and group sizes pass.
6. Keep Project Talent as a secondary option; do not open another acquisition branch unless ELS/HSLS access fails or Project Talent offers a clearly superior approved extract.

## 8. Synchronization and Git discipline

The dated `source_public_*` directories for all four education studies are ignored by Git. Small provenance READMEs, code, and audit summaries remain trackable.

From the Mac repository root:

```bash
DRY_RUN=1 ./scripts/pull_big_data.sh to-hpc education
./scripts/pull_big_data.sh to-hpc education
```

The first command previews the transfer. The second synchronizes `nels88/`, `hsb80/`, `els2002/`, and `hsls09/` to the Rivanna repository location. No rsync transfer was executed during this audit.

## Sources

- NCES DataLab Online Codebook: `https://nces.ed.gov/datalab/onlinecodebook/`
- ELS:2002 available data: `https://nces.ed.gov/surveys/els2002/avail_data.asp`
- HSLS:09 overview and available data: `https://nces.ed.gov/surveys/hsls09/`
- National Longitudinal Surveys data access: `https://nlsinfo.org/content/getting-started/accessing-data`
- Project Talent researcher data page: `https://www.air.org/project-talent/researchers`
- Project Talent public base-year collection: `https://www.icpsr.umich.edu/web/NACDA/studies/33341/`
