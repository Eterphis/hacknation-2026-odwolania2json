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

## D-006 Pełna treść (PDF) i regulamin zadania: realne sprawy testowe, finał 50/30/20, Docker Compose od początku
- **Decyzja:** Do spec.yaml dochodzą: (1) zbiór testowy = co najmniej 10 realnych spraw, a treningowe są syntetyczne, więc liczy się uogólnianie (skany, inne układy), nie dopasowanie do 60 przykładów; (2) rubryka finału wg PDF: F1 50%, elastyczność 30%, architektura i jakość techniczna 20% (regulamin mówi 50/50 — pytanie w Q-002, projekt pokrywa oba warianty); (3) finał dla maks. 3 drużyn; (4) od pierwszego dnia w repo: `docker compose`, dokumentacja architektury, opis konfiguracji klasy dokumentu i dodawania nowej klasy, lista komponentów zewnętrznych (warunki wypłaty nagrody i §4.1 regulaminu); (5) zwycięzca przenosi prawa majątkowe na UZP — w repo tylko nasz kod i zależności open source z licencjami pozwalającymi na to.
- **Dlaczego:** `UZP - Pełna treść zadania konkursowego.pdf` i `UZP - Regulamin zadania konkursowego.pdf` (Downloads) różnią się od README; regulamin zadania ma pierwszeństwo przed regulaminem wydarzenia. PDF z treścią dodaje też §9: UZP szuka podstawy uniwersalnego narzędzia PDF → dane.
- **Kto:** coordinator
- **Data:** 2026-11-21 12:10

## D-007 Koncepcja: silnik recept YAML + model „słowa z ramkami” + spójność sprawy, LLM jako dodatek
- **Decyzja:** Wariant A z Q-003: chudy, konfigurowalny silnik recept (I-001), na wspólnym modelu stron „słowa + ramki” dla PDF-ów cyfrowych i skanów (I-005), z lekkimi kontrolami spójności między dokumentami sprawy (I-002: mocodawca = odwołujący, numer sprawy w tytule przelewu) i dowodem dla każdego pola w UI. Otwarty LLM (I-004) tylko jako dodatek wyłączony domyślnie. Kolejność cięcia: klik-korekta → LLM → ramki na obrazie strony → edytor w przeglądarce.
- **Dlaczego:** najwyższy szacowany wynik sędziego (4,3 przy 50/30/20, 4,5 przy 50/50), pewna ścieżka F1 bez sieci (D-005), elastyczność przez konfigurację i przejrzystość premiowane przez UZP.
- **Kto:** człowiek
- **Data:** 2026-11-21 13:45

## D-008 Sprzęt 16 GB RAM bez GPU; OCR z sesji teammate'a; hosting opcjonalny na końcu
- **Decyzja:** Wszystko (OCR, opcjonalne modele) musi działać na CPU w 16 GB RAM. Wybór silnika OCR przychodzi z researchu w sesji teammate'a; u nas OCR jest wymiennym adapterem za interfejsem „strona → słowa z ramkami”, z RapidOCR (Apache-2.0, pip) jako tymczasowym domyślnym do testów. Darmowy hosting (AWS free tier / Vercel) dopiero po zamrożeniu funkcji, w lekkim trybie bez LLM. Modele Basal-mini/pico sprawdza researcher (`reports/model-basal.md`) jako kandydat na klasyfikator.
- **Dlaczego:** decyzja człowieka; darmowe instancje mają ok. 1 GB RAM, więc pełny pipeline pokazujemy lokalnie / przez docker compose.
- **Kto:** człowiek + coordinator
- **Data:** 2026-11-21 13:45

## D-009 Basal tylko jako opcjonalny klasyfikator, po porównaniu z TF-IDF
- **Decyzja:** Proponowane wartości ze spec.yaml zatwierdzone (Q-001 = A). Rodzina Basal (Remek/basal-*, Apache-2.0, 0,75–1,6 mld parametrów) wchodzi najwyżej jako opcjonalny backend klasyfikacji z klasą „odrzuć”, za tym samym interfejsem co klasyfikator regułowy, i tylko jeśli na naszej ewaluacji pobije tani baseline TF-IDF + regresja logistyczna. Nie robimy fine-tuningu (16 GB CPU, mało czasu); Basal nie wyciąga pól.
- **Dlaczego:** `reports/model-basal.md`: licencja czysta, mieści się na CPU, ale jakość podana tylko przez autora, a biblioteki (transformers 5.x, torch 2.11) nie są sprawdzone na Pythonie 3.13; klasyfikacja 3 typów + odrzucenie jest prosta dla reguł i TF-IDF.
- **Kto:** coordinator (sugestia człowieka do rozważenia)
- **Data:** 2026-11-21 14:05

## D-010 Plan: 10 zadań w 4 falach, kontrakt danych od coordinatora
- **Decyzja:** Kontrakt `odw2json/model.py` (Word/Page/Document, Evidence, Classification, Extraction, CaseResult, protokoły Ingestor/Classifier/Extractor) pisze coordinator na main, żeby fala 1 ruszyła równolegle. Fale: (1) T001 szkielet + CLI + zapis kompletnych JSON-ów, T002 sprawdzarka F1 (dokładne dopasowanie jako `score`, znormalizowane obok; sprawy 01–40 do strojenia, 41–60 odłożone), T003 wczytywanie słów z ramkami + OCR; (2) T004 silnik recept z odrzucaniem (zero nazw klas w `odw2json/engine`), T007 UI, T010 zaszumiony zbiór skanów; (3) T005 recepty przelew + pełnomocnictwo (F1 ≥ 0,95 / 0,90 na 41–60), T006 recepta odwołania (≥ 0,85), T008 Docker Compose + dokumentacja + CI; (4) T009 spójność sprawy (całość ≥ 0,90). Pomocnicze sprawdzarki akceptacji w `.house/accept/` (poza zasięgiem workerów). Wspólny venv Pythona 3.13: `C:/Users/jasiu/workspace/.venv`. Dodatki (druga klasa tylko w YAML, ramki na obrazie strony, LLM/Basal) planujemy po rundzie sędziego o 00:00.
- **Dlaczego:** kamień 18:00 wymaga golden path (T001–T006); progi F1 na odłożonych sprawach pilnują uogólniania, a grep po `odw2json/engine` dowodzi „nowa klasa = tylko konfiguracja” (30% finału).
- **Kto:** coordinator
- **Data:** 2026-11-21 14:40

## D-011 T004 i T010 robi sesja teammate'a
- **Decyzja:** T004 (silnik recept) i T010 (zaszumiony zbiór) wykonuje sesja Claude teammate'a jako worker, według `.house/handoff/T004-T010-teammate.md`: pracuje na gałęziach `task/T004-recipe-engine` i `task/T010-noisy-heldout`, pushuje je, raport w `handoff-reports/` na gałęzi. Bramka (house check, review dla T004, merge) zostaje u coordinatora na maszynie właściciela. Pomocnicze sprawdzarki czytają ścieżkę danych z `UZP_DATA`.
- **Dlaczego:** decyzja człowieka; odciąża limit 3 równoległych agentów tutaj, a jedna bramka scalania na jednej maszynie zachowuje zamrożone kryteria i spójny main.
- **Kto:** człowiek
- **Data:** 2026-11-21 16:00

## D-012 UI w tożsamości Cold Trace (Eterphis), T011 na Sonnecie
- **Decyzja:** Interfejs webowy (T011) nosi system wizualny właściciela Cold Trace według artefaktu https://claude.ai/artifact/WchMUpvmWZxesNduioFZ2o. Lokalna kopia referencyjna zestawu leży w `design/cold-trace/` (tylko do odczytu), a aplikacja serwuje własną kopię z `web/static/coldtrace/`: grit z lokalnych PNG, fonty Anybody i Martian Mono (SIL OFL) hostowane lokalnie, więc działa offline / on-premise. Noc domyślnie, przełącznik Daylight. API i trasy bez zmian. Zadanie wykonał coder na Sonnecie (prośba człowieka). Do `house review` na Windows potrzebny jest prefiks PATH z pakietem winget Claude Code oraz poprawka `house/houselib/review.py` (taskkill zamiast `os.killpg`).
- **Dlaczego:** decyzja człowieka; demo i zrzuty ekranu widzi jury, a przejrzystość ekstrakcji (tabela dowodów) jest oceniana. Zrzuty w `docs/screenshots/` pokazują dowody z makiety (silnik to jeszcze stub T001) — do powtórzenia po T004.
- **Kto:** człowiek + coordinator
- **Data:** 2026-11-21 16:30

## D-013 Fala 3 (T005, T006, T008) u teammate'a; tutaj tylko weryfikacja i scalanie
- **Decyzja:** Zadania implementacyjne fali 3 wykonuje sesja teammate'a według `.house/handoff/wave3-teammate.md` (kolejność przy małym limicie: T005 → T006 → T008). Na maszynie właściciela nie uruchamiamy nowych coderów; house check, review i merge działają normalnie. Poprawki z review T004 (2 MAJOR + 5 MINOR) dokończono tutaj przed scaleniem, F1 bez zmian (0,8737). Zaszumiony zbiór T010 leży w `uzp-data-noisy/` (gitignored).
- **Dlaczego:** decyzja człowieka: limit właściciela 80%, teammate'a 30%, reset o 14:30.
- **Kto:** człowiek
- **Data:** 2026-11-21 17:00

## D-014 Sprawy odłożone 41–60 nie są już w pełni niezależne dla pełnomocnictwa
- **Decyzja:** Teammate w T005, za zgodą właściciela (czat), obejrzał układ tekstu pełnomocnictw w sprawach 41–60, żeby dobić do progu 0,90 (bez kopiowania wartości z gold). Wynik pełnomocnictwa na 41–60 (0,997) traktujemy jako zawyżony. Niezależne miary uogólniania to od teraz: zaszumiony zbiór T010 (OCR), skan z szablonu i odwołanie (T006 nie zaglądało w 41–60).
- **Dlaczego:** test ma prawdziwe, częściowo skanowane dokumenty; zawyżona liczba nie może kierować decyzjami ani trafić do pitchu jako „wynik na danych niewidzianych”.
- **Kto:** człowiek (zgoda) + coordinator (zapis)
- **Data:** 2026-11-21 18:00
