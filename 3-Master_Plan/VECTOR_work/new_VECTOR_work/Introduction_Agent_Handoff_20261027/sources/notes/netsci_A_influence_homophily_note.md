# Network-science background, cluster A: influence (contagion) vs. homophily (sorting)

Source extracts for the dissertation introduction. Built 2026-10-28 from the PDFs listed in `FOUNDY_Intro.bib` (text via `pdftotext -layout`; all 13 PDFs had a text layer, no OCR used).

**Conventions**

- Quotes are copied verbatim from the PDF text layer. Line-break hyphens introduced by the journal layout (e.g. "con-temporaneous") are rejoined; nothing else is changed. `[...]` marks an omission.
- "p." = printed journal page. When the PDF page differs it is given as "PDF p.".
- "Channel / source" lines are **assistant judgment**, not the authors' framing. Channels: development (what a person becomes), evaluation (how a performance is measured/perceived), selection (who wins a scarce slot). Sources: peers vs. organization.
- Limitation tags: [small data], [imperfect measure], [single system], [no model of mechanism], [model not fit to data], [outcome is not selection].

---

## Assistant synthesis (to be written after all papers are read)

---

## 1. Christakis & Fowler 2007 — The spread of obesity in a large social network over 32 years

**Citation.** Christakis, Nicholas A., and James H. Fowler. 2007. "The Spread of Obesity in a Large Social Network over 32 Years." *New England Journal of Medicine* 357 (4): 370–379. DOI: 10.1056/NEJMsa066082. (PDF p. 1 = printed p. 370; PDF p. n = printed p. 369 + n.)

**Data / setting / sample / years.** Framingham Heart Study, Offspring Cohort as 5,124 "egos"; 12,067 egos plus alters connected at some point, 1971–2003. Ties reconstructed from archived handwritten administrative tracking sheets (friends, siblings, spouses, neighbors). 38,611 observed social and family ties to the 5,124 egos; 3,604 unique observed friendships (about 0.7 friendship ties per ego); 45% of egos connected by friendship to another person in the network (p. 372). Obesity = body-mass index (BMI) ≥ 30.

**Design.** Observational, longitudinal. Logistic regression of ego's obesity at t+1 on ego's obesity at t, alter's obesity at t and t+1, and covariates; generalized estimating equations (GEE) (pp. 372–373).

**Main findings (verbatim).**

> "A person's chances of becoming obese increased by 57% (95% confidence interval [CI], 6 to 123) if he or she had a friend who became obese in a given interval. Among pairs of adult siblings, if one sibling became obese, the chance that the other would become obese increased by 40% (95% CI, 21 to 60). If one spouse became obese, the likelihood that the other spouse would become obese increased by 37% (95% CI, 7 to 73). These effects were not seen among neighbors in the immediate geographic location." (Abstract, p. 370)

> "Discernible clusters of obese persons [...] were present in the network at all time points, and the clusters extended to three degrees of separation. These clusters did not appear to be solely attributable to the selective formation of social ties among obese persons." (Abstract, p. 370)

> "Between mutual friends, the ego's risk of obesity increased by 171% (95% CI, 59 to 326) if an alter became obese. In contrast, there was no statistically meaningful relationship when the friendship was perceived by the alter but not the ego (P = 0.70). Thus, influence in friendship ties appeared to be directional." (p. 376)

**Sorting vs. influence.** Names three explanations explicitly: homophily, shared unobserved contemporaneous events (confounding), and induction:

> "We considered three explanations for the clustering of obese people. First, egos might choose to associate with like alters ("homophily"). Second, egos and alters might share attributes or jointly experience unobserved contemporaneous events that cause their weight to vary at the same time (confounding). Third, alters might exert social influence or peer effects on egos ("induction")." (p. 372)

Strategy: (a) lagged ego outcome and lagged alter outcome, "The use of a lagged independent variable for an alter's weight status controlled for homophily." (p. 373); (b) a directionality test, "if unobserved factors drove the association between the ego's obesity and the alter's obesity, then the directionality of friendship should not have been relevant." (p. 373); (c) null neighbor effect and no distance gradient used to argue against a shared local environment (p. 377).

**Limitations.**

- The authors state they cannot test mechanism: "Obesity in alters might influence obesity in egos by diverse psychosocial means [...] Other mechanisms are also possible. Unfortunately, our data do not permit a detailed examination." (p. 377) **[no model of mechanism]**
- Single cohort in one town; friendship ties come from administrative follow-up tracking sheets, not a network survey. The sheets record all first-order relatives "and at least one "close friend" at each of seven examinations between 1971 and 2003" (p. 372), so friendship ties are sparse (0.7 per ego). **[single system] [imperfect measure]** (tagging is assistant reading).
- Homophily handled by regression control, not by design; this is what papers 2, 3, 5, and 6 contest. (assistant reading)
- Outcome is a health state (BMI), not a competitive outcome. **[outcome is not selection]**

**Channel / source (assistant judgment).** Development (peers shape what a person becomes: weight, norms about weight). Source: peers (friends, siblings, spouses); "organization" absent except as the neighborhood/geography null.

---

## 2. Cohen-Cole & Fletcher 2008 — Is obesity contagious? Social networks vs. environmental factors

**Citation.** Cohen-Cole, Ethan, and Jason M. Fletcher. 2008. "Is Obesity Contagious? Social Networks vs. Environmental Factors in the Obesity Epidemic." *Journal of Health Economics* 27 (5): 1382–1387. DOI: 10.1016/j.jhealeco.2008.04.005. (PDF p. n = printed p. 1381 + n.)

**Data / setting / sample / years.** Not Framingham. They re-run the Christakis–Fowler (CF) specification on the National Longitudinal Study of Adolescent Health (Add Health), "a national sample of 7–12th graders in 1994/1995" followed into early adulthood (p. 1383). "[W]e have information on friends for approximately 5000 individuals, nearly 2000 of whom are followed over time along with at least one same-sex friend. [...] This sample size gives us nearly 4000 person-year observations, slightly larger than the 3000 used by CF." (p. 1383). Table 1: "analysis sample N = 1988; two observations per person" (p. 1384). Community = the high school attended (p. 1385, fn. 18).

**Design.** Observational re-analysis / robustness check (econometric). Replicate CF's logit and OLS on Add Health, then add school-specific time trends (contextual / environmental confounders) and individual fixed effects (friend selection).

**Main findings (verbatim).**

> "We find that point estimates of the "social network effect" are reduced and become statistically indistinguishable from zero once standard econometric techniques are implemented. We further note the presence of estimation bias resulting from use of an incorrectly specified dynamic model." (Abstract, p. 1382)

> "After controlling for environmental confounding (through school-specific time trends), our estimate falls by over 30% to 0.037. Finally, we control for friendship selection by controlling for individual fixed effects. With this inclusion, the coefficient of interest declines further and becomes statistically indistinguishable from zero." (p. 1386)

> "Though we do not completely rule out the possibility of induction and person-to-person spread of obesity, our results suggest that shared environmental factors can cause the appearance of social network effects." (p. 1386)

Replication baseline for context: "we find the odds that an Ego becomes obese increase by 80% if his or her Alter is also obese. Broadly, this is in line with the CF finding of 71% for same-sex friends." (p. 1385)

**Sorting vs. influence.** Uses Manski's (1993) three-way split and maps it onto CF's terms:

> "The first is that individuals could choose their friends based on factors associated with weight or weight trajectories. In economics, this is typically referred to as selection (CF as homophily). [...] Second, individuals may adjust behavior because of exposure to common influences. These effects are typically referred to as contextual influences (CF as confounding). [...] Finally, individuals may alter their behavior as others in their group change theirs. Economists are now generally labeling this an endogenous social effect (CF as social network effects)." (p. 1383)

Critique of CF's controls: "Their claim is that "the use of a lagged independent variable for an Alter's weight status controlled for homophily." Unless selection is conditioned only on this variable, this statement is spurious." (p. 1385). On the directionality test: "Since CF never directly control for environmental factors, we view their results using directionality of friendship nominations as suggestive rather than conclusive." (p. 1385).

**Limitations.**

- Different dataset from the one they critique (adolescents in schools vs. adults in Framingham); the authors acknowledge "comparing results across datasets that are quite different in design and focus is usually fraught with difficultly" (p. 1386; "difficultly" is the printed spelling). **[single system]**
- One friend per ego: "We select only one friend to be consistent with CF." (p. 1383, fn. 10). **[imperfect measure]**
- School-specific trends are a coarse proxy for environment: "Though one, in principle, would want many more controls to account for additional contextual effects, we will note shortly that the endogenous effect vanishes even with this relatively simple characterization." (p. 1386)
- Null result is a loss of significance, not an estimate of zero (point estimate 0.033 with CI −0.043 to 0.109 in Table 3, p. 1386). (assistant reading)
- Health outcome. **[outcome is not selection]**

**Channel / source (assistant judgment).** Development, with the key move being to attribute similarity to the shared environment (school / community) rather than peers. Source: organization/environment (the school as context) vs. peers. Useful as the canonical "context, not contagion" counter-reading.

---

## 3. Fowler & Christakis 2008 — Estimating peer effects on health in social networks: a response

**Citation.** Fowler, J. H., and N. A. Christakis. 2008. "Estimating Peer Effects on Health in Social Networks: A Response to Cohen-Cole and Fletcher; and Trogdon, Nonnemaker, and Pais." *Journal of Health Economics* 27 (5): 1400–1405. DOI: 10.1016/j.jhealeco.2008.07.001.

**PAGE-NUMBER WARNING.** The PDF in the library is the **NIH Public Access author manuscript** (PMC), not the typeset article. It carries only manuscript page numbers ("Page 1" … "Page 8"). Journal page numbers 1400–1405 **could not be determined** from this file. All page cites below are "MS p." = manuscript page = PDF page. Wording may differ slightly from the published version.

**Data / setting / sample / years.** Two datasets. (a) Add Health re-analysis using all observed friendships and wave-updated friendship data (Waves 1–3): Table 1 N = 8,504 (models 1–2) and 4,742 (model 3) (MS p. 7). (b) Framingham Heart Study Social Network (FHS-Net) re-estimated with ego fixed effects: Table 2 N = 2,396, "843 Fixed Effects Not Shown" (MS p. 8). Population contrast stated by the authors: "Unlike the FHS-Net, which followed adults over a 32-year period (average age 38 in 1971), AddHealth followed adolescents over a 7-year period (average age 16 in 1995)." (MS p. 1)

**Design.** Observational re-analysis and rebuttal. Re-estimates on Add Health with and without school trends; directionality test (named friend → namer vs. namer → named friend); fixed-effects re-estimation on Framingham.

**Main findings (verbatim).**

> "What is crucial to note here, however, is that the Framingham estimates actually fall inside the confidence intervals of the CCF results for all five specifications. That is, CCF cannot reject the null hypothesis that the Framingham estimates are the true values." (MS p. 2)

> "In model 3 of Table 1, we show that there is no evidence that named friends are influenced by namers (p=0.90), confirming our results in the FHS-Net and providing additional evidence in favor of the causal interpretation regarding social influence in weight behaviors." (MS p. 3)

> "Table 2 shows that when we include fixed effects in our FHS-Net analyses, we find a significant influence of friend's BMI on ego's BMI, and the size of the effect is about the same at 0.05." (MS p. 4)

Replication dispute: "We attempted to replicate the CCF results but were unable to do so [...] We then contacted CCF to ask for the code they used to generate their results. They were unwilling to share this code." (MS p. 2). They report that Cohen-Cole & Fletcher (CCF) "'lock in' Wave 1 friends" and argue "This assumption by CCF stacks the deck against finding an effect" (MS p. 2).

**Sorting vs. influence.** Defends three identification arguments: (1) directionality, "If contextual effects are spuriously driving the relationship between ego and alter, then there is no reason to expect a directional result." (MS p. 3); (2) no distance decay, "We specifically find that the relationship does not decay with physical distance, even up to hundreds of miles away (Fig. 3 in CF)." (MS p. 3); (3) homophily, "In short, this model conditions on the initial weights of the two parties connected via a tie. Additional Monte Carlo simulation results documenting that homophily (ranging from no homophily to complete homophily) does not result in bias in the estimates of induction in this model specification are available at the authors' websites." (MS p. 4)

**Limitations.**

- Still observational; concedes the general difficulty: "causal inference in dyads, let alone in broader social networks, is difficult (Manski 1993)." (MS p. 1). The directionality argument is the one Shalizi & Thomas (paper 5) later show is not sufficient in general. (assistant cross-reference)
- The homophily argument assumes selection is on observed initial weight; the simulations are cited but not in the paper ("available at the authors' websites"). **[imperfect measure]**
- They acknowledge their Framingham time controls "might not capture regional variation within time blocks" (MS p. 4).
- Health outcome. **[outcome is not selection]**

**Channel / source (assistant judgment).** Development; source: peers. The exchange is useful mainly as evidence that the peer-vs-context split was contested on the same data with competing specifications and no design-based resolution.

---

## 4. Aral, Muchnik & Sundararajan 2009 — Distinguishing influence-based contagion from homophily-driven diffusion in dynamic networks

**Citation.** Aral, Sinan, Lev Muchnik, and Arun Sundararajan. 2009. "Distinguishing Influence-Based Contagion from Homophily-Driven Diffusion in Dynamic Networks." *Proceedings of the National Academy of Sciences* 106 (51): 21544–21549. DOI: 10.1073/pnas.0908800106. (PDF p. n = printed p. 21543 + n.)

**Data / setting / sample / years.** Yahoo! instant-messaging (IM) network: "the global network of daily instant messaging (IM) traffic among 27.4 million users of Yahoo.com" combined with "data on the day-by-day adoption of a mobile service application launched in July 2007 (Yahoo! Go)" (pp. 21544–21545). Covariates: "40 time-varying and 6 time-invariant individual and network characteristics" (p. 21545). Adoption window: Fig. 2 covers "July 1 to October 29, 2007" (p. 21545); the text refers to "the 5-month period" (p. 21545). Network: "⬎14 billion page views and sent 3.9 billion messages over 89.3 million distinct relationships" (p. 21545).

**Design.** Observational; dynamic propensity-score matched sampling. Treatment = having 1, 2, 3, or 4+ adopter friends; treated users matched to untreated users with the same estimated likelihood of treatment given observables (p. 21546). Compared with "random matching" (no adjustment for homophily).

**Main findings (verbatim).**

> "We find that previous methods overestimate peer influence in product adoption decisions in this network by 300 –700%, and that homophily explains >50% of the perceived behavioral contagion." (Abstract, p. 21544; spacing around the en dash as printed)

> "Over half of the cumulative adoption of treated users (those with at least one adopter friend) can be attributed to homophily effects (Fig. 4 A and B). The remaining adoption events (49.8%) represent the upper bound of influence effects established by our matched sample estimates." (p. 21547)

> "Comparisons to random therefore incorrectly imply that influence grows superlinearly with the number of adopter friends, whereas there is simply greater homophily in larger groups of adopters." (p. 21547)

**Sorting vs. influence.** Treats homophily as selection bias in a treatment-effects frame: "Homophily in this case creates a selection bias because treatments are not randomly assigned: adopters are more likely to be treated because of similarity with their neighbors." (p. 21546). Matching on observables yields an upper bound on influence: "This procedure establishes upper bounds on the degree to which influence (rather than homophily) explains assortative mixing and temporal clustering in networks." (p. 21546). Also notes heterogeneity: stronger ties and denser local networks raise adoption "controlling for homophily" (p. 21547).

**Limitations (authors' own).**

> "Although the matching process accounts for homophily on all observed characteristics and those unobserved or latent characteristics that are correlated with what we observe, unobserved and uncorrelated latent homophily and unobserved confounding factors or contextual effects (such as correlated exposure to advertising among friends or information from common unobserved friends) may also contribute to assortative mixing and temporal clustering." (p. 21548) **[imperfect measure]**

- One product, one platform: "Yahoo! Go 2.0 does not exhibit direct network externalities [...] We suspect that peer influence effects differ for products with direct network externalities" (p. 21548). **[single system]**
- No tie-formation model: "extending these methods to account for selection processes could prove useful in cases where selection effects are more prevalent" (p. 21548). **[no model of mechanism]**
- Outcome is product adoption. **[outcome is not selection]**

**Channel / source (assistant judgment).** Development in a weak sense (adoption of a behavior/product). Source: peers. The relevant contribution is quantitative: naive peer estimates in big observational networks can be several-fold too large because of sorting.

---

## 5. Shalizi & Thomas 2011 — Homophily and contagion are generically confounded in observational social network studies

**Citation.** Shalizi, Cosma Rohilla, and Andrew C. Thomas. 2011. "Homophily and Contagion Are Generically Confounded in Observational Social Network Studies." *Sociological Methods & Research* 40 (2): 211–239. DOI: 10.1177/0049124111404820.

**PAGE-NUMBER WARNING.** The library PDF is the **arXiv preprint** (arXiv:1004.4704v3 [stat.AP], 30 Nov 2010; 27 pp.), not the typeset journal article. Journal page numbers 211–239 **could not be determined** from this file. Cites below are "arXiv p." (the page number printed at the foot of the preprint, which equals the PDF page). Wording differs slightly from the journal version: the bib's abstract (journal version) reads "The authors consider [...] on his or her behavior", where the preprint reads "We consider [...] on their behavior". If Charles quotes this paper, check against the published version.

**Data / setting / sample / years.** No empirical data. Theoretical argument with causal graphs plus toy simulations; the main toy network has n = 400 nodes, each with one declared friend, mimicking the Christakis–Fowler setup (arXiv pp. 9–10), and is regenerated 5,000 times (arXiv p. 10).

**Design.** Theoretical / proof (identification argument using directed acyclic graphs and d-separation) plus simulation.

**Main findings (verbatim).**

> "We show that, generically, all of these are confounded with each other. Distinguishing them from one another requires strong assumptions on the parametrization of the social process or on the adequacy of the covariates used (or both). In particular we demonstrate, with simple examples, that asymmetries in regression coefficients cannot identify causal effects, and that very simple models of imitation (a form of social contagion) can produce substantial correlations between an individual's enduring traits and their choices, even when there is no intrinsic affinity between them." (Abstract, arXiv p. 1)

> "More precisely, latent homophily and contagion are generically confounded with each other (section 2), and any direct contagion effects cannot be nonparametrically identified from observational data. To identify contagion effects, we need either strong parametric assumptions or strong substantive knowledge that lets us rule out latent homophily as a causal factor." (arXiv p. 3; footnote marker "2" after "data" omitted)

> "This is the result of the type that was cited in Christakis and Fowler (2007); Fowler and Christakis (2008) but produced without any network interaction. [...] It is evident from the histogram that this null distribution is not centered at zero, and about 77% of the sample values are positive, even though there is really no effect. Thus, latent homophilous variables can produce a substantial apparent contagion effect, including the asymmetry expected of actual contagion." (arXiv p. 12; footnote marker "11" omitted)

> "We have seen that when there is latent homophily, contagion effects are unidentifiable, and even the presence of contagion cannot be distinguished observationally from a causal effect of the homophilous trait." (Conclusion, arXiv p. 20)

**Sorting vs. influence.** This is the formal statement that sorting on an unobserved trait and influence cannot be separated by observational data without strong assumptions. It directly targets the Christakis–Fowler directionality (asymmetry) argument and shows a latent-homophily model reproduces "mutual > named > namer" (arXiv p. 12). Constructive options offered (section 4): identifying contagion via non-neighbors, partial-identification bounds, and conditioning on detected network communities, the last with a caveat: "such control-by-clustering will generally be unable to eliminate the confounding" (arXiv p. 20). Burden statement: "this still places the burden on the investigator to pursue as many possible latent factors as may be present — an extremely onerous task in a multi-decade observational study — or to work exclusively with experimental data" (arXiv p. 12).

**Limitations.**

- Negative / identification result; toy parameter values are illustrative: "The parameter values in this model were not chosen to maximize either the apparent contagion effect or its asymmetry, merely to demonstrate their presence." (arXiv p. 12) **[model not fit to data]**
- Says nothing about the size of contagion in any real system. (assistant reading) **[no model of mechanism]** for any specific outcome.
- **[outcome is not selection]** (generic behavior Y).

**Channel / source (assistant judgment).** Method-level; applies to any peer-effect claim in development or evaluation. Most relevant implication for the dissertation: observational similarity among people who share an environment cannot by itself be attributed to peers, which motivates designs where the environment is assigned or the mechanism is modeled explicitly.

---

## 6. VanderWeele 2011 — Sensitivity analysis for contagion effects in social networks

**Citation.** VanderWeele, Tyler J. 2011. "Sensitivity Analysis for Contagion Effects in Social Networks." *Sociological Methods & Research* 40 (2): 240–255. DOI: 10.1177/0049124111404821.

**PAGE-NUMBER WARNING.** The library PDF is the **NIH Public Access author manuscript** (PMC, "available in PMC 2015 January 09"), with manuscript pages "Page 1" … ; journal pages 240–255 **could not be determined** from this file. Cites below are "MS p." (= PDF page). Typos in the manuscript (e.g. "Folwer", "have increase likelihood") are reproduced as printed.

**Data / setting / sample / years.** No new data. Re-analyzes published estimates: Christakis & Fowler on obesity (2007) and smoking (2008), Fowler & Christakis on happiness (2008), Cacioppo, Fowler & Christakis on loneliness (2009), all Framingham; and Cohen-Cole & Fletcher's (2008, *BMJ*) placebo estimates for headaches, acne, and height (Add Health).

**Design.** Methodological: sensitivity analysis (bias-factor formulas) for an unmeasured binary factor U that drives tie formation (latent homophily) or is a shared environment. Asks how strong U must be to "explain away" each published estimate.

**Main findings (verbatim).**

> "Sensitivity analyses suggest that contagion effects for obesity and smoking cessation are reasonably robust to possible latent homophily or environmental confounding; those for happiness and loneliness are somewhat less so. Supposed effects for height, acne and head-aches are all easily explained away by latent homophily and confounding." (Abstract, MS p. 1)

> "For example, to completely explain away the estimate of 57% the unmeasured factor U would have to have increase likelihood of obesity by 3-fold and have a prevalence of 0.7 in friendships in which the alter was obese and only 0.25 in friendships in which the alter was not obese. Although the latent factor U would have to be very strongly related to current obesity [...], the latent U, as can also be seen in Table 1, would need to only be modestly related to obesity to bring down the confidence interval so as to include 0%." (MS p. 6)

> "It should be noted that an estimate that can easily be explained away by an unmeasured factor does not mean that there is no social influence but only that one probably ought not draw that conclusion from the data at hand." (MS p. 10)

Worked example: a U with 1.8-fold effect and prevalence 0.7 vs. 0.3 "would reduce the estimate of the effect of the alter's obesity on the ego's obesity from an increase of 57% (95% CI: 6% to 123%) to an increase of 25% (95 CI: −16% to 77%)." (MS p. 6; "95 CI" as printed)

**Sorting vs. influence.** Accepts Shalizi & Thomas's point that latent homophily biases the Christakis–Fowler estimates even after lagged controls (MS p. 6), and replaces the yes/no identification question with a "how much confounding would it take" question. Notes the same U can represent "a shared environmental factor for the ego and the alter" (MS p. 6). Strongest-surviving estimates: mutual friend for obesity (171%) and spouse for smoking cessation (MS p. 7).

**Limitations (author's own).**

> "Perhaps most importantly, in attempting to reason about whether latent homophily might explain away a contagion effect estimate we have had to make decisions regarding whether homophily of a particular magnitude is or is not plausible. Without studies providing precise measures of such homophily it is difficult to know what levels might be sufficiently large to be considered implausible." (MS p. 9) **[imperfect measure]**

> "Another limitation of the sensitivity analyses here were the assumptions that the latent factor U was binary and that its effects on the ego's being obese were the same irrespective of whether or not the alter was obese [...]. Such assumptions are likely unrealistic." (MS p. 9) **[model not fit to data]**

- Inherits the Framingham data and estimates. **[single system]** **[outcome is not selection]**

**Channel / source (assistant judgment).** Method-level, development channel; source: peers vs. shared environment (U can be either). Useful framing for the dissertation: when design cannot separate sorting from influence, report how strong unobserved sorting would need to be.

---

## 7. McPherson, Smith-Lovin & Cook 2001 — Birds of a feather: homophily in social networks

**Citation.** McPherson, Miller, Lynn Smith-Lovin, and James M. Cook. 2001. "Birds of a Feather: Homophily in Social Networks." *Annual Review of Sociology* 27: 415–444. JSTOR stable URL: http://www.jstor.org/stable/2678628. (PDF is a JSTOR scan with a cover sheet: PDF p. n = printed p. 413 + n.)

**BIB ERROR — check before citing.** The bib entry `mcpherson_birds_2001` has `doi = {10.3982/ECTA7195}`, which is an *Econometrica* DOI prefix and is not this article. The PDF itself shows no DOI. The commonly cited DOI for this article is 10.1146/annurev.soc.27.1.415, but that is **not verified from the PDF**; confirm before use. The bib also has `number = {2001}` and a garbled title field (it contains JSTOR boilerplate).

**Text-layer note.** The JSTOR text layer renders em-dashes as hyphens (e.g. "This principle-the homophily principle-structures"). Quotes below reproduce the text layer and mark these with "[—]" where a dash is clearly meant.

**Data / setting / sample / years.** Literature review (Annual Review). No new data; reviews roughly a century of studies (from 1920s group-formation studies through the late 1990s) on marriage, friendship, work, advice, support, discussion networks, and voluntary associations.

**Design.** Review / synthesis.

**Main findings (verbatim).**

> "Similarity breeds connection. This principle[—]the homophily principle[—]structures network ties of every type, including marriage, friendship, work, advice, support, information transfer, exchange, comembership, and other types of relationship. [...] Homophily in race and ethnicity creates the strongest divides in our personal environments, with age, religion, education, occupation, and gender following in roughly that order. Geographic propinquity, families, organizations, and isomorphic positions in social systems all create contexts in which homophilous relations form." (Abstract, p. 415)

> "We review all of these variants in the work below, attempting to distinguish between homophily effects that are created by the demography of the potential tie pool as baseline homophily and homophily measured as explicitly over and above the opportunity set as inbreeding homophily." (p. 419; footnote marker "5" omitted)

> "The social homogeneity of most organizational foci creates a strong baseline homophily in networks that are formed there. Feld (1982) found that organizational foci produced ties that were twice as homogeneous as would be expected by chance." (p. 433)

On selection vs. influence for behaviors and values:

> "Longitudinal data first became available in the 1970s, and this led to a rather decisive shift in the interpretation of behavioral homophily. Cohen (1977) and Kandel (1978) demonstrated that both positive behaviors of school achievement and negative behaviors like smoking marijuana were homophilous more because of selection into relationships with similar others than because of behavioral influence within friendship cliques." (p. 428)

> "At any rate, selection almost certainly trumps influence or attrition in this domain as well." (p. 429, on value/attitude homophily)

**Sorting vs. influence.** Central contribution is to decompose sorting itself: baseline homophily (driven by who is in the opportunity pool, e.g. the organization's composition) vs. inbreeding homophily (preference over and above the pool). Organizations ("foci": school, work, voluntary groups) create much of the baseline: "School, work, and voluntary organizational foci provide the great majority of ties that are not kin" (p. 431). Reports that, where longitudinal evidence exists, selection outweighs influence for behaviors and attitudes (pp. 428–429).

**Limitations (authors' own).**

> "Still, cross-sectional data on networks can never answer the important questions about the extent to which network patterns, including homophily, are created by selective tie formation or selective tie dissolution. While we have evidence that both processes are important, we have little comprehensive information of how the two processes interrelated or about their relative strength of the two processes are highly tentative." (pp. 437–438; grammar as printed) **[imperfect measure]**

> "Analyses of cross-sectional data often leave such long-term effects of organizational environments misclassified as individual choice or (more appropriately) as unexplained variance, when in fact they are the systematic residues of past foci." (p. 438)

- Review of mostly cross-sectional studies; no unifying model. **[no model of mechanism]** **[model not fit to data]** **[outcome is not selection]** (ties, not competitive outcomes; though the review touches job-search and workplace networks, e.g. pp. 421–422).

**Channel / source (assistant judgment).** Bears on the sorting step that precedes all three channels; strongest link is to source = organization (foci set the opportunity pool, hence baseline homophily). The p. 438 quote is directly usable for the dissertation argument that organizational environment gets misread as individual choice.

---

## 8. Kossinets & Watts 2009 — Origins of homophily in an evolving social network

**Citation.** Kossinets, Gueorgi, and Duncan J. Watts. 2009. "Origins of Homophily in an Evolving Social Network." *American Journal of Sociology* 115 (2): 405–450. DOI: 10.1086/599247. (PDF p. n = printed p. 404 + n.)

**Data / setting / sample / years.** "[T]he population of 30,396 undergraduate and graduate students, faculty, and staff in a large U.S. university, who used their university e-mail accounts to both send and receive messages during one academic year." (p. 410). Merged (1) e-mail logs, (2) individual attributes (status, gender, age, department, years in community), (3) course registration / affiliations by semester (p. 410). Network built from 7,156,162 single-recipient messages (p. 411). Year of data not stated in the excerpts I read; the paper describes it only as "one academic year".

**Design.** Observational, longitudinal (daily network snapshots). Estimates probabilities of tie formation, of entering a shared focus (class / implicit group), and of tie dissolution as functions of pairwise similarity, conditional on network distance and shared foci.

**Main findings (verbatim).**

> "The analysis indicates that highly similar pairs do show greater than average propensity to form new ties; however, it also finds that tie formation is heavily biased by triadic closure and focal closure, which effectively constrain the opportunities among which individuals may select. [...] The authors conclude that the dynamic interplay of choice homophily and induced homophily, compounded over many "generations" of biased selection of similar individuals to structurally proximate positions, can amplify even a modest preference for similar others, via a cumulative advantage–like process, to produce striking patterns of observed homophily." (Abstract, p. 405)

> "In terms of our contrast between choice and induced homophily, therefore, we conclude that homophily observed in our population cannot be unequivocally attributed to either stylized mechanism but appears to depend on both in significant ways. [...] As we observe, however, the vast majority of new ties form between individuals who already share a friend or a group, and once these conditions are met, similarity loses much, and in some cases all, of its effect." (p. 436)

> "Shared social foci, in other words, not only increase the likelihood of tie formation, but also decrease the rate of dissolution [...]. In both cases, moreover, the impact of sharing a focus eliminates the impact of similarity." (p. 434)

Definitions used (from McPherson & Smith-Lovin 1987): "Formally, induced homophily is the level of homophily expected from random mixing within groups given group assignments, and choice homophily is the level of homophily in excess of induced homophily" (p. 407, fn. 3).

**Sorting vs. influence.** Explicitly sets influence aside: "A third possibility is that individuals who are acquainted will become more similar over time via a process of social influence. However, the attributes we consider here are either not malleable (e.g., gender and age) or else do not change appreciably on the time scale of interest (e.g., academic major); thus, although social influence is no doubt important in many contexts, we do not consider it here." (p. 407, fn. 2). Splits sorting into individual choice vs. structure (organization/foci), and notes that structure is itself partly chosen: "structural constraints that may initially appear exogenous are in fact generated endogenously and act effectively as proxies for unobserved individual preferences." (p. 435). Workplace example of purely induced homophily: "If, for example, high school teachers are disproportionately female, and investment bankers are disproportionately male, then the resulting pattern of interactions in their workplaces will generally exhibit gender homophily, even if individuals in both professions select among their available work colleagues without regard to gender." (p. 407)

**Limitations (authors' own).**

> "As we have already indicated, our data clearly lack some attributes, like race and socioeconomic status, that might be more salient with respect to the choice of interaction partners than the available variables. Moreover, the university community in question may be relatively homogeneous on some dimensions, particularly educational background, in comparison to other kinds of communities." (p. 438) **[imperfect measure] [single system]**

> "A business firm, for example, attempting to coordinate the activity of many departments to achieve a single, coherent goal, may display quite different patterns of interactions than a university community." (p. 439)

- The amplification claim is speculative and untested: "we speculate that even a relatively weak preference for homophilous relationships will tend to be amplified over time" and "A thorough answer to this question would require the use of simulation models [...]. Although such an extensive simulation exercise is beyond the scope of this article, it is certainly conceivable" (pp. 436–437). **[no model of mechanism] [model not fit to data]**
- One academic year of e-mail as a proxy for social ties. **[imperfect measure]** Outcome is tie formation. **[outcome is not selection]**

**Channel / source (assistant judgment).** Upstream of all three channels: how the peer set is assembled. Source: organization (classes / foci create the opportunity set) interacting with peer choice. Directly supports the dissertation claim that the organization shapes who one's peers are, so peer and organization sources are not independent.

---

## 9. Centola 2010 — The spread of behavior in an online social network experiment

**Citation.** Centola, Damon. 2010. "The Spread of Behavior in an Online Social Network Experiment." *Science* 329 (5996): 1194–1197. DOI: 10.1126/science.1185231. (PDF p. 1 = printed p. 1194, which it shares with the end of the preceding article; PDF p. n = printed p. 1193 + n for pp. 1–4.)

**Data / setting / sample / years.** "an Internet-based health community, containing 1528 participants recruited from health-interest World Wide Web sites" (p. 1194). Six independent trials, each a matched pair of networks (clustered lattice vs. random rewiring), so 12 diffusion processes (p. 1195). Network sizes "(i) N = 98, Z = 6; (ii) N = 128, Z = 6; and (iii) N = 144, Z = 8" where Z = number of "health buddies"; each trial ran "3 weeks (~1.8 million seconds)" (p. 1196). Behavior: registering for an online health forum. Year: published 2010 (received 22 March 2010 per the page header shown at p. 1194 belongs to the preceding article; experiment dates not stated in the main text).

**Design.** Randomized experiment: participants randomly assigned to network position and condition; network topology fixed by the experimenter.

**Main findings (verbatim).**

> "Individual adoption was much more likely when participants received social reinforcement from multiple neighbors in the social network. The behavior spread farther and faster across clustered-lattice networks than across corresponding random networks." (Abstract, p. 1194)

> "On average, the behavior reached 53.77% of the clustered networks, whereas only 38.26% of the population adopted in the random networks (13)." (p. 1196)

> "Participants were significantly more likely to adopt after receiving a second signal than after receiving only one signal (P < 0.001 using the Cox proportional hazards model)." (p. 1196)

**Sorting vs. influence.** Removes sorting by design: "(i) The present study isolates the effects of network topology, independent of frequently co-occurring factors such as homophily (3, 16), geographic proximity (17), and interpersonal affect (4, 18), which are easily conflated with the effects of topological structure in observational studies" and "(iii) This study eliminates the possibility for social ties to change and thereby identifies the effects of network structure on the dynamics of diffusion without the confounding effects of homophilous tie formation (1, 20)." (p. 1195)

**Limitations (author's own).**

> "As with all experiments, design choices that aided my control of the study also put constraints on the behaviors that I could test. A key limitation of my design is that, unlike in my experiment, adopting a new health behavior is often extremely difficult in the real world." (p. 1196)

> "The modest range of population sizes tested and the correspondingly narrow range of degrees were due to the challenges of recruiting large numbers of people simultaneously." (p. 1196) **[small data]**

> "An important assumption of this study is that the effects of network topology will not be overwhelmed by individuals' exposure to other social factors." (p. 1197)

- Anonymous, no direct communication between buddies (p. 1197); artificial online setting. **[single system]** Low-cost behavior; outcome is adoption. **[outcome is not selection]**

**Channel / source (assistant judgment).** Development (adoption of a behavior) via peers; the structure of the peer network (clustering, redundancy), not just peer attributes, changes outcomes. Organization acts only as the experimenter who sets the network, which is a useful analogy: the organization that designs the network can shift outcomes.

---

## 10. Centola 2011 — An experimental study of homophily in the adoption of health behavior

**Citation.** Centola, Damon. 2011. "An Experimental Study of Homophily in the Adoption of Health Behavior." *Science* 334 (6060): 1269–1272. DOI: 10.1126/science.1207055. (PDF p. n = printed p. 1268 + n; p. 1269 is shared with the end of the preceding article and p. 1272 with the start of the following one.)

**Data / setting / sample / years.** "a World Wide Web social networking environment composed of 710 participants, all of whom were recruited from an online fitness program" (p. 1269). Five trials, each a pair of networks (homophilous vs. unstructured), i.e. 10 networks; "All networks in the study had the same size (N = 72), neighborhood structure (hexagonal lattice network, clustering coefficient = 0.4), and degree distribution (Z = 6)"; "All five trials of the study ran concurrently for 7 weeks." (p. 1270). Behavior: adopting an Internet-based diet diary. Homophily defined on gender, age, and BMI (p. 1270). Calendar dates of the experiment not given in the main text.

**Design.** Randomized experiment. Topology held fixed; only the sorting of participants (homophilous vs. random placement on the same lattice) varied.

**Main findings (verbatim).**

> "Despite the importance of this thesis, confounding factors in observational data have made it difficult to test empirically. We report results from a controlled experimental study on the spread of a health innovation through fixed social networks in which the level of homophily was independently varied. We found that homophily significantly increased overall adoption of a new health behavior, especially among those most in need of it." (Abstract, p. 1269)

> "At the end of week 7, the total number of adopters across all homophilous networks was more than 3 times the total number of adopters in the unstructured networks." (p. 1270)

> "Our findings suggest that obese individuals may be more dependent than healthier individuals on the composition of their social networks for making decisions about adopting health behaviors. This indicates that low adoption levels of health innovations among less healthy individuals (7, 8, 16, 20) may be a function of social environment rather than a baseline reluctance for adoption (25, 26)." (p. 1271)

**Sorting vs. influence.** Turns homophily from a confound into the treatment. The design separates "who your neighbors are" (sorting, set by the experimenter) from network topology and from individual traits: "Are obese individuals simply less likely to adopt a health behavior, or is it their social environment that reduces their likelihood of adoption (25, 26)? Addressing these difficulties requires the ability to independently control the degree of homophily in a social network while simultaneously holding the topology of the network, and the distribution of individual- and population-level parameters, constant." (p. 1269)

**Limitations.**

> "Our experimental design did not permit causal identification at the individual level; however, dyadic-level analyses of the correlations between homophilous ties and the likelihood of behavior spread indicate that partial overlap on traits between neighbors may be sufficient to significantly increase the likelihood of transmission (28) (fig. S11). Although these correlations do not imply causal effects of specific traits, they do suggest that a minimal level of overlapping characteristics between social contacts may improve the spread of behaviors through social networks" (p. 1271) **[no model of mechanism]** (the paper fits a simple threshold-style model in the supplement, Fig. 3 / eq. S1, p. 1271)

- Low counts: "Despite low overall levels of adoption" (p. 1270); 10 networks of 72. **[small data]**
- Online, anonymous, single platform; low-cost behavior. **[single system]** **[outcome is not selection]**

**Channel / source (assistant judgment).** Development via peers, but the lever is the *composition* of the peer environment, which an organization can set. The cleanest experimental evidence in this cluster that the same individual behaves differently depending on who they are placed among, i.e. the environment, not only the individual, predicts the outcome.

---

## 11. Eckles, Kizilcec & Bakshy 2016 — Estimating peer effects in networks with peer encouragement designs

**Citation.** Eckles, Dean, René F. Kizilcec, and Eytan Bakshy. 2016. "Estimating Peer Effects in Networks with Peer Encouragement Designs." *Proceedings of the National Academy of Sciences* 113 (27): 7316–7322. DOI: 10.1073/pnas.1511201113. (PDF p. n = printed p. 7315 + n.)

**Data / setting / sample / years.** Facebook field experiment. "The peer encouragement design ran for 3 wk between September and October 2012. The egos in the data analyzed are 48.9 million Facebook users globally [...]. Approximately 905 million Facebook users were peers of the egos and used the web interface." (p. 7321)

**Design.** Randomized field experiment, analyzed with instrumental variables (IV). Peers (not the focal person) are randomly encouraged, via small interface changes, to give feedback on the focal person's posts; the encouragement is the instrument for feedback received. Key identifying assumption is an exclusion restriction (the encouragement affects the ego only through peer behavior) (pp. 7317–7318).

**Main findings (verbatim).**

> "Because peer effects are often confounded with homophily and common external causes, recent work has used randomized experiments to estimate effects of specific peer behaviors. [...] We find evidence for substantial effects of receiving marginal feedback on multiple behaviors, including giving feedback to others and continued posting. [...] In comparison, observational estimates differ substantially, both underestimating and overestimating effects, suggesting that researchers and policy makers should be cautious in relying on them." (Abstract, p. 7316)

> "Receiving 10% more feedback causes egos to give others 1.1% more likes and 1.1% more comments." (p. 7319); "A 10% increase in feedback causes a 0.7% increase in creating new posts." (p. 7320)

> "For the main outcomes of interest (posting and feedback to others), the observational coefficient estimates are 317–498% larger. On the other hand, they appear to underestimate reply behaviors by 36% and 68% for comments and likes, respectively. That is, in contrast to claims that observational estimates can upper bound true peer effects (6), the sign of the implied large-sample bias of the observational estimators varies across outcomes." (p. 7320)

**Sorting vs. influence.** Names the confounds: "There are many causes of correlated behaviors in networks that make it difficult to identify peer effects, including selective tie formation [i.e., homophily (7)], unobserved correlated external causes, and prior peer effects (4, 8, 9)." (p. 7316). Randomizing peers' behavior removes both sorting and shared environment from the estimate. The p. 7320 result directly qualifies Aral et al. (paper 4): reference (6) is the "upper bound" claim, and the bias of observational estimates is shown to go in either direction. (Cross-reference is assistant reading; the PDF's ref. 6 should be checked if this is cited.)

**Limitations (authors' own).**

> "One limitation of this experiment is that it does not elucidate the mechanisms by which receiving feedback affects egos or distinguish different types of feedback." (p. 7321) **[no model of mechanism]**

> "The plausibility of a key assumption in our model, the exclusion restriction, partly depends on encouragements being minimal. However, encouragements that produce minimal variation can result in imprecise IV estimates; even studies with hundreds of thousands of observations will often suffer from the instruments being too weak (63)." (p. 7321)

- Estimand is encouragement-specific (effect for egos whose peers respond to the nudge) (p. 7321). One platform, one behavior. **[single system]** **[outcome is not selection]**

**Channel / source (assistant judgment).** Evaluation-adjacent: peers' feedback is a (social) evaluation of a person's output, and receiving more of it changes subsequent production. Source: peers, with the organization (platform) controlling the interface that shapes how much peer evaluation occurs. Methodologically the template for "randomize the peer, not the person."

---

## 12. Rajkumar, Saint-Jacques, Bojinov, Brynjolfsson & Aral 2022 — A causal test of the strength of weak ties

**Citation.** Rajkumar, Karthik, Guillaume Saint-Jacques, Iavor Bojinov, Erik Brynjolfsson, and Sinan Aral. 2022. "A Causal Test of the Strength of Weak Ties." *Science* 377 (6612): 1304–1310. DOI: 10.1126/science.abl4476.

**Page-number note.** The PDF footers read "Rajkumar et al., Science 377, 1304–1310 (2022) … n of 7"; individual journal page numbers are not printed. Cites below give "p. 1303 + n (n of 7)", which assumes the 7 article pages map in order onto 1304–1310 (assistant inference from the footer; consistent with the 7-page range).

**Data / setting / sample / years.** LinkedIn "People You May Know" (PYMK) recommendation experiments, retrospectively analyzed. "We performed a retrospective analysis of the randomization created by the PYMK experiments conducted by LinkedIn between 2015 and 2019 in two waves. The first wave examined a global experiment conducted in 2015 that had over 4 million experimental subjects and created over 19 million new connections. [...] The second wave spanned every continent and US state, had more than 16 million experimental subjects, created ~2 billion new connections and recorded more than 70 million job applications that led to 600,000 new jobs during the experimental period" (p. 1304, 1 of 7). Outcome "job transmission" = A works at company c, B later works at c at least one year later, and A and B were connected at least one year before B's move (p. 1304, 1 of 7). Tie strength = number of mutual connections, and interaction intensity (messaging).

**Design.** Randomized experiments (A/B tests of a tie-recommendation algorithm) analyzed as intent-to-treat with instrumental variables, compared against ordinary least squares (OLS) on the same data.

**Main findings (verbatim).**

> "The experiments randomly varied the prevalence of weak ties in the networks of over 20 million people over a 5-year period, during which 2 billion new ties and 600,000 new jobs were created. The results provided experimental causal evidence supporting the strength of weak ties and suggested three revisions to the theory. First, the strength of weak ties was nonlinear. Statistical analysis found an inverted U-shaped relationship between tie strength and job transmission such that weaker ties increased job transmission but only to a point, after which there were diminishing marginal returns to tie weakness. [...] Third, the strength of weak ties varied by industry. Whereas weak ties increased job mobility in more digital industries, strong ties increased job mobility in less digital industries." (Abstract, p. 1304, 1 of 7)

> "Although the OLS analysis replicated previous findings of an apparent paradox of weak ties in which strong ties were more strongly correlated with job transmissions, the experimental IV analysis reversed this result and suggested a nonlinear relationship between tie strength and job transmission in which medium strength ties were the most effective in generating job mobility." (p. 1307, 4 of 7)

**Sorting vs. influence.** States the endogeneity problem in labor-market terms: "network ties and labor market outcomes are endogenous, making the causal link between weak ties and job placement elusive. Individuals' labor market outcomes are likely to be determined by and to simultaneously determine their social networks. The evolution of social networks and job trajectories are also likely correlated with unobserved factors such as effort, ability, and sociability, which confound empirical identification of the link between weak ties and jobs." (p. 1304, 1 of 7). Randomizing which ties are recommended breaks this. The OLS-vs-IV reversal on the same data is a concrete demonstration that sorting can flip the sign of an observational network conclusion.

**Limitations (authors' own).**

> "First, although PYMK experiments provided a robust channel through which to introduce experimental variation into the evolution of human social networks, we could not compel LinkedIn users to take these recommendations. Therefore a degree of self selection exists in who acted on the connection recommendations." (p. 1309, 6 of 7)

> "Second, LinkedIn is a professional social network and may be different than other online social networks such as Facebook or offline social relationships such as those originally studied by Granovetter." (p. 1309, 6 of 7) **[single system]**

> "As the statistical power of the node-level analysis was not sufficient to confirm individual differences between the effects of strong, medium, and weak ties in our experiments, we also analyzed these relationships at the more granular edge level." (p. 1307, 4 of 7)

- Job transmission is inferred from self-reported LinkedIn employment histories. **[imperfect measure]** Does not model why a tie helps (information vs. referral vs. advocacy). **[no model of mechanism]**
- Outcome is job mobility, which is closer to selection than any other paper here, but it is a move between employers, not the outcome of a competition among candidates for a fixed slot; competitors and the employer's decision are not observed. **[outcome is not selection]** (partial; assistant judgment)

**Channel / source (assistant judgment).** Selection-adjacent (access to job opportunities through peers). Source: peers, with the platform (organization) as the party that sets tie formation. Strongest bridge in this cluster from network structure to a labor-market allocation outcome.

---

## 13. Gee, Jones & Burke 2017 — Social networks and labor markets: how strong ties relate to job finding on Facebook's social network

**Citation.** Gee, Laura K., Jason Jones, and Moira Burke. 2017. "Social Networks and Labor Markets: How Strong Ties Relate to Job Finding on Facebook's Social Network." *Journal of Labor Economics* 35 (2): 485–518. DOI: 10.1086/686225. (PDF p. n = printed p. 484 + n.)

**Data / setting / sample / years.** De-identified US Facebook data. Restrictions: US users aged 16–64 who list employer and education and have been on Facebook at least a year; "These restrictions leave 6 million individuals, or about 4% of the US Facebook population. When we connect these 6 million individuals back to their friends, we have a total of 260 million dyads. Of these 6 million people, about 400,000 sequentially work with a pre-existing social tie" (p. 490). Regressions use a random subsample of 1 million dyads (p. 501, fn. 21). Timing: Facebook friendship "is only observable from 2007 onward"; "mean start date (November 2010)" of users' jobs (p. 494; figure caption and footnote text). Tie strength = share of contact (tags, posts, etc.) in the prior year, and number of mutual friends.

**Design.** Observational. Dyad-level regressions with user fixed effects and dyad controls, plus a placebo test that reverses who joined the employer first to bound the causal portion (pp. 501–503, 509).

**Main findings (verbatim).**

> "Using 6 million Facebook users' data, we find evidence for the opposite. We proxy for job help by identifying people who eventually work with a preexisting friend. Using objective tie strength measures and our job help proxy, we find that most people are helped through one of their numerous weak ties but a single stronger tie is significantly more valuable at the margin." (Abstract, p. 485; "preexisting" is hyphenated across a line break in the PDF)

> "For example, increasing the amount of contact with a friend by 10 percentage points increases the likelihood that one will eventually work with that friend by at least 20%." (p. 487)

> "In short, a person is most likely to eventually work with a weak tie because weak ties collectively make up most of a person's social network. However, strengthening an existing tie should increase the probability that one will work with that specific friend." (p. 513)

Framing directly relevant to selection among competitors:

> "If social ties of differing strength benefit more, then this may result in the allocation of a job away from one person and toward another who has the right type of connection (weak or strong) but who is not necessarily a better worker." (p. 486)

**Sorting vs. influence.** Names homophily as a dyad-level confound: "Dyads with higher tie strength may be more likely to be similar (homophily), and so these dyads may be more likely to work at the same employers, even in the absence of actual help through their social networks. Ideally, we would use a dyad fixed effect to control for this source of omitted variable bias, but we only observe each dyad a single time." (pp. 501–502) Takes the network as given: "The network itself is endogenously determined, and the level of tie strength between each dyad is also endogenous. We are most interested in the question of how tie strength affects sequential jobs, so we take the network as given. Our empirical strategy aims to address the second type of endogeneity" (p. 498; footnote marker "18" omitted). User fixed effects absorb individual traits; the placebo reversal is used to bound remaining dyad-level confounding.

**Limitations (authors' own).**

> "We would like to emphasize that these results may not be the true causal effects of tie strength on the likelihood of a sequential job. The principal concern is that tie strength Tik is endogenous, E[Tikeik] ≠ 0." (p. 502) (This is the sentence Rajkumar et al. 2022 quote as motivation; paper 12.)

> "To find the causal impact of tie strength on the likelihood of a sequential job from that friend, one would ideally observe an experiment that randomly assigns first networks and then tie strength. We have found no such experiment" (p. 498)

> "Our sequential job definition is very conservative and cannot measure job help from non-Facebook friends. Additionally Facebook is not primarily a professional social networking website, so we are likely missing many purely professional connections; thus, we think of our 7% rate as a lower bound on the amount of job help in this population." (pp. 492–493) **[imperfect measure]**

- "Facebook users are not a randomly selected sample of the US population." (p. 490) **[single system]**
- Job help is a proxy (later co-employment), validated by a permutation test and a small survey ("matching the survey-provided friends' names was possible for 63 respondents, or 7,497 dyads", p. 493). **[imperfect measure]** **[no model of mechanism]**
- The outcome is ending up at a friend's employer, not winning a contested slot against identified rivals; the employer's decision is unobserved. **[outcome is not selection]** (partial; assistant judgment)

**Channel / source (assistant judgment).** Selection (job allocation) via peers; the p. 486 sentence explicitly states the selection-channel worry that network position, not productivity, can decide who gets the job. Evidence is observational and the competing applicants are not observed.

---
