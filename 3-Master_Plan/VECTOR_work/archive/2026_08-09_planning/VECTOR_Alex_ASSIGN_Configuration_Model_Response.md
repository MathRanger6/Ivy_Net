Yes. I think Alex has identified a **much better route for the purpose
of ASSIGN**.

The important shift is this: we probably do **not** need to invent a new
network-growth model. We need a defensible, minimal **constrained
bipartite assignment mechanism**. The literature already gives us the
structural skeleton, and Quayle gives us the behavioral bias to put
inside it.

The clean story becomes:

> **Start from a bipartite configuration model that controls the degree
> sequence/capacities, then bias otherwise allowable individual–team
> assignments using Quayle-style similarity attraction.**

That is substantially easier to motivate than “we invented a new
formation model.”

### Why the pieces fit

A bipartite configuration model has exactly the structural property Alex
was reaching for. In a bipartite graph with individuals on one side and
teams on the other, we specify degree requirements on both layers. For
our snapshot:

$$
k_i=1
$$

for each individual—one affiliation—and

$$
k_j=C_j
$$

for each team if all roster positions are filled.

With uniform basketball capacity,

$$
k_j=C=15.
$$

Therefore total stubs balance:

$$
\sum_i k_i=\sum_j C_j.
$$

Ordinary bipartite configuration matching would then connect individual
stubs to team stubs without caring about performance similarity.
**That’s precisely the place where Quayle can enter.**

Instead of making the next allowable match uniformly, give individual
$i$’s possible connection to team $j$ the Quayle-inspired weight

$$
\boxed{
w_{ij}
=
e^{-\rho|A_i-\mu_j|}
}
$$

and sample among teams with remaining stubs:

$$
\boxed{
P(i\rightarrow j)
=
\frac{
R_j\,e^{-\rho|A_i-\mu_j|}
}{
\sum_l R_l\,e^{-\rho|A_i-\mu_l|}
}
}
$$

where

$$
R_j=C_j-n_j
$$

is team $j$’s **remaining capacity**.

That equation is worth staring at, because I think it may be the whole
ASSIGN mechanism.

At

$$
\rho=0,
$$

it becomes

$$
P(i\rightarrow j)
=
\frac{R_j}{\sum_l R_l},
$$

which is exactly what you would expect from random matching of an
individual stub to the remaining **team stubs** in a configuration-style
construction.

As $\rho$ increases,

$$
e^{-\rho|A_i-\mu_j|}
$$

biases those structurally available stubs toward teams whose centroids
resemble $i$.

And when

$$
R_j=0,
$$

the team’s probability automatically becomes zero.

**No special “remove the team from rotation” code is conceptually
necessary. Capacity is already built into the configuration mechanism.**

That is elegant.

### One important refinement to our earlier thinking

Notice the $R_j$ term.

Earlier, we had been considering:

$$
P(i\rightarrow j)
=
\frac{e^{-\rho d_{ij}}}
{\sum_{l\in\mathcal F}e^{-\rho d_{il}}}.
$$

That makes every *team* with space one alternative regardless of whether
it has 1 opening or 10 openings.

A configuration-model interpretation says something subtly different
and, I think, more principled: **the objects being matched are stubs**.
A team with 10 remaining positions has 10 available team stubs; one with
1 remaining position has one.

Hence:

$$
\boxed{\text{remaining capacity}\times\text{Quayle similarity}}
$$

becomes the attachment weight.

That isn’t an arbitrary new structural-prestige mechanism like Quayle’s
$f(k_j)$. It’s simply the combinatorics of the configuration model.

And the literature supports the foundation. Saracco et al.’s Bipartite
Configuration Model (BiCM) explicitly extends configuration-model
reasoning to binary undirected bipartite networks by constraining degree
sequences on both layers. Later maximum-entropy work develops this
framework extensively. There is also a separate literature on
**bipartite ERGMs with homophily**, which is useful confirmation that
bipartite degree structure and attribute-dependent edge preference can
coexist mathematically, although I would *not* jump to a full ERGM
unless we need it—the complexity would defeat Alex’s objective.

### Alex’s projection insight is good, with one qualification

Yes, Quayle’s one-mode network can help us conceptually think about what
we see after projecting affiliations onto individuals: members of the
same team become connected/co-members in the projection.

But I would **not claim that Quayle’s model literally is the projection
of our bipartite process**. That’s stronger than we’ve established.
Projection induces cliques/co-membership structure and degree
dependencies that Quayle’s growth process does not explicitly generate.

The safer—and more interesting—statement is:

> Quayle provides the **micro-level similarity mechanism** we want the
> affiliation process to reproduce, while the bipartite configuration
> model supplies the **structural constraints** that Quayle lacks.

That’s enough. We don’t need projection equivalence.

------------------------------------------------------------------------

## The model may now be much simpler than what we were building

For a given formation period $t$, freeze team centroids:

$$
\mu_{j,t-1}.
$$

Each entrant $i$ has ability:

$$
A_{i,t-1}
$$

or an empirically informed entrant draw.

Each team begins with remaining roster capacity:

$$
R_{j,t}=C_j-n_{j,t}^{\text{inc}}.
$$

Randomly order the players requiring assignment.

Then sequentially draw:

$$
\boxed{
P(i\rightarrow j\mid t,s)
=
\frac{
R_{j,t}^{(s)}
e^{-\rho|A_i-\mu_{j,t-1}|}
}{
\sum_l
R_{l,t}^{(s)}
e^{-\rho|A_i-\mu_{l,t-1}|}
}
}
$$

and after assigning $i$ to $j$,

$$
R_{j,t}^{(s+1)}
=
R_{j,t}^{(s)}-1.
$$

Continue until all individual stubs and team stubs are exhausted.

**That’s it.**

We still have the dynamic feedback afterward:

$$
\mu_{j,t-1}
\rightarrow
\text{configuration-style biased matching}
\rightarrow
T_{j,t}
\rightarrow
\mu_{j,t}.
$$

But we no longer need to pretend we’re designing an entire
network-growth theory.

### And the interpretation of $\rho$ stays beautiful

At

$$
\rho=0
$$

we recover the random bipartite configuration-style assignment baseline.

For

$$
\rho>0
$$

we increasingly bias stub matching by similarity.

For very large $\rho$, assignments become strongly assortative **subject
to the degree/capacity constraints**.

That last clause is scientifically interesting:

$$
\boxed{
\text{homophilic preference}
\neq
\text{perfect assortative realization}
}
$$

because capacity can prevent everyone from receiving their most similar
affiliation.

That is precisely the distinction we liked in Quayle—**generative
preference versus realized assortativity**—now transplanted into the
structure we actually need.

And we absolutely should **not** use Quayle’s analytic
$\alpha\leftrightarrow r$ formula. Our capacity constraints and
bipartite matching change the mapping. We can simply simulate the
relationship

$$
\rho
\longrightarrow
\text{realized sorting}
$$

and report it.

## The literature path I would take now

I would **stop hunting for a magical paper that already contains our
exact model**. We don’t need one. I think the defensible lineage is:

1.  **Configuration model / bipartite configuration model** for the
    constrained bipartite matching skeleton.
2.  **Quayle et al. (2006)** for the exponential similarity/homophily
    bias and the crucial preference-versus-assortativity distinction.
3.  **Bipartite ERGM/homophily literature** as supporting precedent that
    attribute-biased formation in bipartite networks is well
    established—not necessarily as our implementation.

The most directly useful BiCM anchor I found is Saracco et al. (2015),
which explicitly develops the bipartite extension of the configuration
model with degree constraints. A recent review of bipartite pattern
detection also distinguishes hard degree-preserving configuration models
from softer maximum-entropy variants. And Bomiriya et al. specifically
study homophily in exponential-family random graph models for bipartite
networks, which is conceptually adjacent to what we’re doing.

*Saracco, F., Di Clemente, R., Gabrielli, A., & Squartini, T. (2015).
Randomizing bipartite networks: the case of the World Trade Web.
Scientific Reports, 5, 10595. https://www.nature.com/articles/srep10595*

*Straka, M. J., Caldarelli, G., & Saracco, F. (2017). Grand canonical
validation of the bipartite international trade network.
https://arxiv.org/abs/1703.04090*

*Saracco, F., et al. (2018). From ecology to finance (and back?): A
review on entropy-based null models for the analysis of bipartite
networks. Journal of Statistical Physics.
https://link.springer.com/article/10.1007/s10955-018-2039-4*

*Bomiriya, R. P., Kuvelkar, A. R., Hunter, D. R., et al. (2023).
Modeling homophily in exponential-family random graph models for
bipartite networks. https://arxiv.org/abs/2312.05673*

*Quayle, A. P., Siddiqui, A. S., & Jones, S. J. M. (2006). Modeling
network growth with assortative mixing. European Physical Journal B, 50,
617–630. https://link.springer.com/article/10.1140/epjb/e2006-00170-5*

The next thing I would do is **not code yet**. I would spend a short,
tightly bounded literature pass verifying whether the exact
weighted-stub rule

$$
R_j e^{-\rho d_{ij}}
$$

already has a recognized name/model lineage, and whether hard degree
preservation introduces any sampling subtlety we need to acknowledge. If
it checks out, I think we may have turned what looked like a weekend
rabbit hole into a very small ASSIGN module with an extremely clean
methodological pedigree.
