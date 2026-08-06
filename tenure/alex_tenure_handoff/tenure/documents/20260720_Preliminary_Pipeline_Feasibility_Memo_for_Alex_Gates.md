# MEMORANDUM

**To:** Alex Gates  
**From:** Charles Levine (with PEER pipeline summary)  
**Date:** July 20, 2026  
**Re:** Preliminary feasibility of automated R1 faculty roster + OpenAlex linkage for tenure–productivity analysis

---

## Purpose

This memo summarizes progress on a pipeline to gather and parse faculty roster data from R1 computer-science departments via the Internet Archive, link those individuals to OpenAlex publication records, and construct performance metrics suitable for studying the relationship between relative productivity and tenure outcomes. The goal is to demonstrate feasibility—not to report final causal estimates.

---

<!-- ## Pipeline stages

| Stage | What it does | Status |
|-------|----------------|--------|
| **0–2** | Setup, DBLP spine, **168-school** R1 CS roster + faculty-list URLs | ✅ Complete |
| **3A–3E** | CDX (Wayback capture index) discovery, HTML download, optional URL rescues | ✅ Operational |
| **4** | Multi-strategy HTML parsing → names and ranks | ✅ Complete |
| **5** | Longitudinal linking within each school (snapshot-level panel) | ✅ Complete |
| **6A–6B** | OpenAlex institution map, author ID resolution, works-by-year | ✅ Complete |
| **7** | Enriched panel: publications + tenure / attrition / censoring events | ✅ Complete |
| **8** | Leave-one-out peer-pool quality metrics | ✅ Complete |
| **9** | Preliminary inverted-U feasibility check (binned tenure rates) | ✅ Complete |
| **10–12** | Cox survival models (Layer B) | 📋 Planned |

Each stage writes checkpoint files to disk so runs can resume without redoing completed work. Detail for Stages 0–5 and 6–9 follows below.

--- -->

## Pipeline performance by stage

**Collection and parsing (Stages 0–5).** We have built a checkpointed, end-to-end workflow covering **168 R1 CS departments** (2000–2024). Wayback CDX discovery identified **34,304 downloadable captures**—dated faculty-list snapshots selected from the Internet Archive, typically several per semester when coverage allows—and Cell 3B logged **35,157 successful HTML retrievals** (~99% of download attempts). *In plain terms: a “planned capture” is one dated Wayback snapshot on our download list (~34K across 168 schools, 2000–2024)—not a count of faculty or career-years.* Multi-strategy HTML parsing extracted **2.59 million faculty name/rank records** from roughly **60,500 archived pages**, yielding **~31,000 unique person–department identities**. Longitudinal linking within each institution (Cell 5) produces **2.56 million snapshot-level rows**—one row per person × year × season × Wayback capture (median **~20 captures per person–year**, because we sample multiple dated snapshots per season). Collapsing those duplicates yields **106,559 person–year observations** for **29,274 faculty**; that deduplicated panel is what downstream OpenAlex enrichment and tenure analysis use.

Parsing reliability is a particular strength: a six-strategy competition assigns a winning parser to every audited HTML file; **no school exceeds our 35% failed-parse exclusion threshold**, and **profile-link parsing wins ~64%** of files. Explicit rank labels are recovered at scale (**~150K assistant**, **~126K associate**, **~278K full** professor mentions among parsed rows), though many listings remain `unknown` because departments format pages inconsistently—we retain raw records and filter downstream.

From this spine we identify **2,331 faculty who ever appear as assistant professors** (**114 departments**), with person-level outcomes of **422 tenure events**, **570 attritions**, and **1,339 right-censored** cases.

**OpenAlex linkage and preliminary analysis signal (Stages 6–9).** OpenAlex author resolution covers **19,925 distinct faculty** in the working sample. Among the tenure-relevant subsample, **805 persons (34.5%)** achieve HIGH or MEDIUM confidence matches; **796** have computable leave-one-out (LOO) peer-pool quality metrics on at least one assistant year. Restricting to resolved outcomes (tenure or attrition) yields **376 inference-ready persons** (**174 tenured, 202 attrited**) with both bibliometric covariates and observed career resolution.

As a first feasibility checkpoint, we binned **1,473 assistant careers** with LOO metrics into 18 peer-quality bins. Resolved-case tenure probability rises from roughly **30%** in the lowest bin to **~67–70%** in bins 16–17 (median LOO quality ≈ 7.6–8.6), then falls to **~42%** in the highest bin—consistent with a preliminary inverted-U pattern, though this is descriptive and not yet adjusted for department or cohort effects.

---

## Department Year Stats

**Plain-language answer for Alex.** Of **4,200 possible department–years** (168 schools × 2000–2024), we have roster data for about **half** (~1,958). For roughly **650 department–years (~16% of the grid)**, multiple independent Wayback captures in the same year agree that we extracted a **stable, near-complete faculty listing** (internal consistency ≥98%). That is our best feasibility estimate without manual validation against official rosters. Coverage is **uneven by school and era**—typically on the order of **~4 strong years per department**, not full 2000–2024 completeness. **159 of 168** schools have at least one such high-stability year.

**Important caveats.**

1. **98% stability ≠ 98% vs truth** — if every snapshot systematically omits adjuncts on subpages, stability can still be 100%.
2. **`unknown` rank inflates counts** — many names are captured but not classified; ranked-only stable department–years are fewer (**~353**).
3. **No department–year audit against IPEDS or department PDFs** — a sample validation on 20–30 department–years would tighten this estimate substantially.

*Method (internal): for each department–year with ≥3 snapshots and ≥10 names on the richest capture, we treat median unique-name count ÷ max unique-name count ≥ 0.98 as “stable near-complete” roster recovery. Stricter criteria (every snapshot ≥98% of max) yield **~379** department–years; requiring union-of-names ≈ max yields **~399**.*

---

## Bottom line

The approach is feasible at scale: we can automatically harvest two decades of R1 faculty rosters, parse them with high per-school reliability, link a substantial minority to OpenAlex at confidence levels suitable for inference, and recover preliminary structure linking relative publication performance to tenure outcomes—the core ingredients for the tenure–productivity study.

---

## Notes (Charles & Alex — internal)

- **Strongest engineering wins for this memo:** the **168-school roster breadth** and **checkpoint/resume design** (each stage writes durable artifacts; interrupted runs resume without redoing completed work).
- **Honest scope statement:** **796 / 2,331 ≈ 34%** is the current OpenAlex-linked inference ceiling under automated name resolution—not a pipeline failure, but the realistic bound for analysis-ready rows today. Row-level coverage is uneven (~17% HIGH, ~10% MEDIUM, ~58% NONE at the person–year level).
- **Stage 9 is descriptive only** (binned tenure rates by LOO quality). Cox survival models (Cells 10–12) are planned but **not yet wired** in `540_tenure_pipeline.ipynb`; do not characterize survival analysis as complete.
- **Planned captures:** **34,304 downloadable** rows in `faculty_snapshots_plan.jsonl` (646 additional CDX bookmark rows are query metadata, not downloads). One capture = one dated Wayback faculty-list snapshot—not a person or person–year.
- **Panel grain (important):** `faculty_panel.jsonl` = **2.56M snapshot-level rows** (Cell 5 raw); `faculty_panel_with_pools.jsonl` = **106.6K deduplicated person–years** (Cell 7+ analysis grain). Do not describe 2.56M as person–years.
- **Main artifacts:** `tenure/tenure_pipeline/faculty_panel_with_pools.jsonl` (~106.6K person–years); advisor export path via `543_package_panel.ipynb` → `R1_tenure_data.csv`.
- **Known limits to flag if asked:** variable per-school Wayback coverage; high censoring (~57% of ever-assistant persons); attrition vs. lateral move not fully disambiguated; rank `unknown` share in raw parses.

---

*Draft for Charles review before send. Statistics from on-disk artifacts in `tenure/tenure_pipeline/` (April–June 2026 runs).*
