# Grandchild diagnostics — D and H_sort (slide / Alex brief notes)

**Use when interpreting:** `GRANDCHILD_rho_sweep_D_H.png`, `GRANDCHILD_rho_vs_assortativity.png`, interval-overlap slides, HAND17 Grandchild panels.

**Acronym style:** first use in prose = **Full Term (ACR)** — e.g. Sum of Squares (SS), Mean Squared Error (MSE).

**VECTOR lock:** **ρ** = generative ASSIGN homophily knob. **H_sort** = realized sorting on a fixed partition (diagnostic). Score ≠ select; ASSIGN ≠ SCORE.

---

## 1. Within-team Mean Squared Error (MSE) **D**

### What D is measuring

For each player \(i\) on team \(g(i)\):

\[
D = \text{average over players of } \left(\hat{A}_i - \mu_{g(i)}\right)^2
\]

where \(\mu_{g(i)}\) is that team’s **final centroid** (roster mean after ASSIGN).

**Plain question:** *“How far is each player from their own team’s average?”*

### How ρ moves D (2015 sweep, C = 15, J = 402)

| ρ | D (mean, illustrative) |
|---|-------------------------|
| 0.00 | ~0.93 (high — mixed rosters) |
| 1.00 | ~0.68 (lower — tighter rosters) |

- **Low ρ:** players land on teams without much regard to similarity → rosters are mixed → players sit far from team mean → **D high**.
- **High ρ:** similar players cluster → rosters are tight → **D lower**.

**Direction is correct:** high ρ → lower D. The gap 0.93 → 0.68 is real sorting pressure, not failure of the model.

### Why D doesn’t crash to ~0 at ρ = 1

Even at maximum homophily, D stays around **0.68**, not zero. That’s normal:

1. **Roster size C = 15** — each team still has 15 distinct players from a continuous ability distribution; they can’t all be identical.
2. **Sequential ASSIGN** — centroids move as rosters fill; it’s not perfect static binning.
3. **μ is the team mean** — D is variance *around* that mean; sorted groups of 15 still have internal spread.
4. **Abilities are fixed** — ρ only reshuffles the same player pool; it doesn’t clone talents.

### D vs H_sort

| Quantity | Question it answers |
|----------|---------------------|
| **D** | Within-team tightness (how homogeneous is each roster?) |
| **H_sort** | Between-team separation / realized assortativity (how much does team label explain ability?) |

Both respond to ρ in the Grandchild sweep, but they are **different diagnostics**.

---

## 2. **H_sort** in plain words

### Equation

\[
H_{\text{sort}} = 1 - \frac{\sum_i \left(\hat{A}_i - \mu_{g(i)}\right)^2}{\sum_i \left(\hat{A}_i - \bar{A}\right)^2}
\]

### In words

1. **Denominator (bottom):** Total Sum of Squares (SS) — how spread out are all players around the **league average** \(\bar{A}\)? (Total dispersion in the pool.)
2. **Numerator (top):** Within-team Sum of Squares (SS) — how spread out are players around **their own team’s mean** \(\mu_{g(i)}\)? (Within-roster dispersion for the partition you’re evaluating.)
3. **Fraction (within-team SS ÷ total SS):** What share of total “spread” is **within teams**?
4. **H_sort = 1 minus that fraction:** How much of the league’s talent dispersion is **accounted for by team membership** — i.e. how sorted the partition is. (Same object as an explained-variance / Analysis of Variance (ANOVA)-style \(R^2\) on team labels.)

**One-sentence version for Alex:**

> If I tell you which roster a player is on, how much of their deviation from the league average is explained by that roster’s mean? — 0 = none, 1 = completely.

### Reading the endpoints

| H_sort | Plain English |
|--------|----------------|
| **≈ 0** | Teams look like random draws from the pool — knowing your team doesn’t explain much about your ability vs the league average. |
| **≈ 1** | Teams are perfectly separated — everyone on a team is essentially at the same ability (each team is a point mass). |

### ρ sweep (assortativity validation slide)

`GRANDCHILD_rho_vs_assortativity.png` — ρ on x-axis, mean **H_sort** on y-axis (30 reps per ρ, 2015 PPM z).

Illustrative endpoints: \(H_{\text{sort}}(0) \approx 0.07 \to H_{\text{sort}}(1) \approx 0.32\).

**Alex story:** turning up ASSIGN homophily ρ raises **realized assortativity** H_sort on the assigned partition.

**Do not say:** “H_sort is ρ” or “we set assortativity to 0.15.” Say: “At ρ = 0.5, realized H_sort ≈ 0.15 on this assign realization.”

---

## 3. Where H_sort appears in slides (inventory)

| Where | Role |
|-------|------|
| **`slides/auto/CHAR_grandchild_h_sort_explainer_AUTO.pptx`** | **Dedicated H_sort definition** (glossary reference — start here for Alex) |
| **`slides/auto/CHAR_grandchild_rho_assortativity_AUTO.pptx`** | ρ vs H_sort validation plot + bullets |
| Interval overlap AUTO slides (empirical + Grandchild) | Formula bullet + numeric readout on each partition |
| **`GRANDCHILD_D_and_H_sort_interpretation.md`** | Full memo (this file) |
| HAND17 slide 1 glossary | **ρ** as “assignment assortativity” — does **not** define H_sort |

There was no standalone H_sort explainer before the AUTO glossary slide above; other decks only report H_sort in passing.

---

## 4. Is H_sort a good assortativity measure for teams?

### For this project: yes — with precise wording

**H_sort** is an **explained-variance** index on a **fixed roster partition** (same object as **H** in the Grandchild spec):

\[
H_{\text{sort}} = 1 - \frac{\text{within-team Sum of Squares (SS)}}{\text{total Sum of Squares (SS) around } \bar{A}}
\]

**Question it answers:** *How much of ability dispersion is accounted for by team labels?*

| H_sort | Meaning |
|--------|---------|
| **≈ 0** | Team membership tells you little (random-like mixing) |
| **≈ 1** | Teams are perfectly separated in ability |

That is the right **outcome** measure to pair with generative homophily **ρ** (preference ≠ realized assortativity; Quayle / Alex).

### Why it works here

1. **VECTOR lock** — ρ is the ASSIGN knob; H_sort is measured **after** assign on that partition.
2. **Mechanism validation** — ρ sweep: H_sort rises monotonically (≈ 0.07 at ρ = 0 → ≈ 0.32 at ρ = 1 on 2015 Grandchild league).
3. **Same player pool** — Compare NCAA vs Grandchild partitions on fixed \(\hat{A}_i\).
4. **Bounded [0, 1]** — Easy on slides and in conversation.

### Caveats (say aloud to Alex)

1. **Not Newman’s network assortativity coefficient** \(r\) — partition explained variance on abilities, not a graph degree–degree correlation.
2. **Partition-dependent** — NCAA team-seasons vs Grandchild J = N/C (402 vs 635 in 2015); compare **trends** and **overlap** diagnostics, not raw levels alone.
3. **Roster size** — With C = 15, even ρ = 1 will not push H_sort near 1.
4. **Complements interval overlap** — Overlap = geometry of talent windows; H_sort = how much labels explain spread. Use both.

### Bottom line for Alex

> **H_sort is our realized assortativity index on rosters** — “how sorted is this partition?” It is the right outcome to pair with generative **ρ**, not a substitute for it.

---

## Roster size & the 20-minute floor (Alex brief — Aug 2026)

**Why NCAA team counts ≠ LG team counts on the same player pool**

| | NCAA (empirical) | LG sim |
|--|----------------|--------|
| Team definition | Real `(team_id, season)` | Synthetic league: **J = N ÷ 15** |
| Players per team | **Mean ~9.6** after ≥20-min filter (median 11; max 19) | **Fixed 15** |
| Team-seasons (2011–2021) | **6,492** | **4,140** |

The analysis panel keeps only player-seasons with **≥20 total ESPN box minutes** (`min_minutes=20`). That is applied **before LOO** when we rebuild from box (`use_prebuilt_panel_csv=False`). It is **not** a filter on ppm — it drops low-minute rows from both the outcome sample and the teammate pool.

**Why 20?** Early exports used **`min_minutes=0`** (~83k rows). Jul 2026 sensitivities showed: **`0`** adds ~21k almost-never-drafted bench rows and **washes/noise** the hero inverted-U; **`20`** gives rotation-level LOO and the cleanest top-ventile dip with **no meaningful loss of drafted players** (+2 rows vs 0). Hero lock: see `Pertinent_Thoughts_Scout.md` § `min_minutes` Floor.

**Inverted-U with full rosters?** **`min_minutes=0`**: pattern **attenuates** — wobbly ventiles, elite dip harder to read; not a falsification. **`min_minutes=10`**: dip **robust**, presentation noisier. We do **not** plan to simulate a minutes distribution in LG — that would overfit listing quirks and confuse ASSIGN with playing-time allocation.

**Slide / figure:** `GRANDCHILD_ncaa_vs_lg_roster_size_compare_2011_2021.png` · AUTO: `slides/auto/CHAR_grandchild_ncaa_roster_size_compare_AUTO.pptx` · companion NCAA-only: `GRANDCHILD_ncaa_roster_size_distribution_2011_2021.png`

**Alex line:**

> “Real teams in our panel average ~10 rotation players; LG repacks the same abilities into 15-man synthetic leagues — so team-season *n* differs even when L_C distributions match. The minutes floor is part of what we mean by ‘roster,’ not a neutral trim.”

---

## Related paths

| Item | Path |
|------|------|
| **H_sort glossary AUTO slide** | `slides/auto/CHAR_grandchild_h_sort_explainer_AUTO.pptx` |
| ρ sweep figures | `grandchild_assign/GRANDCHILD_rho_*.png` |
| ρ assortativity AUTO slide | `slides/auto/CHAR_grandchild_rho_assortativity_AUTO.pptx` |
| Method note | `sports/documents/541_grandchild_homophily_assign_README.md` |
| Regenerate H_sort explainer | `python sports/scripts/build_grandchild_h_sort_explainer_slide.py` |
| Regenerate ρ vs H_sort slide | `python sports/scripts/build_grandchild_rho_assortativity_slide.py` |
