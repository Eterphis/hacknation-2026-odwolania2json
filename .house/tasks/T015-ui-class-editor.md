---
id: T015
title: Add and edit a document class from the web UI (recipe + output schema, validate, try, no restart)
status: review
owner: coder
branch: task/T015-ui-class-editor
depends_on: [T013, T011]
capabilities: [python, frontend]
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 900
  - id: AC-2
    run: "! grep -rnE '#[0-9A-Fa-f]{6}\\b|#[0-9A-Fa-f]{3}\\b|border-radius: *[1-9]|box-shadow|backdrop-filter|filter: *blur' web --include=*.css --include=*.html --include=*.js --exclude-dir=coldtrace"
    timeout: 60
  - id: AC-3
    manual: "Judge in `python -m web`: opens 'Klasy dokumentów', creates a new class (e.g. 'wezwanie' with two fields) from the built-in template, sees a validation error with file/JSON path for a broken regex, fixes it, tests it on an uploaded PDF (classification score, extracted fields with evidence), saves it; the next upload and `python -m odw2json` on ./input use the new class without restart; editing and deleting a class work; the screen follows Cold Trace in night and daylight and at 375px."
protected: []
---
## Objective
UZP scores "ease of adding new document types and data classes without rebuilding the system" (README stage 2, up to
20 points) and the mentors said a new class must be addable through the UI or a configuration file. The engine already
adds a class from `recipes/<name>.yaml` (+ `output_schema`) with hot reload (T004). Give it a screen:
- **API** (JSON, unchanged existing routes): `GET /api/recipes` (exists: list), `GET /api/recipes/{name}` (YAML text +
  output schema + dictionaries it uses), `POST /api/recipes/validate` (text -> ok or a list of errors with JSON path
  and line, using the engine's own loader/validator), `POST /api/recipes/try` (recipe text + uploaded PDFs -> per
  document: classification scores of all classes incl. the draft, extracted JSON, evidence; nothing saved),
  `PUT /api/recipes/{name}` (validate, then write `recipes/<name>.yaml` atomically, with a `.bak` of the previous
  version), `DELETE /api/recipes/{name}` (refuses the three UZP classes unless `force`). Names: `[a-z][a-z0-9_]{1,40}`.
  Writes are disabled with a clear message when env `ODW2JSON_READONLY_RECIPES=1` (public demo hosting).
- **UI** (Cold Trace, `web/static/coldtrace/` kit, role tokens only): a "Klasy dokumentów" view: list of classes with
  field counts; an editor (Martian Mono textarea with line numbers is enough, no heavy editor dependency) prefilled
  from a commented template (`recipes/_template.yaml.example`, explains signals, fields, strategies with one example
  each); "Sprawdź" (validate), "Wypróbuj na PDF" (try), "Zapisz", "Usuń"; errors as fault toasts that say how to fix.
  A simple field builder (name, label variants, normaliser) that writes YAML is a plus, not required.
- Docs: a section in `docs/ADDING_A_DOCUMENT_CLASS.md` "Przez interfejs" with 2 screenshots in `docs/screenshots/`.

## Context
- HOUSE_DIR = C:/Users/jasiu/workspace/.house. Read D-007, D-012 (Cold Trace), D-015..D-018, reports/T004.md (engine,
  hot reload, recipe-only classes), T007.md, T011.md (UI), `design/cold-trace/README.md` (brand book).
- You own `web/` (templates, static, app routes), `tests/test_web*.py`, `recipes/_template.yaml.example`, the docs
  section. Reuse the engine's loader (`odw2json/engine/recipes.py`) for validation; if you need a small public helper
  there (e.g. validate from text), keep it generic and tested. T012 edits pipeline/cli/factory and T014 edits recipes in
  parallel: do not touch those files.
- Verify in a browser: create, try, save, use from CLI, delete; desktop + 375 px, both modes; screenshots.

## Out of scope
Recipe logic for the UZP classes, profiles/workers, LLM.
