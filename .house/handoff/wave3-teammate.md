# Handoff: wave 3 (T005, T006, T008) for the teammate's Claude session

> **PL (dla człowieka):** W swojej sesji Claude Code (w klonie repo, po `git pull`) wklej: „Przeczytaj `.house/handoff/wave3-teammate.md` i wykonaj zadania zgodnie z instrukcją”. Sesja jest workerem: robi gałęzie `task/T005-recipes-przelew-pelnomocnictwo`, `task/T006-recipe-odwolanie`, `task/T008-packaging-docs`, pushuje je i kończy. Weryfikację (house check), review i merge robi coordinator na maszynie właściciela. Kolejność przy małym limicie: T005 (najważniejsze, pełnomocnictwo 0,66 → 0,90), potem T006, na końcu T008.

Same rules as `.house/handoff/T004-T010-teammate.md` (read sections 1, 2 and 4 there: setup, path translation,
how to finish). You are a **worker**: no `house merge`, no edits to `.house/` on your branches, no pushes to `main`.

## 0. Before you start
- `git pull` on `main`. Start only when `git log main --oneline` shows **`merge T004`** (the engine with its review
  fixes) and `merge T010`. If not there yet, ping the owner; do not branch from `task/T004-recipe-engine`.
- Git hook: `.git/hooks/pre-commit` runs `house/bin/house-githook`, which starts with `#!/usr/bin/env python3`. On
  Windows `python3` may be the Microsoft Store stub. Fix once: Settings → Apps → Advanced app settings → App
  execution aliases → turn off `python3.exe`/`python.exe`, and make sure a real Python 3.12+ is on PATH as
  `python3` (e.g. copy `python.exe` to `python3.exe` in your venv's `Scripts/` and put it first on PATH).
  Do not bypass the hook with `--no-verify`.
- New since your last tasks (read them): `.house/reports/T004.md` incl. "Review fixes",
  `.house/reports/review-T004.md`, `.house/reports/T011.md` (UI restyle, merged), `.house/DECISIONS.md` D-012.

## 0b. Engine status (T004 merged on main, review approved with minor findings)
Fix these on the way when your task touches them (generic, small, unit-tested; full list in
`.house/reports/review-T004.md`):
- `nip:?\s*(?P<v>\d[\d -]{8,12}\d)` in odwolanie.yaml and pelnomocnictwo.yaml has no right boundary and can run into
  the next number on the line ("NIP 1234567890 00-950 Warszawa" → 12 digits): T005 and T006 each fix their own recipe.
- `lookup` folds (lowercases) trigger regexes, so `\W \S \D \B` flip meaning: avoid those escapes in dictionary
  triggers, or fold only literal text (strategies.py) if you need them.
- Labels on lines with word boxes have no word boundaries (a short label can match inside a word); a `[]` path whose
  `all: true` strategy finds nothing falls through to a non-`all` strategy and writes a literal `[]` key.

## 1. Tasks (run in parallel only if your limit allows; otherwise in this order)

### T005 — przelew + pelnomocnictwo recipes to held-out F1 (critical)
- Task file: `.house/tasks/T005-recipes-przelew-pelnomocnictwo.md`. Branch `task/T005-recipes-przelew-pelnomocnictwo`.
- Targets on held-out 41-60: przelew >= 0.95 (already ~1.00), **pelnomocnictwo >= 0.90 (now ~0.66)**. Tune on 01-40 only.
- Known gaps from your T004 report: `podpisujacy` not extracted, `mocodawca.nazwa` only 3 phrasings, no
  multi-mocodawca (consortia in 41-60); przelew case 05 `na_rachunek` across lines, case 26 `numer_transakcji` label.
- Do not edit `recipes/odwolanie.yaml` (T006). Generic engine additions only, small, unit-tested.

### T006 — odwolanie recipe, robust for real appeals
- Task file: `.house/tasks/T006-recipe-odwolanie.md`. Branch `task/T006-recipe-odwolanie`.
- Held-out is already ~0.90 (target 0.85): the goal is robustness for the REAL hidden appeals, not overfitting.
  Gaps: narrative layout in 40-60 ("Zaskarżonym czynnościom…") for `czynnosc_*`; OCR template appeal
  (`uzp-data/szablon-aplikacja/input/case1`) gets `Odwolujacy.nazwa`/`Zamawiajacy.nazwa` wrong; `Odwolujacy.krs`
  misses "KRS nr 0000…"; `pelnomocnik.mail` may take the appellant's own e-mail; "(dalej: Odwołujący)" party
  intros, consortia, distractor "Wykonawca wybrany … po stronie Zamawiającego", TED/BZP variants.
- Do not edit the przelew/pelnomocnictwo recipes (T005).

### T008 — packaging and handover docs
- Task file: `.house/tasks/T008-packaging-docs.md`. Branch `task/T008-packaging-docs`.
- Also list the self-hosted UI fonts (Anybody, Martian Mono, SIL OFL) and the Cold Trace kit from
  `.house/reports/T011.md` in `docs/EXTERNAL_COMPONENTS.md`; README screenshots: use `docs/screenshots/` (they show
  mock evidence; mark them as such until retaken).
- AC-1 needs Docker (`docker compose config -q`); if Docker is not installed on your machine, say so in the report.

## 2. Finish
Per section 4 of the first handoff: all acceptance commands pass (translated paths), commit on the task branch,
`git push -u origin <branch>`, report at `handoff-reports/T00X.md` on the branch (what was built, AC results with
the key output line, per-field held-out table for T005/T006, decisions, open issues). Tell the owner which branches
are pushed. Push T005 as soon as it passes: T009 (case consistency, overall >= 0.90) waits for T005 + T006.
