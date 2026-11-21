from __future__ import annotations

import argparse
import logging
import os
import sys

from . import factory
from .pipeline import process_input


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="odw2json", description="PDF cases -> JSON (UZP contract)")
    ap.add_argument("--input", default="./input", help="folder with <case>/*.pdf (default ./input)")
    ap.add_argument("--output", default="./output", help="folder for <case>/<name>.json (default ./output)")
    ap.add_argument("--recipes", default=None, help="folder with <class>.yaml recipes (default ./recipes or env ODW2JSON_RECIPES)")
    args = ap.parse_args(argv)
    if args.recipes:
        os.environ["ODW2JSON_RECIPES"] = args.recipes
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    from .engine import RecipeError

    try:
        factory.recipe_engine()  # fail loudly before processing anything
    except RecipeError as e:
        print(f"recipe error: {e}", file=sys.stderr)
        return 2
    results = process_input(args.input, args.output)
    total = sum(len(r.documents) for r in results)
    written = sum(1 for r in results for d in r.documents if d.output_name)
    print(f"{len(results)} cases, {total} pdfs, {written} json written, {total - written} rejected/failed")
    failed = sum(1 for r in results for d in r.documents if d.warnings)
    if total and failed == total:
        print("every PDF failed; check the log above (dependencies installed? pip install -r requirements.txt)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
