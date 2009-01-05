#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: dialog_preferences.py
# Author: Paul Goins
# Created on: 28 Nov 2008

import gtk
import os

from tab_prefskanjidict import TabPrefsKanjiDict
from tab_prefsfonts     import TabPrefsFonts
from tab_prefskanjitest import TabPrefsKanjiTest
from tab_prefsother     import TabPrefsOther

class DialogPreferences(gtk.Dialog):
    def __init__(self, parent):
        gtk.Dialog.__init__(self, _("Preferences Editor"), parent)
        self.set_border_width(5)

        tabs = gtk.Notebook()
        tabs.append_page(TabPrefsKanjiDict(), gtk.Label(_("Kanji Dictionary")))
        tabs.append_page(TabPrefsFonts(), gtk.Label(_("Fonts")))
        tabs.append_page(TabPrefsKanjiTest(), gtk.Label(_("Kanji test")))

        # Not sure what the os.name is under windows; the below is temporary.
        if os.name == "nt":
            tabs.append_page(TabPrefsOther(), gtk.Label("Other"))

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
        self.response(gtk.RESPONSE_OK)

#void DialogConfig::Update() {
#	Preferences *prefs = Preferences::Get();
#	int options = prefs->kanjidicOptions;
#	int dictionaries = prefs->kanjidicDictionaries;
#
#	/* Set appropriate checkboxes */
#	chkReadings     .set_active(options & KDO_READINGS);
#	chkMeanings     .set_active(options & KDO_MEANINGS);
#	chkHighImp      .set_active(options & KDO_HIGHIMPORTANCE);
#	chkMultiRad     .set_active(options & KDO_MULTIRAD);
#	chkDict         .set_active(options & KDO_DICTIONARIES);
#	chkVocabCrossRef.set_active(options & KDO_VOCABCROSSREF);
#	chkLowImp       .set_active(options & KDO_LOWIMPORTANCE);
#	chkSodStatic    .set_active(options & KDO_SOD_STATIC);
#	chkSodAnim      .set_active(options & KDO_SOD_ANIM);
#
##if 0
#	/* Enable/disable SOD/SODA checkboxes based on existance of directory */
#	/* (DISABLED for now; J-Ben should auto-disable the flag if dicts
#	   are not found, but obviously that needs to be done in the prefs
#	   loader.  I'll add that later.) */
#	string sodDir = Preferences::Get()->GetSetting("sod_dir");
#	chkSodStatic.set_sensitive(
#		FileExists(
#			string(sodDir)
#			.append(1,DSCHAR)
#			.append("sod-utf8-hex")
#			.append(1,DSCHAR)
#			.append("README-License").c_str()));
#	chkSodAnim.set_sensitive(
#		FileExists(
#			string(sodDir)
#			.append(1,DSCHAR)
#			.append("soda-utf8-hex")
#			.append(1,DSCHAR)
#			.append("README-License").c_str()));
##endif
#
#	for(size_t i=0;i<vChkDict.size();i++) {
#		vChkDict[i]->set_active(dictionaries & (1ul << i));
#	}
#
#	/* Init font display */
#	sFontJaNormal = prefs->GetSetting("font.ja");
#	sFontJaLarge  = prefs->GetSetting("font.ja.large");
#	sFontEnNormal = prefs->GetSetting("font.en");
#	sFontEnSmall  = prefs->GetSetting("font.en.small");
#	UpdateFontControl(tvJaNormal, sFontJaNormal);
#	UpdateFontControl(tvJaLarge,  sFontJaLarge);
#	UpdateFontControl(tvEnNormal, sFontEnNormal);
#	UpdateFontControl(tvEnSmall,  sFontEnSmall);
#
#	/* Other Options */
#	chkMobile.set_active(prefs->GetSetting("config_save_target") == "mobile");
#}
