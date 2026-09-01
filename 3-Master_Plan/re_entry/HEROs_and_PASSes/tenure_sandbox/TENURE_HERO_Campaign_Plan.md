# Tenure HERO Campaign Plan — use what we have first

**Prepared by COMPASS** (for Charles; PEER parallel on scrape bolster)  
**Last synced:** 2026-09-01  
**Status:** **Act I starting** — exploratory HERO on rsync’d May 2026 panel; scrape bolster **parallel / later**.

**Alex direction (Sep 2026):** See what tenure HERO / F-HERO can do on **existing** data before treating corpus expansion as the main task.

**Binding:** [`../../../BINDING_Selection_is_its_own_step.md`](../../../BINDING_Selection_is_its_own_step.md) — environment ≠ advancement; score ≠ select.

---

## Print stack (recommended hardcopies)

| # | Document | Path (repo root relative) |
|---|----------|---------------------------|
| **1** | **This campaign plan** | `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/TENURE_HERO_Campaign_Plan.md` |
| **2** | PEER → COMPASS data handoff | `3-Master_Plan/re_entry/20260901_PEER_to_COMPASS_tenure_hero_mac_handoff.md` |
| **3** | PEER data gameplan (strategic contract) | `tenure/documents/TENURE_DATA_GAMEPLAN.md` |
| **4** | Pipeline map (MBB mirror + v0 locks) | `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/TENURE_hero_pipeline.md` |

**Optional fifth:** `tenure/documents/TENURE_SCRAPE_AND_ADJUDICATE_FOR_DUMMIES.md` — when PEER scrape round is active.

**PDF (Mac, repo root):**

```bash
./scripts/convert_single_md_to_pdf.sh 3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/TENURE_HERO_Campaign_Plan.md
./scripts/convert_single_md_to_pdf.sh 3-Master_Plan/re_entry/20260901_PEER_to_COMPASS_tenure_hero_mac_handoff.md
./scripts/convert_single_md_to_pdf.sh tenure/documents/TENURE_DATA_GAMEPLAN.md
./scripts/convert_single_md_to_pdf.sh 3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/TENURE_hero_pipeline.md
```

---

## 0 — One sentence

On the **strict inference panel** already on Mac, plot **tenure rate vs leave-one-out (LOO) department peer quality** the same way we built **MBB HERO** after re-entry — then ask whether the **Wang arc** (phenomenon → minimal model → prediction) carries to academia.

---

## 1 — Campaign arc (four acts)

```text
Act I   Empirical HERO (resolved outcomes, v0 lock)     → NOW
Act II  Empirical F-HERO (+ optional attrition companion)
Act III H_sort / ρ diagnostic (park ASSIGN only if ρ* ≈ 0)
Act IV  Generative replay (optional — after Alex lock)
        ─── parallel track ───
        PEER: scrape bolster on Rivanna (when scheduled)
```

| Act | Question | Status | Owner |
|-----|----------|--------|-------|
| **I — HERO v0** | Tenure rate vs LOO bins on inference panel? | **First plot shipped** — review with Charles | Charles + COMPASS (Mac) |
| **II — F-HERO** | At fixed Â, rate vs department mean T̂_j? | Pending Alex Â lock | Charles + COMPASS |
| **III — ρ** | Department-level assortativity flat or not? | Pending Act I | Charles + COMPASS |
| **IV — Sim replay** | Fit λ, γ, t on frozen departments → sim tenure? | Parked | — |
| **Parallel — data** | More schools / URLs / OA coverage | Parked until chosen | PEER (Rivanna) |

**Win condition (Act I):** One **defensible** tenure HERO figure + binned table + provenance JSON under `tenure_sandbox/hero/`, with sample-loss accounting and Wilson CIs — **exploratory**, not publication-final until Alex lock.

**Not the win condition:** Re-scrape before looking; claiming inverted-U from Apr 2026 Stage 9 alone; using 106K rows without inference filter.

---

## 2 — v0 scientific lock (Charles + COMPASS, Sep 2026)

| Knob | Lock |
|------|------|
| **Input file** | `tenure/tenure_pipeline/faculty_panel_with_pools.jsonl` |
| **Filter** | `match_confidence` ∈ {HIGH, MEDIUM}; non-null `poolq_loo_mean` on assistant rows; `ever_assistant` |
| **Grain** | **Person-level** — mean LOO over assistant years (Stage 9 collapse) |
| **X-axis** | `poolq_loo_mean` → **16 quantile bins** |
| **Y (primary)** | **`tenure_event`** rate among **resolved** (Option A) |
| **Y (companion)** | **`attrition`** rate among resolved (optional second panel) |
| **Censored** | **Excluded** from rate denominator; **included** in quantile rank (`n_all`); counted in table — survival layer later |
| **ρ / homophily** | **Not parked by default** — run diagnostic in Act III; park only if tenure looks like MBB (ρ* ≈ 0) |
| **Outputs** | `tenure_sandbox/hero/` |
| **Script** | `tenure/scripts/tenure_pass_a_hero.py` |

**Resolved endings (plain language):**

- **Tenured** — promoted asst → associate/full within pipeline rules  
- **Attrited** — disappeared without that promotion  
- **Censored** — still assistant at window end → **parked for now**

---

## 3 — Plot menu (priority order)

| P | Deliverable | Spec summary |
|---|-------------|--------------|
| **P0** | Filter manifest + N table | Persons, resolved, censored, depts — console + JSON |
| **P1 ★** | `HERO_tenure_q16_inference_v0.png` | Tenure rate vs LOO Q16; Wilson CI; footer provenance |
| **P1b** | Matching CSV + `*_provenance.json` | Bin counts: n_all, n_resolved, n_censored |
| **P2** | Attrition companion PNG | Same bins, same denominator (resolved) |
| **P3** | Sensitivity: 12 vs 16 bins | Only if bins thin |
| **P4** | F-HERO | After Alex Â field lock |
| **P5** | H_sort / ρ bracket | Act III — tenure department assignment |

Each shipped plot: **PNG + CSV + provenance JSON** (MBB sandbox convention).

---

## 4 — Data & sync (no re-invention)

| Task | Command / path |
|------|----------------|
| Mac already synced | PEER verified 2026-09-01 |
| Refresh panel | `./scripts/rsync_pull_recent_hpc.sh tenure` |
| Do **not** analyze | `faculty_panel.jsonl` (2.56M snapshot rows) as hero grain |
| PEER scrape (parallel) | See [`20260901_COMPASS_to_PEER_tenure_scrape_bolster.md`](../../20260901_COMPASS_to_PEER_tenure_scrape_bolster.md) |

---

## 5 — Alex lock still open (after Act I plots)

1. Outcome **Y** for paper prose (tenure vs attrition emphasis)  
2. Panel **aperture** (years, departments) — especially vs **~56% censored** on last-ps  
3. **Â** for F-HERO slices (`pubs_year` vs cumulative)  
4. LOO pool definition confirmation  
5. Empirical-first vs generative replay scope  
6. **Censored in quantile bins?** — keep in rank + Option A rates (v0) vs resolved-only quantile / resolved-only panel — see [`TENURE_hero_pipeline.md` § censored pros/cons](TENURE_hero_pipeline.md#censored-in-quantile-bins--proscons-for-alex)

---

## 6 — Folder map (where things live)

```text
3-Master_Plan/re_entry/HEROs_and_PASSes/
  sports_sandbox/     ← MBB hero (existing)
  tenure_sandbox/         ← this campaign (NEW)
    TENURE_HERO_Campaign_Plan.md   ← you are here
    TENURE_hero_pipeline.md
    _DISPOSABLE_tenure_hero_thread.md
    hero/                 ← PNG, CSV, JSON
    fhero/                ← later

tenure/tenure_pipeline/   ← input JSONL (rsync)
tenure/scripts/           ← tenure_pass_a_hero.py
tenure/documents/         ← TENURE_DATA_GAMEPLAN (PEER)
```

---

## 7 — Thread log

| Date | Entry |
|------|--------|
| 2026-09-01 | Campaign plan created; Alex “existing data first”; v0 locks; folder scaffold approved. |
