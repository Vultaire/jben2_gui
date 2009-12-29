#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: tab_prefsfonts.py
# Author: Paul Goins
# Created on: 28 Nov 2008

from __future__ import absolute_import

import gtk
import os
from jben import global_refs


class TabPrefsFonts(gtk.VBox):

    def __init__(self):

        gtk.VBox.__init__(self, spacing = 5)

        # We're loading 4 rows of GUI controls, all following the same
        # order: 0 = Japanese Normal, 1 = Japanese Large,
        # 2 = English Normal, 3 = English Small.

        params = [("font.ja", _("Japanese Font, Normal")),
                  ("font.ja.large", _("Japanese Font, Large")),
                  ("font.native", _("English Font, Normal")),
                  ("font.native.small", _("English Font, Small"))]

        self.controls = []
        table = gtk.Table(4, 3)
        for k, s in params:
            self.controls.append(
                (k, gtk.Label(s), gtk.TextView(), gtk.Button(_("Change..."))))

        for i, (key, label, textview, button) in enumerate(self.controls):

            label.set_alignment(1.0, 0.5)

            textview.set_accepts_tab(False)
            textview.set_editable(False)

            # Tacking the font_name onto the textview for convenience
            textview.font_name = self.get_font_name(key)

            self.update_font_control(self.controls[i], textview.font_name)

            button.connect("clicked", self.on_font_change, self.controls[i])

            frame = gtk.Frame()
            frame.add(textview)
            frame.set_shadow_type(gtk.SHADOW_IN)
            bbox = gtk.HButtonBox()
            bbox.pack_start(button)

            table.attach(label, 0, 1, i, i + 1,
                         gtk.FILL, gtk.SHRINK, 5, 5)
            table.attach(frame, 1, 2, i, i + 1,
                         gtk.FILL | gtk.EXPAND, gtk.SHRINK, 5, 5)
            table.attach(bbox, 2, 3, i, i + 1,
                         gtk.SHRINK, gtk.SHRINK, 5, 5)

        self.pack_start(table, expand = False);

    def get_font_name(self, key):
        prefs = global_refs.prefs
        font_name = prefs.get(key)
        if not font_name:
            if os.name == "nt":
                if key == "font.native": return "Tahoma 12"
                elif key == "font.native.small": return "Tahoma 8"
                elif key == "font.ja": return "MS Mincho 16"
                elif key == "font.ja.large": return "MS Mincho 32"
            else:
                if key == "font.native": return "sans 12"
                elif key == "font.native.small": return "sans 8"
                elif key == "font.ja": return "serif 16"
                elif key == "font.ja.large": return "serif 32"
        return font_name

    def update_font_control(self, ctrls, font_name):
        key, label, textview, button = ctrls
        print u"update_font_control: set %08X to font %s" \
              % (id(textview), font_name)
        buf = textview.get_buffer()
        buf.set_text("")

        table = buf.get_tag_table()
        tag = table.lookup("font")
        if tag:
            table.remove(tag)

        tag = gtk.TextTag("font")
        tag.set_property("font", font_name)
        table.add(tag)
        start = buf.get_start_iter()
        buf.insert_with_tags(start, font_name, tag)

    def on_font_change(self, widget, ctrls):
        print("TabPrefsFonts.on_font_change for key %s" % ctrls[0])
        key, label, textview, button = ctrls
	fd = gtk.FontSelectionDialog(_("Choose Font"))
        if "font.ja" in key:
            fd.set_preview_text(_("ROMAJI romaji 日本語　にほんご　ニホンゴ"))
	fd.set_font_name(textview.font_name)
	result = fd.run()
        fd.hide()
        if result == gtk.RESPONSE_OK:
            textview.font_name = fd.get_font_name();
            self.update_font_control(ctrls, textview.font_name)

    def update_prefs(self):
        prefs = global_refs.prefs
        for key, label, textview, button in self.controls:
            buf = textview.get_buffer()
            s = buf.get_start_iter()
            e = buf.get_end_iter()
            text = textview.get_buffer().get_text(s, e, False)
            prefs[key] = text
            print "Setting '%s' to '%s'" % (key, text)
