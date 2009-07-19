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

"""A basic parser for JMdict."""


from xml.sax.handler import ContentHandler, DTDHandler, EntityResolver
from xml.sax.xmlreader import InputSource, XMLReader
import xml.sax
import gzip, gettext
gettext.install('pyjben', unicode=True)

class JMdictEntry(object):

    """JMdict entry.

    For performance/memory reasons, attributes are dynamically
    created.  Safe access to attributes can be done via
    getattr(obj, key, None).

    """

    def to_string(self, **kwargs):
        """A default "to-string" dump of a JMdictEntry."""
        return _(u"<%08X:not_yet_implemented>") % id(self)

class JMDSAXHandler(ContentHandler):

    """SAX handler for JMdict.

    If not using caching, parsing should take a minimal amount of
    memory as only the matching results are stored and returned.  A
    single non-cached search will be slightly faster than a cached one
    (over 10% on my machine).  However, realistically this function
    should only be used for systems which are severely strapped for
    memory.

    Further, rather than using JMdict, why not just use classic EDICT?
    If the extra info is not really needed, it'll greatly speed things
    up to use something else.

    """

    def __init__(self, use_cache, search_str, *args, **kwargs):
        ContentHandler.__init__(self, *args, **kwargs)
        self.parsing = False
        self.entry = None
        self.path = []
        self.full_keys = set()
        self.data = {}
        self.node_content = ""

        self.use_cache = use_cache
        self.search_str = search_str

    def get_path(self):
        return u"/".join([i[0] for i in self.path])

    def get_attr_str(self):
        return u", ".join([u"%s: %s" % (k, v)
                           for k, v in self.path[-1][1].items()])

    def startElement(self, name, attrs):
        if name == "entry":
            self.parsing = True
            self.entry = JMdictEntry()
        elif self.parsing:
            self.path.append((name, attrs))

    def endElement(self, name):
        if self.parsing:
            self.node_content = self.node_content.strip()
            if self.node_content:
                # Assign data as appropriate
                node, attrs = self.path[-1]
                if node == u"ent_seq":   # Unique ID for entry
                    setattr(self.entry, node, int(self.node_content))
                elif node in (u"reb", u"keb"):  # Japanese reading/kanji blobs
                    setattr(self.entry, node, self.node_content)
                elif node == u"re_nokanji":     # A boolean flag
                    setattr(self.entry, node, True)
                else:   # Everything else is a list...
                    data = getattr(self.entry, node, None)
                    if data:
                        data.append(self.node_content)
                    else:
                        setattr(self.entry, node, [self.node_content])
                self.node_content = ""
            if self.path:
                if name != self.path[-1][0]:
                    # Shouldn't ever happen, but mistakes *can* slip in...
                    print u"Mismatch detected, path is %s, element name is %s" \
                          % (self.get_path(), name)
                else:
                    self.path.pop()
            if name == "entry":
                self.entry = None
                self.parsing = False

    def characters(self, content):
        if self.parsing:
            self.node_content += content

    def skippedEntity(self, name):
        # 2 things need to be done here:
        # 1. JMdict entities need to be stored properly
        # 2. Standard XML entities (***IF*** they are ***ALSO*** not parsed)
        #    should be manually put into the character stream.
        if self.parsing:
            if name in (u"lt", u"amp", u"gt", u"quot", u"apos"):
                print u"Houston, we gots ourselves a BIG problem:", name
            else:
                self.node_content += name

from xml.sax.expatreader import ExpatParser
class ExpatParserNoEntityExp(ExpatParser):

    """An overridden Expat parser class which disables entity expansion."""

    def reset(self):
        ExpatParser.reset(self)
        self._parser.DefaultHandler = self.dummy_handler

    def dummy_handler(self, *args, **kwargs):
        pass

class JMdictParser(object):

    def __init__(self, filename, use_cache=True, encoding="utf-8"):
        """Initializer for JMdictParser.

        About use_cache: JMdict is a large, heavy to parse file.
        Although it takes a large amount of memory, it is ideal to
        retain it in memory to increase the speed of subsequent
        searches.

        """
        self.filename = filename
        self.encoding = encoding
        self.cache = None
        self.use_cache = use_cache

    def load_via_sax(self, use_cache, search_str):
        if len(self.filename) >= 3 and self.filename[-3:] == ".gz":
            f = gzip.open(self.filename)
        else:
            f = open(self.filename, "rb")

        sh = JMDSAXHandler(use_cache, search_str)
        isource = InputSource()
        isource.setEncoding("utf-8")
        isource.setByteStream(f)

        # Parser: Since I wish to directly handle the "entities", we
        # need to override default behavior and cannot just use
        # xml.sax.parse.
        parser = ExpatParserNoEntityExp()
        parser.setContentHandler(sh)

        parser.parse(isource)
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
        kp = JMdictParser(sys.argv[1])
    except Exception, e:
        print _(u"Could not create JMdictParser: %s") % unicode(e)
        exit(-1)

    if len(sys.argv) < 3:
        print _(u"Please specify a search query.")
        exit(-1)

    if os.name == "nt":
        charset = "cp932"
    else:
        charset = "utf-8"

    for i, entry in enumerate(kp.search(sys.argv[2].decode(charset))):
        print _(u"Entry %d: %s") % (i+1, entry.to_string())
