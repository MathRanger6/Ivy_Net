# Army porch — band of excellence & θ (Charles → VECTOR)

**Date:** 2026-09-24  
**Audience:** VECTOR — narrative / Act I refresh for Charles + Alex outline revisit  
**Charles print memo (full detail):** `talent/re_entry/BAND_OF_EXCELLENCE_ARMY_PORCH.md` (repo path; Charles may PDF separately)

**Status:** Concept locked in chat; plot-layer code **not yet run** (Army **PDE → Vantage** transition; Vantage not online).

**VECTOR access (Sep 2026):** Repo-connected via **ChatGPT desktop** on Mac — read this file in-repo; **no zip handoff**.

---

## Why VECTOR should care

Act I (Army) is the **scientific origin**. Charles and Alex are sharpening **where congestion is supposed to bind**: not the full captain cross-section from Â = 0 upward, but the **band of excellence** — officers actually competing for **scarce top blocks** inside **real senior-rater ponds**.

This does **not** replace the flipbook’s core HERO claim. It **sharpens** which panels carry mechanism vs descriptive porch.

---

## One-sentence claim (story beat)

**Congestion binds where scarce distinction is at stake** — top blocks and promotion among officers senior raters are really sorting — not across every captain with an OER file.

Tag for outline: **🟡 PARTIAL** until Vantage re-run with optional own–Â = 0 filter on panels 7–8–9; **✅ HAVE** for conceptual framing and existing Run 1–3 matrix (straight LOO / eval-thru / peer-zero sensitivity).

---

## Three filters (VECTOR must not conflate in prose)

| Filter | Meaning |
|--------|---------|
| **Missing SNR history** | `tb_ratio_fwd_snr` = NaN — no SNR-checked evals — **not** zero |
| **Own Â = 0** (proposed plot gate) | Had SNR evals, **never** top-blocked — drop **ratee** from congestion cohort (panels 7–8–9) |
| **Peer Â = 0** (Run 3) | Drop **peers** from pool mean/size in feather — different estimand |

**Binding:** Hero porch = Layer A **outcomes**; these gates define **who is in the conditional congestion read**, not causal peer effects.

---

## Panel roles (Act I porch deck)

| Panel | Role for story |
|-------|----------------|
| **2** | Â / T̂ distributions — full finite sample (transparency) |
| **5** | H_sort — assortativity / pool overlap (PD41 adjacent) |
| **7** | **CCT** — fixed high Â band, promotion vs pool LOO → **primary congestion test** |
| **8** | **Elite pond** — top Â × upper LOO → **band of excellence** |
| **9** | **HERO** — unconditional porch; **descriptive**; lower bins unreliable if own–Â = 0 dropped |

**Narrative order inside Act I:** phenomenon (2, 9 full) → **conditional mechanism (7, 8)** → assortativity (5) as Alex PD41 thread allows.

Charles lock unchanged: **Army HERO shape locked** (Sep 16); this memo adds **which Army slides argue congestion** vs **which show the raw porch**.

---

## θ (basketball model) ↔ Army band

### Model

Team congestion uses viability: \(L^C = \mathrm{mean}\,\sigma(\gamma(A-\theta))\). **θ** = who counts as a viable peer in the **generative** story.

### MBB calibration (what logistic/Bernoulli MLE actually fits)

PD21 Bernoulli MLE fits **λ, γ, t** on fixed rosters; **θ is usually preset** (K/N quantile or median drafted perf), not a free MLE parameter. See `sports/scripts/pd21_draft_bernoulli_mle.py` and `05_Three_Kinds_of_Model.md`.

### Army (today)

- **Discrete θ gates:** ever-TB (Â > 0), CCT band, elite top % — not yet smooth σ(γ(Â−θ)) on SNR pools.
- **Outcome:** competing risks / CIF — not Bernoulli draft; **do not** claim PD21 was ported to Cox Cell 12.
- **Future extension:** calibrate θ̂ from promoted or ever-TB’d officers; optional Army \(L^C\) on SNR pools; long-run score→select replay on fixed empirical pools.

**Cross-domain line for outline:** Basketball **θ** and Army **band of excellence** are the **same scientific object** (viability band for scarce advancement); Army implements it **empirically** before full generative closure.

---

## PD41 assortativity link

PD41 factorial (see `3-Master_Plan/new_VECTOR_work/VECTOR_PD41_Assortativity_Scientific_Brief.md`) tests **ρ vs λ vs K/N** on MBB with **θ frozen**.

Army **Panel 5 (H_sort)** is the **empirical sorting** read on senior-rater pools — complementary, not a substitute for the eight-cell sim. When writing Act I ↔ Act IV bridges:

- MBB PD41 = **does assortative assignment preference matter for congestion effects?**
- Army panel 5 + 7–8 = **what does sorting / congestion look like in the viability band on real promotion data?**

---

## Army compute environment (Sep 2026 — update G1 narrative)

Charles **cannot** run Army data on Mac or export feathers/plots as data files.

| Environment | Status |
|-------------|--------|
| **Mac (Dropbox)** | Scrubbed code + docs only |
| **Old PDE** | Runnable; **uploads blocked** — transcription only |
| **Vantage** | Not online; will start from **frozen repo snapshot**; then **upload Mac files** + screenshot results |

**G1 refresh:** 5-run pool matrix (Runs 1–3 complete on old PDE; Runs 4–5 minus-mean pending). Porch PNGs refresh when Vantage live — not blocking VECTOR **story outline**, but tag Act I figures **🟡 PARTIAL** until then.

---

## Suggested outline tags (VECTOR)

| Beat | Tag | Note |
|------|-----|------|
| Army HERO inverted-U / porch shape | ✅ HAVE | Charles lock Sep 16 |
| Pool grain sensitivity (legacy vs eval-thru vs peer-zero) | 🟡 PARTIAL | Matrix runs done; mosaic/compare on Vantage |
| Band of excellence / conditional CCT + elite | 🟡 PARTIAL | Concept + Act II scripts; own–Â = 0 toggle not coded |
| Army θ / L^C generative closure | ⬜ NEED | Extension; discrete gates OK for near-term talk |
| PD41 eight-cell sim | 🟡 PARTIAL | Brief written; execution not approved |

---

## Thread log

| Date | Entry |
|------|--------|
| 2026-09-24 | Charles + COMPASS: band of excellence memo; θ vs MLE; VECTOR addendum for transition revisit |
