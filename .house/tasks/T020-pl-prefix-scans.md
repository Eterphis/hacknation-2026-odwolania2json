---
id: T020
title: Account numbers keep the printed PL prefix on scanned (OCR) pages, digits only on text-layer pages
status: doing
owner: coder
branch: task/T020-pl-prefix-scans
depends_on: []
capabilities: [python]
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 900
  - id: AC-2
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.prep_skany .acc/sk && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/sk/input --output .acc/sk/output && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred .acc/sk/output --gold .acc/sk/gold"
    expect: "score >= 0.982"
    timeout: 2400
  - id: AC-3
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe C:/Users/jasiu/workspace/.house/accept/prep_input.py .acc/input 01-60 && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/input --output .acc/output && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred .acc/output --gold C:/Users/jasiu/workspace/uzp-data/dane --cases 01-60"
    expect: "score >= 0.9999"
    timeout: 1800
  - id: AC-4
    run: "! grep -rniE 'odwolanie|odwołanie|pelnomocnictw|pełnomocnictw|przelew|mocodawca|OdwolanieKIO|Zamawiajacy|Odwolujacy|z_rachunku|na_rachunek' odw2json/engine"
    timeout: 60
protected: [eval/score.py]
---
## Objective
Implement D-026 (owner's decision until the mentors answer Q-005): an account number read from a page that was
OCR-ed (`Page.source == "ocr"`, a scan) keeps the `PL` country prefix exactly when it is printed (`PL62 2170 …` →
`PL62217000089152501756617062`); read from a PDF text layer (synthetic documents) it stays digits only, as today.
Expected effect: scans `skany/potwierdzenia/0001` and `0006` `z_rachunku` become correct (scan F1 0.9789 → about
0.985); cases 01-60 stay at 1.000; no other scan field changes.

## Facts (checked by the coordinator)
- On all 10 scan transfers, gold has `PL` exactly when the print has `PL` (z_rachunku in 0001 and 0006; never in
  na_rachunek, which is printed without `PL`). Synthetic gold drops `PL` even when printed (przyklad_03).
- Today `recipes/przelew.yaml` uses `normalize: iban_pl` (strips `PL`, keeps 26 digits); normalisers get only the
  string (`odw2json/engine/normalise.py`). Evidence knows the page; `odw2json/model.py:Page.source` is `text|ocr`.

## Design constraints
- Generic and configurable, no class or field names in the engine (AC-4): e.g. a normaliser variant
  `iban_pl_as_printed` plus a way for the engine to tell a normaliser the page source, or a recipe-level option
  (`keep_prefix_on: ocr`). Pick the smallest clean design; document it in `docs/ADDING_A_DOCUMENT_CLASS.md`
  (`tests/test_docs_recipe_reference.py` checks the reference) and add unit tests first (text page → digits, OCR page with
  PL → PL+digits, OCR page without PL → digits, validation still IBAN checksum).
- Use it for both account fields in `recipes/przelew.yaml`. Do not touch OCR (`odw2json/ingest/`), web, eval.

## Context
HOUSE_DIR = C:/Users/jasiu/workspace/.house. Read D-026, Q-005, reports/misses-1.md rows 16-17. Feature freeze is at
09:30: keep it small. Report HOUSE_DIR/reports/T020.md (before/after scan F1 and the two fields).
