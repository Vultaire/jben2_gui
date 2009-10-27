#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: dialog_vocablisteditor.py
# Author: Paul Goins
# Created on: 26 Nov 2008

from __future__ import absolute_import

import gtk
from .widget_storedsize import StoredSizeDialog

class DialogVocabListEditor(StoredSizeDialog):
    def __init__(self, parent):
        StoredSizeDialog.__init__(self, "gui.vocablisteditor.size", -1, -1,
                                  _("Vocab List Editor"), parent)

        self.edit_box = gtk.TextView()
        self.edit_box.set_accepts_tab(False)
        self.edit_box.set_wrap_mode(gtk.WRAP_WORD_CHAR)
        self.edit_box.get_buffer().connect("changed", self.on_text_changed)

        edit_window = gtk.ScrolledWindow()
        edit_window.set_shadow_type(gtk.SHADOW_IN)
        edit_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        edit_window.add(self.edit_box)

        self.vbox.set_spacing(5)
        self.vbox.pack_start(edit_window)
        self.vbox.show_all()

        self.ok_button = gtk.Button(stock = gtk.STOCK_OK)
        self.ok_button.connect("clicked", self.on_ok_clicked)
        self.cancel_button = gtk.Button(stock = gtk.STOCK_CANCEL)
        self.cancel_button.connect("clicked", self.on_cancel_clicked)
        self.apply_button = gtk.Button(stock = gtk.STOCK_APPLY)
        self.apply_button.connect("clicked", self.on_apply_clicked)

        self.action_area.pack_start(self.cancel_button)
        self.action_area.pack_start(self.apply_button)
        self.action_area.pack_start(self.ok_button)
        self.action_area.show_all()

        self.set_has_separator(False)

    def on_text_changed(self, widget):
        print "DialogVocabListEditor.on_text_changed"

    def on_cancel_clicked(self, widget):
        print "DialogVocabListEditor.on_cancel_clicked"
        self.response(gtk.RESPONSE_CANCEL)

    def on_apply_clicked(self, widget):
        print "DialogVocabListEditor.on_apply_clicked"

    def on_ok_clicked(self, widget):
        print "DialogVocabListEditor.on_ok_clicked"
        self.response(gtk.RESPONSE_OK)
