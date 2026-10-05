# Arad and Sibiu: program outcome source check

This offline audit applies the four-county pilot's frozen definition: the highest one or two **distinct cutoff tiers** within each of the original six program subjects, considering only programs with every seat filled. A tie can put multiple programs in a tier. Actual recorded placement is required. The applicant's program preference list is unavailable, so these counts do not measure the institution's applicant-to-seat ratio.

The archived Program Directory identifies programs; the Program Occupancy webpage gives seats, admitted students, vacancies, and the last admitted score. Both counties' program tables balance (seats = admitted + vacancies), and saved local placement rows equal the admitted totals. When a placement row names several possible programs, we compare the top-program yes/no result under *every* possible program code. We never guess a code.

## AR: top 1 cutoff tier(s)

There are **87** listed programs, including **57** fully occupied programs. **6** programs qualify for the specified top tier(s), containing **300** seats. All programs together list **4,310** seats and **3,018** admitted students; the saved local Placement View contains exactly **3,018** rows.

Among **2,947** locally placed applicants from the recovered gymnasium pages, **2,822** connect to one program code. **125** connect to several possible codes: **0** are top-program successes under every possible code, **125** are nonsuccesses under every possible code, and **0** could switch yes/no depending on the code. **0** placements matched no program identity.

## AR: top 2 cutoff tier(s)

There are **87** listed programs, including **57** fully occupied programs. **10** programs qualify for the specified top tier(s), containing **500** seats. All programs together list **4,310** seats and **3,018** admitted students; the saved local Placement View contains exactly **3,018** rows.

Among **2,947** locally placed applicants from the recovered gymnasium pages, **2,822** connect to one program code. **125** connect to several possible codes: **0** are top-program successes under every possible code, **125** are nonsuccesses under every possible code, and **0** could switch yes/no depending on the code. **0** placements matched no program identity.

## SB: top 1 cutoff tier(s)

There are **93** listed programs, including **60** fully occupied programs. **5** programs qualify for the specified top tier(s), containing **250** seats. All programs together list **5,025** seats and **3,276** admitted students; the saved local Placement View contains exactly **3,276** rows.

Among **3,158** locally placed applicants from the recovered gymnasium pages, **2,711** connect to one program code. **447** connect to several possible codes: **0** are top-program successes under every possible code, **447** are nonsuccesses under every possible code, and **0** could switch yes/no depending on the code. **0** placements matched no program identity.

## SB: top 2 cutoff tier(s)

There are **93** listed programs, including **60** fully occupied programs. **10** programs qualify for the specified top tier(s), containing **500** seats. All programs together list **5,025** seats and **3,276** admitted students; the saved local Placement View contains exactly **3,276** rows.

Among **3,158** locally placed applicants from the recovered gymnasium pages, **2,711** connect to one program code. **447** connect to several possible codes: **0** are top-program successes under every possible code, **447** are nonsuccesses under every possible code, and **0** could switch yes/no depending on the code. **0** placements matched no program identity.

## Interpretation

The program and placement source structures support the same *definition* used in the four-county pilot. Any applicants whose possible program codes disagree on the top-program label must remain outside a definite yes/no outcome until resolved or be handled with explicit uncertainty bounds. Capacity is an observed feature of each program, but the number who sought that program is not observed; do not call the observed success fraction the institution's K/N. No HERO curve or causal congestion estimate was produced here.

## Why targeted recovery was needed (before program-page reconciliation)

In **Arad**, the county-wide Placement View prints the same school, technical profile, and technological subject for two programs at Colegiul Economic Arad. The Program Directory distinguishes a **day program** (code `x70`, 125 admitted, cutoff 8.25) from an **evening program** (code `x69`, 25 admitted, cutoff 7.09). The former qualifies for both top-one and top-two under the frozen full-program rule; the latter does not. Before targeted program-page recovery, the missing program code left 149 originating-Arad applicants' labels uncertain. The counts above report the current saved-source result.

In **Sibiu**, three technological programs at Şcoala Naţională de Gaz Mediaş share the Placement View's school, technical profile, and subject. The Program Directory distinguishes **Romanian** (code `x95`, 75 admitted, cutoff 7.84), **German** (code `x93`, 25 admitted, cutoff 6.22), and **Hungarian** (code `x94`, 20 admitted with five vacancies, cutoff 5.91). None qualifies for top one, so the original program ambiguity did not change that outcome. For top two, the Romanian program qualifies while the others do not; before targeted recovery, 114 applicants had uncertain labels. The counts above report the current saved-source result.

The narrow source-recovery target is the archived **program-specific admitted-student webpage** for these five codes. A recovered page must carry the correct source URL code and its student-row count must equal the Program Occupancy admitted count. Only then may we link its printed names and admission scores to the county-wide Placement View. We must not assign a person to a program merely because their score exceeds a cutoff.

## Current closeout result

- AR, top 1: **0 local placement labels still unresolved** under this definition.
- AR, top 2: **0 local placement labels still unresolved** under this definition.
- SB, top 1: **0 local placement labels still unresolved** under this definition.
- SB, top 2: **0 local placement labels still unresolved** under this definition.

Zero unresolved labels closes this particular local-program labeling issue. It does not establish complete eighth-grade cohorts, program preferences, causal identification, or authorize a new outcome analysis.
