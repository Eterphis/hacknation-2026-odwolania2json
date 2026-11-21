---
id: T003
title: Ingest to word-box pages with per-page OCR fallback
status: done
owner: coder
branch: task/T003-ingest-ocr
depends_on: []
capabilities: [python]
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 900
  - id: AC-2
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -c \"import glob,sys; from odw2json.ingest import default_ingestor; ing=default_ingestor(); docs=[ing.ingest(p) for p in glob.glob('C:/Users/jasiu/workspace/uzp-data/dane/*/*.pdf')]; pl=sum(any(c in d.text for c in 'ąęłśżźćńó') for d in docs); boxed=sum(all(p.words and all(0<=w.x0<=w.x1<=p.width+1 and 0<=w.y0<=w.y1<=p.height+1 for w in p.words) for p in d.pages) for d in docs); print('docs',len(docs),'polish',pl,'boxed',boxed); sys.exit(0 if len(docs)>=180 and pl>=170 and boxed>=len(docs)-2 else 1)\""
    timeout: 900
  - id: AC-3
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -c \"import sys; from odw2json.ingest import default_ingestor; d=default_ingestor().ingest('C:/Users/jasiu/workspace/uzp-data/szablon-aplikacja/input/case1/przyklad odwolanie.pdf'); t=d.text.lower(); ok=len(d.pages)==7 and all(p.source=='ocr' and p.words for p in d.pages) and ('odwołuj' in t or 'odwoluj' in t) and 'zamawiaj' in t; print('chars',len(t),'ok',ok); sys.exit(0 if ok else 1)\""
    timeout: 1200
  - id: AC-4
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -c \"import sys; from odw2json.ingest import default_ingestor; d=default_ingestor().ingest('C:/Users/jasiu/workspace/uzp-data/dane/przyklad_07/odwolanie.pdf'); ok=all(p.source=='text' for p in d.pages) and 'Zamawiający' in d.text; print(ok); sys.exit(0 if ok else 1)\""
    timeout: 300
protected: []
---
## Objective
`odw2json.ingest.default_ingestor(config: dict | None = None) -> Ingestor` turns any PDF (digital or scanned) into a `Document` of `Page`s (see `odw2json/model.py`): words with bounding boxes in PDF points (origin top-left), page text in reading order, and `source` = "text" or "ocr" per page. Text-layer pages use pdfplumber words; pages whose text layer is empty or garbage (too few chars, mostly non-letters, broken encoding) are rendered and OCR'd with Polish support, mapping OCR boxes back to PDF points. This single page model is what the recipe engine (T004) and the evidence view (T007) build on.

## Context
- HOUSE_DIR = C:/Users/jasiu/workspace/.house. Read spec.yaml (`task.template_case`, `task.pitfalls`, `deliverables.hardware`), D-005, D-008, reports/licences.md.
- Contract on main, do not change: `odw2json/model.py`. You own `odw2json/ingest/` (package) and its tests; add your dependencies to `requirements.txt` (append lines only; T001 also edits this file, keep merges trivial) and install them into C:/Users/jasiu/workspace/.venv.
- OCR backend sits behind a small `OcrBackend` protocol (`ocr(image) -> list[(text, box, conf)]`) chosen by config key `ocr.backend` (env `ODW2JSON_OCR` overrides). A teammate's session is researching OCR engines; the backend choice may change later, so keep it swappable and document how to add one. Default must work after `pip install -r requirements.txt` on Windows and Linux with no system binaries and no GPU, in 16 GB RAM, and must read Polish diacritics. Candidates: RapidOCR (onnxruntime) with a Latin/Polish-capable recognition model; Tesseract `pol` via pytesseract as an optional backend when the binary exists (Docker). Licences must allow transfer of IP (avoid AGPL: no PyMuPDF, no Ghostscript/ocrmypdf); page rendering via pypdfium2 (Apache-2.0/BSD).
- Reading order: cluster words into lines by y overlap, sort by x; keep a line break between lines and a blank line between blocks with a large vertical gap. Join hyphenated line ends only in `text`, never alter `words`.
- Force UTF-8. Cache OCR results per file hash in a temp dir if it helps the run time (the template scan must OCR in a few minutes on CPU).
- Report in HOUSE_DIR/reports/T003.md: OCR backend chosen and why, timing per page, and the first ~40 OCR lines of the template scan compared with the example values in uzp-data/oczekiwane-json/odwolanie.json (is that example the gold of this scan? say yes/no/unclear with evidence).

## Out of scope
Classification, extraction, CLI wiring (T001/T004 switch the pipeline default to your ingestor). Do not touch `odw2json/model.py`, `eval/`, `recipes/`.
