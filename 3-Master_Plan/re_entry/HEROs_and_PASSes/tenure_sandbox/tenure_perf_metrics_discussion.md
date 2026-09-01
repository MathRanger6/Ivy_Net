# Tenure performance metrics — discussion memo

**Created:** 2026-09-01  
**Audience:** Charles + COMPASS  
**Status:** Living spec fork — not yet locked for Act III (ρ) or F-HERO  

**Context:** Slow-start Q&A after tenure porch BDPs (overlap, distributions) and Q16/Q20 HERO. Clarifies what v0 **actually uses** vs what MBB last-ps does, and lists peer-pool / perf alternatives.

**Related:** [`TENURE_hero_pipeline.md`](TENURE_hero_pipeline.md) · [`TENURE_HERO_Campaign_Plan.md`](TENURE_HERO_Campaign_Plan.md) · `tenure/tenure_pipeline/pool_metrics.py` · [`tenure/documents/PANEL_CSV_GLOSSARY.md`](../../../../tenure/documents/PANEL_CSV_GLOSSARY.md)

---

## TL;DR

| Question | v0 answer |
|----------|-----------|
| Last-ps like MBB? | **No** — HERO collapses **mean LOO over all assistant years**; BDP overlap uses **all assistant person-years**. |
| Cumulative tenure pubs? | **No** for pool / HERO / H_sort — we use **`pubs_year`** (annual). `pubs_cumulative` exists in panel but is unused in v0. |
| Who is in the peer pool? | **`rank == assistant` only**, OpenAlex-matched subset for quality; pool key = **`(uni_slug, year)`** (university × year in code; docs sometimes say “dept-year”). |
| All professors in dept? | **Not in v0** — associates/full not in pool; true department field not in pool key today. |

---

## 1. What perf metric are we using? (Not last-ps)

### MBB reference (reigning hero)

- **Grain:** one row per athlete = **last player-season** (“last-ps”).
- **Perf:** PPM (or ladder metric) **z-scored within season**.
- **Pool pressure:** `poolq_loo` on that cross-section.

### Tenure v0 (locked HERO + porch BDPs)

Two grains — **neither is last-ps:**

| Layer | Unit | X / ability |
|-------|------|-------------|
| **Pass A HERO** (Q16 default, Q20 robustness) | **One person** | **Mean `poolq_loo_mean`** over **assistant years** with non-null LOO |
| **Porch BDP / interval overlap / H_sort** | **Assistant person-year** | **`pubs_year`**, z-scored **within calendar year** |

**`poolq_loo_mean`** at year *t* (Cell 8):

$$
\text{poolq\_loo}(i,t) = \text{mean}\big(\texttt{pubs\_year}(j,t)\big)
$$

for OA-matched assistants *j* in the same pool as *i*, *j ≠ i*.

So HERO x-axis is **time-averaged annual peer pressure**, not “final cumulative pubs at exit.”

---

## 2. Annual pubs vs cumulative — and postdocs with prior work

### Panel fields (OpenAlex)

| Field | Meaning |
|-------|---------|
| **`pubs_year`** | Publications attributed to this person **in calendar `year`** |
| **`pubs_cumulative`** | Running total through `year` (person-level spell; see glossary for gap caveats) |

**v0 pool metrics, HERO, and overlap H_sort use `pubs_year` only.**

### Interpretation

- **Annual `pubs_year`** ≈ *“Who are my publishing peers **this year**?”* — contemporaneous comparison on the assistant clock.
- **Cumulative** ≈ *“Who has the bigger **career stock**?”* — confounded by **years as assistant** (`years_as_asst_so_far`) and time on market.

### Arriving with publications already (postdoc CV)

The panel only observes people **once they appear as assistant** in scrape snapshots.

- Prior career productivity can show up as **high `pubs_year` in early assistant years** (continued output), not as a separate “CV at hire” covariate unless we build one.
- We do **not** currently strip pre-hire pubs or flag “first assistant year.”

**Design fork (parked):** homophily on **cumulative at hire** vs **annual flow on clock** — different economic stories; not interchangeable.

---

## 3. Who is in the peer pool?

### v0 (Cell 8 — `pool_metrics.py`)

- **Members:** rows with **`rank == assistant`** in that `(uni_slug, year)`.
- **Quality computed on:** OpenAlex-matched subset (`openalex_id` present).
- **Excluded from pool:** associate, full, adjunct, unknown rank (for pool membership; they may still appear elsewhere in panel).
- **Pool key in code:** `(uni_slug, year)` — **university-wide assistant cohort that year**, not department slug (department may be implied by scrape URL but is **not** the pool partition key today).

Docstrings say “dept-year”; implementation is **uni × year**. Worth keeping explicit in prose and in any Alex brief.

### Charles’s question: all professors in the department annually?

**Yes — that is a different peer environment**, not a tweak of the current one.

| Spec | Pool members | Perf | Question |
|------|--------------|------|----------|
| **A — v0 (locked HERO)** | Assistants only | `pubs_year` (LOO mean → HERO) | Tenure-track **cohort** pressure among peers |
| **B** | Assistants only | `pubs_cumulative` | Sorting on **stock** among assistants (tenure clock confound) |
| **C** | **All ranks** (asst + assoc + full) | annual or cumulative | Full **departmental** publication environment |
| **D** | Assistants only | last assistant year only (“tenure last-ps”) | MBB-style **exit cross-section** |

**Spec C** is often closer to “who do I compare myself to in the building?” but requires:

- roster definition for **all ranks** at uni/dept × year;
- perf rule for seniors (annual vs cumulative; active researcher filter);
- OpenAlex coverage asymmetry (seniors may be missing or mis-linked).

**Not wired in v0.** Treat A vs C as **two environments** (Alex: environment ≠ advancement), not one blended plot.

---

## 4. Link to homophily (H_sort) and ρ

**Empirical sorting index (H_sort)** = share of cross-person variance in z-scored perf explained by pool assignment (same formula as MBB Grandchild readout).

**Porch overlap (infHM):** H_sort ≈ **0.173** on **`pubs_year` z within year**, pools = uni × year, assistants + OA.

**Homophily parameter (ρ)** in Grandchild ASSIGN is **not** H_sort. ρ is **calibrated** so simulated ASSIGN reproduces empirical H_sort (PD21 recipe), using:

- ability vector (here: `pubs_year` z),
- empirical roster caps per pool,
- Grandchild stub assignment.

If we change perf (annual → cumulative) or pool (assistants only → all ranks), **H_sort and ρ* both change** — that is an **Act III spec lock**, not a cosmetic relabel.

**Campaign policy:** Do **not** assume tenure ρ ≈ 0 like MBB PPM; H_sort ≈ 0.17 already suggests nontrivial sorting on the v0 partition.

---

## 5. Recommended sequencing (Charles + COMPASS)

1. **Keep Q16 HERO + infHM BDPs on Spec A** until Alex sees shape — already locked.
2. **Q20** — inspect dip robustness only; same Spec A perf/pool.
3. **Before ρ bracket:** decide whether Act III repeats **Spec A** or adds **Spec C** (or B/D) as a **parallel** porch, not a replacement, unless Alex reprioritizes.
4. **F-HERO (Act II):** fixed Â slice + department mean pubs — orthogonal but should **cite same pool/perf language** as hero env.

---

## 6. Open decisions (YOU ARE HERE)

| ID | Decision | Options | Default |
|----|----------|---------|---------|
| **P1** | HERO / pool perf | `pubs_year` vs `pubs_cumulative` vs rate (pubs / years on clock) | **`pubs_year`** (v0) |
| **P2** | Pool membership | assistants only vs all ranks | **assistants only** (v0) |
| **P3** | Pool geography | uni × year vs true department × year | **uni × year** (code today) |
| **P4** | HERO grain | mean LOO over spell vs last assistant year | **mean over spell** (v0) |
| **P5** | ρ calibration partition | same as P1–P3 vs separate “environment” spec | **defer** until P1–P3 reviewed with Alex |

---

## Thread log

| Date | Entry |
|------|--------|
| 2026-09-01 | Initial memo from chat: last-ps vs tenure grains; annual vs cumulative; assistant-only vs full-dept pool; ρ link. |
