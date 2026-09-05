# Football data story — plot highlights (talk track)

**Deck:** `FOOTBALL_DATA_STORY_3x3.png` · read **top-left → bottom-right**  
**Reigning HERO lock:** FBS eligible cohort · Q16 team LOO · Y = drafted next NFL draft

Use one sentence per panel when screening a domain; two if Alex asks “why is this here?”

---

## Row 1 — Who is in the pond?

### 1 · Cohort

**Highlight:** Decision universe for **college → NFL draft** — eligible player-seasons with team LOO and own performance index.

**Say:** “N = 70,633 eligible player-seasons, 2.7% drafted — **sparse Y** domain; descriptive porch still tells us if peer ponds sort draftees.”

---

### 2 · Â_i and T̂_j

**Highlight:** Separates **individual talent** from **team-level realized talent** (includes self).

**Say:** “Drafted players sit right-shifted on own index; team talent has its own spread. HERO’s environment axis is **LOO teammates**, not raw team mean.”

---

### 3 · Team LOO distribution (histogram · ECDF)

**Highlight:** Support of the peer-context variable — where LOO teammate quality lives, and whether drafted players come from systematically different ponds.

**Say:** “Left: where LOO mass lives. Right: drafted players’ ponds vs full panel — check for a **left-shift** (better peer context) before any rate story.”

**Not:** An outcome curve — input distribution only.

---

## Row 2 — Geometry and who carries draft mass

### 4 · Outcome mass vs Â (ECDF)

**Highlight:** Where **draft picks** come from in ability space — cumulative share of all Y=1 events by own-index tiers.

**Say:** “Draft mass concentrates in the upper ability tail — panels 7–8 zoom where marginal draft probability lives, not the whole roster.”

---

### 5 · Team interval overlap

**Highlight:** **Sorting overlap** — how much team talent windows stack on the same roster.

**Say:** “FBS rosters aren’t isolated talent bins — intervals overlap. LOO removes self from the peer pond that defines environment.”

---

### 6 · Team roster size |T_j|

**Highlight:** **Pond size** — how many rostered teammates define each season’s LOO pool.

**Say:** “LOO is computed over a real football roster — pond size sets how peer context is measured.”

---

## Row 3 — Conditional stories (all LOO-axis)

### 7 · CCT — fixed Â z ∈ [1, 2] · Q8 LOO

**Highlight:** **Squid vs Jackal within a matched ability band** — exploratory at 2.7% base draft rate.

| Knob | Panel 7 |
|------|---------|
| Who | Fixed z window — own index z ∈ **[1.0, 2.0]** |
| Binning | **Q8** on team LOO *within that band* |
| Question | Among similarly talented players, do **mid-LOO** ponds draft **more** than **top-LOO** ponds? |

**Say:** “Panel 7 is **scaled Act II** — treat as **exploratory**; bin rates are noisy at ~3% or below.”

---

### 8 · Elite pond LOO — top 20% Â · PW5

**Highlight:** **Elite players only** — draft rate vs peer context with piecewise tail binning.

| Knob | Panel 8 |
|------|---------|
| Who | **Top 20% own index** |
| Binning | **PW5** on team LOO within elite gate |
| Question | Among elites, any **tail dip** at extreme high LOO? |

**Say:** “Panel 8 is the elite-pond keeper — same LOO axis, wider Â gate than panel 7; read cautiously given sparse Y.”

---

### 9 · HERO (Pass A · Q16 · LOO) — finale

**Highlight:** **Full-panel environment curve** — draft rate vs team LOO for eligible cohort.

**Read (Q16 bins):** ~1.2% at lowest LOO ventile → gradual rise → peak ~**3.7%** (bins 12, 16) vs 2.7% overall — modest monotonic lift, not MBB-scale separation.

**Say:** “Panel 9 is the **reigning HERO porch** — environment sorts draftees weakly upward; **sparse Y** limits sharp Act II signatures.”

---

## 30-second domain screen (Alex)

1. **Population sane?** → 1, 2, 6
2. **Environment variable sane?** → 3
3. **Draft mass justifies zoom bands?** → 4
4. **Assortment / overlap?** → 5
5. **Act II congestion?** → 7 (exploratory)
6. **Elite tail on LOO?** → 8 (exploratory)
7. **HERO shape?** → 9

**Verdict strip:** HERO shows **modest LOO gradient** (~1% → ~4% across ventiles); Act II panels **exploratory** at 2.7% draft rate — strong advancement gate, thin event counts per bin.

---

## Perf metric story (`FOOTBALL_PERF_METRIC_STORY.png`)

Six HERO rows (one metric each × Q16 + EW16): Alex **volume** · **efficiency** · DIY **recruit rating** · **PPA total** · **usage** · **Â composite**. Peer X = team LOO on the same metric; Y = drafted next NFL draft.

| Row | Metric | One-line gloss |
|-----|--------|----------------|
| 1 | `z_performance_volume` | Alex volume z (box-score production scale). |
| 2 | `z_performance_efficiency` | Alex efficiency z (rate / per-opportunity quality). |
| 3 | `z_diy_recruit_rating` | Recruit rating z (prior · DIY · position_group × season). |
| 4 | `z_diy_ppa_total_all` | CFBD **predicted points added** total z — season value added (skill positions). |
| 5 | `z_diy_usage_overall` | CFBD **offensive usage share** — fraction of team offensive play volume involving this player (**opportunity / role**, not efficiency; not NBA usage rate). Raw `usage_overall` ∈ [0, 1]; 1% winsorize → z within **position_group × season**. Populated mainly for QB / RB_FB / WR_TE (~16% of panel). |
| 6 | `own_performance_index` | Reigning **Â composite** (same as 3×3 deck). |

**Say (row 5 · usage):** “Usage is CFBD’s **touch / involvement share** — how much of the offense runs through him — separate from whether those touches were *good* (PPA) or how Alex scores volume vs efficiency.”

### Usage row — $\hat{T}_j$ vs LOO (congestion punchline)

**Companion figure:** `perf_story/FOOTBALL_usage_Tj_q16_ew16.png` — same usage $z$, but X = **team mean** $\hat{T}_j$ (includes self), not teammate LOO. Sample: skill-pos rows with CFBD usage ($N \approx 11{,}206$, ~7.2% drafted).

| Axis | Question | Q16 draft rate (low → high ventile) | Read |
|------|----------|-------------------------------------|------|
| **$\hat{T}_j$** (team avg usage $z$) | How concentrated is touch share on this offense? | ~**9%** → ~**7%** | **Flat** — team-level usage distribution barely sorts draftees. |
| **LOO** (row 5 · excl. self) | Who else on *my* pond eats touches? | ~**16%** → ~**4%** | **Steep** — congestion in your peer usage pond matters (~4× across ventiles). |

**Highlight:** Team offensive “star vs spread” style doesn’t move draft odds much once you’re in the usage slice. **Who you share targets with** (LOO) paints a completely different porch — literal **role congestion**, not abstract peer talent.

**Say:** “Team usage distribution doesn’t predict draft; **who you share touches with** does — that’s why we LOO, not $\hat{T}_j$.”

**Contrast rows 4 vs 5:** PPA total LOO slopes **up** (better peer production helps); usage LOO slopes **down** (shared touches hurt). Same deck, different peer definition — usage LOO is a **congestion probe**, not a talent-peer axis.

**Not:** Causal claim — descriptive porch only. Own usage still confounds part of the LOO gradient (stars have high own usage *and* low teammate usage LOO); the $\hat{T}_j$ flatline vs LOO steepness is the HERO **environment-axis** lesson even so.

```bash
python scripts/big_fish_data_story.py --domain football --mode perf-story --no-footer --page-size letter
# T_j twin (ad hoc; not in big_fish_data_story.py yet):
# → perf_story/FOOTBALL_usage_Tj_q16_ew16.png
```

---

## Footnotes for honest slides

- **Sparse Y (~2.7%)** — Q16 bins still ~4,400 rows each, but rates are noisy; do not over-read single-bin dips.
- Panels **7–8** use **scaled gates** (z ∈ [1, 2], top 20%) — same family as Legends/tenure scaling, not MBB verbatim.
- Panel 9 is **descriptive porch** (Q16 equal-count bins) — not prespecified HERO regression lock.
- Regenerate: `python scripts/big_fish_data_story.py --domain football --mode all`
