# Romania 2001: Arad and Sibiu gymnasium-source expansion

**Source acquisition plan, October 4, 2026.** This is an expansion of the four-county *source* audit, not a new outcome analysis.

## Why these two counties

The saved Ministry directory, county applicant list, admitted-placement list, unassigned list, program directory, and program occupancy reports are complete for both **Arad (AR)** and **Sibiu (SB)**. The county applicant lists contain 3,192 and 3,310 rows, respectively. These are large enough to be useful follow-ups to Alba, Caraș-Severin, Galați, and Tulcea while keeping the next retrieval bounded. Completeness of a county list alone does not establish complete originating-gymnasium peer groups.

The saved originating-gymnasium directories identify **136 Arad** and **152 Sibiu** school-specific applicant webpages. A no-network preview on October 4 found **zero of those 288 webpages** already checkpointed in the private cache. We therefore have 288 school webpages to request, subject to archival availability.

## Acquisition and stopping rule

The existing source-only worker now accepts AR and SB. It uses the directory's exact school-specific URLs, verifies saved pages by source URL, expected columns, row count, and hashes, and immediately checkpoints each success in the private Desktop cache. Failed URLs remain **unresolved** and retryable. They are never converted into zero-applicant schools. The researcher controls the actual Wayback run in Cursor. The worker prints every requested URL, successful save, progress count, and reason for waiting. Its bounded settings include 22–50-second adaptive spacing, 600- then 1,500-second waits on repeated HTTP 429, and at least ten seconds after HTTP 500/503. Do not run a second archive acquisition notebook concurrently.

The name-free AR/SB progress inventory is `gymnasium_acquisition_status.csv` in this folder. The worker's `--status-file` setting keeps it separate from the prior four-county progress CSV. A no-network preview verified the **0/136 AR, 0/152 SB** starting point and did not write a status file.

Researcher-run notebook: [EDUCATION_20261004_Romania_2001_AR_SB_gymnasium_acquisition.ipynb](../../notebooks/EDUCATION_20261004_Romania_2001_AR_SB_gymnasium_acquisition.ipynb). Its download switch starts **off**.

## Gate after downloading

Only after every obtainable school webpage is checkpointed will we run an offline source reconciliation. It must compare gymnasium rows with county applicant, placement, and unassigned reports; check printed name-plus-score collisions and exam/grade components; identify cross-county placements; verify program identities and capacities; and list all unresolved items. Charles retains the decision on whether each county is suitable for a research result. No AR/SB HERO or combined six-county plot is authorized merely by completing downloads.

## October 5 source-check update

All **136 Arad** and **152 Sibiu** directory-listed gymnasium applicant webpages are now saved and verified. The previously unresolved Arad school 190 page was recovered on retry. A read-only comparison found 3,164 gymnasium applicant rows in Arad and 3,236 in Sibiu; every one has one saved placement or unassigned report row. This is a match among the participating applicants in these webpages, not a claim about all eighth graders.

The reverse check compared the complete county-wide applicant lists against saved gymnasium webpages in six counties. In Arad, 3,121 of 3,192 county-list applicants matched an Arad school page, four matched a school page in another checked county, and 67 matched no page in the six-county set. In Sibiu, the corresponding numbers were 3,192 of 3,310, 20, and 98. **All 165 unmatched county-list rows carry a printed school label ending in another county's abbreviation; none claims an Arad or Sibiu originating school.** That makes them incoming cross-county applicants, not evidence of a missing Arad or Sibiu school webpage. These source counts are saved in `reverse_applicant_school_page_check.csv` and explained in `reverse_applicant_school_page_check.md`. Printed name and score comparisons remain provisional because the archive masks the unique student identifier.

The next offline program gate found that both counties' program seats balance with admitted students and vacancies, and the saved placement row count equals the program-table admitted total. The six-category, fully occupied, top-one/top-two **definition** therefore transfers. Exact program identification does not fully transfer: 149 Arad gymnasium applicants' top-one and top-two yes/no labels are uncertain because a day and evening program share the printed placement identity; 114 Sibiu applicants' top-two labels are uncertain because Romanian, German, and Hungarian programs share the printed identity. Sibiu top-one labels are unaffected. The full source check and the five exact program codes that could resolve this are in `AR_SB_program_outcome_gate.md`. No Arad/Sibiu HERO plot was calculated. Next source task: recover and verify those five program-specific admitted-student webpages or preserve explicit uncertainty bounds; do not assign a code from admission score alone.
