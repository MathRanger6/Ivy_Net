# One-Page Advisor Brief Template
## College Basketball Replication of Army Inverted-U

Date: [YYYY-MM-DD]  
Prepared by: [Name]  
Run ID: [short label]

---

## 1) Objective for this run (2-3 lines)

State exactly what this run tests.

Example:
- Baseline test of inverted-U between team-season pool quality and draft advancement.
- Compare baseline to one alternative mapping with explicit congestion features.

---

## 2) Design snapshot (fill-in table)

| Component | Baseline | Alternative |
|---|---|---|
| Outcome definition |  |  |
| Unit of analysis |  |  |
| Pool definition |  |  |
| Own-performance metric |  |  |
| Pool-quality measure |  |  |
| Key controls |  |  |
| Sample restrictions |  |  |
| Memo data blocks | spine + [list (1)–(8) used] | spine + [list (1)–(8) used] |

*Reference:* `obsolete_documents/sports_gameplan_old/College_Replication_Decision_Memo_Baseline_vs_Alternative_bkup.md` → **Datasets and linkages to enable extended options** (baseline **spine** is unnumbered; **(1)–(8)** are the numbered subsections; **(8)** optional recruiting / pre-college).

---

## 3) Data coverage and match quality

### Core counts
- Total player-season rows: [ ]
- Seasons covered: [ ]
- Teams covered: [ ]
- Positive outcome rate: [ ]

### Match/mapping quality (from pipeline artifacts)
- College-listed draft rows: [ ]
- School-mapped rows: [ ] ([ ]%)
- Athlete-matched rows: [ ] ([ ]%)
- Unresolved school strings remaining: [ ]

### Risk note
- Any known coverage caveats for this run: [1-2 bullets]

---

## 4) Main empirical results (decision-grade)

### Baseline model
- Pool linear term (`beta2`): [estimate, SE/p-value]
- Pool quadratic term (`beta3`): [estimate, SE/p-value]
- Turning point: [value]
- Turning point CI: [[low], [high]]
- Turning point in observed support? [Yes/No]

### Alternative model
- Pool linear term (`beta2`): [estimate, SE/p-value]
- Pool quadratic term (`beta3`): [estimate, SE/p-value]
- Turning point: [value]
- Turning point CI: [[low], [high]]
- Turning point in observed support? [Yes/No]

---

## 5) Nonparametric/binned evidence

- Bin scheme used (deciles/ventiles): [ ]
- Minimum bin count: [ ]
- Visual shape baseline: [monotone / hump / ambiguous]
- Visual shape alternative: [monotone / hump / ambiguous]
- Tail support adequate? [Yes/No]

*Methodological parallel (optional sentence for talks):* Army competing-risks CIFs bin **pool-minus-mean SNR** and plot **promotion vs attrition** over time; this college run bins **peer pool quality** (`poolq_loo`) and plots **draft** — same **“heterogeneity across quantiles + curvature”** spirit, not the same estimand as full **CIF** unless we add event-time competing outcomes later.

One-line visual read:
- [Example: "Both runs rise from low to mid bins; high bins flatten, with stronger hump in baseline."]

---

## 6) Inverted-U verdict

### Baseline verdict
- [Supportive / Mixed / Not supportive]
- Why: [1-2 lines]

### Alternative verdict
- [Supportive / Mixed / Not supportive]
- Why: [1-2 lines]

### Side-by-side interpretation
- What changed between runs: [ ]
- Which assumption appears to drive differences: [ ]

---

## 7) Advisor-facing interpretation (plain English, 4-6 lines)

Use careful associational language.

Template:
- We find [strength] evidence of an inverted-U relationship between peer-pool quality and advancement under [mapping].
- The nonlinear pattern [persists/weakens/disappears] when we switch to [alternative mapping], suggesting [brief mechanism interpretation].
- The turning point falls [inside/outside] observed support, and binned plots are [consistent/inconsistent] with the parametric result.
- These findings are observational and sensitive to [top 1-2 constraints].

---

## 8) Recommended next action (pick one)

- [ ] Proceed to robustness expansion (new metric/outcome).
- [ ] Do one targeted data cleanup cycle, then rerun.
- [ ] Freeze mapping and draft advisor memo section.
- [ ] Other: [ ]

Rationale (2-3 lines):
- [ ]

---

## 9) Reproducibility log

- Notebook/script path: [ ]
- Input artifact versions: [ ]
- Output files produced: [ ]
- Runtime date/time: [ ]
- Any manual interventions: [ ]
- Decision memo **Datasets** alignment: baseline **spine** + numbered blocks **(1)–(8)** actually used this run: [ e.g. (1)(4)(5)(6)(7) or “spine only”; add **(8)** if recruiting layer used ]

---

## Appendix (optional short insert)

Add one mini table or bullet set only if essential:
- key coefficient table excerpt,
- one support diagnostic,
- one note on unresolved matching edge cases.
