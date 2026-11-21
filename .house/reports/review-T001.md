# Review T001

- **Reviewer:** claude
- **Note:** Codex not available; same model family as the author (weaker independence)
- **Base:** d4772533130c51c6536c08677dd09f4418e4239a
- **Head:** 49880f44b2ac39e2c3193b629062d64a25cefabf
- **Status:** ok
- **Blockers:** 0
- **Majors:** 0
- **Minors:** 4
- **Nits:** 3
- **Verdict:** Mergeable. The skeleton, writer and CLI behave as specified. The main follow-up is removing old output files for documents that are now rejected; the classifier issues belong to the stub that T004 replaces.
- **Date:** 2026-11-21 12:22

Treat the findings as an outside opinion, not necessarily right: fix real bugs, log disagreements.

## Review text

MINOR odw2json/pipeline.py:58 — Old output files are never removed. Say `x.pdf` was accepted in an earlier run and is rejected now, or now fails to process. Its old `<output>/<case>/x.json` stays in place. That breaks the rule "nothing is written for rejected documents" whenever the same output folder is used twice, which will happen as soon as the T004 classifier replaces the stub. The narrow fix is to delete `<output>/<case>/<stem>.json` when a document comes back with no output.

MINOR odw2json/pipeline.py:26 — Every `ImportError` is re-raised, which stops the whole batch. The comment says this is meant for a broken environment. But `pdfplumber` is already imported when the ingestor is created, so an `ImportError` here can only come from a lazy import inside pdfminer that one particular PDF triggers, such as an encryption backend for an encrypted file. One such document kills the run and goes against "one broken PDF must never kill the batch". Consider failing loudly only when the error happens on the first document, or catching it and counting it as a failure. `cli.py:21` already returns exit code 1 when every PDF fails.

MINOR odw2json/stubs.py:43 — The strongest signal for `odwolanie` is the regex `^(prezes )?krajow(a|ej) izb`. It does not match the common heading "Do Prezesa Krajowej Izby Odwoławczej", because neither `prezesa` nor a leading `do` is allowed. Such documents then depend on the exact text `odwołujący:` with a colon (+2). Without the colon, or with a space before it, they score 1.0 and are rejected. It's a stub, but AC-2 runs it on 60 real cases, and a wrong rejection means a missing JSON file. Widening the regex to something like `(do )?(prezes\w* )?krajow` fixes it.

MINOR odw2json/stubs.py:47 — An appeal (`odwolanie`) can be misclassified as a transfer (`przelew`). Appeals usually mention the fee "na rachunek" (+1) and "kwota" (+0.5). If the word "przelew" also appears in the first 600 characters (for example "uiszczono wpis przelewem"), the transfer score reaches 4.5 and beats a typical appeal score of 3.0. In that case the tie-break order never applies.

NIT odw2json/pipeline.py:28 — The output name is `pdf.stem + ".json"`, so `a.pdf` and `a.PDF` in the same case write to the same file. This can only happen on case-sensitive filesystems.

NIT odw2json/pipeline.py:56 — Hidden folders such as `.ipynb_checkpoints` or `.DS_Store` folders under the input are processed as cases. Skipping names that start with a dot would be safer.

NIT tests/test_stubs.py:55 — The training data path `C:/Users/jasiu/workspace/uzp-data/dane` is hardcoded and machine-specific. The test is silently skipped everywhere else, and the stub classifier is checked against the same data its keywords were tuned on, so this test proves little about how it handles unseen documents.

The schema key `przez-pelnomocnika` in `schemas/odwolanie.json:15` uses a hyphen while every other key uses underscores. I couldn't check it against the UZP reference schema because the repo-wide search was blocked: the session has no way to approve permission prompts. Please confirm the hyphen matches the reference exactly, since AC-2's shape check depends on it. I also didn't run the acceptance commands, because this review was limited to git and reading files.

VERDICT: Mergeable. The skeleton, writer and CLI behave as specified. The main follow-up is removing old output files for documents that are now rejected; the classifier issues belong to the stub that T004 replaces.
