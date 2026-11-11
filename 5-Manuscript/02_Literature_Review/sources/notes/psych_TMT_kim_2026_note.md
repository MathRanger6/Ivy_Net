# Too-much-talent debate — Kim et al. 2026 plus Swaab 2014 and Gula 2021: source note

Compiled 2026-10-30 by FOUNDY from the library PDFs (`pdftotext`). Journal pages. Not dissertation prose.

## Kim, Zhao, Jang & Zhu (2026)

**Citation.** Kim, Donghun, Yi Zhao, Sou Hyun Jang, and Yongjun Zhu. 2026. "Exploring the Too-Much-Talent effect in academic fields: Evidence from the National Institutes of Health in the United States." *Scientometrics* 131: 8311–8327. DOI 10.1007/s11192-026-05819-3. Published online 24 Sep 2026.

**Data.** 56,400 articles published by NIH institutes and centers (ICs), 2011–2020, analyzed separately for each of 25 ICs (from 119 papers at NCCIH to 17,881 at NCI).

**Unit.** "We defined a research team as a group of researchers involved in writing/publishing an article." The team is the author list.

**Measures.**
- Talent = z(impact) + z(productivity), standardized within IC and year. Impact is the mean 2-year citations of the author's previous papers; productivity is papers per year before year t. Talent is measured only from earlier publications, which the authors call a "temporal holdout".
- Team performance = ln(2-year citations + 1) of the article.
- Controls: team size, funding, year, and author-position dummies.

**Design.**
- Six functional forms (linear, quadratic, cubic, log, logistic, power), compared by AIC.
- A "peak-data sufficiency" check, which answers the Gula et al. critique that an inverted U can rest on too few observations past the peak.
- Then a two-lines (piecewise) test with the Robin Hood breakpoint (Simonsohn 2018), Bonferroni-corrected across the 25 ICs.

**Findings (abstract, p. 8311).** "The log function generally provided a better fit than the quadratic function across NIH ICs. At most one IC showed evidence of a TMT effect, and this effect was not statistically robust. However, employing alternative methods to assess top talent and team performance may produce different results."

**Authors' limitations (Discussion).**
1. Only listed authors are counted.
2. Talent and performance are both measured by publications and citations.
3. "we examined only the direct relationship between the proportion of top talent and team performance … However, Swaab et al. (2014) noted that mediators (e.g., intrateam coordination) may mediate this relationship."
4. They call for qualitative and mixed-methods work.

**The authors do NOT give a "science differs from sports because of division of labor or asynchronous work" explanation.** That claim in the AI overview Charles received (10-30) is the overview's own speculation.

**Assistant judgment.**
- Outcome is the team's (article's) citations, not an individual's advancement, so the outcome is not selection.
- Talent and performance are in the same currency (citations), which is an imperfect measure.
- The "team" is a co-author list, not an organization.
- One funder, so a single system.
- Value for the dissertation: a third failure to replicate the inverted U with proper functional-form tests. Use it for the curve-shape caution, alongside Simonsohn 2018 and Grant & Schwartz 2011.

## Swaab, Schaerer, Anicich, Ronay & Galinsky (2014), *Psychological Science* 25(8): 1581–1591

**Abstract (verbatim, key lines).**
- "Two survey studies found that people believe there is a linear and nearly monotonic relationship between talent and performance."
- "building off research on status conflicts, we predicted that talent facilitates performance—but only up to a point, after which the benefits of more talent decrease and eventually become detrimental as intrateam coordination suffers."
- "Three archival studies revealed that the too-much-talent effect emerged when team members were interdependent (football and basketball) but not independent (baseball)."

**Method, as described by Kim et al. (p. 8312).** A quadratic regression with the proportion of top-third players as the predictor, covering 30 NBA teams, 209 FIFA national teams and 30 MLB teams.

**The mechanism is individual-level rivalry (p. 1582; string-checked).** "In the absence of a clearly defined pecking order, energy that would normally be steered toward intrateam coordination and performance is diverted toward jockeying for dominance."

**Motivation agreed with Alex (10-30 text thread).** These papers motivate the dissertation by contrast. The proposed mechanism is a contest among individuals inside the team, but the outcome is measured only at the team level, so what the contest does to each member's advancement is unobserved.

## Gula, Vaci, Alexandrowicz & Bilalić (2021), *Psychological Science*

- A comment on Swaab et al. It re-analyzed 10 NBA seasons (2002–2012; N = 297) and 64 seasons (1956–2019; N = 1,417).
- It used the same six functional forms plus interrupted (two-line) regression.
- It found no too-much-talent effect. Most functions fit better than the quadratic.

## Also cited by Kim et al., not in library

- **Long et al. 2024** (*German Journal of Exercise and Sport Research* 52(4)?; check). It covers 130 European football teams, varies the threshold for top talent from 10% to 35%, and finds no too-much-talent effect, only diminishing returns.
- **Groysberg, Polzer & Elfenbein 2011** ("Too many cooks spoil the broth," *Organization Science*). Stars among equity-research analysts; relevant to organizational studies.
