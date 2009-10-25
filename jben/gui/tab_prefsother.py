#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: tab_prefsother.py
# Author: Paul Goins
# Created on: 28 Nov 2008

from __future__ import absolute_import

import gtk
import os

from jben.preferences import options


class TabPrefsOther(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self, spacing = 5)


        # Not sure what the os.name is under windows; the below is temporary.
        if os.name == "nt":
            # Windows only: "mobile mode"
            self.chkMobile = gtk.CheckButton(
                _("Mobile mode (settings saved to current directory)"))
            self.chkMobile.set_active(
                str(options.get("config_save_target")) == "mobile")
            self.chkMobile.connect("toggled", self.on_mobile_toggle)
            self.pack_start(self.chkMobile, expand = False)

    def on_mobile_toggle(self, widget):
        print("TabPrefsOther.on_mobile_toggle")

    def update_prefs(self):
        if self.chkMobile.get_active(): s = "mobile"
        else: s = "home"
        options["config_save_target"] = s
