import unittest

from odw2json import stubs
from odw2json.model import Document, Page


def doc(text):
    return Document("x.pdf", [Page(1, 595, 842, [], text, "text")])


class ClassifierTests(unittest.TestCase):
    def setUp(self):
        self.c = stubs.KeywordClassifier()

    def test_przelew(self):
        r = self.c.classify(doc("Potwierdzenie przelewu\nKwota 100 PLN"))
        self.assertEqual(r.doc_class, "przelew")

    def test_pelnomocnictwo(self):
        r = self.c.classify(doc("PEŁNOMOCNICTWO\nUdzielam pełnomocnictwa"))
        self.assertEqual(r.doc_class, "pelnomocnictwo")

    def test_odwolanie(self):
        r = self.c.classify(doc("Prezes Krajowej Izby Odwoławczej\nOdwołanie wobec czynności"))
        self.assertEqual(r.doc_class, "odwolanie")

    def test_reject(self):
        r = self.c.classify(doc("Przepis na szarlotkę"))
        self.assertIsNone(r.doc_class)


class ExtractorTests(unittest.TestCase):
    def test_skeleton(self):
        e = stubs.SkeletonExtractor().extract(doc(""), "przelew")
        self.assertIsNone(e.data["przelew_bankowy"]["kwota"])


class LetterSpacedTests(unittest.TestCase):
    def test_letter_spaced_heading(self):
        r = stubs.KeywordClassifier().classify(doc("P E Ł N O M O C N I C T W O\nMocodawca X"))
        self.assertEqual(r.doc_class, "pelnomocnictwo")
