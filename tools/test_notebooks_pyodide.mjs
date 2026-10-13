#!/usr/bin/env node
/**
 * test_notebooks_pyodide.mjs
 * ==========================
 * Runs notebooks inside Pyodide (the same Python-in-WebAssembly engine that the
 * JupyterLite site uses) and reports which ones fail. GitHub Actions runs it on
 * every push, so a broken notebook shows up before students open it.
 *
 *   node tools/test_notebooks_pyodide.mjs --pyodide <dir with pyodide.mjs> [notebooks or folders...]
 *
 * How each notebook is run
 *   - a fresh Python per notebook, current folder = the notebook's folder
 *   - "%pip install a b" lines -> micropip.install(["a", "b"]) (from PyPI)
 *   - other % / ! lines (e.g. %matplotlib inline) are skipped
 *   - Matplotlib uses the non-interactive Agg backend; plt.show() does nothing
 *   - sys.stdout behaves like the notebook's (write() returns None)
 *   - a cell tagged "raises-exception" may fail without failing the notebook
 *   - notebooks that import OR-Tools are reported as SKIP (no browser build)
 *
 * Options
 *   --pyodide DIR      folder of an unpacked Pyodide release (required)
 *   --timeout SEC      per-notebook time limit (default 300)
 *   --extra-path DIR   local folder to add to sys.path (repeatable; offline testing)
 *   --preload A,B      Pyodide packages to load up front (offline testing)
 *   --summary FILE     also write a Markdown results table (e.g. $GITHUB_STEP_SUMMARY)
 *
 * Exit code is 1 if any notebook FAILs, 0 otherwise.
 */
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const SELF = fileURLToPath(import.meta.url);
const NO_BROWSER_BUILD = { ortools: "Google OR-Tools has no browser build" };

function parseArgs(argv) {
  const opts = { targets: [], extraPaths: [], timeout: 300, pyodide: null, summary: null, child: null, preload: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--pyodide") opts.pyodide = path.resolve(argv[++i]);
    else if (a === "--timeout") opts.timeout = Number(argv[++i]);
    else if (a === "--extra-path") opts.extraPaths.push(path.resolve(argv[++i]));
    else if (a === "--summary") opts.summary = argv[++i];
    else if (a === "--preload") opts.preload = argv[++i].split(",").filter(Boolean);
    else if (a === "--child") opts.child = path.resolve(argv[++i]);
    else opts.targets.push(a);
  }
  if (!opts.pyodide) throw new Error("--pyodide <dir> is required");
  return opts;
}

function findNotebooks(targets) {
  const out = [];
  const walk = (p) => {
    const st = fs.statSync(p);
    if (st.isDirectory()) {
      if (/(^|\/)(\.ipynb_checkpoints|node_modules|\.git)$/.test(p)) return;
      for (const f of fs.readdirSync(p).sort()) walk(path.join(p, f));
    } else if (p.endsWith(".ipynb")) out.push(path.resolve(p));
  };
  for (const t of targets.length ? targets : ["content"]) walk(t);
  return out;
}

// ---------------------------------------------------------------------------
// child: run ONE notebook and print a JSON result on the last line
// ---------------------------------------------------------------------------
async function runOne(nbPath, opts) {
  const nb = JSON.parse(fs.readFileSync(nbPath, "utf8"));
  const cells = nb.cells.filter((c) => c.cell_type === "code");
  const allCode = cells.map((c) => [].concat(c.source).join("")).join("\n");
  for (const [mod, why] of Object.entries(NO_BROWSER_BUILD)) {
    if (new RegExp(`^\\s*(import|from)\\s+${mod}\\b`, "m").test(allCode)) {
      return { status: "SKIP", detail: why };
    }
  }

  const { loadPyodide } = await import(pathToFileURL(path.join(opts.pyodide, "pyodide.mjs")).href);
  const py = await loadPyodide({ indexURL: opts.pyodide + path.sep, stdout: () => {}, stderr: () => {} });
  await py.loadPackage(["micropip", ...opts.preload], { messageCallback: () => {} });

  // the repository (current folder) is visible inside Python at the same absolute path,
  // so notebooks can read data files next to them
  const cwd = process.cwd();
  const mountRoot = nbPath.startsWith(cwd + path.sep) ? cwd : path.dirname(nbPath);
  py.FS.mkdirTree(mountRoot);
  py.FS.mount(py.FS.filesystems.NODEFS, { root: mountRoot }, mountRoot);
  opts.extraPaths.forEach((p, i) => {
    const mnt = `/extra${i}`;
    py.FS.mkdirTree(mnt);
    py.FS.mount(py.FS.filesystems.NODEFS, { root: p }, mnt);
  });

  const ns = py.globals.get("dict")();
  await py.runPythonAsync(
    `
import os, sys, builtins
os.environ["MPLBACKEND"] = "Agg"
os.chdir(${JSON.stringify(path.dirname(nbPath))})
sys.path[:0] = [${opts.extraPaths.map((_, i) => `"/extra${i}"`).join(", ")}]
def display(*objs, **kw):
    for o in objs: print(o)
builtins.display = display
class _LiteStream:
    # same interface as JupyterLite's notebook output stream (pyodide_kernel.display.LiteStream):
    # write() returns None and there is no fileno(), so code that needs either fails here too
    encoding = "utf-8"
    def __init__(self, target): self._target = target
    def write(self, text): self._target.write(text)
    def flush(self): pass
    def isatty(self): return False
sys.stdout, sys.stderr = _LiteStream(sys.__stdout__), _LiteStream(sys.__stderr__)
`,
    { globals: ns }
  );

  const micropip = py.pyimport("micropip");
  for (let idx = 0; idx < nb.cells.length; idx++) {
    const cell = nb.cells[idx];
    if (cell.cell_type !== "code") continue;
    const src = [].concat(cell.source).join("");
    const lines = [];
    for (const line of src.split("\n")) {
      const pip = line.match(/^\s*[%!]\s*pip3?\s+install\s+(.*)$/);
      if (pip) {
        const pkgs = pip[1].split(/\s+/).filter((t) => t && !t.startsWith("-"));
        try {
          await micropip.install(pkgs);
        } catch (e) {
          // offline testing: fine if the package is importable from --extra-path
          const missing = [];
          for (const p of pkgs) {
            const mod = p.split(/[<>=!\[]/)[0].replace(/-/g, "_");
            try {
              await py.loadPackagesFromImports(`import ${mod}`);
              py.runPython(`import ${mod}`, { globals: ns });
            } catch {
              missing.push(p);
            }
          }
          if (missing.length) return { status: "FAIL", detail: `cell ${idx}: cannot install ${missing.join(", ")}` };
        }
        lines.push("");
      } else if (/^\s*[%!]/.test(line)) {
        lines.push("");
      } else {
        lines.push(line);
      }
    }
    const code = lines.join("\n");
    if (!code.trim()) continue;
    const mayRaise = (cell.metadata?.tags || []).includes("raises-exception");
    if (process.env.NB_DEBUG) console.error(`--- cell ${idx}\n${code}`);
    try {
      await py.loadPackagesFromImports(code, { messageCallback: () => {} });
      await py.runPythonAsync(code, { globals: ns, filename: `<cell ${idx}>` });
    } catch (e) {
      if (mayRaise) continue;
      const msg = String(e.message || e).trim().split("\n").filter(Boolean).pop();
      return { status: "FAIL", detail: `cell ${idx}: ${msg}` };
    }
  }
  return { status: "PASS", detail: "" };
}

// ---------------------------------------------------------------------------
// parent: one child process per notebook (isolation + time limit)
// ---------------------------------------------------------------------------
async function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.child) {
    let res;
    try {
      res = await runOne(opts.child, opts);
    } catch (e) {
      res = { status: "FAIL", detail: String(e.message || e).split("\n").filter(Boolean).pop() };
    }
    process.stdout.write("\n@@RESULT@@" + JSON.stringify(res) + "\n");
    process.exit(0);
  }

  const notebooks = findNotebooks(opts.targets);
  const results = [];
  for (const nb of notebooks) {
    const t0 = Date.now();
    const args = [SELF, "--child", nb, "--pyodide", opts.pyodide];
    opts.extraPaths.forEach((p) => args.push("--extra-path", p));
    if (opts.preload.length) args.push("--preload", opts.preload.join(","));
    const proc = spawnSync(process.execPath, args, { encoding: "utf8", timeout: opts.timeout * 1000, maxBuffer: 64 << 20 });
    let res = { status: "FAIL", detail: proc.error ? `timed out after ${opts.timeout}s` : "crashed" };
    const m = (proc.stdout || "").match(/@@RESULT@@(.*)\s*$/);
    if (m) res = JSON.parse(m[1]);
    const secs = ((Date.now() - t0) / 1000).toFixed(1);
    const rel = path.relative(process.cwd(), nb);
    results.push({ ...res, nb: rel, secs });
    console.log(`${res.status.padEnd(4)} ${secs.padStart(6)}s  ${rel}${res.detail ? "  | " + res.detail : ""}`);
  }

  const count = (s) => results.filter((r) => r.status === s).length;
  const line = `${count("PASS")} passed, ${count("FAIL")} failed, ${count("SKIP")} skipped (of ${results.length})`;
  console.log("\n" + line);
  if (opts.summary) {
    const rows = results
      .filter((r) => r.status !== "PASS")
      .map((r) => `| ${r.status} | \`${r.nb}\` | ${r.detail.replace(/\|/g, "\\|")} |`);
    const md = [`### Notebook check (Pyodide)`, "", line, "", ...(rows.length ? ["| Result | Notebook | Detail |", "| --- | --- | --- |", ...rows] : [])];
    fs.appendFileSync(opts.summary, md.join("\n") + "\n");
  }
  process.exit(count("FAIL") ? 1 : 0);
}

main();
