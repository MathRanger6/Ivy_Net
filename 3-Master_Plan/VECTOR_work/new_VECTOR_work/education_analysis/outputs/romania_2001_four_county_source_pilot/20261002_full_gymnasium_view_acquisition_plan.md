# Romania 2001: complete the four-county source pilot

## Why we are doing this

The first twelve originating gymnasiums inspected in each of Caraș-Severin (CS), Galați (GL), and Tulcea (TL) showed why the county-wide applicant list alone cannot define every gymnasium's applicant group. Some students appear on their own gymnasium's applicant webpage but in another county's admissions reports. We therefore need the remaining gymnasium webpages before deciding whether those three counties can join Alba (AB) in a reliable four-county dataset.

This is a **source-completeness task**, not a test of whether gymnasium peer strength affects placement. No HERO curve or national outcome analysis follows automatically from finishing the downloads.

## What the next run obtains

The saved Ministry Gymnasium Directory View lists 171 gymnasiums in CS, 190 in GL, and 103 in TL: 464 in total. Twelve webpages per county are already saved and verified, leaving up to **428 gymnasium applicant webpages** to request. Alba's 168 gymnasium webpages are already saved; this worker does not redownload them.

The worker enumerates only gymnasiums and webpage links recorded in the saved Ministry directory. It checks each saved webpage's original URL, column headings, row count, and file hashes before counting it as complete. New pages are saved immediately in the private Desktop folder; a separate name-free status CSV reports progress. An HTTP error stays **unresolved** and may be retried later. It does not mean that the school had no applicants.

After acquisition, we will audit each county separately: whether every directory-listed gymnasium has a verified applicant webpage; whether students in the county applicant, gymnasium applicant, placement, and unassigned reports can be reconciled without double-counting; and what source gaps remain. The four counties become research-ready only if those checks pass and Charles reviews the remaining limitations.

## Control and stopping rule

The notebook will first show a no-network preview. Charles starts the download cell in Cursor. Requests are sequential, with a 22–50 second adaptive interval. The worker prints the requested URL, the archive response, each newly saved school and row count, periodic county totals, and the reason and expected end of each wait. It stops after preset page, HTTP-attempt, or time limits, or after a third consecutive HTTP 429. The first two consecutive 429s cause 600-second and 1,500-second cooldowns. HTTP 500/503 responses cause at least a ten-second recovery wait. Saved pages survive interruption and are reused on the next run.

Researcher notebook: `../../notebooks/EDUCATION_20261002_Romania_2001_three_county_gymnasium_acquisition.ipynb`. Worker code: `../../code/EDUCATION_20261002_romania_three_county_gymnasium_acquisition.py`. Private source files remain under `~/Desktop/VECTOR_temp/`; the name-free progress file is `full_school_view_acquisition_status.csv` beside this document.

## October 2 request-pattern check

The first full-view run recorded seven HTTP 429 responses through CS gymnasium 171. The first occurred on the run's **first page request**. Subsequent 429s followed **6, 11, 7, 6, 27, and 9** successfully retrieved gymnasium webpages. Each webpage generally entails two HTTP requests: an archive redirect and a successful page response. The number of raw HTTP requests between 429s likewise varied: **13, 24, 15, 13, 56, and 20** (including the ending 429). A fixed “ten requests, then block” rule does not fit these observations. Most 429s occurred after 13–14 HTTP requests in the preceding five minutes, but successful responses also occurred at 14, so this is not evidence of a strict five-minute quota. The worker's 10-minute cooldown also makes several 429s appear about 15–19 minutes apart; that spacing is partly created by our own retry policy. We have not inferred a Wayback quota from this log and have not changed the pacing on its basis.

## Acquisition complete: October 2, 2026

The overnight-style researcher-controlled run finished. An independent, no-network recheck at 20:34 EDT verified **every directory-listed gymnasium webpage**: CS 171/171, GL 190/190, TL 103/103, or **464/464** combined. The run recovered the remaining **428** pages and left **zero unresolved gymnasium codes**. The saved pages contain 2,606 applicant rows in CS, 5,345 in GL, and 1,953 in TL (**9,904 page rows**, not yet certified as distinct people). The request log records 428 successful page responses, 433 archive redirects, and 11 HTTP 429 responses. No new Wayback request was made for this recheck.

This clears the **webpage acquisition gate** for these three counties. It does not clear the separate **student reconciliation gate**. The next offline check must determine whether gymnasium applicant rows can be linked to county applicant, placement, and unassigned reports without relying on same-county residence or treating equal printed names and scores as a guaranteed unique person identifier. Source gaps or ambiguous matches remain open for Charles's review before any HERO or congestion analysis.
