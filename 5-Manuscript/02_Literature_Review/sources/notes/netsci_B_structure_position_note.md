# Network science background, cluster B: structure, position, groups, hierarchy — source note

Prepared 2026-10-28 for the dissertation introduction. Extracts only; not dissertation prose.

**Conventions**

- Quotes are verbatim from the PDF text layer (or from tesseract OCR where the PDF is an image scan; flagged per paper). Each quote was string-checked against the extracted text before inclusion. Line-break hyphens are silently rejoined; ellipses `…` mark my omissions; `[sic]` is not used — OCR glitches in the source were avoided by choosing clean passages.
- "p." = printed journal page. "PDF p." = page of the PDF file, given when different.
- Limitation tags: [small data], [imperfect measure], [single system], [no model of mechanism], [model not fit to data], [outcome is not selection].
- "Channel / source" lines are **my judgment** (assistant), not the authors' framing. Channels: development / evaluation / selection. Sources: peers / organization.

---

## Assistant synthesis (to be filled after all papers are read)

---

## 1. Feld 1991 — Why your friends have more friends than you do

**Citation.** Feld, Scott L. 1991. "Why Your Friends Have More Friends Than You Do." *American Journal of Sociology* 96(6): 1464–1477. DOI 10.1086/229693.

**PDF note.** JSTOR scan with an OCR text layer (some OCR errors in the layer; quotes below were chosen from clean passages and checked). PDF p. = journal p. − 1463 (PDF p. 1 = p. 1464).

**Data / setting.** Mutual friendship nominations from Coleman's *The Adolescent Society* (1961), 12 high schools; worked example on "Marketville" girls (146 girls with any mutual friend). Plus mathematical derivation.

**Design.** Mathematical argument (a property of degree distributions) illustrated with observational sociometric data.

**Main findings.**

- The friendship paradox is a mathematical consequence of degree heterogeneity: "the mean number of friends of friends is always greater than the mean number of friends of individuals" (abstract, p. 1464; repeated p. 1465).
- Mechanism in one sentence: "those with 40 friends show up in each of 40 individual friendship networks and thus can make 40 people feel relatively deprived, while those with only one friend show up in only one friendship network and can make only that one person feel relatively advantaged" (p. 1465; PDF p. 2).
- Empirical illustration: "Of the 146 girls who have any mutual friends, 80 have fewer friends than the mean among their friends while 41 have more; 25 have the same as the mean among their friends." (p. 1466; PDF p. 3). In the Marketville girls, "74% of the individuals would find themselves to be relatively deprived" if comparing to friends' mean (p. 1469; PDF p. 6).
- Formal result (paraphrase; the OCR of the equation is garbled): mean friends-of-friends = mean(x) + variance(x)/mean(x); verbatim gloss: "the mean among friends increases with the variance among individuals, with a given mean among individuals" (p. 1470; PDF p. 7).
- Framing as an evaluation problem: "Friendship is not only a source of satisfaction and security; it is also a way that individuals evaluate themselves and others." (p. 1464). Conclusion: "Individuals who find themselves associated with people with more friends than they have may conclude that they themselves are below average and somehow inadequate." (p. 1476; PDF p. 13).
- Organizational foci (footnote 8): "if friendships are primarily established through one focus or a few foci of activity (Feld 1981), then individuals might have numbers of friends similar to the numbers their own friends have" … "and the experience of relative deprivation may be minimized" (p. 1474; PDF p. 11).

**Model?** Yes — an analytic identity; it is illustrated with Coleman's data, not fit/estimated.

**Limitations.**

- Author's own: "There has been little study of how people determine what is an adequate number of friends" (p. 1464) — the comparison behaviour itself is assumed ("it is reasonable to suppose"), not measured. [imperfect measure] [no model of mechanism] (for the psychological comparison step).
- Illustration drawn from one 1961 dataset, mainly one school. [single system] [small data]
- Outcome is perceived relative deprivation, not any allocation. [outcome is not selection]

**Channel / source (my judgment).** Evaluation (self- and other-evaluation via local reference groups), source = peers; footnote 8 links the size/structure of organizational foci (organization) to the bias. Relevant to selection as a caution: local comparison sets are systematically biased upward by the degree distribution. No competition for slots; no non-monotonic effect.

---

## 2. Newman 2002 — Assortative mixing in networks

**Citation.** Newman, M. E. J. 2002. "Assortative Mixing in Networks." *Physical Review Letters* 89(20): 208701. DOI 10.1103/PhysRevLett.89.208701.

**PDF note.** The file in the library is the **arXiv preprint** (cond-mat/0205405v1, 20 May 2002), 4 pp. + references, not the published PRL version. Printed PRL page numbers (208701-1 … -4) are **not available** from this file; locations below are preprint PDF pages. Wording may differ slightly from the published version — spot-check against PRL before quoting in the dissertation.

**Data / setting.** Ten real networks in Table I (preprint PDF p. 2): five social (physics coauthorship n = 52,909, r = 0.363; biology coauthorship n = 1,520,251, r = 0.127; mathematics coauthorship n = 253,339, r = 0.120; film actor collaborations n = 449,913, r = 0.208; company directors n = 7,673, r = 0.276) and five technological/biological (Internet r = −0.189; WWW r = −0.065; protein interactions r = −0.156; neural network r = −0.163; food web r = −0.276). Note all five "social" networks are collaboration/affiliation projections (co-membership in papers, films, boards).

**Design.** Method (new scalar measure r) + cross-network observational comparison + exactly solvable random-graph model + Monte Carlo simulation.

**Main findings.**

- Definition: "A network is said to show assortative mixing if the nodes in the network that have many connections tend to be connected to other nodes with many connections." (abstract, PDF p. 1). The measure r "is simply the Pearson correlation coefficient of the degrees at either ends of an edge" (PDF p. 1).
- Finding: "of the social networks studied (the top five entries in the table) all have significant assortative mixing, which accords with accepted wisdom within the sociological community" (PDF p. 2).
- Model result: "Within this model we find that assortative networks percolate more easily and that they are also more robust to removal of their highest degree vertices" (PDF p. 4).
- On growth models: Barabási–Albert gives r → 0; "Since these networks show significant disassortative mixing however (Table I), it is clear that the model is incomplete. It is an interesting open question what type of network evolution processes could explain the values of r observed in real-world networks." (PDF p. 2).

**Model?** Yes — an ensemble random-graph model with specified joint degree distribution e_jk, solved by generating functions and checked against simulation (N = 100,000). The model is **not fit** to the Table I networks; it is used to explore consequences (percolation, resilience) of mixing.

**Limitations.**

- Author's own: the mechanism producing r in real networks is an "open question" (PDF p. 2). [no model of mechanism]
- Degree-degree correlation only; a coarse summary of structure. [imperfect measure]
- Model explores consequences, not fit. [model not fit to data]
- [outcome is not selection]

**Channel / source (my judgment).** Structural background, not a channel per se. Relevant because the "social" networks with positive r are all group-affiliation projections (collaborations, boards) — i.e., co-membership in organizations tends to connect well-connected people to each other; links to rich-club / core-periphery and to who sits near high-status peers (peers, organization). No competition or non-monotonicity.

---

## 3. Barabási & Albert 1999 — Emergence of scaling in random networks

**Citation.** Barabási, Albert-László, and Réka Albert. 1999. "Emergence of Scaling in Random Networks." *Science* 286(5439): 509–512. DOI 10.1126/science.286.5439.509.

**PDF note.** The library file is the **arXiv preprint** (cond-mat/9910332v1, 21 Oct 1999; 11 pp. double-spaced), not the Science typeset version. Printed Science page numbers are **not available** from this file; locations are preprint PDF pages. Spot-check wording against Science before quoting.

**Data / setting.** Degree distributions of: actor collaboration graph (N = 212,250, ⟨k⟩ = 28.78, γ_actor = 2.3), WWW (N = 325,729, γ_www = 2.1), power grid (N = 4,941, γ ≈ 4) (Fig. 1 caption, PDF p. 10); citation network γ_cite = 3 (text, PDF p. 3).

**Design.** Observational (empirical degree distributions) + generative model (growth + linear preferential attachment), analytic mean-field solution + simulation; two ablated variants (growth only; preferential attachment without growth).

**Main findings.**

- Mechanism: the power law "is found to be a consequence of the two generic mechanisms that networks expand continuously by the addition of new vertices, and new vertices attach preferentially to already well connected sites" (abstract, PDF p. 1).
- Social illustration of preferential attachment: "For example, a new actor is cast most likely in a supporting role, with more established, well known actors." (PDF p. 5).
- Cumulative advantage by seniority: "Thus older (smaller ti ) vertices increase their connectivity at the expense of the younger (larger ti ) ones, leading with time to some vertices that are highly connected, a ”rich-gets-richer” phenomenon" (PDF p. 6). Model: k_i(t) = m(t/t_i)^0.5; γ = 3 (PDF pp. 6–7).
- Extension to social inequality (speculative): "Similar mechanisms could explain the origin of the social and economic disparities governing competitive systems, since the scale-free inhomogeneities are the inevitable consequence of self-organization due to the local decisions made by the individual vertices, based on information that is biased towards the more visible (richer) vertices, irrespective of the nature and the origin of this visibility." (PDF p. 8).

**Model?** Yes. Compared to data qualitatively (exponent γ_model = 3 vs. empirical 2.1–4); not estimated/fit to any dataset. The time-scaling prediction is explicitly untested: "a scaling property that could be directly tested once time-resolved data on network connectivity becomes available" (PDF p. 6).

**Limitations.**

- Authors' own: "the proposed model cannot be expected to account for all aspects of the studied networks" (PDF p. 7); empirical exponents "scattered between 2.1 and 4" vs. model γ = 3 (PDF p. 7). [model not fit to data]
- Degree (number of ties) as the only node attribute; "visibility" is not decomposed into merit vs. position. [imperfect measure]
- Social-disparity claim is a conjecture, not tested. [no model of mechanism] (for the social application)
- [outcome is not selection] — accrual of ties, not allocation of scarce positions; attachment capacity is unlimited (no fixed slots).

**Channel / source (my judgment).** Selection-like (who gets new ties) driven by accumulated position, not ability — the canonical "cumulative advantage" baseline; source = peers' aggregate choices. Notably no scarcity: everyone can receive links, so no zero-sum competition. Monotonic (more links → more links).

---

## 4. Colizza, Flammini, Serrano & Vespignani 2006 — Detecting rich-club ordering in complex networks

**Citation.** Colizza, V., A. Flammini, M. A. Serrano, and A. Vespignani. 2006. "Detecting Rich-Club Ordering in Complex Networks." *Nature Physics* 2(2): 110–115. DOI 10.1038/nphys209.

**PDF note.** Typeset Nature Physics PDF. PDF p. = journal p. − 109.

**Data / setting.** Four networks (Table 1, p. 112): yeast protein interactions (4,713 nodes); condensed-matter physics coauthorship on arXiv 1995–1998 (15,179 nodes, 43,011 links); worldwide air transportation 2002 (3,880 nodes); Internet autonomous-system level, May 2001 (11,174 nodes). Plus ER, Molloy–Reed, and BA model networks (N = 10^5).

**Design.** Method paper: analytic null model for the rich-club coefficient φ(k) and a degree-preserving randomized null (ρ_ran = φ/φ_ran), applied to observational networks.

**Main findings.**

- Definition: "The ‘rich-club’ phenomenon refers to the tendency of nodes with high centrality, the dominant elements of the system, to form tightly interconnected communities" (abstract, p. 110).
- Social interpretation: "In a social context, for example, a rich-club coefficient increasing with the degree k indicates the dominance of an ‘oligarchy’ of highly connected and mutually communicating individuals, as opposed to a structure consisting of many loosely connected and relatively independent subcommunities." (p. 110).
- Methodological warning: an increasing φ(k) appears even in random graphs — "This implies that the increase of φ(k) is a natural consequence of the fact that vertices with high degree have a larger probability of sharing edges than low-degree vertices." (p. 112; PDF p. 3).
- Result: "we identify a strong rich-club ordering in the scientific collaboration network, providing support to the idea that the elite formed by more influential scientists tends to form collaborative groups within specific domains" (p. 112). Protein network and Internet lack rich-club ordering once normalized (pp. 112–113).
- Distinct from assortativity: "the rich-club phenomenon is not necessarily associated with assortative mixing" (p. 110).

**Model?** A null-model / measurement method, not a generative model of how clubs form. Applied to data; nothing is fit.

**Limitations.**

- Authors' own: richness measured only by degree; "the concept of rich-club ordering should be generalized to evaluate the richness of vertices not just in terms of their degree but in terms of the actual traffic or intensity of interactions handled" (p. 113; PDF p. 4); weighted version deferred: "a detailed account of the evaluation of the weighted rich-club effect will be provided elsewhere" (p. 114; PDF p. 5). [imperfect measure]
- Describes the presence of an elite core, not how it forms. [no model of mechanism]
- Only one social network (coauthorship). [single system]
- [outcome is not selection]

**Channel / source (my judgment).** Structural signature of hierarchy among peers (who connects to the top), source = peers; within an organization, a rich club is the structural form an elite takes. Relevant to selection as a description of the destination state, not the selection process. No competition model; no non-monotonicity.

---

## 5. Clauset, Arbesman & Larremore 2015 — Systematic inequality and hierarchy in faculty hiring networks

**Citation.** Clauset, Aaron, Samuel Arbesman, and Daniel B. Larremore. 2015. "Systematic Inequality and Hierarchy in Faculty Hiring Networks." *Science Advances* 1(1): e1400005. DOI 10.1126/sciadv.1400005.

**PDF note.** Typeset article, 6 pp.; pages printed as "N of 6" — cited below as "p. N/6" (PDF p. = N). Several sentences are broken by figure labels in the default text extraction; these were confirmed with `pdftotext -raw`.

**Data / setting.** "nearly 19,000 tenure-track or tenured faculty, among 461 North American departmental or school-level academic units, in the disciplines of computer science, business, and history" (p. 1/6). 86% of sampled faculty had doctorate and job within the sample ("a nearly closed doctoral ecosystem", p. 1/6). Cross-sectional snapshot of current faculty.

**Design.** Observational network analysis; method = minimum violation ranking (MVR) to extract the prestige ordering that best explains who-hires-whose-graduates; Monte Carlo null; out-of-sample-style placement prediction (AUC) for assistant professors.

**Main findings.**

- Framing (hiring as evaluation): "From the institutional perspective, faculty hiring is an implicit assessment" (p. 1/6). "Differential success rates in such competitions are a hallmark of social hierarchy" (p. 1/6).
- Prestige is explicitly a mix of merit and status: "In this context, prestige in faculty hiring is an operational variable that encompasses differences in both scholastic merit and nonmeritocratic factors such as social status or geography." (p. 1/6).
- Headline: "Across disciplines, we find that faculty hiring follows a common and steeply hierarchical structure that reflects profound social inequality." (abstract, p. 1/6).
- Concentration: faculty production "is highly skewed, with only 25% of institutions producing 71 to 86% of all tenure-track faculty" (p. 2/6).
- Hierarchy steepness: "only 9 to 14% of faculty are placed at institutions more prestigious than their doctorate (r = 0.86 to 0.91)" (p. 3/6); "faculty place an average of 27 to 47 ranks below their doctorate" (p. 3/6).
- Merit argument: "Under a meritocracy, the observed placement rates would imply that faculty with doctorates from the top 10 units are inherently two to six times more productive than faculty with doctorates from the third 10 units." (p. 2/6) … "The magnitude of these differences makes a pure meritocracy seem implausible, suggesting the influence of nonmeritocratic factors like social status." (p. 2/6).
- Gender: "median placement for women graduating from the top 15% of units is 12 to 18% worse than for men from the same institutions" (computer science and business; no difference in history) (p. 3/6).
- Prediction: "Across disciplines, prestige hierarchies make the most accurate predictions of faculty placement, with AUCs ranging from 0.58 to 0.67" (p. 4/6).

**Model?** A ranking-extraction method (MVR) applied to data, plus null-model comparisons. No generative model of how individual candidates are selected; the authors note placement can be predicted "without directly modeling the characteristics or preferences of individuals or institutions" (p. 3/6).

**Limitations (authors' own where possible).**

- Merit and status confounded: "Despite the confounded nature of merit and social status within measurable prestige, the observed hierarchies are sufficiently steep that attributing their structure to differences in merit alone seems implausible." (p. 5/6). [imperfect measure]
- "However, the specific mechanisms that produce and maintain these hierarchies remain unclear" (p. 5/6). [no model of mechanism]
- No individual-level covariates: "A proper study of this phenomenon would require detailed data on the characteristics of the research, mentoring, institutional resources, and other factors that are not part of the present study." (p. 5/6). [imperfect measure]
- Open normative question: "How many meritorious research careers are derailed by the faculty job market’s preference for prestigious doctorates?" (p. 5/6).
- Only successful placements observed (current faculty); unplaced candidates absent — so it measures the outcome distribution among the selected, not the selection odds of the candidate pool (my observation, not the authors'). [imperfect measure]
- Outcome **is** selection (a hire) — the closest paper in this cluster to the dissertation's outcome — but measured at the institution level.

**Channel / source (my judgment).** Selection (scarce faculty slots) and evaluation (hiring as assessment of the doctoral institution); source = organization (doctoral institution's prestige) rather than peers. Strongest evidence in this cluster that the organization one comes from shapes selection independent of plausible merit differences. No within-group competition model; no non-monotonic effect reported.

---

## 6. Guimerà, Uzzi, Spiro & Amaral 2005 — Team assembly mechanisms

**Citation.** Guimerà, Roger, Brian Uzzi, Jarrett Spiro, and Luís A. Nunes Amaral. 2005. "Team Assembly Mechanisms Determine Collaboration Network Structure and Team Performance." *Science* 308(5722): 697–702. DOI 10.1126/science.1106340.

**PDF note.** The library file is the **NIH author manuscript** (PMC, 2007), not the typeset Science article. Printed Science pages (697–702) **cannot be mapped** from this file; locations are author-manuscript pages ("Page N" headers = PDF p.).

**Data / setting.** Broadway musical industry: "we considered all 2258 productions in the period from 1877 to 1990" (ms. p. 2); scientific coauthorship in social psychology (7 journals), economics (9), ecology (10), astronomy (6) (ms. p. 2).

**Design.** Generative model of team assembly (team size m; probability p a slot is filled by an incumbent; probability q an incumbent picks a past collaborator) + observational calibration and correlation with performance (journal impact factor).

**Main findings.**

- "Agents in creative enterprises are embedded in networks that inspire, support, and evaluate their work." (abstract, ms. p. 1).
- Slot-filling model: each team member "has a probability, p, of being drawn from the pool of incumbents and a probability, 1 – p, of being drawn from the pool of newcomers" (ms. p. 3). "Higher values of p indicate fewer opportunities for newcomers to enter a field." (ms. p. 3).
- Phase transition: "four out of the five creative networks we consider are very close to the tipping line at which an invisible college emerges" (ms. p. 4).
- Performance: "The result for p implies that successful teams have a higher fraction of incumbents, who contribute expertise and know-how to the team, whereas the result for q implies that teams that are less diverse typically have lower levels of performance." (ms. p. 5). "Teams publishing in journals with a high-impact factor typically give rise to a large giant component, whereas teams publishing in low-impact journals typically form small isolated clusters." (ms. p. 5).
- Size optimum (framing, citing prior work): "Successful teams evolve toward a size that is large enough to enable specialization and effective division of labor among teammates but small enough to avoid overwhelming costs of group coordination" (ms. p. 1).

**Model?** Yes, and **calibrated to data**: p is read directly from data; "The value of q must be obtained numerically by simulating the model with different tentative values of q until the fraction fR of repeat incumbent-incumbent links predicted by the model coincides with the value measured from the data." (note 36, ms. p. 6). The performance link is correlational across journals.

**Limitations.**

- Performance proxy: "We used each journal's impact factor as a proxy for the typical quality of teams' output." (ms. p. 4). [imperfect measure]
- Astronomy does not fit: "Surprisingly, neither p, q, or S were significantly correlated with impact factor in astronomy." (ms. p. 5); cause unresolved: "Whether these differences are caused by the needs imposed by the creative enterprise itself or to historical or other reasons is a question that we cannot answer conclusively." (ms. p. 5).
- Model generates structure from p, q, m but does not model who among newcomers gets chosen (selection is random within pools). [no model of mechanism] (for individual selection)
- Outcome is team performance, not individual selection. [outcome is not selection]

**Channel / source (my judgment).** Selection (p literally governs how many team slots go to newcomers vs. incumbents — a scarce-slot allocation at the group level) and development (diversity of collaborators); source = peers (incumbent collaborators) and organization (team as the affiliation unit; bipartite person–team structure). Implied non-monotonicity: the authors suggest optimal values of p and q ("a “universal” set of optimal values might exist", ms. p. 5), though no inverted-U is estimated here.

---

## 7. Uzzi & Spiro 2005 — Collaboration and creativity: the small world problem

**Citation.** Uzzi, Brian, and Jarrett Spiro. 2005. "Collaboration and Creativity: The Small World Problem." *American Journal of Sociology* 111(2): 447–504. DOI 10.1086/432782.

**PDF note.** Typeset AJS PDF. PDF p. = journal p. − 446.

**Data / setting.** "Our data include the population of all 2,092 people who worked on 474 musicals of new material produced for Broadway from 1945 to 1989." (p. 465; PDF p. 19). Plus "49 shows that died in preproduction" (p. 465). Artistic-success measure unavailable 1982–1989, "dropping our N for artistic success from 435 to 315" (p. 467).

**Design.** Observational panel of a bipartite artist–production network; network-level small-world quotient Q = CC ratio / PL ratio with Newman–Strogatz–Watts (2001) bipartite random-graph correction; ordered probit (financial hit/flop/failure) and OLS (critics' scores) with controls.

**Main findings.**

- Headline (non-monotonic): "The small world network effect was parabolic; performance increased up to a threshold, after which point the positive effects reversed." (abstract, p. 447). Restated: "Small world networks do benefit performance but only up to a threshold, after which the positive effects of small worlds reverse." (p. 492; PDF p. 46).
- Bipartite representation of organizations: "Bipartite-affiliation networks are distinctive in that all actors in the network are part of at least one fully linked cluster (e.g., all directors on the same board are linked directly to each other), which affects critical social dynamics as well as artificially inflates key small world network statistics." (p. 450; PDF p. 4).
- Mechanism for the downturn, including scarce slots: "The ideas most likely to flow can be conventional rather than fresh ideas because of the common information effect and because newcomers find it harder to land “slots” on productions." (p. 464; PDF p. 18).
- Global structure shapes local returns: "Thus, while collaboration happens between direct relations, the small world influences lower-level mechanisms such as actors’ egocentric webs (Burt 2004)" (p. 465).

**Model?** A verbal theory with a parabolic hypothesis tested by regression on the full population; no generative/formal model of tie formation.

**Limitations (authors' own where possible).**

- Scope limited to bipartite networks: "Our conceptualization of how a small world affects behavior was specific to bipartite-affiliation networks. We did not speculate on how our theory would change for unipartite theories, a natural direction for future research." (p. 493; PDF p. 47).
- Network formation not modelled: "If small world networks can have positive and negative impacts, how do they arise and evolve?" (p. 498; PDF p. 52). Historical interpretation "somewhat speculative" (p. 497). [no model of mechanism]
- One industry; the system-level Q varies only across years (one Q per season-year), so the effective sample for the key variable is ~45 years. [single system] [small data] (my reading)
- Outcome is show-level financial/critical success. [outcome is not selection] — though the slot mechanism is invoked theoretically.

**Channel / source (my judgment).** Development (exposure to diverse vs. homogenized creative material) and, implicitly, selection (newcomers' access to slots as cohesion rises); source = peers (collaborator ties) embedded in organization (productions as groups). **Key non-monotonic result**: benefit up to a point, then harm.

---

## 8. Gould 2002 — The origins of status hierarchies

**Citation.** Gould, Roger V. 2002. "The Origins of Status Hierarchies: A Formal Theory and Empirical Test." *American Journal of Sociology* 107(5): 1143–1178. DOI 10.1086/341744.

**PDF note.** Typeset AJS PDF. PDF p. = journal p. − 1142.

**Data / setting.** Three small-group sociometric datasets (pp. 1162–63): Bales (1956) verbal-communication task groups of sizes 5–8, each pooled into one "archetypal network" per group size; Blatz (1937) play overtures among the five Dionne quintuplets over ~2 years; Newcomb (1961) fraternity — "each of 17 members ranked the others in terms of how friendly they were, once per week for 15 weeks" (p. 1163; PDF p. 21).

**Design.** Formal game-theoretic model (Nash equilibrium of attachment allocation) with closed-form propositions, tested against observed network data (correlations/regressions of dyad asymmetry on status distance, etc.).

**Main findings.**

- Model: "In the model, actors reproduce status hierarchies by adjusting their own status-conferring gestures according to collective attributions." … "Winner-take-all hierarchies are discouraged, however, when people prefer reciprocation of their status-conferring actions." (abstract, p. 1143).
- Amplification: "Socially influenced judgments amplify underlying differences, so that actors who objectively rank above the mean on some abstract quality dimension are overvalued while those ranking below the mean are undervalued—relative to the baseline scenario, in which social influence does not operate." (p. 1146; PDF p. 4).
- Two extremes without reciprocity: "In other words, if self-reinforcing attributions are the only mechanism operating, the only stable outcomes are radical equality or radical inequality." (p. 1149; PDF p. 7).
- Bridging merit and structure: "In other words, it can simultaneously be true, as economistic models suggest, that competitive processes distribute rewards as a function of individual qualities, and, as sociological models propose, that these rewards are nevertheless filtered through structural positions that distribute advantage unevenly." (pp. 1170–71; PDF pp. 28–29).
- Hierarchy without exogenous difference (quintuplets): status positions "can emerge even in the presence of minimal exogenous differences among actors" (p. 1163).
- Organizational prediction: "In the context of work organizations, for instance, q should be higher (implying greater status inequality for sufficiently low s) when it is difficult to disaggregate group achievements into individual contributions." (pp. 1171–72; PDF pp. 29–30).
- Critique of the field: network scholarship tends to "treat network data as determined exogenously, which is to say by some process that is not explicitly modeled." (p. 1172; PDF p. 30).

**Model?** Yes — formal, analytically solved. **Tested against data** via derived propositions that need no measurement of quality or parameters; parameters (s, q) themselves are **not estimated**.

**Limitations (author's own where possible).**

- Social-influence parameter not identified: "Although the degree to which social influence (q) shapes status-conferring judgments could not be assessed directly from the data employed here" (p. 1171; PDF p. 29). [model not fit to data]
- Controls absent: "As a general matter, then, tests of the theory using data from natural settings will need to take fuller account than I have done in the present study of factors beyond sociometric structure." (p. 1169; PDF p. 27). [imperfect measure]
- Very small groups (5–17 people); fit weak in the smallest: "except in the case of groups small enough to render large correlations commonplace" (p. 1171). Bales pooling: "The result is one network where there were originally a dozen or more, which suppresses variation across groups." (p. 1163). [small data]
- Outcome is attention/attachment (status), not allocation of a formal position. [outcome is not selection]

**Channel / source (my judgment).** Evaluation (status as socially influenced judgment of quality; amplification of small quality differences) — source = peers. The work-organization prediction (inequality higher when individual contributions are hard to disaggregate) ties the amplification strength to organizational task structure (organization). Non-monotone in a sense: reciprocity preference caps the cascade (interior equilibria between equality and winner-take-all). Directly relevant to evaluation feeding selection: status is a zero-sum-ish allocation of finite attention.

---

## 9. Lazer & Friedman 2007 — The network structure of exploration and exploitation

**Citation.** Lazer, David, and Allan Friedman. 2007. "The Network Structure of Exploration and Exploitation." *Administrative Science Quarterly* 52(4): 667–694. DOI 10.2189/asqu.52.4.667.

**PDF note.** Typeset ASQ PDF. PDF p. = journal p. − 666.

**Data / setting.** Theory/model only. Agent-based simulation: "we assumed a population of 100 actors" (p. 677) on NK landscapes with "N = 20, and K = 5" (p. 678), averaged over "the same 1000 NK spaces" (p. 678); networks: linear, totally connected, random, small-world (plus hub-spoke).

**Design.** Agent-based simulation (emulation of better-performing neighbours + local search).

**Main findings.**

- "We present an agent-based computer simulation model of information sharing in which the less successful emulate the more successful." (abstract, p. 667).
- Core tradeoff: "Results suggest that when agents are dealing with a complex problem, the more efficient the network at disseminating information, the better the short-run but the lower the long-run performance of the system." (p. 667).
- **Non-monotonic**: "For intermediate time frames, there is an inverted-U relationship between connectedness and performance, in which both poorly and well-connected systems perform badly, and moderately connected systems perform best." (abstract, p. 667).
- Two pathways: "An efficient network positively affects information diffusion, which facilitates the spread of effective strategies, but negatively affects information diversity, which is also positively related to performance." (p. 686; PDF p. 20).
- "Remarkably, the highest performing network in the long run was the slowest, most error prone, and had the longest average path length." (p. 689; PDF p. 23).

**Model?** Yes; simulation only, **not fit to or tested against data**.

**Limitations (authors' own).**

- "As with any purely theory-based research, our results are only as strong as the premises of our approach." (p. 688; PDF p. 22). "Although we would not make managerial recommendations without empirical validation" (p. 689). [model not fit to data]
- **No competition by assumption**: the setting is "parallel problem solving, in which a set of roughly equivalent agents are all seeking to solve the same problem, and the success of any one or subset of agents has no direct effect on other agents" (p. 668; PDF p. 2); "In game theory terms, one might envision each agent playing a game against nature, in which an individual’s performance against nature has no bearing on other players’ payoffs" (p. 668). They flag the extension: "For example, an assumption that actors are competing would reduce the utility of sharing a solution, while assumptions about the presence of some property rights might increase the incentives for exploration over exploitation." (p. 689; PDF p. 23).
- Outcome is system-level performance. [outcome is not selection]

**Channel / source (my judgment).** Development (what solutions individuals reach via peers), source = peers; network as organizational design (organization). **Explicitly non-monotonic** (inverted U at intermediate horizons). Explicitly **excludes competition for positions** — a clear gap the dissertation can name.

---

## 10. Mason & Watts 2012 — Collaborative learning in networks

**Citation.** Mason, Winter, and Duncan J. Watts. 2012. "Collaborative Learning in Networks." *Proceedings of the National Academy of Sciences* 109(3): 764–769. DOI 10.1073/pnas.1110069108.

**PDF note.** Typeset PNAS PDF. PDF p. = journal p. − 763.

**Data / setting.** "a series of 256 Web-based experiments in which groups of 16 individuals collectively solved a complex problem and shared information through different communication networks" (abstract, p. 764); Amazon Mechanical Turk; eight fixed-degree (n = 16, k = 3) networks varying in efficiency; 15 rounds per game (p. 765); 24 baseline (independent) groups of 16 (p. 766).

**Design.** Online randomized experiment (network assigned) + comparison agent-based simulations.

**Main findings.**

- "In contrast to prior work, however, we found that efficient networks outperformed inefficient networks, even in a problem space with qualitative properties thought to favor inefficient networks." (abstract, p. 764).
- Mechanism reversal: "Moreover, we find that inefficient network structures can also decrease exploration, precisely the opposite of what the theory claims they are supposed to accomplish." (p. 769; PDF p. 6).
- Individual vs. collective: copying "thus, players could improve their success by free-riding on others’ exploration" … "the individual decision to exploit negatively impacted the performance of the collective" (p. 768; PDF p. 5).
- **Position effect within a group**: "network efficiency affected the distributions of success, and thereby relative individual performance, in two different and conflicting ways" (p. 768); central players — "those who occupied central positions (i.e., with high betweenness or closeness centrality), consistently earned more points than their peers in the same network" (p. 769; PDF p. 6); and "Thus, depending on whether a given individual cares about relative or absolute performance, and assuming that he or she can also choose his or her network position, he or she may prefer to belong to a more or less centralized network, respectively." (p. 769).
- On models: "agent-based models have, to date, been insufficiently sophisticated and heterogeneous to reflect real human responses to changing circumstances" (p. 769).

**Model?** The experiment tests the Lazer–Friedman prediction; the authors' own simulations reproduce the inefficient-network advantage only for "an intermediate level of myopia" (p. 769). No new model fit to the experimental data.

**Limitations.**

- Authors': "Recognizing that the results of both artificial simulations and artificial experiments should be generalized with caution" (p. 769); landscapes "highly artificial and are likely different from real-world problems in some respects" (p. 766; PDF p. 3).
- Payoffs are individual and non-rival: "Players were paid in direct proportion to their accumulated points; hence, they were motivated to maximize their individual scores but had no incentive to deceive others" (p. 765; PDF p. 2). No scarce slot / rank-based reward. [outcome is not selection]
- Small groups (16), short games (15 rounds), one task. [small data] [single system]

**Channel / source (my judgment).** Development (learning from peers), source = peers; the network structure is an organizational choice (organization). Important for selection: position within the group changes **relative** standing even when everyone's absolute payoff is non-rival — the relative-vs-absolute tension is exactly where a scarce-slot selection rule would bite. Contradicts the inverted-U of Lazer & Friedman for humans in this task.

---

## 11. Granovetter 1973 — The strength of weak ties

**Citation.** Granovetter, Mark S. 1973. "The Strength of Weak Ties." *American Journal of Sociology* 78(6): 1360–1380. (No DOI in bib; JSTOR copy.)

**PDF note.** JSTOR image scan, **no text layer**; text obtained by tesseract OCR (200 dpi). PDF p. 1 is the JSTOR cover; PDF p. = journal p. − 1358 (PDF p. 2 = p. 1360). Quotes were checked against the OCR output; spot-check against the scan before final use.

**Data / setting.** Mostly theoretical argument. Empirical illustration: "a random sample of recent professional, technical, and managerial job changers living in a Boston suburb" (p. 1371); "a random subsample of 100, who were interviewed personally, of the total sample of 282" (fn. 16, p. 1371); tie-strength frequencies reported for N = 54 who found jobs through contacts; information-path lengths for N = 64 (p. 1372).

**Design.** Theory (triadic closure / forbidden triad argument) + small observational survey.

**Main findings.**

- Core proposition: "It is argued that the degree of overlap of two individuals’ friendship networks varies directly with the strength of their tie to one another." (abstract, p. 1360).
- Definition: "the strength of a tie is a (probably linear) combination of the amount of time, the emotional intensity, the intimacy (mutual confiding), and the reciprocal services which characterize the tie." (p. 1361).
- Structural consequence: "What is important, rather, is that all bridges are weak ties." (p. 1364; PDF p. 6).
- Job data: "Of those finding a job through contacts, 16.7% reported that they saw their contact often at the time, 55.6% said occasionally, and 27.8% rarely (N = 54)." (p. 1371; PDF p. 13). Mechanism: "those to whom we are weakly tied are more likely to move in circles different from our own and will thus have access to information different from that which we receive." (p. 1371).
- Information vs. influence (relevant to selection): those reached via long chains or formal channels "are badly placed and dissatisfied in the labor market, and both receive information without influence." (p. 1372; PDF p. 14).
- "From the individual’s point of view, then, weak ties are an important resource in making possible mobility opportunity." (p. 1373; PDF p. 15).
- Macro paradox: "strong ties, breeding local cohesion, lead to overall fragmentation." (p. 1378).

**Model?** Verbal/structural argument (with graph-theoretic notes); not a formal model; job survey is illustrative, not a test of the model.

**Limitations (author's own).**

- "The model offered here is a very limited step in the linking of levels; it is a fragment of a theory." … "My contribution here is mainly, then, exploratory and programmatic" (p. 1378; PDF p. 20).
- Tie strength measured by contact frequency only: "Although this corresponds only to the first of the four dimensions in my definition" (fn. 15, p. 1371). [imperfect measure]
- Small N: "The numbers reported are small because they represent a random subsample of 100, who were interviewed personally, of the total sample of 282." (fn. 16, p. 1371). [small data]
- No baseline: "Since baseline data on acquaintance networks are lacking, this objection remains inconclusive." (fn. 18, p. 1372). [no model of mechanism] (no null for how many job leads should come via weak ties)
- Outcome is job finding (information access) — close to, but not, selection among competitors; the employer's choice is not observed. [outcome is not selection] (partially)

**Channel / source (my judgment).** Selection-adjacent: access to openings and to "influence" on the hiring decision; source = peers (ties), with group boundaries (clusters of strong ties) shaping what information reaches a candidate. No competition among candidates is modelled; no non-monotonicity.

---

## 12. Breiger 1974 — The duality of persons and groups

**Citation.** Breiger, Ronald L. 1974. "The Duality of Persons and Groups." *Social Forces* 53(2): 181–190. DOI 10.2307/2576011.

**PDF note.** JSTOR image scan, **no text layer**; text by tesseract OCR. PDF p. 1 is the JSTOR cover; PDF p. = journal p. + 1. Quotes checked against OCR; spot-check against the scan.

**Data / setting.** Method paper. Illustrative application to Davis, Gardner & Gardner (1941) "Old City" data — the researchers "compiled a table with eighteen rows—one for each woman—and fourteen columns, one for each “event”" (p. 184; PDF p. 5).

**Design.** Method (matrix formalization of two-mode / affiliation networks and their one-mode projections).

**Main findings.**

- Aim: "A metaphor of classical social theory concerning the “intersection” of persons within groups and of groups within the individual is translated into a set of techniques to aid in empirical analysis of the interpenetration of networks of interpersonal ties and networks of intergroup ties." (abstract, p. 181).
- Individuality from affiliations (Simmel): "At the same time, the particular patterning of an individual’s affiliations (or the “intersection” of groups within the person) defines his points of reference and (at least partially) determines his individuality." (p. 181).
- Definition: "Consider a set of individuals and a set of groups such that the value of a tie between any two individuals is defined as the number of groups of which they both are members. The value of a tie between any two groups is defined conversely as the number of persons who belong to both." (pp. 181–82).
- Core result: "Thus: two distinct matrices, one of person-to-person relations (P) and one of group-to-group relations (G), are uniquely defined by and derivable from a single “translation” matrix (A) of person-to-group affiliations." (p. 183; PDF p. 4). (P = AAᵀ, G = AᵀA, Eqs. 3–4.)
- Duality: "persons who are actors in one picture (the P matrix) are with equal legitimacy viewed as connections in the dual picture (the G matrix), and conversely for groups." (p. 184).
- Projection problem: in the Davis data the woman-to-woman matrix is nearly complete ("The ratio 139/153 is 0.91", fn. 6, p. 185) — "Since everyone was connected to virtually everyone else, identification of subgroupings became problematic." (p. 185; PDF p. 6). Working from the dual (event) matrix reduces connectivity "to 30 percent" and recovers Homans's two cliques (p. 185).
- Competition and status in affiliations (asymmetric extension, quoting Simmel): "“Modern competition is described as the fight of all against all, but at the same time it is the fight of all for all”—and thus results not in the chaos of Hobbes (which necessitates external control) but in an intrinsically ordered interweaving of relations based on “the possibilities of gaining favor and connection.”" (p. 189; PDF p. 10). Asymmetric ties are motivated by "the assumption here being that directors of higher-status corporations are more sought after to lend their prestige to the boards of other corporations" (p. 189).

**Model?** A formal representation (algebra of affiliation matrices), not a generative or statistical model; nothing is fit.

**Limitations.**

- No stated limitations section. Illustration is 18 women × 14 events. [small data] [single system]
- Representation only; says nothing about how memberships are allocated. [no model of mechanism]
- [outcome is not selection]

**Channel / source (my judgment).** Foundational for representing the **organization** source: persons and groups as a bipartite structure, with person-person ties derived from co-membership. The asymmetric extension (primary vs. secondary affiliations; status-seeking board appointments) is the closest this paper comes to selection into groups. No non-monotonicity.

---

## 13. Centola & Macy 2007 — Complex contagions and the weakness of long ties

**Citation.** Centola, Damon, and Michael Macy. 2007. "Complex Contagions and the Weakness of Long Ties." *American Journal of Sociology* 113(3): 702–734. DOI 10.1086/521848.

**PDF note.** The library file is a **working-paper draft dated September 12, 2005** (66 pp., double-spaced), **not** the published AJS article; the abstract wording differs from the published version. Printed AJS page numbers **cannot be given** from this file; locations are manuscript pages (= PDF p.). Re-check every quote against the published article before using it in the dissertation.

**Data / setting.** Theory/model only: simulations on Watts–Strogatz ring lattices with random rewiring (e.g., "N = 2000, averaged over 100 realizations", figure captions, ms. pp. 56–58).

**Design.** Analytical argument + agent-based threshold-contagion simulations.

**Main findings.**

- Question: "We test whether this effect of long ties generalizes from simple to complex contagions – those in which the credibility of information or the willingness to adopt an innovation requires independent confirmation from multiple sources." (abstract, ms. p. 2).
- Result: "we demonstrate that long ties may not only fail to speed up complex contagions, they can even preclude diffusion entirely" (abstract, ms. p. 2).
- Bridge width, not length: "For complex contagions, the relevant attribute of a bridge is not the length of a dyadic tie but the width of the bridge, measured by the number of short paths between non-neighbors." (ms. p. 37).
- Caution: "The qualitative differences we discovered between simple and complex contagions should caution network theorists about extrapolating from the spread of disease or information to the spread of participation in political, religious, or cultural movements." (ms. p. 39).

**Model?** Yes; simulation; **not fit to data** (empirical social-movement cases are cited as consistent illustrations).

**Limitations.**

- Simplifying assumptions, stated by the authors: "assuming that every node has equal influence and every tie has equal weight. These assumptions are necessary to identify the structural effects of long ties" (ms. p. 16). Reversible states deferred: "We leave the effects of reversible states to future research." (fn., ms. p. 23). [model not fit to data]
- [outcome is not selection]

**Channel / source (my judgment).** Development/adoption via peers (source = peers): when an outcome requires reinforcement from multiple contacts, clustered (group-like) structure helps and long ties do not — another case where the "more connection is better" intuition fails. Non-monotonicity: the effect of random rewiring depends on the threshold (helps simple, hurts complex contagions); no competition for slots.

---

## 14a. Burt 1992 — Structural Holes: The Social Structure of Competition (chapter 1 only)

**Citation.** Burt, Ronald S. 1992. *Structural Holes: The Social Structure of Competition*. Cambridge, MA: Harvard University Press. (Bib entry is `@misc` with no publisher/pages; publisher from general knowledge — confirm.) Chapter 1, "The Social Structure of Competition," pp. 8–49.

**PDF note.** The library file contains **only chapter 1** (42 PDF pp.), an image scan with no text layer; text by tesseract OCR (`--psm 6`). PDF p. = book p. − 7 (PDF p. 1 = p. 8). Scan edges are cropped/skewed on some pages, so OCR has scattered errors; quotes below were chosen from clean stretches, with one OCR slip flagged. Spot-check against the scan.

**Data / setting.** Theory (chapter 1 is the conceptual argument; empirical chapters not in file).

**Design.** Theory.

**Main findings.**

- Thesis: "It is a description of the way in which social structure renders competition imperfect by creating entrepreneurial opportunities for certain players and not for others." (p. 8; PDF p. 1).
- Scope includes selection outcomes: "I refer to opportunities in a broad sense, but I certainly mean to include the obvious examples of job promotions, participation in significant projects, influential access to important decisions, and so on." (p. 9). "The social capital of people aggregates into the social capital of organizations." (p. 9).
- **Selection among equally able candidates**: "Competition is never perfect. The rules of trade are ambiguous in the aggregate and everywhere negotiable in the particular. The allocation of opportunities is rarely made with respect to a single dimension of abilities needed for a task. Within an acceptable range of needed abilities, there are many people with financial and human capital comparable to your own." … "Criteria other than financial and human capital are used to narrow the pool down to the individual who gets the opportunity. Those other criteria are social capital." … "Of those who are equally qualified, only a select few get the most rewarding opportunities." (p. 10; PDF p. 3).
- Definition: "Nonredundant contacts are connected by a structural hole. A structural hole is a relationship of nonredundancy between two contacts." (p. 18; PDF p. 11).
- Forward reference to promotion evidence (ch. 4, not in file): "Promotions in the firm are strongly correlated, and illuminatingly so for women, with the structural holes in a manager’s network." (p. 33; PDF p. 26; OCR reads "ina", corrected to "in a").
- Benefits are not automatic: "There is no imperative that says players have to take advantage of the benefits provided by structural holes." (p. 37; PDF p. 30).

**Model?** Conceptual model (information and control benefits; tertius gaudens; structural autonomy), formalized in later chapters; no fit in chapter 1.

**Limitations.** Chapter 1 is argument only; evidence deferred to later chapters. [no model of mechanism] is not apt (mechanism is proposed) but [model not fit to data] applies within this chapter. Outcome framed as rate of return, which subsumes promotion. Competition is framed as among "players" in an arena, not explicitly a fixed number of slots.

**Channel / source (my judgment).** **Selection** is explicit: when candidates are comparable on ability, network position (peers' structure) decides who "gets the opportunity" — the clearest statement in this cluster that selection among competitors depends on something other than individual performance. Source = peers (contact network), aggregated to the organization.

---

## 14b. Burt 2004 — Structural holes and good ideas

**Citation.** Burt, Ronald S. 2004. "Structural Holes and Good Ideas." *American Journal of Sociology* 110(2): 349–399. DOI 10.1086/421787.

**PDF note.** Typeset AJS PDF. PDF p. = journal p. − 348. In the text layer the "=" sign is encoded as "p" (e.g., "P p .68"); rendered below as "=".

**Data / setting.** "I draw on data describing 673 managers who ran the supply chain in 2001 for one of America’s largest electronics companies." (p. 359). "Of the 673 managers, 455 completed the network questions (68%)." (p. 360). Personnel records for salary, evaluations, promotion; 455 ideas rated by two senior managers.

**Design.** Observational, cross-sectional network survey + administrative outcomes; regression (salary OLS, ordinal logit for evaluation, logit for promotion); blind idea ratings.

**Main findings.**

- Hypothesis: "The hypothesis in this article is that people who stand near the holes in a social structure are at higher risk of having good ideas." (p. 349). Mechanism: "Opinion and behavior are more homogeneous within than between groups, so people connected across groups are more familiar with alternative ways of thinking and behaving." (abstract, p. 349).
- Outcomes include evaluation and selection: "Compensation, positive performance evaluations, promotions, and good ideas are disproportionately in the hands of people whose networks span structural holes." (abstract, p. 349). "The between-group brokers are more likely to express ideas, less likely to have ideas dismissed, and more likely to have ideas evaluated as valuable." (p. 349).
- Promotion: "Managers brokering connections across segregated groups had significantly higher odds of a promotion or above-average salary increase (P = .68 for C = 10). Managers limited to a circle of densely interconnected colleagues had the least chance (P = .28 for C = 100)." (p. 376; PDF p. 28).
- Rank-dependent returns: "The results of model 1 highlight the third rank of managers as a transition point after which managers enjoyed the salary benefits of brokerage." (fn. 11, p. 371; PDF p. 23).
- Blind evaluation of ideas: judges received "the ideas—unattributed to their sources—and was asked the question: “How much value could be generated if the idea were well executed?”" (p. 377; PDF p. 29).

**Model?** Theoretical mechanism (vision advantage) + regressions; no generative model.

**Limitations (author's own where possible).**

- "The association cannot be causal. Networks do not act, they are a context for action." (p. 354; PDF p. 6). [no model of mechanism] (for causal identification)
- "The caution here is that structural holes and brokerage can be found in almost any task, depending on point of view." (p. 354). [imperfect measure]
- Cross-section: "Disentangling centrality from brokerage would require network and salary data over time" (p. 372; PDF p. 24). [imperfect measure]
- One company, one function. [single system]
- Outcome **includes** selection (promotion), but promotion is pooled with above-average raises in the main model and not modelled as competition for a fixed number of openings (my observation).

**Channel / source (my judgment).** Development (better ideas via exposure to diverse groups), evaluation (ideas and job evaluations), and selection (promotion); source = peers (discussion network) across organizational groups (business units). Rank-dependent effect (benefits begin at a transition rank) is a form of non-linearity; not an inverted U.

---

## 15a. Lazer et al. 2009 — Computational social science (key claims only)

**Citation.** Lazer, David, Alex Pentland, Lada Adamic, Sinan Aral, Albert-László Barabási, Devon Brewer, Nicholas Christakis, Noshir Contractor, James Fowler, Myron Gutmann, Tony Jebara, Gary King, Michael Macy, Deb Roy, and Marshall Van Alstyne. 2009. "Computational Social Science." *Science* 323(5915): 721–723. DOI 10.1126/science.1167742.

**PDF note.** The bib lists two attachments; the typeset Science pages (files/322; 4 PDF pp., PDF p. 1 = p. 721) were used. (The other attachment is an NIH author manuscript with different wording — do not mix.)

**Data / design.** Perspective (no data).

**Key claims.**

- Old data base of network theory: "For example, what does existing sociological network theory, built mostly on a foundation of one-time “snapshot” data, typically with only dozens of people, tell us about massively longitudinal data sets of millions of people, including location, financial transactions, and communications?" (p. 722; PDF p. 2). Also: "To date, research on human interactions has relied mainly on one-time, self-reported data on relationships." (p. 722).
- Position matters: "Similarly, social network Web sites offer a unique opportunity to understand the impact of a person’s position in the network on everything from their tastes to their moods to their health" (p. 722).
- "In short, a computational social science is emerging that leverages the capacity to collect and analyze data with an unprecedented breadth and depth and scale." (p. 722).

**Limitations / relevance.** Programmatic; flags access/privacy as "the thorniest challenges" (p. 722). Tag for the older literature it critiques: [small data] [imperfect measure].

**Channel / source (my judgment).** Methodological framing only: justifies revisiting position-and-outcome questions with complete, longitudinal administrative data (e.g., full draft/promotion records).

---

## 15b. Lazer et al. 2020 — Computational social science: obstacles and opportunities (key claims only)

**Citation.** Lazer, David M. J., Alex Pentland, Duncan J. Watts, Sinan Aral, Susan Athey, Noshir Contractor, Deen Freelon, Sandra González-Bailón, Gary King, Helen Margetts, Alondra Nelson, Matthew J. Salganik, Markus Strohmaier, Alessandro Vespignani, and Claudia Wagner. 2020. "Computational Social Science: Obstacles and Opportunities." *Science* 369(6507): 1060–1062. DOI 10.1126/science.aaz8170.

**PDF note.** Typeset Science Policy Forum; PDF p. 1 = p. 1060.

**Data / design.** Policy Forum (no data).

**Key claims.**

- Definition: "We define CSS as the development and application of computational methods to complex, typically large-scale, human (sometimes simulated) behavioral data (1)." (p. 1060).
- Dependence among observations is the point: "Whereas traditional quantitative social science has focused on rows of cases and columns of variables, typically with assumptions of independence among observations, CSS encompasses language, location and movement, networks, images, and video, with the application of statistical models that capture multifarious dependencies within data." (p. 1060).
- Progress and shortfall: "These studies have greatly improved our understanding of important phenomena, ranging from social inequality to the spread of infectious diseases." … "But the field has also fallen short in important ways." (p. 1060).

**Channel / source (my judgment).** Methodological framing: the "dependencies within data" line is a direct warrant for modelling an individual's selection as dependent on peers rather than as an independent row.

---

## 16a. Nikolaev & Mneimneh 2023 — Affiliation networks with preferential attachment and subsumption (brief)

**Citation.** Nikolaev, Alexey, and Saad Mneimneh. 2023. "Modeling and Analysis of Affiliation Networks with Preferential Attachment and Subsumption." *Physical Review E* 108(1): 014310. DOI 10.1103/PhysRevE.108.014310.

**PDF note.** Typeset PRE; pages are 014310-N (PDF p. N).

**What it models.** A growth model for affiliation (group) networks represented as hypergraphs / simplicial complexes rather than pairwise graphs: "Some networks, however, are better described as groups of nodes rather than a set of pairwise connections. These groups are called affiliations, and the corresponding networks affiliation networks." (abstract, p. 014310-1). Motivation: "When viewed as graphs, affiliation networks do not necessarily exhibit the power law distribution of node degrees that is typically associated with preferential attachment." (p. 014310-1). "Subsumption" = "an affiliation cannot be a subset of another" (p. 014310-1).

**Design / fit.** Analytic + simulation; compared descriptively to KONECT networks (assortativity, clustering; Table II). Not fit: "Although our model was not designed for network replication" (p. 014310-10); framed as a generator: "so the framework also serves as a synthetic generation algorithm for simulation and experimental studies" (p. 014310-1). [model not fit to data] [outcome is not selection]

**Channel / source (my judgment).** Organization representation only (how person–group structures grow with cumulative advantage at the group level). No outcomes, no competition among persons.

---

## 16b. Geard & Bullock 2010 — Competition and the dynamics of group affiliation (brief)

**Citation.** Geard, Nicholas, and Seth Bullock. 2010. "Competition and the Dynamics of Group Affiliation." *Advances in Complex Systems* 13(4): 501–517. DOI 10.1142/S0219525910002712. (PDF filename says 2011; the article itself and the bib say 2010.)

**PDF note.** Typeset ACS PDF. PDF p. = journal p. − 500.

**What it models.** Co-evolution of a social network and multiple, non-exclusive group memberships under finite individual "time and energy" (TAE) capacity: "Given that the resources of individuals are finite, groups can be considered to compete with one another for the time and energy of their members." (abstract, p. 501). Two-way link: "social networks provide the conduits via which groups recruit new members and groups provide the context in which new social ties are formed" (p. 501). Competition is varied via capacity and membership cost (p. 501).

**Findings (simulation).** "Reducing the level of competition between groups (Series A) reduces the level of community structure observed in the social network and increases the level of observed homophily." (p. 513). Diminishing effect: "Most of these gains occur with the initial removal of exclusive membership and further reductions in competition have less impact on group properties." (p. 513). Position: "When individuals have different capacities for group affiliation (Series C), individuals with greater capacity come to occupy more central locations in the social network." (p. 513).

**Design / fit / limitations.** Agent-based simulation; no data. Authors: "the current model omits an explicit description of both an individual’s utility function and a group’s efficacy." (p. 514). [model not fit to data] [outcome is not selection]

**Channel / source (my judgment).** Organization source. Important distinction for the dissertation: here **groups compete for members' time**, not **members competing for slots within a group** — the reverse of the selection problem. Useful as a contrast case.

---
