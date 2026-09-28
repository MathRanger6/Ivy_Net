# One unresolved construction question for the education panels

**Last synced:** 2026-09-28  
**Status:** Ready for Charles to ask. No message has been sent.  
**Scope:** The two supplied files and all three analysis groups: National Education Longitudinal Study of 1988 (NELS:88), High School and Beyond (HS&B) sophomores, and HS&B seniors.

## Question to ask

Did you or your colleague create, rename, combine, filter, recode, or standardize any columns before giving me these two education data files? If so, could you send me the extraction or construction code and any accompanying notes?

If code is unavailable, the essential substitute is a short mapping that identifies:

- the original National Center for Education Statistics variable or variables behind each renamed or constructed column, especially the performance score, school identifier, education outcomes, and survey weights;
- any student exclusions, cohort restrictions, missing-value treatment, recoding, or imputation applied;
- how the standardized performance score was calculated, including the population used to calculate its mean and standard deviation;
- which students were allowed to enter each school peer group and how the analytic-sample flags were made; and
- whether any outcome described as postsecondary entry was derived from attendance information or inferred from the highest credential attained.

One response may cover both files. Please identify any construction step that differed among NELS:88, the HS&B sophomore cohort, and the HS&B senior cohort.

## Why this is the remaining question

Official National Center for Education Statistics documentation already describes the surveys' samples, follow-up waves, test batteries and published composites, education-attainment categories, survey weights, background variables, and the availability of possible augmentation fields. We can research and cite those matters ourselves.

What public documentation cannot reveal is whether the columns in these particular comma-separated value files are unchanged source variables or locally renamed, combined, filtered, recoded, or standardized versions. The construction code is therefore much more useful than answers to a long questionnaire.

This request asks for provenance of the data already supplied. It does not request additional variables, a new extract, or new analysis.

## Internal interpretation rule

Public documentation supplies plausible source-variable matches, but no match should be treated as confirmed until it is connected to the supplied files. For example, the published NELS first-follow-up standardized test composite combines reading and mathematics; that makes it a plausible source for the supplied performance measure and contradicts the repository's unsupported reading/history description, but it does not by itself prove which variable was exported. Apply the same standard to HS&B test composites, education outcomes, and weights.
