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

## D-015 Lokalny LLM dozwolony i punktowany; zewnętrzne API odpada
- **Decyzja:** Zgodnie z mentorami UZP model uruchamiany lokalnie na 16 GB RAM (CPU) daje maksimum punktów w kategorii „moc modelu”; LLM po zewnętrznym API odkładamy całkowicie (bez kluczy, bez wysyłania danych). Ścieżka bez LLM (D-005) zostaje podstawą i musi działać sama; lokalny model (rodzina Qwen3 / Bielik / Basal, tylko Apache-2.0 lub MIT, runtime llama.cpp MIT) wchodzi jako opcjonalny „czytelnik” pól trudnych przy zmienionym układzie (role stron: nadawca/odbiorca), według wzorca z `qa-system-akygabattery` spec-extraction: model przepisuje tekst tak, jak jest wydrukowany, kod normalizuje, każda wartość jest ugruntowana (cytat musi istnieć w tekście strony), a wartość z recepty o pełnej pewności nie jest nadpisywana. Mniejszy model = więcej punktów (README: 1–20 pkt, im mocniejszy, tym mniej).
- **Dlaczego:** test ma zmieniony układ dokumentów, a mentorzy wskazali ustalenie nadawcy/odbiorcy jako najtrudniejsze; reguły na stałych etykietach tego nie uogólnią. Lokalny mały model + ugruntowanie łączy F1 z transparentnością.
- **Kto:** człowiek (odpowiedź mentorów) + coordinator
- **Data:** 2026-11-21 19:00

## D-016 Kontrakt wyjścia według zaktualizowanego README UZP
- **Decyzja:** (1) Dokument odrzucony dostaje plik `<nazwa>.json` z pustym obiektem `{}` zamiast braku pliku (README i `dane/negatywne/readme.md`: „zwrócić pusty plik .json”); tryb przełączalny w konfiguracji (`output.rejected: empty_object | empty_file | none`), dopóki Q-004 pyt. 1 nie rozstrzygnie. (2) Klasyfikacja wyłącznie po treści (nazwy plików nic nie znaczą; `przelew.pdf` zamiast `potwierdzenie_przelewu.pdf`). (3) `czynnosc_powod_id` 1–12 według `oczekiwane-json/czynnosc_powod_id_dict.md` (12 = „Projektowane postanowienia umowy”). (4) Imiona i nazwiska pełnomocnika i mocodawcy w mianowniku.
- **Dlaczego:** ocena = podmiana `input` i porównanie `output` z CLI; brak pliku dla negatywu może być liczony jako błąd.
- **Kto:** coordinator (domyślne założenie do potwierdzenia w Q-004)
- **Data:** 2026-11-21 19:00

## D-017 Dane UZP można upubliczniać; nowe zbiory ewaluacyjne
- **Decyzja:** Dane treningowe i testowe UZP są generowane i wolno je upublicznić: małe próbki mogą trafić do `tests/fixtures/`, a cały zbiór zostaje klonem w `uzp-data/` (rozmiar). Ewaluacja od teraz na czterech zbiorach: syntetyczne 01–40 (strojenie), 41–60 (odłożone, częściowo skażone wg D-014), `dane/skany` (30 skanów ze złotymi JSON — główna niezależna miara, bliska prawdziwemu testowi) i `dane/negatywne` (12 dokumentów do odrzucenia; miara: odsetek poprawnie odrzuconych).
- **Dlaczego:** prawdziwy test ma zmieniony układ i skany; syntetyczne sprawy przestały być dobrą miarą uogólniania.
- **Kto:** człowiek (odpowiedź mentorów) + coordinator
- **Data:** 2026-11-21 19:00

## D-018 Właściciel przejmuje implementację; teammate'om tylko handoffy na żądanie
- **Decyzja:** Prace implementacyjne znowu idą w sesji właściciela (koordynator deleguje do coderów tutaj); handoffy dla teammate'ów piszemy tylko, gdy właściciel o to poprosi. D-013 przestaje obowiązywać.
- **Kto:** człowiek
- **Data:** 2026-11-21 19:00

## D-019 Fala 4: T013 od teammate'a + T012/T014/T015/T016, potem T009
- **Decyzja:** Synchronizacja z handoffem teammate'a (`.house/handoff/teammate-final.md`): jego T013 (nowe dane UZP: `{}` dla odrzuconych, negatywy 16/16, id 12, poprawka kolejności linii OCR, skany 0,73) scalamy z automatycznymi kryteriami dopisanymi przez koordynatora (kształt wyjścia, negatywy, skany ≥ 0,70) — od teraz to bramka regresji. Numeracja jak u teammate'a: T012 = profile + `--workers` + bench (jego propozycja P0–P4 zawężona do D-015: profile `text`/`ocr`, slot na `llm`, bez API i bez P4), T014 = recepty na skanach (cel ≥ 0,80, 41–60 ≥ 0,94), T015 = edytor klas w UI (20 pkt za dodawanie typów), T016 = lokalny mały LLM jako ugruntowany czytelnik słabych pól (spike modeli najpierw, wzorzec spec-extraction właściciela), T009 = spójność sprawy po T014. Równolegle: T012, T014, T015 (rozłączne pliki); T016 po T012 i T014.
- **Dlaczego:** skany to najlepsza miara prawdziwego testu; czas i RAM na laptopie oceniającego wymagają równoległości i pomiaru; elastyczność to 50% finału.
- **Kto:** coordinator (prośba człowieka: „sync, potem plan i ruszaj z falą”)
- **Data:** 2026-11-21 19:30

## D-020 Zmiana kryteriów T003

- **Decyzja:** nowe kryteria akceptacji T003: AC-1 (run), AC-2 (run), AC-3 (run), AC-4 (run)
- **Dlaczego:** UZP upstream 84cc976 added negatives to dane/ (196 PDFs instead of 180, one image-only negative without words); count and boxed thresholds made data-robust, D-017
- **Kto:** coordinator
- **Data:** 2026-11-21 17:44

## D-021 Wnioski z odpowiedzi mentorów (Q-004)
- **Decyzja:** (1) Odrzucony dokument → `{}` (potwierdzone; domyślny tryb `--rejected-json {}` zostaje). (2) Brakujące pole → `null`, jak w złotych JSON-ach; nigdy nie uzupełniamy pola wartością z innego dokumentu sprawy: naprawy w T009 wyłączone w `recipes/case.yaml` (`repair: false`), sprawdzenia spójności zostają jako informacja w `checks` i UI. (3) Sprawa może mieć kilka pełnomocnictw i negatywy obok trzech klas: każdy dokument przetwarzany osobno, krok sprawy działa na listach dokumentów danej klasy. (4) LLM nie daje przewagi punktowej (bez LLM = maksimum, lokalny na 16 GB = maksimum): T016 zostaje tylko wtedy, gdy podnosi F1 lub odporność na nowe układy przy akceptowalnym czasie; domyślny profil pozostaje `ocr`, dopóki bench nie pokaże zysku. (5) Wagi modelu mogą być pobierane przy pierwszym uruchomieniu (laptop ma internet). (6) F1 prawdopodobnie normalizowane do stringów: typy liczba/tekst nie wymagają zmian.
- **Kto:** człowiek (odpowiedzi mentorów) + coordinator
- **Data:** 2026-11-21 21:00

## D-022 Zmiana kryteriów T019

- **Decyzja:** nowe kryteria akceptacji T019: AC-1 (run), AC-2 (run), AC-3 (run), AC-4 (manual)
- **Dlaczego:** Właściciel: akceptowalne wydłużenie OCR przez obróbkę obrazu to do +40% (było +30%)
- **Kto:** coordinator
- **Data:** 2026-11-21 21:56

## D-023 Nazwa produktu: Ślad
- **Decyzja:** Produkt nazywa się **Ślad** (ASCII: `slad`); pod tą nazwą powstaje publiczna kopia z `house export`. Pakiet Pythona zostaje `odw2json`, CLI `python -m odw2json`.
- **Dlaczego:** właściciel poprosił o nazwę projektu inną niż nazwa zadania; „ślad” = trace (identyfikacja Cold Trace) i główny wyróżnik: każde pole ma ślad w dokumencie (strona, fragment, reguła, pewność).
- **Kto:** coordinator (na prośbę człowieka)
- **Data:** 2026-11-21 22:40

## D-024 Zmiana kryteriów T016

- **Decyzja:** nowe kryteria akceptacji T016: AC-1 (run), AC-2 (run), AC-3 (run), AC-4 (manual)
- **Dlaczego:** Właściciel: próg +0,05 F1 na skanach był ustawiony przy ocr = 0,73; przy ocr = 0,96-0,98 jest nieosiągalny. Nowy warunek: llm nie traci względem ocr na żadnym zbiorze i zostaje opcjonalny
- **Kto:** coordinator
- **Data:** 2026-11-21 22:59

## D-025 Publiczne repo zgłoszenia: Eterphis/slad
- **Decyzja:** kopia z `house export` (bez `.house/`, `house/`, `CLAUDE.md`, `TEAM.md`; autor commita: adres noreply GitHuba) opublikowana jako publiczne https://github.com/Eterphis/slad. Repo konkursowe zostaje prywatne. Każda zmiana produktu po tym momencie wymaga ponownego eksportu i pushu do `slad`.
- **Dlaczego:** zgłoszenie na Hacktribe wymaga linku GitHub do działającego prototypu; protokół export.md.
- **Kto:** człowiek (zgoda na publikację) + coordinator
- **Data:** 2026-11-22 06:18

## D-026 Prefiks PL w numerze rachunku: jak we wzorcach
- **Decyzja:** dokument czytany OCR-em (skan) zachowuje prefiks `PL` tak, jak go wydrukowano; dokument z warstwą tekstową (dane syntetyczne) dostaje same cyfry, jak dziś. Do zmiany po odpowiedzi mentorów (Q-005).
- **Dlaczego:** wzorce UZP są tu rozbieżne między źródłami: na 10 skanach przelewów wzorzec ma `PL` dokładnie wtedy, gdy wydruk ma `PL`; syntetyczne przykłady (np. przyklad_03) obcinają `PL` mimo wydruku. Prawdziwy test jest częściowo skanowany.
- **Kto:** człowiek
- **Data:** 2026-11-22 06:25

## D-027 Hosting: Hugging Face Spaces
- **Decyzja:** publiczne demo na Hugging Face Spaces (Docker, darmowe CPU basic), z tego samego kodu co `Eterphis/slad`; edytor klas w trybie tylko do odczytu (`ODW2JSON_READONLY_RECIPES=1`), profil `ocr`, bez LLM. Logowanie do HF i token robi człowiek; coordinator przygotowuje i wypycha pliki Space.
- **Dlaczego:** decyzja właściciela; jury może kliknąć link bez instalacji. Read-only, bo publiczny edytor receptur mógłby zostać zepsuty przez odwiedzających.
- **Kto:** człowiek
- **Data:** 2026-11-22 07:40
