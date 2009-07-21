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

# Need to heavily revise this.
# We get everything in, but things aren't properly associated.
#
# For each Entry:
#  1 ID
#  0+ kanji elements (kanji blob, info, priority)
#  1+ reading elements (reading blob, info, priority)
#  0/1 info elements (bibliography stuff, etc.)
#  1+ sense elements (glosses, etc.)
#
# 


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

    def __init__(self):
        self.ent_seq = None
        self.k_ele = []
        self.r_ele = []
        self.info = None
        self.sense = []

    def to_string(self, **kwargs):
        """A default "to-string" dump of a JMdictEntry."""

        s = []
        s.append(u"JMdictEntry %d" % self.ent_seq)
        if self.k_ele:
            s.append(u"Kanji blobs: %s" % u",".join(
                [elem[u"keb"] for elem in self.k_ele]))
            s.append(u"k_ele: %s" % unicode(self.k_ele))
        if self.r_ele:
            s.append(u"Reading blobs: %s" % u",".join(
                [elem[u"reb"] for elem in self.r_ele]))
            s.append(u"r_ele: %s" % unicode(self.r_ele))
        if self.info: s.append(u"info: %s" % unicode(self.info))
        if self.sense:
            if len(self.sense) == 1:
                s.append(u"Sense: %s" % unicode(self.sense))
            else:
                for i, sense in enumerate(self.sense):
                    s.append(u"Sense %d: %s" % (i+1, unicode(sense)))
        return u"\n".join(s)

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
        if name == u"entry":
            self.parsing = True
            self.entry = JMdictEntry()
        elif self.parsing:
            self.path.append((name, attrs))
            if name in (u"k_ele", u"r_ele", u"sense", u"links", u"audit"):
                # Create a temp var for the current reading, sense, etc.
                key = u"cur_%s" % name
                setattr(self.entry, key, {})
            elif name == u"info":
                self.entry.info = {}

    def endElement(self, name):
        entry = self.entry
        if self.parsing:
            self.node_content = self.node_content.strip()
            if self.node_content:
                # Assign data as appropriate
                node, attrs = self.path[-1]
                # Unique ID for entry
                if node == u"ent_seq":
                    entry.ent_seq = int(self.node_content)
                # Kanji elements (blob, info, priority)
                elif node == u"keb":
                    entry.cur_k_ele[node] = self.node_content
                elif node[:3] == u"ke_":
                    entry.cur_k_ele.setdefault(node, []).append(
                        self.node_content)
                # Reading elements (blob, nokanji?, reading substrs, inf, pri)
                elif node == u"reb":
                    entry.cur_r_ele[node] = self.node_content
                elif node == u"re_nokanji": # special case
                    entry.cur_r_ele[node] = True
                elif node[:3] == u"re_": # reading element (all but nokanji)
                    entry.cur_r_ele.setdefault(node, []).append(
                        self.node_content)
                # Info element
                # links [], bibl [], etym [], audit []
                # links: (tag, desc, uri)
                # audit: upd_date, upd_detl)
                # bibl, etym, and all other child fields: strings
                elif node in (u"bibl", u"etym"):
                    entry.info.setdefault(node, []).append(
                        self.node_content)
                # These info nodes need to be appended on the
                # endElement event.  *** TO DO ***
                elif node in (u"link_tag", u"link_desc", u"link_uri",
                              u"upd_date", u"upd_detl"):
                    setattr(entry, u"cur_%s" % node, self.node_content)
                # Sense elements (all but glosses)
                elif node in (u"stagk", u"stagr", u"pos", u"xref", u"ant",
                              u"field", u"misc", u"s_inf", u"dial",
                              u"example"):
                    entry.cur_sense.setdefault(node, []).append(
                        self.node_content)
                elif node == u"lsource":
                    # xml_lang is common
                    xml_lang = attrs.get(u"xml:lang", u"eng")
                    # ls_* seem new...
                    ls_type = attrs.get(u"ls_type", u"full")
                    ls_wasei = attrs.get(u"ls_wasei")  # Flag for "waseieigo"
                    # We'll do a 4 node tuple for this entry...
                    entry.cur_sense.setdefault(node, []).append(
                        (self.node_content, xml_lang, ls_type, ls_wasei))
                # Glosses...  It seems that <pri> is not yet used, so
                # glosses are pretty straightforward like the above fields.
                elif node == u"gloss":
                    xml_lang = attrs.get(u"xml:lang", u"eng")
                    g_gend = attrs.get(u"g_gend")
                    entry.cur_sense.setdefault(node, []).append(
                        (self.node_content, xml_lang, g_gend))
                elif node == u"pri":
                    print (u"DEBUG: <pri> field detected!  This is a new "
                           u"field; please contact the author with the "
                           u"modification date of your copy of JMdict so he "
                           u"can update J-Ben to support it!")

                else:   # Unhandled
                    print (u"DEBUG: path %s: unhandled node %s with content "
                           u"[%s]" % (self.get_path(), node,
                                      self.node_content))
                self.node_content = ""

            if self.path:
                if name != self.path[-1][0]:
                    # Shouldn't ever happen, but mistakes *can* slip in...
                    print u"Mismatch detected, path is %s, element name is %s" \
                          % (self.get_path(), name)
                else:
                    self.path.pop()

            # Handle composite values
            # First, the dict types...
            if name in (u"k_ele", u"r_ele", u"sense"):
                temp_key = u"cur_%s" % name
                obj = getattr(entry, temp_key)
                getattr(entry, name).append(obj)
                delattr(entry, temp_key)
            # Next, the two tuple types
            elif name == u"links":
                entry.info.setdefault(u"links", []).append(
                    (entry.cur_link_tag,
                     entry.cur_link_desc,
                     entry.cur_link_uri))
                delattr(entry, u"cur_link_tag")
                delattr(entry, u"cur_link_desc")
                delattr(entry, u"cur_link_uri")
            elif name == u"audit":
                entry.info.setdefault(u"audit", []).append(
                    (entry.cur_upd_date,
                     entry.cur_upd_detl))
                delattr(entry, u"cur_upd_date")
                delattr(entry, u"cur_upd_detl")

            # Handle end of entry
            elif name == u"entry":
                for node in (u"k_ele", u"r_ele", u"sense",
                             u"link_tag", u"link_desc", u"link_uri",
                             u"upd_date", u"upd_detl"):
                    if hasattr(entry, u"cur_%s" % node):
                        print vars(entry)
                        print node
                        raise Exception(u"Shouldn't-Happen-Error")

                ent_seq = entry.ent_seq
                if ent_seq in range(1000090, 2014140):
                    print entry.to_string(), "\n"
                if ent_seq >= 1000090:
                    import sys
                    sys.exit(-1)
                entry = None
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
