Source: `sources/FOUNDY_Intro/files/580/Wang et al. - 2025 - 40 An overview of the science of success.pdf` | Read 2026-10-28 | Prepared by helper agent for FOUNDY; quotes to be spot-checked.

Pages are **printed page labels** (printed = PDF index + 591). Quotes are verbatim; line-break hyphens rejoined, apostrophes straightened.

## 0. Verified record

- **Authors:** Xindi Wang, Alexander J. Gates, Albert-László Barabási.
- **Chapter:** "40. An overview of the science of success".
- **Book:** *Handbook of computational social science* (running head).
- **Pages:** 592–608.
- **ISBN:** The footer prints "9781802207309"; it is unlabeled but probably an ISBN.
- **Publisher:** Not printed. The footer reads "Downloaded from https://www.elgaronline.com/", which implies Edward Elgar (inferred).
- **Editors:** Not printed. The metadata copyright line reads "© Taha Yasseri 2025", which suggests Yasseri is the editor (unconfirmed).
- **Year:** 2025, from metadata only.
- **DOI:** not found.
- **Abstract:** in the metadata only, not on the printed pages.

## 1. Structure

- **SUCCESS IS UNBOUNDED** (592–593): Performance is bounded; success is heavy-tailed (log-normal, power law).
- **SUCCESS BREEDS SUCCESS** (593–594): Matthew effect; the Simon, Price, and Barabási–Albert models; van de Rijt experiments.
- **SUCCESS IN SCIENCE** (595)
  - *Scientific Impact* (595–596): Citation model with preferential attachment, fitness, and aging.
  - *Science of Careers* (597): Random-impact rule and Q model.
- **CREATIVE SUCCESS** (597–598)
  - *Success in Art* (598–600): Co-exhibition network and prestige lock-in.
  - *Success in Book Publishing* (600–603): Predicting sales; publisher imprint matters most; limits of machine learning.
- **RECENT TOPICS** (603)
  - *Inequality* (603–604): Gender gap.
  - *Science of Failure* (605–606): Learning from failure.
- **CONCLUSION; FURTHER READING; REFERENCES** (606–608).

## 2. Definitions

- **Success:** "Success, captured by fame, celebrity, popularity, impact, or visibility, is a collective measure, representing a community's recognition of an individual's performance in a particular behavior (Barabási, 2018)." (592)
- **Performance:** "behaviors associated with performance typically follow a bounded distribution, so that most individuals have a relatively similar level of performance, and differences between high-performing individuals are small." (592)
- **The relationship:**
  - "this distinction between performance and success as characterized by bounded and unbounded distributions has important implications that permeate all facets of the 'science of success.'" (592)
  - "the measurable performance characteristics of successful individuals are relatively similar, differing by only small fractions" (593)
- **"Laws":** The chapter does not list the laws from *The Formula* (cited only under Further Reading). Its stated core: "First, we highlight the concept that success is unbounded ... Second, we underscore the phenomenon of success fostering further success" (606). Named rules: "random-impact rule" (597); "prestige lock-in effect" (598).

## 3. Where the environment enters

The channel and source labels are **our coding**; the chapter does not use these categories.

| # | Quote (page) | Cites | Channel | Source |
|---|---|---|---|---|
| 1 | "a community's recognition of an individual's performance" (592) | Barabási 2018 | Evaluation | Peers / community |
| 2 | "the dynamic of social recognition is susceptible to positive feedback operating on arbitrary initial advantages" (593) | Merton 1968 | Evaluation | Peers |
| 3 | "publications receive new citations with probability proportional to their existing number of citations" (594) | Price 1976; Barabási 1999 | Evaluation | Peers (citers) |
| 4 | "early success bestowed on arbitrarily selected recipients produced significant improvements in subsequent rates of success" (594) | van de Rijt 2014 | Evaluation | Peers / audience |
| 5 | "complicated by disciplinary and temporal variation in the processes of scientific recognition" (597) | Aksnes 2019; Haustein 2014; Mingers 2015 | Evaluation | Field |
| 6 | "quantitative signatures of success based on community recognition can be modeled in sports, art, and literature" (598) | Herrera-Guzmán 2023; Uzzi 2008; Uzzi & Spiro 2005 | Evaluation | Mentioned only |
| 7 | "the signatures of success in art are evidenced by exhibitions in prestigious museums and galleries" (598) | Fraiberger 2018 | Evaluation | Organization |
| 8 | "access to future exhibition opportunities is a function of both the artists' current exhibition venue as well as the artist's previous exhibition history" (598) | Fraiberger 2018 | Selection + evaluation | Organization |
| 9 | "the publisher acts as a proxy for the extent of resources and know-how devoted to marketing" (601) | Wang X 2019b | Evaluation (visibility) | Organization |
| 10 | "Publishers also signal a judgment of quality when selecting a book for publication; hence the publisher's quality/prestige facilitates access to more prestigious authors and better manuscripts" (601) | Wang X 2019b | Selection + evaluation | Organization |
| 11 | "imprint (publisher) is the most important feature group, followed closely by previous sales" (603) | Wang X 2019b | Evaluation (predictive) | Organization |
| 12 | "systemic inequality and unequal access to resources can be compounded by the dynamics of recognition underlying success" (604) | Huang 2020 | Development + evaluation | Institution |
| 13 | "the data cover the reviewers' scores and eventual outcome for all applications" (605) | Yin 2019 | Selection (data context only) | Organization (NIH) |

Collaborators, teams, and mentors never appear as determinants of success. "team" and "mentor" have no hits; the one hit for "collaborat" (595) refers to the field's own researchers.

## 4. Gap test

**(a) Local competition for scarce slots: not discussed.** The only hit for "competit" is in the Simon growth model (594): "competition for growth between groups of the same type is not random, but biased by the size of the group". That describes an abstract model, not people. "rank" appears only for the institution ranking (598) and books ranked by sales (601, 603). "peer", "crowd", "congest", "local", and "tournament" have no hits. "relative" appears only in generic usage.

**(b) Adverse or non-monotonic effects of strong peers or prestige: not discussed.** All prestige effects in the chapter are positive or lock-in. "big fish" and "overshadow" have no hits; "pond" matches only "correspond".

**(c) Luck, noise, and selection rules:**
- Luck is discussed: "the random-impact rule also suggests luck is a crucial ingredient to achieve success (Janosov et al., 2020)." (597)
- Chance is discussed: "if success is primarily attributed to chance, and independent of previous experiences (i.e., failures), then the probability of future success should be constant" (605)
- "noise" has no hits.
- No selection rule (top-K, quota, threshold) is modeled; the only mentions are publishers selecting books (row 10) and grant review (row 13).

**(d) Causal identification: never applied to environment effects.**
- The only randomized evidence is on early recognition (row 4).
- "machine learning models often lack the ability to provide a causal explanation, offering insights into associations within the data." (603)
- "the authors performed a series of casual matching experiments" (604; the typo is in the original). The matching is on career length, not environment.
- **Sorting and homophily: not discussed.** "sort" matches only "sorted by their sales" (601); "homophily" has no hits. Prestige lock-in is never tested against sorting.

**(e) Military, drafts, tenure, admissions: none.** "military", "army", "draft", "tenure", "admission", and "school" have no hits. Nearby mentions: the 100-meter dash (592), "sports" (598), "careers in academia" (604), and "ballet academies" (reference title only, 607).

## 5. Open questions

The chapter has no explicit future-work section. Closest statements:
- "With a deeper understanding of the precursors and dynamics of success, it will be possible to develop systems and policies that more reliably highlight the magnitude of human accomplishments." (606)
- "to develop a comprehensive understanding of success, we must also model the impact of inequalities." (604)
- "relatively little is known about the factors contributing to a book's success or the dynamics through which that success is attained." (600)
- "quantitatively studying the relationship between failure and success is limited by data availability and survivorship bias." (605)
- "we must rephrase the conversation about gender inequality around the sustainability of women's careers in academia." (604)

## 6. Key references

- Barabási 2018, *The Formula*. Used for: success as collective recognition.
- Yucesoy & Barabási 2016, "Untangling performance from success," *EPJ DS*. Used for: Wikipedia pageviews as a fame measure.
- Merton 1968, "Matthew effect," *Science*. Used for: rich-get-richer recognition.
- Simon 1955, *Biometrika*. Used for: generic success-breeds-success model.
- Price 1976, "cumulative advantage," *JASIS*. Used for: citation preferential attachment.
- Barabási & Albert 1999, *Science*. Used for: preferential attachment in network growth.
- van de Rijt 2014, "Field experiments of success-breeds-success," *PNAS*. Used for: randomized feedback evidence.
- Wang D 2013, "Long-term scientific impact," *Science*. Used for: citation dynamics model.
- Sinatra 2016, "Evolution of individual scientific impact," *Science*. Used for: random-impact rule; Q.
- Janosov 2020, "Success and luck in creative careers," *EPJ DS*. Used for: luck.
- Fraiberger 2018, "Reputation and success in art," *Science*. Used for: prestige lock-in; institution network.
- Wang X 2019b, "Success in books," *EPJ DS*. Used for: publisher imprint as the top predictor.
- Yucesoy 2018, "Success in books," *EPJ DS*. Used for: bestseller patterns.
- Huang 2020, "Gender inequality in scientific careers," *PNAS*. Used for: dropout drives the gap.
- Yin 2019, "Dynamics of failure," *Nature*. Used for: learning from failure; NIH grants.
- Herrera-Guzmán 2023, "Prestige in US ballet academies," SocArXiv. Used for: passing citation only.
- Uzzi & Spiro 2005, "Collaboration and creativity," *AJS*. Used for: passing citation only.
- Aksnes 2019, *Sage Open*. Used for: field variation in recognition.
- Fortunato 2018, "Science of science," *Science* (Vespignani is a co-author). Used for: interdisciplinary methods.

## 7. Helper's suggestion (helper's view, not the chapter's)

This chapter can support three claims: the field separates bounded, individual performance from unbounded, collective success (recognition); recognition feeds back on itself, with randomized evidence; and organizations such as galleries and publishers are associated with success as gatekeepers and visibility channels, though only predictively. It cannot support claims about local competition for fixed slots, adverse peer or prestige effects, explicit selection rules, or sorting versus causal effects. It also does not cover drafts, promotion, tenure, or admissions. A gap statement should be framed as "this overview does not address X", not as "the field ignores X".
