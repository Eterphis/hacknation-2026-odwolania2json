# ODWOLANIA2JSON (HackNation 2026, partner UZP): rules and task contract check

- Agent / model: researcher (haiku), second pass, 2026-11-21 (replaces the partial first pass)
- Status: Task brief, README, schemas and training folders are now readable. The per-task regulamin, F1 definition, grader, ground_truth.yaml and data license are NOT published in any source read here.

## Answer first

1. The task brief is public: the repo README (`hacknation-2026/README.md`) gives the I/O contract, the F1 metric and the tech rules. Task page `hacknation.pl/zadania` now loads (HTTP 200); its per-task `rules`, `details` and `materials` fields are all `null`, so NO per-task regulamin is published there.
2. Confirmed hard requirements (README): Python 3.13+; `requirements.txt`; ONLY open-source components "(w tym otwarto-zrodlowe modele jezykowe)"; runs on-premise without GPU, "(LLM po API)"; CLI or wrapper script (e.g. `start.bat`); `input/` and `output/` folders in the project root.
3. The LLM-via-API question is the main rules risk. Literal reading: a proprietary hosted LLM is NOT an open-source component, so it is NOT allowed. The parenthesis "(LLM po API)" could mean an open-source model served through a local API. UNCLEAR, needs organizer confirmation before we design around a hosted model.
4. Data: 60 training folders (`dane/przyklad_01` to `przyklad_60`), not 39 as the deck says. Each has 3 reference JSON files and 3 PDFs. NO `ground_truth.yaml` in any folder checked (przyklad_01 returns 404 for it). No license file in the repo (LICENSE 404).
5. F1 definition, grader command, time limits and scoring details: NOT FOUND in any source. The README only says "Podstawowa miara jakosci bedzie wskaznik F1" and links to Wikipedia.
6. Submission: README section 4 requires a title and a GitHub link to a working prototype where documents are uploaded and extraction results are read. Repo, technical docs and own test results are optional. Video and slides are NOT mentioned in the README.

## Sources

| # | Source | Used for | Access |
|---|---|---|---|
| S1 | https://raw.githubusercontent.com/Urzad-Zamowien-Publicznych/hacknation-2026/main/README.md (saved: `C:/Users/jasiu/AppData/Local/Temp/claude/b8fc54a61b30a2eb/ecb978e1-2d2f-4bdf-92ae-67103c3a68f5/scratchpad/odw/README.md`) | I/O contract, tech rules, F1, submission | curl, HTTP 200 |
| S2 | https://raw.githubusercontent.com/Urzad-Zamowien-Publicznych/hacknation-2026/main/oczekiwane-json/odwolanie.json, `pelnomocnictwo.json`, `przelew.json` (saved in the same scratchpad folder) | Reference JSON schemas | curl, HTTP 200 |
| S3 | https://github.com/Urzad-Zamowien-Publicznych/hacknation-2026/tree/main/dane and `/przyklad_01` ... `/przyklad_60` (HTML folder listings) | Training folder layout and count | curl on HTML listing; GitHub REST API rate-limited (403), not used |
| S4 | https://raw.githubusercontent.com/Urzad-Zamowien-Publicznych/hacknation-2026/main/dane/przyklad_01/{odwolanie,pelnomocnictwo,przelew}.json | Sample filled reference output | curl, HTTP 200 |
| S5 | https://github.com/Urzad-Zamowien-Publicznych/hacknation-2026/tree/main/szablon-aplikacja | Template folder: I/O example only, no code | curl on HTML listing |
| S6 | https://hacknation.pl/zadania (saved HTML, scratchpad `odw/zadania.html`; the ODWOLANIA2JSON entry is in the embedded data) | Task card: initiator, prize, rules/details/materials fields | curl, HTTP 200 (earlier WebFetch timeouts; curl worked on retry) |
| S7 | https://hacknation.pl/api/public/dokumenty/28c74284-6390-4665-b8aa-bf4367db79c0/regulamin-hacknation_19.11.pdf (saved; text via `pdftotext`) | General regulamin: jury, IP, deadlines | curl, HTTP 200. Legacy encoding; read via pdftotext. Its own text says "Regulamin obowiazuje od 28 wrzesnia 2026 r." (sec. 6 at end), the file name says 19.11 |
| S8 | https://github.com/Urzad-Zamowien-Publicznych (org) | Other repos | WebFetch: 2 public repos: `hacknation-2026` (updated 2026-11-21) and `open-mercato-ezd` (fork of an open-source CRM/ERP framework, MIT, unrelated) |

Not reached: `https://hacknation.pl/zadania/odwolania2json` returns 404 (the task is a card on `/zadania`, not a subpage). The "per-task regulamin" link is absent from the task card (`rules: null`).

WebSearch lead (not a primary source, not used for any claim): gov.pl attachments with a KIO appeal-review spec. Not linked to this task by any source read.

## Task contract (I/O, schemas, grader)

CONFIRMED (S1, README):
- Input: one case folder per case, each with PDFs of one appeal (`input/caseN/*.pdf`). Three document types: odwolanie, pelnomocnictwo, przelew (potwierdzenie przelewu).
- Output: `output/caseN/` with one JSON per input PDF, "nazwany tak samo jak plik z katalogu input ktoremu odpowiada". Example tree in README: `odwolanie_nr_1.json`, `pelnomocnictwo_nr_1.json`, `przelew_nr_1.json`.
- Run: "interfejs ... CLI, wrapper script (np. plik start.bat), lub inne analogiczne rozwiazanie."

CONFLICT (S1 vs S4): the README example names inputs `odwolanie_nr_1.pdf`, the training folders use `odwolanie.pdf`, `pelnomocnictwo.pdf`, `potwierdzenie_przelewu.pdf` and reference JSON `odwolanie.json`, `pelnomocnictwo.json`, `przelew.json`. The rule "same name as the input PDF" then gives `potwierdzenie_przelewu.json`, not `przelew.json`. UNCLEAR which naming the grader uses.

Reference schemas (S2, S4). The files contain `//` comments and are NOT valid JSON (`odwolanie.json` is missing a comma after `"nazwa"` in `pelnomocnik`). Keys:

- `odwolanie.json`: top key `OdwolanieKIO` with `data` (date from the header, ISO), `czynnosc_dzien` (ISO date of the act that starts the appeal deadline for the first charge, or null), `czynnosc_powod_id` (integer 1-12, from the FIRST charge only), `czynnosc_opis` (canonical description 1:1 with the id, from the first charge only), `miejscowosc` (from the header). Plus `Odwolujacy` (list: `krs`, `nazwa`, `nip`, `regon`, `przez-pelnomocnika` as 1/0 with a hyphen in the key, `pelnomocnik` {`imie_nazwisko`, `nazwa`, `mail`}), `Zamawiajacy` (list: `krs`, `nazwa`, `nip`, `regon`, `prowadzacy_postepowanie` null/1/0), `ZamowieniePubliczne` (`numer_bzp`, `numer_postepowania`, `numer_ted`, `tytul`).
- `pelnomocnictwo.json`: `mocodawca` (list: `data` {`imie_nazwisko`, `krs`, `nazwa`, `nip`, `typ` "osoba_prawna"/"osoba_fizyczna"}, `podpisujacy` (list of {`imie_nazwisko`})), `pelnomocnicy` (list: `imie_nazwisko`, `pesel`).
- `przelew.json`: `przelew_bankowy` with `data_operacji`, `kwota` (number), `na_rachunek`, `numer_transakcji` (nullable), `tytul`, `z_rachunku`.

Code list for `czynnosc_powod_id` (1-12): no published list, but the coordinator read all 60 gold `odwolanie.json` files (2026-11-21) and recovered ids 1-11, always 1:1 with `czynnosc_opis`: 1 Decyzja o odrzuceniu oferty; 2 Ogłoszenie wyboru oferty; 3 Decyzja o wykluczeniu wykonawcy; 4 Publikacja specyfikacji warunków zamówienia (SWZ); 5 Modyfikacja treści SWZ; 6 Odpowiedzi i wyjaśnienia do SWZ; 7 Zaniechanie odrzucenia oferty; 8 Zaniechanie wykluczenia wykonawcy; 9 Decyzja o unieważnieniu postępowania; 10 Zaniechanie unieważnienia postępowania; 11 Opis przedmiotu zamówienia (OPZ). Id 12: NOT FOUND (ask UZP). (The researcher's first pass saw only ids 4 and 9.)
Data note (coordinator): the training data is synthetic (KRS/NIP/REGON start with 999, `*.example` mails), so personal-data concerns about the PDFs are low; the licence question stays open.

Sample reference (S4, przyklad_01): `data` null, `czynnosc_dzien` "2026-03-20", `czynnosc_powod_id` 9, `miejscowosc` null, `numer_ted` "999137-2026", `numer_bzp` "2026/BZP00999778". Note `numer_bzp` format in the schema comment: `YYYY/BZP ########`, but the sample has no space.

Dataset (S3): folders `dane/przyklad_01` to `przyklad_60`. The listing of all 60 folders shows the same six files in each: `odwolanie.pdf`, `odwolanie.json`, `pelnomocnictwo.pdf`, `pelnomocnictwo.json`, `potwierdzenie_przelewu.pdf`, `przelew.json`. Total: 60 sets, 180 PDFs, 180 JSON references. The deck said 39 sets and 117 PDFs. Count from the repo is authoritative for now; the deck numbers are stale or refer to a different snapshot. I did not open the PDFs.

## ground_truth.yaml

NOT FOUND. No `ground_truth.yaml` in `przyklad_01` (HTTP 404) or at `dane/`. The reference is the per-folder JSON (`odwolanie.json`, `pelnomocnictwo.json`, `przelew.json`), which is the same format as the schema above. The deck mentioned `ground_truth.yaml`; that name is not used in the public repo. UNCLEAR whether the hidden grader reads YAML or JSON.

## Scoring

CONFIRMED (S1 README sec. 6-7):
- "Podstawowa miara jakosci bedzie wskaznik F1" (linked to Wikipedia F-score).
- Stage I (preselection): "Jakosc ekstrakcji danych (F1 Score) - 100%", against reference data "na nieznanym zbiorze testowym".
- Stage II (final): F1 50%; "Elastycznosc i mozliwosc rozbudowy rozwiazania" 50% ("Latwosc dodawania nowych typow dokumentow i nowych klas danych bez koniecznosci przebudowy calego systemu").
- Hidden test set: "kompletne sprawy administracyjne przygotowane przez organizatora".

NOT FOUND:
- Exact F1 definition: per field vs per document vs micro/macro; exact match vs normalisation of dates, amounts, NIP, whitespace; list handling; null handling; how wrong document classification counts. None of the sources define it.
- Grader command, timeouts, output encoding.

General regulamin (S7) for Stage I/II: "Etap I - jury danego Konkursu ocenia rozwiazania przeslane przez Uczestnikow za posrednictwem platformy Hacktribe" and top 5 go to Stage II (sec. 5.6a); Stage II = 5 min pitch + max 5 min Q&A (sec. 5.6c). Jury may award nothing below 50% of max points (sec. 5.4). Changes after the deadline are not considered (sec. 5.9).

The deck's "Stage 1 / Stage 2" (preselection / final) and the regulamin's "Etap I / II" are the same two stages in the public text, but the README calls them "Etap 1 - preselekcja" and "Etap 2 - wybor finalny" — consistent.

## Rules verdict

| Item | Verdict | Evidence |
|---|---|---|
| Hosted proprietary LLM via API | UNCLEAR, literal reading NOT ALLOWED | S1 README sec. 5: "wykorzystywac wylacznie komponenty open source (w tym otwarto-zrodlowe modele jezykowe)". A proprietary hosted model is not an open-source component. Parenthesis: "umozliwiac uruchomienie w srodowisku lokalnym (on-premise) bez GPU (LLM po API)". Reading A: open-source model served through a local API (allowed). Reading B: any LLM via API (conflicts with the first sentence). Organizer must confirm. |
| Open-source requirement scope | CONFIRMED that it applies; scope UNCLEAR | "wylacznie komponenty open source" applies to components. Whether our own code needs an OSI licence: not stated. |
| Local run without GPU | CONFIRMED | S1 sec. 5: "uruchomienie w srodowisku lokalnym (on-premise) bez GPU". |
| Python 3.13+ | CONFIRMED | S1 sec. 5: "Python 3.13+". |
| requirements.txt | CONFIRMED | S1 sec. 5: "plik requirements.txt pozwalajacy na szybkie zainstalowanie pozostalych zaleznosci (np. poprzez pip install)". |
| Run method | CONFIRMED | S1 sec. 3: CLI or wrapper (e.g. `start.bat`). |
| AI tools / autonomous agents (general) | UNCLEAR | Not mentioned in S1 README, S7 regulamin, or the task card. The regulamin mentions AI only as a Mentor's expertise (sec. 1.1). |
| Starter code / pre-event code | UNCLEAR | Not forbidden by S7; not addressed by S1. Template folder `szablon-aplikacja` has I/O examples only, no code (S5). |
| IP / author rights | CONFIRMED general rule; task-specific transfer NOT FOUND | S7 sec. 6.1: each participant keeps author rights ("przysluguje mu pelnia autorskich praw majatkowych do swojego wkladu"). S7 sec. 6.3: per-task regulamin "moga przewidywac zasady nabycia przez organizatora ... na zasadach okreslonych w art. 921 par. 3 kodeksu cywilnego (przyrzeczenie publiczne)". The task card has `rules: null`, so no transfer is stated for this task. |
| Partner as promiser of prize | CONFIRMED for the event | S7 sec. 4.9-4.10: the Partner may be the promiser (art. 919 par. 1 kc); the Organizer is one only if the task regulamin says so (sec. 4.11). Task card: initiator URZAD ZAMOWIEN PUBLICZNYCH. |
| Sending a solution = accepting the task rules | CONFIRMED | S7 sec. 4.12. |
| Submission window | CONFIRMED | S7 sec. 5.3 (sic, page item 3): dedicated site available "od godz. 11.00, 21 listopada 2026 r. do godz. 11.00, 22 listopada 2026 r." |
| Per-task criteria published | CONFIRMED that they will be; NOT in the task card | S7 sec. 5.5: criteria "opublikowane wraz z pelnym opisem Zadania, najpozniej w dniu rozpoczecia Wydarzenia o godz. 11:00". Task card: no criteria text. |
| Per-task regulamin | NOT FOUND | Task card `rules: null`, `details: null`, `materials: null`. Re-check at the start. |
| Data license / publishing the training sets in a public repo | UNCLEAR | No LICENSE file (404). The org repo is public and hosts the data, but that does not grant a licence to copy it. Our public repo: do not copy the `dane/` folder without written permission. |
| Personal data in training PDFs | UNCLEAR | Schemas include `pesel` and PESEL-like fields (S2). Sample values look synthetic (domains like `example`, names like "Belmoria"). Not verified against the PDFs. |

## Deliverables

| Deliverable | Value | Source |
|---|---|---|
| Project title | required | S1 sec. 4 |
| GitHub link to a working prototype (upload PDFs, read extraction results) | required | S1 sec. 4 |
| Repo, technical docs, own quality test results | optional | S1 sec. 4 |
| Live demo | Stage II pitch is live (5 + 5 min) | S7 sec. 5.6c; whether a running app is required on the day: UNCLEAR |
| Video | NOT FOUND (not in README or task card) | |
| Slides | NOT FOUND | |
| Repo as ZIP vs link | link to GitHub required (S1 sec. 4) | |
| Cloud deploy allowed | NOT FOUND | |
| External data allowed | NOT FOUND | |
| Format | JSON per input PDF, schema per type; file naming see contract | S1 sec. 3 and S2 |

## Open questions for organizers (UZP booth / Discord)

Answered by this pass (removed from the list): the schema file names and top-level keys; the output tree layout; the Python 3.13 and requirements.txt rule; the GitHub-link submission requirement; the fact that there is no `ground_truth.yaml` in the public data.

Still open:
1. Does "(LLM po API)" allow a hosted proprietary LLM? If not, is an open-source model served through a local API acceptable? Which parts must be open source: our code, the model weights, or only the runtime?
2. Exact F1 definition: per field vs per document; micro vs macro; exact match vs normalisation (dates, amounts, NIP, whitespace); list handling; null handling; how a wrong document type counts.
3. Grader contract: CLI command, time limit per case, whether it reads `output/` as in the README tree, and the exact output file name rule (`odwolanie_nr_1.json` in the README vs `odwolanie.json`/`przelew.json` in the data; `potwierdzenie_przelewu.json` vs `przelew.json`).
4. Which document types and fields are in the hidden test set; can it contain other document types?
5. The full list of 12 `czynnosc_powod_id` codes and their descriptions: where is the published code list?
6. Is `ground_truth.yaml` in the grader? The public data uses JSON.
7. Data licence for the 60 training sets and whether they may be published in our public repo (no LICENSE in the repo).
8. Per-task regulamin: will it transfer author rights to UZP under art. 921 par. 3 kc, and does it cover only the solution or the whole repo?
9. Starter code, pre-event work, and open-source libraries (PDF/OCR parsers, LLM clients): allowed?
10. Deliverables beyond the GitHub link: video (length), slides, live demo requirement on the day, and the exact Hacktribe submission format.
11. Whether AI-coding tools and agents (used by us to build the solution) are allowed under the general rules: the regulamin says nothing; this is a generic question, low priority.

## Points for the coordinator

- Do not design around a hosted proprietary LLM until question 1 is answered. Plan a local open-source model path as the default.
- The F1 definition is needed before the local scorer (`eval/score.py`) is built. Until then, the local scorer should only compare field by field and record the rule used.
- The reference JSON files have `//` comments and are not valid JSON; parse them with a comment-tolerant loader or strip comments before using them as gold data.
- The repo `hacknation-2026` is public and contains the training data; the coordinator's own clone should not be pushed anywhere that copies `dane/`.
