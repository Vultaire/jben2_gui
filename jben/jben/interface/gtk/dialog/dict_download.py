# -*- coding: utf-8 -*-

from __future__ import absolute_import

import gtk
from ..widget.storedsize import StoredSizeDialog


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

    def on_show(self, widget):
        # *** TODO TO DO TODO ***

        # After everything's finished...
        self.ok_btn.set_sensitive(True)

    def _layout(self):
        self.ok_btn = self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.ok_btn.set_sensitive(False)

    def run(self):
        """Single-time run command; hides GTK boilerplate."""
        gtk.Dialog.run(self)
        self.destroy()
