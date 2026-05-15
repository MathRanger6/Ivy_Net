# Alex — Tier 1 sequential model outline

## Role of this document

This note is the **advisor-ordered spine**: each section follows the sequence Alex emphasized (minimal model → assumptions → data → fitting → what we extract). It **does not replace** existing work; it points to it.

**Stable references (do not fork their content here):**

- `Tier1_Briefing_Outline.md` — full technical detail, equations, and data column map.
- `Tier1_Narrative_Outline.md` — narrative arc and voice.
- `sports/documents/tier_1_roadmap.md` — execution contract for `535` / panel columns.
- **`sports/538_alex_tier1_model_and_fit.ipynb`** — notebook that should **mirror this section order** for code + outputs (`537` stays the simulation lab).
- **Wang-style cross-domain template** (same *logical* steps as this outline): `Vector_Questions_and_Modeling_Thoughts.md` §11; mechanics of the Yin–Wang failure/success paper: `wang_paper_model.md`.

---

## 1. Unit of modeling

- State the primary unit \((i,j,t)\) and the empirical row (player–season / player–team–season).
- One sentence: local pool vs global advancement.

*Fill from `Tier1_Briefing_Outline.md` §1; keep only what you will say aloud.*

---

## 2. Minimal model objects (headline only)

- Outcome \(Y\) (global advancement).
- Amalgamated local environment \(L_{ijt}\) (Tier 1 object); first proxy \(Q\).
- Global selection capacity \(\Lambda_t\).
- Role of own performance / ability proxy \(A_{ijt}\) (baseline, not the mechanism headline).

*Detail table: `Tier1_Briefing_Outline.md` §2–§3.*

---

## 3. Minimal assumptions

- Local vs global scarcity framing.
- Leave-self-out for peer-based \(Q\).
- Variable domains (binary \(Y\), standardized \(L\) for fitting, etc.).
- What Tier 1 **defers** (sorting, dynamics, full causal ID).

*Bullets only here; expand in manuscript later.*

---

## 4. Map model to data

One table: object → meaning → `df` column / construction step (`530` / `535` CELL 2–3).

*Canonical table: `Tier1_Briefing_Outline.md` §4.*

---

## 5. Primary estimand

- **Main object to report:** turning point \(L^*\) (or \(Q^*\) in raw units), not only linear coefficients.
- One sentence on why (competing margins / inverted-U readout).

*Formulas: `Tier1_Briefing_Outline.md` §7.*

---

## 6. Fitting plan (ordered)

1. Descriptive bins (no model).
2. Transparent quadratic spec in \(L\) (LPM) + controls as needed.
3. Binary response (logit/probit) for the same index structure.
4. Robustness: FE, clustering, alternative \(L\) proxy, one decomposition term at a time.

*Expand: `Tier1_Briefing_Outline.md` §5–§6.*

---

## 7. Where simulation fits (`537`)

- One short subsection: `537` **illustrates** mechanism and comparative statics; it does **not** replace the empirical ladder unless you explicitly bridge assumptions.
- No requirement to change `537` when this outline or `538` evolve.

---

## 8. Deliverables for the next conversation

- This outline filled in at **talking-point** depth (sub-bullets, not dissertation length).
- Matching cells in **`538_alex_tier1_model_and_fit.ipynb`** so figures/tables follow sections 4–6.

---

## 9. Wang-style program — same skeleton, many domains

Alex’s sequence is how you **lock a minimal empirical model** in one domain. The Wang-line aspiration in your notes is: **(i)** a stable empirical shape, **(ii)** a **small** generative story, **(iii)** extra **testable** predictions, **(iv)** replay in other domains.

**Keep constant across domains (the “minimal model that does the trick”):**

| Layer | What stays the same | What changes per domain |
|------|---------------------|-------------------------|
| **Unit** | Individual (or role-holder) embedded in a **local pool** at time \(t\); outcome is **globally** scarce. | Definition of pool (team, unit, department) and calendar. |
| **Objects** | \(Y\), amalgamated \(L\) (peer/rivalry proxy), \(\Lambda_t\), baseline \(A\). | How you **measure** \(L\), \(Y\), \(\Lambda\) from logs. |
| **Estimand** | Turning point \(L^*\) (or equivalent in z-score then mapped back). | Binning / windowing rules; institutional noise. |
| **Fitting ladder** | Bins → quadratic in \(L\) (LPM) → logit/probit → one decomposition at a time. | FE structure (season vs fiscal year vs cohort). |

**How you *find* minimality (not wish it):**

1. **Start with the briefing’s Tier 1 spec** — one \(L\) proxy, \(L + L^2 + A\), report \(L^*\). That *is* the candidate minimal reduced form.
2. **Add complexity only on forensic rules:** e.g. crowding or minutes enters only if (a) theory says the shape should move with that margin *and* (b) the data move that way, or the minimal spec is badly misspecified in a pre-registered sense. Your “one diagnostic at a time” rule is the operational version of minimality.
3. **Use `537` for Wang-style *comparative statics*** without bloating the empirical notebook: e.g. shift effective \(\Lambda\), concentration, or opportunity; check whether \(L^*\) / top-bin behavior moves in the direction `Vector_Questions` lists (shift of peak, stronger top decline under congestion). That ties “simple mechanism” to **extra predictions**, not only the inverted-U picture.
4. **Per new domain:** copy the **same section headings** (this doc §1–§6) into a short domain addendum or notebook; replace §4’s table with that domain’s column mapping; rerun the ladder. The **abstract** story should read almost unchanged; only the measurement bridge changes.

**Honest scope:** “All domains” is **parallel replay of the same checklist**, not one pooled mega-regression on day one. The Wang papers earn universality by showing the **same qualitative mechanism** with domain-specific codings; your Alex outline is the contract for what must match across those codings.

---

## Changelog

| Date | Note |
|------|------|
| 2026-05-12 | §9: Wang-style cross-domain program — same skeleton, measurement bridge per domain; `537` for comparative statics. |
| 2026-05-12 | Initial skeleton: Alex-sequenced spine; links to existing briefing + new `538` notebook. |
