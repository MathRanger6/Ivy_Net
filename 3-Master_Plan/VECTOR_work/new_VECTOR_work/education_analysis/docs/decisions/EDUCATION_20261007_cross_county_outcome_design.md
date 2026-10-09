# Romania 2001: local-versus-anywhere descriptive outcome extension

Charles authorized this extension after the seven-county school-result and
incoming-student source recovery. It preserves the previously selected
top-one and top-two cutoff tiers, full-program rule, original six subject
categories, and own-exam-score band boundaries. It does not redefine the
original plots or turn the descriptive comparison into a causal estimate.

## Source views and meaning

The score-bearing originating-gymnasium applicant webpages define the
observed peer pool. Separate per-school result webpages show the main-round
outcome: a destination school/profile/specialization or the literal
`NEREPARTIZAT` unassigned marker. Incoming-admitted webpages independently
corroborate movements into one of the seven recovered counties. Program
directory and occupancy webpages give each receiving county's subject,
capacity, admissions count, and last admitted score. The archive masks the
personal identifier. Origin-school code plus printed name and admission
score is a provisional source match, not a certified person identifier.

An out-of-county placement is an observed admissions route. It is not
evidence of a residential move, recruitment, or a student's first choice.
An unassigned student was not placed in this main round; this is not proof of
rejection from any specific program. Preference lists are not observed.

## Frozen paired comparison

For each originating-school applicant, the new ledger distinguishes
unassigned, placed in the origin county, and placed in a different county.
The **home** indicator asks whether actual placement was in a designated
top-tier program in the origin county. The **anywhere observed** indicator
asks whether actual placement was in a designated top-tier program in the
destination county. An outward-bound placement is a known zero for the home
indicator. The anywhere indicator is determined only after the destination
program label matches a source-backed receiving-county program and all
matching program codes share the same top-tier classification. An unresolved
rank is neither a success nor a failure.

Both plotted lines use the **same denominator**: observed applicants with at
least one other observed originating-gymnasium applicant and known home and
anywhere indicators. Own-score bands are calculated on the full applicant
cohort before outcome exclusions. Program cutoff tiers are calculated within
the receiving county and subject under the saved settings; these are relative
destination rankings, not a claim that programs across counties have equal
quality. Cells with fewer than 20 applicants remain in the aggregate CSV
but are hidden from the figure as a display rule.

The separate movement-score table and figure compare examination performance
for home-placed, elsewhere-placed, and unassigned applicants. The multistate
table and figure partition the paired denominator into unassigned, top-one
anywhere, top-two-only anywhere, and other placed programs. The multistate
figure pools **within-origin-county peer-strength quantile ranks**; its x axis
is not a common absolute peer score. Conditioning on observed placement is
not a causal design; the tables and figures are descriptive.

## October 7 source gate and remaining gaps

The source-only audit covers **41,561** applicants from seven origin counties.
Their school-result pages show **576** placements outside the origin county.
**548** have a destination top-one/top-two classification invariant to every
matching program code. **22** have mixed possible ranks, and **6** lead to
Maramureș (MM), whose saved program directory and occupancy page disagree
at one program description. Those **28** remain unresolved for the paired
comparison. All home placements reuse the already verified program-placement
reports, avoiding label ambiguity introduced by school-result pages alone.

Two applicant keys have both placed and unassigned rows on their school-result
webpage; an independent saved placement record corroborates the placed row.
The audit records these cases explicitly. Extra result-only rows are never
silently added to the score-bearing applicant cohort. The exact source audit
is reproducible in
`education_analysis/code/EDUCATION_20261007_romania_cross_county_outcome_ledger.py`.
Five further school-page unassigned applicants share a printed name and
admission score with a placement in a different saved county report. With the
personal ID masked, those may be different people; the paired comparison
leaves these five unresolved rather than overriding the school-page result.
Charles controls the new run switch in the existing descriptive notebook.
The row-level ledger, when saved, remains under `~/Desktop/VECTOR_temp`;
repository outputs contain only name-free aggregates and figures.

This is a seven-origin-county descriptive extension, not a national outcome
analysis. Examination score was measured after time in the gymnasium, and
nonrandom gymnasium membership, grades, geography, preferences, and other
unobserved factors remain potential explanations of any curve.
