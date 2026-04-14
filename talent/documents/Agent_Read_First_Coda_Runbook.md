# Read First: Coda's Replication Runbook

Use this file as the quick-start instruction to any new coding agent.

Note: this runbook assumes the receiving agent already knows the current college data pipeline (especially `sdv_second.ipynb`) and does **not** need basic onboarding.

## Copy/Paste Message to Scout (from Coda)

Scout — please read `current_documents/Agent_Read_First_Coda_Runbook.md` and `current_documents/Army_to_College_Basketball_Replication_Handoff.md` first. These were prepared by **Coda** for this handoff.

Key context from **Coda**: Army work was partly done in a sensitive SWS environment with a code-together/transcribe workflow, so not every historical run is fully replay-visible locally; use docs and saved outputs as authoritative.

Main objective now: test whether college data replicates the Army **upside-down U (inverted-U)** between pool quality and advancement, using at least one baseline and one alternative mapping, with decision-grade diagnostics (quadratic sign, turning point, and binned visual support).

If any mapping/design choice is ambiguous, pause and ask Charles before proceeding.

---

## Message to the new agent

Read the following documents from my other agent, **Coda**, in this order, then continue the college-basketball replication work:

1. `current_documents/Army_to_College_Basketball_Replication_Handoff.md`
2. `current_documents/sports_mechanisms/advisor_packet_COMPACT_CLEAN.md`
3. `current_documents/sports_mechanisms/sports_replication_strategy_FINAL.md`
4. `current_documents/sports_mechanisms/college_basketball_empirical_design.md`
5. `current_documents/sports_mechanisms/model_walkthrough_reference.md`
6. `current_documents/Publication_Plan.md`

Then inspect the active coding notebook for current implementation details:

7. `sdv_second.ipynb`

And the key generated data artifacts:

8. `datasets/mbb/draft_unmapped_college_candidates.csv`
9. `datasets/mbb/draft_unmapped_athlete_candidates.csv`
10. `datasets/mbb/draft_athlete_match.csv`
11. `datasets/mbb/draft_match_review.csv` (read-only for review; do not add label columns—use the template below)
12. `datasets/mbb/draft_match_manual_feedback_template.csv` (structured `accept` / `reject` for optional dedupe)
13. `datasets/mbb/athlete_id_draft_lookup.csv`

---

## Project objective (non-negotiable)

Replicate the Army pattern in college basketball:
- **Upside-down U / inverted-U** relationship between advancement probability and pool quality.

Interpretation should stay careful:
- observational evidence, strong diagnostics, no overclaiming causality.

---

## Army environment context (important)

- Prior Army coding was done in a sensitive SWS environment with a "code together -> transcribe back" workflow.
- Because of that workflow, some Army logic/results may be visible in docs, configs, and saved outputs more than in fully reproducible local run history.
- Do **not** interpret missing local reproducibility of Army runs as conceptual inconsistency; some execution happened in another environment by design.
- This college basketball track is different: data are public and local workflows are much more directly reproducible.

---

## What to look for in Army-style upside-down-U plots

When comparing college results to Army pattern, use these visual cues:
- CIF curves by pool bins where middle bins outperform low bins, but top-end bins lose the same edge (or reverse).
- Final-CIF bar panels that rise through low/mid bins and then flatten/decline at high bins (non-monotone).
- Promotion and attrition panels interpreted jointly, not in isolation.

Reference visual signature from Army outputs:
- Two-panel CIF curves (promotion + attrition) plus corresponding final-CIF bars by bin.

---

## Execution checklist (strategy-first, not onboarding)

### A) Lock decision grid before coding changes
- Confirm which mapping(s) are in-scope for this iteration (at least one primary + one alternative).
- Confirm the advancement definition for this run (draft-only vs broader pro entry).
- Confirm minimum diagnostics package expected by Charles for sign-off.

### B) Use existing pipeline strengths
- Reuse current matching/mapping assets and quality tiers from `sdv_second.ipynb`; do not rebuild fundamentals unless diagnostics fail.
- Preserve reproducibility artifacts and confidence audit trail.

### C) Replication tests that answer the research question
- Baseline + alternative mapping must both report:
  - linear and quadratic pool terms,
  - turning point and uncertainty,
  - nonparametric/binned evidence with support.

### D) Explicit comparison
- Compare where upside-down U appears, weakens, or disappears across mappings.
- Identify which assumptions are doing the work.

### E) Decision-ready output to Charles
- Summarize:
  - where inverted-U appears,
  - where it weakens/fails,
  - what assumptions drive changes,
  - recommended next iteration.

---

## Clarification rule

If intent is ambiguous at any major design choice (outcome definition, pool definition, sample restrictions, robustness scope), **pause and ask Charles for clarification before proceeding**.

---

## One-line handoff prompt you can paste

"Please read `current_documents/Agent_Read_First_Coda_Runbook.md` and all referenced files in order, then continue the college-basketball replication coding workflow to test for an inverted-U relationship between pool quality and advancement."

