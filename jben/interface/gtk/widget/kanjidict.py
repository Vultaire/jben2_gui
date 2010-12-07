#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: tab_kanjidict.py
# Author: Paul Goins
# Created on: 20 Nov 2008

from __future__ import absolute_import

from .search_frame import SearchFrame


class TabKanjiDict(SearchFrame):

    def __init__(self):
        SearchFrame.__init__(self)
        self.querylabel.set_text(_("Enter kanji:"))
        self.indexlabel.set_text(_("of 0 kanji"))

    def search(self, query):
        results = []
        for character in query:
            result = self.dict.search_by_literal(character)
            if result is not None:
                results.append(result)
        return results
