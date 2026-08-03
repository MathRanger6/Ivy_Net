**Paper Directions 15 --- my read (corrected labels)**

Source: transcripts/20260731_Paper_Directions_15_otter_ai_transcript.docx (\~44
min, Jul 31).\
**Slide convention below = your gallery (So_Far\_ slides 1--3):**

  ----------------------------------------
  **Slide**   **Pass**   **Knob**
  ----------- ---------- -----------------
  1           **Pass A** Empirical (no sim
                         knob)

  2           **Pass B** **λ** in score

  3           **Pass C** **ρ** in
                         assignment
  ----------------------------------------

**Headline**

Alex is pleased. You're not off track. The Pass work is **right**. The
shift is **directedness**: fewer items, clearer hierarchy, outputs as
a **characterization slide series** --- and a hard line
between **sensitivity analysis** (now) and **statistical parameter
fitting** (next big insight).

His closing: *"This is still basically what I asked for two weeks ago...
we need to be more directed."*

**What landed well**

**Pass C / ρ:** Assortativity answered cleanly --- flat without ρ,
roster/peer effect appears with ρ. He called that "really good."

**Pass B / λ:** Directionally right (λ = 0 vs λ \> 0 bends the curve),
but **incomplete** --- needs the same systematic treatment as ρ, plus
the double-plot ask below.

**Pass A / empirical:** The real-data side-by-side (talent vs poolq_loo)
is the anchor. The "two x-axes" conversation is about making
the **generative** slides show the same dual readout the empirical slide
already implies.

**Model simplicity:** Collapsed $\mathbf{L}_{\mathbf{C}}$ is fine for
this paper. B vs D decomposition is parked --- development benefits of
good teams are real but not identifiable in promotion data yet → one
black-box **L**.

**Sweep infrastructure:** Rivanna/sweep code is good; reshape output
into a **standard slide series** (equations at top, bold the knob,
figures below) --- not one-off PNGs.

**Three layers (don't merge them)**

**Layer 1 --- Gallery fixes (build on what you have)**

Concrete asks from looking at the deck:

1.  **λ ablation panel** --- mirror Pass C's ρ panel: **fix ρ**, vary **λ**
    (e.g. four subplots at four λ values at one fixed ρ, same layout as Pass C).

2.  **Double-plot in simulation** --- one run (e.g. λ = 0.55, ρ fixed):

    - **Left:** 16 bins on **individual**
      $\mathbf{A}_{\mathbf{i}}$ (sort 1→n, then bin)

    - **Right:** 16 bins on **poolq_loo** (team average talent, LOO)

    - Same scenario both sides --- not separate model runs with
      different λ.

3.  **Overlay λ = 0 vs λ \> 0** on the $A_{i}$-**binned** side for
    deltas.

4.  **Put sort-and-chop back** on the Pass C ρ figure (you cut it
    because it squished the panel).

5.  **Report fitted inputs:** distribution
    of $\mathbf{t}_{\mathbf{j}}$, **σ²**, etc. --- notation
    that **data-fitted** quantities (t̃, empirical draws) differ
    from **simulation-drawn** ones.

Alex called these "puzzle pieces" --- important, but not the deepest
insight. Phase A (below) is the quick gallery pass; Phase B is the same
logic turned into a full one-slide-per-knob characterization deck.

**Layer 2 --- Main mission now: sensitivity characterization (\~4
days)**

Vary **one knob at a time**; keep everything else fixed; show how
the **two curves** move.

**The two curves** (throughout the meeting):

- binned by $\mathbf{A}_{\mathbf{i}}$~ ~→ monotone talent ladder

- binned by **poolq_loo /** $\mathbf{L}_{\mathbf{C}}$ → inverted-U /
  roster-pressure shape

**OAT caveat (interactions):** One knob alone might never produce the Hero-style curve;
ρ and λ (for example) may be necessary together. Alex's one-at-a-time plan maps each knob
around a **working baseline** (539 preset)—not rediscover the inverted-U from zero. If ρ or λ
marginal sweeps look flat, check baseline and consider a small **ρ × λ** panel at the
checkpoint with Alex; Pass A remains the empirical anchor.

**Knobs to characterize** (one slide each: 3 core equations, **bold the
knob**, figure below):

  ------------------------------------------------------------------------------------
  **Knob**                    **Alex's expectation**
  --------------------------- --------------------------------------------------------
  **ρ**                       Matters a lot (Pass C shows this)

  **λ**                       Matters a lot (Pass B starts it; needs full panel)

  **θ** (sigmoid center)      Matters; likely tied to **K/N** (success rate), not
                              "median of selected"

  **γ** (sigmoid slope)       Characterize

  **Distribution of**         Probably doesn't matter much (CLT on team averages) ---
  $\mathbf{A}_{\mathbf{i}}$   but **document** choice + SI robustness

  **Distribution of**         Fix from empirical ballpark; characterize
  $\mathbf{T}_{\mathbf{j}}$   

  **K/N** (selection rate)    **System feature** --- "everybody gets a trophy" vs
                              highly selective regimes
  ------------------------------------------------------------------------------------

**Not yet:** full statistical fitting to real data. At \~41:44: *"I'm
not caring about fitting to data yet --- just characterize what's going
on."*

**Pace:** \~two knobs per day → \~four days for a solid characterization
deck. **Checkpoint with Alex after the first two** (ρ and λ).

**Layer 3 --- Next big insight (after characterization): statistical
fitting, not curve matching**

**Do NOT:** pick ρ or λ by minimizing distance between empirical Hero
curve and simulated curve → that's **curve fitting**.

**DO:** define a **statistic of the raw data** for each parameter:

- **ρ:** e.g. **within-team correlation of ability** (maybe
  log-transformed) --- model-invariant, computable from data alone

- **λ:** a **roster-pressure statistic** --- autocorrelation / "if a
  teammate gets promoted, what does that tell you about your odds?"
  --- **not** the sim selection-score formula

If you nail that, you're "putting a metric on the effect" and "really
going somewhere."

PD14 magnitude (Model A vs B predictive comparison) is **related** but
PD15 is sharper: estimators tied to **parameters**, not just better
prediction. **Park magnitude until characterization is done** unless
Alex says otherwise.

**Other model notes from the conversation**

- **B/D vs L:** Use $\mathbf{L}_{\mathbf{C}}$ only for now; future work
  could split $\lambda_{B}$ and $\lambda_{D}.$

- **Notation:** σ used twice (team $\sigma_{j}$ vs sigmoid σ) ---
  fix. **θ** = sigmoid center (not median of selected). **γ** = sigmoid
  slope.

- **θ and K/N:** Centering θ likely depends on **K/N** (draft slots /
  population), a fixed **system property** (MBB vs Army differ) ---
  sweep it, don't collapse it.

- $\mathbf{A}_{\mathbf{i}}$ **distribution:** Alex
  expects **robustness** (enough spread; CLT on team means), not
  power-law dependence --- show alternatives in SI.

- **Process:** 57-item checklist is too many; same failure mode as
  cranking calculations that feel like progress but aren't the mission.

**How this supersedes the old checklist**

CHARLES_CHECKLIST.md was re-entry + run Pass A/B + PD14 magnitude. That
scaffold did its job.

PD15 says **archive it** and replace with something shorter, phased:

**Phase A --- Gallery honesty (1--2 days)**\
λ panel, sim double-plots, sort-and-chop back, fitted-distribution
callouts.

**Phase B --- Characterization deck (\~4 days)**\
ρ → λ → θ/γ → A distribution → $t_{j}$ → K/N. Checkpoint after ρ + λ.

**Phase C --- Statistical fitting (later)**\
Data statistics for ρˆ and λ̂ ; then revisit PD14 magnitude.

**Still parked:** B/D split, Rivanna hero rebuild, army figures, bin-16
prose polish.

**Open questions (Charles, 2026-08-03)**

1.  **Board vs screen:** When Alex said "flat without assortativity,"
    was that **Pass C on screen**? **Yes — Pass C.**

2.  **Double-plot target:** Left = $A_{i}$-binned, right =
    poolq_loo-binned, same sim run? **Yes — confirmed.**

3.  **λ sign on Model slide:** Use $S_i = A_i - \lambda L_C$ ($\lambda > 0$; congestion enters with a minus sign). Matches the meeting correction to Alex.

4.  **PD14:** Park until after Phase B, or keep as parallel track? **Park until after Phase B.**

**Bottom line**

You didn't waste the last two weeks. Alex said the Pass work
is **right**. The job now is **directed characterization** --- fewer
checklist items, standard slides, two curves every time --- then **fit ρ
and λ to data statistics**, not to curve shape.

**Checklist:** [`3-Master_Plan/re_entry/CHARLES_CHECKLIST.md`](../3-Master_Plan/re_entry/CHARLES_CHECKLIST.md) (PD15). Archived: [`CHARLES_CHECKLIST_archive_20260803.md`](../3-Master_Plan/re_entry/CHARLES_CHECKLIST_archive_20260803.md).
