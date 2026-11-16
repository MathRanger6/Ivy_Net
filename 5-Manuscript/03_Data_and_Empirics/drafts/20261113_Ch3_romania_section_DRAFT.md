# Chapter 3 — Romanian high-school admissions (section draft)

NVECTOR | 13 November 2026 | DRAFT for Charles

Section numbers are placeholders until the chapter is assembled.

**OPEN — chapter analysis specification:** Final counties and sample counts; within-county versus cross-county outcome coverage; subject categories, cutoff tiers, and exclusions; primary peer measure; own-performance bands; binning, pooling weights, and uncertainty reporting; and the figures and descriptive conclusions to retain. Existing analyses described below do not settle these choices. No downturn or common cross-domain shape is assumed.

## X.1 Why this system fits

Romanian high-school admissions provide a setting in which individual academic performance, the school environment, and access to educational opportunities can be examined together. The 2001 records identify applicants’ national examination scores, school-awarded grades, originating schools, and subsequent placement into high-school programs. Applicants from the same originating school form an observed peer group, while placement records show who entered programs with high admission cutoffs. These linked records allow us to ask whether applicants with comparable examination performance differ in their likelihood of entering those programs according to the measured performance of the other applicants from their school.

The originating school defines the peer environment, but competition for high-school places extends beyond that school. Applicants from different schools can enter the same destination programs, each of which offers a specified number of places. This separates the group in which academic performance developed from the wider field in which admission is determined. The records therefore connect a local peer environment to an outcome beyond it. They reveal actual placements, however, rather than applicants’ preference lists, so entry into a program with a high admission cutoff measures access to a selective destination, not necessarily receipt of the applicant’s preferred place.

The records also distinguish performance on a national examination from grades awarded within the originating school. Both contribute to the admission score used in allocation, so applicants with comparable examination results can enter the process with different admission scores. This distinction allows us to examine how school-awarded grades and subsequent placement vary across peer environments among applicants with similar examination performance. The examination itself follows years of schooling, however, so it measures achievement after exposure to that environment rather than ability before entering it.

## X.2 How the data were found

Our search began with the public replication files for Pop-Eleches and Urquiola’s study, *Going to a Better School*. Those files contained admission scores and destination-school identifiers, but the released cohort files did not identify applicants’ originating schools or retain examination scores and school-awarded grades separately. They therefore could not support the comparison we needed: students with similar examination performance coming from different school environments.

The original Romanian Ministry of Education reports offered a way to recover those missing connections. Copies preserved by the Internet Archive’s Wayback Machine included applicant lists organized by originating school, county-level admission reports, and records of placement into high schools and specializations. The school-organized reports were particularly important because they identified applicants through the schools they attended before admission. This made it possible to construct the observed peer groups directly from the Ministry records, without attempting to infer originating schools from the anonymous replication files.

We concentrated on the 2001 admission cohort because the recovered reports preserved both components of academic performance alongside the admission composite. The initial reconstruction in Alba County established that applicant and placement reports could be connected within coded originating schools and that the reported scores could be checked across these overlapping sources. That work provided the basis for extending recovery to additional counties, with coverage assessed separately for each report family.

Reconstructing the data required reconciling several views of the same applicants. County lists, school-organized reports, and destination-program lists overlapped, but they did not always contain the same records. In particular, school reports revealed placements outside the originating county that a county-only construction would miss. We therefore used the reports to check one another, retaining unresolved matches explicitly. The resulting peer population consists of observed participating applicants from each originating school; it does not establish coverage of every student who attended that school.

## X.3 Sources and how they were linked

The applicant reports establish who is observed and which originating school each applicant attended. Reports organized by school contain examination scores, school-awarded grades, and admission composites; school directories supply the codes used to distinguish the originating institutions. These reports define the observed population from which peer measures are calculated. County applicant lists provide an additional check on records and coverage, although their geographic scope can differ from that of the school reports.

Placement reports establish what happened to those applicants in the allocation round. School-organized result lists and county admission lists identify destinations, while separate records identify applicants who remained unassigned. For placements outside the originating county, incoming-applicant reports in the receiving county provide a further source of corroboration. An explicit unassigned entry is kept distinct from an unresolved match: failure to locate a destination does not establish that an applicant received no place.

Program reports describe the opportunities into which applicants were placed. Directories identify the destination high school and specialization, while capacity and occupancy tables record offered places, admitted students, and the lowest admitted score. Together, these sources allow observed destinations to be classified by entrance selectivity and checked against reported admissions totals. The lowest admitted score requires particular care when a program has vacancies, because it need not represent a binding threshold imposed by competition for places.

Linking these reports requires agreement across identifying fields rather than reliance on a single universal student identifier. The inspected archives mask the personal identifier, so reconciliation uses originating-school codes, printed names, and admission scores, with score components and destination information providing additional checks where available. Repeated names, conflicting records, and ambiguous program labels are retained for resolution rather than forced into a match. Reports describing the same applicant are treated as overlapping evidence, not as additional people.

## X.4 Cleaning and the final sample

Cleaning preserves a distinction between the applicants who describe a school’s peer environment and those whose outcomes enter a particular comparison. The starting population comes from the originating-school applicant reports, with schools identified by their county and source code. Examination scores are checked for availability, and applicant and placement records are reconciled against the corresponding source reports. Conflicting or incomplete records require resolution before they can support the affected comparison.

Peer measures are calculated before restricting the applicants whose placement outcomes are analyzed. In the existing leave-one-out analyses, each applicant’s peer mean uses the examination scores of the other observed applicants from the same originating school. An applicant with no observed school peer cannot enter that comparison. Applicants excluded from an outcome analysis can nevertheless remain part of their school’s observed peer environment, and restricting attention to a band of individual performance does not redefine that environment.

The outcome denominator depends on the geographic question being asked. The within-county analyses exclude applicants placed outside their originating county from the outcome denominator while retaining them as peers. Confirmed unassigned applicants remain in the denominator. A separate comparison follows placements both within and beyond the originating county, requiring sufficient destination information to classify the outcome. These designs answer different questions and therefore require separate accounts of their exclusions and final sample sizes.

An uncertain destination label does not always imply an uncertain outcome. Several program codes may remain consistent with a reported placement, yet all may fall on the same side of the chosen selectivity criterion. In that case, the binary outcome can be classified even though the exact program remains unresolved. Where the possible destinations imply different classifications, the outcome remains uncertain. This distinction preserves usable information while keeping uncertainty about program identity separate from uncertainty about selective placement.

**TK — final sample counts and sample-flow table:** Left open at Charles’s request. Populate from the selected chapter analysis once its geographic scope, outcome definition, and exclusions are settled.

## X.5 The four concepts

Individual performance is measured by the applicant’s national examination score. The school-awarded grade average and admission composite are retained as separate quantities because they describe different parts of the transition into high school. Comparing applicants within examination-score bands allows us to examine differences in grades and placement among students with broadly similar measured achievement. The width of each band determines how closely that comparison holds examination performance constant.

The group is the set of observed applicants from the same originating school in the 2001 admission cohort. School codes are interpreted within their county, so identically numbered schools in different counties remain distinct. This definition locates the peer environment before high-school placement. It represents the participating applicants recovered from each school, whose coverage may differ from the school’s complete graduating cohort.

Peer context is measured through the examination performance of those applicants. The full-group mean describes the average performance of the observed school cohort, including the focal applicant. The leave-one-out mean describes the other applicants from that school and can therefore differ between individuals in the same group. Both measures appear in the existing Romanian comparisons. Keeping them distinct allows us to compare a shared school characteristic with the academic environment surrounding a particular applicant.

Advancement is defined as actual placement in a designated set of selective high-school programs. The existing analyses identify these programs through admission-cutoff tiers within county and subject category, comparing entry into the highest tier with entry into the highest two tiers combined. Under the full-occupancy specification, only programs that filled their offered places qualify for this ranking. The outcome therefore records access to a specified selective destination; the geographic coverage, subject categories, and number of included tiers determine which opportunities count.

## X.6 What this system cannot give us

The comparisons describe associations between school environments and subsequent placement, but do not identify the causal contribution of peers. Students attending different originating schools may also differ in family circumstances, geography, educational preferences, and prior achievement. Comparing applicants with similar examination scores narrows one measured difference without making their circumstances equivalent. Because the examination follows years of schooling, this comparison also cannot recover the full developmental contribution of the school environment.

The reconstructed peer groups represent observed admission applicants rather than complete school cohorts. Students who did not participate in the recorded allocation round, followed another educational route, or were absent from the surviving reports may be missing. Such omissions could change both the measured composition of a school and the applicants represented in its placement rate. Conclusions therefore apply to the recovered applicant populations and covered locations; broader coverage requires separate evidence.

The absence of preference lists limits what placement can reveal about competition. An applicant who entered a less selective program may have preferred its subject, location, or other characteristics. The records cannot establish that every applicant sought a place in the programs designated as successful destinations. Consequently, even where program capacities are known, the observed success rate does not identify the ratio of available places to the applicants who actually competed for them.

Admission cutoffs measure realized entrance selectivity rather than educational quality or later benefit. A high cutoff identifies a program entered by applicants with high admission scores, but does not establish how much that program improves learning or subsequent opportunities. Rankings defined within county and subject category are also relative to those settings: the highest-ranked programs in two counties need not have equal cutoffs. The outcome examined here is access to a specified selective destination in the recorded admission round, not the longer-term consequences of attending it.

## X.7 Descriptive results

The descriptive comparisons begin with the relationship between an applicant’s own examination performance and selective placement. Applicants are grouped by examination score, and the proportion entering the designated programs is calculated within each group. This establishes how closely the measured performance used throughout the analysis corresponds to the advancement outcome.

**[OPEN: Select the own-performance figure, confirm its sample and outcome definition, and describe the observed relationship with counts and uncertainty.]**

The next comparison examines placement rates across school peer environments. Using the same outcome definition and eligible applicants allows this relationship to be read alongside the own-performance comparison. The distinction matters because an overall association between peer performance and placement can also reflect differences in the examination performance of the applicants attending those schools.

**[OPEN: Select the primary peer measure and matching figure. Specify binning and pooling weights, then report the observed pattern without presuming a downturn.]**

Comparisons within examination-score bands then examine whether applicants with similar measured achievement have different placement rates across peer environments. Each band provides a separate view of that relationship, allowing its shape and magnitude to differ across levels of individual performance. Applicant and school counts are needed alongside these comparisons, particularly where few observations support the extremes of the peer distribution.

**[OPEN: Select the performance bands and corresponding figures. Report the supported differences, their uncertainty, and any sensitivity to the peer measure or sample definition.]**
