# Jak dodać nową klasę dokumentu (bez programowania)

Klasa dokumentu to jeden plik YAML w `recipes/` i, opcjonalnie, szkielet wyjściowego JSON. Silnik
(`odw2json/engine/`) nie zna żadnej klasy z nazwy: wszystko, co rozpoznaje i wyciąga, pochodzi z receptur.
Nowy lub zmieniony plik w `recipes/` silnik wczytuje przy następnym dokumencie, bez restartu (w Dockerze
`recipes/` jest zamontowany z hosta).

## Krok po kroku: klasa `faktura`

1. **Szkielet wyniku** `schemas/faktura.json` (kompletny zestaw pól; brakujące zostaną `null`):
   ```json
   {"faktura": {"numer": null, "data_wystawienia": null, "kwota_brutto": null, "nip_sprzedawcy": null}}
   ```
   Zamiast tego można podać w recepturze `output_schema: faktura.json` (ścieżka względem pliku receptury).

2. **Receptura** `recipes/faktura.yaml`. Wzorce to wyrażenia regularne Pythona dopasowywane do tekstu
   **bez polskich znaków i małymi literami** (`faktura vat`, nie `Faktura VAT`). Wartość jest wycinana z oryginału,
   więc zachowuje znaki diakrytyczne.
   ```yaml
   class: faktura
   description: Faktura VAT
   classify:
     min_score: 3          # minimum punktów, poniżej = odrzucenie
     margin: 1             # wymagana przewaga nad drugą klasą
     signals:
       - {pattern: "faktura( vat)?", weight: 3, head: 300, squash: true}   # nagłówek, także "F A K T U R A"
       - {pattern: "sprzedawca", weight: 1}
       - {pattern: "do zaplaty", weight: 1}
     forbidden:
       - "faktura korygujaca"
   fields:
     - path: faktura.numer
       strategies:
         - {use: after_label, labels: ["faktura( vat)? nr", "numer faktury"], value: "[a-z0-9/.-]{3,}"}
     - path: faktura.data_wystawienia
       strategies:
         - {use: after_label, labels: ["data wystawienia"]}
       normalize: date_pl
     - path: faktura.kwota_brutto
       strategies:
         - {use: after_label, labels: ["do zaplaty", "razem brutto"], value: "\\d[\\d .]*,\\d{2}"}
       normalize: amount_pl
     - path: faktura.nip_sprzedawcy
       section: sprzedawca
       strategies:
         - {use: regex, pattern: "nip:?\\s*(?P<v>\\d{10}|\\d{3}-\\d{3}-\\d{2}-\\d{2})(?!\\d)"}
       normalize: digits
       validate: nip
   sections:
     - {name: sprzedawca, start: "^sprzedawca", end: "^nabywca"}
   ```

3. **Sprawdzenie:**
   ```
   python -c "from odw2json.engine import load_recipes; load_recipes('recipes')"   # walidacja, błąd wskazuje plik i ścieżkę JSON
   python -m odw2json --input input --output output                                  # albo start.bat
   ```
   W interfejsie webowym (`start.bat web`) widać klasę, punkty wszystkich klas i dla każdego pola: stronę,
   fragment tekstu, regułę i pewność.

4. **Pomiar jakości** (gdy są wzorcowe JSON-y): `python -m eval.score --pred output --gold <wzorce> --report raport.md`.

## Słowniki
`dictionaries/<nazwa>.yaml`: `entries: [{id, label, triggers: [...]}]`. Strategia `lookup` zwraca wpis, którego
fraza (wyrażenie regularne, spacja = dowolny odstęp) występuje w zakresie **najwcześniej**. Przykład:
`dictionaries/czynnosc_powod.yaml` (kody czynności Zamawiającego 1–11).

## Dokumentacja receptury
Pełna, formalna definicja: `recipes/recipe.schema.json` (walidowana przy wczytaniu).

### Klasyfikacja (`classify`)
| Klucz | Znaczenie |
|---|---|
| `signals` | lista `{pattern, weight, head, squash}`; punkty = suma wag trafionych sygnałów |
| `head: N` | szukaj tylko w pierwszych N znakach (tekst ze ściśniętymi odstępami) |
| `squash: true` | dopasuj po usunięciu wszystkich odstępów (nagłówki rozstrzelone, OCR bez spacji) |
| `required` | wszystkie muszą wystąpić, inaczej klasa ma 0 |
| `forbidden` | dowolne trafienie daje klasie 0 (np. ogłoszenie TED zamiast odwołania) |
| `min_score`, `margin` | próg i przewaga nad drugą klasą; inaczej dokument jest odrzucany |

### Sekcje (`sections`)
`{name, start, end, within, include_start}`. Zakres od pierwszego `start` do najbliższego `end` (domyślnie do końca
dokumentu lub sekcji nadrzędnej `within`). Pole z `section:` jest szukane tylko w tym zakresie. Jeśli sekcji nie ma,
pole jest pomijane.

### Pola (`fields`)
| Klucz | Znaczenie |
|---|---|
| `path` | ścieżka w wyniku z kropkami (`a.b.c`); `lista[].pole` z `all: true` = każda wartość to element listy |
| `strategies` | lista prób w kolejności; wygrywa pierwszy kandydat, który przejdzie normalizację |
| `normalize` | nazwa lub lista normalizatorów (poniżej) |
| `validate` | walidator sumy kontrolnej; niezgodność obniża pewność do 0,5, wartość zostaje |
| `list_of_blocks` + `fields` | lista obiektów: każdy `start` otwiera blok (opcjonalnie `end`, `max`), pola zagnieżdżone liczone w bloku |

Kilka wpisów o tej samej ścieżce wykonuje się po kolei, a późniejszy nadpisuje wcześniejszy, jeśli znajdzie wartość.
Daje to regułę ogólną z precyzyjną regułą na wierzchu.

### Strategie (`use:`)
| Strategia | Klucze | Co robi |
|---|---|---|
| `regex` | `pattern`, `all`, `raw` | dopasowanie wzorca; wartość to grupa `v` (albo grupa 1, albo całe dopasowanie); `raw: true` *(gałąź T013)* = z wielkością liter na oryginalnym tekście |
| `after_label` | `labels`, `value`, `max_lines`, `below` | wartość na prawo od etykiety (do przerwy kolumnowej) albo w linii pod etykietą w tej samej kolumnie (siatki bankowe); `value` = wymagany kształt wartości |
| `between` | `start`, `end` | tekst między dwoma wzorcami (domyślnie do pustej linii), łączy przeniesienia wierszy |
| `lookup` | `dictionary`, `return` | wpis słownika z najwcześniej występującą frazą; zwraca `id` (lub `label`, ...) |
| `const` | `value` | stała |
| `derived` | `if_set`, `value`, `else` | `value`, gdy pole `if_set` jest ustawione, inaczej `else` |
| `segments` | `value`, `exclude`, `not_after`, `raw` | *(gałąź T005, po scaleniu)* wartości w kolumnach linii (np. podpisy pod kropkami); `raw: true` = dopasowanie z wielkością liter |

*(gałąź T005, po scaleniu)* `list_of_blocks` dostaje `min_blocks` (mniej początków bloków niż N = jeden blok na
cały zakres, np. jeden mocodawca zamiast konsorcjum) i `merge` (bloki dołączane po kolei do istniejącej listy, np.
grupy podpisów „W imieniu X:” do mocodawców).

### Normalizatory (`normalize:`)
| Nazwa | Wynik |
|---|---|
| `date_pl` | data ISO z `12.03.2026`, `12 marca 2026`, `2026-03-12`, `12.III.2026` |
| `amount_pl` | liczba z `1 234,56 zł`, `1.234,56`, `17.00` |
| `digits` | same cyfry |
| `int` | liczba całkowita |
| `iban_pl` | 26 cyfr rachunku bez `PL` i spacji |
| `ted` | numer TED jako `NNNNNN-RRRR` (także z `RRRR/S NNN-NNNNNN`) |
| `bzp` | numer BZP bez spacji |
| `strip` | pojedyncze spacje, bez przecinków/dwukropków na brzegach |
| `unquote` | jak `strip` i bez cudzysłowów |
| `upper`, `title` | wielkie litery / każde słowo wielką literą |
| `person` | *(gałąź T013)* imię i nazwisko; zapis WERSALIKAMI zamieniony na „Jan Kowalski-Nowak” |
| `company` | *(gałąź T013)* nazwa firmy z poprawką typowych błędów OCR w formie prawnej („Sp. z 0.o.” → „Sp. z o.o.”) |
| `ocr_digits` | *(gałąź T013)* cyfry identyfikatora po OCR: `o`/`O` → 0, `l`/`I` → 1 |

### Walidatory (`validate:`)
`nip`, `regon` (9 lub 14 cyfr), `pesel`, `krs` (10 cyfr), `iban` (mod 97).

### Własne rozszerzenia (programista)
`register_strategy`, `register_normaliser`, `register_validator` w `odw2json/engine/`. Nowa nazwa staje się
dostępna w YAML. Test `tests/test_docs_recipe_reference.py` pilnuje, żeby każda zarejestrowana nazwa była opisana tutaj.
