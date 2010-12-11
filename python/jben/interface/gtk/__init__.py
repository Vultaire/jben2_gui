# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pygtk
pygtk.require("2.0")
import gtk, gobject
import os

from .window.main import Main as WindowMain
from jben import configure


class Interface(object):

    """GTK interface class."""

    def __init__(self, app):
        self.app = app
        self._setup_global_icons()

    def _setup_global_icons(self):
        # Assume working directory is just before "images"...
        data_dir = configure.get_datadir()
        img_dir = os.path.join(data_dir, "images")
        fnames = [
            os.path.join(img_dir, fname) for fname in
            ("jben.xpm", "jben_48.xpm", "jben_32.xpm", "jben_16.xpm")]
        icons = [
            gtk.gdk.pixbuf_new_from_file(fname)
            for fname in fnames
            ]
        gtk.window_set_default_icon_list(*icons)

    def run(self):
        gobject.threads_init()  # Must occur before any GUI stuff, it seems
        jben_win = WindowMain(self.app)
        jben_win.set_sensitive(False)
        jben_win.show_all()
        gtk.main()
