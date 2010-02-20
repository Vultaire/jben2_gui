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
        wframe = gtk.Frame(_("Word dictionaries"))
        cframe = gtk.Frame(_("Character dictionaries"))
        edict_btn = gtk.RadioButton(group=None,
                                    label=_("EDICT (Recommended)"))
        kanjidic_btn = gtk.RadioButton(group=None,
                                       label=_("KANJIDIC (Recommended)"))
        kanjidic2_btn = gtk.RadioButton(group=kanjidic_btn,
                                        label=_("KANJIDIC 2"))
        edict_btn.set_active(True)
        kanjidic_btn.set_active(True)
        d = {wframe: [edict_btn],
             cframe: [kanjidic_btn, kanjidic2_btn]}
        for frame in d:
            box = gtk.VBox(spacing=5)
            for obj in d[frame]:
                box.pack_start(obj, expand=False)
            frame.add(box)
        hbox = gtk.HBox(spacing=5)
        for obj in (wframe, cframe):
            hbox.pack_start(obj)
        hbox.show_all()
        layout = self.get_content_area()
        for obj in (self.server_list, hbox):
            layout.pack_start(obj, expand=False)

    def get_mirror(self):
        return self.server_list.get_active_text()

    def run(self):
        """Single-time run command; hides GTK boilerplate and gets result."""
        result = None
        resp = gtk.Dialog.run(self)
        if resp == gtk.RESPONSE_OK:
            result = self.get_mirror()
        self.destroy()
        return result
