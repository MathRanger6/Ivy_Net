# Quayle (2006) — One-Page Formula & Concept Sheet

**Print target:** one page (briefing / one_page CSS)  
**Purpose:** Fast-reference sheet for the Quayle assortative-growth
mechanism and the distinctions that matter for VECTOR.

## The Core Causal Chain

$$
\boxed{
\text{property}
\rightarrow
\text{similarity }x_{ij}
\rightarrow
\text{homophily }\alpha
\rightarrow
\text{attachment }\Pi
\rightarrow
\text{assortativity }r
\rightarrow
\text{community structure }Q
}
$$

**Do not conflate these objects.** Similarity $x_{ij}$ is a **pairwise
property**; homophily $\alpha$ is a **generative preference strength**;
assortativity $r$ is a **network-level realized outcome**. In
particular:

$$
\boxed{x_{ij}\neq\alpha\neq r}
$$

Two stochastic networks generated with the same $\alpha$ need not
realize exactly the same $r$.

## Governing Attachment Rule — Equation (4)

$$
\Pi(k_j,x_{ij})
=
\frac{f(k_j)e^{-\alpha(1-x_{ij})}}
{\sum_l f(k_l)e^{-\alpha(1-x_{il})}}.
$$

Read this as:

$$
\boxed{
\text{structural attractiveness}
\times
\text{similarity attraction}
\rightarrow
\text{normalized attachment probability}
}
$$

Here $i$ is the incoming vertex, $j$ is the candidate vertex, $l$
indexes all eligible candidates, $k_j$ is candidate $j$’s degree,
$f(k_j)$ is its structural attractiveness, and $\Pi$ is the probability
that $i$ attaches to $j$. Standard BA is the special implementation
$f(k_j)=k_j$.

The similarity weight is $e^{-\alpha(1-x_{ij})}$. At $\alpha=0$,
similarity has no effect. Larger $\alpha$ increasingly penalizes
dissimilar candidates.

## Similarity Functions

**Discrete properties:** $x_{ij}=1$ for the same property and $x_{ij}=0$
for different properties. Therefore:

$$
w_{\mathrm{same}}=1,
\qquad
w_{\mathrm{different}}=e^{-\alpha}.
$$

**Hierarchical properties — Eq. (12):**

$$
x_{ij}=1-\frac{g_{ij}}{G}.
$$

$g_{ij}$ measures hierarchical separation and $G$ is the maximum
hierarchy depth. Closer common ancestry means greater similarity.

**Scalar / continuous properties — Eq. (15):**

$$
\boxed{x_{ij}=1-|p_i-p_j|}
$$

for appropriately scaled $p$. Substituting into Eq. (4) gives Eq. (16):

$$
\boxed{
\Pi(k_j,p_i,p_j)
=
\frac{f(k_j)e^{-\alpha|p_i-p_j|}}
{\sum_l f(k_l)e^{-\alpha|p_i-p_l|}}
}
$$

This scalar form is especially portable: **attribute distance →
exponential similarity preference → attachment probability**.

## Homophily $\alpha$ vs. Assortativity $r$

For the symmetric discrete-property ensemble, Quayle derives:

$$
\boxed{
r=
\frac{1-e^{-\alpha}}
{1+(n_p-1)e^{-\alpha}}
}
\qquad\text{(Eq. 11)}
$$

where $n_p$ is the number of discrete properties. Thus
$\alpha\rightarrow r$: microscopic preference generates macroscopic
assortment.

The inverse is:

$$
\boxed{
\alpha=
\ln\left(
\frac{1+(n_p-1)r}{1-r}
\right)
}
\qquad\text{(Eq. 28)}
$$

But this **does not define $\alpha$ as assortativity**. It infers a
candidate $\alpha$ from observed $r$ **only under Quayle’s discrete
symmetric ensemble assumptions**.

## Assortativity vs. Community Structure

Assortativity $r$ measures property mixing across edges. Modularity $Q$
measures topological community structure:

$$
Q=\sum_u(e_{uu}-a_u^2).
$$

Quayle’s simulations show that $r$ rises before strong $Q$:
**assortative mixing can exist before sharply separated communities
emerge**. Hierarchical similarity can generate hierarchical community
structure.

## What to Remember for VECTOR

- **Similarity $x_{ij}$:** how alike two candidate entities are.
- **Homophily $\alpha$:** how strongly similarity changes attachment
  odds.
- **Attachment $\Pi$:** the stochastic local choice rule.
- **Assortativity $r$:** realized network-level mixing after choices
  accumulate.
- **Modularity $Q$:** downstream community structure.
- The similarity metric is a **modeling choice**, not a natural law.
- Quayle uses **one-mode growth, degree attraction, and no hard
  capacity**.
- Capacity constraints, bipartite affiliation, or reassignment change
  the formation process.
- Therefore **do not transplant Quayle’s Eq. (11) or Eq. (28) into
  VECTOR without re-deriving or empirically validating the new
  $\rho\rightarrow$ realized-assortment relationship.**

> **Five-year memory:** Quayle turns “similar things tend to connect”
> from a descriptive observation into a generative probability rule,
> then follows the consequences upward from local attachment to
> assortative mixing to community structure.

**Source:** Quayle, A. P., Siddiqui, A. S., & Jones, S. J. M. (2006).
*Modeling network growth with assortative mixing*. European Physical
Journal B, 50, 617–630.
