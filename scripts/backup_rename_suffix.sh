#!/usr/bin/env bash
# Rename output files with a suffix and move them into a matching subfolder.
#
# Example (suffix _o_snr in ./talent/re_entry/output/hero):
#   plot.png  ->  ./talent/re_entry/output/hero/o_snr/plot_o_snr.png
#
# Suffix may include a leading underscore (_o_snr) or not (21s -> _21s in filenames).
# Subfolder name = suffix with leading underscores stripped (_o_snr -> o_snr).
#
# Options:
#   --all-output  Process all Army re_entry output folders (basic_data_plots, hero, act2, data_story)
#   --dry-run     Print moves without renaming
#   --include-dot Also rename hidden files (default: skip dotfiles)
#   --in-place    Old behavior: rename in the same directory (no subfolder)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DEFAULT_OUTPUT_ROOT="$REPO_ROOT/talent/re_entry/output"
ARMY_OUTPUT_DIRS=(basic_data_plots hero act2 data_story)

usage() {
  cat <<'EOF'
Usage: backup_rename_suffix.sh [SUFFIX] [DIRECTORY] [OPTIONS]

Default: create SUBFOLDER inside DIRECTORY, rename each file with SUFFIX, move there.
  SUBFOLDER = SUFFIX with leading "_" stripped  (e.g. _o_snr -> o_snr)

If SUFFIX or DIRECTORY is omitted, the script prompts interactively.

Options:
  --all-output  Run on all Army output folders under talent/re_entry/output/
  --dry-run     Preview without moving files
  --include-dot Include hidden files
  --in-place    Legacy: rename in place (no subfolder; not with --all-output)

Examples:
  backup_rename_suffix.sh _o_snr --all-output
  backup_rename_suffix.sh _o_snr --all-output --dry-run
  backup_rename_suffix.sh _o_snr talent/re_entry/output/hero
  backup_rename_suffix.sh                    # prompts for suffix + directory
  backup_rename_suffix.sh 21s talent/re_entry --in-place
EOF
}

dry_run=0
include_dot=0
in_place=0
all_output=0
suffix=""
target_dir=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --dry-run)
      dry_run=1
      shift
      ;;
    --include-dot)
      include_dot=1
      shift
      ;;
    --in-place)
      in_place=1
      shift
      ;;
    --all-output)
      all_output=1
      shift
      ;;
    -*)
      echo "ERROR: Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      if [[ -z "$suffix" ]]; then
        suffix="$1"
      elif [[ -z "$target_dir" ]]; then
        target_dir="$1"
      else
        echo "ERROR: Unexpected argument: $1" >&2
        usage >&2
        exit 1
      fi
      shift
      ;;
  esac
done

if [[ "$all_output" -eq 1 && "$in_place" -eq 1 ]]; then
  echo "ERROR: --all-output cannot be used with --in-place." >&2
  exit 1
fi

if [[ -z "$suffix" ]]; then
  read -r -p "Suffix to insert before extension (e.g. _o_snr): " suffix
fi

if [[ "$all_output" -eq 0 && -z "$target_dir" ]]; then
  read -r -p "Output directory [.]: " target_dir
  target_dir="${target_dir:-.}"
fi

if [[ -z "$suffix" ]]; then
  echo "ERROR: SUFFIX is required." >&2
  usage >&2
  exit 1
fi

if [[ "$suffix" == */* ]]; then
  echo "ERROR: SUFFIX must not contain '/'." >&2
  exit 1
fi

# Filename insert: _o_snr stays as-is; 21s becomes _21s (backward compatible).
insert_suffix() {
  if [[ "$suffix" == _* ]]; then
    printf '%s' "$suffix"
  else
    printf '_%s' "$suffix"
  fi
}

# Subfolder label: _run1_legacy -> run1_legacy
subfolder_from_suffix() {
  local name="${suffix#_}"
  if [[ -z "$name" ]]; then
    echo "ERROR: SUFFIX must be like _run1_legacy (got: $suffix)" >&2
    exit 1
  fi
  printf '%s' "$name"
}

new_name() {
  local base="$1"
  local insert
  insert="$(insert_suffix)"
  if [[ "$base" == *.* && "$base" != .*.* ]]; then
    printf '%s%s.%s' "${base%.*}" "$insert" "${base##*.}"
  elif [[ "$base" == .* && "$base" == *.* ]]; then
    local stem="${base#.*}"
    stem="${base%.${stem}}"
    printf '%s%s.%s' "$stem" "$insert" "${base##*.}"
  else
    printf '%s%s' "$base" "$insert"
  fi
}

process_directory() {
  # Do not use global target_dir here (CLI sets target_dir="" at top level).
  if [[ ! -d "$1" ]]; then
    echo "WARN: skipping missing directory: $1" >&2
    return 0
  fi

  local src_dir label insert dest_subdir dest_dir
  src_dir="$(cd "$1" && pwd)"
  label="${2:-$(basename "$src_dir")}"
  insert="$(insert_suffix)"

  if [[ "$in_place" -eq 0 ]]; then
    dest_subdir="$(subfolder_from_suffix)"
    dest_dir="$src_dir/$dest_subdir"
    if [[ "$dry_run" -eq 1 ]]; then
      echo "DRY-RUN: would create subfolder: $dest_dir"
    else
      mkdir -p -- "$dest_dir"
      echo "Subfolder: $dest_dir"
    fi
  else
    dest_subdir=""
    dest_dir="$src_dir"
  fi

  shopt -s nullglob
  local entries
  if [[ "$include_dot" -eq 1 ]]; then
    entries=("$src_dir"/* "$src_dir"/.[!.]* "$src_dir"/..?*)
  else
    entries=("$src_dir"/*)
  fi

  local renamed=0 skipped=0 path base dest_name dest_path

  for path in "${entries[@]}"; do
    [[ -e "$path" ]] || continue
    [[ -f "$path" ]] || continue

    base="$(basename "$path")"

    if [[ "$in_place" -eq 0 && -n "$dest_subdir" && "$base" == "$dest_subdir" ]]; then
      continue
    fi

    dest_name="$(new_name "$base")"
    dest_path="$dest_dir/$dest_name"

    if [[ -e "$dest_path" ]]; then
      echo "SKIP (exists): [$label] $base -> $dest_subdir/$dest_name" >&2
      skipped=$((skipped + 1))
      continue
    fi

    if [[ "$dry_run" -eq 1 ]]; then
      if [[ "$in_place" -eq 1 ]]; then
        echo "DRY-RUN: [$label] $base -> $dest_name"
      else
        echo "DRY-RUN: [$label] $base -> $dest_subdir/$dest_name"
      fi
    else
      mv -- "$path" "$dest_path"
      if [[ "$in_place" -eq 1 ]]; then
        echo "[$label] $base -> $dest_name"
      else
        echo "[$label] $base -> $dest_subdir/$dest_name"
      fi
    fi
    renamed=$((renamed + 1))
  done

  if [[ "$in_place" -eq 1 ]]; then
    echo "Done [$label]. Renamed: $renamed  Skipped: $skipped  Dir: $src_dir  Insert: ${insert}"
  else
    echo "Done [$label]. Moved: $renamed  Skipped: $skipped  Source: $src_dir  Dest: $dest_subdir/  Insert: ${insert}"
  fi

  TOTAL_RENAMED=$((TOTAL_RENAMED + renamed))
  TOTAL_SKIPPED=$((TOTAL_SKIPPED + skipped))
  DIRS_PROCESSED=$((DIRS_PROCESSED + 1))
}

TOTAL_RENAMED=0
TOTAL_SKIPPED=0
DIRS_PROCESSED=0

if [[ "$all_output" -eq 1 ]]; then
  echo "Army output root: $DEFAULT_OUTPUT_ROOT"
  echo "Suffix: $suffix  ->  subfolder in each dir: $(subfolder_from_suffix)/"
  echo "(Do not use --in-place; default moves files into that subfolder with suffix in filename.)"
  echo "---"
  for sub in "${ARMY_OUTPUT_DIRS[@]}"; do
    process_directory "$DEFAULT_OUTPUT_ROOT/$sub" "$sub"
    echo "---"
  done
  echo "All output folders. Dirs processed: $DIRS_PROCESSED  Total moved: $TOTAL_RENAMED  Total skipped: $TOTAL_SKIPPED"
else
  if [[ ! -d "$target_dir" ]]; then
    echo "ERROR: Not a directory: $target_dir" >&2
    exit 1
  fi
  process_directory "$target_dir"
fi
