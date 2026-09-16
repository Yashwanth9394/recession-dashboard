#!/bin/bash
# Optional manual refresh -- the real automation is .github/workflows/refresh.yml,
# which runs weekly on GitHub's own infrastructure and deploys to GitHub Pages.
# Use this only if you want fresh data locally right now, outside that schedule.
set -euo pipefail
cd "$(dirname "$0")"

LOG="logs/refresh-$(date +%Y-%m-%d).log"
mkdir -p logs

{
  echo "=== Fault Line manual refresh: $(date) ==="

  echo "--- Pulling fresh FRED data ---"
  python3 build_data.py

  echo "--- Committing data ---"
  git add data/dashboard-data.json
  if git diff --cached --quiet; then
    echo "No data changes to commit."
  else
    git commit -m "Manual data refresh $(date +%Y-%m-%d)"
    git push
  fi

  echo "=== Done: $(date) ==="
} >> "$LOG" 2>&1

echo "Refresh complete. Log: $LOG"
