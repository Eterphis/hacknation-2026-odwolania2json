"""Default component wiring: T003 ingestor (text layer + OCR) and the T004 recipe engine.

The recipes directory comes from env ODW2JSON_RECIPES (the CLI's --recipes sets it), default ./recipes.
"""
from __future__ import annotations

from functools import cache

from .model import Classifier, Extractor, Ingestor


@cache
def default_ingestor() -> Ingestor:
    from .ingest import default_ingestor as make

    return make()


@cache
def recipe_engine():
    """One engine serves as both classifier and extractor (recipes loaded once, reloaded on file change)."""
    from .engine import RecipeEngine

    return RecipeEngine()


def default_classifier() -> Classifier:
    return recipe_engine()


def default_extractor() -> Extractor:
    return recipe_engine()
