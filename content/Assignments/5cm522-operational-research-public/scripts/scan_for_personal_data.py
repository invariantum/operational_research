#!/usr/bin/env python3
"""Scan the repository for personal data before it is shared.

Checks every file type that can hide personal data:

* plain text, code, CSV, Markdown, LaTeX, YAML/JSON
* Jupyter notebooks, including saved outputs
* Word / Excel / PowerPoint files (body text *and* hidden metadata: author,
  last-modified-by, SharePoint custom XML, comments, people lists)
* PDFs (text and document metadata)

What it looks for (generic patterns, so this file itself contains no personal data):

* University-style student/staff numbers (9 digits starting with 100)
* e-mail addresses
* absolute local paths that reveal a user name (C:\\Users\\<name>, /Users/<name>, /home/<name>)
* OneDrive / SharePoint paths
* document author metadata
* optional: any extra terms (e.g. a list of student names) passed with --terms FILE.
  Keep that file OUTSIDE the repository.

Usage:
    python scripts/scan_for_personal_data.py                 # scan this repository
    python scripts/scan_for_personal_data.py --terms ~/names.txt
    python scripts/scan_for_personal_data.py path/to/folder

Exit code 0 = nothing found, 1 = findings (listed), so it can be used as a release gate.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Placeholders that are deliberately used in examples and are not personal data.
ALLOWED_IDS = {"100000000"}
ALLOWED_PATH_NAMES = {"<your-name>", "<you>", "<name>", "username", "user", "runner", "public", "default"}
ALLOWED_EMAIL_DOMAINS = (
    "example.com", "example.org",
    # XML namespaces inside Office files look like e-mail-ish strings but are not
    "openxmlformats.org", "w3.org", "microsoft.com", "purl.org",
)
# Name allowed in document metadata (the module leader agreed to be credited by name).
ALLOWED_AUTHORS = {"", "openpyxl", "Sam O'Neill", "Sam O’Neill", "Dr Sam O'Neill", "Dr Sam O’Neill"}

PATTERNS = {
    "student/staff number": re.compile(r"(?<![\d.])100\d{6}(?![\d.])"),
    "e-mail address": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"),
    "local user path": re.compile(r"(?:[A-Za-z]:[\\/]+Users[\\/]+|/Users/|/home/)([^\\/\s\"'<>]+)", re.I),
    "OneDrive/SharePoint path": re.compile(r"OneDrive\s*-|sharepoint\.com", re.I),
}

SKIP_DIRS = {".git", "__pycache__", ".ipynb_checkpoints", ".pytest_cache", "output"}
TEXT_SUFFIXES = {".py", ".md", ".txt", ".csv", ".tex", ".yml", ".yaml", ".json", ".gitignore", ".gitattributes", ".toml", ".cfg", ".ini", ""}
SKIP_FILES = {Path(__file__).name}  # this file documents the patterns


def is_allowed(kind: str, match: re.Match) -> bool:
    text = match.group(0)
    if kind == "student/staff number":
        return text in ALLOWED_IDS
    if kind == "e-mail address":
        return text.lower().endswith(ALLOWED_EMAIL_DOMAINS)
    if kind == "local user path":
        return match.group(1).lower() in ALLOWED_PATH_NAMES
    return False


def scan_text(text: str, where: str, extra_terms: list[re.Pattern], findings: list[str]) -> None:
    for kind, pattern in PATTERNS.items():
        for m in pattern.finditer(text):
            if not is_allowed(kind, m):
                findings.append(f"{where}: {kind}: {m.group(0)[:80]!r}")
    for term in extra_terms:
        for m in term.finditer(text):
            findings.append(f"{where}: listed term: {m.group(0)!r}")


def office_text(path: Path, findings: list[str]) -> str:
    """Return all XML text of an Office file and report risky hidden parts."""
    parts = []
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            low = name.lower()
            if low.startswith("customxml/") or low == "docprops/custom.xml" or "person" in low or "comments" in low:
                findings.append(f"{path}: hidden part present ({name}) - may contain user details")
            if not name.endswith((".xml", ".rels")):
                continue
            xml = z.read(name).decode("utf-8", "ignore")
            if name == "docProps/core.xml":
                for tag in ("dc:creator", "cp:lastModifiedBy"):
                    m = re.search(rf"<{tag}>([^<]*)</{tag}>", xml)
                    if m and m.group(1).strip() not in ALLOWED_AUTHORS:
                        findings.append(f"{path}: metadata {tag} = {m.group(1)!r}")
            # keep visible text only (drop tags) so namespaces do not trigger the e-mail rule
            parts.append(re.sub(r"<[^>]+>", " ", xml))
    return " ".join(parts)


def pdf_text(path: Path, findings: list[str]) -> str:
    try:
        from pypdf import PdfReader
    except ModuleNotFoundError:
        findings.append(f"{path}: cannot scan PDF (install pypdf)")
        return ""
    reader = PdfReader(str(path))
    meta = reader.metadata or {}
    author = str(meta.get("/Author", "") or "").strip()
    if author not in ALLOWED_AUTHORS:
        findings.append(f"{path}: PDF metadata /Author = {author!r}")
    return " ".join((page.extract_text() or "") for page in reader.pages)


def notebook_text(path: Path) -> str:
    nb = json.loads(path.read_text(encoding="utf-8"))
    chunks = [json.dumps(nb.get("metadata", {}))]
    for cell in nb.get("cells", []):
        chunks.append("".join(cell.get("source", [])))
        for out in cell.get("outputs", []):
            chunks.append(json.dumps(out))
    return "\n".join(chunks)


def scan(root: Path, extra_terms: list[re.Pattern]) -> list[str]:
    findings: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.name in SKIP_FILES:
            continue
        rel = path.relative_to(root)
        suffix = path.suffix.lower()
        try:
            if suffix in (".docx", ".xlsx", ".pptx"):
                text = office_text(path, findings)
            elif suffix == ".pdf":
                text = pdf_text(path, findings)
            elif suffix == ".ipynb":
                text = notebook_text(path)
            elif suffix in TEXT_SUFFIXES or path.name.startswith("."):
                text = path.read_text(encoding="utf-8", errors="ignore")
            else:
                continue  # images etc.
        except Exception as exc:  # unreadable file: report rather than silently pass
            findings.append(f"{rel}: could not be scanned ({exc})")
            continue
        scan_text(text, str(rel), extra_terms, findings)
    return [f.replace(str(root) + "/", "").replace(str(root) + "\\", "") for f in findings]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("folder", nargs="?", default=str(REPO_ROOT), help="Folder to scan (default: this repository).")
    parser.add_argument("--terms", help="Text file with extra terms to flag (one per line), e.g. student names.")
    args = parser.parse_args()

    terms: list[re.Pattern] = []
    if args.terms:
        for line in Path(args.terms).read_text(encoding="utf-8").splitlines():
            if line.strip():
                terms.append(re.compile(rf"\b{re.escape(line.strip())}\b", re.I))

    root = Path(args.folder).resolve()
    findings = scan(root, terms)
    if findings:
        print(f"Personal-data scan: {len(findings)} finding(s)")
        for f in findings:
            print("  -", f)
        return 1
    print(f"Personal-data scan: no findings in {root.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
