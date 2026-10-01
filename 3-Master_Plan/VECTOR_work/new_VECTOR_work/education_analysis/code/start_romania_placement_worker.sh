#!/bin/zsh
# Start one bounded, resumable source-only retrieval in the background.
# Usage: ./start_romania_placement_worker.sh [max_new_pages] [max_hours] [optional worker arguments]
# Examples:
#   ./start_romania_placement_worker.sh 40 2 --counties NT
#   ./start_romania_placement_worker.sh 120 6
# Raw source pages and logs remain in ~/Desktop/VECTOR_temp, outside Dropbox/Git.
set -euo pipefail

max_pages="${1:-40}"
max_hours="${2:-2}"
if (( $# >= 2 )); then
  shift 2
elif (( $# == 1 )); then
  shift 1
fi

script_dir="${0:A:h}"
private_dir="$HOME/Desktop/VECTOR_temp/romania_2001_national_main_allocation_v1/background_worker"
pid_file="$private_dir/placement_worker.pid"
mkdir -p "$private_dir"
chmod 700 "$private_dir"

if [[ -f "$pid_file" ]]; then
  old_pid="$(cat "$pid_file")"
  if kill -0 "$old_pid" 2>/dev/null; then
    print "A placement worker is already running with PID $old_pid."
    exit 1
  fi
fi

log_file="$private_dir/placement_worker_$(date +%Y%m%d_%H%M%S).log"
nohup /usr/bin/caffeinate -i /opt/anaconda3/envs/sports_net/bin/python -u \
  "$script_dir/EDUCATION_20261001_romania_background_placement_worker.py" \
  --run --max-new-pages "$max_pages" --max-hours "$max_hours" "$@" \
  > "$log_file" 2>&1 < /dev/null &
worker_pid=$!
print "$worker_pid" > "$pid_file"
print "Started source-only worker; PID: $worker_pid"
print "Live log: $log_file"
print "Aggregate county status: $script_dir/../outputs/romania_2001_national_source_recovery/placement_county_status.csv"
print "To watch: tail -f '$log_file'"
print "To stop gracefully: kill $worker_pid"
