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

    def on_search_clicked(self, widget):
        # For now, searching is disabled.
        print "TabKanjiDict.on_search_clicked"
        self.output.get_buffer().set_text(_("No kanji have been selected."))

    def on_back_clicked(self, widget):
        print "TabKanjiDict.on_back_clicked"
        pass

    def on_forward_clicked(self, widget):
        print "TabKanjiDict.on_forward_clicked"
        pass

    def on_random_clicked(self, widget):
        print "TabKanjiDict.on_random_clicked"
        pass
