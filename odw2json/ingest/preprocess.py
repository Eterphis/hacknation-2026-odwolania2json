"""Page-image cleaning before OCR (config ``ingest.preprocess``).

``levels``: grayscale, then a levels stretch that maps everything lighter than ~140 to white and everything
darker than ~40 to black. Light show-through from the back of a page (grey, mirrored text) goes to white while
dark print stays; the detector no longer merges the ghost text into the printed lines. The black point adapts
to faint scans (it follows the page's darkest ink up to 110), so light print is not washed out.
Only numpy and OpenCV (both already required) are used.
"""
from __future__ import annotations

from typing import Any, Callable

import numpy as np

BLACK_POINT = 40.0   # gray level (0..255) that becomes pure black, for a normal dark-ink scan
MAX_BLACK_POINT = 110.0  # faint scans: the black point follows the page's ink up to this level
SPAN = 100.0         # white point = black point + SPAN


def _levels(image: Any) -> Any:
    from PIL import Image

    g = np.asarray(image.convert("L"), dtype=np.float32)
    ink = float(np.percentile(g, 0.5))  # darkest print on this page
    lo = min(max(BLACK_POINT, ink), MAX_BLACK_POINT)
    hi = lo + SPAN
    out = np.clip((g - lo) / (hi - lo), 0.0, 1.0) * 255.0
    return Image.fromarray(out.astype(np.uint8)).convert("RGB")


PREPROCESSORS: dict[str, Callable[[Any], Any]] = {"levels": _levels}
NAMES = ["none", *PREPROCESSORS]


def preprocess_image(image: Any, name: str) -> Any:
    """Return the cleaned PIL RGB image; ``none`` returns the input untouched."""
    if name == "none":
        return image
    try:
        return PREPROCESSORS[name](image)
    except KeyError:
        raise ValueError(f"unknown ingest.preprocess {name!r}; available: {NAMES}") from None
