#!/usr/bin/env python

# Project: J-Ben, Python front-end
# File: tab_worddict.py
# Author: Paul Goins
# Created on: 20 Nov 2008

import gtk

class TabWordDict:
    def __init__(self):
        self.contents = gtk.VBox(spacing = 5)
        self.contents.set_border_width(5)

        # Top box: "Enter word or expression:" [________]  [ Search ]
        self.querylabel = gtk.Label(_("Enter word or expression:"))
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
        self.contents.pack_start(topbox, expand = False)

        # Middle box: a GTKTextView wrapped in a GTKScrolledWindow
        self.output = gtk.TextView()
        self.output.set_editable(False)
        self.output.set_wrap_mode(gtk.WRAP_WORD_CHAR)
        self.search()
        outputwindow = gtk.ScrolledWindow()
        outputwindow.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        outputwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        outputwindow.add(self.output)
        self.contents.pack_start(outputwindow)

        # Bottom box: [__Back__] [Forward_] [_Random_]    [#  ] "of # vocab"
        self.backbutton = gtk.Button(stock = gtk.STOCK_GO_BACK)
        self.nextbutton = gtk.Button(stock = gtk.STOCK_GO_FORWARD)
        self.randombutton = gtk.Button(_("_Random"))
        self.indexentry = gtk.Entry()
        self.indexentry.set_width_chars(5)
        self.indexentry.set_max_length(5)
        self.indexlabel = gtk.Label(_("of 0 vocab"))

        btnbox2 = gtk.HButtonBox()
        btnbox2.set_spacing(5)
        btnbox2.set_layout(gtk.BUTTONBOX_START)
        btnbox2.pack_start(self.backbutton)
        btnbox2.pack_start(self.nextbutton)
        btnbox2.pack_start(self.randombutton)

        bottombox = gtk.HBox(spacing = 5)
        bottombox.pack_start(btnbox2, expand = False)
        bottombox.pack_end(self.indexlabel, expand = False)
        bottombox.pack_end(self.indexentry, expand = False)
        self.contents.pack_start(bottombox, expand = False)

    def search(self):
        # For now, searching is disabled.
        self.output.get_buffer().set_text(_("No search has been entered."))
