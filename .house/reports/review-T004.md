# Review T004

- **Reviewer:** claude
- **Note:** Codex not available; same model family as the author (weaker independence)
- **Base:** 5d2fdd4745763449334423a657ce37739fa6acab
- **Head:** 0d6a3e64e6285586cfd1e93b80d76633ab1b1d72
- **Status:** ok
- **Blockers:** 0
- **Majors:** 2
- **Minors:** 8
- **Nits:** 3
- **Verdict:** The engine design is sound and free of class-specific code. The main fixes before merge: let recipe `output_schema` survive the pipeline's `complete()`, and fail loudly at startup on a broken recipe instead of silently erroring every document. The rest are minor robustness issues in the engine and recipes.
- **Date:** 2026-11-21 13:12

Treat the findings as an outside opinion, not necessarily right: fix real bugs, log disagreements.

## Review text

I reviewed the diff by reading the code only. Running Python (tests, AC-2, AC-4) was blocked by the permission settings, so none of the acceptance checks were run. AC-3 looks clean from reading: no class-specific names appear in `odw2json/engine/`.

MAJOR odw2json/engine/recipes.py:40 — A recipe's `output_schema` only takes effect inside `RecipeEngine.extract`. Afterwards `pipeline._process_pdf` calls `complete(ext.data, cls.doc_class)`, which loads `schemas/<class>.json` and raises `KeyError` if that file is missing. That error is caught as a document error, so the file gets no output. This breaks the goal that a recipe plus its own skeleton makes a working class. Either the engine's completed result should be final, or `complete` should be skipped or made recipe-aware.
MAJOR odw2json/engine/engine.py:45 — If any recipe is invalid (bad YAML, schema violation, bad regex, duplicate class), `RecipeError` is raised from the `recipes` property on every `classify` call. The pipeline catches it per document, so the whole batch comes out as "error" with no output files and only a logged traceback. Nothing fails loudly at startup. Load once eagerly in the factory or CLI and exit non-zero.
MINOR odw2json/engine/engine.py:151 — Evidence paths don't match the output JSON. `Odwolujacy.nip`, `Zamawiajacy.nazwa` and `mocodawca.data.krs` are lists in the schema, and `_fill` wraps them as `[0]`. The evidence keeps the dotted path, while the model contract shows `Odwolujacy[0].nip`. Anything that joins evidence to output by path, such as UI highlighting or confidence per field, will miss these fields.
MINOR odw2json/engine/strategies.py:232 — Dictionary triggers are documented as plain phrases but are compiled as regexes. A future trigger like "(SWZ)" or "art. 226" would silently mis-match. Use `re.escape` first, then apply the loose-space rule.
MINOR odw2json/engine/engine.py:160 — The squash rewrite removes `\s` tokens and literal spaces from the pattern. It mangles `[^\s]` into `[^]`, which fails to compile, and turns `\s{1,3}` into a dangling `{1,3}`. `_check_regexes` only compiles the unsquashed pattern, so the error surfaces at classify time on every document.
MINOR odw2json/engine/recipes.py:75 — `_check_regexes` skips the after_label `value` patterns, and dictionary triggers are never compiled at load time. A typo there passes load and then fails extraction for every document of that class, so whole documents are lost rather than one field.
MINOR odw2json/engine/strategies.py:180 — On pages without word boxes, a label that matches mid-word leaves the rest of that word as the value. For example, `nr ref\.?` on "Nr referencyjny: ABC123" gives `rest = "erencyjny: ABC123"`, and the `numer_transakcji` value regex then matches "erencyjny". Labels need a trailing `\b`, or the match should be extended to the end of the word.
MINOR odw2json/engine/strategies.py:181 — In plain-text mode, `_continue` reads past `scope.end`, and the "below" line is picked from the whole scope list without checking that it isn't another label. With no `value` pattern, the next label line becomes the value.
MINOR odw2json/engine/normalise.py:56 — `date_pl` doesn't parse Roman-numeral months written with dots ("12.III.2024"), which is common in Polish documents. `\s*` doesn't consume ".", even though `_ROMAN` exists for exactly this case.
MINOR odw2json/engine/engine.py:203 — `_set` replaces an empty intermediate list with a dict (`nxt = nxt[0] if nxt else None` → `obj[p] = {}`). A later dotted field then turns a list-of-blocks result with zero blocks into an object.
NIT odw2json/engine/engine.py:40 — The dictionary cache is only cleared when a recipe file changes, so edits to `dictionaries/*.yaml` are ignored until restart. This is inconsistent with the documented hot reload.
NIT odw2json/engine/engine.py:162 — `head` is applied after squashing on squash signals. The same `head: 300` therefore covers much more text than on a normal signal, which differs from the schema text ("first N chars of the whitespace-collapsed text").
NIT recipes/odwolanie.yaml:57 — `Odwolujacy.krs` uses `krs:?\s*\d{10}` and misses "KRS nr 0000…", while `pelnomocnictwo.yaml` already uses the more tolerant `krs\D{0,30}?`. `Odwolujacy.pelnomocnik.mail` takes the first email in the section, which may be the appellant's own address, not their attorney's.

VERDICT: The engine design is sound and free of class-specific code. The main fixes before merge: let recipe `output_schema` survive the pipeline's `complete()`, and fail loudly at startup on a broken recipe instead of silently erroring every document. The rest are minor robustness issues in the engine and recipes.
