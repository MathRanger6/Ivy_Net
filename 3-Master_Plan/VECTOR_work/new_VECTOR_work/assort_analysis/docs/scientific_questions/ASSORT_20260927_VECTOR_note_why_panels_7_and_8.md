# Note for VECTOR — why we created MBB data-story panels 7 and 8

**From:** Charles (via SCOUT, September 27, 2026)  
**Audience:** VECTOR — keep this distinct from the paused eight-cell assort experiment and from SCOUT provenance memos.  
**Status:** Narrative and design intent only; no execution authorized here.

---

## What “panels 7 and 8” mean

These are **slots 7 and 8** in the men's basketball **3×3 data-story deck** (`MBB_DATA_STORY_reigning_3x3.png`), read after row 1 (population / ability / LOO support) and row 2 (draft-mass ECDF, team interval overlap, roster size). Full talk track: [`3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/data_story/MBB_DATA_STORY_plot_highlights.md`](../../../../re_entry/HEROs_and_PASSes/sports_sandbox/data_story/MBB_DATA_STORY_plot_highlights.md).

They are **not**:

- The paused **ASSORT** simulation or 2015 sorting-index diagnostics in `assort_analysis/outputs/`.
- **530_sports_pipeline** notebook “Cell 7 / Cell 8” (SR merge and legacy interval-overlap port).
- Identified causal peer-effect estimates.

They **are** conditional **outcome** plots on the **leave-one-out teammate pool quality (poolq_LOO)** axis, with **own ability (Â) held fixed** within chosen gates — the “Act II” congestion read in the dissertation story.

---

## Why we added them (Charles’s intent)

### 1. Full HERO (panel 9) is the wrong sole carrier for the mechanism pitch

Panel 9 is the **reigning full-cohort HERO**: draft rate vs poolq_LOO for everyone passing min20 · mg10 · last-ps filters. It answers “what does the **whole** eligible population look like on the environment axis?”

Alex’s congestion story for **who actually competes for scarce draft slots** lives in the **upper ability tail**, where most draft mass concentrates (panel 4 ECDF). Panels **7** and **8** **zoom** to that region with **different scientific questions** and **different binning**, instead of forcing one curve to carry Squid–Jackal logic, elite-tail downturn, and full-sample HERO shape at once.

**For VECTOR:** Reproducing or debating panel 9’s quadratic / β₂ is **not** the same task as the **necessity-of-ρ** factorial in [`VECTOR_PD41_Assortativity_Scientific_Brief.md`](../../VECTOR_PD41_Assortativity_Scientific_Brief.md). Panel 9 is descriptive hero-layer evidence; the eight-cell design is assignment + score + select.

### 2. Panel 7 — fixed high-ability **CCT band** (Squid vs Jackal)

| Design choice | Rationale |
|---------------|-----------|
| **Who:** PPM z ∈ **[2, 3]** within season (narrow high-Â slice, ~top 2–3% of panel; **subset of** top 7%) | Tests **conditional competitive congestion (CCT)** among players who are already similarly talented — the “band of excellence” where marginal draft chances might depend on **peer pond**, not on being mediocre vs star. |
| **X-axis:** poolq_LOO | Environment = **teammates’ ability excluding self**, aligned with hero/score narrative (not raw team mean T̂_j). |
| **Binning:** QTL16 on LOO **within the band** | Prespecified ventiles for **mid-pond vs top-pond** comparison (Squid vs Jackal); primary read is **CCT = YES/NO** on draft rates, not a fitted global parabola. |

**Why it exists separately from panel 8:** The Â gate is **tighter and higher** (fixed z window with ceiling at 3). It targets “among very high Â players, do **middle** LOO ponds beat **top** LOO ponds?” — the classic CCT signature — without mixing in the broader elite pool or piecewise tail bins.

### 3. Panel 8 — **elite pond** (top 7% Â, LOO tail shape)

| Design choice | Rationale |
|---------------|-----------|
| **Who:** **Top 7%** Â (pooled percentile on PPM z; wider than panel 7’s z ∈ [2, 3]) | Covers essentially all **elite** players who carry draft mass, not only the z ∈ [2, 3] slice. |
| **X-axis:** poolq_LOO (same family as panel 7 and 9) | Keeps row 3 of the deck **LOO-aligned** for Alex screening. |
| **Binning:** piecewise **4+7** on LOO | Tuned to read **plateau → peak → downturn** in the **highest-LOO** tail among elites — the “elite pond” keeper (Critical Keeper slot in the manifest). |

**Why it exists separately from panel 7:** Different **Â gate** (broader elite cut vs narrow z band), different **binning** (PW 4+7 vs QTL16), different **question** (extreme LOO tail downturn among elites vs Squid–Jackal within a matched band). Panel 8 is **not** “panel 7 with LOO swapped in”; there was no prespecified run of top-7% Â + PW 4+7 on LOO until this slot was created.

### 4. Narrative order we want VECTOR to respect

From [`VECTOR_PD41_Assortativity_Scientific_Brief.md`](../../VECTOR_PD41_Assortativity_Scientific_Brief.md) §6b (Army parallel, same deck logic):

1. **Full-sample phenomenon** — panels 2, 3, 9 (distributions + full HERO).
2. **Conditional mechanism comparisons** — **panels 7 and 8** (where draft/tenure decisions actually concentrate).
3. **Empirical sorting** — panel 5–style **H_sort** / interval overlap — **complements** but **does not replace** the ρ factorial or the conditional outcome panels.

Panels 7–8 carry the **proposed mechanism argument** in slides: congestion may bite where ability is already high and selection is scarce. They do **not** prove assortative assignment preference (ρ) or identify causal peer effects.

---

## Relation to the current ASSORT campaign

| Topic | Panels 7–8 (MBB deck) | ASSORT workspace (2015 freeze) |
|-------|------------------------|------------------------------|
| Outcome | Ever-draft rate vs LOO bins | Simulated **top-K** winners under ρ, λ, scarcity |
| Ability axis | Within-season PPM z gates | Frozen `ability_standardized` / PPM construction |
| Sorting | Descriptive H_sort elsewhere (panel 5, overlap) | **H_sort** diagnostics, rotation audits, metric provenance |
| Goal | Explain **where** in Â-space conditional curves matter for Alex | Test **whether ρ is necessary** for congestion to move winners |

Do **not** tune ASSORT population rules to reproduce panel 7 or 8 bin counts. Do **not** treat historical BPM **H_sort** ladder values as justification for the same gates on the audit file.

---

## Army and tenure (same slot numbers, different domains)

- **Army (PD41 §6b):** Panels 7–8 mirror the **same narrative roles** — fixed high-ability CCT band and elite-pond conditional — on senior-rater pools; evidence refresh was partial as of September 24 handoff.
- **Tenure PD29 deck:** Panels 7–8 are **scaled probes** (wider z band, top 20% Â for N); see [`tenure_sandbox/data_story/TENURE_DATA_STORY_plot_highlights.md`](../../../../re_entry/HEROs_and_PASSes/tenure_sandbox/data_story/TENURE_DATA_STORY_plot_highlights.md).

MBB panels 7–8 remain the **canonical reference** for what those slot numbers mean in Charles’s story unless a domain memo says otherwise.

---

## Honest footnotes (do not hide from VECTOR)

- Deck **panel 7–8** artifacts often use **2011–21 +DFT** for a sharper Squid–Jackal / tail read; **panel 9** uses the **09–21 last-ps** reigning lock — window mismatch is intentional, not sloppiness. Compare PNGs under `data_story/_compare_0921/` when aligning windows.
- Panel 7 **β₂** (within-band LPM on LOO) is optional annotation; primary CCT read is **Squid vs Jackal rates**.
- Low measured **H_sort** on PPM does **not** falsify the **need** for panels 7–8; those panels hold Â fixed and ask about **outcomes vs LOO**, not variance decomposition by team label alone.

---

## One sentence for VECTOR

**We created panels 7 and 8 so the dissertation could show two prespecified, ability-fixed conditional stories (CCT in a high-Â band and elite-pond LOO tail behavior) where draft mass actually lives — without overloading the full-cohort HERO or conflating those descriptive outcome curves with the assortativity necessity experiment or with H_sort alone.**

---

*Charles-facing note; update PD41 §6b or COMPASS deck memos only if Charles asks for a merge.*
