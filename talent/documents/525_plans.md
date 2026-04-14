# 525 Talent Pool Analysis — Plans and Outline

**Broader way ahead** (mechanism articulation, venues, external data): see **Publication_Plan.md**.

This document captures the plan for **525_talent_pool_analysis.ipynb**, a parallel research track that uses existing 520 (and other) outputs to find **other mechanisms besides OERs** that correlate with strong talent pools—getting at "prestige" through **who** and **where**.

**Status**: Planning. Edit here until we have a solid plan, then code.

---

## 1. Research direction

- **Talent pool** = high mean TB ratio (or similar) from 520 — already built.
- **525** = "What else predicts or aligns with these pools?" → **unit (UIC)** and **rater (senior rater pid_pde)** as candidate mechanisms alongside OER content. A parallel thread: **which UICs (and unit types) are associated with longevity**, and can we describe a **path through the network** (sequence of unit types) for officers who achieve highest rank and longest tenure?
- **Prestige**: Units and senior raters associated with strong pools may be acting as signals or gatekeepers; 525 explores that. Longevity and path analysis adds: "Is there a pattern to where successful, long-tenure officers have been?"

---

## 2. Two main analyses (and why both)

### 2.1 UIC analysis (rated officer → battalion/brigade)

- **Rated officers** are listed by **company UIC** in the data.
- Use **existing UIC tables** to aggregate: company → battalion, company → brigade.
- **Question**: Which **battalion UIC** or **brigade UIC** (by where the **rated** officer was) is associated with the **strongest senior-rating pools**?
- **Different question** (for later): Which UICs by **senior rater** location are associated with strongest pools? Code should support both; we start with **rated officer UIC** aggregated to battalion/brigade.

### 2.2 Senior rater (and later rater) analysis

- **Question**: Do certain **senior rater pid_pde**s consistently correspond to high talent pools?
- **For now**: Focus on **senior raters** only. Code should be written so that **raters** can be added later with minimal change (e.g. a single parameter like `rater_role = 'senior_rater'` vs `'rater'`).
- **Longitudinal extension** (later): Include **lieutenant OERs** so we can track the same senior rater across career stages (e.g. as CPT rating LTs → later as COL rating CPTs/MAJs). Requires LT OER pipeline and consistent senior rater id across ranks.

### 2.3 UICs, longevity, and career paths (new thread)

- **Longevity (definition)**: **Maximum time from commissioning date (or `ofcr_apnt_dt`) to exit from the service.** So longevity = total tenure from entry to separation/attrition. We have appointment dates for officers in the cohort; exit date defines end of service.
- **Longevity (analysis)**: Which UICs (at different aggregations: company, battalion, brigade, etc.) are associated with the **greatest longevity**? Same UIC tables and aggregation levels as above; outcome = tenure from commissioning to exit.
- **UIC categorization**: Use a **categorization of UICs**—e.g. **division**, **function** (combat arms, combat support, combat service support, etc.), or other attributes in your tables—so we can describe units by type, not just by raw UIC.
- **Path through the network**: For officers who achieve the **highest rank** and **longevity**, can we describe their **path** through the network (sequence of unit types / UICs over time) and show that there is a **pattern**? E.g. "officers who make COL and have long careers tend to have passed through certain division/function types in a certain order." That would support a narrative that career trajectory (path through unit types) is associated with outcomes, alongside talent pools and prestige.
- **Data caveat — already-CPT or MAJ at window start**: A large number of officers were **already captains or majors at the beginning of the data window**; we have their appointment date (e.g. `ofcr_apnt_dt`) but we do not observe their full career from commissioning inside our window. For those officers, longevity (commissioning → exit) can still be computed if we have both dates, but **path-through-network** analysis will miss their early career (LT, early CPT) unless we add earlier data (e.g. LT OERs). When reporting longevity-by-UIC or path patterns, we should be clear about whom we observe from what point (e.g. subset who are observed from CPT or earlier vs. those who enter the window as already-MAJ or already-CPT).

---

## 3. Design principles

| Principle | Detail |
|-----------|--------|
| **Senior raters first** | All initial analyses keyed to senior rater and "senior-rating" pools. |
| **Rater-ready** | Functions and notebook structure parameterized so switching to (or adding) **rater** does not require a second pipeline. |
| **UIC from existing tables** | No new UIC logic in 525. Use existing tables to map company → battalion → brigade; support aggregation level (e.g. company / battalion / brigade) as a choice. |
| **Rated officer UIC** | Primary UIC analysis: rated officer's company UIC, aggregated to battalion/brigade, correlated with strength of senior-rating pool. Option to add senior rater UIC later using same aggregation pattern. |
| **UIC categorization** | Use existing or new attributes (division, function, etc.) to label UICs by type so we can analyze paths by unit type, not only by raw UIC. |
| **Longevity and path** | Same UIC tables/aggregation; add analyses for longevity and for sequence of unit types (path) among high-rank, long-tenure officers. |
| **Recompute** | Prefer using 520 cell output products. When recompute is needed (e.g. different pool definition or base), put it in a **separate .py file** callable from 525, not inline in the notebook. |

---

## 4. Data and inputs

- **520 outputs**: Saved cohort, pool definitions, mean TB by pool, and any identifiers (officer, senior rater, etc.) already produced.
- **Existing UIC tables**: Company ↔ battalion ↔ brigade (and any other levels you use). 525 only reads and aggregates; does not define UIC hierarchy.
- **UIC categorization**: Division, function (e.g. combat arms / combat support / combat service support), or other attributes—from existing tables or a small lookup. Needed for path-by-type analysis.
- **Longevity / rank outcomes**: **Longevity** = time from **commissioning date** (or `ofcr_apnt_dt`) **to exit from the service**. Highest rank achieved. Need both entry (commissioning/appointment) and exit dates; may come from 520 cohort, personnel tables, or existing outputs. Note: many officers are already MAJ at start of data window—we have appointment date but path analysis may miss their early career.
- **Later**: LT OER dataset (senior rater id, TB, optional UIC) for longitudinal senior rater analysis.

---

## 5. Proposed 525 notebook layout

1. **Setup and design note**  
   - Short note: senior raters first; UIC from existing tables; code flexible for raters and UIC role.

2. **Load inputs**  
   - Load **specific 520 cell outputs as needed** (not necessarily the full pipeline).  
   - **UIC tables** (company → battalion → brigade) for when we add brigade/battalion.  
   - For **division-level** work: **520 Cell 7** outputs (e.g. `df_pipeline_07_time_varying`) already include **div_name** from DIVISION_CONFIG; use those to associate senior-rating pools with divisions. No separate LT OER load: **LT OER data is already matched to the snapshot dataframe** in 520 (Cell 4 merges OERs to all snapshot rows by pid and date; LT snapshot rows exist in 04a–09; only Cell 10 drops them for Cox). See §8.

3. **Define "strongest senior-rating pools"**  
   - Single definition used everywhere. For **this analysis** use **pool means** (mean TB in pool), not pool-minus-mean — we are ranking pools by quality, not individuals within pools. Reuse or recompute from 520 as needed.

4. **UIC analysis (rated officer → battalion/brigade)**  
   - **Start with division-level aggregation only**; add brigade and battalion once division is working. **520 Cell 7** gives div_name on the snapshot frame; use that to aggregate pool strength by division.  
   - Later: join rated officers to company UIC; map to battalion/brigade via existing tables; aggregate by battalion UIC and brigade UIC.  
   - Prefer **using 520 cell output products** when possible; when recompute is preferable (e.g. different pool definition), do it in a **separate .py file** callable from 525 rather than inline in the notebook.

5. **Senior rater pid_pde analysis**  
   - Which senior rater `pid_pde`s appear most often in high-TB (strongest) pools?  
   - **Expand senior rater view**: same COLs when they were LTC battalion commanders rating LTs — data less sparse (LTs have fewer OERs but some top blocks).  
   - **Switch**: option to **include or exclude** OERs where the **rated officer is LT** (e.g. `include_lt_rated_oers=True/False`).  
   - **No recompute needed for LT OERs** if 520 was run with `load_from_502=True`: 520 attaches **all** OERs to snapshots by pid and date regardless of rated officer rank; LT snapshot rows with OER metrics exist in 04a–09. 525 just filters rows (e.g. keep/drop snapshot rows where rank is 2LT/1LT) via the switch. If a future run did not have LT snapshots in the base, any recompute to add them would live in a **separate .py** callable from 525.

6. **Prestige / interpretation**  
   - Short section: UICs and senior rater persistence as candidate mechanisms that correlate with OER-based talent pools and tie to prestige.

7. **Extensibility**  
   - Where to set `rater_role` (or equivalent) so that raters can be added later.  
   - Where to add senior rater UIC analysis if desired.

8. **UICs and longevity**  
   - At each aggregation level (company, battalion, brigade): which UICs are associated with greatest longevity? (e.g. mean/median tenure by UIC, or survival-style summary.)  
   - Use same UIC tables and categorization as above.

9. **UIC categorization (division, function, etc.)**  
   - Join UICs to division, function, or other type.  
   - Summaries and plots by category (e.g. longevity by function, talent-pool strength by division).

10. **Path-through-network analysis**  
    - For officers who achieve **highest rank** and **longevity**: build their **sequence** of unit types (by division, function, or UIC level) over time.  
    - Describe patterns (e.g. common sequences, modal paths).  
    - Goal: "There is a pattern to the paths of officers who reach the top and stay the longest."

---

## 6. Open questions / to decide

- [ ] Exact 520 output files and columns to load (pool id, mean TB, officer id, senior rater id, div_name from Cell 7).
- [ ] Exact UIC table names and column names for brigade/battalion (when we add them); division comes from 520 Cell 7.
- [ ] Whether "pool" in 520 is defined by time window, rank, branch, etc., and how that maps to 525 (same definition vs. simplified).
- [ ] Resolved: LT OER data is already on snapshot frame (520 Cell 4; LT rows in 04a–09). No separate LT pipeline; use switch in 525 to include/exclude LT-rated rows.

---

## 8. OER data and lieutenant snapshots (current pipeline)

**Summary:** OER data **is already mapped to lieutenant snapshots** in the current pipeline when you use 502 → 512 → 520. LT rows are then dropped when building the Cox survival dataset, but they exist in the intermediate 520 outputs.

**502:** Builds the base snapshot table with **all ranks** (2LT, 1LT, CPT, MAJ, LTC, …). No OER merge in 502.

**512:** Builds `df_oer_enriched` from raw OERs. **Keeps lieutenant OERs**: filtering uses `rated_rank.isin(['O01','O02','O03','O04','2LT','1LT','CPT','MAJ','OOO'])`, so 2LT/1LT rated evals are included. No snapshot merge in 512.

**520 Cell 4:** Merges OERs to snapshots via `assign_oer_to_snapshots_fast(df_snaps=df_base, df_oers=df_oer_enriched, ...)`.  
- When **load_from_502 = True**, `df_base` is 502 output → **includes 2LT/1LT snapshot rows**.  
- Merge is by `pid_pde` and date only (no rank filter). So **lieutenant snapshots get OER metrics** where the eval window contains that snapshot date.  
- Outputs `df_pipeline_04a_basic_metrics` (and downstream 05–09) **with LT rows and their OER data**.

**520 Cell 10 (Cox prep):** Builds survival intervals **only from snapshots on or after `dor_cpt`**. So **LT snapshots are dropped** here and do not appear in `df_pipeline_10_cox_ready` or the Cox model.

**Implication for 525:** You do **not** need a new LT OER pipeline to have OER-on-LT-snapshots. As long as 520 was run with **load_from_502 = True**, the saved intermediates (e.g. `df_pipeline_04a_basic_metrics` or `df_pipeline_09_filtered`) **already contain lieutenant snapshot rows with OER and senior rater info**. For longitudinal senior rater or path analysis, 525 can load one of those dataframes (or 502’s `df_502_base` plus re-running the OER merge for a subset) and **keep** LT rows instead of restricting to `snpsht_dt >= dor_cpt`. No change to 512 is required; the only “missing” piece was using the existing LT rows in analysis.
- [ ] Where do division, function, or other UIC categorizations live? (Existing table or new lookup.)
- [ ] Confirm source for commissioning/appointment date (`ofcr_apnt_dt`) and exit date; ensure longevity (commissioning → exit) can be computed for the cohort. For officers already MAJ at window start, decide how to flag or subset for path analysis (early career not observed).
- [ ] For path analysis: time grain for "sequence" (e.g. per OER, per year, per assignment) and how to handle overlapping or short assignments.

---

## 7. Edits and next steps

- **You**: Edit this doc with clarifications, new sections, or changes to the outline.
- **Next**: Once this plan is solid, create **525_talent_pool_analysis.ipynb** with the structure above and stubs that load 520 outputs and UIC tables, then implement the UIC aggregation and senior rater steps.
