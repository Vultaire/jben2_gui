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
            flags=gtk.DIALOG_MODAL,
            buttons=(gtk.STOCK_OK, gtk.RESPONSE_OK)
            )
        self._layout()

    def _layout(self):
        pass

    def run(self):
        """Single-time run command; hides GTK boilerplate."""
        gtk.Dialog.run(self)
        self.destroy()
