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
        self.set_border_width(5)

        # Top box: "Enter kanji:" [________]  [ Search ]
        self.querylabel = gtk.Label(_("Enter query:"))
        self.queryentry = gtk.Entry()

        self.searchbutton = gtk.Button(_("_Search"))
        self.searchbutton.connect("clicked", self.on_search_clicked)
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
        self.backbutton.connect("clicked", self.on_back_clicked)
        self.forwardbutton = gtk.Button(stock = gtk.STOCK_GO_FORWARD)
        self.forwardbutton.connect("clicked", self.on_forward_clicked)
        self.randombutton = gtk.Button(_("_Random"))
        self.randombutton.connect("clicked", self.on_random_clicked)
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
        # For now, searching is disabled.
        print "SearchFrame.on_search_clicked"

    def on_back_clicked(self, widget):
        print "SearchFrame.on_back_clicked"
        pass

    def on_forward_clicked(self, widget):
        print "SearchFrame.on_forward_clicked"
        pass

    def on_random_clicked(self, widget):
        print "SearchFrame.on_random_clicked"
        pass
