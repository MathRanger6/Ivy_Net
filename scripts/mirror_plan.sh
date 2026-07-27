#!/usr/bin/env bash
# Mirror a Cursor Plan-mode file from ~/.cursor/plans/ into the repo.
#
# Usage:
#   ./scripts/mirror_plan.sh <slug>              # e.g. hero_model_reset
#   ./scripts/mirror_plan.sh <slug> --force      # mirror even if slug looks ephemeral
#   ./scripts/mirror_plan.sh <slug> --new        # new dated filename even if mirror exists
#   ./scripts/mirror_plan.sh --list              # show global plans + mirror status
#   ./scripts/mirror_plan.sh /path/to/foo.plan.md
#
# Repo destination: 3-Master_Plan/plans/YYYYMMDD_<slug>.plan.md
# Reuses an existing *_<slug>.plan.md name when present (unless --new).
#
# PDF (Charles, local):
#   ./scripts/convert_single_md_to_pdf.sh 3-Master_Plan/plans/YYYYMMDD_<slug>.plan.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
GLOBAL_PLANS="${CURSOR_PLANS_DIR:-$HOME/.cursor/plans}"
DEST_DIR="$REPO_ROOT/3-Master_Plan/plans"

# Slug prefixes that are usually throwaway (override with --force).
EPHEMERAL_RE='^(fix_|plans_git_)'

usage() {
  sed -n '2,16p' "$0" | sed 's/^# \?//'
  exit "${1:-0}"
}

slug_from_basename() {
  local base="$1"
  base="${base%.plan.md}"
  if [[ "$base" =~ ^(.+)_[a-f0-9]{8}$ ]]; then
    echo "${BASH_REMATCH[1]}"
  else
    echo "$base"
  fi
}

find_global_plan() {
  local slug="$1"
  local candidate

  if [[ -f "$slug" ]]; then
    echo "$slug"
    return 0
  fi

  if [[ -f "$GLOBAL_PLANS/${slug}.plan.md" ]]; then
    echo "$GLOBAL_PLANS/${slug}.plan.md"
    return 0
  fi

  candidate="$(find "$GLOBAL_PLANS" -maxdepth 1 -name "${slug}_*.plan.md" 2>/dev/null | head -1)"
  if [[ -n "$candidate" && -f "$candidate" ]]; then
    echo "$candidate"
    return 0
  fi

  return 1
}

find_repo_mirror() {
  local slug="$1"
  find "$DEST_DIR" -maxdepth 1 -name "*_${slug}.plan.md" 2>/dev/null | head -1
}

is_ephemeral_slug() {
  local slug="$1"
  [[ "$slug" =~ $EPHEMERAL_RE ]]
}

list_plans() {
  echo "Global plans: $GLOBAL_PLANS"
  echo "Repo mirrors: $DEST_DIR"
  echo ""
  printf "%-36s %-8s %s\n" "GLOBAL" "MIRROR" "SLUG"
  printf "%-36s %-8s %s\n" "------" "------" "----"
  local f slug mirror ephem
  shopt -s nullglob
  for f in "$GLOBAL_PLANS"/*.plan.md; do
    [[ -f "$f" ]] || continue
    slug="$(slug_from_basename "$(basename "$f")")"
    mirror="$(find_repo_mirror "$slug")"
    if [[ -n "$mirror" ]]; then
      printf "%-36s %-8s %s\n" "$(basename "$f")" "yes" "$slug"
    else
      ephem=""
      is_ephemeral_slug "$slug" && ephem=" (ephemeral?)"
      printf "%-36s %-8s %s%s\n" "$(basename "$f")" "no" "$slug" "$ephem"
    fi
  done
}

mirror_plan() {
  local slug="$1"
  local force="${2:-false}"
  local new_file="${3:-false}"
  local src dest existing

  if ! src="$(find_global_plan "$slug")"; then
    echo "ERROR: No plan found for slug/path: $slug" >&2
    echo "  Looked in: $GLOBAL_PLANS" >&2
    exit 1
  fi

  slug="$(slug_from_basename "$(basename "$src")")"

  if [[ "$force" != "true" ]] && is_ephemeral_slug "$slug"; then
    echo "SKIP: '$slug' looks ephemeral (fix_* / plans_git_*). Use --force to mirror anyway." >&2
    exit 2
  fi

  mkdir -p "$DEST_DIR"

  existing="$(find_repo_mirror "$slug")"
  if [[ -n "$existing" && "$new_file" != "true" ]]; then
    dest="$existing"
  else
    dest="$DEST_DIR/$(date '+%Y%m%d')_${slug}.plan.md"
  fi

  cp "$src" "$dest"
  echo "Mirrored:"
  echo "  from: $src"
  echo "  to:   $dest"
  echo ""
  echo "PDF:  ./scripts/convert_single_md_to_pdf.sh \"$dest\""
}

main() {
  local force=false new_file=false

  if [[ $# -eq 0 ]]; then
    usage 1
  fi

  case "${1:-}" in
    -h|--help)
      usage 0
      ;;
    --list)
      list_plans
      exit 0
      ;;
  esac

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --force) force=true; shift ;;
      --new) new_file=true; shift ;;
      -h|--help) usage 0 ;;
      *)
        mirror_plan "$1" "$force" "$new_file"
        exit 0
        ;;
    esac
  done
}

main "$@"
