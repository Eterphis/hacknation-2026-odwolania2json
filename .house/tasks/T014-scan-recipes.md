---
id: T014
title: Recipes robust on real scans - odwolanie and przelew fields that break on changed layouts
status: review
owner: coder
branch: task/T014-scan-recipes
depends_on: [T013]
capabilities: [python]
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 900
  - id: AC-2
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.prep_skany .acc/sk && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/sk/input --output .acc/sk/output && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred .acc/sk/output --gold .acc/sk/gold"
    expect: "score >= 0.80"
    timeout: 2400
  - id: AC-3
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe C:/Users/jasiu/workspace/.house/accept/prep_input.py .acc/input 41-60 && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/input --output .acc/output && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred .acc/output --gold C:/Users/jasiu/workspace/uzp-data/dane --cases 41-60"
    expect: "score >= 0.94"
    timeout: 1800
  - id: AC-4
    run: "! grep -rniE 'odwolanie|odwołanie|pelnomocnictw|pełnomocnictw|przelew|mocodawca|OdwolanieKIO|Zamawiajacy|Odwolujacy' odw2json/engine"
    timeout: 60
protected: []
---
## Objective
Raise exact F1 on the 30 UZP scans (`dane/skany`, our closest proxy for the real test set: same structure, changed
layout, D-017) from 0.73 to >= 0.80 without dropping held-out 41-60 below 0.94, with generic recipe rules a lawyer
would recognise, not per-scan hacks. The mentors named the hardest part: who is who (sender/receiver, Odwołujący vs
Zamawiający vs pełnomocnik) when the text is not uniform.

## Where the points are (HOUSE_DIR/reports/T013.md, "Weakest fields on scans")
- odwolanie (0.66): `ZamowieniePubliczne.tytul` 0/10; pełnomocnik block 0/9 (`imie_nazwisko`, `nazwa` runs into the
  address "… ul. Polna 115", so `przez-pelnomocnika` is 0 instead of 1: derive it from ANY pełnomocnik field found);
  `czynnosc_dzien` 0.10; `Odwolujacy.nazwa` 0.50; `numer_ted` 0.60; czynnosc id/opis 0.75.
- przelew (0.70): `tytul` 0.33 (OCR drops Polish diacritics: "odwolania" vs gold "odwołania" -> a small, generic
  diacritics-restoring normaliser driven by a dictionary file of domain words is fine; no gold copying),
  `numer_transakcji` 0.40, accounts 0.71-0.82 (gold keeps the `PL` prefix in some files: report it, do not chase it).
- pelnomocnictwo is 0.92: leave it unless a shared rule helps (PESEL per attorney is optional).

## Context
- HOUSE_DIR = C:/Users/jasiu/workspace/.house. Read D-007, D-014..D-017, reports/T004.md, T005.md, T006.md, T013.md,
  `docs/ADDING_A_DOCUMENT_CLASS.md` (recipe reference; keep it in sync for anything you add:
  `tests/test_docs_recipe_reference.py` checks it).
- Eval: `python -m eval.prep_skany <dir>` then CLI + `python -m eval.score --pred <dir>/output --gold <dir>/gold --report <file>`.
  The scans are 10 per type; when you tune, check the effect on all of them and on 41-60, and keep negatives at 12/12
  (`<dir>/output/negatywne/*.json` must stay `{}`). OCR words are cached (`%TEMP%/odw2json-ocr-cache`).
- You own `recipes/odwolanie.yaml`, `recipes/przelew.yaml`, `dictionaries/`, generic engine additions + unit tests
  (no class names in `odw2json/engine`). Another coder works on the pipeline/CLI/eval bench (T012) and one on `web/`
  (T015) in parallel: do not edit `odw2json/pipeline.py`, `odw2json/cli.py`, `eval/` or `web/`.
- Report per-field scan table before/after and 41-60 in HOUSE_DIR/reports/T014.md.

## Out of scope
LLM reading (T016), case consistency (T009), `eval/score.py`, `odw2json/model.py`.
