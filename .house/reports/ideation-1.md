# Ideation 1: solution concepts for ODWOLANIA2JSON

- **Agent / model:** ideator (opus)
- **Branch / commits:** none (no commit, per brief)
- **Date:** 2026-11-21 ~12:40
- **Inputs read:** spec.yaml, DECISIONS.md (D-001..D-006), QUESTIONS.md (Q-001, Q-002), ideas.md (empty), playbooks/build.md, reports/source-full-brief.txt, reports/rules-check.md, uzp-data README, the 3 annotated schemas, gold + `pdftotext -enc UTF-8 -layout` of cases 01, 07, 23, 41, 44, 50, 58, and `szablon-aplikacja/`.

## Goal

The task is fixed, so these are five solution concepts (architecture + extraction approach + product angle), each
designed to (a) pass Stage 1 on >= 10 hidden REAL cases (100% F1), (b) win Stage 2 (50% F1, 30% flexibility via
config, 20% architecture/quality; regulamin says 50/50), (c) respect D-005 (no-LLM path gives full valid JSONs),
Python 3.13, open-source only, CPU only, `./input/<case>/*.pdf -> ./output/<case>/<basename>.json`, upload UI,
Docker Compose, docs.

## Findings from the data that every idea must use (new facts, not in spec.yaml yet)

1. **`szablon-aplikacja/input/case1/` holds a "negatywny przyklad.pdf" (a TED contract notice) and the expected
   `output/case1/` contains ONLY `przyklad odwolanie.json`.** So: a PDF that is none of the three classes must
   produce NO output file (or the grader may count it as a false positive). Classification needs an explicit
   "unknown / reject" outcome, not argmax over three classes. Worth adding to spec.task and to Q-002 (confirm).
2. **`przyklad odwolanie.pdf` there is a 7-page, 4 MB PDF with no text layer (pdftotext returns 7 bytes): a SCANNED
   real appeal.** This is the strongest hint of what the hidden real set looks like. OCR is not optional. The
   example values in `oczekiwane-json/*.json` (Filharmonia Pomorska, Pruszków, 2025-10-13, TED 641651-2025;
   ZSCKR/822/2025 Henryków in przelew; ZP.039.2025 in the TED negative) look like they come from real cases;
   hypothesis: the schema example for `odwolanie.json` is the gold of this scanned appeal. If OCR confirms it, we
   get one free real held-out case with gold. Cheap to check once OCR runs.
3. **Diacritics are fine** when pdftotext is told `-enc UTF-8` (Windows default codepage mangles them). Any
   extraction or eval code must force UTF-8 (PYTHONIOENCODING / explicit encoding) or F1 drops on names.
4. **Identifier checksums are only partly valid in the synthetic set** (NIP 75/123, REGON 85/123, IBAN 43/120
   valid). Checksums cannot be a hard filter on training data, but on real data they are valid by construction, so
   they are an excellent soft signal and an OCR-repair oracle (0/O, 1/l/I, 5/S, 8/B substitutions until the
   checksum passes).
5. Layout variation already in training: section order (Odwołujący/Zamawiający swapped), header date at top or
   mid-page, consortia ("1) Lider Konsorcjum:"), a distractor party ("Wykonawca wybrany ... po stronie
   Zamawiającego"), TED as `2026/S 142-999327` or `2026/S171-999656`, BZP as `2026/BZP 00999827`, the act date
   either in a narrative sentence ("Zamawiający w dniu 20 marca 2026 roku unieważnił") or in a numbered list
   ("1) odrzuceniu oferty ... pismem z dnia 4 sierpnia 2026 r."). Bank confirmations come in at least two layouts:
   label-left/value-right rows (case 44) and label-row/value-row two-column grids (case 01), which break naive
   linear "label: value" regexes.
6. `data`/`miejscowosc` are null exactly when the header has no "X, dnia ..." line (15/60): rule = header-only,
   never fall back to other dates. Pełnomocnicy names must be in the nominative ("w mianowniku"); real powers of
   attorney often use the dative/accusative ("udzielam pełnomocnictwa Panu Janowi Kowalskiemu"), so Polish
   morphology matters on real data even though synthetic data is mostly nominative.
7. Licence trap for IP transfer: PyMuPDF is AGPL-3.0, Ghostscript (used by ocrmypdf) is AGPL, spaCy Polish models
   (`pl_core_news_*`) are GPL-3.0, Llama/Gemma/Llama-based PLLuM weights are not OSI open source, Qwen2.5-3B is
   under the Qwen Research licence. Prefer pdfplumber/pdfminer.six (MIT), pypdfium2 (Apache-2.0/BSD-3),
   Tesseract (Apache-2.0), RapidOCR (Apache-2.0), Morfeusz2 (BSD-2) / simplemma (MIT), and Apache-2.0 model
   weights (Bielik, Qwen2.5-1.5B/7B, Mistral-NeMo-based PLLuM-12B). Verify each licence on its model card before
   it goes in the pitch list.

Common skeleton all five share (so the judge can compare the *differentiating* part): `ingest` (text layer via
pdfplumber; OCR fallback per page when the text layer is empty or garbage) -> `classify` (3 classes + reject) ->
`extract` (class-specific, config-driven) -> `normalise/validate` (dates ISO, amounts float, ids digits-only, TED
`NNNNNN-YYYY`, BZP no spaces, dictionary for `czynnosc_powod_id`) -> `write` (schema-shaped JSON, all keys present,
nulls where unknown). Plus `eval/score.py` (field-level micro F1) and a web UI.

---

## I-001 Recepty: declarative YAML extraction recipes per document class

**Pitch (PL):** Każda klasa dokumentu to jeden plik YAML („recepta”): sygnały klasyfikacji, sekcje, pola z
kotwicami, wzorcami i normalizatorami; silnik w Pythonie jest jeden i nie zna żadnego typu dokumentu.

**Golden-path demo.** A UZP analyst uploads a case folder (3-4 PDFs, one scanned) in the web UI. She sees each file
classified with a score, the JSON per file, and for every field the recipe rule that fired plus the source snippet.
Then, live, she copies `recipes/przelew.yaml` to `recipes/zawiadomienie_kio.yaml`, edits six lines in the built-in
editor, re-runs, and a new document class appears with its own JSON, without a restart or a code change.

**Architecture.**
- `engine/` (generic): `TextSource` (page texts + line offsets), `Segmenter` (cuts the text into named sections by
  heading/label patterns from the recipe), `FieldExtractor` (strategies: `after_label`, `regex`, `between`,
  `first_match_in_section`, `list_of_blocks`, `lookup` in a dictionary), `Normaliser` registry (date_pl, amount_pl,
  digits, iban, ted, bzp, person_name_nominative), `Validator` registry (nip, regon, pesel, iban checksum: soft).
- `recipes/<class>.yaml`: the only place where document knowledge lives. `output_schema` points at the target JSON
  skeleton, so the writer always emits every key.
- `dictionaries/czynnosc_powod.yaml` (id -> canonical label + trigger phrases).
- `cli.py`, `start.bat`, `web/` (FastAPI + one HTML page, or Streamlit), `eval/`.

Recipe sketch:

```yaml
class: przelew
output: { file: schemas/przelew.json, root: przelew_bankowy }
classify:
  any: ["potwierdzenie (realizacji|wykonania) (polecenia )?przelewu", "rachunek (odbiorcy|obciążany)"]
  reject_if: ["ogłoszenie o zamówieniu", "TED website"]
  min_score: 2
fields:
  kwota:          { find: after_label, labels: ["Kwota( operacji)?"], type: amount_pl }
  data_operacji:  { find: after_label, labels: ["Data (operacji|transakcji|realizacji)"], type: date_pl }
  z_rachunku:     { find: after_label, labels: ["Rachunek (zleceniodawcy|obciążany|nadawcy)"], type: iban, validate: iban }
  numer_transakcji: { find: after_label, labels: ["Nr ref\\.", "Numer referencyjny"], optional: true }
```

**F1 on real noisy cases.** Labels are lists of regex alternatives (several banks, several law firms' habits),
matched on a normalised text (unicode NFC, hyphenation joined, whitespace collapsed, OCR-confusable map for
labels). `after_label` looks right on the same line, then on the next line in the same column (handles the
two-row grid layout). Each field may declare several strategies tried in order. OCR via Tesseract `pol`
(Docker/apt) with RapidOCR (pip, no system binary) as the Windows fallback. A held-out split (train on 40 cases,
test on 20) plus 5-10 hand-degraded copies (rendered, noised, re-OCRed) guard against overfitting the synthetic
templates.

**Flexibility and architecture score.** The cleanest possible story for the 30%: "new class = new YAML, zero
code"; the engine is a deep module behind `extract(text, recipe) -> (json, evidence)`. Recipe JSON-Schema
validation gives clear errors in the editor. Docs write themselves: ADDING_A_DOCUMENT_CLASS.md is a recipe tutorial.

**Jury wow.** Live: the jury names a document type (e.g. "zawiadomienie o wyborze oferty", or a KRS extract), we
write its recipe on stage in 90 seconds and the UI extracts it.

**Main risks.** Hand-written rules plateau on real documents the team has never seen (real appeals are 20-60 pages
of free prose; the parties may be introduced only as "X sp. z o.o. z siedzibą w Y (dalej: Odwołujący)"). YAML DSLs
grow into a bad programming language if every edge case becomes a new keyword. Rules tuned to 60 synthetic cases
can reach ~0.95 locally and ~0.6 on real scans.

**Effort.** Engine + 3 recipes + CLI: ~8-10 agent-hours; UI with editor: ~3 h; OCR fallback: ~2 h. Fits easily;
the safest baseline. Libraries: pdfplumber/pdfminer.six (MIT), PyYAML (MIT), jsonschema (MIT), pydantic (MIT),
rapidfuzz (MIT), dateparser (BSD-3) or own Polish month table, pytesseract (Apache-2.0) + Tesseract (Apache-2.0),
rapidocr-onnxruntime (Apache-2.0) + onnxruntime (MIT), pypdfium2 (Apache-2.0/BSD-3), FastAPI (MIT) + uvicorn
(BSD-3) or Streamlit (Apache-2.0).

---

## I-002 Sprawa jako graf: cross-document entity resolution with a formal-check report

**Pitch (PL):** Nie czytamy trzech PDF-ów osobno — budujemy jeden graf sprawy (podmioty, numery, kwoty, daty),
głosujemy między dokumentami i sumami kontrolnymi, a jako produkt dajemy referentowi KIO automatyczną kontrolę
formalną odwołania.

**Golden-path demo.** A KIO registry clerk drops a whole case into the UI. She sees the three JSONs and, above them,
a "case card": Odwołujący, Zamawiający, proceedings number, linked across documents with green ticks where the
appeal, the power of attorney and the transfer agree, and red flags where they do not (wpis 7 500 zł paid but the
appeal says EU thresholds -> 15 000/20 000 zł required; the power of attorney signed by a person not on the appeal;
appeal filed 12 days after `czynnosc_dzien` while the deadline is 10). One click shows which document each value
came from.

**Architecture.**
- `mentions/`: a typed-mention extractor over every page of every document: ORG names (legal-form suffix
  grammar: "sp. z o.o.", "S.A.", "sp.k.", "Gmina", "Szpital", ...), PERSON, NIP, REGON, KRS, PESEL, IBAN, money,
  dates, TED, BZP, proceedings ref. Each mention carries document, page, char span, confidence, checksum status.
- `graph/`: entity resolution (same NIP -> same entity; fuzzy name + address clustering with rapidfuzz), role
  assignment (Odwołujący / Zamawiający / wybrany wykonawca / pełnomocnik) as a small scoring problem: proximity to
  role labels, "(dalej: Odwołujący)" coreference, cross-document constraints (mocodawca of the power of attorney ==
  Odwołujący; payer of the transfer == Odwołujący or its law firm; the transfer title mentions the proceedings ref).
- `projectors/<class>.yaml`: maps the resolved graph onto each target JSON (which roles and attributes go where),
  plus `checks/*.yaml`: declarative formal-check rules (amount table for wpis, deadline arithmetic, signatory
  coverage). New document class = a mention-type list + a projector; new business rule = a check file.

**F1 on real noisy cases.** Redundancy is the weapon: the Odwołujący's NIP appears in the appeal and the power of
attorney, the proceedings number in the appeal, the power of attorney and the transfer title. A value misread by
OCR in one document is outvoted by the others; checksums (valid on real data) pick between OCR variants. Role
assignment by constraints is robust to section order and to distractor parties (case 58), which is where label
regexes fail. Output stays per document (the grader compares each file to its own gold), so the graph is only used
to choose among candidates that actually occur in that document, never to copy a value into a document that does
not contain it.

**Flexibility and architecture score.** Strong architecture story (mentions -> graph -> projections is a classic,
explainable pipeline; each layer is a deep module). Flexibility: new classes plug into the same graph, and the
graph is the "canonical data model" the brief literally asks for ("spójny, ustrukturyzowany model danych"). The
formal-check layer is the deployment story for s.9 of the brief (pilot in UZP/KIO).

**Jury wow.** The red flag "wpis za niski" or "odwołanie po terminie" on a real-looking case: it shows we
understand the KIO workflow, not just PDF parsing. UZP jurors know these checks are done by hand today.

**Main risks.** More moving parts than I-001; entity resolution bugs can hurt F1 across all three files at once.
The formal-check rules need domain facts (wpis amounts per value threshold and contract type, deadline 5/10 days,
holidays) that must be right or the wow becomes an embarrassment: verify with the UZP mentors on site. The per-file
gold may reward copying the text as written even when another document has a "better" spelling; never override a
value present in the document itself.

**Effort.** Mentions + roles + projectors: ~12-14 agent-hours; checks + case card UI: ~4 h. Tight but feasible with
3 coders if the mention extractor (shared) lands first. Libraries: pdfplumber (MIT), rapidfuzz (MIT), networkx
(BSD-3, optional), pydantic (MIT), PyYAML (MIT), Tesseract/RapidOCR (Apache-2.0), holidays (MIT) for deadline
arithmetic, FastAPI (MIT).

---

## I-003 Naucz na przykładach: rule induction from (PDF, JSON) pairs

**Pitch (PL):** Nowej klasy dokumentu nie konfigurujemy ręcznie — wrzucamy 5-10 par PDF + oczekiwany JSON, a system
sam wyprowadza czytelną, edytowalną konfigurację ekstrakcji i pokazuje jej trafność na odłożonych przykładach.

**Golden-path demo.** A UZP data officer opens "Nowa klasa", drags in 8 bank confirmations and their 8 JSONs. In 20
seconds she sees the induced config (for each field: learned labels such as "Rachunek odbiorcy", context window,
value pattern, normaliser), its cross-validated F1 per field, and the two fields it could not learn. She accepts,
uploads a ninth confirmation from a bank never seen before and gets its JSON.

**Architecture.**
- `align/`: for each training pair, find every gold leaf value in the document text (exact, then normalised:
  dates in Polish words, amounts with spaces/commas, IBAN with spaces, names inflected via lemma match, fuzzy
  rapidfuzz for long titles). Output: (field, page, span, left context, right context, line geometry).
- `induce/`: per field, generalise the contexts into a small set of anchor rules (the most frequent left-context
  label n-grams, accent- and case-folded; value shape as a regex learned from character classes; section
  constraint from the nearest preceding heading). Rank rules by precision on the training pairs. Optional second
  learner: a CRF token tagger (python-crfsuite) on the same alignments, used when anchor rules have low recall.
- `configs/<class>.induced.yaml`: human-readable, same format a person could write by hand (so I-001's engine can
  execute it). A person may edit it; edits are kept on re-induction.
- `classify/`: class centroids from TF-IDF of the training documents of each class + a reject threshold
  (handles the "negatywny przyklad").
- `eval/`: k-fold CV report per field is produced at induction time and shown in the UI.

**F1 on real noisy cases.** Induction runs on all 60 cases but is evaluated with held-out folds, so we see
generalisation, not memorisation. Labels are learned as sets of variants, and accent/case/OCR folding is applied
both at induction and at runtime. Because the learned rules are anchored on labels rather than template positions,
they transfer to unseen layouts that use the same vocabulary (which legal and banking documents do). Weak spots
(free-prose fields like `czynnosc_powod_id`, `tytul`) get hand-written rule overrides in the same YAML.

**Flexibility and architecture score.** The strongest possible answer to "nowe klasy bez modyfikacji kodu": not
even rules, only examples, and the output is still an auditable config (no black box). Clean ML-lite architecture
(align -> induce -> execute), measurable with built-in CV. It also matches s.9 of the brief: a universal PDF ->
data tool that UZP staff can extend themselves.

**Jury wow.** Live induction of a new class on stage from examples the team prepared (e.g. KRS extracts or KIO
decisions), with its F1 printed right there.

**Main risks.** The synthetic training set is template-generated, so induced labels may be exactly the synthetic
generator's labels; real documents may use others. Alignment of inflected names and of paraphrased titles is
fiddly (gold `tytul` in case 01 matches the PDF only after normalising quotes). The research flavour can eat hours
without a working baseline: must run behind a hand-written baseline (I-001-style) that already passes the golden
path. Live induction demo needs a prepared second class with ~8 examples we label ourselves.

**Effort.** Alignment ~4 h, induction ~5 h, CRF fallback ~3 h (optional), UI ~3 h, on top of a minimal baseline
engine (~6 h). Feasible only as a layer on I-001's engine, not as a standalone first build. Libraries: pdfplumber
(MIT), rapidfuzz (MIT), scikit-learn (BSD-3), python-crfsuite (MIT) / sklearn-crfsuite (MIT), simplemma (MIT) or
Morfeusz2 (BSD-2) for name lemmas, PyYAML (MIT).

---

## I-004 Schemat UZP jako prompt: Polish open LLM with grounding verifier, rules as floor

**Pitch (PL):** Plik `oczekiwane-json/*.json` z komentarzami UZP jest jednocześnie konfiguracją klasy: reguły dają
pełny JSON zawsze, a otwarty polski model (Bielik / PLLuM) przez API poprawia tylko pola o niskiej pewności, i to
wyłącznie wartościami, które da się wskazać w tekście dokumentu.

**Golden-path demo.** An analyst uploads a real, messy appeal (long prose, parties introduced inline). The UI shows
the JSON with each field coloured: green = rule, blue = LLM proposal accepted because the verifier found it in the
text (snippet shown), grey = LLM proposal rejected (not grounded). She switches the LLM off in settings, re-runs,
and still gets a complete, valid JSON (just fewer blue fields).

**Architecture.**
- `schema_loader/`: parses UZP's commented JSON (comments -> field instructions, example values -> types and
  formats). A new class = drop a commented JSON file in `classes/<name>/schema.jsonc` + a few classification
  keywords; optional `rules.yaml` for the deterministic floor.
- `baseline/`: deterministic rules (as in I-001) produce a full JSON with per-field confidence.
- `llm/`: OpenAI-compatible client to any open-weights server (Ollama, llama.cpp server, vLLM, or a hosted open
  model if UZP allows), with JSON-schema-constrained decoding (llama.cpp GBNF / Ollama `format`), prompt built from
  the schema comments + the first ~3 pages (the brief says key data sits there). Called only for fields with
  confidence < threshold, or never when no endpoint is configured.
- `verifier/`: accepts an LLM value only if it is grounded (exact / normalised / fuzzy >= 90 match in the source
  text, checksum valid for ids, date present in the text in any Polish format) and well-formed; otherwise keeps the
  rule value. Logs every decision for transparency.
- `docker-compose.yml`: `app` + optional `llm` service (Ollama with a pinned Apache-2.0 GGUF model, CPU).

**F1 on real noisy cases.** Real appeals are where rules break (free prose, non-template wording, `czynnosc_powod_id`
from the first charge needs reading comprehension); a 7-11B Polish model reads those well. The verifier prevents
the classic LLM failure (hallucinated NIP or date) from costing precision. The rules floor guarantees the D-005
requirement. For speed on CPU, only low-confidence fields go to the model and the context is cut to the relevant
section.

**Flexibility and architecture score.** "Config = UZP's own annotated schema" is the most natural flexibility
story for this jury: UZP already wrote the config format. Clear adapter seam (LLM is one adapter behind an
interface, rules the other). Bielik (Polish community model) or PLLuM (the Polish government's LLM project, from
the ministry that co-organises this event) is a strong narrative, as long as the licence is Apache-2.0.

**Jury wow.** A real-world appeal (scanned) where rules give 6/16 fields and the grounded LLM lifts it to 14/16, each
added value with its source snippet; then "pull the network cable" and the app still delivers.

**Main risks.** Grader may have no network and no LLM (then Stage 1 F1 = the rules floor, so the LLM work buys
nothing for preselection). CPU inference of a 7-11B model: ~5-30 s per field-batch per document; a 1.5-4.5B model
is faster but weaker in Polish. Licence: verify that the chosen weights are Apache-2.0 (Bielik v2/v3, Qwen2.5-7B,
PLLuM-12B NeMo-based are; Llama-based PLLuM, Gemma, Qwen2.5-3B are not OSI). Hosting a model for the jury demo
costs setup time and possibly money.

**Effort.** Baseline rules ~8 h (shared with I-001), schema loader ~2 h, LLM adapter + verifier ~4 h, Docker with
Ollama ~2 h, UI colouring ~2 h. Feasible; the LLM part is cleanly parallel to the rules work. Libraries: pdfplumber
(MIT), httpx (BSD-3), pydantic (MIT), json5/commentjson-style parsing (own 30-line stripper, or json5 (Apache-2.0)),
rapidfuzz (MIT), Ollama (MIT) or llama.cpp / llama-cpp-python (MIT), model weights under Apache-2.0 (verify card),
Tesseract/RapidOCR (Apache-2.0).

---

## I-005 Dowód na stronie: geometry-first token-box pipeline with a visual evidence viewer

**Pitch (PL):** Każdy PDF — cyfrowy czy skan — zamieniamy na te same „słowa z ramkami” na stronie, wyciągamy
wartości po geometrii (etykieta po lewej / nad wartością, kolumny, bloki) i w UI podświetlamy na obrazie strony
dokładnie to miejsce, z którego pochodzi każde pole; poprawka klikiem uczy konfigurację.

**Golden-path demo.** A KIO clerk uploads a scanned power of attorney and a digital bank confirmation. She sees the
page images side by side with the JSON; hovering a field draws its bounding box on the page (and the label box that
anchored it). One field is wrong: she clicks the right word on the page, the field updates, and the UI offers "save
this anchor to the class config", which adds the label to the YAML.

**Architecture.**
- `layout/`: one `Page` model = list of words with bbox + reading order + lines + blocks, built from the PDF text
  layer (pdfplumber `extract_words`) or from OCR (Tesseract TSV / RapidOCR boxes) when the layer is missing.
  Everything downstream is source-agnostic, so scans and digital PDFs take the same code path.
- `kv/`: generic key-value detection: label lexicon match (fuzzy, accent-folded), then value search in spatial
  directions declared per field (`right`, `below`, `right_or_below`, `block_after`), column alignment, stop at the
  next label. Free-prose fields fall back to text regexes over the reading-order text.
- `classes/<class>.yaml`: labels, directions, value types, normalisers, page range ("first 3 pages"), classifier
  keywords and a reject rule.
- `viewer/`: page PNGs (pypdfium2 render) + SVG overlay of evidence boxes in a small web app; the JSON written to
  `./output` is unchanged, evidence goes to a sidecar `./output/<case>/.evidence/<name>.json` (keep it outside the
  graded files, or in a separate folder, to avoid confusing the grader).

**F1 on real noisy cases.** Bank confirmations and forms are tables; geometry handles label-above-value grids
(case 01) and label-left rows (case 44) with one rule, and survives OCR line-merging that destroys linear regexes.
Scans get deskew/binarisation before OCR (Pillow/OpenCV-headless). The evidence viewer makes debugging real
failures fast for the team during the night (look at the page, see why the anchor missed). Morphology
(Morfeusz2/simplemma) converts pełnomocnik names to the nominative.

**Flexibility and architecture score.** Config-driven like I-001, but the transparency criterion ("wspierające
transparentność procesu ekstrakcji danych", explicitly premiowane) is scored visibly: every value has a box on the
page. The click-to-teach loop shows a path to a human-in-the-loop pilot. Source-agnostic layout model is a clean
deep module.

**Jury wow.** Hover over `kwota` and a box lights up on a crooked scan; click a wrong value, fix it on the page,
and the config file diff appears.

**Main risks.** Geometry from OCR on poor scans is noisy (merged columns, skew); two code paths (geometry + prose)
to maintain. Appeals are mostly prose, so geometry helps przelew/pełnomocnictwo more than odwolanie (the highest
field count). The viewer is front-end work that does not raise Stage 1 F1, which gates everything. Tesseract
is a system binary (fine in Docker, needs an installer on Windows); RapidOCR's Polish diacritics quality must be
checked early.

**Effort.** Layout model + KV engine ~8 h, OCR path with boxes ~3 h, viewer ~4 h, click-to-teach ~2 h. Feasible
with three coders; viewer and engine are parallel. Libraries: pdfplumber/pdfminer.six (MIT), pypdfium2
(Apache-2.0/BSD-3), pytesseract (Apache-2.0) + Tesseract (Apache-2.0), rapidocr-onnxruntime (Apache-2.0),
opencv-python-headless (Apache-2.0), Pillow (MIT-CMU/HPND), simplemma (MIT) or Morfeusz2 (BSD-2), PDF.js
(Apache-2.0) if rendering in the browser, FastAPI (MIT).

---

## Comparison

| Idea | Stage 1 F1 on real cases | Flexibility (30%) | Architecture (20%) | Demo wow | Risk | Effort vs 23 h |
|---|---|---|---|---|---|---|
| I-001 Recepty YAML | medium (rules plateau) | high | medium-high | live new class | low | low |
| I-002 Case graph + formal check | high (cross-doc voting, checksum OCR repair) | medium-high | high | domain red flags | medium | medium-high |
| I-003 Induction from examples | medium (synthetic labels) | very high | high | live learning | high | high (needs I-001 under it) |
| I-004 Schema-as-prompt + grounded LLM | high only if the grader runs an LLM; rules floor otherwise | very high (UZP schema = config) | high | rules vs LLM vs offline | medium (infra, licence) | medium |
| I-005 Geometry + evidence viewer | medium-high (tables, scans) | high | high | boxes on the page | medium | medium |

They compose: I-001's recipe engine is the floor that I-003 (induces recipes), I-004 (LLM escalation) and I-005
(geometric strategies) all need, and I-002's cross-document voting can sit on any of them.

## Ideator's favourite

**I-002 on top of a lean I-001 engine.** Stage 1 is 100% F1 on real, partly scanned cases, and the only signal
that is guaranteed to survive OCR noise and unseen layouts is redundancy: the same NIP/KRS/proceedings number
appears in two or three documents of the case and real identifiers carry checksums. No other idea attacks the
real-data gap that directly, and the formal-check card gives the most UZP-specific wow for Stage 2. Pick the
evidence-box viewer from I-005 as the transparency feature if time allows.

## Evidence that would settle the choice within one iteration

- Run OCR (Tesseract pol and RapidOCR) on `szablon-aplikacja/input/case1/przyklad odwolanie.pdf`: if the text
  matches the `oczekiwane-json/odwolanie.json` example values, we have a real held-out case; score every approach
  on it.
- Hold out cases 41-60 (the more realistic template family) while building on 01-40: the gap between in-sample and
  held-out F1 measures how much each approach overfits.
- Count, over the 60 cases, how often each `Odwolujacy` NIP / proceedings ref appears in >= 2 documents of the
  case: that number bounds what I-002's voting can buy.

## Next

- Add finding 1 (negative example -> no output) and finding 2 (real scanned appeal in the template) to spec.task,
  and append to Q-002: "Does a non-appeal PDF in input/ require no output file?".
- Judge scores the five ideas on the rubric; coordinator picks the floor engine first regardless of the choice.
