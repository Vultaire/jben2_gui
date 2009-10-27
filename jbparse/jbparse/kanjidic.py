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

"""A parser for KANJIDIC.

This parser is dependent on a small amount of code kept in the
kanjidic2 parser, so be sure to grab both if you are using these
modules in your own programs.

"""

from __future__ import absolute_import

import re, gzip, gettext
gettext.install('pyjben', unicode=True)

from .kanjidic_common \
     import jstring_convert, kanjidic2_key_to_str, qcode_to_desc


alpha_regex = re.compile(u"(^[^0-9]+)(.*)")

# Copied from J-Ben 1.x and modified using Gnome Character Map's
# "Unicode Block" information.
# Verified against http://unicode.org/Public/UNIDATA/Blocks.txt.

def is_hiragana(uc):
    # 3040..309F; Hiragana
    o = ord(uc)
    return o >= 0x3040 and o <= 0x309F

def is_katakana(uc):
    # 30A0..30FF; Katakana
    # 31F0..31FF; Katakana Phonetic Extensions (Not currently used in J-Ben)
    o = ord(uc)
    return o >= 0x30A0 and o <= 0x30FF

def is_furigana(uc):
    return is_hiragana(uc) or is_katakana(uc)

def jis_hex_to_kuten(hex_code):
    """KANJIDIC2-style kuten string"""
    return u"%s-%s" % (
        (((hex_code >> 8) & 0xFF) - 0x20),
        ((hex_code & 0xFF) - 0x20))

def kanjidic_key_to_kanjidic2(dkey):
    """Converts KANJIDIC dictionary keys to KANJIDIC2.

    If unable to find a KANJIDIC2 key, returns the original key.

    """
    d = {
        "H": "halpern_njecd",
        "N": "nelson_c",
        "V": "nelson_n",
        "IN": "sh_kk",
        "MN": "moro",
        "E": "henshall",
        "K": "gakken",
        "L": "heisig",
        "O": "oneill_names",
        "DB": "busy_people",
        "DC": "crowley",
        "DF": "jf_cards",
        "DG": "kodansha_compact",
        "DH": "henshall3",
        "DJ": "kanji_in_context",
        "DK": "halpern_kkld",
        "DO": "oneill_kk",
        "DS": "sakade",
        "DT": "tutt_cards",
        "DM": "maniette"
        }
    return d.get(dkey, dkey)

class KanjidicEntry(object):

    def __init__(self, raw_entry):
        # Key info
        self.literal = None
        self.meanings = []
        self.kunyomi = []
        self.onyomi = []
        self.nanori = []
        # Secondary info
        self.strokes = None
        self.strokes_miss = []
        self.freq = None
        self.grade = None
        self.jlpt = None
        # Info of low importance for most target users
        self.jis = None
        self.radical = None
        self.radical_c = None  # "Classic" KangXi Zidian radical
        self.radname = None
        self.pinyin = []
        self.korean = []
        # "Query codes": Pattern-based lookup
        # Includes SKIP, DeRoo, Spahn/Hadamitzky, and Four Corners systems
        self.qcodes = {}
        # Dictionary codes
        self.dcodes = {}
        # Dictionary-related metadata
        self.xref = []
        self.misclass = []
        self.unparsed = []

        self.parse_entry(raw_entry)

    def parse_entry(self, raw_entry):
        if not raw_entry:
            return None

        state = ParserState()  # Holds "t class"

        # First 2 fields are always the same
        pieces = raw_entry.split(None, 2)
        misc = pieces.pop()
        self.jis = int(pieces.pop(), 16)
        self.literal = pieces.pop()

        # Parse the remainder
        si = ei = 0
        while si < len(misc):
            c = misc[si]
            i = ord(c)
            if c == u' ':
                si += 1
                continue
            if i > 0xFF or c in (u'-', u'.'):
                # Parse Japanese
                ei = misc.find(u' ', si+1)
                if ei == -1:
                    ei = len(misc) + 1
                sub = misc[si:ei]

                self._parse_japanese(state, sub)
            elif c == u'{':
                # Parse Translation
                si += 1  # Move si inside of {
                ei = misc.find(u'}', si+1)
                if ei == -1:
                    ei = len(misc) + 1
                sub = misc[si:ei]
                ei += 1  # Move ei past }

                self.meanings.append(sub)
            else:
                # Parse info field
                ei = misc.find(u' ', si+1)
                if ei == -1:
                    ei = len(misc) + 1
                sub = misc[si:ei]

                self._parse_info(state, sub)

            si = ei + 1

    def _parse_japanese(self, state, data):
        if not state.t_class:
            # Check hiragana/katakana
            for c in data:
                if is_hiragana(c):
                    self.kunyomi.append(data)
                    break
                elif is_katakana(c):
                    self.onyomi.append(data)
                    break
        elif state.t_class == 1:
            self.nanori.append(data)
        elif state.t_class == 2:
            self.radname = data

    def _parse_info(self, state, data):
        onechar_dicts = set(('H', 'N', 'V', 'E', 'K', 'L', 'O'))
        strval_dicts = set(('DB',))
        intval_dicts = set(('DC', 'DF', 'DG', 'DH', 'DJ',
                            'DK', 'DO', 'DS', 'DT', 'DM'))
        try:
            c = data[0]
            if c == 'U':
                # Unicode value - we alread store the literal as unicode, so let's
                # use this as our encoding sanity check!
                assert ord(self.literal) == int(data[1:], 16), \
                    "Encoding error detected"
            elif c == 'B':
                self.radical = int(data[1:])
            elif c == 'C':
                self.radical_c = int(data[1:])
            elif c == 'F':
                self.freq = int(data[1:])
            elif c == 'G':
                self.grade = int(data[1:])
            elif c == 'J':
                self.jlpt = int(data[1:])
            elif c == 'S':
                i = int(data[1:])
                if not self.strokes:
                    self.strokes = i
                else:
                    self.strokes_miss.append(i)
            elif c == 'W':
                self.korean.append(data[1:])
            elif c == 'Y':
                self.pinyin.append(data[1:])
            elif c == 'X':
                self.xref.append(data[1:])
            elif c == 'Z':
                self.misclass.append(data[1:])
            elif c == 'T':
                state.t_class = int(data[1:])
            # Below this point is dictionary/query codes.
            elif c in onechar_dicts:
                self.dcodes[c] = data[1:]
            elif c == 'P':
                # SKIP codes.
                # Thanks to changes in permissible SKIP code usage (change to
                # Creative Commons licensing in January 2008), we can now use
                # this without problems.  Jack Halpern, thank you!
                if self.qcodes.get('skip'):
                    print "ALERT!  ALERT!  self.skip already set!"
                    exit(1)
                self.qcodes['skip'] = data[1:];
            elif c == 'Q':
                # Four Corner code
                self.qcodes['four_corner'] = data[1:]
            elif c == 'I':  # Spahn/Hadamitzky dictionaries
                if data[1] =='N':
                    # IN = Kanji & Kana (Spahn, Hadamitzky)
                    self.dcodes[data[:2]] = data[2:]
                else:
                    # Query Code: Kanji Dictionary (Spahn, Hadamitzky)
                    self.qcodes['sh_desc'] = data[1:]
            elif c == 'M':
                # Morohashi Daikanwajiten
                self.dcodes[data[:2]] = data[2:]
            elif c == 'D':
                key = data[:2]
                if key in intval_dicts:
                    self.dcodes[key] = int(data[2:])
                elif key in strval_dicts:
                    self.dcodes[key] = data[2:]
                elif key == 'DR':
                    # Query Code: 2001 Kanji (De Roo)
                    self.qcodes['deroo'] = int(data[2:])
                else:
                    self.unparsed.append(data)
            else:
                self.unparsed.append(data)
        except:
            self.unparsed.append(data)

    def to_string(self, **kwargs):
        """A default "to-string" dump of a KanjidicEntry."""
        lines = []
        lines.append(_(u"Literal: %s") % self.literal)
        if self.onyomi:
            lines.append(_(u"Onyomi: %s")
                         % u"、".join(
                             [jstring_convert(us) for us in self.onyomi]))
        if self.kunyomi:
            lines.append(_(u"Kunyomi: %s")
                         % u"、".join(
                             [jstring_convert(us) for us in self.kunyomi]))
        if self.nanori:
            lines.append(_(u"Nanori: %s")
                         % u"、".join(
                             [jstring_convert(us) for us in self.nanori]))
        if self.meanings:
            lines.append(_(u"Meaning: %s") % _(u"; ").join(self.meanings))

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
                if k == "MP": continue
                k = kanjidic2_key_to_str(
                    kanjidic_key_to_kanjidic2(k))
                if k == "MN":
                    lines.append(_(u"%s: %s") % (k, v))
                else:
                    vp = self.dcodes.get("MP")
                    if vp:
                        vol, page = vp.split('.', 1)
                        lines.append(_(u"%s: Index %s, Volume %s, Page %s")
                                     % (k, v, vol, page))
                    else:
                        lines.append(_(u"%s: %s") % (k, v))

        if self.radname:
            lines.append(_(u"Radical name: %s") % self.radname)
        if self.radical:
            lines.append(_(u"Nelson Radical: %d") % self.radical)
        if self.radical_c:
            lines.append(_(u"KangXi Zidian Radical: %d") % self.radical_c)

        if self.korean:
            lines.append(_(u"Korean romanization: %s")
                         % _(u", ").join(self.korean))
        if self.pinyin:
            lines.append(_(u"Pinyin romanization: %s")
                         % _(u", ").join(self.pinyin))

        # "self.unicode" is always present. ;)
        lines.append(_(u"Unicode: 0x%04X") % ord(self.literal))
        if self.jis:
            kuten = jis_hex_to_kuten(self.jis)
            jis_set = u"208"  # For now, hard-code it.
            lines.append(_(u"JIS X 0%s code: Kuten = %s, Hex = 0x%04X")
                         % (jis_set, kuten, self.jis))

        if self.xref:
            for ref in self.xref:
                if ref[0] == 'J':
                    # JIS crossrefs
                    jis_id = ref[1]
                    hexcode = int(ref[2:], 16)
                    kuten = jis_hex_to_kuten(hexcode)
                    if jis_id == '0':
                        lines.append(_(u"Crossref: JIS X 0208: Kuten = %s, "
                                       u"Hex = 0x%04X") % (kuten, hexcode))
                    elif jis_id == '1':
                        lines.append(_(u"Crossref: JIS X 0208: Kuten = %s, "
                                       u"Hex = 0x%04X") % (kuten, hexcode))
                    else:
                        s = _(u"Crossref: JIS (UNHANDLED JIS CODESET): "
                              u"Kuten = %s, Hex = 0x%04X") % (kuten, hexcode)
                        lines.append(s)
                        # Not really "unparsed", but it is unhandled...
                        unparsed.append(s)
                    pass
                else:
                    m = alpha_regex.match(ref)
                    k = kanjidic2_key_to_str(
                        kanjidic_key_to_kanjidic2(m.group(1)))

                    v = ref[m.span()[1]:]
                    lines.append(_(u"Crossref: %s: %s")
                                 % (k, m.group(2)))

        if self.unparsed:
            lines.append(_(u"Unrecognized codes: %s")
                         % (u", ").join(self.unparsed))
            pass

        return u"\n".join(lines)

    def __unicode__(self):
        """Dummy string dumper"""
        strs = [self.literal]
        for l in [self.kunyomi, self.onyomi, self.nanori, self.meanings]:
            strs.extend(l)
        if self.radname:
            strs.insert(3, self.radname)

        return _(u", ").join(strs)

class ParserState(object):
    def __init__(self):
        self.t_class = 0

class KanjidicParser(object):

    def __init__(self, filename, use_cache=True, encoding="EUC-JP"):
        self.filename = filename
        self.encoding = encoding
        self.use_cache = use_cache
        self.cache = {}

    def search(self, query):
        """Returns a list of kanji entries matching kanji in the query.

        Note: Previous versions implemented this as a generator.
        While I liked that solution, it did not maintain the order of
        kanji in the query.  Since the KANJIDIC2 parser does this,
        I've done it here as well for consistency.

        """
        results = []

        data = None
        if self.use_cache: data = self.cache

        if not data:
            if len(self.filename) >= 3 and self.filename[-3:] == ".gz":
                f = gzip.open(self.filename)
            else:
                f = open(self.filename, "rb")
            fdata = f.read()
            f.close()
            fdata = fdata.decode(self.encoding)
            lines = fdata.splitlines()
            lines = [line for line in lines if line and (line[0] != u"#")]

            data = {}
            for line in lines:
                entry = KanjidicEntry(line)
                if self.use_cache:
                    self.cache[entry.literal] = entry
                if entry.literal in query: data[entry.literal] = entry

        for char in query:
            kanji = data.get(char)
            if kanji: results.append(kanji)

        return results

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
