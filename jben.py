#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: jben.py
# Author: Paul Goins
# Created on: 20 Nov 2008

import gettext
gettext.install("jben")

import pygtk
pygtk.require("2.0")
import gtk

from window_main import WindowMain
import preferences

from jben_global import *

def setup_global_icons():
    icon1 = gtk.gdk.pixbuf_new_from_file("jben.xpm")
    icon2 = gtk.gdk.pixbuf_new_from_file("jben_48.xpm")
    icon3 = gtk.gdk.pixbuf_new_from_file("jben_32.xpm")
    icon4 = gtk.gdk.pixbuf_new_from_file("jben_16.xpm")
    gtk.window_set_default_icon_list(icon1, icon2, icon3, icon4)

class JBen:
    """Base class for J-Ben application."""

    def __init__(self):
        setup_global_icons()

        jben_win = WindowMain()
        jben_win.show_all()

    def main(self):
        preferences.set_default_prefs()
        if preferences.load():
            # Only does something if a config file is out of date.
            preferences.upgrade_config_file()

        gtk.main()

        preferences.save()

if __name__ == "__main__":
    gui = JBen()
    gui.main()
