"""Shared helpers for the test suite.

Every test that runs code works on a throw-away copy of the repository, so running the
tests never changes, overwrites or adds files in your working folders.
"""
from __future__ import annotations

import importlib.util
import re
import shutil
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

# Folders that hold tooling or generated files rather than course content.
NON_CONTENT_DIRS = {"scripts", "tests", "docs", "output", "data", "base_data", ".vscode",
                    "__pycache__", ".ipynb_checkpoints", ".pytest_cache", ".git"}

# Third-party packages that may be missing on a machine without the project environment.
OPTIONAL_PACKAGES = {
    "pyomo": "pyomo",
    "simpy": "simpy",
    "ortools": "ortools",
    "sklearn": "scikit-learn",
    "highspy": "highspy",
}


def content_files(pattern: str) -> list[Path]:
    """All course-content files matching `pattern` (e.g. '*.py'), as repo-relative paths."""
    found = []
    for path in sorted(REPO_ROOT.rglob(pattern)):
        rel = path.relative_to(REPO_ROOT)
        if any(part in NON_CONTENT_DIRS for part in rel.parts[:-1]):
            continue
        found.append(rel)
    return found


def with_local_imports(source: str, folder: Path) -> str:
    """Append the source of sibling modules that `source` imports (e.g. a helper .py file)."""
    for name in set(re.findall(r"^\s*(?:import|from)\s+(\w+)", source, re.M)):
        sibling = folder / f"{name}.py"
        if sibling.exists():
            source += "\n" + sibling.read_text(encoding="utf-8")
    return source


def missing_packages(source: str) -> list[str]:
    """Optional packages that `source` imports but which are not installed here."""
    missing = []
    for module, package in OPTIONAL_PACKAGES.items():
        if re.search(rf"^\s*(import|from)\s+{module}\b", source, re.M) and importlib.util.find_spec(module) is None:
            missing.append(package)
    # Pyomo models in this repository are solved with HiGHS (appsi_highs), shipped as `highspy`.
    if "appsi_highs" in source and importlib.util.find_spec("highspy") is None and "highspy" not in missing:
        missing.append("highspy")
    return missing


def skip_if_missing(source: str) -> None:
    missing = missing_packages(source)
    if missing:
        pytest.skip("not installed: " + ", ".join(missing) + " (create the conda environment from environment.yml)")


@pytest.fixture(scope="session")
def repo_copy(tmp_path_factory) -> Path:
    """A disposable copy of the whole repository."""
    dst = tmp_path_factory.mktemp("repo") / REPO_ROOT.name
    shutil.copytree(
        REPO_ROOT,
        dst,
        ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache", ".ipynb_checkpoints", "output"),
    )
    return dst


PYTHON = sys.executable
