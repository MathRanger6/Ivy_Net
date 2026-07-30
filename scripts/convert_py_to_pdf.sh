#!/bin/bash
# Convert a .py (or other source) file to a syntax-colored PDF via Pygments + Playwright.
#
# Default path (option 2 from the re-entry discussion):
#   1) Pygments → standalone HTML with language colors
#   2) Playwright Chromium → PDF (print_background=True keeps token colors)
#
# Usage:
#   ./scripts/convert_py_to_pdf.sh <input.py> [output.pdf]
#   ./scripts/convert_py_to_pdf.sh sports/tier1_pool_assignment.py
#   ./scripts/convert_py_to_pdf.sh sports/tier1_sim_config.py /tmp/sim_config.pdf --style friendly
#
# Options:
#   --style NAME     Pygments style (default: default). Examples: friendly, monokai, vs, xcode
#   --lexer NAME     Force lexer (default: python). Examples: python, python3, bash
#   --no-linenos     Omit line numbers
#   --keep-html      Keep the intermediate .html next to the PDF
#   -h | --help
#
# Environment:
#   IVY_NET_PDF_ENV=sports_net   — conda env (default: sports_net if present)
#   IVY_NET_CHROMIUM_PATH=...    — optional browser binary for Playwright
#   IVY_NET_USE_SYSTEM_CHROME=1 — allow /Applications/Google Chrome.app (OFF by default;
#                                 launching system Chrome from Cursor can pop macOS
#                                 “Problem Report for Google Chrome” dialogs)
#
# Run this from Terminal (your machine), not from the agent sandbox — same habit as
# convert_single_md_to_pdf.sh. Prefer sports_net / tenure_net / talent_net; do not
# assume the agent’s plain python3 has playwright.
#
# Browser preference: Playwright’s own Chromium first (does not touch Chrome.app).
#
set -euo pipefail

STYLE="default"
LEXER="python"
LINENOS=1
KEEP_HTML=false
POSITIONAL=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --style)
            STYLE="${2:?--style requires a name}"
            shift 2
            ;;
        --lexer)
            LEXER="${2:?--lexer requires a name}"
            shift 2
            ;;
        --no-linenos)
            LINENOS=0
            shift
            ;;
        --keep-html)
            KEEP_HTML=true
            shift
            ;;
        -h|--help)
            sed -n '2,28p' "$0" | sed 's/^# \?//'
            exit 0
            ;;
        *)
            POSITIONAL+=("$1")
            shift
            ;;
    esac
done

INPUT_FILE="${POSITIONAL[0]:-}"
OUTPUT_FILE="${POSITIONAL[1]:-}"

if [[ -z "$INPUT_FILE" ]]; then
    echo "❌ Error: input source file is required"
    echo "Usage: ./scripts/convert_py_to_pdf.sh <input.py> [output.pdf] [--style friendly] [--keep-html]"
    exit 1
fi

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPTS_DIR/.." && pwd)"
cd "$WORKSPACE_DIR" || exit 1

# Resolve input path (allow paths relative to cwd or workspace)
if [[ ! -f "$INPUT_FILE" ]]; then
    if [[ -f "$WORKSPACE_DIR/$INPUT_FILE" ]]; then
        INPUT_FILE="$WORKSPACE_DIR/$INPUT_FILE"
    else
        echo "❌ Error: input file not found: $INPUT_FILE"
        exit 1
    fi
fi
INPUT_FILE="$(cd "$(dirname "$INPUT_FILE")" && pwd)/$(basename "$INPUT_FILE")"

if [[ -z "$OUTPUT_FILE" ]]; then
    OUTPUT_FILE="${INPUT_FILE%.*}.pdf"
elif [[ "$OUTPUT_FILE" != /* ]]; then
    OUTPUT_FILE="$WORKSPACE_DIR/$OUTPUT_FILE"
fi

HTML_FILE="${OUTPUT_FILE%.pdf}.html"
TITLE_REL="${INPUT_FILE#"$WORKSPACE_DIR"/}"
if [[ "$TITLE_REL" == "$INPUT_FILE" ]]; then
    TITLE_REL="$(basename "$INPUT_FILE")"
fi

# --- Activate conda (same preference order as generate_pdf_playwright.sh) -----
init_conda_shell() {
    if [[ -f /opt/anaconda3/etc/profile.d/conda.sh ]]; then
        # shellcheck source=/dev/null
        source /opt/anaconda3/etc/profile.d/conda.sh
        return 0
    fi
    for _conda_sh in "${HOME}/miniforge3/etc/profile.d/conda.sh" \
                     "${HOME}/.conda/etc/profile.d/conda.sh"; do
        if [[ -f "$_conda_sh" ]]; then
            # shellcheck source=/dev/null
            source "$_conda_sh"
            return 0
        fi
    done
    if command -v conda >/dev/null 2>&1; then
        eval "$(conda shell.bash hook)"
        return 0
    fi
    return 1
}

CONDA_PYTHON=""
if [[ "${IVY_NET_PDF_FORCE_ACTIVATE:-}" != "1" && -n "${CONDA_PREFIX:-}" && -x "${CONDA_PREFIX}/bin/python" ]]; then
    case "${CONDA_DEFAULT_ENV:-}" in
        sports_net|tenure_net|talent_net)
            echo "Using already-activated conda: ${CONDA_PREFIX}"
            CONDA_PYTHON="${CONDA_PREFIX}/bin/python"
            ;;
    esac
fi

if [[ -z "$CONDA_PYTHON" ]]; then
    if ! init_conda_shell; then
        echo "❌ Error: conda not found. On Rivanna: module load miniforge && re-run."
        exit 1
    fi
    if [[ -n "${IVY_NET_PDF_ENV:-}" ]]; then
        conda activate "${IVY_NET_PDF_ENV}"
    elif conda env list | awk '{print $1}' | grep -qx 'sports_net'; then
        conda activate sports_net
    elif conda env list | awk '{print $1}' | grep -qx 'tenure_net'; then
        conda activate tenure_net
    elif conda env list | awk '{print $1}' | grep -qx 'talent_net'; then
        conda activate talent_net
    else
        echo "❌ Error: No sports_net, tenure_net, or talent_net env. Set IVY_NET_PDF_ENV."
        exit 1
    fi
    CONDA_PYTHON="${CONDA_PREFIX}/bin/python"
fi

echo "Python: $CONDA_PYTHON  (env: ${CONDA_DEFAULT_ENV:-unknown})"
echo "▶ Pygments ($LEXER, style=$STYLE) → HTML → Playwright PDF"
echo "   in:  $INPUT_FILE"
echo "   out: $OUTPUT_FILE"

# --- Step 1: Pygments HTML (full document embeds token CSS) -------------------
"$CONDA_PYTHON" - "$INPUT_FILE" "$HTML_FILE" "$TITLE_REL" "$STYLE" "$LEXER" "$LINENOS" <<'PY'
import sys
from pathlib import Path

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename

src_path = Path(sys.argv[1])
html_path = Path(sys.argv[2])
title = sys.argv[3]
style = sys.argv[4]
lexer_name = sys.argv[5]
linenos = sys.argv[6] == "1"

code = src_path.read_text(encoding="utf-8")
try:
    lexer = get_lexer_by_name(lexer_name)
except Exception:
    lexer = guess_lexer_for_filename(src_path.name, code)

formatter = HtmlFormatter(
    full=True,
    style=style,
    linenos="table" if linenos else False,
    lineanchors="L",
    wrapcode=True,
    title=title,
)

body = highlight(code, lexer, formatter)
# Print-friendly extras (Pygments already injected its style block).
extra = f"""
<style type="text/css">
/* Dense code print: narrow margins + small mono so more of each line fits. */
@page {{ size: Letter; margin: 0.25in; }}
body {{ margin: 0; font-size: 8pt; line-height: 1.15; }}
h1 {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  font-size: 10pt;
  font-weight: 600;
  margin: 0 0 0.45em 0;
  color: #222;
}}
/* Wrap long CODE lines only — never wrap the linenos column (else 10 → 1\\n0). */
td.linenos {{
  vertical-align: top;
  padding-right: 0.45em;
  min-width: 2.8em;
  width: 2.8em;
}}
td.linenos pre {{
  white-space: pre !important;
  word-wrap: normal !important;
  overflow-wrap: normal !important;
  word-break: keep-all !important;
  font-size: 8pt;
  line-height: 1.15;
}}
td.code {{ width: 100%; }}
td.code pre {{
  white-space: pre-wrap !important;
  word-wrap: break-word;
  overflow-wrap: anywhere;
  font-size: 8pt;
  line-height: 1.15;
}}
div.highlight {{ font-size: 8pt; }}
</style>
"""
if "<body>" in body:
    # HtmlFormatter(full=True, title=...) only sets <title>; one visible H1 is enough.
    body = body.replace("<body>", "<body>\n" + extra + f"<h1>{title}</h1>\n", 1)
else:
    body = extra + f"<h1>{title}</h1>\n" + body

html_path.write_text(body, encoding="utf-8")
print(f"✅ HTML written: {html_path} ({html_path.stat().st_size:,} bytes)")
PY

# --- Step 2: Playwright HTML → PDF -------------------------------------------
"$CONDA_PYTHON" - "$HTML_FILE" "$OUTPUT_FILE" <<'PY'
import os
import sys
from pathlib import Path

html_file = Path(sys.argv[1]).resolve()
pdf_file = Path(sys.argv[2]).resolve()

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ Playwright not installed for this Python:")
    print(f"   {sys.executable}")
    print("   Check conda envs first (sports_net / tenure_net / talent_net), e.g.:")
    print("   conda activate sports_net && python -c 'import playwright'")
    print(f"   {sys.executable} -m pip install playwright")
    print(f"   {sys.executable} -m playwright install chromium")
    sys.exit(1)


def launch_browser(p):
    """Prefer Playwright’s bundled Chromium — do NOT grab Google Chrome.app by default.

    Launching /Applications/Google Chrome.app from Cursor/agent has produced macOS
    “Problem Report for Google Chrome” (SIGABRT) dialogs. Opt in only via
    IVY_NET_CHROMIUM_PATH or IVY_NET_USE_SYSTEM_CHROME=1.
    """
    errors = []

    # 1) Explicit path wins
    env_chrome = os.environ.get("IVY_NET_CHROMIUM_PATH", "").strip()
    if env_chrome:
        try:
            return p.chromium.launch(
                executable_path=env_chrome,
                headless=True,
                args=["--disable-gpu"],
            )
        except Exception as e:
            errors.append(f"IVY_NET_CHROMIUM_PATH: {e}")

    # 2) Playwright’s own Chromium (isolated; does not open Chrome.app)
    try:
        return p.chromium.launch(headless=True)
    except Exception as e:
        errors.append(f"bundled chromium: {e}")

    # 3) Opt-in system Chrome only
    if os.environ.get("IVY_NET_USE_SYSTEM_CHROME", "").strip() == "1":
        mac_chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if Path(mac_chrome).exists():
            try:
                return p.chromium.launch(
                    executable_path=mac_chrome,
                    headless=True,
                    args=["--disable-gpu"],
                )
            except Exception as e:
                errors.append(f"macOS Google Chrome: {e}")
        try:
            return p.chromium.launch(channel="chrome", headless=True)
        except Exception as e:
            errors.append(f"channel=chrome: {e}")

    msg = "❌ Could not launch a browser for PDF.\n" + "\n".join(f"   - {x}" for x in errors)
    msg += (
        "\n   From Terminal (not the agent sandbox):\n"
        f"      {sys.executable} -m playwright install chromium\n"
        "   Or set IVY_NET_CHROMIUM_PATH. Avoid IVY_NET_USE_SYSTEM_CHROME unless needed."
    )
    raise RuntimeError(msg)


with sync_playwright() as p:
    browser = launch_browser(p)
    try:
        page = browser.new_page()
        page.goto(html_file.as_uri(), wait_until="load")
        page.emulate_media(media="print")
        page.pdf(
            path=str(pdf_file),
            format="Letter",
            margin={
                "top": "0.25in",
                "right": "0.25in",
                "bottom": "0.25in",
                "left": "0.25in",
            },
            print_background=True,  # keep Pygments token colors
            prefer_css_page_size=True,
        )
    finally:
        browser.close()

if not pdf_file.is_file() or pdf_file.stat().st_size < 100:
    print(f"❌ PDF missing or empty: {pdf_file}")
    sys.exit(1)
print(f"✅ PDF written: {pdf_file} ({pdf_file.stat().st_size:,} bytes)")
PY

if [[ "$KEEP_HTML" != true ]]; then
    rm -f "$HTML_FILE"
else
    echo "ℹ️  Kept HTML: $HTML_FILE"
fi

echo "Done."
