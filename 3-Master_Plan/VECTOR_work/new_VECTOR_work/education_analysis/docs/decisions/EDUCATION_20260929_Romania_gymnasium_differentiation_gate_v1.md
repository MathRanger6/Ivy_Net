# Romania 2001 gymnasium differentiation gate

**Date:** 2026-09-29  
**Status:** Authorized by Charles for implementation and execution.  
**Scope:** Pre-placement differentiation diagnostics only. No placement outcome model, HERO curve, congestion estimate, or causal claim.

## Question

Among participating applicants in the recovered Alba 2001 Ministry reports, do originating gymnasiums organize national-examination performance into meaningfully different groups, or do they look like similarly heterogeneous slices of one county-wide distribution?

This is a go/no-go diagnostic for the proposed peer environment. It does not establish that gymnasiums selected their students through admissions, that the observed applicants represent every eighth-grade classmate, or that a gymnasium caused the measured performance.

## Locked population and measure

- Population: every recoverable participating applicant in the 168 source-coded Alba origin-gymnasium reports. The directory contains seven valid reports with zero participating applicants; they remain in the source accounting but cannot define performance intervals or leave-one-out groups.
- Group: source-native origin-gymnasium code. Printed school names do not merge codes; this preserves the two distinct Căpâlna codes.
- Individual performance, \(A_i\): national examination score, \(E_i\).
- Standardization: one county-wide z-score using the recovered applicant population mean and population standard deviation. No within-gymnasium standardization.
- Grades 5–8 and the admission composite are retained only for formula and completeness checks. They are not alternative specifications in this first gate.

The defensible label is **participating applicants associated with an originating gymnasium**, not all classmates or all gymnasium graduates.

## Required structural checks

1. Recover all 168 school-specific candidate reports.
2. Match each recovered report's row count to the completed structural-audit checkpoint.
3. Require finite examination score, grades 5–8 average, and admission composite on every included row.
4. Recheck the documented truncated formula

   \[
   T_i=\frac{\lfloor100(0.75E_i+0.25G_i)\rfloor}{100}.
   \]

5. Save no name, raw page, or directly identifying field in the permanent Dropbox/repository workspace. The September 30 resumption amendment below governs the separately authorized temporary local cache.
6. If any required report remains unresolved or any row-count check fails, stop before calculating the scientific diagnostics.

### September 30 resumption amendment

Charles authorized a temporary, local cache at `~/Desktop/VECTOR_temp/`, outside Dropbox and the repository. After every successful report retrieval, the complete parsed source table and retrieval metadata will be written atomically to that temporary cache. This permits exact resumption without repeated archive requests. Direct identifiers remain confined to that temporary location.

The permanent research workspace may retain a name-free analytical file containing source code, generated analytical row identifier, \(E_i\), \(G_i\), \(T_i\), and the global standardized examination score. It will not contain names, CNP values, or raw pages. The temporary identifiable cache will be erased only after the completed results, provenance manifest, and narrative have been verified.

## Diagnostics

1. Applicant-count distribution across gymnasium codes, including counts and applicant shares in groups of at least 2, 5, 10, and 20.
2. Overall raw and standardized national-examination-score distribution.
3. For every gymnasium: minimum, first quartile, median, mean, third quartile, maximum, standard deviation, and applicant count.
4. An interval panel sorted by gymnasium mean, showing the full range, middle 50% interval, mean, and group size.
5. The repository sorting index:

   \[
   H_{\mathrm{sort}}
   =1-\frac{\sum_g\sum_{i\in g}(A_i-\bar A_g)^2}
   {\sum_i(A_i-\bar A)^2}.
   \]

6. One thousand deterministic random reassignments of the observed examination scores to the observed slots in the 161 nonempty gymnasium groups. Every reassignment preserves all positive gymnasium sizes exactly; the seven zero-applicant source codes remain separately reported.
7. Random references for the sorting index, interval coverage, interval width, and each gymnasium mean conditional on that gymnasium's observed size.

The randomizations are a finite-sample grouping reference conditional on these applicants and sizes. They are not a claim about uncertainty in a national population.

## Interpretation

- Differentiated means, narrower-than-random intervals, and less-than-random overlap support meaningful organization by gymnasium.
- Different means with broad overlap indicate partial differentiation within substantially heterogeneous schools.
- Results resembling the size-preserving random reference indicate little measured organization of examination performance by gymnasium.
- Strong differentiation without common support would undermine comparisons of similarly performing students across gymnasium environments.

Any result remains descriptive. The national examination occurs after years of gymnasium exposure and is not an unaffected pre-gymnasium ability measure.

## Filing

- Code: `education_analysis/code/`
- Aggregate outputs and figures: `education_analysis/outputs/romania_alba_2001_differentiation_v1/`
- Run record: `education_analysis/docs/run_records/`
- Result narrative: `education_analysis/docs/results/`
