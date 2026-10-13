"""Every notebook must run top to bottom ("Restart & Run All") without errors."""
from __future__ import annotations

import json

import pytest

from conftest import REPO_ROOT, content_files, skip_if_missing

NOTEBOOKS = content_files("*.ipynb")


def notebook_source(path):
    nb = json.loads(path.read_text(encoding="utf-8"))
    return "\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code")


@pytest.mark.parametrize("notebook", NOTEBOOKS, ids=[n.as_posix() for n in NOTEBOOKS])
def test_notebook_executes(notebook, repo_copy):
    nbformat = pytest.importorskip("nbformat")
    nbclient = pytest.importorskip("nbclient")
    skip_if_missing(notebook_source(REPO_ROOT / notebook))

    path = repo_copy / notebook
    nb = nbformat.read(path, as_version=4)
    client = nbclient.NotebookClient(
        nb,
        timeout=900,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
    )
    client.execute()  # raises CellExecutionError, with the failing cell, on any error


def test_notebooks_are_saved_without_outputs():
    """Outputs can contain local paths or personal data, so notebooks are stored clean."""
    dirty = []
    for notebook in NOTEBOOKS:
        nb = json.loads((REPO_ROOT / notebook).read_text(encoding="utf-8"))
        if any(c.get("outputs") for c in nb["cells"] if c["cell_type"] == "code"):
            dirty.append(notebook.as_posix())
    assert not dirty, "Clear outputs before committing: " + ", ".join(dirty)
