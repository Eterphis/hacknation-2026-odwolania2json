"""Build an ./input tree from the UZP training data for acceptance checks (coordinator-owned; workers never edit).

usage: prep_input.py <dest_input_dir> <case spec> [--template]
  case spec: "01-60", "41-60" or "07,23"; cases are copied as <dest>/przyklad_NN/*.pdf
  --template also copies uzp-data/szablon-aplikacja/input/case1 as <dest>/template_case1
"""
import os
import shutil
import sys
from pathlib import Path

DATA = Path(os.environ.get("UZP_DATA", "C:/Users/jasiu/workspace/uzp-data"))  # teammates: set UZP_DATA


def cases(spec: str) -> list[str]:
    out: list[str] = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            out += [f"{i:02d}" for i in range(int(a), int(b) + 1)]
        else:
            out.append(f"{int(part):02d}")
    return out


def main() -> None:
    dest = Path(sys.argv[1])
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    n = 0
    for c in cases(sys.argv[2]):
        src = DATA / "dane" / f"przyklad_{c}"
        dst = dest / f"przyklad_{c}"
        dst.mkdir()
        for pdf in src.glob("*.pdf"):
            shutil.copy2(pdf, dst / pdf.name)
            n += 1
    if "--template" in sys.argv:
        dst = dest / "template_case1"
        dst.mkdir()
        for pdf in (DATA / "szablon-aplikacja" / "input" / "case1").glob("*.pdf"):
            shutil.copy2(pdf, dst / pdf.name)
            n += 1
    print(f"copied {n} pdfs to {dest}")


if __name__ == "__main__":
    main()
