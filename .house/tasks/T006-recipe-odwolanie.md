---
id: T006
title: Complete the odwolanie recipe to the held-out F1 target
status: done
owner: teammate-session
branch: task/T006-recipe-odwolanie
depends_on: [T002, T004]
capabilities: [python]
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 900
  - id: AC-2
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe C:/Users/jasiu/workspace/.house/accept/prep_input.py .acc/input 41-60 && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/input --output .acc/output && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred .acc/output --gold C:/Users/jasiu/workspace/uzp-data/dane --cases 41-60 --types odwolanie"
    expect: "score >= 0.85"
    timeout: 1800
  - id: AC-3
    run: "! grep -rniE 'odwolanie|odwołanie|OdwolanieKIO|Zamawiajacy|Odwolujacy' odw2json/engine"
    timeout: 60
protected: []
---
## Objective
`recipes/odwolanie.yaml` (+ `dictionaries/czynnosc_powod.yaml`) extracts every field of the UZP odwolanie schema with exact-mode F1 >= 0.85 on the HELD-OUT cases 41-60, tuning only on 01-40. The `//` comments in uzp-data/oczekiwane-json/odwolanie.json are the field spec: `data`/`miejscowosc` only from the first-page header line ("X, dnia ..." / "X DD.MM.RRRR", else null); `czynnosc_dzien`, `czynnosc_powod_id` and `czynnosc_opis` decided ONLY from the first zarzut, `czynnosc_opis` 1:1 with the id (code list 1-11 in reports/rules-check.md; id 12 unknown); KRS/NIP/REGON of the Odwołujący or the consortium leader; `przez-pelnomocnika` 1/0 and the pełnomocnik block; Zamawiający list with `prowadzacy_postepowanie` (null unless several zamawiający); `numer_bzp` without spaces, `numer_ted` as NNNNNN-YYYY, `numer_postepowania`, `tytul`.

## Context
- HOUSE_DIR = C:/Users/jasiu/workspace/.house. Read spec.yaml `task`, D-005, D-007, reports/rules-check.md (code list), reports/ideation-1.md findings 5-6 (section order swaps, consortia "1) Lider Konsorcjum:", distractor party "Wykonawca wybrany ... po stronie Zamawiającego", TED/BZP variants, act date in a sentence or a numbered list), the engine docs from T004.
- Scorer: `python -m eval.score --pred <out> --gold C:/Users/jasiu/workspace/uzp-data/dane --cases 01-40 --types odwolanie --report <file>`; never edit `eval/`.
- Generalise for REAL appeals (20-60 pages of prose, parties introduced as "X sp. z o.o. z siedzibą w Y (dalej: Odwołujący)", partly scanned): label/phrase lists with variants, trigger phrases per czynnosc_powod id that a lawyer would recognise, no case-specific hacks, no copying of gold values. If T003's report confirms that the oczekiwane-json/odwolanie.json example is the gold of the scanned template appeal, also report our F1 on it (informational).
- You own `recipes/odwolanie.yaml`, `dictionaries/czynnosc_powod.yaml`, generic engine additions + tests. T005 works on the przelew/pelnomocnictwo recipes in parallel: do not edit them; keep shared engine additions generic and small.
- Report the per-field held-out table in HOUSE_DIR/reports/T006.md.

## Out of scope
przelew/pelnomocnictwo recipes (T005), cross-document checks (T009), `eval/`, `odw2json/model.py`.
