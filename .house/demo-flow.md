# Demo flow: złota ścieżka Ślad (odw2json)

Lista kontrolna do `protocols/demo-checklist.md` i do prób przed Etapem II. Każdy punkt sprawdza się wykonaniem, nie czytaniem kodu.
Pełny scenariusz klików i tekst mówiony: `pitch/demo-plan.md` i `pitch/script.md`. Środowisko: Windows, Python 3.13, 16 GB RAM, bez GPU.

## 0. Czysty start
- [ ] Świeży klon repozytorium (bez `.venv`, bez `output/`); `recipes/` zawiera tylko `odwolanie`, `pelnomocnictwo`, `przelew`.
- [ ] `start.bat` na świeżym klonie kończy się bez błędu (pierwsze uruchomienie: kilka minut na instalację; kolejne: ok. minuty).
- [ ] `docker compose up --build` podnosi interfejs na `http://localhost:8000` (sprawdzić osobno, nie tylko `start.bat`).

## 1. Linia poleceń (kontrakt UZP)
- [ ] `input/przyklad_07/` (3 PDF-y) i `input/case1/` (`negatywny przyklad.pdf`) dają `output/<sprawa>/<ta sama nazwa>.json`.
- [ ] Wyjście `przyklad_07` zgadza się z wzorcem UZP (`uzp-data/dane/przyklad_07/*.json`); klasa wynika z treści, nie z nazwy pliku.
- [ ] Dokument spoza klas (`negatywny przyklad.pdf`) dostaje plik z pustym `{}`.
- [ ] Skan (`przyklad odwolanie.pdf`, bez warstwy tekstowej) jest czytany OCR-em i daje JSON klasy odwołanie.
- [ ] Brakujące pole ma `null`; żaden plik nie jest pominięty.

## 2. Interfejs: sprawa i transparentność
- [ ] `start.bat web`, `http://127.0.0.1:8000` otwiera "Sprawa na wejściu, JSON na wyjściu"; Noc domyślnie, przełącznik Daylight działa.
- [ ] Wgranie 3 PDF-ów z `przyklad_07` i `negatywny przyklad.pdf`, "Przetwórz sprawę": "Rozpoznane: 3. Odrzucone: 1 (pusty JSON {})".
- [ ] Karta odrzuconego dokumentu pokazuje powód (brak pasującej klasy).
- [ ] Zakładka "Dowody dla pól": kolumny Pole, Wartość, Strona, Fragment źródła, Reguła, Pewność; filtr działa (np. `nip`).
- [ ] Zakładka "JSON" pokazuje wynik; "Pobierz JSON" i pobranie ZIP działają.
- [ ] Sprawdzenia spójności sprawy widoczne: NIP mocodawcy zgodny z Odwołującym, numer postępowania w tytule przelewu.
- [ ] Konsola przeglądarki bez błędów krytycznych; widok czytelny na projektorze (125%) i na szerokości telefonu (375 px).

## 3. Nowa klasa bez programowania
- [ ] "Klasy dokumentów": lista 3 klas z oznaczeniem "Klasa zadania UZP".
- [ ] "Nowa klasa z szablonu", nazwa `wezwanie`; "Szkielet z pól" buduje `{"wezwanie": {"kwota": null, "termin": null}}`.
- [ ] "Sprawdź": poprawna receptura daje komunikat o poprawności; zepsuty wzorzec daje błąd z numerem linii i ścieżką.
- [ ] "Wypróbuj na PDF" (`pitch/demo-assets/wezwanie.pdf`): "Rozpoznany jako wezwanie", `kwota` 1234.5 i `termin` 2026-12-15 z fragmentem i stroną; nic nie zapisano.
- [ ] "Zapisz": "Dodano klasę wezwanie", plik `recipes/wezwanie.yaml` istnieje.
- [ ] `python -m odw2json` (albo `start.bat`) na `wezwanie.pdf` bez restartu daje `{"wezwanie": {"kwota": 1234.5, "termin": "2026-12-15"}}`.
- [ ] "Usuń" przywraca 3 klasy; trzech klas UZP nie da się usunąć.

## 4. Liczby i dokumenty zgadzają się z tym, co mówimy
- [ ] `python -m eval.score` na skanach, 41-60, 01-40 i negatywach daje liczby z `pitch/script.md` (tabela "Liczby do podmiany") i z `slides.html` (`NUMS`).
- [ ] README, `docs/EXTERNAL_COMPONENTS.md` i slajd 6 wymieniają te same komponenty i licencje; żadnego AGPL/GPL.
- [ ] Link do repozytorium wpisany w slajdzie 7 i w `pitch/script.md`.

## 5. Plan B gotowy
- [ ] Zrzuty ekranu w `docs/screenshots/` otwarte w osobnych kartach (kolejność w `pitch/demo-plan.md`, Plan B).
- [ ] Nagranie 2-minutowe ścieżki A+B (`pitch/demo-fallback.mp4`, jeszcze nie nagrane).
- [ ] Ścieżka tylko CLI wypróbowana (sekcja 1) oraz Docker zbudowany z wyprzedzeniem.
- [ ] `pitch/slides.html` otwiera się offline i przechodzi strzałkami przez 8 slajdów.
