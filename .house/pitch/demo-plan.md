# Ślad: plan dema na żywo

Łączny czas dema: 2:10 (część A 70 s, część B 60 s), w pitchu od 0:30 do 2:40. Mówione teksty są w `script.md`, sekcje 2 i 3;
tu jest ścieżka klików, co ma być na ekranie i ile to trwa. Etykiety klawiszy pochodzą z aktualnego interfejsu (`web/static/`).

## Przygotowanie (dzień przed i 15 minut przed wejściem)

Wszystko w katalogu głównym repozytorium (`C:/Users/jasiu/workspace`).

1. Czysty klon z GitHuba albo repozytorium z czystym `git status` w `recipes/` (tylko `odwolanie`, `pelnomocnictwo`, `przelew`,
   bez `wezwanie.yaml`). Stan klas sprawdzić w zakładce "Klasy dokumentów".
2. `start.bat web` uruchomić z wyprzedzeniem (pierwsze uruchomienie tworzy `.venv` i instaluje zależności, kilka minut; kolejne ok.
   minuta). Adres: `http://127.0.0.1:8000`. Okno terminala schować, ale nie zamykać.
3. Przeglądarka (Edge lub Chrome) w trybie pełnoekranowym, powiększenie 125% (projektor), tryb Noc (domyślny). Jeśli sala jest jasna,
   przełącznik "Daylight" w pasku górnym. Karta gotowa na stronie "Przetwarzanie".
4. Pliki do wgrania, otwarte w eksploratorze w osobnym oknie, żeby przeciągnąć je jednym ruchem:
   - `uzp-data/dane/przyklad_07/odwolanie.pdf`
   - `uzp-data/dane/przyklad_07/pelnomocnictwo.pdf`
   - `uzp-data/dane/przyklad_07/potwierdzenie_przelewu.pdf`
   - `uzp-data/szablon-aplikacja/input/case1/negatywny przyklad.pdf`
   - opcjonalnie skan: `uzp-data/szablon-aplikacja/input/case1/przyklad odwolanie.pdf` (7 stron, OCR)
   - do części B: `.house/pitch/demo-assets/wezwanie.pdf` (wezwanie do zapłaty, nowa klasa)
5. Próba generalna dokładnie tą ścieżką, dwa razy. Pierwszy przebieg rozgrzewa cache OCR (`%TEMP%/odw2json-ocr-cache`), przez co
   skan na scenie czyta się w sekundy zamiast około minuty. Po próbie usunąć klasę `wezwanie` (klawisz "Usuń", potwierdzenie) i skasować
   `input/demo/` oraz `output/demo/`.
6. Przygotować drugie okno terminala w katalogu repozytorium (część B, krok B7), z historią: `start.bat`.
7. Nagrać Plan B (patrz niżej), zanim wejdziemy na scenę.

## Część A: sprawa, klasy, dowody (70 s)

| # | Czas | Klik / akcja | Co ma być widać | Co mówić (skrót) |
|---|---|---|---|---|
| A1 | 0:00 | Karta "Przetwarzanie" (nagłówek "Sprawa na wejściu, JSON na wyjściu"). W polu "Nazwa sprawy" zostaje `sprawa` albo wpisać `przyklad_07` | strefa "Przeciągnij tu pliki PDF" | "Wgrywam sprawę." |
| A2 | 0:05 | Przeciągnąć 3 PDF-y z `przyklad_07` i `negatywny przyklad.pdf` na strefę (albo kliknąć strefę i zaznaczyć 4 pliki) | kolejka "Pliki w kolejce" z 4 nazwami; aktywny klawisz "Przetwórz sprawę" | "Trzy dokumenty sprawy plus ogłoszenie TED, które nie jest żadnym z nich." |
| A3 | 0:15 | Kliknąć "Przetwórz sprawę" (jedyny klawisz główny) | pasek "Przetwarzanie", po chwili sekcja "Wynik": "Rozpoznane: 3. Odrzucone: 1 (pusty JSON {})." Dokumenty tekstowe: kilka sekund | "Klasę rozpoznajemy po treści, nie po nazwie pliku." |
| A4 | 0:25 | Pokazać kartę odrzuconego dokumentu (oznaczenie "Odrzucony", powód: brak pasującej klasy) | czwarta karta z oznaczeniem odrzucenia | "Czwarty dostaje pusty JSON. To kontrakt UZP." |
| A5 | 0:32 | W karcie odwołania: zakładka "Dowody dla pól (N)" jest domyślnie otwarta. Przewinąć tabelę ("Pole", "Wartość", "Strona", "Fragment źródła", "Reguła", "Pewność"). W polu "Filtruj dowody" wpisać `nip` | wiersze z NIP-em Odwołującego, fragment źródła z podświetloną wartością, pewność 1 | "Każda wartość: strona, fragment, reguła, pewność. NIP przeszedł sumę kontrolną." |
| A6 | 0:48 | Kliknąć zakładkę "JSON", potem "Kopiuj JSON" albo "Pobierz JSON" | JSON w stylu schematu UZP | "To jest plik, który trafia do `output`. Wartości takie, jak w dokumencie." |
| A7 | 0:55 | Przewinąć do bloku sprawdzeń spójności (znaczniki nad kartami dokumentów) | wyniki: NIP mocodawcy zgodny z Odwołującym, numer postępowania w tytule przelewu | "Spójność sprawy: informacja dla człowieka, nie przeróbka wyniku." |
| A8 | opcja, +10 s | Wgrać `przyklad odwolanie.pdf` (skan) jako osobną sprawę | karta z klasą odwołanie i tabelą dowodów, pewność pól z OCR mnożona przez 0,9 | "To skan bez warstwy tekstowej. Czyta go OCR, a dowody wyglądają tak samo." |
| A9 | 1:10 | Kliknąć "Klasy dokumentów" w nawigacji | lista klas | przejście do części B |

Ryzyka A: jeśli "Przetwórz sprawę" trwa dłużej niż 15 s, mówić dalej o tym, co robi (czyta warstwę tekstu, klasyfikuje); jeśli upłynie
30 s bez wyniku, przejść do Planu B.

## Część B: nowa klasa z szablonu, próba na PDF, zapis, CLI (60 s)

Ta ścieżka przeszła w całości odbiór judge'a (`reports/judge-manual-1.md`, sekcja T015) na tym samym PDF-ie i szablonie.

| # | Czas | Klik / akcja | Co ma być widać | Co mówić (skrót) |
|---|---|---|---|---|
| B1 | 0:00 | Widok "Klasy dokumentów": lista trzech klas z oznaczeniem "Klasa zadania UZP". Kliknąć "Nowa klasa z szablonu" | edytor ("Edytor"): po lewej "Receptura (YAML)" z komentowanym szablonem (`class: nowa_klasa`), po prawej "Szkielet wyniku (JSON)" | "Dostaję komentowaną recepturę." |
| B2 | 0:08 | W polu YAML zmienić `class: nowa_klasa` na `class: wezwanie`; jeśli linia `output_schema:` nie zmieniła się sama, zmienić ją na `wezwanie.output.json`. Resztę szablonu zostawić (pola `wezwanie.kwota`, `wezwanie.termin` pasują do dokumentu demonstracyjnego) | zmieniona nazwa | "Zmieniam tylko nazwę klasy. Sygnały i pola już opisują wezwanie do zapłaty." |
| B3 | 0:15 | Kliknąć "Szkielet z pól" | w "Szkielet wyniku (JSON)" pojawia się `{"wezwanie": {"kwota": null, "termin": null}}` | "Szkielet wyniku buduje się z listy pól." |
| B4 | 0:22 | Kliknąć "Sprawdź" | komunikat: "Receptura jest poprawna" (klasa wezwanie, 2 pola) | "To ten sam walidator, który działa w silniku." |
| B5 | 0:28 | Kliknąć "Wypróbuj na PDF", wybrać `wezwanie.pdf` | wynik próby: "Rozpoznany jako wezwanie", punkty klas, tabela dowodów: `wezwanie.kwota` 1234.5 ze strony 1 i fragmentem "Kwota do zapłaty: 1 234,50 zł"; `wezwanie.termin` 2026-12-15, JSON. Nic nie zapisano | "System nigdy nie widział takiego dokumentu. Kwota i termin z fragmentem źródła." |
| B6 | 0:40 | Kliknąć "Zapisz" (jedyny klawisz główny w widoku) | komunikat "Dodano klasę wezwanie"; w liście czwarta klasa | "Zapisane do `recipes/wezwanie.yaml`." |
| B7 | 0:46 | Przełączyć się na okno terminala. `mkdir input\demo`, skopiować `wezwanie.pdf` do `input\demo\`, uruchomić `start.bat`. Potem `type output\demo\wezwanie.json` | `{"wezwanie": {"kwota": 1234.5, "termin": "2026-12-15"}}` (reszta spraw w `input/` bez zmian) | "Bez restartu. Ta sama klasa działa w CLI. Żadnej linii kodu." |
| B8 | 0:58 | Wrócić do przeglądarki, "Usuń" na klasie wezwanie (dwa kliknięcia, potwierdzenie) | lista wraca do 3 klas | "Sprzątam po sobie." (opcjonalnie, można po pitchu) |

Ryzyka B: (1) po wklejeniu edytor może nie przeliczyć `output_schema`; wtedy "Sprawdź" pokaże błąd z numerem linii, co też jest dobrym
demo (naprawić linię). (2) `start.bat` przetwarza cały `input/`, więc przed sceną w `input/` ma być tylko mały zestaw (3-5 plików), inaczej krok B7
zajmie za długo. Najlepiej uruchomić `python -m odw2json --input input\demo --output output\demo`, żeby przetworzyć tylko ten
jeden plik (równoważne, szybsze). (3) Docker: edytor zapisuje do `recipes/` na hoście (montowanie bez `:ro`), ale demo robimy z `start.bat`.

## Plan B (kolejność przełączania)

1. **Zrzuty ekranu.** Pliki w `docs/screenshots/`: `desktop-night-upload.jpg` (wgrywanie), `desktop-night-json.jpg` (JSON),
   `desktop-daylight-results.jpg` (spójność), `desktop-daylight-evidence.jpg` (tabela dowodów), `class-editor-night-error.jpg` (edytor, błąd w linii 34),
   `class-try-mobile-daylight.jpg` (próba na PDF). Otworzyć je z góry w osobnych kartach przeglądarki, w tej kolejności; mówić ten sam tekst.
2. **Nagranie wideo ścieżki A+B.** `[do zrobienia: nagrać 2-minutowy film przebiegu ekranu według tabel A i B, zapisać jako
   .house/pitch/demo-fallback.mp4 i mieć otwarty w odtwarzaczu]`. Do czasu nagrania punkt 1 jest jedynym planem awaryjnym dla przeglądarki.
3. **Ścieżka tylko CLI** (gdy padnie interfejs, a działa Python): w terminalu `python -m odw2json --input input --output output` na sprawie
   `przyklad_07` i `case1`, potem `type output\przyklad_07\odwolanie.json` i `type "output\case1\negatywny przyklad.json"` (wynik `{}`).
   Dowody w CLI ma tylko log; mówić o nich na podstawie zrzutu `desktop-daylight-evidence.jpg`.
4. **Docker** (gdy zawiedzie lokalny Python): `docker compose up --build`, interfejs na `http://localhost:8000`; obraz buduje się około 8 minut,
   więc tylko jeśli został zbudowany wcześniej.
5. **Brak internetu na scenie:** niczego nie szkodzi, fonty i interfejs są lokalne; profil `llm` w demie nie jest używany.

Reguła: nigdy nie próbować naprawiać błędu przed jury dłużej niż 15 sekund. Przełączać się na kolejny krok planu B i mówić dalej.

## Po pitchu (przed pytaniami)

Zostawić otwartą kartę z wynikiem sprawy: na pytania o dowody i spójność wystarczy kliknąć wiersz tabeli. Tabela pomyłek do pytania 6
jest w `.house/reports/misses-1.md`.
