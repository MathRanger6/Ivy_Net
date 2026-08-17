#!/usr/bin/env python3
"""PD21 — Calibrate Grandchild ASSIGN rho to empirical sorting index (H_sort).

Alex (Aug 14): park formal rho MLE; calibrate rho so simulated H_sort matches
empirical H_sort (empirical roster caps, 2011–2021).

Search: ``bracket`` (default) expands then bisects; ``grid`` = uniform legacy sweep.

Run (repo root):
  python sports/scripts/pd21_rho_hsort_calibrate.py --n-seeds 50 --n-jobs 8
  python sports/scripts/pd21_rho_hsort_calibrate.py --method grid --rho-max 0.5
  python sports/scripts/pd21_rho_hsort_calibrate.py --quick

Outputs (HEROs_and_PASSes/pd21_rho/):
  PD21_rho_hsort_calibrate_2011_2021_detail.jsonl   — one row per (season, rho, seed)
  PD21_rho_hsort_calibrate_2011_2021_summary.csv
  PD21_rho_hsort_calibrate_2011_2021_fit.json
  PD21_rho_hsort_calibrate_2011_2021.png
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SPORTS))
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import PD21_RHO, ensure_hero_dirs
from interval_overlap_paths import seasons_label, window_tag

import grandchild_selection_inverted_u_diagnostic as gsel

FULL_PANEL_SEASON_MIN = gsel.FULL_PANEL_SEASON_MIN
FULL_PANEL_SEASON_MAX = gsel.FULL_PANEL_SEASON_MAX
OUT = PD21_RHO
DEFAULT_RHO_REF = 0.5
BASE_SEED = 54210814
BRACKET_RHO_INIT_HI = 0.05
BRACKET_RHO_MAX_DEFAULT = 0.5
RHO_MATCH_DECIMALS = 12


def normalize_rho(rho: float) -> float:
    return round(float(rho), RHO_MATCH_DECIMALS)


def _rho_seed_tag(rho: float) -> int:
    """Deterministic seed offset; finer than 0.001 rho for sub-0.01 bracket values."""
    return int(round(normalize_rho(rho) * 1_000_000))


def _format_duration(seconds: float) -> str:
    if not np.isfinite(seconds) or seconds < 0:
        return "?"
    seconds = int(round(float(seconds)))
    if seconds < 60:
        return f"{seconds}s"
    minutes, sec = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes}m {sec:02d}s"
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes:02d}m"


@dataclass
class RunProgress:
    """Global sim-job counter with periodic ETA for adaptive bracket runs."""

    n_seasons: int
    n_seeds: int
    eval_reference_rho: bool
    report_interval_s: float = 30.0
    run_t0: float = field(default_factory=time.perf_counter)
    jobs_completed: int = 0
    seasons_completed: int = 0
    jobs_by_season: list[int] = field(default_factory=list)
    last_report_t: float = field(default_factory=time.perf_counter)
    reference_phase: bool = False
    reference_seasons_done: int = 0

    def tick(self, n: int = 1) -> None:
        self.jobs_completed += int(n)
        self._maybe_report()

    def season_done(self, jobs_this_season: int) -> None:
        self.seasons_completed += 1
        self.jobs_by_season.append(int(jobs_this_season))
        self._report(force=True)

    def start_reference_phase(self) -> None:
        self.reference_phase = True
        print(
            f"\n[progress] Reference rho={DEFAULT_RHO_REF} — "
            f"{self.n_seasons * self.n_seeds} jobs remaining (est.)",
            flush=True,
        )

    def reference_season_done(self) -> None:
        self.reference_seasons_done += 1
        self._report(force=True)

    def estimate_total_jobs(self) -> int:
        ref_jobs = self.n_seasons * self.n_seeds if self.eval_reference_rho else 0
        if self.reference_phase:
            ref_remaining = (self.n_seasons - self.reference_seasons_done) * self.n_seeds
            return self.jobs_completed + max(0, ref_remaining)
        if self.jobs_by_season:
            avg = sum(self.jobs_by_season) / len(self.jobs_by_season)
        else:
            avg = 4.0 * self.n_seeds
        seasons_left = max(0, self.n_seasons - self.seasons_completed)
        return self.jobs_completed + int(avg * seasons_left) + ref_jobs

    def eta_seconds(self) -> float | None:
        elapsed = time.perf_counter() - self.run_t0
        if self.jobs_completed < 5 or elapsed < 2.0:
            return None
        rate = self.jobs_completed / elapsed
        if rate <= 0:
            return None
        remaining = max(0, self.estimate_total_jobs() - self.jobs_completed)
        return remaining / rate

    def _maybe_report(self) -> None:
        now = time.perf_counter()
        if now - self.last_report_t >= float(self.report_interval_s):
            self._report(force=True)

    def _report(self, *, force: bool = False) -> None:
        now = time.perf_counter()
        if not force and now - self.last_report_t < float(self.report_interval_s):
            return
        self.last_report_t = now
        elapsed = now - self.run_t0
        total_est = self.estimate_total_jobs()
        pct = 100.0 * self.jobs_completed / total_est if total_est > 0 else 0.0
        rate = self.jobs_completed / elapsed if elapsed > 0 else float("nan")
        eta = self.eta_seconds()
        eta_s = f" | ETA ~{_format_duration(eta)}" if eta is not None else ""
        phase = (
            f"ref {self.reference_seasons_done}/{self.n_seasons}"
            if self.reference_phase
            else f"season {self.seasons_completed}/{self.n_seasons}"
        )
        print(
            f"[progress] {self.jobs_completed}/{total_est} jobs ({pct:.0f}%) "
            f"| {rate:.1f} jobs/s | elapsed {_format_duration(elapsed)}{eta_s} "
            f"| {phase}",
            flush=True,
        )


@dataclass
class RhoEval:
    season: int
    rho: float
    n_seeds: int
    h_sort_sim_mean: float
    h_sort_sim_std: float
    global_wss_sim_mean: float


class DetailCache:
    """In-memory view of detail JSONL for skip/reuse during bracket search."""

    def __init__(self, detail_path: Path) -> None:
        self.detail_path = detail_path
        self._rows: list[dict] = []
        if detail_path.exists():
            with detail_path.open(encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        self._rows.append(json.loads(line))

    def eval_at(self, season: int, rho: float) -> RhoEval | None:
        sub = [
            r
            for r in self._rows
            if int(r["season"]) == int(season)
            and np.isclose(normalize_rho(float(r["rho"])), normalize_rho(float(rho)))
        ]
        if not sub:
            return None
        h = np.asarray([float(r["h_sort_sim"]) for r in sub], dtype=float)
        wss = np.asarray([float(r["global_wss_sim"]) for r in sub], dtype=float)
        return RhoEval(
            season=int(season),
            rho=float(rho),
            n_seeds=int(len(sub)),
            h_sort_sim_mean=float(h.mean()),
            h_sort_sim_std=float(h.std(ddof=0)) if len(h) > 1 else 0.0,
            global_wss_sim_mean=float(wss.mean()),
        )

    def done_seeds(self, season: int, rho: float) -> set[int]:
        return {
            int(r["seed"])
            for r in self._rows
            if int(r["season"]) == int(season)
            and np.isclose(normalize_rho(float(r["rho"])), normalize_rho(float(rho)))
        }


def _seed_for(base_seed: int, season: int, rho: float, rep: int) -> int:
    return int(base_seed + int(season) * 10_000 + int(rep) + _rho_seed_tag(rho))


def build_jobs_for_rho(
    sd: SeasonData,
    rho: float,
    n_seeds: int,
    base_seed: int,
    *,
    done_seeds: set[int],
) -> list[tuple[SimJob, np.ndarray, np.ndarray]]:
    jobs: list[tuple[SimJob, np.ndarray, np.ndarray]] = []
    for rep in range(int(n_seeds)):
        seed = _seed_for(base_seed, sd.season, rho, rep)
        if seed in done_seeds:
            continue
        jobs.append((SimJob(season=sd.season, rho=float(rho), seed=seed), sd.ability, sd.roster_caps))
    return jobs


def _print_batch_progress(
    completed: int,
    total: int,
    t0: float,
    *,
    progress: RunProgress | None = None,
) -> None:
    elapsed = time.perf_counter() - t0
    rate = completed / elapsed if elapsed > 0 else float("nan")
    remaining = max(0, total - completed)
    batch_eta = remaining / rate if rate > 0 else None
    batch_eta_s = f" | batch ETA ~{_format_duration(batch_eta)}" if batch_eta is not None else ""
    print(
        f"  completed {completed}/{total} "
        f"({100 * completed / total:.0f}%) "
        f"| {rate:.1f} jobs/s{batch_eta_s}",
        flush=True,
    )


def run_job_batch(
    jobs: list[tuple[SimJob, np.ndarray, np.ndarray]],
    *,
    parallel: str,
    n_jobs: int,
    detail_path: Path,
    cache: DetailCache,
    label: str = "",
    progress: RunProgress | None = None,
) -> None:
    if not jobs:
        return
    prefix = f"{label} " if label else ""
    print(f"{prefix}Running {len(jobs)} sim jobs ...", flush=True)
    t0 = time.perf_counter()
    if parallel == "ray":
        run_parallel_ray(jobs, n_jobs=n_jobs, detail_path=detail_path, progress=progress)
    else:
        run_parallel_process(jobs, n_jobs=n_jobs, detail_path=detail_path, progress=progress)
    print(f"{prefix}Batch done in {time.perf_counter() - t0:.1f}s", flush=True)
    # Reload full detail file into cache after batch append.
    cache._rows = []
    with detail_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                cache._rows.append(json.loads(line))


def ensure_rho_evaluated(
    sd: SeasonData,
    rho: float,
    *,
    n_seeds: int,
    base_seed: int,
    cache: DetailCache,
    parallel: str,
    n_jobs: int,
    detail_path: Path,
    progress: RunProgress | None = None,
) -> RhoEval:
    existing = cache.eval_at(sd.season, rho)
    if existing is not None and existing.n_seeds >= int(n_seeds):
        return existing
    jobs = build_jobs_for_rho(
        sd,
        rho,
        n_seeds,
        base_seed,
        done_seeds=cache.done_seeds(sd.season, rho),
    )
    run_job_batch(
        jobs,
        parallel=parallel,
        n_jobs=n_jobs,
        detail_path=detail_path,
        cache=cache,
        label=rf"season={sd.season} rho={rho:g}",
        progress=progress,
    )
    result = cache.eval_at(sd.season, rho)
    if result is None:
        raise RuntimeError(f"Failed to evaluate season={sd.season} rho={rho}")
    return result


def bracket_rho_for_season(
    sd: SeasonData,
    *,
    n_seeds: int,
    base_seed: int,
    cache: DetailCache,
    parallel: str,
    n_jobs: int,
    detail_path: Path,
    rho_max: float,
    rho_tol: float,
    max_expansions: int,
    max_bisect: int,
    progress: RunProgress | None = None,
) -> tuple[float, float, list[dict]]:
    """Return (rho_star, h_sim_at_star, trace rows). Assumes H_sort non-decreasing in rho."""
    target = float(sd.h_sort_empirical)
    trace: list[dict] = []

    def record(rho: float, ev: RhoEval) -> None:
        err = abs(ev.h_sort_sim_mean - target)
        trace.append(
            {
                "season": sd.season,
                "rho": normalize_rho(rho),
                "h_sort_sim_mean": ev.h_sort_sim_mean,
                "h_sort_sim_std": ev.h_sort_sim_std,
                "h_sort_empirical": target,
                "h_sort_abs_err": err,
                "phase": "bracket",
            }
        )

    ev_lo = ensure_rho_evaluated(
        sd, 0.0, n_seeds=n_seeds, base_seed=base_seed, cache=cache,
        parallel=parallel, n_jobs=n_jobs, detail_path=detail_path, progress=progress,
    )
    record(0.0, ev_lo)
    h_lo = ev_lo.h_sort_sim_mean

    if h_lo >= target:
        return 0.0, h_lo, trace

    lo, hi = 0.0, float(BRACKET_RHO_INIT_HI)
    ev_hi = ensure_rho_evaluated(
        sd, hi, n_seeds=n_seeds, base_seed=base_seed, cache=cache,
        parallel=parallel, n_jobs=n_jobs, detail_path=detail_path, progress=progress,
    )
    record(hi, ev_hi)
    h_hi = ev_hi.h_sort_sim_mean

    expansions = 0
    while h_hi < target and hi < float(rho_max) and expansions < int(max_expansions):
        lo, h_lo = hi, h_hi
        hi = min(hi * 2.0, float(rho_max))
        if np.isclose(hi, lo):
            break
        ev_hi = ensure_rho_evaluated(
            sd, hi, n_seeds=n_seeds, base_seed=base_seed, cache=cache,
            parallel=parallel, n_jobs=n_jobs, detail_path=detail_path, progress=progress,
        )
        record(hi, ev_hi)
        h_hi = ev_hi.h_sort_sim_mean
        expansions += 1
        print(
            f"  season {sd.season}: expand bracket hi={hi:g} "
            f"H_sim={h_hi:.4f} target={target:.4f}",
            flush=True,
        )

    if h_hi < target:
        best_rho = hi if abs(h_hi - target) <= abs(h_lo - target) else lo
        best_ev = cache.eval_at(sd.season, best_rho)
        assert best_ev is not None
        return best_rho, best_ev.h_sort_sim_mean, trace

    for step in range(int(max_bisect)):
        if hi - lo <= float(rho_tol):
            break
        mid = 0.5 * (lo + hi)
        ev_mid = ensure_rho_evaluated(
            sd, mid, n_seeds=n_seeds, base_seed=base_seed, cache=cache,
            parallel=parallel, n_jobs=n_jobs, detail_path=detail_path, progress=progress,
        )
        record(mid, ev_mid)
        h_mid = ev_mid.h_sort_sim_mean
        print(
            f"  season {sd.season}: bisect [{lo:.4f},{hi:.4f}] mid={mid:.4f} "
            f"H_sim={h_mid:.4f} target={target:.4f}",
            flush=True,
        )
        if h_mid < target:
            lo, h_lo = mid, h_mid
        else:
            hi, h_hi = mid, h_mid

    rho_star = 0.5 * (lo + hi)
    ev_star = cache.eval_at(sd.season, rho_star)
    if ev_star is None or ev_star.n_seeds < n_seeds:
        ev_star = ensure_rho_evaluated(
            sd, rho_star, n_seeds=n_seeds, base_seed=base_seed, cache=cache,
            parallel=parallel, n_jobs=n_jobs, detail_path=detail_path, progress=progress,
        )
        record(rho_star, ev_star)
    return rho_star, ev_star.h_sort_sim_mean, trace


def run_bracket_search(
    seasons: list[SeasonData],
    *,
    n_seeds: int,
    base_seed: int,
    parallel: str,
    n_jobs: int,
    detail_path: Path,
    rho_max: float,
    rho_tol: float,
    max_expansions: int,
    max_bisect: int,
    eval_reference_rho: bool,
    progress: RunProgress | None = None,
    reference_rho: float = DEFAULT_RHO_REF,
) -> tuple[list[dict], list[dict]]:
    cache = DetailCache(detail_path)
    per_season_fit: list[dict] = []
    bracket_trace: list[dict] = []

    if progress is None:
        progress = RunProgress(
            n_seasons=len(seasons),
            n_seeds=int(n_seeds),
            eval_reference_rho=bool(eval_reference_rho),
        )

    for sd in seasons:
        jobs_at_start = progress.jobs_completed
        print(f"\nBracket season {sd.season} (H_sort_emp={sd.h_sort_empirical:.4f}) ...", flush=True)
        rho_star, h_sim, trace = bracket_rho_for_season(
            sd,
            n_seeds=n_seeds,
            base_seed=base_seed,
            cache=cache,
            parallel=parallel,
            n_jobs=n_jobs,
            detail_path=detail_path,
            rho_max=rho_max,
            rho_tol=rho_tol,
            max_expansions=max_expansions,
            max_bisect=max_bisect,
            progress=progress,
        )
        progress.season_done(progress.jobs_completed - jobs_at_start)
        best_err = abs(h_sim - sd.h_sort_empirical)
        per_season_fit.append(
            {
                "season": sd.season,
                "rho_star": normalize_rho(rho_star),
                "h_sort_empirical": sd.h_sort_empirical,
                "h_sort_sim_at_star": float(h_sim),
                "h_sort_abs_err": float(best_err),
                "n_seeds": int(n_seeds),
            }
        )
        bracket_trace.extend(trace)
        print(
            f"  => rho*={rho_star:.4f} H_sim={h_sim:.4f} |err|={best_err:.4f}",
            flush=True,
        )

    if eval_reference_rho:
        progress.start_reference_phase()
        print(f"\nReference eval rho={reference_rho:g} ...", flush=True)
        for sd in seasons:
            ensure_rho_evaluated(
                sd,
                float(reference_rho),
                n_seeds=n_seeds,
                base_seed=base_seed,
                cache=cache,
                parallel=parallel,
                n_jobs=n_jobs,
                detail_path=detail_path,
                progress=progress,
            )
            progress.reference_season_done()

    progress._report(force=True)
    return per_season_fit, bracket_trace


@dataclass(frozen=True)
class SeasonData:
    season: int
    ability: np.ndarray
    roster_caps: np.ndarray
    h_sort_empirical: float
    n_players: int
    n_teams: int


@dataclass(frozen=True)
class SimJob:
    season: int
    rho: float
    seed: int


def _output_paths(season_min: int, season_max: int) -> dict:
    tag = window_tag(season_min, season_max) if season_min != season_max else str(season_min)
    stem = f"PD21_rho_hsort_calibrate_{tag}"
    return {
        "detail_jsonl": OUT / f"{stem}_detail.jsonl",
        "summary_csv": OUT / f"{stem}_summary.csv",
        "fit_json": OUT / f"{stem}_fit.json",
        "png": OUT / f"{stem}.png",
        "season_min": season_min,
        "season_max": season_max,
        "seasons": seasons_label(season_min, season_max),
    }


def _load_gc():
    return importlib.import_module("541_grandchild_homophily_assign")


def empirical_h_sort(panel_season: pd.DataFrame) -> float:
    gc = _load_gc()
    work = panel_season.dropna(subset=["perf", "team_id"]).copy()
    work["perf"] = pd.to_numeric(work["perf"], errors="coerce")
    work = work.dropna(subset=["perf"])
    ability = work["perf"].to_numpy(dtype=float)
    pool_id = work.groupby("team_id", observed=True).ngroup().to_numpy(dtype=np.int64)
    return float(gc.realized_sorting_index_H_sort(ability, pool_id))


def load_season_data(season: int) -> SeasonData:
    gc = _load_gc()
    ability, caps, meta = gc.load_empirical_roster_caps_season(int(season), repo_root=REPO)
    from empirical_team_interval_overlap import _prepare_panel

    panel = _prepare_panel()
    sub = panel.loc[panel["season"] == int(season)]
    h_emp = empirical_h_sort(sub)
    return SeasonData(
        season=int(season),
        ability=np.asarray(ability, dtype=float),
        roster_caps=np.asarray(caps, dtype=np.int64),
        h_sort_empirical=h_emp,
        n_players=int(meta["n_players"]),
        n_teams=int(meta["n_teams_empirical"]),
    )


def _run_one_sim(job: SimJob, ability: np.ndarray, caps: np.ndarray) -> dict:
    gc = _load_gc()
    rng = np.random.default_rng(int(job.seed))
    res = gc.run_one_realization(
        ability,
        None,
        float(job.rho),
        roster_caps=caps,
        rng=rng,
        seed=int(job.seed),
    )
    return {
        "season": int(job.season),
        "rho": float(job.rho),
        "seed": int(job.seed),
        "h_sort_sim": float(res.sorting_index_h),
        "global_wss_sim": float(res.global_wss),
        "within_team_mse_sim": float(res.within_team_mse),
    }


def _worker_run(job_dict: dict, ability: np.ndarray, caps: np.ndarray) -> dict:
    job = SimJob(**job_dict)
    return _run_one_sim(job, ability, caps)


def _append_jsonl(path: Path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
        f.flush()


def _load_done_keys(path: Path) -> set[tuple[int, float, int]]:
    done: set[tuple[int, float, int]] = set()
    if not path.exists():
        return done
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            done.add(
                (int(rec["season"]), normalize_rho(float(rec["rho"])), int(rec["seed"]))
            )
    return done


def build_jobs(
    seasons: list[SeasonData],
    rho_grid: np.ndarray,
    n_seeds: int,
    base_seed: int,
    *,
    done: set[tuple[int, float, int]],
) -> list[tuple[SimJob, np.ndarray, np.ndarray]]:
    jobs: list[tuple[SimJob, np.ndarray, np.ndarray]] = []
    for sd in seasons:
        for rho in rho_grid:
            for rep in range(int(n_seeds)):
                rho_n = normalize_rho(float(rho))
                seed = int(base_seed + sd.season * 10_000 + rep + _rho_seed_tag(rho_n))
                key = (sd.season, rho_n, seed)
                if key in done:
                    continue
                job = SimJob(season=sd.season, rho=float(rho), seed=seed)
                jobs.append((job, sd.ability, sd.roster_caps))
    return jobs


def run_parallel_process(
    jobs: list[tuple[SimJob, np.ndarray, np.ndarray]],
    *,
    n_jobs: int,
    detail_path: Path,
    progress: RunProgress | None = None,
) -> int:
    if not jobs:
        return 0
    n_workers = max(1, int(n_jobs))
    completed = 0
    t0 = time.perf_counter()
    report_every = max(1, min(50, len(jobs) // 10 or 1))
    with ProcessPoolExecutor(max_workers=n_workers) as pool:
        futures = {
            pool.submit(_worker_run, {"season": j.season, "rho": j.rho, "seed": j.seed}, a, c): j
            for j, a, c in jobs
        }
        for fut in as_completed(futures):
            rec = fut.result()
            _append_jsonl(detail_path, rec)
            completed += 1
            if progress is not None:
                progress.tick(1)
            if completed % report_every == 0 or completed == len(jobs):
                _print_batch_progress(completed, len(jobs), t0, progress=progress)
    return completed


def run_parallel_ray(
    jobs: list[tuple[SimJob, np.ndarray, np.ndarray]],
    *,
    n_jobs: int,
    detail_path: Path,
    progress: RunProgress | None = None,
) -> int:
    try:
        import ray
    except ImportError as exc:
        raise SystemExit("Ray not installed. Use --parallel process or pip install ray.") from exc

    if not ray.is_initialized():
        ray.init(num_cpus=max(1, int(n_jobs)), ignore_reinit_error=True)

    @ray.remote
    def _ray_run(job_dict: dict, ability: np.ndarray, caps: np.ndarray) -> dict:
        return _worker_run(job_dict, ability, caps)

    completed = 0
    t0 = time.perf_counter()
    pending = [
        _ray_run.remote({"season": j.season, "rho": j.rho, "seed": j.seed}, a, c)
        for j, a, c in jobs
    ]
    while pending:
        done, pending = ray.wait(pending, num_returns=min(50, len(pending)))
        for ref in done:
            rec = ray.get(ref)
            _append_jsonl(detail_path, rec)
            completed += 1
            if progress is not None:
                progress.tick(1)
        _print_batch_progress(completed, len(jobs), t0, progress=progress)
    return completed


def summarize_detail(detail_path: Path) -> pd.DataFrame:
    rows: list[dict] = []
    with detail_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    summary = (
        df.groupby(["season", "rho"], as_index=False)
        .agg(
            n_seeds=("seed", "count"),
            h_sort_sim_mean=("h_sort_sim", "mean"),
            h_sort_sim_std=("h_sort_sim", "std"),
            global_wss_sim_mean=("global_wss_sim", "mean"),
        )
        .sort_values(["season", "rho"])
    )
    return summary


def attach_empirical(summary: pd.DataFrame, seasons: list[SeasonData]) -> pd.DataFrame:
    emp_map = {sd.season: sd.h_sort_empirical for sd in seasons}
    out = summary.copy()
    out["h_sort_empirical"] = out["season"].map(emp_map)
    out["h_sort_abs_err"] = (out["h_sort_sim_mean"] - out["h_sort_empirical"]).abs()
    return out


def pick_rho_per_season(summary: pd.DataFrame) -> pd.DataFrame:
    idx = summary.groupby("season")["h_sort_abs_err"].idxmin()
    best = summary.loc[idx].copy()
    best["rho_star"] = best["rho"].map(normalize_rho)
    best = best.rename(columns={"h_sort_sim_mean": "h_sort_sim_at_star"})
    return best[
        [
            "season",
            "rho_star",
            "h_sort_empirical",
            "h_sort_sim_at_star",
            "h_sort_abs_err",
            "n_seeds",
        ]
    ].sort_values("season")


def pick_rho_longitudinal(summary: pd.DataFrame, *, reference_rho: float = DEFAULT_RHO_REF) -> dict:
    long_rows: list[dict] = []
    summary = summary.copy()
    summary["rho_norm"] = summary["rho"].map(normalize_rho)
    for rho, sub in summary.groupby("rho_norm", sort=True):
        long_rows.append(
            {
                "rho": normalize_rho(rho),
                "mean_abs_err": float(sub["h_sort_abs_err"].mean()),
                "max_abs_err": float(sub["h_sort_abs_err"].max()),
                "h_sort_sim_mean_over_seasons": float(sub["h_sort_sim_mean"].mean()),
            }
        )
    if not long_rows:
        raise ValueError("No rho values in summary for longitudinal pick.")
    long_df = pd.DataFrame(long_rows).sort_values("mean_abs_err")
    best = long_df.iloc[0].to_dict()
    ref = summary.loc[np.isclose(summary["rho"], float(reference_rho))]
    ref_err = float(ref["h_sort_abs_err"].mean()) if not ref.empty else float("nan")
    h_emp_mean = float(summary.groupby("season")["h_sort_empirical"].first().mean())
    return {
        "rho_star_longitudinal": normalize_rho(best["rho"]),
        "h_sort_sim_mean_at_star": float(best["h_sort_sim_mean_over_seasons"]),
        "h_sort_empirical_mean_over_seasons": h_emp_mean,
        "mean_abs_err_at_star": float(best["mean_abs_err"]),
        "max_abs_err_at_star": float(best["max_abs_err"]),
        "reference_rho": float(reference_rho),
        "mean_abs_err_at_reference_rho": ref_err,
        "curve": long_rows,
    }


def reference_at_rho(summary: pd.DataFrame, rho: float) -> pd.DataFrame:
    sub = summary.loc[np.isclose(summary["rho"], float(rho))].copy()
    return sub.sort_values("season")


def _plot_x_hi(
    sub: pd.DataFrame,
    *,
    reference_rho: float,
    plot_xmax: float | None,
) -> float:
    if plot_xmax is not None:
        return float(plot_xmax)
    bracket = sub.loc[~np.isclose(sub["rho"], float(reference_rho)), "rho"]
    if bracket.empty:
        return 0.1
    return max(float(bracket.max()) * 1.15, 0.05)


def _plot_one_season_ax(
    ax: plt.Axes,
    sub: pd.DataFrame,
    *,
    season: int,
    rho_star: float | None,
    show_ylabel: bool,
    reference_rho: float = DEFAULT_RHO_REF,
    plot_xmax: float | None = None,
) -> None:
    h_emp = float(sub["h_sort_empirical"].iloc[0])
    ax.errorbar(
        sub["rho"],
        sub["h_sort_sim_mean"],
        yerr=sub["h_sort_sim_std"].fillna(0.0),
        fmt="o-",
        capsize=2,
        ms=4,
        lw=1.2,
        color="#1a5490",
        label=r"Sim mean $H_{\mathrm{sort}}$",
    )
    ax.axhline(
        h_emp,
        color="#b03030",
        ls="--",
        lw=1.2,
        label=rf"Empirical $H_{{\mathrm{{sort}}}}={h_emp:.3f}$",
    )
    if rho_star is not None:
        ax.axvline(
            float(rho_star),
            color="#2d6a4f",
            ls=":",
            lw=1.2,
            alpha=0.9,
            label=rf"$\rho^*={float(rho_star):g}$",
        )
    ax.set_title(str(season), fontsize=10)
    ax.set_xlabel(r"Homophily $\rho$")
    if show_ylabel:
        ax.set_ylabel(r"Sorting index $H_{\mathrm{sort}}$")
    ax.set_xlim(
        -0.005,
        _plot_x_hi(sub, reference_rho=reference_rho, plot_xmax=plot_xmax),
    )
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=8, loc="upper left", framealpha=0.92)


def _longitudinal_title_suffix(fit: dict) -> str:
    """Title line: longitudinal rho* and matching interval H_sort means."""
    long = fit.get("longitudinal", {})
    rho = float(long.get("rho_star_longitudinal", float("nan")))
    h_sim = long.get("h_sort_sim_mean_at_star")
    h_emp = long.get("h_sort_empirical_mean_over_seasons")
    if h_sim is None:
        for row in long.get("curve", []):
            if np.isclose(float(row["rho"]), rho):
                h_sim = row.get("h_sort_sim_mean_over_seasons")
                break
    if h_emp is None and fit.get("empirical_targets"):
        h_emp = float(
            np.mean([float(t["h_sort_empirical"]) for t in fit["empirical_targets"]])
        )
    if h_sim is not None and h_emp is not None:
        return (
            rf"longitudinal $\rho^*={rho:.3g}$, "
            rf"$\overline{{H}}_{{\mathrm{{sort}}}}^{{\mathrm{{sim}}}}={float(h_sim):.3f}$, "
            rf"$\overline{{H}}_{{\mathrm{{sort}}}}^{{\mathrm{{emp}}}}={float(h_emp):.3f}$"
        )
    return rf"longitudinal $\rho^*={rho:.3g}$"


def _plot_calibration(
    summary: pd.DataFrame,
    seasons: list[SeasonData],
    per_season: pd.DataFrame,
    fit: dict,
    out_path: Path,
    *,
    reference_rho: float = DEFAULT_RHO_REF,
    plot_xmax: float | None = None,
) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    season_list = sorted(summary["season"].unique())
    n = len(season_list)
    title_suffix = _longitudinal_title_suffix(fit)
    star_map = {
        int(row["season"]): float(row["rho_star"])
        for row in per_season.to_dict(orient="records")
    }

    if n == 1:
        fig, ax = plt.subplots(figsize=(7.0, 4.5))
        season = int(season_list[0])
        sub = summary.loc[summary["season"] == season].sort_values("rho")
        _plot_one_season_ax(
            ax,
            sub,
            season=season,
            rho_star=star_map.get(season),
            show_ylabel=True,
            reference_rho=reference_rho,
            plot_xmax=plot_xmax,
        )
        fig.suptitle(
            rf"PD21 $\rho$ calibration — season {season} ({title_suffix})",
            fontsize=12,
            y=0.98,
        )
        fig.tight_layout(rect=(0, 0, 1, 0.94))
    else:
        ncols = 4
        nrows = int(np.ceil(n / ncols))
        fig, axes = plt.subplots(nrows, ncols, figsize=(4.0 * ncols, 3.4 * nrows), squeeze=False)
        for idx, (ax, season) in enumerate(zip(axes.ravel(), season_list)):
            sub = summary.loc[summary["season"] == int(season)].sort_values("rho")
            _plot_one_season_ax(
                ax,
                sub,
                season=int(season),
                rho_star=star_map.get(int(season)),
                show_ylabel=(idx % ncols == 0),
                reference_rho=reference_rho,
                plot_xmax=plot_xmax,
            )
        for ax in axes.ravel()[n:]:
            ax.axis("off")
        fig.suptitle(
            rf"PD21 $\rho$ calibration — simulated vs empirical $H_{{\mathrm{{sort}}}}$ "
            rf"({title_suffix})",
            fontsize=12,
            y=1.01,
        )
        fig.tight_layout(rect=(0, 0, 1, 0.97))

    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="PD21 rho H_sort calibration.")
    parser.add_argument("--season-min", type=int, default=FULL_PANEL_SEASON_MIN)
    parser.add_argument("--season-max", type=int, default=FULL_PANEL_SEASON_MAX)
    parser.add_argument("--n-seeds", type=int, default=50)
    parser.add_argument("--base-seed", type=int, default=BASE_SEED)
    parser.add_argument("--n-jobs", type=int, default=1, help="Worker count (process or Ray CPUs)")
    parser.add_argument(
        "--method",
        choices=("bracket", "grid"),
        default="bracket",
        help="bracket = expand+bisect (default); grid = uniform rho sweep",
    )
    parser.add_argument(
        "--parallel",
        choices=("process", "ray"),
        default="process",
        help="Parallel backend (default: process = stdlib ProcessPool)",
    )
    parser.add_argument("--rho-min", type=float, default=0.0)
    parser.add_argument("--rho-max", type=float, default=0.5, help="Bracket expansion cap / grid upper rho")
    parser.add_argument("--rho-steps", type=int, default=26)
    parser.add_argument(
        "--bracket-tol",
        type=float,
        default=0.001,
        help="Stop bisect when bracket width <= tol",
    )
    parser.add_argument("--bracket-max-expansions", type=int, default=8)
    parser.add_argument("--bracket-max-bisect", type=int, default=12)
    parser.add_argument(
        "--progress-interval",
        type=float,
        default=30.0,
        help="Seconds between global progress + ETA lines (default 30)",
    )
    parser.add_argument(
        "--no-reference-rho",
        action="store_true",
        help="Skip extra reference-rho eval (bracket mode)",
    )
    parser.add_argument(
        "--reference-rho",
        type=float,
        default=DEFAULT_RHO_REF,
        help="Optional reference rho eval for legacy comparison (default 0.5)",
    )
    parser.add_argument(
        "--plot-xmax",
        type=float,
        default=None,
        help="Fix plot x-axis upper limit (e.g. 0.1). Default: zoom to bracket evals, exclude reference.",
    )
    parser.add_argument(
        "--plot-only",
        action="store_true",
        help="Regenerate PNG from existing *_bracket.csv / *_bracket.json (no simulation)",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="bracket: 2015 only, 8 seeds; grid: 3 rho, 4 seeds, 2015 only",
    )
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Ignore existing detail JSONL checkpoint",
    )
    args = parser.parse_args()

    ensure_hero_dirs()
    method = str(args.method)
    if args.quick:
        season_min, season_max = 2015, 2015
        n_seeds = 8 if method == "bracket" else 4
        rho_grid = np.array([0.0, 0.5, 1.5]) if method == "grid" else None
        rho_max = 0.5
    else:
        season_min, season_max = args.season_min, args.season_max
        n_seeds = int(args.n_seeds)
        rho_grid = np.linspace(float(args.rho_min), float(args.rho_max), int(args.rho_steps))
        rho_max = float(args.rho_max)

    paths = _output_paths(season_min, season_max)
    if method == "bracket":
        paths = {
            **paths,
            "detail_jsonl": paths["detail_jsonl"].with_name(
                paths["detail_jsonl"].stem + "_bracket.jsonl"
            ),
            "summary_csv": paths["summary_csv"].with_name(
                paths["summary_csv"].stem + "_bracket.csv"
            ),
            "fit_json": paths["fit_json"].with_name(paths["fit_json"].stem + "_bracket.json"),
            "png": paths["png"].with_name(paths["png"].stem + "_bracket.png"),
        }

    if args.fresh and paths["detail_jsonl"].exists():
        paths["detail_jsonl"].unlink()

    reference_rho = float(args.reference_rho)

    if args.plot_only:
        if not paths["summary_csv"].exists() or not paths["fit_json"].exists():
            raise SystemExit(f"Missing {paths['summary_csv']} or {paths['fit_json']} for --plot-only")
        summary = pd.read_csv(paths["summary_csv"])
        fit = json.loads(paths["fit_json"].read_text(encoding="utf-8"))
        per_season = pd.DataFrame(fit["per_season"])
        ref_rho = float(fit.get("longitudinal", {}).get("reference_rho", reference_rho))
        _plot_calibration(
            summary,
            [],
            per_season,
            fit,
            paths["png"],
            reference_rho=ref_rho,
            plot_xmax=args.plot_xmax,
        )
        print(f"Wrote {paths['png']}")
        return

    print(f"Loading empirical targets {paths['seasons']} ...", flush=True)
    seasons: list[SeasonData] = []
    for season in range(int(season_min), int(season_max) + 1):
        sd = load_season_data(season)
        seasons.append(sd)
        print(
            f"  {season}: N={sd.n_players} J={sd.n_teams} "
            f"H_sort_emp={sd.h_sort_empirical:.4f}",
            flush=True,
        )

    bracket_trace: list[dict] = []
    t0 = time.perf_counter()

    if method == "bracket":
        print(
            f"Method: bracket  rho_max={rho_max:g}  tol={args.bracket_tol:g}  "
            f"seeds={n_seeds}",
            flush=True,
        )
        print(f"Parallel: {args.parallel}  n_jobs={args.n_jobs}", flush=True)
        run_progress = RunProgress(
            n_seasons=len(seasons),
            n_seeds=int(n_seeds),
            eval_reference_rho=not args.no_reference_rho,
            report_interval_s=float(args.progress_interval),
        )
        est = run_progress.estimate_total_jobs()
        print(
            f"Estimated workload: ~{est} sim jobs (adaptive bracket; refines after each season)",
            flush=True,
        )
        per_season_records, bracket_trace = run_bracket_search(
            seasons,
            n_seeds=n_seeds,
            base_seed=args.base_seed,
            parallel=args.parallel,
            n_jobs=args.n_jobs,
            detail_path=paths["detail_jsonl"],
            rho_max=rho_max,
            rho_tol=float(args.bracket_tol),
            max_expansions=int(args.bracket_max_expansions),
            max_bisect=int(args.bracket_max_bisect),
            eval_reference_rho=not args.no_reference_rho,
            progress=run_progress,
            reference_rho=reference_rho,
        )
        per_season = pd.DataFrame(per_season_records)
        print(f"Bracket search finished in {time.perf_counter() - t0:.1f}s", flush=True)
    else:
        done = _load_done_keys(paths["detail_jsonl"])
        jobs = build_jobs(seasons, rho_grid, n_seeds, args.base_seed, done=done)
        total = len(jobs) + len(done)
        print(
            f"Method: grid  {len(rho_grid)} rho × {n_seeds} seeds × {len(seasons)} seasons "
            f"= {total} jobs ({len(done)} already done, {len(jobs)} to run)",
            flush=True,
        )
        print(f"Parallel: {args.parallel}  n_jobs={args.n_jobs}", flush=True)
        if jobs:
            if args.parallel == "ray":
                run_parallel_ray(jobs, n_jobs=args.n_jobs, detail_path=paths["detail_jsonl"])
            else:
                run_parallel_process(jobs, n_jobs=args.n_jobs, detail_path=paths["detail_jsonl"])
            print(f"Grid sweep finished in {time.perf_counter() - t0:.1f}s", flush=True)

    summary = attach_empirical(summarize_detail(paths["detail_jsonl"]), seasons)
    if summary.empty:
        raise SystemExit("No simulation rows — run failed or detail JSONL empty.")
    summary.to_csv(paths["summary_csv"], index=False)

    if method == "grid":
        per_season = pick_rho_per_season(summary)
    longitudinal = pick_rho_longitudinal(summary, reference_rho=reference_rho)
    ref_df = reference_at_rho(summary, reference_rho)

    fit = {
        "generated": date.today().isoformat(),
        "script": "sports/scripts/pd21_rho_hsort_calibrate.py",
        "method": method,
        "season_min": int(season_min),
        "season_max": int(season_max),
        "seasons": paths["seasons"],
        "n_seeds": int(n_seeds),
        "rho_grid": [float(x) for x in sorted(summary["rho"].unique())],
        "bracket": {
            "rho_max": rho_max if method == "bracket" else None,
            "tol": float(args.bracket_tol) if method == "bracket" else None,
            "trace": bracket_trace if method == "bracket" else None,
        },
        "parallel": args.parallel,
        "n_jobs": int(args.n_jobs),
        "empirical_targets": [
            {"season": sd.season, "h_sort_empirical": sd.h_sort_empirical, "n_players": sd.n_players}
            for sd in seasons
        ],
        "per_season": per_season.to_dict(orient="records"),
        "longitudinal": longitudinal,
        "reference_rho_0p5": ref_df.to_dict(orient="records"),
    }
    paths["fit_json"].write_text(json.dumps(fit, indent=2), encoding="utf-8")
    _plot_calibration(
        summary,
        seasons,
        per_season,
        fit,
        paths["png"],
        reference_rho=reference_rho,
        plot_xmax=args.plot_xmax,
    )

    print(
        f"\nLongitudinal rho* = {longitudinal['rho_star_longitudinal']:.4g} "
        f"(mean |error| = {longitudinal['mean_abs_err_at_star']:.4f})"
    )
    print(
        f"  at rho*: mean H_sort^sim = {longitudinal['h_sort_sim_mean_at_star']:.4f}, "
        f"mean H_sort^emp = {longitudinal['h_sort_empirical_mean_over_seasons']:.4f}"
    )
    print(f"Reference rho={reference_rho:g} mean |error| = {longitudinal['mean_abs_err_at_reference_rho']:.4f}")
    print("\nPer-season rho*:")
    print(per_season.to_string(index=False))
    print(f"\nWrote {paths['detail_jsonl']}")
    print(f"Wrote {paths['summary_csv']}")
    print(f"Wrote {paths['fit_json']}")
    print(f"Wrote {paths['png']}")


if __name__ == "__main__":
    main()
