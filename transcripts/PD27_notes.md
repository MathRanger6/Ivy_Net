# Paper Directions 27 — my read (Aug 27, 2026)

**Source:** `transcripts/20260827_Paper_Directions_27_otter_ai_transcript.docx` (~3:46)  
**Figure shown:** [`HERO_ew16_allt_min20_mg10_09_21_last_ps_perm_loo_ever_lastps_ew16.png`](../3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/hero/HERO_ew16_allt_min20_mg10_09_21_last_ps_perm_loo_ever_lastps_ew16.png)  
**Context:** Short porch check-in — Charles showed Alex the **09–21 · last-ps · EW16 HERO** after equal-width bar styling (hue by **n**, counts on bar face) was ported from APGMS/ARGMS minutes plots.  
**Prior:** [`PD25_notes.md`](PD25_notes.md) · [`PD23_notes.md`](PD23_notes.md) · [`../3-Master_Plan/re_entry/_DISPOSABLE_Alex_hero_population_thread.md`](../3-Master_Plan/re_entry/_DISPOSABLE_Alex_hero_population_thread.md) · [`../3-Master_Plan/re_entry/SCOUT_and_COMPASS/20260827_SCOUT_to_COMPASS_2009_21_aperture.md`](../3-Master_Plan/re_entry/SCOUT_and_COMPASS/20260827_SCOUT_to_COMPASS_2009_21_aperture.md)

**Process lock (Charles, Aug 27):** Transcript captured below. **No code until Charles + COMPASS triage** — some items are **not appropriate yet** (see §Feedback items).

---

## Headline

Alex **loved the figure design** — bar styling, readability, sideways **n** on the bar face (“very strong”). Two engineering asks: **real x-axis values** in natural equal-width space (not bin index 1–16), and a **clean deck version** without the provenance footer. Two science threads: **positive β₂** (flat, not concave on 09–21) needs interpretation; **lower-echelon bins** deserve diagnostic work (Charles had been focused on the elite tail).

> **Alex one-liner:** “I love the figure overall … This is a very strong [figure].”

---

## Figure spec (what Alex saw)

| Knob | Value |
|------|--------|
| Plot | **HERO** — mean ever-draft rate vs **poolq_loo** (LOO teammate perf z) |
| Binning | **EW16** (equal width on observed poolq_loo range) |
| Seasons | **2009–2021** (`09_21` slug) |
| Panel | **last-ps** (one row per athlete, final college season) |
| Population | **ALLT** (full panel; not +DFT) |
| Filters | min20 · mg10 · winsor 0.01–0.99 · PPM z within season |
| n / K | n ≈ 22,795 athletes · K ≈ 615 draftees |
| LPM readout (on figure) | β₂ ≈ +0.00172 — **flat / not concave** on this panel |

**Style elements Alex praised:**

- Bar **face color ∝ bin n** (Blues; sparse bins pale, dense dark)
- **Bin population on bar face**, rotated sideways (not floating above)
- Overall **readability** — no more Stack Overflow for label placement

**Current gaps Alex flagged:**

- X-axis still shows **bin index 1–16**, not **real poolq_loo values**
- **n** labels: **centered horizontally** on each bar; **bottom-justified** on the bar face (Otter said “left justified” — Charles read: **bottom**, not left)
- Full **provenance strip** needed for lab work; Alex also wants a **presentation-clean** export

**Code path:** `pass_a_empirical_bundle.py` — `_paint_roster_bars()` when `--poolq-binning equal_width`.

---

## Transcript arc (~3:46)

1. **X-axis / natural space (00:05–01:15)** — Alex: use real variable values on x, not “bin 1 2 3 …”; label “average T̂_j” (Otter: “T e t j”). Charles: for equal width, bars stay equal width only in **natural space**; quantile would need unequal visual widths if axis is honest. Alex agrees; notes **n** labels need **bottom justification** on the bar face (may have looked vertically off).
2. **X-axis reference point (01:15–01:31)** — Open question: when showing **real values** on x, anchor ticks/labels at **bin corner (edge_lo / edge_hi)** vs **bin center**? *(Charles read, Aug 27: this is about **axis labeling**, not LPM fit.)*
3. **Style + deck version (01:31–01:53)** — Alex loves it; wants version **without metadata clutter** around the plot.
4. **β₂ positive (01:53–02:18)** — Charles: LPM quadratic second coefficient **positive** → not inverted-U on this panel. Alex: “We are going to have to think about what this means.”
5. **Lower echelons (02:18–03:20)** — Charles: other plots had **spikes in lowest bins** (sometimes highest bar in bin 1). Alex: “Do a little bit of work on that … understand what’s happening” — not necessarily data error; could be signal.
6. **Wrap (03:20–03:40)** — Alex reaffirms love of figure; Charles notes iterative n-label placement (“on the face … turn him sideways”).

---

## Alex reactions — what landed

| Topic | Alex (paraphrase) | Charles / COMPASS read |
|-------|-------------------|-------------------------|
| **Overall design** | “I love the figure overall … very strong.” | Lock EW styling for deck-quality HERO |
| **Hue + n labels** | Cuts matplotlib fiddling; sideways on bar face works | Already shipped; minor alignment tweak pending |
| **Real x-axis** | Real values, not bin index; natural EW space | **A** for EW plots once axis variable confirmed |
| **Axis label “average T̂_j”** | Said on call | **B** — figure is **poolq_loo HERO**, not T̂_j F-HERO; likely Otter/generic or Alex naming the *family* of plots |
| **n label alignment** | **Centered** on bar; **bottom-justified** on bar face, slightly raised from baseline | **A** — vertical anchor tweak only (horizontal center is correct) |
| **X-axis tick reference** | Corner vs center — “think about which is right” | **B** — where to place **real-value** x labels/ticks (edge vs midpoint), not LPM anchor |
| **Clean deck version** | Strip footer / provenance for slides | **A** — export flag or sibling PNG |
| **β₂ > 0 on 09–21** | “Think about what this means” | **C** — science / aperture; no knee chase on this panel yet |
| **Lower-echelon bins** | “Do a little bit of work” — spikes, data vs signal | **B** — diagnostic memo + maybe 1–2 plots; scope with Charles |
| **Data quality** | “Data’s great … even better when it’s clean” | Supports lower-bin forensics without panic |

---

## Alex — key quotes

1. **X-axis:** “Make it actually the **real values** … don’t do bin 1 2 3 4 5 … make it an x-axis with the **real values**.”
2. **EW logic:** “Equal width should be … **in the natural space**. Otherwise you got to line all these [bars] … I don’t know how they got out of line.”
3. **n labels (Charles read):** Otter: “left justified … **bottom justified on the bar** … raise it up just a little bit.” → **centered horizontally** on each bar; anchor text at **bottom of bar face** (not floating above). “Left” likely Otter garble.
4. **X-axis reference (Charles read):** “Do you use the **corner or the center of the bin** as the point of reference … think about that.” → **axis labels/ticks** when switching to real values, not LPM.
5. **Style:** “I love it … make a version **without all the stuff around it**.”
6. **Shape:** “Second coefficient of the squared term is **positive** … we are going to have to **think about what this means**.”
7. **Lower tail:** “You focused a lot on [elite]. **Do a little bit of work on that** [lower echelons] … let’s understand what’s happening.”
8. **Closing:** “I **love the figure overall** … This is a **very strong** [figure].”

---

## Feedback items — triage (no code until Charles approves)

**Legend:** **A** = do now (small, locked) · **B** = discuss first · **C** = not yet / parked

| # | Alex ask | Cat | Notes / blocker |
|---|----------|-----|-----------------|
| **1** | **Real x-axis values** on EW plots (natural space; equal bar widths) | **A** | **Shipped 2026-08-27:** bin **midpoint** tick labels; bars stay categorical width. |
| **2** | **n label placement** — centered on bar, **bottom-justified** on bar face, slightly raised | **A** | **Shipped 2026-08-27:** uniform anchor at bar base (`y_pad_frac`), not 10% of bar height. |
| **3** | **Clean deck export** — no provenance footer / subtitle clutter | **A** | e.g. `--deck` or `--no-provenance`; keep full PNG for lab. |
| **4** | **X-axis tick/label reference** — corner (edge) vs bin center | **B → locked** | **Center ticks on figure; edge_lo/edge_hi in roster CSV** for forensics. Option B (continuous axis, edges primary) deferred. |
| **5** | **Axis label** — Alex said “average T̂_j” | **B** | This figure is **poolq_loo**; use correct label per plot family. |
| **6** | **Lower-echelon diagnostic** — spikes in bins 1–3 | **B** | Charles mentioned other sweeps where bin 1 was tallest. Scope: one memo + bin CSV review vs full rerun grid. |
| **7** | **Interpret β₂ > 0** on 09–21 last-ps HERO | **C** | Differs from 13–21 HAND concave; era/aperture science — not a styling ticket. |
| **8** | Change population / drop 09–11 / chase concavity on this panel | **C** | Charles flagged “not appropriate yet” — discuss after lower-bin work. |

**Suggested first code batch (if Charles green-lights A-items only):** #1 + #2 + #3 on EW HERO ew16/ew20 sandbox outputs. Resolve #4 (edge vs center ticks) as part of #1 — **no** LPM or aperture changes.

---

## Naming / object clarity (avoid Alex–Charles drift)

| Alex said (Otter) | This figure actually is |
|-------------------|-------------------------|
| “Average T̂_j” | **poolq_loo** (LOO teammate mean perf z) — **HERO** object |
| “Equal width” | EW16 on **poolq_loo** range, 09–21 last-ps |
| Flat / β₂>0 | Marginal **roster-context** hero — not Alex PD25 **fix-Â × T̂_j** knee |

**F-HERO / CCT** (T̂_j on x) was **not** the figure on screen this call — but Alex’s x-axis ask applies to the whole EW plot family.

---

## How this maps to current campaign

| Thread | Link |
|--------|------|
| Working aperture **09–21 last-ps** | SCOUT memo 2026-08-27 · K=615 |
| HERO on 09–21 | **Flat elite** (β₂>0) — not 13–21 HAND concave |
| F-HERO / P2b overlay | Downturn on **T̂_j** still visible on 09–21 ALLT (separate figure) |
| EW vs QTL perm deck | q16/q20/ew16/ew20 on 09–21 |
| APGMS EW styling precedent | Aug 21 BDP — hue + n on bar face |

---

## Open / homework

- [x] Transcript → this doc
- [ ] **Charles:** confirm A/B/C table (especially #4–#8)
- [ ] **COMPASS:** after green-light — implement A-items only; then lower-bin memo (#6)
- [ ] Update disposable thread **YOU ARE HERE** after triage
- [ ] HAND: clean EW HERO for deck vs full provenance for SI

---

## Artifacts

| Item | Path |
|------|------|
| Transcript | `transcripts/20260827_Paper_Directions_27_otter_ai_transcript.docx` |
| **Figure shown** | `sports_sandbox/hero/HERO_ew16_allt_min20_mg10_09_21_last_ps_perm_loo_ever_lastps_ew16.png` |
| EW20 sibling | `sports_sandbox/hero/HERO_ew20_allt_min20_mg10_09_21_last_ps_perm_loo_ever_lastps_ew20.png` |
| Permutation deck | `sports_sandbox/hero_permutation_slides/HERO_permutation_slides_AUTO.pptx` |
| Living population thread | `3-Master_Plan/re_entry/_DISPOSABLE_Alex_hero_population_thread.md` |

---

## Thread log

| Date | Entry |
|------|--------|
| 2026-08-27 AM | PD27 scaffold; process lock (no code until triage). |
| 2026-08-27 PM | Otter transcript ingested (~3:46). Alex **loved** EW HERO style. Engineering: real x-axis, n alignment, deck export. Science: β₂>0 + lower-bin diagnostics — **discuss before code.** |
