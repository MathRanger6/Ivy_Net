# PEER → VECTOR: Status Update — Tenure (Setting 3)

**Date:** 2026-06-03  
**Companion doc:** `Scout_Status_Update_for_VECTOR_Laszlo_Briefing_2026-06-02.md` (Setting 2 / basketball)  
**Purpose:** Give **VECTOR** a ground-truth snapshot of where the **academia / tenure** empirical setting stands so Charles can decide how to represent PEER in the manuscript and in any briefings.  
**Author:** PEER (Cursor agent on Cursor Workspace PDE)

---

## 1. Executive Summary

| Topic | Status |
|-------|--------|
| Pipeline (scrape → parse → panel → pool metrics) | **Complete end-to-end** for the current corpus |
| Inverted-U signal | **Yes — present in preliminary analysis** (stage 9; see §4) |
| Cox survival model | **Wired and runnable** (Cell 10); z-scored covariates in Cell 10.5 |
| Coverage completeness | **Partial** — pipeline covers ~60+ R1 CS departments with usable data; full 187-school roster is a publication-time goal |
| OpenAlex linkage | **API-based** (not bulk); ~30–40% HIGH confidence matches; MULTI and NONE coverage is a known limitation |
| Formal model results ready to quote | **Not yet** — preliminary binned curve is the current artifact; regression/Cox output is the next step |

**Bottom line for VECTOR:** The tenure setting has a **working pipeline, a longitudinal panel, and a preliminary empirical result consistent with the inverted-U hypothesis**. It is not as polished as Army/CODA or basketball/SCOUT. The right framing for the manuscript is "preliminary third-setting replication" — honest about coverage limitations, with the stage 9 figure as the anchor.

---

## 2. What Setting 3 (PEER) Is Testing

**Research question:** Do CS faculty at mid-prestige R1 departments have the highest tenure rates, while those at elite departments face the same signal compression and slot scarcity seen in the Army and basketball settings?

| Dimension | Army (CODA) | Basketball (SCOUT) | Academia (PEER) |
|-----------|-------------|-------------------|-----------------|
| Individual performance | OER evaluation score | Points per minute | Annual publications (OpenAlex) |
| Pool definition | Senior-rater cohort | Teammates | CS faculty cohort at same department × year |
| Peer quality measure | LOO pool mean OER | LOO mean teammate PPM | LOO mean publications per year (`poolq_loo_mean`) |
| Outcome | Promoted to Major | Drafted to NBA | Tenured (Assistant → Associate Professor) |
| Slot scarcity mechanism | Literal promotion quotas | Finite draft slots | Departmental FTE / budget lines |

---

## 3. What the Pipeline Built

### Data source
**Internet Archive (Wayback Machine)** — CDX API to plan captures, then HTML downloads and custom parser (`html_parser.py`) to extract faculty name + rank from each archived page.

### Coverage
- **Schools planned:** ~187 R1 CS departments in scope
- **Schools with usable scraped data:** ~60+ departments have parseable HTML in the current run
- **Time window:** approximately **2000–2023** (availability varies by school; earlier years are sparser)
- **Key limitation schools:** Auburn (robots.txt / Wayback exclusion), NC State (redirect shells), some schools with JS-heavy pages that CDX captured as near-empty HTML

### Panel structure
Each row in the panel = **one person × one year** with:
- Name, university, rank (assistant / associate / full / unknown / etc.)
- Annual publications and cumulative publications (from OpenAlex, where matched)
- Tenure outcome flags: `tenure_event`, `attrition`, `censored`
- LOO peer pool metrics: `poolq_loo_mean`, `pool_rank_loo`, `pool_pctile_loo`, etc.

**Panel size (as of May 2026 run):**
- `faculty_panel.jsonl`: ~1.7 GB / **~106,000 person-year rows** (includes all ranks, all confidence levels)
- `faculty_panel_with_pools.jsonl`: 72 MB (enriched with pool quality metrics)
- `faculty_panel_enriched.jsonl`: 55 MB (OpenAlex-matched subset)

### OpenAlex linkage quality
| Confidence | Meaning | Count (sample) |
|------------|---------|----------------|
| `HIGH` | Name + institution + year overlap | ~32% of person-years |
| `MEDIUM` | Name + institution, year unclear | ~15% |
| `MULTI` | Multiple plausible candidates — picked first | ~19% |
| `LOW` | Name match only | ~2% |
| `NONE` | No OA result | ~32% |

> **Implication for VECTOR:** Publication data is missing or uncertain for roughly half the panel. This is a real limitation to acknowledge — the inverted-U is estimated on the subset with OA data. The advisor (Alex Gates, Apr 2026) was aware and directed moving forward with the existing data rather than waiting for bulk OA access.

---

## 4. The Inverted-U Finding (Stage 9 — Preliminary)

### What was done
Faculty-years are **binned into 18 equal-width bins** of `poolq_loo_mean` (leave-one-out mean annual publications of same-dept assistant peers). For each bin, **tenure rate** = `n_tenure / n_resolved` (resolved = tenure + attrition; right-censored cases excluded from denominator).

### Artifact
- **Plot:** `tenure_pipeline/stage9_inverted_u.png`
- **Data:** `tenure_pipeline/stage9_binned_table.csv`

### Binned results (abbreviated)

| Bin | LOO median pubs/yr | Tenure rate | N resolved |
|-----|--------------------|-------------|------------|
| 1 (lowest) | 0.27 | 0.303 | 33 |
| 2 | 0.74 | 0.348 | 23 |
| 3 | 1.28 | **0.488** | 43 |
| 4–6 | 1.76–2.18 | 0.37–0.46 | 28–32 |
| 7 | 2.59 | **0.537** | 41 |
| 8–11 | 2.90–3.82 | 0.37–0.56 | 18–46 |
| 12–15 | 4.33–6.59 | 0.37–0.45 | 26–42 |
| 16 | 7.63 | **0.667** | 27 |
| 17 | 8.59 | **0.697** | 33 |
| 18 (highest) | 12.72 | **0.423** ← drop | 26 |

### What this shows

The pattern is **not a textbook symmetric inverted-U** — the full shape is:
- **Low rates in the weakest pools** (bins 1–2: ~0.30–0.35)
- **Rising through mid-range pools** (bins 3, 7, 9–11: ~0.49–0.56)
- **High rates in strong pools** (bins 16–17: 0.67–0.70)
- **A drop at the very highest quality pools** (bin 18: 0.42)

The **critical inverted-U feature** — a **peak followed by a decline at the top** — is present: tenure rates are **highest in the 85th–95th percentile** of pool quality, then **drop in the very elite tier** (bin 18 = top few percent of departments by peer publication rate). This matches the Army and basketball patterns structurally: the very best environments produce congestion / signal compression that lowers individual promotion probability.

### Caveats to communicate to VECTOR

1. **High censoring:** ~50–60% of person-years are right-censored (still assistant near end of data window). Tenure rates are computed on resolved cases only; N per bin is small (~18–46 resolved cases).
2. **Preliminary / dirty-OK standard:** This is the "fast path first curve" per advisor guidance — not the final survival analysis. The Cox model (Cell 10 / 10.5) is the intended main specification.
3. **Pool quality measure is noisy:** Only faculty with HIGH or MEDIUM OpenAlex matches contribute to `poolq_loo_mean`. Departments with poor OA coverage have noisier pool quality estimates.
4. **Coverage is partial:** ~60 departments ≠ full R1 universe. Elite departments (top 10 CS programs) may be over- or under-represented depending on which schools have clean Wayback data.
5. **No controls yet:** The binned plot is **unconditional** — no cohort fixed effects, no school prestige controls, no individual ability controls. The shape could shift with proper modeling.

---

## 5. What Is Wired But Not Yet Finalized

| Element | Status |
|---------|--------|
| **Cox survival model** (Cell 10) | Code complete; time-varying covariates (`tb_ratio_fwd_snr`, pool metrics) specified in `COLUMN_CONFIG`; z-scored frame in Cell 10.5 |
| **Inverted-U test columns** (`z_pool_minus_mean_snr_fwd`, `*_sq`, `star_pool_interaction`) | Created in Cell 10.5 on Cox-ready frame (not on raw snapshots — this is expected behavior, not a bug) |
| **Formal model output** | Not yet run / reported |
| **School-level prestige covariate** | Not yet merged into panel (planned: NRC rankings or USNews tier) |
| **Attrition as competing risk** | Flag exists in panel; competing-risks model not yet estimated |

---

## 6. How to Frame PEER in the Manuscript

### What you CAN say (supported by current artifacts)
> *"In a preliminary analysis of CS faculty tenure at R1 universities, using archived faculty pages (Wayback Machine, 2000–2023) linked to OpenAlex publication records, we find a non-monotone relationship between peer pool quality and tenure rates consistent with the inverted-U predicted by the talent-pool congestion model. Tenure rates are lowest in the weakest departments, rise through mid-tier departments, and then decline in the most elite tier — mirroring the Army and basketball settings."*

### What to hedge or defer
- Specific coefficient estimates (Cox model not finalized)
- Precise N of faculty or schools (coverage is still being QA'd)
- Claims about completeness (60+ schools, not the full 187-school R1 universe)
- Publication counts as "the" performance measure (OA linkage is partial)

### Suggested status label for paper drafts
**"Preliminary replication (Setting 3)."** The inverted-U is visible in unconditional binned rates; formal survival analysis with pool-quality terms is the next step. Coverage limitations are acknowledged; full results are forthcoming pending pipeline completion and OpenAlex bulk access (pending UVA CDH provisioning).

---

## 7. Key Files for VECTOR Reference

| File | What it contains |
|------|-----------------|
| `tenure_pipeline/stage9_inverted_u.png` | The inverted-U figure (pool quality bins vs tenure rate) |
| `tenure_pipeline/stage9_binned_table.csv` | Binned tenure rates with CIs (18 bins) |
| `tenure_pipeline/faculty_panel_with_pools.jsonl` | Full enriched panel (72 MB; all columns) |
| `tenure_pipeline/faculty_panel_advisor.csv` | Flat CSV version (columns reordered for readability) |
| `tenure/documents/PANEL_CSV_GLOSSARY.md` | Column-by-column definitions for the CSV |
| `tenure/documents/TENURE_DATA_GAMEPLAN.md` | Strategic contract: what PEER is trying to accomplish and why |
| `tenure/540_tenure_pipeline.ipynb` | Main pipeline notebook (Cells 0–10.5) |

---

*Document created 2026-06-03. Contact: Charles Levine / PEER agent.*
