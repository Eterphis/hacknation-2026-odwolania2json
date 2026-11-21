---
id: T016
title: Local small LLM as a grounded reader for weak fields (profile `llm`, CPU, 16 GB)
status: merged
owner: coder
branch: task/T016-local-llm-reader
depends_on: [T012, T014]
capabilities: [python, ml]
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 900
  - id: AC-2
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.bench --profiles ocr,llm --sets heldout,skany,negatywne --workers 2 --out .acc/bench-llm"
    expect: "bench: 2 profiles x 3 sets ok"
    timeout: 5400
  - id: AC-3
    run: "! grep -rniE 'odwolanie|odwołanie|pelnomocnictw|pełnomocnictw|przelew|mocodawca|OdwolanieKIO|Zamawiajacy|Odwolujacy' odw2json/engine odw2json/llm"
    timeout: 60
  - id: AC-4
    manual: "Judge reads reports/T016.md and the bench table: profile `llm` does not lose to `ocr` on skany, heldout or negatives (exact F1 / reject rate) and stays opt-in (default profile `ocr`), peak RAM < 10 GB at 2 workers, model <= 4B parameters with an Apache-2.0/MIT licence, runs offline after the one-time model download, and every LLM value in the output has evidence with a quote found in the page text."
protected: []
---
## Objective
D-015: a model running locally on the grader's laptop scores the maximum; smaller is better. Add an optional reader
that fills only what the recipes could not read with confidence, following the owner's spec-extraction pattern
(github.com/yano358/qa-system-akygabattery, `.claude/rules/spec-extraction.md`):
- **Transcribe, then compute in code**: the model returns strings as printed (JSON with every field nullable, schema-
  constrained output / grammar), our normalisers turn them into dates, NIPs, amounts, ids.
- **Grounding**: every value comes with a quote; the quote must be found in the page text (OCR text for scans, on a
  folded letters+digits skeleton); a value without a found quote is dropped (or kept as a flagged low-confidence
  proposal, never as a silent answer). Evidence rule = `llm:<model>`.
- **Never overrides** a recipe value with full confidence; it fills nulls and low-confidence values, and decides
  choices the recipes found ambiguous (party roles: who is Odwołujący / Zamawiający / pełnomocnik / mocodawca;
  `czynnosc_powod_id` 1-12 from the first charge).
- **Configuration, not code**: a recipe field opts in with `llm: {question: "...", hint: "..."}` (or a class-level
  `llm:` block); the generic reader builds the prompt from the recipe and the output schema's `//` comments; a new
  class gets LLM help with no code. No class names in `odw2json/llm/` or the engine (AC-3).
- Context budget: send only the relevant page(s)/sections (first page header, party block, first charge), not 60 pages.

## Spike first (time box ~45 min, report the numbers before building)
Measure on this machine (i7-class CPU, 16 GB, no GPU), 3-5 scans: candidates Qwen3 (0.6B/1.7B/4B, Apache-2.0),
Bielik v2/v3 small (Apache-2.0, check the exact licence of the chosen checkpoint), Basal (Apache-2.0, D-009) as GGUF Q4
on **llama.cpp** (MIT) via `llama-cpp-python` (check a CPU wheel for Python 3.13 on Windows; fallback: the llama.cpp
server binary as a subprocess, or onnxruntime-genai MIT). For each: tokens/s, seconds per document, peak RAM, field
accuracy on the weak fields. Pick the smallest model that helps. No Llama/Gemma-licence weights, no AGPL/GPL.

## Context
- HOUSE_DIR = C:/Users/jasiu/workspace/.house. Read D-005, D-009, D-015, D-017, reports/model-basal.md, licences.md,
  T012.md (profiles + bench), T014.md (which fields are still weak on scans).
- You own `odw2json/llm/` (reader, prompt builder, grounding, runtime adapter), `profiles/llm.yaml`, the recipe
  `llm:` schema extension (+ docs in `docs/ADDING_A_DOCUMENT_CLASS.md`), `docs/LLM.md` (model, licence, size, how it is
  used, what it never does: required by the README "opis wykorzystanego LLM"), model download script
  (`python -m odw2json.llm.fetch`, sha256-checked; weights stay out of git), Docker build arg to bake the model in.
- Default profile stays `ocr` until the bench shows `llm` is better and fits the time budget (Q-004 q5).

## Out of scope
Any API/cloud model, fine-tuning, GPU.
