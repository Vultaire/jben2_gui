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

import gzip, gettext
from xml.etree.cElementTree import ElementTree
gettext.install('pyjben', unicode=True)

from .kanjidic_common \
     import jstring_convert, kanjidic2_key_to_str, qcode_to_desc

def jis_kuten_to_hex(kuten):
    """Kuten string to hex conversion"""
    pieces = map(int, kuten.split(u'-'))
    print "DEBUG: kuten: %s, pieces: %s" % (kuten, str(pieces))
    return ((pieces[0] + 0x20) << 8) + (pieces[1] + 0x20)


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
        return header, characters

    def get_header(self):
        d = {}
        for o in self.header.getchildren():
            cdata = "".join((o.text, o.tail)).strip()
            d[o.tag] = cdata
        return "\n".join("%s: %s" % (k, d[k]) for k in sorted(d))


if __name__ == "__main__":
    import sys, os

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

    print "HEADER:\n{\n%s\n}" % p.get_header()
    print "%d characters found" % len(p.characters)
    for i, elem in enumerate(p.characters):
        print
        print "TAG:", elem.tag
        print "TEXT:", "".join((elem.text, elem.tail)).strip()
        print "CHILDREN:", elem.getchildren()
        print "LITERAL:", elem.find("literal").text
        skip_codes = [e for e in elem.findall("query_code/q_code")
                   if e.attrib['qc_type'] == 'skip']
        print "SKIP CODES:", ", ".join(e.text for e in skip_codes)
        if i >= 2: break

    exit(0)

    #for i, kanji in enumerate(kp.search(sys.argv[2].decode(charset))):
    #    lines = kanji.to_string().split(u'\n')
    #    def encode_or_else(s):
    #        try:
    #            val = s.encode("cp932")
    #            val = s
    #        except:
    #            val = None
    #        return val
    #    xlines = map(encode_or_else, lines)
    #    xlines = [l for l in xlines if l]
    #    xlines = u"\n".join(list(xlines))
    #    print _(u"Entry %d:\n%s\n") % (i+1, xlines)
