# Romania 2001: seven-county offline source reconciliation

This audit reads saved, hash-verified Ministry webpages only. It makes no archive request. It compares printed name and admission score **within the same originating-school code**, but the archived personal identifier is masked. A matching printed key is strong source corroboration, not proof of unique person identity.

Across B, AB, CS, GL, TL, AR, and SB, all **41,561** score-bearing gymnasium applicant rows have a corresponding school-result row. The school-result webpages contain **25 additional rows** not found in their same-school score-bearing webpages. **24** carry the Ministry's literal `NEREPARTIZAT` (unassigned) marker; one carries another status. Those rows need a separate source explanation; they are not silently added to a research cohort.

The older Bucharest source audit could not locate **86** gymnasium applicants in its saved county outcome lists. Each has exactly one matching row in the newly recovered result page for the same originating school, and all **86** are explicitly marked `NEREPARTIZAT`. The archived personal ID is masked, so this is a provisional printed-name-and-admission-score match corroborated by school code, not a certified person-identifier linkage. The old 86-person *source gap* is resolved by this view; it does not show a program preference or justify a new analysis yet.

The separate cross-county candidate lists contain **1,730** rows. At printed name-and-score multiplicity, they equal **1,644 admitted + 86 unassigned** incoming rows, with zero unmatched rows in either direction. This verifies the three incoming source views against each other for these destination counties; it does not establish a national transfer rate.

These sources also support **county-to-county flow counts**. Every incoming candidate, admitted, and unassigned row in these seven destination counties prints an origin-school label ending in its county code. The school-result webpages for these seven origin counties print **576** placements with an external destination-county suffix. In the **12 origin–destination county pairs** where both sides are among the seven, the two independent admitted counts agree for all **84** placements. The accompanying `county_flow_counts.csv` gives aggregate counts by origin and destination, never student names. A cross-county admissions route is observable; whether a family moved or a student sought a particular program is not.

The resident-candidate report pages are complete by their own printed page totals in AB, CS, TL, AR, and SB. Their printed name-and-score rows exactly match the score-bearing gymnasium webpages. Bucharest (B) has 6 of 45 projected resident pages, and Galați (GL) has 9 of 11; each has an unresolved archived URL. Their saved resident rows are subsets of the school webpages, but the missing resident pages remain unresolved. A source-printed total matching a school-page count does not substitute for those pages.

## County counts

- **B:** 22,216 school-page rows matched; 16 extra school-result rows; incoming 1400 = 1317 admitted + 83 unassigned; resident pages 6/45 projected (source incomplete).
- **AB:** 3,041 school-page rows matched; 1 extra school-result row; incoming 19 = 19 admitted + 0 unassigned; resident pages 7/7 projected.
- **CS:** 2,606 school-page rows matched; 0 extra school-result rows; incoming 15 = 15 admitted + 0 unassigned; resident pages 6/6 projected.
- **GL:** 5,345 school-page rows matched; 2 extra school-result rows; incoming 100 = 97 admitted + 3 unassigned; resident pages 9/11 projected (source incomplete).
- **TL:** 1,953 school-page rows matched; 0 extra school-result rows; incoming 7 = 7 admitted + 0 unassigned; resident pages 4/4 projected.
- **AR:** 3,164 school-page rows matched; 5 extra school-result rows; incoming 71 = 71 admitted + 0 unassigned; resident pages 7/7 projected.
- **SB:** 3,236 school-page rows matched; 1 extra school-result row; incoming 118 = 118 admitted + 0 unassigned; resident pages 7/7 projected.

## Open source questions

1. Explain the 25 school-result-only rows by inspecting their saved source context and whether they belong to a different allocation route or a report inconsistency. Do not infer a reason from these counts alone.
2. Seek alternative archived captures for the missing B and GL resident-candidate pages; keep the addresses unresolved until Charles decides whether to stop recovery.

This is a source audit, not a HERO or congestion analysis. No student names, personal identifiers, or individual scores are exported in the report or CSV.
