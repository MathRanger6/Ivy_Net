"""Canonical paths for Army BDP / HERO / data-story outputs."""

from __future__ import annotations

from pathlib import Path

# talent/re_entry/ → repo root is parents[2]
_RE_ENTRY = Path(__file__).resolve().parent
REPO = _RE_ENTRY.parents[2]

# Local working outputs (AWS default write target)
ARMY_RE_ENTRY = _RE_ENTRY
OUTPUT_ROOT = ARMY_RE_ENTRY / "output"
BASIC_DATA_PLOTS = OUTPUT_ROOT / "basic_data_plots"
HERO_DIR = OUTPUT_ROOT / "hero"
ACT2_DIR = OUTPUT_ROOT / "act2"
DATA_STORY_DIR = OUTPUT_ROOT / "data_story"

# Repo canonical home (sync PNGs here after AWS for flipbook / git)
HEROS_AND_PASSES = REPO / "3-Master_Plan" / "re_entry" / "HEROs_and_PASSes"
ARMY_SANDBOX = HEROS_AND_PASSES / "army_sandbox"
ARMY_SANDBOX_BDP = ARMY_SANDBOX / "basic_data_plots"
ARMY_SANDBOX_HERO = ARMY_SANDBOX / "hero"
ARMY_SANDBOX_ACT2 = ARMY_SANDBOX / "act2"
ARMY_SANDBOX_DATA_STORY = ARMY_SANDBOX / "data_story"

MANIFEST_RUN1 = ARMY_RE_ENTRY / "manifests" / "army_run1_3x3_manifest.json"

PREFIX = "ARMY"
TAG_RUN1 = "run1"


def ensure_army_output_dirs() -> None:
    for d in (
        BASIC_DATA_PLOTS,
        HERO_DIR,
        ACT2_DIR,
        DATA_STORY_DIR,
        ARMY_SANDBOX_BDP,
        ARMY_SANDBOX_HERO,
        ARMY_SANDBOX_ACT2,
        ARMY_SANDBOX_DATA_STORY,
    ):
        d.mkdir(parents=True, exist_ok=True)


def default_feather_candidates() -> list[Path]:
    """Search order: AWS cwd (talent_pipeline) then repo-local feather."""
    return [
        Path.cwd() / "running_vars" / "df_pipeline_11_cox_analysis.feather",
        REPO / "talent" / "talent_pipeline" / "running_vars" / "df_pipeline_11_cox_analysis.feather",
        REPO / "talent_pipeline" / "running_vars" / "df_pipeline_11_cox_analysis.feather",
    ]


def resolve_feather(explicit: Path | None = None) -> Path:
    if explicit is not None:
        p = explicit.expanduser().resolve()
        if not p.is_file():
            raise FileNotFoundError(p)
        return p
    for cand in default_feather_candidates():
        if cand.is_file():
            return cand.resolve()
    tried = "\n  ".join(str(c) for c in default_feather_candidates())
    raise FileNotFoundError(
        "No df_pipeline_11_cox_analysis.feather found. Run 520 through Cell 11 first.\n"
        f"Tried:\n  {tried}"
    )
