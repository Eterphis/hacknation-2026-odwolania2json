# Pytania do człowieka

Otwarte pytania czekają na briefing („jak tam” / `/house-status`). Po odpowiedzi status zmienia się na
`[answered YYYY-MM-DD]`, a decyzja trafia do `DECISIONS.md`.

Format wpisu: nagłówek drugiego poziomu `Q-<kolejny numer, 3 cyfry> [open] <tytuł>`, pod nim:

```
- **Kontekst:** co się stało i dlaczego to pytanie
- **Opcje:** A) … B) …
- **Rekomendacja:** … (jednym zdaniem dlaczego)
- **Blokuje:** T### | nic
- **Poziom:** krytyczny | zawsze człowiek
- **Termin:** YYYY-MM-DD HH:MM (tylko krytyczny: po tym czasie judge przyjmuje „Domyślnie”)
- **Domyślnie:** A (rekomendacja; pusta = brak domyślnej)
- **Odpowiedź:** —
```

## Q-001 [open] Zatwierdzenie proponowanych wartości ze spec.yaml
- **Kontekst:** Intake ODWOŁANIA2JSON wypełnił `spec.yaml` z decku UZP i postów na Discordzie. Propozycje coordinatora (do zatwierdzenia): (1) mapowanie poziomów rubryki: F1 → 1 = <0,5, 3 ≈ 0,75, 5 ≥ 0,9 na naszych odłożonych zestawach; elastyczność → 1 = typy zaszyte w kodzie, 3 = nowe pole przez konfigurację, 5 = nowy typ dokumentu wyłącznie konfiguracją + dowód dla każdego pola (strona/fragment/pewność) w UI; (2) lokalna sprawdzarka `python eval/score.py --pred output/ --gold <sprawy>/` drukująca `score: <F1>`, budowana jako pierwsze zadanie; (3) kamienie: sob 18:00 golden path (komenda → JSON-y + F1 na 60 sprawach treningowych, świeży klon na Pythonie 3.13 bez GPU), nd 00:00 runda sędziego, nd 09:30 zamrożenie funkcji, nd 10:30 zgłoszenie na Hacktribe; (4) tryb `copilot`, maks. 3 agentów równolegle.
- **Opcje:** A) zatwierdzam wszystko B) zatwierdzam z poprawkami (napisz które)
- **Rekomendacja:** A — wartości wynikają wprost z decku; po publikacji pełnej treści o 11:00 i tak przejdą korektę.
- **Blokuje:** nic (planowanie rusza na tych wartościach)
- **Poziom:** krytyczny
- **Termin:** 2026-11-21 12:00
- **Domyślnie:** A
- **Odpowiedź:** —

## Q-002 [open] Pytania do UZP (stoisko / Discord) przed zamrożeniem architektury
- **Kontekst:** Pełna treść zadania jest już w README repo UZP (github.com/Urzad-Zamowien-Publicznych/hacknation-2026). Regulaminu zadania nadal nie ma (karta na hacknation.pl ma puste pola zasad). Szczegóły i źródła: `.house/reports/rules-check.md`.
  **Zamknięte treścią zadania (2026-11-21):**
  - Modele: „wyłącznie komponenty open source (w tym otwarto-źródłowe modele językowe)”, „bez GPU (LLM po API)” → zamknięte modele (Claude/GPT/Gemini) odpadają; otwarty model przez API jest OK. Decyzja: D-005 (ścieżka bez LLM musi dać pełny wynik).
  - Kontrakt wejścia/wyjścia: foldery `./input/<sprawa>/*.pdf` i `./output/<sprawa>/<ta sama nazwa>.json` w katalogu głównym aplikacji, uruchamianie CLI / `start.bat`, Python 3.13+, `requirements.txt`.
  - Schematy: `oczekiwane-json/{odwolanie,pelnomocnictwo,przelew}.json` (komentarze `//` = reguły pól). Prawda referencyjna = JSON-y w `dane/przyklad_NN/` (60 spraw); `ground_truth.yaml` nie istnieje.
  - Słownik `czynnosc_powod_id`: id 1–11 odtworzone z danych treningowych (lista w raporcie).
  - Zgłoszenie: tytuł + link do GitHub działającego prototypu z wgrywaniem dokumentów i podglądem wyników; opcjonalnie dokumentacja i własne wyniki testów jakości.
  - Prawa autorskie (regulamin zadania §4, PDF z Downloads): zwycięzcy **muszą** podpisać umowę przeniesienia autorskich praw majątkowych na UZP (wszyscy współautorzy, forma pisemna), inaczej tracą nagrodę; komponenty zewnętrzne trzeba wprost wymienić w prezentacji. Nagroda po przekazaniu kodu, instrukcji, Docker Compose i dokumentacji (architektura, konfiguracja klasy dokumentu, dodanie nowej klasy).
  - Zbiór testowy: co najmniej 10 **realnych** spraw (treningowe są syntetyczne); do finału wchodzą maks. 3 drużyny.
  **Zostaje do zapytania na stoisku UZP (kolejność wg wagi):**
  1. Czy sprawdzarka ma sieć i nasz klucz API? Czy „LLM po API” może być zewnętrznym hostingiem otwartego modelu (np. Llama/Qwen u dostawcy), czy tylko serwerem lokalnym (Ollama/llama.cpp)?
  2. Dokładna definicja F1: na poziomie pól-liści? exact match czy normalizacja (wielkość liter, spacje, daty, kwoty)? jak liczone listy (Odwolujacy, pelnomocnicy) i wartości null? błąd klasyfikacji = zero dla dokumentu?
  3. Nazwy plików: README pokazuje `przelew_nr_1.pdf → przelew_nr_1.json`, a dane treningowe mają `potwierdzenie_przelewu.pdf` i `przelew.json` — którą konwencję stosuje sprawdzarka? Czy nazwa pliku wejściowego zdradza typ dokumentu w zbiorze testowym?
  4. Jak sprawdzarka uruchamia kod (komenda, limit czasu na sprawę, system operacyjny)? Czy w zbiorze testowym będą skany bez warstwy tekstowej (OCR) i inne typy dokumentów niż trzy znane?
  5. Jaki jest opis dla `czynnosc_powod_id` = 12?
  6. Licencja danych treningowych: czy wolno je umieścić w publicznym repo (np. w testach)?
  7. Wagi finału: PDF z treścią podaje 50% F1 / 30% elastyczność / 20% architektura i jakość, a regulamin zadania 50% F1 / 50% elastyczność — które obowiązują? Czy wymagane są wideo/slajdy, czy tylko link do repo? Czy wolno użyć kodu przygotowanego przed eventem?
  8. Szablon w repo (`szablon-aplikacja/input/case1`) ma „negatywny przyklad.pdf” (ogłoszenie TED) bez pliku wynikowego, a oczekiwany `przyklad odwolanie.json` jest pusty: czy dla dokumentu spoza 3 klas mamy nie tworzyć żadnego pliku? Czy przykładowe wartości w `oczekiwane-json/odwolanie.json` to prawda referencyjna dla tego zeskanowanego odwołania?
  9. Czy realne sprawy testowe mają tę samą strukturę wejścia (jeden odwołanie, ≥1 pełnomocnictwo, przelew na sprawę), czy mogą zawierać inne dokumenty (np. dowody, załączniki), które mamy pominąć?
- **Opcje:** A) ktoś z drużyny pyta na stoisku UZP i wpisuje odpowiedzi tutaj B) pytamy na Discordzie wyzwania
- **Rekomendacja:** A — odpowiedź od razu; do tego czasu budujemy ścieżkę bez LLM (D-005), lokalną sprawdzarkę z naszą definicją F1 (pola-liście, lekka normalizacja) i obsługujemy obie konwencje nazw plików.
- **Blokuje:** ostateczną definicję F1 w lokalnej sprawdzarce (pyt. 2); wybór hostingu LLM (pyt. 1) — nic z tego nie blokuje startu prac
- **Poziom:** zawsze człowiek
- **Odpowiedź:** —

## Q-003 [open] Wybór koncepcji rozwiązania (ideacja 1)
- **Kontekst:** Ideator dał 5 koncepcji (`.house/reports/ideation-1.md`), researcherzy karty prior-art (`reports/prior-art-I-00N.md`, licencje: `reports/licences.md`), sędzia ocenił je rubryką 50/30/20 (w nawiasie wariant regulaminu 50/50; `reports/ideation-1-judge.md`). Ranking:
  1. **I-001 Recepty** — 3,80 [4,00]. Klasa dokumentu = jeden plik YAML (klasyfikacja, sekcje, pola, normalizatory), jeden silnik dla wszystkich klas. Najbliższe: invoice2data (szablony YAML, MIT). Obrona: polskie normalizatory prawne, dowód dla każdego pola, nowa klasa dodana na żywo bez kodu. Najłatwiejsze do zrobienia, ale „to już istnieje”.
  2. **I-005 Dowód na stronie** — 3,80 [4,00]. Skany i PDF-y cyfrowe → słowa z ramkami; UI rysuje ramkę przy każdym polu, poprawka kliknięciem zapisuje się do konfiguracji. Najbliższe: Docling (MIT), Azure Document Intelligence, Rossum, Label Studio. Obrona: korekta zapisywana do otwartego YAML. Ryzyko: pracochłonne.
  3. **I-004 Schemat UZP jako prompt + LLM z weryfikacją** — 3,50. Konfiguracją są skomentowane schematy UZP, otwarty model (Bielik-1.5B, Apache-2.0) poprawia tylko niepewne pola, weryfikator przyjmuje tylko wartości znalezione w tekście. Najbliższe: NuMind (YC S22), LangExtract, ContextGem. Ryzyko: wysoka „wtórność” i zależność od tego, czy sprawdzarka ma LLM.
  4. **I-002 Sprawa jako graf** — 3,20. Głosowanie wartości między dokumentami sprawy, sumy kontrolne do naprawy OCR, kontrola formalna dla urzędnika KIO. Najbliższe: Parsewise (YC S25), Splink (MIT). Uwaga sędziego: pomysł „za niska opłata” odpada — wszystkie 60 przelewów to opłata skarbowa od pełnomocnictwa (sprawdzone), nie wpis; trzymają się tylko kontrole spójności (mocodawca = odwołujący, numer sprawy w tytule przelewu).
  5. **I-003 Naucz na przykładach** — 2,80. Konfiguracja generowana z 5–10 par PDF+JSON. Najbliższe: Azure custom models, indukcja wrapperów (WIEN). Do odłożenia.
- **Opcje:** A) połączenie wg sędziego: chudy silnik recept I-001 na jednym modelu „słowa + ramki” z I-005 (OCR dla skanów), lekka spójność między dokumentami z I-002, LLM z I-004 tylko jako dodatek wyłączony domyślnie (szacunek sędziego 4,3 [4,5]); B) samo I-001 (najszybciej, najmniej „wow”); C) I-004 jako rdzeń (LLM-first z regułami jako podłogą); D) inny wybór / zmiany
- **Rekomendacja:** A — I-001 daje pewny wynik F1 i elastyczność przez konfigurację, model słów z ramkami jest konieczny i tak (skany), a dowód na stronie i spójność dają przejrzystość, za którą UZP wprost daje punkty. Kolejność cięcia pod presją czasu: klik-korekta → LLM → ramki na obrazie strony → edytor w przeglądarce.
- **Blokuje:** planowanie (T001 kontrakt + szkielet, T002 sprawdzarka F1 z podziałem 01–40 / 41–60, T003 wczytywanie z OCR — wszystkie trzy niezależne)
- **Poziom:** krytyczny
- **Termin:** 2026-11-21 14:30
- **Domyślnie:** A
- **Odpowiedź:** —
