#!/usr/bin/env bash
# generate_variations.sh
#
# Opens all slides-v*.html variations in the default browser for side-by-side review.
# Run from the directory where your slide files were generated.
#
# Usage:
#   bash scripts/generate_variations.sh
#   bash scripts/generate_variations.sh ./output-dir

set -euo pipefail

TARGET_DIR="${1:-.}"

# Find all variation files
VARIATIONS=("$TARGET_DIR"/slides-v*.html)

if [ ${#VARIATIONS[@]} -eq 0 ] || [ ! -f "${VARIATIONS[0]}" ]; then
  echo "❌  No slides-v*.html files found in: $TARGET_DIR"
  echo "    Generate variations first via /whoop-presentation"
  exit 1
fi

echo "📂  Found ${#VARIATIONS[@]} variation(s):"
for f in "${VARIATIONS[@]}"; do
  echo "    • $(basename "$f")"
done
echo ""

# Open each in browser
for f in "${VARIATIONS[@]}"; do
  echo "🌐  Opening $(basename "$f") ..."
  if [[ "$OSTYPE" == "darwin"* ]]; then
    open "$f"
  elif command -v xdg-open &>/dev/null; then
    xdg-open "$f"
  else
    echo "    (Cannot auto-open — open manually: $f)"
  fi
  sleep 0.5  # slight stagger so tabs open in order
done

echo ""
echo "✅  All variations opened. Use arrow keys to navigate slides."
echo "    Once you've reviewed, tell Claude which version to refine."
