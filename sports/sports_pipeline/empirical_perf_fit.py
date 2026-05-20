"""Fit and draw A_i from 530 individual player-season ``perf`` (conditions check).

Run ``fit_and_save`` from ``530_sports_pipeline.ipynb`` CELL 5b after building ``ind``.
537 / 538 use ``draw_empirical_abilities`` when ability choice is ``empirical_530``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from scipy import stats

# (scipy_name, n_params, frozen dist for fit)
_CANDIDATES: tuple[tuple[str, Any], ...] = (
    ("norm", stats.norm),
    ("t", stats.t),
    ("skewnorm", stats.skewnorm),
    ("laplace", stats.laplace),
    ("logistic", stats.logistic),
)


def default_fit_path() -> Path:
    from sports_pipeline.paths import mbb_dir

    return mbb_dir() / "empirical_perf_fit.json"


def _params_to_list(params: tuple[float, ...]) -> list[float]:
    return [float(x) for x in params]


def _ks_pvalue(dist, params: tuple[float, ...], x: np.ndarray) -> float:
    return float(stats.kstest(x, dist.cdf, args=params).pvalue)


def fit_perf_array(
    x: np.ndarray,
    *,
    metric_key: str = "perf",
    z_within_season: bool = True,
    n_sample_for_fit: int | None = 100_000,
    n_bins: int = 60,
) -> dict[str, Any]:
    """Fit parametric laws; pick lowest AIC among successful fits."""
    arr = np.asarray(x, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size < 100:
        raise ValueError(f"need at least 100 finite perf values, got {arr.size}")
    if n_sample_for_fit is not None and arr.size > n_sample_for_fit:
        rng = np.random.default_rng(530_590_5)
        arr = rng.choice(arr, size=int(n_sample_for_fit), replace=False)

    rows: list[dict[str, Any]] = []
    for name, dist in _CANDIDATES:
        try:
            params = tuple(float(p) for p in dist.fit(arr))
            loglik = float(np.sum(dist.logpdf(arr, *params)))
            k = len(params)
            aic = 2 * k - 2 * loglik
            bic = k * np.log(arr.size) - 2 * loglik
            rows.append(
                {
                    "scipy_name": name,
                    "params": _params_to_list(params),
                    "n_params": k,
                    "loglik": loglik,
                    "aic": float(aic),
                    "bic": float(bic),
                    "ks_pvalue": _ks_pvalue(dist, params, arr),
                }
            )
        except Exception as exc:  # noqa: BLE001 — collect failures per candidate
            rows.append(
                {
                    "scipy_name": name,
                    "error": str(exc),
                }
            )

    ok = [r for r in rows if "aic" in r]
    if not ok:
        raise RuntimeError("no distribution fit succeeded")
    best = min(ok, key=lambda r: r["aic"])
    hist_counts, hist_edges = np.histogram(arr, bins=n_bins)
    return {
        "version": 1,
        "source": "530_sports_pipeline CELL 5b",
        "metric_key": str(metric_key),
        "z_within_season": bool(z_within_season),
        "n_fit": int(arr.size),
        "empirical": {
            "mean": float(np.mean(arr)),
            "std": float(np.std(arr, ddof=1)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
        },
        "histogram": {
            "n_bins": n_bins,
            "edges": [float(x) for x in hist_edges],
            "counts": [int(x) for x in hist_counts],
        },
        "best": best,
        "candidates": rows,
    }


def xlabel_from_fit(payload: dict[str, Any]) -> str:
    metric = str(payload.get("metric_key", "perf"))
    if bool(payload.get("z_within_season", True)):
        return "Player-season perf (within-season z)"
    return f"Player-season perf ({metric})"


def overlay_530_reference_on_axis(ax, *, path: Path | None = None) -> tuple[str, bool]:
    """Overlay 530 histogram (if saved) and fitted PDF. Returns (xlabel, had_histogram)."""
    try:
        payload = load_fit(path)
    except FileNotFoundError:
        return "Synthetic ability $A_i$", False

    xlab = xlabel_from_fit(payload)
    had_hist = False
    hist = payload.get("histogram")
    if isinstance(hist, dict) and hist.get("edges") and hist.get("counts"):
        edges = np.asarray(hist["edges"], dtype=float)
        counts = np.asarray(hist["counts"], dtype=float)
        widths = np.diff(edges)
        dens = counts / (float(counts.sum()) * widths)
        ax.step(
            edges,
            np.r_[dens, dens[-1]],
            where="post",
            color="darkorange",
            lw=2.0,
            label=(
                f"530 player-season perf (n={int(payload['n_fit']):,})"
                if payload.get("n_fit") is not None
                else "530 player-season perf"
            ),
        )
        had_hist = True
        xlo, xhi = float(edges[0]), float(edges[-1])
    else:
        em = payload.get("empirical", {})
        xlo = float(em.get("min", -3.0))
        xhi = float(em.get("max", 3.0))

    grid = np.linspace(xlo, xhi, 300)
    ax.plot(
        grid,
        pdf_on_grid(payload, grid),
        color="crimson",
        ls="--",
        lw=1.6,
        alpha=0.95,
        label=f"530 fitted PDF ({payload['best']['scipy_name']})",
    )
    return xlab, had_hist


def save_fit(payload: dict[str, Any], path: Path | None = None) -> Path:
    out = Path(path) if path is not None else default_fit_path()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out


def load_fit(path: Path | None = None) -> dict[str, Any]:
    p = Path(path) if path is not None else default_fit_path()
    if not p.is_file():
        raise FileNotFoundError(
            f"empirical perf fit not found at {p}. Run 530 CELL 5b first."
        )
    return json.loads(p.read_text(encoding="utf-8"))


def scipy_dist_from_fit(payload: dict[str, Any] | None = None, *, path: Path | None = None):
    data = payload if payload is not None else load_fit(path)
    name = str(data["best"]["scipy_name"])
    params = tuple(float(x) for x in data["best"]["params"])
    dist = getattr(stats, name)
    return dist, params, data


def draw_empirical_abilities(
    rng: np.random.Generator,
    n: int,
    *,
    path: Path | None = None,
    payload: dict[str, Any] | None = None,
) -> np.ndarray:
    dist, params, _ = scipy_dist_from_fit(payload, path=path)
    return dist.rvs(*params, size=int(n), random_state=rng)


def pdf_on_grid(
    payload: dict[str, Any],
    grid: np.ndarray,
) -> np.ndarray:
    dist, params, _ = scipy_dist_from_fit(payload)
    return dist.pdf(grid, *params)
