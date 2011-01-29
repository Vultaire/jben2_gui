# -*- coding: utf-8 -*-
"""Dialog for adding kanji by Jouyou grade level."""

from __future__ import absolute_import

import gtk
from ..widget.storedsize import StoredSizeDialog


class AddKanjiByJouyouDialog(StoredSizeDialog):

    def __init__(self, parent):
        StoredSizeDialog.__init__(
            self, "gui.addkanjibyjouyou.size", -1, -1,
            _("Add Kanji By Jouyou Grade"), parent)

        #self.vbox.set_spacing(5)
        #self.vbox.pack_start(main_box)
        #self.vbox.show_all()

        ########################################

        ok_button = gtk.Button(stock=gtk.STOCK_OK)
        cancel_button = gtk.Button(stock=gtk.STOCK_CANCEL)

        ok_button.connect("clicked", self.on_ok_clicked)
        cancel_button.connect("clicked", self.on_cancel_clicked)

        for button in cancel_button, ok_button:
            self.action_area.pack_start(button)
        self.action_area.show_all()

        self.set_has_separator(False)

    def on_cancel_clicked(self, widget):
        self.response(gtk.RESPONSE_CANCEL)

    def on_ok_clicked(self, widget):
        #self.apply()
        self.response(gtk.RESPONSE_OK)
