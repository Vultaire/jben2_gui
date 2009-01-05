#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: tab_prefskanjidict.py
# Author: Paul Goins
# Created on: 28 Nov 2008

import gtk

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

        self.dict_buttons = []
        self.dict_buttons.append(gtk.CheckButton(
                _('"New Japanese-English Character Dictionary" '
                  'by Jack Halpern.')))
        self.dict_buttons.append(gtk.CheckButton(
                _('"Modern Reader\'s Japanese-English Character Dictionary" '
                  'by Andrew Nelson')))
        self.dict_buttons.append(gtk.CheckButton(
                _('"The New Nelson Japanese-English Character Dictionary" '
                  'by John Haig')))
        self.dict_buttons.append(gtk.CheckButton(
                _('"Japanese for Busy People" by AJLT')))
        self.dict_buttons.append(gtk.CheckButton(
                _('"The Kanji Way to Japanese Language Power" '
                  'by Dale Crowley')))
        self.dict_buttons.append(gtk.CheckButton(
                _('"Kodansha Compact Kanji Guide"')))
        self.dict_buttons.append(gtk.CheckButton(
                _('"A Guide To Reading and Writing Japanese" '
                  'by Ken Hensall et al.')))
        self.dict_buttons.append(gtk.CheckButton(
                _('"Kanji in Context" by Nishiguchi and Kono')))
        self.dict_buttons.append(gtk.CheckButton(
                _('"Kanji Learner\'s Dictionary" by Jack Halpern')))
        self.dict_buttons.append(gtk.CheckButton(
                _('"Essential Kanji" by P.G. O\'Neill')))
        self.dict_buttons.append(gtk.CheckButton(
                _('"2001 Kanji" by Father Joseph De Roo')))
        self.dict_buttons.append(gtk.CheckButton(
                _('"A Guide To Reading and Writing Japanese" '
                  'by Florence Sakade')))
        self.dict_buttons.append(gtk.CheckButton(
                _('"Tuttle Kanji Cards" by Alexander Kask')))
        self.dict_buttons.append(gtk.CheckButton(
                _('"Japanese Kanji Flashcards" by White Rabbit Press')))
        self.dict_buttons.append(gtk.CheckButton(
                _('SKIP codes used by Halpern dictionaries')))
        self.dict_buttons.append(gtk.CheckButton(
                _('"Kanji Dictionary" by Spahn & Hadamitzky')))
        self.dict_buttons.append(gtk.CheckButton(
                _('"Kanji & Kana" by Spahn & Hadamitzky')))
        self.dict_buttons.append(gtk.CheckButton(
                _('Four Corner code (various dictionaries)')))
        self.dict_buttons.append(gtk.CheckButton(
                _('"Morohashi Daikanwajiten"')))
        self.dict_buttons.append(gtk.CheckButton(
                _('"A Guide to Remembering Japanese Characters" '
                  'by Kenneth G. Henshal')))
        self.dict_buttons.append(gtk.CheckButton(
                _('Gakken Kanji Dictionary '
                  '("A New Dictionary of Kanji Usage")')))
        self.dict_buttons.append(gtk.CheckButton(
                _('"Remembering The Kanji" by James Heisig')))
        self.dict_buttons.append(gtk.CheckButton(
                _('"Japanese Names" by P.G. O\'Neill')))

        main_opts = gtk.VBox()
        dicts_outer = gtk.VBox()
        other_opts = gtk.VBox()

        main_opts.pack_start(self.chkReadings, expand = False)
        main_opts.pack_start(self.chkMeanings, expand = False)
        main_opts.pack_start(self.chkHighImp, expand = False)
        main_opts.pack_start(self.chkMultiRad, expand = False)

        self.dicts_inner = gtk.VBox()
        for obj in self.dict_buttons:
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

    def on_dictionary_toggle(self, widget):
        self.dicts_inner.set_sensitive(widget.get_active())
