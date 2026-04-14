# VECTOR — full package (browser / no workspace access)

**For Charles:** Upload **this entire file** into Vector’s chat (or paste all of it). Vector does **not** have access to your Cursor project. Optionally **also attach** the two PNG figures (Army final CIF bars Q1–Q8; college mean draft rate by pool bin). If you cannot attach images, Vector can rely on **Section 0** below.

**Task for Vector:** Draft the **email / memo to Brian MacDonald** using **Section 7** outline and all evidence below. Edit for tone; confirm no classified detail on the Army side.

---

## 0. Figure descriptions (if PNGs are not attached)

**Figure A — Army (competing risks, final CIF bars).**  
Eight ordered categories **Q1–Q8** on the x-axis (low to high peer pool quality; pool defined leave-self-out). Y-axis **Final CIF** (~0–0.7): cumulative incidence of **promotion** (event of interest) by end of follow-up, **by bin**. Pattern: low left, **steep rise** through mid bins, **peak** around **Q5–Q6** (~0.71), then **decline** in **Q7–Q8** (Q8 ~0.41). Gradient bar colors light-to-dark blue along bins.

**Figure B — College basketball (draft rate by pool bin).**  
Title along lines of **mean draft rate by ventile/bin of `poolq_loo` (LOO teammate perf)**. X-axis: **8 bins** (1 = lowest leave-one-out teammate pool quality). Y-axis: **Mean Y_draft** (~0–0.018). Pattern: draft rate **rises** from bin 1 through **~bin 7**, then **drops** in **bin 8** — hump-shaped, qualitatively similar to Figure A but **different scale and estimand** (draft incidence on player-seasons, not military promotion CIF).

---

## 1. Army evidence brief (Coda — full text)

### Vector brief: Army evidence package (for Brian MacDonald message & paper)

**Prepared by:** Coda (Army data / `520` thread)  
**Audience:** Vector (drafting external memo) + Charles  
**Use:** Merge with **Scout’s** basketball brief so one coherent note to Yale / ESPN colleague.

#### A. One-sentence bridge

We document a **hump-shaped** relationship between **leave-self-out peer pool quality** and **promotion** in a **rank-ordered internal labor market** (Army), then show a **similar qualitative shape** using **public** college basketball data and **NBA draft** incidence.

#### B. Suggested **second paragraph** draft (Army only — Vector: edit for tone)

*Draft text; confirm numbers with Charles’s final tables.*

In the Army officer data, we study promotion to **Major** (with **attrition** as a competing risk in the full pipeline). Pool quality is constructed so that each officer’s **peer pool mean excludes that officer’s own contribution**—the same **leave-one-out** logic Charles uses verbally as “pool minus mean” (meaning **without** self in the mean). We summarize **promotion** outcomes within **ordered bins** of that pool measure. The **competing-risks** displays include **final promotion incidence** by bin; in the **eight-bin** panel shared with advisors, estimated **final promotion incidence** is **lowest** in the **lowest** pool-quality bins, **rises** through the **middle** of the distribution, and **falls** again in the **highest** pool-quality bins—consistent with **stronger payoffs to pool quality in the middle of the hierarchy** and **diminishing returns** (or **congestion**) when peer pools are extremely strong. Full estimation uses a **time-varying** survival panel and Cox-style modeling elsewhere in the dissertation pipeline; the **bar panel** is a **transparent stratified summary** intended to mirror how we **read** the basketball **draft-rate-by-ventile** figure.

#### C. Interpretation hooks (third paragraph — Army-side angles for Vector)

Vector can blend these with Scout’s basketball interpretation:

1. **Congestion / scarce slots:** At the **top** of the peer-quality distribution, **relative rank** may matter more than **absolute** peer strength; **promotion rates** need not increase monotonically in pool quality.
2. **Signal vs noise:** Very high-quality pools may **compress** observable performance differences, weakening the **signal** of individual accomplishment for boards.
3. **Selection:** Officers sorted into **elite** peer groups may differ on **unobservables**; the figure is **descriptive** at the bin level unless the paper’s models **adjust** further.
4. **Non-transferable literal equality:** Army **final CIF** and college **mean draft rate** are **different estimands**; the claim is **parallel curvature**, not identical magnitudes or causal structure.

#### D. “Anyone else?” (Vector: web / lit check, not Coda’s specialty)

Coda does not maintain a literature database here. **Vector** should run a targeted scan for:

- **Peer effects** and **tournament** / **rank** models in **labor** and **organizations**;
- **Sports** draft prediction and **teammate quality** (NBA combine, college analytics blogs, academic SSRN/RESTUD-style labor);
- **Relative performance** in **internal** labor markets (military, police, firms).

Charles’s Yale contact may know **ESPN-era** analogues (draft models, RPM/BPM contexts) even if academic cites are thin.

#### E. Tenure / academia (forward pointer)

If the **third setting** is tenure: specify **pool** (department peers? field cohort?) and **leave-self-out** construction **before** coding. Army **OER pools** and basketball **rosters** are both **closed teams**; academia’s “team” boundary is **design-critical**.

---

## 2. Cross-team sync — Army thread (Coda — full text)

### Coda → Scout & Vector: Post-replication sync (Army thread)

**From:** Coda (Army / `520` Cox & competing-risks plotting thread with Charles)  
**Purpose:** Align all agents on what the Army side **did** and **showed**, now that Scout has reproduced the **inverted-U** pattern in college basketball.

#### 1. Status

Charles and Scout replicated the **qualitative shape** of the Army finding in a **public, replicable** setting: draft propensity vs **leave-one-out teammate pool quality** in MBB. The parallel is **strategic and interpretive** (nested talent pools, congestion at the top), not a claim that promotion hazards equal draft odds.

#### 2. Army setting

- **Population:** U.S. Army officers after promotion to Captain; time-to-event through promotion to Major, attrition, or censoring (competing risks).
- **Pattern:** Upward mobility vs **peer pool quality** is **nonlinear**: stronger association in the **middle** of the distribution, **lower** estimated promotion incidence at the **highest** pool-quality bins.
- **Figure:** Eight bins **Q1–Q8**; y-axis **final cumulative incidence** of **promotion**; rise through mid bins, drop at top bins.

#### 3. Pool-quality definition (Army)

“Pool minus mean” = **pool mean computed without the officer’s own contribution** (leave-self-out), not “pool minus a fixed cohort mean.” **Own** rating is **not** in **own** pool statistic by construction.

**Implementation:** OER / senior-rater inputs in time-varying survival panel; **`520_pipeline_cox_working.ipynb`**, **`cox_plot_helpers.py`**. Competing-risks **bar panels**: stratify by binned pool; **within bin**, nonparametric summary of promotion incidence (not Cox inside that bar chart).

#### 4. Code map (reference only — Vector does not need files)

`520_pipeline_cox_working.ipynb`, `cox_plot_helpers.py`, `pipeline_config.py` / overrides.

#### 5–8. Scout mirror / Vector memo / handoff archive / tenure pointer

As in original doc: Scout supplies basketball detail; Vector merges; optional third setting = academia / tenure.

---

## 3. Collegiate basketball background (Scout — full text)

### Scout — Collegiate basketball background (for CODA, VECTOR, Brian MacDonald memo)

**Purpose.** Handoff summary of the **530** college-basketball pipeline and **nonparametric bin** evidence mirroring the **inverted-U** pattern from the Army setting, using **public** data.

#### Research question (aligned with Army)

Whether **upward mobility** (here: **NBA draft incidence**) depends on **relative standing within nested talent pools**, with **stronger marginal payoffs in the middle** and **flattening or reversal at the elite tail** — analogous to rank scarcity in a closed military ladder.

#### Outcome and key regressor

- **Outcome:** `Y_draft` — **ever drafted** (binary at player-season; from NBA draft register linked to ESPN `athlete_id`).
- **Peer pool quality:** `poolq_loo` — **leave-one-out mean teammate performance** within **(team_id, collegiate season)**; focal player excluded from the mean.
- **Figure spec:** **`perf` = points per minute (`ppm`)** from ESPN box aggregated to player-season.

#### Data sources

1. ESPN / sportsdataverse-style **game box** → player-season-team panel.  
2. **NBA draft register** + **draft–athlete match** → **`Y_draft`**.  
3. Sports Reference BPM merge **optional**; **not** used for the **PPM** figure described here.

#### Sample and cleaning (basketball plot referenced)

| Choice | Setting |
|--------|--------|
| Collegiate seasons | **2011–2021** |
| Minutes filter | **`min_minutes = 1`** |
| Team draftee restriction | **Off** — `restrict_teams_by_draftees=False` |
| Binning | **`poolq_binning = equal_width`**, **`ventiles = 8`** |
| Winsorization | **`poolq_winsor_quantiles = (0.05, 0.95)`** on `poolq_loo` |

**Scale (typical run):** ~**83k player-seasons**, ~**45k** unique athletes; ~**1.1k** player-seasons with `Y_draft=1`; mean draft rate on sample ~**1.4%** (exact counts in export provenance).

#### Result (visual)

**Mean `Y_draft` by bin of `poolq_loo` (PPM-based LOO):** draft rate **rises** from low through middle–upper bins, **falls in top bin (8)** — **hump-shaped**, consistent with **middle payoffs** and **weaker marginal returns / selection at elite teammate-pool tail**.

#### Reproducibility

**`sports_pipeline/`** + **`530_sports_pipeline.ipynb`**. Exports: dated PNG/CSV/txt under **`exports_dir`**; filename slug encodes metric and binning.

---

## 4. Shared vocabulary (for one coherent memo)

| Term | Meaning |
|------|--------|
| Leave-self-out / “pool minus mean” | Peer mean **excluding self** — **not** own perf in own pool stat. |
| Army y-axis (bars) | **Final CIF** for **promotion** within pool-quality bin. |
| College y-axis (bars) | **Mean `Y_draft`** within `poolq_loo` bin (player-season grain). |
| Claim | **Parallel qualitative shape** (hump / inverted-U tail), not identical institutions or causal IDs. |

---

## 5. Charles’s intro (paste near top of Brian message — Vector may polish)

We’re testing whether upward mobility depends on **relative performance within nested talent pools**, with **stronger payoffs to pool quality in the middle of the hierarchy** and **diminishing returns at the elite tier where slots are scarce**—first in a **closed military promotion market**, then in a **transparent** college-to-pro sports labor market as a **public, replicable** second setting. We’re also exploring whether similar measurement could translate to **academic careers / tenure** after we pressure-test this with you.

---

## 6. Paragraph outline Vector should produce

1. **Paragraph 1 (Army):** Pool definition (leave-self-out), promotion to Major, competing risks context, **Q1–Q8** bar pattern (reference Figure A or Section 0). No classified numbers beyond what Charles approves.
2. **Paragraph 2 (Basketball):** ESPN box + draft register, **ppm**, **poolq_loo**, **2011–2021**, **min_minutes=1**, **no team draftee restriction**, **8 equal-width bins**, **winsor 5–95%**, **N** scale, **hump** with **drop in bin 8** (Figure B / Section 0).
3. **Paragraph 3 (Interpretation + lit):** Congestion / relative rank / signal compression / selection; **different estimands**; brief lit or “we’d love pointers”; invite Brian’s ESPN-analytics perspective. Mention **tenure** as possible third venue.

---

## 7. Deliverable from Vector

**One email-ready message** to **Brian MacDonald** (subject line suggestion optional): intro (Section 5) + three paragraphs (Section 6) + warm close. **Do not** imply Army microdata are shareable. **Do** stress replication with **public** basketball data.

---

*End of Vector browser package. File path on Charles’s machine (for his records only): `current_documents/Vector_Browser_Package_FULL_TEXT.md`*
