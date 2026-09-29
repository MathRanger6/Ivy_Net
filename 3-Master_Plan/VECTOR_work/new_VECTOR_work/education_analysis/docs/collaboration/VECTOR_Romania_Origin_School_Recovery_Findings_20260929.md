# Romania origin-school recovery — findings and stopping point

> **Superseding checkpoint — later September 29:** Read the [standalone archive feasibility report](VECTOR_Romania_Standalone_Ministry_Archive_Feasibility_20260929.md) before using the historical findings below. Linkage to the anonymous replication files is no longer a prerequisite. The new check recovered 2002 student tables, all six Alba 2001 candidate pages (2,982 positions), and an exact 78-student correspondence between candidate and placement reports within one explicitly coded origin school. The CNP headings below do **not** provide usable identifiers: inspected values are repeated placeholders. General admission rules recovered for 2001, 2002, and 2003 all specify 75% examination and 25% school grades; the paper's equal-weight description remains unresolved. National completeness is not established. The older inquiry and next-action recommendations below are historical; request a standalone de-identified source first, with a replication crosswalk optional.


**Date:** September 29, 2026  
**Status:** Bounded source recovery completed. Historical page fragments recovered; no exact link to the anonymous replication records demonstrated. No substantive experiment authorized or run.

## 1. What we found, in plain English

- **The original school information has not disappeared everywhere.** We recovered archived Ministry admissions pages for 2001 and 2003 that explicitly name students' schools of origin.
  - The inspected 2001 pages also preserve the national-exam average and school graduation average separately.
  - The inspected 2003 candidate page preserves the exam average, but does not display a separate graduation-average column.
- **We still cannot attach those school names to our anonymous replication rows reliably.** The public pages and the clean replication files do not supply a documented common student identifier.
  - Finding the original information is different from proving which anonymous row it belongs to.
  - No matching by score, town, destination, track, or combinations of those characteristics was attempted.
- **We have recovered examples, not a complete 2001–2003 dataset.** County coverage, pagination, admissions rounds, and complete peer populations remain unverified. The 2002 student tables were not recovered.
- **The next useful step is a short request to the authors.** An author-supplied de-identified extract or documented link could save a much larger archival reconstruction effort.

**Stopping classification:** The complete, reliably linked pre-high-school gymnasium design is **unavailable from current public data at this checkpoint**. This means unavailable for defensible execution with what we have recovered—not that every historical origin-school record is absent from the internet.

## 2. Why we pursued this narrow recovery

The [PD43 revision](Scholar_Romania_PreHS_Pool_HS_Selection_Collaboration_PD43_Revision_20260929.md) changes the proposed sequence to:

**Gymnasium experience → exam and school-grade performance → competition for high-school places → observed placement.**

That is distinct from the earlier high-school-to-Baccalaureate design we paused. The [narrow recovery request](Scholar_Romania_Origin_School_Recovery_Task_20260929.md) made actual origin-school recovery the immediate gate. The origin cannot be inferred from the destination.

First we checked what the authors originally possessed. Next we followed the historical admissions URLs and inspected surviving page structures. That recovered direct evidence that some required fields survive. It did not recover a documented connection to the anonymized research files, so we stopped before constructing peer groups or examining outcomes.

## 3. Candidate sources and their actual contents

### A. The existing public replication deposit

**Evidence:** Direct repository schema inspection and supplied README/code; [openICPSR deposit, version 1](https://www.openicpsr.org/openicpsr/project/112645/version/V1/view).

- **Years and level:** Clean files `data-AER-4.dta`, `data-AER-5.dta`, and `data-AER-6.dta` represent student records for 2001, 2002, and 2003.
- **Originating gymnasium:** Absent.
- **Separate exam score:** Absent.
- **Separate grades/GPA:** Absent.
- **Destination:** Anonymous high-school and school-track identifiers survive, along with town and cohort.
- **Identifiers:** The clean files contain `grade, bcg, bct, year, ua, us, us2, ct, survey`; no student ID. Other, expanded administrative files contain `sid2`, but the inspected documentation does not explain a public-source crosswalk or an identity-preserving construction recipe.
- **Linkage:** Origin recovery is impossible from these fields alone. No exact link to the archived public records is demonstrated. A custodian-supplied augmented file or documented mapping could change that.
- **Use:** The downloaded license assigns Creative Commons Attribution 4.0 to data and related non-code material, with a separate modified BSD code license. Preserve attribution. That license does not establish rights to reuse independently recovered Ministry records.

Local evidence: [schema gate report](../source_audit/EDUCATION_20260928_Romania_public_schema_gate_report.md), [variable inventory](../../outputs/romania_schema_audit_20260928/variable_inventory.csv), and the original files under `datasets/romania/source_public_openicpsr_20260928/extracted/data/`. The README and supplied analysis scripts begin with the released files; they do not provide the missing raw-admissions-to-release mapping.

### B. Recovered 2003 Ministry candidate table — Alba county

**Evidence:** Directly retrieved archived HTML, including column headings and source links.

- **Original address:** `http://admitere.edu.ro/static/j/AB/cin/`.
- **Verified archived page:** [August 18, 2003 capture](https://web.archive.org/web/20030818012508/http://admitere.edu.ro/static/j/AB/cin/).
- **Year and level:** 2003 admissions; individual candidates. One page inspected. The page declares 154 pages; the remaining pages were not retrieved or verified.
- **Originating gymnasium:** Yes—explicit column `Şcoala de provenienţă`, with source-native school links.
- **Separate exam score:** Yes—`Media de la capacitate`; Romanian-language and mathematics marks also have columns.
- **Separate grades/GPA:** Not in the inspected table's headings. Absence here does not establish absence from all 2003 source files.
- **Destination:** Yes—allocated high school and specialization.
- **Identifiers:** Candidate name, origin county, school links/codes, destination school/track links/codes, and display index. The display index is not established as a persistent student identifier.
- **Linkage:** A future author/custodian mapping is plausible; an exact mapping to released `sid2`, `us`, or `us2` is currently unavailable. Similar numeric codes or matching scores do not establish identity.
- **Use:** Limited source-feasibility inspection was performed. Reuse terms for these independently archived identifiable records were not established. Prefer a de-identified authorized extract; public visibility is not itself a complete reuse authorization.

**How we found it:** The [2003 homepage capture](https://web.archive.org/web/20030712062557/http://admitere.edu.ro:80/) used the site's root, rather than a modern-style `/2003/` directory. Its county menu led to Alba candidate and origin-school reports. This historical URL structure explains why checking only year-specific modern paths is insufficient.

### C. Recovered 2001 Ministry candidate and admitted-student tables — Alba county

**Evidence:** Directly retrieved archived table headings and the county report menu.

**Candidate table:** [August 16, 2002 capture of the 2001 admissions report](https://web.archive.org/web/20020816151117/http://www.edu.ro/adm2001/raport_candidati_total.asp-cj=AB&nj=ALBA&idx=1.htm).

- **Year and level:** 2001 admissions, student-level. The archive capture date is 2002; it is not the admission cohort.
- **Originating school:** A `Şcoală` column appears in the candidate table. The companion admitted-student report explicitly identifies the role as school of origin.
- **Separate exam score:** Yes—`Medie Capacitate`, plus Romanian-language and mathematics marks.
- **Separate grades/GPA:** Yes—`Medie Absolvire`, the school graduation average. A separately published component is therefore directly evidenced.
- **Destination:** Not in this candidate table's inspected headings.
- **Identifiers:** Name, row number, and a `CNP` column—the Romanian national personal identifier.

**Admitted-student table:** [August 16, 2002 capture](https://web.archive.org/web/20020816145842/http://www.edu.ro/adm2001/raport_admisi_per_judet.asp-cj=AB&nj=ALBA&idx=0.htm).

- **Originating gymnasium:** Explicit `Scoală de provenienţă`.
- **Destination:** `Liceu`, `Profil`, and `Specializare`.
- **Score:** Composite admission average; the separate components are in the candidate table above.
- **Identifiers:** Name, row number, and a CNP column also appear here.
- **Linkage:** A shared CNP field suggests a possible deterministic connection between these original tables if lawfully handled by a custodian and validated for uniqueness and coverage. No such join was attempted. It does not supply a link to anonymous replication rows, which do not expose that identifier.
- **Use:** CNP values were not extracted into the report or repository. A de-identified custodian-produced file is the appropriate practical route. No reuse license for the archived personal records was verified.

The [2001 admissions landing page](https://web.archive.org/web/20020802194942/http://www.edu.ro:80/adm2001/) distinguishes the main allocation and a second round. We did not establish full county, round, or page coverage. Separate pages surviving is not proof that an entire national cohort can be reconstructed.

### D. The 2002 admissions source — not recovered in this bounded check

**Evidence:** An exact historical link recovered from the 2003 Ministry homepage:

`http://www.portal.edu.ro/pls/portal30/url/page/ADLIC2002`

- **Year:** 2002.
- **Student level and requested fields:** Not directly verified; no candidate table recovered.
- **Identifiers and linkage:** Unknown. No exact link demonstrated.
- **Use:** No student records acquired from this route; reuse conditions unverified.
- **Limit:** A Wayback availability query returned no snapshot for the requested address/time. Another archive request was rate-limited. Neither result proves that every 2002 archive is missing.

We did not launch an exhaustive crawl or try to work around archive rate limits.

### E. Earlier papers, appendices, author pages, and the legacy data archive

**Evidence:** Documentary inspection; these sources establish provenance but did not yield a richer linked extract.

- [2008 paper version](https://pseweb.eu/ydepot/semin/texte0809/URQ2008CON.pdf), data section around page 7.
- [2011 working paper](https://www.columbia.edu/~cp2124/papers/Pop-Eleches_Urquiola_NBER.pdf), Section 4.1 and footnote 14.
- [Published 2013 paper](https://blogs.cuit.columbia.edu/msu2101/files/2019/08/Pop-Eleches_Urquiola2013.pdf), Section III.A and footnote 17.
- [AEA article and supplements](https://www.aeaweb.org/articles?id=10.1257/aer.103.4.1289); [online appendix](https://www.aeaweb.org/articles/materials/2176).
- [Pop-Eleches research page](https://www.columbia.edu/~cp2124/research.html) and [Urquiola papers page](https://blogs.cuit.columbia.edu/msu2101/papers/).

The paper versions describe original individual admissions records for 2001–2003 containing originating gymnasium and destination. The reported original matching to later Baccalaureate records used names and county, including fuzzy matching. That description is not a released student-key crosswalk and does not authorize us to reproduce identity matching.

Separate exam/GPA columns in a downloadable author extract were not recovered. The inspected appendix did not supply an origin-school crosswalk. The legacy AEA filename `20101433_data.zip` resolves through the DOI for the current openICPSR deposit, rather than establishing a distinct richer release. No additional raw-source archive was found on the inspected author pages or focused mirror searches.

**Linkage:** No new exact key. **Use:** Papers are provenance evidence; hypothetical unreleased author data require permission and documented terms.

## 4. A discrepancy to preserve: the 2003 admission-score formula

The paper describes equal weighting of examination performance and school grades. However, Article 4 of the [official methodology dated November 1, 2002, governing 2003 admissions](https://legislatie.just.ro/Public/DetaliiDocument/44477) specifies:

$$
T = \frac{3E+G}{4},
$$

with two decimals without rounding. Here $E$ denotes the national-exam average and $G$ the grades 5–8 graduation average. Article 15 describes storing these components separately.

This is an unresolved documentary discrepancy. Cohort-specific rules, amendments, and the authors' actual construction need confirmation. We have not established the corresponding 2001–2002 rules in this check. Do not reverse-engineer GPA from the composite under an assumed equal-weight formula; precision and truncation also matter.

The discrepancy does not by itself invalidate the published findings. It does prevent treating the equal-weight description in our earlier collaboration document as a verified rule for every cohort.

## 5. What recovering a field would—and would not—unlock

- **What it could unlock:** A documented origin-school identifier would let us begin assessing whether gymnasiums differ in the academic composition of their students. Separate exam and school-grade components would allow us to distinguish those measured performances.
- **What it would not automatically establish:** Full gymnasium rosters, applicant preferences, complete competitive pools, or causal congestion.
- **An additional coverage gate:** The students present in a published admissions report or the authors' analysis sample may exclude classmates who did not enter that process. We must establish the population before calling its school average the average of all gymnasium peers.
- **A timing qualification:** End-of-gymnasium examination performance precedes high-school selection, but follows gymnasium exposure. It is not a pre-gymnasium measure of innate ability.

No sorting index, peer average, selection curve, reconstructed identity, or substantive outcome model was calculated during this recovery.

## 6. Shortest direct-contact route

**First route: one concise inquiry to the authors.** They are most likely to know both the original extract and the anonymization used in the public deposit.

- Cristian Pop-Eleches: **cp2124@columbia.edu** — [official Columbia directory](https://cdep.sipa.columbia.edu/directory/cristian-pop-eleches).
- Miguel Urquiola: **msu2101@columbia.edu** — [official Columbia Economics profile](https://econ.columbia.edu/econpeople/miguel-urquiola/).

**Fallback:** Ask the Romanian Ministry registry to route a request for an authorized de-identified historical extract to the holder of the 2001–2003 admissions archive: **registratura@edu.gov.ro**, listed on the [official contact page](https://edu.ro/contact). This is a routing contact, not a verified promise that the data remain available.

The minimum useful delivery would include cohort, anonymous student ID, originating gymnasium, exam average, grades 5–8 average, composite score, and destination school/track, with field definitions and coverage. For linkage, request either an author-documented mapping to the public files or a self-contained augmented de-identified version of the same records. Do not assume row order is a key. Names and CNP are unnecessary.

### Suggested author email — draft only, not sent

**Subject:** De-identified origin-school fields for your Romania school-assignment data

Dear Professors Pop-Eleches and Urquiola,

I am investigating how students' peer environments relate to performance and subsequent selective educational placement. Your Romania study is particularly relevant.

I have the public replication files for “Going to a Better School.” The paper describes originating gymnasium in the original 2001–2003 admissions records, but that field and the separate exam and school-grade components do not appear in the clean deposited cohort files.

Do you retain a de-identified extract containing originating gymnasium, national-exam average, grades 5–8 average, composite admission score, and assigned high school/track? An augmented version of the released records, or a documented anonymous link to them, would be ideal. We do not need student names or national personal identifiers.

We found surviving Ministry archive pages with some of these fields, but no reliable mapping to the anonymous release. If sharing an extract is not possible, could you point us to an authorized historical source or the appropriate data custodian?

One clarification would also help: the paper describes equal exam/GPA weighting, while the published 2003 methodology specifies 75%/25%. Do you know which formula applies to each study cohort?

Thank you for any guidance, including access conditions or restrictions.

Charles Levine

## 7. Final disposition and audit trail

- **Completed:** Focused paper/supplement review, source-URL tracing, limited archive-page/header inspection, replication-schema reconciliation, and contact-route identification.
- **Not established:** Complete three-cohort recovery; exact raw-to-replication link; lawful terms for bulk reuse of archived named records; complete peer populations; a resolved cohort-specific score formula.
- **Stopped:** No bulk student scrape, source-data replacement, heuristic linkage, analysis pipeline change, or substantive experiment.
- **Files:** This report records URLs and schemas, not student identities. Original datasets and Scholar documents are unchanged.
- **Recommendation:** Use the unsent author inquiry as the next decision. Do not spend days reconstructing the archive before asking whether the small missing de-identified extract already exists.

