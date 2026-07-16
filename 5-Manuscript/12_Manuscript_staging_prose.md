# Manuscript staging prose (§1–§5) — **not** ChatGPT Scholar VECTOR output

**Canonical name:** `12_Manuscript_staging_prose.md`  
**Original archive:** [`obsolete/original_filenames/20260624_COMPASS_manuscript_draft_v1_sections.md`](obsolete/original_filenames/20260624_COMPASS_manuscript_draft_v1_sections.md)

**Date:** 2026-06-24  
**Author:** COMPASS (Cursor agent) — paragraphs to **copy from**, not read cover-to-cover  
**Ink map:** [`10_Manuscript_ink_map.md`](10_Manuscript_ink_map.md)  
**Dakota (decision points):** [`11_Dakota_feedback_decision_points.md`](11_Dakota_feedback_decision_points.md)  
**Working outline (you edit):** `Manuscript_working_outline_v1.docx`  
**Charles locks:** [`../3-Master_Plan/02_Charles_decisions_locked.md`](../3-Master_Plan/02_Charles_decisions_locked.md)

**Status:** Staging prose for Summer–Fall 2026 submission track. Numbers from manifests at export time. **Copy FROM this file INTO** `Manuscript_working_outline_v1.docx` per ink map (`#10`). Apply Dakota digest fixes before **manuscript §4** (tenure) — especially staging **§4** content, which maps to **manuscript §7** (Predictions), not manuscript §4.

**Manuscript front matter:** Staging **§1** → manuscript **§0** (opening framing). **Not** a separate lit-review chapter before §1 — Wang-style phenomenon first; fuller literature placement in staging **§5.2** (Discussion).

---

## §1 Opening framing (manuscript §0)

**Length target:** ½–1 page after §5→§1→§4 first ink pass. **Ink when:** polish pass once empirical triad + generative language exist — do not block the locked ink order.

### 1.1 What §0 is (and is not)

| §0 **is** | §0 **is not** |
|-----------|----------------|
| Short hook: problem, gap, contribution preview, roadmap | 15-page Introduction + Literature Review |
| States the central observation in plain English | Methods dump or citation laundry list |
| Points reader to §1 figures next | Full Menger / Barabási / Wang exposition (that lives in §2–§3 + Discussion) |

**Wang arc preserved:** §0 frames → **§1 shows the inverted-U** → §2–§3 explain why → §5 mechanism → §7 predictions.

### 1.2 Paste-ready opening (edit into your voice)

**Problem.** Organizations advance members through selective tournaments — promotion boards, draft slots, tenure cases — where evaluators compare individuals to **local peer reference groups**. A recurring question is whether stronger peers help or hurt advancement. The answer is not monotonic: elite peer environments can raise development and visibility while simultaneously compressing returns to marginal distinction when many similarly strong substitutes compete for scarce slots.

**Gap.** Sociological work on **selective ecology and assortative matching** (Menger) explains who enters elite pools; **science-of-success** minimal-model work (Barabási, Wang, Gates) asks for stylized facts and parsimonious mechanisms. Less developed is a cross-domain empirical regularity that **separates developmental upside from competitive constraint** in the same local environment — and links that decomposition to advancement outcomes under finite distinction.

**Contribution (preview).** We document an inverted-U: advancement rates rise with leave-one-out (LOO) peer quality through mid-tier environments, then fall in the most elite tier — in U.S. Army officer promotion, NCAA men's basketball draft selection, and preliminary R1 computer-science tenure. We pair the stylized fact with (1) a minimal generative proof-of-concept in which congestion enters the selection score, (2) model-guided measurements distinguishing team quality from viable-peer congestion, and (3) named prediction-facing readouts. We use associational language throughout; causal identification is not claimed.

**Roadmap.** Section 1 presents the cross-domain empirical pattern. Sections 2–3 develop the benefit–constraint framing (\(L_{\text{net}} = B - D\)) and the move from global competition to constrained local distinction. Section 4 details the tenure setting and limitations. Section 5 presents the minimal generative model and honest axis limitations. Sections 6–7 decompose mechanisms and state testable predictions. Discussion places the work relative to selective-ecology and minimal-model literatures.

### 1.3 Literature placement (where citations land)

| Literature lane | Primary manuscript home | Not here in §0 |
|-----------------|-------------------------|----------------|
| Menger — selective ecology, assortative matching | §2–§3 (conceptual); **§5.2** Discussion | Long exegesis |
| Barabási / Wang — minimal models, stylized facts | §2 hook; **§5.2** Discussion | Full paper summaries |
| Alex Gates (PD10–12) — score, quality vs congestion | §5–§6; **§5.2** Discussion | Operational detail |
| Network-science extensions | **§8** (deferred v1) | — |

**Committee brief only:** Dakota v03 **§9** (“Thoughts to stimulate feedback”) — omit from journal submission draft.

---

## §2 Theory and framing

### 2.1 Advancement under constrained distinction

Organizations advance a fraction of members through selective tournaments — promotion boards, draft slots, tenure cases — where evaluators compare individuals to **local peer reference groups**. When peer pools become elite, two forces coexist: stronger peers can raise development and signaling (**benefit**, \(B\)), and dense clusters of similarly strong, substitutable peers compress marginal returns to distinction (**constraint**, \(D\)). We summarize the net local environment as \(L_{\text{net}} = B - D\) and study how advancement responds to leave-one-out (LOO) peer-quality proxies across three settings.

This framing sits between sociological accounts of **selective ecology and assortative matching** (Menger), which explain who enters elite pools, and **science-of-success** minimal-model discipline (Barabási, Wang, Gates), which asks for stylized facts, parsimonious mechanisms, and model-guided measurements — not curve-fitting alone.

### 2.2 Stylized fact (Rung 1)

We document a repeated **inverted-U**: advancement rates rise with LOO peer quality through mid-tier environments, then fall in the most elite tier. The pattern is established in **U.S. Army officer promotion** (Setting 1) and **NCAA men's basketball draft selection** (Setting 2), with **preliminary** evidence in **R1 computer-science tenure** (Setting 3). We use associational language throughout; causal identification is not claimed.

### 2.3 Minimal mechanism (Rung 2 — basketball generative POC)

Beyond talent-only selection, a score that rewards own ability and penalizes LOO **viable-peer congestion** can produce non-monotone advancement versus team quality in simulation, while ability-only selection does not. Formally, selection uses \(S_i = A_i - \lambda L_{C,\text{LOO}}\) with soft assignment into teams and top-\(K\) advancement. This operationalizes the **constraint leg \(D\)** inside the same \(L_{\text{net}} = B - D\) ontology — not a separate model.

**Mandatory limitation:** The generative proof-of-concept is read on **whole-roster pool mean**; the empirical inverted-U is defined on **LOO pool quality** (`poolq_loo`). We do not claim bin-for-bin generative replication on the LOO axis in v1.

### 2.4 Model-guided measurements (Rung 2.5 — PD12 Priority 3)

Following Alex Gates (Paper Directions 12), the theory proposes **new quantities**, not only fits to legacy curves. We distinguish:

| Quantity | Construct | Basketball column | Interpretation |
|----------|-----------|-------------------|----------------|
| Team quality | Mean peer performance | `poolq_loo` | LOO mean teammate ability |
| Viable-peer congestion | Density above prospect threshold | `crowding_smooth` | \(C_{i,t}\) — constraint leg diagnostic |

Elite environments raise both average talent and substitutability; the downturn should steepen where congestion is high, especially for **near-threshold** individuals, while top latent talent still clears selection.

---

## §3 Methods — minimal model and measurements (basketball anchor)

### 3.1 Empirical Setting 2 (basketball)

Player-season panel with LOO pool quality (`poolq_loo`), draft outcome, and within-season performance controls. Figure 2: inverted-U on ventile bins of LOO pool quality (PPM z within-season). **Artifact:** `scout_manuscript_v1/inverted_u_ventiles_ppm_zwithinseason_2026-06-24.png`.

### 3.2 Generative POC (`sports/538D_development.ipynb` CELL 10 / 539 preset)

Frozen preset: Beta(2,2) ability, uniform team targets, `crowding_smooth` congestion, \(\lambda = 0.55\), top-\(K\) selection. **Contrast panels:** ability-only (monotone) vs congestion-in-score (peak-and-decline on pool mean). **Artifacts:** `generative_ability_only_pool_mean.png`, `generative_congestion_539_pool_mean.png`, `generative_congestion_539_loo_quality.png` (limitation readout).

### 3.3 Axis table

See `scout_manuscript_v1/axis_table_generative_readouts.md` — maps model quantities to empirical columns per setting.

### 3.4 Settings 1 and 3 (empirical legs)

- **Army:** LOO senior-rater pool minus mean; CIF bar panels + cause-specific Cox (Fine–Gray deferred).
- **Tenure:** LOO department peer quality (`poolq_loo_mean`); stage 9 binned plot; inference sample **796 persons / 52 departments** (HIGH+MEDIUM OpenAlex match, `faculty_panel_inference_v1.csv`). Preliminary; Layer B Cox pre-submission.

---

## §4 Predictions

### 4.1 Prediction #1 — Near-threshold heterogeneity (primary)

**Statement:** Holding own performance in the upper tail of the within-season distribution, draft probability should fall more sharply at the highest bins of LOO pool quality than for below-median performers — consistent with stronger distinction compression (\(D\)) where elite peer pools are both high-quality and congested.

**Evidence status:** Exploratory readout exported (`heterogeneity_ventiles_top_tail.png`). Named primary prediction for v1; not a pre-registered confirmatory test.

### 4.2 Prediction #2 — Peak shift with global \(\Lambda\) (prose hook)

**Statement:** Where the number of scarce advancement slots per local pool rises (higher \(\Lambda\)), the peak of the inverted-U should shift — Army board-size narrative (CODA-owned).

**Evidence status:** Prose hook for v1; empirical figure TBD. Not demonstrated in basketball generative sim for this manuscript version.

---

## §5 Discussion and limitations

### 5.1 Contribution

We provide (1) a cross-domain empirical regularity on LOO peer quality, (2) a minimal generative ingredient for congestion in selection, (3) model-guided measurements separating quality from congestion, and (4) named prediction-facing readouts — packaged in a Wang-style ladder. The **development vs competitive constraint** distinction is largely absent from prior talent sociology and is explicit here.

### 5.2 Literature placement

- **Menger:** Selective ecology and assortative matching motivate elite pools; we perform the tri-domain comparison he discusses but does not run.
- **Barabási/Wang:** Performance vs success, feedback, and minimal models motivate structure — our outcome is **bounded advancement probability**, not superstar tail scaling.
- **Alex Gates (PD10–12):** Operational score, quality/congestion split, near-threshold emphasis.

### 5.3 Multiplicative vs additive model form (explicit deferral)

Menger and Wang discuss **multiplicative** skill bundles and log-normal success tails. v1 keeps an **additive selection score** and \(B - D\) decomposition. Multiplicative production functions motivate **future** full \(B(Q) - D(Q)\) generative work and **manuscript §5–§6** inequality discussion — **not** a v1 rewrite. See [`05_Model_Nesting_Note_v1.md`](05_Model_Nesting_Note_v1.md) §7.

### 5.4 Limitations

- Observational designs; no causal claims.
- Generative POC axis ≠ empirical LOO axis (honest).
- Tenure Setting 3 preliminary; attrition may conflate lateral moves.
- Army pool-size audit pending pre-publication.
- Predictions #1/#2 are candidates, not fully validated cross-domain results.

---

## Appendix pointers

| Item | Path |
|------|------|
| D10 bundle | `datasets/mbb/exports_inverted_u_v0/scout_manuscript_v1/` |
| Nesting note | `5-Manuscript/05_Model_Nesting_Note_v1.md` |
| Claim table | `3-Master_Plan/07_Claim_language_guardrails.md` |
| Tenure inference manifest | `tenure_pipeline/faculty_panel_inference_v1_manifest.json` |

---

*End VECTOR manuscript draft v1 sections.*
