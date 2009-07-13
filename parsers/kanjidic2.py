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

"""A parser for KANJIDIC2.

This module is incomplete and currently just holds helper code for the
KANJIDIC parser.

"""

import gzip, xml.sax, gettext
gettext.install('pyjben', unicode=True)

from parsers.kanjidic_common \
     import jstring_convert, kanjidic2_key_to_str, qcode_to_desc

class Kanjidic2Entry(object):

    def __init__(self):
        # Key info
        self.literal = None
        self.jis = None
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
        # Non-D codes: H, N, V, INnnnn, MNnnnnnnn/MPnn.nnnn, Ennnn, Knnnn, Lnnnn, Onnnn
        # D codes: DB, DC, DF, DG, DH, DJ, DK, DM, DO, DR, DS, DT, DM
        self.dcodes = {}

        # Dictionary-related metadata
        self.xref = []
        self.misclass = []

        self.unparsed = []

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
                    for code in self.misclass:
                        code_type = code[:2]
                        code_val = code[2:]
                        if code_type == u'SP':   # "stroke_count"
                            miscodes.append(_(u"%s (stroke count)") % code_val)
                        elif code_type == u'PP': # "posn"
                            miscodes.append(_(u"%s (position)") % code_val)
                        elif code_type == u'BP': # "stroke_and_posn"
                            miscodes.append(_(u"%s (stroke and position)") % code_val)
                        elif code_type == u'RP': # "stroke_diff"
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
                k = kanjidic2_key_to_str(k)
                lines.append(_(u"%s: %s") % (k, v))

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
        if self.jis:
            def jis_hex_to_kuten(hex_code):
                """KANJIDIC2-style kuten string"""
                return u"%s-%s" % (
                    (((hex_code >> 8) & 0xFF) - 0x20),
                    ((hex_code & 0xFF) - 0x20))

            kuten = jis_hex_to_kuten(self.jis)
            lines.append(_(u"JIS code: Kuten = %s, Hex = 0x%04X")
                         % (kuten, self.jis))

        #self.xref = []
        if self.xref:
            # From KANJIDIC documentation:
            #
            # Xxxxxxx -- a cross-reference code. An entry of, say,
            # XN1234 will mean that the user is referred to the kanji
            # with the (unique) Nelson index of 1234. XJ0xxxx and
            # XJ1xxxx are cross-references to the kanji with the JIS
            # hexadecimal code of xxxx. The `0' means the reference is
            # to a JIS X 0208 kanji, and the `1' references a JIS X
            # 0212 kanji.
            #

            # For now, just dump to the console.
            lines.append(_(u"Crossref codes: %s") % ", ".join(self.xref))

            # From J-Ben 1:
            #/* Crossref codes */
            #if(!k.var_j208.empty())
            #result << "<li>JIS-208: " << k.var_j208 << "</li>";
            #if(!k.var_j212.empty())
            #result << "<li>JIS-212: " << k.var_j212 << "</li>";
            #if(!k.var_j213.empty())
            #result << "<li>JIS-213: " << k.var_j213 << "</li>";
            #if(!k.var_ucs.empty())
            #result << "<li>Unicode: " << k.var_ucs << "</li>";
            #if(!k.var_deroo.empty())
            #result << "<li>De Roo code: " << k.var_deroo << "</li>";
            #if(!k.var_nelson_c.empty())
            #result << "<li>Modern Reader's Japanese-English Character "
            #"Dictionary (Nelson): " << k.var_nelson_c << "</li>";
            #if(!k.var_njecd.empty())
            #result << "<li>New Japanese-English Character Dictionary "
            #"(Halpern): " << k.var_njecd << "</li>";
            #if(!k.var_oneill.empty())
            #result << "<li>Japanese Names (O'Neill): " << k.var_oneill
            #<< "</li>";
            #if(!k.var_s_h.empty())
            #result << "<li>Spahn/Hadamitzky Kanji Dictionary code: "
            #<< k.var_s_h << "</li>";

        if self.unparsed:
            lines.append(_(u"Unrecognized codes: %s")
                         % (u", ").join(self.unparsed))

        return u"\n".join(lines)

class KD2SAXHandler(xml.sax.handler.ContentHandler):

    """SAX handler for KANJIDIC2."""

    def __init__(self, *args, **kwargs):
        #self.limit = 1
        xml.sax.handler.ContentHandler.__init__(self, *args, **kwargs)
        self.parsing = False
        self.kanji = None
        self.path = []
        self.full_keys = set()
        self.data = {}

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
                self.data[self.kanji.literal] = self.kanji
                self.kanji = None
                self.parsing = False
                #self.limit -= 1
                #if self.limit <= 0: exit(0)

    def characters(self, content):
        content = content.strip()
        if content and self.parsing:
            # Sanity check: see if the current node type is already
            # included under a different full path.
            #path = self.get_path()
            #self.full_keys.add(path)
            #
            #keys = [k for k in self.full_keys if k[-(len(node)):] == node]
            #if len(keys) != 1:
            #    print "CHECKME: Node: %s, Keys: %s" % (node, str(keys))

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
                        # HANDLE LATER, TODO
                        pass
                    else:
                        self.kanji.qcodes[qc_type] = content
                else:
                    self.kanji.qcodes[qc_type] = content
            elif node == u"dic_ref":          # dic_number/dic_ref
                attr = attrs[u'dr_type']
                if attr == u'moro':
                    m_vol = attrs.get(u'm_vol')
                    m_page = attrs.get(u'm_page')
                    # Do something with this... TODO
                else:
                    try:
                        self.kanji.dcodes[attr] = int(content)
                    except ValueError:
                        self.kanji.dcodes[attr] = content
            elif node == u"cp_value":  # codepoint/cp_value
                pass
            elif node == u"rad_value": # radical/rad_value
                pass
            elif node == u"variant":   # misc/variant
                pass
            elif node == u"rad_name":  # misc/rad_name
                pass
            else:
                try:
                    path = self.get_path()
                    print u"Characters found: path=%s, attrs=(%s), content: %s" \
                          % (path,
                             self.get_attr_str(),
                             content)
                    # Do some stuff based upon the current path and content
                except UnicodeEncodeError:
                    pass  # Can't display code on console; just squelch the output.
                except Exception, e:
                    print u"EXCEPTION occurred:", unicode(e.__class__.__str__), unicode(e)

class Kanjidic2Parser(object):

    def __init__(self, filename, encoding="utf-8"):
        self.filename = filename
        self.encoding = encoding
        self.cache = None

    def load_via_sax(self):
        if len(self.filename) >= 3 and self.filename[-3:] == ".gz":
            f = gzip.open(self.filename)
        else:
            f = open(self.filename, "rb")

        sh = KD2SAXHandler()
        isource = xml.sax.xmlreader.InputSource()
        isource.setEncoding("utf-8")
        isource.setByteStream(f)
        xml.sax.parse(isource, sh)
        f.close()
        self.cache = sh.data

    def search(self, search_str, use_cache=True):
        # Cacheing has 2 meanings in J-Ben:
        # 1. Storing the results of a previous read locally.
        # 2. Reading in prepased data from a file on disk
        #
        # KANJIDIC2 is a huge file; although it's huge to store it in memory,
        # it's even harsher to repeatedly seek the whole file from disk on
        # each search.
        if (not use_cache) or (not self.cache):
            # Pick a loader.
            # Opt 1: sax... very powerful, but too much code with my impl?
            # Opt 2: elementtree... more memory required, loads
            # everything at once...
            # Opt 3: sax... redo to store all vars as lists, or similar.
            self.load_via_sax()  # First attempt of a SAX style loader.

        for char in search_str:
            kanji = self.cache.get(char)
            if kanji: yield kanji


if __name__ == "__main__":
    import sys, os

    if len(sys.argv) < 2:
        print _(u"Please specify a dictionary file.")
        exit(-1)
    try:
        kp = Kanjidic2Parser(sys.argv[1])
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
