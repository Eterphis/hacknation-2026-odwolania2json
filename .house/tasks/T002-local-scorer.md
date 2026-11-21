---
id: T002
title: Local F1 scorer with dev/held-out split
status: review
owner: coder
branch: task/T002-local-scorer
depends_on: []
review: always
capabilities: [python]
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 600
  - id: AC-2
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred C:/Users/jasiu/workspace/uzp-data/dane --gold C:/Users/jasiu/workspace/uzp-data/dane"
    expect: "score >= 0.9999"
    timeout: 300
  - id: AC-3
    run: "mkdir -p .acc/empty && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred .acc/empty --gold C:/Users/jasiu/workspace/uzp-data/dane --cases 41-60"
    expect: "score: 0(\\.0+)?\\s*$"
    timeout: 300
  - id: AC-4
    run: "rm -rf .acc/p1 && mkdir -p .acc/p1/przyklad_01 && cp C:/Users/jasiu/workspace/uzp-data/dane/przyklad_01/odwolanie.json C:/Users/jasiu/workspace/uzp-data/dane/przyklad_01/pelnomocnictwo.json .acc/p1/przyklad_01/ && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred .acc/p1 --gold C:/Users/jasiu/workspace/uzp-data/dane --cases 01"
    expect: "score: 0\\.896[0-9]*\\s*$"
    timeout: 300
protected: []
---
## Objective
`python -m eval.score --pred <dir> --gold <dir> [--cases 41-60|01,07] [--types odwolanie,pelnomocnictwo,przelew] [--report <file.md>]` compares predicted JSONs with gold JSONs and prints, as its LAST line, `score: <F1>` (exact mode, the conservative number we optimise), preceded by `normalized: <F1>` and a short per-type table. With `--report` it writes a markdown report with per-type and per-field precision/recall/F1 and the worst fields. This is the house's local metric (spec `scoring.local_scorer`); every extraction task's acceptance uses it.

## Definition (document it at the top of eval/score.py and in eval/README.md)
- Layout: `<gold>/<case>/*.json`, `<pred>/<case>/*.json`, case folder names must match (`przyklad_NN`); `--cases` filters by the number at the end of the case name. A case missing in pred counts as all-FN.
- Document type of a JSON = from its top-level keys (`OdwolanieKIO` -> odwolanie, `mocodawca`/`pelnomocnicy` -> pelnomocnictwo, `przelew_bankowy` -> przelew), never from the file name (pred files are named after the input PDF, e.g. `potwierdzenie_przelewu.json`, gold is `przelew.json`). Several documents of one type in a case are paired by best agreement.
- Field-level micro F1 over non-null leaves: TP = pred leaf equals gold leaf; pred non-null and different or gold null = FP; gold non-null not matched = FN (a wrong value is one FP + one FN). Both null = ignored. Missing pred document = all its gold leaves FN; extra pred document (e.g. a document that should have been rejected) = all its non-null leaves FP.
- Lists of objects (Odwolujacy, Zamawiajacy, mocodawca, podpisujacy, pelnomocnicy) are aligned by maximum leaf agreement (Hungarian or greedy is fine); unmatched items count fully as FN/FP.
- Exact mode: equal after JSON type-aware comparison (numbers by value: 50 == 50.0; strings exactly). Normalized mode: additionally casefold, NFC, strip, collapse whitespace, drop surrounding quotes, and digit-only comparison when both sides are digit strings with separators.
- Gold JSONs are plain JSON (the commented schemas in oczekiwane-json are not gold).

## Context
- HOUSE_DIR = C:/Users/jasiu/workspace/.house. Gold: C:/Users/jasiu/workspace/uzp-data/dane (60 cases; never copy into the repo; unit tests use tiny hand-written fixtures under tests/fixtures/).
- You own `eval/` (`eval/__init__.py`, `eval/score.py`, `eval/README.md`) and `tests/test_score*.py`. Standard library only (no numpy needed). Force UTF-8.
- Expected numbers: gold vs gold = 1.0; empty pred = 0.0; case 01 without the przelew document = 0.8966 (26 matched leaves, 6 missed).

## Out of scope
Anything in `odw2json/`. Once merged, `eval/score.py` is the reference: later tasks must not change its definition (changes only via a new task with `review: always`).
