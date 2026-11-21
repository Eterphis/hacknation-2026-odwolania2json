"""ingest -> classify -> extract -> write, per case folder."""
from __future__ import annotations

import logging
from pathlib import Path

from . import factory
from .case import apply_case
from .model import CaseResult, Classification, Classifier, DocumentResult, Extractor, Ingestor
from .write import complete, write_json

log = logging.getLogger("odw2json")


def _pdfs(case_dir: Path) -> list[Path]:
    return sorted(p for p in case_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf")


def _process_pdf(pdf: Path, ingestor: Ingestor, classifier: Classifier, extractor: Extractor) -> DocumentResult:
    try:
        doc = ingestor.ingest(str(pdf))
        cls = classifier.classify(doc)
        if cls.doc_class is None:
            return DocumentResult(str(pdf), None, cls, None)
        ext = extractor.extract(doc, cls.doc_class)
        ext.data = complete(ext.data, cls.doc_class)
        return DocumentResult(str(pdf), pdf.stem + ".json", cls, ext)
    except ImportError:  # broken environment, not a bad document: fail loudly
        raise
    except Exception as e:  # one broken PDF must never kill the batch
        log.exception("failed on %s", pdf)
        return DocumentResult(str(pdf), None, Classification(None, 0.0, reason="error"), None, [f"{type(e).__name__}: {e}"])


def process_case(case_dir, ingestor=None, classifier=None, extractor=None) -> CaseResult:
    """Process one case folder; does not write files (the caller decides)."""
    case_dir = Path(case_dir)
    ingestor = ingestor or factory.default_ingestor()
    classifier = classifier or factory.default_classifier()
    extractor = extractor or factory.default_extractor()
    for extra in sorted(p for p in case_dir.rglob("*") if p.is_file() and p.suffix.lower() == ".pdf" and p.parent != case_dir):
        log.warning("skipping %s: PDFs must lie directly in the case folder", extra)
    docs = [_process_pdf(p, ingestor, classifier, extractor) for p in _pdfs(case_dir)]
    return apply_case(CaseResult(case_dir.name, docs))


REJECTED_JSON = ("{}", "empty", "none")


def write_rejected(path: Path, mode: str) -> None:
    """UZP: a document that belongs to no class gets an empty .json ('{}' = valid JSON, 'empty' = 0 bytes)."""
    if mode == "none":
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{}\n" if mode == "{}" else "", encoding="utf-8")


def process_input(input_dir, output_dir, ingestor=None, classifier=None, extractor=None, rejected_json="{}") -> list[CaseResult]:
    """Walk <input>/<case>/*.pdf and write <output>/<case>/<basename>.json for every PDF: the extraction for an
    accepted document, an empty JSON (see `rejected_json`) for a rejected or unreadable one."""
    if rejected_json not in REJECTED_JSON:
        raise ValueError(f"rejected_json must be one of {REJECTED_JSON}")
    input_dir, output_dir = Path(input_dir), Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if not input_dir.is_dir():
        log.warning("input directory %s does not exist", input_dir)
        return []
    ingestor = ingestor or factory.default_ingestor()
    classifier = classifier or factory.default_classifier()
    extractor = extractor or factory.default_extractor()
    for loose in sorted(p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"):
        log.warning("skipping %s: PDFs must lie in <input>/<case>/", loose)
    results: list[CaseResult] = []
    for case_dir in sorted(p for p in input_dir.iterdir() if p.is_dir()):
        res = process_case(case_dir, ingestor, classifier, extractor)
        for d in res.documents:
            if d.output_name and d.extraction is not None:
                write_json(output_dir / res.case / d.output_name, d.extraction.data)
            else:
                write_rejected(output_dir / res.case / (Path(d.input_path).stem + ".json"), rejected_json)
        results.append(res)
    return results
