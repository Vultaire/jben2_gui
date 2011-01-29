#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: jben/gui/dialog/kanjilisteditor.py
# Author: Paul Goins
# Created on: 26 Nov 2008

from __future__ import absolute_import

import gtk
from ..widget.storedsize import StoredSizeDialog



class EditBox(gtk.TextView):

    def __init__(self):
        gtk.TextView.__init__(self)
        self.set_accepts_tab(False)
        self.set_wrap_mode(gtk.WRAP_WORD_CHAR)


class EditWindow(gtk.ScrolledWindow):

    def __init__(self):
        gtk.ScrolledWindow.__init__(self)
        self.set_shadow_type(gtk.SHADOW_IN)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        self.edit_box = EditBox()
        self.add(self.edit_box)


class ShadowedFrame(gtk.Frame):

    def __init__(self, *args, **kwargs):
        gtk.Frame.__init__(self, *args, **kwargs)
        self.set_shadow_type(gtk.SHADOW_IN)


class AddFrame(ShadowedFrame):

    def __init__(self):
        ShadowedFrame.__init__(self, _("Add Kanji"))

        add_from_file = gtk.Button(_("From File"))
        add_by_jouyou = gtk.Button(_("By Jouyou Grade"))
        add_by_jlpt = gtk.Button(_("By JLPT Level"))
        add_by_freq = gtk.Button(_("By Frequency"))

        add_box = gtk.VBox()
        for button in (add_from_file, add_by_jouyou, add_by_jlpt, add_by_freq):
            add_box.pack_start(button, expand=False)

        self.add(add_box)


class SortFrame(ShadowedFrame):

    def __init__(self):
        ShadowedFrame.__init__(self, _("Sort Kanji"))

        sort_by_jouyou = gtk.Button(_("By Jouyou Grade"))
        sort_by_jlpt = gtk.Button(_("By JLPT Level"))
        sort_by_freq = gtk.Button(_("By Frequency"))

        sort_box = gtk.VBox()
        for button in (sort_by_jouyou, sort_by_jlpt, sort_by_freq):
            sort_box.pack_start(button, expand=False)

        self.add(sort_box)


class SideButtons(gtk.VBox):

    def __init__(self):
        gtk.VBox.__init__(self, spacing=5)

        add_frame = AddFrame()
        sort_frame = SortFrame()

        for frame in (add_frame, sort_frame):
            self.pack_start(frame, expand=False)

        direct_edit = gtk.CheckButton(_("Edit directly"))
        align = gtk.Alignment(xalign=1.0)
        align.add(direct_edit)
        self.pack_start(align)


class DialogKanjiListEditor(StoredSizeDialog):
    def __init__(self, parent):
        StoredSizeDialog.__init__(self, "gui.kanjilisteditor.size", -1, -1,
                                  _("Kanji List Editor"), parent)

        edit_window = EditWindow()
        side_buttons = SideButtons()

        #edit_window.edit_box.get_buffer().connect("changed", self.on_text_changed)

        main_box = gtk.HBox(spacing=5)
        main_box.pack_start(side_buttons, expand=False)
        main_box.pack_start(edit_window)

        self.vbox.set_spacing(5)
        self.vbox.pack_start(main_box)
        self.vbox.show_all()

        ok_button = gtk.Button(stock=gtk.STOCK_OK)
        cancel_button = gtk.Button(stock=gtk.STOCK_CANCEL)
        apply_button = gtk.Button(stock=gtk.STOCK_APPLY)

        ok_button.connect("clicked", self.on_ok_clicked)
        cancel_button.connect("clicked", self.on_cancel_clicked)
        apply_button.connect("clicked", self.on_apply_clicked)

        for button in cancel_button, apply_button, ok_button:
            self.action_area.pack_start(button)
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
