"""
Stage 3B — Wayback HTML download (shared by 540 notebook and run_stage3b_cli.py).

Fixes (2026-10):
- Always install via $TMPDIR staging + cp for large HTML and for cloud-sync paths (Dropbox).
- Skip re-download when the last index row for a local_path is a permanent failure and file still missing.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

from wayback.paths import normalize_wayback_slug_filter

MIN_HTML_BYTES = 500
LARGE_HTML_STAGING_BYTES = 150_000

# Archive-side or empty-body failures — safe to stop re-hitting every run.
# Omit "read-back verify failed" (transient Dropbox / sandbox); those retry until file lands.
PERMANENT_DOWNLOAD_ERROR_MARKERS = (
    "too small",
    "HTTP 403",
    "HTTP 404",
    "HTTP 410",
)


def _is_cloud_sync_path(path: Path) -> bool:
    s = str(path)
    return any(x in s for x in ("Dropbox", "CloudStorage", "iCloud"))


def _wayback_insert_id_modifier(url: str) -> str:
    m = re.match(r"^(https://web\.archive\.org/web/)(\d{14})(/)(https?://.+)$", url, re.I)
    if not m:
        return url
    return f"{m.group(1)}{m.group(2)}id_{m.group(3)}{m.group(4)}"


def _write_bytes_via_shell_if_eperm(path: Path, content: bytes) -> bool:
    import shlex

    sp = str(path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    try:
        r = subprocess.run(
            ["/bin/sh", "-c", f"cat > {shlex.quote(sp)}"],
            input=content,
            capture_output=True,
            timeout=300,
        )
        if r.returncode == 0:
            try:
                if path.is_file() and path.stat().st_size == len(content):
                    return True
            except OSError:
                pass
    except Exception:
        pass
    py = "/usr/bin/python3"
    if not Path(py).is_file():
        return False
    try:
        r = subprocess.run(
            [
                py,
                "-c",
                "import sys, pathlib; p=pathlib.Path(sys.argv[1]); "
                "p.parent.mkdir(parents=True, exist_ok=True); "
                "p.write_bytes(sys.stdin.buffer.read())",
                sp,
            ],
            input=content,
            capture_output=True,
            timeout=300,
        )
        if r.returncode == 0:
            try:
                if path.is_file() and path.stat().st_size == len(content):
                    return True
            except OSError:
                pass
    except Exception:
        pass
    return False


def _read_bytes_verify_via_subprocess(path: Path, content: bytes, *, quiet: bool = False) -> bool:
    import shlex

    sp = str(path)
    want_len = len(content)
    want_sha = hashlib.sha256(content).hexdigest()

    try:
        r = subprocess.run(["/bin/cat", sp], capture_output=True, timeout=120)
        if r.returncode == 0 and r.stdout == content and len(r.stdout) >= MIN_HTML_BYTES:
            if not quiet:
                print("     NOTE: verified via /bin/cat.", flush=True)
            return True
    except Exception:
        pass

    try:
        r = subprocess.run(
            ["/usr/bin/openssl", "dgst", "-sha256", sp],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if r.returncode == 0 and r.stdout:
            m = re.search(r"= ([0-9a-f]{64})", r.stdout, re.I)
            if m and m.group(1).lower() == want_sha:
                if not quiet:
                    print("     NOTE: verified via openssl SHA256.", flush=True)
                return True
    except Exception:
        pass

    try:
        r = subprocess.run(
            ["/bin/sh", "-c", f"shasum -a 256 {shlex.quote(sp)}"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if r.returncode == 0 and r.stdout:
            tok = r.stdout.strip().split()
            if tok and tok[0].lower() == want_sha:
                if not quiet:
                    print("     NOTE: verified via shasum SHA256.", flush=True)
                return True
    except Exception:
        pass

    try:
        r = subprocess.run(
            ["/usr/bin/stat", "-f", "%z", sp],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if r.returncode == 0 and r.stdout.strip().isdigit():
            if int(r.stdout.strip()) == want_len and want_len >= MIN_HTML_BYTES:
                if not quiet:
                    print("     NOTE: verified via subprocess stat (size only).", flush=True)
                return True
    except Exception:
        pass

    return False


def _install_html_via_temp_staging(dest: Path, content: bytes) -> bool:
    """Write to $TMPDIR, verify, then cp into *dest* (reliable on Dropbox)."""
    if len(content) < MIN_HTML_BYTES:
        return False

    td = Path(tempfile.gettempdir()) / "faculty_snapshots_3b_staging"
    try:
        td.mkdir(parents=True, exist_ok=True)
    except OSError:
        return False

    name = f"{hashlib.sha256(str(dest).encode()).hexdigest()[:12]}_{dest.name}"
    tmp = td / name
    try:
        try:
            tmp.write_bytes(content)
        except OSError:
            if not _write_bytes_via_shell_if_eperm(tmp, content):
                return False
        ok_tmp = False
        try:
            ok_tmp = tmp.read_bytes() == content
        except OSError:
            ok_tmp = _read_bytes_verify_via_subprocess(tmp, content, quiet=True)
        if not ok_tmp:
            tmp.unlink(missing_ok=True)
            return False

        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(tmp, dest)
        except OSError:
            r = subprocess.run(["/bin/cp", str(tmp), str(dest)], capture_output=True, timeout=120)
            if r.returncode != 0:
                tmp.unlink(missing_ok=True)
                return False

        tmp.unlink(missing_ok=True)

        ok_dest = False
        try:
            ok_dest = dest.read_bytes() == content
        except OSError:
            ok_dest = _read_bytes_verify_via_subprocess(dest, content, quiet=True)
        if ok_dest:
            print("     NOTE: HTML staged in $TMPDIR then copied to destination.", flush=True)
            return True
        return _read_bytes_verify_via_subprocess(dest, content, quiet=False)
    except Exception:
        return False


def _should_use_temp_staging(dest: Path, content: bytes) -> bool:
    if len(content) < MIN_HTML_BYTES:
        return False
    if len(content) >= LARGE_HTML_STAGING_BYTES:
        return True
    return _is_cloud_sync_path(dest)


def _write_snapshot_html(
    dest: Path,
    content: bytes,
    *,
    workspace_fallback: Path | None,
    write_root_label: str,
) -> tuple[bool, str]:
    """Return (ok, error_message)."""
    paths_try = [dest.resolve()]
    if workspace_fallback is not None and workspace_fallback.resolve() != paths_try[0]:
        paths_try.append(workspace_fallback.resolve())

    for pi, wpx in enumerate(paths_try):
        if _should_use_temp_staging(wpx, content):
            if _install_html_via_temp_staging(wpx, content):
                return True, ""
            # fall through to direct write if staging failed

        try:
            wpx.parent.mkdir(parents=True, exist_ok=True)
            try:
                wpx.write_bytes(content)
            except OSError as we0:
                if getattr(we0, "errno", None) == 1 and _write_bytes_via_shell_if_eperm(wpx, content):
                    print(
                        "     NOTE: EPERM on write_bytes — wrote via shell/system python.",
                        flush=True,
                    )
                else:
                    raise
            try:
                fd = os.open(str(wpx), os.O_RDWR)
                try:
                    os.fsync(fd)
                finally:
                    os.close(fd)
            except OSError:
                pass
        except OSError as wexc:
            err = f"write failed: {wexc}"
            if getattr(wexc, "errno", None) == 1 and pi + 1 < len(paths_try):
                print("     NOTE: EPERM — retrying under workspace faculty_snapshots …", flush=True)
                continue
            return False, err

        ok = False
        for _ in range(200):
            try:
                got = wpx.read_bytes()
                if got == content and len(got) >= MIN_HTML_BYTES:
                    ok = True
                    break
            except OSError:
                pass
            time.sleep(0.05)
        if not ok and _read_bytes_verify_via_subprocess(wpx, content):
            ok = True
        if ok:
            return True, ""

        try:
            ds = wpx.stat().st_size
        except OSError:
            ds = -1
        try:
            rlen = len(wpx.read_bytes())
        except OSError:
            rlen = -1
        err = f"read-back verify failed (expected {len(content)} B; read {rlen} B; stat {ds} B) @ {wpx}"
        if ds < 0 and rlen < 0:
            err += f" — missing after write (3B root={write_root_label})."
        if pi + 1 < len(paths_try) and _should_use_temp_staging(wpx, content):
            continue
        return False, err

    return False, "verify failed"


def _last_index_by_local_path(index_path: Path) -> dict[str, dict]:
    last: dict[str, dict] = {}
    if not index_path.is_file():
        return last
    with open(index_path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)
            lp = rec.get("local_path")
            if lp:
                last[lp] = rec
    return last


def _is_permanent_index_failure(rec: dict) -> bool:
    if rec.get("http_status") == 200 and rec.get("file_size_bytes", 0) >= MIN_HTML_BYTES:
        return False
    err = (rec.get("error") or "").strip()
    if not err:
        return rec.get("http_status", -1) not in (200, -1)
    return any(m in err for m in PERMANENT_DOWNLOAD_ERROR_MARKERS)


def download_plan(
    *,
    plan_path: Path,
    index_path: Path,
    session,
    delay: float,
    overwrite,
    snapshot_file_ok,
    resolve_faculty_snapshot_path,
    faculty_snapshot_rel_from_local_path,
    tenure_pipeline_dir: Path,
    faculty_snapshots_write_root: Path,
    cdx_html_timeout: int,
    wayback_slugs: set[str] | None = None,
):
    """Core download loop — reads plan JSONL, fetches HTML, appends to index JSONL."""
    with open(plan_path, encoding="utf-8") as f:
        raw_plan = [json.loads(line) for line in f]

    plan_block_slug: dict[str, bool] = {}
    for r in raw_plan:
        us = r.get("uni_slug")
        if not us:
            continue
        has_real = (
            r.get("local_path")
            and r.get("year") is not None
            and r.get("season")
            and r.get("n_snaps", 1) > 0
        )
        if has_real:
            plan_block_slug[us] = False
        elif r.get("n_snaps") == -1 and r.get("reason"):
            plan_block_slug[us] = True

    plan = [
        r
        for r in raw_plan
        if r.get("plan_row_type") != "cdx_bookmark" and r.get("n_snaps", 1) > 0
    ]

    ghost_ok: list[str] = []
    last_by_lp = _last_index_by_local_path(index_path)
    if index_path.exists():
        with open(index_path, encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                rec = json.loads(line)
                if rec.get("http_status") != 200:
                    continue
                if rec.get("file_size_bytes", 0) < MIN_HTML_BYTES:
                    continue
                lp = rec.get("local_path")
                if not lp:
                    continue
                if not snapshot_file_ok(lp):
                    ghost_ok.append(lp)
    if ghost_ok:
        uniq = list(dict.fromkeys(ghost_ok))
        print(
            f"  WARNING: {len(uniq)} index row(s) claim success but HTML is missing or < {MIN_HTML_BYTES} B on disk."
        )
        print("           Re-fetching those paths (use overwrite=True to force all).")
        for g in uniq[:8]:
            print(f"           — {g}")
        if len(uniq) > 8:
            print(f"           … ({len(uniq) - 8} more)")

    force_all = overwrite is True
    if force_all:
        overwrite_keys: set[str] = set()
    elif isinstance(overwrite, list):
        overwrite_keys = set(overwrite)
    else:
        overwrite_keys = set()

    to_download = []
    n_skipped = 0
    n_plan_dup = 0
    n_plan_blk = 0
    n_perm_skip = 0
    n_slug_skip = 0
    blocked_slugs: set[str] = set()
    seen_lp: set[str] = set()
    slug_filter = normalize_wayback_slug_filter(wayback_slugs)
    if slug_filter:
        print(
            f"  WAYBACK_SLUGS filter : {len(slug_filter)} slug(s) — "
            f"{', '.join(sorted(slug_filter)[:8])}"
            + (f" (+{len(slug_filter)-8} more)" if len(slug_filter) > 8 else "")
        )
    for rec in plan:
        lp = rec.get("local_path")
        if not lp:
            continue
        if slug_filter and rec.get("uni_slug") not in slug_filter:
            n_slug_skip += 1
            continue
        if plan_block_slug.get(rec["uni_slug"], False):
            n_plan_blk += 1
            blocked_slugs.add(rec["uni_slug"])
            continue
        key_legacy = f"{rec['uni_slug']}/{rec['year']}/{rec['season']}"
        already = (
            (not force_all)
            and snapshot_file_ok(lp)
            and lp not in overwrite_keys
            and key_legacy not in overwrite_keys
        )
        if already:
            n_skipped += 1
            continue
        if not force_all and lp not in overwrite_keys and key_legacy not in overwrite_keys:
            prev = last_by_lp.get(lp)
            if prev and _is_permanent_index_failure(prev) and not snapshot_file_ok(lp):
                n_perm_skip += 1
                continue
        if lp in seen_lp:
            n_plan_dup += 1
        else:
            seen_lp.add(lp)
            to_download.append(rec)

    print(f"  Plan total       : {len(plan):>6,}")
    print(f"  Blocked (plan)   : {n_plan_blk:>6,}  (failure sentinel: n_snaps=-1 with reason)")
    print(f"  Duplicate paths  : {n_plan_dup:>6,}  (same local_path repeated in plan — skipped)")
    print(f"  Slug filter skip : {n_slug_skip:>6,}  (not in WAYBACK_SLUGS)")
    print(f"  Permanent skip   : {n_perm_skip:>6,}  (last index failure; file still missing — set overwrite to retry)")
    if blocked_slugs:
        bs = ", ".join(sorted(blocked_slugs)[:10])
        more = f" (+{len(blocked_slugs) - 10} more)" if len(blocked_slugs) > 10 else ""
        print(f"                     {bs}{more}")
    print(f"  Already on disk  : {n_skipped:>6,}")
    print(f"  To download      : {len(to_download):>6,}")

    if not to_download:
        print("  Nothing to do — all snapshots already present or permanently skipped.")
        return

    n_ok = 0
    n_err = 0
    n_total = len(to_download)
    total_bytes = 0
    cur_uni = None
    uni_ok = 0
    uni_err = 0
    uni_bytes = 0
    uni_n_snaps = 0

    def fmt(b):
        if b < 1_048_576:
            return f"{b/1024:.1f} KB"
        if b < 1_073_741_824:
            return f"{b/1_048_576:.2f} MB"
        return f"{b/1_073_741_824:.2f} GB"

    snaps_per_uni = Counter(r["university"] for r in to_download)
    write_root_label = str(faculty_snapshots_write_root)

    from tqdm.auto import tqdm

    with open(index_path, "a", encoding="utf-8") as idx_f:
        for dl_i, rec in enumerate(tqdm(to_download, desc="Downloading", unit="snap"), start=1):
            out_path = resolve_faculty_snapshot_path(rec["local_path"], for_write=True).resolve()
            out_path.parent.mkdir(parents=True, exist_ok=True)

            if rec["university"] != cur_uni:
                if cur_uni is not None:
                    rate = 100 * uni_ok / (uni_ok + uni_err) if (uni_ok + uni_err) else 0
                    avg_kb = (uni_bytes / 1024 / uni_ok) if uni_ok else 0
                    print(
                        f"  └─ {cur_uni}:  {uni_ok}/{uni_n_snaps} OK  ({rate:.0f}%)  "
                        f"avg {avg_kb:.1f} KB/file  │  {fmt(uni_bytes)} this school",
                        flush=True,
                    )
                cur_uni = rec["university"]
                uni_ok = 0
                uni_err = 0
                uni_bytes = 0
                uni_n_snaps = snaps_per_uni[cur_uni]
                pct = 100 * (dl_i - 1) / n_total
                print(
                    f"\n  ── Now downloading: {cur_uni}  ({uni_n_snaps} snaps)"
                    f"  │  overall: {dl_i-1:,}/{n_total:,} ({pct:.1f}%)  {n_ok:,} ✓  {n_err} ✗  "
                    f"│  {fmt(total_bytes)} so far",
                    flush=True,
                )

            print(f"     {rec['year']} {rec['season']}  →  {rec['wayback_url']}", flush=True)

            http_status = -1
            file_size_bytes = 0
            error_msg = ""

            try:
                r = session.get(rec["wayback_url"], timeout=cdx_html_timeout)
                http_status = r.status_code

                if http_status == 429:
                    print("\n  WARNING: 429 rate limit — sleeping 60s then retrying", flush=True)
                    time.sleep(60)
                    r = session.get(rec["wayback_url"], timeout=cdx_html_timeout)
                    http_status = r.status_code

                if http_status == 200:
                    content = r.content
                    if len(content) < MIN_HTML_BYTES:
                        alt = _wayback_insert_id_modifier(rec["wayback_url"])
                        if alt != rec["wayback_url"]:
                            try:
                                r2 = session.get(alt, timeout=cdx_html_timeout)
                                if r2.status_code == 200 and len(r2.content) >= MIN_HTML_BYTES:
                                    r = r2
                                    content = r.content
                            except Exception:
                                pass
                    file_size_bytes = len(content)
                    if file_size_bytes >= MIN_HTML_BYTES:
                        rel_lp = faculty_snapshot_rel_from_local_path(rec["local_path"])
                        ws = (
                            (tenure_pipeline_dir / "faculty_snapshots" / rel_lp).resolve()
                            if rel_lp
                            else None
                        )
                        ok_write, err = _write_snapshot_html(
                            out_path,
                            content,
                            workspace_fallback=ws,
                            write_root_label=write_root_label,
                        )
                        if not ok_write:
                            error_msg = err or "verify failed"
                            n_err += 1
                            uni_err += 1
                            file_size_bytes = 0
                            print(
                                f"     ✗ {error_msg}  │  overall: {n_ok:,} ✓  {n_err} ✗  "
                                f"of {dl_i:,}/{n_total:,}",
                                flush=True,
                            )
                        else:
                            n_ok += 1
                            uni_ok += 1
                            uni_bytes += file_size_bytes
                            total_bytes += file_size_bytes
                            print(
                                f"     ✓ {file_size_bytes/1024:.1f} KB  │  {cur_uni[:30]}: "
                                f"{uni_ok}/{uni_n_snaps}  │  overall: {n_ok:,} ✓  {n_err} ✗  "
                                f"of {dl_i:,}/{n_total:,}  │  {fmt(total_bytes)} total",
                                flush=True,
                            )
                    else:
                        error_msg = (
                            f"too small ({file_size_bytes} bytes) — Wayback empty body; "
                            "pick another timestamp in 3A or capture may be gone"
                        )
                        n_err += 1
                        uni_err += 1
                        print(
                            f"     ✗ too small ({file_size_bytes}B)  │  overall: {n_ok:,} ✓  "
                            f"{n_err} ✗  of {dl_i:,}/{n_total:,}",
                            flush=True,
                        )
                else:
                    error_msg = f"HTTP {http_status}"
                    n_err += 1
                    uni_err += 1
                    print(
                        f"     ✗ HTTP {http_status}  │  overall: {n_ok:,} ✓  {n_err} ✗  "
                        f"of {dl_i:,}/{n_total:,}",
                        flush=True,
                    )

            except Exception as e:
                error_msg = str(e)[:80]
                n_err += 1
                uni_err += 1
                print(
                    f"     ✗ {str(e)[:60]}  │  overall: {n_ok:,} ✓  {n_err} ✗  "
                    f"of {dl_i:,}/{n_total:,}",
                    flush=True,
                )

            idx_f.write(
                json.dumps(
                    {
                        "university": rec["university"],
                        "uni_slug": rec["uni_slug"],
                        "year": rec["year"],
                        "season": rec["season"],
                        "timestamp": rec["timestamp"],
                        "source_url": rec["source_url"],
                        "wayback_url": rec["wayback_url"],
                        "local_path": rec["local_path"],
                        "http_status": http_status,
                        "file_size_bytes": file_size_bytes,
                        "error": error_msg,
                        "downloaded_at": datetime.now().isoformat(),
                    }
                )
                + "\n"
            )
            idx_f.flush()
            time.sleep(delay)

    if cur_uni is not None:
        rate = 100 * uni_ok / (uni_ok + uni_err) if (uni_ok + uni_err) else 0
        avg_kb = (uni_bytes / 1024 / uni_ok) if uni_ok else 0
        print(
            f"  └─ {cur_uni}:  {uni_ok}/{uni_n_snaps} OK  ({rate:.0f}%)  "
            f"avg {avg_kb:.1f} KB/file",
            flush=True,
        )

    print(f"\n  Downloaded OK    : {n_ok:>6,}  ({100*n_ok/n_total:.1f}%)")
    print(f"  Errors           : {n_err:>6,}  ({100*n_err/n_total:.1f}%)")
    print(f"  Total data       : {fmt(total_bytes)}")
    print(f"  Index            : {index_path.resolve()}")


def append_all_fail_sentinels(*, plan_path: Path, index_path: Path) -> None:
    """Append plan sentinels for universities with zero successful index rows (legacy behavior)."""
    if not index_path.is_file():
        return
    with open(index_path, encoding="utf-8") as idx_f:
        idx_recs = [json.loads(l) for l in idx_f if l.strip()]
    uni_ok: dict[str, int] = defaultdict(int)
    for ir in idx_recs:
        uni_ok[ir["university"]] += (
            1
            if ir.get("http_status") == 200 and ir.get("file_size_bytes", 0) >= MIN_HTML_BYTES
            else 0
        )
    with open(plan_path, encoding="utf-8") as pf:
        plan_recs = [json.loads(l) for l in pf if l.strip()]
    uni_pri: dict[str, str] = {}
    for pr in plan_recs:
        u = pr.get("university", "")
        if u and u not in uni_pri and pr.get("n_snaps", 1) > 0 and pr.get("plan_row_type") != "cdx_bookmark":
            uni_pri[u] = pr.get("source_url", "")
    planned_unis = {
        r["university"]
        for r in plan_recs
        if r.get("n_snaps", 1) > 0 and r.get("plan_row_type") != "cdx_bookmark"
    }
    all_fail = [u for u in planned_unis if uni_ok.get(u, 0) == 0]
    if not all_fail:
        return
    print(f"\n  Writing bad sentinels for {len(all_fail)} all-fail school(s) (zero OK rows in index ever):")
    with open(plan_path, "a", encoding="utf-8") as sf:
        for u in sorted(all_fail):
            slug = u.lower().replace(" ", "_").replace("-", "_").replace(",", "").replace(".", "")
            sentinel = {
                "university": u,
                "uni_slug": slug,
                "n_snaps": -1,
                "tried_primary_url": uni_pri.get(u, ""),
                "tried_urls": [],
                "queried_at": time.strftime("%Y-%m-%d"),
                "reason": "Cell 3B: all downloads failed (404/403/too-small)",
            }
            sf.write(json.dumps(sentinel) + "\n")
            print(f"    ⚠  {u}")


def run_stage3b_from_globals(g: dict) -> None:
    """Entry point after CELL 0 has populated ``g`` (notebook or CLI)."""
    import requests

    if not g.get("RUN_CELL3_DOWNLOAD"):
        return
    st3_plan = g["STAGE3_PLAN"]
    if not Path(st3_plan).exists():
        print(f"  ERROR: No download plan found at {st3_plan}")
        print("  Run CELL 3A first — set RUN_CELL3_CDX = True in CELL 0.")
        return

    clk = g["time_start"]("Stage 3B — Wayback HTML Download")
    session = requests.Session()
    session.headers.update(g["CDX_HEADERS"])

    try:
        html_dir = g["STAGE3_HTML_DIR"].resolve()
        if "Desktop" in str(html_dir):
            print("  NOTE: STAGE3_HTML_DIR is under Desktop (iCloud Desktop & Documents can break verify).")
    except Exception:
        pass

    download_plan(
        plan_path=Path(st3_plan),
        index_path=Path(g["STAGE3_INDEX"]),
        session=session,
        delay=g["CDX_DELAY"],
        overwrite=None,
        snapshot_file_ok=g["_snapshot_file_ok"],
        resolve_faculty_snapshot_path=g["resolve_faculty_snapshot_path"],
        faculty_snapshot_rel_from_local_path=g["_faculty_snapshot_rel_from_local_path"],
        tenure_pipeline_dir=Path(g["TENURE_PIPELINE_DIR"]),
        faculty_snapshots_write_root=Path(g["FACULTY_SNAPSHOTS_WRITE_ROOT"]),
        cdx_html_timeout=g["CDX_HTML_TIMEOUT"],
        wayback_slugs=g.get("WAYBACK_SLUGS"),
    )
    append_all_fail_sentinels(plan_path=Path(st3_plan), index_path=Path(g["STAGE3_INDEX"]))
    g["time_stop"](clk)
