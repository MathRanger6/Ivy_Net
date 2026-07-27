# 1. The problem in plain English

**Audience:** Charles, re-entering after time away  
**You do not need any other document open while reading this.**

**Binding insight (read early):** The hero shows **outcomes** (draft rate vs pool quality). **Environment** = **`L_net = B − D`**; **selection** = **`S_i`** (who gets the pick) — a **separate step** from describing the peer environment. See doc **02** and [`../BINDING_Selection_is_its_own_step.md`](../BINDING_Selection_is_its_own_step.md).

---

## The one-sentence dissertation idea

Organizations advance some people and not others. Being surrounded by **strong peers** can **help** you (you learn, you look good by association) and **hurt** you (you are harder to notice, you compete for scarce slots). The dissertation asks whether that **tension** shows up in data — and whether a **simple mechanism** (crowding in selection) can produce curves that look like the data.

Basketball is one **test bed**: college players who get drafted to the NBA.

---

## The basketball “hero” — what we already see in the data

Think of one row per **player-season**: a college player in a given year, on a given team.

**Question:** Does the chance of eventually being **NBA drafted** relate to the **quality of his teammates**?

We measure teammate quality using box-score performance (points per minute, adjusted within season). Crucially, we use **leave-one-out** quality: average teammate performance **excluding the player himself**, so he is not counted in his own pool average.

Call that number **pool quality (leave-one-out)**. Higher means better teammates around him.

**What we plot:** Split all player-seasons into 16 equal-sized bins from lowest to highest pool quality. For each bin, compute the **fraction who were ever drafted**. Connect the dots.

**What we see (qualitative shape):**

- Draft rate **rises** as pool quality increases through the middle bins.
- Rate **levels off** in high-but-not-top bins.
- In the **very top bin only**, rate **drops** — an inverted-U **tail**, not necessarily a symmetric hill.

That plot is the **hero**. It is a **stylized fact** — something real in the NCAA panel under fixed rules (which seasons, which minutes filter, which binning). It is **not** yet a story about why NBA teams behave that way.

**First step — two axes, two curves (real data):** Before the hero is “surprising,” check the obvious axis. Bin the **same** player-seasons by **own college performance** (same ppm stat, z-scored within season) instead of teammate pool quality. Draft rate then rises **monotonically** from the bottom talent bin to the top (~0% → ~7% on the locked July 2026 sample). That is the **talent baseline** — talent matters, as it should. The **hero** bins on **pool quality** instead and gets a **different** shape: rise, plateau, then a **dip in the top pool-quality bin only**. The phenomenon is the **second** curve, not draft itself. We are **not** claiming the NBA ignores talent; we are showing that **peer environment** has its own non-monotone pattern once you look at it on its own axis.

**Important:** The hero shows **who got drafted** vs pool quality. It does **not** tell you whether the bend comes from peer effects on **development** or from **congestion in the selection process itself**. That split is Layer B (doc 02): environment (B − D) vs **selection as its own step** (Alex score).

**Sample size (locked July 2026):** about 62,000 player-seasons; about 1,100 drafted.

---

## Why this matters for the “simplified model” push

Alex’s scientific arc (paraphrased): show the **phenomenon**, then show a **minimal generative rule** where **talent alone is not enough** — you need something like **congestion in who gets selected** — then later add richer measurements and predictions.

You are **not** being asked, in the next few days, to:

- perfectly reproduce every bin of the hero from simulation;
- estimate separate “benefit” and “congestion” functions from one chart;
- unify Army, basketball, and tenure in one model.

You **are** being asked to hold a clear line:

1. **Here are the two empirical curves** — talent baseline (monotone) and hero (pool quality with tail dip); both on real NCAA data under the locked spec.
2. **Here is a disciplined artificial league** where picking purely on talent gives a different curve than picking on talent **minus** a congestion penalty — side by side, honest axes, explicit limits on what we claim.

That is the simplified model **deliverable** for basketball v1. Slide summary: [`Model.pdf`](Model.pdf).

---

## Words you will see again (defined once here)

| Term | Plain meaning |
|------|----------------|
| **Panel** | The main analysis table of **real** college player-seasons — one row per athlete × season × team, with own stats, leave-one-out teammate quality, and draft outcome; we **filter** it, then **bin** it for the hero |
| **Hero** | The binned draft-rate plot vs leave-one-out pool quality |
| **Talent baseline** | Same panel binned by **own** performance instead of pool quality; draft rate rises monotonically (sanity check before the hero) |
| **Pool quality (LOO)** | How good your teammates are on paper, with you removed from the average |
| **Draft rate** | Share of players in a bin who were ever NBA drafted |
| **Stylized fact** | A robust pattern in data under stated rules — not yet causal proof |
| **Generative model / sim** | A computer-made fake league with explicit draft rules |
| **Congestion** | “Too many good peers” — harder to stand out or win a scarce slot |
| **BINDING** | Charles-locked rule: docs/agents must keep **`L_net`** (environment) and **`S_i`** (selection) separate unless you reopen it |

---

## Emotional checkpoint

If the only thing you take from this page is:

> *Good players get drafted more than weak ones (talent baseline). But among teammate environments, the very best pools do not have the highest draft odds — and we have a fixed hero plot that shows that.*

—you have enough to read document **02** (three kinds of model) without guilt about everything else in the repo.

**Next:** [02_Three_Kinds_of_Model.md](02_Three_Kinds_of_Model.md)
