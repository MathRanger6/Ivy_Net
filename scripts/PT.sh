#!/bin/bash
set -euo pipefail
_SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_WORKSPACE_ROOT="$(cd "$_SCRIPTS_DIR/.." && pwd)"
cd "$_WORKSPACE_ROOT" || exit 1

python 1-Various_PDE_and_Chat_stuff/3-reference_documents/convert_to_googledocs.py 1-Various_PDE_and_Chat_stuff/3-reference_documents/Pertinent_Thoughts.md
