# Questions for CODA: from raw Army data to the analysis dataframes

Charles | DRAFT for Charles to approve before sending | 9 November 2026

Chapter 3 of the dissertation (data and empirics) needs an Army data section that starts at the raw data and ends at the columns used in the promotion and attrition histograms. You built most of that chain. The code shows what each step does. It does not always show why, and some of it may have changed on the move from AWS to Palantir Army Vantage.

Please answer from the existing code, notebooks and saved runs. **No new analysis is requested.** Where the answer is "I don't remember" or "never checked," please say so.

The chain we are reading: notebooks 501, 502, 503, 504/509, 512, then `build_df_masters.py`, then 520, all under `talent/talent_pipeline/`.

### 1  What the raw sources are

For each raw source feeding 501–503 and 512: what system or file it comes from, what one raw row represents (an officer, an officer on a date, an evaluation), the key that identifies a person, and which raw columns carry the dates. Please say which raw columns survive into the final panel and which are dropped.

### 2  What is kept and what is dropped, in order

List each filter in the order it is applied: commissioned officers only, branch, rank, year group, inconsistent appointment dates, officers with no evaluation (the `noOER` setting), and anything else. For each, give the reason. If row or officer counts after each step were ever saved, please point to them. A single flow table (raw rows, then officers kept at each step, then the final panel) is what the chapter needs most.

### 3  How promotion and attrition are defined from raw columns

- **Promotion (event 1):** which raw column or change defines it? A rank change between snapshots, a promotion date, or something else? Does it mean promotion to major at any time, or early (below-the-zone) promotion only? Which one is in the final promotion histogram?
- **Attrition (event 2):** how is an exit identified? Does an officer who disappears from the snapshots count as attrition, and how are real exits told apart from a gap in the data, a move to the reserves, or a change of ID?
- **Neither (event 0):** how many officers end the window with no event, and why?

### 4  How a top-box rating is built from evaluations

Which raw evaluation columns give the senior rater's box check, and which values count as the top box? How are rater and senior rater identities obtained (503 hierarchies, 504/509 unit codes, 512 enrichment)? Where are the identities least reliable, such as missing, reassigned or merged units?

### 5  Run of record

Which notebook, configuration and saved run produced `ARMY_G1_pool_minus_mean_fwd_cif_b8.png` and the matching attrition figure? Our reading of the repo is that it is the 20260320 export of 520, using the base year-group filter (2002–2011). Please confirm or correct. If you still have saved outputs, we also need the snapshot date range and, for each band, the number of officers still open at the end (no promotion and no exit).

### 6  What is authoritative and what is superseded

Which of 501–512 and which helper scripts are the pipeline of record, and which are earlier versions to ignore? If an older and a newer version both exist, which would you cite?

### 7  Known quirks a reader should be told about

Anything about the data a careful reader would be surprised by and that is not written down: gaps in snapshot dates, changes in how a field was recorded over time, de-identification effects, years with thin evaluation coverage, or identifiers that change.

### 8  What can be said in print

Is there any restriction on what the dissertation may say about the raw sources, such as field names, counts, or the structure of the evaluation file? If the Army Analytics Group or the Person-Event Data Environment has guidance on this, please point to it. We would rather know now than at the formatting stage.

### Files for reference

- `3-Master_Plan/re_entry/_DISPOSABLE_Ch3_data_empirics_thread.md` (what we have established so far)
- `current_documents/talent_documents/520_PIPELINE_COX_OVERVIEW.md`
- `3-Master_Plan/re_entry/ARMY_fwd_bwd_and_pool_fix_for_dummies.md`
- `3-Master_Plan/re_entry/HEROs_and_PASSes/army_sandbox/EXTRACT_MANIFEST.txt`
- `3-Master_Plan/VECTOR_work/new_VECTOR_work/20261018_CODA_Response_NVector_Army_LOO_Questions.md` (the earlier round; please do not repeat answers already given there)
