x#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: dict_manager.py
# Author: Paul Goins
# Created on: 1 Nov 2009

from __future__ import absolute_import

import gtk
from jben import global_refs


"""
Layout:

"""


class TabPrefsKanjiDict(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self)

        self.chkEdict = gtk.CheckButton(
            _("EDICT (recommended)"))
        #self.chkEdict2 = gtk.CheckButton(
        #    _("EDICT2"))
        self.chkJMdict = gtk.CheckButton(
            _("JMdict (slow, multilingual)"))
        self.chkJMdict_e = gtk.CheckButton(
            _("JMdict_e (English/Japanese only)"))
        self.chkKanjidic = gtk.CheckButton(
            _("KANJIDIC (recommended)"))
        self.chkKanjd212 = gtk.CheckButton(
            _("KANJID212"))
        self.chkKanjidic2 = gtk.CheckButton(
            _("KANJIDIC2 (slow)"))

        self.pack_start(self.chkEdict, expand=False)
        self.pack_start(self.chkEdict, expand=False)
        self.pack_start(self.chkEdict, expand=False)
        self.pack_start(self.chkEdict, expand=False)
        self.pack_start(self.chkEdict, expand=False)
        self.pack_start(self.chkEdict, expand=False)
        self.pack_start(self.chkEdict, expand=False)

        self.update_gui()

    def update_gui(self):
        # This function -does- fudge things a little, but the average user
        # should not notice.
        prefs = global_refs.app.prefs
        self.chkReadings.set_active(
            prefs.get("kdict.render.kunyomi", False))
        self.chkMeanings.set_active(
            prefs.get("kdict.render.meaning", False))
        self.chkHighImp.set_active(
            prefs.get("kdict.render.stroke_count", False))
        self.chkMultiRad.set_active(
            prefs.get("kdict.render.radical_list", False))
        self.chkDict.set_active(
            prefs.get("kdict.render.dictionaries", False))
        self.chkVocabCrossRef.set_active(
            prefs.get("kdict.render.vocab_cross_ref", False))
        self.chkLowImp.set_active(
            prefs.get("kdict.render.cross_ref", False))
        self.chkSodStatic.set_active(
            prefs.get("kdict.render.kanjicafe_sodas", False))
        self.chkSodAnim.set_active(
            prefs.get("kdict.render.kanjicafe_sods", False))

        # Dicts
        for key, obj in self.dict_buttons:
            obj.set_active(prefs.get(key, False))

    def update_prefs(self):
        prefs = global_refs.app.prefs
        b = self.chkReadings.get_active()
        prefs["kdict.render.kunyomi"] = b
        prefs["kdict.render.onyomi"] = b
        prefs["kdict.render.nanori"] = b
        b = self.chkMeanings.get_active()
        prefs["kdict.render.meaning"] = b
        b = self.chkHighImp.get_active()
        prefs["kdict.render.stroke_count"] = b
        prefs["kdict.render.jlpt_level"] = b
        prefs["kdict.render.jouyou_grade"] = b
        prefs["kdict.render.frequency"] = b
        b = self.chkMultiRad.get_active()
        prefs["kdict.render.radical_list"] = b
        b = self.chkDict.get_active()
        prefs["kdict.render.dictionaries"] = b
        b = self.chkVocabCrossRef.get_active()
        prefs["kdict.render.vocab_cross_ref"] = b
        b = self.chkLowImp.get_active()
        prefs["kdict.render.cross_ref"] = b
        prefs["kdict.render.jis-208"] = b
        prefs["kdict.render.jis-212"] = b
        prefs["kdict.render.jis-213"] = b
        prefs["kdict.render.nelson_radical"] = b
        prefs["kdict.render.kangxi_radical"] = b
        prefs["kdict.render.korean"] = b
        prefs["kdict.render.korean_roman"] = b
        prefs["kdict.render.pinyin_roman"] = b
        prefs["kdict.render.radical_name"] = b
        prefs["kdict.render.unicode"] = b
        b = self.chkSodStatic.get_active()
        prefs["kdict.render.kanjicafe_sodas"] = b
        b = self.chkSodAnim.get_active()
        prefs["kdict.render.kanjicafe_sods"] = b

        # Dicts
        for key, obj in self.dict_buttons:
            prefs[key] = obj.get_active()
