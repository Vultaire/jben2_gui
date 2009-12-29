#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: tab_worddict.py
# Author: Paul Goins
# Created on: 20 Nov 2008

from __future__ import absolute_import

from .search_frame import SearchFrame
from jbparse import edict, jmdict

#self.parser = edict.EdictParser(SRC_NAME)
#"""EDICT: Search for Japanese word/phrase"""
#query = u"日本"
#l = [entry for entry in self.parser.search(query)]
#self.assertTrue(len(l) > 0)

#self.parser = jmdict.JMdictParser(SRC_NAME)
#
#"""JMDICT: Search for Japanese word/phrase"""
#parser = self.parser
#desired_indices = ["starts_with"]
#
#data = self._parse_x_entries(SRC_NAME, 10)
#parser.cache = data
#parser.create_indices(data, desired_indices)
#
#query = u"仝"
#l = parser.search(query)


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
