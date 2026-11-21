"""Schema-complete JSON writer: every output has all keys of the UZP schema for its class (null = unknown)."""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"
CLASSES = ("odwolanie", "pelnomocnictwo", "przelew")

_cache: dict[str, Any] = {}


def skeleton(doc_class: str) -> Any:
    """Fresh copy of the null skeleton for a class. Raises KeyError for unknown classes."""
    if doc_class not in CLASSES:
        raise KeyError(doc_class)
    if doc_class not in _cache:
        _cache[doc_class] = json.loads((SCHEMA_DIR / f"{doc_class}.json").read_text(encoding="utf-8"))
    return copy.deepcopy(_cache[doc_class])


def _fill(value: Any, template: Any) -> Any:
    if isinstance(template, dict):
        src = value if isinstance(value, dict) else {}
        return {k: _fill(src.get(k), t) for k, t in template.items()}
    if isinstance(template, list):
        item_t = template[0]
        items = value if isinstance(value, list) and value else [None]
        return [_fill(i, item_t) for i in items]
    return None if isinstance(value, (dict, list)) else value


def complete(data: dict[str, Any], doc_class: str) -> dict[str, Any]:
    """Return data reshaped to the class schema: missing keys -> null, unknown keys dropped,
    lists keep every item (completed) and get one all-null item when empty."""
    return _fill(data, skeleton(doc_class))


def write_json(path: str | Path, data: Any) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return p
