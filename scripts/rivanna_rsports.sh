# Rivanna helpers for the sports / faithful-537 workflow.
#
# One-time: clone tenure_net → sports_net on the cluster (same machine only;
# this copies the solved package set from one env name to another).
#
#   module load miniforge    # if conda is not already on PATH
#   conda create -n sports_net --clone tenure_net -y
#
# Replace an existing sports_net (destructive):
#
#   conda env remove -n sports_net -y
#   conda create -n sports_net --clone tenure_net -y
#
# Sanity check:
#
#   conda run -n sports_net python -c "import matplotlib; print(matplotlib.__version__)"
#
# Install: append ONE line to ~/.bashrc on Rivanna (path must match where you
# cloned Ivy_Net — override with IVY_NET_ROOT if not ~/Ivy_Net):
#
#   source ~/Ivy_Net/scripts/rivanna_rsports.sh
#
# Then in a new login shell: rsports

# Repo root on Rivanna (same convention as tenure/HPC docs).
IVY_NET_ROOT="${IVY_NET_ROOT:-$HOME/Ivy_Net}"

rsports() {
  if ! cd "$IVY_NET_ROOT"; then
    echo "rsports: cannot cd to IVY_NET_ROOT=${IVY_NET_ROOT}" >&2
    echo "  Fix: export IVY_NET_ROOT=/path/to/Ivy_Net  or move/clone the repo to ~/Ivy_Net" >&2
    return 1
  fi
  if ! command -v conda >/dev/null 2>&1; then
    if [[ -f "$HOME/miniforge3/etc/profile.d/conda.sh" ]]; then
      # shellcheck source=/dev/null
      . "$HOME/miniforge3/etc/profile.d/conda.sh"
    elif [[ -f "$HOME/mambaforge/etc/profile.d/conda.sh" ]]; then
      # shellcheck source=/dev/null
      . "$HOME/mambaforge/etc/profile.d/conda.sh"
    fi
  fi
  if ! command -v conda >/dev/null 2>&1; then
    echo "rsports: conda not found. On Rivanna try: module load miniforge" >&2
    return 1
  fi
  conda activate sports_net
}
