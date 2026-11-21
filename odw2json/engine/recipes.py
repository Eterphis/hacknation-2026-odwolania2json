"""Load and validate recipes (recipes/*.yaml) and dictionaries (dictionaries/*.yaml)."""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMA_FILE = ROOT / "recipes" / "recipe.schema.json"


class RecipeError(ValueError):
    """A recipe or dictionary file is invalid; the message names the file and the place."""


@dataclass
class Recipe:
    name: str
    path: Path
    spec: dict[str, Any]

    @property
    def classify(self) -> dict[str, Any]:
        return self.spec["classify"]

    @property
    def fields(self) -> list[dict[str, Any]]:
        return self.spec.get("fields") or []

    @property
    def sections(self) -> list[dict[str, Any]]:
        return self.spec.get("sections") or []

    def skeleton(self) -> Any | None:
        """The output skeleton named by output_schema (None = use the writer's schemas/<class>.json)."""
        ref = self.spec.get("output_schema")
        if not ref:
            return None
        for base in (self.path.parent, ROOT):
            p = base / ref
            if p.is_file():
                return json.loads(p.read_text(encoding="utf-8"))
        raise RecipeError(f"{self.path.name}: output_schema {ref!r} not found")


def recipes_dir(explicit: str | os.PathLike | None = None) -> Path:
    """--recipes option > env ODW2JSON_RECIPES > <repo>/recipes."""
    return Path(explicit or os.environ.get("ODW2JSON_RECIPES") or ROOT / "recipes")


def dictionaries_dir(explicit: str | os.PathLike | None = None) -> Path:
    return Path(explicit or os.environ.get("ODW2JSON_DICTIONARIES") or ROOT / "dictionaries")


_validator = None


def _schema_validator():
    global _validator
    if _validator is None:
        _validator = jsonschema.Draft202012Validator(json.loads(SCHEMA_FILE.read_text(encoding="utf-8")))
    return _validator


def _where(err) -> str:
    return "/".join(str(p) for p in err.absolute_path) or "(top level)"


def _check_regexes(spec: Any, where: str, name: str) -> None:
    keys = {"pattern", "start", "end"}
    if isinstance(spec, dict):
        for k, v in spec.items():
            if k in keys and isinstance(v, str) or k == "labels" and isinstance(v, list):
                for pat in v if isinstance(v, list) else [v]:
                    try:
                        re.compile(pat)
                    except re.error as e:
                        raise RecipeError(f"{name}: {where}/{k}: bad regex {pat!r}: {e}") from None
            _check_regexes(v, f"{where}/{k}", name)
    elif isinstance(spec, list):
        for i, v in enumerate(spec):
            if isinstance(v, str) and where.endswith(("forbidden", "required")):
                _check_regexes({"pattern": v}, f"{where}/{i}", name)
            else:
                _check_regexes(v, f"{where}/{i}", name)


def load_recipe(path: Path) -> Recipe:
    try:
        spec = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        raise RecipeError(f"{path.name}: not valid YAML: {e}") from None
    errors = sorted(_schema_validator().iter_errors(spec), key=lambda e: list(e.absolute_path))
    if errors:
        msgs = "; ".join(f"{_where(e)}: {e.message}" for e in errors[:5])
        raise RecipeError(f"{path.name}: {msgs}")
    _check_regexes(spec, "", path.name)
    return Recipe(spec["class"], path, spec)


def load_recipes(directory: str | os.PathLike | None = None) -> list[Recipe]:
    d = recipes_dir(directory)
    recipes = [load_recipe(p) for p in sorted(d.glob("*.yaml")) + sorted(d.glob("*.yml"))]
    names = [r.name for r in recipes]
    dup = {n for n in names if names.count(n) > 1}
    if dup:
        raise RecipeError(f"{d}: class defined twice: {sorted(dup)}")
    return recipes


def load_dictionary(name: str, directory: str | os.PathLike | None = None) -> list[dict[str, Any]]:
    p = dictionaries_dir(directory) / f"{name}.yaml"
    if not p.is_file():
        raise RecipeError(f"dictionary {name!r} not found ({p})")
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    entries = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(entries, list) or not all(isinstance(e, dict) and isinstance(e.get("triggers"), list) for e in entries):
        raise RecipeError(f"{p.name}: expected 'entries: [{{id, label, triggers: [...]}}]'")
    return entries


def signature(directory: Path) -> tuple:
    """Changes when a recipe file is added, removed or edited (engine reloads without a restart)."""
    files = sorted(directory.glob("*.y*ml"))
    return tuple((f.name, f.stat().st_mtime_ns, f.stat().st_size) for f in files)
