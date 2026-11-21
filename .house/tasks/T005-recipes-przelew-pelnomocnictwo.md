---
id: T005
title: Complete recipes for przelew and pelnomocnictwo to held-out F1 targets
status: done
owner: teammate-session
branch: task/T005-recipes-przelew-pelnomocnictwo
depends_on: [T002, T004]
capabilities: [python]
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 900
  - id: AC-2
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe C:/Users/jasiu/workspace/.house/accept/prep_input.py .acc/input 41-60 && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/input --output .acc/output && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred .acc/output --gold C:/Users/jasiu/workspace/uzp-data/dane --cases 41-60 --types przelew"
    expect: "score >= 0.95"
    timeout: 1800
  - id: AC-3
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe C:/Users/jasiu/workspace/.house/accept/prep_input.py .acc/input 41-60 && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/input --output .acc/output && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred .acc/output --gold C:/Users/jasiu/workspace/uzp-data/dane --cases 41-60 --types pelnomocnictwo"
    expect: "score >= 0.90"
    timeout: 1800
  - id: AC-4
    run: "! grep -rniE 'pelnomocnictw|pełnomocnictw|przelew|mocodawca' odw2json/engine"
    timeout: 60
protected: []
---
## Objective
`recipes/przelew.yaml` and `recipes/pelnomocnictwo.yaml` extract every field of the UZP schemas (see the `//` comments in uzp-data/oczekiwane-json/*.json, they are the field spec) with exact-mode F1 >= 0.95 (przelew) and >= 0.90 (pelnomocnictwo) on the HELD-OUT cases 41-60, tuning only on cases 01-40. Improvements to the engine are allowed only as generic strategies/normalisers (no class names in `odw2json/engine/`), each with a unit test.

## Context
- HOUSE_DIR = C:/Users/jasiu/workspace/.house. Read spec.yaml `task`, D-005, D-007, reports/ideation-1.md findings 5-6 (two bank layouts: label-left/value-right rows and label-row/value-row grids; consortium principals; podpisujacy lists; nominative names), the engine docs from T004.
- Scorer: `python -m eval.score --pred <out> --gold C:/Users/jasiu/workspace/uzp-data/dane --cases 01-40 --report <file>` shows the worst fields; never edit `eval/`.
- Generalise for REAL documents (the hidden test set is real, partly scanned): label lists with several bank/law-firm variants, OCR-tolerant label matching, no case-specific hacks, no copying of gold values. Names of pełnomocnicy in the nominative (simplemma MIT or Morfeusz2 BSD-2 are allowed if needed; spaCy Polish models are GPL: not allowed). `pesel` is a number in the schema example but null in almost all gold files: emit it only when a valid 11-digit PESEL is present.
- You own `recipes/przelew.yaml`, `recipes/pelnomocnictwo.yaml`, dictionaries they need, generic engine additions + tests. T006 works on `recipes/odwolanie.yaml` in parallel: do not edit it; if you both need a new engine strategy, keep it generic and small to avoid merge conflicts.
- Report the per-field held-out table in HOUSE_DIR/reports/T005.md.

## Out of scope
odwolanie recipe (T006), consistency across documents (T009), `eval/`, `odw2json/model.py`.
