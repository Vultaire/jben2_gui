#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: tab_kanjidict.py
# Author: Paul Goins
# Created on: 20 Nov 2008

from __future__ import absolute_import

from .search_frame import SearchFrame
from jbparse import kanjidic, kanjidic2
from jben import global_refs

#self.parser = kanjidic.KanjidicParser(SRC_NAME)
#query = u"食"
#l = [entry for entry in self.parser.search(query)]
#self.assertEqual(len(l), 1)
#self.assertEqual(query, l[0].literal)


class TabKanjiDict(SearchFrame):
    def __init__(self):
        SearchFrame.__init__(self)
        self.querylabel.set_text(_("Enter kanji:"))
        self.indexlabel.set_text(_("of 0 kanji"))
