# 0. Read me first — re-entry (July 2026)

**Last synced:** 2026-08-04

**If you feel lost:** you are in the right place. **Stop opening other project folders** until you finish the documents below in order.

**Print hardcopies:** each re-entry doc has **`Last synced: YYYY-MM-DD`** under the title — keep the newest date when you purge old printouts.

This folder exists because the rest of the repo grew into a **reference library** for agents and for “already immersed” you. That library is still valuable. It is **not** the right entry point while you are re-orienting under time pressure.

---

## Your only reading list (for now)

Read these **in order**. Each is written to stand alone — you should not need to open other files every two sentences.

**#1 confusion (Charles lock):** Environment **`L_net = B − D`** ≠ advancement. Advancement = **score** (**`S_i`**, λ) then **select** (top K now). Locked in doc **02** and [`../BINDING_Selection_is_its_own_step.md`](../BINDING_Selection_is_its_own_step.md).

| Order | Document | Time | What you get |
|-------|----------|------|--------------|
| **1** | [01_The_Problem_in_Plain_English.md](01_The_Problem_in_Plain_English.md) | ~15 min | What the dissertation is asking; what the basketball “hero” curve is |
| **2** | [02_Three_Kinds_of_Model.md](02_Three_Kinds_of_Model.md) | ~25 min | Why “the model” confused you; three separate jobs (describe / explain / simulate) |
| **3** | [03_Three_Day_Basketball_Focus.md](03_Three_Day_Basketball_Focus.md) | ~10 min | What “done” means; what is out of scope |
| **4** | [04_Pass_A_and_Pass_B_in_Plain_English.md](04_Pass_A_and_Pass_B_in_Plain_English.md) | ~15 min | **Before any sim redo:** what Pass A and Pass B are, in sentences (empirical vs simulated, assignment, code map) |
| **5** | [05_Alex_Magnitude_Spec.md](05_Alex_Magnitude_Spec.md) | ~10 min | **Phase C (after characterization):** PD14 predictive importance — parked until [`CHARLES_CHECKLIST.md`](CHARLES_CHECKLIST.md) Phase B done |
| **—** | [06_Lambda_threshold_and_KN_memo.md](06_Lambda_threshold_and_KN_memo.md) | ~10 min | **Optional now:** sort-and-chop λ threshold (4/γ), θ vs K/N open work — read when doing Phase B θ/K/N |
| **—** | [07_Phase_B_Characterization_Slides_Explained.md](07_Phase_B_Characterization_Slides_Explained.md) | ~20 min | **When presenting Phase B deck:** plain-English slide-by-slide walkthrough |
| **—** | [08_PD16_Alex_meeting_takeaways.md](08_PD16_Alex_meeting_takeaways.md) | ~15 min | **After PD16 (Aug 4):** team L_C, θ from K/N, L_C-vs-ρ diagnostics, calibration roadmap |

**PDF:** from repo root:

```bash
./scripts/convert_single_md_to_pdf.sh 3-Master_Plan/re_entry/01_The_Problem_in_Plain_English.md
./scripts/convert_single_md_to_pdf.sh 3-Master_Plan/re_entry/02_Three_Kinds_of_Model.md
./scripts/convert_single_md_to_pdf.sh 3-Master_Plan/re_entry/03_Three_Day_Basketball_Focus.md
./scripts/convert_single_md_to_pdf.sh 3-Master_Plan/re_entry/04_Pass_A_and_Pass_B_in_Plain_English.md
./scripts/convert_single_md_to_pdf.sh 3-Master_Plan/re_entry/05_Alex_Magnitude_Spec.md
```

---

## What we are **not** doing right now

- We are **not** deleting or throwing away prior work.
- We are **not** asking you to read agent mail, COMPASS memos, Pertinent Thoughts, or the old 14-document print stack.
- We are **not** requiring you to reconcile every notation variant across Army / basketball / tenure in one sitting.

See [PARKED_FOR_LATER.md](PARKED_FOR_LATER.md) for a honest list of “good docs, wrong moment.”

---

## After the three documents

**Your manual checkoff (beginning → end):** [`CHARLES_CHECKLIST.md`](CHARLES_CHECKLIST.md) — **post-PD16** (Phase B deck sign-off → team L_C / θ(K/N) / L_C-vs-ρ → Phase C calibration). Mark what **you** ran, wrote, or said. Ignore “Done” tables in OPORD / doc 03 / COMPASS for personal progress.

**Meeting context:** [`../../transcripts/PD16_notes.md`](../../transcripts/PD16_notes.md) (Aug 4); narrative [`08_PD16_Alex_meeting_takeaways.md`](08_PD16_Alex_meeting_takeaways.md). Prior arc: [`PD15_notes.md`](../../transcripts/PD15_notes.md). Archived checklists: [`archive/checklists/`](archive/checklists/README.txt) (`CHARLES_CHECKLIST_archive_20260804_pd15.md`, `CHARLES_CHECKLIST_archive_20260803.md`).

When the three layers make sense again, you can optionally open:

- [`Model.pdf`](Model.pdf) / [`Model.pptx`](Model.pptx) — **your one-slide story** (assign → score → select, unified **S_i**, Alex v1 **(B−D)=−L_C**, empirical Naïve/Hero, knockout **λ=0**)
- `3-Master_Plan/plans/20260721_hero_model_reset.plan.md` — longer working plan (same story, more detail)
- `3-Master_Plan/re_entry/HEROs_and_PASSes/` — subfolders: `pass_a/`, `pass_b/`, `pass_c_rho/`, `sort_chop_lambda/`, `theta/`, `slides/` (see `slides/README.txt`; hand-deck JPEGs in `slides/HAND_slides_images/`)

**Alex v1 minimal model (Jul 2026):** empirical hero + talent baseline; generative **assign → score (`S_i`) → select (top K)** with **λ=0** vs **S_i = A_i − λ·L_C** knockout; side-by-side figure + limitation sentence. **ρ** (assignment assortativity) ablation is optional follow-up — see [`../../sports/540_READ_ME_SIM.md`](../../sports/540_READ_ME_SIM.md) and [`model_OPORD.md`](model_OPORD.md).

**Sim re-entry:** agents doing generative code start at **`sports/540_READ_ME_SIM.md`**, not archived `538D` notebooks.

**Do not open** `sports/documents/Hero_Model_Three_Layers_Memo.md` until doc 02 feels easy — it is a short reference card, not a re-entry guide.

---

## For agents

When Charles says he is **re-entering** or **lost**, default to docs in **`3-Master_Plan/re_entry/`** only. Write new explanatory prose here (narrative, inline definitions). Do not add cross-links to `obsolete/`, agent reports, or shorthand memos unless Charles asks.
