#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: jben/gui/dialog/preferences.py
# Author: Paul Goins
# Created on: 28 Nov 2008

from __future__ import absolute_import

import gtk
import os

from ...widget.storedsize import StoredSizeDialog
from .tab_prefskanjidict import TabPrefsKanjiDict
from .tab_prefsfonts import TabPrefsFonts
from .tab_prefskanjitest import TabPrefsKanjiTest
from .tab_prefsother import TabPrefsOther


class DialogPreferences(StoredSizeDialog):
    def __init__(self, parent):
        StoredSizeDialog.__init__(self, "gui.preferences.size", -1, -1,
                                  _("Preferences Editor"), parent)
        self.set_border_width(5)

        self.tab_kanjidict = TabPrefsKanjiDict()
        self.tab_fonts = TabPrefsFonts()
        self.tab_kanjitest = TabPrefsKanjiTest()
        self.tab_other = None
        tabs = gtk.Notebook()
        tabs.append_page(self.tab_kanjidict, gtk.Label(_("Kanji Dictionary")))
        tabs.append_page(self.tab_fonts, gtk.Label(_("Fonts")))
        tabs.append_page(self.tab_kanjitest, gtk.Label(_("Kanji test")))

        # Not sure what the os.name is under windows; the below is temporary.
        if os.name == "nt":
            self.tab_other = TabPrefsOther()
            tabs.append_page(self.tab_other, gtk.Label("Other"))

        self.vbox.set_spacing(5)
        self.vbox.pack_start(tabs)
        self.vbox.show_all()

        self.ok_button = gtk.Button(stock = gtk.STOCK_OK)
        self.ok_button.connect("clicked", self.on_ok_clicked)
        self.cancel_button = gtk.Button(stock = gtk.STOCK_CANCEL)
        self.cancel_button.connect("clicked", self.on_cancel_clicked)

        self.action_area.pack_start(self.cancel_button)
        self.action_area.pack_start(self.ok_button)
        self.action_area.show_all()

        self.set_has_separator(False)

        # Needed: Update function.  Updates selected options depending on
        # currently stored preferences.
        ##self.update();

    def on_cancel_clicked(self, widget):
        print "DialogPreferences.on_cancel_clicked"
        self.response(gtk.RESPONSE_CANCEL)

    def on_ok_clicked(self, widget):
        print "DialogPreferences.on_ok_clicked"
        self.update_prefs()
        self.response(gtk.RESPONSE_OK)

    def update_prefs(self):
        self.tab_kanjidict.update_prefs()
        self.tab_fonts.update_prefs()
        self.tab_kanjitest.update_prefs()
        if self.tab_other:
            self.tab_other.update_prefs()

#
#	/* Other Options */
#	chkMobile.set_active(prefs->GetSetting("config_save_target") == "mobile");
#}
