#!/usr/bin/env python3
"""Rebuild every PDF from its LaTeX source.

Each `name.tex` is compiled (twice, so cross-references settle) in a temporary folder and the
result is copied to `name.pdf` next to the source. Build clutter (.aux, .log, .synctex.gz) never
touches the repository.

Requires a LaTeX distribution with `pdflatex` on the PATH (MiKTeX on Windows, MacTeX on macOS,
TeX Live on Linux). The PDFs are already committed, so you only need this after editing a .tex file.

Usage:
    python tools/build_pdfs.py                 # rebuild all
    python tools/build_pdfs.py 03-in-class-test     # rebuild one folder
    python tools/build_pdfs.py --check         # only report .tex files whose PDF is missing/older
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {"output", ".git", "tools"}


def tex_files(folder: Path) -> list[Path]:
    return [p for p in sorted(folder.rglob("*.tex")) if not SKIP_DIRS.intersection(p.relative_to(REPO_ROOT).parts)]


def build(tex: Path) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy2(tex, Path(tmp) / tex.name)
        for _ in range(2):
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex.name],
                cwd=tmp, capture_output=True, text=True, errors="replace",
            )
            if result.returncode != 0:
                log = (Path(tmp) / tex.with_suffix(".log").name)
                tail = log.read_text(errors="replace")[-2000:] if log.exists() else result.stdout[-2000:]
                print(f"FAILED  {tex.relative_to(REPO_ROOT)}\n{tail}")
                return False
        shutil.copy2(Path(tmp) / tex.with_suffix(".pdf").name, tex.with_suffix(".pdf"))
    print(f"built   {tex.with_suffix('.pdf').relative_to(REPO_ROOT)}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("folder", nargs="?", default=str(REPO_ROOT))
    parser.add_argument("--check", action="store_true", help="only list missing or out-of-date PDFs")
    args = parser.parse_args()
    files = tex_files(Path(args.folder).resolve())

    if args.check:
        stale = [t for t in files if not t.with_suffix(".pdf").exists()
                 or t.with_suffix(".pdf").stat().st_mtime < t.stat().st_mtime]
        for t in stale:
            print("needs rebuild:", t.relative_to(REPO_ROOT))
        print(f"{len(files) - len(stale)}/{len(files)} PDFs up to date")
        return 1 if stale else 0

    if shutil.which("pdflatex") is None:
        print("pdflatex not found - install MiKTeX / MacTeX / TeX Live first.")
        return 1
    ok = all([build(t) for t in files])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
