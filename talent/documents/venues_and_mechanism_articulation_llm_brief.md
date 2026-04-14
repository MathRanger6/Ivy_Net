# Venues & mechanism articulation — LLM brief (Scholar GPT / GPT)

**Purpose:** Paste this document (or sections) into GPT / Scholar GPT to explore **how to articulate the mechanism** of your main result **for different research communities**, and to get **per-venue fit** plus a **rollup comparison**.  
**Audience:** The model only (not a polished memo for your advisor).  
**Related docs:** `Publication_Plan.md` (items 1.2 mechanism, 1.4 venues), `replication_data_search.md` (public-data angle), `External_Data_Search_Brief.md` (dataset search). **Advisor transcript:** `260313_Paper_directions_otter_ai.txt` (root of this repo).

---

## 1. Project summary (for the model)

- **Question:** Does **rating-pool quality** (mean peer performance in one’s evaluation pool) predict **promotion probability** for U.S. Army officers? Pools are defined by **senior rater × time** (and optionally rank/branch); peer performance is summarized via **top-block (TB) share**; outcome is promotion (e.g., CPT→MAJ), with **competing risks** (promotion vs attrition vs censoring) and **cumulative incidence** (CIF) by pool-quality bins.
- **Data (proprietary):** Personnel snapshots (502), OER linkage (512), Cox/pool pipeline (520). Cannot be shared; replication uses **other public datasets** (see `replication_data_search.md`).
- **Main stylized finding:** **Inverted U** — promotion probability **rises** with pool quality, then **weakens or reverses** at the **highest** pool-quality bins (diminishing returns / “too strong a pool” pattern). Documented with equal-width binning (e.g., 8 and 25 bins) in the Run 1 / 17_1 profile.
- **Substantive extensions (in progress / planned):** Associate pools with **units (UIC)** and **divisions**; identify **which UICs or senior raters consistently host “strong pools”** over time — speaks to whether the system concentrates talent on **people vs organizations** (advisor-framed).

---

## 2. What “mechanism” means here (working definition)

The paper needs a **clear story for why** pool quality would relate to promotion **non-monotonically**: e.g., **signal / learning / credibility** in stronger peer groups; **competition / rank-in-group** or **marginal differentiation** so that at the very top pool, relative standing is harder to establish; **selection / sorting** into pools; **organizational or rater behavior** (who gets pooled with whom). The **empirical object** is well defined (pools from the evaluation architecture); the **behavioral / organizational mechanism** is what you are iterating with the model and literatures.

**Advisor guidance (transcript):** Treat mechanism articulation as **iterative with literature**: articulate mechanism → find literatures → refine mechanism → repeat. Do this **separately for different communities** because **framing and citation bases differ**.

---

## 3. Venue / community suggestions (from advisor conversation)

Use these as **explicit targets** when asking the model for tailored mechanism language. (Northwestern / **Noshir Contractor**–style **management science** was named as a natural **high-visibility** home; not AER / core labor economics.)

| Community (advisor) | How it was characterized | Notes |
|---------------------|---------------------------|--------|
| **Management science** (e.g., NU / network & org — **Noshir Contractor** genre) | Natural, **high-visibility** venue type for this kind of result | Primary candidate in discussion |
| **Operations research / systems** (e.g., **Peter Bailey**–style community) | **Dynamic networks**, **optimal flows**, **resource allocation**; people as flows through a system | “Niche” but relevant; military OR is an “easy button” but broader OR/systems framing also fits |
| **Business dynamics** (MIT-anchored) | Reframe as a **dynamical system**: people **entering/leaving**, stocks and flows | Fits if you emphasize system dynamics over cross-sectional HR |
| **People analytics / organizational behavior analytics** | Workforce outcomes, talent systems, and organizational decision processes; can bridge to management science | Treat as a **co-equal** venue track to evaluate in parallel |
| **Core economics (e.g., AER)** | **Not** the target | Advisor explicit |
| **Major interdisciplinary journals** | **Not** first target without more results and/or **additional datasets** (e.g., “magic number **three**” settings: Army + two public analogs) | Interdisciplinary story is a **stretch goal** |

**Process reminder (advisor):** Pick **two or three** communities to develop in parallel; use GPT to **reframe** the same core result for each; compare which framing is **strongest** for reviewers and for **literature engagement**. For now, evaluate at least: management science, people analytics, OR/systems, and business dynamics.

---

## 4. Copy-paste prompts for GPT / Scholar GPT

### 4.1 Per-venue mechanism articulation (run once per community)

Replace `[COMMUNITY]` with one of: *management science (org networks)*, *people analytics / organizational behavior analytics*, *operations research & dynamic resource allocation on networks (Peter Bailey-style systems/flows)*, *business dynamics / dynamical systems of workforce flows*.

```
I am writing an empirical paper on U.S. Army officer promotions. Outcome: promotion to major (competing risks). Key predictor: the mean "top block" rate of peers in my performance-evaluation pool (pool defined by senior rater × time). Finding: promotion probability increases with pool quality up to a point, then shows diminishing returns or a decline at the highest pool-quality bins (inverted-U pattern).

Task: For the [COMMUNITY] audience, write:
(1) A 2–3 paragraph mechanism story that could appear in the introduction/discussion — causal language should be careful (hypotheses, not proof).
(2) 5–8 constructs or theoretical hooks this audience expects named explicitly (e.g., social networks, tournament incentives, congestion, credibility, sorting — whichever fits).
(3) 8–12 specific papers or streams I should cite (with 1-line rationale each).
(4) What a skeptical reviewer in this community would say is weakest in my current design, and how I should preempt it in one paragraph.

Do not assume I can share microdata; emphasize what is identifiable from observational promotion and pool structure.
```

Add this follow-up block if you want more depth:

```
Now extend your answer with implementation-ready outputs:
(5) A one-page argument map with 3 testable hypotheses (H1/H2/H3), each linked to observables in my design.
(6) A "threats to inference" table with columns: threat, why it matters here, feasible robustness check using my current data, and ideal check requiring new data.
(7) A 6-item reviewer checklist for [COMMUNITY] with pass/fail criteria.
(8) Two alternative title templates and a 120-word abstract opening paragraph in this community's style.

Constraints:
- Separate what is "identifiable now" vs "plausible but not identified."
- Flag any recommendation that requires data I probably do not have.
- Keep language at manuscript-ready quality.
```

### 4.2 Management-science / Contractor-genre emphasis (your example)

```
Same setup as above. Imagine I want to situate the paper near the kind of work associated with Noshir Contractor at Northwestern: networks, teams, organizational forms, and computational social science in management.

How should I articulate the mechanism so it reads as a management-science contribution (not labor economics, not generic HR)? Give: (a) a tight elevator pitch, (b) a discussion-section mechanism subsection outline, (c) which ASQ/SMJ/Org Science/Management Science-type conversations are closest, and (d) what would be "off" if I used labor-economics tournament language instead of management language.
```

### 4.2B People analytics emphasis (co-equal venue track)

```
Same empirical setup. Now frame this for a people analytics audience as a first-class target (not a fallback), while keeping conceptual rigor suitable for management journals.

Deliver:
(a) A mechanism articulation in people-analytics language (2 paragraphs) that is still theory-linked.
(b) A practical relevance paragraph for talent management leaders without overclaiming causality.
(c) A shortlist of likely journal/community homes and what each expects empirically.
(d) The top 5 ways this can fail in review in people analytics, and exact edits to avoid those failures.

Then produce a bridge paragraph that maps people-analytics framing to management-science framing so one paper can speak to both communities.
```

### 4.2C Business Dynamics emphasis (system dynamics track)

```
Same empirical setup. Reframe this for a Business Dynamics / system-dynamics audience (MIT-style stocks, flows, feedback, delays, and path dependence in organizational systems).

Deliver:
(a) A 2-paragraph mechanism articulation using explicit stock-flow-feedback language.
(b) A causal-loop style description in text (no diagram needed) with reinforcing and balancing loops tied to the inverted-U finding.
(c) A list of state variables, flow variables, and decision rules that could be represented in a simple simulation model aligned with my empirical setting.
(d) A section outline for a paper that combines my empirical results with a lightweight system-dynamics interpretation.
(e) 8-10 literature streams or exemplar papers this audience would expect, with one-line rationale each.

Constraints:
- Keep claims consistent with observational evidence (no overclaiming causality).
- Distinguish clearly between empirical findings and conceptual dynamic-system interpretation.
- End with a short paragraph translating this framing back into language legible to management-science and people-analytics reviewers.
```

### 4.2D OR/systems emphasis (Peter Bailey-style framing)

```
Same empirical setup. Reframe this for an operations research / systems audience in the style Alex referenced as "Peter Bailey's community": dynamic networks, optimal flows, and people-as-resource-allocation over time.

Deliver:
(a) A 2-paragraph mechanism articulation using OR/systems language (flows, constraints, allocation, queueing/congestion, dynamic assignment).
(b) A conceptual model sketch in words: decision variables, state variables, objective(s), constraints, and what the inverted-U implies operationally.
(c) A list of analysis extensions that stay consistent with my current observational data (e.g., heterogeneity checks, stability over time, sensitivity analyses), separated from ideas that require additional data.
(d) A reviewer-risk table with: likely OR/systems critique, why it arises here, and how to preempt it in framing and robustness.
(e) 8-10 likely literature streams or exemplar papers to engage, with one-line fit notes.

Constraints:
- Keep all claims aligned with non-experimental evidence.
- Explicitly separate descriptive/associational results from optimization interpretations.
- End with a short bridge paragraph translating this OR/systems framing back to management science and people analytics language.
```

### 4.3 Rollup comparison table (single prompt)

```
Using the same empirical setup and inverted-U finding, produce a Markdown table with one row per research community: Management science (org networks); People analytics; OR/systems (Peter Bailey-style dynamic flows on networks); Business dynamics (MIT-style). Columns:

| Community | Core reader | Mechanism framing (1 sentence) | Canonical methods they expect | Best-fit story for inverted-U | Misfit risks | 3 must-cite paper types | Suggested title keywords |

After the table, recommend which single community is the best primary target if only one paper can be written, and which should be "secondary framing" in the intro footnote or discussion.
```

Optional stricter variant:

```
Add two columns to the same table:
| "What this audience will reject quickly" | "Minimum robustness package expected before submission" |

Then rank communities 1-4 on:
- fit to current evidence,
- publication feasibility in 6-9 months,
- downside risk if reviewers demand causal identification beyond current design.
```

### 4.4 Connect mechanism to “talent on people vs organizations” (advisor theme)

```
Same empirical setup. I may show which senior raters and/or which UICs consistently host high top-block pools over time. Write two alternative mechanism paragraphs: (A) interpretation if talent is concentrated on **stars** (people-specific pooling/rater effects); (B) interpretation if talent is concentrated on **units** (organizational breeding grounds). Then give a short "empirical disambiguation" subsection outline: what patterns would support A vs B vs both.
```

---

## 5. After the model responds — what you should do

1. **Paste the best mechanism paragraphs** back into `Publication_Plan.md` §2 (Mechanism articulation) as drafts tagged by community.  
2. **Use the rollup table** to decide **primary vs secondary** venue strategy before deep journal formatting.  
3. **Re-run external-data prompts** (`External_Data_Search_Brief.md`) once the **mechanism labels** stabilize — advisor: articulation **first**, then brainstorm domains/datasets where the same effect might replicate.

---

## 5B. Best prompt order (30-minute workflow)

Use this sequence to get cleaner outputs fast and avoid prompt drift.

### Minute 0-2: Set context once

- Paste Sections 1-3 of this brief into a fresh chat.
- Add one instruction: "Treat this as the fixed study context; ask before changing assumptions."

### Minute 3-10: Generate per-community mechanisms

- Run **4.1** four times, once each for:
  - management science
  - people analytics
  - OR/systems
  - business dynamics
- Ask for concise outputs first; depth comes next.

### Minute 11-16: Deepen strongest two framings

- For management track, run **4.2**.
- For people analytics track, run **4.2B**.
- Then run the **follow-up depth block** under 4.1 for your top two communities only.

### Minute 17-22: Force decision-quality comparison

- Run **4.3** (rollup table).
- Then run the **optional stricter variant** to surface rejection risks and minimum robustness package.

### Minute 23-27: Tie to your next analyses

- Run **4.4** (people vs organizations concentration) so your mechanism language aligns with planned UIC/senior-rater analyses.
- Ask one extra question: "Which of my planned analyses most increases credibility for each community?"

### Minute 28-30: Lock action outputs

- Ask model for a final bundle:
  - one primary community recommendation,
  - one secondary framing,
  - a 6-bullet "what to write this week" list,
  - a 6-bullet "what to test next in code" list.
- Copy these into `Publication_Plan.md` sections 2 and 3.

**Quick quality check before you trust outputs:**
- Does each mechanism paragraph clearly separate **identifiable evidence** from **interpretation**?
- Are the cited literatures actually aligned with the named community?
- Did the model avoid overclaiming causality?

---

## 6. Source note

Venue communities, process (mechanism ↔ literature iteration), and “magic number three” interdisciplinary logic are summarized from **Alex Gates**, conversation **2026-03-13**, transcript `260313_Paper_directions_otter_ai.txt`. Northwestern / Noshir Contractor reference is as stated in that conversation.
