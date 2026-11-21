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
- **Kontekst:** Intake ODWOŁANIA2JSON wypełnił `spec.yaml` z decku UZP i postów na Discordzie. Propozycje coordinatora (do zatwierdzenia): (1) mapowanie poziomów rubryki: F1 → 1 = <0,5, 3 ≈ 0,75, 5 ≥ 0,9 na naszych odłożonych zestawach; elastyczność → 1 = typy zaszyte w kodzie, 3 = nowe pole przez konfigurację, 5 = nowy typ dokumentu wyłącznie konfiguracją + dowód dla każdego pola (strona/fragment/pewność) w UI; (2) lokalna sprawdzarka `python eval/score.py --pred out/ --gold data/` drukująca `score: <F1>`, budowana jako pierwsze zadanie; (3) kamienie: sob 18:00 golden path (komenda → JSON-y + F1 na 39 zestawach, świeży klon na Pythonie 3.13 bez GPU), nd 00:00 runda sędziego, nd 09:30 zamrożenie funkcji, nd 10:30 zgłoszenie na Hacktribe; (4) tryb `copilot`, maks. 3 agentów równolegle.
- **Opcje:** A) zatwierdzam wszystko B) zatwierdzam z poprawkami (napisz które)
- **Rekomendacja:** A — wartości wynikają wprost z decku; po publikacji pełnej treści o 11:00 i tak przejdą korektę.
- **Blokuje:** nic (planowanie rusza na tych wartościach)
- **Poziom:** krytyczny
- **Termin:** 2026-11-21 12:00
- **Domyślnie:** A
- **Odpowiedź:** —

## Q-002 [open] Pytania do UZP (stoisko / Discord) przed zamrożeniem architektury
- **Kontekst:** Ogólny regulamin nie mówi nic o AI/LLM/open source; regulaminu zadania jeszcze nie ma (strona nie odpowiadała, repo UZP z danymi niewidoczne przed 11:00). Najważniejsze niejasności zmieniają architekturę: (1) czy „LLM po API” (deck) oznacza, że wolno użyć hostowanego modelu komercyjnego mimo wymogu „wyłącznie komponenty open source”, czy tylko otwarte modele (np. lokalnie na CPU / otwarte wagi przez API)? (2) dokładna definicja F1 (per pole? exact match? normalizacja dat/kwot/NIP? listy i null?) i kontrakt sprawdzarki (komenda, układ katalogów wejścia/wyjścia, nazwy plików, limity czasu); (3) skąd słowniki ID typu `czynnosc_powod_id`; (4) czy regulamin zadania przenosi prawa autorskie na UZP. Pełna lista 10 pytań: `.house/reports/rules-check.md`.
- **Opcje:** A) ktoś z drużyny pyta na stoisku UZP po 11:00 i wpisuje odpowiedzi tutaj B) pytamy na Discordzie wyzwania
- **Rekomendacja:** A — odpowiedź od razu; do tego czasu budujemy ścieżkę bez zależności od decyzji (parser PDF, klasyfikacja, sprawdzarka F1) i trzymamy LLM za wymiennym adapterem.
- **Blokuje:** wybór silnika ekstrakcji (LLM vs reguły), lokalna sprawdzarka F1
- **Poziom:** zawsze człowiek
- **Odpowiedź:** —
