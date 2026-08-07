# Markdown → PDF — formatting guide (VECTOR / companion deliverables)

**Last synced:** 2026-08-07

**Audience:** VECTOR — any `.md` Charles converts to PDF on his Mac.

**Companion-specific layout (anchors, BLACK/BLUE/RED, chapter template):** see **`Companion_Markdown_Formatting_Guide.md`** in this folder.

**Your deliverable:** Return **markdown only**. Charles converts locally with `./scripts/convert_single_md_to_pdf.sh`. Do not run Playwright or commit PDFs unless he asks.

**Menger precedent:** chapter `.docx` in `docs/Menger/Companion Docs/` → `Complete_Companion.pdf`. **Quayle:** return `.md`; Charles runs the convert script.

**Pipeline:** Pandoc (markdown → HTML + KaTeX) → Playwright (HTML → PDF). Default CSS: **`pdf_styles_narrow.css`** (dense, 0.1in margins).

---

## 1. Document skeleton

```markdown
# Title — one line

**Last synced:** YYYY-MM-DD

**Standalone:** one sentence — reader needs no other files.

---

## Section

Body text…
```

- One `#` title at top.
- **`Last synced:`** under title.
- `---` between sections is OK — **not** YAML front matter.

---

## 2. Math — required for Quayle

Pandoc flags: `markdown+tex_math_single_backslash+tex_math_dollars-yaml_metadata_block`  
Rendering: **KaTeX** (`--katex`).

### Inline — `$…$`

| ✅ Do | ❌ Don't |
|-------|---------|
| `$\alpha$`, `$r$`, `$x_{ij}$` | Double backslashes `\\alpha` |
| `$\Pi(k_j, x_{ij})$` | `\( … \)` unless unavoidable |
| `$n_p$` discrete property count | Bare subscripts in prose |

**Single backslash:** `\alpha`, `\rho`, `\gamma`, `\theta`, `\sigma`, `\mathrm`, `\neq`, `\approx`, `\in`, `\text`, `\frac`, `\sum`, `\propto`.

### Display — `$$…$$` on own lines

```markdown
$$
\Pi(k_j, x_{ij}) = \frac{f(k_j)\, e^{-\alpha(1-x_{ij})}}{\sum_l f(k_l)\, e^{-\alpha(1-x_{il})}}
$$
```

| ✅ Do | ❌ Don't |
|-------|---------|
| Full equations in `$$ … $$` | Bare `\mathrm{...}` lines without `$` |
| `\big(`, `\big)` for readability | Empty `\[ \]` or `\(\)` |

### Network-paper symbols (Quayle)

| Symbol | Write |
|--------|--------|
| Homophily | `$\alpha$` |
| Assortativity coefficient | `$r$` |
| Similarity | `$x_{ij}$` |
| Modularity | `$Q$` |
| Vertex property | `$p_i$` |
| Attachment probability | `$\Pi$` |

### Greek in prose

Wrap: `$\alpha$` or spell out “alpha”. Avoid bare Unicode next to underscores.

### Math in tables

Inline only inside cells — no multi-line `$$` in tables.

---

## 3. Structure

### Headings

- One `#` (title). Then `##`, `###`, `####`.
- Do not skip levels.

### Tables

Standard markdown; keep narrow for letter + narrow margins.

### Lists

- `-` bullets; `1.` for numbered sequences.

### Blockquotes

```markdown
> **Note:** …
```

Use for asides; companion **quotations** use the companion formatting guide (spans / bold), not generic blockquotes.

### HTML spans

Raw HTML (e.g. `<span style="color:…">`) is **allowed** and needed for companion color voices. Pandoc passes them through to Playwright.

---

## 4. YAML and horizontal rules

**YAML front matter is disabled.**

- Line with only `---` = horizontal rule.
- Do **not** start with `---` / `title:` / `---` metadata blocks.

---

## 5. CSS preset (Charles chooses)

| Preset | Use |
|--------|-----|
| **`pdf_styles_narrow.css`** | **Default** — companion volumes, dense notes |
| `pdf_styles.css` | Wider margins |
| `pdf_styles_briefing.css` | Short briefs |

You do not embed CSS in the markdown.

---

## 6. Page breaks

- Large `$$` blocks and wide tables force breaks.
- Dense companions: prefer inline `$…$` in running prose; reserve `$$` for important displayed equations.

---

## 7. Good vs bad examples

**Bad** (broken PDF):

```markdown
\[ \Pi = f(k) e^{-\alpha} \]
```

**Good:**

```markdown
$$
\Pi = f(k)\, e^{-\alpha(1-x_{ij})}
$$
```

**Bad:**

```markdown
r = 1 - e^{-α} / (1 + (np - 1)e^{-α})
```

**Good:**

```markdown
$$
r = \frac{1 - e^{-\alpha}}{1 + (n_p - 1)e^{-\alpha}}
$$
```

---

## 8. Handoff checklist

- [ ] `#` title + `**Last synced:**`
- [ ] All math in `$…$` or `$$…$$`; single backslashes
- [ ] No empty math delimiters
- [ ] Standalone document — no “see repo file X”
- [ ] Companion color/template rules in **`Companion_Markdown_Formatting_Guide.md`** if delivering a companion volume

---

## 9. Charles debugs PDF issues

If math shows as raw `\alpha`: missing `$` delimiters.  
Charles may use `--keep-html` on convert to inspect KaTeX output.

---

**End of guide.**
