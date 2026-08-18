"""Shared PD21 AUTO slide copy — authoritative for HAND paste (Aug 2026).

Charles copies title, subtitle, bullets, and claim verbatim from AUTO decks.
Hero panel = min-20 drop + box QC + roster caps (HAND20 slide 14 — hero calibration).
ppm0lt20 = contrast only (HAND20 slides 15–16), not the locked calibration estimand.
"""

from __future__ import annotations

from pd22_slide_common import mapprox, marrow


def is_contrast_panel(fit: dict) -> bool:
    panel = fit.get("panel") or {}
    if panel.get("panel_mode") == "ppm_zero_below":
        return True
    return panel.get("ppm_zero_below_minutes") is not None


def panel_bullet(fit: dict) -> str:
    if is_contrast_panel(fit):
        return (
            r"Panel: 2011–2021 MBB · all roster rows kept · raw PPM$=0$ if minutes$<20$ · "
            r"no roster caps — contrast / legacy estimand only."
        )
    return (
        r"Panel: 2011–2021 MBB · min$\geq20$ min player-season drop · box QC at panel build · "
        r"empirical roster caps · PPM z-scored within season."
    )


def calibrate_title(fit: dict) -> str:
    if is_contrast_panel(fit):
        return (
            r"PD21 — Calibrate homophily $\rho$ to empirical sorting index "
            r"$H_{\mathrm{sort}}$ (contrast: ppm0lt20 — not for calibration)"
        )
    return (
        r"PD21 — Calibrate homophily $\rho$ to empirical sorting index "
        r"$H_{\mathrm{sort}}$ (hero panel — locked calibration)"
    )


def calibrate_role_bullet(fit: dict) -> str:
    if is_contrast_panel(fit):
        return (
            r"PD21 contrast (Aug 2026): ppm0lt20 panel — illustrative only; "
            r"do not use for locked longitudinal $\rho$ calibration."
        )
    return r"PD21 locked calibration (Aug 2026): bracket search on hero panel for Alex ASSIGN $\rho$."


def calibrate_claim(fit: dict) -> str:
    long = fit.get("longitudinal", {})
    err_ref = float(long.get("mean_abs_err_at_reference_rho", 0.112))
    if is_contrast_panel(fit):
        rho_star = float(long.get("rho_star_longitudinal", 0.57))
        return (
            rf"Claim (PD21 contrast): ppm0lt20 inflates longitudinal $\rho^* \approx {rho_star:.3g}$ — "
            r"not the hero estimand; 2013$\rightarrow$2014 per-season jump traces ESPN box-depth break "
            r"(PD22 ESPN coverage — HAND20 slide 9)."
        )
    rho_star = float(long.get("rho_star_longitudinal", 0.0))
    h_emp = float(long.get("h_sort_empirical_mean_over_seasons", 0.064))
    return (
        rf"Claim (Alex): Hero panel — LG ASSIGN $\rho^*={rho_star:.3g}$ matches modest empirical "
        rf"$H_{{\mathrm{{sort}}}}\approx{h_emp:.3f}$; legacy $\rho=0.5$ overshoots (${err_ref:.2f}$ mean $|error|$). "
        r"Model–measurement fit on this panel — not a claim that NCAA rosters are random."
    )


def hero_do_dont_bullets(fit: dict) -> list[str]:
    """Hero calibration slide — block over-interpretation of $\rho^*=0$ (HAND20 slide 14)."""
    long = fit.get("longitudinal", {})
    h_emp = float(long.get("h_sort_empirical_mean_over_seasons", 0.064))
    h_sim = float(long.get("h_sort_sim_mean_at_star", 0.082))
    per = fit.get("per_season", [])
    n_zero = sum(1 for row in per if float(row.get("rho_star", 1.0)) == 0.0)
    return [
        r"$\rho^*=0$ — what we DO say: on the locked hero panel, the LG ASSIGN homophily knob "
        rf"calibrates to zero ({n_zero}/{len(per)} seasons); empirical $H_{{\mathrm{{sort}}}}\approx "
        rf"{h_emp:.3f}$ ({mapprox(h_emp)} on $[0,1]$ scale); sim at $\rho^*$ slightly high "
        rf"({mapprox(h_sim)}); turning $\rho$ up overshoots (see legacy $\rho=0.5$ bullet).",
        r"$\rho^*=0$ — what we DO NOT say: NCAA has no team formation; Duke and a weak D-I "
        r"school draw from the same talent pool; real-world assortativity is absent; Hero inverted-U "
        r"/ $\lambda$ / SELECT story is dead.",
        r"$H_{{\mathrm{{sort}}}}$ is realized sorting on a fixed roster partition (VECTOR lock) — "
        r"not the generative $\rho$ knob. Box QC lowered measured $H_{{\mathrm{{sort}}}}$ vs pre-QC "
        r"($\sim 0.10 \rightarrow \sim 0.06$); modest $\neq$ zero. "
        r"Contrast: ppm0lt20 panel (HAND20 slide 15).",
    ]


def contrast_do_dont_bullets() -> list[str]:
    """ppm0lt20 contrast guardrails (HAND20 slide 15)."""
    return [
        r"Contrast slide only: ppm0lt20 (all roster rows, PPM$=0$ if min$<20$, no caps) inflates "
        r"$\rho^*$ and the 2013$\rightarrow$2014 per-season jump — do not use for locked calibration.",
        r"Footer claim on this slide is about contrast failure mode — not the hero-panel "
        r"near-zero $\rho^*$ story on the hero calibration slide (HAND20 slide 14).",
    ]


def timeseries_title(fit: dict) -> str:
    if is_contrast_panel(fit):
        return (
            r"PD21 — Per-season $\rho^*$ and empirical $H_{\mathrm{sort}}$ "
            r"(contrast: ppm0lt20 — not for calibration)"
        )
    return (
        r"PD21 — Per-season $\rho^*$ and empirical $H_{\mathrm{sort}}$ "
        r"(hero panel — locked calibration)"
    )


def timeseries_claim(fit: dict) -> str:
    if is_contrast_panel(fit):
        return (
            r"Claim (PD21 contrast): 2013$\rightarrow$2014 jump in per-season $\rho^*$ on ppm0lt20 "
            r"is ESPN roster-depth artifact — hero min-20 panel gives flat $\rho^*$; "
            r"see PD22 ESPN coverage (HAND20 slide 9)."
        )
    return (
        r"Claim (Alex): Hero panel gives flat per-season $\rho^*$ ($=0$ all seasons) — "
        r"use this estimand for longitudinal $\rho$ calibration, not ppm0lt20."
    )


def _season_rho(per: list[dict], season: int) -> float | None:
    for row in per:
        if int(row["season"]) == season:
            return float(row["rho_star"])
    return None


def jump_2013_2014_bullet(fit: dict) -> str | None:
    if not is_contrast_panel(fit):
        return None
    per = fit.get("per_season", [])
    r13 = _season_rho(per, 2013)
    r14 = _season_rho(per, 2014)
    if r13 is None or r14 is None:
        return None
    return (
        rf"2013$\rightarrow$2014 per-season $\rho^*$: {marrow(r13, r14, decimals=3)} — "
        r"coincides with raw ESPN player-season count jump; not used for locked calibration."
    )


def inset_bullet(fit: dict) -> str:
    if is_contrast_panel(fit):
        return (
            r"Figure bottom-right inset: per-season $\rho^*$ — red dots jump at 2014; "
            r"dotted line = mean $\rho^*$ across seasons."
        )
    return (
        r"Figure bottom-right inset: per-season $\rho^*$ — flat at $0$ all seasons on hero panel."
    )
