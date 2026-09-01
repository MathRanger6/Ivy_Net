#!/bin/bash
# One-time (or post-migration) setup: Playwright Chromium for convert_single_md_to_pdf.sh on Mac.
# Run from repo root after conda activate sports_net (or tenure_net).
#
# Usage: ./scripts/setup_playwright_pdf_mac.sh
#
# Installs browsers to ~/Library/Caches/ms-playwright/ (same as old Mac). Not in git/Dropbox.

set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=generate_pdf_playwright.sh
source /dev/null 2>/dev/null || true

init_conda_shell() {
    if [[ -f /opt/anaconda3/etc/profile.d/conda.sh ]]; then
        # shellcheck source=/dev/null
        source /opt/anaconda3/etc/profile.d/conda.sh
        return 0
    fi
    return 1
}

if [[ -z "${CONDA_PREFIX:-}" ]] || [[ ! -x "${CONDA_PREFIX}/bin/python" ]]; then
    if init_conda_shell; then
        if conda env list | awk '{print $1}' | grep -qx 'sports_net'; then
            conda activate sports_net
        elif conda env list | awk '{print $1}' | grep -qx 'tenure_net'; then
            conda activate tenure_net
        else
            echo "❌ Activate sports_net or tenure_net first."
            exit 1
        fi
    else
        echo "❌ conda not found. Run: conda activate sports_net"
        exit 1
    fi
fi

PY="${CONDA_PREFIX}/bin/python"
echo "▶ Installing Playwright Chromium for PDF conversion"
echo "   Python: $PY"
"$PY" -m pip show playwright >/dev/null 2>&1 || {
    echo "❌ playwright package missing in this env. Run: pip install playwright"
    exit 1
}
"$PY" -m playwright install chromium

echo ""
echo "✅ Done. Test:"
echo "   ./scripts/convert_single_md_to_pdf.sh 3-Master_Plan/re_entry/03_Three_Day_Basketball_Focus.md"
echo ""
echo "Browsers live in: ~/Library/Caches/ms-playwright/"
