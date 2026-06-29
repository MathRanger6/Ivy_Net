# Generative model closure checklist (SCOUT C1–C8)

**Canonical name:** `06_Generative_closure_checklist.md`  
**Original archive:** [`obsolete/original_filenames/20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md`](obsolete/original_filenames/20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md)

**Date:** 2026-06-15 (checklist); **D10 export done** 2026-06-24 — see [`08_Basketball_figures_on_disk.md`](08_Basketball_figures_on_disk.md)

Charles: Path II unchanged. **C1–C4 + C7 → green** after D10 bundle. C6 partial (prediction #2 still Army/CODA). C8 exported in bundle.

> **Note:** Body below retains June 15 “pre-D10” color counts in places; trust the **June 24** status line above and [`08_Basketball_figures_on_disk.md`](08_Basketball_figures_on_disk.md) for what is on disk today.

---

## Summary (one screen for Alex)

| Color | Count | Meaning |
|-------|-------|---------|
| **Green** | 3 now → **5 after D10** | Scientifically demonstrated; needs packaging only |
| **Yellow** | 4 now → **2 after D10** | Done in notebook/playground; not yet frozen for manuscript |
| **Red** | **0** | Nothing missing that blocks §3 draft under Path II |

**Single next task:** D10 manuscript export bundle (`export_scout_manuscript_bundle_v1.py`) — **1–2 sessions**, packaging only.

---

## §1 — Closure checklist (SCOUT-owned)

| # | Criterion | Status | Evidence | Blocker | Color |
|---|-----------|--------|----------|---------|-------|
| **C1** | Talent-only (ability-only) generative baseline **fails** qualitatively vs inverted-U stylized fact | **DONE** | 538D CELL 10: `w=0` / ability-only score → monotone on pool-mean axis; documented in [`538_Cell10_Generative_Manual.md`](../sports/documents/538_Cell10_Generative_Manual.md) | Export to bundle (D10) | **Yellow** → Green after D10 |
| **C2** | Congestion-in-score run produces **stable qualitative** peak-and-decline (pool-mean axis OK under Path II) | **DONE** | 538D CELL 10 + `SELECTION_539_*` preset (`tier1_sim_config.py`); state in `sports/tier1_cell10_playground_state.json` | Export PNG + settings JSON to bundle | **Yellow** → Green after D10 |
| **C3** | **Axis table** frozen: model quantity ↔ empirical quantity ↔ setting | **PARTIAL** | Prose + two-row logic in [`20260611_1640_SCOUT_to_COMPASS_model_coherence.md`](20260611_1640_SCOUT_to_COMPASS_model_coherence.md) §A3; **no** standalone `axis_table_generative_readouts.md` on disk yet | SCOUT D10 | **Yellow** → Green after D10 |
| **C4** | **Score equation one-pager** frozen with λ / soft-assignment semantics | **PARTIAL** | `sports/tier1_sim_config.py` (`SELECTION_539_*` constants); [`538_Cell10_Generative_Manual.md`](../sports/documents/538_Cell10_Generative_Manual.md) | SCOUT: extract to `score_equation_one_pager.md` in bundle | **Yellow** → Green after D10 |
| **C5** | **Honest limitation prose** drafted (Rung 2 axis ≠ Rung 1 axis) | **DONE** | Exact VECTOR sentence in [`20260611_1640_SCOUT_to_COMPASS_model_coherence.md`](20260611_1640_SCOUT_to_COMPASS_model_coherence.md) §A3 | VECTOR ink | **Green** (prose ready; VECTOR pastes) |
| **C6** | ≥ **two predictions** traceable to mechanism (not curve replication); **includes model-guided measurable** (quality vs congestion) | **PARTIAL** | **(1) Near-threshold heterogeneity:** `datasets/mbb/exports_inverted_u_v0/heterogeneity_ventiles_top_tail.{png,csv}` (538D CELL 4D, 2026-06-02). **(2) Peak shift with global Λ:** **not basketball-owned** — Army/CODA natural home; basketball K-slots secondary | Prediction #2 = CODA + VECTOR prose; #1 export refresh optional in D10 | **Yellow** (1 of 2 strong in SCOUT lane) |
| **C7** | **Manuscript export bundle** on disk (D10): empirical Fig 2 + generative contrast + **Tier 2.5 feature panel** + manifest | **MISSING** | Script specified in [`20260611_1640_SCOUT_to_COMPASS_model_coherence.md`](20260611_1640_SCOUT_to_COMPASS_model_coherence.md) §D; **not yet built** | SCOUT D10; Charles **C9** path lock | **Yellow** until built |
| **C8** *(PD12 optional)* | **Quality vs congestion** distinction **exported** in D10 (axis table row + congestion column/panel) | **PARTIAL** | `crowding_smooth` in pipeline; not yet named closure row on disk | SCOUT D10 | **Yellow** → Green after D10 |

**SCOUT closure rule:** Items C1–C4 + C7 go **green** when D10 lands. C5 already green. C6 stays **yellow** until cross-domain prediction map names Army Λ + basketball near-threshold — acceptable for v1 §3 closure; §4 can carry yellow honestly.

---

## §2 — Honest inventory (blunt, per rung)

### Rung 1 — Empirical inverted-U on LOO pool quality

**Publication-ready for basketball** with one housekeeping refresh. The inverted-U on `poolq_loo` is established in `530`/`538`; best frozen artifacts on disk are April 2026 ventile exports (`inverted_u_ventiles_ppm_zwithinseason_2026-04-06.png` + CSV under `datasets/mbb/exports_inverted_u_v0/`). **Single refresh:** re-run 530 export with a June dated slug before VECTOR locks Figure 2 captions — science unchanged, provenance hygiene only. No generative machinery required for Rung 1.

### Rung 2 — Minimal generative mechanism (CELL 10)

**Demonstrated interactively, not yet manuscript-frozen.** Score \(S_i = A_i - \lambda L_{C,\text{LOO}}\) with soft assignment runs in 538D CELL 10; 539 preset loads `SELECTION_539_*`; talent-only fails; congestion-in-score shows peak-and-decline on **pool mean**. **Playground-only today:** generative PNGs live in widget output + `tier1_cell10_playground_state.json`, not in `exports_inverted_u_v0/`. **Exportable in one session** via D10 script.

### Rung 3 — Predictions / decomposition

**One prediction artifact exists on disk; one is cross-domain.** Near-threshold heterogeneity (CELL 4D) exported June 2026. Mean×SD (4B/4C) and full Wang-ladder LPM exports remain notebook-only — supplement tier, not closure blockers. Peak-shift-with-Λ is conceptual in basketball; CODA owns Army instantiation.

---

## §3 — Explicit non-requirements (v1 — stop worrying)

SCOUT **confirms** COMPASS draft list. Charles should **ignore until post-draft:**

| Item | SCOUT verdict |
|------|---------------|
| Generative LOO-pool-quality bin-for-bin match | **Out of scope** v1 |
| Per-domain calibration of λ (Army / sports / tenure) | **Out of scope** v1 |
| Full deconstructable B–D estimation in generative simulation | **Out of scope** v1 |
| Mean × dispersion as **primary** prediction | **Deferred** (VECTOR) |
| Network extensions as closure criteria | **Out of scope** v1 |
| SCOUT draft Cox / tenure Layer B | **Out of scope** v1 |

**SCOUT additions:**

- **538D decomposes 539** as a manuscript claim — false; do not require before draft.
- **Generative match on LOO pool quality axis** even qualitatively — not closure (honest limitation panel only).
- **June-dated empirical Fig 2** — nice-to-have before submission, not Tier 2 closure.
- **Time-to-draft Cox / competing risks in basketball** — Army-only sophistication (CODA Q11; SCOUT agrees).
- **Harmonized bin count across settings** — PEER deferred (18 equal-width tenure bins vs basketball ventiles); cosmetic only.
- **Frozen generative parameter sensitivity sweep** — post-draft robustness.

---

## §4 — Cross-domain: basketball Tier 2 closure

| Setting | Basketball generative enough for Tier 2 closure? | What this setting must show instead |
|---------|--------------------------------------------------|-------------------------------------|
| **Army (CODA)** | **Yes** — Army does **not** need generative sim for v1 | **Empirical Rung 1:** CIF inverted-U on LOO pool minus mean + cause-specific Cox with quadratics. **Predictions:** near-threshold effects; promotion vs attrition; **peak shift with board size / Λ** (CODA-owned). |
| **Basketball (SCOUT)** | **Yes — this is where generative lives** | Rung 1 LOO inverted-U (empirical) + Rung 2 Alex score POC (generative on pool mean). |
| **Tenure (PEER)** | **Yes** — tenure does **not** need generative sim for v1 | **Rung 1 only:** preliminary empirical inverted-U on `poolq_loo_mean` (stage 9, ~55 depts inference N). Layer B Cox = pre-submission upgrade, **not** Tier 2 closure. *(PEER Round 2 confirmed.)* |

**Version B vs Version C (today):**

- **Version B (qualitative cross-domain consistency):** **Satisfied** — Army established, basketball established, tenure **preliminary** (honest label). One shared phenomenon (inverted-U on LOO peer-quality proxy); setting-specific methods.
- **Version C (prediction test from minimal model):** **Partially satisfied** — basketball near-threshold heterogeneity (SCOUT); Army near-threshold + Λ-shift (CODA); tenure **not required** for v1. Basketball generative closes the **mechanism** leg; Army/tenure close **empirical** legs at different maturity.

Under Path II, Charles does **not** need to “apply the generative model” in all three domains — one generative proof-of-concept (basketball) + three empirical stylized facts (at varying maturity) is the v1 architecture.

---

## §5 — Single next SCOUT task

| Field | Answer |
|-------|--------|
| **Task** | Build **`sports/scripts/export_scout_manuscript_bundle_v1.py`** → output **`datasets/mbb/exports_inverted_u_v0/scout_manuscript_v1/`** (unless Charles locks C9 alternate path) |
| **Unlocks** | **C1, C2, C3, C4, C7 → green**; refreshes empirical Fig 2 slug; freezes generative contrast PNGs (ability-only vs 539 preset; pool-mean + LOO-pool-quality readout panels); writes `manifest.json`, `axis_table_generative_readouts.md`, `score_equation_one_pager.md` |
| **Effort** | **1–2 sessions** — packaging + one 530 re-export; no new science |
| **Charles locks needed first?** | **Y — C9 only** (bundle directory path). C7–C8 (PERF_METRIC, bin count) already SCOUT-defaulted in [`20260611_1640_SCOUT_to_COMPASS.md`](20260611_1640_SCOUT_to_COMPASS.md); proceed with defaults if Charles silent |

---

## §6 — Handoff to VECTOR

### Ready to ink (now)

- Rung 1 empirical claim: inverted-U on **LOO pool quality** in college basketball (530/538).
- Path II architecture sentence: generative POC ≠ LOO-axis replication.
- Nesting chain from [`20260611_1640_SCOUT_to_COMPASS_model_coherence.md`](20260611_1640_SCOUT_to_COMPASS_model_coherence.md) §B5.
- Limitation sentence from same file §A3 (Rung 2 vs Rung 1 axis).
- Talent-only failure as **concept** (mechanism needs congestion term).
- Setting 3 tenure = **preliminary** empirical leg (PEER stage 9).

### Ink with caveat

- **Generative peak-and-decline figure** — caveat: *“Qualitative POC on whole-roster pool mean; not a reproduction of the LOO-pool-quality empirical axis.”*
- **Near-threshold heterogeneity figure** — caveat: *“Empirical prediction-facing readout; not fitted from generative simulation.”*
- **Score equation** — caveat: *“539 preset constants; not domain-calibrated λ.”*

### Do not ink yet

- “Generative model reproduces basketball inverted-U on LOO pool quality.”
- “538D implements full B(Q)−D(Q) decomposition.”
- “Peak location shifts with Λ in basketball generative sim” (unless/until CODA+SCOUT joint export exists).
- Any June 2026 empirical Fig 2 caption without checking slug date in bundle manifest.

---

## §7 — One sentence for Charles (Alex script)

> **“We will call the minimal model complete when the basketball generative score POC is frozen in a manuscript export bundle — talent-only fails, congestion-in-score bends curves on pool mean, at least one model-guided empirical quantity is exported (team quality vs viable-peer congestion), at least one prediction readout is on disk (near-threshold heterogeneity), axis table and limitation prose are frozen — while Army and tenure stay empirical inverted-U legs at honest maturity, without generative LOO bin-for-bin match or full 3-domain parameter identifiability.”**

*PD12 B-lite closure — see [`20260615_1200_COMPASS_PD12_reassessment.md`](20260615_1200_COMPASS_PD12_reassessment.md) §Q2.*

---

## Round 2 — SCOUT read receipt (all correspondence)

SCOUT read **all** agent-facing files in `3-Master_Plan/` (37 files). **Reading everything was helpful** for §4 (CODA Army row, PEER tenure row) and for COMPASS stale-reference flags (April Fig 2 slug, PEER Cox wording).

| New since Round 1 | SCOUT action |
|-------------------|--------------|
| [`obsolete/correspondence_rounds/20260615_1012_PEER_to_SCOUT_round2.md`](obsolete/correspondence_rounds/20260615_1012_PEER_to_SCOUT_round2.md) | Incorporated §4 tenure row; bin-spec defer accepted |
| [`20260615_1010_COMPASS_Round1_correspondence_audit.md`](20260615_1010_COMPASS_Round1_correspondence_audit.md) | Confirms 1626 round complete; this file closes June 15 queue |
| [`20260615_1008_CODA_Round1_agent_mailbox.md`](20260615_1008_CODA_Round1_agent_mailbox.md) | Incorporated Army §4 row |
| [`20260615_1008_PEER_round1_inbox_and_cross_agent.md`](20260615_1008_PEER_round1_inbox_and_cross_agent.md) | Read; aligned |

**SCOUT holds** after this file unless Charles routes D10 implementation or VECTOR asks axis-table wording for tenure proxy row.

---

*End SCOUT minimal model closure — Round 2.*
