---
id: T018
title: Fix the rule-fixable misses - PESEL per attorney, Odwolujacy section end, duplicate and glued person names
status: review
owner: coder
branch: task/T018-recipe-misses
depends_on: []
capabilities: [python]
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 900
  - id: AC-2
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.prep_skany .acc/sk && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/sk/input --output .acc/sk/output && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred .acc/sk/output --gold .acc/sk/gold"
    expect: "score >= 0.970"
    timeout: 2400
  - id: AC-3
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe C:/Users/jasiu/workspace/.house/accept/prep_input.py .acc/input 41-60 && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/input --output .acc/output && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred .acc/output --gold C:/Users/jasiu/workspace/uzp-data/dane --cases 41-60"
    expect: "score >= 0.9986"
    timeout: 1800
  - id: AC-4
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe C:/Users/jasiu/workspace/.house/accept/prep_input.py .acc/dev 01-40 && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/dev --output .acc/devout && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred .acc/devout --gold C:/Users/jasiu/workspace/uzp-data/dane --cases 01-40"
    expect: "score >= 0.999"
    timeout: 1800
  - id: AC-5
    run: "! grep -rniE 'odwolanie|odwołanie|pelnomocnictw|pełnomocnictw|przelew|mocodawca|OdwolanieKIO|Zamawiajacy|Odwolujacy' odw2json/engine"
    timeout: 60
protected: [eval/score.py]
---
## Objective
Fix, with generic recipe rules and small engine features, the misses that HOUSE_DIR/reports/misses-1.md found to be
fixable without a model: scan F1 from 0.9639 to >= 0.970 (about what the `llm` profile reaches today), held-out 41-60
not below 0.9986 (target 1.0), dev 01-40 not below 0.999, negatives stay `{}`.

## The four fixes (misses-1.md, table rows in brackets)
1. **PESEL per attorney** (rows 7, 9, 11-12, 19) in `recipes/pelnomocnictwo.yaml`: read `PESEL:? <11 digits>`
   printed in or right after each pełnomocnik's entry (inside parentheses, after `nr wpisu …,`, without a colon,
   after titles like `r. pr.`), validated with the PESEL checksum (a validator exists for the LLM path, see
   `odw2json/llm/` and the recipe `validate:` reference). Attach it to the right person when there are several.
2. **End of the Odwołujący section** (row 20) in `recipes/odwolanie.yaml`: the section must stop at headings of
   other parties such as `Wykonawca wybrany`, `uczestnik (postępowania odwoławczego)`, `Przystępujący`, so identifiers
   of the next company (KRS of Cervin Konstrukcje in przyklad_52) are not taken.
3. **Duplicate people** (rows 5, 10): in lists of persons (pelnomocnicy, mocodawca podpisujacy) merge items whose
   names are the same after folding (casefold, no diacritics) or differ by at most one character (OCR `Zawadżki` vs
   `Zawadzki`). Keep the mixed-case form; on a tie, keep the form read at the signature / later in the document. Make
   it a generic, opt-in list option in the engine (e.g. `dedupe: {key: imie_nazwisko, fuzzy: 1}`), documented.
4. **Glued names** (row 6, `HalinaBaran - Prezes Zarządu`): in person-name values only (the `person` normalizer or a
   new one used by person fields), split a token at a lower→Upper boundary when both parts look like name words
   (each part starts upper-case and has >= 2 letters), e.g. `HalinaBaran` → `Halina Baran`. Do NOT apply it to company
   names, identifiers, e-mails or URLs (`BudMax`, `ePUAP`, `eKRS` must stay). Owner's hint: Polish documents rarely
   write `CosTakiego` in running text, but company names do, hence the restriction to person fields. Also check that
   the signatory list then picks up Halina Baran (pel 0004).

## Context
- HOUSE_DIR = C:/Users/jasiu/workspace/.house. Read reports/misses-1.md first (links to every PDF, our JSON and gold),
  then reports/T014.md, `docs/ADDING_A_DOCUMENT_CLASS.md` (recipe reference: keep it in sync,
  `tests/test_docs_recipe_reference.py` checks it), D-014 (do not tune on 41-60 layouts beyond these named misses),
  D-021 (missing field = null; never copy values from other documents).
- Eval: `python -m eval.prep_skany <dir>` then CLI + `python -m eval.score --pred <dir>/output --gold <dir>/gold --report <file>`;
  `.acc/misses/list_misses.py` in the main checkout lists every wrong leaf (copy it, it takes set/pred/gold/cases).
  OCR words are cached, scans run fast.
- You own `recipes/*.yaml`, `dictionaries/`, generic additions in `odw2json/engine/` + unit tests, and the recipe
  docs. Another coder works on OCR image preprocessing in `odw2json/ingest/` (T019): do not edit `odw2json/ingest/`,
  `odw2json/pipeline.py`, `web/`, `eval/`.
- Out of scope: `PL` account prefix (gold sets disagree, row 16-17), OCR-garbled lines (rows 1-4, 18: T019),
  the sole-trader principal (rows 13-15), the LLM reader.
- Report HOUSE_DIR/reports/T018.md: scan / 41-60 / 01-40 F1 before and after, which misses are fixed, any new ones.
