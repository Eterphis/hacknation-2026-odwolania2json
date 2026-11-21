---
id: T001
title: Package skeleton, schema-complete writer and CLI input/output contract
status: review
owner: coder
branch: task/T001-skeleton-cli
depends_on: []
review: always
capabilities: [python]
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 600
  - id: AC-2
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe C:/Users/jasiu/workspace/.house/accept/prep_input.py .acc/input 01-60 && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/input --output .acc/output && C:/Users/jasiu/workspace/.venv/Scripts/python.exe C:/Users/jasiu/workspace/.house/accept/output_shape.py .acc/input .acc/output"
    expect: "ok: 180 files"
    timeout: 900
  - id: AC-3
    run: "test -f start.bat && test -f input/.gitkeep && test -f output/.gitkeep && grep -qi pdfplumber requirements.txt && grep -q '^.acc/' .gitignore"
    timeout: 60
protected: []
---
## Objective
A runnable package `odw2json` that implements the UZP input/output contract end to end with stub logic: `python -m odw2json --input <dir> --output <dir>` (defaults `./input`, `./output`) walks `<input>/<case>/*.pdf`, runs ingest -> classify -> extract for every PDF through the interfaces in `odw2json/model.py`, and writes `<output>/<case>/<pdf basename>.json` for every accepted document and nothing for rejected ones. Every written JSON is schema-complete: all keys of the UZP reference schema for its class present, `null` where unknown. Stubs are clearly marked and replaced by T003 (ingest) and T004 (classify/extract).

## Context
- HOUSE_DIR = C:/Users/jasiu/workspace/.house. Read spec.yaml (`task`, `deliverables`), D-004..D-008.
- Contract (already on main, owned by the coordinator, do NOT change): `odw2json/model.py` (Word, Page, Document, Evidence, Classification, Extraction, DocumentResult, Check, CaseResult, Ingestor/Classifier/Extractor protocols).
- UZP reference schemas (JSON with `//` comments, one has a missing comma): C:/Users/jasiu/workspace/uzp-data/oczekiwane-json/{odwolanie,pelnomocnictwo,przelew}.json. Training data: C:/Users/jasiu/workspace/uzp-data/dane/przyklad_NN/ (gitignored; never copy it into the repo).
- You own: `odw2json/__main__.py`, `odw2json/cli.py`, `odw2json/pipeline.py`, `odw2json/write.py`, `odw2json/stubs.py`, `schemas/` (clean skeletons: same keys as the UZP schemas, all leaves null, lists with exactly one item template; the writer emits one list item per extracted entity and, when nothing was found, one item with all leaves null — null leaves cost nothing in the scorer and keep the shape), `start.bat` (Windows: runs the CLI with the repo's Python), `requirements.txt`, `input/.gitkeep`, `output/.gitkeep`, `.gitignore` additions (`.acc/`, `input/*`, `output/*` except `.gitkeep`), `tests/` for these modules.
- `pipeline.py` exposes `process_case(case_dir, ingestor, classifier, extractor) -> CaseResult` and `process_input(input_dir, output_dir, ingestor=None, classifier=None, extractor=None) -> list[CaseResult]`; `None` = defaults, resolved by a small factory (`odw2json/factory.py` or inside pipeline) that later tasks switch from stubs to real modules. The web UI (T007) will call `process_case`.
- Stub ingestor: pdfplumber page text only (no OCR, empty `words` allowed). Stub classifier: keyword scores on the text (e.g. "potwierdzenie" + "przelew" -> przelew, "pełnomocnictw" heading -> pelnomocnictwo, "odwołanie" + "Krajowej Izby" -> odwolanie), reject when nothing matches. Stub extractor: returns the null skeleton.
- Force UTF-8 everywhere (file reads/writes, `json.dump(..., ensure_ascii=False)`), output must not depend on the Windows code page.
- Python 3.13; shared venv C:/Users/jasiu/workspace/.venv (install what you add to requirements.txt into it). Tests: `python -m unittest discover -s tests -t .`.

## Out of scope
OCR and word boxes (T003), the recipe engine and real classification (T004), the scorer (T002), UI (T007), Docker/docs (T008). Do not edit `odw2json/model.py`; if the contract is insufficient, write a Q in your report and work around it.
