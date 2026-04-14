# tenure_pipeline/viz_pipeline.py
# ---------------------------------------------------------------------------
# Summary visualizations for the PEER tenure pipeline.
# Same display + disk pattern as talent_pipeline/cox_plot_helpers.py:
#   fig.savefig(path)  →  plt.show()  →  plt.close(fig)
# Run %matplotlib inline in the notebook (540 CELL 0) before any viz import so show()
# renders in the notebook and does not block like a Qt/Tk window.
#   plot_stage3a()     — CDX discovery rollup (call after Cell 3A)
#   plot_stage3a_enrollment_bin_heatmap() — year×enrollment-bin aggregate (coverage + tier)
#   plot_stage3b()     — HTML download rollup (call after Cell 3B)
#   plot_stage4_diag() — HTML parse quality diagnostic (call after Cell 4)
#   plot_stage5()      — Longitudinal panel summary (call after Cell 5)
#
# Usage from the notebook:
#   import importlib, sys
#   _tp = str(WORKSPACE_ROOT / 'tenure_pipeline')
#   if _tp not in sys.path: sys.path.insert(0, _tp)
#   import viz_pipeline; importlib.reload(viz_pipeline)
#   viz_pipeline.plot_stage3a(plan_records, df_schools,
#                             CDX_YEAR_MIN, CDX_YEAR_MAX,
#                             WORKSPACE_ROOT / 'tenure_pipeline' / 'stage3a_summary.png',
#                             school_sort='volume')  # or 'alphabetical' for A→Z on bars/heatmap
# ---------------------------------------------------------------------------
import json
import re
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.ticker import MaxNLocator
from pathlib import Path


# ── School enrollment (total UG+grad) — annual rows in school_enrollment_annual.csv
# Fixed cutpoints; edit to match your IPEDS / NCES extract.
_DEFAULT_ENROLLMENT_CSV = Path(__file__).resolve().parent / 'school_enrollment_annual.csv'
ENROLLMENT_SMALL_MAX = 15000    # tier 1: strictly below
ENROLLMENT_MEDIUM_MAX = 35000   # tier 2: [SMALL_MAX, MEDIUM_MAX); tier 3: >= MEDIUM_MAX

TIER_COL = {
    0: '#B0BEC5',   # enrollment unknown (modal / row N/A)
    1: '#1565C0',   # small
    2: '#F57C00',   # medium
    3: '#2E7D32',   # large
}
TIER_LAB_SHORT = {
    0: 'Enrollment N/A',
    1: f'Small (<{ENROLLMENT_SMALL_MAX:,})',
    2: f'Medium [{ENROLLMENT_SMALL_MAX:,}–{ENROLLMENT_MEDIUM_MAX})',
    3: f'Large (≥{ENROLLMENT_MEDIUM_MAX:,})',
}
TIER_LIGHT = {0: '#ECEFF1', 1: '#E3F2FD', 2: '#FFF3E0', 3: '#E8F5E9'}
HM_GAP = '#ECEFF1'       # no plan row for that calendar year
HM_NEUTRAL = '#9E9E9E'   # plan row exists but no enrollment for that (school, year)


def _tier_from_total(val) -> int:
    if val is None:
        return 0
    try:
        if isinstance(val, float) and np.isnan(val):
            return 0
        t = float(val)
    except (TypeError, ValueError):
        return 0
    if t < ENROLLMENT_SMALL_MAX:
        return 1
    if t < ENROLLMENT_MEDIUM_MAX:
        return 2
    return 3


def load_enrollment_lookup(path=None) -> dict:
    """(university, year) -> total enrollment; year int; university exact string from CSV."""
    p = Path(path) if path is not None else _DEFAULT_ENROLLMENT_CSV
    if not p.exists():
        return {}
    df = pd.read_csv(p, comment='#')
    if df.empty:
        return {}
    df.columns = [str(c).strip() for c in df.columns]
    need = {'university', 'year', 'total_enrollment'}
    if not need.issubset(df.columns):
        return {}
    df = df.dropna(subset=['university', 'year'], how='any')
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df['total_enrollment'] = pd.to_numeric(df['total_enrollment'], errors='coerce')
    df = df.dropna(subset=['year', 'total_enrollment'])
    out = {}
    for _, r in df.iterrows():
        out[(str(r['university']).strip(), int(r['year']))] = float(r['total_enrollment'])
    return out


def _modal_tier_from_years(lookup: dict, university: str, years: list) -> int:
    tiers = []
    for y in years:
        tr = _tier_from_total(lookup.get((university, int(y))))
        if tr > 0:
            tiers.append(tr)
    if not tiers:
        return 0
    return Counter(tiers).most_common(1)[0][0]


_SCHOOL_SORT_CHOICES = frozenset({'volume', 'alphabetical'})


def _norm_school_sort(school_sort):
    """Validate school_sort for bar charts / heatmap rows: 'volume' or 'alphabetical'."""
    s = 'volume' if school_sort is None else str(school_sort).lower()
    if s not in _SCHOOL_SORT_CHOICES:
        raise ValueError(
            f"school_sort must be 'volume' or 'alphabetical', not {school_sort!r}"
        )
    return s


_BINNING_CHOICES = frozenset({'quantile', 'equal_width'})


def _enrollment_bin_indices(
    enroll: np.ndarray,
    n_bins: int,
    binning: str,
) -> np.ndarray:
    """
    Assign each school to a size bin for one calendar year.

    Parameters
    ----------
    enroll : (n_schools,) float
        Total enrollment that year; NaN if missing from lookup.
    n_bins : int
        Number of rows in the aggregate heatmap.
    binning : 'quantile' | 'equal_width'
        quantile — equal counts per bin (within this year’s valid enrollments).
        equal_width — equal spans on the enrollment axis; bins may be empty.

    Returns
    -------
    (n_schools,) int32
        Bin id in ``0 .. n_bins-1``, or ``-1`` if enrollment missing (or invalid).
    """
    binning = str(binning).lower().strip()
    if binning not in _BINNING_CHOICES:
        raise ValueError(f"binning must be 'quantile' or 'equal_width', not {binning!r}")
    n_bins = int(n_bins)
    if n_bins < 2:
        raise ValueError("n_bins must be >= 2")

    n = len(enroll)
    out = np.full(n, -1, dtype=np.int32)
    m = np.isfinite(enroll)
    if not m.any():
        return out

    if binning == 'quantile':
        v = enroll[m].astype(float, copy=False)
        idx_all = np.where(m)[0]
        order = np.argsort(v, kind='mergesort')
        n_valid = int(v.shape[0])
        n_groups = min(n_bins, max(1, n_valid))
        for b in range(n_groups):
            lo = b * n_valid // n_groups
            hi = (b + 1) * n_valid // n_groups if b < n_groups - 1 else n_valid
            out[idx_all[order[lo:hi]]] = b
        return out

    # equal_width
    v = enroll[m].astype(float, copy=False)
    lo, hi = float(np.min(v)), float(np.max(v))
    if hi <= lo:
        out[m] = 0
        return out
    edges = np.linspace(lo, hi, n_bins + 1)
    clamped = np.clip(enroll.astype(float, copy=False), lo, hi)
    b = np.searchsorted(edges, clamped, side='right') - 1
    b = np.clip(b, 0, n_bins - 1)
    b[~m] = -1
    return b.astype(np.int32)


def plot_stage3a_enrollment_bin_heatmap(
    plan_records,
    df_schools,
    cdx_year_min,
    cdx_year_max,
    out_path,
    plan_path=None,
    enrollment_path=None,
    *,
    n_bins: int = 20,
    binning: str = 'quantile',
):
    """
    Two-panel figure: aggregate **year × enrollment-size bin** (not per school).

    **Top:** Fraction of schools in each bin with **any** CDX plan row that calendar year
    (0–1, sequential colormap). **Bottom:** **Median** enrollment in the bin that year,
    mapped through the same fixed tier cutpoints as ``TIER_COL`` (small / medium / large).

    Rows are **bin 0 = smallest** enrollments that year, **bin n_bins−1 = largest**.
    Binning is recomputed **each year** from that year’s headcounts (cross-sectional strata).

    Parameters
    ----------
    plan_records, plan_path
        Same as ``plot_stage3a`` (plan JSONL rows; bookmark / n_snaps<=0 stripped).
    df_schools
        Must include ``university`` (panel schools).
    cdx_year_min, cdx_year_max
        Calendar year columns (same window as Stage 3A).
    out_path
        Where to save the PNG.
    enrollment_path
        ``school_enrollment_annual.csv`` path (see ``load_enrollment_lookup``).
    n_bins
        Number of horizontal strata (default 20; use 40 for finer slices if the panel is large).
    binning
        ``quantile`` — equal-count bins; ``equal_width`` — equal enrollment width (sparse bins possible).
    """
    out_path = Path(out_path)
    binning = str(binning).lower().strip()
    if binning not in _BINNING_CHOICES:
        raise ValueError(f"binning must be 'quantile' or 'equal_width', not {binning!r}")
    n_bins = int(n_bins)
    if n_bins < 2:
        raise ValueError("n_bins must be >= 2")

    _plan = list(plan_records) if plan_records else []
    if not _plan and plan_path and Path(plan_path).exists():
        with open(plan_path, encoding='utf-8') as f:
            _plan = [json.loads(l) for l in f]
    _plan = [
        r for r in _plan
        if r.get('plan_row_type') != 'cdx_bookmark' and r.get('n_snaps', 1) > 0
    ]

    plan_set = set()
    for r in _plan:
        try:
            plan_set.add((str(r['university']).strip(), int(float(r['year']))))
        except (KeyError, TypeError, ValueError):
            continue

    schools = [str(u).strip() for u in df_schools['university'].tolist()]
    lookup = load_enrollment_lookup(enrollment_path)
    years = list(range(int(cdx_year_min), int(cdx_year_max) + 1))
    n_y = len(years)

    cov = np.full((n_bins, n_y), np.nan, dtype=float)
    med_tier = np.full((n_bins, n_y), np.nan, dtype=float)

    for yi, yr in enumerate(years):
        enroll = np.array(
            [lookup.get((u, int(yr)), np.nan) for u in schools],
            dtype=float,
        )
        bins = _enrollment_bin_indices(enroll, n_bins, binning)
        for b in range(n_bins):
            idx = np.where(bins == b)[0]
            if idx.size == 0:
                continue
            e_sub = enroll[idx]
            hits = sum(1 for i in idx if (schools[i], yr) in plan_set)
            cov[b, yi] = hits / float(idx.size)
            med = float(np.median(e_sub))
            med_tier[b, yi] = float(_tier_from_total(med))

    # ── Figure: coverage (sequential) + median tier (discrete) ─────────────────
    fig, (ax_cov, ax_tr) = plt.subplots(
        2,
        1,
        figsize=(20, 12),
        facecolor='#F7F9FC',
        sharex=True,
        gridspec_kw={'height_ratios': [1.05, 1.0], 'hspace': 0.22},
    )
    _bin_lab = 'quantile (equal count)' if binning == 'quantile' else 'equal enrollment width'
    fig.suptitle(
        f'Stage 3A — Enrollment bin × Year (aggregate)  │  {_bin_lab}, n_bins={n_bins}  │  '
        f'{cdx_year_min}–{cdx_year_max}',
        fontsize=12,
        fontweight='bold',
        y=0.98,
        color='#1A237E',
    )

    cmap_cov = plt.cm.Blues.copy()
    cmap_cov.set_bad(color='#ECEFF1')
    mcov = np.ma.masked_invalid(cov)
    im1 = ax_cov.imshow(
        mcov,
        aspect='auto',
        interpolation='nearest',
        origin='upper',
        cmap=cmap_cov,
        vmin=0.0,
        vmax=1.0,
        extent=[-0.5, n_y - 0.5, n_bins - 0.5, -0.5],
    )
    cb = fig.colorbar(im1, ax=ax_cov, fraction=0.02, pad=0.02)
    cb.set_label('Share of schools in bin with ≥1 plan row', fontsize=9)
    ax_cov.set_ylabel('Size bin (0 = smallest) →', fontsize=9, color='#37474F')
    ax_cov.set_title(
        'Coverage depth by enrollment stratum',
        fontsize=11,
        fontweight='bold',
        pad=8,
    )
    ax_cov.set_yticks(np.arange(0, n_bins, max(1, n_bins // 8)))

    cmap_tier = ListedColormap([TIER_COL[1], TIER_COL[2], TIER_COL[3]])
    norm_tier = BoundaryNorm([0.5, 1.5, 2.5, 3.5], cmap_tier.N)
    cmap_tier.set_bad('#ECEFF1')
    mtr = np.ma.masked_invalid(med_tier)
    im2 = ax_tr.imshow(
        mtr,
        aspect='auto',
        interpolation='nearest',
        origin='upper',
        cmap=cmap_tier,
        norm=norm_tier,
        extent=[-0.5, n_y - 0.5, n_bins - 0.5, -0.5],
    )
    ax_tr.set_ylabel('Size bin (0 = smallest) →', fontsize=9, color='#37474F')
    ax_tr.set_xticks(np.arange(n_y) + 0.0)
    ax_tr.set_xticklabels(years, fontsize=8, rotation=40, ha='right')
    ax_tr.set_xlabel('Calendar year', fontsize=9)
    ax_tr.set_title(
        'Median enrollment in bin → fixed tier cutpoints '
        f'(<{ENROLLMENT_SMALL_MAX:,} / {ENROLLMENT_SMALL_MAX:,}–{ENROLLMENT_MEDIUM_MAX:,} / '
        f'≥{ENROLLMENT_MEDIUM_MAX:,})',
        fontsize=10,
        fontweight='bold',
        pad=8,
    )
    ax_tr.set_yticks(np.arange(0, n_bins, max(1, n_bins // 8)))
    leg_t = [
        mpatches.Patch(facecolor=TIER_COL[1], label=TIER_LAB_SHORT[1]),
        mpatches.Patch(facecolor=TIER_COL[2], label=TIER_LAB_SHORT[2]),
        mpatches.Patch(facecolor=TIER_COL[3], label=TIER_LAB_SHORT[3]),
        mpatches.Patch(facecolor='#ECEFF1', edgecolor='#B0BEC5', label='No schools in bin'),
    ]
    ax_tr.legend(handles=leg_t, loc='lower right', fontsize=8, ncol=2, framealpha=0.92)
    plt.setp(ax_cov.get_xticklabels(), visible=False)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='#F7F9FC')
    plt.show()
    plt.close(fig)
    print(f"  Saved → {out_path}")


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 3A: CDX Discovery rollup
# ─────────────────────────────────────────────────────────────────────────────

def plot_stage3a(plan_records, df_schools, cdx_year_min, cdx_year_max,
                 out_path, plan_path=None, school_sort='volume',
                 enrollment_path=None):
    """
    Three-panel CDX discovery summary figure.

    **Metrics:** The plan can have **many rows per school** when ``CDX_SNAPS_PER_SEASON`` > 1
    (multiple Wayback timestamps per spring/fall band). The **lollipop** uses **row counts**
    (autoscale). The **donut** tiers use **distinct (year, season) bands** per school
    (comparable to the old “one row per band” scale, max ~50 for 2000–2024 × 2 seasons).

    School coloring (lollipop + heatmap) uses **total UG+grad enrollment** tiers from
    ``school_enrollment_annual.csv`` (annual rows; modal tier across ``cdx_year_min``–``cdx_year_max``
    for the lollipop; heatmap cells use that year's tier, neutral if enrollment missing).

    Parameters
    ----------
    plan_records  : list of dicts  (in-memory records from Cell 3A, may be empty)
    df_schools    : pd.DataFrame   (loaded from STAGE2_OUT)
    cdx_year_min  : int            (CDX_YEAR_MIN constant)
    cdx_year_max  : int            (CDX_YEAR_MAX constant)
    out_path      : Path | str     (where to save the PNG)
    plan_path     : Path | None    (STAGE3_PLAN jsonl — fallback if plan_records empty)
    school_sort   : str            'volume' (default): by planned row count / heatmap
                                   logic; 'alphabetical': A→Z top→bottom on lollipop + heatmap.
    enrollment_path : Path | None  CSV ``university,year,total_enrollment`` (see module constants).
    """
    out_path = Path(out_path)
    ss = _norm_school_sort(school_sort)

    # Load data — prefer in-memory, fall back to disk
    _plan = list(plan_records) if plan_records else []
    if not _plan and plan_path and Path(plan_path).exists():
        with open(plan_path, encoding='utf-8') as f:
            _plan = [json.loads(l) for l in f]
    # Strip sentinel records (n_snaps <= 0) and CDX bookmark rows
    _plan = [
        r for r in _plan
        if r.get('plan_row_type') != 'cdx_bookmark' and r.get('n_snaps', 1) > 0
    ]

    _sch = df_schools.copy()

    # ── Wrangle ───────────────────────────────────────────────────────────────
    df_p = pd.DataFrame(_plan) if _plan else pd.DataFrame(
        columns=['university', 'year', 'season'])
    per = (df_p.groupby('university')
               .agg(n_planned=('year', 'count'),
                    yr_min=('year', 'min'),
                    yr_max=('year', 'max'))
               .reset_index())
    if not df_p.empty:
        n_bands_s = (
            df_p.drop_duplicates(subset=['university', 'year', 'season'])
            .groupby('university')
            .size()
            .reset_index(name='n_bands')
        )
        per = per.merge(n_bands_s, on='university', how='left')
    else:
        per['n_bands'] = 0
    per['n_bands'] = per['n_bands'].fillna(0).astype(int)

    missing = set(_sch['university']) - set(per['university'])
    if missing:
        per = pd.concat([per, pd.DataFrame({
            'university': list(missing),
            'n_planned':  0,
            'yr_min':     np.nan,
            'yr_max':     np.nan,
            'n_bands':    0,
        })], ignore_index=True)
    per['yr_span'] = (per['yr_max'] - per['yr_min'] + 1).fillna(0)
    lookup = load_enrollment_lookup(enrollment_path)
    years_win = list(range(int(cdx_year_min), int(cdx_year_max) + 1))
    per['tier'] = per['university'].apply(
        lambda u: _modal_tier_from_years(lookup, u, years_win))
    if ss == 'volume':
        per = per.sort_values(['n_planned', 'tier'],
                              ascending=[True, False]).reset_index(drop=True)
    else:
        per = per.sort_values('university', ascending=True).reset_index(drop=True)
    TIER  = [(0, 0,   'Zero\n(0)',      '#C62828'),
             (1, 9,   'Sparse\n(1–9)',  '#FF5722'),
             (10, 24, 'Partial\n(10–24)', '#FFA000'),
             (25, 39, 'Good\n(25–39)', '#66BB6A'),
             (40, 50, 'Strong\n(40–50)', '#1565C0')]

    n_cov = int((per['n_planned'] > 0).sum())
    n_tot = len(per)
    _sort_note = '' if ss == 'volume' else '  │  school order: A→Z'
    _mean_bands = float(per['n_bands'].mean()) if n_tot else 0.0
    _sum_bands = int(per['n_bands'].sum())

    # ── Figure layout ─────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(22, 18), facecolor='#F7F9FC')
    gs  = gridspec.GridSpec(2, 2, figure=fig,
                            height_ratios=[3, 1.2],
                            width_ratios=[2.2, 1],
                            hspace=0.36, wspace=0.22)
    fig.suptitle(
        f'Stage 3A — CDX Discovery  │  {n_cov}/{n_tot} schools with coverage  │  '
        f'{len(df_p):,} plan rows  │  {_sum_bands:,} distinct (year×season) bands total  │  '
        f'mean {_mean_bands:.1f} bands/school  │  {cdx_year_min}–{cdx_year_max}'
        f'{_sort_note}',
        fontsize=12, fontweight='bold', y=0.997, color='#1A237E')

    # ── Panel A: Lollipop ─────────────────────────────────────────────────────
    ax_l = fig.add_subplot(gs[0, 0])
    n    = len(per)
    yp   = np.arange(n)

    def _lolli_color(n_planned, tier):
        if n_planned == 0:
            return '#C62828'
        return TIER_COL[tier] if tier > 0 else TIER_COL[0]

    col  = [_lolli_color(v, t)
            for v, t in zip(per['n_planned'], per['tier'])]
    for yi, xi, ci, ti in zip(yp, per['n_planned'], col, per['tier']):
        bg = '#FFEBEE' if xi == 0 else TIER_LIGHT.get(ti, TIER_LIGHT[0])
        ax_l.axhspan(yi - 0.47, yi + 0.47,
                     color=bg,
                     alpha=0.5, zorder=0)
        ax_l.plot([0, xi], [yi, yi], color=ci, alpha=0.48,
                  lw=1.4, solid_capstyle='round', zorder=2)
    _yr = per['yr_span'].to_numpy(dtype=float, copy=False)
    dot_s = np.where(_yr > 0, 22 + _yr * 8, 16.0).astype(float)
    _xp = per['n_planned'].to_numpy(dtype=float, copy=False)
    ax_l.scatter(_xp, yp, c=col, s=dot_s, zorder=5,
                 edgecolors='white', linewidths=0.6, alpha=0.92)
    _xmax = float(per['n_planned'].max()) if n else 0.0
    _xmax = max(_xmax * 1.08, 8.0)
    ax_l.set_xlim(-0.5, _xmax)
    ax_l.xaxis.set_major_locator(MaxNLocator(nbins=9, min_n_ticks=5))
    _pos_np = per.loc[per['n_planned'] > 0, 'n_planned']
    if len(_pos_np) > 0:
        _med = float(_pos_np.median())
        ax_l.axvline(_med, color='#78909C', ls=':', lw=1.1, alpha=0.75, zorder=3)
        _y_ref = (n - 0.8) if ss == 'volume' else 0.8
        ax_l.text(
            _med + _xmax * 0.01, _y_ref,
            f'median rows\n{_med:,.0f}',
            fontsize=7.5, color='#546E7A', va='top',
        )
    ax_l.set_yticks(yp)
    ax_l.set_yticklabels(per['university'], fontsize=5.2)
    ax_l.set_xlabel(
        'Planned snapshot rows per school (each row = one Wayback capture; multi-capture per band)',
        fontsize=9,
    )
    ax_l.set_title(
        'Plan rows per school\n'
        'dot size ∝ calendar span (yr_max−yr_min)   │   red = zero plan rows   │   color = enrollment tier',
        fontsize=10, fontweight='bold', pad=8,
    )
    ax_l.spines[['top', 'right']].set_visible(False)
    ax_l.tick_params(axis='y', length=0, pad=3)
    ax_l.grid(axis='x', alpha=0.18, lw=0.8)
    if ss == 'alphabetical':
        ax_l.invert_yaxis()
    leg_h  = [mpatches.Patch(facecolor=TIER_COL[w], label=TIER_LAB_SHORT[w])
              for w in [1, 2, 3]]
    leg_h += [mpatches.Patch(facecolor=TIER_COL[0], label=TIER_LAB_SHORT[0])]
    leg_h += [mpatches.Patch(facecolor='#C62828', label='Zero coverage')]
    ax_l.legend(handles=leg_h, fontsize=8.5, loc='lower right',
                framealpha=0.88, edgecolor='#CFD8DC')

    # ── Panel B: Coverage tier donut (by distinct year×season bands, not raw rows) ─
    ax_d = fig.add_subplot(gs[0, 1])
    _nb_tier = per['n_bands'].clip(upper=50)  # align with 0–50 band scale (multi-URL edge cases)
    tc = [int(((_nb_tier >= lo) & (_nb_tier <= hi)).sum())
          for lo, hi, *_ in TIER]
    ax_d.pie(
        tc,
        labels=[f'{lab}\n({c})' for (_, _, lab, _), c in zip(TIER, tc)],
        colors=[c for *_, c in TIER],
        startangle=90,
        wedgeprops=dict(width=0.54, edgecolor='white', linewidth=2.5),
        textprops=dict(fontsize=9.5),
    )
    ax_d.text(0, 0, f'{n_cov}\ncovered', ha='center', va='center',
              fontsize=15, fontweight='bold', color='#1A237E')
    ax_d.set_title(
        'Coverage tier by distinct\n(year × season) bands / school\n'
        '(max ~50 for 2000–2024 × spring+fall)',
        fontsize=11, fontweight='bold', pad=10,
    )

    # ── Panel C: Year × School heatmap ────────────────────────────────────────
    ax_h  = fig.add_subplot(gs[1, :])
    years = list(range(cdx_year_min, cdx_year_max + 1))
    if ss == 'volume':
        cov_s = per[per['n_planned'] > 0].sort_values(
            ['tier', 'n_planned'], ascending=[True, False])
        zero_s = per[per['n_planned'] == 0].sort_values(
            ['tier', 'university'], ascending=[True, True])
    else:
        cov_s = per[per['n_planned'] > 0].sort_values(
            'university', ascending=True)
        zero_s = per[per['n_planned'] == 0].sort_values(
            'university', ascending=True)
    sch_ord = pd.concat([cov_s, zero_s])['university'].tolist()
    plan_set = set()
    for r in _plan:
        try:
            plan_set.add((r['university'], int(float(r['year']))))
        except (KeyError, TypeError, ValueError):
            continue
    mat = np.zeros((len(sch_ord), len(years)), dtype=float)
    for si, s in enumerate(sch_ord):
        for yi, yr in enumerate(years):
            if (s, yr) not in plan_set:
                mat[si, yi] = 0.0
            else:
                tot = lookup.get((s, yr))
                if tot is None:
                    mat[si, yi] = 4.0
                else:
                    mat[si, yi] = float(_tier_from_total(tot))
    # Gap vs tier fills: light grey for no plan row; neutral for plan but no enrollment.
    hm_cmap = ListedColormap(
        [HM_GAP, TIER_COL[1], TIER_COL[2], TIER_COL[3], HM_NEUTRAL])
    hm_norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5, 4.5], hm_cmap.N)
    # No grid lines — on ~100+ rows, faint edges can wash out or moiré at 150 dpi.
    ax_h.pcolormesh(mat, cmap=hm_cmap, norm=hm_norm,
                    shading='flat', edgecolors='none', linewidths=0, rasterized=True)
    ax_h.set_xlim(0, len(years))
    ax_h.set_ylim(0, len(sch_ord))
    ax_h.set_xticks(np.arange(len(years)) + 0.5)
    ax_h.set_xticklabels(years, fontsize=8, rotation=40, ha='right')
    ax_h.set_yticks([])
    ax_h.set_ylabel('← zeros    all schools    covered →', fontsize=8, color='#546E7A')
    ax_h.set_title(
        f'Year × School Availability Map  ({cdx_year_min}–{cdx_year_max})'
        '   │   each row = one school   │   filled = any plan row that year   │   color = enrollment tier',
        fontsize=10, fontweight='bold')
    n_cov_s = len(cov_s)
    ax_h.axhline(n_cov_s, color='#E53935', lw=1.5, ls='--', alpha=0.65)
    ax_h.text(0.4, n_cov_s + 0.15,
              ' ── zero-coverage schools below', fontsize=7.5, color='#E53935')
    hm_leg = [mpatches.Patch(facecolor=TIER_COL[1], label=TIER_LAB_SHORT[1]),
              mpatches.Patch(facecolor=TIER_COL[2], label=TIER_LAB_SHORT[2]),
              mpatches.Patch(facecolor=TIER_COL[3], label=TIER_LAB_SHORT[3]),
              mpatches.Patch(facecolor=HM_NEUTRAL, label='Plan row, enrollment N/A'),
              mpatches.Patch(facecolor=HM_GAP, edgecolor='#78909C', label='No plan row/year')]
    ax_h.legend(handles=hm_leg, loc='lower right', fontsize=8.5,
                ncol=3, framealpha=0.88)
    if ss == 'alphabetical':
        ax_h.invert_yaxis()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='#F7F9FC')
    plt.show()
    plt.close(fig)
    print(f"  Saved → {out_path}")


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 3B: HTML Download rollup
# ─────────────────────────────────────────────────────────────────────────────

def plot_stage3b(index_records, df_schools, out_path, index_path=None,
                 school_sort='volume', enrollment_path=None,
                 cdx_year_min=None, cdx_year_max=None):
    """
    Four-panel HTML download summary figure.

    Per-school OK bars and tier panels use **modal enrollment tier** across
    ``cdx_year_min``–``cdx_year_max`` (same window as Stage 3A), from ``school_enrollment_annual.csv``.

    Parameters
    ----------
    index_records : list of dicts  (in-memory from Cell 3B, may be empty)
    df_schools    : pd.DataFrame   (loaded from STAGE2_OUT)
    out_path      : Path | str     (where to save the PNG)
    index_path    : Path | None    (STAGE3_INDEX jsonl — fallback if index_records empty)
    school_sort   : str            'volume' (default): by total file downloads per school;
                                   'alphabetical': A→Z top→bottom on the per-school bar chart.
    enrollment_path : Path | None  CSV ``university,year,total_enrollment``.
    cdx_year_min, cdx_year_max : int | None  defaults 2000–2024 if missing.
    """
    out_path = Path(out_path)
    ss = _norm_school_sort(school_sort)

    # Load data — prefer in-memory, fall back to disk
    _idx = list(index_records) if index_records else []
    if not _idx and index_path and Path(index_path).exists():
        with open(index_path, encoding='utf-8') as f:
            _idx = [json.loads(l) for l in f]

    if not _idx:
        print("  No download index found — run Cell 3B first.")
        return

    _sch = df_schools.copy()
    _valid_unis = set(_sch['university'])

    # Drop ghost records from schools no longer in df_schools
    _before = len(_idx)
    _idx = [r for r in _idx if r.get('university') in _valid_unis]
    _dropped = _before - len(_idx)
    if _dropped:
        print(f"  plot_stage3b: dropped {_dropped} ghost record(s) from retired schools.")

    # ── Wrangle ───────────────────────────────────────────────────────────────
    df_i = pd.DataFrame(_idx)
    df_i['ok'] = df_i['http_status'] == 200
    df_i['kb'] = df_i['file_size_bytes'] / 1024
    lookup = load_enrollment_lookup(enrollment_path)
    _ymin = int(cdx_year_min) if cdx_year_min is not None else 2000
    _ymax = int(cdx_year_max) if cdx_year_max is not None else 2024
    years_win = list(range(_ymin, _ymax + 1))
    df_i['tier'] = df_i['university'].apply(
        lambda u: _modal_tier_from_years(lookup, u, years_win))

    def _ecat(row):
        if row['ok']:
            return 'OK (200)'
        s = row.get('http_status', -1)
        e = str(row.get('error', ''))
        if s == 404:                                  return 'HTTP 404'
        if s == 503:                                  return 'HTTP 503'
        if s not in (-1, 200) and s > 0:             return f'HTTP {s}'
        if 'timed out' in e or 'timeout' in e.lower(): return 'Timeout'
        if 'nameresolution' in e.lower() or 'gaierror' in e.lower(): return 'DNS Error'
        if 'too small' in e.lower():                  return 'Too Small'
        if e:                                         return 'Conn Error'
        return 'Other'

    df_i['err_cat'] = df_i.apply(_ecat, axis=1)

    per_b = (df_i.groupby('university')
             .agg(n_ok=('ok', 'sum'),
                  n_total=('ok', 'count'),
                  mean_kb=('kb', 'mean'),
                  tier=('tier', 'first'))
             .reset_index())
    per_b['n_err']   = per_b['n_total'] - per_b['n_ok']
    per_b['ok_rate'] = per_b['n_ok'] / per_b['n_total']
    if ss == 'volume':
        per_b = per_b.sort_values('n_total', ascending=True).reset_index(drop=True)
    else:
        per_b = per_b.sort_values('university', ascending=True).reset_index(drop=True)

    SCOL = {'OK (200)':    '#2E7D32',
            'HTTP 404':    '#F9A825',
            'HTTP 503':    '#E65100',
            'Timeout':     '#6A1B9A',
            'DNS Error':   '#B71C1C',
            'Conn Error':  '#880E4F',
            'Too Small':   '#006064',
            'Other':       '#546E7A'}

    n_ok_tot  = int(df_i['ok'].sum())
    n_tot_dl  = len(df_i)
    n_sch     = df_i['university'].nunique()
    ok_kb_all = df_i.loc[df_i['ok'] & (df_i['kb'] > 0.5), 'kb']
    mean_kb_ok = ok_kb_all.mean() if len(ok_kb_all) else 0
    _sort_note = '' if ss == 'volume' else '  │  bar chart: A→Z'

    # ── Figure ────────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(22, 18), facecolor='#F7F9FC')
    gs  = gridspec.GridSpec(2, 2, figure=fig,
                            height_ratios=[2.5, 1.2],
                            width_ratios=[2.2, 1],
                            hspace=0.34, wspace=0.25)
    fig.suptitle(
        f'Stage 3B — HTML Download  │  {n_ok_tot:,}/{n_tot_dl:,} files OK'
        f'  ({100 * n_ok_tot / n_tot_dl:.1f}%)  │  {n_sch} schools'
        f'  │  avg {mean_kb_ok:.0f} KB per OK file'
        f'{_sort_note}',
        fontsize=13, fontweight='bold', y=0.997, color='#1A237E')

    # ── Panel A: Per-school stacked bar ───────────────────────────────────────
    ax_b = fig.add_subplot(gs[0, 0])
    yp   = np.arange(len(per_b))
    bar_c = [TIER_COL[t] if t > 0 else TIER_COL[0] for t in per_b['tier']]
    ax_b.barh(yp, per_b['n_ok'],  height=0.72, color=bar_c, alpha=0.85, zorder=3)
    ax_b.barh(yp, per_b['n_err'], left=per_b['n_ok'], height=0.72,
              color='#EF5350', alpha=0.70, hatch='//', zorder=3)
    for yi, (_, row) in enumerate(per_b.iterrows()):
        ax_b.text(row['n_total'] + 0.2, yi,
                  f"{row['ok_rate'] * 100:.0f}%",
                  va='center', fontsize=5.2, color='#37474F')
    ax_b.axvline(50, color='#90A4AE', ls='--', lw=0.9, alpha=0.5)
    _y50 = (len(per_b) - 0.8) if ss == 'volume' else 0.8
    ax_b.text(50.4, _y50, '50 max', fontsize=7, color='#78909C', va='top')
    ax_b.set_yticks(yp)
    ax_b.set_yticklabels(per_b['university'], fontsize=5.2)
    ax_b.set_xlabel('Number of File Downloads', fontsize=9)
    ax_b.set_title('Download Results per School  (% = success rate)\n'
                   '■ OK (colored by enrollment tier)   ▨ Error / Failed',
                   fontsize=10, fontweight='bold', pad=8)
    ax_b.spines[['top', 'right']].set_visible(False)
    ax_b.tick_params(axis='y', length=0, pad=3)
    ax_b.grid(axis='x', alpha=0.18, lw=0.8)
    leg_b  = [mpatches.Patch(facecolor=TIER_COL[w], label=TIER_LAB_SHORT[w])
              for w in [1, 2, 3]]
    leg_b += [mpatches.Patch(facecolor=TIER_COL[0], label=TIER_LAB_SHORT[0])]
    leg_b += [mpatches.Patch(facecolor='#EF5350', hatch='//', label='Error')]
    ax_b.legend(handles=leg_b, fontsize=8.5, loc='lower right', framealpha=0.88)
    if ss == 'alphabetical':
        ax_b.invert_yaxis()

    # ── Panel B: Status donut ─────────────────────────────────────────────────
    ax_d = fig.add_subplot(gs[0, 1])
    ev   = df_i['err_cat'].value_counts()
    ax_d.pie(
        ev.values,
        labels=[f'{k}\n({v:,})' for k, v in ev.items()],
        colors=[SCOL.get(k, '#9E9E9E') for k in ev.index],
        startangle=90,
        wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2.5),
        textprops=dict(fontsize=9),
    )
    ax_d.text(0, 0, f'{n_ok_tot:,}\nOK', ha='center', va='center',
              fontsize=15, fontweight='bold', color='#2E7D32')
    ax_d.set_title('Download Status\nBreakdown', fontsize=11, fontweight='bold', pad=10)

    # ── Panel C: File size violin + strip ─────────────────────────────────────
    ax_v = fig.add_subplot(gs[1, 0])
    ok_df = df_i[(df_i['ok']) & (df_i['kb'] > 0.5)].copy()
    ok_df['log_kb'] = np.log10(ok_df['kb'])
    tiers_order = [t for t in [1, 2, 3] if (ok_df['tier'] == t).any()]
    if tiers_order:
        wdat = [ok_df[ok_df['tier'] == t]['log_kb'].values for t in tiers_order]
        pos = np.arange(1, len(tiers_order) + 1, dtype=float)
        parts = ax_v.violinplot(
            wdat, positions=pos.tolist(),
            showmedians=True, showextrema=True, widths=0.72)
        for pc, t in zip(parts['bodies'], tiers_order):
            pc.set_facecolor(TIER_COL[t])
            pc.set_alpha(0.62)
        parts['cmedians'].set_color('#212121')
        parts['cmedians'].set_linewidth(2.5)
        for el in ['cbars', 'cmaxes', 'cmins']:
            parts[el].set_color('#90A4AE')
        rng = np.random.default_rng(42)
        for i, t in enumerate(tiers_order):
            dat = wdat[i]
            if not len(dat):
                continue
            jit = rng.uniform(-0.1, 0.1, len(dat))
            ax_v.scatter(np.full(len(dat), pos[i]) + jit, dat,
                         color=TIER_COL[t], alpha=0.18, s=4, zorder=4)
            med = np.median(dat)
            ax_v.text(pos[i] + 0.38, med, f'{10**med:.0f} KB',
                      fontsize=8.5, va='center', color='#212121', fontweight='bold')
        ax_v.set_xticks(pos)
        ax_v.set_xticklabels([TIER_LAB_SHORT[t] for t in tiers_order], fontsize=9)
    else:
        ax_v.text(
            0.5, 0.5, 'No OK files with size > 0.5 KB\nin tiers 1–3',
            transform=ax_v.transAxes, ha='center', va='center',
            fontsize=11, color='#78909C')
    ax_v.set_yticks([0, 1, 2, 3])
    ax_v.set_yticklabels(['1 KB', '10 KB', '100 KB', '1 MB'], fontsize=8)
    ax_v.set_ylabel('File size (log scale)', fontsize=9)
    ax_v.set_title('File Size Distribution by Enrollment Tier\n'
                   'violin + jittered strip  │  median labeled  │  successful downloads only',
                   fontsize=10, fontweight='bold')
    ax_v.spines[['top', 'right']].set_visible(False)
    ax_v.grid(axis='y', alpha=0.2, lw=0.8)

    # ── Panel D: Cumulative file size CDFs by tier ────────────────────────────
    ax_c = fig.add_subplot(gs[1, 1])
    for t in tiers_order:
        dat = np.sort(ok_df[ok_df['tier'] == t]['log_kb'].values)
        if not len(dat):
            continue
        cdf = np.arange(1, len(dat) + 1) / len(dat)
        ax_c.plot(dat, cdf, color=TIER_COL[t], lw=2.4,
                  label=TIER_LAB_SHORT[t], alpha=0.88)
        ax_c.fill_between(dat, cdf, alpha=0.10, color=TIER_COL[t])
    all_dat = np.sort(ok_df['log_kb'].values)
    if len(all_dat):
        ax_c.plot(all_dat, np.arange(1, len(all_dat) + 1) / len(all_dat),
                  color='#212121', lw=1.5, ls='--', alpha=0.55, label='All files')
    for q, lbl in [(0.25, 'Q1'), (0.50, 'Q2'), (0.75, 'Q3')]:
        ax_c.axhline(q, color='#B0BEC5', lw=0.8, ls=':')
        ax_c.text(ax_c.get_xlim()[0] + 0.02, q + 0.015, lbl, fontsize=7, color='#78909C')
    ax_c.set_xticks([0, 1, 2, 3])
    ax_c.set_xticklabels(['1 KB', '10 KB', '100 KB', '1 MB'], fontsize=8)
    ax_c.set_ylabel('Cumulative fraction of files', fontsize=9)
    ax_c.set_xlabel('File size (log scale)', fontsize=9)
    ax_c.set_title('Cumulative File Size Distribution\n'
                   '(CDF by tier — rightward shift = larger pages)',
                   fontsize=10, fontweight='bold')
    ax_c.legend(fontsize=8.5, framealpha=0.88, loc='upper left')
    ax_c.spines[['top', 'right']].set_visible(False)
    ax_c.grid(alpha=0.18, lw=0.8)
    ax_c.set_ylim(0, 1.03)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='#F7F9FC')
    plt.show()
    plt.close(fig)
    print(f"  Saved → {out_path}")


# ---------------------------------------------------------------------------
# plot_stage4_diag — HTML parse quality diagnostic
# ---------------------------------------------------------------------------
def plot_stage4_diag(parsed_records, df_schools, out_path, parsed_path=None,
                     rank_dist_logx=False, school_sort='volume'):
    """
    Four-panel parse quality figure.

    Panel 1 (left, tall)  — Per-school bar chart: **mean faculty count per calendar
                            snapshot** (one value per ``(year, season)``). Multiple HTML
                            files for the same semester (e.g. main faculty + affiliates
                            URLs) are **merged** into that single snapshot count. Cell 4's
                            console ``avg …/file`` divides by **file** count — the two
                            match when there is exactly one file per semester; otherwise
                            they differ. Schools in ``df_schools`` with **no** rows in the
                            parse file appear as grey bars at 0.
    Panel 2 (top-right)   — Year-over-year line chart for the top-10 schools by
                            record count (shows temporal consistency).
    Panel 3 (mid-right)   — Rank distribution across all records.
    Panel 4 (bot-right)   — Distribution of per-snapshot faculty counts (histogram).

    rank_dist_logx : bool
        If True, use a logarithmic x-axis on the rank-distribution panel (helps when
        one rank dominates the counts).
    school_sort : str
        'volume' (default): schools by avg faculty per snapshot (high → top); 'alphabetical':
        A→Z top→bottom on the parse-quality bar chart (easier lookup).
    """
    out_path = Path(out_path)
    ss = _norm_school_sort(school_sort)

    # Prefer on-disk parsed file when given — avoids stale in-memory ``parsed_records``
    # after Cell 4 appends new rows in the same notebook session.
    _recs = []
    if parsed_path and Path(parsed_path).exists():
        with open(parsed_path, encoding='utf-8') as f:
            _recs = [json.loads(l) for l in f if l.strip()]
    elif parsed_records:
        _recs = list(parsed_records)
    if not _recs:
        print("  No parsed records found — run Cell 4 first.")
        return

    df = pd.DataFrame(_recs)
    df['year'] = df['year'].astype(int)

    # ── Per-school summary ────────────────────────────────────────────────────
    snap_counts  = df.groupby(['uni_slug', 'year', 'season']).size().reset_index(name='n')
    # Descending + invert_yaxis: best school (y=0) at top of bar chart (volume mode).
    school_avg   = snap_counts.groupby('uni_slug')['n'].mean().dropna()
    if ss == 'volume':
        school_avg = school_avg.sort_values(ascending=False)
    else:
        school_avg = school_avg.sort_index(ascending=True)
    school_total = df.groupby('uni_slug').size().sort_values()

    def _tier(avg):
        if avg >= 20: return '#2ECC71'   # green  — good
        if avg >= 8:  return '#F39C12'   # amber  — marginal
        return '#E74C3C'                  # red    — poor

    def _uni_to_slug(u):
        return re.sub(r'[^a-z0-9]+', '_', str(u).lower()).strip('_')

    roster_missing = []
    if df_schools is not None and len(df_schools) and 'university' in df_schools.columns:
        roster_slugs = {_uni_to_slug(u) for u in df_schools['university']}
        roster_missing = sorted(roster_slugs - set(df['uni_slug'].unique()))

    miss_set = set(roster_missing)
    if roster_missing:
        miss_series = pd.Series(0.0, index=roster_missing)
        school_avg_plot = pd.concat([school_avg, miss_series])
        if ss == 'alphabetical':
            school_avg_plot = school_avg_plot.sort_index(ascending=True)
    else:
        school_avg_plot = school_avg

    colours = [
        '#BDC3C7' if slug in miss_set else _tier(v)
        for slug, v in school_avg_plot.items()
    ]

    # ── Figure layout ─────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(20, max(10, len(school_avg_plot) * 0.28 + 4)), facecolor='#F7F9FC')
    gs  = gridspec.GridSpec(3, 2, figure=fig,
                            left=0.28, right=0.97, top=0.96, bottom=0.05,
                            hspace=0.55, wspace=0.35,
                            height_ratios=[1.4, 1, 1])
    ax_bar = fig.add_subplot(gs[:, 0])   # full left column
    ax_ts  = fig.add_subplot(gs[0, 1])   # top-right
    ax_rk  = fig.add_subplot(gs[1, 1])   # mid-right
    ax_hi  = fig.add_subplot(gs[2, 1])   # bot-right

    # --- Panel 1: per-school avg faculty/snapshot bar chart ------------------
    ax_bar.barh(range(len(school_avg_plot)), school_avg_plot.values,
                color=colours, edgecolor='white', linewidth=0.4)
    ax_bar.set_yticks(range(len(school_avg_plot)))
    ax_bar.set_yticklabels(
        [s.replace('_', ' ').title() for s in school_avg_plot.index],
        fontsize=7.5
    )
    ax_bar.set_xlabel(
        'Mean faculty per (year, season) snapshot — same semester from multiple URLs combined',
        fontsize=8,
    )
    _p1_sub = f'  │  grey = 0 parsed records ({len(roster_missing)} roster)' if roster_missing else ''
    ax_bar.set_title(
        'Parse Quality by School\n(mean per calendar snapshot, not per HTML file — see docstring)'
        + _p1_sub,
        fontsize=10,
        fontweight='bold',
    )
    ax_bar.axvline(20, color='#2ECC71', lw=1.2, ls='--', alpha=0.7, label='>=20 = good')
    ax_bar.axvline(8,  color='#F39C12', lw=1.2, ls='--', alpha=0.7, label='>=8  = marginal')
    ax_bar.legend(fontsize=8, loc='lower right')
    for i, (slug, val) in enumerate(school_avg_plot.items()):
        if slug in miss_set:
            ax_bar.text(0.15, i, '0', va='center', fontsize=6.5, color='#5D6D7E')
        else:
            ax_bar.text(val + 0.5, i, f'{val:.0f}', va='center', fontsize=6.5)
    ax_bar.spines[['top', 'right']].set_visible(False)
    ax_bar.grid(axis='x', alpha=0.18, lw=0.8)
    # Default axes.margins(y=0.05) adds ~5% of the y-range on each end — on 0..n-1
    # that is several "phantom" category rows above Purdue; axvline then spans that gap.
    ax_bar.margins(y=0)
    n_school = len(school_avg_plot)
    # set_ylim must come *before* invert_yaxis — calling set_ylim after invert can
    # reset inversion so category 0 (A or best school) ends up at the bottom again.
    ax_bar.set_ylim(-0.5, n_school - 0.5)
    ax_bar.invert_yaxis()

    # --- Panel 2: year-over-year for top-10 schools --------------------------
    top10   = school_total.nlargest(10).index
    palette = plt.cm.tab10.colors
    for i, slug in enumerate(top10):
        sub = (snap_counts[snap_counts['uni_slug'] == slug]
               .groupby('year')['n'].mean().reset_index())
        ax_ts.plot(sub['year'], sub['n'], marker='o', markersize=3,
                   label=slug.replace('_university', '').replace('_', ' ').title(),
                   color=palette[i % 10], lw=1.4)
    ax_ts.set_title('Year-over-Year Faculty Count\n(top-10 schools by record volume)',
                    fontsize=9, fontweight='bold')
    ax_ts.set_xlabel('Year', fontsize=8)
    ax_ts.set_ylabel('Avg faculty/snapshot', fontsize=8)
    ax_ts.legend(fontsize=6.5, ncol=2, framealpha=0.85)
    ax_ts.spines[['top', 'right']].set_visible(False)
    ax_ts.grid(alpha=0.18, lw=0.8)
    y_data = []
    for line in ax_ts.get_lines():
        y_data.extend(np.asarray(line.get_ydata(), dtype=float).ravel())
    if y_data:
        ymax = float(np.nanmax(y_data))
        if ymax > 0:
            ax_ts.set_ylim(0, ymax * 1.06)

    # --- Panel 3: rank distribution ------------------------------------------
    RANK_COLOURS = {
        'assistant': '#3498DB', 'associate': '#2ECC71', 'full': '#8E44AD',
        'emeritus':  '#95A5A6', 'lecturer':  '#E67E22', 'adjunct': '#BDC3C7',
        'research':  '#1ABC9C', 'clinical':  '#E74C3C', 'visiting': '#F1C40F',
        'other':     '#7F8C8D',
    }
    rank_counts = df['rank'].value_counts()
    ax_rk.barh(rank_counts.index,
               rank_counts.values,
               color=[RANK_COLOURS.get(r, '#AAB7B8') for r in rank_counts.index],
               edgecolor='white', linewidth=0.4)
    ax_rk.set_title('Rank Distribution\n(all records)', fontsize=9, fontweight='bold')
    if rank_dist_logx:
        ax_rk.set_xscale('log')
    ax_rk.set_xlabel(
        'Record count (log scale)' if rank_dist_logx else 'Record count',
        fontsize=8,
    )
    _vmax = float(rank_counts.max()) if len(rank_counts) else 1.0
    for i, v in enumerate(rank_counts.values):
        if rank_dist_logx and v > 0:
            x_text = v * 1.08
        else:
            x_text = v + _vmax * 0.01
        ax_rk.text(x_text, i, f'{v:,}', va='center', fontsize=7.5)
    ax_rk.spines[['top', 'right']].set_visible(False)
    ax_rk.grid(axis='x', alpha=0.18, lw=0.8)

    # --- Panel 4: per-snapshot faculty count histogram -----------------------
    ax_hi.hist(snap_counts['n'], bins=40, color='#3498DB', edgecolor='white',
               linewidth=0.4, alpha=0.88)
    ax_hi.axvline(snap_counts['n'].median(), color='#E74C3C', lw=1.5, ls='--',
                  label=f'median = {snap_counts["n"].median():.0f}')
    ax_hi.set_title('Distribution of Faculty per Snapshot', fontsize=9, fontweight='bold')
    ax_hi.set_xlabel('Faculty extracted per snapshot', fontsize=8)
    ax_hi.set_ylabel('Number of snapshots', fontsize=8)
    ax_hi.legend(fontsize=8)
    ax_hi.spines[['top', 'right']].set_visible(False)
    ax_hi.grid(alpha=0.18, lw=0.8)

    # ── Figure title & summary stats ─────────────────────────────────────────
    n_schools  = df['uni_slug'].nunique()
    n_snaps    = snap_counts.shape[0]
    n_good     = (school_avg >= 20).sum()
    n_marginal = ((school_avg >= 8) & (school_avg < 20)).sum()
    n_poor     = (school_avg < 8).sum()
    _sort_note = '' if ss == 'volume' else '  │  left bar chart: A→Z'
    _miss_note = f'  │  {len(roster_missing)} roster school(s) with 0 parsed records (grey bars)' if roster_missing else ''
    fig.suptitle(
        f'Stage 4 — HTML Faculty Parse Quality  |  {len(df):,} records  |  '
        f'{n_schools} schools  |  {n_snaps:,} snapshots  |  '
        f'avg {snap_counts["n"].mean():.1f} faculty/snapshot\n'
        f'GREEN {n_good} good (>=20)   AMBER {n_marginal} marginal (8-19)   RED {n_poor} poor (<8)'
        f'{_sort_note}{_miss_note}',
        fontsize=11, fontweight='bold', color='#2C3E50', y=0.98
    )

    # ── Print flagged schools ─────────────────────────────────────────────────
    if roster_missing:
        print(f"\n  Roster schools with no parsed records ({len(roster_missing)}) — grey bars on left; "
              f"often condemned in Cell 4, blocked plan, or not yet parsed:")
        for s in roster_missing[:35]:
            print(f"     {s}")
        if len(roster_missing) > 35:
            print(f"     … ({len(roster_missing) - 35} more)")

    poor_schools = school_avg[school_avg < 8].index.tolist()
    if poor_schools:
        print(f"\n  Warning: schools with avg < 8 faculty/snapshot (may need parser fix or URL update):")
        for s in poor_schools:
            print(f"     {s:<50}  avg {school_avg[s]:.1f}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='#F7F9FC')
    plt.show()
    plt.close(fig)
    print(f"\n  Saved -> {out_path}")


# ---------------------------------------------------------------------------
# plot_stage5 — Longitudinal panel summary
# ---------------------------------------------------------------------------
def plot_stage5(panel_records, df_schools, out_path,
                panel_path=None, collision_path=None, school_sort='volume'):
    """
    Four-panel figure for the linked faculty panel.

    Panel 1 (top-left)  — Unique faculty observed per year (all schools stacked
                          area, showing growth of the dataset over time).
    Panel 2 (top-right) — Panel-length distribution: how many snapshot years
                          does each faculty member appear in?
    Panel 3 (bot-left)  — Per-school faculty count (bar chart, sorted).
    Panel 4 (bot-right) — Rank composition over time (stacked area %).

    school_sort : str
        'volume' (default): schools by unique faculty count; 'alphabetical': A→Z top→bottom on panel 3.
    """
    out_path = Path(out_path)
    ss = _norm_school_sort(school_sort)

    _recs = list(panel_records) if panel_records else []
    if not _recs and panel_path and Path(panel_path).exists():
        with open(panel_path, encoding='utf-8') as f:
            _recs = [json.loads(l) for l in f if l.strip()]
    if not _recs:
        print("  No panel records found — run Cell 5 first.")
        return

    df = pd.DataFrame(_recs)
    df['year'] = df['year'].astype(int)

    # Unique faculty per year
    by_year = (df.groupby('year')['faculty_id']
                 .nunique()
                 .reset_index(name='n_faculty')
                 .sort_values('year'))

    # Panel length per faculty member
    panel_len = (df.groupby('faculty_id')['year']
                   .agg(lambda yrs: yrs.max() - yrs.min() + 1)
                   .reset_index(name='span_years'))

    # Per-school faculty count (unique faculty_id)
    by_school = (df.groupby('uni_slug')['faculty_id']
                   .nunique()
                   .reset_index(name='n_faculty'))
    if ss == 'volume':
        by_school = by_school.sort_values('n_faculty', ascending=True).reset_index(drop=True)
    else:
        by_school = by_school.sort_values('uni_slug', ascending=True).reset_index(drop=True)

    # Rank composition over time (% of observations per year)
    RANK_COLOURS = {
        'assistant': '#3498DB', 'associate': '#2ECC71', 'full': '#8E44AD',
        'emeritus':  '#95A5A6', 'lecturer':  '#E67E22', 'adjunct': '#BDC3C7',
        'research':  '#1ABC9C', 'clinical':  '#E74C3C', 'visiting': '#F1C40F',
        'instructor':'#AAB7B8', 'other':     '#7F8C8D',
    }
    rank_year = (df.groupby(['year', 'rank'])
                   .size()
                   .unstack(fill_value=0))
    rank_year_pct = rank_year.div(rank_year.sum(axis=1), axis=0) * 100

    # ── Figure ────────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(20, 14), facecolor='#F7F9FC')
    gs  = gridspec.GridSpec(2, 2, figure=fig,
                            left=0.07, right=0.97, top=0.93, bottom=0.07,
                            hspace=0.38, wspace=0.28)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 0])
    ax4 = fig.add_subplot(gs[1, 1])

    # --- Panel 1: unique faculty per year ------------------------------------
    ax1.fill_between(by_year['year'], by_year['n_faculty'],
                     alpha=0.55, color='#3498DB')
    ax1.plot(by_year['year'], by_year['n_faculty'],
             color='#2980B9', lw=2, marker='o', markersize=4)
    ax1.set_title('Unique Faculty Observed per Year', fontsize=10, fontweight='bold')
    ax1.set_xlabel('Year', fontsize=9)
    ax1.set_ylabel('Unique faculty IDs', fontsize=9)
    ax1.spines[['top', 'right']].set_visible(False)
    ax1.grid(alpha=0.18, lw=0.8)

    # --- Panel 2: panel-length distribution ----------------------------------
    max_span = panel_len['span_years'].max()
    bins = range(1, max_span + 2)
    ax2.hist(panel_len['span_years'], bins=bins,
             color='#8E44AD', edgecolor='white', linewidth=0.5, alpha=0.88,
             align='left')
    ax2.axvline(panel_len['span_years'].median(), color='#E74C3C', lw=1.8,
                ls='--', label=f'median = {panel_len["span_years"].median():.0f} yrs')
    ax2.set_title('Panel Length Distribution\n(years each faculty member appears)',
                  fontsize=10, fontweight='bold')
    ax2.set_xlabel('Years in panel', fontsize=9)
    ax2.set_ylabel('Number of faculty', fontsize=9)
    ax2.legend(fontsize=9)
    ax2.spines[['top', 'right']].set_visible(False)
    ax2.grid(alpha=0.18, lw=0.8)

    # --- Panel 3: per-school unique faculty count ----------------------------
    y_pos = range(len(by_school))
    ax3.barh(list(y_pos), by_school['n_faculty'],
             color='#2ECC71', edgecolor='white', linewidth=0.4)
    ax3.set_yticks(list(y_pos))
    ax3.set_yticklabels(
        [s.replace('_', ' ').title() for s in by_school['uni_slug']],
        fontsize=7.0
    )
    ax3.set_xlabel('Unique faculty observed', fontsize=9)
    ax3.set_title('Unique Faculty per School\n(total across all years)',
                  fontsize=10, fontweight='bold')
    for i, v in enumerate(by_school['n_faculty']):
        ax3.text(v + by_school['n_faculty'].max() * 0.01, i,
                 str(v), va='center', fontsize=6.5)
    ax3.spines[['top', 'right']].set_visible(False)
    ax3.grid(axis='x', alpha=0.18, lw=0.8)
    if ss == 'alphabetical':
        ax3.invert_yaxis()

    # --- Panel 4: rank composition over time (stacked %) --------------------
    rank_order = ['full', 'associate', 'assistant', 'emeritus', 'adjunct',
                  'research', 'lecturer', 'visiting', 'clinical', 'instructor', 'other']
    present = [r for r in rank_order if r in rank_year_pct.columns]
    bottoms = np.zeros(len(rank_year_pct))
    for rank in present:
        vals = rank_year_pct[rank].values
        ax4.bar(rank_year_pct.index, vals, bottom=bottoms,
                label=rank, color=RANK_COLOURS.get(rank, '#AAB7B8'),
                edgecolor='none', width=0.85)
        bottoms += vals
    ax4.set_title('Rank Composition Over Time\n(% of panel observations)',
                  fontsize=10, fontweight='bold')
    ax4.set_xlabel('Year', fontsize=9)
    ax4.set_ylabel('% of observations', fontsize=9)
    ax4.set_ylim(0, 105)
    ax4.legend(fontsize=7.5, ncol=2, loc='upper left', framealpha=0.88)
    ax4.spines[['top', 'right']].set_visible(False)
    ax4.grid(axis='y', alpha=0.18, lw=0.8)

    # ── Title ─────────────────────────────────────────────────────────────────
    n_fac    = df['faculty_id'].nunique()
    n_sch    = df['uni_slug'].nunique()
    n_coll   = df['collision'].sum()
    yr_range = f"{df['year'].min()}–{df['year'].max()}"
    _sort_note = '' if ss == 'volume' else '  │  panel 3 schools: A→Z'
    fig.suptitle(
        f'Stage 5 — Longitudinal Faculty Panel  |  {len(df):,} observations  |  '
        f'{n_fac:,} unique faculty  |  {n_sch} schools  |  {yr_range}\n'
        f'{n_coll:,} collision flags ({n_coll/n_fac*100:.1f}% of faculty)'
        f'{_sort_note}',
        fontsize=11, fontweight='bold', color='#2C3E50', y=0.97
    )

    # ── Print collision summary ───────────────────────────────────────────────
    if n_coll:
        print(f"\n  {n_coll:,} name-key collisions flagged "
              f"(two display names → same key at same school).")
        print(f"  See {collision_path or 'faculty_panel_collisions.jsonl'} for details.")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='#F7F9FC')
    plt.show()
    plt.close(fig)
    print(f"\n  Saved -> {out_path}")
