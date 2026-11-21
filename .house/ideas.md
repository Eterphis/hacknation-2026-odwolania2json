# Archiwum pomysłów

Każdy pomysł raz. Ideator sprawdza ten plik, zanim cokolwiek zaproponuje — nie wracamy do wypróbowanych
pomysłów bez nowego argumentu.

| ID | Pomysł | Najbliższe istniejące | Status | Wynik / dlaczego | Raport |
|---|---|---|---|---|---|
<!-- status: proposed | chosen | trying | worked | failed | rejected | parked -->
| I-001 | Recepty: każda klasa dokumentu to plik YAML (klasyfikacja, sekcje, pola z kotwicami, normalizatory); jeden generyczny silnik, nowa klasa bez kodu | invoice2data (szablony YAML, MIT wg PyPI) | proposed | — | reports/ideation-1.md |
| I-002 | Sprawa jako graf: wzmianki z wszystkich PDF-ów sprawy, rozpoznanie ról i głosowanie między dokumentami + sumy kontrolne (naprawa OCR); produkt = automatyczna kontrola formalna odwołania (wpis, termin, umocowanie) | Parsewise (YC S25, multi-doc); Splink (MIT) do łączenia encji | proposed | — | reports/ideation-1.md |
| I-003 | Naucz na przykładach: indukcja czytelnej konfiguracji ekstrakcji z 5-10 par PDF + JSON (dopasowanie wartości, uogólnienie etykiet, opcjonalnie CRF), z CV F1 per pole | Azure Document Intelligence custom models; WIEN (Kushmerick 1997) | proposed | — | reports/ideation-1.md |
| I-004 | Schemat UZP jako prompt: komentowany oczekiwane-json = konfiguracja klasy; reguły zawsze dają pełny JSON, otwarty polski LLM (Bielik/PLLuM, Apache-2.0) poprawia tylko pola o niskiej pewności, weryfikator przyjmuje wyłącznie wartości obecne w tekście | NuMind (YC S22, komercyjny), ContextGem (Apache-2.0) i Google LangExtract (Apache-2.0) = LLM z dowodem źródła; ryzyko nowości wysokie (reports/prior-art-I-004.md) | proposed | — | reports/ideation-1.md |
| I-005 | Dowód na stronie: wspólny model „słowa z ramkami” dla skanów i PDF-ów cyfrowych, ekstrakcja po geometrii (etykieta obok/nad wartością), podgląd ramek dowodu na obrazie strony i poprawka klikiem zapisywana do konfiguracji | Docling (MIT, layout), Azure Document Intelligence i Rossum (komercyjne, podgląd na stronie), Label Studio (Apache-2.0, korekta); ryzyko nowości średnio-wysokie (reports/prior-art-I-005.md) | proposed | — | reports/ideation-1.md |
