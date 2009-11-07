#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: tab_worddict.py
# Author: Paul Goins
# Created on: 20 Nov 2008

from __future__ import absolute_import

from .search_frame import SearchFrame


class TabWordDict(SearchFrame):
    def __init__(self):
        SearchFrame.__init__(self)
        self.querylabel.set_text(_("Enter word or expression:"))
        self.indexlabel.set_text(_("of 0 vocab"))

    def on_search_clicked(self, widget):
        # For now, searching is disabled.
        print "TabWordDict.on_search_clicked"
        self.output.get_buffer().set_text(_("No search has been entered."))

    def on_back_clicked(self, widget):
        print "TabWordDict.on_back_clicked"
        pass

    def on_forward_clicked(self, widget):
        print "TabWordDict.on_forward_clicked"
        pass

    def on_random_clicked(self, widget):
        print "TabWordDict.on_random_clicked"
        pass
