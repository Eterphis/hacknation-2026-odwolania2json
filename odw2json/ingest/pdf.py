"""PDF -> Document: text-layer words via pdfplumber, per-page OCR fallback via pypdfium2 + an OcrBackend."""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path

from odw2json.model import Document, Page, Word

from .layout import build_text, is_garbage_text
from .ocr import OcrBackend, OcrLine, get_backend

DEFAULT_DPI = 200
DEFAULT_MIN_CONF = 0.6  # OCR lines below this are noise (e.g. black redaction bars read as 'n on nn')
MAX_SIDE_PX = 2400  # cap the rendered bitmap (a 150-dpi A4 scan is already 1240 pt wide)
_CACHE_VERSION = 1


def lines_to_words(lines: list[OcrLine], scale: float, min_conf: float = 0.0) -> list[Word]:
    """Split OCR lines into words; box x-extent is shared out by character count. Pixels -> PDF points."""
    words: list[Word] = []
    for text, (x0, y0, x1, y1), conf in lines:
        parts = text.split()
        if not parts or conf < min_conf:
            continue
        total = sum(len(p) for p in parts) + (len(parts) - 1)
        span = x1 - x0
        cursor = 0
        for p in parts:
            wx0 = x0 + span * cursor / total
            wx1 = x0 + span * (cursor + len(p)) / total
            cursor += len(p) + 1
            words.append(Word(p, wx0 / scale, y0 / scale, wx1 / scale, y1 / scale, max(0.0, min(1.0, conf))))
    return words


def _clamp(words: list[Word], width: float, height: float) -> list[Word]:
    out = []
    for w in words:
        x0 = min(max(w.x0, 0.0), width)
        x1 = min(max(w.x1, x0), width)
        y0 = min(max(w.y0, 0.0), height)
        y1 = min(max(w.y1, y0), height)
        out.append(Word(w.text, x0, y0, x1, y1, w.conf))
    return out


class PdfIngestor:
    def __init__(self, backend: OcrBackend | None = None, config: dict | None = None):
        cfg = dict((config or {}).get("ingest") or {})
        self._config = config
        self._backend = backend
        self.dpi = int(cfg.get("dpi", DEFAULT_DPI))
        self.min_conf = float(((config or {}).get("ocr") or {}).get("min_conf", DEFAULT_MIN_CONF))
        self._backend_id = (
            type(backend).__name__ if backend is not None
            else os.environ.get("ODW2JSON_OCR") or ((config or {}).get("ocr") or {}).get("backend") or "rapidocr"
        )
        self.cache_dir: Path | None = None
        if cfg.get("cache", True):
            self.cache_dir = Path(cfg.get("cache_dir") or Path(tempfile.gettempdir()) / "odw2json-ocr-cache")

    @property
    def backend(self) -> OcrBackend:
        if self._backend is None:
            self._backend = get_backend(self._config)
        return self._backend

    # -- public -----------------------------------------------------------------------------------------------
    def ingest(self, pdf_path: str) -> Document:
        import pdfplumber

        pages: list[Page] = []
        pdfium_doc = None
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, pl in enumerate(pdf.pages):
                    width, height = float(pl.width), float(pl.height)
                    words = self._text_words(pl)
                    text = build_text(words)
                    if is_garbage_text(text):
                        if pdfium_doc is None:
                            import pypdfium2

                            pdfium_doc = pypdfium2.PdfDocument(pdf_path)
                        words = self._ocr_page(pdf_path, pdfium_doc, i, width, height)
                        pages.append(Page(i + 1, width, height, words, build_text(words), "ocr"))
                    else:
                        pages.append(Page(i + 1, width, height, _clamp(words, width, height), text, "text"))
        finally:
            if pdfium_doc is not None:
                pdfium_doc.close()
        return Document(path=str(pdf_path), pages=pages)

    # -- internals --------------------------------------------------------------------------------------------
    @staticmethod
    def _text_words(pl) -> list[Word]:
        raw = pl.extract_words(keep_blank_chars=False, use_text_flow=False, x_tolerance=3, y_tolerance=3)
        return [Word(r["text"], float(r["x0"]), float(r["top"]), float(r["x1"]), float(r["bottom"])) for r in raw]

    def _ocr_page(self, pdf_path, pdfium_doc, index: int, width: float, height: float) -> list[Word]:
        key = self._cache_key(pdf_path, index)
        cached = self._cache_read(key)
        if cached is not None:
            return _clamp(cached, width, height)
        scale = min(self.dpi / 72.0, MAX_SIDE_PX / max(width, height))
        page = pdfium_doc[index]
        try:
            image = page.render(scale=scale).to_pil().convert("RGB")
        finally:
            page.close()
        words = lines_to_words(self.backend.ocr(image), scale, self.min_conf)
        # map by the real pixel/point ratio so rounding of the bitmap size never shifts boxes
        words = _clamp(words, width, height)
        self._cache_write(key, words)
        return words

    def _cache_key(self, pdf_path, index: int) -> str | None:
        if self.cache_dir is None:
            return None
        h = hashlib.sha256()
        with open(pdf_path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        backend = self._backend_id
        h.update(f"|{index}|{self.dpi}|{self.min_conf}|{backend}|{_CACHE_VERSION}".encode())
        return h.hexdigest()

    def _cache_read(self, key: str | None) -> list[Word] | None:
        if key is None or self.cache_dir is None:
            return None
        f = self.cache_dir / f"{key}.json"
        try:
            return [Word(*w) for w in json.loads(f.read_text(encoding="utf-8"))]
        except (OSError, ValueError, TypeError):
            return None

    def _cache_write(self, key: str | None, words: list[Word]) -> None:
        if key is None or self.cache_dir is None:
            return
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            tmp = self.cache_dir / f"{key}.tmp{os.getpid()}"
            tmp.write_text(
                json.dumps([[w.text, w.x0, w.y0, w.x1, w.y1, w.conf] for w in words], ensure_ascii=False),
                encoding="utf-8",
            )
            os.replace(tmp, self.cache_dir / f"{key}.json")
        except OSError:
            pass
