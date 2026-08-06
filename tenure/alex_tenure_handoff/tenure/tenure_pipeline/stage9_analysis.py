# stage9_analysis.py — Stage 9: Inverted-U Analysis
#
# Collapses faculty_panel_with_pools.jsonl to one record per person,
# bins by leave-self-out (LOO) peer pool quality, computes tenure /
# attrition rates per bin with Wilson CIs, and saves a 2-panel PNG
# plus a summary CSV.

import json
import math
from collections import defaultdict
from pathlib import Path
import statistics


# ── Wilson binomial confidence interval ───────────────────────────────────────

def _wilson_ci(n_success, n_total, z=1.96):
    """Return (lo, hi) Wilson score interval for a proportion.  Safe for n=0."""
    if n_total == 0:
        return (0.0, 1.0)
    p = n_success / n_total
    denom = 1 + z ** 2 / n_total
    center = (p + z ** 2 / (2 * n_total)) / denom
    spread = z * math.sqrt(p * (1 - p) / n_total + z ** 2 / (4 * n_total ** 2)) / denom
    return (max(0.0, center - spread), min(1.0, center + spread))


# ── Person-level collapse ──────────────────────────────────────────────────────

def _load_person_level(in_path):
    """
    Read faculty_panel_with_pools.jsonl.  Collapse to one record per person:
      loo_mean  — mean poolq_loo_mean across all assistant-rank years with a
                  computable LOO value  (persons with NO computable LOO are dropped)
      tenure    — bool
      attrition — bool
      censored  — bool
      uni_slug  — university slug (last seen)

    Returns a list of dicts.
    """
    person = defaultdict(lambda: {
        'loo_vals':  [],
        'tenure':    False,
        'attrition': False,
        'censored':  False,
        'uni_slug':  '',
    })

    with open(str(in_path)) as f:
        for line in f:
            r = json.loads(line)
            if not r.get('ever_assistant'):
                continue
            fid = r['faculty_id']
            p = person[fid]
            p['tenure']    = bool(r.get('tenure_event', False))
            p['attrition'] = bool(r.get('attrition', False))
            p['censored']  = bool(r.get('censored', False))
            p['uni_slug']  = r.get('uni_slug', '')
            if r.get('rank') == 'assistant':
                v = r.get('poolq_loo_mean')
                if v is not None:
                    p['loo_vals'].append(v)

    rows = []
    for fid, p in person.items():
        if not p['loo_vals']:
            continue
        rows.append({
            'faculty_id': fid,
            'loo_mean':   statistics.mean(p['loo_vals']),
            'tenure':     p['tenure'],
            'attrition':  p['attrition'],
            'censored':   p['censored'],
            'uni_slug':   p['uni_slug'],
        })
    return rows


# ── Log / z-score helpers ──────────────────────────────────────────────────────

def _apply_log(rows):
    """Add 'loo_log' key: log(1 + loo_mean).  Handles loo_mean = 0 safely."""
    import math
    for r in rows:
        r['loo_log'] = math.log1p(r['loo_mean'])


def _apply_z_score(rows, src_key='loo_mean'):
    """
    Z-score the values at src_key, storing result in 'loo_z'.
    Returns (mean, std) for reporting.  If std == 0, loo_z = 0.
    """
    vals = [r[src_key] for r in rows]
    mu  = sum(vals) / len(vals)
    std = (sum((v - mu) ** 2 for v in vals) / len(vals)) ** 0.5
    for r in rows:
        r['loo_z'] = (r[src_key] - mu) / std if std > 0 else 0.0
    return mu, std


# ── Binning ────────────────────────────────────────────────────────────────────

def _bin_rows(rows, n_bins, bin_method='quantile', z_score=False, log_bin=False):
    """
    Assign each row a 'bin' key (1-indexed).

    bin_method='quantile'    — equal number of people per bin (rank-based)
    bin_method='equal_width' — equal range per bin (variable N per bin)
    log_bin=True             — transform LOO to log(1 + LOO) before binning;
                               useful with equal_width to avoid outlier-dominated bins
    z_score=True             — z-score the (possibly log-transformed) values before
                               binning; irrelevant for quantile (rank-preserving) but
                               changes equal_width boundaries to SD units

    Transform order: log → z-score → bin.

    Returns rows sorted by the binning key.
    """
    if log_bin:
        _apply_log(rows)

    if z_score:
        src = 'loo_log' if log_bin else 'loo_mean'
        _apply_z_score(rows, src_key=src)
        sort_key = lambda r: r['loo_z']
    elif log_bin:
        sort_key = lambda r: r['loo_log']
    else:
        sort_key = lambda r: r['loo_mean']

    rows_sorted = sorted(rows, key=sort_key)

    if bin_method == 'quantile':
        n = len(rows_sorted)
        for i, r in enumerate(rows_sorted):
            r['bin'] = min(int(i * n_bins / n) + 1, n_bins)

    elif bin_method == 'equal_width':
        vals = [sort_key(r) for r in rows_sorted]
        lo, hi = min(vals), max(vals)
        width = (hi - lo) / n_bins if hi > lo else 1.0
        for r in rows_sorted:
            v = sort_key(r)
            b = int((v - lo) / width) + 1
            r['bin'] = min(b, n_bins)

    else:
        raise ValueError("bin_method must be 'quantile' or 'equal_width'")

    return rows_sorted


def _aggregate_bins(rows_sorted, n_bins, exclude_censored):
    """
    Build a list of per-bin summary dicts.
    If exclude_censored=True, tenure_rate and attrition_rate are computed
    only on resolved cases (tenure + attrition); censored are shown as a count.
    """
    bins = []
    for b in range(1, n_bins + 1):
        in_bin = [r for r in rows_sorted if r['bin'] == b]
        if not in_bin:
            continue

        n_all  = len(in_bin)
        n_ten  = sum(1 for r in in_bin if r['tenure'])
        n_att  = sum(1 for r in in_bin if r['attrition'])
        n_cens = sum(1 for r in in_bin if r['censored'])

        n_res  = n_ten + n_att if exclude_censored else n_all

        ten_rate = n_ten / n_res if n_res > 0 else None
        att_rate = n_att / n_res if n_res > 0 else None
        ten_ci   = _wilson_ci(n_ten, n_res) if n_res > 0 else (None, None)
        att_ci   = _wilson_ci(n_att, n_res) if n_res > 0 else (None, None)

        loo_vals = [r['loo_mean'] for r in in_bin]
        has_log  = 'loo_log' in in_bin[0]
        has_z    = 'loo_z'   in in_bin[0]
        log_vals = [r['loo_log'] for r in in_bin] if has_log else None
        z_vals   = [r['loo_z']   for r in in_bin] if has_z   else None
        bins.append({
            'bin':            b,
            'n_all':          n_all,
            'n_tenure':       n_ten,
            'n_attrition':    n_att,
            'n_censored':     n_cens,
            'n_resolved':     n_res,
            'tenure_rate':    ten_rate,
            'tenure_ci_lo':   ten_ci[0],
            'tenure_ci_hi':   ten_ci[1],
            'attrition_rate': att_rate,
            'attr_ci_lo':     att_ci[0],
            'attr_ci_hi':     att_ci[1],
            'loo_min':        min(loo_vals),
            'loo_median':     statistics.median(loo_vals),
            'loo_max':        max(loo_vals),
            'loo_log_median': statistics.median(log_vals) if log_vals is not None else None,
            'loo_z_median':   statistics.median(z_vals)   if z_vals   is not None else None,
        })
    return bins


# ── Plot ───────────────────────────────────────────────────────────────────────

def _plot_inverted_u(bins, out_path, n_bins, exclude_censored,
                     bin_method='quantile', z_score=False, log_bin=False,
                     n_persons=None):
    try:
        import matplotlib
    except ImportError:
        print("  ⚠  matplotlib not found — skipping plot (install it in the active kernel)")
        return
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker

    bin_nums   = [b['bin']            for b in bins]
    ten_rates  = [b['tenure_rate']    for b in bins]
    att_rates  = [b['attrition_rate'] for b in bins]
    ten_lo     = [b['tenure_ci_lo']   for b in bins]
    ten_hi     = [b['tenure_ci_hi']   for b in bins]
    att_lo     = [b['attr_ci_lo']     for b in bins]
    att_hi     = [b['attr_ci_hi']     for b in bins]
    n_res_list = [b['n_resolved']     for b in bins]
    n_all_list = [b['n_all']          for b in bins]

    # X-tick labels: show median of the binning-space value below each bin number
    has_z   = z_score  and bins[0].get('loo_z_median')   is not None
    has_log = log_bin  and bins[0].get('loo_log_median') is not None

    if has_z:
        xtick_labels = [
            'Q{}\n({:.2f}σ)'.format(b['bin'], b['loo_z_median']) for b in bins
        ]
        loo_unit = 'z-scored log(1+LOO) (σ)' if log_bin else 'z-scored LOO (σ)'
    elif has_log:
        xtick_labels = [
            'Q{}\n({:.2f})'.format(b['bin'], b['loo_log_median']) for b in bins
        ]
        loo_unit = 'log(1+LOO)'
    else:
        xtick_labels = [
            'Q{}\n({:.1f})'.format(b['bin'], b['loo_median']) for b in bins
        ]
        loo_unit = 'raw LOO (pubs/yr)'

    method_label = 'quantile bins (≈equal N)' if bin_method == 'quantile' else 'equal-width bins'
    pop_note = 'resolved' if exclude_censored else 'all (incl. censored)'

    # Build the population line for the title
    if n_persons is not None:
        n_tot  = n_persons.get('n_with_loo', 0)
        n_ten  = n_persons.get('n_tenure', 0)
        n_att  = n_persons.get('n_attrition', 0)
        n_cens = n_persons.get('n_censored', 0)
        n_res  = n_persons.get('n_resolved', 0)
        pct = lambda a, b: '{:.0f}%'.format(a / b * 100) if b > 0 else 'n/a'
        pop_line = (
            'N = {:,} persons total  ·  '
            'tenure {:,} ({})  ·  '
            'attrition {:,} ({})  ·  '
            'censored {:,} ({})  ·  '
            'resolved {:,}'.format(
                n_tot,
                n_ten,  pct(n_ten,  n_tot),
                n_att,  pct(n_att,  n_tot),
                n_cens, pct(n_cens, n_tot),
                n_res,
            )
        )
    else:
        pop_line = ''

    fig, axes = plt.subplots(2, 1, figsize=(9, 7.5), sharex=True)
    title_lines = (
        "Inverted-U Check: Tenure / Attrition Rate by LOO Peer Pool Quality\n"
        "{} bins, {}; N above point = {} cases; 95% Wilson CI".format(
            n_bins, method_label, pop_note)
    )
    if pop_line:
        title_lines += '\n' + pop_line
    fig.suptitle(title_lines, fontsize=10.5, fontweight='bold', y=0.99)

    colors = {'tenure': '#2166AC', 'attrition': '#D6604D'}

    def _one_panel(ax, rates, ci_lo, ci_hi, color, label, ylabel):
        yerr_lo = [max(0.0, r - lo) for r, lo in zip(rates, ci_lo)]
        yerr_hi = [max(0.0, hi - r) for r, hi in zip(rates, ci_hi)]
        ax.errorbar(
            bin_nums, rates,
            yerr=[yerr_lo, yerr_hi],
            fmt='o-', color=color, linewidth=1.8, markersize=6,
            capsize=4, elinewidth=1.2, label=label
        )
        mean_rate = sum(rates) / len(rates)
        ax.axhline(mean_rate, color=color, alpha=0.25, linestyle=':', linewidth=1.2,
                   label='overall mean ({:.1%})'.format(mean_rate))
        # Annotate: N resolved above, N total (grey) below
        for x, rate, n_res, n_all in zip(bin_nums, rates, n_res_list, n_all_list):
            ax.annotate(str(n_res), (x, rate),
                        textcoords='offset points', xytext=(0, 8),
                        ha='center', fontsize=7.5, color='#444')
            ax.annotate('/{}'.format(n_all), (x, rate),
                        textcoords='offset points', xytext=(0, -11),
                        ha='center', fontsize=6.5, color='#999')
        ax.set_ylabel(ylabel, fontsize=10)
        ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0, decimals=0))
        ax.set_ylim(0, None)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.legend(fontsize=8.5)

    _one_panel(axes[0], ten_rates, ten_lo, ten_hi,
               colors['tenure'],    'Tenure rate',    'Tenure rate')
    _one_panel(axes[1], att_rates, att_lo, att_hi,
               colors['attrition'], 'Attrition rate', 'Attrition rate')

    axes[1].set_xlabel(
        "LOO peer pool quality bin  (1 = lowest, {} = highest)\n"
        "Median {} shown below each bin label\n"
        "LOO = mean pubs/yr of all other OA-matched co-hired assistants "
        "in same dept-year".format(n_bins, loo_unit),
        fontsize=8.5
    )
    axes[1].set_xticks(bin_nums)
    axes[1].set_xticklabels(xtick_labels, fontsize=7.5)

    plt.tight_layout()
    fig.savefig(str(out_path), dpi=150, bbox_inches='tight')
    plt.close(fig)


# ── Console table ──────────────────────────────────────────────────────────────

def _print_table(bins):
    has_z = bins[0].get('loo_z_median') is not None
    if has_z:
        header = (
            "  {:>3}  {:>6}  {:>6}  {:>6}  {:>6}  {:>8}  {:>7}  {:>6}"
            .format('Bin', 'N_all', 'N_res', 'Ten%', 'Att%', 'LOO_med', 'LOO_z', 'N_cens')
        )
    else:
        header = (
            "  {:>3}  {:>6}  {:>6}  {:>6}  {:>6}  {:>8}  {:>6}"
            .format('Bin', 'N_all', 'N_res', 'Ten%', 'Att%', 'LOO_med', 'N_cens')
        )
    print(header)
    print("  " + "-" * (len(header) - 2))
    for b in bins:
        ten_pct = '{:5.1f}%'.format(b['tenure_rate'] * 100) if b['tenure_rate'] is not None else '  n/a '
        att_pct = '{:5.1f}%'.format(b['attrition_rate'] * 100) if b['attrition_rate'] is not None else '  n/a '
        if has_z:
            print(
                "  {:>3}  {:>6}  {:>6}  {:>6}  {:>6}  {:>8.2f}  {:>+7.2f}  {:>6}"
                .format(b['bin'], b['n_all'], b['n_resolved'],
                        ten_pct, att_pct, b['loo_median'],
                        b['loo_z_median'], b['n_censored'])
            )
        else:
            print(
                "  {:>3}  {:>6}  {:>6}  {:>6}  {:>6}  {:>8.2f}  {:>6}"
                .format(b['bin'], b['n_all'], b['n_resolved'],
                        ten_pct, att_pct, b['loo_median'], b['n_censored'])
            )


# ── CSV writer ─────────────────────────────────────────────────────────────────

def _save_csv(bins, csv_path):
    if not bins:
        return
    headers = list(bins[0].keys())
    with open(str(csv_path), 'w') as f:
        f.write(','.join(headers) + '\n')
        for b in bins:
            f.write(','.join(
                '' if v is None else str(round(v, 6) if isinstance(v, float) else v)
                for v in b.values()
            ) + '\n')


# ── Main entry point ───────────────────────────────────────────────────────────

def build_inverted_u(in_path, out_dir, n_bins=12, exclude_censored=True,
                     bin_method='quantile', z_score=False, log_bin=False):
    """
    Build the inverted-U analysis from faculty_panel_with_pools.jsonl.

    Parameters
    ----------
    in_path           : path to faculty_panel_with_pools.jsonl  (Stage 8 output)
    out_dir           : directory for stage9_inverted_u.png + stage9_binned_table.csv
    n_bins            : number of bins (default 12)
    exclude_censored  : if True (default), rates are computed on resolved cases
                        (tenure + attrition) only; censored shown as a count column
    bin_method        : 'quantile'    — equal number of people per bin (default)
                        'equal_width' — equal LOO range per bin (variable N)
    log_bin           : if True, transform LOO to log(1 + LOO) before binning;
                        most useful with equal_width to prevent outliers dominating
                        the upper bins (LOO is right-skewed, max ~27 pubs/yr)
    z_score           : if True, standardise the (possibly log-transformed) LOO to
                        (x - mean) / std before binning; transform order: log → z → bin

    Returns
    -------
    dict with summary stats and output paths
    """
    in_path = Path(in_path)
    out_dir = Path(out_dir)

    # ── Sample-loss accounting ────────────────────────────────────────────────
    print("  Loading person-level data …")
    rows = _load_person_level(in_path)

    n_with_loo  = len(rows)
    n_tenure    = sum(1 for r in rows if r['tenure'])
    n_attrition = sum(1 for r in rows if r['attrition'])
    n_censored  = sum(1 for r in rows if r['censored'])
    n_resolved  = n_tenure + n_attrition

    print("\n  ── Sample-loss accounting ──────────────────────────────────")
    print("  Persons with computable LOO (analysis population) : {:,}".format(n_with_loo))
    print("    → tenure events      : {:,}  ({:.1f}%)".format(n_tenure,    n_tenure    / n_with_loo * 100))
    print("    → attrition          : {:,}  ({:.1f}%)".format(n_attrition, n_attrition / n_with_loo * 100))
    print("    → censored (still asst ≈ 2024) : {:,}  ({:.1f}%)".format(n_censored, n_censored / n_with_loo * 100))
    print("  Resolved (tenure + attrition)    : {:,}  ← N for rate calcs".format(n_resolved))
    print("  bin_method={!r}  log_bin={}  z_score={}  exclude_censored={}".format(
        bin_method, log_bin, z_score, exclude_censored))
    if bin_method == 'quantile' and (log_bin or z_score):
        print("  Note: log_bin/z_score have no effect on quantile bin assignment"
              " (rank-preserving); transformed values shown in table/plot for reference.")

    # ── Bin and aggregate ─────────────────────────────────────────────────────
    rows_sorted = _bin_rows(rows, n_bins, bin_method=bin_method,
                            z_score=z_score, log_bin=log_bin)
    bins = _aggregate_bins(rows_sorted, n_bins, exclude_censored)

    # ── Console table ─────────────────────────────────────────────────────────
    print("\n  ── Binned rates ({} {} bins) ────────────────────────────────".format(
        n_bins, bin_method))
    _print_table(bins)

    # ── Save CSV ──────────────────────────────────────────────────────────────
    csv_path = out_dir / 'stage9_binned_table.csv'
    _save_csv(bins, csv_path)
    print("\n  CSV  → {}".format(csv_path))

    # ── Plot ──────────────────────────────────────────────────────────────────
    png_path = out_dir / 'stage9_inverted_u.png'
    _plot_inverted_u(bins, png_path, n_bins, exclude_censored,
                     bin_method=bin_method, z_score=z_score, log_bin=log_bin,
                     n_persons={
                         'n_with_loo':  n_with_loo,
                         'n_tenure':    n_tenure,
                         'n_attrition': n_attrition,
                         'n_censored':  n_censored,
                         'n_resolved':  n_resolved,
                     })
    print("  PNG  → {}".format(png_path))

    return {
        'n_persons_with_loo': n_with_loo,
        'n_tenure':           n_tenure,
        'n_attrition':        n_attrition,
        'n_censored':         n_censored,
        'n_resolved':         n_resolved,
        'n_bins':             n_bins,
        'bin_method':         bin_method,
        'log_bin':            log_bin,
        'z_score':            z_score,
        'exclude_censored':   exclude_censored,
        'csv_path':           str(csv_path),
        'png_path':           str(png_path),
    }
