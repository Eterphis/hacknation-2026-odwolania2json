---
id: T010
title: Noisy scanned held-out set as a proxy for the real test cases
status: todo
owner: teammate-session
branch: null
depends_on: [T002, T003]
capabilities: [python]
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 900
  - id: AC-2
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.make_noisy --cases 41-50 --out C:/Users/jasiu/workspace/uzp-data-noisy && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -c \"import glob,sys,pdfplumber; fs=glob.glob('C:/Users/jasiu/workspace/uzp-data-noisy/input/*/*.pdf'); txt=sum(1 for f in fs if any((p.extract_text() or '').strip() for p in pdfplumber.open(f).pages)); g=glob.glob('C:/Users/jasiu/workspace/uzp-data-noisy/gold/*/*.json'); print(len(fs),txt,len(g)); sys.exit(0 if len(fs)==30 and txt==0 and len(g)==30 else 1)\""
    timeout: 1800
  - id: AC-3
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input C:/Users/jasiu/workspace/uzp-data-noisy/input --output .acc/noisy-out && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred .acc/noisy-out --gold C:/Users/jasiu/workspace/uzp-data-noisy/gold"
    expect: "score: [0-9.]+\\s*$"
    timeout: 3600
protected: []
---
## Objective
`python -m eval.make_noisy --cases 41-50 --out <dir>` builds `<dir>/input/przyklad_NN/*.pdf` (image-only PDFs, no text layer) and `<dir>/gold/przyklad_NN/*.json` (copies of the gold) from the held-out training cases by rendering each page (pypdfium2) at a scan-like DPI and degrading it reproducibly with a fixed seed: slight rotation (±1.5°), blur, JPEG artefacts, salt-and-pepper noise, uneven brightness, optional stamp/signature blob. Then the full pipeline and scorer run on it, so we measure what OCR does to F1 — our only proxy for the hidden REAL, partly scanned cases. The score is informational (no threshold); report it next to the clean held-out score in HOUSE_DIR/reports/T010.md with the 10 worst fields.

## Context
- HOUSE_DIR = C:/Users/jasiu/workspace/.house. Read spec.yaml `task.test_data`, `task.template_case`, D-006, D-008.
- Output stays outside the repo (C:/Users/jasiu/workspace/uzp-data-noisy, data licence unclear). You own `eval/make_noisy.py` and its tests (do NOT edit `eval/score.py`). pypdfium2 (Apache-2.0/BSD-3), Pillow (MIT-CMU), numpy (BSD) are fine; append to requirements.txt and install into C:/Users/jasiu/workspace/.venv.
- Write PDFs from images with Pillow (`save(..., save_all=True)`) or img2pdf (LGPL: avoid); no AGPL tools.

## Out of scope
Changing OCR or recipes to raise the noisy score (that becomes follow-up tasks from your report).
