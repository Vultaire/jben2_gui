#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gettext
gettext.install('pyjben', unicode=True)

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

def jstring_convert(us):
    """Convert's from Jim Breen's -x.xx- notation to 〜x(xx)〜 notation."""
    if us[0] == u'-' or us[-1] == u'-':
        us = us.replace(u'-', u'〜')
    parts = us.split('.', 1)
    if len(parts) == 1: return us
    return u"%s(%s)" % tuple(parts)

class KanjidicEntry(object):

    def __init__(self):
        # Key info
        self.literal = None
        self.jis = None
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
        self.radical = None
        self.radical_c = None  # "Classic" KangXi Zidian radical
        self.radname = None
        self.pinyin = []
        self.korean = []

        # "Query codes": Pattern-based lookup
        # Includes SKIP, DeRoo, Spahn/Hadamitzky, and Four Corners systems
        # Codes: P, DRnnnn, Inxnn.n, Qnnnn.n
        self.skip = []
        self.deroo = None
        self.sh_desc = None
        self.fc = None

        # Dictionary codes
        # Non-D codes: H, N, V, INnnnn, MNnnnnnnn/MPnn.nnnn, Ennnn, Knnnn, Lnnnn, Onnnn
        # D codes: DB, DC, DF, DG, DH, DJ, DK, DM, DO, DR, DS, DT, DM
        self.dcodes = {}

        # Dictionary-related metadata
        self.xref = []
        self.misclass = []

        self.unparsed = []

    def to_string(self, **kwargs):
        """A default "to-string" dump of a KanjidicEntry."""
        lines = []
        lines.append(self.literal)
        if self.onyomi:
            lines.append(_(u"Onyomi: %s")
                         % u" ".join(
                             [jstring_convert(us) for us in self.onyomi]))
        if self.kunyomi:
            lines.append(_(u"Kunyomi: %s")
                         % u" ".join(
                             [jstring_convert(us) for us in self.kunyomi]))
        if self.nanori:
            lines.append(_(u"Nanori: %s")
                         % u" ".join(
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
        if self.skip:
            lines.append(_(u"SKIP code: %s")
                         % _(u", ").join(self.skip))
        if self.misclass:
            miscodes = []
            for code in self.misclass:
                code_type = code[:3]
                code_val = code[3:]
                if code_type == u'ZSP': # "stroke_count"
                    miscodes.append(_(u"%s (stroke count)") % code_val)
                elif code_type == u'ZPP': # "posn"
                    miscodes.append(_(u"%s (position)") % code_val)
                elif code_type == u'ZBP':   # "stroke_and_posn"
                    miscodes.append(_(u"%s (stroke and position)") % code_val)
                elif code_type == u'ZRP': # "stroke_diff"
                    miscodes.append(_(u"%s (debatable count)") % code_val)
                else:
                    lines.append(_(u"Unrecognized misclassification code: %s")
                                 % unicode(code))
            if miscodes:
                lines.append(_(u"SKIP miscodes: %s")
                             % _(u", ").join(miscodes))
        if self.deroo:
            lines.append(_(u"De Roo code: %s") % self.deroo)
        if self.sh_desc:
            lines.append(_(u"Spahn/Hadamitzky Kanji Dictionary code: %s")
                         % self.sh_desc)
        if self.fc:
            lines.append(_(u"Four Corner code: %s") % self.fc)
        # STILL NEED TO HANDLE THESE:
        #self.dcodes = {}
        if self.dcodes:
            # Need to handle on a per dict basis
            pass

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
            pass

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

    def __init__(self, filename, encoding="EUC-JP"):
        f = open(filename, "rb")
        data = f.read()
        f.close()
        data = data.decode(encoding)
        self.data = data.splitlines()

    def get_entry(self):
        line = None
        while self.data and (not line or line[0] == u"#"):
            line = self.data.pop(0).strip()
        return self.parse_line(line)


    def _parse_japanese(self, entry, state, data):
        if not state.t_class:
            # Check hiragana/katakana
            for c in data:
                if is_hiragana(c):
                    entry.kunyomi.append(data)
                    break
                elif is_katakana(c):
                    entry.onyomi.append(data)
                    break
        elif state.t_class == 1:
            entry.nanori.append(data)
        elif state.t_class == 2:
            entry.radname = data

    def _parse_info(self, entry, state, data):
        try:
            c = data[0]
            if c == 'U':
                # Unicode value - we alread store the literal as unicode, so let's
                # use this as our encoding sanity check!
                assert ord(entry.literal) == int(data[1:], 16), \
                    "Encoding error detected"
            elif c == 'B':
                entry.radical = int(data[1:])
            elif c == 'C':
                entry.radical_c = int(data[1:])
            elif c == 'F':
                entry.freq = int(data[1:])
            elif c == 'G':
                entry.grade = int(data[1:])
            elif c == 'J':
                entry.jlpt = int(data[1:])
            elif c == 'S':
                i = int(data[1:])
                if not entry.strokes:
                    entry.strokes = i
                else:
                    entry.strokes_miss.append(i)
            elif c == 'W':
                entry.korean.append(data[1:])
            elif c == 'Y':
                entry.pinyin.append(data[1:])
            elif c == 'X':
                entry.xref.append(data[1:])
            elif c == 'Z':
                entry.misclass.append(data[1:])
            elif c == 'T':
                state.t_class = int(data[1:])
            # Below this point is dictionary/query codes.
            # Much of this is copied and modified from J-Ben 1's source code.
            elif c == 'H':
                # New Japanese-English Character Dictionary (Halpern)
                entry.dcodes["halpern_njecd"] = data[1:]
            elif c == 'N':
                # Modern Reader's Japanese-English Character Dictionary (Nelson)
                entry.dcodes["nelson_c"] = data[1:]
            elif c == 'V':
                # The New Nelson's Japanese-English Character Dictionary
                entry.dcodes["nelson_n"] = data[1:]
            elif c == 'P':
                # SKIP codes.
                # Thanks to changes in permissible SKIP code usage (change to
                # Creative Commons licensing in January 2008), we can now use
                # this without problems.
                entry.skip.append(data[1:]);
            elif c == 'I':  # Spahn/Hadamitzky dictionaries
                if data[1] =='N':
                    # Kanji & Kana (Spahn, Hadamitzky)
                    entry.dcodes["sh_kk"] = data[2:]
                else:
                    # Query Code: Kanji Dictionary (Spahn, Hadamitzky)
                    entry.sh_desc = data[1:]
            elif c == 'Q':
                # Four Corner code
                entry.fc = data[1:]
            elif c == 'M':
                if data[1] == 'N':
                    # Morohashi Daikanwajiten Index
                    #entry.dcodes["moro"].insert(0,"] ps->substr(2));
                    pass
                elif data[1] == 'P':
                    # Morohashi Daikanwajiten Volume/Page
                    #entry.dcodes["moro"] \
                    #    .append(1, '/').append(ps->substr(2));
                    pass
            elif c == 'E':
                # A Guide to Remembering Japanese Characters (Henshall)
                entry.dcodes["henshall"] = data[1:]
            elif c == 'K':
                # Gakken Kanji Dictionary ("A New Dictionary of Kanji Usage")
                entry.dcodes["gakken"] = data[1:]
            elif c == 'L':
                # Remembering the Kanji (Heisig)
                entry.dcodes["heisig"] = data[1:]
            elif c == 'O':
                # Japanese Names (O'Neill)
                entry.dcodes["oneill_names"] = data[1:]
            elif c == 'D':
                c = data[1]
                if c == 'B':
                    # Japanese for Busy People (AJLT)
                    entry.dcodes["busy_people"] = data[2:]
                elif c == 'C':
                    # The Kanji Way to Japanese Language Power (Crowley)
                    entry.dcodes["crowley"] = int(data[2:])
                elif c == 'F':
                    # Japanese Kanji Flashcards (White Rabbit Press)
                    entry.dcodes["jf_cards"] = int(data[2:])
                elif c == 'G':
                    # Kodansha Compact Kanji Guide
                    entry.dcodes["kodansha_compact"] = int(data[2:])
                elif c == 'H':
                    # A Guide To Reading and Writing Japanese (Henshall)
                    entry.dcodes["henshall3"] = int(data[2:])
                elif c == 'J':
                    # Kanji in Context (Nishiguchi and Kono)
                    entry.dcodes["kanji_in_context"] = int(data[2:])
                elif c == 'K':
                    # Kodansha Kanji Learner's Dictionary (Halpern)
                    entry.dcodes["halpern_kkld"] = int(data[2:])
                elif c == 'O':
                    # Essential Kanji (O'Neill)
                    entry.dcodes["oneill_kk"] = int(data[2:])
                elif c == 'R':
                    # Query Code: 2001 Kanji (De Roo)
                    entry.deroo = int(data[2:])
                elif c == 'S':
                    # A Guide to Reading and Writing Japanese (Sakade)
                    entry.dcodes["sakade"] = int(data[2:])
                elif c == 'T':
                    # Tuttle Kanji Cards (Kask)
                    entry.dcodes["tutt_cards"] = int(data[2:])
                elif c == 'M':
                    # Yves Maniette's French adaption of Heisig
                    entry.dcodes["maniette"] = int(data[2:])
                else:
                    entry.unparsed.append(data)
            else:
                entry.unparsed.append(data)
        except:
            entry.unparsed.append(data)

    def parse_line(self, line):
        if not line:
            return None
        entry = KanjidicEntry()
        state = ParserState()  # Holds "t class"

        # First 2 fields are always the same
        pieces = line.split(None, 2)
        entry.literal = pieces.pop(0)
        entry.jis = int(pieces.pop(0), 16)
        misc = pieces.pop()

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

                self._parse_japanese(entry, state, sub)
            elif c == u'{':
                # Parse Translation
                si += 1  # Move si inside of {
                ei = misc.find(u'}', si+1)
                if ei == -1:
                    ei = len(misc) + 1
                sub = misc[si:ei]
                ei += 1  # Move ei past }

                entry.meanings.append(sub)
            else:
                # Parse info field
                ei = misc.find(u' ', si+1)
                if ei == -1:
                    ei = len(misc) + 1
                sub = misc[si:ei]

                self._parse_info(entry, state, sub)

            si = ei + 1

        return entry

    def search(self, literal):
        entry = self.get_entry()
        while entry:
            if literal == entry.literal: break
            entry = self.get_entry()
        return entry


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
        charset = "sjis"
    else:
        charset = "utf-8"
    entry = kp.search(sys.argv[2].decode(charset))
    print "RESULTS:", entry.to_string()

#    err_count = 0
#    entry = kp.get_entry()
#    while entry:
#        try:
#            if entry.unparsed:
#                lines = []
#                lines.append(_(u"[%s] Unparsed: [%s]")
#                             % (entry.literal, ", ".join(entry.unparsed)))
#                print u"\n".join(lines)
#        except UnicodeEncodeError, e:
#            err_count += 1
#        entry = kp.get_entry()
#    if err_count:
#        print _(u"Warning: could not print %d entries, since they could not be "
#                 "properly displayed on your terminal.") % err_count
