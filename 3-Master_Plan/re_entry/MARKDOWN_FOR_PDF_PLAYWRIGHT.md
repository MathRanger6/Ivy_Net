# Markdown → PDF — formatting guide for COMPASS (upload this file)

**Last synced:** 2026-08-07

**How Charles uses this:** Upload **this entire `.md` file** (or its PDF) into the COMPASS chat at the start of a drafting session. COMPASS has **no repo access** — everything COMPASS needs is **in this document**.

**Your deliverable:** Return a **single `.md` file** (plain markdown). Charles converts it to PDF on his Mac. **Do not** run conversion scripts, commit PDFs, or assume access to repo paths unless Charles attaches them.

**Pipeline (Charles only):** Pandoc (markdown → HTML + KaTeX) → Playwright (HTML → PDF). Default style: narrow margins (`pdf_styles_narrow.css`).

**New Mac / post-migration (once):** Playwright’s browser bundle lives in `~/Library/Caches/ms-playwright/` — it does **not** sync via git or Dropbox. Either run `./scripts/setup_playwright_pdf_mac.sh` (with `conda activate sports_net`) or just run any PDF convert; the script auto-installs Chromium if missing.

---

## 1. Document skeleton — copy this

```markdown
# Title — one line

**Last synced:** YYYY-MM-DD

**Audience:** …

**Standalone:** one sentence — reader needs no other files.

---

## Section

Body text…
```

- **`#` title:** one H1 at top (document title).
- **`Last synced:`** under title — Charles uses this to pick the newest printout.
- **`---` horizontal rules:** OK between sections (see §5 — not YAML).

---

## 2. Math — rules that actually work

Charles’s converter uses Pandoc with **KaTeX** and these math flags:

`markdown+tex_math_single_backslash+tex_math_dollars-yaml_metadata_block`

### Inline math — single `$…$`

| ✅ Do | ❌ Don't |
|-------|---------|
| `$S_i = A_i - \lambda L_C$` | `\(S_i = ...\)` (avoid) |
| `$\rho = 8$`, `$\theta = 0.72$` | Double backslashes `\\lambda` — write `\lambda` |
| `$T_{j^*}$` for assign target | Bare `T_j*` in prose (underscore breaks Markdown) |

**Single backslash** for LaTeX: `\lambda`, `\rho`, `\gamma`, `\theta`, `\sigma`, `\mathrm`, `\neq`, `\approx`, `\in`, `\text`.

### Display math — `$$…$$` on their own lines

```markdown
$$
L_C = \mathrm{mean}_{j}\,\sigma\big(\gamma(A_j - \theta)\big)
$$
```

| ✅ Do | ❌ Don't |
|-------|---------|
| Full equation inside `$$ … $$` | Bare `\mathrm{...}` line with no `$` delimiters |
| Short display blocks | Empty `\[ \]` or `\(\)` |
| `\big(`, `\big)` for readable parens | Incomplete fragments like `\[ A_i + \]` |

**Always prefer `$$` over `\[ \]`** for display math.

### Subscripts, stars, hats

| Meaning | Write |
|---------|--------|
| Assign target (star index) | `$T_{j^*}$` or `$T_{j*}$` |
| Realized team mean | `$T_j$` |
| Empirical ability | `$\hat{A}_i$` |
| Score / congestion | `$S_i$`, `$L_C$` |

### Greek in prose

Wrap in math or spell out: `$\rho$` or “rho”. Avoid bare Unicode ρ next to underscores (Markdown italic breaks).

### Math in tables

Use **inline** math only inside cells:

```markdown
| Knob | Score rule |
|------|------------|
| **λ** | `$S_i = A_i - \lambda L_C$` |
```

Do not put multi-line `$$` blocks inside table cells.

---

## 3. Project symbols (inline — no other doc required)

| Write | Avoid |
|-------|-------|
| `$L_{\mathrm{net}} = B - D$` | Unwrapped `$L_net$` |
| **ASSIGN → SCORE → SELECT** as three steps | Merging “environment” with “advancement” |
| `$K/N$` when formal | Ambiguous K/N in equations |
| **team smooth** `$L_C$` (Aug 2026 default) | LOO `mean_{j \neq i}` unless documenting legacy |

**Binding rule (always):** Environment (`$L_{\mathrm{net}} = B - D$`) is not advancement. Advancement = **score** (`$S_i = A_i - \lambda L_C$`) then **select** (top K). Hero = outcomes. Never merge into one model.

---

## 4. Structure, tables, code

### Headings

- One `#` (title). Body: `##`, `###`, `####`.
- Do not skip levels (`#` then `###`).
- Do not use `#` mid-doc for emphasis — use **bold** or `##`.

### Tables

Standard markdown tables; keep columns narrow (Charles prints on letter paper, narrow margins).

### Lists

- `-` bullets; 2-space indent for nesting.
- `1.` numbered lists for sequences or action items.

### Code and file paths

- Inline: `` `filename.py` `` or `` `folder/doc.md` `` — paths are **labels for Charles**, not links you can open.
- Fenced blocks for short snippets only; long lines truncate in PDF.

### Blockquotes

For Alex quotes or one-line claims:

```markdown
> **Claim:** Real rosters sit at high coverage peak — sim ρ must match overlap, not sort-and-chop.
```

---

## 5. Horizontal rules and YAML

**YAML front matter is disabled** in Charles’s pipeline.

- A line containing only `---` is a **horizontal rule**, not metadata.
- **Do not** start files with Pandoc YAML (`---` / `title:` / `---`) — it will not set PDF options.

---

## 6. CSS presets (Charles picks — you do not embed CSS)

| Preset name | When Charles uses it |
|-------------|----------------------|
| **narrow** (default) | COMPASS notebooks, re_entry memos, dense notes |
| standard | Wider margins |
| briefing | Short Alex-facing briefs |
| one_page | Extreme one-pager — say at top of your draft if needed |
| notebook | Jupyter exports only |

If the doc must fit **one printed page**, say so under the title: `**Print target:** one page (briefing CSS)`.

---

## 7. Page breaks and length

- Large `$$` blocks and wide tables force page breaks.
- For dense briefs: prefer inline `$…$` over display `$$`.
- For Alex one-pagers: short sentences, fewer tables, note print target.

---

## 8. Good vs bad examples

### Display equation

**Bad** (renders broken):

```markdown
\[ A_i + T_j^* + \]
```

**Good:**

```markdown
$$
\text{Legacy assign: draw } A_i,\; T_{j^*},\;\text{then soft-match with } \rho
$$
```

### Symbol in prose

**Bad:** `T_j* and rho overlap in assign.`

**Good:** `$T_{j^*}$ and $\rho$ overlap in ASSIGN.`

### Bare LaTeX line

**Bad** (may show literal backslashes):

```markdown
L_C = \mathrm{mean}_{j}\sigma(\gamma(A_j - \theta))
```

**Good:**

```markdown
$$
L_C = \mathrm{mean}_{j}\,\sigma\big(\gamma(A_j - \theta)\big)
$$
```

---

## 9. Checklist before you hand `.md` back to Charles

- [ ] One `#` title + `**Last synced:**` date
- [ ] All math in `$…$` or `$$…$$`; single backslashes only
- [ ] Subscripts braced: `$T_{j^*}$`, `$A_i$`
- [ ] No empty math delimiters; no half-finished `\[ \]`
- [ ] Tables reasonably narrow; no HTML tables
- [ ] Document is **standalone** — no “see repo file X” without pasting the needed content
- [ ] You return **markdown only** — Charles runs PDF conversion

---

## 10. If math looks wrong in PDF (Charles debugs)

Charles may re-run with HTML kept to inspect KaTeX. Common fixes:

- Raw `\lambda` in output → add missing `$` delimiters
- Garbled subscripts → use `$T_{j^*}$` not `T_j*`
- Empty math box → fill in or delete `\[ \]` blocks

---

**End of guide.** Attach this file when starting a COMPASS drafting session; ask COMPASS to follow §2–§9 on every PDF-bound memo.
