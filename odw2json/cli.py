from __future__ import annotations

import argparse
import logging
import sys

from .pipeline import process_input


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="odw2json", description="PDF cases -> JSON (UZP contract)")
    ap.add_argument("--input", default="./input", help="folder with <case>/*.pdf (default ./input)")
    ap.add_argument("--output", default="./output", help="folder for <case>/<name>.json (default ./output)")
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    results = process_input(args.input, args.output)
    total = sum(len(r.documents) for r in results)
    written = sum(1 for r in results for d in r.documents if d.output_name)
    print(f"{len(results)} cases, {total} pdfs, {written} json written, {total - written} rejected/failed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
