---
id: T021
title: Real appeal layout - two-column party header (label beside a wrapped value) and the "pn.: <title>" wording
status: done
owner: coder
branch: task/T021-two-column-header
depends_on: []
capabilities: [python]
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 900
  - id: AC-2
    run: "rm -rf .acc/tpl && mkdir -p .acc/tpl/in/case1 && cp 'C:/Users/jasiu/workspace/uzp-data/szablon-aplikacja/input/case1/przyklad odwolanie.pdf' .acc/tpl/in/case1/ && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/tpl/in --output .acc/tpl/out --workers 1 && C:/Users/jasiu/workspace/.venv/Scripts/python.exe C:/Users/jasiu/workspace/.house/accept/template_case1.py .acc/tpl/out"
    timeout: 1200
  - id: AC-3
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.prep_skany .acc/sk && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/sk/input --output .acc/sk/output && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred .acc/sk/output --gold .acc/sk/gold"
    expect: "score >= 0.9789"
    timeout: 2400
  - id: AC-4
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe C:/Users/jasiu/workspace/.house/accept/prep_input.py .acc/input 01-60 && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/input --output .acc/output && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred .acc/output --gold C:/Users/jasiu/workspace/uzp-data/dane --cases 01-60"
    expect: "score >= 0.9999"
    timeout: 1800
  - id: AC-5
    run: "! grep -rniE 'odwolanie|odwołanie|pelnomocnictw|pełnomocnictw|przelew|mocodawca|OdwolanieKIO|Zamawiajacy|Odwolujacy|zamawiaj|odwoluj' odw2json/engine odw2json/ingest"
    timeout: 60
protected: [eval/score.py, .house/accept/template_case1.py]
---
## Objective
Read real KIO appeals whose party header is laid out in two columns: the label (`Odwołujący:`, `Zamawiający:`) sits in
a left column, vertically centred against a multi-line value in the right column. OCR reading order then puts the
label on the SECOND line of the wrapped name, so today the section starts mid-name. Also read the title written as
`pn.:\n<title>" (postępowanie nr …)`. HARD TIME BOX: feature freeze is 09:30; the coordinator merges only if every AC
is green by 09:00. If you see it will not make it, stop, report what works and what does not, and leave the branch.

## The evidence (HOUSE_DIR/reports/judge-1.md sections 1.2 and 4; the only real-layout appeal we have)
`uzp-data/szablon-aplikacja/input/case1/przyklad odwolanie.pdf`, page 1 OCR text today:
```
Spółka z ograniczona odpowiedzialnością
Warszawa
Odwołujący: KRS:
tel. fax. e-mail:
reprezentowany przez radcę prawnego
Kancelaria Prawna - Radca Prawny
...
Miejskie Przedsiębiorstwo Oczyszczania w m. st. Warszawie Spółka z ograniczoną
Zamawiający: odpowiedzialnością
Warszawa
...
podstawie art. 275 pkt 1 ustawy ... pn.:
Dostawa preparatów do instalacji przetwarzania odpadów zlokalizowanej przy ul. Kampinoskiej
1 w Warszawie" (postępowanie nr RZP.27.29.2025.KD)
```
Today: `Odwolujacy.nazwa = "KRS"`, `pelnomocnik.imie_nazwisko = "Kancelaria Prawna"`,
`Zamawiajacy.nazwa = "odpowiedzialnością Warszawa"`, `tytul = null`. (The appellant's name is redacted in this sample:
the line `Spółka z ograniczona odpowiedzialnością` above the label; null or that line are both acceptable, a label like
`KRS` is not.) AC-2 checks: Zamawiający name = the full two-line name, Odwołujący not a label, title read, pełnomocnik
person not the firm.

## Approach (pick the smallest generic one)
- Preferred: in the layout/ingest step (`odw2json/ingest/layout.py`, word boxes are available) detect a short label
  line whose label word sits left of a right-column block, and re-order so the label comes BEFORE the whole block
  (the block = consecutive lines whose left x matches the value column and whose vertical span contains the label).
  Generic, no class or field names (AC-5). It must not change text-layer synthetic PDFs (AC-4 = 1.000) nor the scans
  (AC-3 no regression).
- Or: a generic engine strategy option (e.g. `section ... include_lines_above: <n>` when the label line's remainder
  continues a wrapped value), documented in docs/ADDING_A_DOCUMENT_CLASS.md.
- Title: a YAML-only change in `recipes/odwolanie.yaml` letting the title end at `"?\s*\(\s*(postępowanie\s+)?(nr|numer)`.
- Party values must not swallow contact lines (`tel. fax. e-mail:`, `KRS:` with no number) or the address city.

## Context
HOUSE_DIR = C:/Users/jasiu/workspace/.house. TDD for the code (synthetic word boxes in tests). Own: `odw2json/ingest/layout.py`
(+ tests), `recipes/odwolanie.yaml`, generic engine additions + docs. Do not touch `web/`, `eval/score.py`, the accept
script. Main moves while you work (T020 lands in engine/normalise + przelew recipe): merge main into your branch before
the final `house check` if it moved. Report HOUSE_DIR/reports/T021.md (before/after on the template fields, scans,
01-60, and what is still wrong).
