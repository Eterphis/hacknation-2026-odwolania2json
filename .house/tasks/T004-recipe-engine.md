---
id: T004
title: Generic recipe engine and classifier with reject (zero class-specific code)
status: done
owner: teammate-session
branch: task/T004-recipe-engine
depends_on: [T001, T003]
review: always
capabilities: [python]
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 900
  - id: AC-2
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe C:/Users/jasiu/workspace/.house/accept/prep_input.py .acc/input 01-60 --template && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/input --output .acc/output && C:/Users/jasiu/workspace/.venv/Scripts/python.exe C:/Users/jasiu/workspace/.house/accept/output_shape.py .acc/input .acc/output --expect-reject 'negatywny przyklad.pdf' --check-class"
    expect: "ok: 181 files"
    timeout: 1800
  - id: AC-3
    run: "! grep -rniE 'odwolanie|odwołanie|pelnomocnictw|pełnomocnictw|przelew|OdwolanieKIO|mocodawca|Zamawiajacy' odw2json/engine"
    timeout: 60
  - id: AC-4
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -c \"import sys,jsonschema,json,yaml,glob; s=json.load(open('recipes/recipe.schema.json',encoding='utf-8')); fs=glob.glob('recipes/*.yaml'); [jsonschema.validate(yaml.safe_load(open(f,encoding='utf-8')),s) for f in fs]; print(len(fs),'recipes valid'); sys.exit(0 if len(fs)>=3 else 1)\""
    timeout: 120
protected: []
---
## Objective
The heart of D-007: one generic engine in `odw2json/engine/` that knows NO document type. Everything about a class lives in `recipes/<class>.yaml`: classification signals (weighted regex/keyword signals, required/forbidden signals, minimum score), the output schema file, sections, and fields with ordered extraction strategies, normalisers and validators. The engine implements the `Classifier` and `Extractor` protocols from `odw2json/model.py`, returns an `Evidence` (path, value, page, snippet, rule, confidence, bbox when known) for every non-null field, and the pipeline default switches from T001's stubs to T003's ingestor + this engine. Recipes for the three UZP classes are shipped with classification complete and a first set of easy fields; T005/T006 complete the fields.

## Design (keep it a deep module behind a small interface)
- `load_recipes(dir) -> list[Recipe]` validated against `recipes/recipe.schema.json` (JSON-Schema; clear error messages: they will show in the UI). Recipes dir from config/`--recipes` CLI option/env `ODW2JSON_RECIPES`, default `./recipes`; adding a YAML file adds a class with no restart beyond re-running.
- Classification: score every recipe on the document text (normalised: NFC, casefold, diacritics-insensitive option, whitespace collapsed); best recipe above its `min_score` and with a margin over the runner-up wins; otherwise reject (`doc_class=None`, reason filled). The TED notice in the template case must be rejected; the scanned template appeal must be accepted as odwolanie (via OCR text).
- Strategies (registry, each a small function; recipes refer to them by name): `regex` (named group), `after_label` (value right of the label on the same line, else the line below in the same column using word boxes — handles the two-row bank grid), `between` (start/end patterns), `section` scoping (fields searched inside a named section cut by heading patterns), `list_of_blocks` (repeat a field group per block, e.g. several mocodawcy/pelnomocnicy/podpisujacy), `lookup` (map text to a dictionary id via trigger phrases from `dictionaries/<name>.yaml`), `const`/`derived` (e.g. a flag set when another field is non-null). Fields try strategies in order; first valid value wins.
- Normalisers (registry): `date_pl` (ISO from "15 lipca 2026", "15.07.2026", "07-07-2026"), `amount_pl` (float from "1 234,56 zł"), `digits`, `iban_pl` (digits only, no PL prefix, 26 digits), `ted` (NNNNNN-YYYY from "2026/S 142-999327"), `bzp` (no spaces), `strip`, `upper`/`title` where needed. Validators (soft, lower confidence, never drop values): `nip`, `regon`, `pesel`, `krs`, `iban` checksums.
- Writer fills the schema skeleton from `schemas/` (T001) so every key is present.
- Unit tests must include a fake class defined only by a YAML written to a temp dir (classified and extracted from a synthetic `Document`), proving a new class needs no code.

## Context
- HOUSE_DIR = C:/Users/jasiu/workspace/.house. Read spec.yaml `task` (schemas_are_annotated, dictionary, template_case, pitfalls), D-005, D-007, reports/ideation-1.md (I-001 recipe sketch, findings 5-6 on layout variation), reports/ideation-1-judge.md ("Recommended plan").
- Contract on main: `odw2json/model.py` (do not change). T001 pipeline/writer/schemas and T003 ingestor are merged before you start.
- You own `odw2json/engine/`, `recipes/` (schema + three class recipes with classification), `dictionaries/`, the pipeline default switch, and tests. PyYAML, jsonschema, rapidfuzz (MIT) are fine; no AGPL/GPL.
- Data: C:/Users/jasiu/workspace/uzp-data (gitignored, never copy into the repo; tests use small synthetic documents).

## Out of scope
Completing all fields for odwolanie/pelnomocnictwo/przelew (T005, T006), cross-document checks (T009), UI (T007). Do not edit `eval/` or `odw2json/model.py`.
