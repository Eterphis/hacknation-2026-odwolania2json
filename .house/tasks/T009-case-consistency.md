---
id: T009
title: Case-level consistency checks and cross-document value voting
status: review
owner: coder
branch: task/T009-case-consistency
depends_on: [T005, T006]
capabilities: [python]
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 900
  - id: AC-2
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe C:/Users/jasiu/workspace/.house/accept/prep_input.py .acc/input 41-60 && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/input --output .acc/output && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred .acc/output --gold C:/Users/jasiu/workspace/uzp-data/dane --cases 41-60"
    expect: "score >= 0.90"
    timeout: 1800
  - id: AC-3
    run: "! grep -rniE 'odwolanie|odwołanie|pelnomocnictw|pełnomocnictw|przelew|mocodawca' odw2json/engine"
    timeout: 60
protected: []
---
## Objective
After all documents of a case are extracted, a generic case step fills `CaseResult.checks` and may repair low-confidence values using the other documents, driven by configuration (`recipes/case/relations.yaml` or a `relations:` block), not code: e.g. pełnomocnictwo mocodawca name/NIP/KRS == odwolanie Odwołujący (or consortium member); a pełnomocnik in the pełnomocnictwo == odwolanie pełnomocnik; the proceedings number or pełnomocnik name appears in the przelew title; identifiers that fail a checksum but match another document's checksum-valid value after OCR-confusable substitutions (0/O, 1/l/I, 5/S, 8/B) are replaced, with the repair recorded in the evidence. Overall exact F1 on held-out 41-60 >= 0.90 and never lower than before this task (report both numbers). The web UI already renders `checks`.

## Context
- HOUSE_DIR = C:/Users/jasiu/workspace/.house. Read D-007 (I-002-lite only: data-consistency checks; NO fee/deadline legal checks: all training transfers are stamp duty for the power of attorney, judge evidence E4 in reports/ideation-1-judge.md), the engine docs, `odw2json/model.py` (`Check`, `CaseResult`).
- Checksums are only partly valid in the synthetic data (spec `task.pitfalls`): use them as a soft signal; never drop a value only because a checksum fails.
- You own `odw2json/case/` (or `odw2json/engine/case.py`, generic), `recipes/case/relations.yaml`, tests; pipeline wiring of the case step.

## Out of scope
New extraction fields, UI changes, `eval/`, `odw2json/model.py`.
