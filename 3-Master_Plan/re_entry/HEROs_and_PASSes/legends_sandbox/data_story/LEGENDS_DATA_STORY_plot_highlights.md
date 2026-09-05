# Legends data story — plot highlights (talk track)

**Deck:** `LEGENDS_DATA_STORY_3x3.png` · read **top-left → bottom-right**  
**Reigning HERO lock:** dev cohort · full 2y follow-up · Q16 team LOO · Y = top-tier debut within 2y

Use one sentence per panel when screening a domain; two if Alex asks “why is this here?”

---

## Row 1 — Who is in the pond?

### 1 · Cohort

**Highlight:** Decision universe for **developmental → top-tier** promotion — not already-pro players, not censored stints.

**Say:** “N = 1,879 eligible dev stints, 37% promoted within 2y — peer context is **team LOO** on Alex’s performance index, not league tier alone.”

---

### 2 · Â_i and T̂_j

**Highlight:** Separates **individual talent** from **team-level realized talent** (includes self).

**Say:** “Promoted players sit right-shifted on own index; team talent has its own spread. HERO’s environment axis is **LOO teammates**, not raw team mean.”

---

### 3 · Team LOO distribution (histogram · ECDF)

**Highlight:** Support of the peer-context variable — where LOO teammate quality lives, and whether promoted players come from systematically better ponds.

**Say:** “Left: where LOO mass lives on the index scale. Right: promoted players’ ponds are **stochastically better** — descriptive prerequisite before any binning story.”

**Not:** An outcome curve — input distribution only.

---

## Row 2 — Geometry and who carries promotion mass

### 4 · Outcome mass vs Â (ECDF)

**Highlight:** Where **promotions** come from in ability space — cumulative share of all Y=1 events by own-index tiers.

**Say:** “Most promotion mass concentrates in the upper ability tail — panels 7–8 zoom where the marginal promotion decision actually happens.”

---

### 5 · Team interval overlap

**Highlight:** **Sorting overlap** — how much team talent windows stack on the same roster (assortment geometry).

**Say:** “Rosters aren’t isolated talent bins — intervals overlap. That’s why LOO (remove self) matters more than ‘my team’s average’ alone.”

---

### 6 · Team roster size |T_j|

**Highlight:** **Pond size** — how many rostered teammates define each stint’s LOO pool.

**Say:** “LOO is computed over a real esports roster, not an abstract league average — pond size sets how noisy peer context is.”

---

## Row 3 — Conditional stories (all LOO-axis)

### 7 · CCT — fixed Â z ∈ [1, 2] · Q8 LOO

**Highlight:** **Squid vs Jackal within a matched ability band** — mid-pond vs top-pond LOO bins, holding **own index z ∈ [1, 2]** fixed (scaled Act II gate for thin esports tails).

| Knob | Panel 7 |
|------|---------|
| Who | Fixed z window — own index z ∈ **[1.0, 2.0]** |
| Binning | **Q8** on team LOO *within that band* |
| Question | Among similarly talented dev players, do **mid-LOO** ponds promote **more** than **top-LOO** ponds? (CCT signature) |

**Say:** “Panel 7 is **Act II conditional congestion** on a scaled z slice — classic Squid–Jackal test, not the full HERO curve.”

**Not:** MBB’s z ∈ [2, 3] band — LoL dev cohort is thinner; tenure-style scaling applies.

---

### 8 · Elite pond LOO — top 20% Â · PW5

**Highlight:** **Elite dev players only** — promotion rate vs peer context with piecewise tail binning on LOO.

| Knob | Panel 8 |
|------|---------|
| Who | **Top 20% own index** (pooled percentile cut) |
| Binning | **PW5** on team LOO within elite gate |
| Question | Among elites, does promotion rate **plateau or dip** in the highest-LOO tail? |

**Say:** “Panel 8 is the **elite-pond keeper** — same LOO axis as HERO, but an explicit top-20% Â gate and tail-focused bins.”

---

### 9 · HERO (Pass A · Q16 · LOO) — finale

**Highlight:** **Full-panel environment curve** — promotion rate vs team LOO for everyone passing cohort filters.

**Read (Q16 bins):** ~19% at lowest LOO ventile → monotonic rise → **~57%** at top two ventiles (bins 15–16).

**Say:** “Panel 9 is the **reigning HERO porch** — strong middle rise into elite LOO ponds; panels 7–8 ask *where* in Â-space conditional shapes live.”

---

## 30-second domain screen (Alex)

1. **Population sane?** → 1, 2, 6
2. **Environment variable sane?** → 3
3. **Promotion mass justifies zoom bands?** → 4
4. **Assortment / overlap?** → 5
5. **Act II congestion?** → 7
6. **Elite tail on LOO?** → 8
7. **HERO shape?** → 9

**Verdict strip:** Strong HERO rise (low LOO ~19% → top LOO ~58%); scaled CCT/elite gates for Act II — **promotion-rich** domain (37% Y rate).

---

## Footnotes for honest slides

- **Y = 2y promotion** (not 1y) — more events, still censored on `full_2y_followup`.
- Panels **7–8** use **scaled gates** (z ∈ [1, 2], top 20%) — not MBB top-7% / z ∈ [2, 3] verbatim.
- Panel 9 is **descriptive porch** (Q16 equal-count bins) — not prespecified HERO regression lock.
- Regenerate: `python scripts/big_fish_data_story.py --domain legends --mode all`
