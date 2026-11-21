# Review T004

- **Reviewer:** claude
- **Note:** Codex not available; same model family as the author (weaker independence)
- **Base:** 5d2fdd4745763449334423a657ce37739fa6acab
- **Head:** d1514c887fb8686402fb50f37f443cc549dec231
- **Status:** ok
- **Blockers:** 0
- **Majors:** 0
- **Minors:** 5
- **Nits:** 4
- **Verdict:** Approve with minor fixes. The engine is generic (AC-3 passes), and the classify-with-reject, evidence paths and skeleton completion all hold up. The issues are about reload and robustness, not wrong output on today's recipes.
- **Date:** 2026-11-21 13:28

Treat the findings as an outside opinion, not necessarily right: fix real bugs, log disagreements.

## Review text

I found no blockers. There are three MINOR robustness issues worth fixing before T005/T006 build on this, plus a few nits. I could not run AC-1, AC-2 or AC-4, because this review was limited to git and reading files. AC-3 passes: the forbidden class words do not appear anywhere in `odw2json/engine`.

MINOR web/app.py:90 — The "eager recipe load" check here does nothing after the first request. `factory.default_classifier()` returns the cached engine without reading `.recipes`, so it never re-validates. If someone edits a recipe into a broken state while the server runs, the hot-reload `recipes` property raises `RecipeError` inside `classify` for every document. The pipeline catches that, so each document gets its own `error` result: exactly the "error per document" this check was meant to prevent. Calling `factory.recipe_engine().recipes` here would fix it.

MINOR odw2json/engine/engine.py:134 — Hot reload only watches `recipes/*.y*ml`. The `_dicts` cache is cleared only when a recipe file changes, so edits to `dictionaries/*.yaml` or to an `output_schema` skeleton are ignored until a recipe changes or the process restarts. This contradicts the "no restart" promise in the comment.

MINOR odw2json/engine/strategies.py:968 — `fold()` is applied to dictionary triggers, and the schema documents triggers as regexes. `fold` lowercases them, which turns `\W`, `\S`, `\D` and `\B` into their opposites (`\w`, `\s`, `\d`, `\b`). Today's dictionary only uses `\w`, so nothing breaks yet. The same happens at load time in recipes.py:716, so the load-time check won't catch it either. Folding only the literal text, or leaving escape sequences alone, would avoid this.

MINOR recipes/odwolanie.yaml:1281 — The NIP pattern `\d[\d -]{8,12}\d` can run on into the next number on the same line. For example, "NIP 1234567890 00-950 Warszawa" yields `123456789000`. That value is kept at confidence 0.5 instead of being cut at 10 digits. The same pattern appears at :1319 and pelnomocnictwo.yaml:1379.

MINOR odw2json/engine/strategies.py:883 — On plain-text pages, `_continue` reads continuation lines from `t.lines[i+1:]` without the field's scope. With `max_lines > 1`, a value can pull in lines from past the end of its section.

NIT odw2json/engine/strategies.py:789 — With `loose_spaces`, every unescaped space becomes `\s*`, including spaces inside character classes. A label like `[a-z ]` turns into `[a-z\s*]`. The schema says "a space matches optional whitespace" without mentioning this.

NIT odw2json/engine/engine.py:196 — The block that rewrites evidence paths with `_output_path` appears twice. It's harmless because the function is idempotent, but it's a copy-paste leftover.

NIT odw2json/engine/engine.py:104 — `import dataclasses` appears twice.

NIT odw2json/engine/engine.py:272 — For `squash` signals, `head` counts characters of the whitespace-stripped text, so `head: 300` covers more of the document than the same value on a normal signal. The schema describes `head` as counting the "whitespace-collapsed text".

VERDICT: Approve with minor fixes. The engine is generic (AC-3 passes), and the classify-with-reject, evidence paths and skeleton completion all hold up. The issues are about reload and robustness, not wrong output on today's recipes.
