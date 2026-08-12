"""Progress reporting for long season-loop diagnostics."""

from __future__ import annotations

import time


class SeasonProgress:
    """Tick once per season with elapsed time and ETA."""

    def __init__(self, label: str, season_min: int, season_max: int) -> None:
        self.label = label
        self.seasons = list(range(int(season_min), int(season_max) + 1))
        self.n = len(self.seasons)
        self.done = 0
        self.t0 = time.perf_counter()

    def header(self) -> None:
        print(f"{self.label}: {self.n} seasons", flush=True)

    def tick(self, season: int, detail: str) -> None:
        self.done += 1
        elapsed = time.perf_counter() - self.t0
        pct = 100 * self.done / self.n if self.n else 100.0
        eta = (self.n - self.done) * (elapsed / self.done) if self.done < self.n else 0.0
        eta_s = f", ~{eta:.0f}s left" if self.done < self.n else ""
        print(
            f"  [{self.done}/{self.n}] season {season} ({pct:.0f}%) | {detail} | "
            f"{elapsed:.0f}s elapsed{eta_s}",
            flush=True,
        )

    def finish(self) -> None:
        elapsed = time.perf_counter() - self.t0
        print(f"{self.label} finished in {elapsed:.1f}s.", flush=True)


class StepProgress:
    """Coarse progress for outer loops (e.g. C sweep arms)."""

    def __init__(self, label: str, steps: list) -> None:
        self.label = label
        self.steps = list(steps)
        self.n = len(self.steps)
        self.done = 0
        self.t0 = time.perf_counter()

    def header(self) -> None:
        print(f"{self.label}: {self.n} steps", flush=True)

    def begin(self, step) -> None:
        self.done += 1
        elapsed = time.perf_counter() - self.t0
        print(
            f"\n=== {self.label} step {self.done}/{self.n}: {step} ({elapsed:.0f}s elapsed) ===",
            flush=True,
        )

    def finish(self) -> None:
        elapsed = time.perf_counter() - self.t0
        print(f"{self.label} finished in {elapsed:.1f}s.", flush=True)
