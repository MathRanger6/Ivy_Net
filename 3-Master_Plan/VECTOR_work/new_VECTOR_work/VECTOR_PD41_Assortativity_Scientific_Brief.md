# VECTOR — PD41 Assortativity Investigation

## Scientific Questions and Test Design

**Last synced:** 2026-09-24

**Status:** Working document for Charles and VECTOR. Revise as our discussions develop, distinguishing evidence, interpretations, proposals, and decisions. Charles has authorized this document update; the eight-cell design remains proposed and awaits approval. No simulations or experiments have been executed for this brief.

**Recommendation:** An eight-cell test that isolates assignment, congestion, and selection scarcity. Its first purpose is to determine whether assortative preference is necessary for congestion to change advancement outcomes under specified conditions. Reproducing the empirical MBB curve is a separate, stronger requirement.

The September 24 revision incorporates the Army band-of-excellence framing and evidence limitations in §6b. It preserves the proposed basketball design, parameter settings, and estimands. Pending decisions remain in §8; substantive revisions are recorded below.

## 1. What Alex asked—and what remains a hypothesis

The original **PD41 transcript**, at 03:50–04:51, records Charles identifying “does assortativity matter?” as the priority and Alex affirming it as a principal blocker. At 06:55, Alex again places resolving assortativity before reshaping the presentation. Charles's earlier “boundary condition” suggestion at 00:43 is exploratory, not an established finding. [S1]

**PD40 is more explicit.** At 29:30–29:35, Alex asks whether assortativity is needed and says that it is acceptable if it is not. At 52:29–54:22, he distinguishes two possibilities: incorrect measurement versus an incorrect assumption that the model requires assortativity. He also cautions against drawing general model conclusions from basketball alone. [S2]

Charles's present request sharpens this into three questions:

1. Does assortativity matter to the model?
2. Can congestion produce the same effect without assortative assignment?
3. Can unusually scarce selection make MBB a boundary case?

The **scarcity explanation is a working hypothesis**. The factorial design below is VECTOR's proposed test, not a design explicitly prescribed in PD41. Existing cross-domain curves and sorting statistics do not yet answer it.

## 2. Separate five meanings of “congestion matters”

Use the current Grandchild assignment mechanism:

$$
P(i\rightarrow j\mid\text{current rosters})
\propto R_j\exp\!\left[-\rho\left|A_i-\mu_j\right|\right].
$$

Here $R_j$ is remaining capacity and $\mu_j$ is the evolving team mean. At $\rho=0$, assignment follows remaining capacity without ability-based preference. That does **not** force realized sorting to zero. Measure, before selection,

$$
H_{\mathrm{sort}}
=1-\frac{\sum_i\left(A_i-\bar A_{g(i)}\right)^2}
{\sum_i\left(A_i-\bar A\right)^2}.
$$

SCORE uses the established team congestion measure:

$$
C_j=\frac{1}{n_j}\sum_{h\in j}\sigma\!\left[\gamma(A_h-\theta)\right],
\qquad
S_i=A_i-\lambda C_{g(i)}.
$$

These equations distinguish:

- **Penalty:** $\Delta S_i=-\lambda C_{g(i)}$.
- **Ranking change:** different penalties reverse some ordering of candidates.
- **Advancement change:** those changes affect winners or selection probabilities.
- **Aggregate nonlinearity:** the resulting outcome curve is nonlinear.
- **Empirical explanation:** its particular shape agrees with a properly matched empirical target.

A penalty alone proves little: if everyone receives the same penalty, rankings and exact top-$K$ winners remain unchanged. Rank changes away from the selection cutoff need not change winners. Because $C_j$ is common within a team, this specification changes rankings **between teams**, while preserving within-team ability order. [S4–S5; mathematical implications]

## 3. Minimal factorial design

The proposed first experiment uses **one frozen 2015 MBB ability vector and its corresponding empirical roster-capacity multiset**, prepared under one explicitly recorded eligibility/filter specification. Preserve individual identities, $N$, capacities, performance scaling, and abilities throughout.

Use these declared scenario settings—not fitted MBB parameters:

- **Assignment:** Grandchild $\rho=0$ versus $\rho=1$.
- **Congestion:** $\lambda=0$ versus $\lambda=1$, with raw $C_j\in[0,1]$; no automatic congestion rescaling.
- **Scarcity:** $K=\operatorname{round}(0.01N)$ versus $\operatorname{round}(0.10N)$; record actual $K/N$.
- **Viability:** $\gamma=10$, $\theta=F_A^{-1}(0.99)$, both held fixed.
- **Selection:** exact global top-$K$ on **unclipped** scores, with a fixed tie-breaking order.

The 1% setting is an **MBB-like scarcity scenario**, not a verified annual eligibility-based estimate. The repository's gallery configuration already distinguishes MBB-like scarcity around 1% from its 10% characterization setting. Neither should be substituted for the empirical HERO's approximately 2.7% *ever-drafted* rate. [S9]

| Cell | $\rho$ | $\lambda$ | $K/N$ target | Score | Congestion comparison |
|---|---:|---:|---:|---|---|
| L00 | 0 | 0 | 1% | $A_i$ | Low-scarcity-fraction baseline |
| L01 | 0 | 1 | 1% | $A_i-C_j$ | L01 − L00 |
| L10 | 1 | 0 | 1% | $A_i$ | Assortative baseline |
| L11 | 1 | 1 | 1% | $A_i-C_j$ | L11 − L10 |
| H00 | 0 | 0 | 10% | $A_i$ | Less-scarce baseline |
| H01 | 0 | 1 | 10% | $A_i-C_j$ | H01 − H00 |
| H10 | 1 | 0 | 10% | $A_i$ | Assortative baseline |
| H11 | 1 | 1 | 10% | $A_i-C_j$ | H11 − H10 |

**Why freeze $\theta$?** Existing routines derive $\theta$ from $K/N$. Allowing that here would change congestion construction and selection capacity simultaneously. Freezing $\theta$ identifies the effect of changing **SELECT capacity alone**. A later comparison with $\theta(q)=F_A^{-1}(1-q)$ would test the coupled model and must be labeled accordingly. [S10]

For each of **100 proposed assignment replicates**, form just two rosters, one per $\rho$. Reuse each roster for both $\lambda$ values and both $K$ values. Couple assignment randomness across $\rho$ using the same arrival permutation and underlying uniform draws where feasible. Top-$K$ needs no additional selection randomness.

Two useful invariants follow:

- With $\lambda=0$, the winners at a given $K$ must be identical across assignments, although their peer-quality curve can change.
- With $\theta$ fixed, changing $K$ must not change scores, rankings, congestion, or $H_{\mathrm{sort}}$.

This first experiment tests the deterministic selection model. It does not establish robustness to noisy selection.

## 4. Estimands and shape diagnostics

For **every cell and replicate**, retain individual scores, ranks, selection indicators, team congestion, LOO peer quality, and realized $H_{\mathrm{sort}}$.

The principal estimands are:

### Winner displacement

At fixed assignment and $K$,

$$
D_{\rho,q}
=\mathbb{E}\!\left[
\frac{\left|W_{\rho,1,q}\mathbin{\triangle}W_{\rho,0,q}\right|}{2K}
\right].
$$

This is the fraction of slots whose recipients change when congestion activates. Also report rank displacement and which ability groups gain or lose.

Do not use the population-average change in selection as the principal effect: with exact $K$ fixed, it is necessarily zero.

### Individual advancement

$$
\Delta\pi_i(\rho,q)
=\mathbb{E}\!\left[Y_i(\rho,1,q)-Y_i(\rho,0,q)\right].
$$

Here probabilities average over randomized assignments. Conditional on a particular roster, top-$K$ outcomes are deterministic; these are not calibrated real-world draft probabilities.

### Curve changes

Let $x_i$ be LOO mean teammate ability and $m_{\rho,\lambda,q}(x)$ the advancement curve. Report

$$
\Delta m_{\rho,q}(x)
=m_{\rho,1,q}(x)-m_{\rho,0,q}(x).
$$

Freeze bin membership within each roster across $\lambda$ and $K$. Display the actual numerical $x$-values; do not silently replace LOO with team mean. Team-mean plots can be a separately labeled secondary diagnostic.

### Interactions

For a common curve diagnostic $G$,

$$
I_q=
\left[G_{1,1,q}-G_{1,0,q}\right]
-
\left[G_{0,1,q}-G_{0,0,q}\right].
$$

Then compare $I_{0.01}$ with $I_{0.10}$. Apply the same logic to winner displacement. This distinguishes an assignment–congestion interaction from its moderation by scarcity.

### Predefined shape summaries and uncertainty

Predefine three separate shape summaries:

1. **Upper-tail decline:** selection rate in the highest peer-quality quintile minus the preceding quintile. Also report the lower-to-upper-middle rise. These fixed percentile regions provide a stable shape summary; they represent different numerical $x$-ranges across assignments.
2. **Global quadratic curvature:** fit $Y\sim1+x+x^2$; report $\beta_2$, the implied turning point, and whether it lies within supported $x$-values. A negative coefficient alone is insufficient evidence of an interior hump.
3. **Congestion-induced shape change:** differences in those diagnostics between $\lambda=1$ and $\lambda=0$. A hump already present at $\lambda=0$ is not evidence that congestion generated it.

Use paired replicate uncertainty intervals, showing both Monte Carlo precision and variation across assignments. Do not treat player observations as independent replications of a whole-league experiment.

For “negligible,” the proposed preregistered equivalence margins are **1% of winner slots displaced** and **$0.1q$ in the tail-rate contrast**. These are proposed substantive tolerances for approval, not statistical facts. An imprecise estimate overlapping zero establishes neither absence nor equivalence.

Finally, matching these diagnostics would establish **shape agreement under the simulation readout**. Claiming reproduction of the existing MBB HERO additionally requires matching its population, ever-draft outcome, last-season readout, and binning.

## 5. What can be reused

The existing repository contains useful components, but not a completed version of this factorial test.

- **Grandchild assignment and $H_{\mathrm{sort}}$:** reusable mechanisms. A saved 30-replicate sweep records mean $H_{\mathrm{sort}}\approx0.06635$ at $\rho=0$ and $0.32208$ at $\rho=1$, for its particular fixed-size-roster specification. This directly demonstrates why $\rho=0$ must not be labeled $H_{\mathrm{sort}}=0$; it does not establish either value for the proposed population. [S4, S11]
- **Matched $\lambda$ ablation:** `pass_b_lambda_ablation_bundle.py` reuses one assigned roster across $\lambda$ arms. That is the right pairing principle. Its saved experiment uses a different assignment kernel, Beta abilities, 10% selection, and team-mean plots. [S6]
- **Historical knockout and Grandchild $\lambda$ sweep:** useful precedents and archived outcomes, but some comparisons change seeds across $\lambda$. The latter explicitly uses `seed + 31*i`, so it does not isolate $\lambda$ on identical rosters. [S7]
- **Pass C:** varies assignment while holding scoring fixed, but its saved “low” arm is $\rho=0.001$, not exactly zero, and it does not cross $\lambda$ with scarcity. Its Gaussian assignment kernel also differs from Grandchild. [S8]
- **Scoring/selection utilities:** require explicit specification review before reuse. They can automatically rescale congestion, clip scores, and cap selection by positive-score count. Those behaviors would violate the proposed exact-$K$, unclipped comparison. [S5]

Thus, existing outputs inform parameter choices and implementation structure; they do not already answer the necessity question.

## 6. How to interpret possible results

| Result | What it would establish | What it would not establish |
|---|---|---|
| **A. Effect only with assortativity** | Evidence that assignment preference is enabling the specified effect at the tested settings, provided the $\rho=0$ effect is demonstrably negligible. | Universal necessity, or necessity at other $\lambda$, $\gamma$, group sizes, distributions, or selection rules. |
| **B. Effect without assortativity** | A counterexample to strict necessity of assortative **preference** for that particular effect. | Zero realized sorting, or reproduction of the empirical curve. |
| **C. Effect without assortativity only at 1%** | Evidence consistent with scarcity enabling the effect where assignment preference is absent. | The location of a boundary interval, or proof that actual MBB occupies it. Two scarcity levels cannot identify a range. |
| **D. Scores/ranks/winners change, empirical shape fails** | Congestion is active at the demonstrated level. | An explanation of the empirical curve. |
| **E. Different parameter cells yield similar curves** | Evidence of observational ambiguity at the chosen curve resolution. | Equivalence of their mechanisms. Individual winners, score changes, and sorting can still differ. |

Necessity and sufficiency must be attached to a named effect. Positive sorting by itself need not generate a downturn; likewise, a successful $\rho>0$, $\lambda>0$ cell demonstrates that the **full tested configuration** can generate the pattern, not that assortativity alone is sufficient.

## 6b. Army parallel: band of excellence and empirical sorting

This brief remains **MBB simulation-first**. Army supplies the empirical origin and a complementary question: where within senior-rater pools should congestion affect officers competing for scarce distinction? The September 24 materials emphasize the **band of excellence**. This is a mechanism hypothesis and an agreed presentation emphasis in those records, not independent evidence that congestion binds only in that band. Zero top-block history alone does not establish that an officer never competed for distinction. [S12–S13]

### Panel roles and narrative order

The revised Act I sequence is **full-sample phenomenon → conditional comparisons → empirical sorting**:

- **Panels 2 and 9:** distributions and the full-cohort HERO supply descriptive context. Preserve the full-cohort Panel 9; an own-zero-filtered version is a conditional comparison and must be labeled accordingly.
- **Panels 7 and 8:** the fixed high-ability CCT band and elite-pond comparison carry the proposed mechanism argument. These are conditional outcome comparisons, not identified causal peer effects.
- **Panel 5:** $H_{\mathrm{sort}}$ describes observed pool sorting. It complements the MBB intervention on assignment preference $\rho$; it cannot substitute for the eight-cell test. [S12–S13]

### Three distinct filters

**Missing SNR history** (NaN), **finite own top-block ratio equal to zero**, and **zero-valued peers excluded from pool construction** must remain distinct. The proposed own-zero gate removes focal officers from plots; the Run 3 peer-zero sensitivity changes pool means and sizes. Apply the existing minimum pool size of three before the focal restriction. That restriction neither rebuilds pools nor requires three remaining ever-top-blocked officers. Ever-top-blocked is a coarse proxy for being in contention, distinct from the fixed high-ability and elite bands. Changes in the plotted lower tail after exclusion may reflect composition. [S12–S13]

### Viability threshold versus empirical gates

In basketball, $\theta$ determines how each peer contributes to

$$
C_j=\frac{1}{n_j}\sum_{h\in j}\sigma\!\left[\gamma(A_h-\theta)\right].
$$

Army's focal gates determine **whose outcomes are plotted**. The handoff calls these the “same scientific object”; this brief treats that as a **conceptual analogy**, not a mathematical equivalence. A focal restriction leaves existing pool measures unchanged; smooth viability weighting changes congestion construction. This preserves the source's reasoning while explicitly qualifying its stronger wording. [S12–S13; mathematical distinction]

The PD21 calibration is described as fitting $\lambda$, $\gamma$, and temperature $t$ with $\theta$ preset under the selected rule. This neither estimates an Army threshold nor resolves the calibration/replay mismatch in §7. Senior-rater top-block scarcity and promotion scarcity concern different selection outcomes. Army's promotion/attrition/censoring framework must be tied to each figure's actual outcome and estimator; it is not a port of basketball's Bernoulli calibration. Smooth Army congestion and score-to-selection replay remain extension proposals. [S3, S12–S13]

### Evidence and access status

Tag the **Army figure refresh and conditional band comparisons 🟡 PARTIAL**. The handoff reports Runs 1–3 completed and Runs 4–5 pending; these are progress reports, not independent verification of resulting figures. The own-zero plotting toggle is described as planned, default off. The historical HERO shape remains Charles's recorded assessment; refreshed straight-LOO results require their own provenance. [S12–S13]

The September 24 access record says Mac access covers scrubbed code and documents; old PDE remains runnable but blocks uploads; Vantage is not yet online. Army data and figure refreshes remain on Army systems, with screenshots and error text supplying feedback. The conceptual bridge can guide discussion while the empirical refresh remains pending. [S12–S14]

## 7. Limits that remain binding

The Bernoulli calibration/$K$-draw mismatch, boundary $\rho$ fit, Army provenance discrepancies, different empirical/simulation axes, and tenure cohort/survival limitations remain unresolved. None should be absorbed into a “validated parameter set.”

The current MBB curve has a local tail decline alongside positive fitted quadratic curvature. Its target should therefore remain that measured combination—not a presumed globally concave parabola. Annual simulation outcomes and the existing ever-drafted HERO are also different outcomes.

The proposed eight cells cannot identify dependence on all $\lambda$ values, ability distributions, group sizes, or selection rules. A null result everywhere would leave the chosen positive-$\lambda$ setting insufficiently informative; it would not prove that congestion never matters. A scarcity-specific result would justify a subsequent, bounded scarcity grid—not an immediate universal conclusion.

## 8. Pending decisions for Charles and VECTOR

The recommendation remains a **mechanism-isolation experiment**. These three choices are proposed, not yet approved:

1. Exact, unclipped top-$K$ for the first comparison.
2. Fixed $\theta$, $\gamma$ and congestion scaling; scenario values $\rho=1$, $\lambda=1$, $q=0.01$ versus $q=0.10$.
3. The proposed effect tolerances and paired replication plan.

After approval, the smallest executable step is a separate driver around the existing assignment and congestion components, implementing the eight cells and recording the individual-level comparisons. It should first verify the invariants above, then run the paired replicates. **No refitting is needed for this scenario test.** Claims about a calibrated annual MBB mechanism would require the separate outcome-and-likelihood alignment already identified.

## Revision record

- **Initial brief:** Recorded the PD41 questions, proposed eight-cell design, estimands, interpretation rules, and unresolved calibration and provenance limits.
- **2026-09-24 — Repository addendum:** Added the Army porch parallel in §6b.
- **2026-09-24 — Working-document revision:** At Charles's request, made this an evolving discussion document; expanded §6b to distinguish focal filters from peer construction, conceptual analogy from mathematical equivalence, and reported progress from verified results. Preserved the proposed basketball design and outstanding decisions.

Record substantive changes to questions, assumptions, evidence, and decisions here. Identify superseded interpretations explicitly rather than silently replacing them. Document revisions do not by themselves authorize experiments.

## Repository sources

Source labels below are repository-relative. Links point to the corresponding local files in Cursor Workspace PDE.

- **S1 — Original PD41:** [transcripts/20260922_Paper_Directions_41_otter_ai_transcript.docx](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/transcripts/20260922_Paper_Directions_41_otter_ai_transcript.docx>).
- **S2 — Original PD40:** [transcripts/20290917_Paper_Directions_40_otter_ai_transcript.docx](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/transcripts/20290917_Paper_Directions_40_otter_ai_transcript.docx>). Its internal meeting date is September 17, **2026**, despite the filename.
- **S3 — Earlier calibration discussion:** [transcripts/20260814_Paper_Directions_21_otter_ai_transcript.docx](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/transcripts/20260814_Paper_Directions_21_otter_ai_transcript.docx>). Inspected passages distinguish assignment estimation from selection and explicitly rescale $\lambda$ by temperature.
- **S4 — Assignment and sorting:** [sports/541_grandchild_homophily_assign.py](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/sports/541_grandchild_homophily_assign.py>).
- **S5 — Congestion, score transformations, selection:** [sports/tier1_pool_assignment.py](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/sports/tier1_pool_assignment.py>).
- **S6 — Matched $\lambda$ design:** [sports/scripts/pass_b_lambda_ablation_bundle.py](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/sports/scripts/pass_b_lambda_ablation_bundle.py>).
- **S7 — Seed-varying precedents:** [sports/scripts/pass_b_generative_knockout_bundle.py](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/sports/scripts/pass_b_generative_knockout_bundle.py>) and [sports/scripts/grandchild_lambda_select_sweep.py](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/sports/scripts/grandchild_lambda_select_sweep.py>).
- **S8 — Assignment ablation:** [sports/scripts/pass_c_rho_ablation_bundle.py](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/sports/scripts/pass_c_rho_ablation_bundle.py>).
- **S9 — Existing scarcity settings:** [sports/scripts/gallery_knobs.py](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/sports/scripts/gallery_knobs.py>).
- **S10 — Existing $K$–$\theta$ coupling and shape label:** [sports/scripts/grandchild_selection_inverted_u_diagnostic.py](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/sports/scripts/grandchild_selection_inverted_u_diagnostic.py>).
- **S11 — Saved sorting results:** [3-Master_Plan/re_entry/HEROs_and_PASSes/grandchild_assign/GRANDCHILD_rho_sweep_summary.csv](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/HEROs_and_PASSes/grandchild_assign/GRANDCHILD_rho_sweep_summary.csv>), read alongside its metadata.
- **S12 — Army narrative addendum:** [3-Master_Plan/VECTOR_work/handoff_upload_no_repo/10_Army_band_excellence_and_theta_Sep24.md](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/handoff_upload_no_repo/10_Army_band_excellence_and_theta_Sep24.md>). September 24 planning and progress record; not independent verification of Army outputs.
- **S13 — Charles’s Army print memo:** [talent/re_entry/BAND_OF_EXCELLENCE_ARMY_PORCH.md](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/talent/re_entry/BAND_OF_EXCELLENCE_ARMY_PORCH.md>). September 24 planning and progress record; not independent verification of Army outputs.
- **S14 — Current handoff and access checklist:** [3-Master_Plan/re_entry/_DISPOSABLE_CHARLES_VECTOR_handoff_checklist.md](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/_DISPOSABLE_CHARLES_VECTOR_handoff_checklist.md>). September 24 planning and progress record; not independent verification of Army outputs.
