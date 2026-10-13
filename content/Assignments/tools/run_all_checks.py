#!/usr/bin/env python3
"""One command to check the whole repository.

Runs, in order:
  1. the personal-data scan (tools/scan_for_personal_data.py)
  2. the test suite (tools/tests/), which
       - runs every Python script and every notebook top to bottom,
       - checks the Part B data generator is deterministic and leak-free,
       - checks published answer files still match the code that produced them,
       - checks every LaTeX source has its PDF and every Office file is valid.

All code runs on a temporary copy, so nothing in your folders is changed.

Usage (from the repository root, inside the conda environment):
    python tools/run_all_checks.py            # everything (takes a few minutes)
    python tools/run_all_checks.py --quick    # skip notebook execution
    python tools/run_all_checks.py --allow-skips

Tests are *skipped* (not failed) when a package such as pyomo is missing. A skipped test has
not been checked, so by default any skip makes this script exit with an error.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--quick", action="store_true", help="skip executing notebooks")
    parser.add_argument("--allow-skips", action="store_true", help="do not treat skipped tests as a failure")
    args = parser.parse_args()

    print("=" * 70, "\n1/2  Personal-data scan\n" + "=" * 70)
    scan = subprocess.run([sys.executable, str(REPO_ROOT / "tools" / "scan_for_personal_data.py")], cwd=REPO_ROOT)

    print("=" * 70, "\n2/2  Test suite\n" + "=" * 70)
    try:
        import pytest  # noqa: F401
    except ModuleNotFoundError:
        print("pytest is not installed - activate the project environment (see README).")
        return 1
    cmd = [sys.executable, "-m", "pytest", "tools/tests", "-v", "-rs", "-p", "no:cacheprovider"]
    if args.quick:
        cmd += ["-k", "not test_notebook_executes"]
    if not args.allow_skips:
        cmd += ["--junitxml", str(REPO_ROOT / "output" / "test-results.xml")]
    tests = subprocess.run(cmd, cwd=REPO_ROOT)

    skipped = 0
    if not args.allow_skips:
        import xml.etree.ElementTree as ET
        report = REPO_ROOT / "output" / "test-results.xml"
        if report.exists():
            suite = ET.parse(report).getroot()
            suite = suite if suite.tag == "testsuite" else suite.find("testsuite")
            skipped = int(suite.get("skipped", 0))

    print("=" * 70)
    ok = scan.returncode == 0 and tests.returncode == 0 and skipped == 0
    print("Personal-data scan :", "PASS" if scan.returncode == 0 else "FAIL")
    print("Test suite         :", "PASS" if tests.returncode == 0 else "FAIL")
    if skipped:
        print(f"Skipped tests      : {skipped} (missing packages - see the 'SKIPPED' lines above;"
              " create the environment from environment.yml, or use --allow-skips)")
    print("RESULT             :", "ALL CHECKS PASSED" if ok else "CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
