"""Adaptive, sequential Wayback retrieval for the bounded Romania audit.

Importing this module makes no network requests. The client identifies the
academic project, adapts its interval to observed success/failure, honors
Retry-After and robots.txt, and persists pacing across restarts. A missing
robots.txt (HTTP 404) means no rules were published at that endpoint.

Public accessibility and a contact header do not establish permission to
publish or redistribute personal records. Page bodies remain in memory.
"""
import datetime
import email.utils
import json
import random
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from pathlib import Path
from zoneinfo import ZoneInfo

USER_AGENT = (
    "RomaniaEducationResearch/1.0 "
    "(academic research; contact: charles.levine@virginia.edu)"
)
ROBOT_AGENT = "RomaniaEducationResearch"
ARCHIVE_ORIGIN = "https://web.archive.org"
CONNECTION_TIMEOUT_SECONDS = 25
DEFAULT_INITIAL_INTERVAL_SECONDS = 2.0
DEFAULT_MINIMUM_INTERVAL_SECONDS = 1.2
DEFAULT_MAXIMUM_INTERVAL_SECONDS = 60.0
DEFAULT_MAX_RUNTIME_HOURS = 6.0
PACING_STATE_VERSION = 2
SUCCESS_STREAK_TO_SPEED_UP = 10
SPEED_UP_FACTOR = 0.90
FAILURE_SLOWDOWN_FACTOR = 1.75
JITTER_FRACTION = 0.10
MAX_REDIRECTS = 5
LOG_TIMEZONE = ZoneInfo("America/New_York")


class RetrievalStopped(RuntimeError):
    """The run stopped safely; unresolved addresses remain eligible for another pass."""


class NoAutomaticRedirect(urllib.request.HTTPRedirectHandler):
    """Expose redirects so every redirected request receives pacing checks."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def retry_after_seconds(value, now):
    """Interpret Retry-After as seconds or an HTTP date."""
    if not value:
        return None
    try:
        return max(0.0, float(int(value.strip())))
    except ValueError:
        try:
            date = email.utils.parsedate_to_datetime(value)
            if date.tzinfo is None:
                date = date.replace(tzinfo=datetime.timezone.utc)
            return max(0.0, date.timestamp() - now)
        except (ValueError, TypeError, OverflowError):
            return None


class ArchiveClient:
    """One sequential, adaptive client shared by every retrieval in a run."""

    def __init__(
        self,
        output_directory,
        emit,
        *,
        archive_use_acknowledged=False,
        initial_interval_seconds=DEFAULT_INITIAL_INTERVAL_SECONDS,
        minimum_interval_seconds=DEFAULT_MINIMUM_INTERVAL_SECONDS,
        maximum_interval_seconds=DEFAULT_MAXIMUM_INTERVAL_SECONDS,
        max_runtime_hours=DEFAULT_MAX_RUNTIME_HOURS,
        resume_interval_cap_seconds=None,
        max_http_attempts=None,
        reuse_recorded_robots_absence=False,
        success_step_seconds=None,
        random_adaptive_fraction=None,
        pace_redirects=True,
        jitter_fraction=JITTER_FRACTION,
    ):
        if minimum_interval_seconds <= 0:
            raise ValueError("minimum_interval_seconds must be positive")
        if not minimum_interval_seconds <= initial_interval_seconds <= maximum_interval_seconds:
            raise ValueError("Require minimum <= initial <= maximum interval")
        if max_runtime_hours <= 0:
            raise ValueError("max_runtime_hours must be positive")
        if resume_interval_cap_seconds is not None and not (
            minimum_interval_seconds <= resume_interval_cap_seconds <= maximum_interval_seconds
        ):
            raise ValueError("Require minimum <= resume interval cap <= maximum interval")
        if max_http_attempts is not None and max_http_attempts < 1:
            raise ValueError("max_http_attempts must be positive")
        if success_step_seconds is not None and success_step_seconds <= 0:
            raise ValueError("success_step_seconds must be positive")
        if random_adaptive_fraction is not None and not 0 < random_adaptive_fraction < 1:
            raise ValueError("random_adaptive_fraction must be between zero and one")
        if not 0 <= jitter_fraction < 1:
            raise ValueError("jitter_fraction must be between zero and one")

        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(parents=True, exist_ok=True)
        self.emit = emit
        self.archive_use_acknowledged = archive_use_acknowledged
        self.opener = urllib.request.build_opener(NoAutomaticRedirect())
        self.minimum_interval = float(minimum_interval_seconds)
        self.maximum_interval = float(maximum_interval_seconds)
        self.interval = float(initial_interval_seconds)
        self.max_http_attempts = max_http_attempts
        self.http_attempts = 0
        self.success_step_seconds = success_step_seconds
        self.random_adaptive_fraction = random_adaptive_fraction
        self.pace_redirects = pace_redirects
        self.jitter_fraction = jitter_fraction
        self.deadline = time.monotonic() + max_runtime_hours * 3600
        self.last_request_finished = None
        self.success_streak = 0
        self.consecutive_failures = 0
        self.robot_rules = None
        self.robot_interval = 0.0
        self.robots_checked = False
        self.state_path = self.output_directory / "retrieval_adaptive_state.json"
        self.not_before = 0.0
        self.last_status = None
        self.last_error = None
        self.last_url = None
        self.last_request_label = None
        self.last_response_headers = {}
        self.last_response_body = b""

        if self.state_path.exists():
            try:
                state = json.loads(self.state_path.read_text())
                # Version 1 treated missing archived captures (HTTP 404) as
                # server pressure and could persist an unnecessarily long
                # interval. Ignore that old state once after this correction.
                if state.get("state_version") == PACING_STATE_VERSION:
                    self.interval = min(
                        self.maximum_interval,
                        max(
                            self.minimum_interval,
                            float(state.get("interval_seconds", self.interval)),
                        ),
                    )
                    self.not_before = float(state.get("not_before_utc", 0.0))
                else:
                    self.emit({
                        "kind": "adaptive_state_reset",
                        "reason": "Earlier pacing state predates neutral 404 handling",
                    })
            except (OSError, ValueError, TypeError, json.JSONDecodeError):
                self.emit({"kind": "adaptive_state_ignored", "reason": "Unreadable state file"})

        # An explicitly bounded trial may begin faster than the saved interval.
        # Preserve any server-requested not-before time and the normal ability
        # to slow back down after failures.
        if resume_interval_cap_seconds is not None and self.interval > resume_interval_cap_seconds:
            previous = self.interval
            self.interval = float(resume_interval_cap_seconds)
            self.emit({"kind": "pace_trial_start", "old_seconds": previous,
                       "new_seconds": self.interval})

        # The same private acquisition log already records a completed 404
        # robots.txt check. Reuse that result on subsequent runs of this
        # bounded archive job; if the log is absent or inconclusive, check it.
        if reuse_recorded_robots_absence and self._prior_robots_absence_recorded():
            rules = urllib.robotparser.RobotFileParser()
            rules.parse([])
            self.robot_rules = rules
            self.robots_checked = True
            self.emit({"kind": "robots_absence_reused", "status": 404})

    def _prior_robots_absence_recorded(self):
        log_path = self.output_directory / "retrieval_events.jsonl"
        if not log_path.exists():
            return False
        last_result = None
        with log_path.open(encoding="utf-8") as stream:
            for line in stream:
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event.get("kind") == "robots_attempt":
                    last_result = None
                elif event.get("kind") == "robots_absent" and event.get("status") == 404:
                    last_result = "absent"
                elif event.get("kind") == "robots_checked":
                    last_result = "rules_present"
        return last_result == "absent"

    def _save_state(self, reason):
        self.state_path.write_text(json.dumps({
            "state_version": PACING_STATE_VERSION,
            "saved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "interval_seconds": self.interval,
            "not_before_utc": self.not_before,
            "reason": reason,
        }, indent=2) + "\n")

    def _validate_url(self, url):
        parsed = urllib.parse.urlsplit(url)
        if (
            parsed.scheme != "https"
            or parsed.netloc != "web.archive.org"
            or parsed.username
            or parsed.password
        ):
            raise RetrievalStopped("URL or redirect leaves the approved HTTPS archive host.")

    def _wait(self, seconds, reason):
        seconds = max(0.0, float(seconds))
        if time.monotonic() + seconds + CONNECTION_TIMEOUT_SECONDS > self.deadline:
            raise RetrievalStopped("Configured run-time limit reached; checkpoints preserved.")
        # Calculate both timestamps once for this pause, including its remaining
        # duration when resuming a persisted backoff. UTC arithmetic also handles
        # a pause spanning a daylight-saving change correctly.
        started_utc = datetime.datetime.now(datetime.timezone.utc)
        started = started_utc.astimezone(LOG_TIMEZONE)
        resume = (started_utc + datetime.timedelta(seconds=seconds)).astimezone(LOG_TIMEZONE)
        timing = {
            "pause_started_at": started.isoformat(),
            "expected_resume_at": resume.isoformat(),
            "timezone": LOG_TIMEZONE.key,
            "timing": (
                f"\nPaused: {started:%Y-%m-%d %H:%M:%S %Z} | "
                f"Resume expected: {resume:%Y-%m-%d %H:%M:%S %Z}"
            ),
        }
        if seconds:
            self.emit({"kind": "retrieval_wait", "seconds": round(seconds, 1), "reason": reason, **timing})
        remaining = seconds
        while remaining > 0:
            step = min(remaining, 15.0)
            time.sleep(step)
            remaining -= step
            if remaining >= 15:
                self.emit({"kind": "retrieval_wait_remaining", "seconds": round(remaining, 1),
                           "reason": reason, **timing})

    def wait_between_passes(self, seconds, pass_number):
        """Pause before revisiting unresolved addresses."""
        self._wait(seconds, f"Cooldown before unresolved-address pass {pass_number}")

    def _pace(self, next_request):
        if time.time() < self.not_before:
            self._wait(self.not_before - time.time(),
                       f"Saved server backoff before {next_request}")
        if self.last_request_finished is None:
            return
        base = max(self.interval, self.robot_interval)
        jittered = base * random.uniform(1 - self.jitter_fraction, 1 + self.jitter_fraction)
        elapsed = time.monotonic() - self.last_request_finished
        prior = (
            f" after {self.last_request_label} returned HTTP {self.last_status}"
            if self.last_request_label and self.last_status is not None else ""
        )
        variation = (
            f" with ±{self.jitter_fraction:.0%} variation"
            if self.jitter_fraction else " without random variation"
        )
        self._wait(max(0.0, jittered - elapsed),
                   f"Client pacing before {next_request}{prior}; "
                   f"{base:.1f}s target{variation}")

    def _once(self, url):
        """Perform one identified request; retain its body only in memory."""
        request = urllib.request.Request(url, headers={
            "User-Agent": USER_AGENT,
            "From": "charles.levine@virginia.edu",
            "Accept": "text/html,application/xhtml+xml,text/plain;q=0.9,*/*;q=0.5",
        })
        try:
            with self.opener.open(request, timeout=CONNECTION_TIMEOUT_SECONDS) as response:
                return response.status, dict(response.headers.items()), response.read(), None
        except urllib.error.HTTPError as error:
            with error:
                return error.code, dict(error.headers.items()), error.read(), None
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            return None, {}, b"", str(error)

    def _success(self):
        self.consecutive_failures = 0
        self.success_streak += 1
        old = self.interval
        if self.random_adaptive_fraction is not None:
            self.interval = max(
                self.minimum_interval,
                self.interval * (1 - random.uniform(0, self.random_adaptive_fraction)),
            )
            self.success_streak = 0
        elif self.success_step_seconds is not None:
            self.interval = max(self.minimum_interval, self.interval - self.success_step_seconds)
            self.success_streak = 0
        elif self.success_streak >= SUCCESS_STREAK_TO_SPEED_UP:
            self.interval = max(self.minimum_interval, self.interval * SPEED_UP_FACTOR)
            self.success_streak = 0
        if self.interval != old:
            self.emit({"kind": "adaptive_pace", "direction": "faster",
                       "old_seconds": round(old, 2), "new_seconds": round(self.interval, 2)})
        self._save_state("successful request")

    def _failure(self, reason, *, retry_after=None):
        self.success_streak = 0
        self.consecutive_failures += 1
        old = self.interval
        factor = (
            1 + random.uniform(0, self.random_adaptive_fraction)
            if self.random_adaptive_fraction is not None else FAILURE_SLOWDOWN_FACTOR
        )
        self.interval = min(self.maximum_interval, self.interval * factor)
        if retry_after is not None:
            self.not_before = max(self.not_before, time.time() + retry_after)
        self.emit({"kind": "adaptive_pace", "direction": "slower", "reason": reason,
                   "old_seconds": round(old, 2), "new_seconds": round(self.interval, 2),
                   "consecutive_failures": self.consecutive_failures,
                   "not_before_utc": self.not_before or None})
        self._save_state(reason)

    def _check_robots(self):
        """HTTP 404 means no robots rules were published at this endpoint."""
        if self.robots_checked:
            return
        url = ARCHIVE_ORIGIN + "/robots.txt"
        self._validate_url(url)
        self._pace("robots.txt check")
        status, headers, body, error = self._once(url)
        self.last_request_finished = time.monotonic()
        self.last_status = status
        self.last_request_label = "robots.txt"
        headers = {k.lower(): v for k, v in headers.items()}
        self.emit({"kind": "robots_attempt", "url": url, "status": status, "error": error})

        if status == 404:
            rules = urllib.robotparser.RobotFileParser()
            rules.parse([])
            self.robot_rules = rules
            self.robots_checked = True
            self._success()
            self.emit({"kind": "robots_absent", "status": 404,
                       "meaning": "No published robots.txt rules at this endpoint"})
            return
        if status == 200:
            text = body.decode("utf-8", errors="replace")
            if "<html" in text.lower() or "<!doctype html" in text.lower():
                raise RetrievalStopped("robots.txt returned HTML; source retrieval stopped.")
            rules = urllib.robotparser.RobotFileParser()
            rules.parse(text.splitlines())
            self.robot_rules = rules
            delay = rules.crawl_delay(ROBOT_AGENT)
            rate = rules.request_rate(ROBOT_AGENT)
            self.robot_interval = max(
                float(delay or 0),
                rate.seconds / rate.requests if rate and rate.requests else 0,
            )
            self.robots_checked = True
            self._success()
            self.emit({"kind": "robots_checked",
                       "minimum_interval_seconds": self.robot_interval})
            return

        retry_after = retry_after_seconds(headers.get("retry-after"), time.time())
        self._failure("robots.txt could not be verified", retry_after=retry_after)
        raise RetrievalStopped(
            f"robots.txt check returned {status or error}; source retrieval stopped."
        )

    def get(self, url, request_label=None):
        """Return (body, effective_url), or None while recording an unresolved request."""
        if not self.archive_use_acknowledged:
            raise RetrievalStopped(
                "Set archive_use_acknowledged=True after reviewing the notebook parameters."
            )
        self._check_robots()
        label = request_label or "archived page"

        for redirect_number in range(MAX_REDIRECTS + 1):
            if self.max_http_attempts is not None and self.http_attempts >= self.max_http_attempts:
                raise RetrievalStopped(
                    f"Bounded pace trial reached {self.max_http_attempts} HTTP attempts; "
                    "saved checkpoints are preserved."
                )
            self._validate_url(url)
            if self.robot_rules is not None and not self.robot_rules.can_fetch(ROBOT_AGENT, url):
                raise RetrievalStopped("robots.txt disallows this archive URL.")
            if redirect_number == 0 or self.pace_redirects:
                self._pace(f"{label} redirect follow-up" if redirect_number else label)
            status, headers, body, error = self._once(url)
            self.http_attempts += 1
            self.last_status = status
            self.last_error = error
            self.last_url = url
            self.last_request_label = label
            self.last_response_headers = headers.copy()
            self.last_response_body = body
            self.last_request_finished = time.monotonic()
            headers = {k.lower(): v for k, v in headers.items()}
            self.emit({"kind": "http_attempt", "url": url, "status": status,
                       "error": error, "request_label": label,
                       "redirect_follow_up": redirect_number > 0,
                       "interval_seconds": round(self.interval, 2)})

            if status == 200:
                self._success()
                return body, url

            if status in (301, 302, 303, 307, 308):
                location = headers.get("location")
                if not location:
                    self._failure("redirect without Location")
                    return None
                if self.pace_redirects:
                    self._success()
                else:
                    self.consecutive_failures = 0
                    self._save_state("archive redirect")
                url = urllib.parse.urljoin(url, location)
                continue

            retry_after = retry_after_seconds(headers.get("retry-after"), time.time())
            if status == 429:
                self._failure("HTTP 429", retry_after=max(300.0, retry_after or 0.0))
                return None
            if status in (401, 403, 451):
                self._failure(f"HTTP {status}", retry_after=retry_after)
                return None
            if status is None or 500 <= status <= 599:
                self._failure(error or f"HTTP {status}", retry_after=retry_after)
                return None

            if status in (404, 410):
                # A missing historical capture is a property of this archived
                # URL/timestamp, not evidence that the server wants us to slow
                # down. Preserve the interval and let the caller search another
                # capture timestamp.
                self.success_streak = 0
                self.consecutive_failures = 0
                self.emit({
                    "kind": "capture_missing",
                    "status": status,
                    "url": url,
                    "interval_seconds": round(self.interval, 2),
                })
                self._save_state(f"HTTP {status} archived capture missing")
                return None

            self._failure(f"HTTP {status}", retry_after=retry_after)
            return None

        self._failure("too many redirects")
        return None
