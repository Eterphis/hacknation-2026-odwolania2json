import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from odw2json.ingest import PdfIngestor
from odw2json.ingest.preprocess import PREPROCESSORS, preprocess_image

SCAN = Path("C:/Users/jasiu/workspace/uzp-data/dane/skany/odwolania/0005/0005.pdf")


class PreprocessImageTests(unittest.TestCase):
    def _img(self):
        a = np.full((40, 60, 3), 250, np.uint8)
        a[5:10, :] = 20      # dark print
        a[20:25, :] = 190    # light show-through
        a[30:35, :] = 100    # mid grey
        return Image.fromarray(a)

    def test_none_returns_same_image(self):
        im = self._img()
        self.assertIs(preprocess_image(im, "none"), im)

    def test_levels_whitens_showthrough_keeps_print(self):
        out = np.asarray(preprocess_image(self._img(), "levels"))
        self.assertEqual(out.shape, (40, 60, 3))
        self.assertLess(out[7, 10, 0], 15)
        self.assertEqual(out[22, 10, 0], 255)
        self.assertEqual(out[2, 10, 0], 255)
        self.assertTrue(0 < out[32, 10, 0] < 255)

    def test_levels_adapts_to_faint_print(self):
        a = np.full((30, 30, 3), 250, np.uint8)
        a[10:15, :] = 120  # faint print, nothing darker
        out = np.asarray(preprocess_image(Image.fromarray(a), "levels"))
        self.assertLess(out[12, 5, 0], 30)  # still read as ink

    def test_unknown_name(self):
        with self.assertRaises(ValueError):
            preprocess_image(self._img(), "nope")

    def test_registry(self):
        self.assertIn("levels", PREPROCESSORS)


class FakeBackend:
    def __init__(self):
        self.sizes = []

    def ocr(self, image):
        self.sizes.append(np.asarray(image).min())
        return [("x", (1, 1, 20, 10), 0.9)]


@unittest.skipUnless(SCAN.exists(), "UZP data not available")
class WiringTests(unittest.TestCase):
    def test_config_and_cache_key(self):
        with tempfile.TemporaryDirectory() as d:
            a = PdfIngestor(backend=FakeBackend(), config={"ingest": {"cache_dir": d, "preprocess": "none"}})
            b = PdfIngestor(backend=FakeBackend(), config={"ingest": {"cache_dir": d, "preprocess": "levels"}})
            self.assertEqual(a.preprocess, "none")
            self.assertEqual(b.preprocess, "levels")
            self.assertNotEqual(a._cache_key(SCAN, 0), b._cache_key(SCAN, 0))
            a.ingest(str(SCAN))
            fb = FakeBackend()
            b2 = PdfIngestor(backend=fb, config={"ingest": {"cache_dir": d, "preprocess": "levels"}})
            b2.ingest(str(SCAN))
            self.assertTrue(fb.sizes)  # not served from the 'none' cache

    def test_default_is_levels(self):
        self.assertEqual(PdfIngestor(backend=FakeBackend()).preprocess, "levels")

    def test_env_overrides_config(self):
        import os
        os.environ["ODW2JSON_PREPROCESS"] = "none"
        try:
            self.assertEqual(PdfIngestor(backend=FakeBackend(), config={"ingest": {"preprocess": "levels"}}).preprocess, "none")
        finally:
            del os.environ["ODW2JSON_PREPROCESS"]

    def test_bad_name_rejected(self):
        with self.assertRaises(ValueError):
            PdfIngestor(backend=FakeBackend(), config={"ingest": {"preprocess": "nope"}})


if __name__ == "__main__":
    unittest.main()
