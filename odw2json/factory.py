"""Default component wiring. Later tasks switch these from stubs to the real modules."""
from __future__ import annotations

from .model import Classifier, Extractor, Ingestor


def default_ingestor() -> Ingestor:
    from .stubs import PdfplumberIngestor  # T003 replaces

    return PdfplumberIngestor()


def default_classifier() -> Classifier:
    from .stubs import KeywordClassifier  # T004 replaces

    return KeywordClassifier()


def default_extractor() -> Extractor:
    from .stubs import SkeletonExtractor  # T004 replaces

    return SkeletonExtractor()
