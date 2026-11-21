"""Check an ./output tree against ./input (coordinator-owned acceptance helper; workers never edit).

usage: output_shape.py <input_dir> <output_dir> [--expect-reject NAME ...]
- every input PDF not listed in --expect-reject must have <output>/<case>/<basename>.json
- every listed PDF must have NO json
- each json must have exactly the key structure of one of the three UZP reference schemas
  (lists: every item has the keys of the reference item); values are not checked
Prints "ok: N files" and exits 0, or lists problems and exits 1.
"""
import json
import os
import re
import sys
from pathlib import Path

SCHEMAS = Path(os.environ.get("UZP_DATA", "C:/Users/jasiu/workspace/uzp-data")) / "oczekiwane-json"  # teammates: set UZP_DATA


def load_commented(path: Path):
    lines = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if "//" in line and "http" not in line:
            line = line[: line.index("//")]
        lines.append(line.rstrip())
    text = "\n".join(lines)
    text = re.sub(r'("|\d|null)\s*\n(\s*")', r"\1,\n\2", text)  # add commas lost with the comments
    text = re.sub(r",(\s*[}\]])", r"\1", text)
    text = re.sub(r",\s*,", ",", text)
    return json.loads(text)


def shape(v):
    if isinstance(v, dict):
        return {k: shape(x) for k, x in v.items()}
    if isinstance(v, list):
        return [shape(v[0])] if v else []
    return None


def same(a, b, path, probs):
    if isinstance(b, dict):
        if not isinstance(a, dict):
            probs.append(f"{path}: expected object")
            return
        if set(a) != set(b):
            probs.append(f"{path}: keys {sorted(set(a) ^ set(b))} differ")
        for k in set(a) & set(b):
            same(a[k], b[k], f"{path}.{k}", probs)
    elif isinstance(b, list):
        if not isinstance(a, list):
            probs.append(f"{path}: expected list")
            return
        for i, item in enumerate(a):
            same(item, b[0], f"{path}[{i}]", probs)
    elif isinstance(a, (dict, list)):
        probs.append(f"{path}: expected scalar or null")


def _diff(data, ref) -> list[str]:
    p: list[str] = []
    same(data, ref, "", p)
    return p


def expected_class(name: str) -> str | None:
    """Class implied by a training/template file name (--check-class); None = unknown."""
    n = name.lower()
    if "przelew" in n:
        return "przelew"
    if "pelnomocnictwo" in n or "pełnomocnictwo" in n:
        return "pelnomocnictwo"
    if "odwolanie" in n or "odwołanie" in n:
        return "odwolanie"
    return None


def main() -> None:
    inp, outp = Path(sys.argv[1]), Path(sys.argv[2])
    rejects = set(sys.argv[sys.argv.index("--expect-reject") + 1 :]) if "--expect-reject" in sys.argv else set()
    refs = {p.stem: shape(load_commented(p)) for p in SCHEMAS.glob("*.json")}
    probs: list[str] = []
    n = 0
    for pdf in sorted(inp.glob("*/*.pdf")):
        js = outp / pdf.parent.name / (pdf.stem + ".json")
        if pdf.name in rejects:
            if js.exists():
                probs.append(f"{js}: should not exist (reject)")
            continue
        if not js.exists():
            probs.append(f"{js}: missing")
            continue
        data = json.loads(js.read_text(encoding="utf-8"))
        best = None
        for name, ref in refs.items():
            p: list[str] = []
            same(data, ref, name, p)
            if best is None or len(p) < len(best):
                best = p
        probs += [f"{js}: {x}" for x in best[:3]]
        if "--check-class" in sys.argv:
            want = expected_class(pdf.name)
            got = min(refs, key=lambda name: len(_diff(data, refs[name])))
            if want and got != want:
                probs.append(f"{js}: classified as {got}, expected {want}")
        n += 1
    if probs:
        print("\n".join(probs[:40]))
        print(f"FAIL: {len(probs)} problems")
        sys.exit(1)
    print(f"ok: {n} files")


if __name__ == "__main__":
    main()
