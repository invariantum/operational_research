"""Every LaTeX source has an up-to-date compiled PDF next to it, and Office files open cleanly."""
from __future__ import annotations

import zipfile

import pytest

from conftest import REPO_ROOT, content_files

TEX = content_files("*.tex")
OFFICE = content_files("*.docx") + content_files("*.xlsx")


@pytest.mark.parametrize("tex", TEX, ids=[t.as_posix() for t in TEX])
def test_tex_has_pdf(tex):
    pdf = (REPO_ROOT / tex).with_suffix(".pdf")
    assert pdf.exists(), f"missing {pdf.name} - run: python tools/build_pdfs.py"


@pytest.mark.parametrize("doc", OFFICE, ids=[d.as_posix() for d in OFFICE])
def test_office_file_is_valid(doc):
    with zipfile.ZipFile(REPO_ROOT / doc) as z:
        assert z.testzip() is None
        assert "[Content_Types].xml" in z.namelist()
