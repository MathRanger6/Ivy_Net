"""Polite, sequential Wayback retrieval. Importing this module makes no requests.

Before a live run, review the archive's published crawling guidance and supply
--policy-reviewed. robots.txt is then checked automatically at run time.
Public accessibility and a contact header do not constitute a reuse license.
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

# These are operational pacing settings, not research parameters.
USER_AGENT = (
    "RomaniaEducationResearch/1.0 "
    "(academic research; contact: charles.levine@virginia.edu)"
)
ROBOT_AGENT = "RomaniaEducationResearch"
PAUSE_SECONDS = (15, 30)
RETRY_PAUSE_SECONDS = (60, 90)
MAX_ATTEMPTS_PER_URL = 2
MAX_CONSECUTIVE_FAILURES = 3
CONNECTION_TIMEOUT_SECONDS = 25
RUN_LIMIT_SECONDS = 12 * 60
ARCHIVE_ORIGIN = "https://web.archive.org"


class RetrievalStopped(RuntimeError):
    """Stop this run without treating inaccessible pages as absent records."""


class NoAutomaticRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def retry_after_seconds(value, now):
    """Interpret either seconds or an HTTP date; never shorten the server's wait."""
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
    def __init__(self, output_directory, emit, *, policy_reviewed=False):
        self.output_directory = Path(output_directory)
        self.emit = emit
        self.policy_reviewed = policy_reviewed
        self.opener = urllib.request.build_opener(NoAutomaticRedirect())
        self.robot_rules = None
        self.robot_interval = 0.0
        self.last_request_finished = None
        self.deadline = time.monotonic() + RUN_LIMIT_SECONDS
        self.failures = 0
        self.state_path = self.output_directory / "retrieval_pause.json"
        self.not_before = 0.0
        if self.state_path.exists():
            self.not_before = json.loads(self.state_path.read_text())["not_before_utc"]

    def _validate_url(self, url):
        parsed = urllib.parse.urlsplit(url)
        if (
            parsed.scheme != "https"
            or parsed.netloc != "web.archive.org"
            or parsed.username
            or parsed.password
        ):
            raise RetrievalStopped("Redirect or URL leaves the approved HTTPS archive host.")

    def _wait(self, seconds, reason):
        seconds = max(0, seconds)
        if time.monotonic() + seconds + CONNECTION_TIMEOUT_SECONDS > self.deadline:
            raise RetrievalStopped("Twelve-minute run limit: preserve checkpoints and stop.")
        self.emit({"kind": "retrieval_wait", "seconds": round(seconds, 1), "reason": reason})
        # Short sleeps allow interruption and visible countdowns during longer backoff.
        remaining = seconds
        while remaining > 0:
            step = min(remaining, 15)
            time.sleep(step)
            remaining -= step
            if remaining >= 15:
                self.emit({"kind": "retrieval_wait_remaining", "seconds": round(remaining, 1)})

    def _pause_across_runs(self, seconds, reason):
        self.not_before = max(self.not_before, time.time() + seconds)
        self.output_directory.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps({
            "not_before_utc": self.not_before,
            "reason": reason,
        }, indent=2) + "\n")
        self.emit({"kind": "retrieval_stopped", "reason": reason,
                   "not_before_utc": self.not_before})
        raise RetrievalStopped(reason)

    def _once(self, url):
        """One HTTP request, with body retained only in memory."""
        request = urllib.request.Request(url, headers={
            "User-Agent": USER_AGENT,
            "From": "charles.levine@virginia.edu",
        })
        try:
            with self.opener.open(request, timeout=CONNECTION_TIMEOUT_SECONDS) as response:
                return response.status, dict(response.headers.items()), response.read()
        except urllib.error.HTTPError as error:
            with error:
                return error.code, dict(error.headers.items()), b""

    def _download(self, url, *, checking_robots=False):
        for redirect_number in range(6):
            self._validate_url(url)
            if not checking_robots and not self.robot_rules.can_fetch(ROBOT_AGENT, url):
                raise RetrievalStopped("robots.txt disallows this archive URL; no request sent.")
            for attempt in range(MAX_ATTEMPTS_PER_URL):
                if time.time() < self.not_before:
                    raise RetrievalStopped("A saved server/backoff waiting period has not expired.")
                if self.last_request_finished is not None:
                    interval = max(random.uniform(*PAUSE_SECONDS), self.robot_interval)
                    elapsed = time.monotonic() - self.last_request_finished
                    self._wait(max(0, interval - elapsed), "Spacing sequential archive requests")
                elif time.monotonic() + CONNECTION_TIMEOUT_SECONDS > self.deadline:
                    raise RetrievalStopped("Twelve-minute run limit reached.")
                status = None
                try:
                    status, headers, body = self._once(url)
                    headers = {k.lower(): v for k, v in headers.items()}
                    error_text = None
                except (urllib.error.URLError, TimeoutError, OSError) as error:
                    headers, body = {}, b""
                    error_text = str(error)
                self.last_request_finished = time.monotonic()
                self.emit({"kind": "http_attempt", "url": url, "status": status,
                           "attempt": attempt + 1, "error": error_text})

                # Stop rather than retry a refusal or explicit rate limit.
                if status in (401, 403, 451):
                    raise RetrievalStopped(f"HTTP {status}: access restriction; no automatic retry.")
                if status == 429:
                    delay = retry_after_seconds(headers.get("retry-after"), time.time())
                    self._pause_across_runs(max(300, delay or 0),
                                            "HTTP 429: rate limit; stopped this run.")
                if status is not None and status >= 400 and headers.get("retry-after"):
                    delay = retry_after_seconds(headers["retry-after"], time.time())
                    self._pause_across_runs(max(300, delay or 0),
                                            f"HTTP {status}: honor Retry-After; stopped this run.")

                transient = status is None or (status is not None and 500 <= status <= 599)
                if transient:
                    self.failures += 1
                    if self.failures >= MAX_CONSECUTIVE_FAILURES:
                        self._pause_across_runs(300, "Three consecutive transient failures.")
                    if attempt + 1 < MAX_ATTEMPTS_PER_URL:
                        self._wait(random.uniform(*RETRY_PAUSE_SECONDS), "Transient failure backoff")
                        continue
                    return None
                self.failures = 0
                if status in (301, 302, 303, 307, 308):
                    location = headers.get("location")
                    if not location:
                        raise RetrievalStopped("Redirect without Location.")
                    url = urllib.parse.urljoin(url, location)
                    break  # Redirect is checked and paced as a separate request.
                if status == 200:
                    return body, url
                self.emit({"kind": "unverified_page", "url": url, "status": status})
                return None
            else:
                return None
        raise RetrievalStopped("Too many archive redirects; stopped.")

    def get(self, url):
        if not self.policy_reviewed:
            raise RetrievalStopped(
                "Review published archive crawling guidance before using --policy-reviewed."
            )
        if self.robot_rules is None:
            result = self._download(ARCHIVE_ORIGIN + "/robots.txt", checking_robots=True)
            if result is None:
                raise RetrievalStopped("robots.txt could not be verified; no source-page retrieval.")
            body, _ = result
            text = body.decode("utf-8", errors="replace")
            if "<html" in text.lower() or "<!doctype html" in text.lower():
                raise RetrievalStopped("robots.txt returned HTML; manual review required.")
            rules = urllib.robotparser.RobotFileParser()
            rules.parse(text.splitlines())
            self.robot_rules = rules
            delay = rules.crawl_delay(ROBOT_AGENT)
            rate = rules.request_rate(ROBOT_AGENT)
            self.robot_interval = max(
                float(delay or 0),
                rate.seconds / rate.requests if rate and rate.requests else 0,
            )
            self.emit({"kind": "robots_checked", "minimum_interval_seconds": self.robot_interval})
        return self._download(url)

