#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, Paul Goins
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""A parser for KANJIDIC2."""

from __future__ import absolute_import

import os, gzip, gettext
from xml.etree.cElementTree import ElementTree
gettext.install('pyjben', unicode=True)

from .kanjidic_common \
     import jstring_convert, kanjidic2_key_to_str, qcode_to_desc

def jis_kuten_to_hex(kuten):
    """Kuten string to hex conversion"""
    pieces = map(int, kuten.split(u'-'))
    print "DEBUG: kuten: %s, pieces: %s" % (kuten, str(pieces))
    return ((pieces[0] + 0x20) << 8) + (pieces[1] + 0x20)


class Kanjidic2Node(object):

    def __init__(self, xml_node):
        self.xml = xml_node
        self.literal = self._get_literal()

    def _get_literal(self):
        literal = self.xml.find("literal").text.strip()
        assert len(literal) == 1, "Literal has more than one character!"
        return literal

    def _get_grade(self):
        o = self.xml.find("misc/grade")
        return int(o.text)

    def _get_freq(self):
        # By the spec, it seems like multiple freqs are possible??
        # So... let's get all entries and assert.
        o = self.xml.findall("misc/freq")
        if not o:
            return None
        assert len(o) == 1, (
            u"Character %s: Expected 1 freq entry, found %d" %
            (self._get_literal(), len(o)))
        return int(o[0].text)

    def _get_jlpt(self):
        o = self.xml.find("misc/jlpt")
        return int(o.text)

    def _get_nanori(self):
        nodes = self.xml.findall("reading_meaning/nanori")
        if not nodes:
            return None
        nanori = [o.text for o in nodes]
        return nanori

    def _get_attrdict(self, path, attr_name):
        """Helper: stores elements on path in dict, keyed by attribute."""
        d = {}
        nodes = self.xml.findall(path)
        attrs = set(o.attrib.get(attr_name) for o in nodes)
        for attr in attrs:
            d[attr] = [o.text for o in nodes
                       if o.attrib.get(attr_name) == attr]
        return d

    def _get_readings(self):
        """Returns dictionary of reading lists, keyed by type."""
        return self._get_attrdict("reading_meaning/rmgroup/reading", "r_type")

    def _get_meanings(self):
        """Returns dictionary of gloss lists, keyed by language prefix."""
        meaning_d = self._get_attrdict(
            "reading_meaning/rmgroup/meaning", "m_lang")
        if None in meaning_d:
            meaning_d['en'] = meaning_d[None]
            del meaning_d[None]
        return meaning_d

    def __unicode__(self):
        readings = self._get_readings()
        meanings = self._get_meanings()
        nanori = self._get_nanori()
        grade = self._get_grade()
        jlpt = self._get_jlpt()
        freq = self._get_freq()

        pieces = []
        pieces.append(u"Literal: %s" % self.literal)

        pieces.append(u"On-yomi: %s" % u"、".join(readings['ja_on']))
        pieces.append(u"Kun-yomi: %s" % u"、".join(readings['ja_kun']))
        pieces.append(u"Nanori: %s" % u"、".join(nanori))

        pieces.append(u"Korean (Hangul): %s" %
                      u", ".join(readings['korean_h']))
        pieces.append(u"Korean (Romanized): %s" %
                      u", ".join(readings['korean_r']))
        pieces.append(u"Pinyin: %s" % u", ".join(readings['pinyin']))

        for lang in sorted(meanings):
            pieces.append(u"Meanings (%s): %s" %
                          (lang, "; ".join(meanings[lang])))

        if jlpt:
            pieces.append(u"JLPT grade level: %d" % jlpt)
        if grade:
            pieces.append(u"Jouyou grade level: %d" % grade)
        if freq:
            pieces.append(u"Newspaper frequency: %d" % freq)

        pieces.append(u"Unicode value: %04X" % ord(self.literal))

        return u"\n".join(pieces)


class Parser(object):

    def __init__(self, filename, encoding="utf-8"):
        """Initializer for Kanjidic2Parser.

        About use_cache: Kanjidic2 is a large, heavy to parse file.
        Although it takes a large amount of memory, it is better to
        retain it in memory to increase the speed of subsequent
        searches.

        """
        if not os.path.exists(filename):
            raise Exception("Dictionary file does not exist.")
        self.filename = filename
        self.encoding = encoding
        self.indexed = False
        self.header, self.characters = self.load_via_etree()

    def load_via_etree(self):
        if len(self.filename) >= 3 and self.filename[-3:] == ".gz":
            f = gzip.open(self.filename)
        else:
            f = open(self.filename, "rb")
        et = ElementTree(file=f)
        f.close()
        nodes = et.getroot().getchildren()
        header, characters = nodes[0], nodes[1:]
        characters = [Kanjidic2Node(char) for char in characters]
        return header, characters

    def get_header(self):
        d = {}
        for o in self.header.getchildren():
            cdata = "".join((o.text, o.tail)).strip()
            d[o.tag] = cdata
        return "\n".join("%s: %s" % (k, d[k]) for k in sorted(d))

    def search(self, query):
        self.create_indices()
        for u in query:
            c = self.by_kanji.get(u)
            if c:
                yield c

    def create_indices(self):
        if self.indexed:
            return
        self.indexed = True
        self.by_kanji = {}
        for char in self.characters:
            literal = char.xml.find("literal").text.strip()
            self.by_kanji[literal] = char


def encode_or_else(s):
    if os.name == "nt":
        charset = "cp932"
    else:
        charset = "utf-8"
    lines = s.split(u"\n")
    out = []
    for line in lines:
        try:
            val = line.encode(charset)
            out.append(line)
        except:
            pass
    return u"\n".join(out)


if __name__ == "__main__":
    import sys

    try:
        dfname, args = sys.argv[1], sys.argv[2:]
        assert args
    except (IndexError, AssertionError):
        print _(u"Syntax: %s <dict_file> <character [...]>") % sys.argv[0]
        exit(-1)

    try:
        p = Parser(dfname)
    except Exception, e:
        print _(u"Could not create Kanjidic2Parser: %s") % unicode(e)
        exit(-1)

    if os.name == "nt":
        charset = "cp932"
    else:
        charset = "utf-8"

    print "HEADER"
    print "======"
    print p.get_header()
    print
    print "%d characters found" % len(p.characters)

    for i, kanji in enumerate(p.search("".join(args).decode(charset))):
        kstr = encode_or_else(unicode(kanji))
        print _(u"Entry %d:\n%s\n") % (i+1, kstr)
