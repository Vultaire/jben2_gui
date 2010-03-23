# -*- coding: utf-8 -*-

from __future__ import absolute_import

import gtk, gobject
from ..widget.storedsize import StoredSizeDialog
from jben.dict_downloader import static_mirror_list


class DictDownloadSelect(StoredSizeDialog):

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
        wframe = gtk.Frame(_("Word dictionaries"))
        cframe = gtk.Frame(_("Character dictionaries"))
        self.edict_btn = gtk.RadioButton(
            group=None, label=_("EDICT (Recommended)"))
        self.kanjidic_btn = gtk.RadioButton(
            group=None, label=_("KANJIDIC (Recommended)"))
        self.kanjidic2_btn = gtk.RadioButton(
            group=self.kanjidic_btn, label=_("KANJIDIC 2"))
        self.edict_btn.set_active(True)
        self.kanjidic_btn.set_active(True)
        d = {wframe: [self.edict_btn],
             cframe: [self.kanjidic_btn, self.kanjidic2_btn]}
        for frame in d:
            box = gtk.VBox(spacing=5)
            for obj in d[frame]:
                box.pack_start(obj, expand=False)
            frame.add(box)
        dictbox = gtk.HBox(spacing=5)
        for obj in (wframe, cframe):
            dictbox.pack_start(obj)
        dictbox.show_all()
        layout = self.get_content_area()
        for obj in (self.server_list, dictbox):
            layout.pack_start(obj, expand=False)

    def get_mirror(self):
        return self.server_list.get_active_text()

    def get_dl_files(self):
        files = []
        d = {
            self.edict_btn: "edict.gz",
            self.kanjidic_btn: "kanjidic.gz",
            self.kanjidic2_btn: "kanjidic2.xml.gz",
            }
        for btn in d:
            if btn.get_active():
                files.append(d[btn])
        return files

    def run(self):
        """Single-time run command; hides GTK boilerplate and gets result.

        Returns two items: a mirror, and a list of dictionaries to download.

        """
        result = (None, None)
        resp = gtk.Dialog.run(self)
        if resp == gtk.RESPONSE_OK:
            result = (self.get_mirror(), self.get_dl_files())
        self.destroy()
        return result
