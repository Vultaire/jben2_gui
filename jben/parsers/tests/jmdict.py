# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest, time
from cStringIO import StringIO
from ..parsers import jmdict
from xml.sax.xmlreader import InputSource

SRC_NAME = "jmdict"
SRC_DIR = "../dicts"

SRC_NAME = "/".join((SRC_DIR, SRC_NAME))

class JMdictTest(unittest.TestCase):

    def setUp(self):
        self.parser = jmdict.JMdictParser(SRC_NAME)

    def test_japanese_search(self):
        """JMDICT: Search for Japanese word/phrase"""
        parser = self.parser
        desired_indices = ["starts_with"]

        data = self._parse_x_entries(SRC_NAME, 10)
        parser.cache = data
        parser.create_indices(data, desired_indices)

        query = u"仝"
        l = parser.search(query)
        #print
        #print "====="
        #for entry in l:
        #    print entry.to_string()
        self.assertTrue(len(l) > 0)
        #print "====="
        query = u"おなじく"
        l = parser.search(query)
        #for entry in l:
        #    print entry.to_string()
        #print "====="
        self.assertTrue(len(l) > 0)

    def test_native_search(self):
        """JMDICT: Search for non-Japanese word/phrase"""
        # Let's cheat a little: reading in the whole JMdict will make
        # our unit tests UNBEARABLY slow.
        #
        # This test will fail if "repetition mark" does not show up
        # within the first 10 entries.  In such a case, the test will
        # need to be updated.
        parser = self.parser
        desired_indices = ["starts_with"]

        data = self._parse_x_entries(SRC_NAME, 10)
        parser.cache = data
        parser.create_indices(data, desired_indices)

        query = u"repetition mark"
        l = parser.search(query)
        self.assertTrue(len(l) > 0)

    def test_unparsed(self):
        """JMDICT: Check for unhandled JMDICT fields"""
        l = [k for k in self.parser.search(u"")]
        unparsed = set()
        for key, entry in self.parser.cache.iteritems():
            for item in entry.unparsed: unparsed.add(item)
        if unparsed:
            #self.fail(u"Unhandled fields found: %s" % u", ".join(unparsed))
            print u"\n\tWARNING: Unhandled fields found: %s" \
                  % u", ".join(unparsed)

    def test_caching(self):
        """JMDICT: Check that caching is working"""
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
        """JMDICT: Check that parser works without caching."""
        self.parser = jmdict.JMdictParser(SRC_NAME, use_cache=False)

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

    def _parse_x_entries(self, filename, max_entries):
        """Helper function: reads max_entries entries from the JMdict file.

        The text for max_entries entries of JMdict are naively read
        in, then converted to a file-like object which the parser will
        use.

        """
        # Copied from parsers.jmdict
        if len(filename) >= 3 and filename[-3:] == ".gz":
            f = gzip.open(filename)
        else:
            f = open(filename, "rb")

        # Grab just the first max_entries entries, then close f and
        # make a new "f" via the StringIO lib.
        lines = []
        count = 0
        while True:
            line = f.readline()
            lines.append(line)
            if "</entry>" in line:
                count += 1
                if count >= max_entries: break
        f.close()
        lines.append("</JMdict>\n")
        f = StringIO("".join(lines))

        # Continuing from parsers.jmdict...
        sh = jmdict.JMDSAXHandler(True, "beef")
        isource = InputSource()
        isource.setEncoding("utf-8")
        isource.setByteStream(f)

        # Parser: Since I wish to directly handle the "entities", we
        # need to override default behavior and cannot just use
        # xml.sax.parse.
        parser = jmdict.ExpatParserNoEntityExp()
        parser.setContentHandler(sh)

        parser.parse(isource)
        f.close()
        return sh.data

    def test_limited_parse(self):
        """JMDICT: Parse 5 entries successfully."""
        data = self._parse_x_entries(SRC_NAME, 5)
        self.assertEqual(len(data), 5)

    def test_indexing(self):
        parser = self.parser
        desired_indices = ["starts_with"]

        data = self._parse_x_entries(SRC_NAME, 5)

        print "CREATING INDICES"
        parser.create_indices(data, desired_indices)

        print "j_ind keys:", parser.j_ind.keys()
        for name, index in parser.j_ind.iteritems():
            #print "\t%s: %s" % (name, str(index))
            print "\t%s keys: %s" % (name, str(index.keys()))
            for k, s in index.iteritems():
                print "\t\t%s: %s" % (k, str(s))
        print "n_ind keys:", parser.n_ind.keys()
        for name, index in parser.n_ind.iteritems():
            print "\t%s keys: %s" % (name, str(index.keys()))
            for name2, index2 in index.iteritems():
                #print "\t\t%s: %s" % (name2, str(index2))
                print "\t\t%s keys: %s" % (name2, str(index2.keys()))
                for k, s in index2.iteritems():
                    print "\t\t\t%s: %s" % (k, str(s))


    def tearDown(self):
        self.parser = None

    #del test_japanese_search
    #del test_native_search
    del test_unparsed
    del test_caching
    del test_no_cache

    del test_limited_parse
    del test_indexing

if __name__ == "__main__":
    unittest.main()
