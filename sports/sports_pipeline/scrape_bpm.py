"""
Sports-Reference CBB **advanced** team-season scrape → ``bpm_player_season_raw.csv``.

Pulls the same HTML table as ``obsolete_files/sports_gameplan_old/scrape_bpm_bkup.ipynb``:
**BPM, OBPM, DBPM** (when SR publishes them) plus PER / WS columns on men’s pages:

``https://www.sports-reference.com/cbb/schools/{slug}/men/{sr_year}.html``

**Etiquette:** throttle (~20 GETs/min sliding window + jitter), set a real **User-Agent**
with contact via ``PipelineConfig.sr_scrape_contact`` or ``ScrapeBpmConfig.user_agent``.
Respect https://www.sports-reference.com/robots.txt .

**Batch inputs:** ``datasets/mbb/bpm_scrape_jobs.csv`` (columns ``school_slug``, ``sr_year``),
from the merge notebook. **Resume:** skips (slug, year) already present in the raw CSV.
**403:** pairs append to ``bpm_scrape_skip_pairs.csv`` and are skipped later.

**Dependencies:** ``pip install -e '.[scrape]'`` (requests, beautifulsoup4, lxml; tqdm optional).
"""

from __future__ import annotations

import csv
import io
import random
import re
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Callable

import pandas as pd

from sports_pipeline import paths

# ---------------------------------------------------------------------------
# Optional SR slug fixes (panel slug → SR URL segment). CSV overrides + extends this.
# ---------------------------------------------------------------------------
SR_SCHOOL_SLUG_ALIASES: dict[str, str] = {
    "alabama-aandm": "alabama-am",
    "alabama-st": "alabama-state",
    "albany": "albany-ny",
    "alcorn-st": "alcorn-state",
    "appalachian-st": "appalachian-state",
    "ar-pine-bluff": "arkansas-pine-bluff",
    "arizona-st": "arizona-state",
    "arkansas-st": "arkansas-state",
    "bethune": "bethune-cookman",
    "birm-southern": "birmingham-southern",
    "boise-st": "boise-state",
    "boston-univ": "boston-university",
    "bowling-green": "bowling-green-state",
    "byu": "brigham-young",
    "c-connecticut": "central-connecticut-state",
    "c-michigan": "central-michigan",
    "charleston": "college-of-charleston",
    "charleston-so": "charleston-southern",
}

BASE = "https://www.sports-reference.com"
ADVANCED_TABLE_IDS = ("players_advanced", "advanced")
STATS_TABLE_CLASS = "stats_table"

_slug_alias_cache: dict[str, str] | None = None


def _require_scrape_deps() -> tuple[Any, Any]:
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError as e:
        raise ImportError(
            "SR BPM scrape needs requests + beautifulsoup4 + lxml. "
            "Install: pip install -e '.[scrape]'"
        ) from e
    return requests, BeautifulSoup


def _aliases_csv_path() -> Path:
    return paths.sr_school_slug_aliases_csv()


def _nonempty_slug_map(d: dict[str, str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for k, v in d.items():
        ks = str(k).strip()
        vs = "" if v is None else str(v).strip()
        if ks and vs:
            out[ks] = vs
    return out


def build_sr_slug_alias_map() -> dict[str, str]:
    m: dict[str, str] = {}
    p = _aliases_csv_path()
    if p.is_file():
        adf = pd.read_csv(p, dtype=str, keep_default_na=False)
        if "panel_slug" not in adf.columns:
            raise ValueError(f"{p} must have column panel_slug; got {list(adf.columns)}")
        if "sr_slug" not in adf.columns:
            adf["sr_slug"] = ""
        for _, row in adf.iterrows():
            pk = str(row["panel_slug"]).strip()
            sv = str(row["sr_slug"]).strip()
            if pk and sv:
                m[pk] = sv
    m.update(_nonempty_slug_map(SR_SCHOOL_SLUG_ALIASES))
    return m


def refresh_sr_slug_alias_cache() -> None:
    global _slug_alias_cache
    _slug_alias_cache = build_sr_slug_alias_map()


def resolve_sr_school_slug(panel_slug: str) -> str:
    global _slug_alias_cache
    if _slug_alias_cache is None:
        refresh_sr_slug_alias_cache()
    s = str(panel_slug).strip()
    return _slug_alias_cache.get(s, s)  # type: ignore[union-attr]


def team_men_season_url(school_slug: str, sr_year: int) -> str:
    sr_slug = resolve_sr_school_slug(school_slug)
    return f"{BASE}/cbb/schools/{sr_slug}/men/{int(sr_year)}.html"


def sr_year_from_box_season(box_season: int) -> int:
    """Identity default: SR URL year label matches ``mbb_df_player_box`` ``season``."""
    return int(box_season)


@dataclass
class ScrapeBpmConfig:
    """Knobs for ``run_batch`` (defaults match the legacy ``scrape_bpm`` notebook)."""

    jobs_csv: Path = field(default_factory=paths.bpm_scrape_jobs_csv)
    out_raw_csv: Path = field(default_factory=paths.bpm_raw_csv)
    skip_pairs_csv: Path = field(default_factory=paths.bpm_scrape_skip_pairs_csv)
    aliases_csv: Path = field(default_factory=_aliases_csv_path)
    #: ~20 GETs / minute sliding window; set to 0 to disable window (spacing only).
    sr_max_requests_per_minute: int = 20
    sr_rate_window_sec: float = 60.0
    request_delay_jitter_sec: float = 0.75
    http_throttle_max_retries: int = 6
    http_throttle_base_backoff_sec: float = 20.0
    raw_flush_every_n_ok: int = 1
    resume_skip_scraped: bool = True
    max_fetches_per_run: int | None = None
    force_demo_slugs: bool = False
    #: Full User-Agent header; if None, built from ``default_user_agent_contact``.
    user_agent: str | None = None
    default_user_agent_contact: str = "set PipelineConfig.sr_scrape_contact"


class _ScrapeRuntime:
    def __init__(self, cfg: ScrapeBpmConfig, requests_mod: Any, headers: dict[str, str]):
        self.cfg = cfg
        self.requests = requests_mod
        self._req_times: deque[float] = deque()
        self._last_wall: float | None = None
        self.session = requests_mod.Session()
        self.session.headers.update(headers)

    def _request_delay_sec(self) -> float:
        rpm = int(self.cfg.sr_max_requests_per_minute)
        if rpm <= 0:
            return 8.0
        return float(self.cfg.sr_rate_window_sec) / float(rpm)

    def pause_before_get(self) -> None:
        rpm = int(self.cfg.sr_max_requests_per_minute)
        win = float(self.cfg.sr_rate_window_sec)
        jit = float(self.cfg.request_delay_jitter_sec)

        def _prune(now: float) -> None:
            while self._req_times and self._req_times[0] <= now - win:
                self._req_times.popleft()

        if rpm <= 0:
            time.sleep(self._request_delay_sec() + (random.uniform(0.0, jit) if jit > 0 else 0.0))
            return

        now = time.time()
        _prune(now)
        while len(self._req_times) >= rpm:
            wait_until = self._req_times[0] + win
            sleep_for = max(0.0, wait_until - time.time())
            if sleep_for > 0:
                time.sleep(sleep_for)
            now = time.time()
            _prune(now)

        j = random.uniform(0.0, jit) if jit > 0 else 0.0
        min_gap = self._request_delay_sec() + j
        if self._last_wall is not None:
            gap_needed = min_gap - (time.time() - self._last_wall)
            if gap_needed > 0:
                time.sleep(gap_needed)
        now = time.time()
        _prune(now)
        while len(self._req_times) >= rpm:
            wait_until = self._req_times[0] + win
            sleep_for = max(0.0, wait_until - time.time())
            if sleep_for > 0:
                time.sleep(sleep_for)
            now = time.time()
            _prune(now)

    def register_sent(self) -> None:
        t = time.time()
        self._last_wall = t
        if int(self.cfg.sr_max_requests_per_minute) > 0:
            self._req_times.append(t)

    def _backoff_seconds(self, resp: Any, throttle_attempt: int) -> float:
        ra = resp.headers.get("Retry-After")
        if ra is not None:
            try:
                return max(float(ra), 1.0)
            except ValueError:
                pass
        return float(self.cfg.http_throttle_base_backoff_sec) * (2**throttle_attempt)

    def get(self, url: str) -> tuple[int, str]:
        """HTTP GET after rate limit; retries 429/503; returns ``(status_code, text)``."""
        throttle_attempt = 0
        while True:
            self.pause_before_get()
            self.register_sent()
            r = self.session.get(url, timeout=90)
            if r.status_code in (429, 503):
                if throttle_attempt >= int(self.cfg.http_throttle_max_retries):
                    return r.status_code, r.text
                wait = self._backoff_seconds(r, throttle_attempt)
                print(
                    f"  (throttle {r.status_code}: sleeping {wait:.1f}s, "
                    f"attempt {throttle_attempt + 1}/{self.cfg.http_throttle_max_retries})"
                )
                time.sleep(wait)
                throttle_attempt += 1
                continue
            return r.status_code, r.text


def _unwrap_sr_comments(html: str) -> str:
    return re.sub(r"<!--|-->", "", html)


def parse_advanced_player_table(html: str, BeautifulSoup: Callable[..., Any]) -> pd.DataFrame:
    soup = BeautifulSoup(html, "lxml")

    def _find_by_ids(s: Any) -> Any:
        for tid in ADVANCED_TABLE_IDS:
            n = s.find("table", id=tid)
            if n is not None:
                return n
        return None

    node = _find_by_ids(soup)
    if node is None:
        html2 = _unwrap_sr_comments(html)
        soup2 = BeautifulSoup(html2, "lxml")
        node = _find_by_ids(soup2)
        if node is None:
            soup = soup2
    if node is None:
        for t in soup.find_all("table", class_=STATS_TABLE_CLASS):
            txt = t.get_text(" ", strip=True)
            if "Player" not in txt:
                continue
            if "BPM" in txt or "WS/40" in txt or "Win Shares" in txt:
                node = t
                break
    if node is None:
        raise ValueError(
            "Advanced table not found. Inspect page for <table id=\"players_advanced\"> "
            "or extend parse_advanced_player_table fallbacks."
        )
    dfs = pd.read_html(io.StringIO(str(node)), flavor="lxml")
    return dfs[0]


def tidy_advanced_df(df: pd.DataFrame, school_slug: str, sr_year: int) -> pd.DataFrame:
    out = df.copy()
    if "Player" in out.columns:
        mask_totals = out["Player"].astype(str).str.contains("Team Totals", case=False, na=False)
        out = out.loc[~mask_totals]
    out.insert(0, "school_slug", school_slug)
    out["sr_year"] = int(sr_year)
    out["box_season"] = sr_year_from_box_season(int(sr_year))
    out["source_url"] = team_men_season_url(school_slug, sr_year)
    out["scrape_date"] = date.today().isoformat()
    return out


def _ensure_alias_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file():
        pd.DataFrame({"panel_slug": [], "sr_slug": []}).to_csv(path, index=False)


def _alias_panel_slugs_in_csv(path: Path) -> set[str]:
    if not path.is_file() or path.stat().st_size == 0:
        return set()
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    if "panel_slug" not in df.columns:
        return set()
    return set(df["panel_slug"].astype(str).str.strip())


def _append_404_panel_slug_now(path: Path, slug: str, seen: set[str]) -> None:
    s = str(slug).strip()
    if not s or s in seen:
        return
    seen.add(s)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([s, ""])


def _read_skip_pairs(path: Path) -> set[tuple[str, int]]:
    if not path.is_file() or path.stat().st_size == 0:
        return set()
    df = pd.read_csv(path, low_memory=False)
    if "school_slug" not in df.columns or "sr_year" not in df.columns:
        return set()
    df = df.dropna(subset=["school_slug", "sr_year"])
    df["sr_year"] = pd.to_numeric(df["sr_year"], errors="coerce")
    df = df.dropna(subset=["sr_year"])
    return {
        (str(a).strip(), int(y))
        for a, y in zip(df["school_slug"].astype(str), df["sr_year"].astype(int))
        if str(a).strip()
    }


def _append_skip_pair(path: Path, slug: str, year: int, seen: set[tuple[str, int]]) -> None:
    key = (str(slug).strip(), int(year))
    if not key[0] or key in seen:
        return
    seen.add(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not path.is_file() or path.stat().st_size == 0
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["school_slug", "sr_year"])
        w.writerow([key[0], key[1]])


def _read_out_raw_safe(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path, low_memory=False)
    except (pd.errors.ParserError, UnicodeDecodeError) as e:
        print("Warning: OUT_RAW parse error — on_bad_lines='skip'.", e)
        return pd.read_csv(path, on_bad_lines="skip", engine="python")


def _flush_raw_buffer(path: Path, buf: list[pd.DataFrame], write_header: bool) -> bool:
    if not buf:
        return write_header
    chunk = pd.concat(buf, ignore_index=True)
    if path.is_file() and path.stat().st_size > 0:
        existing = _read_out_raw_safe(path)
        all_cols = list(dict.fromkeys(list(existing.columns) + list(chunk.columns)))
        existing = existing.reindex(columns=all_cols)
        chunk = chunk.reindex(columns=all_cols)
        pd.concat([existing, chunk], ignore_index=True).to_csv(path, index=False)
    else:
        chunk.to_csv(path, mode="w", header=True, index=False)
    buf.clear()
    return False


def _dedupe_out_raw(path: Path) -> None:
    if not path.is_file() or path.stat().st_size == 0:
        return
    batch = _read_out_raw_safe(path)
    dedupe_cols = [c for c in ("school_slug", "sr_year", "Player") if c in batch.columns]
    if len(dedupe_cols) == 3:
        batch = batch.drop_duplicates(subset=dedupe_cols, keep="last")
    batch.to_csv(path, index=False)


def _load_job_pairs(cfg: ScrapeBpmConfig) -> pd.DataFrame:
    p = cfg.jobs_csv
    if p.is_file() and not cfg.force_demo_slugs:
        jobs = pd.read_csv(p, low_memory=False)
        for c in ("school_slug", "sr_year"):
            if c not in jobs.columns:
                raise ValueError(f"{p} must include columns school_slug, sr_year; got {list(jobs.columns)}")
        jobs = jobs.dropna(subset=["school_slug", "sr_year"]).copy()
        jobs["sr_year"] = pd.to_numeric(jobs["sr_year"], errors="coerce")
        jobs = jobs.dropna(subset=["sr_year"])
        jobs["school_slug"] = jobs["school_slug"].astype(str).str.strip()
        jobs = jobs[jobs["school_slug"].str.len() > 0]
        return (
            jobs[["school_slug", "sr_year"]]
            .drop_duplicates()
            .sort_values(["sr_year", "school_slug"], kind="mergesort")
            .reset_index(drop=True)
        )
    demo = pd.DataFrame(
        {
            "school_slug": [
                "duke",
                "north-carolina",
                "gonzaga",
                "virginia",
                "connecticut",
            ],
            "sr_year": 2024,
        }
    )
    print("No jobs CSV (or force_demo_slugs) — demo schools × single season.")
    return demo


def _headers_for_config(cfg: ScrapeBpmConfig) -> dict[str, str]:
    ua = cfg.user_agent
    if not ua:
        c = cfg.default_user_agent_contact.strip()
        ua = f"Dissertation-research/1.0 (contact: {c}; BPM scrape for academic use)"
    return {
        "User-Agent": ua,
        "Accept-Language": "en-US,en;q=0.9",
    }


def run_batch(
    scrape_cfg: ScrapeBpmConfig | None = None,
    *,
    pipeline_cfg: Any | None = None,
) -> dict[str, Any]:
    """
    Fetch team-season advanced tables and append to ``bpm_player_season_raw.csv``.

    If ``pipeline_cfg`` is passed, merges ``sr_scrape_contact`` and ``sr_scrape_max_fetches``
    when the scrape config leaves defaults.
    """
    requests_mod, BeautifulSoup = _require_scrape_deps()
    cfg = scrape_cfg or ScrapeBpmConfig()
    if pipeline_cfg is not None:
        contact = getattr(pipeline_cfg, "sr_scrape_contact", None)
        if contact and cfg.user_agent is None:
            cfg.default_user_agent_contact = str(contact)
        mx = getattr(pipeline_cfg, "sr_scrape_max_fetches", None)
        if mx is not None and cfg.max_fetches_per_run is None:
            cfg.max_fetches_per_run = int(mx)

    headers = _headers_for_config(cfg)
    pairs = _load_job_pairs(cfg)
    out_raw = Path(cfg.out_raw_csv)
    skip_path = Path(cfg.skip_pairs_csv)
    alias_path = Path(cfg.aliases_csv)

    if not cfg.resume_skip_scraped and out_raw.is_file():
        out_raw.unlink()
        print("resume_skip_scraped False — cleared", out_raw.name)

    _ensure_alias_csv(alias_path)
    alias_seen = _alias_panel_slugs_in_csv(alias_path)
    refresh_sr_slug_alias_cache()
    skip_seen = _read_skip_pairs(skip_path)

    have: set[tuple[str, int]] = set()
    if cfg.resume_skip_scraped and out_raw.is_file() and out_raw.stat().st_size > 0:
        ex = _read_out_raw_safe(out_raw)
        if "school_slug" in ex.columns and "sr_year" in ex.columns:
            sy = pd.to_numeric(ex["sr_year"], errors="coerce")
            for sl, y in zip(ex["school_slug"].astype(str).str.strip(), sy):
                if pd.notna(y):
                    have.add((sl, int(y)))
        print(f"Resume: {len(have)} team-seasons already in {out_raw.name}")

    def _row_key(r: pd.Series) -> tuple[str, int]:
        return (str(r["school_slug"]).strip(), int(r["sr_year"]))

    pending_mask = pairs.apply(
        lambda r: _row_key(r) not in have and _row_key(r) not in skip_seen,
        axis=1,
    )
    to_fetch_full = pairs.loc[pending_mask].reset_index(drop=True)
    n_total = len(pairs)
    n_done_at_start = n_total - len(to_fetch_full)
    to_fetch = to_fetch_full

    if cfg.max_fetches_per_run is not None:
        lim = int(cfg.max_fetches_per_run)
        if lim < 0:
            raise ValueError("max_fetches_per_run must be >= 0 or None")
        to_fetch = to_fetch.iloc[:lim].reset_index(drop=True)
        print(f"max_fetches_per_run={lim} — capped this run to {lim} page(s)")

    print(
        f"Job list: {n_total} unique slug×year | "
        f"in raw (resume): {len(have)} | skip_pairs: {len(skip_seen)} | "
        f"pending before cap: {len(to_fetch_full)} | this run: {len(to_fetch)}"
    )

    try:
        from tqdm.auto import tqdm as tqdm_bar
    except ImportError:
        tqdm_bar = None  # type: ignore[misc, assignment]

    rt = _ScrapeRuntime(cfg, requests_mod, headers)
    n_ok = 0
    n_fail = 0
    fail_404: set[str] = set()
    fail_other: list[tuple[str, int, str]] = []
    raw_buf: list[pd.DataFrame] = []
    raw_header = not (out_raw.is_file() and out_raw.stat().st_size > 0)
    interrupted = False

    pbar = None
    if tqdm_bar is not None and len(to_fetch) > 0:
        pbar = tqdm_bar(
            total=n_total,
            initial=min(n_done_at_start, n_total),
            desc="SR BPM scrape",
            dynamic_ncols=True,
            unit="page",
            mininterval=0.5,
        )
    elif tqdm_bar is None and len(to_fetch) > 0:
        print("(install tqdm for a progress bar)")

    t0 = time.time()
    try:
        try:
            for _, row in to_fetch.iterrows():
                slug = str(row["school_slug"]).strip()
                yr = int(row["sr_year"])
                url = team_men_season_url(slug, yr)
                try:
                    code, text = rt.get(url)
                    if code == 403:
                        n_fail += 1
                        _append_skip_pair(skip_path, slug, yr, skip_seen)
                        print(f"FAIL {slug} {yr}: HTTP 403 (logged to {skip_path.name})")
                    elif code == 404:
                        n_fail += 1
                        fail_404.add(slug)
                        _append_404_panel_slug_now(alias_path, slug, alias_seen)
                        print(f"FAIL {slug} {yr}: HTTP 404 (panel_slug appended to aliases CSV)")
                    elif code != 200:
                        n_fail += 1
                        fail_other.append((slug, yr, f"HTTP {code}"))
                        print(f"FAIL {slug} {yr}: HTTP {code}")
                    else:
                        raw = parse_advanced_player_table(text, BeautifulSoup)
                        raw_buf.append(tidy_advanced_df(raw, slug, yr))
                        n_ok += 1
                        if len(raw_buf) >= int(cfg.raw_flush_every_n_ok):
                            raw_header = _flush_raw_buffer(out_raw, raw_buf, raw_header)
                except Exception as e:
                    n_fail += 1
                    msg = str(e)
                    print(f"FAIL {slug} {yr}: {e}")
                    if "404" in msg and "Not Found" in msg:
                        fail_404.add(slug)
                        _append_404_panel_slug_now(alias_path, slug, alias_seen)
                    else:
                        fail_other.append((slug, yr, msg))
                if pbar is not None:
                    pbar.update(1)
                    pos = min(n_done_at_start + n_ok + n_fail, n_total)
                    pbar.set_postfix(
                        ok=n_ok,
                        fail=n_fail,
                        list_pct=f"{100 * pos / n_total:.1f}%" if n_total else "n/a",
                        refresh=False,
                    )
        except KeyboardInterrupt:
            interrupted = True
            print("KeyboardInterrupt — flushing buffer, then stop.")
    finally:
        raw_header = _flush_raw_buffer(out_raw, raw_buf, raw_header)
        if pbar is not None:
            pbar.close()

    elapsed = time.time() - t0
    print(f"Done in {elapsed:.1f}s — ok={n_ok} fail={n_fail}")

    refresh_sr_slug_alias_cache()
    if n_ok > 0 and out_raw.is_file() and out_raw.stat().st_size > 0:
        _dedupe_out_raw(out_raw)
        br = _read_out_raw_safe(out_raw)
        print("Updated", out_raw, "rows:", len(br))
    elif len(to_fetch) == 0:
        print("Nothing to fetch — left", out_raw)

    return {
        "stage": "scrape_bpm",
        "out_raw": str(out_raw),
        "n_ok": n_ok,
        "n_fail": n_fail,
        "n_to_fetch": len(to_fetch),
        "interrupted": interrupted,
        "fail_404_slugs": sorted(fail_404),
        "fail_other": fail_other,
        "seconds": elapsed,
    }


def fetch_html(url: str, *, scrape_cfg: ScrapeBpmConfig | None = None) -> str:
    """Single-page fetch (200 body only). For smoke tests."""
    requests_mod, _ = _require_scrape_deps()
    cfg = scrape_cfg or ScrapeBpmConfig()
    rt = _ScrapeRuntime(cfg, requests_mod, _headers_for_config(cfg))
    code, text = rt.get(url)
    if code != 200:
        raise RuntimeError(f"HTTP {code} for {url}")
    return text
