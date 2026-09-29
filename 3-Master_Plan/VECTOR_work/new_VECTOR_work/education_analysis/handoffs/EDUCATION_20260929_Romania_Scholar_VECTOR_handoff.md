# Romania education data: handoff to Scholar VECTOR

**Date:** 2026-09-29  
**Purpose:** Transfer the verified schema findings, variable interpretation, code relationships, scientific assessment, and postsecondary-data boundary from the public replication archive for Pop-Eleches and Urquiola, *Going to a Better School: Effects and Behavioral Responses*.

## 1. Source and inspection status

The source is the complete public openICPSR replication archive, project 112645, version 1.

- Project page: <https://www.openicpsr.org/openicpsr/project/112645/version/V1/view>
- Article: <https://doi.org/10.1257/aer.103.4.1289>
- Downloaded archive: `Romania_112645-V1.zip`
- Archive SHA-256: `00744e3b266f0d8a7ea3578dca733758f523fb62a5143a6216de523aa979b99b`
- ZIP integrity: passed
- Contents: eight Stata datasets, three deposited Stata programs, README files, and a license.

The original `.dta` files are deliberately excluded from this compact handoff ZIP. They occupy approximately 928 MB uncompressed and are not needed to review the schema conclusions. Complete file hashes, dimensions, and variable metadata are included in the machine-readable inventories.

## 2. Eight-file inventory

| File | Rows | Variables | Best current interpretation | Principal use in deposited code |
|---|---:|---:|---|---|
| `data-AER-1.dta` | 3,621,905 | 19 | Cutoff-expanded administrative analysis file. Students appear repeatedly across relevant admission cutoffs. Contains cutoff distance, access/treatment measures, school-quality measures, Baccalaureate outcomes, composite town/cohort/cutoff grouping, and an anonymous student identifier. | Figures 1–3 and Tables 1, 3–5, with other files used for particular table components. This is the main regression-discontinuity file. |
| `data-AER-2.dta` | 3,313,386 | 7 | Reduced cutoff-expanded file containing the school-quality outcome and regression-discontinuity variables. | Used in Table 3 specifications concerning school-level quality. |
| `data-AER-3.dta` | 8,836,005 | 9 | Alternative cutoff-expanded administrative file containing a track-related school-quality measure, Baccalaureate outcomes, and regression-discontinuity variables. | Used in Tables 3–5 for alternative school/track-quality and Baccalaureate specifications. |
| `data-AER-4.dta` | 107,812 | 9 | Clean student-level administrative file for the 2001 admission cohort. One anonymous student record per row. | Table 1 sample and institutional summaries. Best file for ordinary peer-pool construction in 2001. |
| `data-AER-5.dta` | 110,912 | 9 | Clean student-level administrative file for the 2002 admission cohort. | Same role for 2002. |
| `data-AER-6.dta` | 115,413 | 9 | Clean student-level administrative file for the 2003 admission cohort. | Same role for 2003. |
| `data-AER-7.dta` | 11,931 | 95 | Survey-enriched cutoff analysis file. Contains family background, perceived school quality, parental effort, tutoring, homework, perceived peer rank/behavior, and teacher experience/certification measures. | Figure 4 and Tables 2, 6–8, and 10. |
| `data-AER-8.dta` | 5,770 | 26 | Smaller classroom-focused survey analysis file with student- and classroom-level behavioral measures and classroom peer quality. | Table 9. |

### Important grain distinction

Files 1–3 are expanded around admission cutoffs. Their millions of rows are not millions of distinct students. They are appropriate for the published regression-discontinuity design but not for counting ordinary school-track peer groups without reconstructing the expansion.

Files 4–6 are the cleanest inputs for our descriptive peer-environment analysis. Together they contain 334,137 student rows across the 2001–2003 cohorts.

Files 7–8 contain the authors' survey material and behavioral-response measures. They are valuable for mechanism interpretation, but their much smaller samples and specialized grains must not be silently combined with the full administrative peer-pool analysis.

## 3. Variable map

Many administrative variables have no attached Stata labels. The mappings below come from the published paper, the deposited code, and structural checks. Interpretations marked **direct** are clear from the clean files and code; interpretations marked **derived/code-based** depend on the authors' naming and use in the deposited programs.

### Student identity

- `sid2` — anonymous student identifier in files 1–3, 7, and 8 (**direct from code use**, including clustering at the student level).
- Files 4–6 do not contain `sid2`. Each is already one administrative student record per row. A reproducible row identifier is sufficient for within-file leave-one-out peer calculations, but it is not a key for external person-level linkage.
- `ct` — observation counter equal to one in files 4–6; the authors sum it to count students.

### Prior performance and cohort

- `grade` — pre-assignment transition score in files 4–6 (**direct**). It is complete for all 334,137 student rows.
- `year` — admission cohort in files 4–6 (**direct**): 2001, 2002, or 2003.
- `Y` — cohort/year term in expanded files (**code-based**).
- `z`, `zga`, `zg` — score/cutoff-level quantities in expanded or survey files (**code-based; exact formulas should be taken from the article before reuse**).

### Town, school, track, and classroom

- `ua` — town identifier in files 4–6 (**direct from nesting and code**).
- `us` — school identifier in files 4–6 (**direct from nesting and code**).
- `us2` — school-track identifier in files 4–6 (**direct from nesting and code**).
- `uazY` — composite regression-discontinuity fixed-effect group involving town, cutoff/score, and cohort in expanded files (**code-based**).
- `usY`, `us2BY`, `usYprspB`, and `usYclass` — composite school, track, program, cohort, or classroom grouping identifiers used for clustering or absorbed effects in the survey programs (**code-based; preserve rather than rename until fully reconstructed**).
- `agus` — average transition score at the assigned school or school-quality level used by the authors (**paper/code-based**).
- `agus2`, `agus2B` — track-related or alternative school-quality averages (**paper/code-based; exact construction needs provenance before new use**).
- `agus_class` — classroom average transition score in file 8 (**paper/code-based**).

The clean-file nesting check passed without exception: every `us2` maps to one `us` and one `ua`, and every `us` maps to one `ua` within the deposited cohorts.

### Admission cutoff and access

- `dzag` — signed transition-score distance from an admission cutoff (**direct from figure axes and code**).
- `dga` — indicator for gaining access at the cutoff / being on the admission side of the threshold (**paper/code-based**).
- `dzag_after` — post-cutoff slope term used in the regression-discontinuity specification (**code-based**).
- `dzagr01`, `dzgr01`, `dzagr05` — rounded/binned versions of cutoff distance used for figures (**code-based**).
- `better` — indicator connected to access to a better school in file 1 (**paper/code-based**).
- `prsp` and related composite identifiers — program/preference/cutoff grouping terms (**not yet sufficiently reconstructed for a new estimand**).

The public deposit preserves genuine threshold-based admission variation. It does not preserve a complete ranked applicant-choice set that would define one unambiguous competing population \(N\) for every school-track opening. Therefore, cutoff position or cutoff percentile is the defensible first measure of selectivity. Realized enrollment is not automatically an official capacity \(K\), and a simple \(K/N\) must not be manufactured.

### Baccalaureate and later observed outcomes

- `bct` — indicator that the student took the Baccalaureate examination (**direct**).
- `bcg` — Baccalaureate examination grade (**direct**).

Across files 4–6:

- 275,719 of 334,137 students are coded as taking the examination;
- 58,418 are coded as not taking it;
- 257,433 takers have an observed grade;
- 18,286 takers have a missing grade; and
- no non-taker has a recorded Baccalaureate grade.

These should remain two outcomes: examination participation, followed by examination grade among takers with observed grades. Combining them into one invented success score would obscure two different processes.

### Behavioral and mechanism variables

Files 7–8 contain measures concerning tutoring, homework, parental effort, perceived class rank, peer behavior, school reputation and quality, teacher experience, teacher certification/didactic rank, demographics, household resources, and classroom averages. They can help interpret behavioral responses to school assignment. They are not later postsecondary outcomes.

## 4. How the files relate

The deposited README says:

1. `code-AER-1.do` produces Figures 1–3 and Tables 1, 3, 4, and 5 using files 1–6.
2. `Code-AER-2.do` produces Figure 4 and Tables 2, 6, 7, 8, and 10 using file 7.
3. `Code-AER-3.do` produces Table 9 using file 8.

Our interpretation is:

- files 4–6 preserve the ordinary student-by-assigned-environment structure;
- files 1–3 transform administrative records into cutoff-expanded structures for causal regression-discontinuity estimates;
- file 7 merges the cutoff design with the authors' survey measures at student, track, and school levels; and
- file 8 narrows the survey design to classroom assignment and classroom-level mechanisms.

This produces two related but distinct research designs:

1. **Peer-pool description:** Use files 4–6 to describe sorting, peer composition, own relative standing, and later Baccalaureate outcomes.
2. **Cutoff-based identification:** Use files 1–3 and possibly files 7–8 to estimate the effect of gaining access to a better school/environment near an admission threshold.

The first design can show the empirical structure of the environments. The second can identify the effect of access to a bundle of school features. Neither by itself isolates a pure causal peer effect unless additional assumptions and evidence justify that interpretation.

## 5. Current scientific assessment for our question

### What Romania can test well

Romania is a strong public-data match for several parts of the talent/performance, assignment, assortativity, congestion/scarcity, and success framework:

- **Prior performance:** Every student in files 4–6 has a pre-assignment transition score.
- **Assignment:** Students are assigned to observable schools and academic tracks.
- **Identifiable peer environment:** Cohort × school-track groups are reconstructable. There are 5,002 such cells across 2001–2003. Median cell sizes are 50, 56, and 60 students by cohort.
- **Sorting:** We can measure how similar students are within school-track environments using the prior transition score.
- **Relative standing:** We can calculate a student's standing relative to leave-one-out school-track peers.
- **Scarcity/selectivity:** Admission cutoffs provide a real threshold governing access to stronger environments.
- **Later success/performance:** We observe whether students take the Baccalaureate examination and, for most takers, their grade.
- **Identification opportunity:** Students close to cutoffs provide a credible comparison for the effect of access to a stronger school environment.
- **Mechanism evidence:** Survey files include behavioral responses, perceived peers, parents, tutoring, teachers, and classrooms.

### What Romania cannot establish automatically

- It cannot give one clean universal \(K/N\) because the complete ranked applicant-choice sets and official capacities are not plainly preserved in the clean student files.
- It cannot treat realized school-track size as official capacity without further evidence.
- It cannot interpret Baccalaureate participation as a fixed-\(K\) award. Scarcity governs entry into the school-track environment; the later examination is an attainment/performance outcome.
- It cannot identify a pure peer effect simply because access to a better school changes outcomes. Crossing a cutoff changes a bundle that may include peers, teachers, resources, reputation, curriculum, and behavior.
- It cannot use the cutoff-expanded row counts as student counts.
- It cannot support person-level linkage beyond the deposited outcomes from files 4–6 alone because those files lack a stable named student identifier.
- It cannot answer college-environment congestion questions because the deposit stops before actual postsecondary application and enrollment.

### Recommended conceptual separation

Keep three objects separate:

1. **Sorting:** Who is grouped with whom before later outcomes are observed?
2. **Peer environment and relative standing:** What environment and position does the student experience after assignment?
3. **Effect of access:** What changes at an admission cutoff when a similarly scored student gains access to the stronger school-track environment?

This separation prevents a descriptive association from being mislabeled as causal congestion and prevents the regression-discontinuity estimate from being mislabeled as a pure peer effect.

## 6. Postsecondary and later-attainment search

The complete variable inventory for all eight files was searched for college/university application, admission, enrollment, institution, major, degree, and later educational-attainment fields. The deposited Stata programs were also searched for these concepts.

**Finding:** The public replication package contains no student-level variables for:

- college or university applications;
- college or university admission;
- postsecondary enrollment;
- postsecondary institution attended;
- field of study or major;
- college degree completion; or
- later educational attainment after the Baccalaureate stage.

Variables such as `head_educ_*` and `mom_educ_*` describe parental education in the survey file. They are background covariates, not the focal student's later attainment.

The Baccalaureate is a secondary-school leaving examination and may influence eligibility or competition for later university entry, but `bct` and `bcg` do not record whether a student applied to, entered, attended, or completed university.

Therefore, this archive supports a study of **secondary-school assignment, peer environments, and later secondary-school examination outcomes**. It does not support a direct analysis of university application or college-environment congestion.

## 7. Evidence levels and remaining verification

### Verified directly from deposited files

- file dimensions and hashes;
- variable names, formats, and attached labels;
- clean student-level structure of files 4–6;
- cohort, town, school, and school-track nesting;
- group-size distributions;
- completeness of the transition score and grouping identifiers;
- Baccalaureate participation and grade missingness; and
- absence of postsecondary outcome fields from all eight schemas.

### Supported by deposited code and the published article

- meaning of cutoff-distance and treatment variables;
- use of `sid2` as a student clustering identifier;
- school-, track-, and classroom-level average-score measures; and
- relationship among administrative, survey, and cutoff-expanded files.

### Still requires caution or fuller reconstruction

- exact formulas used to construct every abbreviated expanded-file variable;
- precise construction of composite identifiers such as `uazY`, `us2BY`, and `usYprspB`;
- exact risk set behind each cutoff and whether a defensible local selection-intensity proxy beyond cutoff percentile can be constructed;
- interpretation of realized enrollment relative to official capacity; and
- whether missing Baccalaureate grades among takers are administratively meaningful or ordinary missingness.

## 8. Immediate bounded scientific question

The defensible descriptive question is:

> Among students with similar pre-assignment transition scores, how are assigned school-track peer performance and the student's relative position associated with later Baccalaureate participation and performance?

The separate identification question is:

> Among students close to an admission cutoff, what is the effect of gaining access to the stronger school environment on later Baccalaureate outcomes and documented behavioral responses?

These questions should be developed separately before considering how their evidence can be combined.

