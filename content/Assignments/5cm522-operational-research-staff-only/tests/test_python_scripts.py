"""Every Python script in the repository must run from start to finish without errors."""
from __future__ import annotations

import subprocess

import pytest

from conftest import PYTHON, REPO_ROOT, content_files, skip_if_missing, with_local_imports

# Command-line arguments for scripts that need them. Dummy IDs only.
SCRIPT_ARGS = {
    "generate_data.py": ["--student_id", "100000000"],
}

SCRIPTS = content_files("*.py")


@pytest.mark.parametrize("script", SCRIPTS, ids=[s.as_posix() for s in SCRIPTS])
def test_script_runs(script, repo_copy):
    source = (REPO_ROOT / script).read_text(encoding="utf-8")
    skip_if_missing(with_local_imports(source, (REPO_ROOT / script).parent))
    path = repo_copy / script
    result = subprocess.run(
        [PYTHON, path.name, *SCRIPT_ARGS.get(path.name, [])],
        cwd=path.parent,
        capture_output=True,
        text=True,
        timeout=900,
    )
    assert result.returncode == 0, f"{script} failed:\n{result.stdout[-3000:]}\n{result.stderr[-3000:]}"
