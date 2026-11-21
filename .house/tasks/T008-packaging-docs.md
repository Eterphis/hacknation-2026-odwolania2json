---
id: T008
title: Packaging and handover docs - start.bat, Docker Compose, CI, architecture and new-class guide
status: todo
owner: null
branch: null
depends_on: [T004, T007]
capabilities: [python, devops, docs]
acceptance:
  - id: AC-1
    run: "test -f Dockerfile && test -f docker-compose.yml && docker compose config -q"
    timeout: 120
  - id: AC-2
    run: "test -f docs/ARCHITECTURE.md && test -f docs/ADDING_A_DOCUMENT_CLASS.md && test -f docs/EXTERNAL_COMPONENTS.md && test -f .github/workflows/ci.yml && test -f start.bat && grep -qi 'recipes/' docs/ADDING_A_DOCUMENT_CLASS.md && grep -qi 'licen' docs/EXTERNAL_COMPONENTS.md"
    timeout: 60
  - id: AC-3
    run: "rm -rf .acc/venv && py -3.13 -m venv .acc/venv && .acc/venv/Scripts/python.exe -m pip install -q -r requirements.txt && .acc/venv/Scripts/python.exe -m odw2json --help && .acc/venv/Scripts/python.exe -c 'import web.app'"
    timeout: 1500
  - id: AC-4
    manual: "Judge on a clean checkout: `docker compose up --build` serves the web UI on localhost and `docker compose run --rm cli` (or the documented equivalent) processes ./input into ./output; start.bat does the same on Windows with Python 3.13; README quick start works without reading the code."
protected: []
---
## Objective
Everything the jury and UZP need to run, judge and take over the solution (regulamin §3.5 handover: source code, run instructions, Docker Compose configuration, documentation with architecture, how extraction of a document class is configured and how to add a new class; §4.1: external components named). Concretely: `start.bat` (Windows: creates/uses a venv, installs requirements once, runs the CLI on ./input -> ./output; an option to start the web UI), `Dockerfile` (python:3.13-slim, CPU only, optional Tesseract `pol` layer if T003 supports it) and `docker-compose.yml` with a `web` service (UI on a port) and a `cli` service (mounts ./input and ./output), a GitHub Actions workflow running the unit tests on Python 3.13 (no UZP data in CI: tests use repo fixtures), and docs:
- `README.md` (public, Polish per spec.languages.public): what it is, quick start (start.bat / CLI / Docker / web), input/output contract, how quality was measured (our eval and its numbers placeholder), screenshots placeholder.
- `docs/ARCHITECTURE.md`: modules (ingest -> classify -> extract -> write, recipes, dictionaries, web, eval) with a diagram (mermaid), data model (`odw2json/model.py`), design decisions (D-005 no-LLM floor, config-only classes, evidence/transparency), extension points (OCR backend, recipe strategies, optional LLM/Basal classifier).
- `docs/ADDING_A_DOCUMENT_CLASS.md`: step-by-step tutorial adding a class with only a YAML file (+ optional output schema), recipe reference (every strategy, normaliser, validator, classification signal) generated or kept in sync with the engine registries.
- `docs/EXTERNAL_COMPONENTS.md`: every third-party library/model/tool with version, licence and link (from requirements.txt and HOUSE_DIR/reports/licences.md), and a statement that no AGPL/GPL component is used.
- Root `.gitignore`/`.dockerignore` keep data and outputs out.

## Context
- HOUSE_DIR = C:/Users/jasiu/workspace/.house. Read spec.yaml (`deliverables`, `rules.task_regulamin`, `languages`), D-005..D-009, reports/licences.md, the code merged from T001-T004 and T007.
- Root README.md currently describes the house tooling repo: replace it with the product README and move the house/team notes to `TEAM.md` (already exists; keep it) so the public repo reads as the product. The public submission is produced later by `house export`; do not worry about removing `house/` here.
- You own the files listed above.

## Out of scope
Engine/recipe logic, UI features. Docs describe what exists; mark planned items as planned.
