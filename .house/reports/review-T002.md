# Review T002

- **Reviewer:** claude
- **Note:** Codex not available; same model family as the author (weaker independence)
- **Base:** d4772533130c51c6536c08677dd09f4418e4239a
- **Head:** 7e412b01d3efd8abac800796cf07409e53a13271
- **Status:** ok
- **Blockers:** 0
- **Majors:** 0
- **Minors:** 2
- **Nits:** 4
- **Verdict:** Approve with minor fixes. The scoring logic looks correct, but the scorer should fail loudly instead of printing 0.0 when a path is wrong or no cases are selected.
- **Date:** 2026-11-21 12:15

Treat the findings as an outside opinion, not necessarily right: fix real bugs, log disagreements.

## Review text

I'm writing up the review now. I couldn't run anything: the tests, the AC commands and my sanity checks were all denied because this session has no way to approve commands. Everything below comes from reading the diff, plus Grep checks on the gold data. Those checks found 180 gold files (60 cases × 3) with consistent top-level keys. None of the odwolanie-only keys appear in `pelnomocnictwo.json` or `przelew.json`, so detecting the type from top-level keys is safe on this data.

MINOR eval/score.py:349 — If `--gold` doesn't exist, gold is treated as empty. If `--pred` doesn't exist, every case counts as FN. If `--cases` matches no gold folder, or is a reversed range like `60-41` (`parse_cases` at line 283 then returns an empty set), the result is the same. In every one of these cases the scorer prints `score: 0.0000`, exits with 0 and gives no warning, so a typo in a path or a range looks like a real zero. It should error out or warn when the gold folder is missing, the pred folder is missing, or no cases were scored.
MINOR eval/score.py:323 — With `--types`, pred documents of unknown type (filed under `"unknown"` at line 321) are always skipped. So `--types odwolanie` never charges for a broken or unrecognised extra document, and the filtered score comes out higher than the matching slice of the full score. The docstring's "applied to gold and pred alike" hides this. Either document it or count unknown pred documents in the filtered score.
NIT eval/score.py:56 — The code also treats `Zamawiajacy` and `ZamowieniePubliczne` as odwolanie keys, but the docstring (line 12) and README (line 12) only list `OdwolanieKIO`/`Odwolujacy`. Since the docstring is called the reference definition, it should match the code.
NIT eval/score.py:425 — `write_report` runs before the `normalized:` and `score:` lines are printed. If the report path can't be written (for example its folder is missing), the run ends in a traceback and the `score:` last-line contract breaks. Print the score lines first, or wrap the report write.
NIT eval/score.py:102 — The digit-only rule in normalized mode also treats dates as equal to plain digit strings (`2026-03-20` == `20260320`). This only affects the diagnostic normalized number, but it is looser than the docstring suggests.
NIT eval/README.md:22 — I couldn't check the sanity figure (`case 01 without przelew = 0.8966`) because I wasn't able to run AC-4. Nothing in the diff says which cases are held out (41-60 is implied only by AC-3).

On the core logic, I found no problems:
- **Pairing:** the Hungarian implementation is the standard one. Cost = −TP·1e6 + (FP+FN) is correct for maximising agreement, padding with dummy rows/columns is handled, and pairs with zero TP give the same totals as leaving both sides unmatched.
- **Counting:** TP/FP/FN follow the spec, and per-field paths are the same whether a document is matched or unmatched.
- **Exact equality:** it is type-aware, and `True != 1`.
- **Data handling:** no gold data is copied into the repo, the tests use inline fixtures, and nothing leaks between the dev and held-out cases.

VERDICT: Approve with minor fixes. The scoring logic looks correct, but the scorer should fail loudly instead of printing 0.0 when a path is wrong or no cases are selected.
