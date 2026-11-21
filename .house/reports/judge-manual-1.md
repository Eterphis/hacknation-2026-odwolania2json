# Judge report: manual acceptance criteria, round 1

- **Agent / model:** judge (Claude Opus 5.5)
- **Date:** 2026-11-21, 20:50-21:10
- **Build under test:** `main` at d038cc9 (T008, T011, T015, T016 merged), fresh `git clone C:/Users/jasiu/workspace`
  into the judge scratchpad (`.../scratchpad/judge/judge-clone`). Inputs: `input/przyklad_07/` (3 PDFs from
  `uzp-data/dane/przyklad_07`) and `input/case1/` (2 PDFs from `uzp-data/szablon-aplikacja/input/case1`).
- **Browser:** Playwright 1.48 driving installed Edge (`channel="msedge"`), fresh context per run (clean profile).
- Scratchpad root used below: `C:/Users/jasiu/AppData/Local/Temp/claude/b8fc54a61b30a2eb/ecb978e1-2d2f-4bdf-92ae-67103c3a68f5/scratchpad/judge`
  (`$J`). Drivers: `$J/t008.py`, `$J/t011.py`, `$J/t011b.py`, `$J/t015.py`, `$J/t015b.py`, `$J/t015c.py`,
  `$J/ground_check.py`; logs `$J/shots/t011-log.txt`, `$J/shots/t015-log.txt`, `$J/shots/t015b-log.txt`,
  `$J/docker-build.log`, `$J/docker-cli.log`.
- The main checkout was not touched outside `.house` (`git status` shows only `.house/PROGRESS.md`); the real
  `recipes/` still holds only the three UZP classes. All servers and the compose project were stopped/removed.

| Criterion | Verdict | Recorded with `house check` |
|---|---|---|
| T008 AC-4 (Docker + start.bat + README quick start) | **PASS** (one serious defect outside the literal AC) | yes |
| T011 AC-4 (Cold Trace review of the web UI) | **PARTIAL** (375 px: clipped key + 20 px horizontal page scroll) | no |
| T015 AC-3 (class editor) | **PARTIAL** (flow fully works; Cold Trace: two prime keys in one view, heading broken mid-word at 375 px) | no |
| T016 AC-4 (local LLM reader) | **PARTIAL** (all clauses met except the +0.05 skany target: +0.0068) | no |

---

## 1. T008 AC-4: clean checkout, Docker, start.bat, README quick start: PASS

**Docker image build** (`docker compose -p judgeclone build web`, Docker 29.9.3): exit 0 in 8 min 0 s (mostly pip
downloads), image `odw2json:latest` 575 MB, RapidOCR models baked in at build time. Log: `$J/docker-build.log`.

**`docker compose up --build`** (run as `-d` so I could drive it): container `judgeclone-web-1` up,
`GET http://localhost:8000/` -> 200 two seconds after start. Golden path in a clean Edge profile (`$J/t008.py`):
uploaded the 5 PDFs as one case, processed in 42.7 s, summary "Rozpoznane: 4. Odrzucone: 1 (pusty JSON {})."; cards:
negatywny przyklad.pdf rejected, the other four recognised with output names; ZIP download 2229 B with
`output/docker_mix/<5 files>.json`. Screenshot `$J/shots/t008-docker-web-results.png`.

**`docker compose run --rm cli`** on the clean `./input`: exit 0 in 49.3 s, `2 cases, 5 pdfs, 4 json written,
1 rejected/failed`. `output/przyklad_07/{odwolanie,pelnomocnictwo,potwierdzenie_przelewu}.json` are each an
**exact match** of the UZP gold JSON (`a == b` after `json.load`), `output/case1/negatywny przyklad.json` is `{}`.
Output is identical to the same run through the host venv except the line ending of `{}` (see defects).
`docker compose down` removed the container and network.

**start.bat (Windows, Python 3.13):** not re-run by me (costs a fresh venv + pip install). I cite the coordinator's
run on a fresh GitHub clone about an hour earlier: 2 cases, 5 PDFs, exit 0, 54 s, case 07 F1 1.0, negative -> `{}`.
I read `start.bat`: `py -3.13 -m venv`, fallback message with the download URL, reinstall only when
`requirements.txt` changes, `start.bat web` serves the UI. The host-venv CLI run in this clone (same code path as
start.bat after the venv) gave the same 6 files.

**README quick start:** I used only the README commands (`docker compose up --build`, `docker compose run --rm cli`,
`python -m odw2json`, `python -m web --port`), with input laid out as the README says (`input/<sprawa>/*.pdf`).
Everything worked without reading code. The README reads well for an AI judge too: what it does, quick start per
platform, a class/field table, measured F1 per set, screenshots.

**Defects (not part of the literal AC, but a juror will hit the first one):**
1. **High: class editor returns HTTP 500 under Docker.** `docker-compose.yml:10` mounts `./recipes:/app/recipes:ro`
   for the web service, so "Zapisz" in "Klasy dokumentów" fails: toast "Nie udało się zapisać · Serwer odrzucił
   zapytanie (500)", container log `OSError: [Errno 30] Read-only file system: '/app/recipes/...'`
   (`web/recipes_api.py:139` `_atomic_write`). The README advertises the editor (README "Zakładka „Klasy dokumentów”").
   Screenshot `$J/shots/t008-docker-class-save.png`. Fix: drop `:ro` on the web service's recipes mount (the CLI
   service may keep it), or set `ODW2JSON_READONLY_RECIPES=1` on the web service so the UI shows its proper
   read-only message instead of a 500.
2. Low: `odw2json/pipeline.py:60` writes the rejected `{}` with `write_text` (no `newline="\n"`), so on Windows it is
   `{}\r\n` while accepted JSONs are LF (`odw2json/write.py:60`). Valid JSON either way.

---

## 2. T011 AC-4: Cold Trace review of the web UI: PARTIAL

Server: `python -X utf8 -m web --port 8765` started from the clone. Driver `$J/t011.py` audits computed styles in
night/daylight at 1360 px and 375 px (mobile emulation, touch), before and after processing 5 PDFs (przyklad_07 +
template case1). Full output in `$J/shots/t011-log.txt`.

| Checklist item | Result | Evidence |
|---|---|---|
| Night default | pass | empty storage, OS `prefers-color-scheme: light` -> `data-theme="dark"`, switch `aria-checked=false` |
| Daylight switch works | pass | click -> `data-theme=light`, `localStorage ct-theme=light`, `aria-checked=true`, body bg rgb(214,229,238); survives reload; clicking back -> dark |
| Role tokens only | pass | frozen AC-3 grep is clean on main; audit found no text in a colour other than the ink tokens (`nonInkTextColours: {}`) |
| Chamfers, not rounding | pass | computed `border-radius > 0` only on vias (`.ct-v`) and the toggle thumb; frames use clip-path chamfers |
| Colour only in lines/vias/traces | pass | no non-ink text colours; state is carried by tag vias and score traces (screenshots) |
| One prime key per view | pass | `Przetwórz sprawę` is the only prime `.ct-btn` before and after results (ZIP/JSON keys are ground) |
| Anybody wide + Martian Mono | pass | h1 Anybody `font-stretch: 150%`, h2 145%; body, JSON `pre`, evidence `td` in Martian Mono; both faces loaded from the self-hosted `fonts.css` |
| Sentence case | pass | no heading/key/tag with Title Case or ALL CAPS |
| No shadows, glows, blur, emoji | pass | no element with `box-shadow`/`text-shadow`/`filter`/`backdrop-filter`; 0 emoji, 0 exclamation marks in page text |
| 375 px, 44 px targets | **fail (partial)** | all visible interactive elements >= 44x44, no overflow before results or on the evidence tab (table scrolls inside its box: 1031 px in a 295 px box) **but** after opening the JSON tab the page scrolls horizontally: `scrollWidth 395 > 375`, the culprit is the "Pobierz odwolanie.json" ground key (right edge 395 px), its label visibly clipped ("Pobierz odwolanie.jso"). Longer names (`potwierdzenie_przelewu.json`, `przyklad odwolanie.json`) are worse. `$J/shots/t011-04-json-dark-375.png` |
| Focus visible (signal) | pass | links/switch/drop zone: 2 px solid rgb(56,221,255); the case input shows focus by `.ct-input:focus-within` (aurora fill) per the kit |
| Eterphis lockup in top bar | pass | `.topbar .eph-lockup--h` with 2 SVGs (mark + wordmark), mark 40 px high, `aria-label="Eterphis, strona główna"`, links home |
| Upload shows classes, rejected doc, JSON, evidence | pass | 4 recognised cards with class + score traces; "Odrzucony · Brak pasującej klasy" for `negatywny przyklad.pdf` with summary "(pusty JSON {})"; JSON tab with Martian Mono `pre`; evidence `.ct-table` with 20 rows for odwolanie; consistency checks shown as tags. No console errors. |

Screenshots: `$J/shots/t011-01-default-night.png`, `$J/shots/t011-02-after-switch-daylight.png`,
`$J/shots/t011-03-results-{dark,light}-{1360,375}.png`, `$J/shots/t011-04-json-{dark,light}-{1360,375}.png`,
`$J/shots/t011-05-rejected-{dark,light}-{1360,375}.png`.

**Defects**
1. **375 px overflow (blocks PASS):** `web/static/app.js:196` builds the key `"Pobierz " + d.output_name`; the kit's
   key face is `white-space: nowrap` (`web/static/coldtrace/bundle.css:262`), so the key exceeds the 327 px column.
   Cheapest fix: label it "Pobierz JSON" (file name is already shown in the card), or let this key wrap/shrink
   (`max-width: 100%` and ellipsis on the face) in `web/static/app.css`.
2. Copy (Cold Trace voice, Polish UI): engine strings in English reach the screen: "recipe odwolanie.yaml" as the
   "Dlaczego ta klasa" reason (`odw2json/engine/engine.py:77`), "rejected: forbidden signal"
   (`odw2json/engine/engine.py:62`), "1 value(s) agree" / "not found on the other side: ..."
   (`odw2json/case/step.py:132-133`). Not a checklist failure on its own, but a Polish jury sees mixed languages.
3. Minor: evidence `td` has `font-variant-numeric: normal`; Martian Mono is monospaced, so digits align anyway.

---

## 3. T015 AC-3: "Klasy dokumentów" editor: PARTIAL

Run against the server started from the scratch clone (its own `recipes/`), never against the workspace recipes.
Drivers `$J/t015.py` (create, broken regex, try, save, upload, theme/375 audit, delete) and `$J/t015b.py`
(race-free edit re-run, CLI, delete, upload after delete). Test PDF `$J/shots/wezwanie.pdf` (text layer, generated
with Edge print-to-PDF: "WEZWANIE DO ZAPŁATY ... Kwota do zapłaty: 1 234,50 zł ... w terminie do 15.12.2026").

| Step | Result | Evidence |
|---|---|---|
| Open "Klasy dokumentów" | pass | list of 3 UZP classes with field counts and "Klasa zadania UZP" tags (`t015-01-list-night.png`) |
| New class from template, 'wezwanie' with two fields | pass | template loaded (`class: nowa_klasa`), renamed to `wezwanie`; "Szkielet z pól" built `{"wezwanie": {"kwota": null, "termin": null}}` |
| Broken regex -> error with file/JSON path | pass | `(\d[\d .]*,\d{2}` -> error list "linia 27 · fields/0/strategies/0/value · bad regex ... missing ), unterminated subpattern at position 0 (check brackets ...)", gutter line 27 marked, fault toast "Receptura nie przeszła sprawdzenia: 1 błąd" (`t015-02-broken-regex-night.png`) |
| Fix -> valid | pass | "Receptura jest poprawna · Klasa wezwanie, 2 pola.", error list hidden |
| Try on uploaded PDFs | pass | 2 files: wezwanie.pdf "Rozpoznany jako wezwanie", draft score 5 (przelew 2, others 0), evidence table `wezwanie.kwota 1234.5 p.1 "Kwota do zapłaty: 1 234,50 zł" after_label 1` and `wezwanie.termin 2026-12-15 p.1 "...w terminie do 15.12.2026..." regex 1`, JSON shown; the UZP appeal PDF "Nie rozpoznany jako wezwanie, wygrała: odwolanie"; toast "Nic nie zostało zapisane" (`t015-03-try-night.png`) |
| Save | pass | "Dodano klasę wezwanie"; `recipes/wezwanie.yaml` + `recipes/wezwanie.output.json` on disk |
| Next upload uses it, no restart | pass | same server process: upload of wezwanie.pdf -> "Rozpoznany · wezwanie", score 5, 2 evidence rows (`t015-04-upload-uses-class-night.png`) |
| `python -m odw2json` on ./input uses it | pass | from the clone, default profile and paths, `input/judge_wezwanie/wezwanie.pdf` added: exit 0 in 3.0 s, `output/judge_wezwanie/wezwanie.json` = `{"wezwanie": {"kwota": 1234.5, "termin": "2026-12-15"}}`, other cases unchanged |
| Edit | pass | description and signal weight 3 -> 4 changed and saved ("Zapisano klasę wezwanie"), file on disk updated, previous version kept as `.bak`; next upload scores 6 instead of 5. (My first edit attempt raced the async `openEditor` load; the re-run waits for the editor to load and passes.) |
| Delete | pass | two-step Cut key ("Potwierdź usunięcie"), notice "Usunięto klasę wezwanie · przeniesiony do wezwanie.yaml.bak"; list back to 3; next upload of wezwanie.pdf -> "Odrzucony · rejected: best przelew 2 < min_score 4" |
| Night / daylight / 375 px | **partial** | no horizontal scroll at 375 (scrollWidth 375), all targets >= 44 px, no shadows, rounding only on vias, both themes render (`t015-06-editor-{light-1360,dark-375,light-375}.png`). **But** see defects 1-2. |

**Defects**
1. **Two prime keys in one view (checklist: exactly one):** with the editor open, `#view-classes` shows two prime
   keys, "Nowa klasa z szablonu" (`web/static/index.html:128`) and "Zapisz" (`web/static/index.html:166`), both
   plain `.ct-btn` (measured with `$J/t015c.py` at 1360 and 375 px). Fix: make "Nowa klasa z szablonu" a ground key
   (or ground it while the editor is open).
2. **Heading broken mid-word at 375 px:** "Klasy dokume|ntów" over 3 lines, caused by
   `overflow-wrap: anywhere` in `web/static/app.css:178`. Fix: drop it and lower the clamp (e.g. `9.5vw`) or use
   `hyphens: auto` (the page is `lang="pl"`).
3. Low: delete moves only the recipe to `.bak` and leaves `recipes/<name>.output.json` behind
   (`web/recipes_api.py:249-262`); a delete also overwrites the `.bak` from the last edit. Seen on disk after delete:
   `wezwanie.output.json`, `wezwanie.output.json.bak`, `wezwanie.yaml.bak`.
4. Under Docker the editor cannot save at all (T008 defect 1).

---

## 4. T016 AC-4: local LLM reader: PARTIAL

Sources: `.house/reports/T016.md`, `.house/reports/T016-bench.md`, `bench/history.csv`, code in `odw2json/llm/`,
bench outputs in `C:/Users/jasiu/workspace/.acc/bench-llm/work/runs/`.

| Clause | Result | Evidence |
|---|---|---|
| `llm` beats `ocr` on skany F1, **target +0.05** | **not met** | history.csv (6d073f0 and c1c42dc, 2 workers): ocr skany 0.9639, llm 0.9707 -> **+0.0068**, 14 % of the target. `diff -r` of the two output trees: exactly 4 values differ, all `pelnomocnicy[*].pesel` null -> filled (pel_0004, pel_0007, pel_0009 x2). |
| No loss on heldout | pass | heldout 0.9986 vs 0.9986; `diff -r ocr-heldout-w2/out llm-heldout-w2/out` is empty |
| No loss on negatives | pass | reject accuracy 100 % both; `diff -r` of the negatywne outputs is empty |
| Peak RAM < 10 GB at 2 workers | pass | 5111 MB (heldout), 4973 MB (skany), 5145 MB on the re-run |
| Model <= 4B params, Apache-2.0/MIT | pass | `profiles/llm.yaml` -> `models/Qwen3-1.7B-Q8_0.gguf` (1,834,426,016 B on disk); `odw2json/llm/fetch.py` registry pins repo, size, sha256 and licence "Apache-2.0" for all four models (<= 4B) |
| Offline after one-time download | pass (by code reading) | the only network code is `fetch.py` (`urllib.request.urlretrieve`, sha256-checked); `runtime.py` loads a local GGUF via `Llama(model_path=...)`; failed download never fails the run (`fetch.py:54-67`). I did not pull the network cable. |
| Every LLM value has evidence with a quote found in the page text | pass | code: `reader.py:180-195` drops any answer whose quote is not found in the pages the model saw (`grounding.PageText.find`, folded skeleton, min 3 chars) or whose value is not inside its quote; filled values get evidence `Evidence(path, value, page, snippet, "llm:<model>", 0.8)` (`reader.py:228-231`); group items go through the same `_candidate`. Outputs: `$J/ground_check.py` re-ingested the three scans and found all 4 LLM values in the OCR page text: `'PESEL: 69102340858'` p.1, `'PESEL: 90082629103'` p.1, `'PESEL: 68091502944'` p.1, `'PESEL: 82070226436'` p.1. |

**Verdict reasoning.** Every clause except the uplift target holds, and the safety story (grounding, never-override)
checks out in code and on outputs. The +0.05 target is missed by a factor of 7. Context: the target was written when
`ocr` scored 0.7344 on scans (history.csv b8a6b80); T014 recipes then raised `ocr` to 0.9639, leaving 0.036 of
headroom, most of it lines that OCR lost entirely, which no reader of the OCR text can recover. That explains the
miss but does not change the criterion, so this is PARTIAL, not PASS.

**Recommendation: keep `llm` opt-in, do not make it default, do not drop it.** Cost: p95 goes from 0.38 s to
128.7 s per document on this laptop, docs/min from 516 to 6.9 on skany, +4.8 GB RAM, for +0.0068 F1. Benefit worth
keeping: a generic, class-agnostic, grounded fallback any new recipe can opt into with `llm:` (a good "extensibility
+ robustness" story for the pitch), at zero cost when the profile is off. If the coordinator wants this AC closed,
that is a Q-### to the human about re-baselining the target, not something the judge changes.

---

## Reviews by the other model family
The only `reports/review-*.md` files cover T001, T002 and T004; none covers the four tasks judged here.

## Cheapest change that gains the most
Three one-line web fixes close two PARTIALs and remove the 500 a Docker juror would hit:
(a) `docker-compose.yml:10`: drop `:ro` on the web service's `./recipes` mount (or set `ODW2JSON_READONLY_RECIPES=1`);
(b) `web/static/app.js:196`: label the per-document download key "Pobierz JSON";
(c) `web/static/index.html:128`: `class="ct-btn ct-btn--ground"` for "Nowa klasa z szablonu", plus removing
`overflow-wrap: anywhere` at `web/static/app.css:178`. Then re-check T011 AC-4 and T015 AC-3 (about 10 minutes).

---

## Re-check after the fixes (main 8bdac0c, local commit, not pushed), 2026-11-21

Fresh `git clone C:/Users/jasiu/workspace` -> `$J/clone2` (HEAD 8bdac0c; diff vs d038cc9: `docker-compose.yml`,
`web/static/app.css`, `web/static/app.js`, `web/static/index.html`). Server `python -X utf8 -m web --port 8766` from
the clone, Edge via Playwright, clean context per run. Drivers: `$J/recheck.py` (new), plus the earlier `$J/t011.py`,
`$J/t015.py`, `$J/t015b.py` re-run unchanged. Output log `$J/shots2-recheck-log.txt`, screenshots in `$J/shots2/`.
A CPU-heavy LLM trace was running on the machine, so I did not judge timings.

### Previously failing items
| Item | 375 night | 375 daylight | 1360 night | 1360 daylight |
|---|---|---|---|---|
| Process view, all 4 JSON tabs open: `scrollWidth` / overflowing elements | 375 / none | 375 / none | 1360 / none | 1360 / none |
| Per-document download key | "Pobierz JSON" x4, `aria-label`/`title` "Pobierz odwolanie.json" | same | same | same |
| Class view, list only: prime keys | none | none | none | none |
| Class view, editor open: prime keys | "Zapisz" only | "Zapisz" only | "Zapisz" only | "Zapisz" only |
| Class view `scrollWidth` (list / editor) | 375 / 375 | 375 / 375 | 1360 / 1360 | 1360 / 1360 |
| Class heading | 30 px, 2 lines "Klasy / dokumentów", `overflow-wrap: normal`, no mid-word break | same | 72 px, 1 line | same |
| Touch targets < 44 px | none | none | none | none |
| `[id=null]` elements / console errors | 0 / none | 0 / none | 0 / none | 0 / none |

Screenshots: `$J/shots2/re-json-{dark,light}-{375,1360}.png`, `$J/shots2/re-classes-{dark,light}-{375,1360}.png`,
`$J/shots2/re-editor-{dark,light}-{375,1360}.png`, `$J/shots2/t011-04-json-dark-375.png` (key reads "Pobierz JSON", fully visible).
Note: at 375 px the heading's `scrollWidth` is a few px wider than its own box, but the word ends inside the 16 px
gutter and the page does not scroll (screenshot `re-classes-light-375.png`). With the editor closed the class view has
no prime key at all; I accept that, because the rule is there to stop competing prime keys, and a browse state needs no prime action.

### Sanity pass on the rest
- **T011 checklist** (`t011.py` re-run, all 4 theme x width combinations after processing 5 PDFs): night default with
  empty storage (even with OS light), Daylight switch toggles `data-theme`, `localStorage` and `aria-checked` and
  survives reload; no rounding except vias/thumb, no shadows/filters, 0 emoji, 0 "!", no non-ink text colours, one
  prime key ("Przetwórz sprawę"), Anybody 150 % / Martian Mono (body, JSON, table), no Title Case/ALL CAPS, Eterphis
  lockup (2 SVGs, 40 px, links home); rejected card, classes with scores, JSON tab and the 20-row evidence table all present.
- **T015 flow** (`t015.py` + `t015b.py` re-run against the clone's own `recipes/`): broken regex -> "linia 27 ·
  fields/0/strategies/0/value"; fixed -> "Klasa wezwanie, 2 pola"; try on 2 PDFs -> 1 of 2 recognised, evidence for
  kwota 1234.5 and termin 2026-12-15; save -> "Dodano klasę wezwanie"; next upload recognised (score 5); edit saved
  and on disk (weight 4 -> next upload score 6, `.bak` kept); `python -m odw2json` on ./input wrote
  `{"wezwanie": {"kwota": 1234.5, "termin": "2026-12-15"}}`; delete -> list back to 3, next upload rejected.
  375 px and daylight editor metrics: no overflow, no small targets, no shadows.
- **Docker class editor** (optional): `docker compose -p judgeclone2 up --build -d` from the clone (cached, 9.5 s),
  `PUT /api/recipes/docker_test` -> 200 `created: true`, listed, `docker_test.yaml` appeared in the host
  `recipes/`; `DELETE` -> 200 with `.bak`. The T008 defect 1 (500 on save) is fixed. Compose project removed afterwards.
- Known and out of scope, still present: English engine messages, leftover `.output.json` after delete.

### Re-check verdicts
- **T011 AC-4: PASS**, recorded with `house check`.
- **T015 AC-3: PASS**, recorded with `house check`.
