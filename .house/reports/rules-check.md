# ODWOLANIA2JSON (HackNation 2026, partner UZP): rules and task contract check

- Agent / model: researcher (haiku), 2026-11-21
- Status: PARTIAL. The full task brief and the per-task regulamin could not be read. Only the general HackNation regulamin and the partner deck were checked.

## Answer first

1. The full ODWOLANIA2JSON brief is not readable from this environment yet. hacknation.pl/zadania timed out (WebFetch and curl, several attempts). hacknation.pl/zadania/odwolania2json returns HTTP 404. Re-check at 11:00 (Sat 21.11) when the brief is published.
2. The challenge repo is not public. github.com/Urzad-Zamowien-Publicznych lists exactly one public repo, `open-mercato-ezd`. It is a fork of open-mercato/open-mercato (MIT, TypeScript, updated 2026-02-13) with no PDF, KIO or ground-truth content. The deck's "Dokumentacja, schematy JSON i zestawy treningowe: github.com/Urzad-Zamowien-Publicznych/" therefore points at an org where the challenge material is not visible yet. Likely reasons: the material is published at 11:00 with the brief, or it sits in a private repo.
3. The general HackNation regulamin says nothing about AI tools, LLM APIs, autonomous agents, open source, or starter code. Those rules must come from the per-task regulamin. Status: UNCLEAR until the task regulamin is published.
4. The general regulamin does allow the partner (as promiser of the prize) to acquire author rights to a solution, via a per-task rule under art. 921 par. 3 kc. Status: CONFIRMED that this is possible in principle. Whether ODWOLANIA2JSON does it: UNCLEAR.

## Sources

| # | Source | Used for | Access |
|---|---|---|---|
| S1 | HackNation general regulamin, PDF: https://hacknation.pl/api/public/dokumenty/28c74284-6390-4665-b8aa-bf4367db79c0/regulamin-hacknation_19.11.pdf | Sections 1-11, rules, IP, jury, timeline | Read via WebFetch (saved locally) and `pdftotext`. Text copy: `C:/Users/jasiu/AppData/Local/Temp/claude/ab89df811496cc91/32e4944d-0964-4318-9ffd-6edb916c9b8f/scratchpad/regulamin/regulamin.txt`. Document says "Regulamin obowiazuje od 28 wrzesnia 2026" (sic, file name says 19.11). |
| S2 | UZP / HackNation 2026 partner deck (text extract): `C:/Users/jasiu/AppData/Local/Temp/claude/ab89df811496cc91/32e4944d-0964-4318-9ffd-6edb916c9b8f/scratchpad/uzp.txt` | Task summary, dataset, scoring, technical rules, contact | Local copy from the earlier intake. Treated as data. |
| S3 | https://github.com/Urzad-Zamowien-Publicznych (org page) and the GitHub REST API for the org | Repo list | Org page read via WebFetch: 1 public repo. API unauthenticated call hit the rate limit. `gh` is not authenticated on this machine. |
| S4 | https://github.com/Urzad-Zamowien-Publicznych/open-mercato-ezd | Checked whether it holds challenge data | WebFetch summary: fork of Open Mercato, MIT, no KIO/PDF/ground-truth content. Not cloned. |
| S5 | https://hacknation.pl/zadania | Full task brief, per-task regulamin | NOT REACHED: WebFetch timeout (x3). `curl` returns 000 for the root hacknation.pl; the regulamin PDF URL returns 200. |
| S6 | WebSearch lead (not a primary source): a gov.pl tender specification (OPZ) for a KIO appeal-review tool that uses PDF-to-JSON extraction, n8n nodes, Karta Odwolania (DOCX/JSON), ground_truth.yaml. Example URLs: https://www.gov.pl/attachment/e42cbf99-4374-42d5-86fa-a4845fb3215a and https://www.gov.pl/attachment/bdb47781-f494-472a-aebb-a68b53e7cc4e | Possibly the source spec behind this challenge. Not confirmed as the same project. Not read in full. |

Search for the exact term "ODWOLANIA2JSON" with hacknation returned no page that names the task.

## Task contract (I/O, schemas, grader)

Confirmed from S2 (partner deck). The full schemas are NOT available yet.

- Input: PDF files of one KIO appeal case. Three document types: odwolanie (appeal), pelnomocnictwo (power of attorney), potwierdzenie przelewu (transfer confirmation). Each PDF describes a different fragment of the same case.
- Steps in the deck: classify the document, extract fields, return JSON that matches the schema for that document type.
- Output: JSON per document, one schema per type. The deck shows an example with top-level keys `"OdwolanieKIO"` (with `"czynnosc_powod_id": 9`, `"miejscowosc": null`) and `"Odwolujacy": [ ... ]`. The example is a preview, not a full schema.
- Reference outputs: `odwolanie.json`, `pelnomocnictwo.json`, `przelew.json`.
- Training data: 39 example sets, 117 PDFs, 3 reference JSON files. Each set also has `ground_truth.yaml`. Format of the YAML: UNCLEAR (no example read).
- Grader I/O (CLI signature, input folder layout, output file names): UNCLEAR. Not in the deck. Expected to be in the brief or the repo.
- Dictionary / ID fields such as `czynnosc_powod_id`: the code list source is UNCLEAR. Not in the deck.
- Data license: UNCLEAR.
- Data download: the deck names the org repo as the source for the data. The org currently exposes no data repo, so data is NOT downloadable from here yet.

## Scoring details

Confirmed from S2:
- Stage 1 (preselection, automated): 100% extraction F1 on a hidden test set. The deck says results are checked on a test set not published before.
- Stage 2 (final): 50% extraction F1, 50% flexibility and extensibility. Flexibility covers new document types and fields without rebuilding the system.
- Premium features listed in the deck: new document classes, configuration without code changes, extraction transparency.

UNCLEAR:
- How F1 is computed (per field, exact match, normalisation, list handling). Not stated in S2. Needs the brief or the grader.
- Whether Stage 1 is also used for the jury's Stage I (the general regulamin says the jury scores Hacktribe submissions in Stage I, top 5 go to Stage II). The deck's Stage 1 / Stage 2 names may not match the regulamin's Stage I / II. Confirm.

Confirmed from S1 (general regulamin):
- Section 5.4: a jury may award no prize if no solution reaches at least 50% of the maximum points.
- Section 5.6: Stage I = Hacktribe submissions scored by the jury (minimum 3 members). Top 5 teams per task go to Stage II.
- Section 5.6c: Stage II = 5 minutes pitch and 5 minutes Q&A.
- Section 5.9: no changes after the deadline are considered.
- Section 5.5: per-task criteria are published with the full brief, at the latest on the start day at 11:00.
- Section 4.6: team size up to 6.
- Section 4.19: prize pool per task 11,000 to 34,000 PLN gross.

## Rules verdict

Items below apply to ODWOLANIA2JSON, using the general regulamin (S1) and the partner deck (S2). The per-task regulamin is NOT read.

| Item | Verdict | Evidence |
|---|---|---|
| allowed_ai (general) | UNCLEAR | S1 contains no AI rule. The only AI mention is in the definition of Mentor (sztuczna inteligencja expert, sec. 1.1b). |
| allowed_ai (task) | UNCLEAR | Deck S2 slide 05: "bez GPU – LLM po API" is listed next to "Lokalne uruchomienie" and "Open source" under "WYMAGANE". The deck implies an LLM accessed through an API is acceptable. It is not a rule text. Need the per-task regulamin. |
| allowed_autonomous_agents | UNCLEAR | Not mentioned in S1 or S2. |
| LLM APIs (hosted) | UNCLEAR, deck suggests allowed | S2: "bez GPU – LLM po API" (listed as a requirement). Conflicts with "Open source" unless the LLM client is open source and the model may be remote. Ask the organizer. |
| Open source constraint | CONFIRMED as a deck requirement, not as a regulamin rule | S2 slide 05: "WYMAGANE: Open source; Lokalne uruchomienie". Whether this counts for the model weights, a hosted LLM, or only the code: UNCLEAR. |
| Local run without GPU | CONFIRMED as a deck requirement | S2 slide 05: "Lokalne uruchomienie", "bez GPU". |
| Python 3.13+ / requirements.txt / CLI or .bat | Stated in the intake brief from the Discord post, NOT verified from a primary source here | Not in S1 or S2. |
| Starter code prepared before the event | UNCLEAR | S1 does not forbid pre-event code. Per-task regulamin needed. |
| IP transfer to partner | UNCLEAR (possible) | S1 sec. 6.1-6.3: each participant keeps author rights to their contribution; the per-task regulamin may transfer author rights to the organiser of the task under art. 921 par. 3 kc (public promise) by agreement. |
| Partner promise of prize (art. 919 par. 1 kc) | CONFIRMED that it can be the partner | S1 sec. 4.9-4.11: the partner may be the promiser; the organiser is one only if the task regulamin says so. |
| Submission method | CONFIRMED for the general event | S1 sec. 5.6a: solutions go through the Hacktribe platform. Dedicated page for submissions opens 21.11 11:00, closes 22.11 11:00 (S1 sec. 4.3). |
| Deadline | CONFIRMED from the event timeline (spec.yaml, from the same regulamin) | Coding ends 22.11 11:00. S1 sec. 4.3. |
| Sending a solution means accepting the task rules | CONFIRMED | S1 sec. 4.12. |
| Registration | Conditioned on a ticket | S1 sec. 3: registration on eventory.cc/event/hacknation-2026. |

## Deliverables

Each value comes from the source named. null = unknown.

| Deliverable | Value | Source |
|---|---|---|
| video_required | null | Not in S1 or S2 |
| video_max_seconds | null | Not in S1 or S2 |
| live_demo | true (Stage II is a live pitch to the jury, 5 + 5 min) | S1 sec. 5.6c. Whether a running app is needed: UNCLEAR |
| slides | null | Not in S1 or S2 |
| repo_submission | null (repo link or ZIP unknown) | Not in S1 or S2 |
| starter_code_allowed | null | Not in S1 or S2 |
| ai_apis_allowed | null (deck suggests LLM API is OK) | S2 slide 05 only |
| external_data_allowed | null | Not in S1 or S2 |
| cloud_deploy_allowed | null | Not in S1 or S2 |
| format | null (deck implies JSON output per document) | S2 slide 02 |

## Open questions for organizers (UZP booth / Discord)

1. Does "LLM po API" mean a hosted API (e.g. a commercial model endpoint) is allowed, given the "Open source" requirement? Which parts must be open source: code only, or model weights too?
2. Is the Stage 1 automatic F1 the same as the regulamin's Stage I jury score, or a separate preselection? Please give the exact F1 definition: per field, per document, exact match, normalisation, list handling, null handling.
3. Which document types and fields are in the hidden test set? Can the test set have document types not in the 3 listed?
4. Grader contract: CLI command, input folder layout, output file names and location, JSON key order and encoding, timeouts, and whether a Docker image or Python version is checked.
5. ground_truth.yaml: format and meaning of each key. Are the dictionary IDs (e.g. czynnosc_powod_id) defined in a published code list? Where is it?
6. Data license for the 39 example sets and the 3 reference JSON schemas. Can we use them in a public repo? Is the repo going to be public?
7. Is the per-task regulamin going to transfer author rights to UZP (art. 921 par. 3 kc)? If yes, is it limited to the solution, or does it cover the whole repo?
8. Starter code and pre-event work: allowed? Pre-existing open-source libraries (e.g. PDF parsers, OCR, LLM clients) allowed?
9. Deliverables: video (length), slides, repo or ZIP, public demo, cloud deploy, the format of the submission on Hacktribe.
10. Is the wider HackNation AI rule (any AI-tool use, agents) identical to the general regulamin, or is there an extra rule for this task?

## Open points for the coordinator

- Re-run this check after 11:00 on 21.11 when hacknation.pl/zadania and the org repo may be readable. Then mark the unknown items above.
- If the repo stays empty, the schemas and grader are unknown. Plan the design around the deck only, and ask the organizers (question list above).
- Do not clone anything from the org. Only `open-mercato-ezd` exists and it is an unrelated fork.
- The gov.pl tender spec (S6) may be the procurement source for this challenge. It was not verified as such, and it is not a rules source.
