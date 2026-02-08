"""Tiny CLI helpers to run the test suite from `poetry run`.

Provides two entry points used by poetry scripts:
- `test` / `app.cli:run` - runs pytest with any forwarded args
- `test-coverage` / `app.cli:coverage` - runs pytest with coverage and writes tests/coverage.xml

These wrappers keep behavior consistent whether run in CI or locally.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run() -> None:
    """Run pytest forwarding any CLI args provided after the script name.

    This uses os.execvp to replace the current process with pytest so the
    output streams directly to the console (useful when called via Poetry).
    """
    args = sys.argv[1:]
    cmd = [sys.executable, "-m", "pytest"] + args
    os.chdir(ROOT)
    os.execvp(cmd[0], cmd)


def coverage() -> None:
    """Run pytest with coverage and write XML to ./tests/coverage.xml.

    Replaces current process with pytest so output is non-buffered and visible
    when invoked via `poetry run test:coverage`.
    """
    args = sys.argv[1:]
    coverage_dir = ROOT / "tests" / "coverage"
    coverage_file = coverage_dir / "coverage.xml"
    coverage_db = coverage_dir / ".coverage"
    coverage_dir.mkdir(parents=True, exist_ok=True)

    # Set COVERAGE_FILE to write the .coverage data file into backend/tests/coverage/
    os.environ["COVERAGE_FILE"] = str(coverage_db)

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--cov=app",
        f"--cov-report=xml:{coverage_file}",
    ] + args
    os.chdir(ROOT)
    os.execvp(cmd[0], cmd)
