# Ideation 1: judge scoring of I-001..I-005

- **Agent / model:** judge (opus)
- **Date:** 2026-11-21 ~13:30 (time left to freeze 2026-11-22 09:30: ~20 h; max 3 parallel sonnet coders)
- **Inputs read:** spec.yaml (scoring, task, rules, deliverables, timeline), DECISIONS.md D-001..D-006, QUESTIONS.md
  Q-001/Q-002, playbooks/lifecycle.md §2, playbooks/build.md, reports/ideation-1.md, prior-art-I-001..005.md,
  reports/licences.md. No `reports/review-*.md` exists yet (nothing to weigh).
- **Scale:** rubric criteria 1-5 per the spec's level mapping (F1: 1 = <0.5, 3 = ~0.75, 5 = >=0.9 on held-out incl.
  noisy cases; Flexibility: 1 = hardcoded, 3 = new field via config, 5 = new type via config only, live, with
  per-field evidence in the UI; Architecture: 1 = one script, 3 = modules + README + tests, 5 = deep modules,
  ARCHITECTURE + ADDING_A_DOCUMENT_CLASS docs, `docker compose up`, CI green). Scores are the expected outcome if the
  idea is built in the time left, not the best case. Weighted total uses the PDF weights 0.5/0.3/0.2; the
  regulamin variant (0.5 F1 / 0.5 flexibility) is given in brackets.

## Evidence I gathered (spot checks on the training data, read-only)

All commands run against `C:/Users/jasiu/workspace/uzp-data`, text via `pdftotext -enc UTF-8 -layout` into the
judge scratchpad, stats with a 90-line Python script (scratchpad `spot.py`).

| # | Check | Result | Consequence |
|---|---|---|---|
| E1 | Leaf count per gold file over 60 cases | odwolanie 1335, pelnomocnictwo 621, przelew 360 (58% / 27% / 15%) | The appeal carries most of the F1 mass, and it is the prose document. Geometry (I-005) helps the 42% that are form-like; prose handling decides the rest. |
| E2 | Non-date string leaves found verbatim (whitespace/case folded) in their own PDF text | odwolanie 894/983 (91%), pelnomocnictwo 392/458 (86%), przelew 237/240 (99%) | On synthetic data, anchor rules can reach ~0.9. The 14% gap in pelnomocnictwo is normalisation (nominative names, typ, nulls), not missing text. |
| E3 | Cross-document redundancy | Odwołujący NIP appears in the PoA text 60/60, in the transfer 0/60; numer_postepowania in the PoA 60/60 and in the transfer 60/60. Gold: mocodawca nazwa == Odwołujący nazwa 60/60, mocodawca NIP == Odwołujący NIP 60/60, appeal's pełnomocnik in the PoA list 60/60, proceedings ref in transfer title 60/60 | I-002 voting can touch about 5-8 leaves per case (mocodawca nazwa/nip/krs, Odwołujący nazwa/nip/krs, numer_postepowania, pełnomocnik name), roughly 15-20% of leaves. Real but bounded; worth a small module, not an architecture. |
| E4 | Transfer purpose and amount | 60/60 transfer titles are "opłata skarbowa od pełnomocnictwa ...", none is a wpis; amounts 17/34/50/100/200 do not track the number of attorneys (e.g. 100 zł with 1 or 2 attorneys, 34 zł with 1) | **I-002's flagship wow ("wpis 7 500 zł paid but EU threshold needs 15 000") is built on a false premise for this data**: the transfer is stamp duty for the PoA, not the appeal fee. A fee-amount check would flag most synthetic cases as wrong. Only data-consistency checks (E3) are safe without UZP confirming the law. |
| E5 | `szablon-aplikacja/input/case1/negatywny przyklad.pdf` (TED notice) | Contains "Krajowa Izba Odwoławcza", "odwołania", "Organ odwoławczy" | A keyword classifier for `odwolanie` fires on the negative example. The reject class needs positive structure cues (Odwołujący/Zamawiający sections, "zarzucam", "wnoszę o") plus reject cues (TED notice headings). Must be a test from day one. |
| E6 | OCR tooling on this machine | `which tesseract` -> not found; no rapidocr/pytesseract/pdfplumber in the Python 3.13 site; Docker 29.4 present; Ollama not installed (tools.json) | OCR is unbuilt and unverified everywhere. If the grader runs `start.bat` on Windows without a Tesseract binary, every scan scores 0. A pip-only OCR (RapidOCR + onnxruntime, Apache-2.0) must be the default on Windows, Tesseract in Docker. I-004's local LLM has no runtime here yet. |
| E7 | `czynnosc_powod_id` distribution | ids 1-11, 4-9 examples each (no 12) | Classifying the first charge from ~5 synthetic examples per class is weak on real prose; 2 leaves per case (id + opis) ride on it. This is where an LLM (I-004) would earn most, if it is allowed to run. |

Not verified (could not, no OCR available): whether `oczekiwane-json/odwolanie.json` example values are the gold of
the scanned template appeal. This stays the first check once OCR runs.

## Scores per idea

### I-001 Recepty (YAML recipes, one generic engine)

| Criterion | Score | Justification (evidence) |
|---|---|---|
| F1 (0.5) | 3 | Anchor rules reach ~0.9 on synthetic data (E2) but plateau on real prose and unseen layouts; expect ~0.7-0.75 on real cases with OCR (E1, ideation risk section). |
| Flexibility (0.3) | 5 | The plan is exactly level 5: new class = one YAML, live demo, rule + snippet per field (card I-001 "new class = a file, shown live"). |
| Architecture (0.2) | 4 | One deep engine behind `extract(doc, recipe) -> (json, evidence)`; risk that the YAML DSL bloats into a bad language keeps it from 5 until docs + CI exist. |
| **Weighted** | **3.80** [4.00] | |
| Feasibility | 5 | ~10-13 agent-hours for engine + 3 recipes + CLI + OCR; fits with room. |
| Q-002 risk | 2 | No network needed; exposed only to the F1 definition (normaliser output must match gold formats exactly). |
| Novelty risk (card) | 4 | Medium-high: invoice2data (MIT) is the same mechanism; Azure/Google template models. Defence = Polish legal normalisers, evidence, live new class. |

### I-002 Sprawa jako graf (cross-document resolution + formal checks)

| Criterion | Score | Justification (evidence) |
|---|---|---|
| F1 (0.5) | 3 | Voting covers only ~15-20% of leaves (E3) and NIP never appears in the transfer; ER bugs can hit three files at once. Upside on OCR'd identifiers via checksums. |
| Flexibility (0.3) | 3 | New class needs mention types + a projector over roles; role logic is code, not config, so "new class via config only" is only partly true. |
| Architecture (0.2) | 4 | mentions -> graph -> projections is a clean, explainable pipeline, but more moving parts to document and test. |
| **Weighted** | **3.20** [3.00] | |
| Feasibility | 3 | ~16-18 agent-hours on top of a floor engine it still needs; tight. |
| Q-002 risk | 2 | No network; if UZP's F1 rewards text as written, cross-doc overrides must never copy values (ideator already notes it). |
| Novelty risk (card) | 2 | Linking is established (Splink), formal checks are the least-covered part (card I-002) **but** the fee check is wrong on this data (E4). |

### I-003 Naucz na przykładach (rule induction from PDF + JSON pairs)

| Criterion | Score | Justification (evidence) |
|---|---|---|
| F1 (0.5) | 2 | Induced labels are the synthetic generator's labels; transfer to real documents is the open question it cannot answer in time (card I-003 practical risk). Inherits the I-001 floor at best. |
| Flexibility (0.3) | 4 | Strongest story on paper (examples only), but the live induction of a second class needs ~8 labelled examples we do not have; delivered level likely 4. |
| Architecture (0.2) | 3 | align -> induce -> execute is clean, but a research layer half-finished at 09:30 hurts the quality score. |
| **Weighted** | **2.80** [3.00] | |
| Feasibility | 2 | ~12 h on top of a ~6 h baseline; alignment of inflected names is fiddly (E2 gap). |
| Q-002 risk | 2 | No network; same F1-definition exposure. |
| Novelty risk (card) | 4 | High for the concept (WIEN 1997, Azure custom models); medium for the readable-config variant. |

### I-004 Schemat UZP jako prompt (rules floor + grounded open LLM)

| Criterion | Score | Justification (evidence) |
|---|---|---|
| F1 (0.5) | 3 | The floor is I-001 (3). The LLM lifts prose fields (E7, parties introduced inline) only if the grader runs it; on CPU with a licence-clean 1.5-4.5B Polish model (licences.md) quality on legal text is unbenchmarked. Expected 3, upside 4. |
| Flexibility (0.3) | 4 | "UZP's own annotated schema is the config" is a strong story, but offline a new class from a schema alone yields nulls; the rules file is still needed for D-005. |
| Architecture (0.2) | 4 | Clear adapter seam (rules vs LLM behind one interface), compose with an optional `llm` service; extra infra to keep working. |
| **Weighted** | **3.50** [3.50] | |
| Feasibility | 3 | Ollama absent (E6), model download + CPU latency + verifier ~8 h beyond the floor. |
| Q-002 risk | 4 | If the grader has no network/LLM (Q-002 q1), all LLM work buys 0 in Stage 1 (100% F1). |
| Novelty risk (card) | 5 | HIGH: LangExtract and ContextGem (Apache-2.0) do LLM extraction with source tracing. |

### I-005 Dowód na stronie (word-box page model, geometry, evidence viewer)

| Criterion | Score | Justification (evidence) |
|---|---|---|
| F1 (0.5) | 3 | Geometry handles both transfer layouts and OCR line merging (ideation finding 5) but 58% of leaves sit in prose (E1); expected 3, upside on scanned forms. |
| Flexibility (0.3) | 5 | Config-driven like I-001 plus visible per-field evidence (premiowana transparentność); click-to-teach writes back to YAML. |
| Architecture (0.2) | 4 | One source-agnostic `Page` model for scans and digital PDFs is the deepest module of the five; two extraction paths (geometry + prose) to maintain. |
| **Weighted** | **3.80** [4.00] | |
| Feasibility | 3 | Full idea (viewer + click-to-teach) ~17 h; the page model alone is ~4-5 h and fits. |
| Q-002 risk | 2 | No network; the evidence sidecar must stay out of the graded `./output/<case>/` files. |
| Novelty risk (card) | 4 | Medium-high on the viewer (Docling, Azure DI, Rossum); defensible part = write-back of the anchor into open YAML. |

## Ranking

| Rank | Idea | Weighted (0.5/0.3/0.2) | [0.5/0.5] | Feasibility | Q-002 risk | Novelty risk |
|---|---|---|---|---|---|---|
| 1= | I-001 Recepty | 3.80 | 4.00 | 5 | 2 | 4 |
| 1= | I-005 Dowód na stronie | 3.80 | 4.00 | 3 | 2 | 4 |
| 3 | I-004 Schema as prompt + grounded LLM | 3.50 | 3.50 | 3 | 4 | 5 |
| 4 | I-002 Case graph + formal check | 3.20 | 3.00 | 3 | 2 | 2 |
| 5 | I-003 Induction from examples | 2.80 | 3.00 | 2 | 2 | 4 |

The tie between I-001 and I-005 breaks on feasibility: I-001 first, I-005's page model folded into it. No idea is
rejected outright; I-003 should be parked (no Stage 1 gain, highest delivery risk). The rubric has no novelty
criterion, so novelty risk matters only for the Q&A; regulamin §4.1 makes us name external solutions anyway, so name
invoice2data, Docling and LangExtract before the jury does.

## Recommended plan: a combination

**"Recepty na stronie":** a lean I-001 recipe engine running on I-005's source-agnostic word-box page model, with
I-002 reduced to a cross-document consistency/voting module, and I-004's grounded LLM as an optional last-stage
adapter, off by default. Expected score if built: F1 4 (target >= 0.82 on held-out + noisy copies; OCR and the
reject class are what protect it on real cases), Flexibility 5, Architecture 4-5 -> **~4.3** [4.5].

Parts, in build order:

1. **Contract + eval (wave 1, parallel).** Interfaces `ingest(pdf) -> Document(pages of words with bbox)`,
   `classify(Document, recipes) -> class | None`, `extract(Document, recipe) -> (json, evidence)`; recipe YAML
   JSON-Schema; output skeletons from `oczekiwane-json` (all keys, nulls); `eval/score.py` with a 01-40 dev /
   41-60 held-out split.
2. **Ingest with OCR fallback (wave 1, parallel).** I-005's `Page` model: pdfplumber words for text-layer pages,
   OCR words (RapidOCR pip default on Windows, Tesseract `pol` in Docker) for empty/garbage pages; UTF-8 forced.
3. **Engine + classifier with reject + przelew recipe (wave 2).** I-001 strategies (`after_label` right-or-below,
   `regex`, `between`, `list_of_blocks`, `lookup`), normaliser/validator registries, checksum as soft signal.
4. **odwolanie and pelnomocnictwo recipes (wave 2-3, parallel).** Including `czynnosc_powod` dictionary with trigger
   phrases (first charge only), header-only date/place rule, nominative names (simplemma MIT / Morfeusz2 BSD-2).
5. **Upload UI + evidence (wave 3, parallel).** FastAPI + one page: upload a case, see class + score, JSON, and per
   field page + snippet + rule; built-in recipe editor or "copy recipe, re-run" flow for the live new class.
6. **Packaging (wave 3, parallel).** `start.bat`, `requirements.txt`, `docker compose up`, ARCHITECTURE.md,
   ADDING_A_DOCUMENT_CLASS.md, external-components list, CI running unittest + eval on a sample.
7. **Case consistency (I-002-lite, wave 4).** Voting among candidates present in the same document using E3
   relations (PoA principal = Odwołujący, proceedings ref in transfer title, pełnomocnik in PoA list) + checksum OCR
   repair; a green/red consistency strip in the UI. No fee or deadline law checks unless UZP mentors confirm the rules
   (E4).
8. **Noisy held-out set (wave 4).** Render 10 training PDFs to images, degrade, re-OCR; plus the template scan if
   its gold is confirmed. This is our only proxy for "real, partly scanned".
9. **Stretch, after the 00:00 judge round:** a second shipped class as YAML only (e.g. TED notice or KRS extract),
   then evidence boxes on the page image (pypdfium2 render + SVG), then I-004's grounded LLM adapter for prose
   fields (Bielik-1.5B/4.5B Apache-2.0 via Ollama, compose profile, verifier accepts only values found in the text),
   then click-to-teach.

**Cut first under time pressure (in this order):** click-to-teach -> LLM adapter -> box overlay on page images (keep
text snippet evidence) -> in-browser recipe editor (keep the "copy YAML, re-run" demo) -> consistency strip in the UI
(keep voting in the engine). **Never cut:** eval, OCR fallback, reject class, output skeleton completeness,
`docker compose`, the two docs (prize handover §3.5).

## Golden-path demo (3 sentences)

A UZP clerk drops a real-looking case folder (a scanned appeal, a power of attorney, a bank confirmation and a stray
TED notice) into the web UI (or `./input` + `start.bat`) and gets one JSON per recognised document in `./output`,
with the TED notice skipped and, for every field, the page, source snippet and recipe rule that produced it plus a
consistency strip (PoA principal = appellant, proceedings number in the transfer title). Live on stage we copy a
recipe to `recipes/<new class>.yaml`, edit a few labels, re-run, and the new document type is classified and
extracted without a code change. The eval page closes it: F1 on held-out training cases and on noisy re-OCR'd copies,
per document type and per field.

## Cheapest way to gain a point, per criterion

- **F1:** OCR fallback + reject class verified on the template case in wave 1 (a scanned appeal with no text layer
  is 58% of a case's leaves at 0 without OCR; a wrongly emitted TED JSON is a false positive). Then fix the top-3
  field errors that the held-out eval shows.
- **Flexibility:** ship a second extra class as YAML only, with a test that loads it and a grep-style test that no
  class name appears in `engine/` (proves "zero class-specific code").
- **Architecture:** `docker compose up` + GitHub Actions running the unit tests and eval on 5 cases + ARCHITECTURE.md
  with the 4-module diagram (ingest / classify / extract / write).

## First 3 tasks (wave 1, independent, 3 coders)

1. **T001 Contract and skeleton:** package layout, the three interfaces above, `Document`/`Page`/`Word` dataclasses,
   recipe YAML JSON-Schema, output skeletons generated from `oczekiwane-json`, CLI `./input/<case>/*.pdf ->
   ./output/<case>/<basename>.json` writing schema-complete null JSONs, `start.bat`, `requirements.txt`. Acceptance:
   CLI on the 60 cases writes 180 valid files with every key present; non-matching PDFs write nothing.
2. **T002 Local scorer:** `eval/score.py --pred --gold` printing `score: <F1>`; field-level micro F1 over leaves,
   exact mode and light-normalised mode reported side by side, list items aligned by best match, missing/extra file
   = all its leaves FN/FP; dev/held-out split; per-field table. Protected file. Acceptance: gold vs gold = 1.0, null
   skeletons give the baseline number, a perturbed copy gives the hand-computed value.
3. **T003 Ingest with OCR fallback:** pdfplumber words with bbox; per-page OCR when the text layer is empty or
   garbage (RapidOCR default, Tesseract optional), UTF-8 safe; returns the same `Page` model. Acceptance: all 180
   training PDFs ingest with diacritics intact; the 7-page template scan yields readable Polish text; report states
   whether its text matches the `oczekiwane-json/odwolanie.json` example values (free real held-out case if yes).

## Risks if Q-002 answers go against us

- **No network / no LLM at the grader (q1):** plan unaffected (LLM is stretch, off by default, D-005). I-004 as the
  main idea would lose its whole F1 upside.
- **F1 = exact match without normalisation (q2):** normalisers must emit gold formats exactly (ISO dates, float kwota,
  digits-only IBAN, `2026/BZP00999778` without spaces, `NNNNNN-YYYY` TED). T002 reports both modes so we see the gap.
- **File naming (q3):** classify by content only, always write `<input basename>.json`; low risk.
- **Grader environment (q4), not in Q-002 wording but implied:** Windows without a Tesseract binary -> pip-only OCR
  default (E6). Highest technical risk of the plan.
- **Non-case documents in test folders (q8/q9):** reject class covers it; a false accept costs a whole file of FPs.

## Top 2 risks

1. **Real scanned cases vs synthetic training:** rules tuned on 60 synthetic cases (91% verbatim, E2) may fall to
   ~0.6 on real scans, and OCR is unbuilt and has no runtime on this machine (E6). Mitigation: OCR + noisy held-out
   set in waves 1 and 4, held-out split from the first eval.
2. **Domain wow built on a wrong premise:** I-002's fee check contradicts the data (E4: transfers are PoA stamp duty,
   amounts inconsistent); showing it to UZP jurors would cost credibility. Keep only data-consistency checks unless
   UZP mentors confirm a legal rule.

## Single cheapest change that gains the most score

Put the OCR fallback (RapidOCR pip default, Tesseract in Docker) and the reject class into wave 1 and test both on
`szablon-aplikacja/input/case1` before 18:00: every scanned test document otherwise scores 0, and the template is
UZP's own hint that real test cases are scans.
