# -*- coding: utf-8 -*-

from __future__ import absolute_import

import gtk, gobject
from ..widget.storedsize import StoredSizeDialog
from jben.dict_downloader import static_mirror_list


class DictMirrorSelect(StoredSizeDialog):

    def __init__(self, app, parent):
        StoredSizeDialog.__init__(
            self, "gui.dialog.dict_mirror_select.size", -1, -1,
            title=_("Select download site"),
            parent=parent,
            flags=gtk.DIALOG_MODAL,
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                     gtk.STOCK_OK, gtk.RESPONSE_OK)
            )
        self.app = app
        self._layout()

    def _layout(self):
        self.server_list = gtk.combo_box_new_text()
        for row in static_mirror_list:
            self.server_list.append_text(row)
        self.server_list.set_active(0)
        self.server_list.show()

        layout = self.get_content_area()
        layout.pack_start(self.server_list, expand=False)

    def get_mirror(self):
        return self.server_list.get_active_text()

    def run(self):
        """Single-time run command; hides GTK boilerplate and gets result.

        Returns the selected mirror's URI.

        """
        resp = gtk.Dialog.run(self)
        if resp == gtk.RESPONSE_OK:
            result = self.get_mirror()
        else:
            result = None
        self.destroy()
        return result
