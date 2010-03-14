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

import os, gzip, gettext, warnings
from xml.etree.cElementTree import ElementTree
gettext.install('pyjben', unicode=True)

from .kanjidic_common \
     import jstring_convert, kanjidic2_key_to_str, qcode_to_desc

def jis_kuten_to_hex(kuten):
    """Kuten string to hex conversion"""
    pieces = map(int, kuten.split(u'-'))
    return ((pieces[0] + 0x20) << 8) + (pieces[1] + 0x20)

def xml2text(o):
    return o.text

def mapdict(fn, d):
    result = {}
    for k, v in d.iteritems():
        result[k] = map(fn, v)
    return result


class Kanjidic2Node(object):

    def __init__(self, xml_node):
        self.xml = xml_node
        self.literal = self._get_literal()

    def _get_literal(self):
        literal = self.xml.find("literal").text.strip()
        assert len(literal) == 1, _(u"Literal has more than one character!")
        return literal

    def get_grade(self):
        o = self.xml.find("misc/grade")
        return int(o.text) if o else None

    def get_freq(self):
        # By the spec, it seems like multiple freqs are possible??
        # So... let's get all entries and assert.
        o = self.xml.findall("misc/freq")
        if not o:
            return None
        assert len(o) == 1, _(
            u"Character %s: Expected 1 freq entry, found %d") % \
            (self._get_literal(), len(o))
        return int(o[0].text)

    def get_jlpt(self):
        o = self.xml.find("misc/jlpt")
        return int(o.text) if o else None

    def get_strokes(self):
        """Gets stroke count.

        Returns a tuple of (stroke_count, miscounts), where miscounts
        is either None or a list of common miscounts for the
        character.

        """
        nodes = self.xml.findall("misc/stroke_count")
        scnode, misnodes = nodes[0], nodes[1:]
        sc = int(nodes[0].text)
        if misnodes:
            miss = map(int, [o.text for o in misnodes])
        else:
            miss = None
        return (sc, miss)

    def _get_nanori_nodes(self):
        nodes = self.xml.findall("reading_meaning/nanori")
        return nodes or None

    def _get_attrdict(self, path, attr_name):
        """Helper: stores elements on path in dict, keyed by attribute."""
        d = {}
        nodes = self.xml.findall(path)
        #attrs = set(o.attrib.get(attr_name) for o in nodes)
        for o in nodes:
            d.setdefault(o.attrib.get(attr_name), []).append(o)
        #for attr in attrs:
        #    d[attr] = [o for o in nodes
        #               if o.attrib.get(attr_name) == attr]
        return d

    def _get_reading_nodes(self):
        """Returns dictionary of reading lists, keyed by type."""
        # NEEDS AN UPDATE: Just noticed, rmgroup allows
        # readings/meanings to be meaningfully grouped together.  We
        # -can- dump everything together, but we -should- handle the
        # groups.
        return self._get_attrdict("reading_meaning/rmgroup/reading", "r_type")

    def _get_meaning_nodes(self):
        """Returns dictionary of gloss lists, keyed by language prefix."""
        # NEEDS AN UPDATE: See _get_reading_nodes.
        meaning_d = self._get_attrdict(
            "reading_meaning/rmgroup/meaning", "m_lang")
        if None in meaning_d:
            meaning_d['en'] = meaning_d[None]
            del meaning_d[None]
        return meaning_d

    def _get_dictcodes(self):
        return self._get_attrdict("dic_number/dic_ref", "dr_type")

    def _get_querycodes(self):
        return self._get_attrdict("query_code/q_code", "qc_type")

    def get_nanori(self):
        nanori = map(xml2text, self._get_nanori_nodes() or [])
        if nanori:
            return _(u"%s: %s") % (_(u"Nanori"), u"、".join(nanori))

    def get_readings(self, rtypes):
        """Gets readings as text strings.

        Takes in any number of reading keys, and returns a list
        containing user-friendly output strings.

        Valid keys include: ja_on, ja_kun, korean_h, korean_r, pinyin,
        and nanori.

        Note: Nanori is also handled independently, as it is stored
        differently than the other readings.

        """
        d = {
            "ja_on": _(u"On-yomi"),
            "ja_kun": _(u"Kun-yomi"),
            "korean_h": _(u"Korean (Hangul)"),
            "korean_r": _(u"Korean (Romanized)"),
            "pinyin": _(u"Pinyin"),
            }
        romanized = ("korean_r", "pinyin")
        j_readings = ("ja_on", "ja_kun")
        readings = mapdict(xml2text, self._get_reading_nodes())
        pieces = []
        for rt in rtypes:
            if rt == "nanori":
                s = self.get_nanori()
                if s:
                    pieces.append(s)
            elif rt in d:
                if rt not in readings:
                    continue
                r_list = readings[rt]
                if rt in j_readings:
                    r_list = map(jstring_convert, r_list)
                separator = u", " if rt in romanized else u"、"
                reading_str = separator.join(r_list)
                pieces.append(_(u"%s: %s") % (d[rt], reading_str))
        return pieces

    def get_meanings(self):
        meanings = mapdict(xml2text, self._get_meaning_nodes())
        pieces = []
        for lang in sorted(meanings):
            pieces.append(_(u"Meanings (%s): %s") %
                          (lang, u"; ".join(meanings[lang])))
        return pieces

    def get_dict_codes(self, keys, all=False):
        """Gets dictionary codes as strings for display to the user.

        Accepts a list of dictionary keys.  To get all keys, set the
        all keyword to true.  (The keys parameter will be ignored in
        this case.)

        """
        pieces = []
        dicts = self._get_dictcodes()
        for dcode in sorted(dicts):
            if (not all) and dcode not in keys:
                continue
            nodes = dicts[dcode]
            assert len(nodes) == 1, _(
                u"Character %s: Multiple (%d) entries found for "
                u"dict code %s") % \
                (self._get_literal(), len(nodes), dcode)
            o = nodes[0]
            dname = kanjidic2_key_to_str(dcode)
            if dcode == "moro":
                s = _(u"Index %s, volume %s, page %s") % \
                    (o.text, o.attrib['m_vol'], o.attrib['m_page'])
            else:
                s = o.text
            pieces.append(_(u"%s: %s") % (dname, s))
        return pieces

    def get_query_codes(self, keys, all=False):
        pieces = []
        qcodes = self._get_querycodes()
        for qcode in sorted(qcodes):
            if (not all) and qcode not in keys:
                continue
            nodes = qcodes[qcode]
            qname = qcode_to_desc(qcode)
            if qcode == "skip":
                d = {}
                for o in nodes:
                    d.setdefault(o.attrib.get("skip_misclass"), []).append(o)
                for misclass in sorted(d):
                    if misclass:
                        outname = _(u"%s miscode (%s)") % (qname, misclass)
                    else:
                        outname = qname
                    s = u", ".join(o.text for o in d[misclass])
                    pieces.append(_(u"%s: %s") % (outname, s))
            else:
                s = u", ".join(o.text for o in nodes)
                pieces.append(_(u"%s: %s") % (qname, s))
        return pieces

    def get_radicals(self):
        pieces = []
        d = self._get_attrdict("radical/rad_value", "rad_type")
        for key in sorted(d):
            nodes = d[key]
            for o in nodes:
                pieces.append(u"%s: %s" % (key, o.text))
        return pieces

    def get_codepoints(self):
        pieces = []
        d = self._get_attrdict("codepoint/cp_value", "cp_type")
        for key in sorted(d):
            nodes = d[key]
            for o in nodes:
                pieces.append(u"%s: %s" % (key.upper(), o.text))
        return pieces

    def get_variants(self):
        pieces = []
        d = self._get_attrdict("misc/variant", "var_type")
        for key in sorted(d):
            nodes = d[key]
            for o in nodes:
                pieces.append(u"%s: %s" % (key.upper(), o.text))
        return pieces

    def _get_radical_name_nodes(self):
        return self.xml.findall("misc/rad_name")

    def get_radical_names(self):
        """Get radical names.  Returned as a single string."""
        names = [o.text for o in self._get_radical_name_nodes()]
        return u"、".join(names) if names else None

    def __unicode__(self):

        def indent_strs(strs, amount=2):
            if strs:
                return [u"%s%s" % (u" " * amount, s) for s in strs]

        pieces = []

        pieces.append(u"=" * 70)
        pieces.append(_(u"Literal: %s") % self.literal)
        pieces.append(u"-" * 70)

        pieces.append(_(u"Readings:"))
        r_strs = indent_strs(self.get_readings(
            ("ja_on", "ja_kun", "nanori", "korean_h", "korean_r", "pinyin")))
        pieces.extend(r_strs)
        pieces.append(u"-" * 70)

        m_strs = indent_strs(self.get_meanings())
        pieces.extend(m_strs)
        pieces.append(u"-" * 70)

        pieces.append(_(u"Miscellaneous:"))
        jlpt = self.get_jlpt()
        if jlpt:
            pieces.append(_(u"  JLPT grade level: %d") % jlpt)
        grade = self.get_grade()
        if self.get_grade():
            pieces.append(_(u"  Jouyou grade level: %d") % grade)
        freq = self.get_freq()
        if self.get_freq():
            pieces.append(_(u"  Newspaper frequency: %d") % freq)
        strokes, misstrokes = self.get_strokes()
        pieces.append(_(u"  Stroke count: %d") % strokes)
        if misstrokes:
            pieces.append(_(u"  Common stroke miscounts: %s") %
                          ", ".join(map(str, misstrokes)))
        pieces.append(u"-" * 70)

        pieces.append(_(u"Dictionary codes:"))
        d_strs = indent_strs(self.get_dict_codes([], all=True))
        pieces.extend(d_strs)
        pieces.append(u"-" * 70)

        pieces.append(_(u"Query codes:"))
        qc_strs = indent_strs(self.get_query_codes([], all=True))
        pieces.extend(qc_strs)
        pieces.append(u"-" * 70)

        pieces.append(_(u"Other information:"))

        pieces.append(_(u"  Radicals:"))
        rad_strs = indent_strs(self.get_radicals(), amount=4)
        pieces.extend(rad_strs)

        radnames = self.get_radical_names()
        if radnames:
            pieces.append(u"    %s: %s" %
                          (_(u"Radical names"), radnames))

        pieces.append(_(u"  Codepoints:"))
        cp_strs = indent_strs(self.get_codepoints(), amount=4)
        pieces.extend(cp_strs)

        variant_strs = indent_strs(self.get_variants(), amount=4)
        if variant_strs:
            pieces.append(_(u"  Variants:"))
            pieces.extend(variant_strs)

        pieces.append(u"=" * 70)

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
            raise Exception(u_("Dictionary file does not exist."))
        self.filename = filename
        self.encoding = encoding
        self.indexed = False
        self.header, self.characters = self.load_via_etree()
        self._check_version()

    def _check_version(self):
        version = int(self.header.find('file_version').text)
        assert version >= 4, _(
            u"This parser won't work with versions of KANJIDIC2 "
            u"older than version 4.")
        if version > 3:
            s = _(u"Parser version is for version 4, detected version is %d"
                  ) % version
            warnings.warn(s)

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
            cdata = u"".join((o.text, o.tail)).strip()
            d[o.tag] = cdata
        return u"\n".join(u"%s: %s" % (k, d[k]) for k in sorted(d))

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

    print u"HEADER"
    print u"======"
    print p.get_header()
    print
    print u"%d characters found" % len(p.characters)

    for i, kanji in enumerate(p.search("".join(args).decode(charset))):
        kstr = encode_or_else(unicode(kanji))
        print _(u"Entry %d:\n%s\n") % (i+1, kstr)
