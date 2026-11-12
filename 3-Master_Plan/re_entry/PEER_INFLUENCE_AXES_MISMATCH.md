# Peer context axes across domains

**Revised:** 10 November 2026; handoff status 11 November 2026  
**For:** Charles, CODA and COMPASS; Chapter 3 empirical alignment  
**Purpose:** Distinguish full-group performance, leave-one-out peer performance, relative standing and sigmoid-based roster pressure before comparing the Army, basketball and tenure figures.

## Handoff status (11 November 2026)

Charles has the Army **520** pipeline running on **Vantage**. He is provisioning the mosaic code next. This memo’s axis definitions are unchanged. What changed is permission to produce the comparison.

**COMPASS task now:** Specify HERO plots and Band of Excellence plots for **B1, B2, and B3** on **one frozen 520 run**. Same officers, same peer-group membership, same outcome, same filters. CODA and Charles execute the plots on Vantage. COMPASS does not own the Army notebook.

**Not this task:** Choosing the axis because one curve looks more like an inverted U. Integrating **B4** into the Army code. The survival chapter and the LG assignment chapter are separate decisions and do not change these axis definitions.

**B4 comes after** the B1–B3 comparison, and only once theta, gamma, the performance scale, and self-inclusion are written down. B4 needs each peer’s performance, not only a stored mean.

**Band of Excellence** is a sample restriction (the band where scarce distinction is at stake), not a fifth axis. See `talent/re_entry/BAND_OF_EXCELLENCE_ARMY_PORCH.md`. Report B1, B2, and B3 both on the full eligible sample (HERO) and inside the declared band (BoE). Do not switch the peer definition when switching the sample.

## What needs correcting

The historical Army figure and the documented basketball and tenure figures do not use the same horizontal quantity. The reviewed Army figure uses **own performance minus the leave-one-out peer mean**. The documented basketball and tenure comparisons use **the leave-one-out peer mean itself**. These are different questions, not interchangeable versions of “group talent.”

The previous memo also used “peer mean” too loosely and described roster pressure as though we had not yet defined it. The manuscript already defines shared roster pressure as the **average of sigmoid-transformed competitive relevance**, and the basketball comparison implements both shared and leave-one-out versions. A raw sum of peer performance is not that construct.

This revision separates four axes. It does not choose the measure that gives the strongest-looking curve, or declare roster pressure empirically superior. The 10 November text did not itself run anything. The 11 November handoff above authorizes the B1–B3 comparison on the live 520 run. The scientific question still determines which measure belongs in a comparison.

**Label change:** The previous memo’s B1 becomes **B2** below; its B2 becomes **B3**. Its proposed B3 is replaced by the properly specified **B4**. **B1** now means the full-group mean T_j. These labels organize this memo; they do not rename production columns or manuscript notation.

## Figure A remains the own-performance comparison

Figure A plots observed advancement outcomes against the individual's own measured performance, A_i. This is Charles’s “naïve plot,” a descriptive relationship, not automatically the deterministic top-K model.

The outcome must be named separately in each domain: recorded Army promotion, ever drafted, or tenure among the included cases, for example. The axis repair does not make these outcomes identical estimands or resolve follow-up and censoring differences.

## Four distinct choices for the environmental comparison

For the definitions below, G_j is a specified group at a specified time, n_j is its number of members, and i is a member of that group. A_h denotes member h’s measured performance on the declared analysis scale. It is not a claim that measured performance is intrinsic talent.

The equations assume valid performance measurements for the included members. Actual code must document missingness, zeros, exclusions and the denominator used.

### B1 — Full-group mean performance T_j

$$
T_j=\frac{1}{n_j}\sum_{h\in G_j} A_h.
$$

**Question:** How does advancement vary with the average performance of the whole group, including the focal individual?

This is the manuscript’s T_j. It is shared by all members of the same fixed group. When used as the group-quality congestion applied to individual i, the manuscript connects it to C_{Q,i}=T_{g(i)}.

Because the focal person contributes to this mean, changing their performance changes B1 even if every other member is unchanged. This is a property of the construct, not an error. Label it **full-group mean, including self**, rather than just “peer mean.”

### B2 — Leave-one-out peer mean C_{LOO,i}

$$
C_{\mathrm{LOO},i}
=\frac{1}{n_j-1}\sum_{\substack{h\in G_j\\h\ne i}} A_h,
\qquad n_j>1.
$$

**Question:** How does advancement vary with the average performance of the other members of the focal individual’s group?

This is the leave-one-out (LOO) peer mean. It is indexed by i because different members exclude different contributions. It is not generally one shared value for team j. Excluding self removes the direct inclusion of A_i in the average; it does not remove sorting, shared context or other confounding.

For the same complete group and performance scale,

$$
C_{\mathrm{LOO},i}=\frac{n_jT_j-A_i}{n_j-1}.
$$

B1 and B2 are closely related but distinct. Neither should be silently substituted for the other. In the Army code, a column called pool_tb_ratio_mean_snr_fwd is B2 when exclude_self=True; the word “mean” in its name does not make it T_j.

### B3 — Relative performance, own minus LOO peer mean

$$
D_i=A_i-C_{\mathrm{LOO},i}.
$$

D_i is explanatory notation in this memo, not a requested manuscript or code rename.

**Question:** How does advancement vary with how far the individual’s measured performance lies above or below the average of their peers?

This is a performance difference, not an ordinal rank. It is the quantity calculated by the reviewed Army pool_minus_mean_snr_fwd column. The historical display uses its standardized version, z_pool_minus_mean_snr_fwd.

A high difference can arise from high own performance, low peer performance, or both. Therefore a promotion gradient across B3 does not by itself establish a promotion gradient across peer strength. Standardizing the difference does not change that interpretation. Holding A_i exactly fixed, an increase in the peer mean produces an equal decrease in D_i; across a mixed population, own performance also varies.

The historical Army figure remains useful, labeled **promotion versus relative performance within the peer pool**. It cannot serve as the direct B1 or B2 comparison merely by changing its caption.

### B4 — Roster pressure based on competitive relevance

Roster pressure first transforms each member’s performance into competitive relevance:

$$
v_h=\sigma\!\left(\gamma(A_h-\theta)\right)
=\frac{1}{1+\exp[-\gamma(A_h-\theta)]},
\qquad \gamma>0.
$$

Theta is the performance threshold around which relevance changes most rapidly; gamma controls transition sharpness. Competitive relevance is not an individual selection probability.

The manuscript’s shared roster pressure is

$$
C_j=\frac{1}{n_j}\sum_{h\in G_j}v_h.
$$

**Question:** How does advancement vary with the concentration of competitively relevant members in the group?

The shared definition includes the focal individual and assigns every member of the same fixed group the same pressure. In the score equation, the applied value is C_i=C_{g(i)}, with S_i=A_i-\lambda C_i; selection remains a separate step. C_i is a generic congestion input in the model, not a statement that every congestion measure is roster pressure.

We have also implemented an empirical leave-one-out variant:

$$
C_{\mathrm{RP,LOO},i}
=\frac{1}{n_j-1}\sum_{\substack{h\in G_j\\h\ne i}}v_h.
$$

The latter symbol is descriptive notation here. The basketball comparison names these columns rp_shared and rp_loo. It compares them; it does not silently replace the shared manuscript specification. Use **B4-shared** and **B4-LOO** when distinguishing these variants in this memo.

## What roster pressure does and does not measure

The sequence is **transform each member’s performance, then average**. Applying a sigmoid to the group mean is generally not equivalent to averaging individual sigmoid values. Thus two groups can share the same T_j but have different roster pressure.

Averaging relevance measures competitive concentration. Summing relevance would instead produce a soft count of contenders, and would increase with group size at fixed average relevance. Summing raw performance is a third quantity. These alternatives should not share the same label.

For large gamma, shared roster pressure approaches the fraction of members above theta, with half weight for members exactly at theta. It does not become a literal number of rivals or a ratio of contenders to available positions. For finite inputs and positive finite gamma, the mathematical value lies between zero and one.

Accordingly, B4 cannot be reconstructed in general from a peer mean and group size alone. Those summaries do not retain the performance distribution needed for the nonlinear transformation. They can reconstruct a raw sum under appropriate conditions, but not sigmoid-based roster pressure.

Theta and gamma must be declared along with the performance scale, the reference population, and self-inclusion. A threshold derived from scarcity is a proposed specification requiring justification, not a consequence of the sigmoid. Different domains need a defensible mapping to the same construct; using identical numerical thresholds on incompatible raw scales would not create comparability.

Finally, a local evaluation group need not be the complete pool competing for the final opportunity. An Army senior-rater pool and a promotion-board eligibility pool are different objects unless demonstrated otherwise. The model can represent local congestion affecting scores before global selection; it does not require a fixed promotion quota within every local group. Likewise, association with roster pressure does not identify a causal negative peer effect.

## What the inspected files establish

### Army

The current Mac helper explicitly calculates pool_minus_mean as own performance minus the computed pool mean. The current config has POOL_EXCLUDE_SELF=True. With that setting, pool_tb_ratio_mean_snr_fwd corresponds to **B2** and pool_minus_mean_snr_fwd to **B3**. The plotting script defaults to z_pool_minus_mean_snr_fwd, hence B3.

The March plot provenance audit identifies the historical figure family with this difference axis. The March and April exported helpers implement legacy snapshot-by-rater grouping; the current Mac config selects active_at_eval_thru. A local config is evidence of available settings, not proof of what ran on AWS or Vantage.

As of 11 November 2026 the 520 pipeline runs on Vantage. That does not mean a B1 or B2 HERO has been produced, and no Army B4 has been validated. The March figure remains the historical B3 result. The presence of an old feather file on the offline machine is not assumed.

### Basketball

The documented canonical HERO provenance identifies poolq_loo as the LOO teammate mean of standardized performance: **B2**. This is evidence about those named figures, not every sports plot ever produced.

The existing roster-pressure comparison explicitly calculates **B1** as T_j, **B2** as loo_performance, **B4-shared** as rp_shared, and **B4-LOO** as rp_loo, from full eligible team-season rosters before focal-player filtering. The generic sports helper also distinguishes poolq_loo from pool_c_smooth_team, the shared mean sigmoid relevance.

Therefore roster-pressure implementation is further along than the old memo suggested. Legacy variables called crowding or congestion do not override these definitions.

### Tenure

The documented decision-year HERO provenance specifies the LOO mean career publication rate of other faculty in the whole department: **B2**. That saved display uses resolved outcomes and excludes censored/transferred cases. It is not automatically a common-horizon probability for all entrants.

This revision does not verify a completed tenure B4 implementation or establish that every tenure figure uses that same cohort and peer definition.

### Other domains

Audit the named figure and generating calculation before assigning a B label. Similar captions, mosaics or curve shapes are insufficient. No cross-domain B4 standard has been empirically validated by this memo.

## Keep pool membership separate from the axis choice

There are two independent decisions: **who belongs in the reference group**, and **what quantity is calculated from that group**.

The exported Army helper uses legacy snpsht_dt × snr_rater_bwd groups for the forward senior-rater measures. The current code can construct peers active at an evaluation anchor, using rating windows. Changing membership can change all four axes.

For active-at-anchor groups, different focal officers may have different dates and overlapping but nonidentical peer sets. Do not call T_j or C_j shared across an entire senior-rater identifier if the underlying roster is not actually common. Specify the group at the relevant time, or identify the focal-specific reference set.

The axis comparison should use one frozen membership definition first. A later comparison of legacy versus active-at-anchor membership is a separate sensitivity analysis.

## Recommended comparison before wider reruns

Charles has authorized that comparison on the live 520 run (see the handoff status). Use **B2, the LOO peer mean**, as the peer-strength axis to line up with the documented basketball and tenure figures. Retain **B1, full-group T_j**, as an explicit comparison and **B3** as the distinct relative-performance result already in the historical Army figure. Which axis the dissertation treats as primary is still not locked. B4 remains the model-based candidate to investigate after this comparison.

1. Identify one Army run of record and reproduce Figure A and the historical B3 figure with their actual filters, outcomes and denominators.
2. On the same focal sample and same underlying peer membership, calculate or verify B1 and B2. Preserve the original raw values and document any standardization.
3. If reconstructing B1 from stored B2, use the actual number m_i of included peers: T=(A_i+m_i*C_LOO,i)/(m_i+1). This requires a valid own value on the same scale and a reference group consisting of exactly those peers plus the focal individual. Check missing-value, zero-exclusion, duplicate-record and pool-size semantics first. The Army pool_size field may count peers rather than the full group.
4. Compare A, B1, B2 and B3 without switching to a different cohort for each curve. Report missingness and exclusions. Compute peer measures before restricting the focal people to a performance band or final record.
5. Examine B2 within declared own-performance bands, recognizing that a band only approximates fixed performance. Report support and uncertainty; small extreme bins can distort visual interpretation.
6. Add B4 only when the individual peer performances and memberships are available, and theta, gamma, scaling and self-inclusion have been specified. Preserve the distinction between shared and LOO pressure.

For reproduction, retain the historical eight equal-width bins where applicable, after checking the generating configuration. Subsequent binning comparisons should be explicit. Across domains, harmonize the construct and reporting, not numerical edges across incompatible units.

Do not choose B1, B2, B3 or B4 because it gives the clearest downturn or strongest monotonic relationship. A weak or absent peer-strength pattern is a result, not a reason to relabel relative performance as peer strength. Differently labeled analyses may coexist, but they cannot be presented as replications of the same relationship.

## What to preserve in the authorized export

For the agreed offline analysis, preserve the generating code/configuration and run identifier together with the permitted records needed to establish:

- Stable deidentified person and group identifiers, membership/rating windows and observation timing.
- Own performance and its scale; peer mean, difference and actual peer count; zero/missingness rules and relevant eligibility filters.
- Outcome coding and event/follow-up information, so recorded proportions, cumulative incidence and fitted predictions remain distinguishable.
- Individual peer-performance records at the relevant times, or another sufficient approved representation for the declared roster-pressure calculation.

A final-row-per-officer extract with only A_i, a peer mean and a difference may suffice for some axis comparisons but cannot generally support new theta/gamma experiments. Preserve the full eligible peer reference population needed for aggregation, even when only a subset of officers appears in the plot. Export scope remains for Charles and the PDE/Vantage team to determine.

## What remains to decide

The near-term display is settled: HERO and Band of Excellence plots for B1, B2, and B3 on one frozen 520 run. Still open: the authoritative Army membership and time definition for that run, and, after the comparison, whether B4-shared or B4-LOO is the empirical question and how theta and gamma are set. Do not interpret B4 across domains before that calibration is written down.

The Army March result remains a relative-performance finding. Its role in the dissertation can be preserved without treating it as the same axis as the basketball and tenure peer-mean findings. Roster pressure is a precisely defined candidate explanation; it has not been established as the universal replacement for those empirical measures.

## Sources and revision record

This revision uses local code and saved records, not a new analysis of Army data:

- [Current Army helper](../../talent/talent_pipeline/add_cum_oer_metrics_mod_working.py) and [config](../../talent/talent_pipeline/pipeline_config.py).
- [March exported helper](../../talent/Army_AWS_download/TALENT_NET_export_20260320-1000/add_cum_oer_metrics_mod_working.py) and [April exported helper](../../talent/Army_AWS_download/TALENT_NET_export_20260421-0802/add_cum_oer_metrics_mod_working.py).
- [Army HERO plotting script](../../talent/re_entry/army_hero_slide_plot.py), [plot provenance audit](ARMY_PLOT_PROVENANCE_AUDIT.md), [column inventory](../../talent/documents/512_520_CELL_COLUMN_INVENTORY.md) and [Chapter 3 working record](_DISPOSABLE_Ch3_data_empirics_thread.md).
- [Saved model chapter](../../5-Manuscript/04_Model/drafts/Model_Chapter_Shared_Working_Draft.docx), especially the competitive-relevance and roster-pressure definitions.
- [Basketball roster-pressure calculation](../VECTOR_work/new_VECTOR_work/manuscript_figures/section_4_5/roster_pressure_comparison/roster_pressure_analysis.py), function add_roster_pressure, and [sports pool helper](../../sports/tier1_pool_assignment.py), function add_team_pool_columns.
- [Canonical basketball HERO provenance](HEROs_and_PASSes/pass_a/HERO_q16_allt_min20_mg10_9_21_last_ps_provenance.json).
- [Tenure HERO provenance](HEROs_and_PASSes/tenure_sandbox/hero/HERO_tenure_q16_decision_dept_loo_infHM_provenance.json).

**10 November revision:** At Charles’s request, separated T_j from LOO peer mean, reassigned all B labels consistently, restored the sigmoid-average definition and existing shared/LOO implementation, and removed the proposed rule of choosing an axis by the strength of its curve. Preserved the Army provenance caveats. No manuscript, data, code or figures were changed, and no models were run.

**11 November handoff:** Vantage 520 is running. Added the COMPASS task (B1–B3 HERO and Band of Excellence on one frozen run; B4 later). Updated the sentences that still said no Vantage run existed and that new runs were not authorized. No new figures were produced for this edit.

The [previous memo](../VECTOR_work/new_VECTOR_work/manuscript_backups/peer_axes_before_B1_B4_20261110.md) is retained for history. Its B labels and proposed raw-sum roster-pressure definition are superseded by this revision.

