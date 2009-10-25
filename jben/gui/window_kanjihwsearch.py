#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: window_kanjihwsearch.py
# Author: Paul Goins
# Created on: 25 Nov 2008

from __future__ import absolute_import

import gtk

from jben.jben_global import *
from .widget_hwpad import WidgetHWPad
from .widget_storedsize import StoredSizeWindow


class WindowKanjiHWSearch(StoredSizeWindow):
    def __init__(self, param="gui.kanjihwsearch.size"):
        StoredSizeWindow.__init__(self, param, 200, 230, gtk.WINDOW_TOPLEVEL)
        self.set_title(_("%s: Kanji Handwriting Pad") % PROGRAM_NAME)
        self.set_border_width(5)

        contents = gtk.VBox(spacing = 5)

        drawing_frame = gtk.Frame(_("Draw Kanji (Right click erases)"))
        drawing_frame.set_shadow_type(gtk.SHADOW_IN)
        self.drawing_widget = WidgetHWPad()
        drawing_frame.add(self.drawing_widget)
        drawing_frame.connect("button-release-event",
                              self.on_hwpad_button_released)

        self.buttons = []
        for i in range(5):
            button = gtk.Button("　")
            button.connect("clicked", self.on_kanji_clicked)
            button.set_sensitive(False)
            self.buttons.append(button)

        btnbox = gtk.HBox(spacing = 5)
        for button in self.buttons:
            btnbox.pack_start(button)

        # So our buttons won't stretch the full horizontal width, we wrap them
        # in a gtk.Alignment object.
        btnalign = gtk.Alignment(0.5, 0.5, 0.0, 0.0)
        btnalign.add(btnbox)

        self.clear = gtk.Button(_("Clear"))
        self.clear.connect("clicked", self.on_clear_clicked)
        btnbox2 = gtk.HButtonBox()
        btnbox2.pack_start(self.clear)

        contents.pack_start(drawing_frame)
        contents.pack_start(btnalign, expand = False)
        contents.pack_start(btnbox2, expand = False)

        self.add(contents)
        self.show_all()

    def on_kanji_clicked(self, widget):
        print "WindowKanjiHWSearch.on_kanji_clicked\n\t(%s)" % widget
        s = widget.get_label()
        if s == None or s == "　":
            s = ""
        clipboard = gtk.Clipboard()
        clipboard.set_text(s)

    def on_clear_clicked(self, widget):
        print "WindowKanjiHWSearch.on_clear_clicked"
        self.drawing_widget.clear()

    def on_hwpad_button_released(self, widget, event):
        print "WindowKanjiHWSearch.on_hwpad_button_released"
        results = self.drawing_widget.get_results()

        def assign_buttons(result, button):
            if button is None: return
            if result is None:
                button.set_label("　")
                button.set_sensitive(False)
            else:
                button.set_label(result)
                button.set_sensitive(True)

        map(assign_buttons, results, self.buttons)

        return True
