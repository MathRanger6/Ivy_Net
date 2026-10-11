# Romania 2001: four-county program-label source gate

This offline check uses saved, hash-verified Ministry pages only. It exports county counts, not names or scores. It applies the previously chosen six program categories, full-occupancy rule, and top-one/top-two cutoff tiers only to test source-label certainty. It does not calculate success rates.

Applicants: **23,318**. Corresponding school-result rows: **23,318**. Rows with a missing or nonunique school-specific printed name-and-score key: **0**. The archived personal identifier is masked, so all matches remain provisional.

Among uniquely matched rows: **22,448** home placements, **160** away placements, and **710** unassigned. Home placement labels identify one directory program for **20,331** rows and multiple programs for **2,117** rows; **0** have no directory match. Already-saved program-specific reports corroborate exact codes for **5,787** home placements. Top-one labels are unresolved for **0** home placements; top-two for **0**. An unresolved label is never coded as a failure by default.

Supplemental destination-program reports added to the private source cache contribute TM: 200 verified admitted rows, CJ: 100 verified admitted rows. These reports identify program codes; they do not add students to the applicant denominator.

## County detail

- **CT:** 6,507 applicants; 6,213 home placements; 43 away placements; 251 unassigned; 172 multiple-program labels; top-one/top-two unresolved 0/0; occupancy difference +0.
- **PH:** 6,131 applicants; 5,879 home placements; 52 away placements; 200 unassigned; 322 multiple-program labels; top-one/top-two unresolved 0/0; occupancy difference +0.
- **TM:** 5,795 applicants; 5,561 home placements; 15 away placements; 219 unassigned; 860 multiple-program labels; top-one/top-two unresolved 0/0; occupancy difference +0.
- **CJ:** 4,885 applicants; 4,795 home placements; 50 away placements; 40 unassigned; 763 multiple-program labels; top-one/top-two unresolved 0/0; occupancy difference +0.

Occupancy difference equals the program tables' admitted total minus home-origin placements plus admitted arrivals from other counties. A nonzero difference requires source review; a zero difference is an aggregate check, not person-level proof.

The **0** program-code groups responsible for mixed top-two labels are listed, with name-free counts, in top2_ambiguous_program_groups.csv. Resolving them requires an exact program-code source for the affected placements; no choice is inferred from the ambiguous school/profile/specialization label.

This is a source gate, not a HERO plot, program preference measure, or national outcome analysis.
