# Assortativity investigation — experiment choices and their reasons

**Last synced:** 2026-09-25  
**Status:** Living record of Charles's design decisions and VECTOR's explanations. Documentation is authorized. The analytical implementation and experiment have not been authorized or executed. Remaining choices are listed explicitly below.

## 1. Purpose and how to read this document

This document records the decisions made as Charles and VECTOR design the first assortativity investigation. It explains what each choice means, why it was made, what it holds fixed, and what it allows us to conclude. Numerical examples are teaching examples, not results from the basketball data.

The starting question is whether a preference for joining similar-ability teammates is necessary for congestion to change who receives a scarce advancement opportunity. A related question is whether the answer depends on how few opportunities are available. Producing the particular observed basketball outcome curve is a further requirement; changing some winners alone would not establish that empirical explanation.

The original scientific brief supplies the broader scientific motivation and proposed outcome measures. This decision record supplies the subsequent choices made in our September 25 conversation. When an earlier proposal differs from a decision recorded here, the difference is stated explicitly rather than silently erased. A design choice is not permission to begin coding or run an experiment.

## 2. Language and explanations

Charles requests detailed explanations and welcomes verbosity in these documents. Explain the idea in ordinary language before presenting equations. Include brief examples where helpful, and distinguish an illustrative example from a measured finding.

Unless Charles has himself used a shorthand expression, write the full term followed by the proposed shorthand in parentheses. Continue doing this on subsequent uses until Charles uses the shorthand himself. VECTOR introducing or defining an abbreviation does not establish that Charles has adopted it. Familiarity with one expression does not imply familiarity with a related expression.

For equations, explain each symbol in words when it is introduced in a section. Present one necessary question at a time during the design discussion. Multiple-choice questions are useful when their alternatives are genuinely different scientific choices.

## 3. Population: one frozen 2015 basketball panel

**Charles's decision:** begin with the 2015 men's basketball player panel and its corresponding observed team roster capacities.

Each player keeps the same identity and measured ability throughout the experiment. The collection of team capacities also stays fixed. Assignment changes which players occupy those team seats. We are not drawing a new population of abilities whenever we change a model setting.

The purpose is to understand the mechanism on one fixed population before introducing differences between seasons. A finding in 2015 would not, by itself, establish the same finding in other seasons or other domains.

Ability will use player-season points per minute constructed afresh from the frozen game-level box data and then standardized for the experiment as specified below. Existing exported panels remain historical comparison artifacts and will not supply the experimental population.

**September 25 historical-review clarification:** Charles described how one-game opponent appearances entered as apparent seasons and how excluding them changed the empirical curve. The [data hygiene and model-history review](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260925_SCOUT_data_hygiene_and_model_history.md>) records the coverage rule, its evolution, the separate individual minutes floor, and the original reasoning. The governing coverage, minutes, source-build, and canonical-team choices are now recorded below; the final eligible population remains subject to confirmation by the separately authorized rebuild. Selecting 2015 did not approve a particular saved export.

The adopted coverage rule retains team-seasons with at least eleven captured games. The adopted individual minutes floor is twenty total observed season minutes, with lower-minute players removed rather than assigned zero points per minute. The history contains an earlier dropping-versus-zeroing exchange, which is preserved as history rather than treated as the current rule. VECTOR's earlier explanation of the six old two-player teams was too definite: their individual provenance has not been reconstructed.

### Team-season coverage rule

**Charles's decision for the new experiment:** include a 2015 team-season only if the preserved box-score extract contains at least eleven distinct captured games for that team-season. In the historical configuration language, set the minimum-team-season-games threshold to ten and retain only counts strictly greater than ten. Dash-name placeholder records are removed before the captured-game count.

This is a team-season coverage rule. It does not require every player to appear in eleven games, prove that the extract contains the team's full schedule, or independently establish Division I membership. Its purpose is to exclude fragmentary environments that cannot defensibly represent a season. Because included teams define the observed capacity multiset and fixed congestion reference, the same eligibility rule must govern both.

The historical record now supplies the missing decision sequence. Six captured games was the first working rule. Charles then asked what would happen under the stricter eleven-game rule; the archived comparison reported twenty-three additional team-seasons removed and no additional drafted player-season loss. Charles replied, “I think we should go with 10 to get real seasons,” where ten was the configuration threshold retaining eleven or more captured games. The [SCOUT response](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260925_SCOUT_response_data_hygiene_and_model_history.md>) and [COMPASS addendum](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260925_COMPASS_addendum_data_hygiene_and_model_history.md>) describe the campaign history; the [archived decision exchange](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/.specstory/history/2026-06-11_08-19-11-0400-compass.md:215669>) is the primary decision evidence. The saved before-and-after curve pair compares no coverage filter with eleven games, not six games with eleven.

### Individual minutes eligibility

**Charles's decision for the first experiment:** include only players with at least twenty total captured minutes during the 2015 season. A player below that floor is excluded from the assignment population, the observed roster capacity assigned to their team, the calculation of teammate environment and congestion, and every outcome readout.

Twenty means accumulated captured minutes for the player-season-team record, not twenty minutes per game and not twenty game appearances. The purpose is to avoid treating a scoring rate based on extremely limited exposure as a sufficiently supported ability measurement. The resulting capacity is therefore the number of **eligible analytical players** on the observed team, not the institution's complete listed roster.

The zero-points-per-minute construction remains historical evidence and a possible later sensitivity analysis. It is not used in the first experiment because assigning zero points per minute is a substantive ability assumption. Zero is not a neutral representation of missing or weakly observed performance; it would also change team composition, teammate averages, and congestion.

### Unique athletes and canonical 2015 team

**Charles's decision:** each athlete enters the frozen 2015 assignment population exactly once. Before player-season aggregation, assign each athlete to the team for which the frozen game file contains the greatest number of distinct 2015 game records. Use total minutes as the tie-breaker. If both quantities remain tied, stop and report the athlete for manual review; do not choose a team silently. Remove the athlete's rows assigned to other teams, and preserve an audit of every removed athlete-team record.

This rule responds to a verified 2015 source anomaly rather than an abstract transfer problem. A read-only audit found 27 athlete-game combinations recorded under both opposing teams, all concentrated in two games and all carrying duplicated statistics or duplicated blank roster entries. After applying the eleven-captured-game team rule and twenty-total-minute player-team rule, the provisional table contained 4,270 player-team rows but only 4,266 unique athletes. The four extra rows were High Point players copied to Arkansas–Pine Bluff in their November 15, 2014 game: Brian Richardson, Devante Wallace, Lorenzo Cugini, and Adam Weary. The duplicated rows gave Arkansas–Pine Bluff 18 apparent eligible players instead of 14. Each athlete had far more rostered games and minutes with High Point, so the canonical-team rule removes the four false Arkansas–Pine Bluff records while retaining the High Point records.

The other duplicated game was Auburn versus Tulsa. Its incorrect opposing-team records did not produce another athlete with two eligible team records after the twenty-minute rule. The audit found no genuine eligible 2015 same-season transfer requiring two assignment units. This canonical-team decision is therefore a bounded 2015 data-quality rule. It must not be generalized to erase genuine transfers in other seasons without a separate investigation.

### Ability source and standardization

**Settled standardization decision:** after applying the eleven-captured-game team rule and twenty-total-minute player rule, standardize the accepted points-per-minute values once across the final eligible 2015 population using the population standard deviation.

**Settled source decision:** rebuild the 2015 player-season input from the frozen game-level box data. Repository inspection and SCOUT's updated reconciliation establish three separate layers: the game-level source contains points and minutes but no points-per-minute column; panel construction sums retained points and minutes at the player-season-team level and calculates points per minute once; downstream analysis copies that stored column into the performance variable rather than dividing again. Existing exported panels may be used only for provenance comparisons and must not supply the new experimental population.

The exact construction order is: apply game-level quality-control rules; resolve every athlete to one canonical 2015 team using the documented rule; aggregate retained game rows into player-season point and minute totals; calculate points per minute as total points divided by total minutes, assigning a missing value when total minutes equal zero; remove player-season rows below the twenty-total-minute eligibility floor; freeze the eligible 2015 population; and standardize its accepted points-per-minute values. The minimum-minutes rule removes entire player-season rows after the rate is calculated. It does not alter the rate of a player who remains eligible.

Let $r_i$ denote the accepted points-per-minute value for eligible player $i$. Let $N$ be the number of eligible 2015 players, let

$$
\mu_A=\frac{1}{N}\sum_{i=1}^{N}r_i,
$$

and use the population standard deviation

$$
s_A=\sqrt{\frac{1}{N}\sum_{i=1}^{N}(r_i-\mu_A)^2}.
$$

The experiment's standardized ability is

$$
A_i=\frac{r_i-\mu_A}{s_A}.
$$

This makes the final fixed population's mean ability zero and its population standard deviation one. Standardization occurs after both eligibility rules, so excluded teams and players do not influence the ability scale.

Before execution, the implementation specification must still verify identifier integrity, the exact canonical-team audit fields, missing or zero minutes, and the remaining game-level quality-control operations. A comparison with a saved panel may test lineage or reveal stale filters, but it is diagnostic evidence only. No existing panel, source, or calculation may be substituted silently.

**Fresh-output preference:** Charles prefers a fresh investigation with its own derived inputs and results. Existing sweeps and generated roster files serve only as historical evidence. Do not use them as experimental inputs, resume them, or overwrite them. Candidate preserved source extracts and any reusable code components must be identified and reviewed separately; constructing new analytical inputs or executing code still requires authorization.

## 4. Repetition: 100 paired assignment repetitions

**Charles's decision:** start with 100 repetitions of the assignment comparison.

For each repetition, create one assignment without similarity preference and one assignment with similarity preference. Thus, the design calls for 100 pairs of assignments, or 200 assignments in total. The same assigned rosters are then reused for the scoring and selection comparisons described below.

These repetitions describe variation from the assignment process for the fixed 2015 population. They are not 100 independently observed basketball seasons. More repetitions can improve the precision of the simulation averages without expanding the population to which the findings apply.

**Charles's seed decision:** use `20260925` as one declared master seed and derive 100 distinct, recorded repetition seeds from it. Within each repetition, initialize the two assignment-preference conditions from the same repetition seed so that they receive the same random player order and corresponding underlying choice sequence. Save the master seed, derivation method, and all repetition seeds with the eventual run record.

The seed is a transparent reproducibility choice based on the decision date, not a parameter chosen after inspecting results. Reusing a repetition seed does not force identical rosters: the two assignment-preference settings attach different probabilities to the coupled random choices. Congestion, scaling, and selection comparisons reuse each resulting roster and introduce no further random draw.

## 5. Assignment preference: rho equal to zero versus one

**Charles's decision:** compare the assignment-preference parameter ($\rho$) at zero and one, using the Levine–Gates assignment mechanism.

At $\rho=0$, ability similarity does not affect a player's placement probabilities. A team with more remaining seats has a proportionally larger chance of receiving that player. Assignment is uniform over the remaining seats; teams need not have equal probabilities.

At $\rho=1$, the player prefers teams whose current average ability is closer to their own, while remaining capacity still matters. The receiving team's average updates as players join it.

Random assignments can produce differences between team averages even at $\rho=0$. Therefore, zero preference does not mean every team has identical ability or that measured sorting must be exactly zero. We will distinguish the rule governing assignment from the sorting that happens to result.

## 6. Shared randomness: compare conditions under matched circumstances

**Charles's decision:** within each repetition, use the same player arrival order and the same underlying random draws for the two assignment-preference conditions, wherever the implementation allows this without changing either condition's intended probabilities.

Imagine dealing the same list of arriving players twice. On the first deal, team probabilities depend only on open seats. On the second, similarity also matters. Reusing the underlying random numbers does not require placing each player on the same team: the probabilities to which those numbers are applied differ.

This procedure is called using common random numbers. It preserves stochastic assignment in each condition and can make the difference between conditions easier to estimate. It does not remove randomness from the model, and it is not guaranteed to reduce uncertainty for every outcome. The pairing and its implementation must be checked.

**Charles's related decision:** reuse each assigned roster across both congestion settings, both selection fractions, and both congestion-scaling versions. A change in a scoring parameter must not quietly trigger a new roster draw.

## 7. Congestion weight: lambda equal to zero versus one

**Charles's decision:** compare the congestion-weight parameter ($\lambda$) at zero and one.

Write a player's ability as $A_i$, and the raw congestion of that player's assigned team as $C_{g(i)}$. The notation $g(i)$ identifies the team containing player $i$. With raw congestion, the score is

$$
S_i=A_i-\lambda C_{g(i)}.
$$

At $\lambda=0$, the score is ability alone. At $\lambda=1$, raw team congestion is subtracted from ability. These are declared scenario settings, not fitted real-world parameter estimates.

For example, ability of 1.2 and raw congestion of 0.2 yield a score of 1.0 when $\lambda=1$. The size of that subtraction depends on the congestion scale, which is why the scaling decision in Section 11 matters.

## 8. Selection scarcity: one percent versus ten percent

**Charles's decision:** begin with selection fractions of 1% and 10%.

The number of eligible players is $N$, and the number of available slots is $K$. The ratio $K/N$ describes the fraction selected. With 1,000 eligible players, these settings would mean selecting 10 or 100 players. With the actual panel, integer rounding must be specified and the achieved fraction recorded.

Charles explicitly noted that many domains select more than 10%. Accordingly, 10% is an initial comparison point, not an upper limit on the model or a representative rate for every domain. A later investigation may need higher fractions. The 1% scenario is also not a verified estimate of annual draft eligibility and selection in the supplied panel.

**Charles's rounding decision:** multiply the target selection fraction by the final eligible population size and round to the nearest whole number. If the unrounded result is exactly halfway between two integers, round upward. Record both the resulting number of slots and the achieved selection fraction in every experiment record.

For the currently audited population of 4,266 eligible athletes, the 1% target gives $42.66$ and therefore $K=43$; the 10% target gives $426.6$ and therefore $K=427$. The achieved fractions are approximately $1.007\%$ and $10.009\%$. These counts remain contingent on the final authorized rebuild confirming $N=4{,}266$; the rounding rule, rather than hard-coded counts, is authoritative.

## 9. Viability: a fixed threshold and a fixed transition sharpness

**Charles's decision:** hold the viability threshold ($\theta$) at the 99th percentile of the frozen 2015 ability distribution and hold the transition-sharpness parameter ($\gamma$) at 10.

Calculate the 99th percentile using linear interpolation between the two neighboring ordered ability values when the percentile position is not an integer. This is the conventional current pandas and NumPy linear quantile rule. It treats standardized ability as continuous and prevents the threshold from jumping arbitrarily to one observed player. The calculation method must be recorded explicitly with the resulting threshold value.

The interpolated threshold does not need to leave exactly 1% of players strictly above it. Its job is to locate the midpoint of the smooth viability transition; the number of advancement winners is determined separately by $K$. This distinction keeps the viability definition separate from the selection rule.

Each player's contribution to congestion is a smooth value between zero and one:

$$
v_h=\frac{1}{1+\exp[-\gamma(A_h-\theta)]}.
$$

Here $v_h$ is player $h$'s viability contribution. A player exactly at the threshold contributes 0.5. Players far below it contribute close to zero; players far above it contribute close to one. The transition-sharpness parameter controls how abruptly those contributions change around the threshold.

**Charles's decision:** use one shared team-level congestion measure calculated over every eligible member of the assigned roster, including the focal player:

$$
C_j=\frac{1}{n_j}\sum_{h\in j}v_h.
$$

Here $n_j$ is team $j$'s eligible analytical roster size. Every member of a particular team receives the same congestion value. The repository implementation supports this definition through the `crowding_smooth_team` mode; the current gallery configuration calls it `team_smooth` and makes it the default. The implementation also contains a legacy leave-one-out congestion option, but that option is not part of the primary experiment.

This choice preserves congestion as a property of the shared team environment. For a simple hard-threshold illustration, suppose four of ten players are viable. Full-team congestion is $4/10=0.40$ for every player. If the focal player were removed from their own calculation, a viable player would receive $3/9\approx0.33$, while a nonviable player would receive $4/9\approx0.44$. Players on the same team would therefore receive different congestion penalties partly because of their own viability. That is a substantive change to the scoring mechanism, not a mathematically equivalent way to calculate the same team quantity.

Leave-one-out teammate quality remains a distinct empirical measure that may be used on an outcome curve's horizontal axis. It must not be substituted for the shared congestion term entering the score. Leave-one-out congestion is reserved as a possible later sensitivity analysis only if the primary findings or a specific scholarly concern make it necessary; it will not enlarge the main design automatically.

Holding the threshold fixed means the definition of a viable peer is unchanged when we move from selecting 1% to selecting 10%. We can then attribute the intended selection-capacity change to the number of slots, without simultaneously changing how congestion is constructed.

The alternative was to move the threshold from the 99th to the 90th ability percentile when selection expands. That would change both the scoring ingredients and the selection capacity. Charles chose to postpone evaluating that coupled formulation.

The limitation is deliberate: the 10% condition still uses the stringent 99th-percentile viability threshold. This is a controlled mechanism comparison, not a final formulation for all domains.

## 10. Winner rule: exactly the highest K scores, without clipping

**Accepted working selection rule:** calculate scores, rank all eligible players, and take exactly the highest $K$. Do not replace negative scores with zero or exclude players solely because their scores are negative. There is no extra random selection draw after scoring in this first experiment.

For example, if three slots are available and scores are 2.1, 0.4, -0.2, -1.0, and -3.2, the first three players are selected. The negative score of the third player does not leave a slot empty.

**Charles's explicit tie decision:** break exact score ties by ascending frozen player identifier: the alphabetically or numerically lower identifier ranks first. The same fixed order applies to every condition and repetition. Before execution, verify that the identifier is nonmissing and uniquely defines every player in the frozen panel, and record whether its stored type requires numeric or text ordering. If identifier integrity fails, stop and report the problem rather than silently using row order or another field.

Stochasticity remains in assignment. For any one completed assignment, scoring and selection are deterministic. A later test of random selection would be a separately specified experiment.

Two expected checks follow. First, when congestion is turned off, the selected players at a given slot count must be identical across assignments. Second, changing the slot count alone must not change anyone's score or rank. It changes how far down the existing ranking selection extends.

## 11. Congestion scaling: compare raw values with one fixed standardization

**Charles's decisions:** compare raw congestion with a scaled version; for the scaled version, use one reference mean and standard deviation held fixed across all assignment conditions and repetitions. Calculate that reference distribution from the observed 2015 team assignments.

The raw version remains

$$
S_i^{\mathrm{raw}}=A_i-\lambda C_{g(i)}.
$$

For the standardized version, let $\mu_{C,\mathrm{ref}}$ be the reference mean congestion and $s_{C,\mathrm{ref}}$ its positive standard deviation. Then

$$
Z_{C,i}^{\mathrm{ref}}=
\frac{C_{g(i)}-\mu_{C,\mathrm{ref}}}{s_{C,\mathrm{ref}}},
\qquad
S_i^{\mathrm{standardized}}=A_i-\lambda Z_{C,i}^{\mathrm{ref}}.
$$

The same two reference numbers must be used for every assignment-preference condition, congestion weight, selection fraction, and repetition. Congestion in a new condition is expressed in units of the reference spread; it need not itself have mean zero or standard deviation one in that condition.

### Why use the same measuring stick?

Consider a hypothetical comparison. With no similarity preference, mean congestion is 0.10 and the standard deviation is 0.01. A team at 0.11 is one standard deviation above that mean. With positive similarity preference, suppose mean congestion remains 0.10 but the standard deviation is 0.10. A team at 0.20 is now one standard deviation above its condition's mean.

If each condition is standardized separately, both teams receive a standardized congestion value of +1. The penalty treats those two deviations as equal even though the second raw deviation is ten times larger. This would change the effective penalty strength between assignment conditions, potentially concealing variation created by assignment itself.

With a common reference mean of 0.10 and standard deviation of 0.05, the two hypothetical teams instead receive standardized values of 0.2 and 2.0. Their differences are measured on one common scale. These example numbers have not been calculated from the real panel.

### What centering does, and what scaling does

Subtracting one common mean raises every score by the same amount after the congestion penalty is applied. It does not change rankings or exact top-$K$ winners. Below-average congestion appears as a score bonus, but the common centering does not itself change who wins.

Dividing by a standard deviation changes the strength of differences in congestion relative to differences in ability. Algebraically,

$$
S_i^{\mathrm{standardized}}
=A_i-\frac{\lambda}{s_{C,\mathrm{ref}}}C_{g(i)}
+\frac{\lambda\mu_{C,\mathrm{ref}}}{s_{C,\mathrm{ref}}}.
$$

The last term is identical for everyone. For this winner rule, the standardized version therefore produces the same ranking as the raw formula with an effective congestion weight of $\lambda/s_{C,\mathrm{ref}}$.

This corrects an earlier oversimplification in our discussion: a fixed rescaling is another penalty-strength choice, not an independent congestion mechanism. Comparing the versions assesses sensitivity to that strength. Agreement between them does not establish robustness to every possible scaling or congestion weight.

At $\lambda=1$, one reference standard deviation of extra congestion subtracts one ability-score unit. Interpreting that unit as exactly one standard deviation of the final analysis sample depends on verifying the ability standardization and filtering described in Section 3.

### Earlier options and what remains unresolved

The discussion previously considered multiplying congestion by the 90th-minus-10th percentile spread of ability, multiplying by the ability standard deviation, or matching existing code. None of those was selected as an additional experimental version. The latest adopted direction is raw congestion alongside fixed-reference standardization of congestion itself.

Read-only inspection of the existing scoring utility found that its automatic scale is the 90th-minus-10th percentile spread of ability, with a fallback of 4.0. That is not congestion z-scoring and must not silently run on top of the agreed standardization.

### Why use the observed 2015 team assignments as the reference?

The observed 2015 assignments provide an empirical measuring stick that is external to the simulated experimental conditions. Under this choice, one standardized unit means one standard deviation of congestion in the observed 2015 basketball setting. The reference mean and standard deviation will be calculated once and will not change when assignment preference, congestion weight, selection scarcity, or the repetition changes.

This choice avoids allowing either the no-assortative-preference simulation or the combined simulated treatments to define the units by which their own results are evaluated. It also gives the units a concrete interpretation tied to the basketball data.

The observed assignments are not theoretically neutral. They reflect many real forces beyond the assignment mechanism represented in the experiment. We are using them to define a stable empirical scale, not claiming that they were generated by the model or that they represent assignment without assortative preference.

### Why give every player equal weight?

**Charles's decision:** give every player in the observed 2015 population equal weight in the fixed congestion reference distribution.

Congestion is calculated at the team level, but it enters the score of every player assigned to that team. Equal-player weighting therefore treats congestion as an exposure experienced by individuals. If team $j$ has $n_j$ players and team congestion $C_j$, its congestion value contributes $n_j$ observations to the reference distribution. The reference mean is

$$
\mu_{C,\mathrm{ref}}=
\frac{\sum_j n_j C_j}{\sum_j n_j}.
$$

For a simple example, suppose a five-player team has congestion of $0.20$ and a fifteen-player team has congestion of $0.80$. Equal-player weighting gives

$$
\frac{5(0.20)+15(0.80)}{20}=0.65.
$$

Equal-team weighting would instead produce $(0.20+0.80)/2=0.50$. That answer describes the average team, but it gives the five-player and fifteen-player teams the same influence even though the second team's congestion enters three times as many individual scores.

Equal-player weighting fits this experiment because selection and advancement are individual outcomes, the congestion penalty is applied to individual scores, and larger teams expose more individuals to their team congestion. Team-level summaries can still be reported as descriptive information, but they will not define the standardization used in player scoring.

### Why use the population standard deviation?

**Charles's decision:** calculate the spread using the population standard deviation of the equal-player-weighted observed 2015 reference distribution.

Let the total number of observed 2015 players be $N=\sum_j n_j$. The fixed reference standard deviation is

$$
s_{C,\mathrm{ref}}=
\sqrt{
\frac{1}{N}
\sum_j n_j\left(C_j-\mu_{C,\mathrm{ref}}\right)^2
}.
$$

Equivalently, every player receives their observed team's congestion value, and the squared differences from the equal-player-weighted mean are averaged across all $N$ players before taking the square root.

The population formula divides by $N$. The sample standard deviation would divide by $N-1$. We selected the population formula because the observed 2015 players included in the frozen reference panel are the complete fixed population whose congestion scale we intend to describe. We are not using those players as a random sample to estimate the spread of a larger hypothetical population. With many players, the numerical difference between the two formulas would likely be small, but fixing the convention prevents software defaults from changing the scale silently.

### Mandatory response to an exactly zero reference spread

**Charles's decision:** before any simulation or scoring begins, require a check that the reference population standard deviation is greater than zero. If it is exactly zero, stop and report the problem without substituting a fallback value, switching silently to raw congestion, or dropping the standardized comparison.

An exactly zero standard deviation means that every player in the observed 2015 reference population has the same congestion value. The standardized expression would require division by zero and would therefore be undefined. It would also mean that the chosen reference population contains no congestion variation from which to construct a standardized scale.

The stopped process must preserve and report the calculated reference mean, the zero standard deviation, and diagnostic information needed to understand why there is no spread. Any change to the reference population or removal of the standardized comparison must return to Charles and VECTOR as a scientific design decision; software must not make that decision automatically.

### Mandatory response to an extremely small positive reference spread

**Charles's decision:** because the congestion measure is theoretically bounded between zero and one, use $10^{-8}$ as a fixed numerical threshold. If the reference population standard deviation satisfies

$$
0<s_{C,\mathrm{ref}}\leq10^{-8},
$$

stop before simulation or scoring, report the problem, and use no automatic fallback. The same prohibitions adopted for an exactly zero spread apply: do not replace the spread with the threshold, do not substitute another constant, do not switch silently to raw congestion, and do not drop the standardized comparison.

This threshold protects against numerical instability. It is not a claim that congestion differences below $10^{-8}$ are scientifically unimportant, nor is it an effect-size threshold. With such a small denominator, numerical noise or rounding differences could become large standardized penalties and could determine rankings.

Whenever the reference spread exceeds the threshold, the record for the future experiment must still report both the actual reference population standard deviation and the implied raw-scale multiplier

$$
\frac{1}{s_{C,\mathrm{ref}}}.
$$

For example, if $s_{C,\mathrm{ref}}=0.05$, the multiplier is $20$. A raw congestion difference of $0.05$ then equals one standardized congestion unit. Reporting the multiplier makes the strength of the standardized scoring rule visible rather than hiding it inside the transformation.

## 12. Primary outcome: changes in who is selected

**Charles's decision:** the primary outcome is how many selected players are replaced when congestion is switched on. Curve shape is a separate diagnostic and is not the success criterion for the experiment.

For a fixed assignment, selection fraction, and congestion representation, let $W_0$ be the set of players selected when the congestion weight is zero and let $W_1$ be the set selected when the congestion weight is one. Both sets contain exactly $K$ players. The displacement count is

$$
D=|W_0\setminus W_1|=|W_1\setminus W_0|.
$$

The equality holds because the two winner sets have the same size: every player displaced from the ability-only winner set is replaced by one player entering under congestion. Also report the displacement fraction

$$
d=\frac{D}{K}.
$$

For example, if $K=43$ and six ability-only winners lose their places when congestion is turned on, then $D=6$ and $d=6/43\approx 0.140$, or approximately 14 percent. This measures a real change in advancement even if the plotted outcome curve is monotonic, flat, or otherwise unlike the empirical basketball curve.

Calculate displacement separately for each assignment-preference condition, each selection fraction, and each congestion representation. Across the 100 paired assignment repetitions, report the mean, median, observed range, and proportion of repetitions with any displacement. Also report the paired difference in displacement between the two assignment-preference conditions.

**Charles's decision on interpretation:** do not impose an arbitrary numerical threshold for declaring displacement meaningful or negligible. Report the observed count, fraction, distribution, and paired contrast transparently. The reason is that a researcher-chosen cutoff could turn an otherwise descriptive mechanism test into another adjustable parameter and could encourage a preferred conclusion. A zero result, a very small result, and a large result should remain visibly different findings rather than being forced through an unsupported binary rule. Scientific interpretation will consider the magnitude, consistency across repetitions, and differences across the prespecified conditions.

Across repetitions, also report the central 95% simulation range, defined by the 2.5th and 97.5th percentiles. This range describes variation across the 100 randomized assignments; it is not a population confidence interval and must not be labeled as one.

Outcome curves remain secondary evidence. For this first experiment, divide each assigned roster population into sixteen equal-count bins ordered by leave-one-out mean teammate ability. Use the frozen player identifier to order exact peer-quality ties before assigning bin positions. Freeze each repetition's bin membership across congestion weights, selection fractions, and congestion representations; display the actual mean leave-one-out teammate ability and mean selection rate in every bin. Average the bin-level selection rates across the 100 repetitions and display their central 95% simulation ranges.

Call this a **simulated assignment-outcome diagnostic**, not a reproduced HERO. Sixteen bins preserve the existing visual resolution and can reveal a localized right-tail dip that five quintile bins could hide. Do not fit a quadratic regression, estimate a turning point, or formally classify an inverted-U in this first experiment. Winner displacement answers whether congestion changes advancement under the specified mechanism. Reproducing the empirical HERO is a later, stronger task requiring a matched population, outcome, horizontal axis, and binning procedure.

## 13. How the comparisons fit together

The original brief proposed eight combinations: two assignment-preference settings, two congestion weights, and two selection fractions. We now retain those eight labeled combinations for each of two congestion representations: raw and fixed-reference standardized.

That creates sixteen labeled comparisons per repetition, but they are not sixteen independent experiments. In particular, the raw and standardized versions coincide when congestion is turned off. Their ability-only baseline should be shared and must not be counted as independent evidence twice.

The same 200 assignments described in Section 4 support both representations. No additional assignment draw is needed merely because we change how a fixed roster's congestion enters scoring. Apply the proposed winner-displacement and curve diagnostics separately to each representation; do not pool the versions into one undifferentiated result.

## 14. Remaining choices and verification before execution

1. Translate the settled rebuild-from-box, canonical-team, and shared full-team congestion choices into a fully auditable construction specification, then complete the capacity audit. Coverage, minutes eligibility, unique-athlete treatment, points-per-minute construction, post-eligibility standardization convention, and inclusion of the focal player in congestion are settled. Documentary agreement does not authorize executing the panel rebuild.
2. Translate the settled master-seed and paired-assignment rule into the implementation specification and verify that the chosen assignment routine consumes the coupled random sequence consistently. The fixed threshold uses linear interpolation for the 99th percentile, and nearest-integer slot rounding with exact halves rounded upward is settled.
3. Implement the settled reporting specification exactly: unbinned winner displacement is primary; central 95% simulation ranges summarize repetition variation; and sixteen-bin simulated assignment-outcome curves are secondary diagnostics without quadratic fitting, turning-point estimation, or formal inverted-U classification. The earlier brief's proposed numerical tolerances are superseded for the primary displacement outcome.
4. Finalize the experiment plan with the exact files, held-fixed quantities, manipulated quantities, possible-result interpretations, and provenance protections. Obtain explicit authorization before creating analytical code or executing the experiment.

## 15. Storage and authority

All newly created investigation material belongs under the existing `assort_analysis/` workspace. General Markdown belongs under `docs/`; code, notebooks, data, and outputs have their approved separate folders. Existing repository sources remain in place. The earlier working brief remains outside the investigation folder as a historical and scientific reference, with a pointer to this decision record.

Charles authorized creation of the directory structure and orientation file. He has now explicitly requested ongoing detailed documentation of our choices. Those permissions do not authorize analytical code, data transformations, figure generation, or experiment execution.

## 16. Sources and revision history

**Decision source:** Charles's September 25 conversation with VECTOR. Accepted choices above reflect his individual answers; explanations and mathematical implications are VECTOR's reasoning. Unresolved questions and implementation checks have not been promoted to decisions.

**Scientific starting point:** `VECTOR_PD41_Assortativity_Scientific_Brief.md` in the parent VECTOR documentation workspace. The September 24 proposal remains the source for broader motivation, Army comparisons, unresolved calibration issues, and proposed outcome diagnostics.

**Implementation evidence inspected without execution:** `sports/scripts/grandchild_selection_inverted_u_diagnostic.py`, particularly the preparation settings requesting within-season ability standardization; and `sports/tier1_pool_assignment.py`, functions `default_crowding_l_z_scale` and `effective_l_for_selection`, which define the older ability-spread multiplier. These are source-code observations, not reproduced empirical results.

**2026-09-25 — Initial decision record:** collected the choices made one at a time; recorded the comparison of raw congestion with one fixed reference standardization; left the reference population open; corrected the interpretation of fixed scaling as an effective congestion-weight change; preserved Charles's request for detailed explanations and repeated expansion of unfamiliar shorthand.

**2026-09-25 — Reference-population decision:** selected the observed 2015 team assignments as the fixed empirical reference distribution for congestion standardization. Left player-versus-team weighting and calculation conventions open.

**2026-09-25 — Reference-weighting decision:** selected equal-player weighting because congestion enters individual scores and selection is an individual outcome. Documented why unequal roster sizes make equal-team weighting answer a different question. Left the standard-deviation convention and safeguards open.

**2026-09-25 — Reference-spread calculation:** selected the population standard deviation because the frozen observed 2015 reference panel is the complete fixed population being described, rather than a sample used to infer a larger hypothetical population. Left zero-spread and very-small-spread safeguards open.

**2026-09-25 — Exactly zero reference spread:** required a pre-execution stop with diagnostic reporting and no automatic fallback. Left the definition and treatment of a positive but extremely small spread open.

**2026-09-25 — Extremely small positive reference spread:** selected $10^{-8}$ as a fixed numerical stop threshold on the theoretical zero-to-one congestion scale. Required diagnostic reporting, no automatic fallback, and reporting of the actual reference spread and implied raw-scale multiplier whenever the threshold is passed. The threshold is a numerical safeguard, not a scientific effect-size judgment.

**2026-09-25 — Shared team congestion:** selected one team-level congestion value calculated over every eligible roster member, including the focal player, and applied that same value to every player on the team. Repository inspection confirmed that `team_smooth` maps to `crowding_smooth_team` and is the current gallery default; the leave-one-out version is a separate legacy option. Leave-one-out teammate quality remains distinct as an empirical curve axis, while leave-one-out congestion is excluded from the primary design and reserved only as a possible later sensitivity analysis.

**2026-09-25 — Integer slot counts:** selected nearest-integer rounding of the target fraction times the final eligible population size, with exact halves rounded upward. For the currently audited $N=4{,}266$, this gives 43 slots for the 1% condition and 427 slots for the 10% condition; the achieved fractions must be reported, and the counts must be recalculated if the authorized rebuild changes $N$.

**2026-09-25 — Viability-threshold quantile:** selected linear interpolation for the 99th percentile of the final standardized ability distribution. The resulting interpolated value defines the midpoint of the smooth viability transition and is separate from the whole-number selection capacity $K$; it is not required to place exactly 1% of players strictly above the threshold.

**2026-09-25 — Random seeds and pairing:** selected master seed `20260925`, from which 100 recorded repetition seeds will be derived. Each repetition seed is reused across $\rho=0$ and $\rho=1$ to couple player order and underlying random choices while allowing the different assignment probabilities to produce different rosters. All scoring conditions reuse the resulting roster without additional randomness.

**2026-09-25 — Exact score ties:** selected ascending frozen player identifier as the deterministic tie-breaker. The order is fixed across all conditions and repetitions and introduces no post-scoring random draw. Identifier uniqueness, missingness, and numeric-versus-text storage must be verified before execution; a failed check stops the process.

**2026-09-25 — Reporting package:** retained unbinned winner displacement as the primary result and selected the central 2.5th-to-97.5th percentile simulation range to describe variation across 100 assignments. Selected sixteen equal-count leave-one-out teammate-ability bins for a secondary simulated assignment-outcome diagnostic, with bin membership frozen across scoring and scarcity conditions within each repetition. The diagnostic will display actual peer-quality values and will not be labeled a reproduced HERO, fitted quadratically, assigned a turning point, or formally classified as an inverted-U.

**2026-09-25 — Data hygiene and historical reasoning:** recorded Charles's fresh-output preference and the one-game-opponent problem; added a source review and question document for SCOUT; kept the exact population provisional; corrected the certainty of VECTOR's earlier two-player-roster explanation. Preserved the accepted experiment settings. No analytical code, data, or figures were created or changed.

**2026-09-25 — Team-season coverage rule:** after reviewing SCOUT, COMPASS, the saved comparison figures, and the primary archived decision exchange, Charles selected at least eleven captured games for each included 2015 team-season. Recorded the rule as coverage rather than proof of a complete season or Division I membership.

**2026-09-25 — Individual minutes eligibility:** Charles selected a floor of twenty total captured 2015 minutes. Players below the floor are excluded from assignment, capacities, teammate and congestion calculations, and outcome readouts. The zero-points-per-minute construction is deferred as a possible sensitivity analysis.

**2026-09-25 — Ability standardization and source clarification:** Charles selected standardization after both eligibility filters using the eligible 2015 population mean and population standard deviation. VECTOR initially misread Charles's belief that points per minute was provided as an instruction never to calculate it. Code inspection and SCOUT's updated response established that ESPN supplies game-level points and minutes, while the panel build calculates season points per minute once from their retained totals. Charles selected a fresh build from that frozen game-level source rather than trusting a saved panel export.

**2026-09-25 — Points-per-minute source settled:** After reviewing SCOUT's updated reconciliation, Charles selected a fresh rebuild from the frozen game-level box data. The new panel will calculate season points per minute once from aggregated retained points and minutes, then exclude rows below twenty total minutes and standardize across the final eligible 2015 population. Existing panels are comparison artifacts only. This decision authorizes documentation, not construction or execution.

**2026-09-25 — Canonical 2015 team:** A read-only source audit found 27 athlete-game assignments duplicated across both opposing teams in two games. Four false High Point-to-Arkansas–Pine Bluff copies survived the twenty-minute rule, producing 4,270 player-team rows for 4,266 athletes and inflating Arkansas–Pine Bluff's capacity from 14 to 18. Charles selected one canonical team per athlete based on the greatest number of distinct 2015 game records, then total minutes; unresolved ties stop for manual review. The decision is limited to the verified 2015 anomaly and does not establish a general no-transfer policy.

**2026-09-25 — Primary outcome:** Charles selected winner displacement as the primary outcome: the count and fraction of ability-only winners replaced when congestion is switched on for the same assignment and slot count. Curve shape remains a separately reported diagnostic and is not a required success condition. This directly tests whether congestion changes advancement without tuning the experiment to reproduce an inverted-U.

**2026-09-25 — No arbitrary effect threshold:** Charles selected transparent magnitude reporting rather than a researcher-chosen cutoff for whether displacement matters. Report the mean, median, range, proportion of repetitions with any displacement, and paired assignment-preference contrast. Interpret the prespecified results on their observed magnitude and consistency without tuning a threshold after seeing them.
