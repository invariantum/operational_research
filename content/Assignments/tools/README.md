# Tools (maintainers)

Run from `content/Assignments` with the project environment active (see the main README).

| Command | What it does |
|---|---|
| `python tools/run_all_checks.py` | Personal-data scan + the whole test suite (`--quick` skips running notebooks; `--allow-skips` tolerates missing packages) |
| `python tools/scan_for_personal_data.py` | Release gate: student/staff numbers, e-mail addresses, local user paths, OneDrive/SharePoint links (also hidden ones inside Office files) and author metadata. `--terms <file outside the repo>` adds your own list of names |
| `python tools/build_pdfs.py [folder]` | Rebuilds every PDF from its `.tex` source (`--check` only lists stale PDFs). Needs MiKTeX, MacTeX or TeX Live |

`tests/` holds the checks that `run_all_checks.py` runs with pytest. Every test that executes code works on a
temporary copy of the folder, so it never changes your files.

The course website runs the notebooks once more in the browser engine (Pyodide) on every push; see
`.github/workflows/test-notebooks.yml` at the top of the repository.
