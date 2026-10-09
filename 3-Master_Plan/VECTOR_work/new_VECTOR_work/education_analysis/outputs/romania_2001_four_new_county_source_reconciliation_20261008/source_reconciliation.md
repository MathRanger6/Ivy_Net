# Romania 2001: four newly downloaded counties — offline source reconciliation

This check reads saved, hash-verified Ministry webpages only. It made no archive requests. The exported files contain county counts, never names or individual scores. A printed name-and-admission-score match is provisional because the archived personal identifier is masked.

The four counties have **791 school-result reports** containing **23,326 printed rows**. Every report listed by its saved school directory is present.

The incoming-candidate lists contain **588 rows**: **572 admitted** and **16 rejected/unassigned** in their separate outcome lists. Candidate rows lacking a matching incoming-outcome row: **0**; outcome rows lacking an incoming-candidate row: **0**. This compares printed name and admission score with multiplicity, not certified person identifiers.

The county-wide resident-candidate lists are complete by their source-printed totals in PH and CJ. CT and TM still have missing archived pages; their saved rows are only a subset of their projected lists. All four counties have school-result reports, but the separate gymnasium score reports with both examination and school-grade components have not been downloaded for these counties. Consequently, this audit cannot yet reproduce the seven-county applicant-to-school-result reconciliation or certify peer pools.

## County details

- **CT:** 185 school-result reports and 6,507 rows; resident-candidate pages 9/14; 4,500 saved resident rows match a school-result row, 0 do not. Incoming 126 = 123 admitted + 3 rejected/unassigned.
- **PH:** 259 school-result reports and 6,134 rows; resident-candidate pages 13/13; 6,131 saved resident rows match a school-result row, 0 do not. Incoming 83 = 82 admitted + 1 rejected/unassigned. The 3 additional school-result rows are marked unassigned.
- **TM:** 202 school-result reports and 5,795 rows; resident-candidate pages 8/12; 4,000 saved resident rows match a school-result row, 0 do not. Incoming 224 = 213 admitted + 11 rejected/unassigned.
- **CJ:** 145 school-result reports and 4,890 rows; resident-candidate pages 10/10; 4,885 saved resident rows match a school-result row, 0 do not. Incoming 155 = 154 admitted + 1 rejected/unassigned. The 5 additional school-result rows are marked unassigned.

## Cross-county source check

For **26** origin–destination county pairs involving at least one of these four counties and with both counties in the eleven-county cache, **26** have equal counts in the originating county's school-result report and the destination county's incoming-admitted list. **0** pairs differ. These are aggregate source counts, not a student-level match.

Incoming-admitted rows whose printed origin-school label could not be read as an external county: **0** across all eleven cached destinations.

## What remains open

1. Recover the missing CT and TM resident-candidate pages or retain their URL addresses as unresolved.
2. Download and verify the gymnasium score-component reports for these four counties before matching applicants to their results or constructing peer pools.

No scientific outcome, HERO plot, program ranking, or congestion analysis was run.
