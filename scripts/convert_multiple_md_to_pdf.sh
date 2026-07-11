#!/bin/bash
# Convert several numbered-stack .md files to PDF via convert_single_md_to_pdf.sh.
#
# Usage:
#   ./scripts/convert_multiple_md_to_pdf.sh [--pandoc] [--narrow] [--keep-html] 01_ 02_ 05_ 10_
#   ./scripts/convert_multiple_md_to_pdf.sh 2 5 9          # same as 02_ 05_ 09_
#
# Prefix rules:
#   - Looks only in 3-Master_Plan/ and 5-Manuscript/ (top level; not obsolete/).
#   - Matches files whose names start with NN_ (two-digit reading-stack numbers).
#   - If one prefix matches multiple files, prompts you to pick (requires a TTY).
#
# Extra flags (--pandoc, --keep-html) are forwarded to each single-file conversion.
#
# Requires Bash 3.2+ (macOS /bin/bash and Rivanna default — no mapfile/Bash 4 needed).

set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPTS_DIR/.." && pwd)"
SINGLE_SCRIPT="$SCRIPTS_DIR/convert_single_md_to_pdf.sh"

USE_PANDOC=false
USE_NARROW=false
KEEP_HTML=false
PREFIXES=()

usage() {
    cat <<'EOF'
Usage: ./scripts/convert_multiple_md_to_pdf.sh [options] <prefix> [prefix ...]

Options (forwarded to convert_single_md_to_pdf.sh where applicable):
  --pandoc      Use pandoc/LaTeX backend (Rivanna-friendly)
  --narrow      Use pdf_styles_narrow.css (0.1in margins)
  --keep-html   Keep intermediate HTML (Playwright only)
  -h, --help    Show this help

Arguments:
  prefix        Two-digit stack id, with or without trailing underscore
                Examples: 02_   02   5   05_

Examples:
  ./scripts/convert_multiple_md_to_pdf.sh 01_ 02_ 03_
  ./scripts/convert_multiple_md_to_pdf.sh --narrow 1 2 5 10
  ./scripts/convert_multiple_md_to_pdf.sh --pandoc 06_ 08_

Search roots (top level only):
  3-Master_Plan/NN_*.md
  5-Manuscript/NN_*.md
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --pandoc)
            USE_PANDOC=true
            shift
            ;;
        --narrow)
            USE_NARROW=true
            shift
            ;;
        --keep-html)
            KEEP_HTML=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            while [[ $# -gt 0 ]]; do
                PREFIXES+=("$1")
                shift
            done
            ;;
        -*)
            echo "❌ Unknown option: $1" >&2
            usage >&2
            exit 1
            ;;
        *)
            PREFIXES+=("$1")
            shift
            ;;
    esac
done

if [[ ${#PREFIXES[@]} -eq 0 ]]; then
    echo "❌ Error: at least one prefix is required (e.g. 02_ 05_)" >&2
    usage >&2
    exit 1
fi

if [[ ! -x "$SINGLE_SCRIPT" ]]; then
    chmod +x "$SINGLE_SCRIPT"
fi

normalize_prefix() {
    local raw="$1"
    local digits
    digits="$(echo "$raw" | tr -d '_')"
    if [[ ! "$digits" =~ ^[0-9]+$ ]]; then
        echo "❌ Invalid prefix (expected digits): $raw" >&2
        return 1
    fi
    printf '%02d_' "$((10#$digits))"
}

find_candidates() {
    local prefix="$1"
    local dir rel f
    for dir in "$WORKSPACE_DIR/3-Master_Plan" "$WORKSPACE_DIR/5-Manuscript"; do
        [[ -d "$dir" ]] || continue
        rel="${dir#"$WORKSPACE_DIR/"}"
        for f in "$dir"/${prefix}*.md; do
            [[ -f "$f" ]] || continue
            printf '%s\n' "$rel/$(basename "$f")"
        done
    done
}

collect_candidates() {
    local prefix="$1"
    CANDIDATES=()
    local line
    while IFS= read -r line; do
        [[ -n "$line" ]] && CANDIDATES+=("$line")
    done <<EOF
$(find_candidates "$prefix")
EOF
}

pick_candidate() {
    local prefix="$1"
    shift
    local -a matches=("$@")
    local count="${#matches[@]}"

    if [[ "$count" -eq 1 ]]; then
        echo "${matches[0]}"
        return 0
    fi

    echo "⚠️  Prefix ${prefix} matches ${count} files:" >&2
    local i=1
    for m in "${matches[@]}"; do
        echo "  [$i] $m" >&2
        ((i++)) || true
    done

    if [[ ! -t 0 ]]; then
        echo "❌ Ambiguous prefix ${prefix} and stdin is not a TTY — re-run interactively or use a unique prefix." >&2
        return 1
    fi

    local choice
    while true; do
        read -r -p "Enter number [1-${count}] (or q to skip): " choice
        case "$choice" in
            q|Q)
                echo "⏭️  Skipped ${prefix}" >&2
                return 2
                ;;
        esac
        if [[ "$choice" =~ ^[0-9]+$ ]] && (( choice >= 1 && choice <= count )); then
            echo "${matches[$((choice - 1))]}"
            return 0
        fi
        echo "Invalid choice." >&2
    done
}

CSS_ARG=""
if [[ "$USE_NARROW" == true ]]; then
    CSS_FILE="$WORKSPACE_DIR/pdf_styles_narrow.css"
    if [[ ! -f "$CSS_FILE" ]]; then
        echo "❌ Error: --narrow requested but not found: $CSS_FILE" >&2
        exit 1
    fi
    CSS_ARG="$CSS_FILE"
elif [[ -f "$WORKSPACE_DIR/pdf_styles.css" ]]; then
    CSS_ARG="$WORKSPACE_DIR/pdf_styles.css"
fi

SINGLE_FLAGS=()
if [[ "$USE_PANDOC" == true ]]; then
    SINGLE_FLAGS+=(--pandoc)
fi
if [[ "$KEEP_HTML" == true ]]; then
    SINGLE_FLAGS+=(--keep-html)
fi

RESOLVED=()
FAILED=0
SKIPPED=0

for raw_prefix in "${PREFIXES[@]}"; do
    prefix="$(normalize_prefix "$raw_prefix")" || exit 1

    collect_candidates "$prefix"
    if [[ ${#CANDIDATES[@]} -eq 0 ]]; then
        echo "❌ No .md found for prefix ${prefix} (looked in 3-Master_Plan/, 5-Manuscript/)" >&2
        FAILED=$((FAILED + 1))
        continue
    fi

    if ! rel_path="$(pick_candidate "$prefix" "${CANDIDATES[@]}")"; then
        pick_status=$?
        if [[ "$pick_status" -eq 2 ]]; then
            SKIPPED=$((SKIPPED + 1))
            continue
        fi
        FAILED=$((FAILED + 1))
        continue
    fi

    RESOLVED+=("$rel_path")
done

if [[ ${#RESOLVED[@]} -eq 0 ]]; then
    echo "❌ Nothing to convert." >&2
    exit 1
fi

echo "▶ Converting ${#RESOLVED[@]} file(s)..."
echo ""

CONVERT_OK=0
CONVERT_FAIL=0

for rel_path in "${RESOLVED[@]}"; do
    input="$WORKSPACE_DIR/$rel_path"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📄 $rel_path"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    convert_args=()
    if (( ${#SINGLE_FLAGS[@]} > 0 )); then
        convert_args+=("${SINGLE_FLAGS[@]}")
    fi
    convert_args+=("$input" "")
    if [[ -n "$CSS_ARG" ]]; then
        convert_args+=("$CSS_ARG")
    fi

    if "$SINGLE_SCRIPT" "${convert_args[@]}"; then
        CONVERT_OK=$((CONVERT_OK + 1))
    else
        echo "❌ Failed: $rel_path" >&2
        CONVERT_FAIL=$((CONVERT_FAIL + 1))
    fi
    echo ""
done

echo "Summary: ${CONVERT_OK} succeeded, ${CONVERT_FAIL} failed, ${SKIPPED} skipped, ${FAILED} unresolved prefix(es)."

if [[ "$CONVERT_FAIL" -gt 0 || "$FAILED" -gt 0 ]]; then
    exit 1
fi
