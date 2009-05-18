#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: tab_prefskanjitest.py
# Author: Paul Goins
# Created on: 28 Nov 2008
# Note: Original author of this was Alain Bertrand.  I fixed some bugs,
#       ported it to Python and rearranged some things.

import gtk

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

        label_strs = [_("Correct answer: "), _("Wrong answer: "),
                      _("Show answer: "), _("Stop drill: ")]
        labels = []
        for str in label_strs:
            l = gtk.Label(str)
            l.set_alignment(0.0, 0.5)
            labels.append(l)

        self.ent_correct = gtk.Entry()
        self.ent_wrong = gtk.Entry()
        self.ent_show = gtk.Entry()
        self.ent_stop = gtk.Entry()
        for o in [self.ent_correct, self.ent_wrong,
                  self.ent_show, self.ent_stop]:
            o.set_max_length(1)
            o.set_size_request(30, -1)

        shortcut_table = gtk.Table(2,4)
        shortcut_table.set_border_width(5)
        shortcut_table.set_row_spacings(5)
        shortcut_table.set_col_spacings(5)
        shortcut_table.set_col_spacing(1, 20)
        print("Col spacing: %d" % shortcut_table.get_col_spacing(1))
        shortcut_table.attach(labels[0], 0,1,0,1, gtk.FILL, gtk.FILL)
        shortcut_table.attach(self.ent_correct, 1,2,0,1, gtk.FILL, gtk.FILL)
        shortcut_table.attach(labels[1], 2,3,0,1, gtk.FILL, gtk.FILL)
        shortcut_table.attach(self.ent_wrong, 3,4,0,1, gtk.FILL, gtk.FILL)
        shortcut_table.attach(labels[2], 0,1,1,2, gtk.FILL, gtk.FILL)
        shortcut_table.attach(self.ent_show, 1,2,1,2, gtk.FILL, gtk.FILL)
        shortcut_table.attach(labels[3], 2,3,1,2, gtk.FILL, gtk.FILL)
        shortcut_table.attach(self.ent_stop, 3,4,1,2, gtk.FILL, gtk.FILL)

        shortcut_frame = gtk.Frame(_("Keyboard shortcuts"))
        shortcut_frame.add(shortcut_table)

        self.pack_start(reading_frame, expand=False)
        self.pack_start(writing_frame, expand=False)
        self.pack_start(shortcut_frame, expand=False)

    def update_prefs(self):
        pass
