# Main idea

Systems that concentrate high-performing individuals generate endogenous congestion in evaluative comparisons, producing diminishing and eventually negative marginal returns to elite affiliation.

---

The important thing is that congestion should not just mean “more good people nearby.” It must alter how evaluation and organizational selection operate.

There are several plausible mechanisms, and they are not mutually exclusive.

## One broad class is comparative evaluation

Evaluators rarely assess candidates in isolation. They compare candidates against local reference groups. In elite environments, evaluators become calibrated upward:

- “good” becomes normal,
- standout performances appear less exceptional,
- marginal differences are harder to perceive.

In NCAA basketball, a 15 PPG scorer on a mid-tier team may dominate attention, while the same player on a stacked roster becomes one of several interchangeable high-level contributors.

So congestion affects signal distinctiveness.

Formally, the evaluator observes:

$$
\text{signal}_i = a_i - f(\text{local peer quality}) + \epsilon_i
$$

not simply $a_i$.

## A second mechanism is attribution dilution

In strong teams, success becomes harder to assign individually:

- Was the player good because of the system?
- Were they benefiting from elite teammates?
- Were their statistics suppressed or inflated by surrounding talent?

This is especially plausible in:

- academia (“the lab effect”),
- sports (“system player”),
- firms (“brand halo”),
- entertainment (“ensemble success”).

Elite environments create ambiguity in causal attribution.

## Third is finite attention

Scouts, committees, evaluators, and organizations have bounded cognitive capacity. Weak teams may receive little attention, but elite teams may contain too many plausible candidates.

Then evaluators triage:

- they focus on obvious stars,
- or use heuristics,
- or stop differentiating carefully among near-equals.

This naturally harms “marginally excellent” candidates.

The model predicts the congestion penalty should be strongest precisely for near-threshold individuals because:

- obvious superstars survive congestion,
- weak candidates were never competitive,
- but borderline elite candidates are substitutable.

## Fourth is organizational risk minimization

When many viable candidates coexist, organizations may become more conservative because the marginal benefit of selecting any one individual declines.

In NBA terms:

- if several teammates look similarly promising,
- scouts may prefer the more physically prototypical,
- younger,
- or already famous player.

Congestion increases substitutability, which increases reliance on heuristics.

## Fifth is opportunity suppression

Elite teams often allocate unevenly:

- minutes,
- touches,
- leadership roles,
- late-game opportunities,
- media visibility,
- recommendation strength,
- developmental investment.

So congestion changes not only evaluation but the production of observable signals themselves.

This is especially important because the mechanism becomes recursive:

- viable peers suppress opportunities,
- suppressed opportunities reduce evaluative distinctiveness,
- reduced distinctiveness reinforces congestion.

## Sixth is queueing and timing

Organizations often advance only a few people at a time. In elite environments, many qualified individuals accumulate simultaneously.

Then:

- some are delayed,
- some exit,
- some become invisible.

This creates temporal congestion even if eventual success remains possible.

The strongest theoretical framing is probably:

> “Elite environments increase both capability and substitutability.”

That is the key tension.

- **Weak environments:** low capability, low substitutability.
- **Moderately strong environments:** high capability, manageable substitutability.
- **Elite environments:** very high capability, extreme substitutability.

Congestion matters because organizations do not reward absolute quality perfectly. They allocate scarce opportunities under uncertainty, finite attention, and comparative evaluation. When many highly viable candidates coexist, marginal distinctions become compressed and selection becomes noisier, more heuristic, and more locally comparative.

---

## NCAA basketball

NCAA basketball is actually a very nice setting for this because the “viable peer” idea is directly observable.

You need to operationalize three things:

- own ability ($a_i$),
- team quality ($\bar{a}_t$),
- viable-peer congestion ($C_{i,t}$).

A clean first-pass setup:

$$
a_i = \text{points per minute}_i
$$

or better:

$$
a_i = \text{NBA predictive composite}
$$

because raw scoring is position-sensitive. A stronger measure might combine:

- points/min,
- BPM,
- WS/40,
- usage-adjusted efficiency,
- recruiting rank,
- height/athletic proxies.

But points/min is acceptable as a proof of concept.

Then:

$$
\bar{a}_t = \frac{1}{n_t}\sum_j a_j
$$

Now the key issue is defining viable peers.

The model says congestion is not “good teammates.” It is the density of teammates who plausibly compete for the same scarce advancement outcome.

So in NCAA→NBA, viable peers are:

- high-level NBA-caliber prospects,
- especially those occupying overlapping evaluative roles.

**Simplest operationalization:**

$$
C_{i,t} = \frac{1}{n_t-1} \sum_{j \neq i} \mathbb{1}(a_j > \theta)
$$

where $\theta$ is a prospect threshold.

For example:

- top 15% of Division I players in points/min,
- projected NBA draft probability > 5%,
- former McDonald’s All-Americans,
- future professional players,
- or teammates receiving combine invitations.

This is already strong.

But the more convincing version is role-specific congestion.

A center is not competing against guards for draft slots in the same way. So define:

$$
C_{i,t}^{\text{role}} = \frac{1}{n_t-1} \sum_{j \neq i} w_{ij}\,\mathbb{1}(a_j > \theta)
$$

where $w_{ij}$ measures positional similarity.

For example:

- same listed position,
- similar shot profile,
- similar height,
- similar latent playstyle embedding.

That becomes much more compelling because it distinguishes:

- “strong teammates help exposure”
- from
- “too many similar NBA prospects suppress visibility.”

Then your empirical model becomes:

$$
P(\text{draft}_i) = f(a_i,\, \bar{a}_t,\, C_{i,t})
$$

**Prediction:**

- $a_i > 0$,
- $\bar{a}_t$ initially positive,
- $C_{i,t} < 0$.

The strongest version would show:

- raw team quality gives an inverted U,
- viable-peer congestion explains the downturn.

So:

**Baseline:**

$$
\text{Draft}_i \sim a_i + \bar{a}_t + \bar{a}_t^2
$$

**Mechanism:**

$$
\text{Draft}_i \sim a_i + \bar{a}_t + C_{i,t}
$$

and the quadratic term weakens substantially.

Even stronger: show that the downturn exists primarily for players near the NBA viability margin.

The theory predicts:

- elite superstars still get drafted,
- weak players never had a chance,
- congestion mostly harms “borderline NBA-caliber” players.

That is a very distinctive prediction.

So estimate separately for:

- top 1% performers,
- middle-high prospects,
- ordinary players.

The inverted U should be strongest in the middle-high group.

You could also exploit natural experiments:

- Kentucky/Duke mega-recruiting years,
- transfer portal shocks,
- one-and-done era changes,
- NIL-induced concentration.

For example: after a school recruits several elite guards, existing guards’ draft probabilities should decline conditional on performance.

That is directly aligned with the mechanism.

---

## Secondary phenomena

Yes. The secondary phenomena are where this becomes more than curve-fitting.

The core empirical test should not be only:

$$
P(\text{success}) \sim f(\bar{a}_t)
$$

It should test whether the downturn is mediated by viable-peer density.

So the model predicts three linked patterns:

### First

The inverted U should weaken or disappear after controlling for viable-peer density.

**Baseline:**

$$
Y_i \sim a_i + \bar{a}_t + \bar{a}_t^2
$$

**Mechanism test:**

$$
Y_i \sim a_i + \bar{a}_t + \bar{a}_t^2 + C_{i,t}
$$

where

$$
C_{i,t} = \frac{1}{n_t-1}\sum_{j\neq i}\mathbb{1}(a_j > \theta)
$$

or a smooth version.

If the theory is right, $C_{i,t}$ should be negative, and the negative quadratic/team-quality downturn should shrink.

### Second

The downturn should be strongest where peer viability is most concentrated. Split teams into bins by $C_{i,t}$. The high-congestion bin should show the steepest right-side decline. Low-congestion teams should mostly show monotone or saturating returns to team quality.

### Third

The downturn should be stronger in systems with more assortative sorting. For example:

- elite academic departments versus less stratified departments,
- top sports teams versus more parity-heavy leagues,
- highly ranked firms versus less hierarchical labor markets,
- selective graduate programs versus broad-access programs.

The comparative test is:

$$
Y_i \sim a_i + \bar{a}_t + \bar{a}_t^2 + A_s \bar{a}_t^2
$$

where $A_s$ measures system-level assortativity. The interaction should be negative: stronger assortativity produces a stronger top-end penalty.

### A cleaner set of secondary predictions

- **Viable-peer density mediates the elite-team penalty.**  
  The negative top-end effect should be reduced after adding $C_{i,t}$.

- **The penalty should be strongest near the viability threshold.**  
  Very weak people do not compete. True superstars may still succeed. The biggest harm should fall on high-but-not-dominant individuals.

  **Empirical test:**

  $$
  Y_i \sim a_i + \bar{a}_t + C_{i,t} + a_i \times C_{i,t}
  $$

  The congestion penalty should be largest for people just above the serious-candidate threshold.

- **The penalty should be weaker when evaluation is externally benchmarked.**  
  If success depends on standardized metrics, the local comparison penalty should shrink. If success depends on committees, coaches, recommenders, prestige narratives, or limited internal nominations, it should grow.

- **The penalty should be stronger when opportunity capacity is fixed.**  
  If each team/lab/department can only plausibly advance a small number of people, viable-peer congestion matters more.

- **Congestion should delay success, not only reduce it.**  
  In elite teams, people may still eventually succeed, but after longer waiting times.

  Test with survival models:

  $$
  h_i(t) = h_0(t)\exp(\beta_1 a_i + \beta_2 \bar{a}_t + \beta_3 C_{i,t})
  $$

  Prediction: $\beta_3 < 0$, especially among high-ability individuals.

- **The penalty should increase after a strong cohort enters.**  
  This is a nice quasi-experimental test. If a team suddenly recruits several high-ability members, the success probability of existing near-threshold members should fall.

  Difference-in-differences style:

  $$
  Y_{i,t+1} \sim \text{PostStrongCohort}_{team,t} + a_i + \text{team FE} + \text{cohort FE}
  $$

  Prediction: existing members are crowded out.

- **The penalty should be partly reversible through mobility.**  
  People who leave elite congested teams for strong-but-less-congested teams should have improved success odds, conditional on own ability.

  That is probably the strongest “unexpected” prediction: elite departure can increase success probability.

In paper terms, I would frame the tests as:

> “Beyond reproducing an inverted-U association between team quality and individual advancement, the model predicts that the downturn should be explained by the density of viable peers, concentrated among near-threshold candidates, amplified in highly assortative systems, and partially reversed by moves to less congested environments.”

---

**Alexander Gates**  
Assistant Professor  
School of Data Science  
University of Virginia  
https://www.alexandergates.net/
