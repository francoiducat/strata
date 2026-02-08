#!/usr/bin/env bash
# Generate HTML coverage report from existing coverage data located at tests/coverage/.coverage
# Usage: ./scripts/generate_coverage_html.sh
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

COV_DIR="tests/coverage"
COV_DB="$COV_DIR/.coverage"
OUT_DIR="$COV_DIR/html"

if [ ! -f "$COV_DB" ]; then
  echo "Coverage data file not found at $COV_DB"
  echo "Run './scripts/test_coverage.sh' first to produce coverage data."
  exit 1
fi

export COVERAGE_FILE="$COV_DB"

# Use python -m coverage to generate html (coverage.py must be installed in the environment)
poetry run python -m coverage html -d "$OUT_DIR"

echo "HTML coverage generated at $OUT_DIR/index.html"

