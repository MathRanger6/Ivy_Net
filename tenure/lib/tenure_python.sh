#!/usr/bin/env bash
# Resolve Python 3.10+ for tenure pipeline scripts (tenure_net).
# Source from shell wrappers:  PY="$(tenure_python)"  or  exec "$(tenure_python)" script.py
#
# Do not use bare `python3` on macOS — /usr/bin/python3 is often 3.9.

tenure_python() {
  _tenure_py_ok() {
    [[ -n "${1:-}" && -x "$1" ]] && "$1" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null
  }

  if [[ -n "${TENURE_PYTHON:-}" ]] && _tenure_py_ok "$TENURE_PYTHON"; then
    echo "$TENURE_PYTHON"
    return 0
  fi

  if [[ "${CONDA_DEFAULT_ENV:-}" == tenure_net && -n "${CONDA_PREFIX:-}" ]]; then
    if _tenure_py_ok "${CONDA_PREFIX}/bin/python"; then
      echo "${CONDA_PREFIX}/bin/python"
      return 0
    fi
  fi

  local cand
  for cand in \
    "${HOME}/miniconda3/envs/tenure_net/bin/python" \
    "${HOME}/anaconda3/envs/tenure_net/bin/python" \
    "/opt/anaconda3/envs/tenure_net/bin/python" \
    "/opt/homebrew/Caskroom/miniconda/base/envs/tenure_net/bin/python"; do
    if _tenure_py_ok "$cand"; then
      echo "$cand"
      return 0
    fi
  done

  echo "ERROR: tenure_net Python 3.10+ not found. Create/update with:" >&2
  echo "  conda env create -f environment-tenure_net.yml   # repo root" >&2
  echo "  conda activate tenure_net" >&2
  return 1
}
