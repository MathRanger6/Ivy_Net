#!/usr/bin/env bash
# Sync large / gitignored data between Mac (Dropbox) and Rivanna.
#
# *** RUN ON YOUR MAC, NOT ON RIVANNA ***
#   to-hpc    = Mac → Rivanna
#   from-hpc  = Rivanna → Mac
#   unzip     = Mac only (no SSH; unzips git-tracked .zip archives)
#
# Catalog: scripts/BIG_DATA_MANIFEST.md
# Policy:  scripts/DATA_SYNC.md §4b
#
# Usage (Mac terminal):
#   ./scripts/pull_big_data.sh unzip
#   ./scripts/pull_big_data.sh to-hpc big-fish      # LoL + football (~250 MB)
#   ./scripts/pull_big_data.sh to-hpc datasets      # all datasets/ big trees (~7+ GB)
#   ./scripts/pull_big_data.sh to-hpc all           # datasets + tenure (+ sweep on from-hpc only)
#   ./scripts/pull_big_data.sh from-hpc tenure
#   ./scripts/pull_big_data.sh list-scopes
#   ./scripts/pull_big_data.sh --help
#
# Scopes: all | datasets | big-fish | education | apache | mbb | tenure | sweep
#
# Dry run:  DRY_RUN=1 ./scripts/pull_big_data.sh to-hpc big-fish

set -euo pipefail

IVY_NET_SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=rsync_hpc_include.sh
source "${IVY_NET_SCRIPTS_DIR}/rsync_hpc_include.sh"

_usage() {
  cat <<'EOF'
Sync large / gitignored data (Mac ↔ Rivanna over SSH).

RUN ON MAC ONLY — not on Rivanna login nodes.

Commands:
  unzip              Unzip Big Fish .zip → working CSV paths (no SSH)
  to-hpc [scope]     Mac → Rivanna  (default scope: datasets)
  from-hpc [scope]   Rivanna → Mac  (default scope: datasets)

Scopes:
  all        datasets + tenure (+ sweep when from-hpc)  [10 GB+]
  datasets   big-fish + education + apache + mbb under datasets/
  big-fish   LoL + football unzipped CSVs (~250 MB)
  education  nels88 + hsb80
  apache     Apache OSS Big Fish panel
  mbb        datasets/mbb bulk (~7 GB)
  tenure     tenure/tenure_pipeline panels (excl. HTML snapshots)
  sweep      sports simulation sweep outputs

Examples:
  ./scripts/pull_big_data.sh to-hpc big-fish
  ./scripts/pull_big_data.sh to-hpc datasets
  ./scripts/pull_big_data.sh from-hpc all

Full inventory: scripts/BIG_DATA_MANIFEST.md
EOF
}

_list_scopes() {
  awk '/^\| Scope \||^\|-------|^\| \*\*`all`\*\*/ {print}' "${IVY_NET_SCRIPTS_DIR}/BIG_DATA_MANIFEST.md"
}

main() {
  local cmd="${1:-unzip}"
  local scope="${2:-datasets}"

  case "${cmd}" in
    -h|--help|help)
      _usage
      exit 0
      ;;
    list-scopes|scopes)
      _list_scopes
      exit 0
      ;;
    unzip|local)
      ivy_unzip_big_fish
      ;;
    from-hpc|pull-hpc|pull)
      ivy_rsync_sync_big_data pull "${scope}"
      ;;
    to-hpc|push-hpc|push)
      ivy_rsync_sync_big_data push "${scope}"
      ;;
    *)
      echo "Unknown command: ${cmd}" >&2
      _usage >&2
      exit 1
      ;;
  esac
}

main "$@"
