"""Default component wiring: T003 ingestor (text layer + OCR) and the T004 recipe engine.

The recipes directory comes from env ODW2JSON_RECIPES (the CLI's --recipes sets it), default ./recipes.
The processing profile (`profiles/<name>.yaml`, odw2json/profiles.py) picks the ingestor options: `--profile` >
env ODW2JSON_PROFILE > `ocr`.
"""
from __future__ import annotations

from functools import cache

from .model import Classifier, Extractor, Ingestor


@cache
def ingestor_for(profile: str) -> Ingestor:
    from . import profiles
    from .ingest import default_ingestor as make

    return make(profiles.load_profile(profile).ingest_config())


def default_ingestor() -> Ingestor:
    """Ingestor of the active profile (env ODW2JSON_PROFILE, default `ocr`); an unset env gives today's behaviour."""
    from . import profiles

    return ingestor_for(profiles.resolve_name())


@cache
def recipe_engine():
    """One engine serves as both classifier and extractor (recipes loaded once, reloaded on file change)."""
    from .engine import RecipeEngine

    eng = RecipeEngine()
    eng.recipes  # load eagerly: a broken recipe raises RecipeError here, at startup, not once per document
    return eng


def default_classifier() -> Classifier:
    return recipe_engine()


def default_extractor() -> Extractor:
    return recipe_engine()


def build_components(profile: str | None = None) -> tuple[Ingestor, Classifier, Extractor]:
    """(ingestor, classifier, extractor) for a profile; what every pool worker builds once."""
    from . import profiles

    return ingestor_for(profiles.resolve_name(profile)), default_classifier(), default_extractor()
