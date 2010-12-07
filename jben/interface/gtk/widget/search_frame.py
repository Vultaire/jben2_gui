#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: search_frame.py
# Author: Paul Goins
# Created on: 1 Nov 2009

import gtk


class SearchFrame(gtk.VBox):

    def __init__(self):
        gtk.VBox.__init__(self, spacing = 5)
        self.dict = None
        self._layout()
        self.queryentry.connect("activate", self.on_search_clicked)
        self.searchbutton.connect("clicked", self.on_search_clicked)
        self.backbutton.connect("clicked", self.on_back_clicked)
        self.forwardbutton.connect("clicked", self.on_forward_clicked)
        self.randombutton.connect("clicked", self.on_random_clicked)

    def _layout(self):
        self.set_border_width(5)

        # Top box: "Enter kanji:" [________]  [ Search ]
        self.querylabel = gtk.Label(_("Enter query:"))
        self.queryentry = gtk.Entry()

        self.searchbutton = gtk.Button(_("_Search"))
        btnbox = gtk.HButtonBox()
        btnbox.set_spacing(5)
        btnbox.set_layout(gtk.BUTTONBOX_START)
        btnbox.pack_start(self.searchbutton)

        topbox = gtk.HBox(spacing = 5)
        topbox.pack_start(self.querylabel, expand = False)
        topbox.pack_start(self.queryentry)
        topbox.pack_start(btnbox, expand = False)
        self.pack_start(topbox, expand = False)

        # Middle box: a GTKTextView wrapped in a GTKScrolledWindow
        self.output = gtk.TextView()
        self.output.set_editable(False)
        self.output.set_wrap_mode(gtk.WRAP_WORD_CHAR)
        self.on_search_clicked(None)
        outputwindow = gtk.ScrolledWindow()
        outputwindow.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        outputwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        outputwindow.add(self.output)
        self.pack_start(outputwindow)

        # Bottom box: [__Back__] [Forward_] [_Random_]    [#  ] "of # kanji"
        self.backbutton = gtk.Button(stock = gtk.STOCK_GO_BACK)
        self.forwardbutton = gtk.Button(stock = gtk.STOCK_GO_FORWARD)
        self.randombutton = gtk.Button(_("_Random"))
        self.indexentry = gtk.Entry()
        self.indexentry.set_width_chars(5)
        self.indexentry.set_max_length(5)
        self.indexlabel = gtk.Label(_("of 0 items"))

        btnbox2 = gtk.HButtonBox()
        btnbox2.set_spacing(5)
        btnbox2.set_layout(gtk.BUTTONBOX_START)
        btnbox2.pack_start(self.backbutton)
        btnbox2.pack_start(self.forwardbutton)
        btnbox2.pack_start(self.randombutton)

        bottombox = gtk.HBox(spacing = 5)
        bottombox.pack_start(btnbox2, expand = False)
        bottombox.pack_end(self.indexlabel, expand = False)
        bottombox.pack_end(self.indexentry, expand = False)
        self.pack_start(bottombox, expand = False)

    def on_search_clicked(self, widget):
        query = self.queryentry.get_text().decode("utf-8").strip()
        if not query:
            self.output.get_buffer().set_text(
                _("No query has been entered."))
            return
        if not self.dict:
            self.output.get_buffer().set_text(
                _("ERROR: Could not connect to database parser."))
            return
        self.disable_gui()
        results = self.search(query)
        out_str = u"\n\n".join(unicode(result) for result in results)
        if not out_str:
            out_str = _(u"No entries found.")
        self.output.get_buffer().set_text(out_str)
        self.enable_gui()

    def search(self, query):
        """Default search implementation."""
        print u"SEARCHING: %s" % query
        return self.dict.search(query)

    def disable_gui(self):
        self.set_sensitive(False)
        rect = self.get_allocation()
        self.get_window().invalidate_rect(self.get_allocation(), True)
        gtk.gdk.window_process_all_updates()

    def enable_gui(self):
        self.set_sensitive(True)

    def on_back_clicked(self, widget):
        print "%s.on_back_clicked" % str(self)

    def on_forward_clicked(self, widget):
        print "%s.on_forward_clicked" % str(self)

    def on_random_clicked(self, widget):
        print "%s.on_random_clicked" % str(self)

    def set_dict(self, d):
        self.dict = d
