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

# Parsing is now handled, but some things are still needed:
#
# 1. Passing in of the parser object, or some config structure, so
#    that only desired fields are stored.  (Otherwise we'll waste more
#    memory than necessary on our cache, and on JMdict there's a lot
#    of stuff to store.)
# 2. Indices
#
# HOW TO INDEX JMDICT ENTRIES
#
# JMdict is a Japanese-English dictionary file, however in practice it
# is used for bidirectional searches.
#
# What we have: big list of entries, japanese readings/kanji as
# central entries, glosses as native language entries, multiple
# glosses per entry.
#
# Japanese indexing, *basic*
# Entries to consider:
#    reb+, keb*.  Index on both for sure.  Do first 
# Indices
# 1. Starts-with index: {first_char: set()} or {first_char: []}
#    - We could do secondary buckets if desired, but let's just do one
#      to start.
#    - Separate dicts for readings/kanji?  Same?  (If separate, we
#      need to search both...)
#
# Native language indexing
# Entries to consider: gloss
# Other factors: language (default: en, others supported)

# - dict indexes can be made in the same way, but only one rather than
#   the dual reading/kanji dicts for Japanese.
# - Should be able to create indices in separate languages
# - Should be able to restrict searches to a single language
# FORMAT:
# native_indices {lang: indices={}}
# (Dict based on lang, maps to other indices}

from xml.sax.handler import ContentHandler, DTDHandler, EntityResolver
from xml.sax.xmlreader import InputSource
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
        self.data = []
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

                # LATER: do some optimization if doing non-cached searches.
                # (probably won't help many people though...)
                #if not self.use_cache:
                #    raise Exception(u"JMdict no-cache-mode not yet supported!")
                #else:
                #    self.data.append(entry)

                # For now: all entries go into the data list.
                self.data.append(entry)

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

class Parser(object):

    def __init__(self, filename, use_cache=True, encoding="utf-8"):
        """Initializer for JMdictParser.

        About use_cache: JMdict is a large, heavy to parse file.
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

        # All cached entries will be stored here
        self.entries = []
        self.entry_count = 0

        # Indices
        # Basic level index: key: set()
        #     Alternatively: key: list (constant order)

        self.j_ind = {}  # Japanese (ind_type: index)
        self.n_ind = {}  # Native (lang: lang_indices)
        #                      (lang: index)
        self.index_list = ["starts_with"]  # List of indices to auto-create

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

    def search(self, search_str, index="starts_with", n_langs=["eng"],
               n_fallback=True):
        """Search JMdict for a Japanese or native language query.

        search_str: the query
        index: index to use (valid values: starts_with, None)
        n_langs: list of native languages to search for
        n_fallback: If True, processes languages in a "fallback" fashion:
                    for each entry examined, only look at the first language
                    to have glosses and ignore the rest.
        """
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

            self.create_indices(data, self.index_list)

        results = []
        if index == "starts_with":
            # Indexed lookup
            key = search_str[0]

            # Japanese first:
            idx = self.j_ind.get(index)
            if idx:
                idx = idx.get(key)
            if idx:
                for entry in [data[i] for i in idx]:
                    added = False
                    for k_ele in entry.k_ele:
                        if search_str == k_ele[u"keb"][:len(search_str)]:
                            results.append(entry)
                            added = True
                            break
                    if added: continue
                    for r_ele in entry.r_ele:
                        if search_str == r_ele[u"reb"][:len(search_str)]:
                            results.append(entry)
                            break

            # Native language next:
            # WEAKNESS: if we later support searching via other
            # languages which use Chinese characters, we may end up
            # with duplicates with this code.
            for lang in n_langs:
                search_keys = None
                idx = self.n_ind.get(lang)
                if idx:
                    idx = idx.get(index)
                if idx:
                    idx = idx.get(key)
                if idx:
                    for entry in [data[i] for i in idx]:
                        if n_fallback:
                            # NOT YET IMPLEMENTED
                            pass
                        #else:

                        for sense in entry.sense:
                            for gloss, lang, gender in sense[u"gloss"]:
                                if search_str == gloss[:len(search_str)]:
                                    results.append(entry)
                                    continue
        elif not index:
            # Non-indexed lookup
            # WARNING: this could be VERY slow!
            for entry in data:
                # Japanese search:
                # *** TO DO ***

                # Native language search:
                for sense in entry.sense:
                    for gloss, lang, gender in sense[u"gloss"]:
                        if lang not in n_langs:
                            continue
                        if search_str == gloss[:len(search_str)]:
                            results.add(entry)
                            break
        else:
            raise Exception(u"Unhandled index type: %s" % index)

        return results

    def create_indices(self, data, desired_indices):
        """Creates desired indices for a set of input data."""
        # Initialize indices
        self.j_ind = {}
        self.n_ind = {}

        for i, entry in enumerate(data):
            for index_name in desired_indices:
                if index_name == "starts_with":
                    # Make targets
                    j_targets = set()
                    n_targets = {}
                    for k_ele in entry.k_ele:
                        j_targets.add(k_ele[u"keb"][0])
                    for r_ele in entry.r_ele:
                        j_targets.add(r_ele[u"reb"][0])
                    for sense in entry.sense:
                        if not sense.has_key(u"gloss"): continue
                        for gloss, lang, gender in sense[u"gloss"]:
                            n_targets.setdefault(lang, set()).add(gloss[0])
                    # Append to indices (assuming indices as lists)
                    for target in j_targets:
                        self.j_ind.setdefault(index_name, {}) \
                            .setdefault(target, []) \
                            .append(i)
                    for lang, targ_set in n_targets.iteritems():
                        for target in targ_set:
                            self.n_ind.setdefault(lang, {}) \
                                .setdefault(index_name, {}) \
                                .setdefault(target, []) \
                                .append(i)
                else:
                    raise Exception(u"Unsupported index type")

if __name__ == "__main__":
    import sys, os

    if len(sys.argv) < 2:
        print _(u"Please specify a dictionary file.")
        exit(-1)
    try:
        kp = Parser(sys.argv[1])
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
