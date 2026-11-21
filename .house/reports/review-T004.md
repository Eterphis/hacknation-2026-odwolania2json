# Review T004

- **Reviewer:** claude
- **Note:** Codex not available; same model family as the author (weaker independence)
- **Base:** d9b0dce275b4dd8b68e77db0cf32ec8215fcb28d
- **Head:** 7f445067d028ea43248c8fed87090e00d5b58269
- **Status:** ok
- **Blockers:** 0
- **Majors:** 0
- **Minors:** 8
- **Nits:** 2
- **Verdict:** Approve with minor fixes. Nothing blocking; the most worth fixing are the trigger folding that flips regex escapes and the `[]` path mixing.
- **Date:** 2026-11-21 14:01

Treat the findings as an outside opinion, not necessarily right: fix real bugs, log disagreements.

## Review text

Read the full diff; writing up the findings now.

MINOR odw2json/engine/strategies.py:968 — `lookup` runs `fold()` over the trigger regex before compiling it. `fold` lowercases everything, so escapes flip meaning: `\W`→`\w`, `\S`→`\s`, `\D`→`\d`, `\B`→`\b`, and `\A`/`\Z` break. Both the dictionary docs and the schema say triggers are regexes, so a trigger like `nie\Wodrzucil` silently matches the wrong text. The current `czynnosc_powod.yaml` only uses `\w`, so nothing breaks today. The same `fold(str(trig))` call is at recipes.py:716. Fix: fold only the characters outside escapes, or document that only lowercase escapes are allowed.

MINOR odw2json/engine/engine.py:236-262 — when a field's path contains `[]` and its `all: true` strategy finds nothing, the loop falls through to the next strategy. If that one is not `all`, `_set` writes a literal key `"pelnomocnicy[]"`. The schema allows this combination and the load-time checks don't catch it. Result: the value is silently lost (`fill` drops the unknown key) and the evidence path is wrong. Reject the mix at load time, or treat `[]` paths as list paths in both branches.

MINOR odw2json/engine/strategies.py:912 / 896 — on lines with word boxes, labels are searched with no word boundaries at all. `_LABEL_END` is only added for plain-text lines, and neither branch has a start boundary. Example: the przelew label `suma` also matches inside "podsumowanie" or "sumaryczna". Whatever amount sits to the right of that word then becomes `kwota`. The `value` regex limits the damage but doesn't stop it. Add `(?<!\w)` in front and use the same end boundary on both paths.

MINOR odw2json/engine/engine.py:269-273 — `head` is applied after squashing when `squash: true`. So for squash signals it counts whitespace-free characters, but the schema says it counts characters of the whitespace-collapsed text. For example, `pelnomocnictw` with `head: 300` actually covers about 350+ characters of the collapsed text. Either cut the head first and squash after, or fix the schema description.

MINOR odw2json/engine/recipes.py:722-725 — `signature()` only watches recipe YAML files. If a dictionary file changes, the engine keeps the cached `_dicts` until some recipe file changes. In the long-running web app, dictionary edits are never picked up. That contradicts the "reloaded on file change, no restart" promise. Include the dictionary files in the signature.

MINOR web/app.py:105 — `factory.default_classifier()` only fails up front until the first successful load, because `@cache` keeps the engine after that. If a recipe file breaks later, the request is not rejected early. Instead, `self.recipes` raises inside `classify` for each document, and pipeline.py:29 swallows each one as "error". The batch is then silently dropped instead of showing one clear message. Call `factory.recipe_engine().recipes` there so the reload check runs on every request.

MINOR odw2json/write.py:1209-1213 — `complete()` always reshapes by `schemas/<class>.json` when that file exists, even if the recipe declares a different `output_schema`. So the output loses the recipe-only keys. The evidence paths, though, were computed against the recipe's skeleton, so they no longer match the written JSON. This doesn't affect the three shipped recipes, which have no `output_schema`.

MINOR recipes/odwolanie.yaml:1281 (also :1319, pelnomocnictwo.yaml:1379, cited as lines of the diff output, not of the files) — `nip:?\s*(?P<v>\d[\d -]{8,12}\d)` has no right boundary, so it can run into following digits. Example: "NIP: 1234567890 123456789" is captured as `1234567890123`. The validator then marks it at 0.5 confidence, but the wrong value is still output.

NIT odw2json/engine/engine.py:104-105, 196-199 — `import dataclasses` appears twice. The evidence path rewrite block is also duplicated. It's harmless because `_output_path` gives the same result when run twice, but it is a copy-paste leftover.

NIT odw2json/factory.py:1156 — `recipe_engine` is `@cache`d and reads `ODW2JSON_RECIPES` when it is created. A second `cli.main(["--recipes", other])` in the same process keeps using the first directory.

The engine itself contains no class-specific code. Classification-with-reject, evidence generation and the factory switch look correct. I only read the code and did not run the acceptance commands.

VERDICT: Approve with minor fixes. Nothing blocking; the most worth fixing are the trigger folding that flips regex escapes and the `[]` path mixing.
