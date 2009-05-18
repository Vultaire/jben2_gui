#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: tab_prefsfonts.py
# Author: Paul Goins
# Created on: 28 Nov 2008

import gtk

class TabPrefsFonts(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self, spacing = 5)

        # We're loading 4 rows of GUI controls, all following the same
        # order: 0 = Japanese Normal, 1 = Japanese Large,
        # 2 = English Normal, 3 = English Small.

        labels = []
        labels.append(gtk.Label(_("Japanese Font, Normal")))
        labels.append(gtk.Label(_("Japanese Font, Large")))
        labels.append(gtk.Label(_("English Font, Normal")))
        labels.append(gtk.Label(_("English Font, Small")))
        for l in labels:
            l.set_alignment(1.0, 0.5)

        self.JaNormalDisp = gtk.TextView()
        self.JaLargeDisp  = gtk.TextView()
        self.EnNormalDisp = gtk.TextView()
        self.EnSmallDisp  = gtk.TextView()
        displays = []
        displays.append(self.JaNormalDisp)
        displays.append(self.JaLargeDisp)
        displays.append(self.EnNormalDisp)
        displays.append(self.EnSmallDisp)
        for d in displays:
            d.set_accepts_tab(False)
            d.set_editable(False)
        frames = []
        for i in range(4):
            frames.append(gtk.Frame())
            frames[i].add(displays[i])
            frames[i].set_shadow_type(gtk.SHADOW_IN)

        self.btnJaNormal = gtk.Button(_("Change..."))
        self.btnJaLarge  = gtk.Button(_("Change..."))
        self.btnEnNormal = gtk.Button(_("Change..."))
        self.btnEnSmall  = gtk.Button(_("Change..."))
        buttons = []
        buttons.append(self.btnJaNormal)
        buttons.append(self.btnJaLarge)
        buttons.append(self.btnEnNormal)
        buttons.append(self.btnEnSmall)
        for b in buttons:
            b.connect("clicked", self.on_font_change)
        bboxes = []
        for i in range(4):
            bboxes.append(gtk.HButtonBox())
            bboxes[i].pack_start(buttons[i])

        table = gtk.Table(4, 3)
        for i in range(4):
            table.attach(labels[i], 0, 1, i, i + 1,
                         gtk.FILL, gtk.SHRINK, 5, 5)
            table.attach(frames[i], 1, 2, i, i + 1,
                         gtk.FILL | gtk.EXPAND, gtk.SHRINK, 5, 5)
            table.attach(bboxes[i], 2, 3, i, i + 1,
                         gtk.SHRINK, gtk.SHRINK, 5, 5)

        self.pack_start(table, expand = False);

    def on_font_change(self, widget):
        print("TabPrefsFonts.on_font_change")

    def update_prefs(self):
        pass

#	/* Init font display */
#	sFontJaNormal = prefs->GetSetting("font.ja");
#	sFontJaLarge  = prefs->GetSetting("font.ja.large");
#	sFontEnNormal = prefs->GetSetting("font.en");
#	sFontEnSmall  = prefs->GetSetting("font.en.small");
#	UpdateFontControl(tvJaNormal, sFontJaNormal);
#	UpdateFontControl(tvJaLarge,  sFontJaLarge);
#	UpdateFontControl(tvEnNormal, sFontEnNormal);
#	UpdateFontControl(tvEnSmall,  sFontEnSmall);
