#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: tab_prefskanjidict.py
# Author: Paul Goins
# Created on: 28 Nov 2008

from __future__ import absolute_import

import gtk
from jben import global_refs


class TabPrefsKanjiDict(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self)

        self.chkReadings = gtk.CheckButton(
            _("Include on-yomi, kun-yomi and nanori (name) readings"))
        self.chkMeanings = gtk.CheckButton(
            _("Include English meanings"))
        self.chkHighImp = gtk.CheckButton(
            _("Include stroke count, Jouyou grade and newspaper "
              "frequency rank"))
        self.chkMultiRad = gtk.CheckButton(
            _("Include radical component list"))
        self.chkDict = gtk.CheckButton(
            _("Include dictionary reference codes"))
        self.chkVocabCrossRef = gtk.CheckButton(
            _("Show vocab from your study list which use the kanji"))
        self.chkLowImp = gtk.CheckButton(
            _("Other information "
              "(Radical #'s, Korean and Pinyin romanization)"))
        self.chkSodStatic = gtk.CheckButton(
            _("Use stroke order diagrams if present"))
        self.chkSodAnim = gtk.CheckButton(
            _("Use animated stroke order diagrams if present (tests only)"))

        # I use the same names used in KANJIDIC2 for the various dictionary
        # flags.
        self.dict_buttons = []
        self.dict_buttons.append(
            ("kdict.render.dcode.halpern_njecd",
             gtk.CheckButton(
                 _('"New Japanese-English Character Dictionary" '
                   'by Jack Halpern.'))))
        self.dict_buttons.append(
            ("kdict.render.dcode.nelson_c",
             gtk.CheckButton(
                 _('"Modern Reader\'s Japanese-English Character Dictionary" '
                   'by Andrew Nelson'))))
        self.dict_buttons.append(
            ("kdict.render.dcode.nelson_n",
             gtk.CheckButton(
                 _('"The New Nelson Japanese-English Character Dictionary" '
                   'by John Haig'))))
        self.dict_buttons.append(
            ("kdict.render.dcode.busy_people",
             gtk.CheckButton(
                 _('"Japanese for Busy People" by AJLT'))))
        self.dict_buttons.append(
            ("kdict.render.dcode.crowley",
             gtk.CheckButton(
                 _('"The Kanji Way to Japanese Language Power" '
                   'by Dale Crowley'))))
        self.dict_buttons.append(
            ("kdict.render.dcode.kodansha_compact",
             gtk.CheckButton(
                 _('"Kodansha Compact Kanji Guide"'))))
        self.dict_buttons.append(
            ("kdict.render.dcode.henshall3",
             gtk.CheckButton(
                 _('"A Guide To Reading and Writing Japanese" '
                   'by Ken Henshall et al.'))))
        self.dict_buttons.append(
            ("kdict.render.dcode.kanji_in_context",
             gtk.CheckButton(
                 _('"Kanji in Context" by Nishiguchi and Kono'))))
        self.dict_buttons.append(
            ("kdict.render.dcode.halpern_kkld",
             gtk.CheckButton(
                 _('"Kanji Learner\'s Dictionary" by Jack Halpern'))))
        self.dict_buttons.append(
            ("kdict.render.dcode.oneill_kk",
             gtk.CheckButton(
                 _('"Essential Kanji" by P.G. O\'Neill'))))
        self.dict_buttons.append(
            ("kdict.render.qcode.deroo",
             gtk.CheckButton(
                 _('"2001 Kanji" by Father Joseph De Roo'))))
        self.dict_buttons.append(
            ("kdict.render.dcode.sakade",
             gtk.CheckButton(
                 _('"A Guide To Reading and Writing Japanese" '
                   'by Florence Sakade'))))
        self.dict_buttons.append(
            ("kdict.render.dcode.tutt_cards",
             gtk.CheckButton(
                 _('"Tuttle Kanji Cards" by Alexander Kask'))))
        self.dict_buttons.append(
            ("kdict.render.dcode.jf_cards",
             gtk.CheckButton(
                 _('"Japanese Kanji Flashcards" by Hodges and Okazaki'))))
        self.dict_buttons.append(
            ("kdict.render.qcode.skip",
             gtk.CheckButton(
                 _('SKIP codes used by Halpern dictionaries'))))
        self.dict_buttons.append(
            ("kdict.render.qcode.sh_desc",
             gtk.CheckButton(
                 _('"Kanji Dictionary" by Spahn & Hadamitzky'))))
        self.dict_buttons.append(
            ("kdict.render.dcode.sh_kk",
             gtk.CheckButton(
                 _('"Kanji & Kana" by Spahn & Hadamitzky'))))
        self.dict_buttons.append(
            ("kdict.render.qcode.four_corner",
             gtk.CheckButton(
                 _('Four Corner code (various dictionaries)'))))
        self.dict_buttons.append(
            ("kdict.render.dcode.moro",
             gtk.CheckButton(
                 _('"Morohashi Daikanwajiten"'))))
        self.dict_buttons.append(
            ("kdict.render.dcode.henshall",
             gtk.CheckButton(
                 _('"A Guide to Remembering Japanese Characters" '
                   'by Kenneth G. Henshall'))))
        self.dict_buttons.append(
            ("kdict.render.dcode.gakken",
             gtk.CheckButton(
                 _('Gakken Kanji Dictionary '
                   '("A New Dictionary of Kanji Usage")'))))
        self.dict_buttons.append(
            ("kdict.render.dcode.heisig",
             gtk.CheckButton(
                 _('"Remembering The Kanji" by James Heisig'))))
        self.dict_buttons.append(
            ("kdict.render.dcode.oneill_names",
             gtk.CheckButton(
                 _('"Japanese Names" by P.G. O\'Neill'))))
        self.dict_buttons.append(
            ("kdict.render.dcode.maniette",
             gtk.CheckButton(
                 _("Codes from Yves Maniette's French version of Heisig"))))

        main_opts = gtk.VBox()
        dicts_outer = gtk.VBox()
        other_opts = gtk.VBox()

        main_opts.pack_start(self.chkReadings, expand = False)
        main_opts.pack_start(self.chkMeanings, expand = False)
        main_opts.pack_start(self.chkHighImp, expand = False)
        main_opts.pack_start(self.chkMultiRad, expand = False)

        self.dicts_inner = gtk.VBox()
        for key, obj in self.dict_buttons:
            self.dicts_inner.pack_start(obj, expand = False)
        self.dicts_inner.set_sensitive(False)

        dicts_scrollwindow = gtk.ScrolledWindow()
        dicts_scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                      gtk.POLICY_AUTOMATIC)
        # GTKmm ScrolledWindow worked with just an add;
        # pyGTK required add_with_viewport... why the diff?
        dicts_scrollwindow.add_with_viewport(self.dicts_inner)

        dicts_outer.pack_start(self.chkDict, expand = False)
        dicts_outer.pack_start(dicts_scrollwindow)

        other_opts.pack_start(self.chkVocabCrossRef, expand = False)
        other_opts.pack_start(self.chkLowImp, expand = False)
        other_opts.pack_start(self.chkSodStatic, expand = False)
        other_opts.pack_start(self.chkSodAnim, expand = False)

        self.pack_start(main_opts, expand = False)
        self.pack_start(dicts_outer)
        self.pack_start(other_opts, expand = False)

        self.chkDict.connect("toggled", self.on_dictionary_toggle)

        self.update_gui()

    def on_dictionary_toggle(self, widget):
        self.dicts_inner.set_sensitive(widget.get_active())

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
