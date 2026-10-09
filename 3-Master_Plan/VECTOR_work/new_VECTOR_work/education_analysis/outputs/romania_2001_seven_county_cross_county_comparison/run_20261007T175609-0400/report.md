# Seven-county local-versus-anywhere comparison

The same observed gymnasium applicants enter both lines of each paired plot. Home means a top program in the originating county; anywhere means a top program in the actual destination county. Both program rankings use the saved notebook's top-one/top-two, full-program, subject-category settings. A placement outside the home county is a known zero for the home outcome but enters the anywhere outcome only after its destination program's rank is source-resolved.

Applicants in the source ledger: **41,561**. Paired denominator after requiring a gymnasium peer and both rankings: **41,469** (top one), **41,469** (top two). These are participating admissions-round applicants, not every eighth grader.

## Source limits

Out-of-county placements with an unresolved destination-program rank: **28**. The unreconciled destination catalog county code(s): **MM**. There are also **5** school-page unassigned applicants with a same-name-and-score placement elsewhere in the saved national reports; masked IDs prevent treating that as the same person. These rows remain unresolved and are excluded from both lines of the paired plot, rather than being called failures. Exact source-status counts are in `source_audit.csv`.

The archived personal identifier is masked. Matches based on origin school plus printed name and admission score are provisional. The archive does not show student preference lists: unassigned does not mean rejected by a particular program, and an origin–destination county link does not explain why the student applied there. Examination score was measured after time in the gymnasium. These figures are descriptive, not causal evidence of congestion.

`movement_score_composition.csv` compares own examination performance across home placed, elsewhere placed, and unassigned applicants. `multistate_cells.csv` splits the common denominator into unassigned, top-one, top-two-only, and other placed programs. All exports in this folder are name-free aggregates; the optional row-level ledger stays on the Desktop.
