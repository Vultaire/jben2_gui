# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pygtk
pygtk.require("2.0")
import gtk
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
        icons = [gtk.gdk.pixbuf_new_from_file(
                os.path.join(mod_path, "..", "..", "images", f))
                 for f in files]
        gtk.window_set_default_icon_list(*icons)

    def run(self):
        jben_win = WindowMain()
        jben_win.set_sensitive(False)
        jben_win.show_all()

        wdict_avial, kdict_avail = self.app.check_dicts()
        if not all(wdict_avail, kdict_avail):
            # Schedule dictionary check and enabling of main window
            # sometime after gtk.main starts...
            # *** TO DO ***
            pass

        # Main loop
        gtk.main()
