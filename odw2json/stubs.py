"""STUBS (T001). Replaced by T003 (ingest: text layer + OCR + word boxes) and T004 (classify/extract recipes)."""
from __future__ import annotations

import re

from .model import Classification, Document, Extraction, Page
from .write import skeleton


class PdfplumberIngestor:
    """STUB: pdfplumber page text only, no OCR, no word boxes."""

    def ingest(self, pdf_path: str) -> Document:
        import pdfplumber

        pages: list[Page] = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, pg in enumerate(pdf.pages, 1):
                pages.append(Page(i, float(pg.width), float(pg.height), [], pg.extract_text() or "", "text"))
        return Document(str(pdf_path), pages)


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


class KeywordClassifier:
    """STUB: keyword scores on the text; rejects when nothing matches."""

    def classify(self, doc: Document) -> Classification:
        t = _norm(doc.text)
        przelew = float("potwierdzenie" in t) + float("przelew" in t)
        odwolanie = float("odwołanie" in t or "odwolanie" in t) + float("krajowej izby" in t)
        scores = {
            "przelew": przelew if przelew >= 2 else 0.0,
            "pelnomocnictwo": 2.0 * float("pełnomocnictw" in t or "pelnomocnictw" in t),
            "odwolanie": odwolanie if odwolanie >= 2 else 0.0,
        }
        best = max(scores, key=lambda k: scores[k])
        if scores[best] <= 0:
            return Classification(None, 0.0, scores, "no keyword matched")
        return Classification(best, scores[best], scores, "keyword stub")


class SkeletonExtractor:
    """STUB: returns the null skeleton."""

    def extract(self, doc: Document, doc_class: str) -> Extraction:
        return Extraction(skeleton(doc_class))
