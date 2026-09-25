# Men’s basketball assortativity — why empirical sorting looks near zero

**Prepared:** September 25, 2026  
**Author lane:** COMPASS (scientific framing; not a pipeline audit)  
**Trigger:** Charles debrief after long conversation with Alex — pause assortativity sensitivity grid until pool composition and performance metric are re-examined.

**Standalone:** This memo states the scientific worry, separates “real world” sorting from measured **H_sort**, lists confounders tied to points-per-minute and roster construction, and proposes a ordered diagnostic menu. It does **not** authorize new runs.

**Same folder (read separately — not merged here):** [SCOUT evidence note](20260925_MBB_Assort_issue_thoughts_SCOUT.md) · [VECTOR scientific note](20260925_MBB_Assort_issue_thoughts_VECTOR.md). Section **11** below adds COMPASS-only reactions after reading those two.

---

## 1. The core intuition (and why it is reasonable)

**Common-sense claim:** Division I men’s basketball is not a league of random talent placement. A roster like Duke or UConn is not a flat mix of mediocre and elite players in the way a naïve “no sorting” story would suggest. Most players who **earn meaningful minutes** on those teams are **very good** relative to the national pool.

**Empirical readout today:** On the locked hero panel (minimum twenty season minutes, eleven captured games per team-season, within-season points-per-minute z-score, leave-one-out teammate quality), realized sorting index **H_sort** is **small** (bracket calibrations often find homophily parameter **ρ ≈ 0** matches empirical **H_sort**). That can sound like “basketball has no assortativity,” which conflicts with common sense.

**COMPASS read:** The conflict is usually **not** “NCAA is actually random.” It is **“our measured partition + ability coordinate + peer definition compress sorting into a statistic that looks like zero.”** That is a **measurement and pool-definition** problem before it is a “reject homophily in the model” problem.

---

## 2. Two boundary conditions that dominate the basketball story

Alex and Charles named two scarce-resource limits that Army does not share in the same form:

| Boundary | Basketball | Why it matters for us |
|----------|------------|------------------------|
| **Scarce selection** | Draft rate **K/N ≈ 1%** | Hero curve is estimated on a **tiny** positive class; tail behavior is noisy; small denominator moves look like “no assortativity effect.” |
| **Scarce on-court slots** | **Five** players at a time | **Congestion** for “who gets seen / who gets the ball / who gets the stat line” is about **rotation and minutes**, not “fifteen names on a roster sheet.” |

The second point is the new emphasis from today’s conversation. Our generative story speaks about **peer pools** and **congestion in the score**, but much of the empirical panel still defines peer context from **season-long roster aggregates** (leave-one-out mean teammate points-per-minute z-score over everyone who clears season filters).

**Mismatch in one sentence:** We are modeling **congestion as if the relevant peer group is the full listed roster**, while the **sport’s scarce interaction slot is five players on the floor.**

That mismatch does not prove assortativity is high; it explains why **congestion measured through full-roster, rate-based points per minute** may **understate** the strategic peer pressure draft-relevant players actually felt.

---

## 3. How points-per-minute helps — and how it confounds sorting and congestion

### 3.1 Why points per minute was attractive

Total season points confounds **talent** with **opportunity** (seniority, rotation trust, injury, blowouts). Points per minute asks: **“What did you produce per unit of playing time?”** That aligns with “talent should not be proxied by minutes alone.”

### 3.2 How points per minute interacts with sorting index **H_sort**

Ability on the main panel is **within-season z-scored points per minute** across **all retained player-seasons** in that year (after filters). That construction:

1. **Forces a single national spread** each season — everyone is expressed relative to the same cross-section.
2. **Preserves substantial individual dispersion** — histograms of **Â_i** are wide, not collapsed.
3. **Does not guarantee large between-team dispersion** in team means **T̂_j** or in leave-one-out pool quality — those depend on **who is averaged together** on each roster.

Charles’s “huge bands of talent at all levels” is **true at the player level** in z-space. Assortativity in our index is **not** “are players different?” It is **“do team labels explain much of that player-level variance?”** A league can have wide player dispersion and still show **low H_sort** if rosters are **similarly wide** team-to-team (each team has stars, rotation, and bench noise in comparable proportions).

**Elite programs in z-space:** A “good” player at a mid-major and a “good” player at a blueblood can sit **not far apart** in within-season z after filtering to rotation players — both are above average producers in their contexts, but z-scoring **pools contexts** for **interpretation and hero bins**. Team **means** move, but not necessarily enough to push **H_sort** toward Army-like values without stronger peer definitions.

**Correction (after VECTOR / SCOUT):** Within a season, **within-season z-scoring is an affine transform** of raw points per minute — it **does not by itself raise or lower H_sort** (numerator and denominator of the sorting index scale together). What moves **H_sort** is **who is retained**, **raw rate construction**, and **team assignment**, not the z step alone. Earlier prose here that sounded like “z hides tier → low H_sort” was **imprecise**; z matters for **comparability language and leave-one-out hero**, not for the sorting-index algebra.

### 3.3 How points per minute torpedoes the **congestion** narrative (mechanism, not data bug)

**Congestion** in the score is meant to capture **crowding among viable peers** for a scarce outcome (draft attention, role, touches). Points per minute:

- **Rewards efficiency in low minutes** — a player who scores in a short stint can look **deceptively strong** per minute.
- **Is extremely noisy at low minutes** — denominators make rates unstable; zero-point games create literal zeros.
- **Is partly an outcome of role and lineup** — who you share the floor with affects shots, not just “who you are.”

So points per minute is doing **double duty**: it is both **ability input** and a **shadow of on-court opportunity structure**. When bench players with **few minutes per game** remain in the **peer denominator**, they inflate roster size without representing **on-court competition** for the five simultaneous slots.

Charles’s instinct — **“I don’t trust points per minute for guys who don’t play more than five minutes in a game”** — targets exactly that: **wrong peers + wrong signal**, not merely “outliers.”

---

## 4. What the hero tail still shows (and what it does not)

On the **post–box-quality-control** panel, the **elite right-tail dip** in draft rate is **much weaker** than Army’s, and under some specs it **disappears** as a concave quadratic (flat top ventiles). That pattern fed the worry: **“Maybe assortativity does not matter in the model.”**

**Separate two claims:**

| Claim | Evidence status |
|-------|-----------------|
| **Peer context matters for draft odds** (middle rise in hero bins) | Still supported on defended panel |
| **Elite-bin downturn is robust** | **Not** supported on post-QC leave-one-out axis — much of July dip was contamination |
| **Low H_sort means no real sorting in nature** | **Does not follow** — index is partition- and metric-dependent |
| **Low calibrated ρ means Levine–Gates cannot sort** | **Does not follow** — bracket matches **realized H_sort**, not “true homophily in the world” |

The hero and **H_sort** answer **different questions**. You can have a **hero shape** that responds to leave-one-out pool quality while **H_sort** on the same abilities and rosters stays small because **team labels explain little variance** in the chosen coordinate.

---

## 5. Why we might not “see” assortativity empirically — candidate explanations

Ordered from **most aligned with today’s conversation** to **worth testing but secondary**.

### A. Peer pool definition (full roster vs rotation vs on-court unit)

- **Current default:** Leave-one-out mean teammate **perf** over roster members on `(team_id, season)` after season filters.
- **Structural issue:** Fifteen-man roster ≠ five on-court congestion; walk-on and deep-bench minutes dilute or distort means.
- **Charles direction:** Exclude or down-weight players below **five minutes per game** (or similar) from **peer context**, not necessarily from the focal sample — mirror Army “drop zero–top-block peers from pool mean.”

### B. Performance metric (points per minute and its z-score)

- Rate metric + short minutes → unstable **Â_i** and polluted teammate means.
- Alternatives (box plus, offensive rating, minutes as separate channel) were explored; **points per minute won the hero shape gate** for the **old** peer definition — not necessarily for a **rotation-restricted** pool.

### C. Individual season minutes floor (twenty total minutes)

- **Production lock:** drop player-seasons with **< 20** total season minutes.
- **Effect:** Removes many non-rotation rows from **both** focal set and peers (when rebuild path is used).
- **Does not fix:** Per-game floor; stars’ peers can still include low-minute-per-game bench players who cleared twenty **season** minutes.

### D. Team captured-games filter (eleven games)

- Removes fragmentary one-game opponents; **does not** enforce Division I membership or full schedule completeness.
- **Weak teams with partial schedules** were part of the **T̂_j inflation** worry in the VECTOR history review.

### E. Population scope (all teams vs Division I vs draft-producing programs)

| Restriction | Intent | Risk |
|-------------|--------|------|
| **All retained teams (ALLT hero)** | General NCAA estimand | Mixes tiers; z-scores absorb tier in one national scale |
| **Division I only** | Cleaner comparability | Needs defensible membership rule in extract |
| **Teams with ever-drafted player (+DFT)** | “Places that produce pros” | **Selection on outcome**; assortativity and hero both shift — fine as **sensitivity**, dangerous as **only** estimand |
| **Power conferences / tiers** | Explicit stratification | Smaller N; different scientific claim |

**COMPASS view:** “Draft-ever teams only” is a **reasonable sensitivity** for the Squid-vs-Jackals story (comparable ambition environments), **not** a substitute for fixing peer definition on the main panel.

### F. Within-season standardization itself

- Z-scoring **within season** changes **units and verbal comparability**, not **H_sort** on a fixed retained sample (see §3.2 correction).
- Common-sense “everyone on Duke is good” is about **latent talent / recruiting tier**; points-per-minute z is **observed scoring rate** — defenders and role players need not rank “elite” on that scalar even when they are elite basketball players.

### G. Leave-one-out vs team mean axis

- Hero bins on **poolq_loo**; **T̂_j** diagnostics can look more separated than leave-one-out suggests.
- Sorting index can differ if computed on partitions that emphasize **team means** vs **teammate exclusion**.

---

## 6. Direct answers to Charles’s “what are we missing?” list

| Question | Short answer |
|----------|------------|
| **Should there be talent assortativity in men’s Division I basketball?** | **Yes in the real institution** — recruiting, scholarships, and role allocation sort talent. **Not necessarily high in our H_sort** on this panel. |
| **Is it the performance metric?** | **Partly.** Points per minute conflates rate talent with role and low-minute noise; it fights the congestion story when peers include non-competitors. |
| **Is it the twenty-minute season filter?** | **Partly.** It helps but is **coarse**; it does not encode **five on court** or **per-game rotation**. |
| **Is it the team games filter?** | **Partly for fragmentary opponents**, not for the Duke-vs-mid-major logic. |
| **Division I only?** | **Worth a labeled sensitivity** if membership is definable in data. |
| **Draft-ever teams only?** | **Worth a sensitivity**, not the sole fix; conditions on the outcome ecosystem. |
| **Are we missing assortativity, or mis-measuring pools?** | **Prioritize mis-measured pools and peer sets** before concluding ρ = 0 is “truth.” |

---

## 7. Proposed “one more thing” before assortativity sensitivity grid

This aligns with what Charles told Alex — **re-look pool composition** driven by **metric + filters**, not another ρ sweep on the same panel.

### 7.1 Scientific hypotheses to test (document only)

1. **Rotation peer hypothesis (hero / congestion axis):** Leave-one-out pool quality recomputed over **rotation-eligible teammates only** can **move the empirical draft curve** and change **interpreted congestion** even when focal **Â_i** is fixed — **without changing H_sort** (VECTOR distinction).
2. **Sample / metric hypothesis (H_sort):** **H_sort** and bracket **ρ*** change only if the **retained athlete set**, **raw points-per-minute definition**, or **team labels** change — e.g. drop unstable low-minute players from the panel, or redefine rate with a minutes floor in the denominator. Direction **not guaranteed** to rise.
3. **On-court congestion hypothesis (generative):** Team **L_C** in the Levine–Gates score uses **full eligible roster** in planned assort runs; a rotation-restricted empirical peer average is **not** interchangeable without declaring a **different generative model** (VECTOR construction spec).
4. **Rate vs level hypothesis:** A second performance construct (not a silent swap for points per minute) may show higher between-team dispersion — each measure needs its own missingness audit.
5. **Tier stratification hypothesis:** **H_sort** may read higher **within** conference or draft-producing subsets — separate estimand, not a fix for the national panel.
6. **Null benchmark hypothesis:** **H_sort ≈ 0.06** is not self-interpreting; compare to **exchangeable random team assignment** expectation **(J−1)/(N−1)** on the **same** N, J, and ability vector (VECTOR; not yet run on the freeze population).

### 7.2 Ordered diagnostic menu (for SCOUT / VECTOR when Charles authorizes runs)

**VECTOR’s bounded first step (COMPASS agrees this should precede a long menu):** one **2015 rotation audit** — minutes, appearances with positive minutes, minutes per appearance; share of peer pool below a provisional five-minute-per-game rule; **same focal players**, leave-one-out with vs without low-minute teammates in the peer mean only. **Gate:** settle [initial execution stop](../source_review/ASSORT_20260925_initial_execution_stop.md) (points-with-missing-minutes, canonical team) before calling results final.

**Broader menu (after audit, if warranted):**

1. **Describe** peer dilution — define **denominator** for any “per game” rule (games with positive minutes vs all captured games).
2. **Recompute leave-one-out only** under peer exclusions — **hold focal Â_i and team assignment fixed**; report hero ventiles.
3. **If sample or PPM definition changes:** recompute **H_sort**, permutation null, and **ρ** bracket on the **new** population — do not expect step 2 alone to move **H_sort**.
4. **Optional labeled subsets:** season-specific Division I membership crosswalk; draft-ever teams — sensitivity only.
5. **Do not** subset or threshold-hunt to **recover** a preferred inverted-U (VECTOR warning; COMPASS agrees).

### 7.3 What not to do

- Do **not** treat **ρ ≈ 0** on the current panel as proof that homophily is absent in college basketball.
- Do **not** drop assortativity from the model **until** peer pool and metric sensitivity is documented.
- Do **not** conflate fixing the hero tail with restoring **low** elite-bin draft rates from pre-QC contamination.

---

## 8. Squid team vs Jackals team (framing for the paper)

Charles’s Squid / Jackals metaphor is **about tier and opportunity**, not literal team names:

- **Same human capital type** (good-to-elite player) can face **different congestion** on a **contending roster** vs a **mid-tier roster**.
- Points-per-minute z-scores **partially equate** those players across institutions, which helps comparability but **blurs** the institutional sorting story **H_sort** is supposed to detect.
- The empirical hero asks about **leave-one-out teammate quality vs draft**, which **does** speak to Squid-vs-Jackals **conditional on making the panel** — but only if **teammates in the average are the ones who actually shared rotation and opportunity.**

**One sentence that summarizes the research pivot:** *We are not abandoning assortativity; we are testing whether near-zero **H_sort** is an artifact of full-roster, rate-based peers in a five-on-court sport.*

---

## 9. Related repo documents

| Topic | Path |
|-------|------|
| POST-QC hero vs pre-QC tail | `3-Master_Plan/re_entry/HEROs_and_PASSes/PD20_22_campaign_big_picture.md` |
| Data hygiene history (SCOUT) | `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260925_SCOUT_response_data_hygiene_and_model_history.md` |
| Campaign framing (COMPASS) | `.../ASSORT_20260925_COMPASS_addendum_data_hygiene_and_model_history.md` |
| Assign / score / select reference | `3-Master_Plan/re_entry/LG_model_desk_reference.md` |
| Reigning hero lock spec | `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/README.md` |
| Binding: score ≠ select | `3-Master_Plan/BINDING_Selection_is_its_own_step.md` |

---

## 10. Suggested next step for Charles

1. **Socialize** this framing with Alex — confirm the **one-more-thing** is **peer-pool / per-game minutes**, not another global ρ sweep.
2. **Authorize SCOUT** (when ready) to implement **leave-one-out recomputation with peer eligibility rules** as a **sensitivity branch**, with provenance JSON mirroring Pass A sensitivity discipline.
3. **Freeze** assortativity investigation population **after** that branch, not before.

---

## 11. Additions after reading SCOUT and VECTOR (same day)

These are **COMPASS-only** reactions — not a merged consensus document.

### 11.1 Separate estimands (borrowed clarity from SCOUT)

| Object | One-line question |
|--------|-------------------|
| Empirical **H_sort** | Do team labels explain much of **Â_i** variance on real rosters? |
| Calibrated **ρ*** | What assign homophily matches that partition? (On post-QC panel, **ρ* often hits the ρ=0 boundary** because empirical **H_sort** can sit **below** the sim mean at ρ=0 — **nearest boundary**, not “exact random match.”) |
| Assort experiment | Does **ρ** or **λ** move **top-K winners** at fixed roster? |
| Hero | Draft rate vs **poolq_loo** — outcome layer; not **H_sort** |

Low **ρ*** is **not** the same claim as “basketball has no recruiting sort in the real world.”

### 11.2 Five on court — refine, do not caricature (VECTOR)

- **More than five** players rotate over a season; **position and role** split competition for minutes and shots.
- Teammates on court can **help** scoring, not only crowd it — congestion is not “count bodies ≥ five.”
- Low minutes per appearance may reflect **selection** (depth burying a good player on a great team), not automatic “non-competitor.” COMPASS still favors **reliability** and **peer-definition** probes; VECTOR warns against moralizing the cutoff.

### 11.3 Saved magnitude anchor (SCOUT)

Post–box-QC, **H_sort ~ 0.06–0.07** on defended panels is **weak sorting**, not literally zero. Pre–QC **2015 ≈ 0.114** in an **Aug 14** bracket file is **not** the same population as today’s **≥11 games** panel (**≈ 0.061** in Aug 19 trace). Do not mix when telling the story.

### 11.4 Points per minute ≠ latent “Duke is all good” (VECTOR)

Elite programs may recruit stronger **latent** talent while **observed scoring rate** stays a narrow, role-sensitive outcome. Small **H_sort** on points-per-minute z **does not falsify** Charles’s institutional intuition — it bounds what that **measure** says about **between-team dispersion**.

### 11.5 Where COMPASS still pushes beyond VECTOR’s minimal audit

- **Align generative congestion with sport structure** remains a **model-design** thread for after the descriptive audit — not something the hero-only leave-one-out tweak resolves.
- **Army-style peer exclusion** (drop non-competitors from pool **mean** only) is still a useful **analogy** for rotation-restricted **leave-one-out**, even though it does not touch **H_sort** by itself.

---

*COMPASS scientific memo — no execution authorized. Last content pass: 2026-09-25 (post SCOUT / VECTOR read).*
