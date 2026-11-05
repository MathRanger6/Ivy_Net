# LG: a bipartite configuration model with metadata assortativity

**Last synced:** 2026-11-03 (14:35; replaces the 14:30 version, which wrongly treated "configuration model with metadata assortativity" as a second, separate model)

**Audience:** Charles — a lunch read on what kind of network model LG is and how it differs from the usual assortative models.

**Standalone:** Everything needed is on these pages; the symbols are defined where they first appear.

---

## The short answer

The LG (Levine–Gates) model **is** a bipartite configuration model with assortativity. What sets it apart from the usual assortative network models is three things:

1. **What people sort on.** The usual models sort on *degree*, a property of the network itself. LG sorts on *metadata*: a property each person brings from outside the network, here the performance measure $A_i$.
2. **The structure.** LG is bipartite (people and groups), every person has exactly one link, and every group has a hard roster capacity. In that structure, degree carries nothing to sort on: all people have degree one and the group degrees are fixed by capacity. Metadata is the only thing sorting *can* be about.
3. **How assortativity arises.** It is not imposed as a target. It emerges from a preference, applied as people arrive one at a time, for groups whose current mean resembles them, and it is limited by roster capacity.

---

## The configuration model, in one paragraph

A node's *degree* is its number of links. A *configuration model* fixes every node's degree and otherwise connects nodes at random. Picture each node with as many "stubs" (half-links) as its degree, then join stubs at random. In the *bipartite* version there are two kinds of nodes, and stubs join only across kinds. In LG, each person has one stub and group $j$ has $n_j$ stubs, one per roster seat. **With the preference switched off ($\rho = 0$), LG is exactly the bipartite configuration model:** each arriving person takes a uniformly random open seat.

---

## The usual assortative models sort on degree

**Assortativity** is the tendency of similar nodes to be linked. In most network-science work, "similar" means *similar degree*: hubs linked to hubs, or, in the disassortative case, hubs linked to low-degree nodes.

- **Degree-assortative configuration models.** These fix the degrees and also how often nodes of each degree pair with each other (Newman 2002), or start from a configuration model and rewire links until degrees are correlated across links (Xulvi-Brunet and Sokolov 2004). The sorted trait, degree, is part of the network itself.
- **Not the Barabási–Albert model.** In BA, a new node attaches to existing nodes in proportion to their degree. That is *preferential attachment*, not assortative mixing, and BA networks come out roughly neutral in degree assortativity. The difference matters for LG: its open-seat factor $R_j$ is stub counting, not preferential attachment. A group with more open seats is likelier to receive the next person because it has more stubs, not because it is already popular.

---

## Metadata assortativity: sorting on a property from outside the network

Assortativity can also be measured on a node property that is not part of the network: age, race, field, or performance. Newman (2003) gave the standard measure. For a numerical property, it is the correlation of that property across the two ends of every link. This is well-established *measurement*.

What LG adds is a **generative** model: a configuration model whose links form under a preference based on metadata, so that metadata assortativity emerges rather than being measured after the fact.

---

## How LG works

All groups start empty. People arrive in random order. Person $i$ joins group $j$ with probability

$$
P(i \to j) = \frac{R_j \, e^{-\rho\,|A_i - T_j|}}{\sum_h R_h \, e^{-\rho\,|A_i - T_h|}},
$$

where $R_j$ is the number of open seats (stubs) in group $j$ and $T_j$ is the current mean performance of its members. After each arrival, the receiving group's mean is updated.

- **$R_j$ is the configuration-model part:** a seat-weighted random choice among open stubs.
- **$e^{-\rho|A_i - T_j|}$ is the metadata part:** a preference for groups whose current mean is close to the person's own performance.
- **$\rho$ is a preference, not an amount of sorting.** It says how strongly people are drawn to similar groups. How much sorting actually results also depends on roster sizes, the spread of performance, and early luck in who arrived first.

---

## LG next to the usual assortative models

| | Degree-assortative configuration model | LG |
|---|---|---|
| Network | One kind of node | Bipartite: people and groups |
| Degrees | Fixed, varied across nodes | Fixed: one per person; roster size per group |
| Trait sorted on | Degree (part of the network) | Performance $A_i$ (metadata) |
| How sorting arises | Target mixing pattern, or rewiring | Arrival-by-arrival preference for similar group means |
| Parameter | Degree correlation or mixing matrix | $\rho$, a preference |
| Limit on sorting | Degree sequence | Roster capacity |

---

## Measuring the sorting LG produces

**The sorting index.** The project measures realized sorting by

$$
H_{\mathrm{sort}} = 1 - \frac{\sum_i \big(A_i - T_{g(i)}\big)^2}{\sum_i \big(A_i - \bar{A}\big)^2},
$$

the share of the variation in performance that lies between group means. Here $T_{g(i)}$ is the final mean of person $i$'s group and $\bar{A}$ is the population mean.

**Random assignment already gives some sorting.** At $\rho = 0$, group means still differ by chance, and on average

$$
E[H_{\mathrm{sort}}] = \frac{J-1}{N-1}
$$

with $J$ groups and $N$ people. Checked by simulation today: 12 groups of 15 give 0.061, against 0.061 from the formula. So zero preference does not mean zero sorting. Groups can differ without assortativity. What assortativity adds is a link between a person's own performance and the strength of that person's group.

**The bridge to Newman's measure.** Link two people if they share a group (the "projection" of the bipartite network onto people) and take Newman's metadata assortativity $r$ on that network. For groups of equal size $n$,

$$
r = \frac{n\,H_{\mathrm{sort}} - 1}{n - 1}.
$$

This was checked numerically today and matches to four decimals; unequal group sizes need a weighted version. The two measures carry the same information, rescaled. One difference is worth using: under random assignment $r$ averages $-1/(N-1)$, essentially zero, while $H_{\mathrm{sort}}$ averages $(J-1)/(N-1)$. **$r$ puts its zero at "no sorting beyond chance,"** which network scientists will expect and which compares more easily across systems with different group sizes.

---

## Questions to take to lunch

1. **How to name it in the chapter.** For example, "a bipartite configuration model with metadata assortativity," with the attachment rule described as seat-weighted matching biased by similarity of performance. An open item from earlier notes: check whether this exact rule, $R_j e^{-\rho|A_i - T_j|}$, already has a name in the literature.
2. **$H_{\mathrm{sort}}$ or $r$?** They are rescalings of each other for equal groups. $r$ is what network-science readers expect; $H_{\mathrm{sort}}$ is what the project uses now.
3. **Evolving group means.** Updating $T_j$ after each arrival makes the outcome depend on who arrives first. That fits a system where people choose groups as rosters fill. Does it fit the Army, where the organization places officers, and faculty hiring?
4. **Fitting $\rho$.** It is now fit by simulating rosters and matching the observed $H_{\mathrm{sort}}$. With observed rosters, this stays separate from fitting the selection parameters.

---

## Glossary

- **Bipartite network:** two kinds of nodes (here people and groups), with links only between kinds.
- **Degree:** a node's number of links.
- **Stub:** a half-link; a node has as many stubs as its degree.
- **Configuration model:** fix every node's degree, then join stubs at random.
- **Metadata:** a property of a node from outside the network, here performance $A_i$.
- **Homophily:** a *preference* for similar others (LG's $\rho$).
- **Assortativity:** the *realized* tendency of similar nodes to be linked ($H_{\mathrm{sort}}$ or $r$).
- **Preferential attachment:** attaching in proportion to degree, as in the Barabási–Albert model; not the same as assortativity.

## Works mentioned

- Newman, M. E. J. (2002). Assortative mixing in networks. *Physical Review Letters* 89 (20), 208701. doi:10.1103/PhysRevLett.89.208701
- Newman, M. E. J. (2003). Mixing patterns in networks. *Physical Review E* 67 (2), 026126. doi:10.1103/PhysRevE.67.026126
- Xulvi-Brunet, R., and Sokolov, I. M. (2004). Reshuffling scale-free networks: From random to assortative. *Physical Review E* 70 (6), 066102. doi:10.1103/PhysRevE.70.066102
- Barabási, A.-L., and Albert, R. (1999). Emergence of scaling in random networks. *Science* 286 (5439), 509–512. doi:10.1126/science.286.5439.509

(All four confirmed in Zotero 2026-11-03.)
