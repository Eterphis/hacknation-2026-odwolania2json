# Review T004

- **Reviewer:** claude
- **Note:** Codex not available; same model family as the author (weaker independence)
- **Base:** ec89a858ca760cddc21045a2d075b82f9d31e16d
- **Head:** 79c15f422455ec2248301349b846173578b892b7
- **Status:** ok
- **Blockers:** 0
- **Majors:** 0
- **Minors:** 5
- **Nits:** 4
- **Verdict:** Approve with minor fixes. The engine is generic and correct for the shipped recipes. The real risks are latent: the trigger fold changing regex escapes, the label rewrite not being validated at startup, and stale dictionaries after a reload.
- **Date:** 2026-11-21 13:55

Treat the findings as an outside opinion, not necessarily right: fix real bugs, log disagreements.

## Review text

MINOR odw2json/engine/strategies.py:237 — The `lookup` strategy and `recipes.py:136` apply `fold()` to the trigger, and dictionary triggers are regexes. `fold` lowercases everything, so `\W`, `\S` and `\D` in a trigger silently become `\w`, `\s` and `\d`, which match the opposite characters. The current dictionary only uses `\w`, so nothing breaks today. The next person who writes `\S+` or `\D` gets wrong matches with no error.

MINOR odw2json/engine/strategies.py:58 — With `loose_spaces`, every unescaped space becomes `\s*`, including spaces inside a character class (`[a b]` → `[a\s*b]`) and spaces before a quantifier (`x {2}` → `x\s*{2}`, which is a `re.error`, or `x ?` → `x\s*?`). `_check_regexes` (`recipes.py:83`) only compiles the label as written, not the rewritten form that actually runs, nor the `_LABEL_END`-suffixed variant. A bad label therefore passes the startup check and then fails on every document. Each failure is caught per document, so whole documents quietly come out as "error".

MINOR odw2json/engine/engine.py:32 — Recipes reload when a file changes, but the signature only covers `recipes/`. Edits to `dictionaries/*.yaml` are never picked up until a recipe file changes. Also, `classify` and `extract` each read `self.recipes` separately. A reload between the two calls, such as a class being renamed or a YAML being saved half-written, makes `extract` fail for a document that was just classified.

MINOR odw2json/write.py:50 — `complete()` reshapes data to `schemas/<class>.json` whenever that file exists. The pipeline calls it after `extract`. If a recipe sets an `output_schema` that differs from the default and the default file also exists, the engine's completed output is reshaped a second time, and fields that only exist in `output_schema` are dropped. The engine and the writer should use the same skeleton.

MINOR recipes/odwolanie.yaml:70 — The `pelnomocnik.imie_nazwisko` pattern takes the first two words after `reprezentowan\w* przez`. Text like "reprezentowana przez Prezesa Zarządu …" therefore produces "Prezesa Zarządu" as the proxy name. The derived `przez-pelnomocnika` then becomes 1, although a board acting for its own company is not a proxy. `\s+` can also join a name across a line break. This could hurt accuracy before T006 lands.

NIT odw2json/engine/engine.py:96 — The evidence-path remap (`_output_path`) runs twice. The repeat is harmless because the function is idempotent, but it is clearly a merge or copy-paste leftover.

NIT odw2json/engine/engine.py:4 — `import dataclasses` appears twice.

NIT odw2json/engine/engine.py:172 — For `squash` signals, `head` counts characters of the text with all whitespace removed. The schema describes it as the "whitespace-collapsed text". So `head: 300` covers noticeably more of the document for squash signals than for ordinary ones.

NIT odw2json/engine/engine.py:252 — `_normalise` silently skips every normaliser except `int` when the value is not a string (lookup, const, derived). A recipe that asks for `strip` on a lookup label gets no warning; this is fine, but it isn't documented.

I only read the diff; as instructed, I didn't run the tests or the acceptance checks. A `git grep` with the AC-3 pattern finds no class-specific words in `odw2json/engine`. The checksums for NIP, REGON, PESEL and IBAN are correct. Classification rejects a document when the best score is below `min_score` or its lead over the runner-up is below `margin`. A failure on one document stays isolated by the pipeline's existing per-document `try`. The `make_noisy` change fixes the PDF creation and modification dates, so its output is the same on every run. I found nothing that leaks training data into test data, and nothing that affects scoring.

VERDICT: Approve with minor fixes. The engine is generic and correct for the shipped recipes. The real risks are latent: the trigger fold changing regex escapes, the label rewrite not being validated at startup, and stale dictionaries after a reload.
