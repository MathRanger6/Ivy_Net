# Romania Ministry archive: can it stand alone?
## Bounded feasibility findings — September 29, 2026

**Decision in plain English:** Yes, the recovered 2001 records justify treating the Ministry archive as a possible independent dataset. We no longer require a connection to the anonymous American Economic Review (AER) replication files. The follow-on Alba audit recovered reports for all 168 source-directory origin-school codes. This passes the archive-retrieval and report-correspondence gate; it does not establish a complete population of every eighth-grade classmate.

**Strongest evidence:** All six candidate pages in the inspected Alba county report family survive, containing 2,982 displayed records. All 168 school-specific candidate reports listed in the Ministry's Alba origin-school directory were recovered. Across the name correspondences that can be compared directly, the admission composite, examination score, and school-grade average have zero disagreements. Forty-four school reports add 78 applicant occurrences absent from their Alba county-labelled groups; companion placement reports locate all 78. This demonstrates that school reports recover genuine cross-county placements that a county-only construction would omit.

**What remains uncertain:** These reports describe participating applicants associated with an originating gymnasium. They do not prove that every eighth-grade graduate or every student following another admissions route is present. Two source codes also share the same printed Căpâlna school label and must remain code-distinguished. National archive completeness, geographic consistency, and permission for broader reuse are not established. No substantive experiment has run.

### Completion addendum — Alba 2001 structural audit

The resumable audit completed on its second pass with **168 of 168 directory codes recovered and zero unresolved addresses**. The school reports contain 3,041 row occurrences before any cross-report deduplication. That number must not be called 3,041 unique students, because source reports can overlap and same-name schools require code-level treatment.

For 2,963 directly comparable name occurrences, the school-specific and county reports agree on the admission composite, national examination average, and grades 5–8 average in every case. The 78 additional applicant occurrences span 44 origin-school reports. Every additional occurrence was found in the corresponding placement report; none was silently treated as missing. The largest difference occurs for source code 149, whose school report contains 13 applicants while only four appear under its Alba county label, leaving nine placements recovered through the school-specific view.

The only apparent county-to-school omissions occur under the duplicated printed label `SCOALA GENERALA CLASELE I - VIII CAPILNA`, which is represented by source codes 189 and 226. This is a source-identity issue to preserve, not evidence that those printed names disappeared from the archive.

Direct outputs: [final summary](../../outputs/romania_alba_2001_structural_audit_20260929/origin_report_check_summary.json), [empty unresolved queue](../../outputs/romania_alba_2001_structural_audit_20260929/unresolved_addresses.json), and [append-only school checkpoints](../../outputs/romania_alba_2001_structural_audit_20260929/origin_report_checks.jsonl). These outputs contain aggregate diagnostics rather than student names.

This report supersedes the earlier [origin-school recovery checkpoint](VECTOR_Romania_Origin_School_Recovery_Findings_20260929.md), specifically its replication-linkage gate, its failure to recover 2002 tables, and its suggestion that a CNP heading might provide a usable identifier. Scholar's documents remain unchanged.

## 1. Why the task changed

First we searched for originating gymnasium because it is absent from the released replication files. That made linkage to those files appear essential.

Scholar then identified the simpler route: our revised PD43 question ends at high-school/track assignment. If the Ministry's own records contain the necessary fields, we can examine that transition without importing the later Baccalaureate outcomes.

Accordingly, this check asked whether the Ministry reports can support a standalone cohort. It did not calculate sorting, estimate congestion, compare schools' outcomes, or search for a favorable empirical result.

The intended sequence remains:

\[
\text{gymnasium experience}
\longrightarrow (E_i,G_i)
\longrightarrow T_i
\longrightarrow \text{observed high-school/track placement}.
\]

Here \(E_i\) is the national examination average, \(G_i\) the grades 5–8 average, and \(T_i\) the admission composite. Both components are measured after substantial gymnasium exposure. The examination is more standardized; it is not a pre-gymnasium measure of untouched ability.

## 2. What survives, year by year

### 2001: strongest standalone prospect

**Candidate-report coverage.** Six Alba pages contain successive displayed positions 1–2,982, with page counts 500, 500, 500, 500, 500, and 482. They contain origin-school labels, examination averages, graduation averages, admission averages, and subject marks.

**Placement-report coverage.** Six companion admitted-student pages contain 2,977 positions; a separate unassigned report contains five. These counts agree with the corresponding county allocation totals. They are overlapping views of the candidate population, not another 2,982 students to add.

This establishes coverage of the inspected report family. It does not establish that every Alba gymnasium graduate, every applicant in another round, or every student crossing a county boundary appears there.

**A usable connection demonstrated locally.** The source directory provides explicit originating-school codes and links to reports for each school. For the 2001 Alba school identified by source code 101, the candidate report and the placement report each contain 78 rows. All 78 printed names are unique within each report and match exactly across them. Their admission composites agree in all 78 cases.

The match used the same explicitly coded origin school and cohort, then exact printed-name agreement. Scores were an independent check, not a matching key. No approximate name matching, inferred origin, or score/town/destination reconstruction was used. This is a local feasibility demonstration; exact names are not established as persistent or nationally unique identifiers.

**Important correction about identifiers.** The column headed CNP contains a repeated nonnumeric placeholder in the inspected reports. It cannot identify students. The initial key diagnostic exposed this problem; any attempted CNP-based linkage statistics were rejected. The valid 78-student check is a separate exact-text comparison. Names and personal identifiers have not been saved in the repository audit outputs.

**Geography and codes.** The recovered Alba origin-school directory contains 168 entries with school codes, registration-center codes, school names, addresses, and urban/rural labels. Destination specialization and occupancy reports contain 85 entries with destination descriptions and capacity information. These are promising geographic and capacity sources. A nationally consistent town/market mapping has not been constructed.

**Beyond Alba.** First candidate pages for Cluj and Iași each yielded 500 rows. Thus 3,982 displayed candidate positions were inspected across these county report families. This is a retrieval count, not a validated national count of distinct people. The 78-student school check is inside Alba and must not be added again.

Sources: [Alba candidate page](https://web.archive.org/web/20020816151117/http://www.edu.ro/adm2001/raport_candidati_total.asp-cj=AB&nj=ALBA&idx=1.htm), [admitted students](https://web.archive.org/web/20020816145842/http://www.edu.ro/adm2001/raport_admisi_per_judet.asp-cj=AB&nj=ALBA&idx=0.htm), [origin-school directory](https://web.archive.org/web/20020624015545/http://www.edu.ro/adm2001/raport_scoli_din_judet.asp-cj=AB&nj=ALBA&idx=0.htm), [county allocation totals](https://web.archive.org/web/20020620020159/http://www.edu.ro/adm2001/statistici/situatie_repartizare_pe_judet.htm). Exact page addresses, capture dates, hashes, and counts are preserved in the [sanitized audit record](../../outputs/romania_archive_feasibility_20260929/verified_2001_audit_metadata.json).

### 2002: student tables recovered, but components still missing

Following the old portal's redirects and county image-map links recovered actual 2002 student tables. This corrects the earlier report's unsuccessful recovery.

The inspected tables contain origin county, originating school, admission composite, admitted/rejected status, destination school, specialization code, specialization, instructional level, attendance format, and language. They do **not** separately display the examination average and grades 5–8 average.

Two Alba pages yielded positions 1–100; one Cluj page yielded positions 1–50. That is 150 displayed records inspected. The county summary gives 3,318 Alba candidates, but the expected terminal page was not recovered through the tested address. We have not established complete county or national coverage.

Origin-school labels survive; a stable coded origin-school-to-town connection has not been validated in these inspected views. No missing grade component was algebraically reconstructed.

Sources: [national report index](https://web.archive.org/web/20020802231703/http://www.portal.edu.ro/adlic/reports/rapoarte/common/index.htm), [Alba first page](https://web.archive.org/web/20021002102651/http://www.portal.edu.ro/adlic/reports/rapoarte/raport_numeAB0.html), [Alba second page](https://web.archive.org/web/20021018204807/http://www.portal.edu.ro/adlic/reports/rapoarte/raport_numeAB1.html), [Cluj first page](https://web.archive.org/web/20021016004309/http://www.portal.edu.ro/adlic/reports/rapoarte/raport_numeCJ0.html), [national totals](https://web.archive.org/web/20020802224521/http://www.portal.edu.ro/adlic/reports/raport_situatie_judete.html).

### 2003: useful fields, serious paging uncertainty

The inspected Alba candidate page contains 20 records with originating school, examination average, admission composite, and destination school/track. It does not separately display the grades 5–8 average.

The site declares 154 pages for Alba. Its original navigation script confirms the later-page filename pattern. Tested pages 2, 77, and 154 returned archive errors rather than recovered tables. A tested live historical mirror timed out. These failures demonstrate a retrieval gap in this check, not proof that no alternate snapshot exists.

An origin-specific school report also survives with seven rows, but it may overlap the candidate page; those rows are not added to the verified count of 20. Origin and destination directories survive in part. Their complete geographic coverage has not been verified.

Sources: [Alba candidate page](https://web.archive.org/web/20030818012508/http://admitere.edu.ro/static/j/AB/cin/), [origin directory](https://web.archive.org/web/20030804024828/http://admitere.edu.ro/static/j/AB/sc/), [origin-specific report](https://web.archive.org/web/20030818015153/http://admitere.edu.ro/static/j/AB/sc/c/101/), [navigation script](https://web.archive.org/web/20030801230809/http://admitere.edu.ro/scripts/f.js).

## 3. Recoverable counts versus published cohort counts

**2001:** A Ministry account reports 183,475 registrations for computerized allocation. We inspected 3,982 displayed candidate positions, including the complete 2,982-position Alba candidate report family. We have not estimated how many national records could ultimately be recovered. [Ministry account](https://web.archive.org/web/20020803160934/http://www.edu.ro/adm2001/2001-10-23-ADLIC-rom.htm)

**2002:** The recovered national summary reports 196,109 registered, 191,546 admitted, and 4,563 unassigned. Our directly inspected candidate pages contain 150 positions. The summary is dated July 16; second-round reports must be kept separate. [Official summary](https://web.archive.org/web/20020802224521/http://www.portal.edu.ro/adlic/reports/raport_situatie_judete.html)

**2003:** Summing the 42 county rows in the recovered official table gives 187,100 registered, 185,632 placed, and 1,468 unplaced. These are this table's totals, not a newly established complete final-year population. The precise allocation-round coverage still needs confirmation. Twenty candidate positions were directly inspected without adding potentially overlapping school reports. [Official county table](https://web.archive.org/web/20040530093215/http://admitere.edu.ro/static/n/llt/)

These registration totals are not counts of all young people, all gymnasium graduates, or all classmates.

The paper's Table 1 instead reports analysis samples of 107,812, 110,912, and 115,413 for 2001–2003. Those are not the correct national archive-recovery targets. The released 334,137-row sample and a national admissions population are different universes. The paper also treats town as an approximate local schooling market; a county code alone cannot reproduce that definition. [Published paper, Table 1 and accompanying discussion](https://www.columbia.edu/~cp2124/papers/Pop-Eleches_Urquiola(2013).pdf)

**Bottom line for feasibility:** No complete national cohort has yet been verified. Reporting that fact is more defensible than projecting a national recovery count from a few surviving pages.

## 4. The weighting question, checked separately for each year

For the general admission route, the recovered official rules specify:

\[
T_i^{*}=0.75E_i+0.25G_i,
\qquad
T_i=\frac{\lfloor100T_i^{*}\rfloor}{100}.
\]

The second expression represents keeping two decimal places without rounding for these positive grades. Special vocational or aptitude-test routes require their own rules; the general formula must not be applied indiscriminately.

### 2001

Order 4421 of August 31, 2000, Annex I, Article 13 specifies 75% examination and 25% school grades, with two decimals without rounding. The archived document contains historical enrollment-procedure language and an inconsistent annex year label, so it should not alone establish the final computerized allocation procedure. For the **weighting**, we also checked the actual Alba data: all 2,982 inspected candidate rows equal the truncated 75/25 calculation. Only five also equal the truncated 50/50 calculation. [Archived Ministry rule](https://web.archive.org/web/20010426190700/http://www.edu.ro/radm2001.htm)

### 2002

Order 4899 of October 31, 2001, Annex I, Article 4, for 2002–2003 specifies 75/25 and two decimals without rounding. The inspected 2002 student tables lack the separate components, so an individual-row arithmetic check was not possible. [Archived Ministry methodology](https://web.archive.org/web/20020819231531/http://www.edu.ro/anxom4899.htm)

### 2003

The methodology associated with Order 4857 of November 1, 2002, Article 4, for 2003–2004 specifies 75/25 and two decimals without rounding. The inspected 2003 candidate view does not supply the separate school-grade component needed for a direct arithmetic check. [Official legislation record](https://legislatie.just.ro/Public/DetaliiDocument/44477)

**Interpretation:** Checking cohorts was the correct first step. However, the recovered general rules do not support a change from 50/50 to 75/25 between these three years. The paper's equal-weight description remains a documentary discrepancy; it is not explained by such a change in the rules inspected here. We should ask the authors for clarification before asserting why their description differs. This finding alone does not establish that their empirical results are invalid.

## 5. What could bias a reconstructed gymnasium pool?

**Missing pages may omit a systematic slice of students.** Alphabetical or score-ordered pages are not random samples. A surviving first page cannot represent an entire school or county.

**A complete admissions report may still be an incomplete gymnasium cohort.** Students who did not enter that allocation round, failed an eligibility requirement, followed another route, or applied across county boundaries could be absent. We must name the population honestly: participating applicants unless full graduating-cohort coverage is established.

**Two reports can count the same students.** Candidate, admitted, unassigned, and school-specific pages must be reconciled rather than stacked. Archive captures of different dates may duplicate or revise the same report.

**School codes require year and county context.** A number such as 101 must not be assumed to represent the same school across years. Use source-native year/county/school identifiers first. Directory addresses can help map location, but a national town key and a defensible competitive market remain unverified.

**Exact names can still fail at scale.** The 78-student check had no duplicate names within the coded school. A larger reconstruction must detect duplicate names and conflicting records and leave ambiguous cases unresolved. Silently discarding them could change the apparent peer pool.

**Placement is observed; a success definition is not yet chosen.** High-school/track allocation is a real capacity-constrained event. Treating a specific placement as a scarce distinction still requires a defensible opportunity and its relevant competitors. Overall placement rates are not automatically the selection intensity \(K/N\) for a desirable school or track.

These issues are feasibility conditions, not evidence for or against congestion.

## 6. Completed gate and next decision

**Concentrate on 2001 and keep the replication crosswalk secondary.** It is the only inspected year with both score components and a demonstrated county-wide origin-to-placement architecture.

The bounded Alba 2001 construction-and-completeness audit is now complete. It shows that candidate and destination information can be connected across all 168 source-directory origin-school codes and that school-specific reports repair cross-county truncation in the Alba-labelled county list. The defensible population is still **participating applicants associated with each coded gymnasium**, not every classmate or gymnasium graduate.

The next decision is scientific rather than archival: define the precise applicant population, the high-school/track opportunity being treated as scarce, its relevant competitors and capacity, and the interpretation of the two post-gymnasium score components. Only after that specification is agreed should any sorting, congestion, or selection calculation run.

If archival reconstruction becomes disproportionate, the shortest request is to the paper's authors for a **de-identified original admissions extract**, with year, origin-school code, exam component, grades 5–8 component, destination school/track, allocation round, and geography. Ask for documentation of coverage and the 75/25 versus equal-weight description. A link to their anonymous replication files is optional unless we later need a variable that the admissions source lacks.

No inquiry has been sent. Broader reuse terms for the archived individual records remain unverified; the replication deposit's license cannot automatically be transferred to Ministry pages.

## 7. What actually ran, and where this stops

Python in the existing sports_net environment retrieved and inspected a bounded set of public archival pages. It checked headings, page positions and counts, identifier usability, score arithmetic, and one school-specific exact-text correspondence. No outcome model, simulation, sorting estimate, figure, or substantive experiment ran.

The saved [audit metadata](../../outputs/romania_archive_feasibility_20260929/verified_2001_audit_metadata.json) contain source URLs, hashes, counts, and diagnostics, not student names or raw personal records. The unusable CNP-based join output is explicitly excluded. Original data, replication code, and Scholar documents are unchanged.

**Current stopping point:** The complete Alba source-directory report family is recoverable for 2001, and its internal score and placement correspondence passes this structural audit. Full graduating-cohort coverage, national completeness, and the substantive estimand are not established. Any sorting, congestion, or selection analysis requires a new explicit execution decision.
