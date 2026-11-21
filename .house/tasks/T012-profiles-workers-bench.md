---
id: T012
title: Processing profiles, parallel workers and an F1-vs-cost bench on all evaluation sets
status: todo
owner: null
branch: null
depends_on: [T013]
capabilities: [python, devops]
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 900
  - id: AC-2
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.prep_skany .acc/pw && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/pw/input --output .acc/pw/out1 --workers 1 && C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m odw2json --input .acc/pw/input --output .acc/pw/out4 --workers 4 && git diff --no-index --quiet .acc/pw/out1 .acc/pw/out4 && echo same-output"
    expect: "same-output"
    timeout: 2400
  - id: AC-3
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.bench --profiles text,ocr --sets heldout,skany,negatywne --workers 1,4 --out .acc/bench"
    expect: "bench: 2 profiles x 3 sets ok"
    timeout: 3600
protected: []
---
## Objective
Adapted from the teammate proposal (HOUSE_DIR/handoff/proposal-T012-tiers.md) to D-015 (local model only, no API).
UZP grades by swapping `./input` and running the CLI on an office laptop (i7, 16 GB, no GPU), and the final scores
the balance of quality and cost. Ship:
1. **Profiles** = config files `profiles/<name>.yaml` selected by `--profile` / env `ODW2JSON_PROFILE` / Docker env,
   default `ocr`: `text` (text layer + recipes only; scans give `{}`), `ocr` (+ RapidOCR on pages without text: the
   current default behaviour). Leave a documented slot for `llm` (T016 adds it: same file format, no code change).
   A profile only switches components/options the factory already knows (ingestor, OCR on/off, later the LLM reader);
   output of the default profile must equal today's output.
2. **`--workers N`** (default `min(4, cpu_count // 2)`, env `ODW2JSON_WORKERS`): a process pool over documents,
   components built once per worker, output identical to `--workers 1` (AC-2), deterministic file writing, a failed
   document becomes `{}` + a logged error, never a crashed run. Keep peak RAM under ~8 GB at 4 workers (measure).
3. **`python -m eval.bench`**: for each profile x set (`dev` 01-40, `heldout` 41-60, `skany` 30 scans, `noisy` T010 if
   present, `negatywne` 12) and each worker count: exact + normalized F1 (via `eval.score` as a library or CLI, never
   edit `eval/score.py`), reject accuracy on negatives, wall time per document p50/p95, docs/min, peak RSS of all
   workers (psutil, BSD), model size on disk. Writes `<out>/bench-<date>-<commit>.json` + a markdown table, appends
   `bench/history.csv`, prints `bench: <P> profiles x <S> sets ok` at the end. A `--gate` flag fails when F1 on
   heldout/skany drops > 0.005 vs the last accepted row or p95 time / peak RAM grow > 20%.
4. Docs: `docs/PROFILES.md` (profiles, workers, bench, how to read the table) and README/CLI help updated.

## Context
- HOUSE_DIR = C:/Users/jasiu/workspace/.house. Read D-015..D-018, reports/T003.md (OCR, cache), T008.md (Docker,
  start.bat), T013.md (rejected JSON modes, prep_skany), handoff/proposal-T012-tiers.md.
- You own `odw2json/pipeline.py`, `odw2json/cli.py`, `odw2json/factory.py` (profile wiring), `profiles/`, `eval/bench.py`
  (+ tests), `docs/PROFILES.md`, Docker/start.bat env pass-through. T014 edits recipes and T015 edits `web/` in
  parallel: do not touch those. The web app must keep working (it calls `process_case`).
- Windows: use `multiprocessing` spawn-safe code (`if __name__ == "__main__"` guards, picklable work items).

## Out of scope
The LLM reader itself (T016), recipe changes, UI.
