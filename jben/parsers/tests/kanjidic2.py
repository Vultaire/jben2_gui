# -*- coding: utf-8 -*-

import unittest, time
from parsers import kanjidic2

SRC_NAME = "kanjidic2.xml"
SRC_DIR = "../dicts"

SRC_NAME = "/".join((SRC_DIR, SRC_NAME))

class Kanjidic2Test(unittest.TestCase):

    def setUp(self):
        self.parser = kanjidic2.Kanjidic2Parser(SRC_NAME)

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

    def test_caching(self):
        """KANJIDIC2: Check that caching is working"""
        self.assertFalse(self.parser.cache)
        t = time.time()
        self.test_single_kanji_search()
        first_t = time.time() - t

        self.assertTrue(self.parser.cache)
        t = time.time()
        self.test_single_kanji_search()
        second_t = time.time() - t

        print "\n\tFirst query time:  %f" % first_t
        print "\tSecond query time: %f" % second_t
        self.assertTrue(second_t <= first_t)

    def test_no_cache(self):
        """KANJIDIC2: Check that parser works without caching."""
        self.parser = kanjidic2.Kanjidic2Parser(SRC_NAME, use_cache=False)

        self.assertFalse(self.parser.cache)
        t = time.time()
        self.test_single_kanji_search()
        first_t = time.time() - t

        self.assertFalse(self.parser.cache)
        t = time.time()
        self.test_single_kanji_search()
        second_t = time.time() - t

        print "\n\tFirst query time:  %f" % first_t
        print "\tSecond query time: %f" % second_t

    def tearDown(self):
        self.parser = None

if __name__ == "__main__":
    unittest.main()
