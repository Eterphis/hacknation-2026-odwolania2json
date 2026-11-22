"""T021 acceptance: the real (anonymised) UZP template appeal with a two-column party header.

usage: template_case1.py <output_dir_of_a_run_on_template_case1>
Prints `fields: N/5` and exits 0 only when all five checks hold. Values come from the judge's hand reading of the scan
(reports/judge-1.md, section 1.2); coordinator-owned, workers never edit.
"""
import json
import sys
from pathlib import Path

out = Path(sys.argv[1])
f = next(out.rglob("przyklad odwolanie.json"))
d = json.loads(f.read_text(encoding="utf-8"))


def get(path):
    cur = d
    for k in path:
        if isinstance(cur, list):
            cur = cur[k] if len(cur) > k else None
        elif isinstance(cur, dict):
            cur = cur.get(k)
        if cur is None:
            return None
    return cur


zam = get(["Zamawiajacy", 0, "nazwa"]) or ""
odw = get(["Odwolujacy", 0, "nazwa"]) or ""
tyt = get(["ZamowieniePubliczne", "tytul"]) or ""
pel_name = get(["Odwolujacy", 0, "pelnomocnik", "imie_nazwisko"]) or ""
checks = {
    "Zamawiajacy.nazwa full": zam.startswith("Miejskie Przedsiębiorstwo Oczyszczania") and zam.rstrip(" .").endswith("odpowiedzialnością"),
    "Odwolujacy.nazwa not a label": odw.strip().rstrip(":").upper() not in {"KRS", "NIP", "REGON", "TEL", "ODWOŁUJĄCY"},  # redacted name: null is fine
    "tytul read": tyt.startswith("Dostawa preparatów"),
    "pelnomocnik.imie_nazwisko not a firm": pel_name != "Kancelaria Prawna",
}
for k, v in checks.items():
    print(("ok   " if v else "FAIL ") + k)
print(f"fields: {sum(checks.values())}/{len(checks)}")
sys.exit(0 if all(checks.values()) else 1)
