# Misses on scans and held-out 41-60 (profile `ocr`, main 8bdac0c)

Run: `python -m odw2json --workers 4` on the 30 UZP scans (`dane/skany`, prepared with `eval.prep_skany`) and on
cases 41-60. Then a field-by-field diff against gold with the `eval/score.py` pairing (`.acc/misses/list_misses.py`).
Exact F1: scans **0.9639**, 41-60 **0.9986**. Raw lists: [skany.json](../../.acc/misses/skany.json),
[heldout.json](../../.acc/misses/heldout.json). Every Qwen prompt, schema and answer, in full:
[qwen_prompts.md](../../.acc/misses/qwen_prompts.md) (trace: [llm_trace.json](../../.acc/misses/llm_trace.json)).
The `.acc/` files are local only (gitignored).

**Totals:** 18 wrong leaves on scans in 8 documents and 2 on 41-60. The `llm` profile fixes 4 of the 20. Most of the
rest can be fixed with recipe rules, without a model.

## All misses

| # | Document (PDF / our JSON / gold) | Field | Ours | Gold | Cause | `llm` |
|---|---|---|---|---|---|---|
| 1-4 | odwołanie skan 0005: [pdf](../../uzp-data/dane/skany/odwolania/0005/0005.pdf) / [ours](../../.acc/misses/skany/output/odw_0005/0005.json) / [gold](../../uzp-data/dane/skany/odwolania/0005/0005.json) | czynnosc_powod_id, czynnosc_opis, numer_bzp, numer_postepowania | null | 11, "Opis przedmiotu zamówienia (OPZ)", 2026/BZP00879135/03, ZP/12/2026 | **OCR lost the lines.** The values are printed (page 1: [image](../../.acc/misses/odw0005_p1.png)), but text bleeding through from the back page garbles exactly those lines: OCR gives `nr referencyjny: Z e ien` and `1a n z tf y:` | asked about czynność and numer; answered null (the text does not contain them). BZP not asked (`when: bzp` does not match) |
| 5 | pełnomocnictwo skan 0002: [pdf](../../uzp-data/dane/skany/pelnomocnictwa/0002/0002.pdf) / [ours](../../.acc/misses/skany/output/pel_0002/0002.json) / [gold](../../uzp-data/dane/skany/pelnomocnictwa/0002/0002.json) | pelnomocnicy[] (extra) | "MATEUSZ WIERZBICKI" | (only "Mateusz Wierzbicki") | the same person in capitals and in mixed case, not deduplicated | not asked |
| 6 | pełnomocnictwo skan 0004: [pdf](../../uzp-data/dane/skany/pelnomocnictwa/0004/0004.pdf) / [ours](../../.acc/misses/skany/output/pel_0004/0004.json) / [gold](../../uzp-data/dane/skany/pelnomocnictwa/0004/0004.json) | mocodawca.podpisujacy[] | missing | "Halina Baran" | OCR glued the words: `HalinaBaran - Prezes Zarządu` | not asked |
| 7 | (same document) | pelnomocnicy.pesel | null | 69102340858 | recipe misses `PESEL: …` inside the parenthesis after the name | **fixed** |
| 8 | pełnomocnictwo skan 0007: [pdf](../../uzp-data/dane/skany/pelnomocnictwa/0007/0007.pdf) / [ours](../../.acc/misses/skany/output/pel_0007/0007.json) / [gold](../../uzp-data/dane/skany/pelnomocnictwa/0007/0007.json) | mocodawca.podpisujacy[] | missing | "Łukasz Sosnowski" | consortium: the second member's signatory is not read (OCR reads `Lukasz`, without the Ł) | not asked for podpisujacy; the model wrongly listed both board members as pełnomocnicy (not accepted) |
| 9 | (same document) | pelnomocnicy.pesel | null | 90082629103 | recipe misses the PESEL after `nr wpisu …,` | **fixed** |
| 10 | pełnomocnictwo skan 0008: [pdf](../../uzp-data/dane/skany/pelnomocnictwa/0008/0008.pdf) / [ours](../../.acc/misses/skany/output/pel_0008/0008.json) / [gold](../../uzp-data/dane/skany/pelnomocnictwa/0008/0008.json) | mocodawca.podpisujacy[] (extra) | "Szymon Zawadżki" | (only "Szymon Zawadzki") | OCR reads `Zawadżki` in the body and `Zawadzki` at the signature: 2 people instead of 1 | not asked |
| 11-12 | pełnomocnictwo skan 0009: [pdf](../../uzp-data/dane/skany/pelnomocnictwa/0009/0009.pdf) / [ours](../../.acc/misses/skany/output/pel_0009/0009.json) / [gold](../../uzp-data/dane/skany/pelnomocnictwa/0009/0009.json) | pelnomocnicy[0,1].pesel | null | 68091502944, 82070226436 | `(pracownik Mocodawcy, PESEL: …)` not read | **fixed (both)** |
| 13-15 | pełnomocnictwo skan 0010: [pdf](../../uzp-data/dane/skany/pelnomocnictwa/0010/0010.pdf) / [ours](../../.acc/misses/skany/output/pel_0010/0010.json) / [gold](../../uzp-data/dane/skany/pelnomocnictwa/0010/0010.json) | mocodawca.data: typ, nazwa, imie_nazwisko | osoba_prawna, "1. Andrzej Wróbel – radca prawny…", null | osoba_fizyczna, null, "Paweł Brzozowski" | the principal is a sole trader (`Brzozowski Asterion Usługi Techniczne…`); the recipe treats him as a company and takes the next line (the attorney) as the name | no `llm:` block for mocodawca |
| 16 | przelew skan 0001: [pdf](../../uzp-data/dane/skany/potwierdzenia/0001/0001.pdf) / [ours](../../.acc/misses/skany/output/prz_0001/0001.json) / [gold](../../uzp-data/dane/skany/potwierdzenia/0001/0001.json) | z_rachunku | 6221… | PL6221… | **gold is inconsistent**: scans keep the printed `PL`, synthetic gold drops it (e.g. przyklad_03 prints `PL3920…`, gold `3920…`). We follow the synthetic set | n/a |
| 17 | przelew skan 0006: [pdf](../../uzp-data/dane/skany/potwierdzenia/0006/0006.pdf) / [ours](../../.acc/misses/skany/output/prz_0006/0006.json) / [gold](../../uzp-data/dane/skany/potwierdzenia/0006/0006.json) | z_rachunku | 7521… | PL7521… | as above | n/a |
| 18 | przelew skan 0008: [pdf](../../uzp-data/dane/skany/potwierdzenia/0008/0008.pdf) / [ours](../../.acc/misses/skany/output/prz_0008/0008.json) / [gold](../../uzp-data/dane/skany/potwierdzenia/0008/0008.json) | tytul | "opiata skarbowa od peinomocnictwa dla adw Rafał Maknowsiu…" | "opłata skarbowa od pełnomocnictwa dla adw. Rafał Malinowski…" | OCR misreads (`ł`→`i`, `Malinowski`→`Maknowsiu`) | not asked (value confident); it would not help anyway, since the quote must come from the same OCR text |
| 19 | 41-60 przyklad_43: [pdf](../../uzp-data/dane/przyklad_43/pelnomocnictwo.pdf) / [ours](../../.acc/misses/heldout/output/przyklad_43/pelnomocnictwo.json) / [gold](../../uzp-data/dane/przyklad_43/pelnomocnictwo.json) | pelnomocnicy.pesel | null | 85071204278 | `PESEL 85071204278` without a colon, after `r. pr.` | the model found the PESEL but answered the first name only (`"Katarzyna"`), so its item did not match our `Katarzyna Michalak` and was dropped |
| 20 | 41-60 przyklad_52: [pdf](../../uzp-data/dane/przyklad_52/odwolanie.pdf) / [ours](../../.acc/misses/heldout/output/przyklad_52/odwolanie.json) / [gold](../../uzp-data/dane/przyklad_52/odwolanie.json) | Odwolujacy.krs | 9992630248 | null | the Odwołujący section does not stop at `Wykonawca wybrany (potencjalny uczestnik…)`, so we took the KRS of the next company (Cervin Konstrukcje sp.j.) | not asked |

## What the model is asked

One call per document, only for fields the recipe left empty (or read with low confidence) and that opt in with `llm:`
in the recipe. Context: the first pages of OCR text (2 pages, max 4500 characters for odwołanie; 1 page, 3500
characters for pełnomocnictwo and przelew). System prompt (verbatim):

```
You read the text of a Polish legal or banking document (it may come from OCR and contain errors). Transcribe values
exactly as they are printed: do not translate, reformat, correct or guess. For every field return `value` and
`quote`, where `quote` is a short verbatim passage of the text that contains the value. When the text does not state
the value, return null (or an empty list). /no_think
```

User message for pełnomocnictwo skan 0004 (call 2 in [qwen_prompts.md](../../.acc/misses/qwen_prompts.md)), with the
document text shortened:

```
Fields:
- pelnomocnicy: a list. The persons who are granted the power of attorney (pelnomocnicy), not the principal and not
  the signatories.  Each item has: imie_nazwisko = Full name without professional titles (no adw., radca prawny).;
  pesel = The PESEL number (11 digits) printed for this person, or null.

Document text:
"""
<OCR text of page 1, 1382 characters>
"""
Answer with JSON only.
```

Answer: `{"pelnomocnicy": [{"imie_nazwisko": {"value": "Krzysztof Jodłowski", "quote": "Krzysztof Jodłowski (radca
prawny, nr wpisu PO-4973, PESEL: 69102340858}"}, "pesel": {"value": "69102340858", "quote": "PESEL: 69102340858"}}]}`.
The quote is found in the page text, so the value is accepted with evidence `llm:Qwen3-1.7B-Q8_0`.

Calls: 5 (odw 0005, pel 0004, 0007, 0009, przyklad_43), 48-75 s each on this laptop's CPU. Accepted: 4 PESELs.

## Recommendations, cheapest first

1. **PESEL rule in `recipes/pelnomocnictwo.yaml`** (misses 7, 9, 11, 12, 19). Read `PESEL:? <11 digits>` near each
   pełnomocnik name, with checksum validation. This makes the recipe recover what the model does now, plus przyklad_43,
   and it is deterministic and instant. Scan F1 rises to about the `llm` level without a model.
2. **End the Odwołujący section at `wykonawca wybrany | uczestnik | przystępując`** in `recipes/odwolanie.yaml`
   (miss 20).
3. **Deduplicate people** in pełnomocnicy and podpisujacy by folded name (casefold, no diacritics, edit distance ≤ 1),
   keeping the mixed-case or signature form (misses 5, 10). Split glued `NameSurname` tokens before matching (miss 6).
4. **OCR preprocessing for show-through** (misses 1-4, 18). Binarise or raise contrast on the page image before
   RapidOCR, or re-OCR lines with low recognition confidence at a higher scale. This is the only fix for these misses;
   no reader (rules or LLM) can recover text that OCR drops. Worth a short experiment on the 30 scans with the OCR cache
   cleared (`--cold`).
5. **Sole-trader principal** (misses 13-15). Rule: no KRS, a CEIDG wording or a surname at the start of the firm name
   that matches the signatory, then `typ: osoba_fizyczna`, `imie_nazwisko` = the signatory, `nazwa` = null. Riskier;
   do it after 1-3.
6. **`PL` prefix** (16, 17): leave as is. The two gold sets disagree, and the synthetic convention (no `PL`) covers more
   documents. This is worth a question to the mentors.
7. **`llm` profile**: keep it opt-in. After fix 1 its remaining gain on these sets is about zero. Its group prompt
   also needs `imie_nazwisko` matched by surname, not by the exact string (miss 19).
