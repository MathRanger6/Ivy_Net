# VECTOR — PD41 Assortativity Investigation

## Scientific Questions and Test Design

**Last synced:** 2026-09-25

**Status:** Working document for Charles and VECTOR. The September 25 discussion settled the principal settings and paired-assignment design, and added a comparison of raw congestion with congestion standardized using one fixed, equal-player-weighted reference calculated from the observed 2015 team assignments with the population standard deviation. A reference spread at or below $10^{-8}$ requires a stop with no fallback; verification and other choices in Section 8 remain open. Documentation is authorized; analytical implementation and execution have not been authorized. No simulations or experiments have been executed for this brief.

**Current design:** The eight combinations of assignment, congestion weight, and selection scarcity will be compared under two congestion representations: raw and fixed-reference standardized. Their congestion-off baselines coincide. The first purpose is to determine whether assortative preference is necessary for congestion to change advancement outcomes under specified conditions. Reproducing the empirical men's basketball outcome curve is a separate, stronger requirement.

The September 24 Army discussion and evidence limitations remain in Section 6b. The September 25 choices, their plain-language explanations, examples, and unresolved details are maintained in the [detailed experiment decision record](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/decisions/ASSORT_20260925_experiment_choices_and_rationale.md>). That record supersedes the earlier raw-only proposal and the earlier description of all design choices as unapproved. The proposed outcome measures and effect tolerances still require review.

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

Scoring uses the established team congestion measure. The raw-congestion version is:

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

Charles selected **one frozen 2015 men's basketball ability vector and its corresponding empirical roster-capacity multiset**. The exact source panel and eligibility/filter specification still require verification. Preserve individual identities, $N$, capacities, performance scaling, and abilities throughout.

Use these declared scenario settings—not fitted MBB parameters:

- **Assignment:** Grandchild $\rho=0$ versus $\rho=1$.
- **Congestion weight:** $\lambda=0$ versus $\lambda=1$ in both the raw and fixed-reference standardized versions described below. Do not apply an additional automatic rescaling.
- **Scarcity:** $K=\operatorname{round}(0.01N)$ versus $\operatorname{round}(0.10N)$; record actual $K/N$.
- **Viability:** $\gamma=10$, $\theta=F_A^{-1}(0.99)$, both held fixed.
- **Selection:** exact global top-$K$ on **unclipped** scores, with a fixed tie-breaking order based on the frozen player identifier. No additional random draw follows scoring.

Charles emphasized that many domains select more than 10%; the chosen 10% level is a starting comparison, not a domain-general upper bound. The slot-count rounding convention and the fixed ability percentile calculation must be documented before execution.

The 1% setting is an **MBB-like scarcity scenario**, not a verified annual eligibility-based estimate. The repository's gallery configuration already distinguishes MBB-like scarcity around 1% from its 10% characterization setting. Neither should be substituted for the empirical HERO's approximately 2.7% *ever-drafted* rate. [S9]

The following table describes the raw-congestion version. The same settings will also be evaluated using the fixed-reference standardized formula below.

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

For each of **100 assignment repetitions selected by Charles**, form just two rosters, one per $\rho$. Reuse each roster for both $\lambda$ values, both $K$ values, and both congestion representations. Charles selected the same arrival permutation and coupled underlying uniform draws across $\rho$, where feasible without changing either assignment distribution. This pairing can improve comparison precision; it does not reduce the stochasticity of each assignment condition or guarantee lower uncertainty for every outcome. Top-$K$ needs no additional selection randomness.

**September 25 scaling decision:** retain raw congestion and add a version using one reference mean, $\mu_{C,\mathrm{ref}}$, and one positive reference standard deviation, $s_{C,\mathrm{ref}}$:

$$
S_i^{\mathrm{standardized}}
=A_i-\lambda\frac{C_{g(i)}-\mu_{C,\mathrm{ref}}}{s_{C,\mathrm{ref}}}.
$$

Charles approved holding these reference values fixed across all conditions and repetitions and calculating them from the observed 2015 team assignments, with every player weighted equally and spread calculated using the population standard deviation. This supplies an empirical scale that is external to the simulated treatments; it does not imply that the observed assignments were generated by the model or represent a theoretically neutral assignment process. Equal-player weighting is appropriate because congestion enters individual scores and selection is an individual outcome; teams with more players therefore contribute more congestion exposures. The population formula is appropriate because the frozen observed 2015 panel is the complete fixed reference population being described, not a sample used to infer a larger hypothetical population. A reference spread at or below $10^{-8}$ requires the future process to stop before simulation or scoring, report diagnostics, and use no automatic fallback. The threshold protects numerical stability and is not a scientific effect-size judgment. A passing run must report the actual spread and $1/s_{C,\mathrm{ref}}$, its implied raw-scale multiplier. Standardizing each assignment condition separately could rescale away differences in congestion spread caused by assignment itself.

With exact top-$K$ selection, the common mean contributes only a common score shift. The fixed-reference standardized ranking is therefore identical to raw-congestion ranking at an effective congestion weight of $\lambda/s_{C,\mathrm{ref}}$. Treat the comparison as sensitivity to penalty strength, not two independent mechanisms. The two versions coincide at $\lambda=0$; shared baselines must not be counted as independent evidence. All outcome summaries in Section 4 must be reported separately by congestion representation.

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

### Secondary shape display and simulation variation

Winner displacement is the unbinned primary result. Across the 100 repetitions, report its central 95% simulation range using the 2.5th and 97.5th percentiles alongside the already selected mean, median, full range, frequency of any displacement, and paired assignment-preference contrast. This percentile range describes variation across randomized assignments and is not a population confidence interval.

For a secondary visual diagnostic, form sixteen equal-count bins ordered by leave-one-out mean teammate ability within each assigned roster population. Freeze each repetition's bin membership across congestion weights, selection fractions, and congestion representations. Display the actual mean peer-quality value and selection rate for every bin, then average bin rates across repetitions and show their central 95% simulation ranges.

Label this a **simulated assignment-outcome diagnostic**, not a reproduced HERO. Do not fit a quadratic regression, estimate a turning point, or formally classify an inverted-U in this first experiment. A properly matched HERO comparison remains a later and stronger task requiring alignment of population, outcome, horizontal axis, and binning.

## 5. Historical precedents and components requiring review

Charles prefers fresh derived inputs and outputs for this investigation. Existing sweeps and generated roster files are historical evidence only: they will not supply experimental inputs, be resumed, or be overwritten. The repository contains useful implementation precedents, but not a completed version of this factorial test. Preserved source extracts and reusable code components require separate provenance and specification review before any authorized implementation.

- **Grandchild assignment and $H_{\mathrm{sort}}$:** reusable mechanisms. A saved 30-replicate sweep records mean $H_{\mathrm{sort}}\approx0.06635$ at $\rho=0$ and $0.32208$ at $\rho=1$, for its particular fixed-size-roster specification. This directly demonstrates why $\rho=0$ must not be labeled $H_{\mathrm{sort}}=0$; it does not establish either value for the proposed population. [S4, S11]
- **Matched $\lambda$ ablation:** `pass_b_lambda_ablation_bundle.py` reuses one assigned roster across $\lambda$ arms. That is the right pairing principle. Its saved experiment uses a different assignment kernel, Beta abilities, 10% selection, and team-mean plots. [S6]
- **Historical knockout and Grandchild $\lambda$ sweep:** useful precedents and archived outcomes, but some comparisons change seeds across $\lambda$. The latter explicitly uses `seed + 31*i`, so it does not isolate $\lambda$ on identical rosters. [S7]
- **Pass C:** varies assignment while holding scoring fixed, but its saved “low” arm is $\rho=0.001$, not exactly zero, and it does not cross $\lambda$ with scarcity. Its Gaussian assignment kernel also differs from Grandchild. [S8]
- **Scoring/selection utilities:** require explicit specification review before reuse. They can automatically rescale congestion, clip scores, and cap selection by positive-score count. Those behaviors would violate the proposed exact-$K$, unclipped comparison. [S5]

These historical outputs help explain earlier reasoning and implementation choices; they do not already answer the necessity question or fix the population for the new experiment.

**Population history reconciled for team coverage:** Charles's September 25 account of the one-game-opponent problem is supported by the August records. The [SCOUT response](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260925_SCOUT_response_data_hygiene_and_model_history.md>), [COMPASS addendum](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260925_COMPASS_addendum_data_hygiene_and_model_history.md>), saved figures, and [archived decision exchange](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/.specstory/history/2026-06-11_08-19-11-0400-compass.md:215669>) establish the sequence: six captured games was the first working rule; Charles then tested and adopted a rule retaining at least eleven captured games. Charles has selected that eleven-game rule for the new 2015 experiment. It is a coverage requirement, not proof of a complete season or Division I membership. Individual low-minute treatment and the rest of the eligible population remain provisional. The saved figures are historical outputs inspected without reproduction.

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

## 8. Decisions made and questions still open

**September 25 construction stop:** The first authorized construction attempt has not reached simulation. Applying the agreed games-first canonical-team rule literally assigns three athletes to a team with more no-play roster records and zero minutes, excluding their otherwise eligible played seasons and yielding 4,263 rather than the previously audited 4,266 athletes. Separately, 100 otherwise eligible athletes have game rows with recorded points but missing minutes. The [source-data stop report](assort_analysis/docs/source_review/ASSORT_20260925_initial_execution_stop.md) documents both issues. Canonical-team and partial-stat treatment require explicit scientific decisions before the 100 paired repetitions can run.

**Current population decisions:** include only 2015 team-seasons with at least eleven captured games and only players with at least twenty total captured minutes. A player below the minutes floor is excluded from assignment, observed capacity, teammate and congestion calculations, and outcome readouts. Rebuild the player-season input from the frozen game-level box data. Resolve each athlete to one canonical 2015 team using the greatest number of distinct game records, then total minutes; stop for manual review if both remain tied. Then aggregate retained points and minutes, calculate points per minute once, remove rows below twenty total minutes, and standardize across the final eligible 2015 population using the population mean and population standard deviation. The resulting capacities represent eligible analytical players rather than complete listed rosters. Existing exported panels are provenance comparisons only and will not supply the experimental population.

The canonical-team rule addresses verified source duplication: 27 athlete-game combinations appear under both opponents in two 2015 games. Four false High Point records copied to Arkansas–Pine Bluff survived the minutes floor, creating 4,270 apparent player-team rows for 4,266 athletes and inflating Arkansas–Pine Bluff's analytical capacity from 14 to 18. No genuine eligible same-season transfer was found. Treat this as a bounded 2015 data-quality correction, not a general policy against transfers.

The investigation remains a **mechanism-isolation experiment**. Charles selected the 2015 population; 100 paired assignment repetitions; $\rho=0$ versus $\rho=1$; $\lambda=0$ versus $\lambda=1$; selection fractions of 1% and 10%; fixed $\gamma=10$ and a fixed 99th-percentile $\theta$; deterministic top-$K$ selection with exact ties resolved by ascending frozen player identifier; reused rosters; and coupled assignment draws. Use `20260925` as the master seed, derive and record 100 repetition seeds, and reuse each repetition seed across the two assignment-preference settings so that their player order and underlying random choices are coupled. Calculate $\theta$ by linear interpolation at the 99th percentile of the final standardized ability distribution; this locates the smooth viability transition and need not leave exactly 1% of players strictly above it. Convert each selection fraction to a whole-number slot count by nearest-integer rounding, with exact halves rounded upward, and report the achieved fraction. At the currently audited $N=4{,}266$, this gives 43 and 427 slots; an authorized rebuild must confirm or recalculate those counts. Charles also selected raw congestion alongside one fixed-reference standardization calculated from the observed 2015 team assignments with equal-player weighting and the population standard deviation. Congestion will be one shared team-level mean of smooth viability calculated over every eligible roster member, including the focal player, and applied equally to all members of that team. This matches the written mechanism and the repository's current `team_smooth` default. Leave-one-out congestion is excluded from the primary design and retained only as a possible later sensitivity analysis; leave-one-out teammate quality remains a separate empirical curve-axis measure.

**Primary outcome decision:** for each fixed assignment and slot count, compare the ability-only winner set with the congestion-on winner set. Report both the number of displaced winners and that number divided by $K$. Summarize displacement separately by assignment preference, scarcity, and congestion representation. Across repetitions, report the mean, median, observed range, central 95% simulation range, proportion with any displacement, and paired difference between assignment-preference conditions. Do not impose an arbitrary minimum-effect threshold: the observed magnitude and consistency are the findings. A sixteen-bin simulated assignment-outcome curve is secondary diagnostic evidence and is not a reproduced HERO. Producing or formally classifying an inverted-U is not part of this first experiment's success criterion.

The next evidence task is to translate the frozen input, filters, ability scaling, player identifiers, capacities, shared team-congestion definition, paired seeds, and settled reporting package into an auditable construction specification. The [detailed experiment decision record](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/decisions/ASSORT_20260925_experiment_choices_and_rationale.md>) explains these points in detail.

**Execution remains separately gated by Charles's explicit authorization.** Agreement on individual design choices does not authorize creating a driver or running experiments. After the specification is complete and execution is authorized, a separate driver can reuse the existing assignment and congestion components and verify the stated invariants before the experiment. No fitting to draft outcomes is required for this scenario test. Claims about a calibrated annual basketball mechanism would require the separate outcome-and-likelihood alignment already identified.

## Revision record

- **2026-09-25 — Historical review and fresh outputs:** Recorded Charles's account of the one-game-opponent problem and his preference for fresh investigation outputs. Linked the evidence review and questions for SCOUT; retained the exact population as provisional and preserved the accepted experiment settings. No analytical execution.

- **2026-09-25 — Team-season coverage:** Incorporated SCOUT and COMPASS responses plus the original archived decision exchange. Charles selected at least eleven captured games for the new 2015 experiment. Kept individual low-minute treatment open.

- **2026-09-25 — Individual minutes eligibility:** Charles selected at least twenty total captured 2015 minutes and excluded lower-minute players from every layer of the first experiment. Deferred zero-points-per-minute treatment as a possible sensitivity analysis.

- **2026-09-25 — Ability measurement:** Charles selected final-population standardization using the population standard deviation. After code inspection and SCOUT's updated reconciliation clarified that points per minute is constructed at panel build rather than supplied by ESPN, Charles selected a fresh build from the frozen game-level box data. Existing exported panels remain comparison artifacts. Documentation is authorized; executing the build is not.

- **2026-09-25 — Canonical team:** A read-only 2015 audit identified duplicated opponent-team assignments rather than genuine eligible transfers. Charles selected one team per athlete by greatest distinct-game coverage, then total minutes, with unresolved ties stopped for review. This corrects the four false eligible Arkansas–Pine Bluff rows and preserves 4,266 unique athletes without generalizing the rule beyond the audited 2015 population.

- **2026-09-25 — Primary outcome:** Charles selected winner displacement—the count and proportion of ability-only winners replaced when congestion is switched on—as the primary result. Curve shape remains a separate diagnostic, so the investigation will not tune its settings merely to place an inverted-U “on the paper.”

- **2026-09-25 — Effect interpretation:** Charles rejected an arbitrary minimum-effect cutoff. The report will show displacement's mean, median, range, frequency of any displacement, and paired assignment-preference contrast, allowing the prespecified magnitude and consistency to remain visible without another adjustable threshold.

- **2026-09-25 — Shared team congestion:** Charles selected the full-team smooth-viability mean, including the focal player, as the single congestion value applied to every player on a team. Read-only code inspection confirmed the current `team_smooth` default maps to `crowding_smooth_team`; the leave-one-out implementation is a distinct legacy option. Leave-one-out congestion is outside the primary design and may be considered later only as a sensitivity analysis.

- **2026-09-25 — Integer slot counts:** Charles selected nearest-integer rounding, with exact halves rounded upward, for converting each target selection fraction into $K$. At the currently audited population of 4,266, the resulting counts are 43 and 427; final execution records must also report the achieved fractions and recalculate the counts if the rebuild changes $N$.

- **2026-09-25 — Viability-threshold quantile:** Charles selected linear interpolation for the 99th percentile of the final standardized ability distribution. This interpolated value defines the midpoint of the smooth viability transition and remains distinct from the selection capacity $K$.

- **2026-09-25 — Random seeds and pairing:** Charles selected master seed `20260925` and 100 derived, recorded repetition seeds. Each repetition seed will initialize both assignment-preference conditions, coupling their random player order and underlying choices while allowing their differing probabilities to produce different rosters.

- **2026-09-25 — Exact score ties:** Charles selected ascending frozen player identifier as the deterministic tie-breaker. Identifier uniqueness, missingness, and stored type must be verified before execution; failure stops the process rather than allowing a silent row-order fallback.

- **2026-09-25 — Reporting package:** Charles retained unbinned winner displacement as primary and selected central 95% simulation ranges across the 100 repetitions. Sixteen equal-count leave-one-out teammate-ability bins will provide a secondary simulated assignment-outcome diagnostic. It will not be labeled a reproduced HERO or subjected to quadratic fitting, turning-point estimation, or formal inverted-U classification.

- **2026-09-25 — Design decisions:** Recorded Charles's selected population, settings, repetition and pairing choices, and deterministic tie rule. Replaced the raw-only proposal with raw congestion plus one fixed-reference standardization; left the reference population open. Added the mathematical qualification that fixed scaling changes effective congestion strength. Linked the detailed decision record; implementation and execution remain unauthorized.

- **2026-09-25 — Reference population:** Selected the observed 2015 team assignments as the source of the fixed congestion reference distribution; left player-versus-team weighting and calculation conventions open.

- **2026-09-25 — Reference weighting:** Selected equal-player weighting because congestion enters individual scores and individual selection is the outcome; left the standard-deviation convention and safeguards open.

- **2026-09-25 — Reference spread calculation:** Selected the population standard deviation because the frozen observed 2015 panel is the complete fixed reference population being described; left zero-spread and very-small-spread safeguards open.

- **2026-09-25 — Exactly zero reference spread:** Required a pre-execution stop with diagnostic reporting and no automatic fallback; left the positive but extremely small spread safeguard open.

- **2026-09-25 — Extremely small positive reference spread:** Selected $10^{-8}$ as a fixed numerical stop threshold on the theoretical zero-to-one congestion scale; required diagnostic reporting, no automatic fallback, and reporting of the actual passing spread and implied raw-scale multiplier. The threshold is not a scientific effect-size judgment.

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
