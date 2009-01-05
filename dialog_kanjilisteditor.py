#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: dialog_kanjilisteditor.py
# Author: Paul Goins
# Created on: 26 Nov 2008

import gtk

class DialogKanjiListEditor(gtk.Dialog):
    def __init__(self, parent):
        gtk.Dialog.__init__(self, _("Kanji List Editor"), parent)

        self.edit_box = gtk.TextView()
        self.edit_box.set_accepts_tab(False)
        self.edit_box.set_wrap_mode(gtk.WRAP_WORD_CHAR)
        self.edit_box.get_buffer().connect("changed", self.on_text_changed)

        edit_window = gtk.ScrolledWindow()
        edit_window.set_shadow_type(gtk.SHADOW_IN)
        edit_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        edit_window.add(self.edit_box)

        add_frame = gtk.Frame(_("Add Kanji"))
        add_frame.set_shadow_type(gtk.SHADOW_IN)
        sort_frame = gtk.Frame(_("Sort Kanji"))
        sort_frame.set_shadow_type(gtk.SHADOW_IN)

        self.add_from_file = gtk.Button(_("From File"))
        self.add_by_jouyou = gtk.Button(_("By Jouyou Grade"))
        self.add_by_jlpt   = gtk.Button(_("By JLPT Level"))
        self.add_by_freq   = gtk.Button(_("By Frequency"))
        add_box = gtk.VBox()
        add_box.pack_start(self.add_from_file, expand = False)
        add_box.pack_start(self.add_by_jouyou, expand = False)
        add_box.pack_start(self.add_by_jlpt, expand = False)
        add_box.pack_start(self.add_by_freq, expand = False)
        add_frame.add(add_box)

        self.sort_by_jouyou = gtk.Button(_("By Jouyou Grade"))
        self.sort_by_jlpt   = gtk.Button(_("By JLPT Level"))
        self.sort_by_freq   = gtk.Button(_("By Frequency"))
        sort_box = gtk.VBox()
        sort_box.pack_start(self.sort_by_jouyou, expand = False)
        sort_box.pack_start(self.sort_by_jlpt, expand = False)
        sort_box.pack_start(self.sort_by_freq, expand = False)
        sort_frame.add(sort_box)

        side_buttons = gtk.VBox(spacing = 5)
        side_buttons.pack_start(add_frame, expand = False)
        side_buttons.pack_start(sort_frame, expand = False)

        main_box = gtk.HBox(spacing = 5)
        main_box.pack_start(side_buttons, expand = False)
        main_box.pack_start(edit_window)

        self.vbox.set_spacing(5)
        self.vbox.pack_start(main_box)
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
        print "DialogKanjiListEditor.on_text_changed"

    def on_cancel_clicked(self, widget):
        print "DialogKanjiListEditor.on_cancel_clicked"
        self.response(gtk.RESPONSE_CANCEL)

    def on_apply_clicked(self, widget):
        print "DialogKanjiListEditor.on_apply_clicked"

    def on_ok_clicked(self, widget):
        print "DialogKanjiListEditor.on_ok_clicked"
        self.response(gtk.RESPONSE_OK)
