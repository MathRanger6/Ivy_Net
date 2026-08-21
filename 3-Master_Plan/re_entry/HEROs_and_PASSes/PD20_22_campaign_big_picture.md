# PD20–22 campaign — big picture in plain English

**Audience:** Charles — read-aloud companion to the HAND deck and narrative memo slides  
**Last synced:** 2026-08-19  
**Companion:** HAND deck map in [`slides/README.txt`](slides/README.txt); detail in [`pd22_minutes/PD22_minutes_panel_investigation_todo.md`](pd22_minutes/PD22_minutes_panel_investigation_todo.md)

This page is the **wavetops-to-now** story: where the dissertation came from, the **Wang-style** ladder (phenomenon → simplest mechanism → predictions), what the current basketball push is doing, where we hit a snag, what we did about it, and where we stand today.

**How to read it:** Acts and investigation threads use the same beats as the narrative memo slides — **Why this came up → What we ran → What showed up → What you can say**. Italic quotes are speakable lines, not stage directions.

---

## Part 0 — Where the whole dissertation started

### Army careers and the “inverted-U”

We studied **U.S. Army officer careers** — who gets promoted, who stalls, who leaves. In that data we found a recurring pattern: when you bin people by **how strong their peer group is** (the quality of the people around them), the rate of **advancement** (promotion, selection to the next level) often **rises through the middle** and then **drops in the very best peer environments**. That shape — up, then a dip at the top — we now call the **inverted-U** (or “hero curve tail”: rise, plateau, dip).

Plain meaning: **being surrounded by excellent peers is not always best for getting selected.** Sometimes the very strongest peer pools are the hardest places to stand out or win a scarce slot.

### The cross-domain mission

We asked: **Is that pattern special to the Army, or does it show up elsewhere?**

So we picked two other domains to test the same *kind* of question:

| Domain | “Advancement” outcome | “Peer environment” axis |
|--------|----------------------|-------------------------|
| **NCAA men’s basketball (MBB)** | Ever **NBA drafted** | Quality of **college teammates** (leave-one-out pool quality) |
| **R1 university faculty** | **Tenure** | Quality of **department / peer group** (parallel story, parked for later) |

**Basketball became the main working example** because we have rich box-score data, a clear scarce slot (draft picks), and a plot we can show in one slide — the **hero**.

**What you can say:** *“Army showed the shape; basketball is where we can build the full mechanism story — data, a scarce slot, and one slide that captures the phenomenon.”*

### The hero (MBB stylized fact — POST-QC, Aug 2026)

**Hero** = our name for the empirical chart: split college player-seasons into bins by **teammate pool quality** (with the player removed from his own average so he does not grade himself). Plot **draft rate** in each bin.

What we see on the **POST-QC** NCAA panel (2011–2021, team-seasons with **≥10 ESPN games**, min 20 minutes, locked hero spec):

- Draft rate **rises** as teammate quality improves through the middle bins — roster context matters beyond talent alone.
- Rate **levels off** at the elite ventiles — **no robust dip** in the top bin on the panel we defend (peak bin 15 ~3.25%, bin 16 ~3.21%; tail Δ ≈ −0.03 pp).

The **July 2026 inverted-U tail** (elite bin dip to ~1.2%) **replays exactly** only on **pre-QC** data (`mg=0`, exhibition cameos inflating bin 16). Audit trail: `pass_a/sensitivity/` (39 labeled specs + July replay PNG).

That is **Layer A**: honest outcome facts on a defensible panel. It is **not** yet proof of *why* (development vs crowding in the ranking process). **Generative Pass B/C** still show inverted-U in the wind tunnel; we do **not** claim bin-for-bin match to empirical ventiles.

---

## Part 1 — The Wang-style arc (smaller picture)

### Why we go past Layer A

**Why this came up:** You cannot stop at “here is a pretty plot.” Reviewers — and you — will ask three follow-ups the hero alone cannot answer:

1. **Why might the curve bend?** Peers could help you develop *or* crowd you out in the race for scarce slots. The hero mixes those stories into one outcome line.
2. **Could a simple selection story mechanism (rule) produce this shape?** Not a full NBA front-office model — the **smallest** ingredient that might matter (e.g. congestion in the **score** that ranks who gets picked).
3. **What else should be true if that mechanism is right?** A checkable prediction — not just “the curve exists.”

**What you can say:** *“Layer A is the weather report — we saw the cloud. Part 1 is the disciplined next step: name the simplest mechanism, test it in a wind tunnel, then ask what the story predicts.”*

That is the **Wang-style arc** — not one giant regression that tries to fit the hero, simulate the league, and predict the draft in a single equation.

### The ladder (phenomenon → mechanism → predictions)

The dissertation reads as a **ladder**, not one giant regression. The reference is **Wang**-style science-of-science work: **show the pattern**, **propose the simplest mechanism that could produce it**, **test something the mechanism predicts** — then write. You climb rungs; you do not jump from the weather report to a wind tunnel without the middle steps.

### Rung 1 — Phenomenon (Layer A) — closed with honest limits (Aug 2026)

**Job:** *What does the data look like?*

On the **POST-QC** panel you have:

- **Talent baseline:** draft rate rises monotonically with own ability (left panel — sanity check).
- **Roster context:** draft rate rises through middle teammate-quality bins, then a **flat elite tail** (not the sharp inverted-U dip from July pre-QC).

The surprising object is still the **second curve** — draft rate vs **teammate pool quality** — but the elite-bin story on MBB is **weaker** than the Army cross-domain read. The **July tail is a sensitivity artifact** (cameo contamination at `mg=0`), documented in `pass_a/sensitivity/`.

**What you can say:** *“On cleaned ESPN data, roster quality predicts draft rate non-monotonically in the middle; we do not claim a sharp elite dip. The generative model asks whether congestion in the score can bend selection — that is Rung 2/C, not a bin-for-bin copy of Layer A.”*

**What this does not prove:** Why the middle bends, or that any one formula “is” the NBA draft.

**Why the next rung is a story in words:** You have the curve; you do not yet have a **mechanism**. Rung 2 starts with prose — B vs D, score vs select — so you do not accidentally treat the hero regression or the sim as one merged object.

### Rung 2 — Simplest mechanism story (Layer B) — words first, not code

**Job:** *Why could excellent peers both help and hurt — and how could that connect to who gets selected?*

The move here is **deliberate simplification**. You are **not** trying to reproduce every bin of the hero on day one. You are trying to name the **minimal ingredients** that could matter:

1. **Environment (development story):** Peers can **help** (benefit **B** — you learn, you look good in a strong context) and **hurt** (congestion **D** — harder to stand out). Net peer environment is **`L_net ≈ B − D`**. This describes the **peer field around you** — it does **not** by itself pick draft winners.

2. **Advancement (selection story) — two steps, not one:**  
   - **Score:** How do we **rank** candidates? The v1 score is **`S_i = talent − λ × L_C`** — own ability minus a weight on **viable-peer congestion** on the roster.  
   - **Select:** Given those ranks, **who wins** the scarce slots? (v1: **top K** picks; later: soft **Gibbs** / temperature.)

**Binding rule (do not merge these):** Environment ≠ advancement. **Score** (ranking formula) ≠ **select** (winner rule). The **hero** is an **outcome** on real data; it is not the same object as **`S_i`**.

**What you can say at this rung:** *“Congestion in the **score** could bend who gets selected even under a fixed winner rule; the hero alone cannot tell development from crowding in the rank.”*

**What this still does not prove:** That NBA front offices compute **`S_i`** literally, or that separate **B(Q)** and **D(Q)** curves are estimated from one chart.

**Why we build a fake league next:** A story in words is not enough — you need to know the minimal ingredient **can** change who gets picked when you write the rules explicitly. That is Layer C: wind tunnel, not “the sim is the NBA.”

### Rung 2 — Minimal generative test (Layer C) — simplest fake league

**Job:** *If we write explicit rules on paper, does the minimal ingredient actually change who gets picked?*

Only **after** the story is clear do we build the **fake league** (sim **LG**, Levine–Gates). Think **wind tunnel**, not “the sim is the NBA”:

- Create synthetic players → put them on teams → **score** → **select** winners → plot draft rate by bins.
- **Headline contrast (knockout):** Same league, same top-K rule — compare scoring on **talent only** (λ = 0) vs scoring with **congestion in the score** (λ > 0). Does talent-only scoring fail to tell the congestion story?

That is the **simplified model deliverable** for basketball v1: side-by-side curves, honest axis labels, one **limitation sentence** (mechanism **can** bend outcomes; we are **not** claiming bin-for-bin match yet).

**Phase B (PD16, Aug 2026):** Before fitting parameters to real data, we built **characterization decks** — sweep knobs in the sim and ask which ones **can** produce an inverted-U-shaped outcome. That structure was accepted at PD16.

**Why Rung 3 matters:** Showing a shape — even in a wind tunnel — is still descriptive unless the story **predicts** something else. Cross-domain replication, knockout contrasts, and (later) draft prediction gains are how the ladder earns “science,” not just “nice plots.”

### Rung 3 — Predictions (Wang move) — test something the story implies

**Job:** *The model should say something checkable beyond “the curve exists.”*

Wang papers do not stop at “here is a shape.” They ask: **if this mechanism is right, what else should we see?** Examples in our project (not all done yet):

| Prediction type | Plain question | Status |
|-----------------|----------------|--------|
| **Cross-domain** | Same inverted-U in Army + MBB (+ tenure preliminary)? | Army **yes**; MBB **middle rise + flat elite tail** on POST-QC (Army tail stronger); tenure parked |
| **Knockout in sim** | Remove congestion from the **score** → different draft curve? | **Yes** — Layer C headline |
| **Predictive gain (PD14)** | Does adding roster congestion to a **draft prediction model** beat ability-only? | **Parked** after Phase B — Model A vs B |
| **Near-threshold / composition** | Under **few slots**, does congestion matter most for **top-ability** players? | Candidate; ties to **K** and λ sweeps |

You do **not** need every prediction finished before the next checkpoint. You **do** need to know where you are on the ladder: phenomenon → minimal mechanism → generative POC → **then** richer fits and predictions.

### How Part 1 connects to what follows

```
Part 0  Hero on real data (Layer A)
   ↓
Part 1  Wang arc: story (Layer B) → wind-tunnel sim (Layer C) → predictions
   ↓
Part 2  LG pipeline in detail (ASSIGN → SCORE → SELECT) + Phase B / PD17
   ↓
Part 3  HAND campaign Acts I–IV (PD20–22 — calibration, panel, policy)
```

The **current push** (PD20–22) lives mostly in **Part 3**. It assumes you accept Part 1’s ladder: we are **calibrating and defending the inputs** to the fake league and the real panel so ρ, λ, and panel policy are not hand-waved.

**What you can say:** *“Part 1 is the scientific ladder; Part 2 is how the fake league is wired; Part 3 is the current campaign — making those inputs defensible before we fit SELECT and λ*.”*

---

## Part 2 — The LG pipeline in detail (one mechanism, three steps)

**Why this section exists:** Part 1 explained *why* we have a wind tunnel and *what* the rungs are. Part 2 is the wiring diagram — one pipeline, three steps, three knob families. Without this, ρ, λ, and K feel like magic numbers.

Part 1 said *why* we have a fake league. Part 2 is *how* it is wired — the three-step pipeline we locked:

| Step | Plain question | Knob people argue about |
|------|----------------|-------------------------|
| **ASSIGN** | Who sits on which team? | **ρ (rho)** — homophily: do similar players cluster on the same roster? |
| **SCORE** | How do we **rank** players? | **λ (lambda)** — does peer congestion **subtract** from your rank? \(S_i = \text{talent} - \lambda \times L_C\) |
| **SELECT** | Who **wins** the scarce slots? | **K** — how many picks; later **temperature** for soft random selection |

**PD17 (empirical MBB):** Real rosters, interval-overlap pictures, **H_sort** (sorting index — how much players on a team look alike vs spread out), and λ sweeps on **real** team sizes. This grounds ASSIGN and SCORE in the **same panel** the hero uses.

**Why Part 3 comes next:** Once the ladder and pipeline make sense, the immediate job is **not** more philosophy — it is defending the **real player table** and the **calibration numbers** that feed LG. That is the PD20–22 HAND campaign.

---

## Part 3 — The current HAND campaign in four acts (I → IV)

**Why this campaign:** PD20 cleared soft SELECT; then we discovered the ESPN panel needed hygiene and a minutes policy before we could cite ρ* with a straight face. The HAND deck is the evidence trail — four acts, 21 slides.

Your **CHAR_PD20_HAND** deck is the meeting story for this campaign. It has **21 slides** in **four acts**:

### Act I — PD20: “Does soft selection kill the inverted-U?” (slides 1–4)

**Why this came up:** We want to replace rigid **top-K** selection with a softer **Gibbs** rule (weighted random draws — like a temperature dial). Before investing in full statistical fitting (**MLE** = maximum likelihood estimation), we need to know: **does the inverted-U still show up?**

**What we ran:** Temperature sweep on 2011–2021 MBB with real roster sizes.

**What showed up:** The inverted-U **survives**. Cold temperature nests the old top-K rule; hot temperature flattens things a different way.

**What you can say:** *“PD20 gate cleared — the inverted-U survives soft SELECT; we can move toward MLE. ρ calibration stays a separate step.”*

---

### Act II — PD22 panel backup: “Why do we trust the hero panel?” (slides 5–13)

**Why this came up:** Before we cite a **ρ** number, we must defend **the table of real players** that feeds ASSIGN and H_sort.

**Panel** = the main analysis table — one row per college player-season with minutes, points-per-minute (**PPM**), draft flag, team, season.

We discovered the raw **ESPN box score** feed is messy:

- **Dash placeholders** — fake rows with name `"-"` and zero minutes (e.g. inflated roster counts).
- **Fragmentary team-seasons** — schools with only one game in the box file (not a real season for our purposes).

So we added **box QC** at panel build:

- Drop dash-name rows.
- Drop team-seasons with too few games (keep teams with at least 11 games in the box).

Slides 5–8 show **before vs after** QC (roster sizes, games per team-season).

We also document:

- **ESPN 2013→2014 depth break** (slide 9) — more bench rows listed later; matters for contrast policies.
- **Drafted-player retention vs minutes floor** (slide 10).
- **Minutes and PPM distributions** (slides 11–13) — why low-minute rows are noisy.

**Minutes floor:** For years we kept only players with **at least 20 minutes** in the season and **dropped** everyone below that. We call that **drop sub-20** (drop players under 20 minutes). We z-score PPM within season for ability input.

**What you can say:** *“The ESPN feed needed box QC before we could defend roster slides — dash placeholders and one-game ‘seasons’ were inflating counts. Drop sub-20 is about PPM noise, not claiming every row is draft-safe.”*

---

### Act III — PD21: “What ρ should ASSIGN use?” (slides 14–16)

**Why this came up:** **ρ calibration** = bracket search — turn the homophily knob in the sim until **simulated sorting (H_sort)** matches **empirical NCAA sorting** on the same panel.

- **Slide 14 — hero panel (locked):** drop sub-20, box QC, empirical roster caps → longitudinal **ρ* ≈ 0** (all 11 seasons). Modest H_sort ≈ 0.06. **Not** “NCAA is random” — model–measurement fit on this panel.
- **Slides 15–16 — ppm0lt20 contrast:** alternate policy “keep everyone, set PPM = 0 if minutes &lt; 20” → **inflated ρ*** (~0.57) and wild 2013→2014 jump. **Illustrative only — wrong estimand** for locked calibration.

**What you can say:** *“Near-zero ρ* is model–measurement fit on modest sorting — not a claim that NCAA assignment is random. The ppm0lt20 arm is contrast only.”*

---

### Act IV — PD22 policy and overlap (slides 17–21)

After Act II–III were in the deck, we appended the **PD22 investigation results**:

| Slide | Question |
|-------|----------|
| 17 | What happens to the **ability distribution** under PPM-zero vs drop? |
| 18 | Do bench zeros **cluster** and inflate H_sort? |
| 19 | **Panel policy compare** — drop vs PPM-zero at min 20 (decision slide) |
| 20–21 | **Interval overlap** 2012 & 2013 — why ρ*=0 but rosters look “sorted” in pictures |

**What you can say (Act IV):** *“Drop at 20 is locked — PPM-zero barely moves sorting. Overlap pictures measure roster geometry; bracket ρ* measures sim fit to H_sort — different questions.”*

**Why Part 4 follows:** Acts II–III looked straightforward on paper — “here is the panel, here is ρ*.” While building those slides, two snags forced a deeper investigation. Part 4 names what broke; Parts 5–6 are how we fixed it.

---

## Part 4 — The snag (while we were doing Act II)

Act II was supposed to be quick backup: “here is how we build the panel.”

**Two snags appeared:**

1. **Data hygiene:** Raw ESPN box data were worse than we thought. Roster-size slides showed absurd tails (e.g. 115 players on a team). We could not defend the panel without **box QC** — that changed measured H_sort (~0.10 → ~0.06) and therefore **ρ*** (mixed non-zero seasons → all seasons ρ*=0 on the locked panel).

2. **Policy question (PD22, Aug 17):** Alex asked: “Why 20 minutes? Why **drop** sub-20 players instead of **keeping** them and setting their PPM to **zero**?”  
   - **Drop sub-20** = remove those rows from the panel.  
   - **PPM-zero** = keep them on the roster but force their scoring stat to zero.  
   The concern was that identical zeros would pile up on benches and **fake homophily** (inflated ρ*).

Also: an **older calibration slide** (pre–box-QC, “WITH ROSTER CAPS”) showed **6 of 11 seasons at ρ*=0** but **2013 ≈ 0.07**. That sent us on a **2012 vs 2013** side quest. After box QC, **both** seasons are ρ*=0 on the locked panel — the old contrast was a **panel epoch** issue, not drop vs zero.

**What you can say:** *“The snag was not the science — it was dirty data and an unsettled minutes policy. We split the fix: clean the feed, defend drop vs PPM-zero, then lock ρ on one coherent panel story.”*

---

## Part 5 — Fixing the snag: A, then B, then C

We split the fix into three chunks:

### A — Clean the data at the source (box QC)

**Why this came up:** Without this, roster slides and H_sort targets are contaminated by placeholders and one-game “seasons.”

**What we ran:** Filters at **panel build** (not by editing the frozen CSV). Documented in [`pd22_minutes/BOX_QC_panel_build_policy.md`](pd22_minutes/BOX_QC_panel_build_policy.md).

**What showed up:** Roster counts cluster near NCAA dress cap (~15); drafted-player counts essentially unchanged at min 20.

**Status:** **Done.** Wired into pipeline defaults. PD21 bracket **re-run** on post-QC panel (Aug 17).

---

### B — PD22 minutes and panel-policy investigation (PD22 scope)

**Why this came up:** Defend **drop sub-20** and reject **PPM-zero** as the locked policy before locking **ρ** on the hero panel.

**What we did:** See Part 6 (items 1–3 inside B).

**Status:** **Done** (items 1–11, 15 memo; item 12 team-rank forensics **skipped**; items 13–14 optional).

---

### C — Lock ρ calibration and reconcile the story

**Why this came up:** After A and B, we need one coherent line: which panel, which ρ*, what to claim and what **not** to claim.

**What we did:**

- Re-ran **PD21 bracket** on **drop sub-20 + box QC** panel → ρ* = 0 all seasons (slide 14).
- Kept **ppm0lt20** as contrast only (slides 15–16).
- Showed **overlap plots** still look sorted at ρ*=0 (slides 20–21) — bracket fit and roster geometry answer **different questions**.

**Status:** **Done** for calibration artifacts. HAND slide 14 matches locked JSON. **No second ρ re-run needed** because PD22 chose **drop**, which slide 14 already used — the ρ* pattern changed because of **box QC**, not because we rejected PPM-zero.

**Why Part 6 exists:** Part 5 says “we did B” — Part 6 is the thread-by-thread evidence inside B (minutes floor, drop vs zero, overlap reconciliation).

---

## Part 6 — Inside B: items 1, 2, and 3

When we opened **B**, we broke it into three threads:

### B1 — Justify the 20-minute floor (PD22 items 1–5)

**Question:** Is “20 minutes” arbitrary? What PPM are we throwing away?

**What we ran:** Minutes ECDF, PPM of filtered-out players, drafted-player audit, overlay plots.

**What showed up:**

- Most of the panel lives **above** 20 minutes; below 20 is bench noise and zero-minute sit-outs/transfers.
- At 20 we drop **44** drafted player-seasons; **42** were **0-minute** rows. One ever-draft career fully lost (Ricky Ledo pattern); everyone else keeps real rotation years.

**What you can say:** *“We keep the floor at 20 and drop sub-20 — not because every row is draft-safe, but because PPM below 20 is too noisy for ASSIGN.”*

---

### B2 — Drop vs PPM-zero (PD22 items 6–9)

**Question:** Does forcing sub-20 players to **PPM = 0** change sorting and ρ* in a way that matters?

**What we ran:** Ability histograms, all-zero team sanity check, bench-zero vs H_sort correlation, side-by-side bracket comparison (slide 19).

**What showed up:**

- PPM-zero adds ~**13k** bench rows and a big zero/low-z tail in ability.
- **No** all-zero team-seasons (sanity pass).
- League mean **H_sort** moves only **0.064 → 0.065** (Δ ≈ 0.001).
- Stored PPM-zero bracket ρ* ≈ 0.57 targets an **old pre-QC panel** — not valid on today’s data.

**What you can say:** *“Drop at 20 is the locked policy — PPM-zero barely moves sorting and targets the wrong panel epoch. Slide 14 already used drop; no ρ re-run for that choice.”*

---

### B3 — Reconcile ρ*=0 with overlap pictures (PD22 items 10–11)

**Question:** Bracket fit says ρ*=0 — but overlap plots look heavily sorted. And an older slide had 2013 at ρ* ≈ 0.07.

**What we ran:** Single-season interval overlap for **2012** and **2013** on the locked panel.

**What showed up:**

- **89%** (2012) and **95%** (2013) of the talent grid has **more than one team** covering the same ability bin — massive stacking even at ρ*=0.
- The remembered **2013 ρ* ≈ 0.07** came from the **pre–box-QC** calibration slide, not the locked panel.

**What you can say:** *“ρ*=0 is a modest calibration fit on H_sort ≈ 0.06 — not ‘rosters look disjoint in the overlap figures.’ Bracket fit and geometry answer different questions.”*

---

### B4 — Hero tail on POST-QC panel (Aug 2026)

**Question:** Does the July inverted-U tail survive on the panel we defend (`mg≥10`, drop sub-20)?

**What we ran:** Rebuilt hero on POST-QC panel; 39-spec sensitivity grid (`pass_a/sensitivity/`); exact July replay at `mg=0`.

**What showed up:**

- **POST-QC canonical:** n=46,306; peak bin 15 @ 3.25%; bin 16 @ 3.21% — **flat elite tail** (β₂ > 0).
- **July replay (`mg=0`):** n=62,180; peak bin 12 @ 2.62%; bin 16 @ 1.16% — **bit-for-bit match** to July artifact; 66% of old bin 16 was ≤10-game cameo team-seasons at 0% draft rate.
- **Only 1 of 32** POST-QC grid specs shows ≥2 declining bins after peak (ew20 / 2013–2021); tail still weaker than July and not concave.

**What you can say:** *“The hero middle rise is real on cleaned data; the elite dip was pre-QC contamination. We document both — canonical POST-QC for Alex, July replay in sensitivity folder only.”*

**Why Part 7 follows:** Parts 0–6 got us through the defensive campaign. Part 7 is the checkpoint — what is locked, what is parked, and what the main line is next.

---

## Part 7 — Where we stand right now (August 19, 2026)

### Wavetops

| Level | Status |
|-------|--------|
| **Dissertation mission** | Army inverted-U → test in MBB (hero) and later tenure |
| **Rung 1 — Hero (Layer A)** | **Closed with honest limits** — POST-QC middle rise + flat elite tail; July tail = pre-QC sensitivity |
| **Rung 2 — Mechanism story (Layer B)** | B−D vs score/select locked in prose; knockout concept defined |
| **Rung 2 — Generative POC (Layer C)** | Phase B characterization deck; briefed at PD16 |
| **Rung 3 — Predictions** | Sim knockout done; **PD14 predictive gain** = best MBB Rung 3 while Army locked out |
| **LG pipeline detail** | ASSIGN → SCORE → SELECT; PD17 empirical (H_sort, intervals, λ sweeps) |
| **Act I PD20** | Gibbs SELECT gate cleared (generative inverted-U survives soft SELECT) |
| **Act II panel** | Box QC + minutes/PPM backup slides in HAND |
| **Snag fix A** | Box QC done |
| **Snag fix B** | PD22 investigation done — **drop sub-20** locked |
| **Snag fix C** | ρ* ≈ 0 on locked panel; overlap story reconciled |
| **Snag fix D** | Hero POST-QC audit done — Rung 1 language + plots updated |

### Exact next beat (main line)

You are **not** blocked on panel policy or ρ re-calibration for drop-vs-zero.

**Resume the scientific main line:**

1. **SELECT / MLE** — PD20 cleared the gate; next lock **K-draw semantics**, then statistical fit for SELECT parameters.  
2. **λ*, t*, γ** — fit SCORE/SELECT on the locked panel story.  
3. **Manuscript** — hero + mechanism + honest limits; tenure and Army when MBB v1 is tight.

**Optional / parked:** PD22 item 12 (team-rank forensics), items 13–14 (caps-off sensitivity, minutes ladder). Do not let these block the main line unless asked in meeting.

### What lies ahead (summary)

| Track | What |
|-------|------|
| **Main line** | SELECT / MLE → λ*, t*, γ → side-by-side deliverable (hero + sim, honest limits) |
| **Rung 3** | PD14 predictive gain, near-threshold tests — **unpark as MBB Rung 3** while Army access locked |
| **Parked** | PD22 items 12–14, tenure third leg — appendix, not blockers |
| **Horizon** | Three-setting paper (Army + MBB + tenure preliminary) as one Wang-style ladder |

### One breath — closing line

> We cleared soft SELECT (PD20). We cleaned the ESPN panel (box QC) and defended **drop sub-20** over **PPM-zero** (PD22). On that locked panel, **ρ* ≈ 0** matches modest sorting — not random NCAA rosters — and overlap pictures still look stacked because they measure **geometry**, not the homophily knob. **Hero Rung 1 is closed:** middle rise on POST-QC, flat elite tail, July dip documented as pre-QC sensitivity only. We can go back to **fitting SELECT** and **PD14 predictive gain** without reopening panel policy.

**Open next:** Lock K-draw semantics for Gibbs SELECT, then scope MLE for λ*, t*, and PD14 draft-prediction contrast.

---

## Glossary (shorthand → plain English)

| Term | Plain English |
|------|----------------|
| **Hero** | Empirical plot: draft rate vs teammate pool quality (POST-QC: middle rise + flat elite tail) |
| **Wang-style arc** | Phenomenon → simplest mechanism → testable predictions → write (not one mega-model) |
| **Layer A / B / C** | A = describe curve; B = mechanism story in words; C = fake-league code test |
| **Knockout** | Same sim + winner rule; remove congestion from the **score** (λ = 0) and compare curves |
| **Inverted-U** | Rise then (often) dip — advancement rate peaks below the very best peer bin; **Army yes; MBB elite tail flat on POST-QC** |
| **Panel** | Table of real player-seasons we analyze |
| **PPM** | Points per minute — scoring rate from box stats |
| **Drop sub-20** | Remove player-seasons with &lt; 20 total minutes |
| **PPM-zero** | Keep sub-20 players but set their PPM to 0 |
| **Box QC** | Hygiene filters when building panel from ESPN box (dash rows, low-game teams) |
| **ρ (rho)** | Homophily knob in **ASSIGN** — similar players cluster on teams |
| **λ (lambda)** | Congestion weight in **SCORE** — peer field subtracts from rank |
| **H_sort** | Sorting index — how much realized roster ability clumps by team |
| **ρ*** | Calibrated ρ that makes sim H_sort match empirical H_sort |
| **LG / Grandchild** | Our sim pipeline: ASSIGN → SCORE → SELECT |
| **LOO** | Leave-one-out — pool quality excluding the player himself |
| **Gibbs SELECT / temperature** | Soft random selection instead of deterministic top-K |
| **MLE** | Fitting model parameters statistically to data |
| **HAND deck** | `CHAR_PD20_HAND.pptx` — your edited meeting slides (not AUTO) |
| **AUTO deck** | Script-generated `*_AUTO.pptx` — copy figures/bullets into HAND |
| **Panel epoch** | Which rules built the panel (pre-QC vs post-QC changes ρ* targets) |

---

## How this doc relates to others

| Need | Read |
|------|------|
| Dissertation “why” + Wang arc | [`../01_The_Problem_in_Plain_English.md`](../01_The_Problem_in_Plain_English.md) |
| Three layers / score ≠ select (full) | [`../02_Three_Kinds_of_Model.md`](../02_Three_Kinds_of_Model.md) |
| Predictive importance (Rung 3, parked) | [`../05_Alex_Magnitude_Spec.md`](../05_Alex_Magnitude_Spec.md) |
| ASSIGN → SCORE → SELECT formulas | [`Alex_LG_three_step_briefing.md`](Alex_LG_three_step_briefing.md) |
| HAND slide numbers | [`slides/README.txt`](slides/README.txt) |
| PD22 task list + numbers | [`pd22_minutes/PD22_minutes_panel_investigation_todo.md`](pd22_minutes/PD22_minutes_panel_investigation_todo.md) |
| Conversational meeting memo slides | `slides/auto/CHAR_PD20_22_takeaways_memo_AUTO.pptx` — narrative companion; paste each HAND slide after its footer cue |

---

*Optional read-aloud order for the HAND deck: Acts I → II → IV (17–19) → III (14–16) → IV (20–21) — policy evidence before ρ and overlap.*
