# -*- coding: utf-8 -*-
"""Dialog for adding kanji by newspaper frequency."""

from __future__ import absolute_import

import gtk
from ..widget.infomessage import show_message


class AddKanjiByFreqDialog(gtk.Dialog):

    def __init__(self, parent):
        gtk.Dialog.__init__(
            self, _("Add Kanji By Newspaper Frequency"), parent),

        buttons = []
        for i in xrange(2):
            # Basically, SpinButtons seem to be intended for use with
            # gtk.Adjustments.  If not, then a lot of code is required
            # afterward to make the buttons work even to a minimal
            # level.
            #
            # Because of this...  we'll play things PyGTK's way.
            adj = gtk.Adjustment(1, 1, 2501, 1, 100)
            button = gtk.SpinButton(adj)
            button.set_numeric(True)
            buttons.append(button)
        self.low_rank, self.high_rank = buttons

        low_label = gtk.Label(_("From:"))
        high_label = gtk.Label(_("To:"))

        tbl = gtk.Table(2, 2)

        for i, label in enumerate((low_label, high_label)):
            align = gtk.Alignment(xalign=1.0, yalign=0.5)
            align.add(label)
            tbl.attach(align, 0, 1, i, i+1, xpadding=5, ypadding=5)
        for i, combo in enumerate((self.low_rank, self.high_rank)):
            tbl.attach(combo, 1, 2, i, i+1, xpadding=5, ypadding=5)

        self.vbox.set_spacing(5)
        self.vbox.pack_start(tbl)
        self.vbox.show_all()

        buttons=[
            (gtk.STOCK_CANCEL, self.on_cancel_clicked),
            (gtk.STOCK_OK, self.on_ok_clicked),
            ]

        for stock_code, handler in buttons:
            button = gtk.Button(stock=stock_code)
            button.connect("clicked", handler)
            self.action_area.pack_start(button)

        self.action_area.show_all()

    def on_cancel_clicked(self, widget):
        self.response(gtk.RESPONSE_CANCEL)

    def on_ok_clicked(self, widget):
        freq_min, freq_max = self.get_freq_range()

        if freq_min <= freq_max:
            self.response(gtk.RESPONSE_OK)
        else:
            show_message(
                self, _(u"Invalid range selected"),
                _(u"The upper rank cannot be lower than the lower rank."))

    def get_freq_range(self):
        freq_min = self.low_rank.get_value_as_int()
        freq_max = self.high_rank.get_value_as_int()
        return (freq_min, freq_max)
