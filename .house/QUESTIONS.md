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
  8. Czy realne sprawy testowe mają tę samą strukturę wejścia (jeden odwołanie, ≥1 pełnomocnictwo, przelew na sprawę), czy mogą zawierać inne dokumenty (np. dowody, załączniki), które mamy pominąć?
- **Opcje:** A) ktoś z drużyny pyta na stoisku UZP i wpisuje odpowiedzi tutaj B) pytamy na Discordzie wyzwania
- **Rekomendacja:** A — odpowiedź od razu; do tego czasu budujemy ścieżkę bez LLM (D-005), lokalną sprawdzarkę z naszą definicją F1 (pola-liście, lekka normalizacja) i obsługujemy obie konwencje nazw plików.
- **Blokuje:** ostateczną definicję F1 w lokalnej sprawdzarce (pyt. 2); wybór hostingu LLM (pyt. 1) — nic z tego nie blokuje startu prac
- **Poziom:** zawsze człowiek
- **Odpowiedź:** —
