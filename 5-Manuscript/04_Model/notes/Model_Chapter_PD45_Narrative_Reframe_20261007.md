# Chapter 4 working reframe after PD45

**Status:** Proposed prose and section order for Charles's review, not an edit to the shared Word draft. Based on Alex and Charles's October 7 conversation in `transcripts/20261007_Paper_Directions_45_otter_ai_transcript.docx`, especially Alex at 04:16–06:14 and 00:00–03:35 (the transcript export places these passages out of time order). Scholar VECTOR's separate handoff has not yet been located and may refine this map.

## The chapter's route through the model

Begin with the advancement decision. Suppose each person has an underlying performance characteristic $A_i$. In the simplest benchmark, a decision maker observes it perfectly, ranks candidates by $A_i$, and awards the $K$ available opportunities to the top $K$. This establishes what the model is trying to explain before introducing a team-formation algorithm.

Next relax perfect observation. A stochastic **SELECT** rule makes advancement uncertain while preserving the limited number of opportunities. The intended exact-$K$ rule draws one winner at a time from the remaining candidates with conditional probability proportional to $\exp(S_i/t_{\mathrm{SELECT}})$. In the talent-only benchmark, $S_i=A_i$. The temperature governs how strongly higher scores are favored; it does not itself estimate a literal measurement-error distribution for $A_i$. The legacy implementation and the empirical fitting likelihood require their existing caveats later in the chapter.

Then explain what the talent-only benchmark omits. People spend time on teams, where peers can become credible competitors for attention and advancement. Define the congestion quantity from those peers, introduce its smooth threshold (sigmoid) as specified in the existing model, and let the ranking score become $S_i=A_i-\lambda C_i$. Keep **SCORE** (how candidates are ranked) separate from **SELECT** (how winners are chosen). This is the central mechanism. Discuss possible benefits of peers in motivation or future work, without treating a development benefit minus a competitive drawback as an additional fitted component of this model.

Finally ask where those teams come from. Initially the model can take teams as given. For simulations, **ASSIGN** constructs teams and allows their composition to be assortative rather than random. Assignment is therefore a necessary simulation device and a source of variation in competitive environments, but it is not a coequal prediction target alongside score and selection. This is the order of *exposition*. A simulated person's chronological path can still be **ASSIGN → SCORE → SELECT**.

## Draft opening for discussion

Scientific organizations often advance only a limited number of people from a larger pool of capable contributors. A natural starting point is to imagine that each person has an underlying performance characteristic, $A_i$, which the organization can observe perfectly. If $K$ opportunities are available, the $K$ highest-performing people are selected. This benchmark makes the role of scarcity explicit, but it leaves two consequential features of actual decisions out of view.

First, performance is not perfectly observed. Selection may therefore favor stronger candidates without reproducing the same ranking every time. We represent this uncertainty with a stochastic selection rule that still awards exactly $K$ opportunities. Second, contributors are evaluated after spending time among peers. Strong peers may also be credible alternatives for the same scarce opportunities. We capture this competitive pressure in a congestion term that changes a candidate's **score for advancement** before selection occurs. The question is whether people with comparable own performance can face different chances of advancement because the set of plausible competitors around them differs.

Team formation enters once that mechanism is clear. Empirical teams can be observed directly; simulations need a way to construct them. Our assignment procedure creates groups with specified roster sizes and allows similarity in underlying performance to shape who joins whom. It generates the peer configurations on which congestion depends. The model then scores individuals within those configurations and selects recipients of the limited opportunities.

## What changes in the current Word draft

1. Revise the opening that currently presents ASSIGN, SCORE, and SELECT as three equal scientific stages. Open instead with the talent-only benchmark and scarce selection.
2. Move the current long **ASSIGN** discussion, now before **SCORE**, after the scoring and selection mechanism. Introduce team membership briefly before congestion, then explain its simulation construction later.
3. Keep the detailed sigmoid congestion definition and $S_i=A_i-\lambda C_i$; check its indexing against the current notation before moving equations.
4. Move the current $B-D$ discussion out of the formal scoring presentation. Preserve it as motivation or future work, explicitly separate from the implemented congestion score.
5. Preserve the verified exact-$K$ versus legacy-code caveat, and the separate Bernoulli maximum-likelihood fitting account. Neither mismatch should be smoothed away by the narrative revision.

**Verification still needed before revising the shared chapter:** Scholar VECTOR's handoff; the precise score and sigmoid notation in the live Word file; and the intended placement of parameter-regime history and empirical fitting after this exposition change. No new simulation or Romania outcome analysis is implied by this editorial map.
