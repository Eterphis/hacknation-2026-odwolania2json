# Handoff: teammate session -> orchestrator (2026-11-21, after D-018)

> **PL (dla człowieka):** Sesja teammate'a kończy pracę. Wszystko jest wypchnięte. Do scalenia zostały dwie gałęzie:
> `task/T013-new-uzp-data` (dostosowanie do nowych danych UZP; skany 0,56 → 0,73, negatywy 16/16, każdy PDF ma JSON)
> i jeden commit na `task/T008-packaging-docs` (dokumentacja nowych normalizatorów). Obie łączą się z `main` czysto,
> testy po scaleniu przechodzą (131 OK). Propozycja T012 (poziomy P0–P4) wymaga korekty pod D-015: LLM lokalnie, bez API.

## 1. State of every branch (all pushed, no local changes)
| Branch | Head | On main? | What to do |
|---|---|---|---|
| task/T005-recipes-przelew-pelnomocnictwo | 1c15b15 | merged (6c2084e) | nothing |
| task/T006-recipe-odwolanie | 32e5cad | merged (56cd8f1) | nothing |
| task/T008-packaging-docs | 7b521ad | 4e094c8 merged; **7b521ad not** | merge the one follow-up commit (docs rows for `regex raw`, `person`, `company`, `ocr_digits`; needed once T013 is in, else `tests/test_docs_recipe_reference.py` fails) |
| **task/T013-new-uzp-data** | see `git log` | **no** | review + merge (contains T005+T006 history, already on main; code merges cleanly). Report: `teammate-handoff/T013.md` on that branch (move it to `.house/reports/T013.md` as usual) |
| proposal/T012-T013-tiers-and-new-data | c054bf3 | no | task texts for `.house/tasks/` (see 4); do not merge as code |
| handoff/teammate-final | this file | no | read, then move to `.house/handoff/` or delete |

Checked on a throw-away worktree: `origin/main` + T013 + T008 follow-up -> `Ran 131 tests ... OK (skipped=4)`,
`dane/skany` score 0.7344, no conflicts.

## 2. Results (exact F1, eval/score.py, new UZP gold)
| Set | main before T013 | with T013 |
|---|---|---|
| dev 01-40 | ~0.999 | 0.9992 |
| held-out 41-60 (partly contaminated: T005 looked at 41-60 with the owner's OK, D-014) | 0.9444 | 0.9444 (odw 0.9045, pel 0.9971, prz 1.0000) |
| `dane/skany` 30 scans | 0.56-0.58 | **0.7344** (odw 0.6562, pel 0.9211, prz 0.6957) |
| `dane/negatywne` 12 + 4 negatives inside przyklad_04/10/24/37 | 15/16 rejected, no file written | **16/16 -> `{}`** |
| every input PDF gets `<name>.json` | no | 226/226 |
Note: T013 rules were written while reading `dane/skany` texts and pred-vs-gold diffs, so 0.73 is a dev number (D-017
calls skany the main independent measure: a new untouched set would be needed for that).

## 3. What T013 contains (details: teammate-handoff/T013.md on the branch)
- **D-016 (1) done:** rejected/unreadable PDF -> `{}`; CLI `--rejected-json {}|empty|none` / env `ODW2JSON_REJECTED_JSON`
  (maps to D-016's `output.rejected: empty_object|empty_file|none`; rename if you want the config key).
- **D-016 (3) done:** code 12 + official labels (UZP changed code 6 text to "Odpowiedzi/wyjaśnienia do SWZ" in gold).
- KIO rulings rejected (the false accept in the baseline).
- **OCR reading order fix** (`odw2json/ingest/layout.py`): skewed scan lines merged 2-4 text lines into one; now lines
  group by centre distance with a fixed band and words that overlap horizontally never share a line. Biggest gain.
- Engine (generic, tested): `regex raw: true`, `merge` without duplicates, normalisers `person` (ALL CAPS -> Name),
  `company` ("Sp. z 0.o." -> "Sp. z o.o."), `ocr_digits`.
- pelnomocnictwo for real letters: "X z siedzibą w", signatories from "reprezentowana przez: X – Prezes" and
  "Dokument podpisany przez X", attorneys listed after "udziela pełnomocnictwa:" without titles; plural "udzielają".
- `eval/prep_skany.py`: input/gold trees for `dane/skany` + `dane/negatywne`.

## 4. Open work, by expected F1 gain (for new tasks)
1. **odwolanie on scans (0.66)**: `ZamowieniePubliczne.tytul` 0/10, pełnomocnik block 0/9 (`przez-pelnomocnika` 0.10),
   `czynnosc_dzien` 0.10, `Odwolujacy.nazwa` 0.50 (party roles = the mentors' "hardest part", D-015), `numer_ted` 0.60.
2. **przelew on scans (0.70)**: `tytul` 0.33 (OCR drops diacritics: "odwolania" vs gold "odwołania"; rules can't restore
   them, a grounded local LLM reader or a diacritics dictionary can), `numer_transakcji` 0.40, accounts 0.71-0.82
   (gold keeps the `PL` prefix in prz_0001/0006 but not elsewhere: ask or ignore).
3. pelnomocnictwo: `pesel` per attorney 0/4 (needs a per-item field next to `imie_nazwisko`), sole trader as principal.
4. `.house/accept/output_shape.py` still requires NO json for listed rejects: update to accept `{}` (D-016).
5. **T012 tiers + bench** (`proposals/T012-demo-tiers.md` on the proposal branch) **must be adapted to D-015**:
   P3/P4 = local model via llama.cpp (Qwen3 / Bielik / Basal, Apache-2.0/MIT, CPU, 16 GB), no API; P3 stays a grounded
   gap-filler (value must be quoted from the page, never overwrites a full-confidence recipe value). Keep P0 text,
   P1 +OCR, P2 +classifier (TF-IDF+LR, then Basal-pico/mini), `--workers N`, the bench on dev/41-60/skany/negatywne with
   F1 + p50/p95 time + throughput at 1/2/4/8 workers + peak RAM + model size, and the regression gate.
   `proposals/T013-new-uzp-data.md` is done by the branch above.
6. Speed: first OCR run of 42 PDFs ~8.5 min sequential (~12 s per scanned doc); OCR words cached in
   `%TEMP%/odw2json-ocr-cache`. Parallel workers (T012 step 1) are the cheap win for the grader's time budget (Q-004 q5).

## 5. Environment notes (this machine, for whoever continues here)
- Git hook: `python3` is the MS Store alias here; fixed by `.venv/Scripts/python3.exe` (copy of python.exe) first on PATH.
- `uzp-data` pulled to upstream 84cc976 (the owner's machine must pull too).
- A dev web server of the T005 branch may still run on port 8010 (preview config `odw2json-web-t005` in
  `Desktop/hackathon/.claude/launch.json`); port 8000 is another session's `preview` demo. Docker image `odw2json:latest`
  is built locally (T008).
- Worktrees here: `.worktrees/T005-…`, `T006-…`, `T008-…`, `T013-…`, `proposal-tiers`, `handoff-final` (all clean);
  safe to remove after merging.
