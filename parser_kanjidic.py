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


class KanjidicEntry(object):

    def __init__(self):
        # Key info
        self.literal = None
        self.meanings = []
        self.kunyomi = []
        self.onyomi = []
        self.nanori = []

        # Secondary info
        self.strokes = None
        self.strokes_alt = []
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

    def __unicode__(self):
        """Dummy string dumper"""
        strs = [self.literal]
        for l in [self.kunyomi, self.onyomi, self.nanori, self.meanings]:
            strs.extend(l)
        if self.radname:
            strs.insert(3, self.radname)

        return u", ".join(strs)

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
                    entry.strokes_alt.append(i)
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


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print _("Please specify a dictionary file.")
        exit(-1)
    try:
        kp = KanjidicParser(sys.argv[1])
    except Exception, e:
        print _("Could not create KanjidicParser: %s") % str(e)
        exit(-1)

    err_count = 0
    entry = kp.get_entry()
    while entry:
        try:
            if entry.unparsed:
                lines = []
                lines.append(_(u"[%s] Unparsed: [%s]")
                             % (entry.literal, ", ".join(entry.unparsed)))
                print u"\n".join(lines)
        except UnicodeEncodeError, e:
            err_count += 1
        entry = kp.get_entry()
    if err_count:
        print _("Warning: could not print %d entries, since they could not be "
                "properly displayed on your terminal.") % err_count
