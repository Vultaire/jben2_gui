# -*- coding: utf-8 -*-

from __future__ import absolute_import

import gtk, gobject
from ..widget.storedsize import StoredSizeDialog
from jben.download_thread import DownloadThread


class DictDownload(StoredSizeDialog):

    """Downloads dictionaries from a specified mirror."""

    def __init__(self, parent, mirror, files):
        StoredSizeDialog.__init__(
            self, "gui.dialog.dict_download.size", -1, -1,
            title=_("Download dictionaries"),
            parent=parent,
            flags=gtk.DIALOG_MODAL
            )
        self._layout()
        self.connect("show", self.on_show)
        self.urls = ["/".join((mirror, f)) for f in files]

    def on_show(self, widget):
        # *** TODO TO DO TODO ***
        # Temporarily: just finish
        self.on_finished()

    def on_finished(self):
        # After everything's finished...
        self.ok_btn.set_sensitive(True)

    def _layout(self):
        self.ok_btn = self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.ok_btn.set_sensitive(False)

    def run(self):
        """Single-time run command; hides GTK boilerplate."""
        gtk.Dialog.run(self)
        self.destroy()
