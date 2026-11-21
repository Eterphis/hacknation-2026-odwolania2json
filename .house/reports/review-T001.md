# Review T001: package skeleton, schema-complete writer, CLI I/O contract

- **Reviewer:** judge (opus), standing in for `house review` (no claude/codex CLI on this machine)
- **Branch:** task/T001-skeleton-cli @ 9b07de6 (2 commits over main), worktree `.worktrees/T001-skeleton-cli`; branch not modified
- **Date:** 2026-11-21

VERDICT: CHANGES

Two MAJOR defects, both cheap (about 15 lines in total). The I/O contract, writer, schemas and pipeline seam are good.

## What I ran
| Check | Result |
|---|---|
| `python -m unittest discover -s tests -t .` | 20 tests OK (the CLI test prints its summary line to stdout, harmless) |
| AC-2 reproduced in scratch (prep_input 01-60, CLI, output_shape.py) | `60 cases, 180 pdfs, 180 json written`, `ok: 180 files` |
| **Class actually written per file** (top-level key of each output JSON) | **odwolanie.json -> pelnomocnictwo schema 60/60; potwierdzenie_przelewu.json -> pelnomocnictwo 3/60** (przyklad_08, 15, 37); pelnomocnictwo 60/60 correct. 63/180 docs (35%) get the wrong schema |
| Template case `uzp-data/szablon-aplikacja/input/case1` | both PDFs rejected, nothing written. `przyklad odwolanie.pdf` is a scan with no text layer (7 pages, 12 chars), so this is expected until T003 (OCR); `negatywny przyklad.pdf` (TED notice) correctly rejected |
| Odd names: case `sprawa źółć 1`, files `Odwołanie Nr 1.PDF`, `pełnomocnictwo.v2.Pdf`, `notatka.txt`, file named ` `, empty case folder, nested `pod folder/przelew.pdf`, loose `input/loose.pdf`, a non-PDF named `broken.pdf`, a `.json` in a case | `Odwołanie Nr 1.json`, `pełnomocnictwo.v2.json` written in `sprawa źółć 1/`; UTF-8, no BOM, no `\u` escapes; txt/json/blank-name ignored; broken.pdf logged as an error and skipped, batch continues. Nested and loose PDFs ignored **silently** (see MINOR-1) |
| `start.bat` run via `cmd /c` from `C:\` | `cd /d "%~dp0"` works from any cwd. With no repo `.venv` it fell back to PATH `python` (msys64, no pdfplumber): **every PDF failed with ModuleNotFoundError, summary `0 json written`, exit code 0** (see MAJOR-2) |
| Schemas vs `uzp-data/oczekiwane-json` and vs all 180 training JSONs | key-for-key identical; no extra or missing paths in any training file; training data never has an empty list or a null object, so "one all-null item" and "object of nulls" match the reference shape |

## Findings

### MAJOR-1 Stub classifier labels every odwołanie as pełnomocnictwo — `odw2json/stubs.py:37,40`
`pelnomocnictwo` scores 2.0 whenever the substring "pełnomocnictw" appears **anywhere** (every odwołanie mentions the attorney's power of attorney; some transfer titles say "opłata skarbowa od pełnomocnictwa"), and `max()` breaks the 2.0-vs-2.0 tie by dict order, so pelnomocnictwo wins over odwolanie (line 40). The three przelew failures have no "potwierdzenie" word, so przelew scores 0 (line 36) and the pelnomocnictwo keyword wins.
Why it matters before T004: main will emit the wrong schema for 100% of appeals, so any interim F1 run with the T002 scorer, and any T007 UI demo, shows odwolanie = 0 and a misleading baseline. AC-2 passed only because `output_shape.py` accepts "one of the three schemas" (the worker report's "stub accepts every training document" is true, but the classes are wrong). `tests/test_stubs.py:19` uses an odwołanie text without the word "pełnomocnictw", so the tests miss it.
Fix: look for the heading only near the start of the document (e.g. the first ~300 chars of squashed text) for pelnomocnictwo, drop the "potwierdzenie" requirement or accept "przelew"+"rachunk"/"kwota", and break ties in order odwolanie > przelew > pelnomocnictwo; add a test with a real-looking odwołanie text that mentions "pełnomocnictwo". Coordinator: make `output_shape.py` (or a new accept helper) check the class against the training filename (odwolanie/pelnomocnictwo/potwierdzenie_przelewu) so a green AC means a correct class.

### MAJOR-2 Missing dependency is swallowed as per-document failure, exit 0 — `odw2json/pipeline.py:27`, `odw2json/stubs.py:14`, `odw2json/cli.py:20`
`import pdfplumber` is lazy inside `ingest()`, and `except Exception` around each PDF catches the `ModuleNotFoundError`, so an environment without `pip install -r requirements.txt` produces an empty `output/` and exit code 0. That is exactly how a jury run in a fresh environment fails, and it would score as broken with no visible cause beyond a wall of tracebacks. The same applies later to OCR engines (T003) and recipe/config load errors (T004).
Fix: build the components before the loop and let construction errors escape (import pdfplumber in `PdfplumberIngestor.__init__` or at module top; factory failures are not per-document), re-raise `ImportError`/`OSError` from `_process_pdf` instead of turning them into warnings, and return a non-zero exit code from `cli.main` when PDFs were found and every one failed with an error (not a rejection). Optionally `start.bat` prints "run pip install -r requirements.txt" when `python -c "import pdfplumber"` fails.

### MINOR-1 Nested and loose PDFs are ignored silently — `odw2json/pipeline.py:15,53`
`input/loose.pdf` and `input/<case>/<sub>/x.pdf` produce no output and no log line. The contract is flat `<case>/*.pdf`, so ignoring is defensible, but a missed file costs F1 recall with no trace. At least `log.warning` each skipped PDF; better, recurse inside a case and mirror the relative path in output (`rglob("*")` + `relative_to(case_dir)`), which also makes a stray sub-folder in the hidden set harmless.

### MINOR-2 Writer hard-codes the three classes and lives outside the recipe config — `odw2json/write.py:9-10,17`
`CLASSES` is a fixed tuple and `skeleton()` raises `KeyError` for anything else, so a fourth class added "only in YAML" (D-010 goal, flexibility 30-50% of the final) still needs a code change here. Discover classes from `schemas/*.json` (or let T004's recipe point at its schema file) and drop the tuple. `SCHEMA_DIR` sits outside the package (`parent.parent / "schemas"`); fine for the repo layout, but T008's Docker image must copy `schemas/`, and T004 should not create a second copy of the same shape inside recipes.

### MINOR-3 A dict where a list is expected is silently discarded — `odw2json/write.py:30`
If an extractor returns `{"Odwolujacy": {"nazwa": "X"}}` (single entity as an object, a likely recipe-author mistake), `_fill` replaces it with one all-null item and the value is lost. Wrap a dict into `[dict]` before filling; one line plus a test.

### MINOR-4 Small robustness and seam notes
- `odw2json/pipeline.py:35-37` and `:49-51` duplicate default resolution; `factory.default_*()` build a fresh instance on every `process_case` call. For the web UI (T007, one call per upload) and an OCR engine (T003) with seconds of model load, factory should cache (e.g. `functools.cache`) or return one `Components` object.
- `process_input` never clears stale JSONs: a document accepted in an earlier run and rejected now keeps its old file. Fine for a fresh jury run; note it in the README or delete `<output>/<case>/*.json` for cases being reprocessed.
- `start.bat:4` changes cwd to the repo, so a relative `--input ..\x` is resolved against the repo, not the caller's folder. Acceptable (the contract uses repo-relative `input/`), worth one line in the README.
- There is no `start.sh` for Linux/macOS juries; T008 (Docker) covers it, but a two-line `start.sh` is cheap.

## Seam assessment (codebase-design)
`pipeline` is a reasonably deep module: two functions (`process_case` pure and write-free for the UI, `process_input` for the CLI), Protocol-typed injection, per-document fault isolation. `factory` is shallow (three one-line functions) but it is the single documented switch point for T003/T004, so it passes the deletion test as a seam; caching would give it real depth. `write.complete` is the right single place for schema completion and keeps the extractor free of shape concerns. No contract change to `model.py` is needed. Nothing here blocks T003/T004/T007 once MAJOR-2's "components built before the loop" change is in.

## Cheapest change with the most value
Fix the classifier tie (`stubs.py:37,40`: heading-only match for pelnomocnictwo plus odwolanie-first tie-break) and make AC-2 check the class by filename; it turns 63 wrong-schema outputs into correct ones and makes every later F1 baseline honest.
