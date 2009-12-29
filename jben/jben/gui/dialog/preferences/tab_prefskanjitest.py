#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: tab_prefskanjitest.py
# Author: Paul Goins
# Created on: 28 Nov 2008
# Note: Original author of this was Alain Bertrand.  I fixed some bugs,
#       ported it to Python and rearranged some things.

from __future__ import absolute_import

import gtk
from jben import global_refs


class TabPrefsKanjiTest(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self, spacing=5)

        self.chk_reading_onyomi = gtk.CheckButton(_("Show onyomi"))
        self.chk_reading_kunyomi = gtk.CheckButton(_("Show kunyomi"))
        self.chk_reading_english = gtk.CheckButton(_("Show English meaning"))
        reading_vbox = gtk.VBox()
        reading_vbox.pack_start(self.chk_reading_onyomi, expand=False)
        reading_vbox.pack_start(self.chk_reading_kunyomi, expand=False)
        reading_vbox.pack_start(self.chk_reading_english, expand=False)
        reading_frame = gtk.Frame(_("Reading test"))
        reading_frame.add(reading_vbox)

        self.chk_writing_onyomi = gtk.CheckButton(_("Show onyomi"))
        self.chk_writing_kunyomi = gtk.CheckButton(_("Show kunyomi"))
        self.chk_writing_english = gtk.CheckButton(_("Show English meaning"))
        writing_vbox = gtk.VBox()
        writing_vbox.pack_start(self.chk_writing_onyomi, expand=False)
        writing_vbox.pack_start(self.chk_writing_kunyomi, expand=False)
        writing_vbox.pack_start(self.chk_writing_english, expand=False)
        writing_frame = gtk.Frame(_("Writing test"))
        writing_frame.add(writing_vbox)

        shortcut_table = gtk.Table(2,4)
        strings = [
            ("keys.kanjitest.correct", _("Correct answer: ")),
            ("keys.kanjitest.wrong", _("Wrong answer: ")),
            ("keys.kanjitest.show", _("Show answer: ")),
            ("keys.kanjitest.stop", _("Stop drill: "))
            ]
        self.shortcut_ctls = []
        prefs = global_refs.prefs
        for key, label_str in strings:
            label = gtk.Label(label_str)
            label.set_alignment(0.0, 0.5)

            entry = gtk.Entry()
            keyval = prefs.get(key)
            if keyval:
                keyval = int(keyval)
                uval = gtk.gdk.keyval_to_unicode(keyval)
                s = unichr(uval).encode("utf-8")
                entry.set_text(s)
            entry.set_max_length(1)
            entry.set_size_request(30, -1)

            self.shortcut_ctls.append((key, label, entry))

        shortcut_table.set_border_width(5)
        shortcut_table.set_row_spacings(5)
        shortcut_table.set_col_spacings(5)
        shortcut_table.set_col_spacing(1, 20)

        for i, (key, label, entry) in enumerate(self.shortcut_ctls):
            entry.connect("key-press-event", self.on_key_press_event,
                          self.shortcut_ctls[i])
            x = (i % 2) * 2
            y = i / 2
            shortcut_table.attach(label, x, x+1, y, y+1,
                                  gtk.FILL, gtk.FILL)
            shortcut_table.attach(entry, x+1, x+2, y, y+1,
                                  gtk.FILL, gtk.FILL)

        shortcut_frame = gtk.Frame(_("Keyboard shortcuts"))
        shortcut_frame.add(shortcut_table)

        self.pack_start(reading_frame, expand=False)
        self.pack_start(writing_frame, expand=False)
        self.pack_start(shortcut_frame, expand=False)

    def on_key_press_event(self, widget, event, data=None):
        key, label, entry = data

        if event.keyval in (gtk.keysyms.Up,
                            gtk.keysyms.Down,
                            gtk.keysyms.Left,
                            gtk.keysyms.Right,
                            gtk.keysyms.Tab,
                            gtk.keysyms.ISO_Left_Tab, # Shift-Tab...?
                            gtk.keysyms.Escape,
                            gtk.keysyms.Return,
                            gtk.keysyms.BackSpace,
                            gtk.keysyms.Delete):
            return False
        try:
            ukeyval = gtk.gdk.keyval_to_unicode(event.keyval)
            strval = unichr(ukeyval).encode("utf-8")
            widget.set_text(strval)
        except:
            print _("Unhandled keypress captured: "
                    "keyval: 0x%X, hardware_keycode: 0x%X") \
                % (event.keyval, event.hardware_keycode)
        return True

    def update_prefs(self):
        prefs = global_refs.prefs
        for key, label, entry in self.shortcut_ctls:
            s = entry.get_text()
            if not s.strip():
                prefs.pop(key, None)
            else:
                uval = ord(s.decode())
                prefs[key] = str(gtk.gdk.unicode_to_keyval(uval))
