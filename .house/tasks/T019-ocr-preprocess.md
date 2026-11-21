---
id: T019
title: Experiment - page image preprocessing before OCR against show-through and faint scans
status: doing
owner: coder
branch: task/T019-ocr-preprocess
depends_on: []
capabilities: [python]
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 900
  - id: AC-2
    run: "rm -rf .acc/coldcache .acc/skc && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.prep_skany .acc/skc && ODW2JSON_OCR_CACHE_DIR=.acc/coldcache C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/skc/input --output .acc/skc/output && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred .acc/skc/output --gold .acc/skc/gold"
    expect: "score >= 0.9639"
    timeout: 3600
  - id: AC-3
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe C:/Users/jasiu/workspace/.house/accept/prep_input.py .acc/input 41-60 && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/input --output .acc/output && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.score --pred .acc/output --gold C:/Users/jasiu/workspace/uzp-data/dane --cases 41-60"
    expect: "score >= 0.9986"
    timeout: 1800
  - id: AC-4
    manual: "Judge reads reports/T019.md: variants tried, measured on the 30 scans with a cold OCR cache (F1 per type, wrong leaves, median/p95 seconds per document, peak RAM), the chosen default and why; preprocessing is on by default only if it does not lower scan F1 and costs at most +40% OCR time; misses-1.md rows 1-4 and 18 say recovered or not, with the OCR line before/after."
protected: [eval/score.py]
---
## Objective
Find out whether cleaning the page image before RapidOCR recovers lines that OCR garbles today, and ship it as the
default if it helps. The trigger is HOUSE_DIR/reports/misses-1.md rows 1-4: on scan `skany/odwolania/0005` the
lines with `ZP/12/2026`, `2026/BZP 00879135/03` and `Opisu Przedmiotu Zamówienia (OPZ)` are printed clearly, but
text bleeding through from the back page makes OCR return `nr referencyjny: Z e ien` and `1a n z tf y:`
(page image: `.acc/misses/odw0005_p1.png` in the main checkout). Row 18 (`opiata … Maknowsiu` in a transfer title) is
a second, different case (low resolution / faint print).

## What to try (measure each, keep what wins)
- Grayscale + contrast stretch / gamma, so light show-through goes to white while dark print stays.
- Global (Otsu) and adaptive (Sauvola / mean) binarisation; light morphological open to remove speckle.
- Higher render scale (dpi) only for low-confidence lines, i.e. a second OCR pass on lines whose recognition score is
  below a threshold, keeping the better line.
- Licence-clean only (numpy, Pillow, opencv-python-headless are fine: Apache/MIT/BSD; check
  `docs/EXTERNAL_COMPONENTS.md` and add anything new there). CPU only, RAM within the T012 budget (4 workers < 8 GB).

## Constraints
- Configurable in the ingest config / profile (e.g. `ingest.preprocess: none | <name>`), default chosen by data.
- The OCR cache key must include the preprocessing settings, so cached results from another setting are never reused.
- Pages with a text layer are untouched (41-60 are mostly text PDFs: AC-3 guards that nothing changes there).
- Measure with a cold cache (`ODW2JSON_OCR_CACHE_DIR=<fresh dir>` or `python -m eval.bench --sets skany --cold`),
  1 and 4 workers, and keep negatives `{}` (`eval.bench --sets negatywne`).

## Context
- HOUSE_DIR = C:/Users/jasiu/workspace/.house. Read reports/misses-1.md, reports/T003.md (ingest/OCR), T012.md
  (profiles, workers, bench, cold-OCR numbers), `docs/PROFILES.md`.
- You own `odw2json/ingest/`, its tests, `profiles/*.yaml` ingest keys, `docs/PROFILES.md` and
  `docs/EXTERNAL_COMPONENTS.md` entries, `requirements.txt` (new deps only if they win). Another coder works on
  recipes and `odw2json/engine/` (T018) in parallel: do not edit `recipes/`, `dictionaries/`, `odw2json/engine/`,
  `web/`, `eval/score.py`.
- Report HOUSE_DIR/reports/T019.md (see AC-4).
