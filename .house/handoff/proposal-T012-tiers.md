---
id: T012
title: Processing tiers P0-P4 as config profiles, run in parallel, with a bench of F1 vs cost (demo + regression gate)
status: todo
owner: null
branch: null
depends_on: [T013]
capabilities: [python, ml, devops]
increment: P5
acceptance:
  - id: AC-1
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m unittest discover -s tests -t ."
    timeout: 900
  - id: AC-2
    run: "C:/Users/jasiu/workspace/.venv/Scripts/python.exe -m eval.bench --tiers P0,P1,P2 --sets heldout,skany,negatywne --workers 4 --out .acc/bench"
    expect: "tiers: 3 .* ok"
    timeout: 3600
  - id: AC-3
    manual: "Web UI 'Porównaj poziomy': one upload is processed by every enabled tier at the same time; per tier: JSON, F1-like agreement with the best tier, time per document, peak RAM, LLM calls/tokens; the bench table (F1 vs time vs RAM vs model size) is shown and exported."
protected: []
---
## Objective
UZP wants the balance point between extraction quality and cost on an office laptop (i7, 16 GB RAM, no GPU; LLM only
via an EU API, smaller models score more: README stage 2, 1-20 pts). Ship the pipeline as **tiers that differ only by a
profile file** (no code change = also proves "configuration, not code"), run them **in parallel** on the same input, and
measure each tier on the same sets, so the demo shows the curve and CI catches regressions.

## Tiers (each one = previous + one component; profile `profiles/P*.yaml`)
| Tier | Components | What it adds | Expected cost on i7/16 GB |
|---|---|---|---|
| **P0 tekst** | text layer + recipes (regex/layout strategies) | floor: deterministic, offline, ms per page; scans -> empty JSON | <0.2 s/doc, <300 MB |
| **P1 + OCR** | P0 + RapidOCR (ONNX, CPU) on pages without text | scans | ~10-12 s/scanned doc today, ~1.5 GB peak |
| **P2 + klasyfikator** | P1 + typed classifier: TF-IDF+LR baseline (P2a) and Basal-pico 0.75B / basal-2.0-mini 1.5B GGUF on CPU (P2b, D-009) | class/reject from content (negatives), `czynnosc_powod_id` as a 12-way choice from the first charge, yes/no decisions (`przez-pelnomocnika`, `prowadzacy_postepowanie`); no spans | P2a ~ms; P2b ~0.5-2 s/decision, ~2-3 GB |
| **P3 + mały LLM (fallback)** | P2 + small instruct model via EU API (e.g. Bielik-1.5B/4.5B, PLLuM-12B as upper bound) **only for fields that are null or below a confidence threshold** | gap filling on prose/scans; value must be found verbatim in the text (else rejected) so evidence stays | 1 call per weak field, capped per document |
| **P4 referencja (nie do zgłoszenia)** | full-document extraction by a large LLM via API | upper bound for the curve | many tokens; shows what the small tiers lose |

Rules: a later tier never overwrites a high-confidence recipe value (only fills gaps/decides choices); every value keeps
an Evidence row with the tier that produced it; every tier is selectable in CLI (`--profile P2`), Docker env and UI.

## Parallelism
- Within a tier: `--workers N` process pool over documents (OCR and CPU models are process-bound; one model instance
  per worker, models loaded once per worker). Default N = min(4, cores/2) to stay under 16 GB.
- Across tiers (demo): one upload fans out to all enabled tiers concurrently (separate output dirs/columns); P3/P4 API
  calls are async with a concurrency limit and timeout; a slow tier never blocks the others (progress per tier).

## How to measure (eval/bench.py, one JSON + one markdown table per run, file name = date + commit)
Sets: `dev` 01-40, `heldout` 41-60, `skany` (30 scans with gold, T013), `noisy` (T010), `negatywne` (12, expect empty JSON).
Per tier and set:
- quality: F1 exact + normalized (eval/score.py), per type and per field; reject accuracy on negatives and false rejects
  on real documents;
- cost: wall time per document p50/p95, total throughput docs/min at N = 1, 2, 4, 8 workers, peak RSS (psutil, all
  workers), CPU %, model parameters (B) and size on disk, LLM calls/tokens/latency/estimated cost per case;
- value per cost: delta-F1 vs previous tier per extra second and per extra GB.
Regression gate (CI, no UZP data in CI -> runs on the owner machine / nightly): fail when a tier's F1 on heldout or
skany drops > 0.005 vs the last accepted run, when a tier is worse than the tier below on any set, or when p95 time /
peak RAM grows > 20%. Keep the history in `bench/history.csv` to plot F1 vs time vs RAM vs model size.

## Versions to build, in order
1. P0/P1 profiles + `--workers` + bench on dev/heldout/skany/negatywne (fast win: parallel OCR, empty JSON).
2. P2a TF-IDF+LR (classification/reject, czynnosc id) - cheapest learned component, decides if P2b is worth it.
3. P2b Basal-pico, then basal-2.0-mini (choice/yes-no only), compare with P2a on the same bench.
4. P3 with one small EU-API model and a confidence threshold sweep (0.5/0.7/0.9) - plot F1 vs number of LLM calls.
5. P4 once, as the reference point for the pitch; UI "Porównaj poziomy" + docs (`docs/TIERS.md`, LLM description
   required by the README).

## Out of scope
Changing recipes for F1 (T005/T006/T013), GPU, any non-EU LLM provider.
