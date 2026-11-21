# Dziennik decyzji

Każda decyzja, która zmienia kierunek, zakres albo zasady pracy. Najnowsze na dole.
Format wpisu: nagłówek drugiego poziomu `D-<kolejny numer, 3 cyfry> <krótki tytuł>`, pod nim:

```
- **Decyzja:** …
- **Dlaczego:** …
- **Kto:** człowiek | judge | coordinator
- **Data:** YYYY-MM-DD HH:MM
```

## D-001 Dwa zadania: ODWOŁANIA2JSON tutaj, Radar Innowacji w osobnym repo
- **Decyzja:** Drużyna robi dwa zadania. To repo (Eterphis/hacknation-2026) = ODWOŁANIA2JSON (UZP). Radar Innowacji (Podkarpackie Centrum Innowacji) ma osobne repo konkursu `house/contests/radar-innowacji` z własnym `.house/`.
- **Dlaczego:** house prowadzi jeden konkurs na repo (spec, zamrożone kryteria, bramka scalania, eksport); osobne zgłoszenia na Hacktribe.
- **Kto:** człowiek
- **Data:** 2026-11-21 10:37

## D-002 Tryb build z mierzalnym rdzeniem F1
- **Decyzja:** `kind: build` z rubryką (F1 50% + elastyczność 50%) oraz metryką F1 liczoną lokalnie przez własną kopię sprawdzarki z `ground_truth.yaml`. Preselekcja to 100% F1, więc sprawdzarka powstaje jako pierwsze zadanie, a kryteria akceptacji zadań ekstrakcji to progi F1.
- **Dlaczego:** finał to pitch + rozbudowywalność (build), ale do finału wchodzi się wyłącznie przez F1 na ukrytym zbiorze; `house exp` (tryb optimize) nie działa na Windowsie.
- **Kto:** coordinator
- **Data:** 2026-11-21 10:37

## D-003 Python 3.13 jako wersja projektu
- **Decyzja:** Projekt budujemy i testujemy na Pythonie 3.13 (wymóg sprawdzarki UZP: 3.13+). house dalej działa na 3.12.
- **Dlaczego:** automatyczna ocena UZP uruchomi kod na 3.13+; różnice wersji wychodziłyby dopiero u nich.
- **Kto:** człowiek
- **Data:** 2026-11-21 10:37

## D-004 Intake zaktualizowany z pełnej treści zadania (README repo UZP)
- **Decyzja:** Źródłem prawdy jest `README.md` z github.com/Urzad-Zamowien-Publicznych/hacknation-2026 (deck tylko pomocniczo). Wiążące ustalenia: kontrakt `./input/<sprawa>/*.pdf → ./output/<sprawa>/<ta sama nazwa>.json` uruchamiany CLI/`start.bat`; schematy z komentarzami w `oczekiwane-json/` traktujemy jako specyfikację pól; prawdą referencyjną są pliki JSON w `dane/przyklad_NN/` (60 spraw, nie 39; brak `ground_truth.yaml`); zgłoszenie = tytuł + link do GitHub działającego prototypu z wgrywaniem dokumentów i podglądem wyników.
- **Dlaczego:** pełna treść opublikowana 2026-11-21 11:00 zastępuje deck i wpisy z Discorda.
- **Kto:** coordinator
- **Data:** 2026-11-21 11:30

## D-005 Ścieżka bez LLM musi dawać pełny wynik F1
- **Decyzja:** Rdzeń ekstrakcji działa deterministycznie (tekst PDF + reguły/konfiguracja) i sam generuje kompletne JSON-y. LLM to opcjonalny adapter wyłącznie z otwartymi modelami (wymóg „wyłącznie komponenty open source, w tym otwarto-źródłowe modele językowe”), włączany konfiguracją; bez klucza/sieci aplikacja nie może się wywrócić ani zgubić pól.
- **Dlaczego:** preselekcja to 100% F1 z automatycznej sprawdzarki UZP; nie wiemy, czy da nam sieć i klucz API (Q-002). Dane treningowe mają warstwę tekstową i powtarzalny układ, więc reguły są realne; zamknięte modele (Claude/GPT) są wykluczone treścią zadania.
- **Kto:** coordinator
- **Data:** 2026-11-21 11:30
