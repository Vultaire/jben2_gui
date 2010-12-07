# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pygtk
pygtk.require("2.0")
import gtk, gobject
import os

from .window.main import Main as WindowMain


class Interface(object):

    """GTK interface class."""

    def __init__(self, app):
        self.app = app
        self._setup_global_icons()

    def _setup_global_icons(self):
        files = ["jben.xpm", "jben_48.xpm", "jben_32.xpm", "jben_16.xpm"]
        mod_path = os.path.dirname(__file__)
        icons = [
            gtk.gdk.pixbuf_new_from_file(
                os.path.join(mod_path, "..", "..", "images", f))
            for f in files
            ]
        gtk.window_set_default_icon_list(*icons)

    def run(self):
        gobject.threads_init()  # Must occur before any GUI stuff, it seems
        jben_win = WindowMain(self.app)
        jben_win.set_sensitive(False)
        jben_win.show_all()
        gtk.main()
