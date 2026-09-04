# MBB data story — plot highlights (talk track)

**Deck:** `MBB_DATA_STORY_reigning_3x3.png` · read **top-left → bottom-right**  
**Reigning HERO lock:** 09–21 · last-ps · EW16 poolq_LOO · min20 · mg10 · ever-Y

Use one sentence per panel when screening a domain; two if Alex asks “why is this here?”

---

## Row 1 — Who is in the pond?

### 1 · Cohort

**Highlight:** This is the **decision universe** — one row per athlete at final college season, POST-QC filters, and the outcome we care about (ever drafted).

**Say:** “N = 22,795 last-ps rows, 615 ever-drafted — everything below is about whether **peer context** predicts draft beyond **own ability**.”

---



### 2 · Â_i and T̂_j

**Highlight:** Separates **individual talent** (Â) from **team-level realized talent** (T̂_j, includes self).

**Say:** “Draftees sit right-shifted on ability; team talent has its own distribution. HERO’s environment axis is **LOO peers**, not raw T̂_j — this panel sets up *who* vs *where*.”

---



### 3 · poolq_LOO distribution (3a histogram · 3b ECDF)

**Highlight:** Shows the **support** of the peer-context variable — where LOO teammate quality lives on the z-scale, and whether drafted players come from systematically different ponds.

**3a (histogram, no winsor):** Raw LOO support — full spread without 1–99% clip artifacts at the tails. Blue = all last-ps rows; purple +DFT overlay = rows on teams with any ever-drafted athlete.

**3b (ECDF):** Same comparison in cumulative form. If the **+DFT curve sits above and left** of the full-panel curve, draftees systematically come from **higher peer ponds** — the entire drafted subpopulation is shifted toward better LOO, not just a histogram bump in one bin.

**Value:** Before any binning story, you need LOO to be **non-degenerate** and to see that draftees **sort into better teammate contexts** on average — a descriptive prerequisite for HERO, not the hero curve itself.

**Say:** “Left: where LOO mass lives. Right: drafted players’ ponds are **stochastically better** — the +DFT curve rises faster. That’s the input side before we bin draft *rates*.”

**Not:** An outcome curve — descriptive **input** distribution only (reigning HERO lock still winsorizes LOO at fit time; this panel is porch truth-telling).

---



## Row 2 — Geometry and who carries draft mass



### 4 · Draft mass vs Â (ECDF)

**Highlight:** **Where draft picks come from in ability space** — cumulative share of all drafts accounted for by ability tiers.

**Value:** Justifies **fixing Â bands** later (CCT, elite pond): most draft mass is **not** uniform across ability — a thin slice of Â carries disproportionate draft probability. Without this, “fix Â at z∈[2,3]” or “top 7%” looks arbitrary.

**Say:** “Most draft capital concentrates in the upper ability tail — so when we **hold ability fixed** in panels 7–8, we’re zooming where the **marginal draft decision** actually happens, not the whole roster.”

**Pairs with:** Panel 2 (marginal Â) but Panel 4 answers **draft-weighted** importance, not headcount.

---



### 5 · Team interval overlap

**Highlight:** **Sorting overlap** — how much team talent windows stack on the same roster (assortment / congestion geometry).

**Say:** “Teams aren’t isolated talent bins — intervals overlap. That’s why LOO (who’s left when you remove self) matters more than ‘my team’s average’ alone.”

---



### 6 · Team roster size |T_j|

**Highlight:** **Pond size** — how many meaningful minutes-players define each team-season LOO pool.

**Say:** “LOO is computed over ~12–13 rotation players per team-season (min20). Peer context is a **real roster**, not an abstract league average.”

---



## Row 3 — Conditional stories (all LOO-axis)



### 7 · CCT P1 — fixed Â z ∈ [2,3] · QTL16 · LOO

**Highlight:** **Squid vs Jackal within a matched ability band** — mid-pond vs top-pond LOO ventiles, holding **PPM z ∈ [2, 3]** fixed (upper tail with a **ceiling at z = 3**, not a ventile label).


| Knob     | Panel 7                                                                                                       |
| -------- | ------------------------------------------------------------------------------------------------------------- |
| Who      | **Fixed z window** — PPM z ∈ **[2.0, 3.0]** (within-season z; **not** “ventiles 2–3”)                         |
| Share    | **~2.4%** of +DFT all-ps panel (11–21 deck: n = 425); **⊂ top 7%** (everyone in [2, 3] is above the top-7% cut z ≳ 1.5) |
| Binning  | **QTL16** on poolq_LOO *within that band*                                                                     |
| Question | Among similarly talented players, do **mid-LOO** ponds draft **more** than **top-LOO** ponds? (CCT signature) |
| Read     | Squid (mid) vs Jackal (top) draft rates; CCT = YES if Squid > Jackal                                          |
| Optional | Within-band LPM on raw poolq_LOO: **β₂ < 0** (concave) — supports CCT but **not** the prespecified test (deck: β₂ ≈ −0.49) |


**Say:** “Panel 7 is **Act II conditional congestion** on a **narrow z slice** [2, 3] — roughly the top **~2–3%** of ability, capped below the extreme z > 3 tail. Same LOO axis, but a **tighter Â gate** than panel 8’s top 7%. Classic CCT Squid–Jackal test — not the full HERO curve.”

**Not:** Top-7% elite gate; not piecewise tail bins; not the reigning 09–21 last-ps aperture. Deck uses **11–21 +DFT** (sharper Squid–Jackal gap). **09–21 still CCT=YES** (35% vs 28%) — side-by-side: `_compare_0921/COMPARE_panel7_CCT_z23_9_21_vs_11_21.png`.

---



### 8 · Elite pond LOO — top 7% Â · PW 4+7 · LOO

**Highlight:** **Elite players only** — draft rate vs **peer context** with **piecewise tail** binning on LOO (coarse low + fine high LOO).


| Knob     | Panel 8                                                                       |
| -------- | ----------------------------------------------------------------------------- |
| Who      | **Top 7% Â** (pooled percentile cut on PPM z; deck 11–21: z ≳ **1.49**)     |
| Share    | **7.0%** of +DFT all-ps panel (11–21 deck: n = 1,237) — **wider** than panel 7 |
| Binning  | **PW 4+7** on poolq_LOO (piecewise tail — not QTL, not EW16)                  |
| Question | Among elites, does draft rate **rise then fall** in the **highest-LOO** tail? |
| Read     | Plateau → peak → **downturn** in top LOO bins (+DFT 11–21: 25% → 14% tail)    |


**Say:** “Panel 8 is the **elite-pond keeper** — same LOO axis as HERO, but the explicit **top 7%** Â gate (broader than panel 7’s z ∈ [2, 3] slice) and PW 4+7 bins tuned for the **elite tail dip**.”

**Compare windows:** `_compare_0921/COMPARE_panel8_elite_top7_9_21_vs_11_21.png` — downturn visible in both (09–21: 26% → 17% tail; 11–21 deck: 25% → 14%).

---



### 7 vs 8 — one-liner contrast

**Panel 7:** Among **very-high-Â** players (**z ∈ [2, 3]**, ~top 2–3% · capped at z = 3), do **middle** peer ponds beat **top** peer ponds? → **CCT / Squid vs Jackal**.  
**Panel 8:** Among **elite** players (**top 7%** Â, z ≳ ~1.5), what happens at the **extreme high-LOO** tail? → **Elite pond downturn**.

Same **LOO x-axis family**; different **Â gate** (panel 7 is a **narrower, higher** subset of panel 8), **binning**, and **question**.

| Â gate | Definition | +DFT 11–21 (deck) | Reigning 09–21 last-ps ALLT |
| ------ | ---------- | ----------------- | --------------------------- |
| Panel 7 | z ∈ **[2, 3]** | 425 rows (**2.4%**) | 733 rows (**3.2%**) |
| Panel 8 | **Top 7%** | 1,237 rows (**7.0%**) · z ≳ 1.49 | 1,596 rows (**7.0%**) · z ≳ 1.65 |

---



### 9 · HERO (Pass A · EW16 · LOO) — finale

**Highlight:** **Full-panel environment curve** — draft rate vs poolq_LOO for everyone passing filters (not ability-fixed).

**Say:** “Panel 9 is the **reigning HERO** — middle rise, flat elite LOO tail on POST-QC panel; β₂ ≈ +0.0017 (not concave on this spec). Panels 7–8 explain *where* in Â-space the interesting conditional shapes live.”

---



## 30-second domain screen (Alex)

1. **Population sane?** → 1, 2, 6
2. **Environment variable sane?** → 3
3. **Draft mass justifies zoom bands?** → 4
4. **Assortment / overlap?** → 5
5. **Act II congestion?** → 7
6. **Elite tail on LOO?** → 8
7. **HERO shape?** → 9

**Verdict strip:** HERO middle rise + flat/dip elite tail; CCT band shows Squid vs Jackal; elite pond shows LOO tail drop among top 7%.

---



## Footnotes for honest slides

- Panels **7–8:** 2011–21 +DFT (deck); panel **9:** 09–21 last-ps ALLT (reigning lock). Row 3 is **LOO-aligned**; window/pop differ slightly.  
- **09 vs 11–21 compares** (same spec, +DFT all-ps): `_compare_0921/COMPARE_panel7_*.png`, `COMPARE_panel8_*.png`; source PNGs `*_9_21.png` / `*_11_21.png`.  
- Panel 7 **Â gate** = fixed **z window** [2, 3], not ventiles; **⊂ top 7%**. Panel 8 = **percentile top 7%**.  
- Panel 8 binning = **PW 4+7**, not QTL16 or EW16. Panel 7 binning = **QTL16** within the z band.  
- Panel 7 **β₂** (within-band LPM on poolq_LOO) is optional annotation only; primary read = **Squid vs Jackal / CCT=YES**. Panel 9 **β₂** is full-panel HERO curvature — different sample and question.

---
