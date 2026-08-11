"""Readout bullets for PD17 interval-overlap reference slides."""

from __future__ import annotations

from h_sort_readout import h_sort_definition_bullet, h_sort_note_bullet, h_sort_value_bullet


def empirical_overlap_bullets(meta: dict, *, paired_compare: bool = False) -> list[str]:
    cov_max = meta.get("coverage_max")
    cov_norm = meta.get("coverage_max_normalized")
    cov_frac = meta.get("coverage_frac_gt_1")
    dis_max = meta.get("coverage_disjoint_max")
    span = meta.get("perf_span", {})
    n_ts = meta.get("n_team_seasons")

    bullets = [
        r"Each team-season: talent window [\min \hat{A}_{i}, \max \hat{A}_{i}] on PPM z.",
        r"Coverage = how many windows cover a point on the spectrum (530 CELL 8).",
        r"Red dashed: disjoint sort-and-chop on same player-seasons (537 B analog).",
        h_sort_definition_bullet(),
    ]
    h_line = h_sort_value_bullet(meta.get("H_sort"), label="NCAA partition")
    if h_line:
        bullets.append(h_line)
    if cov_max is not None and dis_max is not None:
        line = rf"Max coverage={cov_max:,}; sort-and-chop max={dis_max}."
        if cov_norm is not None:
            line += rf" Normalized peak={cov_norm:.2f}."
        bullets.append(line)
    if cov_frac is not None:
        bullets.append(rf"{100 * cov_frac:.0f}\% of grid points have >1 team covering.")
    if span and n_ts:
        bullets.append(
            rf"Roster span: mean={span.get('mean', 0):.2f} z, "
            rf"median={span.get('median', 0):.2f} z ({n_ts:,} team-seasons)."
        )
    if paired_compare:
        bullets.append(r"Paired compare window — match season span to Grandchild sim slide.")
    else:
        bullets.append(
            r"Full panel 2011–2021 — pooled team-seasons (not 1:1 with single-season sim)."
        )
    bullets.append(h_sort_note_bullet())
    return bullets


def grandchild_overlap_bullets(meta: dict, *, paired_compare: bool = False) -> list[str]:
    assign = meta.get("assignment", {})
    ref = meta.get("ncaa_window_reference") or meta.get("empirical_hand17_reference") or {}
    cov_max = meta.get("coverage_max")
    cov_norm = meta.get("coverage_max_normalized")
    cov_frac = meta.get("coverage_frac_gt_1")
    dis_max = meta.get("coverage_disjoint_max")
    span = meta.get("perf_span", {})
    n_units = meta.get("n_team_seasons") or meta.get("n_teams")
    rho = assign.get("rho", "?")

    bullets = [
        r"Each team-season: talent window [\min \hat{A}_{i}, \max \hat{A}_{i}] on PPM z.",
        r"Coverage = how many roster windows cover a point (530 CELL 8).",
        rf"Grandchild ASSIGN: \rho={rho:g}, endogenous \mu_j — no T_{{j^*}}.",
        r"Red dashed: disjoint sort-and-chop on same player pool (537 B analog).",
        h_sort_definition_bullet(),
    ]
    h_line = h_sort_value_bullet(
        meta.get("H_sort") or assign.get("H_sort") or assign.get("sorting_index_h"),
        label="Assign partition",
    )
    if h_line:
        bullets.append(h_line)
    if cov_max is not None and dis_max is not None:
        line = rf"Sim max coverage={cov_max:,}; sort-and-chop max={dis_max}."
        if cov_norm is not None:
            line += rf" Normalized peak={cov_norm:.2f}."
        bullets.append(line)
    if cov_frac is not None:
        bullets.append(rf"{100 * cov_frac:.0f}\% of grid points have >1 team covering.")
    if span and n_units:
        bullets.append(
            rf"Roster span: mean={span.get('mean', 0):.2f} z, "
            rf"median={span.get('median', 0):.2f} z ({n_units:,} team-seasons)."
        )
    if ref and paired_compare:
        ref_cov = ref.get("coverage_max")
        ref_frac = ref.get("coverage_frac_gt_1")
        ref_h = ref.get("H_sort")
        parts = []
        if ref_cov is not None:
            parts.append(rf"NCAA ref max cov={ref_cov:,}")
        if ref_frac is not None:
            parts.append(rf"NCAA overlap grid={100 * ref_frac:.0f}\%")
        if ref_h is not None:
            parts.append(rf"NCAA H_{{sort}}={ref_h:.3f}")
        if parts:
            bullets.append("; ".join(parts) + ".")
    bullets.append(h_sort_note_bullet())
    return bullets
