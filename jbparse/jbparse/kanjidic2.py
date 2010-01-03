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

import gzip, xml.sax, gettext
gettext.install('pyjben', unicode=True)

from .kanjidic_common \
     import jstring_convert, kanjidic2_key_to_str, qcode_to_desc

def jis_kuten_to_hex(kuten):
    """Kuten string to hex conversion"""
    pieces = map(int, kuten.split(u'-'))
    print "DEBUG: kuten: %s, pieces: %s" % (kuten, str(pieces))
    return ((pieces[0] + 0x20) << 8) + (pieces[1] + 0x20)

class Kanjidic2Entry(object):

    def __init__(self):
        # Key info
        self.literal = None
        self.meanings = {}
        self.ja_kun = []
        self.ja_on = []
        self.nanori = []

        # Secondary info
        self.strokes = None
        self.strokes_miss = []
        self.freq = None
        self.grade = None
        self.jlpt = None

        # Info of low importance for most target users
        self.cps = []  # JIS codepoints
        self.radical = None
        self.radical_c = None  # "Classic" KangXi Zidian radical
        self.radname = None
        self.pinyin = []
        self.korean_h = []
        self.korean_r = []

        # "Query codes": Pattern-based lookup
        # Includes SKIP, DeRoo, Spahn/Hadamitzky, and Four Corners systems
        # Codes: P, DRnnnn, Inxnn.n, Qnnnn.n
        self.qcodes = {}

        # Dictionary codes
        # Non-D codes: H, N, V, INnnnn, MNnnnnnnn/MPnn.nnnn, Ennnn,
        #              Knnnn, Lnnnn, Onnnn
        # D codes: DB, DC, DF, DG, DH, DJ, DK, DM, DO, DR, DS, DT, DM
        self.dcodes = {}

        # Dictionary-related metadata
        self.xref = []
        self.misclass = []

    def to_string(self, **kwargs):
        """A default "to-string" dump of a Kanjidic2Entry."""
        lines = []
        lines.append(_(u"Literal: %s") % self.literal)
        if self.ja_on:
            lines.append(_(u"Onyomi: %s")
                         % u"、".join(
                             [jstring_convert(us) for us in self.ja_on]))
        if self.ja_kun:
            lines.append(_(u"Kunyomi: %s")
                         % u"、".join(
                             [jstring_convert(us) for us in self.ja_kun]))
        if self.nanori:
            lines.append(_(u"Nanori: %s")
                         % u"、".join(
                             [jstring_convert(us) for us in self.nanori]))
        if self.meanings:
            for k, v in self.meanings.iteritems():
                lines.append(_(u"Meaning (%s): %s") % (k, _(u"; ").join(v)))

        if self.strokes:
            lines.append(_(u"Stroke count: %d") % self.strokes)
        if self.strokes_miss:
            lines.append(_(u"Common miscounts: %s")
                         % _(u", ").join(self.strokes_miss))
        if self.freq:
            lines.append(_(u"Newspaper Frequency: %d") % self.freq)
        if self.grade:
            if self.grade in range(1, 7):
                grade_str = unicode(self.grade)
            elif self.grade == 8:
                grade_str = _(u"General usage")
            elif self.grade == 9:
                grade_str = _(u"Jinmeiyou (Characters for names)")
            elif self.grade == None:
                grade_str = _(u"Unspecified")
            else:
                grade_str = _(u"Unhandled grade level (Grade %d)") % self.grade
            lines.append(_(u"Jouyou Grade: %s") % grade_str)
        if self.jlpt:
            lines.append(_(u"JLPT Level: %d") % self.jlpt)

        # Query codes
        if self.qcodes:
            for k, v in self.qcodes.iteritems():
                desc = qcode_to_desc(k)
                lines.append(_(u"%s code: %s") % (desc, self.qcodes[k]))

                if k == 'skip' and self.misclass:
                    miscodes = []
                    for code_type, code_val in self.misclass:
                        if code_type == u'stroke_count':
                            miscodes.append(_(u"%s (stroke count)") % code_val)
                        elif code_type == u'posn':
                            miscodes.append(_(u"%s (position)") % code_val)
                        elif code_type == u'stroke_and_posn':
                            miscodes.append(_(u"%s (stroke and position)") % code_val)
                        elif code_type == u'stroke_diff':
                            miscodes.append(_(u"%s (debatable count)") % code_val)
                        else:
                            lines.append(_(u"Unrecognized misclassification code: %s")
                                         % unicode(code))
                    if miscodes:
                        lines.append(_(u"SKIP miscodes: %s")
                                     % _(u", ").join(miscodes))

        if self.dcodes:
            # Probably we should sort these in some way... but for
            # now, just display.
            for k, v in self.dcodes.iteritems():
                k_desc = kanjidic2_key_to_str(k)
                if k == "moro":
                    # v is a (index, volume, page) tuple.  v/p may be null.
                    if v[1] or v[2]:
                        v = u"index %s, volume %d, page %d" % v
                    else:
                        v = unicode(v[0])
                lines.append(_(u"%s: %s") % (k_desc, v))

        if self.radname:
            lines.append(_(u"Radical name: %s") % self.radname)
        if self.radical:
            lines.append(_(u"Nelson Radical: %d") % self.radical)
        if self.radical_c:
            lines.append(_(u"KangXi Zidian Radical: %d") % self.radical_c)

        if self.korean_h:
            lines.append(_(u"Korean: %s")
                         % _(u", ").join(self.korean_h))
        if self.korean_r:
            lines.append(_(u"Korean romanization: %s")
                         % _(u", ").join(self.korean_r))
        if self.pinyin:
            lines.append(_(u"Pinyin romanization: %s")
                         % _(u", ").join(self.pinyin))

        # "self.unicode" is always present. ;)
        lines.append(_(u"Unicode: 0x%04X") % ord(self.literal))

        if self.cps:
            for jis_set, kuten in self.cps:
                # jis_set == "jis###" - we'll just splice the last 3 digits in
                hexcode = jis_kuten_to_hex(kuten)
                lines.append(_(u"JIS X 0%s code: Kuten = %s, Hex = 0x%04X")
                             % (jis_set[3:], kuten, hexcode))

        if self.xref:
            for var_type, code in self.xref:
                d = {
                    'jis208': u'JIS X 0208',
                    'jis212': u'JIS X 0212',
                    'jis213': u'JIS X 0213',
                    'deroo': u'De Roo',
                    'njecd': u'Halpern NJECD',
                    's_h': u'Kanji Dictionary (Spahn/Hadamitzky)',
                    'nelson_c': u'"Classic" Nelson',
                    'oneill': u"Japanese Names (O'Neill)",
                    'ucs': u'Unicode hex'
                    }
                s = d.get(var_type, var_type)
                if var_type[:3] == u'jis':
                    hexcode = jis_kuten_to_hex(code)
                    lines.append(_(u"Crossref: JIS X 0208: Kuten = %s, "
                                   u"Hex = 0x%04X") % (code, hexcode))
                else:
                    lines.append(_(u"Crossref: %s code: %s") % (s, code))

        return u"\n".join(lines)

class KD2SAXHandler(xml.sax.handler.ContentHandler):

    """SAX handler for KANJIDIC2.

    If not using caching, parsing should take a minimal amount of
    memory as only the matching results are stored and returned.  A
    single non-cached search will be slightly faster than a cached one
    (over 10% on my machine).  However, realistically this function
    should only be used for systems which are severely strapped for
    memory.

    Further, rather than using KANJIDIC2, why not just use classic
    KANJIDIC?

    """

    def __init__(self, use_cache, search_str, *args, **kwargs):
        xml.sax.handler.ContentHandler.__init__(self, *args, **kwargs)
        self.parsing = False
        self.kanji = None
        self.path = []
        self.full_keys = set()
        self.data = {}

        self.use_cache = use_cache
        self.search_str = search_str

    def get_path(self):
        return u"/".join([i[0] for i in self.path])

    def get_attr_str(self):
        return u", ".join([u"%s: %s" % (k, v)
                           for k, v in self.path[-1][1].items()])

    def startElement(self, name, attrs):
        if name == "character":
            self.parsing = True
            #print "startElement called:", name, attrs
            #print "Beginning of character entry found"
            self.kanji = Kanjidic2Entry()
        elif self.parsing:
            self.path.append((name, attrs))
            #print u"Current path: %s, attributes: %s" % \
            #      (self.get_path(), str(attrs.items()))

    def endElement(self, name):
        if self.parsing:
            if self.path:
                if name != self.path[-1][0]:
                    # Shouldn't ever happen, but mistakes *can* slip in...
                    print u"Mismatch detected, path is %s, element name is %s" \
                          % (self.get_path(), name)
                else:
                    self.path.pop()
            if name == "character":
                #print "endElement called:", name
                #print "End of character entry reached"
                if self.use_cache or (self.kanji.literal in self.search_str):
                    self.data[self.kanji.literal] = self.kanji
                self.kanji = None
                self.parsing = False

    def characters(self, content):
        content = content.strip()
        if content and self.parsing:
            node, attrs = self.path[-1]

            # I am exploiting the fact that any given element type can
            # only belong to one type of parent.  For example,
            # "reading" objects are always fully pathed-out to
            # reading_meaning.rmgroup.reading.

            # In case this changes in the future, I've attached
            # comments of the full paths below.

            if node == u"literal":     # literal
                self.kanji.literal = content
            elif node == u"reading":   # reading_meaning/rmgroup/reading
                # These will do stuff in the future...
                #on_type = attrs.get(u"on_type")
                #r_status = attrs.get(u"r_status")
                # Store reading
                getattr(self.kanji, attrs[u'r_type']).append(content)
            elif node == u"meaning":   # reading_meaning/rmgroup/meaning
                m_lang = attrs.get(u'm_lang', u'en')
                self.kanji.meanings.setdefault(m_lang, []).append(content)
            elif node == u"nanori":    # reading_meaning/nanori
                self.kanji.nanori.append(content)
            elif node == u"grade":     # misc/grade
                self.kanji.grade = int(content)
            elif node == u"freq":      # misc/freq
                self.kanji.freq = int(content)
            elif node == u"jlpt":      # misc/jlpt
                self.kanji.jlpt = int(content)
            elif node == u"stroke_count":   # misc/strokes
                if not self.kanji.strokes:
                    self.kanji.strokes = int(content)
                else:
                    self.kanji.strokes_miss.append(int(content))
            elif node == u"q_code":    # query_code/q_code
                qc_type = attrs[u'qc_type']
                if qc_type == 'skip':
                    misclass = attrs.get(u'skip_misclass')
                    if misclass:
                        self.kanji.misclass.append((misclass, content))
                    else:
                        self.kanji.qcodes[qc_type] = content
                else:
                    self.kanji.qcodes[qc_type] = content
            elif node == u"dic_ref":          # dic_number/dic_ref
                attr = attrs[u'dr_type']
                if attr == u'moro':
                    m_vol = attrs.get(u'm_vol')
                    m_page = attrs.get(u'm_page')
                    if m_vol: m_vol = int(m_vol)
                    if m_page: m_page = int(m_page)
                    self.kanji.dcodes[attr] = (content, m_vol, m_page)
                else:
                    try:
                        self.kanji.dcodes[attr] = int(content)
                    except ValueError:
                        self.kanji.dcodes[attr] = content

            elif node == u"cp_value":  # codepoint/cp_value
                cp_type = attrs[u'cp_type']
                if cp_type != u'ucs':
                    self.kanji.cps.append((cp_type, content))
            elif node == u"rad_value": # radical/rad_value
                rad_type = attrs[u'rad_type']
                if rad_type == "classical":
                    self.kanji.radical_c = int(content)
                else: # nelson_c
                    self.kanji.radical = int(content)
            elif node == u"variant":   # misc/variant
                var_type = attrs[u'var_type']
                self.kanji.xref.append((var_type, content))
            elif node == u"rad_name":  # misc/rad_name
                self.kanji.radname = content
            else:  # Anything unhandled...
                try:
                    path = self.get_path()
                    print u"Characters found: path=%s, attrs=(%s), content: %s" \
                          % (path,
                             self.get_attr_str(),
                             content)
                except UnicodeEncodeError:
                    pass  # Can't display code on console; just squelch the output.
                except Exception, e:
                    print u"EXCEPTION occurred:", \
                          unicode(e.__class__.__str__), unicode(e)

class Parser(object):

    def __init__(self, filename, use_cache=True, encoding="utf-8"):
        """Initializer for Kanjidic2Parser.

        About use_cache: Kanjidic2 is a large, heavy to parse file.
        Although it takes a large amount of memory, it is ideal to
        retain it in memory to increase the speed of subsequent
        searches.

        """
        if not os.path.exists(filename):
            raise Exception("Dictionary file does not exist.")
        self.filename = filename
        self.encoding = encoding
        self.cache = None
        self.use_cache = use_cache

    def load_via_sax(self, use_cache, search_str):
        if len(self.filename) >= 3 and self.filename[-3:] == ".gz":
            f = gzip.open(self.filename)
        else:
            f = open(self.filename, "rb")

        sh = KD2SAXHandler(use_cache, search_str)
        isource = xml.sax.xmlreader.InputSource()
        isource.setEncoding("utf-8")
        isource.setByteStream(f)
        xml.sax.parse(isource, sh)
        f.close()
        return sh.data

    def search(self, search_str):
        data = None
        if self.use_cache: data = self.cache
        if not data:
            # Pick a loader.
            # Opt 1: sax... very powerful, but too much code with my impl?
            # Opt 2: elementtree... more memory required, loads
            # everything at once...
            # Opt 3: sax... redo to store all vars as lists, or similar.

            # First attempt of a SAX style loader.
            data = self.load_via_sax(self.use_cache, search_str)

            if self.use_cache: self.cache = data

        for char in search_str:
            kanji = data.get(char)
            if kanji: yield kanji


if __name__ == "__main__":
    import sys, os

    if len(sys.argv) < 2:
        print _(u"Please specify a dictionary file.")
        exit(-1)
    try:
        kp = Parser(sys.argv[1])
    except Exception, e:
        print _(u"Could not create Kanjidic2Parser: %s") % unicode(e)
        exit(-1)

    if len(sys.argv) < 3:
        print _(u"Please specify a kanji.  "
                u"(Copy/paste, or Alt-Zenkaku/Hankaku)")
        exit(-1)

    if os.name == "nt":
        charset = "cp932"
    else:
        charset = "utf-8"

    for i, kanji in enumerate(kp.search(sys.argv[2].decode(charset))):
        lines = kanji.to_string().split(u'\n')
        def encode_or_else(s):
            try:
                val = s.encode("cp932")
                val = s
            except:
                val = None
            return val
        xlines = map(encode_or_else, lines)
        xlines = [l for l in xlines if l]
        xlines = u"\n".join(list(xlines))
        print _(u"Entry %d:\n%s\n") % (i+1, xlines)
