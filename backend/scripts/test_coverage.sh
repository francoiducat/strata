#!/usr/bin/env bash
# Run tests with coverage and write XML to backend/tests/coverage/coverage.xml
# Usage: ./scripts/test_coverage.sh [pytest-args]
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

# Ensure the tests/coverage/ dir exists
mkdir -p tests/coverage

# Tell coverage.py where to put its data file (avoid creating .coverage in repo root)
export COVERAGE_FILE="${PWD}/tests/coverage/.coverage"

# Run pytest with coverage and write coverage.xml into tests/coverage/coverage.xml
poetry run pytest --cov=app --cov-report=xml:./tests/coverage/coverage.xml "$@"

echo "Coverage XML written to tests/coverage/coverage.xml (coverage DB: $COVERAGE_FILE)"
