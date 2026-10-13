"""Release gate: the repository must not contain personal data."""
import subprocess

from conftest import PYTHON, REPO_ROOT


def test_no_personal_data_found():
    result = subprocess.run(
        [PYTHON, str(REPO_ROOT / "tools" / "scan_for_personal_data.py"), str(REPO_ROOT)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout
