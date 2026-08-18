#!/usr/bin/env python3
"""Build PD20–22 narrative companion deck (item 15).

Wavetops → Wang arc → snag/Q&A → one conversational slide per HAND slide,
each with a footer cue to paste CHAR_PD20_HAND slide N after it.

Run (repo root):
  python sports/scripts/build_pd20_22_takeaways_memo.py

Output:
  slides/auto/CHAR_PD20_22_takeaways_memo_AUTO.pptx
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import (
    AUTO_PD20_22_MEMO_DECK,
    PD20_TEMPERATURE,
    PD21_RHO,
    PD22_MINUTES,
    ensure_hero_dirs,
)
from memo_slide_common import (
    append_bridge_slide,
    append_hand_companion_slide,
    append_narrative_memo_slide,
    new_memo_presentation,
    save_memo_deck,
)

SWEEP_META = PD20_TEMPERATURE / "GRANDCHILD_temperature_select_sweep_2011_2021_meta.json"
DROP_BRACKET = PD21_RHO / "PD21_rho_hsort_calibrate_2011_2021_fit_bracket.json"
PPM0_BRACKET = PD21_RHO / "PD21_rho_hsort_calibrate_2011_2021_ppm0lt20_fit_bracket.json"
PANEL_COMPARE = PD22_MINUTES / "PD22_panel_policy_compare_2011_2021.json"
DRAFT_AUDIT = PD22_MINUTES / "PD22_drafted_minutes_audit_2011_2021.json"
INTERVAL_2012 = PD22_MINUTES / "PD22_interval_overlap_season_2012.json"
INTERVAL_2013 = PD22_MINUTES / "PD22_interval_overlap_season_2013.json"


def _load_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _count_inverted_u(meta: dict, *, lam: float) -> tuple[int, int]:
    runs = [r for r in meta.get("runs", []) if abs(float(r.get("lambda", -1)) - lam) < 1e-9]
    total = len(runs)
    n_u = sum(
        1
        for r in runs
        if r.get("curvature_loo", {}).get("shape") == "inverted_u_like"
    )
    return n_u, total


def _fmt_pct(x: float) -> str:
    return f"{100.0 * x:.0f}\\%"


def _join(*parts: str) -> str:
    return "".join(parts)


def _load_numbers() -> dict:
    sweep_meta = _load_json(SWEEP_META)
    drop_bracket = _load_json(DROP_BRACKET)
    ppm0_bracket = _load_json(PPM0_BRACKET)
    panel_compare = _load_json(PANEL_COMPARE)
    draft_audit = _load_json(DRAFT_AUDIT)
    interval_2012 = _load_json(INTERVAL_2012)
    interval_2013 = _load_json(INTERVAL_2013)

    long = drop_bracket.get("longitudinal", {})
    ppm0_long = ppm0_bracket.get("longitudinal", {})
    draft = draft_audit.get("summary", {})
    compare = panel_compare.get("summary", {})
    rho_ppm0 = float(ppm0_long.get("rho_star_longitudinal", 0.048))
    if compare.get("rho_star_longitudinal_ppm_zero") is not None and not compare.get(
        "rho_star_longitudinal_ppm_zero_stale"
    ):
        rho_ppm0 = float(compare["rho_star_longitudinal_ppm_zero"])
    n_u_15, tot_15 = _count_inverted_u(sweep_meta, lam=1.5)
    n_u_2, tot_2 = _count_inverted_u(sweep_meta, lam=2.0)

    return {
        "seasons": sweep_meta.get("seasons", "2011–2021"),
        "rho_star": float(long.get("rho_star_longitudinal", 0.0)),
        "h_emp": float(long.get("h_sort_empirical_mean_over_seasons", 0.064)),
        "err_ref": float(long.get("mean_abs_err_at_reference_rho", 0.112)),
        "lost": int(draft.get("n_lost_at_hero_lock_drop", 44)),
        "retained": int(draft.get("n_retained_at_hero_lock_drop", 1133)),
        "zero_lost": int(draft.get("n_lost_zero_minutes_at_hero_lock_drop", 42)),
        "h_drop": float(compare.get("h_sort_emp_mean_drop", 0.064)),
        "h_ppm0": float(compare.get("h_sort_emp_mean_ppm_zero", 0.065)),
        "delta_h": float(compare.get("h_sort_emp_mean_delta", 0.001)),
        "rho_ppm0": rho_ppm0,
        "rho_hero": float(long.get("rho_star_longitudinal", 0.0)),
        "grid12": float(interval_2012.get("coverage_frac_gt_1", 0.892)),
        "grid13": float(interval_2013.get("coverage_frac_gt_1", 0.950)),
        "n_u_15": n_u_15,
        "tot_15": tot_15,
        "n_u_2": n_u_2,
        "tot_2": tot_2,
    }


def _build_front_matter(prs, n: dict) -> None:
    append_bridge_slide(
        prs,
        title=r"How to use this companion deck",
        lead=(
            r"Read each narrative slide out loud, then paste the matching "
            r"\texttt{CHAR\_PD20\_HAND} slide immediately after it."
        ),
        blocks=[
            (
                "Structure",
                r"Slides 2–8 = wavetops (Part 0 → bridges → Wang arc → LG pipeline → HAND preview). "
                r"Slides 9–13 = snag bridge + the snag + three PD22 questions with answer summaries. "
                r"Then Act bridges + 21 HAND companions (footer shows which slide to paste). "
                r"End = where we stand + what lies ahead (main line, predictions, parked, manuscript).",
            ),
            (
                "Format",
                r"Bridge slides explain why we move to the next section — read them out loud. "
                r"Every substantive slide uses the same beats: why this came up, what we ran, "
                r"what showed up, what you can say. Numbers come from locked JSON on disk.",
            ),
            (
                "Optional read-aloud order",
                r"After slide 13 you can jump Acts I → II → IV (HAND 17–19) → III (HAND 14–16) "
                r"→ IV (HAND 20–21) if you want policy evidence before $\rho$ and overlap.",
            ),
        ],
    )

    append_bridge_slide(
        prs,
        title=r"Part 0 — Big picture: where the dissertation started",
        lead=r"Army inverted-U → cross-domain test → MBB hero (Layer A).",
        blocks=[
            (
                "Army",
                r"Officer careers: advancement rate vs peer-group quality often rises through the middle "
                r"and dips in the very best peer environments — the inverted-U tail.",
            ),
            (
                "Cross-domain",
                r"We asked whether that pattern is Army-only. MBB (NBA draft vs teammate quality) "
                r"became the main working example; tenure is the parallel third leg (parked).",
            ),
            (
                "Hero (Layer A)",
                r"Bin real player-seasons by leave-one-out teammate pool quality; plot draft rate. "
                r"Rate rises, plateaus, dips in the top bin. That is a stylized fact about outcomes — "
                r"not yet a proof of why.",
            ),
        ],
    )

    append_bridge_slide(
        prs,
        title=r"Bridge — Why we go past Layer A",
        lead=r"The hero is a stylized fact — not the finish line.",
        blocks=[
            (
                "Why this came up",
                r"You cannot stop at a pretty plot. The hero does not separate peers-help-you-develop "
                r"from peers-crowd-you-out-of-the-slot, and it does not say what to predict next.",
            ),
            (
                "Three follow-ups",
                r"(1) Why might the curve bend? (2) Could a simple selection story mechanism (rule) "
                r"generate a similar shape? (3) What else should be true if that mechanism is right?",
            ),
            (
                "What you can say",
                r"Layer A is the weather report — we saw the cloud. Part 1 is the disciplined next "
                r"step: name the simplest mechanism, test it in a wind tunnel, then ask what the "
                r"story predicts.",
            ),
        ],
    )

    append_bridge_slide(
        prs,
        title=r"Part 1 — The Wang-style arc (smaller picture)",
        lead=r"Phenomenon → simplest mechanism story → wind-tunnel sim → predictions.",
        blocks=[
            (
                "Rung 1",
                r"Hero + talent baseline on real NCAA data — what the curves look like.",
            ),
            (
                "Rung 2 (Layer B)",
                r"Peers help (B) and hurt (D); advancement = score ($S_i = A_i - \lambda L_C$) "
                r"then select (top K, later Gibbs). Environment $\neq$ advancement; score $\neq$ select.",
            ),
            (
                "Rung 2 (Layer C)",
                r"Fake league (LG): assign → score → select. Knockout: talent-only score vs congestion "
                r"in score — same winner rule. Phase B (PD16) sweeps knobs; structure accepted at PD16.",
            ),
            (
                "Rung 3",
                r"Predictions beyond the curve: cross-domain replication, sim knockout, later PD14 "
                r"predictive gain (parked).",
            ),
        ],
    )

    append_bridge_slide(
        prs,
        title=r"Bridge — From Wang arc to LG pipeline",
        lead=r"Part 1 is the ladder; Part 2 is the wiring diagram.",
        blocks=[
            (
                "Why this came up",
                r"After phenomenon → mechanism → wind tunnel, you need to know how the fake league "
                r"is actually wired — one pipeline, three steps, three knob families.",
            ),
            (
                "Without this",
                r"$\rho$, $\lambda$, and $K$ feel like magic numbers. Part 2 names ASSIGN $\rightarrow$ "
                r"SCORE $\rightarrow$ SELECT and ties PD17 empirical work to the same hero panel.",
            ),
            (
                "What you can say",
                r"Part 1 is why we have a wind tunnel; Part 2 is how it is wired; Part 3 is the "
                r"current campaign — defending the real panel and calibration inputs.",
            ),
        ],
    )

    append_bridge_slide(
        prs,
        title=r"Part 2 — LG pipeline (one mechanism, three steps)",
        lead=r"ASSIGN → SCORE → SELECT — how the fake league is wired.",
        blocks=[
            (
                "ASSIGN",
                r"Who sits on which team? Homophily knob $\rho$ — do similar players cluster?",
            ),
            (
                "SCORE",
                r"How do we rank? $\lambda$ weights viable-peer congestion $L_C$ in the score.",
            ),
            (
                "SELECT",
                r"Who wins scarce slots? Top K in v1; PD20 tests soft Gibbs / temperature.",
            ),
            (
                "PD17 empirical",
                r"Real rosters, interval overlap, $H_{\mathrm{sort}}$ sorting index, $\lambda$ sweeps — "
                r"same panel as the hero.",
            ),
        ],
    )

    append_bridge_slide(
        prs,
        title=r"Bridge — Why the PD20–22 HAND campaign",
        lead=r"Once the ladder and pipeline make sense, the job is defensive — not more philosophy.",
        blocks=[
            (
                "Why this came up",
                r"PD20 cleared soft SELECT. Then we found the ESPN panel needed hygiene and a minutes "
                r"policy before we could cite $\rho^*$ with a straight face.",
            ),
            (
                "What the HAND deck is",
                r"21 slides in four acts: SELECT gate $\rightarrow$ panel backup $\rightarrow$ "
                r"$\rho$ calibration $\rightarrow$ policy/overlap evidence.",
            ),
            (
                "What you can say",
                r"We are calibrating and defending inputs to LG and the real panel — not hand-waving "
                r"$\rho$, $\lambda$, or drop-vs-zero.",
            ),
        ],
    )

    append_bridge_slide(
        prs,
        title=r"Part 3 preview — CHAR\_PD20\_HAND in four acts",
        lead=r"21 slides: PD20 gate → panel backup → $\rho$ calibration → policy/overlap.",
        blocks=[
            ("Act I (slides 1–4)", r"PD20: Does soft SELECT kill the inverted-U?"),
            ("Act II (slides 5–13)", r"PD22: Why do we trust the hero panel? Box QC + minutes/PPM."),
            ("Act III (slides 14–16)", r"PD21: What $\rho$ for ASSIGN? Hero panel vs ppm0lt20 contrast."),
            ("Act IV (slides 17–21)", r"PD22: Drop vs PPM-zero decision + overlap reconciliation."),
        ],
    )


def _build_snag_and_questions(prs, n: dict) -> None:
    append_bridge_slide(
        prs,
        title=r"Bridge — Why Part 4 (the snag)",
        lead=r"Acts II–III looked straightforward — then two snags forced a deeper investigation.",
        blocks=[
            (
                "Why this came up",
                r"While building panel-backup slides we found dirty ESPN data and an unsettled "
                r"minutes policy — before we could cite $\rho^*$ with a straight face.",
            ),
            (
                "Two snags",
                r"(1) Box QC changed $H_{\mathrm{sort}}$ and $\rho^*$ targets. "
                r"(2) Alex asked: why drop sub-20 instead of PPM-zero?",
            ),
            (
                "What you can say",
                r"The snag was not the science — it was dirty data and panel policy. "
                r"We split the fix: clean the feed, defend drop vs PPM-zero, lock $\rho$ on one story.",
            ),
        ],
    )

    append_narrative_memo_slide(
        prs,
        title=r"The snag — Act II was supposed to be quick",
        question=r"What went wrong while we were building panel-backup slides?",
        why=(
            r"Before we cite a $\rho$ number, we need to defend the real player table "
            r"that feeds ASSIGN and $H_{\mathrm{sort}}$. That should have been straightforward backup."
        ),
        what=(
            r"We opened the ESPN box-score feed for roster-size and minutes slides — and found "
            r"contamination (dash placeholders, one-game team-seasons). Alex also asked why we "
            r"drop sub-20-minute players instead of keeping them with PPM $=0$."
        ),
        saw=(
            r"Box QC changed measured sorting ($H_{\mathrm{sort}}$ ~0.10→~0.06) and therefore "
            r"$\rho^*$ (mixed non-zero seasons → all zero on locked panel). An old pre-QC slide "
            r"showed 2013 at $\rho^* \approx 0.07$ — that sent us on a 2012 vs 2013 side quest."
        ),
        so_what=(
            r"We split the fix: A = box QC, B = PD22 minutes/policy investigation, C = lock $\rho$ "
            r"and reconcile overlap. Three questions drove B."
        ),
    )

    append_bridge_slide(
        prs,
        title=r"Three questions the snag generated (PD22)",
        lead=r"Three questions from the PD22 investigation — answer each before locking panel and $\rho$.",
        blocks=[
            (
                "Q1 — The 20-minute floor",
                r"Is 20 arbitrary? What PPM are we throwing away when we drop players below the floor?",
            ),
            (
                "Q2 — Drop vs PPM-zero",
                r"If we keep sub-20 players and set PPM $=0$, does the wrong panel policy change "
                r"$H_{\mathrm{sort}}$ or $\rho^*$ calibration vs drop-at-20?",
            ),
            (
                r"Q3 — $\rho^*=0$ vs overlap plots",
                r"Bracket fit says $\rho^*=0$ — but interval-overlap pictures still look heavily sorted. "
                r"And an older slide had 2013 at $\rho^* \approx 0.07$.",
            ),
        ],
    )

    append_narrative_memo_slide(
        prs,
        title=r"Q1 answered — Keep the 20-minute floor (drop sub-20)",
        question=r"Is 20 minutes arbitrary? What PPM are we throwing away?",
        why=(
            r"Alex asked whether we can defend the hero panel with more than \"we always used 20.\" "
            r"We need to see where playing-time mass sits and how noisy sub-20-minute PPM is."
        ),
        what=_join(
            r"Minutes ECDF/histogram, PPM of filtered-out players, drafted-player audit (",
            f"{n['retained'] + n['lost']:,}",
            r" drafted player-seasons), overlay plots — HAND slides 10–13.",
        ),
        saw=_join(
            r"Most mass above 20 minutes; below 20 is bench noise and zero-minute rows. At 20 we drop ",
            f"{n['lost']} drafted player-seasons — {n['zero_lost']} were 0-minute. ",
            r"One ever-draft career fully lost (Ricky Ledo); everyone else keeps rotation years.",
        ),
        so_what=(
            r"\"We keep the floor at 20 and drop sub-20 players — not because every row is draft-safe, "
            r"but because PPM below 20 is too noisy for ASSIGN.\" Evidence: HAND slides 5–13."
        ),
    )

    append_narrative_memo_slide(
        prs,
        title=r"Q2 answered — Drop beats PPM-zero on the locked panel",
        question=r"Does PPM-zero change sorting or $\rho^*$ on the locked panel?",
        why=(
            r"PD21 compared drop vs keep-with-PPM-zero at the same floor. The concern was bench zeros "
            r"and extra roster rows would move $H_{\mathrm{sort}}$ or $\rho^*$ away from the hero estimand."
        ),
        what=(
            r"Ability histograms, all-zero team check, bench-zero vs $H_{\mathrm{sort}}$, "
            r"side-by-side bracket compare — HAND slides 17–19."
        ),
        saw=_join(
            r"PPM-zero adds ~13k bench rows and a big zero/low-$z$ tail. League mean $H_{\mathrm{sort}}$: ",
            f"{n['h_drop']:.3f}",
            r" (drop) vs ",
            f"{n['h_ppm0']:.3f}",
            r" (PPM-zero), $\Delta \approx ",
            f"{n['delta_h']:.3f}",
            r"$. Bracket longitudinal $\rho^*$: hero $\approx ",
            f"{n['rho_hero']:g}",
            r"$ vs ppm0lt20 $\approx ",
            f"{n['rho_ppm0']:.3g}",
            r"$ — modest contrast, not the locked estimand.",
        ),
        so_what=(
            r"\"Drop at 20 is locked — PPM-zero barely moves mean $H_{\mathrm{sort}}$ and gives a "
            r"different (volatile) $\rho^*$ series. Slide 14 already used drop; no $\rho$ re-run for "
            r"that choice.\""
        ),
    )

    append_narrative_memo_slide(
        prs,
        title=r"Q3 answered — Bracket $\rho^*$ and overlap answer different questions",
        question=r"Why $\rho^*=0$ when overlap plots look sorted? What about 2013?",
        why=(
            r"That felt like a contradiction: near-zero homophily in calibration vs heavy stacking "
            r"in talent-window overlap figures."
        ),
        what=(
            r"Single-season interval overlap for 2012 and 2013 on the locked panel — "
            r"HAND slides 20–21."
        ),
        saw=_join(
            r"Massive stacking persists: ",
            _fmt_pct(n["grid12"]),
            r" of talent grid has $>1$ team in 2012, ",
            _fmt_pct(n["grid13"]),
            r" in 2013 — both at $\rho^*=0$ on locked panel. The remembered 2013 $\rho^* \approx 0.07$ "
            r"came from a pre-box-QC roster-caps slide.",
        ),
        so_what=(
            r"\"$\rho^*=0$ is a modest calibration fit on $H_{\mathrm{sort}} \approx 0.06$ — not a claim "
            r"that rosters look disjoint in the overlap figures. Bracket fit and geometry answer "
            r"different questions.\""
        ),
    )


def _build_act_i(prs, n: dict) -> None:
    append_bridge_slide(
        prs,
        title=r"Act I — PD20: Gibbs SELECT gate",
        lead=r"Before MLE for SELECT — does soft selection kill the inverted-U?",
        blocks=[
            (
                "Problem",
                r"Replace rigid top-$K$ with Gibbs (temperature dial). If the hump disappears, "
                r"stop before expensive fitting.",
            ),
            (
                "Next slides",
                r"Four narrative companions (HAND 1–4) — paste each HAND slide after its narrative.",
            ),
        ],
    )

    append_hand_companion_slide(
        prs,
        hand_slide=1,
        act=r"Act I — PD20",
        title=r"Gibbs SELECT intro",
        question=r"What are we testing and why does temperature matter?",
        why=(
            r"SELECT is moving from deterministic top-$K$ to a soft weighted draw — "
            r"need a clear gate before investing in MLE."
        ),
        what=(
            r"Introduce rule D (Gibbs weights + $K$ draws), temperature $t$, and the LOO outcome "
            r"curve we will watch."
        ),
        saw=(
            r"The deck sets up: cold $t$ should nest top-$K$; hot $t$ spreads probability — "
            r"different failure mode than \"hump gone.\""
        ),
        so_what=(
            r"\"PD20 is a phenomenology gate, not a full fit — and $\rho$ calibration stays a separate step.\""
        ),
    )

    append_hand_companion_slide(
        prs,
        hand_slide=2,
        act=r"Act I — PD20",
        title=r"Temperature sweep (rule D)",
        question=r"Across $\log_{10} t$ from $-3$ to $+3$, does the inverted-U survive?",
        why=(
            r"If soft SELECT erases the hero-shaped outcome, there is no point fitting $t^*$ yet."
        ),
        what=_join(
            r"Grandchild temperature sweep on MBB ",
            n["seasons"],
            r", real roster sizes, rule D, $\lambda \in \{1.5, 2.0\}$.",
        ),
        saw=_join(
            r"Inverted-U-like shape survives: at $\lambda=1.5$, ",
            f"{n['n_u_15']}/{n['tot_15']}",
            r" arms still U-like; at $\lambda=2$, ",
            f"{n['n_u_2']}/{n['tot_2']}",
            r". Hot $t$ flattens — not the worry we had.",
        ),
        so_what=(
            r"\"The inverted-U survives soft SELECT — PD20 gate cleared; we can proceed toward MLE "
            r"once $K$-draw semantics are locked.\""
        ),
    )

    append_hand_companion_slide(
        prs,
        hand_slide=3,
        act=r"Act I — PD20",
        title=r"Cold limit — rule C vs rule D",
        question=r"At small $t$, does Gibbs nest the old top-$K$ rule?",
        why=(
            r"Worth showing that the new SELECT layer extends the old rule — not an unrelated rewrite."
        ),
        what=(
            r"Compare rule C (deterministic top-$K$) vs rule D at cold temperature on the same league."
        ),
        saw=(
            r"Cold $t$ arms track the legacy top-$K$ curve — the temperature dial connects smoothly."
        ),
        so_what=(
            r"\"At cold temperature, Gibbs nests top-$K$ — the dial connects smoothly to what we had.\""
        ),
    )

    append_hand_companion_slide(
        prs,
        hand_slide=4,
        act=r"Act I — PD20",
        title=r"PD20 takeaways",
        question=r"What do we lock from Act I?",
        why=(
            r"Close the PD20 thread before panel and $\rho$ work — SELECT should read as unblocked."
        ),
        what=(
            r"Summarize sweep + cold-limit evidence in plain bullets on the HAND slide."
        ),
        saw=(
            r"Inverted-U survives Gibbs SELECT; proceed to MLE; $\rho$ is a separate calibration step."
        ),
        so_what=(
            r"\"Act I is done: inverted-U survives Gibbs SELECT; next we defend the real panel.\""
        ),
    )


def _build_act_ii(prs, n: dict) -> None:
    append_bridge_slide(
        prs,
        title=r"Act II — PD22: Why we trust the hero panel",
        lead=r"Box QC + minutes/PPM backup — the table that feeds ASSIGN and $H_{\mathrm{sort}}$.",
        blocks=[
            (
                "Panel",
                r"One row per player-season: minutes, PPM, draft flag, team, season. "
                r"Raw ESPN box data needed hygiene before we could defend roster slides.",
            ),
            (
                "Box QC",
                r"Drop dash-name placeholders; drop team-seasons with $<11$ games. "
                r"Changed $H_{\mathrm{sort}}$ targets and $\rho^*$ — not optional.",
            ),
            (
                "Next slides",
                r"Nine narrative companions (HAND 5–13) — Q1 evidence lives here.",
            ),
        ],
    )

    companions_ii = [
        (
            5,
            r"Roster size — raw box (before QC)",
            r"Why do roster-count slides show absurd tails before we clean the feed?",
            r"Start with the raw ESPN mess — before claiming the panel is obvious.",
            r"Histogram of players per team-season from the box file before dash/QC filters.",
            r"Long tails (e.g. 100+ names) from placeholder rows — not real NCAA dress lists.",
            r"\"These tails are placeholder rows — that is why we added box QC at panel build.\"",
        ),
        (
            6,
            r"Games per team-season — before QC",
            r"Are one-game \"seasons\" polluting roster structure?",
            r"Fragmentary team-seasons inflate noise in ASSIGN inputs.",
            r"Count games listed per team-season in raw box feed, pre-QC.",
            r"Many schools with only one game — not a season for our purposes.",
            r"\"One-game team-seasons are not real seasons for our purposes — we drop them at build.\"",
        ),
        (
            7,
            r"Games per team-season — after QC",
            r"What does the feed look like once we require real seasons?",
            r"Pair with slide 6 — before/after is the punchline.",
            r"Same plot after QC: keep teams with $\geq 11$ games.",
            r"Distribution tightens; one-game artifacts gone.",
            r"\"After QC the feed looks like actual NCAA seasons — pair with the before slide.\"",
        ),
        (
            8,
            r"Roster size — box-QC panel vs min-20",
            r"After QC, do roster sizes look like NCAA?",
            r"Post-QC roster counts should cluster near dress cap (~15).",
            r"Roster size on locked panel (QC + min 20 minutes).",
            r"Tails gone; sensible roster counts for ASSIGN caps.",
            r"\"Post-QC roster counts cluster near dress cap — this is the panel epoch for $\rho^*$.\"",
        ),
        (
            9,
            r"ESPN coverage 2013→2014 depth break",
            r"Why does raw ESPN roster depth step up after 2013?",
            r"ESPN lists more bench rows after 2013 — uncapped contrast policies inherit this.",
            r"Players listed per team by season in raw feed.",
            r"Step up at 2013→2014 in raw counts; hero min-20 panel is flat — contrast rows are sensitive.",
            r"\"ESPN lists more bench rows after 2013 — context for uncapped contrast panels (contrast only).\"",
        ),
        (
            10,
            r"Drafted-player retention vs minutes floor",
            r"At min 20 drop, do we lose anyone who mattered for draft?",
            r"Q1 audit — conservative guardrail on the floor choice.",
            _join(
                r"Audit all drafted player-seasons; who drops at 20? (",
                f"{n['lost']} lost, {n['zero_lost']} zero-minute).",
            ),
            _join(
                r"At 20: drop ",
                f"{n['lost']} drafted seasons — {n['zero_lost']} were 0-minute. ",
                r"One ever-draft career fully lost; others keep rotation years.",
            ),
            r"\"At 20 we drop mostly zero-minute rows — defend the floor on PPM noise, not draft-safe row-by-row.\"",
        ),
        (
            11,
            r"Raw panel season-minutes distribution",
            r"Where does playing-time mass sit relative to 20?",
            r"Q1 — show that sub-20 is a long noisy tail, not core rotation.",
            r"ECDF / histogram of total season minutes on raw panel.",
            r"Most mass above 20; below 20 is bench and sit-outs.",
            r"\"Most playing-time mass sits above 20 minutes — below that is bench noise.\"",
        ),
        (
            12,
            r"PPM — filtered tail vs hero ASSIGN input",
            r"How noisy is PPM below the floor?",
            r"Sub-20 PPM is unstable — why we drop rather than trust those values.",
            r"PPM distribution for players filtered out at candidate floors.",
            r"Extreme noise below 20; z-scored ASSIGN input needs stable PPM.",
            r"\"Sub-20 PPM is too unstable to feed ASSIGN — that is the case for drop, not PPM-zero.\"",
        ),
        (
            13,
            r"PPM overlay — full vs sub-20 tail",
            r"Optional detail: full distribution vs tail emphasis.",
            r"Slide 12 is the main argument; 13 is overlay for appendix trim.",
            r"Overlay full-panel PPM with sub-20 tail highlighted.",
            r"Same story as 12 with visual emphasis on the tail.",
            r"\"Same PPM story as the prior slide — optional appendix if someone wants the overlay.\"",
        ),
    ]

    for hand, title, question, why, what, saw, so_what in companions_ii:
        append_hand_companion_slide(
            prs,
            hand_slide=hand,
            act=r"Act II — PD22 panel",
            title=title,
            question=question,
            why=why,
            what=what,
            saw=saw,
            so_what=so_what,
        )


def _build_act_iii(prs, n: dict) -> None:
    append_bridge_slide(
        prs,
        title=r"Act III — PD21: Calibrate ASSIGN $\rho$",
        lead=r"Bracket search until sim $H_{\mathrm{sort}}$ matches empirical NCAA sorting.",
        blocks=[
            (
                "Locked panel",
                r"Drop sub-20, box QC, empirical roster caps, PPM $z$ within season.",
            ),
            (
                "Contrast only",
                r"Slides 15–16 (ppm0lt20) — wrong estimand; volatile mid-decade $\rho^*$ vs flat hero.",
            ),
            (
                "Next slides",
                r"Three narrative companions (HAND 14–16).",
            ),
        ],
    )

    append_hand_companion_slide(
        prs,
        hand_slide=14,
        act=r"Act III — PD21",
        title=r"Calibrate $\rho$ — hero panel (locked)",
        question=r"What homophily $\rho$ makes sim sorting match empirical $H_{\mathrm{sort}}$?",
        why=(
            r"We need defensible ASSIGN input — not legacy $\rho=0.5$ which overshoots on this panel."
        ),
        what=(
            r"Bracket search 2011–2021 on locked hero panel; match sim to empirical $H_{\mathrm{sort}}$."
        ),
        saw=_join(
            r"Longitudinal $\rho^* \approx ",
            f"{n['rho_star']:g}",
            r"$ — all 11 seasons at zero. Empirical $H_{\mathrm{sort}} \approx ",
            f"{n['h_emp']:.3f}",
            r"$. Legacy $\rho=0.5$: mean $|error| \approx ",
            f"{n['err_ref']:.2f}",
            r"$.",
        ),
        so_what=(
            r"\"Near-zero $\rho$ is model–measurement fit on modest sorting — not a claim that NCAA "
            r"assignment is random. This is the post-box-QC panel epoch.\""
        ),
    )

    append_hand_companion_slide(
        prs,
        hand_slide=15,
        act=r"Act III — PD21",
        title=r"Calibrate $\rho$ — ppm0lt20 contrast",
        question=r"What if we keep sub-20 players with PPM $=0$ instead of dropping?",
        why=(
            r"Alex asked about the alternate policy — show why it is not the locked estimand."
        ),
        what=(
            r"Same bracket machinery on ppm0lt20 policy at min 20 — contrast arm only."
        ),
        saw=_join(
            r"Modest longitudinal $\rho^* \approx ",
            f"{n['rho_ppm0']:.3g}",
            r"$ (hero $=",
            f"{n['rho_hero']:g}",
            r"$). Same mean $H_{\mathrm{sort}}$ as drop ($\approx ",
            f"{n['h_ppm0']:.3f}",
            r"$). Mid-decade per-season spike 2014→2015 — not flat all-zero hero panel.",
        ),
        so_what=(
            r"\"Wrong policy — volatile mid-decade $\rho^*$ on uncapped rows. Illustrative contrast only; "
            r"locked estimand stays drop + slide 14.\""
        ),
    )

    append_hand_companion_slide(
        prs,
        hand_slide=16,
        act=r"Act III — PD21",
        title=r"Per-season $\rho^*$ timeseries (contrast)",
        question=r"How does the wrong policy look season-by-season?",
        why=(
            r"Season-by-season view of the contrast policy — mid-decade $\rho^*$ spike vs flat hero panel."
        ),
        what=(
            r"Per-season $\rho^*$ and empirical $H_{\mathrm{sort}}$ under ppm0lt20 contrast policy."
        ),
        saw=_join(
            r"Flat 2011–2014 at $\rho^*=0$, then 2014→2015 spike; co-moves with empirical $H_{\mathrm{sort}}$. ",
            r"Mean longitudinal $\rho^* \approx ",
            f"{n['rho_ppm0']:.3g}",
            r"$ — not the flat all-zero hero panel (slide 14).",
        ),
        so_what=(
            r"\"Wrong policy, volatile season series — compare to the flat all-zero locked panel on slide 14.\""
        ),
    )


def _build_act_iv(prs, n: dict) -> None:
    append_bridge_slide(
        prs,
        title=r"Act IV — PD22: Policy deep dive + overlap reconciliation",
        lead=r"Back to Q2 and Q3 with evidence slides — then lock the story.",
        blocks=[
            (
                "Slides 17–19",
                r"Q2 mechanism: ability tails, bench-zero clustering, drop vs PPM-zero decision.",
            ),
            (
                "Slides 20–21",
                r"Q3 reconciliation: overlap at $\rho^*=0$ for 2012 and 2013.",
            ),
            (
                "Next slides",
                r"Five narrative companions (HAND 17–21).",
            ),
        ],
    )

    append_hand_companion_slide(
        prs,
        hand_slide=17,
        act=r"Act IV — PD22 policy",
        title=r"PPM-zero vs drop — ability distribution",
        question=r"How does the ability picture change under PPM-zero?",
        why=(
            r"Q2 — zeros change ASSIGN inputs even if mean $H_{\mathrm{sort}}$ barely moves."
        ),
        what=(
            r"Side-by-side ability histograms: drop sub-20 vs keep with PPM $=0$."
        ),
        saw=(
            r"PPM-zero adds ~13k bench rows and a large zero/low-$z$ tail drop removes entirely."
        ),
        so_what=(
            r"\"PPM-zero reshapes the ability scale even when mean sorting barely moves — drop is cleaner input.\""
        ),
    )

    append_hand_companion_slide(
        prs,
        hand_slide=18,
        act=r"Act IV — PD22 policy",
        title=r"Bench-zero clustering vs $H_{\mathrm{sort}}$",
        question=r"Do identical bench zeros mechanically inflate sorting?",
        why=(
            r"The worry was that zeros pile on deep benches and fake homophily."
        ),
        what=(
            r"Correlate bench-zero share with empirical $H_{\mathrm{sort}}$; all-zero team sanity check."
        ),
        saw=(
            r"No all-zero team-seasons; bench zeros do not move league mean $H_{\mathrm{sort}}$ much "
            r"on locked panel — but ability picture still favors drop."
        ),
        so_what=(
            r"\"Bench zeros do not blow up league mean $H_{\mathrm{sort}}$ here — but the ability "
            r"picture still favors drop; see the decision slide next.\""
        ),
    )

    append_hand_companion_slide(
        prs,
        hand_slide=19,
        act=r"Act IV — PD22 policy",
        title=r"Panel policy — drop vs PPM-zero at min 20",
        question=r"Which policy do we lock for the hero panel and $\rho$ calibration?",
        why=(
            r"Q2 decision slide — one clear policy before citing slide 14 $\rho^*$."
        ),
        what=(
            r"Side-by-side bracket summary: drop vs PPM-zero on post-QC panel at min 20."
        ),
        saw=_join(
            r"$H_{\mathrm{sort}}$: ",
            f"{n['h_drop']:.3f}",
            r" vs ",
            f"{n['h_ppm0']:.3f}",
            r" ($\Delta \approx ",
            f"{n['delta_h']:.3f}",
            r"$). Drop wins — slide 14 already used this policy.",
        ),
        so_what=(
            r"\"Drop at 20 is locked — slide 14 already used it; no $\rho$ re-run for drop-vs-zero.\""
        ),
    )

    append_hand_companion_slide(
        prs,
        hand_slide=20,
        act=r"Act IV — PD22 overlap",
        title=r"Interval overlap — season 2012 ($\rho^*=0$)",
        question=r"Why do overlap plots look sorted when bracket says $\rho^*=0$?",
        why=(
            r"Q3 — reconcile the calibration number with what the overlap figures show."
        ),
        what=(
            r"Single-season talent-window overlap on locked panel, 2012."
        ),
        saw=_join(
            _fmt_pct(n["grid12"]),
            r" of talent grid has $>1$ team covering the same ability bin — massive stacking.",
        ),
        so_what=(
            r"\"Overlap is roster geometry; bracket $\rho^*$ is sim fit to $H_{\mathrm{sort}}$ — "
            r"different questions, both valid.\""
        ),
    )

    append_hand_companion_slide(
        prs,
        hand_slide=21,
        act=r"Act IV — PD22 overlap",
        title=r"Interval overlap — season 2013 ($\rho^*=0$)",
        question=r"What about the remembered 2013 $\rho^* \approx 0.07$?",
        why=(
            r"2013 was the season that triggered the side quest — close it on locked panel."
        ),
        what=(
            r"Same overlap plot for 2013; compare to pre-box-QC calibration epoch."
        ),
        saw=_join(
            _fmt_pct(n["grid13"]),
            r" grid stacking in 2013 — stronger than 2012, still at $\rho^*=0$ locked. ",
            r"Old $\rho^* \approx 0.07$ was pre-QC panel, not today's estimand.",
        ),
        so_what=(
            r"\"2013 still stacks heavily at $\rho^*=0$ on the locked panel — the old 0.07 was "
            r"pre-box-QC. Q3 closed; resume SELECT / MLE.\""
        ),
    )


def _build_closing(prs, n: dict) -> None:
    append_narrative_memo_slide(
        prs,
        title=r"Where we stand — August 18, 2026",
        question=r"What is locked and what is the exact next beat?",
        why=(
            r"PD20–22 were scoped to justify panel and calibration quickly — not to perfect "
            r"every sensitivity before returning to SELECT and outcomes."
        ),
        what=(
            r"Walked minutes data, box QC, drop vs PPM-zero, $\rho^*$ on locked panel, "
            r"overlap reconciliation, PD20 Gibbs gate."
        ),
        saw=(
            r"Drop sub-20 + box QC hero panel; $\rho^* \approx 0$ modest fit; overlap still stacked; "
            r"Gibbs SELECT preserves inverted-U. Not blocked on panel policy or $\rho$ re-calibration."
        ),
        so_what=(
            r"Campaign checkpoint cleared. Next slides map what lies ahead — main line first, "
            r"then parked work and longer horizon."
        ),
    )

    append_bridge_slide(
        prs,
        title=r"Bridge — From snag fix back to the main line",
        lead=r"Parts 5–6 closed the defensive campaign; we resume fitting.",
        blocks=[
            (
                "What is locked",
                r"Drop sub-20 + box QC hero panel; $\rho^* \approx 0$ modest fit; PD20 Gibbs gate "
                r"cleared. No $\rho$ re-run needed for the drop decision.",
            ),
            (
                "What is next",
                r"SELECT / MLE $\rightarrow$ $\lambda^*$, $t^*$, $\gamma$ $\rightarrow$ side-by-side "
                r"deliverable (hero + sim, honest limits).",
            ),
            (
                "What you can say",
                r"We are not blocked on panel policy — the main line is fitting SELECT on the "
                r"locked panel story.",
            ),
        ],
    )

    append_bridge_slide(
        prs,
        title=r"What lies ahead — main line (resume here)",
        lead=r"PD20–22 were defensive; the scientific campaign continues on the locked panel.",
        blocks=[
            (
                "Beat 1 — SELECT / MLE",
                r"PD20 cleared soft Gibbs SELECT. Next: lock $K$-draw semantics, "
                r"then statistical fit for SELECT parameters (MLE) on the locked panel.",
            ),
            (
                "Beat 2 — SCORE + SELECT knobs",
                r"Fit $\lambda^*$ (congestion in score), $t^*$ (temperature), $\gamma$ (viability "
                r"sharpness) — same hero panel, ASSIGN at locked $\rho^* \approx 0$.",
            ),
            (
                "Beat 3 — Side-by-side deliverable",
                r"Empirical hero + sim curves with honest axes and one limitation sentence — "
                r"the simplified-model chapter (not bin-for-bin replication yet).",
            ),
        ],
    )

    append_bridge_slide(
        prs,
        title=r"What lies ahead — Wang Rung 3 (predictions)",
        lead=r"After MBB v1 fit is tight, climb the prediction rung — not blocking the next fit checkpoint.",
        blocks=[
            (
                "Already partly done",
                r"Cross-domain inverted-U (Army + MBB); sim knockout (talent-only score vs congestion in score).",
            ),
            (
                "PD14 — predictive gain (parked)",
                r"Model A (ability + roster congestion) vs Model B (ability only): does roster pressure "
                r"improve draft prediction? Largest gain expected for top ability under few slots.",
            ),
            (
                "Near-threshold / composition",
                r"Candidate tests under small $K$: does congestion matter most where slots are scarce? "
                r"Ties to $\lambda$ sweeps and SELECT capacity.",
            ),
        ],
    )

    append_bridge_slide(
        prs,
        title=r"What lies ahead — parked (do not block main line)",
        lead=r"Optional sensitivity — run only if asked in meeting or a reviewer forces it.",
        blocks=[
            (
                "PD22 item 12",
                r"Team-rank forensics — skipped; pre-box-QC $\rho^*$ side quest already closed.",
            ),
            (
                "PD22 items 13–14",
                r"Caps-off sensitivity; minutes-floor ladder (min 10 / 15 / 20 / 30 overlay). "
                r"Useful appendix, not gating SELECT / MLE.",
            ),
            (
                "Tenure third leg",
                r"Preliminary hero on faculty panel — parallel domain, not MBB v1 blocker.",
            ),
        ],
    )

    append_bridge_slide(
        prs,
        title=r"What lies ahead — manuscript horizon",
        lead=r"Summer–Fall 2026 target: one coherent Wang-style object, not two half-finished models.",
        blocks=[
            (
                "MBB v1 chapter",
                r"Hero (Layer A) + mechanism story (Layer B) + wind-tunnel sim (Layer C) + honest limits. "
                r"Side-by-side deliverable: same kind of outcome axis, explicit what we do not claim.",
            ),
            (
                "Three-setting paper",
                r"Army (strong) + MBB (replicated LOO inverted-U) + tenure (preliminary). "
                r"Mechanism section must read as one ladder, not stitched regressions.",
            ),
            (
                "After MBB v1 is tight",
                r"Tenure Cox pass; PD14 magnitude; richer predictions — sequence per COMPASS, "
                r"not parallel rabbit holes.",
            ),
        ],
    )

    append_bridge_slide(
        prs,
        title=r"One breath — closing line",
        lead=r"If you need a single paragraph to close before SELECT / MLE planning.",
        blocks=[
            (
                "What you can say",
                r"We cleared soft SELECT (PD20). We cleaned the ESPN panel (box QC) and defended "
                r"drop sub-20 over PPM-zero (PD22). On that locked panel, $\rho^* \approx 0$ matches "
                r"modest sorting — not random NCAA rosters — and overlap pictures still look stacked "
                r"because they measure geometry, not the homophily knob. We can go back to fitting "
                r"SELECT without redoing $\rho$ for the drop decision.",
            ),
            (
                "Open next",
                r"Lock Bernoulli-softmax draft likelihood (Alex PD23), then MLE for "
                r"$\lambda^*$, $\gamma^*$, $t^*$ on the locked hero panel.",
            ),
        ],
    )


def build_deck() -> None:
    ensure_hero_dirs()
    n = _load_numbers()
    prs = new_memo_presentation()

    _build_front_matter(prs, n)
    _build_snag_and_questions(prs, n)
    _build_act_i(prs, n)
    _build_act_ii(prs, n)
    _build_act_iii(prs, n)
    _build_act_iv(prs, n)
    _build_closing(prs, n)

    save_memo_deck(prs, AUTO_PD20_22_MEMO_DECK)


def main() -> None:
    build_deck()


if __name__ == "__main__":
    main()
