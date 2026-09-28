# Education — what the existing NELS panel can support

**Last synced:** 2026-09-28  
**Status:** Internal source audit executed in `sports_net`; substantive transition models have not been fitted.  
**Purpose:** Establish a trustworthy starting point for the education investigation without expanding its scope.

## 1. Where we are going, and why

PD42 shifted the immediate empirical effort to education. The question is whether school context and a student's standing within it relate differently to entering postsecondary education and to completing a bachelor's degree. A final degree outcome combines those steps. Separating them may teach us something even if neither curve turns downward.

We first inspected the supplied panel rather than launching another sequence of filters. That inspection established that the sample flags and peer calculations are reproducible. It also exposed a small number of source-definition questions. Our next step should resolve those questions, not request a broad new dataset or search for a more favorable curve.

**Decision gate:** Internal consistency largely passes. Source provenance is incomplete. Keep the existing files and their definitions intact; settle the source mapping before presenting adjusted entry/completion estimates as substantive findings.

## 2. What we checked and found

- **Population: 10,545 students in 1,418 recorded school groups.** Student identifiers are complete and unique. The existing `analytic_sample_min10` flag selects 7,238 students in 536 schools, matching the earlier saved sample count.
- **The minimum is ten sampled students, including the focal student.** It is not ten other peers. There are 878 accepted students with exactly nine peers. This corrects the plotting script's informal “min-10 peers” wording without changing the filter.
- **Eligibility flags reproduce exactly.** The supplied minimum-five and minimum-ten flags agree with the corresponding recorded school size, available performance and peer mean, and observed outcome. This reproduces the supplied flags; it does not recover the original extraction program or prove every upstream inclusion decision.
- **Peer calculations reproduce closely.** School size and peer count match exactly. The largest difference in the raw leave-one-out average is 0.00000733 score units; in its standardized counterpart, 0.000000270. Counts of higher-scoring peers and equal-scoring peers match exactly. These small average discrepancies are consistent with numerical storage precision, not evidence of a substantively different peer pool.
- **Rank handles ties by giving half credit.** The stored within-school percentile equals the fraction of other sampled students below the focal student, plus half the fraction tied. It is sampled test-score standing, not a transcript-reported graduating-class rank.
- **Own-score standardization is coherent.** One linear transformation reproduces `own_performance_z` to within 0.000000548. Its implied reference mean is about 51.96450 and spread 10.19234. The original reference population remains undocumented; a fitted identity does not identify it.
- **Weights are usable numbers, but their identity is not verified.** All 7,238 accepted students have positive follow-up weights, ranging from 14.706 to 3,313.975. The extract lacks survey strata and replicate weights. A school-cluster correction alone would not recreate the full survey design.

For student $i$ in sampled school group $j$, the verified peer identities are:

$$
\overline A_{-i,j}=\frac{\sum_{k\in j}A_k-A_i}{n_j-1},
\qquad
R_i=\frac{\#\{k\ne i:A_k<A_i\}+\tfrac12\#\{k\ne i:A_k=A_i\}}{n_j-1}.
$$

Peer construction here uses the supplied school cells, including students who may lack an observed later outcome. It must not silently be recalculated only among degree respondents.

## 3. What the outcome columns actually contain

The stored analytic sample contains:

- **5,888 recorded postsecondary entrants out of 7,238 students: 81.35%.**
- **2,605 recorded bachelor's-or-higher recipients out of 7,238 students: 35.99%.**
- **2,605 recipients among the 5,888 recorded entrants: 44.24%.**

These are newly verified, unweighted descriptions of the supplied columns. They are not national estimates, adjusted relationships, or evidence of a congestion mechanism.

Every recorded bachelor's recipient is also recorded as an entrant. The stored columns therefore satisfy the accounting identity:

$$
P(B=1)=P(E=1)P(B=1\mid E=1).
$$

The mapping from `degree_code_2000` is exact: codes 1–6 mean entry; 3–6 mean associate-or-higher; 4–6 mean bachelor's-or-higher; −3 becomes zero in all three indicators; −9 becomes missing. The full panel has 1,869 code −3 students, of whom 1,350 are in the analytic sample (18.65%). Thus the meaning of that skip code matters directly to the entry comparison.

**Source evidence supports, rather than contradicts, this recode.** An externally hosted reproduction of the NELS electronic codebook identifies `F4HHDG` as applicable to respondents with postsecondary experience, labels −3 a legitimate skip, and distinguishes −9 as missing. It also documents ordinary degree categories matching our extract. This is original codebook content hosted on a researcher's site, not an authenticated copy of our extract's release. We have not established that `degree_code_2000` is precisely this variable or inspected its original derivation program. [W1]

There are 366 full-panel students recorded as postsecondary entrants without the ordinary high-school-diploma indicator. Do not call these nesting errors: that indicator excludes general educational development credentials and other categories. The appropriate hierarchy for this comparison is bachelor's completion within entry; an ordinary diploma is not a required first rung for every student.

## 4. The performance measure needs its source name

The canonical education primer calls own performance a reading-plus-history composite. We tested the simple mean of the two supplied subject columns; it does not reproduce `own_performance_raw` (10,475 mismatches among 10,477 comparable rows). Neither individual subject column reproduces it either.

This does **not** prove that the stored measure is invalid, or exclude some other composite construction. It establishes that we cannot recover the claimed definition through that simple calculation. Until the source variable or recipe is identified, call it the **supplied baseline performance score**. Do not relabel it as pure ability, invent an alternative subject combination, or rebuild it.

This matters because the planned comparison holds prior measured performance approximately constant. We should know which performance and which measurement date that statement refers to.

## 5. What the existing plotting code does

Direct inspection of `scripts/big_fish_data_story.py` confirms that the education branch uses the supplied analytic flags and precomputed standardized peer mean. The bachelor's outcome is plotted with unweighted bin averages. The high-performance probe restandardizes own performance within the accepted population, selects the one-to-two-standard-deviation band, and uses ordinary Wilson intervals.

Consequently, that probe is a broad-band descriptive comparison. It does not hold individual performance exactly fixed, adjust for socioeconomic status, or supply survey-design-adjusted uncertainty. A change of scale for selecting the band is not, by itself, a mathematical inconsistency with the peer axis. The important distinction is the population and conditioning used.

## 6. Was the augmentation request researched?

**The earlier VECTOR addendum has identifiable, substantive source support.** The inspected COMPASS primer and portfolio documents do not establish who performed the original availability checks. We should not attribute those checks to COMPASS without a research record. Our current verification establishes the following:

- **Applications were collected, with limited coverage.** Official documentation describes reports about two institutions, not a complete application history. [W2]
- **Derived application and admission indicators require care.** The report's `EVR4YRA` counts reported four-year enrollment as evidence of application; `ACPT4YR` can likewise infer acceptance from the first institution attended. A future request must distinguish reported decisions from such inferred indicators. [W3]
- **Transcript rank is documented.** `F2RRANK` and `F2RCSIZE` support the report's class-rank measure. This is a different measure from our sampled score percentile. [W3]
- **Historical selectivity linkage exists.** The official NCES–Barron's listing identifies 1992 ratings and institution identifiers, with restricted-use access. Existence does not establish access or successful linkage for our students. [W4]
- **A later HS&B sophomore follow-up exists.** The official overview documents the 1992 sophomore resurvey and 1993 transcript update. This does not give the senior cohort the same follow-up. [W5]

Direct retrieval of several NCES overview/data-product pages failed during this pass. The Barron's listing and HS&B overview were verified through indexed official text; the applications page and 98-105 PDF were retrieved directly. Exact release-level destination fields, linkage completeness, and the colleague's permissions remain unverified.

**No broad augmentation request is warranted yet.** If later needed, first destination and historical selectivity would distinguish entry anywhere from entry into a selective institution. Direct application and admission records would help distinguish applying, receiving an offer, and enrolling. Neither addition alone would identify causal congestion.

## 7. The smallest useful next step

Recover the construction recipe or answer this short source question:

> For the supplied NELS panel, which original variables and waves produced `own_performance_raw`, `school_id`, `degree_code_2000`, and `followup_weight_2000`? Is `degree_code_2000` copied from `F4HHDG`, with −3 representing respondents without postsecondary experience? Please provide the extraction/recoding program or the relevant variable definitions, including the standardization population.

This is a request to understand data already supplied, not a request to augment them with new research variables. No message has been sent.

Once confirmed, keep the existing minimum-ten-student population and peer definitions fixed. Specify one comparison of entry, bachelor's completion overall, and completion among entrants, with declared baseline performance/background adjustment. Preserve the distinction between association and causation and account explicitly for survey limitations. Do not silently add both a score, its peer mean, and their exact difference as independent linear predictors. Record the specification before fitting it.

## 8. Reproducibility and sources

All new files are under `3-Master_Plan/VECTOR_work/new_VECTOR_work/education_analysis/`:

- Program: `code/EDUCATION_20260928_nels_source_audit.py`.
- Results and execution metadata: `outputs/source_audit_20260928/audit_summary.json`.
- Complete observed outcome mappings: `degree_code_2000_crosswalk.csv` and `hs_completion_code_2000_crosswalk.csv` in that output folder.
- The program records source and script SHA-256 fingerprints, Python path/version, package versions, and execution time. It verifies that the original CSV fingerprint is unchanged. It was run once, then extended to verify rank/tie rules and report both strict and storage-scale numerical tolerances, and rerun. No model, filter, outcome, or source file was altered.

Repository evidence: `datasets/nels88/nels88_big_fish_panel.csv`; its accompanying source email; `scripts/big_fish_data_story.py` (education specification, `_load_eligible_frame`, `_bin_table_on`, `run_cct_probe`); `3-Master_Plan/re_entry/HEROs_and_PASSes/EDUCATION_dataset_primer.md`; the existing VECTOR education review/addendum. Searches covered the data directories and relevant source/document files, not the large historical chat archives. The missing extraction program may exist outside those searched locations.

- **W1:** [NELS electronic codebook excerpt hosted by Juan Battle](https://www.juanbattle.com/files/2012/04/Battles-Code-Book.pdf), PDF pages 30–31: `F4HSTYPE`, `F4HHDG`, response universes and code labels.
- **W2:** [NCES 98-105, application/acceptance discussion](https://nces.ed.gov/pubs98/access/98105-13.asp).
- **W3:** [NCES 98-105](https://nces.ed.gov/pubs98/98105.pdf), printed pages 80 and 85–86, rank and derived application/admission definitions.
- **W4:** [NCES–Barron's historical admissions competitiveness files](https://nces.ed.gov/use-work/dataset/nces-barrons-admissions-competitiveness-index-data-files-1972-1982-1992-2004-2008-2014).
- **W5:** [NCES HS&B overview](https://nces.ed.gov/surveys/hsb/).
