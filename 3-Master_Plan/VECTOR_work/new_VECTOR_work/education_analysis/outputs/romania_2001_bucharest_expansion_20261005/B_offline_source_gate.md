# Bucharest 2001: saved admissions source check

This check reads saved Romanian Ministry admissions webpages without making a web request. It saves aggregate counts only; printed names and scores remain in memory. A printed name and admission score are provisional evidence of a match because the archived personal identifier is masked.

The **Gymnasium Applicant View** has 289 verified originating-school webpages with 22,216 applicant rows. These describe participants in this admissions round, not necessarily every eighth grader at those schools.

The **Placement View** combines 3,000 rows on saved county placement webpages with 20,171 rows from 297 separately saved program placement webpages. Repeated records appearing in both views are counted once. The combined 21,969 records equal the published admitted total of 21,969. This verifies the Bucharest placement source at the aggregate level.

Among the school-page rows, 20,652 have exactly one matching Bucharest placement record; 1,421 have exactly one matching saved Bucharest unassigned record; 0 have multiple possible saved outcome rows; and 143 have no saved Bucharest outcome row. A person in the last group might have an out-of-county outcome or appear on an unresolved source webpage. Of those, 53 have one placement in another county, 4 have one other-county unassigned row, 0 have ambiguous other-county reports, and 86 have no outcome in any of the 41 saved county report sets. The latter remain unresolved and must not be counted as unsuccessful.

The saved **County Applicant View** contains 1,500 rows, of which 1,448 match a school-page row on printed name, admission score, exam score, and grades 5–8 average. 20,768 school-page rows do not appear in the saved county applicant pages. This comparison is limited by the missing pages.

## Open source questions

County applicant pages complete: **False**; unresolved pages: **1**. Unassigned pages complete: **False**; unresolved pages: **1**. The original county placement page series also has an unresolved page, although the recovered program reports reconcile the combined placement records to the published admitted total. Recover or account for the missing county applicant and unassigned pages, then review applicants with no outcome in the saved county reports. Do not run a Bucharest HERO or congestion analysis from these counts.
