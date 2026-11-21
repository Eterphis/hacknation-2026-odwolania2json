# Handoff: T004 and T010 for a teammate's Claude session

> **PL (dla człowieka):** Otwórz Claude Code w swoim klonie repo i wklej: „Przeczytaj `.house/handoff/T004-T010-teammate.md` i wykonaj oba zadania zgodnie z instrukcją”. Twoja sesja jest workerem, nie coordinatorem: robi gałęzie `task/T004-recipe-engine` i `task/T010-noisy-heldout`, pushuje je i kończy. Scalanie (house check, review, merge) robi coordinator na maszynie właściciela (yano358). Daj mu znać na czacie, gdy gałęzie są wypchnięte.

You are a **worker**, not the coordinator. Do not run `house merge`, do not edit `.house/` on your branches, do
not push to `main`. Two independent tasks; run them in parallel (two subagents, two worktrees) or one after another.

## 1. Setup (once)

1. Clone or pull the repo: `git@github.com:Eterphis/hacknation-2026-odwolania2json.git`, branch `main`
   (needs T001, T002, T003, T007 merged: check that `odw2json/ingest/`, `eval/score.py` and `web/` exist).
2. Get the UZP data (licence unclear: never commit it): clone
   `https://github.com/Urzad-Zamowien-Publicznych/hacknation-2026` into `<repo>/uzp-data` (gitignored), then set
   the env var `UZP_DATA=<absolute path to that folder>` for every shell (the acceptance helpers read it).
3. Python 3.13 venv, e.g. `<repo>/.venv` (gitignored): `pip install -r requirements.txt`. The OCR stack
   (rapidocr, onnxruntime, opencv-python-headless<5) is large; install once. CPU only, 16 GB RAM is the target.
4. Read, in this order: `AGENTS.md` (if present), `.house/spec.yaml` (`task`, `scoring`, `deliverables`),
   `.house/DECISIONS.md` (D-004..D-010), `odw2json/model.py` (the contract, do not change it),
   `.house/reports/T001.md`, `T002.md`, `T003.md`, `T007.md`, then your task file.

## 2. Path translation

The task files were written for the owner's machine. Translate when you run acceptance commands:

| In the task file | On your machine |
|---|---|
| `C:/Users/jasiu/workspace/.venv/Scripts/python.exe` | your Python 3.13 venv |
| `C:/Users/jasiu/workspace/uzp-data` | `$UZP_DATA` |
| `C:/Users/jasiu/workspace/uzp-data-noisy` | any folder outside the repo, e.g. `<repo>/../uzp-data-noisy` |
| `C:/Users/jasiu/workspace/.house/accept/*.py` | `<repo>/.house/accept/*.py` (read-only for you) |
| `C:/Users/jasiu/workspace/.house` (HOUSE_DIR) | `<repo>/.house`, but read-only: see section 4 |

Do not change any acceptance command or threshold. If one cannot pass for a reason outside your task, say so in
your report instead of working around it.

## 3. The tasks

### T004 — generic recipe engine + classifier with reject
- Task file: `.house/tasks/T004-recipe-engine.md` (objective, design, acceptance AC-1..AC-4, owned files).
- Branch: `git worktree add .worktrees/T004-recipe-engine -b task/T004-recipe-engine` from current `main`.
- The critical path of the whole project: T005/T006 (recipes to F1 targets) and T008 wait for it. Aim to push
  within ~2 hours; push a working version early rather than a perfect one late.
- Must hold: no document class names in `odw2json/engine/` (AC-3 greps for them); recipes validated by
  `recipes/recipe.schema.json`; the TED notice in the template case rejected and the scanned template appeal
  accepted as odwolanie (AC-2 with `--check-class`); a unit test with a fake class defined only in YAML.
- Inputs worth knowing (from T001/T003 reports): letter-spaced headings ("P E Ł N O M O C N I C T W O") need
  whitespace-squashed matching; OCR text sometimes drops spaces ("OstrówMazowiecka"), so label matching should
  be tolerant; `write.py` discovers classes from `schemas/*.json`; components are built in `odw2json/factory.py`
  (switch the defaults there to the T003 ingestor and your engine).
- Marked `review: always`: the coordinator runs an independent review before merging, so keep the diff readable.

### T010 — noisy scanned held-out set
- Task file: `.house/tasks/T010-noisy-heldout.md`.
- Branch: `git worktree add .worktrees/T010-noisy-heldout -b task/T010-noisy-heldout` from current `main`.
- Independent of T004; it measures what OCR does to F1 on degraded copies of held-out cases 41-50 (pypdfium2
  render + Pillow degradations, fixed seed, image-only PDFs, gold copied alongside, all outside the repo).
- The score in AC-3 is informational (no threshold); with the T001 stub extractor it will be near 0 until T004
  lands. Report the number you get and, if T004 is already on `main` or on its branch, also the number with it.

## 4. How to finish

1. Run every acceptance command of your task (translated paths) until all pass; run
   `python -m unittest discover -s tests -t .` on your branch.
2. Commit on your task branch only, then `git push -u origin task/T004-recipe-engine` (and/or
   `task/T010-noisy-heldout`).
3. Write your report as a file **on the branch** at `handoff-reports/T004.md` (or `T010.md`), English, sections:
   what was built, acceptance results (each AC: pass/fail + the key output line), decisions you made, open issues.
   The coordinator moves it into `.house/reports/` and deletes the folder before merging (task branches must not
   carry `.house/` files, the house merge gate refuses them).
4. Tell the owner the branch is pushed. Do not merge, do not open a PR unless asked.
