"""
Canonical faculty URL normalization and snapshot path resolution (Cell 0 + apply_url_updates).
"""
from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

SNAPSHOT_LOCAL_PREFIX = "tenure/tenure_pipeline/faculty_snapshots"
LEGACY_SNAPSHOT_PREFIX = "tenure_pipeline/faculty_snapshots"

_WWW_PAIR = frozenset({"cse.msu.edu"})


def slugify(name: str) -> str:
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


make_slug = slugify


def normalize_faculty_url(u: str) -> str:
    u = (u or "").strip()
    if not u:
        return ""
    p = urlparse(u)
    if (p.hostname or "").lower() == "web.archive.org" and "/web/" in (p.path or ""):
        m = re.search(r"(https?://[^\s]+)", p.path or "")
        if m:
            u = m.group(1).rstrip("/")
            p = urlparse(u)
    host = (p.hostname or "").lower()
    if not host:
        return u
    if host in _WWW_PAIR:
        host = "www." + host
    path = p.path or "/"
    if path != "/" and not path.endswith("/"):
        path = path + "/"
    q = p.query or ""
    return f"{host}{path}{('?' + q) if q else ''}"


def faculty_source_id(url: str) -> str:
    nu = normalize_faculty_url(url)
    if not nu:
        return "unknown"
    return hashlib.sha256(nu.encode("utf-8")).hexdigest()[:8]


def faculty_snapshot_rel_from_local_path(
    local_path: str,
    *,
    snapshot_local_prefix: str = SNAPSHOT_LOCAL_PREFIX,
) -> str | None:
    lp = (local_path or "").replace("\\", "/").strip()
    new = snapshot_local_prefix + "/"
    legacy = LEGACY_SNAPSHOT_PREFIX + "/"
    if lp.startswith(new):
        return lp[len(new) :].lstrip("/")
    if lp.startswith(legacy):
        return lp[len(legacy) :].lstrip("/")
    return None


def normalize_wayback_slug_filter(slugs) -> set[str] | None:
    """None = no filter (all schools). Accept str, list, set, or None."""
    if slugs is None or slugs is False:
        return None
    if isinstance(slugs, str):
        s = slugs.strip()
        return {s} if s else None
    out = {str(s).strip() for s in slugs if str(s).strip()}
    return out if out else None


@dataclass
class SnapshotPathContext:
    workspace_root: Path
    tenure_pipeline_dir: Path
    faculty_snapshots_write_root: Path
    stage3_html_dir: Path
    snapshot_local_prefix: str = SNAPSHOT_LOCAL_PREFIX

    def search_roots(self) -> list[Path]:
        roots: list[Path] = []
        seen: set[Path] = set()
        for d in (
            self.faculty_snapshots_write_root,
            self.stage3_html_dir,
            self.tenure_pipeline_dir / "faculty_snapshots",
            self.workspace_root / "tenure_pipeline" / "faculty_snapshots",
            Path.home() / "Desktop" / "faculty_snapshots",
        ):
            try:
                r = d.resolve()
            except OSError:
                continue
            if r not in seen:
                seen.add(r)
                roots.append(r)
        return roots

    def resolve(self, local_path: str, *, for_write: bool = False) -> Path:
        lp = (local_path or "").replace("\\", "/").strip()
        rel = faculty_snapshot_rel_from_local_path(lp, snapshot_local_prefix=self.snapshot_local_prefix)
        if rel is None:
            return (self.workspace_root / lp).resolve()
        primary = (self.stage3_html_dir / rel).resolve()
        if for_write:
            return (self.faculty_snapshots_write_root / rel).resolve()
        for root in self.search_roots():
            p = (root / rel).resolve()
            if p.is_file():
                return p
        return primary

    def disk_html_to_plan_local_path(self, html_path: Path) -> str:
        html_path = html_path.resolve()
        for root in self.search_roots():
            try:
                rel = html_path.relative_to(root)
                return f"{self.snapshot_local_prefix}/{rel.as_posix()}"
            except ValueError:
                continue
        return html_path.relative_to(self.workspace_root).as_posix()

    def iter_slugs_with_html(self) -> list[str]:
        seen: set[str] = set()
        for root in self.search_roots():
            if not root.is_dir():
                continue
            for d in root.iterdir():
                if not d.is_dir():
                    continue
                if any(d.rglob("*.html")):
                    seen.add(d.name)
        return sorted(seen)

    def school_html_dir(self, uni_slug: str) -> Path | None:
        """First existing directory for uni_slug among search roots."""
        for root in self.search_roots():
            p = root / uni_slug
            if p.is_dir():
                return p
        return self.stage3_html_dir / uni_slug


def snapshot_path_context_from_globals(g: dict) -> SnapshotPathContext:
    return SnapshotPathContext(
        workspace_root=Path(g["WORKSPACE_ROOT"]),
        tenure_pipeline_dir=Path(g["TENURE_PIPELINE_DIR"]),
        faculty_snapshots_write_root=Path(g["FACULTY_SNAPSHOTS_WRITE_ROOT"]),
        stage3_html_dir=Path(g["STAGE3_HTML_DIR"]),
        snapshot_local_prefix=g.get("SNAPSHOT_LOCAL_PREFIX", SNAPSHOT_LOCAL_PREFIX),
    )
