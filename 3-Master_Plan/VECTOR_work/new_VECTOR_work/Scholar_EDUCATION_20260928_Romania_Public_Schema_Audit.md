# Romania Public Replication Package — Schema Feasibility Audit

**Date:** 2026-09-28  
**Prepared by:** Original VECTOR / Scholar GPT  
**For:** Charles Levine and new VECTOR  
**Status:** Public-web audit complete to the ICPSR authentication boundary. No data were downloaded or analyzed.

## Executive judgment

**Romania remains a serious public-data candidate, but it has not yet passed the peer-pool gate.**

The public evidence now establishes that the openICPSR replication archive contains eight Stata `.dta` files, including three large microdata files. Independent reproducibility work using the deposited `data-AER-1.dta` confirms that this file contains student-level identifiers, transition score, cutoff information, a better-school treatment indicator, and Baccalaureate exam score.

The original Pop-Eleches–Urquiola paper establishes that the authors' underlying 2001–2007 administrative admissions data contain each student's transition score and allocated school/track, and that the 2001–2003 cohorts are linked to Baccalaureate participation and grade.

**What remains unverified is the decisive variable question:** whether the public deposited `.dta` files retain stable assigned-school and assigned-track identifiers that allow students to be reconstructed into school/track/cohort peer pools.

The current openICPSR interface requires authentication before downloading the `.dta` files. Original VECTOR cannot cross that authenticated download boundary from the present web environment.

Therefore:

> **Do not reject Romania, and do not yet declare it usable. One authenticated schema inspection is required.**

If school/track/cohort identifiers coexist with transition score and Baccalaureate outcomes in the public files, the public-data search should stop and Romania should move to a bounded analysis-design phase.

---

## 1. Public archive — verified

The openICPSR project is:

**Pop-Eleches & Urquiola, “Going to a Better School: Effects and Behavioral Responses”**  
Project DOI: `10.3886/E112645V1`

The public archive lists:

- `data-AER-1.dta` — ~314.3 MB
- `data-AER-2.dta` — ~123.2 MB
- `data-AER-3.dta` — ~429.8 MB
- `data-AER-4.dta` — ~4.8 MB
- `data-AER-5.dta` — ~5 MB
- `data-AER-6.dta` — ~5.2 MB
- `data-AER-7.dta` — ~4.4 MB
- `data-AER-8.dta` — ~642 KB
- three Stata `.do` files
- README in DOCX and PDF formats

This is therefore a real public replication-data deposit, not a code-only archive.

**Project:**  
https://www.openicpsr.org/openicpsr/project/112645/version/V1/view

---

## 2. What `data-AER-1.dta` is known to contain

A later public reproducibility/methodological project explicitly uses the original deposited `data-AER-1.dta` and provides preprocessing code.

That code describes `data-AER-1.dta` as:

> “2001–2003 cohort administrative data (multiples by school-cutoff)”

It reconstructs:

- `Students` — student ID
- `Towns` — town ID
- `W` — transition score
- `C` — admission cutoff
- `D` — indicator for entering the school above the cutoff / better school
- `Y` — Baccalaureate exam score

The preprocessing code also demonstrates that the raw replication file contains duplicated student observations associated with school cutoffs and explicitly deduplicates by student ID for its own RD application.

This is important for our audit:

1. The public file is genuinely individual-level.
2. Student identity survives.
3. Prior transition performance survives.
4. Baccalaureate performance survives.
5. Admission/cutoff structure survives.
6. The file is **not** simply a clean one-row-per-student panel; the replication representation must be understood before using it for peer-pool construction.

Public reproducibility repository:

https://github.com/youjin1207/IVs_inMultiRD

Relevant preprocessing source:

`Code/preprocess.R`

---

## 3. What the original paper establishes about the source administrative data

The original AER paper states that the administrative admissions data cover the 2001–2003 and 2005–2007 admission cohorts and provide, for all students:

- student name;
- originating gymnasium;
- transition score;
- allocated school/track.

For the 2001–2003 cohorts, admissions records were linked to:

- whether the student took the Baccalaureate exam;
- Baccalaureate exam performance.

The paper's Figure 1 explicitly uses:

- average transition score of peers encountered at school;
- Baccalaureate taken;
- Baccalaureate grade.

Thus the published research confirms that the authors had sufficient information to construct school-level peer quality and link it to later outcomes.

The paper also conducts school- and track-level cutoff analyses and clusters some analyses at school-cohort and school-track-cohort levels, confirming that school/track/cohort structures existed in the analytical source data.

**AER paper:**  
https://pubs.aeaweb.org/doi/10.1257/aer.103.4.1289

---

## 4. The decisive unresolved question

The existence of school/track identifiers in the authors' confidential/source administrative data does **not** prove that those identifiers were retained in the deposited public replication files.

The later reproducibility project exposes student ID, town ID, transition score, cutoff, treatment/better-school status, and Baccalaureate score, but its public data dictionary does not identify an assigned-school or assigned-track variable.

That omission may mean one of several things:

1. school/track identifiers exist in `data-AER-1.dta` but were unnecessary for the later project's preprocessing;
2. they exist under encoded variable names not documented by that later project;
3. the public AER replication data transformed the source records into cutoff-relative observations and removed direct school/track identity;
4. another one of `data-AER-2.dta` through `data-AER-8.dta` contains the identifiers needed for school/track peer pools.

The web evidence does not adjudicate among these possibilities.

---

## 5. Authentication boundary

The openICPSR archive is publicly listed, but the current download route redirects to ICPSR authentication before serving files.

Original VECTOR's web environment cannot authenticate into that account flow.

This is **not** a restricted-use application problem. It is a normal authenticated public-download interface.

Therefore the remaining gate should be easy for Charles/new VECTOR to resolve locally:

1. Log into ICPSR/openICPSR.
2. Download the README and, ideally, inspect `data-AER-1.dta` first.
3. Do not run substantive analysis.
4. Report the schema only.

---

## 6. Exact schema inspection requested from new VECTOR

After Charles downloads the public file(s) into the education workspace, perform a read-only/schema-only inspection.

For each `.dta`, report:

- row count;
- column count;
- variable names;
- Stata variable labels;
- whether each of the following exists directly or can be unambiguously decoded:

### Required
- stable student ID;
- admission cohort/year;
- transition score;
- assigned school ID;
- assigned academic track ID;
- Baccalaureate taken;
- Baccalaureate grade.

### Strongly desirable
- town ID;
- school/track admission cutoff;
- track capacity;
- school capacity;
- peer-quality variable already used by authors;
- indicators allowing one-row-per-student reconstruction;
- variables identifying which cutoff-expanded rows correspond to the student's realized assignment.

Do not fit models or generate HERO curves during this inspection.

---

## 7. Pass/fail rule

### PASS — stop searching

Romania passes the immediate public-data gate if the public deposit allows construction of a unique student-level table containing:

- student ID;
- cohort;
- transition score;
- assigned school and/or assigned track;
- later Baccalaureate outcome.

If **track** survives, prefer testing `cohort × school × track` as the first candidate peer pool because tracks are institutionally meaningful instructional groups.

If only **school** survives, school × cohort remains scientifically useful.

A PASS moves Romania to a bounded analysis-specification stage. It does **not** authorize analysis automatically.

### PARTIAL PASS

If the deposit contains student ID, transition score, cutoff/better-school treatment, and Baccalaureate outcome but no stable school/track identity, Romania remains valuable for RD/relative-position work but **cannot support our common LOO peer-pool experiment from the public files alone**.

At that point, assess whether another deposited file restores pool identity before moving to Chicago.

### FAIL

If no public deposited file preserves a reconstructable peer-group identifier, perform the bounded Chicago access audit, then Kenya if needed.

---

## 8. What Romania can answer if it passes

A successful public schema would support:

**Own prior performance**  
Student transition score before high-school assignment.

**Peer environment**  
LOO mean transition score among assigned school/track peers.

**Sorting**  
Realized `H_sort` using transition score and assigned pool.

**Later outcome**  
Baccalaureate participation and/or Baccalaureate grade.

**Selection intensity / selectivity**  
Admission cutoff or cutoff percentile; use K/N only if a defensible risk set can actually be constructed.

**Identification layer**  
Near-cutoff RD comparisons of students with similar prior scores who gain access to different school environments.

The descriptive peer-environment analysis and RD analysis are separate estimands and must remain separate.

---

## 9. Important conceptual caution

Romania contains real congestion/scarcity in **entry into school/track environments**.

It does not automatically contain a fixed-K downstream distinction among students after they enter those environments.

Therefore Romania would be:

- a strong assignment/sorting/peer-environment domain;
- a strong relative-position domain;
- a strong quasi-experimental environment-effect domain;

but not automatically a direct institutional analog of Army top-block rationing or NBA draft selection.

That limitation is scientifically useful and should be preserved rather than hidden.

---

## 10. Message to new VECTOR

Original VECTOR has completed the public-web portion of the Romania schema audit.

**Finding:** Romania remains promising, but the web evidence cannot verify that stable assigned-school/track identifiers survive in the public replication `.dta` files.

The openICPSR download requires normal account authentication, which Original VECTOR cannot perform from the present environment.

Please do **not** duplicate the external literature search.

Once Charles obtains the public replication file(s), perform only the schema inspection described above. Do not fit substantive models until Charles reviews the pass/fail result.

Until then:

- preserve NELS:88 and HS&B:80 work;
- do not invest in restricted-use acquisition;
- do not begin Chicago/Kenya unless Romania fails the peer-pool gate.

---

## Current conclusion

**Romania has passed the conceptual, public-availability, prior-performance, later-outcome, and identification gates.**

It has **not yet passed the peer-pool identifier gate**.

One authenticated public-file schema inspection will decide whether Romania becomes the immediate education candidate.
