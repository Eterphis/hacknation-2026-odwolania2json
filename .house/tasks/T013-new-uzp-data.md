---
id: T013
title: Adapt to the updated UZP data - empty JSON for rejects, negatives, scans with gold, code 12
status: done
owner: teammate-session
branch: task/T013-new-uzp-data
depends_on: [T005, T006]
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
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.prep_skany .acc/sk && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/sk/input --output .acc/sk/output && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -c \"import glob,sys; fs=glob.glob('.acc/sk/input/negatywne/*.pdf'); bad=[f for f in fs if open(f.replace('input','output',1)[:-4]+'.json',encoding='utf-8').read().strip()!='{}']; print(len(fs),'negatives,',len(bad),'not rejected',bad); sys.exit(0 if len(fs)==12 and not bad else 1)\""
    timeout: 2400
  - id: AC-4
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.prep_skany .acc/sk2 && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/sk2/input --output .acc/sk2/output && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred .acc/sk2/output --gold .acc/sk2/gold"
    expect: "score >= 0.70"
    timeout: 2400
  - id: AC-5
    run: "! grep -rniE 'odwolanie|odwołanie|pelnomocnictw|pełnomocnictw|przelew|mocodawca|OdwolanieKIO|Zamawiajacy' odw2json/engine"
    timeout: 60
protected: []
---
## Objective
Bring the solution in line with the updated UZP repo (upstream 84cc976, D-016, D-017): every input PDF gets
`<name>.json`, a rejected or unreadable document gets `{}` (`--rejected-json {}|empty|none`, env
`ODW2JSON_REJECTED_JSON`, Q-004 q1 open); the 12 documents in `dane/negatywne` and the negatives inside some
`przyklad_NN` are rejected (KIO rulings included); `czynnosc_powod_id` 1-12 with the official labels; extraction works
on the 30 scans of `dane/skany` (gold next to each PDF), laid out for the scorer by `eval/prep_skany.py`.

## Context
- Built by the teammate session (report: HOUSE_DIR/reports/T013.md; task text: proposal branch
  `proposal/T012-T013-tiers-and-new-data`). The coordinator wrote these acceptance checks afterwards so they serve as
  the regression gate for later tasks: output shape, negatives, scan F1 floor (0.70; measured 0.7344, a dev number
  because the rules were written while reading the scans, D-017).
- Includes the T008 follow-up commit (docs rows for the new strategies/normalisers) and the coordinator's fix of the
  T001 stub test for the renamed `przelew.pdf`.

## Out of scope
Further scan F1 (T014), tiers/bench and the local LLM (T012), UI class editor (T015), case consistency (T009).
