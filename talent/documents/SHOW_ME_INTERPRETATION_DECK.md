# Show Me: Prestige and Pool Effects
Advisor‑ready summary deck (8–12 slides)

---

## 1. Research question and framing
- Do **prestige assignments** and **senior‑rater pool context** change promotion outcomes?
- "Big fish / strong pond" framing for both **prestige** and **pool** effects
- Population: YGs 2002–2011 (with targeted branch filters)

---

## 2. Methods (one slide)
- Cox proportional hazards with time‑varying covariates
- Key metrics are **z‑scored** for comparability
- Interpretation uses **hazard ratios** (relative promotion risk)

---

## 3. Part 1 — Prestige story overview
- Focus: prestige exposure + cumulative TB ratio
- Runs used:
  - **Run 8**: no SF/Aviation (regular officers)
  - **Run 9**: IN/AR/FA only (combat arms)
  - **Run 4**: YGs 2002–2006 (cohort robustness)

---

## 4. Run 8 (regular officers): key findings
- `z_cum_tb_rcvd_ratio_snr` dominates promotion signal
- `z_prestige_mean` positive but modest
- **Negative interaction** → diminishing returns at high prestige + high TB
- Coefficients: 0.3235, 0.0783, **−0.0159** (interaction)

![Run 8 interaction surface](/Users/charleslevine/.cursor/projects/Users-charleslevine-Library-CloudStorage-Dropbox-1-Documents-00-Dissertation-0-Next-Chapter-Code-and-Data-New-SQL-and-PY-Code-Cursor-Workspace-PDE/assets/image-02acbd44-a431-445a-9fa3-b1c2145e5e90.png)

---

## 5. Run 9 (combat arms): contrast
- TB ratio even more dominant
- Prestige effect smaller
- **Interaction flips slightly positive** → near‑additive effects
- Coefficients: 0.3437, 0.0588, **+0.00815** (interaction)

![Run 9 interaction surface](/Users/charleslevine/.cursor/projects/Users-charleslevine-Library-CloudStorage-Dropbox-1-Documents-00-Dissertation-0-Next-Chapter-Code-and-Data-New-SQL-and-PY-Code-Cursor-Workspace-PDE/assets/image-588e3344-6ff1-42a7-8870-09a362f7d759.png)

---

## 6. Run 8 vs Run 9 (prestige takeaway)
- Both: TB ratio is the strongest driver
- Run 8: **dampening interaction** (strong‑pond effect)
- Run 9: **near‑additive** (minimal dampening)
- Interpretation: prestige effect depends on context and branch mix

![Run 8 contour](/Users/charleslevine/.cursor/projects/Users-charleslevine-Library-CloudStorage-Dropbox-1-Documents-00-Dissertation-0-Next-Chapter-Code-and-Data-New-SQL-and-PY-Code-Cursor-Workspace-PDE/assets/image-9e6c796c-7abe-4fb5-a41b-667b66f998b7.png)
![Run 9 contour](/Users/charleslevine/.cursor/projects/Users-charleslevine-Library-CloudStorage-Dropbox-1-Documents-00-Dissertation-0-Next-Chapter-Code-and-Data-New-SQL-and-PY-Code-Cursor-Workspace-PDE/assets/image-fc44100f-e596-4cbb-af18-9f34f865766d.png)

---

## 7. Run 4 (cohort robustness)
- YGs 2002–2006 only
- **Stronger negative interaction** than Run 8
- Suggests dampening effect persists and may be stronger in earlier cohorts
- Coefficients: 0.2022, 0.0867, **−0.0293**

---

## 8. Part 2 — Pool story overview
- Two runs needed to handle collinearity in individual TB metrics
- Run 1: **absolute TB vs pool TB**
- Run 2: **rank‑normalized TB vs pool TB**

---

## 9. Run 1 (absolute TB vs pool TB)
- Both main effects positive
- **Positive interaction** → strong pools amplify individual TB
- Pool TB mean is the larger main effect
- Coefficients: 0.2455, 0.3596, **+0.1079**

---

## 10. Run 2 (rank‑normalized TB vs pool TB)
- Both main effects positive
- Interaction ~0 → near‑additive
- Pool TB mean still dominant
- Coefficients: 0.3620, 0.5123, **+0.00335**

---

## 11. Pool story takeaway
- Pool strength matters across definitions of performance
- Interaction depends on how "individual TB" is measured
- Strong‑pool amplification appears when using **absolute TB**

---

## 12. Bottom line (advisor summary)
- **Prestige effects are real but modest**
- **TB ratio is the strongest driver**
- Interaction sign flips by cohort/branch context
- Pool strength consistently matters; amplification appears in some definitions
