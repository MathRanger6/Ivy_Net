# Paper Directions 25 — my read (Aug 21, 2026)

**Source:** `transcripts/20260821_Paper_Directions_25_otter_ai_transcript.docx` (~21 min)  
**Whiteboard:** `transcripts/PD25_board.jpeg`  
**Context:** Alex returned after thinking about **fix Â_i**; Charles had been building minutes BDP (APGMS/ARGMS) and porch CCT read.  
**Prior:** [`PD23_notes.md`](PD23_notes.md) (MLE next) · [`PD24_notes.md`](PD24_notes.md) (BPM extra) · [`../3-Master_Plan/re_entry/SCOUT_and_COMPASS/CCT_Campaign_Plan.md`](../3-Master_Plan/re_entry/SCOUT_and_COMPASS/CCT_Campaign_Plan.md)

---

## Headline

Alex’s **canonical empirical test** for fixed Â: plot **P(success)** vs **team talent** and expect a **flat plateau**, then a **congestion downturn** only when team quality pushes enough peers past the selection threshold (**K/N**, linked to **θ** and **γ** in the model). **Bin the X-axis on purpose** — need ≥ **two bins after** the congestion zone or you will never see the downturn. **Explore empirically first** (CCT), then connect inflection to the generative model.

---

## Whiteboard (PD25_board.jpeg)

| Element | Read |
|---------|------|
| Title | **Fix A_i group** (top performers / top log scale) |
| Main axes | **X = team talent** (average team Â / T̂_j) · **Y = P(s)** = draft rate |
| Small sketch | Ability distribution for fixed group; **K/N** marked on upper tail |
| Main curve | **Flat**, then **sharp drop** at congestion onset |
| Formula at knee | **(K/N − θ) / γ** — inflection is **selection-mechanism dependent** |
| Bracket | High team-talent region **≥ K/N** (“Team A_i”) |

This is **not** the marginal hero curve. It is **conditional on Â** with **team environment on X**.

---

## Alex — key quotes (paraphrased)

1. **Shape:** “For a fixed AI group … flat … then congestion kicks in … downward trend.”
2. **Where:** Downturn should appear only when team talent gets **close to K/N** (NCAA: **very high** on X because K is tiny).
3. **Story:** “All the action happens **up here**” — zoom the high team-talent tail, not league-wide marginals.
4. **Binning:** Optimize **X resolution** — need **at least two points after** the downturn; blind 16-quantile ventiles may miss it. Back-of-envelope: “I’m never going to expect this with **under 20 bins**” — use calculation to **prune sweeps**, not replace them.
5. **Power tradeoff:** More bins + finer Â slices → fewer people per cell; **K is very small** in NBA draft data.
6. **Order:** “Almost say just first explore **empirically** still” — then fit inflection in the model.
7. **Minutes:** Charles’s APGMS/ARGMS / min-floor work — Alex **yes** (panel who-counts); separate from but feeds estimand choice.

---

## How this maps to CCT work (Aug 21)

| Alex ask | Already built | Gap |
|----------|---------------|-----|
| Fix Â, conditional draft rate | P1 matched band × **poolq_loo** (+DFT whisper ~2 pp) | ✓ partial win on **peer** axis |
| Same, **T̂_j on X** | **P2b** tail bins — flat-then-down (+DFT) | ✓ **YES** — plateau ~34% → tail ~8% (z [2,3]) |
| Empirical first | Act II sweep, BDP, minutes plots, triptych | ✓ on track |
| K/N-aware X bins | P2b piecewise 4+20 tail bins | ✓ shipped |
| Inflection = f(θ, γ, K/N) | Not yet | **Act III / MLE bridge** after P2b |

**Reconciliation:** P1 on **poolq_loo** is the right *peer-congestion* microscope. Alex’s board is the *team-talent* version of the same fix-Â logic. Both can be true: full panel **T̂_j** rises (program quality); **+DFT high tail** may still show flat-then-down if binned correctly.

---

## Engineering ticket — **Priority 2b** — **SHIPPED 2026-08-21**

See [`CCT_Campaign_Plan.md` §3 Priority 2b](../3-Master_Plan/re_entry/SCOUT_and_COMPASS/CCT_Campaign_Plan.md) · outputs in `basic_data_plots/CCT_draft_rate_fixedAi_Tj_knbins_*`.

**One-liner for Alex:** “We’re holding Â fixed and binning the **high team-talent tail** on purpose — and we see your flat-then-down picture on +DFT.”

---

## Open / homework

- [ ] COMPASS: K/N → minimum X-bin count memo (θ, γ, roster N, draft K)
- [x] SCOUT: P2b figure + JSON with `edge_lo` / `edge_hi` / `n` per bin (2026-08-21)
- [ ] Charles: eyeball P2b + triptych — rehearse §8 Alex paragraph for HAND
- [ ] Later: map empirical knee to model inflection (MLE phase)
- [ ] **After next week (Alex):** paper framing + outline (placeholders OK); then 50% writing / 50% code-data

---

## Artifacts

| Item | Path |
|------|------|
| Transcript | `transcripts/20260821_Paper_Directions_25_otter_ai_transcript.docx` |
| Whiteboard | `transcripts/PD25_board.jpeg` |
| Campaign addendum | `3-Master_Plan/re_entry/SCOUT_and_COMPASS/CCT_Campaign_Plan.md` §3 Priority 2b |
