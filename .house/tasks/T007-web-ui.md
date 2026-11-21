---
id: T007
title: Web prototype - upload a case, see classes, JSON and per-field evidence
status: doing
owner: coder
branch: task/T007-web-ui
depends_on: [T001]
capabilities: [python, frontend]
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 900
  - id: AC-2
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -c \"import sys; from fastapi.testclient import TestClient; from web.app import app; c=TestClient(app); fs=[('files',(n,open('C:/Users/jasiu/workspace/uzp-data/dane/przyklad_07/'+n,'rb'),'application/pdf')) for n in ('odwolanie.pdf','pelnomocnictwo.pdf','potwierdzenie_przelewu.pdf')]; r=c.post('/api/process',files=fs); j=r.json(); names=sorted(d['output_name'] or '' for d in j['documents']); print(r.status_code,names); h=c.get('/'); sys.exit(0 if r.status_code==200 and names==['odwolanie.json','pelnomocnictwo.json','potwierdzenie_przelewu.json'] and all('data' in d and 'evidence' in d and 'classification' in d for d in j['documents']) and h.status_code==200 else 1)\""
    timeout: 900
  - id: AC-3
    manual: "Judge opens the UI in a browser, uploads przyklad_07 plus the template case (scan + TED notice), sees each file's class and score (TED marked as rejected), the JSON per document with a download button (single JSON and a ZIP in the ./output layout), and for each field its value, page, snippet and rule; the page is usable at 1280px and on a phone width."
protected: []
---
## Objective
The prototype UZP asks for ("link do GitHub działającego prototypu umożliwiający wgranie dokumentów i odczytanie rezultatów"): a FastAPI app (`web/app.py`, run with `python -m web` or `uvicorn web.app:app`) with one page where a user uploads the PDFs of a case (drag and drop, several files), the server runs `odw2json.pipeline.process_case` on them in a temp case folder, and the page shows per document: detected class and score (or "odrzucony" with the reason), the JSON (pretty, copy/download), and an evidence table (field path, value, page, source snippet, rule, confidence), plus the case consistency checks when present. Download all results as a ZIP in the `output/<case>/<name>.json` layout. UI language Polish.

## Context
- HOUSE_DIR = C:/Users/jasiu/workspace/.house. Read spec.yaml (`deliverables`, `scoring.rubric` transparency), D-007.
- API: `POST /api/process` (multipart `files`) -> `{"case": str, "documents": [{"input_name", "output_name", "classification": {"doc_class","score","scores","reason"}, "data", "evidence": [...], "warnings"}], "checks": [...]}` built from `CaseResult` (dataclasses.asdict is fine); `GET /` serves the page; `GET /api/recipes` lists the loaded recipe classes (for the "new class" demo later). Works with T001 stubs now and the real engine later without changes.
- Plain HTML + a little vanilla JS (or htmx) served by FastAPI; no Node build step. Keep it clean and readable, not a template look. FastAPI (MIT), uvicorn (BSD-3), python-multipart (Apache-2.0), httpx for TestClient; add to requirements.txt (append) and install into C:/Users/jasiu/workspace/.venv.
- Must also run in "light mode" on a small free host later (no LLM; OCR may be slow): show a progress state while processing.
- You own `web/` and its tests.

## Out of scope
Engine logic, recipe editing in the browser (later stretch), Docker (T008), evidence boxes drawn on page images (later stretch; leave a hook: evidence may carry `bbox`).
