# Judge report 1: rubric round on the public repo (Ślad)

- **Agent / model:** judge (Claude Opus 5.5)
- **Date:** 2026-11-22, 06:30-07:30
- **Build under test:** public https://github.com/Eterphis/slad, commit `2fa4750` ("Ślad: odwołania KIO do JSON"),
  shallow-cloned into the judge scratchpad (`$S` = `C:/Users/jasiu/AppData/Local/Temp/claude/ab89df811496cc91/ecb978e1-2d2f-4bdf-92ae-67103c3a68f5/scratchpad`,
  clone at `$S/pub/slad`). Product code is identical to the private `main` except CRLF line endings (`diff -rq` on
  `odw2json recipes web eval docs tests profiles dictionaries schemas`). T020 (PL prefix on scans) is **not** in the
  public repo yet.
- **Environment:** fresh `py -3.13 -m venv` + `pip install -r requirements.txt` from the public clone: exit 0. Own OCR
  cache `ODW2JSON_OCR_CACHE_DIR=$S/run/ocrcache` (seeded with a copy of the shared cache for the 30 scans; the template
  scan and the noisy set were OCR'd cold). No server or container was started. Nothing in the repo or the T020 worktree
  was touched.

## 0. What I ran and saw

| Check | Command (from `$S/pub/slad`, fresh venv) | Result |
|---|---|---|
| Unit tests, CI-style | `python -X utf8 -m unittest discover -s tests -t .` | **270 tests OK, 10 skipped** (no uzp-data next to the clone), 18 s |
| Public CI | `gh run list -R Eterphis/slad` | run 44988765171 `tests` on `main`: **success**, 40 s |
| 30 UZP scans | `eval.prep_skany` → `odw2json --workers 4` → `eval.score` | **0.9789** (odwołanie 0.9943, pełnomocnictwo 0.9677, przelew 0.9444); 25/30 documents exactly equal to gold |
| Negatives (12) | same run, `negatywne/` | **12/12 `{}`** |
| Held-out 41-60 | `odw2json --workers 4` → `eval.score --cases 41-60` | **1.0000** (TP 706, FP 0, FN 0) |
| Template case (UZP `szablon-aplikacja/input/case1`) | `odw2json --workers 1` (cold OCR, 7-page scan) | 54 s; TED notice → `{}`; real appeal scan → JSON, see 1.2 |
| Noisy proxy (cases 53-60 rendered as scans, seed 7; the same cases score 1.000 as text PDFs) | `eval.make_noisy --cases 53-60 --seed 7` → `odw2json --workers 4` (cold OCR, 101 pages, **9 min 11 s**) → `eval.score` | **0.8964** (odwołanie 0.9448, **pełnomocnictwo 0.7339**, R 0.645, przelew 0.9167). Worst fields: `mocodawca[].data.nazwa` 14 errors, `mocodawca[].podpisujacy[].imie_nazwisko` 11 FN (0 TP), `przelew.tytul` 8, `ZamowieniePubliczne.tytul` 5. Report: `$S/run/noisy/report.md` |
| Docker | not re-run (8 min build). Cited: `reports/judge-manual-1.md` §1 PASS; its high defect (read-only `recipes` mount → HTTP 500 in the class editor) is fixed in the public `docker-compose.yml` (web mounts `./recipes` writable) | |

## 1. Scores per criterion

### 1.1 Jakość ekstrakcji (F1), weight 0.5: **4 / 5**

Level text (spec): 1 = F1 < 0.5; 3 = F1 ~ 0.75; 5 = F1 ≥ 0.9 on our held-out cases, incl. a few realistic/noisy ones.

Evidence for:
- Measured above, on the public code: scans 0.9789, 41-60 1.000, negatives 12/12. After T020 (reported, not yet in the
  public repo): scans 0.9854 (`reports/T020.md`).
- Rejection works on real-world negatives (TED notices, KIO rulings, ministry decisions).

Evidence against (why not 5):
- **The one real-layout document we have scores about 0.73.** The UZP template scan `przyklad odwolanie.pdf` is a
  real, anonymised KIO appeal (not synthetic; no gold). Hand-built gold from its OCR text (`$S/run/out/case1/przyklad odwolanie.json`):
  - correct (8): `data` 2025-06-16, `czynnosc_dzien` 2025-06-10, `czynnosc_powod_id` 4, `czynnosc_opis`, `miejscowosc`
    Warszawa, `przez-pelnomocnika` 1, `numer_bzp` 2025/BZP00270698, `numer_postepowania` RZP.27.29.2025.KD;
  - wrong: `Odwolujacy.nazwa` = `"KRS"` (FP), `pelnomocnik.imie_nazwisko` = `"Kancelaria Prawna"` (FP),
    `Zamawiajacy.nazwa` = `"odpowiedzialnością Warszawa"` instead of `Miejskie Przedsiębiorstwo Oczyszczania w m. st.
    Warszawie Spółka z ograniczoną odpowiedzialnością` (FP + FN), `pelnomocnik.nazwa` null instead of `Kancelaria Prawna -
    Radca Prawny` (FN), `tytul` null instead of `Dostawa preparatów do instalacji przetwarzania odpadów zlokalizowanej przy
    ul. Kampinoskiej 1 w Warszawie` (FN).
  - Field F1 = 16 / (16 + 3 + 3) = **0.73**. Some of the misses come from the redaction, but two have a structural cause
    that the hidden test will likely repeat (below).
- **Root cause 1: two-column party header.** Real appeals put the label in a left column, vertically centred against a
  multi-line value on the right. OCR line ordering puts `Zamawiający:` on the *second* line of the wrapped name
  (`Miejskie … Spółka z ograniczoną` / `Zamawiający: odpowiedzialnością` / `Warszawa`). The section regex starts at the
  label, so the first half of the name falls outside it. The synthetic set (and its scans) never has this layout, so
  0.979 does not measure it. Fixing it needs layout code (`ingest/layout.py`) or a multi-span strategy, so it is not
  safe before 09:30.
- **Root cause 2: title wording.** `tytul` strategy 2 needs `", nr referencyjny|numer postępowania"` after the title.
  Real text has `pn.:\n<title>" (postępowanie nr RZP…)`. This one is a YAML-only fix (improvement 3).
- **Noise alone costs about 0.10.** The same eight held-out cases go from 1.000 as text PDFs to **0.896** as
  synthetic scans. Pełnomocnictwo collapses (0.73): the principal's name and the signatories are not read from noisy
  OCR (signatories 0 of 11). This set is harsher than the UZP scans (0.979), but it shows where real, poorer scans
  will hurt: the signature block and the principal of a power of attorney.
- The rules were tuned on 01-40, the 41-60 pełnomocnictwo layouts were seen, and the scan set fed the misses analysis
  (README says this honestly). The 0.98 is an upper bound, not an estimate.
- T020 tunes the PL convention to the scan gold. If the hidden real gold follows the synthetic convention instead,
  this costs 2 leaves per scanned przelew. It is a coin flip that the human decided (D-026), not a defect.

**Estimate for the hidden Stage 1 set** (≥ 10 real cases, changed layout, partly scanned): odwołanie 0.75-0.88 (the
header and title layouts above; odwołanie has the most leaves, so it dominates micro-F1), pełnomocnictwo 0.73-0.95
(0.73 on the noisy proxy),
przelew 0.80-0.95 (real bank confirmations vary; the recipe has generic labels and positional fallbacks).
**Overall about 0.80-0.90.** That sits between level 3 (~0.75) and level 5 (≥ 0.9), so the score is 4. A team whose
rules only fit the synthetic layout would land well below this. Our OCR, rejection and checksums are strong.

### 1.2 Elastyczność i możliwość rozbudowy, weight 0.3: **4 / 5** (5 if demo part B lands live)

Level text: 3 = new field via config; 5 = new document type via config only, demonstrated live, with per-field evidence
(page/snippet/confidence) in the UI.

Evidence for:
- No class name appears anywhere in `odw2json/engine/`, `ingest/` or `pipeline.py` (`grep -rn "odwolanie\|pelnomocnictwo\|przelew"`
  → nothing). Classes are `recipes/*.yaml` validated by `recipes/recipe.schema.json`. Strategies, normalisers and
  validators are registries (`register_strategy`, …). OCR backends are pluggable (`register_backend`).
- Hot reload: `recipes.signature()` keys on file name, mtime and size, so a new YAML is picked up on the next document
  (`engine.py:34`).
- Web class editor: template → validate with line numbers → try on a PDF without saving → save. The full flow passed in
  `reports/judge-manual-1.md` (T015) on the demo PDF.
- Transparency (named as a bonus in the brief): every field carries page, snippet, rule, confidence and bbox, shown in the
  evidence table. Case consistency checks are reported, not applied to the output.
- An optional grounded LLM reader per field (`llm:` block in the recipe): it extends to new classes without code.

Evidence against (why a sceptical jury gives 4):
- "Bez programowania" is generous. A recipe is Python regex over diacritic-folded lowercase text. `recipes/odwolanie.yaml`
  is 246 lines of dense lookahead regex (e.g. the `Odwolujacy.nip` prose pattern). A UZP clerk cannot write that, so a
  new class at production quality still needs a regex-literate developer. Expect this question.
- "Demonstrated live" has not happened yet: Stage 1 jurors see only the repo and screenshots.
- Dictionary edits are not hot-reloaded (`signature()` watches only recipe files; still-open review finding in
  `review-T004.md`). Minor, unless someone edits `dictionaries/` live.

### 1.3 Architektura i jakość techniczna, weight 0.2: **4 / 5**

Level text: 3 = modules + README + tests; 5 = deep modules behind small interfaces, docs/ARCHITECTURE +
ADDING_A_DOCUMENT_CLASS, docker compose up works, CI tests green.

Evidence for:
- Small contract in `odw2json/model.py`: `Document/Page/Word/Evidence/Extraction` plus three Protocols
  (`Ingestor.ingest`, `Classifier.classify`, `Extractor.extract`). `factory.py` (74 lines) is the only wiring point.
  `RecipeEngine` is a deep module (one class serves as both classifier and extractor, about 360 lines, five public
  methods). Profiles (`text`/`ocr`/`llm`) are YAML. A process pool gives deterministic output.
- 270 unit tests green locally, public CI green, Dockerfile bakes the OCR models in for offline runs, `start.bat`
  bootstraps a venv on Python 3.13, and `eval/` ships its own scorer and benchmark with a regression gate.
- Licence hygiene: no AGPL/GPL (PyMuPDF, Ghostscript and spaCy pl were rejected on purpose). This matters for the §4 IP
  transfer.

Evidence against (why not 5): the docs the regulamin says it judges flexibility from are partly stale or leak
internal notes.
- `docs/ARCHITECTURE.md` contradicts the product in four places:
  - The diagram (line 15) says a rejected document gets "brak pliku wyjściowego", and line 54 says "nie dostaje pliku
    JSON". The product writes `{}`.
  - Line 32: "miejsce na `llm`". The llm profile exists.
  - Line 64: case consistency is "*planowane* (T009)". It is implemented (`odw2json/case/`, `recipes/case/relations.yaml`).
  - The module table omits `odw2json/llm/`, `odw2json/case/` and `ingest/preprocess.py`.
- Internal task IDs in public docs: `docs/ADDING_A_DOCUMENT_CLASS.md` lines 125-167 (`*(T018)*`, `*(gałąź T013)*`,
  `*(gałąź T005, po scaleniu)*`); `ARCHITECTURE.md` "D-005"; `docs/LLM.md:18` points to `reports/T016.md`, which is not
  in the repo.
- `docs/EXTERNAL_COMPONENTS.md` misses **llama-cpp-python (MIT)**, **the Qwen3-1.7B weights (Apache-2.0)** and **psutil
  (BSD-3)**. The pitch says "Pełna lista jest w docs/EXTERNAL_COMPONENTS.md", and regulamin §4.1 requires naming every
  external solution.
- The pitch says "test akceptacyjny to sprawdza grepem". That test lives in the private house checks, not in the public
  `tests/`, so a juror cannot find it.

### Weighted total

| Criterion | Weight (spec 50/30/20) | Score | Weighted |
|---|---|---|---|
| F1 | 0.5 | 4 | 2.0 |
| Elastyczność | 0.3 | 4 | 1.2 |
| Architektura | 0.2 | 4 | 0.8 |
| **Total** | | | **4.0 / 5 (80%)** |

Regulamin 50/50 (F1 + flexibility, the latter judged from architecture description, code and presentation): 0.5·4 +
0.5·4 = **4.0**. Stage 1 (100% F1): **4**, estimated hidden F1 0.80-0.90. Upside: elasticity 5 after a clean live
demo, architecture 5 after the docs fix → 4.3 (spec) / 4.5 (regulamin).

## 2. Top risks

### Stage 1 (hidden F1)
1. **Two-column party headers in real appeals** (label beside a wrapped value): Zamawiający/Odwołujący `nazwa`,
   pełnomocnik fields. Seen on the only real appeal we have. Not fixable safely before 09:30.
2. **Title and other prose phrasings** not in the synthetic set (`pn.: … (postępowanie nr …)`). YAML-fixable
   (improvement 3).
3. **Pełnomocnictwo on poor scans**: on the noisy proxy, the principal name and signatories are mostly lost (0.73).
4. **Real bank confirmations and real pełnomocnictwa** in layouts we have never seen. A misclassified document loses all
   its leaves (min_score 4 with margin 1). Rejection is strict, which helps on negatives and hurts on unusual positives.
5. **The PL convention** (T020) may be the opposite of the hidden gold. Scope is 2 leaves per scanned przelew.
6. **Time on the grader's laptop**: cold OCR has a 6 s median, but p95 is 86 s for a dense 5-6 page scan with the second
   pass (`T019.md`). The 24-document noisy set took 9 min with 4 workers here. Ten fully scanned cases come to about
   15-30 min. That is fine, unless the grader has a time limit.

### Stage II (pitch / Q&A)
1. **Demo step A8 shows wrong values.** The optional scan in the demo is the template appeal, whose output has
   `Odwolujacy.nazwa = "KRS"`, `pelnomocnik = "Kancelaria Prawna"` and `Zamawiajacy = "odpowiedzialnością Warszawa"`
   in plain sight. A juror who reads the JSON sees failure on the only real document. Replace it with
   `uzp-data/dane/skany/odwolania/0001/0001.pdf` (matches gold exactly).
2. **"Regex is programming"**: the "bez programowania" claim against 246 lines of lookahead regex. Prepare a straight
   answer: the template and the `after_label`/`between`/`lookup` strategies cover most fields without regex; regex is
   the escape hatch; the optional `llm:` block takes a plain-language question per field.
3. **"What is your F1 on real documents?"** Q4 says "nie wiemy". Better to give the honest number: on the one real
   (anonymised) appeal from the UZP template we read 8 of 11 checkable fields correctly. Two misses come from the
   two-column header, which is the next fix.
4. **Stale numbers and claims after T020**: slide 5 / NUMS 0.9789 → 0.9854, przelew 0.9444 → 0.9815. Q6 and slide line
   292 still say "przyjęliśmy konwencję syntetyczną" for PL, which is wrong after D-026/T020.
5. **Open placeholders**: Q1 "[potwierdzić ze zespołem, że wszyscy współautorzy podpiszą]" (the §4 IP transfer is a
   prize condition), Q7 public instance, and the fallback video, which is not recorded.
6. **Part B timing**: 8 steps in 60 s including a terminal switch and `start.bat`. `start.bat` processes all of
   `input/` and checks the venv first.

## 3. Improvements that are safe before 09:30 (ranked, max 6)

| # | Improvement | Expected gain | Effort | Risk |
|---|---|---|---|---|
| 1 | **Swap demo scan A8** to `dane/skany/odwolania/0001/0001.pdf` (exact match with gold; warm the OCR cache in rehearsal). Update `demo-plan.md` A8 and script §2 | Removes the single most visible failure on stage. Protects elasticity and F1 credibility (+0.3 to +0.5 on the Stage II impression) | 5 min | none (pitch files only) |
| 2 | **Fix `docs/ARCHITECTURE.md`**: rejected → `{}`; llm is real; case consistency implemented (`odw2json/case/`, `recipes/case/relations.yaml`); add rows for `llm/`, `case/`, `ingest/preprocess.py`. Strip `T0xx`/"gałąź"/`D-0xx`/`reports/T016.md` notes from `docs/*.md`. Add llama-cpp-python, Qwen3-1.7B and psutil to `EXTERNAL_COMPONENTS.md`. Then re-export and push to `slad` | Architecture 4 → 5 (+0.2 weighted), flexibility read from the docs (regulamin), §4.1 compliance | 25-30 min | very low: docs only. `tests/test_docs_recipe_reference.py` checks the recipe reference, so run the tests before the export |
| 3 | **`tytul` strategy for `pn.: <title>" (postępowanie nr …)`** in `recipes/odwolanie.yaml`: allow `["”]?\s*[,(]\s*(?:postepowanie\s+)?(?:nr|numer)` as the end. Gate: 01-40 / 41-60 = 1.000, scans ≥ 0.9854, and the template scan gets the title | +1 leaf per real appeal written in this common style (about +0.01 to 0.02 hidden F1). Also a live example of "fix = one line of YAML" for the pitch | 20-30 min (coder + check) | low: YAML only, regression gate on all sets |
| 4 | **Update pitch numbers and the PL wording after T020** (NUMS, script table, Q3 p95 wording: "ułamek sekundy" is true only for text PDFs; scans have a 6 s median and a p95 of tens of seconds) | Avoids a contradiction a juror can catch in the README | 10 min | none |
| 5 | **Pre-stage part B**: `input/demo/wezwanie.pdf` placed beforehand. Run `python -m odw2json --input input\demo --output output\demo` from shell history instead of `start.bat` | Part B fits in 60 s. Flexibility is the criterion this moment earns | 5 min | none |
| 6 | **Fill Q1 / Q7 placeholders, record the 2-minute fallback video**. Change "test akceptacyjny sprawdza grepem" to "możecie sprawdzić: `grep -rn odwolanie odw2json/engine` nic nie zwraca" (true in the public repo) | Removes three Q&A weak spots. A fallback exists if the demo fails | 20 min (video) + 5 min | none |

Not on the list: the two-column header fix (layout code, highest F1 upside, about 1-2 h, could regress scans) is not
safe before freeze. If the coordinator still wants it, it must sit behind the full gate (01-60 = 1.000, scans ≥ 0.9854,
negatives 12/12) and be merged before 09:30 or dropped.

## 4. Stage II pitch review (script.md + demo-plan.md, 5 min)

- **Timing**: 30+70+60+40+40+30+30 = 300 s. No slack at all. Cut the optional A8 entirely, or keep it only if part A
  finishes early.
- **F1 (0.5)**: covered in §2 (live values) and §5 (numbers by set, scans first, honest caveat on synthetic 1.000).
  Clear. Missing: one sentence on real-layout behaviour. Our misses list is a strength if we frame it: "we know exactly
  where it breaks".
- **Flexibility (0.3)**: §3 (live new class, try-on-PDF, save, CLI) is the strongest moment of the pitch, and §6 repeats
  it. Clear. Add one sentence that the `llm:` block lets a new class work with plain-language questions, so a new class
  does not depend on regex skill.
- **Architecture (0.2)**: §4 diagram, one contract (page = words with boxes), deterministic, local CPU, licences. Clear.
  "test akceptacyjny to sprawdza grepem" is not verifiable in the public repo (improvement 6).
- **Claims the product does not do (or not as stated)**:
  - Q6 and slide 7 (line 292): "wybraliśmy konwencję syntetyczną" for PL. False after T020 is merged and exported.
  - Q3: "p95 czasu rośnie z ułamka sekundy". Only true for text PDFs. Scans are seconds to tens of seconds.
  - Q4 and §6: "Pełna lista jest w docs/EXTERNAL_COMPONENTS.md". Not true for the LLM components until improvement 2.
  - Q6 points to `reports/misses-1.md`, which is private. Do not point the jury to it, or put a short misses section in
    the README.
  - "bez programowania" (§3, §6, README): defensible only with the regex caveat ready (risk 2).
  - All other statements I checked against code or runs are true: rejection to `{}`; class by content; checksum → 0.5
    confidence with the value kept; OCR ×0.9; grounded LLM quotes; hot reload; Docker offline OCR; permissive licences;
    12/12 negatives; 0.9789 scans on the public code.

## Single cheapest change that gains the most score

**Swap the demo scan (A8) for `dane/skany/odwolania/0001/0001.pdf`** (5 minutes, zero risk). The current one shows
three wrong fields on the only real document, live, in front of the jury. Right after it: the 25-minute
`ARCHITECTURE.md`/`EXTERNAL_COMPONENTS.md` fix plus re-export, the cheapest +0.2 on the written rubric.
