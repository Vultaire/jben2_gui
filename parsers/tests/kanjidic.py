# -*- coding: utf-8 -*-

import unittest, time
from parsers import kanjidic

SRC_NAME = "kanjidic"
SRC_DIR = "../dicts"

SRC_NAME = "/".join((SRC_DIR, SRC_NAME))

class KanjidicTest(unittest.TestCase):

    def setUp(self):
        self.kp = kanjidic.KanjidicParser(SRC_NAME)

    def test_single_kanji_search(self):
        """KANJIDIC: Search for single kanji"""
        query = u"食"
        l = [entry for entry in self.kp.search(query)]
        self.assertEqual(len(l), 1)
        self.assertEqual(query, l[0].literal)

    def test_multi_kanji_search(self):
        """KANJIDIC: Search for multiple kanji at once"""
        query = u"上下"
        l = [entry for entry in self.kp.search(query)]
        self.assertEqual(len(l), 2)
        for char in query:
            self.assertTrue(char in [entry.literal for entry in l])

    def test_mixed_search(self):
        """KANJIDIC: Search query with kanji and non-kanji characters"""
        query = u"天気はいいから、散歩しましょう。  Right?"
        l = [entry for entry in self.kp.search(query)]
        self.assertEqual(len(l), 4)
        for char in u"天気散歩":
            self.assertTrue(char in [entry.literal for entry in l])

    def test_unparsed(self):
        """KANJIDIC: Check for unhandled KANJIDIC fields"""
        l = [k for k in self.kp.search(u"")]
        unparsed = set()
        for key, kanji in self.kp.cache.iteritems():
            for item in kanji.unparsed: unparsed.add(item)
        if unparsed:
            #self.fail(u"Unhandled fields found: %s" % u", ".join(unparsed))
            print u"\n\tWARNING: Unhandled fields found: %s" \
                  % u", ".join(unparsed)

    def test_caching(self):
        """KANJIDIC: Check that caching is working"""
        self.assertFalse(self.kp.cache)
        t = time.time()
        self.test_single_kanji_search()
        first_t = time.time() - t

        self.assertTrue(self.kp.cache)
        t = time.time()
        self.test_single_kanji_search()
        second_t = time.time() - t

        print "\n\tFirst query time:  %f" % first_t
        print "\tSecond query time: %f" % second_t
        self.assertTrue(second_t <= first_t)

    def test_no_cache(self):
        """KANJIDIC: Check that parser works without caching."""
        self.kp = kanjidic.KanjidicParser(SRC_NAME, use_cache=False)

        self.assertFalse(self.kp.cache)
        t = time.time()
        self.test_single_kanji_search()
        first_t = time.time() - t

        self.assertFalse(self.kp.cache)
        t = time.time()
        self.test_single_kanji_search()
        second_t = time.time() - t

        print "\n\tFirst query time:  %f" % first_t
        print "\tSecond query time: %f" % second_t

    def tearDown(self):
        self.kp = None

if __name__ == "__main__":
    unittest.main()



if __name__ == "__main__":
    import sys, os

    if len(sys.argv) < 2:
        print _(u"Please specify a dictionary file.")
        exit(-1)
    try:
        kp = KanjidicParser(sys.argv[1])
    except Exception, e:
        print _(u"Could not create KanjidicParser: %s") % unicode(e)
        exit(-1)

    if len(sys.argv) < 3:
        print _(u"Please specify a kanji.  "
                u"(Copy/paste, or Alt-Zenkaku/Hankaku)")
        exit(-1)

    if os.name == "nt":
        charset = "cp932"
    else:
        charset = "utf-8"

    for i, entry in enumerate(kp.search(sys.argv[2].decode(charset))):
        print _(u"Entry %d:\n%s\n") % (i+1, entry.to_string())
