# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest, time
from ..parsers import edict

SRC_NAME = "edict"
SRC_DIR = "../dicts"

SRC_NAME = "/".join((SRC_DIR, SRC_NAME))

class EdictTest(unittest.TestCase):

    def setUp(self):
        self.parser = edict.EdictParser(SRC_NAME)

    def test_japanese_search(self):
        """EDICT: Search for Japanese word/phrase"""
        query = u"日本"
        l = [entry for entry in self.parser.search(query)]
        self.assertTrue(len(l) > 0)

    def test_native_search(self):
        """EDICT: Search for non-Japanese word/phrase"""
        query = u"Japan"
        l = [entry for entry in self.parser.search(query)]
        self.assertTrue(len(l) > 0)

    def test_unparsed(self):
        """EDICT: Check for unhandled EDICT fields"""
        l = [k for k in self.parser.search(u"")]
        unparsed = set()
        for key, entry in self.parser.cache.iteritems():
            for item in entry.unparsed: unparsed.add(item)
        if unparsed:
            #self.fail(u"Unhandled fields found: %s" % u", ".join(unparsed))
            print u"\n\tWARNING: Unhandled fields found: %s" \
                  % u", ".join(unparsed)

    def test_caching(self):
        """EDICT: Check that caching is working"""
        self.assertFalse(self.parser.cache)
        t = time.time()
        self.test_japanese_search()
        first_t = time.time() - t

        self.assertTrue(self.parser.cache)
        t = time.time()
        self.test_japanese_search()
        second_t = time.time() - t

        print "\n\tFirst query time:  %f" % first_t
        print "\tSecond query time: %f" % second_t
        self.assertTrue(second_t <= first_t)

    def test_no_cache(self):
        """EDICT: Check that parser works without caching."""
        self.parser = edict.EdictParser(SRC_NAME, use_cache=False)

        self.assertFalse(self.parser.cache)
        t = time.time()
        self.test_japanese_search()
        first_t = time.time() - t

        self.assertFalse(self.parser.cache)
        t = time.time()
        self.test_japanese_search()
        second_t = time.time() - t

        print "\n\tFirst query time:  %f" % first_t
        print "\tSecond query time: %f" % second_t

    def tearDown(self):
        self.parser = None

if __name__ == "__main__":
    unittest.main()
