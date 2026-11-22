# Ślad: scenariusz pitchu (5 minut + 5 minut pytań)

Etap II, 22.11.2026, 15:15. Wyzwanie UZP "Odwołania2json". Język: polski. Slajdy: `slides.html` (strzałki, jeden slajd na sekcję).
Demo na żywo prowadzi się według `demo-plan.md`. Kryteria w nawiasach to rubryka z `spec.yaml`: F1 (waga 0,5), elastyczność i
rozbudowa (0,3), architektura i jakość techniczna (0,2); regulamin zadania mówi 50/50 dla F1 i elastyczności, więc obie
części musi być słychać wyraźnie.

## Liczby do podmiany (jedno miejsce)

Liczby z gwiazdką zmieniają się po dwóch ostatnich scaleniach. Po aktualizacji podmień je tutaj, w `slides.html`
(obiekt `NUMS` na początku skryptu, jedno miejsce) i w odpowiedziach na pytania poniżej.

| Klucz | Wartość | Co to jest |
|---|---|---|
| `skany` | 0,9789 | dokładne F1, 30 skanów UZP (`dane/skany`), główna miara, najbliższa prawdziwemu testowi (reguły powstały też z analizy pomyłek na tych skanach) |
| `skany_odw` | 0,9943 | to samo, tylko odwołania |
| `skany_pel` | 0,9677 | to samo, tylko pełnomocnictwa |
| `skany_prz` | 0,9444 | to samo, tylko potwierdzenia przelewu |
| `heldout` | 1,000 | przykłady 41-60 (odłożone; pełnomocnictwa częściowo oglądane przy strojeniu, D-014) |
| `dev` | 1,000 | przykłady 01-40 (strojenie reguł) |
| `negatywne` | 12/12 | dokumentów spoza klas odrzuconych (dostają `{}`) |
| czas OCR | ok. 6 s | mediana na dokument, OCR na zimno (`docs/PROFILES.md`) |

Zasada na scenie: skany są naszą główną liczbą, bo UZP testuje na prawdziwych, częściowo skanowanych sprawach. Wynik
1,000 na zbiorach syntetycznych mówimy jednym zdaniem i od razu z zastrzeżeniem (patrz sekcja 4).

---

## 1. Problem (0:00-0:30, 30 s). Slajd 1

Cel: jury rozumie, komu i co dajemy. (Kryteria: wstęp do wszystkich trzech.)

> Sprawa odwoławcza do KIO to kilka PDF-ów: odwołanie, pełnomocnictwo, potwierdzenie wpisu. Dane z nich trzeba
> odczytać i wpisać do systemu: kto odwołuje się od czego, kto go reprezentuje, czy wpis został wniesiony. Dziś robi to
> człowiek, a część dokumentów to skany.
>
> My nazwaliśmy to rozwiązanie Ślad. Ślad dostaje folder ze sprawą i oddaje po jednym JSON-ie na dokument. Przy każdej
> wartości zostawia ślad: stronę, fragment tekstu, regułę i pewność. Urzędnik nie musi nam wierzyć na słowo, bo każdą
> liczbę może sprawdzić w dokumencie w kilka sekund.

Przejście: "Pokażę to na prawdziwym przebiegu."

## 2. Demo na żywo, część A: sprawa i transparentność (0:30-1:40, 70 s). Slajd 2, potem przeglądarka

Kryteria: F1 (widać poprawne wartości na żywo), elastyczność i przejrzystość (tabela dowodów, premiowane przez UZP).
Kroki klik po kliku: `demo-plan.md`, część A.

> Wgrywam sprawę przyklad_07: odwołanie, pełnomocnictwo i potwierdzenie przelewu. Dokładam czwarty plik, ogłoszenie
> TED, które do żadnej z trzech klas nie należy. Klasę rozpoznajemy tylko po treści, nazwa pliku nic nie znaczy.
>
> Trzy dokumenty rozpoznane z punktacją klas, czwarty odrzucony: dostaje pusty JSON, tak jak chce kontrakt UZP.
>
> Otwieram odwołanie. Tu jest tabela dowodów: pole, wartość, strona, fragment źródła z zaznaczoną wartością, reguła i
> pewność. NIP Odwołującego ma pewność jeden, bo przeszedł sumę kontrolną. Gdyby nie przeszedł, pewność spadłaby do 0,5, ale
> wartość zostaje taka, jak w dokumencie. Niczego nie poprawiamy po cichu.
>
> A tu sprawdzenie spójności sprawy: NIP mocodawcy z pełnomocnictwa zgadza się z NIP-em Odwołującego, numer postępowania
> jest w tytule przelewu. To informacja dla człowieka, nie przeróbka wyniku.

Jeśli zostało czasu (opcjonalnie, 10 s): wgrać skan `przyklad odwolanie.pdf` (OCR, 7 stron; po rozgrzaniu cache wynik od ręki) i
powiedzieć: "To jest skan bez warstwy tekstowej, czyta go OCR, a tabela dowodów wygląda tak samo."

## 3. Demo na żywo, część B: nowa klasa dokumentu bez programowania (1:40-2:40, 60 s). Slajd 3, potem przeglądarka

Kryteria: elastyczność i rozbudowa (waga 0,3, to jest ten moment, który ją zdobywa), architektura (YAML zamiast kodu).

> Teraz to, o co pytacie w zadaniu: nowy rodzaj dokumentu bez przebudowy systemu. Zakładka "Klasy dokumentów", "Nowa klasa z
> szablonu". Dostaję komentowaną recepturę: sygnały rozpoznania i pola z gotowymi strategiami. Zmieniam nazwę na "wezwanie".
>
> "Wypróbuj na PDF": wskazuję wezwanie do zapłaty, którego system nigdy nie widział. Jest rozpoznane jako nowa klasa, kwota
> i termin wyciągnięte, każde z fragmentem źródła. Nic jeszcze nie zapisałem. Gdyby wzorzec był zły, "Sprawdź" wskaże linię
> pliku i ścieżkę błędu.
>
> "Zapisz". Teraz ta sama klasa działa w linii poleceń, bez restartu: kopiuję PDF do `input` i uruchamiam `start.bat`. W
> `output` jest JSON z kwotą i terminem. Nikt nie ruszył kodu w Pythonie.

Uwaga dla prowadzącego: po części B usunąć klasę z interfejsu (klawisz "Usuń"), żeby repozytorium wróciło do trzech klas.

## 4. Jak to działa i dlaczego można temu ufać (2:40-3:20, 40 s). Slajd 4 (diagram)

Kryteria: architektura i jakość techniczna (0,2), transparentność. Jeden diagram: PDF, odczyt (warstwa tekstu albo OCR), klasyfikacja po treści,
ekstrakcja z receptur YAML, JSON plus dowody.

> Architektura jest prosta i ma jeden kontrakt: strona to słowa z ramkami, niezależnie od tego, czy przyszły z warstwy
> tekstu PDF, czy z OCR. Dalej klasyfikator i ekstraktor sterują się wyłącznie plikami YAML. W kodzie silnika nie ma
> nazw klas, a test akceptacyjny to sprawdza grepem.
>
> Domyślnie nie ma tu żadnego modelu językowego. Reguły są deterministyczne, działają lokalnie na CPU, na laptopie z 16 GB bez
> GPU, i dane nie opuszczają komputera. Opcjonalnie włączamy mały lokalny model, Qwen3-1.7B na licencji Apache-2.0, ale tylko jako
> czytelnika pól, których reguły nie odczytały. Wartość od modelu przyjmujemy wyłącznie wtedy, gdy cytat, który podał, istnieje w
> tekście strony. Inaczej odrzucamy.

## 5. Jakość: liczby i uczciwe zastrzeżenia (3:20-4:00, 40 s). Slajd 5

Kryteria: F1 (waga 0,5). Tu liczy się wiarygodność, więc mówimy najpierw o skanach.

> Mierzymy własnym miernikiem: F1 na poziomie pól, dokładne porównanie wartości. Główna miara to trzydzieści skanów od UZP,
> bo to najbliżej prawdziwego testu: F1 `{skany}`. Odwołania `{skany_odw}`, pełnomocnictwa `{skany_pel}`, przelewy `{skany_prz}`.
> Dwanaście dokumentów spoza klas, dwanaście odrzuconych.
>
> Na zbiorach syntetycznych mamy 1,000, ale to mówię z zastrzeżeniem: reguły stroiliśmy na przykładach 01-40, a układ
> pełnomocnictw z 41-60 oglądaliśmy przy strojeniu, więc ten wynik traktujemy jako zawyżony. Dlatego decyzji nie opieramy na
> nim, tylko na skanach. Znamy też nasze pomyłki i mamy je spisane, do nich wrócę w pytaniach.

## 6. Rozbudowa i komponenty zewnętrzne (4:00-4:30, 30 s). Slajd 6

Kryteria: elastyczność (0,3), architektura (0,2), wymóg regulaminu §4.1 (wymienić komponenty zewnętrzne).

> Nowa klasa to jeden plik YAML, także z interfejsu. Dla UZP to podstawa pod uniwersalne narzędzie PDF do danych, o którym
> mówi zadanie: ta sama maszyna, inne receptury.
>
> Komponenty zewnętrzne, wszystkie na licencjach permisywnych: pdfplumber (MIT), RapidOCR z modelami PP-OCR na ONNX Runtime
> (Apache-2.0 i MIT), pypdfium2, FastAPI (MIT), opcjonalnie Qwen3-1.7B (Apache-2.0) z llama.cpp (MIT). Świadomie odrzuciliśmy
> PyMuPDF i Ghostscript na AGPL oraz modele spaCy na GPL, żeby przekazanie praw do UZP było czyste. Pełna lista jest w
> `docs/EXTERNAL_COMPONENTS.md`.

## 7. Prośba (4:30-5:00, 30 s). Slajd 7

> Prosimy o trzy rzeczy. Pierwsza: dajcie nam prawdziwe skany, na których to złamie się szybciej niż na naszych, bo każdy taki
> przypadek to nowa reguła w YAML-u, nie przepisywanie kodu. Druga: potraktujcie Ślad jako bazę pod pilotaż w UZP, całość jest
> w repozytorium, z Docker Compose, dokumentacją architektury i opisem dodawania klasy. Trzecia: wskażcie następny typ pisma z
> waszych spraw, a pokażemy, ile zajmuje jego dodanie.
>
> Ślad: każda wartość ma swój ślad. Dziękujemy.

Repozytorium: https://github.com/Eterphis/slad

---

## Plan awaryjny w skrócie

Jeśli demo się wywróci: patrz `demo-plan.md`, sekcja "Plan B". Zdania, które można powiedzieć bez przeglądarki, siedzą na slajdach 2-3
(zrzuty ekranu z `docs/screenshots/` można wstawić do `slides.html` zamiast żywego demo).

---

## 10 prawdopodobnych pytań jury

**1. Czy wszystkie komponenty mają licencje, które pozwalają przekazać rozwiązanie UZP?**
Tak. Tylko licencje permisywne (MIT, Apache-2.0, BSD, OFL dla fontów), zero AGPL i GPL. Odrzuciliśmy PyMuPDF i Ghostscript
(AGPL) oraz modele spaCy `pl_core_news_*` (GPL). Lista z wersjami i linkami: `docs/EXTERNAL_COMPONENTS.md`. System wizualny
Cold Trace i logo Eterphis to nasz własny projekt. Przeniesienie praw majątkowych według §4 regulaminu: `[potwierdzić ze
zespołem, że wszyscy współautorzy podpiszą]`.

**2. Czy używacie LLM? Jakiego, i co z danymi?**
Domyślnie nie. Pełny wynik daje ścieżka regułowa. Profil `llm` jest opcjonalny: lokalny Qwen3-1.7B (Apache-2.0, GGUF, llama.cpp
na CPU, około 3 GB RAM), bez żadnego zewnętrznego API i bez wysyłania danych. Model przepisuje wartość razem z cytatem, a my
przyjmujemy ją tylko, gdy cytat jest w tekście strony; nigdy nie nadpisujemy wartości odczytanej regułą z pełną pewnością.
Wagi (1,8 GB) pobierają się raz przy pierwszym użyciu, potem działa offline. Zmierzyliśmy też koszt: 1-3 minuty na wywołanie na
laptopie bez GPU, więc profil jest wyłączony domyślnie.

**3. Dlaczego LLM nie jest domyślny, skoro dałby elastyczność?**
Bo na naszych zbiorach prawie nic nie dokłada, a kosztuje czas i pamięć. Zysk na skanach był rzędu +0,007 F1 (przed ostatnimi
poprawkami reguł, teraz bliski zerowi), a p95 czasu rośnie z ułamka sekundy do ponad dwóch minut na dokument. Zostawiamy go jako
opt-in z receptury (`llm:`), działający także dla nowych klas, bo przy zmienionym układzie dokumentów może się przydać.
Mentorzy UZP potwierdzili, że rozwiązanie bez LLM i z lokalnym LLM dostaje to samo maksimum punktów w tej kategorii.

**4. Jak to się zachowa na prawdziwych sprawach, które wyglądają inaczej niż wasze dane?**
Nie wiemy na pewno, i mówimy to wprost. Dlatego główną miarą są skany UZP (`dane/skany`), a nie przykłady syntetyczne, a recepty
opierają się na etykietach i strukturze (sekcje, kolumny, sumy kontrolne), nie na pozycji w pliku. Mamy też zaszumiony zbiór do
testu OCR (`eval/make_noisy.py`). Gdy układ się zmieni, poprawka to linia w YAML-u, a w tabeli dowodów od razu widać, które
pole zawiodło i na jakim fragmencie.

**5. Jak dodać nową klasę dokumentu? Ile to trwa?**
Jeden plik YAML w `recipes/` (sygnały klasyfikacji, pola, strategie, normalizatory, walidatory) i opcjonalnie szkielet JSON.
Silnik wczytuje go przy następnym dokumencie, bez restartu. Interfejs ma edytor: szablon, walidacja z numerem linii, próba na PDF
bez zapisywania, zapis. Dziś pokazaliśmy to w około minutę. Opis: `docs/ADDING_A_DOCUMENT_CLASS.md`. Gdy wbudowane strategie nie
wystarczą, programista dopisuje strategię (`register_strategy`), a jej nazwa jest od razu dostępna w YAML.

**6. Jakich pomyłek jesteście świadomi?**
Z analizy 20 pomyłek (`reports/misses-1.md`) naprawiliśmy większość regułami (PESEL przy pełnomocniku, koniec sekcji Odwołującego,
duplikaty i sklejone imiona). Linie gubione przez OCR przez prześwitujący druk z drugiej strony skanu czytamy drugi raz po oczyszczeniu obrazu (tylko
zaszumione pasy strony, +23% czasu OCR); to odzyskało numer postępowania i BZP w skanie 0005. Zostały: tytuł przelewu
zniekształcony przez słaby druk (OCR nie odzyskuje go żadnym wariantem), konsorcjum, gdzie nie czytamy podpisującego drugiego członka, mocodawca jako osoba fizyczna prowadząca działalność, oraz prefiks
`PL` w numerze rachunku: w skanach UZP złoty JSON go zachowuje, w danych syntetycznych nie, więc wybraliśmy konwencję
syntetyczną i zapytaliśmy mentorów.

**7. Czy da się to wystawić jako usługę, gdzie to działa?**
Tak, ale świadomie w trybie lokalnym. Lokalnie: `start.bat web` albo `docker compose up --build`, na CPU, w 16 GB RAM, bez GPU i
bez sieci (poza jednorazowym pobraniem wag modelu, jeśli ktoś włączy profil `llm`). Pierwsze uruchomienie instaluje zależności
(kilka minut), kolejne trwa około minuty. Publiczna instancja: `[wpisać, czy jest i pod jakim adresem; jeśli nie ma, powiedzieć:
nie wystawiamy jej, bo dokumenty spraw nie powinny opuszczać urzędu]`. Darmowe instancje w chmurze mają około 1 GB RAM, więc
tam uruchomilibyśmy tylko lekki profil `text`, bez OCR.

**8. Bezpieczeństwo i prywatność: co się dzieje z wgranymi dokumentami?**
Nic nie wychodzi poza maszynę: brak zewnętrznych API, brak telemetrii, fonty hostowane lokalnie, interfejs działa offline.
`start.bat web` nasłuchuje na 127.0.0.1. Interfejs nie ma uwierzytelniania, bo to narzędzie lokalne; na serwerze współdzielonym
trzeba je postawić za zwrotnym proxy organizacji. Zapis receptur można zablokować zmienną `ODW2JSON_READONLY_RECIPES=1`. Kolejne kroki
przed produkcją to uwierzytelnianie i polityka przechowywania wgranych plików, których nie robiliśmy w ciągu doby hackathonu.

**9. Skąd wiecie, że wynik jest poprawny? Co z walidacją danych?**
Trzy warstwy. Sumy kontrolne NIP, REGON, PESEL, KRS i IBAN obniżają pewność pola do 0,5, ale wartość zostaje taka, jak w
dokumencie. Spójność między dokumentami sprawy (NIP mocodawcy i Odwołującego, numer postępowania w tytule przelewu) widać jako
informację w interfejsie, nigdy jako zmianę wyniku. A przy każdej wartości jest fragment źródła, więc człowiek sprawdza w sekundę. Dla
brakującego pola zwracamy `null`, tak jak złote JSON-y UZP.

**10. Co dalej, jeśli wygracie? Co z rozwojem i utrzymaniem?**
Repozytorium zawiera wszystko, co regulamin każe przekazać: kod, instrukcję uruchomienia, Docker Compose, dokumentację architektury,
opis konfiguracji klasy i dodawania nowej. Kolejny krok to pilotaż na prawdziwych sprawach UZP: zbieramy przypadki, które zawodzą,
dodajemy reguły w YAML-u i mierzymy `eval.score` oraz `eval.bench` z bramką regresji, żeby poprawka jednej klasy nie psuła
innych. Drugi kierunek z zadania to uniwersalne narzędzie PDF do danych: nowe klasy pism UZP dodajemy samym YAML-em.

---

## Do zrobienia przed wejściem na scenę (prowadzący)

- Podmienić liczby z gwiazdką (tabela na górze, `NUMS` w `slides.html`).
- [zrobione] Link do repozytorium w slajdzie 7 i w sekcji 7: https://github.com/Eterphis/slad
- Zdecydować, czy pokazujemy skan z OCR w części A (jest w `demo-plan.md`, krok A7).
- Zrobić nagranie awaryjne (w `demo-plan.md`, Plan B), bo jeszcze go nie ma.
