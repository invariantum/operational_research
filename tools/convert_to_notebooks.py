#!/usr/bin/env python3
"""
convert_to_notebooks.py
=======================

Turn the course's Python scripts (and Markdown notes that contain ```python
blocks) into Jupyter notebooks that run in the browser (JupyterLite / Pyodide),
in Google Colab and in Anaconda Jupyter.

What it does to each file
-------------------------
* Writes ``<name>.ipynb`` next to ``<name>.py`` (or ``<name>.md``).
* Adds a first code cell that installs the packages the browser does not ship
  with (Pyomo, HiGHS bindings, SimPy, openpyxl) using ``%pip install``.
* Replaces the GLPK / CBC solvers, which are separate programs and cannot run
  in a browser, with HiGHS through ``SolverFactory('appsi_highs')``.
* Splits a script into cells at its top-level ``# comment`` headings, but only
  when every resulting cell is valid Python on its own; otherwise the script
  stays in one cell.
* Adds a warning cell when the code needs OR-Tools, which has no browser build.

It can also patch existing notebooks in place (``--patch-notebooks``): solver
swap plus the install cell, nothing else.

Usage
-----
    python tools/convert_to_notebooks.py content/Lectures
    python tools/convert_to_notebooks.py content/Lectures --force
    python tools/convert_to_notebooks.py content/Lectures --patch-notebooks
    python tools/convert_to_notebooks.py "content/Lectures/Semester 2/Week 03 - Discrete Event Simulation with SimPy/1 Lecture/Notes/1 Intro to SimPy and the M-M-1 queue.md"

Existing notebooks are never overwritten unless ``--force`` is given.
Only the Python standard library is needed.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import uuid
from pathlib import Path

# --------------------------------------------------------------------------
# Settings
# --------------------------------------------------------------------------

# Packages that are NOT bundled with Pyodide and must be installed with %pip.
# NumPy, SciPy, pandas, Matplotlib, scikit-learn and NetworkX load
# automatically when imported, so they are not listed here.
PIP_FOR_IMPORT = {
    "pyomo": ["pyomo", "highspy"],
    "simpy": ["simpy"],
    "openpyxl": ["openpyxl"],
    "ipywidgets": ["ipywidgets"],
    "ipympl": ["ipympl"],
}

# Two things in the browser (JupyterLite) break Pyomo, so the first cell of every
# Pyomo notebook adapts it there (sys.platform == "emscripten"); nothing changes in
# Colab or Anaconda, and solving is unaffected:
#  1. no threads: Pyomo's HiGHS interfaces capture solver output with a helper
#     thread -> "RuntimeError: can't start new thread"
#  2. the notebook's output stream returns None from write(); model.pprint() and
#     model.display() expect a number -> "TypeError: ... 'int' and 'NoneType'"
BROWSER_FIX_MARKER = "pyomo.common.tee.capture_output"
BROWSER_FIX_V2_MARKER = "_browser_patched"
OLD_PYOMO_BROWSER_FIX = """import sys
if sys.platform == "emscripten":  # browser only: no threads, so skip Pyomo's output capture
    import contextlib, pyomo.common.tee
    pyomo.common.tee.capture_output = lambda *args, **kwargs: contextlib.nullcontext()
    for _m in ("pyomo.contrib.appsi.solvers.highs", "pyomo.contrib.solver.solvers.highs"):
        if _m in sys.modules:
            sys.modules[_m].capture_output = pyomo.common.tee.capture_output"""
PYOMO_BROWSER_FIX = """import sys
if sys.platform == "emscripten":  # only in the browser (JupyterLite): adapt Pyomo to it
    import contextlib, pyomo.common.tee, pyomo.common.formatting as _fmt
    # 1) browsers have no threads: skip Pyomo's threaded capture of solver output
    pyomo.common.tee.capture_output = lambda *args, **kwargs: contextlib.nullcontext()
    for _m in ("pyomo.contrib.appsi.solvers.highs", "pyomo.contrib.solver.solvers.highs"):
        if _m in sys.modules:
            sys.modules[_m].capture_output = pyomo.common.tee.capture_output
    # 2) the notebook's output returns None from write(); model.pprint()/display() need a number
    if not getattr(_fmt.StreamIndenter, "_browser_patched", False):
        class _Counted:
            def __init__(self, s): self._s = s
            def write(self, data): self._s.write(data); return len(data)
            def __getattr__(self, name): return getattr(self._s, name)
        def _init(self, ostream, indent=" " * 4, _orig=_fmt.StreamIndenter.__init__):
            _orig(self, ostream, indent)
            if not isinstance(self.target_os, _Counted):
                object.__setattr__(self, "target_os", _Counted(self.target_os))
        _fmt.StreamIndenter.__init__ = _init
        _fmt.StreamIndenter._browser_patched = True"""

NO_BROWSER_BUILD = {"ortools": "Google OR-Tools"}

SOLVER_PATTERN = re.compile(r"""SolverFactory\(\s*(['"])(glpk|cbc)\1""")
SOLVER_REPLACEMENT = "SolverFactory('appsi_highs'"
# "try these solvers in turn" lists, e.g. for name in ["cbc", "glpk", ...]
SOLVER_LIST_PATTERN = re.compile(r"""\[(\s*)(?=(['"])(?:cbc|glpk)\2)""")

KERNELSPEC = {"name": "python3", "display_name": "Python 3", "language": "python"}

# folders whose scripts are kept for reference only (no notebook beside them)
SKIP_DIRS = {".ipynb_checkpoints", "__pycache__", "archive"}  # plus any "... Source Files" folder


# --------------------------------------------------------------------------
# Notebook helpers
# --------------------------------------------------------------------------

def _cell_id() -> str:
    return uuid.uuid4().hex[:8]


def md_cell(text: str) -> dict:
    return {"cell_type": "markdown", "id": _cell_id(), "metadata": {},
            "source": text.strip("\n").splitlines(keepends=True)}


def code_cell(text: str) -> dict:
    return {"cell_type": "code", "id": _cell_id(), "metadata": {},
            "execution_count": None, "outputs": [],
            "source": text.strip("\n").splitlines(keepends=True)}


def _stable_ids(cells: list[dict]) -> None:
    """Cell ids derived from position + content, so re-running the converter
    on an unchanged script produces an identical notebook (clean git diffs)."""
    import hashlib
    for i, cell in enumerate(cells):
        digest = hashlib.sha1(f"{i}:{''.join(cell['source'])}".encode()).hexdigest()
        cell["id"] = digest[:8]


def new_notebook(cells: list[dict]) -> dict:
    _stable_ids(cells)
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": KERNELSPEC,
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write_notebook(nb: dict, path: Path, indent: int = 1) -> None:
    path.write_text(json.dumps(nb, indent=indent, ensure_ascii=False) + "\n", encoding="utf-8")


def detect_indent(text: str) -> int:
    """Keep an existing notebook's JSON indentation (Colab uses 2, Jupyter 1) so diffs stay small."""
    for line in text.splitlines()[1:3]:
        stripped = line.lstrip(" ")
        if stripped:
            return max(1, len(line) - len(stripped))
    return 1


# --------------------------------------------------------------------------
# Source analysis and rewriting
# --------------------------------------------------------------------------

def imported_modules(source: str) -> set[str]:
    mods = set(re.findall(r"^\s*(?:import|from)\s+([A-Za-z_]\w*)", source, re.M))
    return mods


def required_packages(source: str) -> list[str]:
    mods = imported_modules(source)
    if re.search(r"read_excel|to_excel", source):
        mods.add("openpyxl")
    if re.search(r"^\s*%matplotlib\s+(widget|ipympl)", source, re.M):
        mods.add("ipympl")
    pkgs: list[str] = []
    for mod, needed in PIP_FOR_IMPORT.items():
        if mod in mods:
            pkgs += [p for p in needed if p not in pkgs]
    return pkgs


def install_line(source: str) -> str | None:
    pkgs = required_packages(source)
    return f"%pip install {' '.join(pkgs)}" if pkgs else None


def swap_solver(source: str) -> tuple[str, bool]:
    new = SOLVER_PATTERN.sub(SOLVER_REPLACEMENT, source)
    if "appsi_highs" not in new:
        new = SOLVER_LIST_PATTERN.sub(lambda m: '["appsi_highs", ' + m.group(1), new)
    return new, new != source


def setup_cell(source: str) -> dict | None:
    line = install_line(source)
    if not line:
        return None
    text = (
        "# Run this cell first.\n"
        "# In the browser (JupyterLite) it installs the extra packages into this tab;\n"
        "# in Colab or Anaconda it installs them with pip (already installed = no change).\n"
        + line
    )
    if "pyomo" in imported_modules(source):
        text += "\n\n" + PYOMO_BROWSER_FIX
    return code_cell(text)


SCIPY_HIGHS = re.compile(r"\b(linprog|milp)\s*\(")


def browser_warnings(source: str) -> list[dict]:
    cells = []
    if "pyomo" in imported_modules(source) and SCIPY_HIGHS.search(source):
        cells.append(md_cell(
            "> **Browser warning.** This notebook uses SciPy's `linprog`/`milp` *and* Pyomo with HiGHS. "
            "In the browser both bring their own copy of HiGHS and the kernel crashes "
            "(\"table index is out of bounds\"). Split it into two notebooks, or run it in Colab or Anaconda."
        ))
    for mod, name in NO_BROWSER_BUILD.items():
        if mod in imported_modules(source):
            cells.append(md_cell(
                f"> **Does not run in the browser.** This notebook uses {name}, which has no "
                "WebAssembly build. Run it in Google Colab or Anaconda Jupyter "
                f"(`pip install {mod}`)."
            ))
    return cells


def _is_valid(chunk: str) -> bool:
    """True if the chunk compiles on its own (catches 'yield' outside a function too)."""
    try:
        compile(chunk, "<cell>", "exec", flags=ast.PyCF_ONLY_AST)
        compile(chunk, "<cell>", "exec")
        return True
    except SyntaxError:
        return False


def split_script(source: str) -> list[str]:
    """Split at top-level comment headings preceded by a blank line."""
    lines = source.splitlines(keepends=True)
    chunks: list[list[str]] = [[]]
    for i, line in enumerate(lines):
        starts_heading = (
            line.startswith("#")
            and not line.startswith("#!")
            and i > 0
            and lines[i - 1].strip() == ""
            and any(l.strip() for l in chunks[-1])
        )
        if starts_heading:
            chunks.append([])
        chunks[-1].append(line)
    parts = ["".join(c).strip("\n") for c in chunks if "".join(c).strip()]
    # merge chunks that hold only comments into the next one
    merged: list[str] = []
    carry = ""
    for p in parts:
        if all(l.strip().startswith("#") or not l.strip() for l in p.splitlines()):
            carry += p + "\n\n"
            continue
        merged.append(carry + p)
        carry = ""
    if carry:
        if merged:
            merged[-1] += "\n\n" + carry.strip("\n")
        else:
            merged.append(carry.strip("\n"))
    if len(merged) > 1 and all(_is_valid(p) for p in merged):
        return merged
    return [source.strip("\n")]


def docstring_and_body(source: str) -> tuple[str | None, str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None, source
    doc = ast.get_docstring(tree)
    if not doc or not tree.body:
        return None, source
    first = tree.body[0]
    lines = source.splitlines(keepends=True)
    body = "".join(lines[first.end_lineno:])
    head = "".join(lines[: first.lineno - 1])  # shebang / coding / comments before docstring
    return doc, head + body


def title_from_name(path: Path) -> str:
    title = path.stem.replace("_", " ").strip()
    return title[:1].upper() + title[1:]


# --------------------------------------------------------------------------
# Converters
# --------------------------------------------------------------------------

def convert_script(path: Path) -> tuple[dict, list[str]]:
    source = path.read_text(encoding="utf-8", errors="replace")
    notes: list[str] = []
    source, swapped = swap_solver(source)
    if swapped:
        notes.append("solver GLPK -> HiGHS")
    doc, body = docstring_and_body(source)

    intro = f"# {title_from_name(path)}\n\n"
    if doc:
        intro += doc.strip() + "\n\n"
    intro += f"*Notebook version of `{path.name}`.*"
    if swapped:
        intro += (" The solver was changed from GLPK to HiGHS (`appsi_highs`) so it runs in "
                  "the browser; the model and its answers are unchanged.")

    cells = [md_cell(intro)]
    cells += browser_warnings(source)
    setup = setup_cell(source)
    if setup:
        cells.append(setup)
    cells += [code_cell(chunk) for chunk in split_script(body)]
    return new_notebook(cells), notes


FENCE = re.compile(r"^```(\w*)\s*$")


def convert_markdown(path: Path) -> tuple[dict, list[str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    cells: list[dict] = []
    notes: list[str] = []
    buf: list[str] = []
    code: list[str] | None = None
    lang = ""
    all_code = ""
    for line in text.splitlines(keepends=True):
        m = FENCE.match(line.rstrip("\n"))
        if code is None and m:
            if "".join(buf).strip():
                cells.append(md_cell("".join(buf)))
            buf = []
            code, lang = [], m.group(1).lower()
            continue
        if code is not None and line.strip() == "```":
            block = "".join(code)
            if lang in ("python", "py", "python3") and not _is_valid(block):
                # a fragment (e.g. "..." placeholders): show it, don't run it
                cells.append(md_cell(f"```python\n{block}```"))
                if "fragment shown as text" not in notes:
                    notes.append("fragment shown as text")
            elif lang in ("python", "py", "python3"):
                block, swapped = swap_solver(block)
                if swapped and "solver GLPK -> HiGHS" not in notes:
                    notes.append("solver GLPK -> HiGHS")
                cells.append(code_cell(block))
                all_code += block + "\n"
            else:
                cells.append(md_cell(f"```{lang}\n{block}```"))
            code = None
            continue
        (code if code is not None else buf).append(line)
    if "".join(buf).strip():
        cells.append(md_cell("".join(buf)))

    front = browser_warnings(all_code)
    setup = setup_cell(all_code)
    if setup:
        front.append(setup)
    cells = cells[:1] + front + cells[1:] if cells else front
    return new_notebook(cells), notes


APT_GLPK = re.compile(r"^\s*!\s*(sudo\s+)?apt(-get)?\s+install\b.*(glpk|coinor|cbc).*$\n?", re.M)
SHELL_PIP = re.compile(r"^(\s*)[!%]\s*pip3?\s+install\s+(.*)$", re.M)


def _fix_pip_line(match: re.Match) -> str:
    """'!pip install -q pyomo' -> '%pip install pyomo highspy' (works in JupyterLite)."""
    indent, args = match.group(1), match.group(2)
    pkgs = [a for a in args.split() if not a.startswith("-")]
    if any(p.lower().startswith("pyomo") for p in pkgs) and "highspy" not in pkgs:
        pkgs.append("highspy")
    return f"{indent}%pip install {' '.join(pkgs)}"


def _complete_install_cell(nb: dict, all_code: str) -> list[str]:
    """Make the first %pip cell install every package the notebook needs and,
    for Pyomo notebooks, carry the browser fix."""
    notes: list[str] = []
    needed = required_packages(all_code)
    for cell in nb["cells"]:
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell.get("source", []))
        m = re.search(r"^(\s*%pip install)(.*)$", src, re.M)
        if not m:
            continue
        have = m.group(2).split()
        missing = [p for p in needed if p not in have]
        if missing:
            src = src[: m.start()] + m.group(1) + " " + " ".join(have + missing) + src[m.end():]
            notes.append(f"added {', '.join(missing)} to %pip install")
        if "pyomo" in imported_modules(all_code) and BROWSER_FIX_V2_MARKER not in all_code:
            if OLD_PYOMO_BROWSER_FIX in src:
                src = src.replace(OLD_PYOMO_BROWSER_FIX, PYOMO_BROWSER_FIX)
                notes.append("Pyomo browser fix updated")
            elif BROWSER_FIX_MARKER not in all_code:
                src = src.rstrip("\n") + "\n\n" + PYOMO_BROWSER_FIX
                notes.append("Pyomo browser fix added")
        cell["source"] = src.splitlines(keepends=True)
        break
    return notes


def patch_notebook(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    nb = json.loads(raw)
    notes: list[str] = []
    all_code = ""
    has_pip = False
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell.get("source", []))
        new, swapped = swap_solver(src)
        if swapped and "solver GLPK -> HiGHS" not in notes:
            notes.append("solver GLPK -> HiGHS")
        cleaned = APT_GLPK.sub("", new)
        if cleaned != new:
            notes.append("apt-get GLPK install removed")
        fixed = SHELL_PIP.sub(_fix_pip_line, cleaned)
        if fixed != cleaned:
            notes.append("pip line made browser-compatible")
        if re.search(r"^\s*%pip install", fixed, re.M):
            has_pip = True
        if fixed != src:
            cell["source"] = fixed.splitlines(keepends=True)
        all_code += fixed + "\n"
    if not has_pip:
        setup = setup_cell(all_code)
        if setup:
            nb["cells"].insert(0, setup)
            notes.append("install cell added")
    else:
        notes += _complete_install_cell(nb, all_code)
    if nb.get("nbformat_minor", 0) >= 5:
        for cell in nb["cells"]:
            cell.setdefault("id", _cell_id())
    if notes:
        write_notebook(nb, path, indent=detect_indent(raw))
    return notes


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def iter_files(target: Path, suffixes: tuple[str, ...]):
    if target.is_file():
        if target.suffix in suffixes:
            yield target
        return
    for p in sorted(target.rglob("*")):
        if (p.is_file() and p.suffix in suffixes and not (set(p.parts) & SKIP_DIRS)
                and not any(part.endswith("Source Files") for part in p.parts)):
            yield p


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("targets", nargs="+", type=Path, help="files or folders")
    ap.add_argument("--force", action="store_true", help="overwrite existing notebooks")
    ap.add_argument("--patch-notebooks", action="store_true",
                    help="patch existing .ipynb files instead of converting scripts")
    ap.add_argument("--markdown", action="store_true",
                    help="also convert .md files that contain ```python blocks")
    args = ap.parse_args(argv)

    made = skipped = 0
    for target in args.targets:
        if args.patch_notebooks:
            for nb_path in iter_files(target, (".ipynb",)):
                notes = patch_notebook(nb_path)
                if notes:
                    print(f"patched  {nb_path}  ({', '.join(dict.fromkeys(notes))})")
                    made += 1
            continue

        suffixes = (".py", ".md") if (args.markdown or target.suffix == ".md") else (".py",)
        for src in iter_files(target, suffixes):
            if src.suffix == ".md" and "```python" not in src.read_text(errors="replace"):
                continue
            if src.parent.name == "tools":
                continue
            out = src.with_suffix(".ipynb")
            if out.exists() and not args.force:
                print(f"exists   {out}  (use --force to overwrite)")
                skipped += 1
                continue
            nb, notes = (convert_markdown if src.suffix == ".md" else convert_script)(src)
            write_notebook(nb, out)
            made += 1
            print(f"wrote    {out}" + (f"  ({', '.join(notes)})" if notes else ""))
    print(f"\n{made} notebook(s) written or patched, {skipped} skipped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
