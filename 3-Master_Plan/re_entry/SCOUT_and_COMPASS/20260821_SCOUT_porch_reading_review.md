# SCOUT review — Porch Reading (`20260820_COMPASS_Charles_CCT_porch_reading.md`)

**Date:** 2026-08-21  
**Reviewer:** SCOUT  
**Document reviewed:** [`20260820_COMPASS_Charles_CCT_porch_reading.md`](20260820_COMPASS_Charles_CCT_porch_reading.md) (COMPASS unified porch read)

---

## Verdict

**Approved for Charles/Ginger use.** Substance aligns with BDP JSON sidecars, HAND17 Slide 5, Track C, MLE fit artifacts, and both agent memos merged into the porch doc. **No factual forks** with COMPASS on NCAA basketball claims.

**Three minor clarifications** below (one wording, two footnotes). None change the story or next-step priority.

---

## Spot-checks passed

| Claim (porch) | SCOUT verify | Source |
|---------------|--------------|--------|
| PPM mg10 min20: n=46,306 PS; +DFT n=17,659 | ✓ | `basic_data_plots/BDP_Ai_Tj_mg10_min20_11_21.json` |
| +DFT Â_i mean ≈ +0.09, sd 0.76 (24% narrower) | ✓ mean 0.087, sd 0.757 | same JSON |
| +DFT T̂_j sd 0.19 vs 0.25 (26% narrower) | ✓ 0.186 vs 0.251 | same JSON |
| Team-seasons 3,842 vs +DFT 1,494 | ✓ | same JSON |
| BPM/OBPM compression table (26/46/43%) | ✓ | BDP JSONs at mg10 min20 |
| Roster \|T_j\| at min20: mean 12.0 vs 11.8 | ✓ | `BDP_team_size_mg10_min20_11_21.json` |
| NCAA draft rate ~2–2.5% | ✓ 1133/46306 = **2.45%** | same PPM JSON `theta_K_over_N` |
| MLE λ̂ ≈ 2.6, t̂ ≈ 1.1 (γ=18 fixed, 2013–2021) | ✓ λ=2.57, t=1.07 | `pd21_mle/PD21_draft_bernoulli_mle_2013_2021.json` |
| +DFT overlay = teams with ≥1 draftee in window | ✓ | `bdp_ai_tj_distributions.py` `_apply_dft` |
| Track C: no POST-QC elite dip; BPM/OBPM monotone rise | ✓ | Track C memo + JSON |
| July mg=0 dip = cameo/QC artifact | ✓ | Round 3 B5–B6, sensitivity PNGs |
| poolq_loo preferred over T̂_j for “pond” | ✓ | BINDING + hero pipeline |
| Priority 1 = matched Â × pond | ✓ | both agent memos |

---

## Clarifications (minor — not blockers)

### 1. Interval **width** vs **shift** (wording)

**Part 1** quotes you saying HAND17 intervals **“widens”** with T̂_j. **Part 6** correctly says typical **span ≈ 2.85 z** and width **does not collapse** — intervals **shift right** as T̂_j rises.

**SCOUT read:** The defendable empirical fact is **shift + overlap**, not a strong monotonic **widening** of [min Â, max Â] with team quality. Before talk/slides, prefer **“intervals move up”** unless you have a quantified span-by-T̂_j plot that shows widening.

**Suggested one-line fix in porch doc (optional):** Part 1 bullet → *“intervals move up (and may spread at the top — check span plot)”*.

### 2. +DFT orange line — who is in the overlay?

Glossary: *“Teams with ≥1 draftee.”* Accurate for **team** histogram. For **player** Â_i orange line: it is **all player-seasons on those teams** in the window (including non-drafted players), not drafted players only.

**Footnote worth one sentence in glossary:** *“+DFT player histogram = everyone on a draft-history team-season, not drafted players only.”*

### 3. Army promotion ~35–40% — not re-verified this session

**SCOUT did not re-open Army data** for this porch review. Wording in Part 2 / Part 3 / glossary matches project lore and Charles’s prior descriptions. **No NCAA claim depends on it.** If a reviewer challenges the Army baseline rate, cite the primary Army analysis doc — not this porch read alone.

---

## What SCOUT explicitly endorses

1. **CCT not falsified** by today’s marginals — agree.  
2. **Act I BDP closed** — agree.  
3. **Act II = conditional plots** (Priority 1 matched Â × poolq_loo) — agree; script name `pass_a_congestion_conditional.py` is fine when you green-light.  
4. **Do-not-do list** (§11) — agree.  
5. **Alex paragraph** (§12) — factually aligned; safe to read aloud.  
6. **Army screams / NCAA whispers** framing — agree; K/N distinction in Part 2 table is **important** and correctly stated.

---

## Header update

Porch doc line 5 should read: **SCOUT review: Complete (2026-08-21)** — see this file.

---

**Bottom line for Charles:** COMPASS did a faithful merge. Read it on the porch with confidence. When you pick Priority 1, send slide title + `mg10 min20 11_21` (or variant) and SCOUT builds the microscope.

— **SCOUT**
