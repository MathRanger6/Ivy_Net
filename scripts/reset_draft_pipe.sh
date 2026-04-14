#!/bin/bash
set -euo pipefail
_SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_WORKSPACE_ROOT="$(cd "$_SCRIPTS_DIR/.." && pwd)"
cd "$_WORKSPACE_ROOT" || exit 1

rm ./datasets/mbb/exports_inverted_u_v0/*.*