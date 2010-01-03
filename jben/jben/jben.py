#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: jben.py
# Author: Paul Goins
# Created on: 20 Nov 2008

"""J-Ben main module."""

from __future__ import absolute_import

import gettext
gettext.install("jben")

import pygtk
pygtk.require("2.0")
import gtk

from jben.gui.window.main import WindowMain
from jben.preferences import Preferences
from jben.dict import DictManager
from jben import global_refs

from os import path

class JBen(object):

    """Base class for J-Ben application."""

    def __init__(self):
        # Init globals
        global_refs.prefs = Preferences()
        global_refs.dictmgr = DictManager()
        # Init app object vars
        self.setup_global_icons()

    def setup_global_icons(self):
        files = ["jben.xpm", "jben_48.xpm", "jben_32.xpm", "jben_16.xpm"]
        mod_path = path.dirname(__file__)
        icons = [gtk.gdk.pixbuf_new_from_file(
                path.join(mod_path, "images", f))
                 for f in files]
        gtk.window_set_default_icon_list(*icons)

    def main(self):
        jben_win = WindowMain()
        jben_win.show_all()
        gtk.main()
        global_refs.prefs.save()

if __name__ == "__main__":
    app = JBen()
    app.main()
