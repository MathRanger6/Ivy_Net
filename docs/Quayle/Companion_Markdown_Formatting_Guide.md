# Companion Volume — markdown formatting guide (VECTOR)

**Last synced:** 2026-08-07

**Audience:** VECTOR — formatting the Quayle companion for Charles’s PDF converter.

**Read with:** `Companion_Volume_Creation_Protocol_v2.md` (intellectual structure) + `Markdown_to_PDF_Formatting_Guide.md` (math and Pandoc rules).

**Style exemplar:** `Complete_Companion.pdf` (merged Menger print). Chapter-level source for Menger lives as **`.docx`** in `docs/Menger/Companion Docs/` — Charles can upload one chapter (e.g. Ch. 10) if you need a side-by-side structural model. For Quayle, deliver **`.md`**; Charles converts with `convert_single_md_to_pdf.sh`.

---

## 1. Deliverable format

- **VECTOR delivers `.md` for Quayle** (Menger used Word `.docx` chapters instead). Charles runs `./scripts/convert_single_md_to_pdf.sh`.
- Return **one standalone `.md` file** (or one `.md` per chapter if too large — ask Charles first).
- **Do not** produce PDF, embed CSS, or use YAML front matter (`---` at file start = horizontal rule only).

**Document header (copy):**

```markdown
# Quayle Companion Volume — Modeling Network Growth with Assortative Mixing

**Last synced:** YYYY-MM-DD

**Source:** Quayle, Siddiqui & Jones (2006), *European Physical Journal B* 50, 617–630.

**Standalone:** Guided reading edition; read beside the source PDF.

---
```

---

## 2. Three voices — how to encode in markdown

The protocol defines **BLACK bold** (quotations), **BLUE** (interpretation), **RED** (implications). In markdown for Charles’s pipeline, use **HTML spans** so colors survive Pandoc → Playwright:

### BLACK bold — quotations worth underlining

Use for verbatim manuscript quotes (short) and “Key Quotations Worth Underlining” lists:

```markdown
<span style="color:#111;font-weight:bold">"Assortative mixing is often assumed to refer to degree assortativity, but we do not refer to degree assortativity when using this term, unless otherwise stated."</span>
```

Or, when color is unnecessary, **bold** alone is acceptable for quote lists:

```markdown
**"The governing equation is a combination of two preferential attachment rules."**
```

Prefer **span + bold** for integrated commentary; use plain **bold** in quotation bullet lists under `### Key Quotations Worth Underlining`.

### BLUE — interpretation

Wrap interpretive prose (usually longer than the source passage):

```markdown
<span style="color:#1a5490">The authors are separating *homophily* (the tendency to link to similar vertices, parameterized by α) from *assortativity* (the measured mixing pattern in the finished network, coefficient r). The model generates the latter from the former during growth — this is the paper's central mechanistic claim.</span>
```

### RED — implications (light touch for Quayle)

Use sparingly — synthesis chapter and appendix mainly:

```markdown
<span style="color:#b03030">This scalar similarity kernel (Eq. 15–16) is the most transferable piece for generative "similar agents cluster" stories — including organizational matching — without importing the full degree-attachment story.</span>
```

### Interweaving

Do **not** segregate all BLUE in one block and all RED at the end. Alternate naturally within **Integrated Commentary**, as in Menger.

---

## 3. Chapter template (match Menger / Complete_Companion.pdf)

Each conceptual unit:

```markdown
## Unit 3 — Scalar properties and continuous similarity

### Anchor (Original Text)

<span style="color:#111;font-weight:bold">"A network may also show assortative mixing by other types of vertex properties, notably including scalar or vector properties."</span>

### Key Quotations Worth Underlining

- **"We suggest a simple form for the vertex similarity given by,"**
- **"Scalar properties may be either discrete or continuous, depending on the property or the accuracy required."**

### Integrated Commentary

<span style="color:#1a5490">… BLUE interpretation …</span>

<span style="color:#b03030">… optional RED implication …</span>

### Margin Notes Worth Scribbling in the Manuscript

- α vs r — don't conflate
- Eq. (15) defines similarity; Eq. (16) plugs into Eq. (4)
```

**Rules:**

- **Anchor:** verbatim opening of the idea block — **never paraphrase, never invent** (Protocol Part V).
- **Unit titles:** conceptual, not “pp. 621–622”.
- **Margin Notes:** short bullets Charles would pencil in — optional but valuable.

---

## 4. Density and layout (print-first)

From Lessons Learned + Protocol Part VIII:

- **Dense prose** — minimal whitespace between paragraphs.
- **No slide-deck spacing** — avoid one-sentence paragraphs unless emphatic.
- **Narrow mental column** — ~80-character lines in source markdown when possible.
- **Tables:** sparingly; keep narrow. Prefer prose + quotation lists.
- **Horizontal rules `---`:** OK between major units, not between every subsection.

Charles prints with **0.1in margins** (`pdf_styles_narrow.css`) — optimize for annotation, not screen reading.

---

## 5. Math in companion volumes

Quayle is equation-heavy. Follow **`Markdown_to_PDF_Formatting_Guide.md`** in full. Quick reminders:

| Write | Avoid |
|-------|-------|
| `$\alpha$`, `$r$`, `$x_{ij}$`, `$\Pi(k_j, x_{ij})$` | Bare `\alpha` or `T_j*` outside `$…$` |
| Display: `$$ … $$` on own lines | Bare `\mathrm{...}` lines without delimiters |
| `$$r = \frac{1 - e^{-\alpha}}{1 + (n_p - 1)e^{-\alpha}}$$` | Empty `\[ \]` blocks |

When quoting an equation from the paper, show it in display math **and** cite the equation number in prose.

---

## 6. Synthesis chapter and appendix

**Synthesis (`## Final Synthesis` or last unit):** Not a summary. Answer Protocol Part XIII — why the paper matters, deepest contributions, ideas that transfer, assumptions to doubt, five-year memory.

**Appendix (`## Appendix — …`):** One cross-cutting mechanism (Protocol Part XIV). Suggested titles for Quayle:

- *Homophily → assortativity → community structure* (causal chain)
- *Hidden assumptions in the growth model*
- *What transfers vs what is domain-specific*

---

## 7. Quality checklist before handoff

- [ ] Every unit has **Anchor (Original Text)** — verbatim
- [ ] **Key Quotations** section in each unit
- [ ] BLUE spans on interpretive prose; RED sparse
- [ ] All math in `$…$` or `$$…$$`
- [ ] **`Last synced:`** date under title
- [ ] Passes **underline test** (each unit has at least one underline-worthy idea)
- [ ] No placeholder chapters; no “TBD”
- [ ] Reads like Menger companion — not Cliff Notes

---

## 8. If something is unclear

Ask Charles. He can supply additional examples from Menger work, prior companion chapters, or formatting tweaks — see **`VECTOR_Quayle_Companion_Commission.md`**.
