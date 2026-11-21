---
id: T013
title: Adapt to the updated UZP data (45 upstream commits) - empty JSON for rejects, scans, renamed files, code 12
status: todo
owner: null
branch: null
depends_on: [T005, T006]
capabilities: [python]
increment: P2
priority: urgent (before T012)
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 900
  - id: AC-2
    manual: "Every PDF in input gets an output JSON with the same name; a rejected document (dane/negatywne, negatives inside przyklad_NN) gets an EMPTY .json file (0 bytes or {} - check what UZP means and say which)."
  - id: AC-3
    manual: "eval on dane/skany (30 scans with gold, 10 per type) is reported per type and per field; target set by the coordinator after the first run (baseline below)."
protected: []
---
## Why (found 2026-11-21 ~15:30 by the teammate session)
The local `uzp-data` clone was 45 commits behind upstream `Urzad-Zamowien-Publicznych/hacknation-2026` (now pulled on
the teammate machine; the owner's machine must `git -C <uzp-data> pull` too). Changes that hit us:
1. **Rejected documents must produce an empty `.json`** ("Zbiór danych zawiera też kategorie dokumentów, które NIE
   powinny być zidentyfikowane (zwrócić pusty plik .json)"). Our pipeline writes NO file for a rejected document.
2. **Negatives**: `dane/negatywne/` (12 PDFs: TED/BZP notices, KIO judgment, ministry decisions, a JPK brochure, a
   procedure guide) and negatives inside some `przyklad_NN` folders (e.g. `2025_S 112-383751.pdf`,
   `2025_BZP 00143067_01.pdf`). README: classify by content, "nazwa pliku może być różna".
3. **Scans with gold**: `dane/skany/{odwolania,pelnomocnictwa,potwierdzenia}/000N/000N.{pdf,json}` (30 docs).
4. `potwierdzenie_przelewu.pdf` renamed to `przelew.pdf` in 2 cases (more may follow): check `.house/accept/prep_input.py`,
   tests and docs that hard-code the old name.
5. `czynnosc_powod_id` code **12 = "Projektowane postanowienia umowy"** (dictionary has 1-11), official list in
   `oczekiwane-json/czynnosc_powod_id_dict.md`; names (pełnomocnik, mocodawca osoba fizyczna) **in the nominative**.
6. README scoring changed (stage 2): 1-20 pts for LLM size (smaller = more points), 1-20 flexibility, 1-10 extras (GUI);
   test machine: office laptop i7, 16 GB RAM, no GPU; an LLM, if used, only via an API with a key, provider with EU/EEA
   servers and a stated processing scope; "dokumentacja techniczna w tym opis wykorzystanego LLM". -> T012.

## Baseline measured on the new data (branch task/T005 = best extraction, 2026-11-21)
- `dane/skany` (30 scans, gold present): **score 0.5633** (odwolanie 0.5878, pelnomocnictwo 0.4340, przelew 0.6364).
  Worst: pelnomocnicy/podpisujacy 0/31, odwolanie czynnosc_* and tytul 0/10, pelnomocnik block 0/9.
- `dane/negatywne` (12): 11 rejected, **1 accepted wrongly** (`KIO_KIO 2617-21.pdf`, a KIO judgment).
- Speed: 42 PDFs (30 scans) in **8 min 27 s**, sequential (~12 s per scanned document). See T012 for parallelism.

## Scope
Pipeline/writer (empty JSON for rejects), recipes (negatives forbidden signals: judgment "wyrok"/"sygn. akt KIO"
headers; code 12 triggers), OCR-robust labels for the scan layouts, acceptance helper for the new file names (ask the
coordinator: `.house/accept/` is read-only for workers), eval runner for `dane/skany` (gold lives next to the PDF).
