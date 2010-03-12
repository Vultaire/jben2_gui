# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest, time
from jbparse import kanjidic2

SRC_NAME = "kanjidic2.xml"
SRC_DIR = "../../dicts"

SRC_NAME = "/".join((SRC_DIR, SRC_NAME))

class Kanjidic2Test(unittest.TestCase):

    def setUp(self):
        self.parser = kanjidic2.Parser(SRC_NAME)

    def test_single_kanji_search(self):
        """KANJIDIC2: Search for single kanji"""
        query = u"食"
        l = [entry for entry in self.parser.search(query)]
        self.assertEqual(len(l), 1)
        self.assertEqual(query, l[0].literal)

    def test_multi_kanji_search(self):
        """KANJIDIC2: Search for multiple kanji at once"""
        query = u"上下"
        l = [entry for entry in self.parser.search(query)]
        self.assertEqual(len(l), 2)
        for char in query:
            self.assertTrue(char in [entry.literal for entry in l])

    def test_mixed_search(self):
        """KANJIDIC2: Search query with kanji and non-kanji characters"""
        query = u"天気はいいから、散歩しましょう。  Right?"
        l = [entry for entry in self.parser.search(query)]
        self.assertEqual(len(l), 4)
        for char in u"天気散歩":
            self.assertTrue(char in [entry.literal for entry in l])

    def tearDown(self):
        self.parser = None

if __name__ == "__main__":
    unittest.main()
