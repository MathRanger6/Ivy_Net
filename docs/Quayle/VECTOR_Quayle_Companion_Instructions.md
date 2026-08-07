# Quayle Companion Volume — Instructions for VECTOR (Charles reads this too)

**Last synced:** 2026-08-07

**From:** Charles Levine  
**To:** VECTOR  
**Job:** Guided reading companion for Quayle, Siddiqui & Jones (2006)

**Charles’s plan:** Print this document, read it, upload **this file plus everything else in the Quayle folder** to VECTOR, then work Phase 1 → 2 → approval → 3.

---

## 0. What you are building (both of us)

A **companion volume** is **not** a summary, lit review, study guide, or paraphrase.

It **is** a guided intellectual edition: Charles reads the **source paper PDF side-by-side** with your commentary and feels like an attentive co-author is explaining what deserves underlining, what mechanisms matter, and what assumptions hide in the math.

**Success test:** *Reading beside an exceptionally insightful co-author.*  
**Failure modes:** invented anchors, sparse quotes, executive-summary tone, placeholder chapters, excessive whitespace. See **`Companion_Volume_Lessons_Learned.md`**.

**Menger precedent (June 2026):** You and Charles built **`Complete_Companion.pdf`** from chapter **Word `.docx`** files (see **`Menger_Companion_Chapter_10_EXAMPLE.docx`** in this folder). **Quayle uses the same intellectual format** but you deliver **markdown** (`.md`); Charles converts to PDF locally.

---

## 1. Source paper

**Quayle, A. P., Siddiqui, A. S., & Jones, S. J. M. (2006).**  
*Modeling network growth with assortative mixing.*  
*European Physical Journal B*, 50, 617–630.

**File in this folder:** `Quayle_Siddiqui_Jones_2006_assortative_mixing.pdf` (~14 pages)

---

## 2. Files in this folder — read before you write anything

| # | File | Role |
|---|------|------|
| 1 | **`VECTOR_Quayle_Companion_Instructions.md`** | **This document** — process, phases, scope |
| 2 | `Quayle_Siddiqui_Jones_2006_assortative_mixing.pdf` | Source manuscript |
| 3 | `Companion_Volume_Creation_Protocol_v2.md` | Binding operating manual |
| 4 | `Companion_Volume_Lessons_Learned.md` | What worked / failed on Menger |
| 5 | `Reader_Context_Profile.md` | How Charles reads (dense, quotes, print) |
| 6 | `Research_Context_Overview.md` | Background for **light** RED hooks only |
| 7 | `Complete_Companion.pdf` | Merged Menger companion — **print density & structure target** |
| 8 | `Menger_Companion_Chapter_10_EXAMPLE.docx` | **One chapter exemplar** — section skeleton, voice mix (Word era) |
| 9 | `Companion_Volume_Formatting_Guide.docx` | Original BLACK / BLUE / RED rules (Word) |
| 10 | `Companion_Markdown_Formatting_Guide.md` | **How to encode the three voices in `.md`** (HTML spans, unit template) |
| 11 | `Markdown_to_PDF_Formatting_Guide.md` | **Math + Pandoc** — `$…$`, `$$…$$`, symbols |
| 12 | `Companion_Volume_Request_TEMPLATE.docx` | Generic kickoff template from Menger/Rosen round (reference) |

**Additional materials:** Charles can supply more on request (other Menger chapters, deep-reading notes, papers). **Ask first** — do not assume you need them.

---

## 3. Workflow — four phases (do not skip)

### Phase 1 — Read everything

Before proposing or writing companion prose, read carefully:

1. This instructions file  
2. **`Companion_Volume_Creation_Protocol_v2.md`** (binding)  
3. **`Reader_Context_Profile.md`** + **`Companion_Volume_Lessons_Learned.md`**  
4. **`Complete_Companion.pdf`** — note density, anchors, quote load, synthesis  
5. **`Menger_Companion_Chapter_10_EXAMPLE.docx`** — one chapter’s section structure  
6. **`Companion_Markdown_Formatting_Guide.md`** + **`Markdown_to_PDF_Formatting_Guide.md`** — how Quayle deliverable must look in `.md`  
7. **`Quayle_Siddiqui_Jones_2006_assortative_mixing.pdf`** — the full paper  

Treat Menger as **style exemplar**; treat the protocol as **binding**.

---

### Phase 2 — Propose companion architecture (required before drafting)

**Do NOT begin writing companion chapters yet.**

Identify **conceptual units** in Quayle — **not** page boundaries, **not** paragraph-by-paragraph commentary.

Deliver to Charles a **Companion Architecture Proposal** containing:

#### A. Chapter / unit list

For each proposed unit (aim **~8–12 units** for this 14-page paper, plus synthesis + appendix):

| Field | Requirement |
|-------|-------------|
| **Unit number** | 1, 2, 3, … |
| **Proposed title** | Conceptual (e.g. “Scalar properties and the similarity kernel”) |
| **Anchor** | **Verbatim** opening text of the first paragraph in this block — never paraphrase, never invent |
| **Major concepts** | Bullet list |
| **Relative importance** | High / medium / low for Charles’s understanding |

Suggested unit map (starting point — revise after reading):

1. Introduction — homophily vs assortativity, why generic vertex properties  
2. Model core — Eq. (4), degree PA × similarity product  
3. Discrete properties — δ function, Eq. (8), appendix $r(\alpha)$  
4. Hierarchical properties — tree similarity, Eq. (12)–(14)  
5. Scalar / continuous properties — **Eq. (15)–(16)** (high priority)  
6. Community structure & modularity — what claims matter  
7. Simulation results — discrete case (Figs. 2–4)  
8. Simulation results — hierarchical case (Figs. 6–9)  
9. Summary & limitations in the paper  
10. **Final synthesis** (your voice — not a summary)  
11. **Appendix** — one cross-cutting mechanism (e.g. homophily → assortativity → community)  

#### B. Deep-structure memo

Also provide:

- Major **mechanisms** (phenomenon → mechanism → assumptions → boundaries)  
- Recurring **themes**  
- **Hidden assumptions**  
- **Transferable concepts** (network science, not Charles’s code)  
- Planned **synthesis chapter** focus  
- Planned **appendix** focus  

#### C. Formatting acknowledgment

Confirm you will use:

- **`Companion_Markdown_Formatting_Guide.md`** for unit skeleton and three voices  
- **`Markdown_to_PDF_Formatting_Guide.md`** for all math  

---

### Phase 3 — Wait for Charles’s approval

After Phase 2, **STOP**.

Do not draft integrated commentary until Charles approves the architecture (he may rename units, merge/split, or reprioritize).

---

### Phase 4 — Write the companion (after approval)

Deliver **markdown** (`.md`):

- One file **`Quayle_Companion_Volume.md`** preferred; or one `.md` per unit if size forces it (ask Charles).  
- Charles converts: `./scripts/convert_single_md_to_pdf.sh Quayle_Companion_Volume.md Quayle_Companion_Volume.pdf pdf_styles_narrow.css`  
- **You do not produce PDF.**

#### Unit template (each conceptual unit)

```markdown
## Unit N — [Title]

### Anchor (Original Text)

<span style="color:#111;font-weight:bold">"[Verbatim opening sentence(s) from paper…]"</span>

### Key Quotations Worth Underlining

- **"[Quote 1]"**
- **"[Quote 2]"**

### Integrated Commentary

<span style="color:#1a5490">[BLUE — what the author is really saying; usually longer than the source passage.]</span>

<span style="color:#b03030">[RED — optional; sparse; why this might matter beyond the paper.]</span>

### Margin Notes Worth Scribbling in the Manuscript

- …
```

**Three voices:**

| Voice | Markdown | Job |
|-------|----------|-----|
| **BLACK bold** | `<span style="color:#111;font-weight:bold">` or `**quote**` in quotation lists | Verbatim underline candidates |
| **BLUE** | `<span style="color:#1a5490">…</span>` | Interpretation — **dominant** |
| **RED** | `<span style="color:#b03030">…</span>` | Implications — **sparse**; synthesis + appendix mainly |

Interweave BLUE and RED naturally — do not dump all RED at the end.

#### Synthesis chapter (required)

Answer (Protocol Part XIII):

- Why does this paper matter?  
- Deepest contributions?  
- What transfers?  
- What assumptions deserve skepticism?  
- What should Charles remember in five years?  

**Not** a bullet summary of units.

#### Appendix (required)

One cross-cutting mechanism distributed through the paper (Protocol Part XIV).  
Example title: *Homophily → assortativity → community structure*.

---

## 4. Quayle-specific reading priorities

Charles cares most about understanding:

- **Homophily** $\alpha$ vs **assortativity** $r$ — vocabulary discipline  
- **Governing equation (4)** — product of degree attachment and similarity preference  
- **Scalar properties (§2.3, Eqs. 15–16)** — similarity kernel and attachment law (**high priority**)  
- Discrete vs hierarchical cases — when each matters  
- **Appendix** — ensemble $r(\alpha)$ and inverting for $\alpha$ (Eq. 28)  
- Community / modularity results — main claims vs detail Charles can skim  

---

## 5. RED / project connections — light touch

This companion is **for paper mastery**, not simulation implementation.

- Interweave RED **sparingly** in unit commentary.  
- A **few paragraphs total** in synthesis + appendix may note: Charles is reading this because **assortative mixing** is intellectually adjacent to **assortative matching** in organizational/advancement work (`Research_Context_Overview.md`).  
- **No** file paths, function names, code, or “assign rule” deliverable.

---

## 6. Quality bar (checklist before handoff)

- [ ] Architecture was **approved** before drafting  
- [ ] Every unit has **verbatim Anchor** — underline test passed  
- [ ] **Key Quotations** in every unit — dense, not sparse  
- [ ] BLUE generally **longer** than the passage it interprets  
- [ ] All math in `$…$` or `$$…$$` per formatting guide  
- [ ] **`Last synced:`** date under document `#` title  
- [ ] Synthesis + appendix present — not placeholders  
- [ ] Document converts cleanly for Charles (no empty `\[ \]`, no bare LaTeX lines)  

---

## 7. What Charles does after you deliver

1. Review `.md`  
2. Run PDF conversion on his Mac  
3. Print and read beside `Quayle_Siddiqui_Jones_2006_assortative_mixing.pdf`  

---

## 8. Start here (VECTOR)

**Your first deliverable is Phase 2 only:** Companion Architecture Proposal + deep-structure memo.

**Do not write Unit 1 until Charles approves.**

When ready, send the architecture proposal to Charles in chat.

---

**End of instructions.**
