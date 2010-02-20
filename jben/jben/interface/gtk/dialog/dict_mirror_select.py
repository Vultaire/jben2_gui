# -*- coding: utf-8 -*-

from __future__ import absolute_import

import gtk, gobject
from ..widget.storedsize import StoredSizeDialog
from jben.dict_downloader import static_mirror_list


class MirrorSelect(StoredSizeDialog):

    def __init__(self, parent):
        StoredSizeDialog.__init__(
            self, "gui.dialog.dict_mirror_select.size", -1, -1,
            title=_("Select download site"),
            parent=parent,
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                     gtk.STOCK_OK, gtk.RESPONSE_OK)
            )
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

    def on_cancel(self, widget):
        self.response(None)
