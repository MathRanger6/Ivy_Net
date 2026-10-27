Source: `/Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/JAZZ_Model_Chapter_Shared_Working_Draft.pdf` | Date read: 2026-10-27 | Prepared by helper agent for FOUNDY; quotes to be spot-checked.

# Model chapter (JAZZ draft): handoff for the introduction

PDF page = printed page. Quotes are verbatim; [bracketed] math is normalized from garbled glyphs.

## 1. Structure

- Ch. 4 "A model of competitive congestion and advancement"; 4.1 Individual performance and success in groups — p1
- 4.2 Selecting the highest performing individuals — p2: 4.2.1 Performance and the selection population p2; 4.2.2 The score and the selection rule p3
- 4.3 Allowing uncertainty in selection — p4: 4.3.1 Gibbs-weighted selection without replacement p4; 4.3.2 Selection temperature and limiting behavior p6
- 4.4 Introducing local competitive congestion — p7: 4.4.1 A first approximation using average peer performance p9; 4.4.2 From average peers to credible competitors p11; 4.4.3 Aggregating competitive relevance into a group adjustment p12; 4.4.4 How local composition changes global comparisons p15
- 4.5 Mathematical behavior and parameter regimes — p16: 4.5.1 Threshold location and transition sharpness p17; 4.5.2 Penalty strength and score scale p21; 4.5.3 Scarcity and the selection margin p25; 4.5.4 Interpreting selection patterns across group environments p29
- 4.6 Generating artificial groups with controlled sorting — p33: 4.6.1 Representing individuals and groups p34; 4.6.2 Sequential assignment with evolving centroids p34; 4.6.3 Measuring the sorting that results p39; 4.6.4 Using artificial groups to investigate congestion p41
- 4.7 What the completed mechanism experiments establish — p42: 4.7.1 Experimental setting and interpretation p42; 4.7.2 Congestion can change winners without similarity preference p43; 4.7.3 Penalty strength and the visibility of the tail p44; 4.7.4 Assignment preference and scarcity p45; 4.7.5 What remains to be established p47
- 4.8 The bridge to empirical fitting — p48
- Appendix 4A Technical qualifications and the historical fitting record — p51: 4A.1 The intended stochastic rule and legacy software p51; 4A.2 Differences between the stated selection rule and earlier implementations p52; 4A.3 Normalization and threshold construction p54; 4A.4 Saved estimates and parameter transfer p55; 4A.5 Alternative congestion specifications p57; 4A.6 Expected sorting under random assignment p58; 4A.7 From competitive relevance to selection outcomes p61; 4A.8 Why a shared penalty cancels under local selection p64
- Appendix 4B Sources for the equations and completed results — p66

## 2. Phenomenon statement (p1)

"Strong peers can accelerate individual development and performance, but those same peers can also intensify competition for attention, responsibility, and recognition. The same environment that elevates performance can therefore make advancement more difficult, with the net effect varying across individuals. We observe the phenomenon that similar individuals placed in different environments may consequently experience very different chances of ultimately advancing."

"What features of an individual’s local environment determine whether that environment ultimately helps or hinders advancement, and how do those effects interact with individual performance? This chapter connects the local social environments studied in network science with the allocation of recognition and advancement studied in the science of success." … "The phenomenon, rather than any one institutional setting, is the object of the model."

## 3. Definitions

1. **Naïve benchmark** (p2): "We call this performance-only, deterministic top-[K] model the naïve benchmark." A model, not the naive plot; naive plot never appears, and HERO (pp. 53, 67 only) is never defined.
2. **SCORE vs SELECT** (p4): "Thus, SCORE establishes competitive standing and SELECT allocates the available opportunities."
3. **Top-K** (p3): "SELECT then ranks individuals by [S_i] and awards the [K] available opportunities to the [K] highest-scoring candidates."
4. **Scarcity** (p3): "The selection fraction [K/N] describes the selection scarcity".
5. **Gibbs weights** (p4): "Gibbs weighting gives higher-scoring candidates a greater chance of selection while allowing lower-scoring candidates to be selected." Weight: exp(S_i/t_sel).
6. **Selection temperature** (p4): "Lower temperatures give score differences greater influence; higher temperatures make the selection probabilities more similar."
7. **Congestion** (p8): "We focus here on this competitive pressure, which we call congestion". Score: S_i = A_i − λC_i.
8. **Full-group mean** (p9): "Let [T_j] denote the mean performance of all [n_j] members of group [j], including the focal individual".
9. **Leave-one-out (LOO) peer mean** (p9): "A leave-one-out peer mean instead averages only the other members of the group". Correct (eq. 4.11).
10. **Roster pressure** (p11): "We now introduce roster pressure as a third measure of congestion, based on the competitive relevance of a group’s members."
11. **Band of excellence** (p30): "strong performers who are credible contenders but whose selection is not assured".
12. **Maximum likelihood estimation (MLE)** (p48): "The method selects parameter values that make the observed outcomes most probable under a specified probability model." The completed fit is softmax-Bernoulli, not exact-K.

## 4. Claims the introduction must set up

Sources are my suggestions, not the chapter's; verify before use.

1. p1 "those same peers can also intensify competition for attention, responsibility, and recognition". Spillovers (Mas & Moretti 2009) vs relative standing (Davis 1966; Marsh 1987).
2. p1 "similar individuals placed in different environments may consequently experience very different chances of ultimately advancing". The introduction's naive and HERO plots across domains.
3. p1 "connects the local social environments studied in network science with the allocation of recognition and advancement studied in the science of success". Merton 1968; Fortunato et al. 2018.
4. p1 "The phenomenon, rather than any one institutional setting, is the object of the model." Show the domains share groups, noisy records, and scarce slots.
5. p4 "Real selection processes, however, contain uncertainty." Noisy review (Pier et al. 2018); choice models (Luce 1959; Plackett 1975).
6. p25 "meeting a qualification standard does not guarantee selection". Tournament theory (Lazear & Rosen 1981).
7. p11 "Improvement by someone far below the level needed to contend for advancement may raise the group mean while changing the competitive environment very little." Competitive crowding (Bothner et al. 2007).
8. p15 "Competition for attention, opportunities to stand out, and sponsorship provides possible explanations". Cumulative advantage (Merton 1968); mentorship (Ma et al. 2020).
9. p16 "This is a modeling choice, not a claim that advancement decisions are entirely global." Facts on centralized selection; a shared penalty matters only across groups (4A.8).
10. p29 "A rising selection rate can reflect the concentration of high-performing individuals in stronger groups." Sorting confound (Manski 1993); assortative mixing (Newman 2002).

## 5. Literature

There is no external bibliography. p66: "They are a reproducibility record rather than an external literature bibliography." The 17 entries are repository files, so none has an author, year, or venue:

[1] MBB replay memo + COMPASS log; [2] PD20 likelihood explainer and notes; [3] tier1_pool_assignment.py; [4] pd21_draft_bernoulli_mle.py; [5] SCOUT response memo, inverted-U diagnostic script; [6] tier1 script, MBB replay memo; [7] diagnostic script; [8] ρ/H_sort calibration JSON; [9] 2009–2021 MLE JSON; [10] 2013–2021 MLE JSON; [11] MBB replay memo; [12] MLE_basics.md; [13] PD44 work map; [14]–[17] ASSORT September 2026 simulation reports and briefing.

Every entry is cited, so none is orphaned. The Plackett–Luce sentence on p5 cites [1], but the Plackett–Luce source is [2]. Network science, the science of success (p1), Plackett–Luce (p5), and Wilson intervals (p32) are named with no literature citation.

## 6. Conflicts and risks

**(a) LOO described as own minus peer mean: none found.** Two related problems. First, the selection curve in 4.5.4 uses the full-group mean, which includes the person's own performance; p30: "A curve plotted against [T_j] therefore compares selection across groups with different average performance". Figures 4-4, 4-5, and 4-7 use the LOO mean instead. Second, p15 calls LOO "the initial leave-one-out specification", contradicting p10: "Its use as a descriptive measure does not require us to use it as the congestion term in the selection score."

**(b) Universal inverted-U: none found; disclaimed.** p29: "Congestion can change who is selected without producing an inverted-U curve."

**(c) Causal language: results are disclaimed** (pp. 31, 32, 43). The risk is p1: "We observe the phenomenon that similar individuals placed in different environments may consequently experience very different chances of ultimately advancing." Nothing there supports "We observe", and "consequently" implies causation.

**(d) One congestion measure as settled: partial risk.** Three measures are offered, but roster pressure is privileged. p58: "The refined model retains the full-group mean as a measure of shared roster pressure". p57 softens this: "These choices require explicit identification wherever their results are compared."

**(e) LG prominence: moderate risk.** It is framed as a tool (pp. 33–34): "Assignment is therefore a device for studying the consequences of group composition." But it gets a full section (4.6), and p34 names it: "The mechanism used here, referred to as the LG mechanism". Its preference parameter ρ drives the headline results in 4.7.2 and 4.7.4.

**(f) Basketball framing: high risk from 4.5.4 on.** All evidence is basketball. p48: "The completed fitting work used observed basketball rosters". Army promotion (p46) and tenure (p16) get one mention each; admissions none.

Drafting problems: an empty "Summary" heading (p16); the broken "Observed rosters already We represent" (p34); an orphan fragment reusing equation numbers (4.31)–(4.33) (pp. 65–66).

## 7. Figures

- 4-1 (p20): logistic competitive relevance vs performance; varying γ and θ.
- 4-2 (p22): nine people; scores change continuously with λ, winners in discrete steps.
- 4-3 (p28): same nine people at three vs one place; quantile-aligned θ.
- 4-4 (p32): basketball draft rate vs LOO teammate mean; all vs top 7%.
- 4-5 (p33): draft rate vs LOO teammate mean, two high-performance bands.
- 4-6 (p38): toy LG assignment: six people, two groups, evolving centroids.
- 4-7 (p45): 2015 simulation, λ = 0–4; equal-width vs quantile bins.
- 4-8 (p47): 2015 simulation, ρ = 1 vs 0.05 at 50% and 1% selection.
